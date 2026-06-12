# Example Run (Template)

This is a template showing the shape of a run report. The numbers below are
placeholders in angle brackets, not measurements. **No real result is committed
to this repository.** You generate a real one by running:

```bash
export SICHGATE_BASE_URL="http://localhost:8000/v1"
python run_reference.py --model "<your-model>" --probes probes/ \
  --temperature 0.0 --context-window <window> --out results/my_run.json
```

When you run it, `results/my_run.json` will have this structure:

```json
{
  "model": "<model name, e.g. Qwen/Qwen2-1.5B-Instruct>",
  "temperature": 0.0,
  "context_window": <window>,
  "judge_model": "<judge model>",
  "methodology": "sichgate-reference-v1.0",
  "summary": {
    "integrity_score": <0-100>,
    "tier": "<SG-1 | SG-2 | SG-3 | SG-4>",
    "gate": "<BLOCKED | CONDITIONAL | APPROVED>",
    "applicable_probes": <N>,
    "safety_findings": <count>,
    "capability_findings": <count>,
    "not_applicable": <count>,
    "weight_sum": <W>,
    "weight_max": <N*10>,
    "severity_breakdown": {"S4": <n>, "S3": <n>, "S2": <n>, "S1": <n>}
  },
  "results": [ { "probe_id": "...", "failure_type": "...", "severity": "...", "...": "..." } ]
}
```

## Reproducing a published number

If a SichGate report or post cites a number, it should name the model, the
quantization, the temperature, the context window, the judge model, and the
methodology version. With those six things and this repository, you can re-run
and check the number yourself. A cited number that does not name those six
things is not reproducible, and you should treat it as a claim rather than a
measurement. That standard applies to our numbers too.

## Pinning, so a run is reproducible

- Set `--temperature 0.0` for deterministic decoding where the backend supports it.
- Record the exact model revision (HuggingFace commit hash or registry digest),
  not just the model name.
- Record the quantization (for example, `q4_k_m`, `awq-int4`, `gptq-4bit`).
- Use the same judge model and version across runs you intend to compare.

The differential drift measurement (the same probes across base, fine-tuned, and
quantized revisions of one model) is what the SichGate product automates on top
of this. This reference edition gives you one stage. Running it across stages by
hand is possible; doing it as a gated, tracked pipeline is the product.
