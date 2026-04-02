# PagePilot Dropshipping Skill

AI-powered product page generation and Shopify automation. Scrape products from AliExpress/Amazon, generate high-converting landing pages, and deploy to Shopify with one click.

## Overview

PagePilot Dropshipping integrates the PagePilot AI engine into OpenClaw. Turn any product URL into a fully optimized Shopify store in minutes.

### Features

- **Product Scraping**: Extract product data (title, images, specs, pricing) from AliExpress, Amazon, or any Shopify store
- **AI Page Generation**: Create landing pages in 40+ languages with customizable tone and templates
- **Shopify Deploy**: Publish directly to your Shopify store with product sync and inventory linking
- **CRO Intelligence**: Get daily winning products and conversion analysis

### Pricing Tiers

| Tier | Pages/Month | Stores | Price |
|------|-------------|--------|-------|
| Free | 3 | 1 | $0 (lifetime) |
| Lite | 50 | 1 | $39/mo |
| Pro | 150 | 3 | $59/mo |
| Expert | 250 | 5 | $79/mo |

## Quick Start

```bash
# 1. Scrape a product
tool("pagepilot-dropshipping", "scrape_product", {
  "source_url": "https://www.aliexpress.com/item/123456.html",
  "target_market": "US",
  "extract_media": true,
  "extract_specs": true
})
# Returns: {"product_data": {...}}

# 2. Generate landing page
tool("pagepilot-dropshipping", "generate_page", {
  "product_data": <from_scrape>,
  "tone": "professional",
  "target_audience": "tech enthusiasts",
  "language": "en",
  "template_type": "product_launch",
  "seo_keywords": ["buy online", "best price"],
  "cta_text": "Add to Cart"
})
# Returns: {"page_id": "...", "html_blocks": [...], "score": 0.87}

# 3. Deploy to Shopify
tool("pagepilot-dropshipping", "deploy_to_shopify", {
  "page_id": "<from_generate>",
  "store_url": "your-store.myshopify.com",
  "product_sync": true,
  "inventory_sync": true
})
# Returns: {"shopify_page_id": "...", "live_url": "..."}

# 4. Get winning products (intelligence)
tool("pagepilot-dropshipping", "get_winning_products", {
  "limit": 10,
  "niche": "electronics"
})

# 5. Analyze conversion potential
tool("pagepilot-dropshipping", "analyze_conversion", {
  "page_id": "<page_id>"
})
```

## Tools

- `scrape_product` — Extract product data from any URL
- `generate_page` — AI-generated landing page with ad copy and meta tags
- `deploy_to_shopify` — Publish page and optionally create product + inventory sync
- `get_winning_products` — Daily curated list of high-potential products
- `analyze_conversion` — Conversion score and improvement suggestions

## Requirements

- Shopify store (for deploy)
- PagePilot API key (configure in environment variables)
- Internet connection

## Configuration

Set environment variables:
- `PAGEPILOT_API_KEY` — your PagePilot API key
- `PAGEPILOT_BASE_URL` — API endpoint (default: https://app.pagepilot.ai/api/v2/)

## Integration Flow

1. User provides product URL
2. Scrape → Generate → Preview → Deploy
3. Monitor conversion via Shopify analytics

## Notes

This skill wraps the PagePilot AI service. You need an active PagePilot account and API access. Pricing tiers apply.
