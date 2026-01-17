from fastapi.routing import APIRouter
from services.manifesto import ManifestoService

manifesto_router = APIRouter()

@manifesto_router.post("/generate")
async def generate_manifesto():
    manifesto = ManifestoService.create_manifesto()
    print("Generated Manifesto:", manifesto)
    return {"manifesto": manifesto}