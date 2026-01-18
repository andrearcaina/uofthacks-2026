from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class CampaignChannel(str, Enum):
    EMAIL = "EMAIL"
    YOUTUBE_SHORTS = "YOUTUBE_SHORTS"

class CampaignRequest(BaseModel):
    hit_video_summary: str
    channels: List[CampaignChannel] = [CampaignChannel.EMAIL, CampaignChannel.YOUTUBE_SHORTS]