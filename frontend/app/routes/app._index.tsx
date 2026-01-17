import {
  Button,
  Card,
  Layout,
  Page,
  Text,
  BlockStack,
  TextField,
  InlineStack,
  Badge,
  Box,
  SkeletonBodyText,
  Divider,
  Icon,
} from "@shopify/polaris";
import {
  SearchIcon,
  MagicIcon, // Swapped SparklesIcon for this
  CheckIcon,
  AlertCircleIcon,
  ClockIcon
} from "@shopify/polaris-icons";
import { TitleBar } from "@shopify/app-bridge-react";
import { useState } from "react";
import { ManifestoWidget } from "../components/manifest_widget";

export default function Index() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isComparing, setIsComparing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);
  const [comparisonResult, setComparisonResult] = useState<string | null>(null);

  const analyzeUrl = async () => {
    if (!url) {
      shopify.toast.show("Please enter a video ID");
      return;
    }

    setIsLoading(true);
    setAnalysisResult(null);
    setComparisonResult(null);
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
        setAnalysisResult(data.data?.analysis || JSON.stringify(data, null, 2));
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

  const compareToManifesto = async () => {
    if (!analysisResult) {
      shopify.toast.show("No analysis result to compare");
      return;
    }

    setIsComparing(true);
    setComparisonResult(null);
    try {
      const response = await fetch("/api/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          manifesto: "", 
          summary: analysisResult
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Comparison Response:", data);
        setComparisonResult(data.comparison || JSON.stringify(data, null, 2));
        shopify.toast.show("Comparison complete!");
      } else {
        shopify.toast.show("Comparison request failed");
      }
    } catch (error) {
      console.error("Error calling compare API:", error);
      shopify.toast.show("Failed to connect to API");
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <Page fullWidth>
      <TitleBar title="Command Center" />
      
      <BlockStack gap="800">
        <Layout>
          <Layout.Section>
              <ManifestoWidget />
          </Layout.Section>
        </Layout>

        {/* Main Intelligence Interface */}
        <Layout>
          <Layout.Section variant="oneThird">
            <Card>
              <BlockStack gap="500">
                <BlockStack gap="200">
                  <Text as="h2" variant="headingMd">Intelligence Source</Text>
                  <Text as="p" variant="bodySm" tone="subdued">
                    Input a target URL to extract insights and align with brand manifesto.
                  </Text>
                </BlockStack>
                
                <Box paddingBlockEnd="200">
                    <TextField
                    label="Resource URL"
                    labelHidden
                    value={url}
                    onChange={setUrl}
                    placeholder="https://youtube.com/watch?v=..."
                    autoComplete="off"
                    prefix={<Icon source={SearchIcon} />}
                    clearButton
                    onClearButtonClick={() => setUrl("")}
                    disabled={isLoading}
                    />
                </Box>

                <Button 
                    variant="primary" 
                    size="large"
                    onClick={analyzeUrl} 
                    loading={isLoading}
                    icon={MagicIcon}
                    fullWidth
                >
                    Analyze Signal
                </Button>

                {isLoading && (
                    <Box paddingBlock="400">
                        <BlockStack gap="200">
                            <SkeletonBodyText lines={3} />
                        </BlockStack>
                    </Box>
                )}
              </BlockStack>
            </Card>
            
            <Box paddingBlockStart="400">
                <BlockStack gap="200" inlineAlign="center">
                    <Badge tone="info" icon={ClockIcon}>Last scan: Just now</Badge>
                </BlockStack>
            </Box>
          </Layout.Section>

          {/* Results Area */}
          <Layout.Section>
            <BlockStack gap="400">
                {!analysisResult && !isLoading && (
                    <Card>
                        <Box minHeight="300px" padding="1000">
                          <BlockStack align="center" inlineAlign="center" gap="400">
                              <Box background="bg-surface-secondary" padding="300" borderRadius="full">
                                  <Icon source={SearchIcon} tone="subdued" />
                              </Box>
                              <Text as="p" variant="headingSm" tone="subdued">Awaiting Intelligence</Text>
                          </BlockStack>
                        </Box>
                    </Card>
                )}

                {analysisResult && (
                <Card>
                    <BlockStack gap="400">
                        <InlineStack align="space-between">
                            <InlineStack gap="200">
                                <Icon source={CheckIcon} tone="success"/>
                                <Text as="h3" variant="headingMd">Signal Analysis</Text>
                            </InlineStack>
                            <Badge tone="success">Processed</Badge>
                        </InlineStack>
                        
                        <Divider />
                        
                        <Box padding="400" background="bg-surface-secondary" borderRadius="200">
                            <Text as="p" variant="bodyMd" fontWeight="medium">{analysisResult}</Text>
                        </Box>

                        <InlineStack align="end">
                            <Button 
                                onClick={compareToManifesto} 
                                icon={MagicIcon}
                                disabled={isComparing}
                                loading={isComparing}
                            >
                                Compare to Manifesto
                            </Button>
                        </InlineStack>
                    </BlockStack>
                </Card>
                )}

                {comparisonResult && (
                <Card>
                    <BlockStack gap="400">
                        <InlineStack gap="200">
                            <Icon source={AlertCircleIcon} tone="magic"/>
                            <Text as="h3" variant="headingMd">Manifesto Alignment</Text>
                        </InlineStack>
                        <Divider />
                        <Text as="p">{comparisonResult}</Text>
                    </BlockStack>
                </Card>
                )}
            </BlockStack>
          </Layout.Section>
        </Layout>
      </BlockStack>
    </Page>
  );
}