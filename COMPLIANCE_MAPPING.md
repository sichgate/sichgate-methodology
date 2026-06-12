# Compliance Mapping

This document maps attack categories to control references in five frameworks:
MITRE ATLAS, the NIST AI Risk Management Framework, the EU AI Act,
OWASP Top 10 for LLM Applications (2025 edition), and ISO/IEC 42001.
The reference subset below covers MITRE ATLAS, NIST AI RMF, and the EU AI Act.
OWASP LLM Top 10 and ISO/IEC 42001 mappings are included in the full production
compliance report produced by a managed assessment.

## How to read this

This mapping is **informational**. It indicates which framework controls a given
category is *relevant to*. It does not constitute a legal determination that a
finding *violates* a specific article, and it is not a substitute for counsel.

This distinction is deliberate. A tool that prints "this output violates EU AI
Act Article 15" is making a legal claim it is not positioned to make. A finding
maps to the article's subject matter; whether it constitutes a violation is a
legal interpretation that depends on the deployment, the jurisdiction, and facts
the tool does not have. We map. We do not adjudicate.

Use these mappings to organize evidence for a review, to point counsel at the
relevant control, and to structure an audit response. Do not hand a raw mapping
to a regulator as a finding of compliance or non-compliance.

## Mapping table

| Category | MITRE ATLAS (technique area) | NIST AI RMF | EU AI Act (relevant subject) |
|---|---|---|---|
| Multi-Turn Escalation | Jailbreak / LLM Prompt Injection | MEASURE 2.6, MEASURE 2.7 | Art. 15 (robustness) |
| Context Manipulation | LLM Prompt Injection (indirect) | MEASURE 2.6 | Art. 15, Art. 10 (data governance) |
| PII / PHI Disclosure | LLM Data Leakage | MEASURE 2.10, MAP 5.1 | Art. 10 (data governance) |
| System Prompt Extraction | LLM Meta Prompt Extraction | MEASURE 2.7 | Art. 15 |
| Medical Misinformation | LLM Harmful Content Generation | MEASURE 2.11 | Art. 9 (risk management) |
| Demographic / Clinical Bias | (cross-cuts) | MEASURE 2.11, GOVERN 4.1 | Art. 10.3 (bias examination) |
| Prompt Injection (Direct) | LLM Prompt Injection | MEASURE 2.6 | Art. 15 |
| Robustness / Signal Handling | LLM Prompt Injection | MEASURE 2.7 | Art. 15 |

The production implementation maps across 43 ATLAS technique constants spanning
8 tactic areas. The table above is the reference subset that corresponds to the
example probes shipped in this repository.

## Versioning

Framework references drift. The EU AI Act implementing acts, the NIST RMF
profile updates, and ATLAS technique revisions all change over time. Each run
records the framework versions the mapping was generated against, so an old
report can be read against the framework as it stood when the report was made.
A mapping with no version stamp is not trustworthy, and the runner does not
produce one.
