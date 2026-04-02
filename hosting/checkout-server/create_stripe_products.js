#!/usr/bin/env node
/**
 * Create Stripe products and prices for OpenClaw catalog
 * Run: STRIPE_SECRET=sk_live_... node create_stripe_products.js
 */

import Stripe from 'stripe';
import 'dotenv/config';

const stripe = new Stripe(process.env.STRIPE_SECRET!, {
  apiVersion: '2025-04-30.basil'
});

const products = [
  // Hosting tiers (subscriptions)
  { name: 'OpenClaw Hosted Basic', price: 19, interval: 'month', description: 'Fully managed AI agent hosting — 1 vCPU, 1GB RAM, 25GB SSD' },
  { name: 'OpenClaw Hosted Pro', price: 39, interval: 'month', description: '2 vCPU, 2GB RAM, 50GB SSD + Proactive Ops Monitor + ToolRouter' },
  { name: 'OpenClaw Hosted Team', price: 99, interval: 'month', description: '4 vCPU, 4GB RAM, 100GB SSD + multi-agent coordination + shared memory' },

  // Premium skills (one-time)
  { name: 'Memory Stack Core', price: 29, interval: null, description: 'WAL + Working Buffer for context persistence across sessions' },
  { name: 'Session Wrap-Up Premium', price: 29, interval: null, description: 'Automated daily flush, MEMORY updates, git commit + push' },
  { name: 'Chaos Engineering', price: 49, interval: null, description: 'Adversarial testing + auto-healing shadow skills' },
  { name: 'Git Workflows Pro', price: 49, interval: null, description: 'Interactive rebase, worktree management, reflog recovery, subtrees, PR automation' },
  { name: 'Agent Harness Doctor', price: 99, interval: null, description: 'Audit and fix agent harnesses with health scoring' },
  
  // Subscriptions for tools
  { name: 'Proactive Ops Monitor', price: 29, interval: 'month', description: 'Token utilization tracking, health dashboard, alerts' },
  { name: 'ToolRouter Gateway', price: 49, interval: 'month', description: 'Unified access to 150+ tools via ToolRouter API' },

  // PagePilot tiers
  { name: 'PagePilot Dropshipping Lite', price: 39, interval: 'month', description: '50 pages/month, 1 store' },
  { name: 'PagePilot Dropshipping Pro', price: 59, interval: 'month', description: '150 pages/month, up to 3 stores' },
  { name: 'PagePilot Dropshipping Expert', price: 79, interval: 'month', description: '250 pages/month, up to 5 stores' },

  // Bundles
  { name: 'Power User Pack', price: 149, interval: null, description: 'BUNDLE: Memory Stack + Wrap-Up + Agent Doctor + Git Workflows Pro' }
];

async function createAll() {
  console.log('Creating Stripe products and prices...\n');
  
  for (const p of products) {
    // Create product
    const product = await stripe.products.create({
      name: p.name,
      description: p.description,
      type: 'service',
    });
    
    // Create price
    const price = await stripe.prices.create({
      product: product.id,
      unit_amount: p.price * 100,
      currency: 'usd',
      recurring: p.interval ? { interval: p.interval } : undefined,
    });
    
    console.log(`✅ ${p.name}`);
    console.log(`   Product ID: ${product.id}`);
    console.log(`   Price ID: ${price.id}${p.interval ? ` (${p.interval})` : ' (one-time)'}\n`);
  }
  
  console.log('All products created. Copy these price IDs into hosting/landing-page.html');
}

createAll().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});