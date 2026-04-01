#!/usr/bin/env node
/**
 * OpenClaw Provisioning CLI
 * Runs on the target VPS to install and configure the agent
 *
 * Usage: curl https://myprovisioningserver.com/setup | node
 * Or: node setup.js <token>
 */

import { execSync } from 'child_process';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';
import { https } from 'http';

const AGENT_ID = process.env.AGENT_ID || `agent-${Math.random().toString(36).substring(7)}`;
const OPENCLAW_REPO = 'https://github.com/openclaw/openclaw.git';
const INSTALL_DIR = '/opt/openclaw';

function run(cmd) {
  try {
    execSync(cmd, { stdio: 'inherit' });
  } catch (e) {
    console.error(`❌ Failed: ${cmd}`);
    throw e;
  }
}

function main() {
  console.log('🚀 Starting OpenClaw agent provisioning...\n');

  // 1. Install dependencies (Ubuntu/Debian)
  console.log('📦 Installing system packages...');
  run('apt-get update -qq');
  run('apt-get install -y -qq git curl wget sudo docker.io docker-compose > /dev/null');

  // 2. Start Docker
  console.log('🐳 Starting Docker...');
  run('systemctl start docker');
  run('systemctl enable docker');

  // 3. Create openclaw user
  console.log('👤 Creating openclaw user...');
  try {
    run('useradd -r -s /bin/bash -m -d /opt/openclaw openclaw');
  } catch (e) {
    // user might exist
  }

  // 4. Clone OpenClaw repo
  console.log('📥 Cloning OpenClaw...');
  if (!existsSync(INSTALL_DIR)) {
    run(`git clone ${OPENCLAW_REPO} ${INSTALL_DIR}`);
  }

  // 5. Generate config
  console.log('⚙️  Generating configuration...');
  const config = {
    agentId: AGENT_ID,
    gateway: {
      bind: '0.0.0.0',
      port: 8080
    },
    node: {
      host: 'localhost',
      port: 8080
    },
    telemetry: {
      enabled: false
    },
    skills: {
      dir: join(INSTALL_DIR, 'skills')
    },
    memory: {
      dir: join(INSTALL_DIR, 'workspace', 'memory')
    }
  };
  const configPath = join(INSTALL_DIR, 'config', 'agent.json');
  mkdirSync(join(INSTALL_DIR, 'config'), { recursive: true });
  writeFileSync(configPath, JSON.stringify(config, null, 2));

  // 6. Create docker-compose.yml
  console.log('📝 Writing docker-compose.yml...');
  const compose = `
version: '3.8'
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    container_name: openclaw-agent
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ${INSTALL_DIR}/workspace:/workspace
      - ${INSTALL_DIR}/config:/config
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - NODE_ENV=production
      - AGENT_ID=${AGENT_ID}
    command: ["node", "/app/dist/cli.js", "start", "--config", "/config/agent.json"]
`;
  writeFileSync(join(INSTALL_DIR, 'docker-compose.yml'), compose.trim());

  // 7. Permissions
  console.log('🔐 Setting permissions...');
  run(`chown -R openclaw:openclaw ${INSTALL_DIR}`);

  // 8. Start agent
  console.log('▶️  Starting OpenClaw agent...');
  execSync('docker compose -f /opt/openclaw/docker-compose.yml up -d', { stdio: 'inherit' });

  // 9. Wait for health
  console.log('⏳ Waiting for agent to become healthy...');
  for (let i = 0; i < 30; i++) {
    try {
      const resp = https.get('http://localhost:8080/health', (res) => {
        if (res.statusCode === 200) {
          console.log('\n✅ Agent is running!');
          console.log(`📡 Dashboard: http://${getPublicIP()}:8080`);
          console.log(`🆔 Agent ID: ${AGENT_ID}`);
          return;
        }
      });
    } catch (e) {}
    console.log('.');
    execSync('sleep 2');
  }
  console.log('\n⚠️  Agent may not be healthy yet. Check logs: docker logs openclaw-agent');

  // 10. Print info
  console.log('\n📋 Next steps:');
  console.log('- Configure gateway URL in your OpenClaw client');
  console.log('- Install premium skills via clawhub');
  console.log('- Set up Telegram/Signal bridge if desired\n');
}

function getPublicIP() {
  try {
    // Try to get public IP from metadata service (Hetzner, DigitalOcean, etc.)
    const resp = https.get('http://169.254.169.254/latest/meta-data/public-ipv4', (r) => {
      let data = '';
      r.on('data', d => data += d);
      r.on('end', () => console.log(data));
    });
  } catch (e) {
    return 'YOUR_VPS_IP';
  }
}

main();
