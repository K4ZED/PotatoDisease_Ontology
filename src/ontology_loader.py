from rdflib import Graph
import os

def load_graph():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(project_dir, "knowledge", "PotatoDisease.ttl")
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph
