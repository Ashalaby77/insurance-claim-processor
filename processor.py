"""
processor.py — core document processor, now WITH a RAG coverage assessment.
Workflow: read -> extract -> validate -> RETRIEVE policies (RAG) -> assess coverage -> summarize.
"""

import boto3
import json
import config
from prompt_manager import PromptManager
from model_invoker import invoke
from validator import validate_json, check_required_fields
from rag import retrieve_policies, build_context

s3 = boto3.client("s3", region_name=config.REGION)
prompts = PromptManager()

REQUIRED_FIELDS = [
    "claimant_name", "policy_number", "incident_date",
    "claim_amount", "incident_description",
]


def process_document(bucket, key, model_id=config.DEFAULT_MODEL):
    print(f"Reading s3://{bucket}/{key} ...")
    obj = s3.get_object(Bucket=bucket, Key=key)
    document_text = obj["Body"].read().decode("utf-8")

    print("Extracting information ...")
    extract_prompt = prompts.get("extract_info", document_text=document_text)
    raw_extraction = invoke(extract_prompt, model_id=model_id, temperature=0.0)

    print("Validating extracted data ...")
    is_valid, result = validate_json(raw_extraction)
    if is_valid:
        problems = check_required_fields(result, REQUIRED_FIELDS)
        extracted_info = result
        validation_status = "valid" if not problems else f"issues: {problems}"
    else:
        extracted_info = raw_extraction
        validation_status = result

    # --- RAG STEP: retrieve relevant policy info based on the claim text ---
    print("Retrieving relevant policies (RAG) ...")
    relevant_policies = retrieve_policies(document_text, top_k=2)
    policy_context = build_context(relevant_policies)
    retrieved_ids = [p["id"] for p in relevant_policies]

    print("Assessing coverage using retrieved policies ...")
    coverage_prompt = prompts.get(
        "assess_coverage",
        policy_context=policy_context,
        claim_info=json.dumps(extracted_info),
    )
    coverage_assessment = invoke(coverage_prompt, model_id=model_id, temperature=0.3)

    print("Generating summary ...")
    summary_prompt = prompts.get("generate_summary", extracted_info=json.dumps(extracted_info))
    summary = invoke(summary_prompt, model_id=model_id, temperature=0.5)

    return {
        "model_used": model_id,
        "validation_status": validation_status,
        "extracted_info": extracted_info,
        "retrieved_policies": retrieved_ids,
        "coverage_assessment": coverage_assessment.strip(),
        "summary": summary.strip(),
    }


if __name__ == "__main__":
    result = process_document(bucket=config.BUCKET_NAME, key="claims/claim1.txt")
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(json.dumps(result, indent=2))
