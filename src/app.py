from flask import Flask, render_template, request
from .ontology_loader import load_graph
from .query_service import (
    list_diseases,
    list_symptoms,
    get_symptoms_of_disease,
    get_diseases_by_symptom,
)
from .api import api

app = Flask(__name__, static_folder="../static", template_folder="../templates")
graph = load_graph()
app.register_blueprint(api)


def pretty_label(iri: str) -> str:
    local = iri.split("#")[-1]
    result = []
    for i, c in enumerate(local):
        if i > 0 and c.isupper() and not local[i - 1].isupper():
            result.append(" ")
        result.append(c)
    return "".join(result)


@app.route("/")
def index():
    raw = list_diseases(graph)
    diseases = [{"iri": iri, "name": pretty_label(iri)} for iri in raw]
    return render_template("index.html", diseases=diseases)


@app.route("/disease")
def disease_detail():
    iri = request.args.get("iri")
    if not iri:
        return "Missing iri", 400
    symptoms = get_symptoms_of_disease(graph, iri)
    return render_template("disease.html", iri=iri, symptoms=symptoms)


@app.route("/diagnose", methods=["GET", "POST"])
def diagnose():
    all_symptoms = list_symptoms(graph)
    result = None
    if request.method == "POST":
        selected = request.form.getlist("symptoms")
        counts = {}
        for symptom_iri in selected:
            diseases = get_diseases_by_symptom(graph, symptom_iri)
            for d in diseases:
                counts[d] = counts.get(d, 0) + 1
        result = [
            {"iri": d, "name": pretty_label(d), "score": score}
            for d, score in sorted(counts.items(), key=lambda x: x[1], reverse=True)
        ]
    return render_template("diagnose.html", symptoms=all_symptoms, result=result)


def create_app():
    return app


if __name__ == "__main__":
    app.run(debug=True)
