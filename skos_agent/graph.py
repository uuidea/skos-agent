# skos_agent/graph.py

from langgraph.graph import StateGraph
from typing import Dict, Any

# Import all node functions
from skos_agent.nodes.read_document import read_document
from skos_agent.nodes.split_text import split_text
from skos_agent.nodes.extract_concepts import extract_concepts
from skos_agent.nodes.rank_concepts import rank_concepts
from skos_agent.nodes.generate_skos import generate_skos
from skos_agent.nodes.write_ttl import write_ttl

def create_agent():
    graph = StateGraph(dict)

    # Define nodes
    graph.add_node("read", read_document)
    graph.add_node("split", split_text)
    graph.add_node("extract", extract_concepts)
    graph.add_node("rank", rank_concepts)
    graph.add_node("generate", generate_skos)
    graph.add_node("write", write_ttl)

    # Entry point
    graph.set_entry_point("read")

    # Flow:
    graph.add_edge("read", "split")
    graph.add_edge("split", "extract")
    graph.add_edge("extract", "rank")
    graph.add_edge("rank", "generate")
    graph.add_edge("generate", "write")

    return graph.compile()