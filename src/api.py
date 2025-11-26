from flask import Blueprint, jsonify, request
from .ontology_loader import load_graph
from .query_service import (
    list_diseases,
    list_symptoms,
    list_leaf_symptoms,
    list_stem_symptoms,
    list_tuber_symptoms,
    get_symptoms_of_disease,
    get_diseases_by_symptom,
    get_disease_symptom_pairs,
    get_diseases_with_control_actions,
)

graph = load_graph()
api = Blueprint("api", __name__)

@api.route("/api/diseases", methods=["GET"])
def api_diseases():
    diseases = list_diseases(graph)
    return jsonify(diseases)

@api.route("/api/symptoms", methods=["GET"])
def api_symptoms():
    symptoms = list_symptoms(graph)
    return jsonify(symptoms)

@api.route("/api/symptoms/leaf", methods=["GET"])
def api_leaf_symptoms():
    symptoms = list_leaf_symptoms(graph)
    return jsonify(symptoms)

@api.route("/api/symptoms/stem", methods=["GET"])
def api_stem_symptoms():
    symptoms = list_stem_symptoms(graph)
    return jsonify(symptoms)

@api.route("/api/symptoms/tuber", methods=["GET"])
def api_tuber_symptoms():
    symptoms = list_tuber_symptoms(graph)
    return jsonify(symptoms)

@api.route("/api/disease", methods=["GET"])
def api_disease_detail():
    iri = request.args.get("iri")
    if not iri:
        return jsonify({"error": "missing iri"}), 400
    symptoms = get_symptoms_of_disease(graph, iri)
    return jsonify({"iri": iri, "symptoms": symptoms})

@api.route("/api/symptom", methods=["GET"])
def api_symptom_detail():
    iri = request.args.get("iri")
    if not iri:
        return jsonify({"error": "missing iri"}), 400
    diseases = get_diseases_by_symptom(graph, iri)
    return jsonify({"iri": iri, "diseases": diseases})

@api.route("/api/disease-symptom", methods=["GET"])
def api_disease_symptom_pairs():
    pairs = get_disease_symptom_pairs(graph)
    data = [{"disease": d, "symptom": s} for d, s in pairs]
    return jsonify(data)

@api.route("/api/disease-control", methods=["GET"])
def api_disease_control():
    pairs = get_diseases_with_control_actions(graph)
    data = [{"disease": d, "control": c} for d, c in pairs]
    return jsonify(data)
