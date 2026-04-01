# Provisioning Server Deployment Guide

## Pre-deploy

1. Ensure you have:
   - Stripe Secret Key (`sk_live_...`)
   - Stripe Webhook Secret (`whsec_...`)
   - Hetzner API Token (from Hetzner Cloud Console → API Tokens)
   - Desired public URL (e.g., `https://openclaw-provisioning.onrender.com`)

2. Create a new GitHub repo for this server (or use existing)

## Deploy to Render (recommended)

1. Push `provisioning-server/` directory to a GitHub repository
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect the repository
4. Settings:
   - Name: `openclaw-provisioning`
   - Environment: Node
   - Build Command: `npm install`
   - Start Command: `node server.js`
   - Plan: Starter ($7/mo) for always-on (free tier may sleep)
5. Environment Variables:
   - `STRIPE_SECRET` = your Stripe secret key
   - `STRIPE_WEBHOOK_SECRET` = your webhook signing secret
   - `HETZNER_API_TOKEN` = your Hetzner API token
   - `PROVISIONING_BASE_URL` = `https://openclaw-provisioning.onrender.com`
6. Create Web Service (deploy)

## Configure Stripe Webhook

1. In Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Endpoint URL: `https://openclaw-provisioning.onrender.com/webhook/stripe`
4. Description: `OpenClaw Provisioning`
5. Select events: `checkout.session.completed`
6. Click "Add endpoint"
7. Copy the **Signing secret** (starts with `whsec_`) and paste into Render env var `STRIPE_WEBHOOK_SECRET` (if not already)

## Test

1. Trigger a test webhook:
   ```bash
   stripe listen --forward-to https://openclaw-provisioning.onrender.com/webhook/stripe
   stripe trigger checkout.session.completed
   ```
2. Check Render logs for output: should log provisioning details
3. Verify `/admin/customers` endpoint shows the test entry

## Going Live

- Ensure Stripe Checkout sessions are created with `metadata.tier` set to `basic`, `pro`, or `team`
- The webhook will then auto-provision VPS and email credentials (email sending not yet implemented; currently logs to console)

## Custom Domain (optional)

In Render service settings, add Custom Domain:
- Provide your domain (e.g., `provisioning.openclaw.ai`)
- Render gives DNS records to add (CNAME or A)
- Update `PROVISIONING_BASE_URL` env var to match

---

That's it. The server is now live and provisioning.
