# OpenClaw Hosted Agents — Provisioning Server

This server handles customer signup and VPS provisioning for OpenClaw Hosted Agents.

## Components

- `server.js` — Express app with webhooks and setup script generator
- `provisioning-cli/setup.sh` — Bash script that runs on the new VPS to install OpenClaw
- `docker-compose.yml` — optional, to run server in Docker

## How It Works

1. Customer purchases hosting via Stripe Checkout (separate frontend)
2. Stripe sends `checkout.session.completed` webhook to `/webhook/stripe`
3. Server:
   - Creates VPS via provider API (Hetzner)
   - Stores customer record
   - Sends email with credentials and setup URL: `https://provisioning.openclaw.ai/setup?agent_id=...`
4. Customer (or automated) visits the setup URL, downloads `setup.sh`, runs it on the VPS
5. Script installs Docker, pulls OpenClaw, starts agent container
6. Agent becomes accessible at `ws://VPS_IP:8080`

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `PORT` | Server port (default 3000) |
| `STRIPE_SECRET` | Stripe secret key (`sk_test_` or `sk_live_`) |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (optional, recommended) |
| `HETZNER_API_TOKEN` | Hetzner Cloud API token |
| `PROVISIONING_BASE_URL` | Public URL of this server (for setup links) |

## Local Development

```bash
npm install
cp .env.example .env
# Edit .env with test keys
npm start
```

Test endpoints:
- `GET /health` — should return `OK`
- `GET /setup?agent_id=test123` — returns `setup.sh` with agent ID injected

Test webhook locally with Stripe CLI:
```bash
stripe listen --forward-to localhost:3000/webhook/stripe
stripe trigger checkout.session.completed
```

## Deployment

### Render (recommended)

- Create new Web Service
- Build command: `npm install`
- Start command: `node server.js`
- Add environment variables
- Set auto-deploy on git push

### Vercel / Railway

Also compatible; just ensure Node runtime and environment vars set.

## Provider Integration

Currently supports **Hetzner Cloud**. To add others (DigitalOcean, Linode):

Edit `createVPS()` function in `server.js`:
- Implement API call to create a server with Ubuntu 22.04, 1GB+ RAM
- Return `{ id, ip, user, password }`

Return credentials so the email can include them.

## Customization

- Email template: modify `sendEmail()` function (currently logs to console)
- Setup script: edit `provisioning-cli/setup.sh` (bash)
- Agent configuration: edit the `config/agent.json` generation in setup.sh

## Security Notes

- The `/setup` endpoint is public; it only serves a static script. No auth needed because the `agent_id` is random.
- VPS credentials should be sent via email or stored encrypted.
- Use HTTPS in production (handled by Render automatically).
- Validate Stripe webhook signatures if `STRIPE_WEBHOOK_SECRET` set.

## Monitoring

- Check server logs for errors
- Monitor `/admin/customers` for provisioning status
- Set up alerts for failed VPS creations

## Future Improvements

- [ ] Database persistence (currently in-memory only)
- [ ] Retry logic for failed VPS creation
- [ ] Multi-provider failover
- [ ] Customer dashboard (status, logs, restart)
- [ ] Telemetry/Optout
- [ ] Docker image for server

---

*Built by Nero ⚡ for OpenClaw Hosted Agents.*
