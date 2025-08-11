# langgraph/config.py
import os
from pathlib import Path

# --- 1️⃣  Allow remote Ollama URL via env var or fallback -----------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://desktop.gentoo-gecko.ts.net:11434")
MODEL_NAME  = os.getenv("MODEL_NAME", "gpt-oss:20b")   # choose the model you have on Ollama
MAX_TOKENS  = int(os.getenv("MAX_TOKENS", 8192))

# Where the resulting Turtle file will be written
OUTPUT_TTL = Path("output/skos_concept_scheme.ttl")
OUTPUT_TTL.parent.mkdir(parents=True, exist_ok=True)