from fastapi import APIRouter, Depends
from pydantic import BaseModel
from config import get_config
from services.manifesto import ManifestoService

manifesto_router = APIRouter()

class ManifestoRequest(BaseModel):
    shop_domain: str
    access_token: str

@manifesto_router.post("/generate")
async def generate_manifesto(
    request: ManifestoRequest, 
    settings: dict = Depends(get_config)
):
    
    print("🚀 Generating manifesto...")

    manifesto_service = ManifestoService(
        shop=request.shop_domain,
        token=request.access_token,
        shopify_api_key=settings["shopify_api_key"],
        shopify_api_secret=settings["shopify_api_secret"],
        backboard_api_key=settings["backboard_api_key"]
    )
    manifesto = await manifesto_service.create_manifesto()

    return {"status": "success", "manifesto": manifesto}