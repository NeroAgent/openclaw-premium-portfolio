# PagePilot Constraints & NERO Bypasses

## Hard Limits (All Plans)
- AI Images: 5/month (insufficient for scale)
  - *NERO Fix:* Integrate with stable-diffusion-local (Termux) or Midjourney API
- Page Generation: 50-250/month depending on tier
  - *NERO Fix:* Cache templates locally, modify HTML via regex instead of regenerating
- Shopify Stores: Max 5 on Expert plan
  - *NERO Fix:* Use Shopify Partners API for store spinning (developer accounts = unlimited dev stores)

## Technical Debt
- No WooCommerce: Shopify-only
  - *NERO Fix:* Deploy to Shopify → Use Shopify Buy Button embed on external sites
- Limited Customization: Block-based (no drag-drop)
  - *NERO Fix:* Post-process HTML with BeautifulSoup injection after PagePilot export
- Theme Lock-in: Requires Dawn/Sense
  - *NERO Fix:* Extract generated sections → inject into custom themes via Shopify Theme API

## API Gaps (Reverse Engineered)
- No Webhook Support: No native order notifications to external systems
  - *NERO Fix:* Poll Shopify Admin API every 60s → forward to AgentMail:9005
- No A/B Testing: Only on Pro/Expert plans
  - *NERO Fix:* Generate 2 variants → manual 50/50 traffic split via Shopify redirect scripts