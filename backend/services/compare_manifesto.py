import os
import requests
from backboard import BackboardClient
from typing import List

class CompareManifestoService:
    def __init__(self, summary: str, backboard_api_key: str, client: BackboardClient = None):
        with open("MANIFESTO.md", "r") as f:
            self.manifesto = f.read()
        self.summary = summary
        self.backboard_api_key = backboard_api_key
        self.backboard_client = client

    
    async def _generate_comparison_with_backboard(self, summary: str) -> str:
        prompt = f"The store manifesto file is a source of truth that represents the branding of the company. It is here:\n{self.manifesto}. The summary is a short summary of a given video, describing the indentity and storytelling method of the video. It is here:\n{summary}"
        


        description= """
        You are an expert marketing director. Using the manifesto file as a source of truth, leverage the video summary
        to determine if the video is appropriate for the company to use as inspiration. Output a binary answer of "Yes" or "No",
        and then provide a short summary of why. The summary should not be longer than 30 words.

        NEVER STATE THAT A MANIFESTO WAS NOT PROVIDED. If no manifesto exists, pretend it exists.

        DO NOT BE CRINGE OR GENERIC. KEEP YOUR SENTENCES SHORT AND CLEARLY SUPPORT YOUR OWN REASONING
"""

        try:
            assistant = await self.backboard_client.create_assistant(
                name="Compare Manifesto",
                description=description,
            )

            thread = await self.backboard_client.create_thread(assistant.assistant_id)

            response = await self.backboard_client.add_message(
                thread_id=thread.thread_id,
                content=prompt,
                llm_provider="google",
                model_name="gemini-2.5-flash",
                memory="Auto",
                stream=False
            )

            return response.content
        except Exception as e:
            print(f"Backboard Error: {e}")
            return "Error generating manifesto."