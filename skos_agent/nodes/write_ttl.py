# skos_agent/nodes/write_ttl.py
import rdflib
from typing import Dict, Any
from skos_agent.config import OUTPUT_TTL

def write_ttl(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Persist the RDF graph to the configured file.
    """
    # The key MUST be exactly 'graph'
    g: rdflib.Graph = context["graph"]

    # Write the Turtle serialization
    with open(OUTPUT_TTL, "wb") as fp:
        fp.write(g.serialize(format="turtle").encode("utf-8"))

    return {"status": f"Written to {OUTPUT_TTL}"}