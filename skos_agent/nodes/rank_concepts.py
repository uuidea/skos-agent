# skos_agent/nodes/rank_concepts.py

from typing import Dict, Any
from collections import Counter

def rank_concepts(state: Dict[str, Any]) -> Dict[str, Any]:
    concepts = state["concepts"]
    freq = Counter(c["label"] for c in concepts)
    unique_labels = list(dict.fromkeys(c["label"] for c in concepts))
    print(len(unique_labels))
    ranked = sorted(unique_labels, key=lambda l: freq[l], reverse=True)
    top_labels = ranked[:20]
    top_concepts = [c for c in concepts if c["label"] in top_labels]
    print("done ranking")
    return {"top_concepts": top_concepts}