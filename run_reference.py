#!/usr/bin/env python3
"""SichGate reference runner.

Run the open probe subset against any OpenAI-compatible endpoint and write a
report with the integrity score, verdict, and the SAFETY_MISALIGNMENT /
CAPABILITY_LIMITATION / NOT_APPLICABLE breakdown.

Example:

    export SICHGATE_BASE_URL="http://localhost:8000/v1"
    python run_reference.py --model "Qwen/Qwen2-1.5B-Instruct" \
        --probes probes/ --temperature 0.0 --context-window 32768 \
        --out results/my_run.json

No numbers are committed to this repository. You generate them.
"""

import argparse
import json
import sys
from dataclasses import asdict

from sichgate_reference.models import OpenAICompatibleClient
from sichgate_reference.classifier import JudgeClassifier
from sichgate_reference.runner import load_probes, run_probe, score


def main():
    ap = argparse.ArgumentParser(description="SichGate reference runner")
    ap.add_argument("--model", required=True, help="Target model name")
    ap.add_argument("--probes", default="probes/", help="Probe file or directory")
    ap.add_argument("--base-url", default=None, help="OpenAI-compatible base URL")
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--context-window", type=int, default=8192,
                    help="Target model context window, in tokens, for the guard")
    ap.add_argument("--judge-model", default=None,
                    help="Judge model name. Defaults to the target model.")
    ap.add_argument("--out", default="results/run.json")
    args = ap.parse_args()

    model = OpenAICompatibleClient(
        model=args.model, base_url=args.base_url, api_key=args.api_key,
        temperature=args.temperature, context_window=args.context_window,
    )
    judge_client = OpenAICompatibleClient(
        model=args.judge_model or args.model, base_url=args.base_url,
        api_key=args.api_key, temperature=0.0, context_window=args.context_window,
    )
    judge = JudgeClassifier(judge_client)

    probes = load_probes(args.probes)
    print(f"Loaded {len(probes)} probes. Target: {args.model} "
          f"(ctx {args.context_window}, temp {args.temperature})", file=sys.stderr)

    results = []
    for p in probes:
        r = run_probe(p, model, judge)
        results.append(r)
        if not r.is_applicable():
            flag = "N/A (guard)"
        elif r.passed:
            flag = "PASS"
        else:
            flag = f"FAIL/{r.failure_type.value}/{r.severity.value}"
        print(f"  {p.id:10s} {flag}", file=sys.stderr)

    summary = score(results)
    report = {
        "model": args.model,
        "temperature": args.temperature,
        "context_window": args.context_window,
        "judge_model": args.judge_model or args.model,
        "methodology": "sichgate-reference-v1.0",
        "summary": summary,
        "results": [asdict(r) for r in results],
    }
    with open(args.out, "w") as fh:
        json.dump(report, fh, indent=2, default=str)

    print(f"\nIntegrity score: {summary['integrity_score']}/100", file=sys.stderr)
    print(f"Verdict: {summary['verdict']}", file=sys.stderr)
    print(f"Report written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
