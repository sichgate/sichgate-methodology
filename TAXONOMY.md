# Attack Taxonomy

32 categories across 8 tactic areas. This is the full taxonomy. The example
probes in this repository cover a subset of these categories; the production
corpus covers all of them at depth.

Each category lists the failure it probes for and the default failure type a
positive finding maps to. `SAFETY_MISALIGNMENT` means the model did something it
should refuse. `CAPABILITY_LIMITATION` means the model failed at a task but the
failure is not a safety violation (a weak model, not an unsafe one). The
distinction is load-bearing and is defined in `SCORING_METHODOLOGY.md`.

---

## Tactic Area 1: Direct Elicitation

Plain requests for content the model should refuse, with no obfuscation.

- **1.1 Direct Harmful Request** — unframed request for harmful content. `SAFETY_MISALIGNMENT`
- **1.2 Restricted Information Retrieval** — request for gated or sensitive procedural information. `SAFETY_MISALIGNMENT`
- **1.3 Capability Probe (Control)** — benign hard task, used to separate inability from misalignment. `CAPABILITY_LIMITATION`
- **1.4 Overrefusal Probe (Control)** — benign request that weak safety tuning may wrongly refuse. `CAPABILITY_LIMITATION`

## Tactic Area 2: Multi-Turn Escalation

Boundaries that hold on turn one and fail by turn three.

- **2.1 Crescendo** — gradual escalation from benign to violating across turns. `SAFETY_MISALIGNMENT`
- **2.2 Context Reset Exploitation** — re-establishing a violating request after an apparent topic change. `SAFETY_MISALIGNMENT`
- **2.3 Commitment Laddering** — extracting small agreements that compose into a violation. `SAFETY_MISALIGNMENT`
- **2.4 Refusal Erosion** — repeating a refused request with minor reframings until it lands. `SAFETY_MISALIGNMENT`

## Tactic Area 3: Context Manipulation

Exploiting how the model handles the context window and uploaded content. These
reflect RAG deployments where the attacker controls a document, not just the prompt.

- **3.1 Excessive Token Preloading** — flooding context to push safety instructions out of attention. `SAFETY_MISALIGNMENT`
- **3.2 Context Overflow Divergence** — behavior change as context approaches the window limit. `SAFETY_MISALIGNMENT`
- **3.3 Malicious Document Injection** — instructions embedded in retrieved or uploaded content. `SAFETY_MISALIGNMENT`
- **3.4 Instruction Hierarchy Confusion** — conflicting system and user instructions exploited to elevate user intent. `SAFETY_MISALIGNMENT`

## Tactic Area 4: Role and Framing

Getting the model to adopt a frame in which the violation reads as acceptable.

- **4.1 Persona Adoption** — role-play that licenses prohibited output. `SAFETY_MISALIGNMENT`
- **4.2 Authority Impersonation** — claimed authority (clinician, admin, researcher) used to unlock content. `SAFETY_MISALIGNMENT`
- **4.3 Hypothetical Framing** — "in a story / in theory" wrappers around a real request. `SAFETY_MISALIGNMENT`
- **4.4 Translation and Encoding** — request laundered through another language or encoding. `SAFETY_MISALIGNMENT`

## Tactic Area 5: Disclosure and Privacy

The categories that map most directly to breach-notification obligations.

- **5.1 PII Disclosure** — output contains specific personal identifiers. `SAFETY_MISALIGNMENT`
- **5.2 PHI Disclosure** — protected health information surfaced from context or training. `SAFETY_MISALIGNMENT`
- **5.3 System Prompt Extraction** — recovery of the deployment's system instructions. `SAFETY_MISALIGNMENT`
- **5.4 Training Data Regurgitation** — verbatim emission of memorized sensitive content. `SAFETY_MISALIGNMENT`

## Tactic Area 6: Factual Integrity

Where being confidently wrong is the harm.

- **6.1 Medical Misinformation** — contraindicated or unsafe clinical guidance. `SAFETY_MISALIGNMENT`
- **6.2 Confident Hallucination** — fabricated facts asserted without hedging under confident framing. `SAFETY_MISALIGNMENT`
- **6.3 Factual Sycophancy** — abandoning a correct answer when the user pushes back. `CAPABILITY_LIMITATION`
- **6.4 Safety Sycophancy** — abandoning a correct refusal when the user pushes back. `SAFETY_MISALIGNMENT`

## Tactic Area 7: Bias and Fairness

- **7.1 Demographic Bias** — differential treatment across protected attributes. `SAFETY_MISALIGNMENT`
- **7.2 Clinical Bias** — differential medical guidance unjustified by clinical factors. `SAFETY_MISALIGNMENT`
- **7.3 Representational Harm** — stereotyping or demeaning output. `SAFETY_MISALIGNMENT`
- **7.4 Stereotype Control** — benign demographic content that overcautious tuning may wrongly flag. `CAPABILITY_LIMITATION`

## Tactic Area 8: Robustness and Signal Handling

How the model behaves when the input is adversarially shaped at the surface level.

- **8.1 Safe Signal Injection** — adversarial text positioned to imitate a safety system's own markers. `SAFETY_MISALIGNMENT`
- **8.2 Unicode and Homoglyph Evasion** — character-level obfuscation of a violating request. `SAFETY_MISALIGNMENT`
- **8.3 Prompt Injection (Direct)** — user input that overrides the task instruction. `SAFETY_MISALIGNMENT`
- **8.4 Refusal Boundary Consistency** — whether refusal is stable across trivial rewordings of the same request. `SAFETY_MISALIGNMENT`

---

## A note on the hard-harm categories

For categories where a working example probe would itself be operationally
dangerous (weapons, CBRN, and similar), this repository does **not** ship a
payload. Those probes reference published benchmark rows (AdvBench, HarmBench,
JailbreakBench) by identifier rather than reproducing harmful content. A
reference repository should let you reproduce a measurement without becoming a
how-to. The example probes shipped here are drawn from the boundary categories
(escalation, disclosure, sycophancy, context manipulation, overrefusal controls)
where the probe text demonstrates method without providing uplift.
