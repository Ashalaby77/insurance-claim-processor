"""
rag.py — a SIMPLE Retrieval Augmented Generation component.

The RAG pattern has three parts:
  1. RETRIEVE  - find the policy info relevant to this claim
  2. AUGMENT   - add that info to the prompt
  3. GENERATE  - the model answers using the retrieved info

Here we RETRIEVE using simple keyword matching. In a full production system you would
instead EMBED the text into vectors and do SIMILARITY SEARCH in a vector store
(e.g. Amazon OpenSearch, or let Bedrock Knowledge Bases handle it). The *pattern* is
identical - only the retrieval mechanism changes.
"""

import json
import os

# Load the policy "knowledge base" once
_policy_path = os.path.join(os.path.dirname(__file__), "..", "policy_docs", "policies.json")
with open(_policy_path) as f:
    _POLICIES = json.load(f)["policies"]


def retrieve_policies(claim_text, top_k=2):
    """
    RETRIEVE step: score each policy by how many of its keywords appear in the claim,
    and return the top_k most relevant ones.

    (In full RAG this is where embeddings + vector similarity search would go.)
    """
    claim_lower = claim_text.lower()
    scored = []
    for policy in _POLICIES:
        score = sum(1 for kw in policy["keywords"] if kw in claim_lower)
        if score > 0:
            scored.append((score, policy))

    # Sort by score (highest first) and take the top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [policy for score, policy in scored[:top_k]]


def build_context(policies):
    """AUGMENT step: format the retrieved policies into text for the prompt."""
    if not policies:
        return "No specific policy information found."
    return "\n\n".join(f"[{p['id']}]\n{p['text']}" for p in policies)
