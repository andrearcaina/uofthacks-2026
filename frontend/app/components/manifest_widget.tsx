import { useEffect } from "react";
import { useFetcher } from "@remix-run/react";
import {
    Card,
    Button,
    BlockStack,
    Text,
    Banner,
    Box,
    InlineStack,
    Divider,
    Icon,
    SkeletonBodyText,
} from "@shopify/polaris";
import { MagicIcon, FileIcon, WandIcon } from "@shopify/polaris-icons";
import ReactMarkdown from "react-markdown";

export function ManifestoWidget() {
    const fetcher = useFetcher<any>();
    const isLoading = fetcher.state !== "idle";
    const data = fetcher.data;
    const hasManifesto = !!data?.manifesto?.manifesto;

    useEffect(() => {
        if (data?.status === "error") {
        shopify.toast.show("Failed to fetch manifesto", { isError: true });
        }
    }, [data]);

    if (hasManifesto) {
        return (
        <Card>
            <BlockStack gap="400">
                <InlineStack gap="200" align="start">
                    <Box background="bg-surface-success" padding="100" borderRadius="200">
                        <Icon source={FileIcon} tone="success" />
                    </Box>
                    <BlockStack gap="050">
                        <Text as="h3" variant="headingMd">Brand Manifesto</Text>
                        <Text as="p" variant="bodySm" tone="subdued">Core Identity & Guidelines</Text>
                    </BlockStack>
            </InlineStack>
            
            <Divider />
            
            <Box paddingBlock="200">
                <ReactMarkdown
                    components={{
                        h1: ({ children }) => (
                        <Box paddingBlockEnd="400">
                            <Text as="h1" variant="headingXl">{children}</Text>
                            <Divider />
                        </Box>
                        ),
                        h2: ({ children }) => (
                        <Box paddingBlockStart="400" paddingBlockEnd="200">
                            <Text as="h2" variant="headingLg" tone="success">{children}</Text>
                        </Box>
                        ),
                        h3: ({ children }) => (
                        <Box paddingBlockStart="300" paddingBlockEnd="100">
                            <Text as="h3" variant="headingMd">{children}</Text>
                        </Box>
                        ),
                        p: ({ children }) => (
                        <Box paddingBlockEnd="300">
                            <Text as="p" variant="bodyMd" lineHeight="28px">{children}</Text>
                        </Box>
                        ),
                        li: ({ children }) => (
                        <div style={{ marginLeft: "24px", marginBottom: "8px" }}>
                            <Text as="p" variant="bodyMd">• {children}</Text>
                        </div>
                        ),
                        strong: ({ children }) => (
                            <Text as="span" fontWeight="bold" tone="success">{children}</Text>
                        ),
                    }}
                    >
                    {data.manifesto.manifesto}
                </ReactMarkdown>
            </Box>
            </BlockStack>
        </Card>
        );
    }

    if (isLoading) {
        return (
            <Card>
                <BlockStack gap="400">
                    <InlineStack gap="200" align="start">
                        <SkeletonBodyText lines={1} />
                    </InlineStack>
                    <Divider />
                    <Box paddingBlock="400">
                        <SkeletonBodyText lines={6} />
                    </Box>
                </BlockStack>
            </Card>
        )
    }

    return (
        <Banner
        tone="success"
        icon={MagicIcon}
        title="AI Co-founder Active"
        >
        <InlineStack align="space-between" blockAlign="center" gap="400">
            <Text as="p" variant="bodyMd">
            System is currently monitoring store identity violations and trend opportunities.
            </Text>
            
            <fetcher.Form method="post" action="/api/view_manifesto">
                <Button
                    variant="plain"
                    icon={WandIcon}
                    submit
                    loading={isLoading}
                >
                    View Manifesto
                </Button>
            </fetcher.Form>
        </InlineStack>
        </Banner>
    );
}