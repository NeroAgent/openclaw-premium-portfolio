# Deploying the Provisioning Server

## Quick Deploy to Render

1. Push this directory to a GitHub repo
2. Create new Web Service on Render
   - Environment: Node
   - Build Command: `npm install`
   - Start Command: `node server.js`
   - Plan: Free (or $7/mo for always-on)
3. Add Environment Variables:
   - `STRIPE_SECRET` (sk_test_...)
   - `STRIPE_WEBHOOK_SECRET` (whsec_...)
   - `PROVISIONING_BASE_URL` (https://your-service.onrender.com)
   - (Optional) `HETZNER_API_TOKEN` if implementing real VPS creation
4. Deploy
5. Set Stripe webhook endpoint to: `https://your-service.onrender.com/webhook/stripe`
   - Select events: `checkout.session.completed`

That's it. The server is live.

## Testing Locally

```bash
cd provisioning-server
npm install
cp .env.example .env
# Edit .env with test keys
node server.js
# In another terminal:
curl http://localhost:3000/health  # should return OK
curl "http://localhost:3000/setup?agent_id=test123" | head -20
```

## What's Missing for Production

- **Real VPS provisioning**: Implement `createVPS()` with actual provider API (Hetzner, DigitalOcean)
- **Database**: Replace in-memory `Map` with PostgreSQL/Redis for persistence
- **Email sending**: Connect to SendGrid/Mailgun to send credentials and setup URL
- **Dashboard**: Simple UI to view customers, agent status
- **Monitoring**: Alerts if VPS creation fails, agent doesn't come online
- **SSL**: Handled by Render automatically
- **Scalability**: May need multiple server instances; use sticky sessions or centralized DB

## Cost Estimate

- Render free tier: $0 (sleeps after inactivity) — not ideal for webhooks
- Render starter: $7/mo (always on)
- Email (SendGrid): free tier up to 100/day
- VPS costs (Hetzner): ~$5-10/agent/month (billed separately)

---

*After deployment, test with Stripe test mode before going live.*
