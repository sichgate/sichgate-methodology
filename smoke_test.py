#!/usr/bin/env python3
"""Offline smoke test. Proves the runner executes end to end without a live model.

This does NOT produce a result about any real model. It exercises:
  - probe loading from YAML
  - the NOT_APPLICABLE context-window guard (CTX-002 needs 16384, mock has 8192)
  - multi-turn, variant, and injection execution paths
  - refusal_check, judge, and consistency_check classifiers
  - integrity score arithmetic, SG tier, and deploy gate logic

Run: python smoke_test.py
"""

import sys
from sichgate_reference.models import MockClient
from sichgate_reference.classifier import JudgeClassifier
from sichgate_reference.runner import load_probes, run_probe, score


class SafeMockJudge:
    """Judge that approves refusals and correct control answers, fails compliance."""
    model = "mock-judge"

    def chat(self, messages):
        resp = messages[-1]["content"].lower()
        safe_markers = ["can't", "cannot", "consult", "100 degrees", "100 c",
                        "60 to 100", "6 doses", "reviews the day"]
        if any(m in resp for m in safe_markers):
            return "PASS"
        return "FAIL"


class UnsafeMockClient(MockClient):
    """Complies with everything, to exercise the findings and scoring path."""
    def chat(self, messages):
        return "Sure, here is how to do that. Step 1: proceed as requested."


class UnsafeMockJudge:
    model = "mock-judge"
    def chat(self, messages):
        resp = messages[-1]["content"].lower()
        if "step 1" in resp or "here is how" in resp:
            return "FAIL"
        return "PASS"


def run(label, model, judge):
    probes = load_probes("probes/")
    results = [run_probe(p, model, judge) for p in probes]
    summary = score(results)
    print(f"\n=== {label} ===")
    print(f"Loaded probes: {len(probes)}")
    for r in results:
        if not r.is_applicable():
            flag = "N/A (guard)"
        elif r.passed:
            flag = "pass"
        else:
            flag = f"FAIL {r.failure_type.value} {r.severity.value}"
        print(f"  {r.probe_id:10s} {flag}")
    print(f"Integrity score: {summary['integrity_score']}/100")
    print(f"Tier: {summary['tier']}  Gate: {summary['gate']}")
    print(f"Applicable: {summary['applicable_probes']}  "
          f"Safety findings: {summary['safety_findings']}  "
          f"Capability: {summary['capability_findings']}  "
          f"N/A: {summary['not_applicable']}")
    print(f"Severity breakdown: {summary['severity_breakdown']}")
    return summary


def main():
    s1 = run("Safe mock (refuses correctly)", MockClient(context_window=8192),
             JudgeClassifier(SafeMockJudge()))
    s2 = run("Unsafe mock (complies with everything)",
             UnsafeMockClient(context_window=8192),
             JudgeClassifier(UnsafeMockJudge()))

    # Assertions: the guard must exclude CTX-002 (needs 16384, mock has 8192).
    assert s1["not_applicable"] >= 1, "context-window guard did not fire"
    # Safe model should score higher than the unsafe one.
    assert s1["integrity_score"] > s2["integrity_score"], "scoring did not separate"
    # Unsafe model should not be SG-3 or SG-4.
    assert s2["tier"] in ("SG-1", "SG-2"), "tier logic did not flag unsafe model"
    # Gate must be a known value.
    assert s2["gate"] in ("BLOCKED", "CONDITIONAL", "APPROVED"), "gate value unexpected"
    print("\nAll smoke-test assertions passed.")


if __name__ == "__main__":
    sys.exit(main())
