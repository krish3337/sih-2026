"""
run_evaluation.py — Evaluates the recommendation pipeline on the test queries dataset.
Calculates Precision@1 overall and broken out by language.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from collections import defaultdict

# Import pipeline initialization from our demo script
from run_demo import init_pipeline


def main():
    # Ensure correct encoding on Windows
    sys.stdout.reconfigure(encoding="utf-8")
    
    try:
        pipeline = init_pipeline()
    except Exception as exc:
        print(f"Failed to initialize pipeline: {exc}")
        print("Ensure GEMINI_API_KEY is set in your environment.")
        sys.exit(1)

    try:
        with open("data/test_queries.json", "r", encoding="utf-8") as fh:
            test_queries = json.load(fh)
    except FileNotFoundError:
        print("ERROR: data/test_queries.json not found.")
        sys.exit(1)

    if not test_queries:
        print("No test queries found in data/test_queries.json")
        sys.exit(0)

    print(f"\nStarting evaluation of {len(test_queries)} queries...\n")
    
    total_correct = 0
    language_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    start_time = time.time()
    
    for i, tq in enumerate(test_queries, 1):
        query = tq.get("input_text", "")
        expected_id = tq.get("expected_standard_id", "")
        lang = tq.get("language", "Unknown")
        
        print(f"[{i}/{len(test_queries)}] Query ({lang}): '{query}'")
        
        try:
            # Run through the pipeline
            result = pipeline.recommend(query)
            
            # Extract top standard from primary_recommendations
            primary = result.get("primary_recommendations", [])
            
            # Match on base_id since that's what expected_id likely maps to,
            # or standard_id if exact match is required. We check both to be safe.
            predicted_base = primary[0]["base_id"] if primary else None
            predicted_full = primary[0]["standard_id"] if primary else None
            
            is_correct = (expected_id == predicted_base) or (expected_id == predicted_full)
            
            if is_correct:
                total_correct += 1
                language_stats[lang]["correct"] += 1
                print(f"  ✓ Pass (Predicted: {predicted_base})")
            else:
                print(f"  ✗ Fail (Expected: {expected_id}, Predicted: {predicted_base})")
                
            language_stats[lang]["total"] += 1
            
        except Exception as e:
            print(f"  ! Error evaluating query: {e}")
            language_stats[lang]["total"] += 1

    elapsed = time.time() - start_time
    
    # ── Summary ─────────────────────────────────────────────────────────────
    print("\n" + "="*50)
    print("  EVALUATION RESULTS (Precision@1)")
    print("="*50)
    
    total_queries = len(test_queries)
    p_at_1 = (total_correct / total_queries) * 100 if total_queries > 0 else 0
    print(f"Overall Precision@1: {total_correct}/{total_queries} ({p_at_1:.1f}%)\n")
    
    print("Breakdown by Language:")
    for lang, stats in sorted(language_stats.items()):
        ltotal = stats["total"]
        lcorrect = stats["correct"]
        lp_at_1 = (lcorrect / ltotal) * 100 if ltotal > 0 else 0
        print(f"  - {lang:7s}: {lcorrect}/{ltotal} ({lp_at_1:.1f}%)")
        
    print(f"\nTime taken: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
