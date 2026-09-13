"""config.py — central settings for the claim processor."""

# The S3 bucket where claim documents live (change to your bucket name)
BUCKET_NAME = "claim-documents-poc-sha"

# AWS region
REGION = "us-east-1"

# Model IDs on Amazon Bedrock (cross-region inference profiles, note the "us." prefix).
# Haiku = fast + cheap (default). Sonnet = smarter, used for comparison.
HAIKU_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
SONNET_MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

DEFAULT_MODEL = HAIKU_MODEL
