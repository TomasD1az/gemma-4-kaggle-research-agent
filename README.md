# gemma4

## Project Catalyst (MVP Phase 1)

This repository provides an offline-first autonomous research lab scaffold for Gemma 4 on a single RTX 4090.

### Structure

- `agent/`: Planner/Executor orchestration (`Think-Code-Verify` loop).
- `sandbox/`: Local Python subprocess sandbox.
- `knowledge/`: Local-first ChromaDB + sentence-transformers RAG helpers.
- `output/`: Generated artifacts (plots, CSVs, summaries).
- `app.py`: Streamlit dashboard for monologue + artifacts + sovereignty status.
- `finetune.py`: Unsloth LoRA/QLoRA template for scientific adaptation.

### Running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Notes on model loading (4090 focus)

- Load Gemma 4 31B (Q4_K_M) through `llama-cpp-python` with maximum practical `n_gpu_layers`.
- Run executor model (E2B/E4B) as a smaller secondary process.
- Keep combined footprint near ~20GB VRAM to preserve workspace and KV cache headroom.
