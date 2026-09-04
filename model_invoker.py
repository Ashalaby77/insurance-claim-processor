"""
model_invoker.py — one clean, reusable way to call Amazon Bedrock.

Why: every part of the app that needs the model uses this single function,
so the Bedrock/Converse details live in exactly one place.
"""

import boto3
import config

_bedrock = boto3.client("bedrock-runtime", region_name=config.REGION)


def invoke(prompt_text, model_id=config.DEFAULT_MODEL, temperature=0.0, max_tokens=1000):
    """
    Send one prompt to a Bedrock model via the Converse API and return the text reply.

    prompt_text : the instruction/question
    model_id    : which model (defaults to our Haiku default)
    temperature : 0.0 = precise/repeatable, higher = more creative
    max_tokens  : cap on response length
    """
    response = _bedrock.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt_text}]}],
        inferenceConfig={"temperature": temperature, "maxTokens": max_tokens},
    )
    return response["output"]["message"]["content"][0]["text"]
