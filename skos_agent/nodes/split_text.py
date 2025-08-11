# skos_agent/nodes/split_text.py
from typing import Dict, List, Any
from langchain_core.messages import ChatMessage

MAX_CHARS = 8000
DELIMITER = "\n\n"

def split_text(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Splits the document text into chunks that fit the LLM context window.
    """
    # Allow a plain string as input (the error was caused by this case)
    if isinstance(context, str):
        text = context
        meta = {}
    else:
        text = context["text"]
        meta = context.get("meta", {})

    chunks: List[str] = []
    while text:
        if len(text) <= MAX_CHARS:
            chunks.append(text)
            break
        # find a nice split point
        split_at = text.rfind(DELIMITER, 0, MAX_CHARS)
        if split_at == -1:
            split_at = MAX_CHARS
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()

    print("done splitting document")
    return {"chunks": chunks, "meta": meta}
