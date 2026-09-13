"""
compare_models.py — run the same document through two models and compare
latency, JSON validity, and output. Produces the 'findings' for model right-sizing.
"""
import boto3
import time
import config
from prompt_manager import PromptManager
from model_invoker import invoke
from validator import validate_json

s3 = boto3.client("s3", region_name=config.REGION)
prompts = PromptManager()


def run_one_model(document_text, model_id):
    start = time.time()
    prompt = prompts.get("extract_info", document_text=document_text)
    raw_output = invoke(prompt, model_id=model_id, temperature=0.0)
    elapsed = time.time() - start
    is_valid, parsed = validate_json(raw_output)
    return {
        "model": model_id,
        "time_seconds": round(elapsed, 2),
        "valid_json": is_valid,
        "output_length": len(raw_output),
        "extracted": parsed if is_valid else raw_output,
    }


def compare(bucket, key, models):
    print(f"Reading s3://{bucket}/{key} ...\n")
    obj = s3.get_object(Bucket=bucket, Key=key)
    document_text = obj["Body"].read().decode("utf-8")
    results = []
    for model_id in models:
        print(f"Running {model_id.split('.')[-1][:20]} ...")
        results.append(run_one_model(document_text, model_id))
    return results


if __name__ == "__main__":
    results = compare(config.BUCKET_NAME, "claims/claim1.txt",
                     [config.HAIKU_MODEL, config.SONNET_MODEL])
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)
    for r in results:
        print(f"\nModel: {r['model']}")
        print(f"  Time:        {r['time_seconds']} seconds")
        print(f"  Valid JSON:  {r['valid_json']}")
        print(f"  Output size: {r['output_length']} chars")
        name = r['extracted'].get('claimant_name', 'N/A') if r['valid_json'] else 'parse failed'
        print(f"  Claimant:    {name}")
    fastest = min(results, key=lambda x: x["time_seconds"])
    print("\n" + "-" * 60)
    print(f"Fastest: {fastest['model'].split('.')[-1][:20]} ({fastest['time_seconds']}s)")
    print("-" * 60)
