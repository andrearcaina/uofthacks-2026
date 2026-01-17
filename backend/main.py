import os
import json
import time
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from twelvelabs import TwelveLabs

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TwelveLabs client
client = TwelveLabs(api_key=os.getenv("TWELVELABS_API_KEY"))

# Store the current index ID
current_index_id = None


def get_or_create_index(index_name: str = "video-analysis-index"):
    """Get existing index or create a new one"""
    global current_index_id
    
    # Try to find existing index
    try:
        indexes = client.indexes.list()
        for idx in indexes:
            if idx.name == index_name:
                current_index_id = idx.id
                print(f"Using existing index: id={idx.id}")
                return idx.id
    except Exception as e:
        print(f"Error listing indexes: {e}")
    
    # Create new index if not found
    index = client.indexes.create(
        index_name=index_name,
        models=[{"model_name": "pegasus1.2", "model_options": ["visual", "audio"]}]
    )
    current_index_id = index.id
    print(f"Created index: id={index.id}")
    return index.id


class AnalyzeRequest(BaseModel):
    url: str
    prompt: Optional[str] = "Provide a theme analysis of this video. Use 3 short sentences"


@app.post("/api/analyze")
async def analyze_video(request: AnalyzeRequest):
    """Analyze a video and return the complete response"""
    
    # 1. Get or create index
    index_id = get_or_create_index()
    
    # 2. Upload video from URL
    print(f"Uploading video from URL: {request.url}")
    asset = client.assets.create(
        method="url",
        url=request.url
    )
    print(f"Created asset: id={asset.id}")
    
    # 3. Index the video
    indexed_asset = client.indexes.indexed_assets.create(
        index_id=index_id,
        asset_id=asset.id
    )
    print(f"Created indexed asset: id={indexed_asset.id}")
    
    # 4. Wait for indexing to complete
    print("Waiting for indexing to complete...")
    while True:
        indexed_asset = client.indexes.indexed_assets.retrieve(
            index_id,
            indexed_asset.id
        )
        print(f"  Status={indexed_asset.status}")
        
        if indexed_asset.status == "ready":
            print("Indexing complete!")
            break
        elif indexed_asset.status == "failed":
            return {"status": "error", "message": "Indexing failed"}
        
        time.sleep(5)
    
    # 5. Analyze the video
    result = {"analysis": ""}
    text_stream = client.analyze_stream(
        video_id=indexed_asset.id,
        prompt=request.prompt
    )
    
    # 6. Process the results
    full_text = ""
    for text in text_stream:
        if text.event_type == "text_generation":
            full_text += text.text
            print(text.text, end="", flush=True)
    
    print()  # New line after streaming
    result["analysis"] = full_text
    
    return {"status": "success", "data": result}


@app.get("/")
async def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)