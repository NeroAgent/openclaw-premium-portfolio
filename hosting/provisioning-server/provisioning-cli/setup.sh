#!/bin/bash
set -e

echo "🚀 OpenClaw Agent Provisioning"
echo "=============================="

AGENT_ID="${AGENT_ID:-agent-$(head /dev/urandom | tr -dc a-z0-9 | head -c8)}"
INSTALL_DIR="/opt/openclaw"
OPENCLAW_REPO="https://github.com/openclaw/openclaw.git"

echo "📦 Installing packages..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git curl wget sudo docker.io docker-compose > /dev/null

echo "🐳 Starting Docker..."
systemctl start docker
systemctl enable docker

echo "👤 Creating openclaw user..."
if ! id -u openclaw >/dev/null 2>&1; then
  useradd -r -s /bin/bash -m -d "$INSTALL_DIR" openclaw
fi

echo "📥 Cloning OpenClaw..."
if [ ! -d "$INSTALL_DIR/.git" ]; then
  git clone "$OPENCLAW_REPO" "$INSTALL_DIR"
fi

echo "⚙️  Writing config..."
mkdir -p "$INSTALL_DIR/config"
cat > "$INSTALL_DIR/config/agent.json" <<JSON
{
  "agentId": "$AGENT_ID",
  "gateway": { "bind": "0.0.0.0", "port": 8080 },
  "node": { "host": "localhost", "port": 8080 },
  "telemetry": { "enabled": false },
  "skills": { "dir": "$INSTALL_DIR/skills" },
  "memory": { "dir": "$INSTALL_DIR/workspace/memory" }
}
JSON

echo "📝 Writing docker-compose.yml..."
cat > "$INSTALL_DIR/docker-compose.yml" <<'YAML'
version: '3.8'
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    container_name: openclaw-agent
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - /opt/openclaw/workspace:/workspace
      - /opt/openclaw/config:/config
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - NODE_ENV=production
      - AGENT_ID=AGENT_ID_PLACEHOLDER
    command: ["node", "/app/dist/cli.js", "start", "--config", "/config/agent.json"]
YAML

sed -i "s/AGENT_ID_PLACEHOLDER/$AGENT_ID/" "$INSTALL_DIR/docker-compose.yml"

echo "🔐 Setting permissions..."
chown -R openclaw:openclaw "$INSTALL_DIR"

echo "▶️  Starting agent..."
docker compose -f "$INSTALL_DIR/docker-compose.yml" up -d

echo "⏳ Waiting for agent..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "UNKNOWN_IP")
for i in {1..30}; do
  if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo ""
    echo "✅ Agent running!"
    echo "📡 Dashboard: http://$PUBLIC_IP:8080"
    echo "🆔 Agent ID: $AGENT_ID"
    break
  fi
  echo -n "."
  sleep 2
done

echo ""
echo "📋 Next:"
echo "1. Configure gateway in OpenClaw client: ws://$PUBLIC_IP:8080"
echo "2. Install premium skills via clawhub"
echo "3. Set up Telegram/Signal bridge if needed"
