from fastapi import APIRouter, Depends, HTTPException
from config import get_config, get_backboard_client
from services.campaign import CampaignService
from models.campaign import CampaignRequest, PublishRequest
from backboard import BackboardClient

campaign_router = APIRouter()

@campaign_router.post("/draft")
async def create_campaign_draft(
    request: CampaignRequest,
    client: BackboardClient = Depends(get_backboard_client)
):
    """
    Synchronous endpoint to generate drafts.
    """
    service = CampaignService(
        shop=request.shop_domain,
        token=request.access_token,
        client=client
    )
    
    # Blocking call to service
    draft = await service.generate_draft(
        goal=request.campaign_goal,
        channels=request.channels
    )
    
    return draft

@campaign_router.post("/publish")
def publish_campaign(
    request: PublishRequest,
    client: BackboardClient = Depends(get_backboard_client)
):
    """
    Endpoint to publish and track AI-generated campaigns to Shopify.
    """
    service = CampaignService(
        shop=request.shop_domain,
        token=request.access_token,
        client=client
    )
    
    try:
        shopify_event = service.publish_campaign(request.campaign_data)
        
        if "marketing_event" not in shopify_event or "id" not in shopify_event["marketing_event"]:
            raise HTTPException(status_code=500, detail="Failed to publish campaign to Shopify.")
        
        return {
            "status": "published",
            "shopify_event_id": shopify_event["marketing_event"]["id"],
            "shopify_event": shopify_event["marketing_event"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
