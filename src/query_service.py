from rdflib import Graph

BASE_PREFIX = "http://example.org/potato/"

from rdflib import Graph

def list_diseases(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?disease
    WHERE {
        ?disease rdf:type ?t .
        ?t rdfs:subClassOf* ex:PotatoDisease .
    }
    ORDER BY ?disease
    """
    return [str(row["disease"]) for row in graph.query(query)]

def list_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?symptom
    WHERE {
        ?symptom rdf:type ex:Symptom .
    }
    ORDER BY ?symptom
    """
    return [str(row["symptom"]) for row in graph.query(query)]

def list_leaf_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?symptom
    WHERE {
        ?symptom rdf:type ex:LeafSymptom .
    }
    ORDER BY ?symptom
    """
    return [str(row["symptom"]) for row in graph.query(query)]

def list_stem_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?symptom
    WHERE {
        ?symptom rdf:type ex:StemSymptom .
    }
    ORDER BY ?symptom
    """
    return [str(row["symptom"]) for row in graph.query(query)]

def list_tuber_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?symptom
    WHERE {
        ?symptom rdf:type ex:TuberSymptom .
    }
    ORDER BY ?symptom
    """
    return [str(row["symptom"]) for row in graph.query(query)]

def get_symptoms_of_disease(graph: Graph, disease_iri: str):
    query = """
    PREFIX ex: <http://example.org/potato/>

    SELECT ?symptom
    WHERE {
        ?symptom ex:indicatesDisease <%s> .
    }
    ORDER BY ?symptom
    """ % disease_iri
    return [str(row["symptom"]) for row in graph.query(query)]

def get_diseases_by_symptom(graph: Graph, symptom_iri: str):
    query = """
    PREFIX ex: <http://example.org/potato/>

    SELECT ?disease
    WHERE {
        <%s> ex:indicatesDisease ?disease .
    }
    ORDER BY ?disease
    """ % symptom_iri
    return [str(row["disease"]) for row in graph.query(query)]

def get_disease_symptom_pairs(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>

    SELECT ?disease ?symptom
    WHERE {
        ?symptom ex:indicatesDisease ?disease .
    }
    ORDER BY ?disease ?symptom
    """
    return [(str(row["disease"]), str(row["symptom"])) for row in graph.query(query)]

def get_diseases_with_leaf_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?disease
    WHERE {
        ?symptom rdf:type ex:LeafSymptom .
        ?symptom ex:indicatesDisease ?disease .
    }
    ORDER BY ?disease
    """
    return [str(row["disease"]) for row in graph.query(query)]

def get_diseases_with_stem_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?disease
    WHERE {
        ?symptom rdf:type ex:StemSymptom .
        ?symptom ex:indicatesDisease ?disease .
    }
    ORDER BY ?disease
    """
    return [str(row["disease"]) for row in graph.query(query)]

def get_diseases_with_tuber_symptoms(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?disease
    WHERE {
        ?symptom rdf:type ex:TuberSymptom .
        ?symptom ex:indicatesDisease ?disease .
    }
    ORDER BY ?disease
    """
    return [str(row["disease"]) for row in graph.query(query)]

def get_diseases_with_control_actions(graph: Graph):
    query = """
    PREFIX ex: <http://example.org/potato/>

    SELECT DISTINCT ?disease ?action
    WHERE {
        ?disease ex:hasControlAction ?action .
    }
    ORDER BY ?disease ?action
    """
    return [(str(row["disease"]), str(row["action"])) for row in graph.query(query)]
