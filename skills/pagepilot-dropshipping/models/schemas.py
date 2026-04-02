"""
Data schemas for PagePilot-NERO integration
"""

PRODUCT_SCHEMA = {
    "source": "str", # aliexpress|amazon|shopify|other_shopify
    "source_url": "str",
    "scraped_at": "timestamp",
    "title_original": "str",
    "title_optimized": "str", # AI generated
    "description_raw": "text",
    "description_html": "text", # CRO-optimized HTML
    "images": {
        "supplier_originals": ["url"],
        "ai_generated": ["url"], # Max 5
        "variant_count": "int"
    },
    "pricing": {
        "supplier_cost": "float",
        "suggested_retail": "float",
        "profit_margin": "float",
        "currency": "str"
    },
    "specifications": "dict",
    "shipping": {
        "methods": ["str"],
        "typical_delivery_days": "int",
        "e_packet_available": "bool"
    }
}

PAGE_SCHEMA = {
    "page_id": "str",
    "template_type": "product_launch|preorder|upsell|waitlist|lead_gen",
    "shopify_theme": "dawn|sense|custom",
    "blocks": ["header", "hero", "benefits", "social_proof", "faq", "cta"],
    "seo": {
        "title": "str",
        "description": "str",
        "canonical": "str",
        "og_image": "url"
    },
    "performance": {
        "lighthouse_desktop": "int", # 99 typical
        "lighthouse_mobile": "int", # 91 typical
        "load_time_sec": "float"
    },
    "conversion_elements": {
        "trust_badges": ["secure_checkout", "money_back", "fast_shipping"],
        "urgency_timers": "bool",
        "social_proof_popup": "bool",
        "sticky_cta": "bool"
    }
}

ANALYTICS_SCHEMA = {
    "page_id": "str",
    "impressions": "int",
    "ctr_percent": "float",
    "add_to_cart_rate": "float", 
    "purchase_rate": "float",
    "roas": "float",
    "competitor_comparison": {
        "their_price": "float",
        "our_price": "float",
        "differentiation_score": "float"
    }
}