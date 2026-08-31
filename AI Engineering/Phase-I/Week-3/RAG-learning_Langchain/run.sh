#!/usr/bin/env bash
set -euo pipefail

# Bootstrap virtualenv and install deps, then run a demo RAG step
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

echo "Running example: step5_simple_rag.py"
python src/step5_simple_rag.py
