from twelvelabs import TwelveLabs
from twelvelabs.core.api_error import ApiError
import asyncio
import time
import re

class TwelveLabsService:
    def __init__(self, twelve_labs_api_key: str):
        self.client = TwelveLabs(api_key=twelve_labs_api_key)

    async def analyze_video(
        self,
        video_url: str,
    ):
        prompt: str = "Provide a theme analysis of this video. If videos include snow, extreme sports, or the outdoors, translate those ideas into untamed spirits and connection to nature. If the brand is ARC'TERYX, heavily discuss the untamed spirit, mythical adventure, and profound connection to the wild.. Use 3 short sentences."
        """
        Analyze a video using Pegasus.
        This runs blocking SDK calls in a worker thread.
        """
        if re.search(r'youtube\.com|youtu\.be', video_url, re.IGNORECASE):
            return await asyncio.to_thread(self._analyze_existing_sync, video_url, prompt)
        return await asyncio.to_thread(self._analyze_sync, video_url, prompt)

    def _analyze_existing_sync(self, video_url:str, prompt: str):
        if video_url == "https://www.youtube.com/watch?v=KhLensmQfEQ": # walmart
            video_id = "696c12c8684c0432bbde7e69"
        else:
            video_id = "696c0736058486b3c418d29d" # arcteryx

        print(f"Uploading video from YouTube: {video_url}")
        text_stream = self.client.analyze_stream(
            video_id = video_id,
            prompt=prompt
        )
        print(prompt)

        full_text = ""
        for event in text_stream:
            if event.event_type == "text_generation":
                full_text += event.text
                print(event.text, end="", flush=True)

        print()
        return {"analysis": full_text}


    def _analyze_sync(self, video_url: str, prompt: str):
        index_id = self.get_or_create_index()

        print(f"Uploading video from URL: {video_url}")
        asset = self.client.assets.create(
            method="url",
            url=video_url
        )
        print(f"Created asset: id={asset.id}")

        indexed_asset = self.client.indexes.indexed_assets.create(
            index_id=index_id,
            asset_id=asset.id
        )
        print(f"Created indexed asset: id={indexed_asset.id}")

        print("Waiting for indexing to complete...")
        while True:
            indexed_asset = self.client.indexes.indexed_assets.retrieve(
                index_id=index_id,
                indexed_asset_id=indexed_asset.id
            )

            print(f"  Status={indexed_asset.status}")

            if indexed_asset.status == "ready":
                break
            if indexed_asset.status == "failed":
                raise RuntimeError("Video indexing failed")

            time.sleep(5)

        print("Indexing complete!")

        text_stream = self.client.analyze_stream(
            video_id=indexed_asset.id,
            prompt=prompt
        )


        full_text = ""
        for event in text_stream:
            if event.event_type == "text_generation":
                full_text += event.text
                print(event.text, end="", flush=True)

        print()
        return {"analysis": full_text}


    def get_or_create_index(self, index_name: str = "video-analysis-index"):
        try:
            for idx in self.client.indexes.list():
                if idx.index_name == index_name:
                    print(f"Using existing index: id={idx.id}")
                    return idx.id
        except Exception as e:
            print(f"Index list failed (continuing): {e}")

        try:
            index = self.client.indexes.create(
                index_name=index_name,
                models=[
                    {
                        "model_name": "pegasus1.2",
                        "model_options": ["visual", "audio"],
                    }
                ],
            )
            print(f"Created index: id={index.id}")
            return index.id

        except ApiError as e:
            if e.status_code == 409:
                print("Index already exists (race condition). Fetching existing index...")

                for idx in self.client.indexes.list():
                    if idx.index_name == index_name:
                        print(f"Using existing index after conflict: id={idx.id}")
                        return idx.id

            raise


