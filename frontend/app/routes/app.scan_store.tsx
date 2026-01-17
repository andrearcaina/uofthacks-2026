import { useEffect } from "react";
import { useFetcher } from "@remix-run/react";
import { Page, Layout, Card, Button, BlockStack, Text, Banner } from "@shopify/polaris";
import { TitleBar } from "@shopify/app-bridge-react";

export default function Index() {
    // setup the Fetcher (The background worker)
    const fetcher = useFetcher<any>();

    // check loading state to disable button while scanning
    const isLoading = fetcher.state === "submitting" || fetcher.state === "loading";
    const data = fetcher.data;

    // the Action: Calls your /api/scan-store route
    const generateManifesto = () => {
    fetcher.submit({}, { method: "POST", action: "/api/scan_store" });
    };

    // feedback Loop: Watch for the result
    useEffect(() => {
    if (data?.status === "success") {
        console.log("Manifesto Created:", data.manifesto);
        shopify.toast.show("Success! Agent Manifesto Generated.");
    } else if (data?.status === "error") {
        console.error("Agent Error:", data);
        shopify.toast.show("Agent Connection Failed", { isError: true });
    }
    }, [data]);

    return (
    <Page>
        <TitleBar title="AGENT AI SYSTEM" />
        <Layout>
        <Layout.Section>
            <Card>
            <BlockStack gap="500">
                <Text as="h2" variant="headingLg">
                    Agent Status: <span style={{color: "green"}}>Active & Watching</span>
                </Text>
                
                <Text as="p">
                    The Agent is ready to scan your store's products and about page to 
                    generate the <strong>BRAND_MANIFESTO.md</strong>.
                </Text>
                
                {/* SUCCESS BANNER */}
                {data?.status === "success" && (
                <Banner tone="success" title="Identity Crystallized">
                    <p>
                    <strong>Success!</strong> The <code>BRAND_MANIFESTO.md</code> file 
                        has been generated in your backend folder.
                    </p>
                </Banner>
                )}

                {/* ERROR BANNER */}
                {data?.status === "error" && (
                <Banner tone="critical" title="Connection Failed">
                    <p>
                        Could not connect to Python. Is <code>uvicorn main:app</code> running on port 8000?
                    </p>
                </Banner>
                )}
                
                {/* THE BUTTON */}
                <Button 
                variant="primary" 
                onClick={generateManifesto}
                loading={isLoading}
                disabled={isLoading}
                >
                {isLoading ? "Scanning Store DNA..." : "Generate Brand Manifesto"}
                </Button>

            </BlockStack>
            </Card>
        </Layout.Section>
        
        {/* DEBUGGING: Show raw output if successful */}
        {data?.manifesto && (
            <Layout.Section>
                <Card>
                <BlockStack gap="200">
                    <Text as="h3" variant="headingSm">Agent Output (Debug):</Text>
                    <pre style={{ overflowX: "scroll", padding: "10px", background: "#f4f4f4" }}>
                    {JSON.stringify(data.manifesto, null, 2)}
                    </pre>
                </BlockStack>
                </Card>
            </Layout.Section>
        )}
        </Layout>
    </Page>
    );
}