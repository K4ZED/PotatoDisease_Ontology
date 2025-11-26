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


@app.route("/")
def index():
    diseases = list_diseases(graph)
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
            d for d, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)
        ]
    return render_template("diagnose.html", symptoms=all_symptoms, result=result)


def create_app():
    return app


if __name__ == "__main__":
    app.run(debug=True)
