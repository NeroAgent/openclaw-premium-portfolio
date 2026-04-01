#!/usr/bin/env node
/**
 * Test the provisioning flow end-to-end (without Stripe)
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Simulate what the webhook does
async function simulateWebhook() {
  const email = 'test@example.com';
  const tier = 'basic';
  const agentId = 'agent-test123';
  
  // Mock VPS creation
  const vps = {
    id: 'vps-' + Math.random().toString(36).substring(7),
    ip: '1.2.3.4',
    user: 'root',
    password: 'changeme'
  };
  
  console.log(`📧 Provisioning for ${email}:`);
  console.log(`   Agent ID: ${agentId}`);
  console.log(`   VPS IP: ${vps.ip}`);
  
  // Generate setup URL
  const baseUrl = 'http://localhost:3000';
  const setupUrl = `${baseUrl}/setup?agent_id=${agentId}&vps_ip=${vps.ip}`;
  console.log(`   Setup URL: ${setupUrl}`);
  
  // Fetch setup script
  const https = await import('https');
  https.get(setupUrl, (resp) => {
    let data = '';
    resp.on('data', chunk => data += chunk);
    resp.on('end', () => {
      console.log('\n📥 Setup script (first 20 lines):');
      console.log(data.split('\n').slice(0, 20).join('\n'));
      console.log('\n✅ Test complete. In real flow:');
      console.log('1. Email above credentials + setup URL to customer');
      console.log('2. Customer runs: curl -sL "setupUrl" | bash');
      console.log('3. Agent starts on VPS at ws://IP:8080');
    });
  }).on('error', (e) => {
    console.error('❌ Error fetching setup script:', e.message);
  });
}

simulateWebhook();
