# OpenClaw Hosted — Checkout Server

Simple server that serves the landing page and creates Stripe Checkout Sessions for the three pricing tiers.

## Setup

1. Create products & prices in Stripe Dashboard (Products → Add product):
   - Basic: $19/mo → copy Price ID (e.g., `price_1...`)
   - Pro: $39/mo
   - Team: $99/mo

2. Edit `landing-page.html` and replace:
   - `price_BASIC_PLACEHOLDER` with actual Basic Price ID
   - `price_PRO_PLACEHOLDER` with Pro Price ID
   - `price_TEAM_PLACEHOLDER` with Team Price ID
   - `pk_live_XXXXXXXXXXXXXX` with your Stripe publishable key

3. Deploy this server (Render, Railway, Fly.io):
   - Set env var `STRIPE_SECRET` = your Stripe secret key (`sk_live_...`)
   - Set `BASE_URL` = your server's public URL (e.g., `https://openclaw-checkout.onrender.com`)

4. Point your domain (or use Render's URL) to access the landing page.

5. Add Stripe webhook (optional) if you want to handle post-purchase events (the provisioning server will handle that).

## Files

- `server.js` — Express app, serves `public/landing-page.html` and POST `/create-checkout-session`
- `public/landing-page.html` — edit with your Stripe publishable key and price IDs

## Deploy to Render

- Create Web Service
- Build: `npm install`
- Start: `node server.js`
- Env: `STRIPE_SECRET`, `BASE_URL`
- Plan: Free (may sleep) or Starter

---

That's all. When customers click "Get Started", they go through Stripe Checkout and subscribe. The provisioning server (separate) will receive `checkout.session.completed` webhook and auto-provision.
