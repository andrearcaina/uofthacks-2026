export enum CampaignChannel {
    EMAIL = "EMAIL",
    INSTAGRAM = "INSTAGRAM",
    BLOG = "BLOG",
}

interface CampaignRequest {
    campaign_goal: string;
    channels: CampaignChannel[];
}

interface PublishRequest {
    campaign_data: any;
}

/**
 * Creates a campaign draft by calling the Remix API route.
 */
export async function createCampaignDraft(
    goal: string,
    channels: CampaignChannel[]
) {
    const payload: CampaignRequest = {
        campaign_goal: goal,
        channels,
    };

    try {
        const response = await fetch("/api/campaign/draft", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Remix API Error: ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Failed to create campaign draft:", error);
        throw error;
    }
}

/**
 * Publishes a campaign by calling the Remix API route.
 */
export async function publishCampaign(
    campaignData: any
) {
    const payload: PublishRequest = {
        campaign_data: campaignData,
    };

    try {
        const response = await fetch("/api/campaign/publish", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Remix API Error: ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Failed to publish campaign:", error);
        throw error;
    }
}
