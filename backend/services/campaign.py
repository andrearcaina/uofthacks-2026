import requests
from typing import Dict, List, Optional
from backboard import BackboardClient
import time
import random

class CampaignService:
    def __init__(self, client: BackboardClient):
        self.backboard_client = client
        self.manifesto = self._load_manifesto()
        self.assistant = None

    def _load_manifesto(self) -> str:
        with open("MANIFESTO.md", "r") as f:
            return f.read()
        
    async def _ensure_assistant(self):
        """Internal helper to ensure the Brand Guardian exists."""
        if not self.assistant:
            description = (
                "You are the Lead Brand Strategist. Your mission is to protect our brand identity "
                "while scaling the success of viral content. Use the provided Manifesto "
                "as your absolute law for voice, tone, and decision-making.\n\n"
                f"MANIFESTO:\n{self.manifesto}"
            )
            self.assistant = await self.backboard_client.create_assistant(
                name="BrandGuardianStrategist",
                description=description,
            )

    async def generate_video_scripts(self) -> Dict:
            time.sleep(15)

            list = ["elevenlabs1.mp4", "elevenlabs2.mp4", "elevenlabs3.mp4", "elevenlabs4.mp4", "elevenlabs5.mp4"]
    
            # randomly select 2 items from the list
            random_selection = random.sample(list, 2)

            return {
                "elevenlabs_video_file_paths": random_selection,
            }
    
    async def generate_draft_email(self) -> Dict:
        """Generates email draft. Can reuse a thread to maintain context."""
        try:
            await self._ensure_assistant()
            
            thread_id = None

            # Reuse existing thread if provided, otherwise create new
            active_thread_id = thread_id or (await self.backboard_client.create_thread(self.assistant.assistant_id)).thread_id

            hit_video_summary = ""

            with open("SUMMARY.md", "r") as f:
                hit_video_summary += f.read()

            with open("COMPARISON.md", "r") as f:
                hit_video_summary += "\n\n" + f.read()

            prompt = f"""
            Context: {hit_video_summary}
            TASK: Create a marketing email draft that leverages this viral momentum. Make it less than 60 words. Replace all mentions of brand to align with our Manifesto ({self.manifesto}).
            STRATEGY: Do not be pushy. Align with the Manifesto's values. Drive traffic without devaluing the brand.
            """

            response = await self.backboard_client.add_message(
                thread_id=active_thread_id,
                content=prompt,
                llm_provider="anthropic",
                model_name="claude-opus-4-20250514", 
                stream=False
            )

            return {
                "thread_id": active_thread_id,
                "email_content": response.content,
            }
        except Exception as e:
            return {"error": f"Email Draft Failed: {str(e)}"}