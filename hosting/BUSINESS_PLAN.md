# OpenClaw Hosted Agents — Business Plan & Operations

**Version:** 1.0  
**Date:** 2026-04-01  
**Owner:** Nero ⚡

---

## 1. Value Proposition

"Turnkey AI agents. Zero setup, always-on, persistent memory. Deploy your OpenClaw agent in one click, we handle the servers, updates, and backups."

### Customer Pain
- OpenClaw install is technical (PRoot, dependencies, memory limits)
- Agents die when device sleeps/reboots
- No SLA, no support
- Hard to expose to web (port forwarding, SSL)

### Our Solution
- Fully managed VPS with OpenClaw pre-installed
- Web dashboard + API endpoint
- Telegram/Signal bridges included
- Automated backups
- 24/7 uptime monitoring
- Premium skills optionally installed (Memory Stack, ToolRouter)

---

## 2. Market & Pricing

### TAM
~10k OpenClaw users (estimate from ClawHub downloads, GitHub stars). 5-10% willing to pay → 500-1000 potential customers.

### Pricing Tiers

| Tier | Resources | Price | Monthly Cost (us) | Margin |
|------|-----------|-------|-------------------|--------|
| Basic | 1 vCPU, 1GB RAM, 25GB SSD | $19/mo | $8 | 58% |
| Pro   | 2 vCPU, 2GB RAM, 50GB SSD | $39/mo | $15 | 62% |
| Team | 4 vCPU, 4GB RAM, 100GB SSD + shared Redis | $99/mo | $35 | 65% |

**Add-ons:**
- Extra storage: $0.10/GB/mo
- Premium skills bundle: +$29/mo (includes all our paid skills except Git Workflows)
- Custom domain/SSL: $5/mo

### Trial
- 7-day free trial (Basic tier) with credit card
- 24-hour money-back guarantee

---

## 3. Costs & Financials

### COGS per Customer (monthly)

| Item | Basic | Pro | Team |
|------|-------|-----|------|
| VPS (Hetzner CX11/ CX21/ CX31) | $5.50 | $10 | $20 |
| Backup storage (S3) | $0.50 | $1 | $2 |
| Bandwidth | $1 | $2 | $5 |
| Monitoring (UptimeRobot/Pingdom) | $0.50 | $0.50 | $0.50 |
| **Total COGS** | **$7.50** | **$13.50** | **$27.50** |

### Gross Margin
- Basic: (19-7.5)/19 = **60.5%**
- Pro: (39-13.5)/39 = **65.4%**
- Team: (99-27.5)/99 = **72.2%**

### Assumptions for 100 Customers
- Mix: 60% Basic, 30% Pro, 10% Team
- MRR = 60*19 + 30*39 + 10*99 = $3,300
- COGS = 60*7.5 + 30*13.5 + 10*27.5 = $1,075
- **Gross profit = $2,225/mo**

Support: 20h/mo at $100/h = $2,000/mo (initially owner's time, later hire)

---

## 4. Go-to-Market

### Phase 1: Beta (Month 1-2)
- Limit to 20 customers
- Price: $10/mo Basic, $20/mo Pro (50% off)
- Manual onboarding (email)
- Gather feedback, fix bugs
- Ask for testimonials

### Phase 2: Public Launch (Month 3)
- Full pricing
- Launch on OpenClaw Discord, Telegram, X
- Dev.to/Hacker News post: "OpenClaw Hosted — zero-config AI agents"
- ClawHub listing (featured)
- Affiliate program: 10% recurring commission

### Phase 3: Scale (Month 4-6)
- Automation: provisioning API, self-serve signup
- Add Team tier
- Explore partnerships (ToolRouter, OpenClaw official recommendation)

---

## 5. Technical Architecture

### Components

1. **Provisioning Service** (this repo)
   - Express app with Stripe webhook
   - Integrates with VPS provider API (Hetzner)
   - Generates unique agent_id and setup URL
   - Sends email with credentials

2. **Setup Script** (`setup.sh`)
   - Runs on the fresh VPS
   - Installs Docker, clones OpenClaw, writes config, starts container
   - Reports success back to provisioning service

3. **Hosted Agent** (Docker container)
   - Standard OpenClaw + optional premium skills
   - Exposes gateway on port 8080
   - Daily backups to S3 (using session-sync-cloud skill)
   - Logs aggregated to central Loki (optional)

4. **Customer Dashboard** (future)
   - View logs, restart agent, resource usage
   - Access web terminal
   - Manage billing (via Stripe portal)

5. **Monitoring & Alerting**
   - Prometheus metrics from agent (memory, CPU, API latency)
   - Alerts on downtime, high resource usage
   - Uptime monitoring (external ping)

### VPS Provider Choice

- **Primary:** Hetzner Cloud (good price, API, EU/US locations)
- **Backup:** DigitalOcean, Linode
- **Why not AWS:** Cost

---

## 6. Operations & Support

### Ops Tasks (weekly)
- Check monitoring alerts
- Review failed backups
- Apply security updates to host (VPS provider handles some)
- Update OpenClaw base images quarterly

### Support Channels
- **Email:** support@openclaw.ai (ticketing system later)
- **ClawHub DM:** for quick questions
- **Documentation:** self-hosted guide (install, config, troubleshooting)

### SLA
- Uptime: 99.5% (excluding maintenance)
- Support response: <24h foremail, <4h for critical (agent down)

---

## 7. Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Abuse (spam, illegal content) | High | Medium | TOS, monitoring, rate limits, abuse contact |
| Agent crashes due to bad skill | Medium | High | Sandboxing (Docker), auto-restart, alert on non-zero exit |
| VPS provider outage | High | Low | Multi-provider failover (DNS switch) |
| Churn (agent not useful) | Medium | Medium | Include Memory Stack (sticky), good onboarding |
| Competition (bigger hosting co) | Medium | Medium | First-mover in OpenClaw niche, build brand |

---

## 8. Development Roadmap

**Week 1-2: MVP**
- [ ] Provisioning server with Stripe test mode
- [ ] Setup script working on fresh Hetzner VPS
- [ ] Manual onboarding process (invite email)
- [ ] Basic backup (session-sync-cloud to S3)

**Week 3-4: Beta**
- [ ] Customer dashboard (logs, restart button)
- [ ] Auto install premium skills
- [ ] Telegram bridge integration
- [ ] Monitoring alerts

**Week 5-6: Polish**
- [ ] Self-service signup (Stripe Checkout)
- [ ] FAQ / docs site
- [ ] Team tier multi-agent support

---

## 9. Success Metrics

| Metric | Target (Month 6) |
|--------|------------------|
| Customers | 100 |
| MRR | $3,300 |
| Churn | <5% monthly |
| Support tickets/ customer/ month | <1 |
| Uptime | 99.5% |
| NPS | >40 |

---

## 10. Decision: Build vs Buy

We already have the OpenClaw agent; building this hosting service is mostly ops and automation. No off-the-shelf alternative gives us control over pricing and integration with our premium skills.

**Go.**
