# Hosting Setup — To Resume Later

**Date:** 2026-04-01  
**Status:** Provisioning server code complete, not yet deployed

## What's Built

- Provisioning server (`hosting/provisioning-server/`) with:
  - Stripe webhook handler (`/webhook/stripe`)
  - Setup script endpoint (`/setup?agent_id=...`)
  - Hetzner Cloud API integration (real VPS creation)
  - Mock mode when `HETZNER_API_TOKEN` unset
- Docker Compose and Render deployment config (`render.yaml`)
- Setup script (`provisioning-cli/setup.sh`) for VPS

## What's Needed to Deploy

1. **Stripe webhook** configured to point to live server URL
2. **Hetzner API token** (if using real provisioning; else use mock)
3. **Deploy to Render** (or other host) with env vars:
   - `STRIPE_SECRET` (sk_live_...)
   - `STRIPE_WEBHOOK_SECRET` (whsec_...)
   - `HETZNER_API_TOKEN` (optional)
   - `PROVISIONING_BASE_URL` (your server URL)
4. **Email sending** (not implemented; currently just logs)
5. **Customer dashboard** (future)
6. **Database persistence** (currently in-memory only)

## Alternative: Switch to Free-Tier Provider

Consider using Railway or Fly.io to offer free tier hosting. Would need to retool the `createVPS()` function for their APIs.

## Remember To

- [ ] Decide: Hetzner (paid) vs free-tier provider
- [ ] Deploy server to Render (or other)
- [ ] Set up Stripe webhook endpoint
- [ ] Test end-to-end: purchase → webhook → VPS creation → email → customer runs setup
- [ ] Build simple customer status page (optional)
- [ ] Implement email sending (SendGrid/Mailgun)
- [ ] Add database (Postgres/Redis) for persistence
- [ ] Create landing page for Hosted Agents product
- [ ] Set up billing/tier logic in Stripe Checkout sessions

---

*When returning, start here.*
