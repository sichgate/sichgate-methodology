# Threat Model

This document states what the SichGate methodology assumes about the attacker,
the deployment, and the model, and what it deliberately does not cover. Stating
this is the difference between a methodology and a marketing claim.

## The deployment we are modeling

A small language model, 1.5B to 8B parameters, quantized to 4-bit or 8-bit
precision, deployed close to the user. Examples: a clinical decision-support
assistant on an edge device in a facility with no reliable internet, a triage
chatbot embedded in a patient-facing portal, an on-prem model in a regulated
environment where data cannot leave the building.

These deployments share three properties that academic jailbreak research
usually assumes away:

1. The model is quantized. Alignment learned at full precision degrades when
   weights are rounded. A model that refuses correctly as a 16-bit checkpoint
   does not necessarily refuse correctly at 4-bit.
2. The users are non-experts with unlimited query access. Patients, clinicians,
   intake staff. They are not running attack frameworks. They are typing.
3. The cost of a single bad output is high and sometimes legally reportable.
   A PII disclosure can trigger a breach notification. A confident piece of
   medical misinformation can reach a patient.

## The attacker we are modeling

Zero-knowledge, black-box, interactive.

- **No weights.** The attacker cannot read or modify model parameters.
- **No gradients.** The attacker cannot compute loss gradients or run
  gradient-guided suffix search.
- **No internal access.** No logit access, no activation steering, no fine-tuning.
- **What they have:** a text interface, patience, and the ability to take many
  turns in a conversation.

This is the patient clinician with a keyboard. It is also, importantly, the
accidental attacker: the well-meaning user who phrases a request in a way that
walks the model past a boundary it should have held.

## What this methodology does NOT cover

We are explicit about this because a methodology that hides its limits is worse
than useless.

- **Gradient-based attacks** (GCG, AutoDAN, and successors). These require weight
  access and achieve higher attack success rates against aligned models. They
  represent an upper bound on risk. We measure a lower bound.
- **Adversarial suffix generation.** Out of scope for the same reason.
- **Activation steering and representation engineering.** Requires internal access.
- **Supply-chain attacks on the model artifact itself** (poisoned checkpoints,
  malicious serialization). Real, important, and a different tool's job.

If your threat model includes an attacker with weight access, this methodology
is necessary but not sufficient. Use it alongside gradient-based tooling, not
instead of it.

## Why the lower bound is the useful bound

Most production incidents are not GCG suffixes. They are a real person, with no
adversarial intent or with very ordinary adversarial intent, finding that the
model does the wrong thing when asked plainly, asked twice, or asked sideways.
The floor is where the incidents are. Measuring the floor reliably, across the
quantization stages a model actually ships in, is the gap this methodology fills.

The ceiling matters too. We just do not pretend to measure it.
