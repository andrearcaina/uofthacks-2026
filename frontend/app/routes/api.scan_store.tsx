import { authenticate } from "../shopify.server";
import type { ActionFunctionArgs } from "@remix-run/node";
import { data } from "@remix-run/node"; // <--- Import this

export const action = async ({ request }: ActionFunctionArgs) => {
    const { session } = await authenticate.admin(request);

    if (!session) {
        return data({ 
            status: "error", message: "No session found" 
        }, { 
            status: 401 
        });
    }

    const { shop, accessToken } = session;
    console.log(`🔑 Handing off control of ${shop} to Python...`);

    try {
        const pythonResponse = await fetch("http://127.0.0.1:8000/api/manifesto/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                shop_domain: shop,
                access_token: accessToken 
            }),
        });

        const result = await pythonResponse.json();

        return { status: "success", manifesto: result }; 

    } catch (error) {
        console.error("Python Connection Failed:", error);
        return data({ 
            status: "error", message: "Python Brain is offline" 
        }, { 
            status: 500 
        });
    }
};