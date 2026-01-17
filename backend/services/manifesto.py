import os
import requests
from backboard import BackboardClient
from typing import List

class ManifestoService:
    def __init__(self, shop: str, token: str, shopify_api_key: str, shopify_api_secret: str, backboard_api_key: str):
        self.shop = shop
        self.token = token
        self.shopify_api_key = shopify_api_key
        self.shopify_api_secret = shopify_api_secret
        self.backboard_api_key = backboard_api_key
        self.backboard_client = BackboardClient(api_key=self.backboard_api_key)

    async def create_manifesto(self):
        if self._check_manifesto_exists():
            return self.view_manifesto()

        print("Scanning store for data...")
        store_data = self._scan_store()
        if not store_data:
            return "Failed to retrieve store data."

        manifesto = await self._generate_manifesto_with_backboard(store_data)

        self._save_manifesto_to_file(manifesto)

        return {"manifesto": manifesto}

    def view_manifesto(self):
        if not self._check_manifesto_exists():
            return "No manifesto found."

        print("Reading existing manifesto...")

        with open("MANIFESTO.md", "r") as f:
            manifesto_content = f.read()

        return {"manifesto": manifesto_content}

    def _scan_store(self):
        url = f"https://{self.shop}/admin/api/2024-01/graphql.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.token
        }
        
        query = """
        {
            shop { name description }
            products(first: 17) {
            edges { node { title descriptionHtml tags } }
            }
        }
        """
        
        try:
            response = requests.post(url, json={"query": query}, headers=headers)
            if response.status_code != 200:
                print(f"Shopify API Error: {response.text}")
                return None
                
            data = response.json().get("data", {})
            shop_desc = data.get("shop", {}).get("description", "No description")
            products = data.get("products", {}).get("edges", [])
            
            product_text = "\n".join([
                f"- Product: {p['node']['title']} | Tags: {p['node']['tags']}" 
                for p in products
            ])
            
            return product_text
        except Exception as e:
            print(f"Fetch Error: {e}")
            return None
    
    async def _generate_manifesto_with_backboard(self, store_data: List[str]) -> str:
        prompt = f"Generate a MANIFESTO.md for the following store data:\n{store_data}. Send me just the MD content."
        
        description= """
        You are an expert manifesto generator. Create a compelling and unique manifesto
        based on the store data provided. The manifesto should reflect the brand's values,
        mission, and vision in a concise and engaging manner. Manifesto should be formatted in markdown,
        and it must be shorter than 100 words.

        DO NOT BE CRINGE OR GENERIC. MAKE IT UNIQUE TO THE STORE AND THE VISION OF WHAT IT REPRESENTS.
"""

        try:
            assistant = await self.backboard_client.create_assistant(
                name="Manifesto Generator",
                description=description,
            )

            thread = await self.backboard_client.create_thread(assistant.assistant_id)




            response = await self.backboard_client.add_message(
                thread_id=thread.thread_id,
                content=prompt,
                llm_provider="google",
                model_name="gemini-2.5-flash",
                stream=False    
            )

            return response.content
        except Exception as e:
            print(f"Backboard Error: {e}")
            return "Error generating manifesto."
        
    def _save_manifesto_to_file(self, manifesto: str, filename: str = "MANIFESTO.md"):
        try:
            with open(filename, "w") as f:
                f.write(manifesto)
        except Exception as e:
            print(f"File Write Error: {e}")
    
    def _check_manifesto_exists(self, filename: str = "MANIFESTO.md") -> bool:
        return os.path.isfile(filename)
