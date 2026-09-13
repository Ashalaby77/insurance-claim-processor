"""
prompt_manager.py — keeps all prompt templates in one place.
Mirrors Amazon Bedrock's "Prompt Management" feature (versioned, reusable templates).
"""


class PromptManager:
    def __init__(self):
        self.templates = {
            "extract_info": """Extract the following information from this insurance claim document.
Return ONLY valid JSON (no markdown, no code fences, no extra text) with these exact keys:
claimant_name, policy_number, incident_date, claim_amount, incident_description.

Document:
{document_text}
""",
            "generate_summary": """Based on this extracted claim information, write a concise
2-3 sentence summary of the claim for a claims adjuster.
Return only the summary text, with no headers or markdown.

{extracted_info}
""",
            "assess_coverage": """You are an insurance claims assistant. Using ONLY the policy
information provided below, assess this claim. State whether it appears covered, mention the
relevant deductible and any limits, and note any requirements (like a police report).
Base your answer only on the provided policy info. Keep it to 3-4 sentences.

POLICY INFORMATION:
{policy_context}

CLAIM DETAILS:
{claim_info}
""",
        }

    def get(self, template_name, **kwargs):
        template = self.templates.get(template_name)
        if template is None:
            raise ValueError(f"Template '{template_name}' not found")
        return template.format(**kwargs)
