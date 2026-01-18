import requests
from typing import Dict, List, Optional
from backboard import BackboardClient

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

    async def generate_video_scripts(self, hit_video_summary: str) -> Dict:
        """Generates Shorts scripts based on a hit video."""
        try:
            await self._ensure_assistant()
            thread = await self.backboard_client.create_thread(self.assistant.assistant_id)

            prompt = f"""
            A video is hitting. Summary: {hit_video_summary}
            TASK: Generate 2 YouTube Short scripts that replicate the 'hook' of the hit video but stay 100% on-brand.
            """

            response = await self.backboard_client.add_message(
                thread_id=thread.thread_id,
                content=prompt,
                llm_provider="google",
                model_name="anthropic/claude-sonnet-4.5", 
                stream=False
            )

            return {
                "thread_id": thread.thread_id,
                "scripts": response.content,
                "status": "success"
            }
        except Exception as e:
            return {"error": f"Video Generation Failed: {str(e)}"}

    async def generate_draft_email(self, hit_video_summary: str, thread_id: Optional[str] = None) -> Dict:
        """Generates email draft. Can reuse a thread to maintain context."""
        try:
            await self._ensure_assistant()
            
            # Reuse existing thread if provided, otherwise create new
            active_thread_id = thread_id or (await self.backboard_client.create_thread(self.assistant.assistant_id)).thread_id

            prompt = f"""
            Context: {hit_video_summary}
            TASK: Create a marketing email draft that leverages this viral momentum.
            STRATEGY: Do not be pushy. Align with the Manifesto's values. Drive traffic without devaluing the brand.
            """

            response = await self.backboard_client.add_message(
                thread_id=active_thread_id,
                content=prompt,
                llm_provider="google",
                model_name="anthropic/claude-sonnet-4.5", 
                stream=False
            )

            return {
                "thread_id": active_thread_id,
                "email_content": response.content,
            }
        except Exception as e:
            return {"error": f"Email Draft Failed: {str(e)}"}