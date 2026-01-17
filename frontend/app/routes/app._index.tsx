import { Button, Card, Layout, Page, Text, BlockStack, TextField } from "@shopify/polaris";
import { TitleBar } from "@shopify/app-bridge-react";
import { useState } from "react";

export default function Index() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const runScan = () => {
    console.log("Calling Agent...");
    shopify.toast.show("Agent Activation Signal Sent!"); 
  };

  const analyzeUrl = async () => {
    if (!url) {
      shopify.toast.show("Please enter a video ID");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("API Response:", data);
        shopify.toast.show("Analysis complete!");
      } else {
        shopify.toast.show("API request failed");
      }
    } catch (error) {
      console.error("Error calling API:", error);
      shopify.toast.show("Failed to connect to API");
    } finally {
      setIsLoading(false);
    }
  };

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
                Your AI Co-founder is currently monitoring the store for 
                identity violations and trend opportunities.
              </Text>
              
              <Button variant="primary" onClick={runScan}>
                Run Identity Vibe Check
              </Button>
            </BlockStack>
          </Card>
        </Layout.Section>

        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h3" variant="headingMd">Analyze URL</Text>
              <TextField
                label="URL"
                value={url}
                onChange={setUrl}
                placeholder="https://example.com"
                autoComplete="off"
              />
              <Button variant="primary" onClick={analyzeUrl} loading={isLoading}>
                Analyze
              </Button>
            </BlockStack>
          </Card>
        </Layout.Section>
        
        <Layout.Section variant="oneThird">
          <Card>
            <BlockStack gap="200">
              <Text as="h3" variant="headingMd">Memory (BackBoard)</Text>
              <Text as="p" tone="subdued">Visual Style: Cyber-Y2K</Text>
              <Text as="p" tone="subdued">Tone: Sassy</Text>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}