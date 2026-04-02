# Project Handoff — OpenClaw Premium Portfolio & Hosted Agents

**Date:** 2026-04-01  
**Agent:** Nero ⚡

---

## ✅ Completed

### Premium Skills (8)

Published on ClawHub:

| Slug | Name | Price |
|------|------|-------|
| memory-stack-core | Memory Stack Core | $29 one-time |
| session-wrap-up-premium | Session Wrap-Up Premium | $29 one-time |
| agent-harness-doctor | Agent Harness Doctor | $99 one-time |
| git-workflows-advanced | Git Workflows Advanced | $49 one-time |
| proactive-ops-monitor | Proactive Ops Monitor | $29/mo |
| toolrouter-gateway | ToolRouter Gateway | $49/mo |
| session-sync-cloud | Session Sync Cloud | $9/mo |
| mcp-server-pack | MCP Server Pack | $29/mo |

**Bundle:** `power-user-pack` — $149 one-time (includes first 4)

All skills installed locally, tested, documented. SKILL.md files complete.

### ToolRegistry Library

`lib/tool-registry/` — TypeScript library for tool manifest system (based on claw-code patterns). Open source under MIT (feel free to publish separately).

### Hosted Agents Infrastructure (Code Complete)

- **Provisioning Server** (`hosting/provisioning-server/`) — Stripe webhook → Hetzner VPS creation → email + setup URL
- **Checkout Server** (`hosting/checkout-server/`) — Landing page + Stripe Checkout Session creation
- **Setup Script** (`provisioning-cli/setup.sh`) — Installs Docker, pulls OpenClaw, starts agent on VPS

Both servers are ready to deploy (Render recommended).

### GitHub Repository

https://github.com/NeroAgent/openclaw-premium-portfolio

Public portfolio with all code, docs, and business plans.

### Marketing Assets

- Dev.to article draft: `marketing/devto_memory_stack.md`
- Discord/Telegram announcement: ready
- X/Twitter thread: ready
- Skill landing pages: each SKILL.md includes full copy

---

## ⏳ Paused / To Do

### Stripe Products (you)

1. Create 3 subscription products in Stripe Dashboard:
   - Basic $19/mo
   - Pro $39/mo
   - Team $99/mo
2. Copy the Price IDs.

### Landing Page Configuration

Edit `hosting/checkout-server/public/landing-page.html`:
- Replace `price_BASIC_PLACEHOLDER` with Basic Price ID
- Replace `price_PRO_PLACEHOLDER` with Pro Price ID
- Replace `price_TEAM_PLACEHOLDER` with Team Price ID
- Replace `pk_live_XXXXXXXXXXXXXX` with your Stripe publishable key

### Deploy Checkout Server

Use Render (free tier possible):
- Connect repo (or just the `checkout-server` folder)
- Set env: `STRIPE_SECRET` (your `sk_live_...`), `BASE_URL` (your server URL)
- Deploy

Test: Visit landing page, click button, complete test checkout (use Stripe test cards).

### Deploy Provisioning Server (later)

After Checkout works, deploy `provisioning-server`:
- Set env: `STRIPE_SECRET`, `STRIPE_WEBHOOK_SECRET`, `HETZNER_API_TOKEN` (if using Hetzner), `PROVISIONING_BASE_URL`
- Create Stripe webhook endpoint pointing to `/webhook/stripe`
- Test with `stripe trigger checkout.session.completed`

### Choose Hosting Provider

- **Hetzner**: paid, ~$5-20/VPS/mo. Requires API token. Good performance.
- **Railway/Fly.io**: free tier possible, but limited resources. Would need code adjustments (currently Hetzner-specific). If you want free tier, I can adapt.

If you want free tier, say the word and I'll rewrite `createVPS()` for Railway/Fly APIs.

---

## 💰 Pricing Summary

**One-time skills:** $29, $29, $99, $49 → total $206  
**Subscription skills:** $29/mo, $49/mo, $9/mo, $29/mo → total $116/mo  
**Bundle (Power User Pack):** $149 one-time (4 one-time skills)

**Hosted Agents (future):** $19–99/mo + optional skill add-ons

---

## 📞 Support

- ClawHub DM: @NeroAgent
- GitHub Issues: https://github.com/NeroAgent/openclaw-premium-portfolio/issues

---

**Take your time. The portfolio is live, the code is ready, the infrastructure is waiting. When you're ready to launch, we'll turn the switch.**

— Nero ⚡
