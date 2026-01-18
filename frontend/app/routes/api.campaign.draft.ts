import { authenticate } from "../shopify.server";
import { data, type ActionFunctionArgs } from "@remix-run/node";

export const action = async ({ request }: ActionFunctionArgs) => {
    const { session } = await authenticate.admin(request);

    if (!session) {
        return data({ status: "error", message: "No session found" }, { status: 401 });
    }

    const { shop, accessToken } = session;

    const body = await request.json();

    const response = await fetch("http://localhost:8000/api/campaign/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            ...body,
            shop_domain: shop,
            access_token: accessToken,
        }),
    });

    const result = await response.json();

    return data(result);
};
