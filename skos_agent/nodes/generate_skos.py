# langgraph/nodes/generate_skos.py
from typing import Dict, Any
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS

def generate_skos(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Turn the ranked concept list into a SKOS RDF graph.
    """
    top_concepts = state.get("top_concepts", [])
    g = Graph()
    g.bind("skos", SKOS)
    EX = Namespace("http://example.org/concept/")

    for concept in top_concepts:
        # Build a URI for the concept
        # Replace spaces with underscores (simple sanitisation)
        uri = EX[concept["label"].replace(" ", "_")]

        # Declare the URI as a SKOS concept
        g.add((uri, RDF.type, SKOS.Concept))

        # Add the preferred label
        g.add((uri, SKOS.prefLabel, Literal(concept["label"], lang="en")))

        # Optional: add a definition
        if "definition" in concept:
            g.add((uri, SKOS.definition, Literal(concept["definition"], lang="en")))

        # Optional: add a scope note
        if "scopeNote" in concept:
            g.add((uri, SKOS.scopeNote, Literal(concept["scopeNote"], lang="en")))

    # Naive relationship inference: use positional order
    for i, c1 in enumerate(top_concepts):
        for j, c2 in enumerate(top_concepts):
            if i == j:
                continue
            uri1, uri2 = EX[c1["label"].replace(" ", "_")], EX[c2["label"].replace(" ", "_")]
            # if c1 before c2 → c1 is broader of c2
            if i < j:
                g.add((uri1, SKOS.broader, uri2))
                g.add((uri2, SKOS.narrower, uri1))
            # also add related link
            g.add((uri1, SKOS.related, uri2))

    return {"graph": g}


