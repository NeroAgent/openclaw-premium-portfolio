/**
 * Provisioning Server — handles Stripe webhooks and serves setup scripts
 * Run with: node server.js
 */

import express from 'express';
import { readFileSync } from 'fs';
import { join } from 'path';
import crypto from 'crypto';

const app = express();
app.use(express.json());

// In-memory store for pilot (use DB in prod)
const customers = new Map();

const STRIPE_SECRET = process.env.STRIPE_SECRET;
const HETZNER_API_TOKEN = process.env.HETZNER_API_TOKEN;

async function createVPS(tier, agentId) {
  const serverTypes = {
    basic: { name: 'cx11', cpu: 1, memory: 1, disk: 20 },
    pro: { name: 'cx21', cpu: 1, memory: 2, disk: 40 },
    team: { name: 'cx31', cpu: 2, memory: 4, disk: 60 }
  };
  const st = serverTypes[tier] || serverTypes.basic;

  if (!HETZNER_API_TOKEN) {
    return {
      id: 'vps-mock-' + crypto.randomBytes(4).toString('hex'),
      ip: '127.0.0.1',
      user: 'root',
      password: 'changeme'
    };
  }

  const payload = JSON.stringify({
    name: `openclaw-${agentId.slice(0, 10)}`,
    server_type: { name: st.name },
    image: { name: 'ubuntu-22.04' },
    networks: { ipv4: true, ipv6: false },
    location: { name: 'nbg1' }
  });

  const https = await import('https');
  const options = {
    hostname: 'api.hetzner.cloud',
    port: 443,
    path: '/v1/servers',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${HETZNER_API_TOKEN}`,
      'Content-Length': payload.length
    }
  };

  const resp = await new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });

  if (resp.statusCode !== 202) {
    throw new Error(`Hetzner error ${resp.statusCode}: ${resp.body}`);
  }

  const server = JSON.parse(resp.body);
  return {
    id: server.server.id,
    ip: server.server.public_net.ipv4.ip,
    user: 'root',
    password: server.server.root_password
  };
}

// Stripe webhook
app.post('/webhook/stripe', async (req, res) => {
  const event = req.body;
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const email = session.customer_email;
    const tier = session.metadata.tier;
    const agentId = 'agent-' + crypto.randomBytes(4).toString('hex');

    try {
      const vps = await createVPS(tier, agentId);
      customers.set(email, { agentId, vpsId: vps.id, status: 'provisioning', tier, ip: vps.ip });

      console.log(`📧 Provisioning for ${email}: Agent ${agentId}, IP ${vps.ip}`);
      const baseUrl = process.env.PROVISIONING_BASE_URL || 'http://localhost:3000';
      const setupUrl = `${baseUrl}/setup?agent_id=${agentId}&vps_ip=${vps.ip}`;
      console.log(`   Setup URL: ${setupUrl}`);

      // TODO: send email with credentials
      res.json({ ok: true, agentId, setupUrl });
    } catch (err) {
      console.error('❌ Provisioning failed:', err);
      res.status(500).json({ error: 'provisioning_failed', message: err.message });
    }
  } else {
    res.json({ ok: true });
  }
});

app.get('/setup', (req, res) => {
  const { agent_id } = req.query;
  if (!agent_id) {
    return res.status(400).send('Missing agent_id');
  }

  const scriptPath = join(process.cwd(), 'provisioning-cli', 'setup.sh');
  let script = readFileSync(scriptPath, 'utf8');
  script = script.replace(/AGENT_ID=".*?"/, `AGENT_ID="${agent_id}"`);

  res.set('Content-Type', 'text/plain');
  res.set('Content-Disposition', 'attachment; filename="setup.sh"');
  res.send(script);
});

app.get('/admin/customers', (req, res) => {
  const list = [];
  for (const [email, data] of customers) {
    list.push({ email, ...data });
  }
  res.json(list);
});

app.get('/health', (req, res) => res.send('OK'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Provisioning server listening on ${PORT}`));
