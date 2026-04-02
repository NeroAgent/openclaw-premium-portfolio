"""
NERO PagePilot Automation Workflow
Integrates with VisionService (9004) for competitor analysis 
and AgentMail (9005) for order notifications
"""

WORKFLOW_SCHEMA = {
    "workflow_id": "pagepilot_nero_pipeline",
    "trigger": "vision_detected_product_opportunity",
    
    "steps": [
        # Step 1: Screen Capture Analysis (via VisionService)
        {
            "service": "nerovision:9004",
            "action": "capture_and_extract",
            "params": {
                "source": "competitor_ad_screenshot",
                "extract": ["product_url", "pricing", "claims"]
            },
            "output_var": "competitor_data"
        },
        
        # Step 2: PagePilot Product Scraping
        {
            "service": "pagepilot:9006", 
            "action": "scrape_product",
            "input": "$competitor_data.supplier_url",
            "output_var": "raw_product"
        },
        
        # Step 3: AI Page Generation
        {
            "service": "pagepilot:9006",
            "action": "generate_page",
            "params": {
                "tone": "aggressive", # Based on competitor analysis
                "language": "en",
                "template_type": "product_launch",
                "improve_upon_competitor": "$competitor_data.claims"
            },
            "output_var": "generated_page"
        },
        
        # Step 4: NERO Review (Human-in-the-loop)
        {
            "service": "neroclaw",
            "action": "request_approval",
            "params": {
                "preview_html": "$generated_page.html_blocks",
                "predicted_cvr": "$generated_page.score",
                "cost_estimate": "0.78", # Per PagePilot claim
                "decision_timeout": 300 # 5 min timeout for auto-deploy
            },
            "branches": {
                "approved": "step_5_deploy",
                "rejected": "step_5a_learn"
            }
        },
        
        # Step 5a: Error Learning Loop
        {
            "id": "step_5a_learn",
            "service": "neroclaw",
            "action": "log_correction",
            "params": {
                "skill": "pagepilot_dropshipping",
                "error_type": "page_rejected",
                "context": "$generated_page",
                "storage": "~/.neroclaw/skills/pagepilot_dropshipping/corrections.jsonl"
            }
        },
        
        # Step 5: Shopify Deployment
        {
            "id": "step_5_deploy",
            "service": "pagepilot:9006", 
            "action": "deploy_to_shopify",
            "params": {
                "store_url": "$NERO_SHOPIFY_STORE",
                "auto_enable_checkout": True,
                "pixel_tracking": ["meta", "tiktok", "google"]
            },
            "output_var": "live_listing"
        },
        
        # Step 6: AgentMail Notification
        {
            "service": "agentmail:9005",
            "action": "send_alert",
            "params": {
                "subject": "New Product Live: $raw_product.title",
                "body": "URL: $live_listing.live_url | Predicted CVR: $generated_page.score%",
                "tags": ["dropshipping", "auto_deployed"]
            }
        }
    ],
    
    "error_handling": {
        "scrape_failed": "fallback_to_manual_input",
        "shopify_rate_limit": "exponential_backoff_max_3",
        "ai_image_exhausted": "use_supplier_images_with_watermark"
    }
}