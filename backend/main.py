import os
import json
import time
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.manifesto import manifesto_router
from routers.twelvelabs import twelvelabs_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(manifesto_router, prefix="/api/manifesto")
app.include_router(twelvelabs_router, prefix="/api/twelvelabs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)