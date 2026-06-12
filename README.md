# SichGate Methodology (Reference Edition)

This repository is the open, reproducible reference for the SichGate adversarial
evaluation methodology for small language models (SLMs). It contains the full
attack taxonomy, the severity rubric with numeric thresholds, the annotation
guidelines used to classify model outputs, a runnable subset of probes, and a
runner you can point at any OpenAI-compatible endpoint to reproduce a result
yourself.

It is a reference edition on purpose. The methodology is open so you can inspect
it, run it, and reproduce a number. The production corpus and the differential
engine are not here. See [What is and is not in this repository](#what-is-and-is-not-in-this-repository).

## Why this exists

Most published "AI red-team methodologies" are claims without artifacts. You get
a taxonomy table and a failure rate, and no way to check either. That is not a
methodology, it is a press release.

This repository is the opposite. Every category is defined. Every severity level
has a numeric threshold. Every example probe ships with its full configuration,
its expected behavior, and the rule used to judge the response. The runner
executes. If you want to know whether the method produces the result it claims,
you run it and find out.

## Quickstart

```bash
pip install -r requirements.txt

# Point at any OpenAI-compatible endpoint (vLLM, Ollama, TGI, a hosted API).
export SICHGATE_BASE_URL="http://localhost:8000/v1"
export SICHGATE_API_KEY="not-needed-for-local"

python run_reference.py \
  --model "Qwen/Qwen2-1.5B-Instruct" \
  --probes probes/ \
  --temperature 0.0 \
  --out results/my_run.json
```

The runner sends each probe (single or multi-turn), captures the response, applies
the documented classifier, and writes a report with the `SAFETY_MISALIGNMENT` /
`CAPABILITY_LIMITATION` / `NOT_APPLICABLE` breakdown. A template for what a
completed run looks like is in [`results/EXAMPLE_RUN_TEMPLATE.md`](results/EXAMPLE_RUN_TEMPLATE.md).

No reproduced numbers are committed to this repository. The point is that you
produce them. If a number appears here, it is in a file you generated.

## What is and is not in this repository

| In this repository (open) | In the SichGate product (proprietary) |
|---|---|
| Full attack taxonomy: 32 categories, 8 tactic areas | The full probe corpus (154+ probes) |
| Severity rubric S1 through S4 with numeric thresholds | Quantization-aware safety drift detection (differential testing across base, fine-tuned, and quantized stages) |
| Annotation guidelines and the classification process | Managed assessment delivery and reporting |
| 13 example probes with full configs | Orchestration, run history, scoring pipeline |
| A runnable reference runner and classifier | Managed assessment service (tier issuance, registry listing) |
| Certification tier thresholds (`compute_tier()` in `sichgate_reference/certification.py`) | The public model registry |
| Compliance framework mapping (informational) | |

This split is deliberate and it is the same split every credible security product
makes. The method is inspectable. The corpus is not, for the same reason a
penetration testing firm does not publish its client findings. Open methodology,
proprietary implementation.

## Scope and threat model

This methodology evaluates **black-box, zero-knowledge** adversarial behavior:
no model weights, no gradients, no adversarial suffix generation. The realistic
attacker against a 4-bit SLM running on an air-gapped clinical device is a
non-expert with a keyboard and unlimited queries, not an attacker running
AutoDAN against weights they do not have.

Gradient-based attacks achieve higher attack success rates and represent an
upper bound on risk. We do not claim to cover them, and we say so in
[`THREAT_MODEL.md`](THREAT_MODEL.md). This methodology measures the floor: what
breaks when an ordinary user pushes on a deployed, quantized model. The floor is
where most production incidents actually live.

## The thing the method is actually for

Safety behavior learned during alignment does not survive quantization cleanly.
A model that refuses correctly at full precision can drift when its weights are
rounded to 4-bit integers. Measuring that drift across base, fine-tuned, and
quantized stages is what the SichGate product does. This reference edition gives
you the taxonomy and severity machinery that the drift measurement sits on top
of, so you can see how a single-stage evaluation works before deciding whether
the cross-stage version is worth paying for.

## Repository layout

```
README.md                               This file.
THREAT_MODEL.md                         Scope, assumptions, what is out of scope and why.
TAXONOMY.md                             32 categories across 8 tactic areas.
SCORING_METHODOLOGY.md                  S1–S4 severity, integrity score, and certification tiers.
ANNOTATION_GUIDELINES.md               How outputs are classified. Edge cases. Agreement process.
COMPLIANCE_MAPPING.md                  Informational mapping to ATLAS, NIST AI RMF, EU AI Act.
probes/                                13 example probes with full configs.
sichgate_reference/
  __init__.py
  schema.py                            Probe and Result data structures; FailureType, Severity enums.
  certification.py                     compute_tier() and compute_gate() — the only place threshold logic lives.
  classifier.py                        Refusal heuristic and JudgeClassifier.
  models.py                            Model client interface and MockClient.
  runner.py                            Probe execution, scoring, and result aggregation.
tests/
  test_certification.py               Pytest suite for compute_tier() and compute_gate().
run_reference.py                       Entry point.
results/                               Run output template. You fill this by running.
```

## Citing

If you use this methodology, cite the underlying research:

> Moshenets, P. "Safety as a Secondary Objective: Systematic Adversarial
> Evaluation of Small Language Models in High-Stakes Deployments." 2026.

## License

The methodology, taxonomy, severity rubric, and example probes in this repository
are released under the terms in [`LICENSE`](LICENSE). The SichGate name and the
production implementation are not licensed here.
