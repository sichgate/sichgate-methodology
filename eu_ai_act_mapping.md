# EU AI Act Compliance Mapping

## Deployer Liability Framework

Under **EU AI Act Article 3**, deployers of high-risk AI systems bear primary
responsibility for ensuring systems comply with the requirements of Chapter III,
Section 2. AI systems deployed in the following contexts fall under the high-risk
categories enumerated in **Annex III**:

- Medical device interfaces and clinical decision support
- Credit scoring and financial risk assessment
- Employment screening
- Customer-facing advisory tools in regulated sectors

A deployer who ships a system without conducting adversarial evaluation cannot
claim that vulnerability responsibility lies with the model vendor. The deployer
is the party whose risk exposure is directly affected by the findings in this
evaluation framework.

**Enforcement deadline:** EU AI Act high-risk requirements apply from **2 August 2026**.
Deployers who cannot produce evaluation records meeting Annex IV documentation
requirements at that date face potential enforcement exposure.

---

## Article-Level Mapping

### Article 9 — Risk Management System

> Deployers must establish and implement a risk management system covering all
> foreseeable risks to health, safety, and fundamental rights throughout the
> system lifecycle.

| Finding | Mapped probe categories |
|---|---|
| Crescendo jailbreak (universal vulnerability) | `alignment_crescendo` |
| Sycophancy reversal of safety-compliance positions | `alignment_sycophancy` (critical probes) |
| Context-window displacement (Llama/Mistral families) | `inf_ctx_etp`, `inf_ctx_cod` |

### Article 10 — Data and Data Governance

> Deployers must implement measures to address reasonably foreseeable risks of
> biased outputs.

| Finding | Mapped probe categories |
|---|---|
| Demographic bias in clinical pain assessment | `bias_fairness` (medical context) |
| Demographic bias in mental health context | `bias_fairness` (mental health context) |
| Fine-tuning-amplified bias (MedGemma-4B) | `bias_fairness` (all dimensions) |

### Article 14 — Human Oversight

> Deployers must implement measures enabling human oversight, including the
> ability to detect and address malfunctions.

| Finding | Mapped probe categories |
|---|---|
| Sycophancy reversal under routine user pressure | `alignment_sycophancy` |
| Competing objectives: helpfulness overrides safety | `alignment_competing_objectives` |
| Alignment consistency drift under paraphrase | `alignment_consistency` |

### Article 15 — Accuracy, Robustness, and Cybersecurity

> Systems must achieve appropriate levels of accuracy, robustness, and
> cybersecurity, and be resilient against attempts by unauthorised third parties
> to alter their use.

| Finding | Mapped probe categories |
|---|---|
| Context-window injection (all models) | `inf_ctx_cwi` |
| Context overflow displacement (Llama/Mistral) | `inf_ctx_cod` |
| Instruction hijacking | `instruction_hijacking` |
| JSON/XML smuggling | `json_xml_smuggling` |
| Payload splitting | `payload_splitting` |
| Multi-turn role-conditioned compliance | `multiturn_rci`, `multiturn_ccm`, `multiturn_tdpe` |

---

## Annex IV — Technical Documentation Requirements

Annex IV specifies the technical documentation that deployers must produce.
The following evaluation outputs map directly to Annex IV requirements:

| Annex IV Section | Required documentation | Provided by SichGate evaluation |
|---|---|---|
| §1 | General description of system and intended purpose | Scope definition, model card |
| §1a | System capabilities and limitations | Failure rate summary, weighted risk score |
| §1e | Hardware requirements and deployment configuration | Quantisation config, inference parameters |
| §2c | Risk management measures implemented | Remediation guidance per finding |
| §2d | Changes made during lifecycle | Differential analysis (base vs. fine-tuned) |
| §2g | Robustness testing results | Full per-category findings table |
| §2h | Cybersecurity measures | Context-window and injection findings |
| §3 | Monitoring and oversight procedures | Consistency and sycophancy findings |
| §5 | Post-market monitoring system | Crescendo and multi-turn findings |

---

## GDPR Article 9 — Special Category Data

Relevant to EU-regulated deployments processing biometric, health, or other
special-category data.

| Finding | Probe |
|---|---|
| Model overrides data protection when helpfulness conflicts | `competing_obj_biometric_data_conflict` (Mistral-7B, critical) |
| Model endorses unauthorised data disclosure | `alignment_sycophancy` (hipaa_compliance probe) |

---

## CycloneDX 1.6 AIBoM

The proprietary implementation (`sichgate-pro`) generates EU AI Act Annex IV
Technical Files with cryptographic attestation in CycloneDX 1.6 AIBoM format.
The open methodology does not include AIBoM generation. Contact
`research@sichgate.com` for access to the proprietary implementation.
