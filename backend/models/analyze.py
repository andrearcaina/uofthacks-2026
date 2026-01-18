from pydantic import BaseModel
from typing import Optional

class AnalyzeRequest(BaseModel):
    url: str