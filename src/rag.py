"""
rag.py — a SIMPLE Retrieval Augmented Generation component.

The RAG pattern: RETRIEVE relevant info -> AUGMENT the prompt -> GENERATE grounded answer.
Here we RETRIEVE using keyword matching. In a full production system you would instead
EMBED text into vectors and do SIMILARITY SEARCH in a vector store (e.g. Amazon OpenSearch,
or let Bedrock Knowledge Bases handle it). The pattern is identical; only retrieval changes.
"""
import json
import os

_policy_path = os.path.join(os.path.dirname(__file__), "..", "policy_docs", "policies.json")
with open(_policy_path) as f:
    _POLICIES = json.load(f)["policies"]


def retrieve_policies(claim_text, top_k=2):
    """RETRIEVE: score policies by keyword overlap with the claim, return top_k.
    (In full RAG this is where embeddings + vector similarity search would go.)"""
    claim_lower = claim_text.lower()
    scored = []
    for policy in _POLICIES:
        score = sum(1 for kw in policy["keywords"] if kw in claim_lower)
        if score > 0:
            scored.append((score, policy))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [policy for score, policy in scored[:top_k]]


def build_context(policies):
    """AUGMENT: format retrieved policies into text for the prompt."""
    if not policies:
        return "No specific policy information found."
    return "\n\n".join(f"[{p['id']}]\n{p['text']}" for p in policies)
