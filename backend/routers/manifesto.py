from fastapi import APIRouter, Depends
from config import get_config, get_backboard_client
from services.manifesto import ManifestoService
from models.manifesto import ManifestoRequest
from backboard import BackboardClient

manifesto_router = APIRouter()

@manifesto_router.post("/generate")
async def generate_manifesto(
    request: ManifestoRequest,
    client: BackboardClient = Depends(get_backboard_client)
):
    
    print("🚀 Generating manifesto...")

    manifesto_service = ManifestoService(
        shop=request.shop_domain,
        token=request.access_token,
        client=client
    )
    manifesto = await manifesto_service.create_manifesto()

    return {"status": "success", "manifesto": manifesto["manifesto"]}