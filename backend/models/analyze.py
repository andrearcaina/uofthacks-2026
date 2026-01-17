from pydantic import BaseModel
from typing import Optional

class AnalyzeRequest(BaseModel):
    url: str
    prompt: Optional[str] = "Provide a theme analysis of this video. Use 3 short sentences"
