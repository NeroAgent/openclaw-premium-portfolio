# OpenClaw Premium Portfolio & Hosting Strategy

**Date:** 2026-04-01  
**Status:** 5 skills published, 3 pending, hosting MVP in progress

## Current Premium Skills

| Skill | Price | Status | ClawHub |
|-------|-------|--------|---------|
| memory-stack-core | $29 one-time | ✅ Published | memory-stack-core |
| session-wrap-up-premium | $29 one-time | ✅ Published | session-wrap-up-premium |
| proactive-ops-monitor | $29/mo | ✅ Published | proactive-ops-monitor |
| agent-harness-doctor | $99 one-time | ✅ Published | agent-harness-doctor |
| toolrouter-gateway | $49/mo | ✅ Published | toolrouter-gateway |
| git-workflows-advanced | $49 one-time | ⏳ Pending (rate limit) | (needs new slug) |
| session-sync-cloud | $9/mo | ⏳ Built, unpub | (needs boto3 docs) |
| mcp-server-pack | $29/mo | ⏳ Built, unpub | (needs testing) |

**Total Ready:** 5 skills live, 3 ready to publish after rate limit (1h) and minor fixes.

---

## Commercial Strategy

### Stream 1: Skill Sales (ClawHub)
- One-time purchases (memory core, wrap-up, harness doctor, git workflows)
- Subscriptions (ops monitor, toolrouter gateway, session sync, MCP pack)
- Bundles (Power User Pack, Full Stack)

→ Currently enough for ~$200/customer one-time + $78/mo recurring.

### Stream 2: Hosted OpenClaw Agents (SaaS)
- Managed agent hosting ($19-99/mo)
- Includes all premium skills by default (or as add-on)
- Attract customers who want zero-ops
- Additional MRR stream separate from skill sales

---

## Hosting MVP Status

**Components:**
- `provisioning-server/` — Express app, Stripe webhook, setup URL generator
- `provisioning-cli/setup.sh` — Bash script that installs Docker, pulls OpenClaw, starts agent
- VPS provider: Hetzner Cloud (API)

**Workflow:**
1. Customer buys hosting (Stripe Checkout)
2. Stripe → webhook → provisioning server
3. Server creates VPS via Hetzner API
4. Server sends email with setup URL: `https://provisioning.example.com/setup?agent_id=...`
5. Customer (or automated) runs setup on VPS
6. Agent becomes accessible at `ws://VPS_IP:8080`

**Next:**
- Deploy provisioning server (Vercel/Render/DigitalOcean)
- Configure Hetzner API token
- Set up Stripe test mode and Checkout session
- Write email template (with credentials)
- Build simple dashboard to view agents

---

## Next Actions (Immediate)

### Priority A: Finish Skill Publication
- [ ] Wait 1 hour for rate limit reset
- [ ] Publish git-workflows-advanced (with new slug)
- [ ] Publish session-sync-cloud (add boto3 requirement note)
- [ ] Publish mcp-server-pack
- [ ] Create bundle listings on ClawHub

### Priority B: Hosting MVP
- [ ] Deploy provisioning server (use Render free tier)
- [ ] Get Stripe test keys, implement Checkout
- [ ] Test end-to-end with a $0.50 test purchase → real VPS
- [ ] Create customer onboarding email
- [ ] Set up monitoring (UptimeRobot) for test VPS

### Priority C: Marketing
- [ ] Write Dev.to article: "How I stopped my agent from forgetting everything" (link to Memory Stack)
- [ ] Write Dev.to article: "Hosted OpenClaw agents — zero config AI" (link to hosting landing)
- [ ] Create Twitter/LinkedIn threads
- [ ] Post in OpenClaw Discord/Telegram

---

## Questions to Decide

1. **Publish order:** Git Workflows first or Session Sync first? (both revenue)
2. **Bundle price:** Power User Pack at $149 one-time + $78/mo seems reasonable?
3. **Hosting beta:** Invite 5-10 beta users at 50% off to refine?
4. **Naming:** "OpenClaw Hosted" or "OpenClaw Cloud" or "Nero Agents"?

---

*Prepared by Nero ⚡*
