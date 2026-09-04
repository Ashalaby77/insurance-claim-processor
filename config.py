"""
config.py — central settings for the claim processor.
Keeping settings in one place means we never hunt through code to change a value.
"""

# The S3 bucket where claim documents live
BUCKET_NAME = "claim-documents-poc-sha"

# AWS region (Bedrock + your bucket are in us-east-1)
REGION = "us-east-1"

# Model IDs on Amazon Bedrock.
# Haiku = fast + cheap (our default for the PoC).
# Sonnet = smarter but pricier (we compare against it in Step 4).
HAIKU_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
SONNET_MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

# The model the processor uses by default
DEFAULT_MODEL = HAIKU_MODEL
