# skos_agent/nodes/extract_concepts.py
import json
from typing import Dict, List, Any

from langchain_core.messages import HumanMessage
import ollama
from skos_agent.config import OLLAMA_URL, MODEL_NAME, MAX_TOKENS

def extract_concepts(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calls Ollama to extract all concept candidates from the text chunks.
    Returns a list of concept objects with raw labels.
    """
    chunks = context["chunks"]
    print(len(chunks))

    client = ollama.Client(OLLAMA_URL)

    all_concepts: List[Dict[str, Any]] = []

    for i, chunk in enumerate(chunks):
        prompt = (
            "You are a semantic analyst. Given the following text chunk, "
            "extract the *most important* concepts and for each concept provide:\n"
            "- a short label (1 word)\n" #(preferably 1 and max 3 words)\n"
            "- a concise definition (<= 30 words)\n"
            "- an example sentence (optional)\n"
            "- a scope note if needed (optional)\n"
            "Return a JSON array of objects. If no concept is found, return an empty array.\n\n"
            f"Text chunk ({i+1}/{len(chunks)}):\n{chunk}\n"
        )
 
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            options={"temperature": 0.2, "max_tokens": MAX_TOKENS},
        )

        try:
            content = response["message"]["content"].strip()

            # ---- NEW: Strip ```json fences (if present) ----
            if content.startswith("```"):
                # Find the first newline after the opening fence
                nl_idx = content.find("\n", 3)
                if nl_idx != -1:
                    content = content[nl_idx + 1 :].strip()
                else:
                    content = content[3:].strip()
                # Remove the closing fence if it exists
                if content.endswith("```"):
                    content = content[:-3].strip()

            # Optional: strip leading/trailing quotes that some models add
            content = content.strip('"')

            # ---- END OF NEW SECTION ----

            data = json.loads(content)

            # Accept both raw arrays and objects with a "concepts" key
            if isinstance(data, list):
                all_concepts.extend(data)
                print(len(all_concepts))
            elif isinstance(data, dict) and "concepts" in data:
                all_concepts.extend(data["concepts"])
            else:
                print(f"[WARN] Unexpected format from Ollama: {data!r}")

        except Exception as e:
            # Log parsing failure but keep processing remaining chunks
            print(f"[ERROR] Failed to parse Ollama output: {e}")
    print(f"done extracting {len(all_concepts)} concepts")
    return {"concepts": all_concepts}
