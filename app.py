from flask import Flask, render_template, request
from knowledge.ontology_loader import load_knowledge
from knowledge.inference import diagnose

app = Flask(__name__)

knowledge = load_knowledge("PotatoDisease.ttl")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/diagnose", methods=["GET", "POST"])
def diagnose_view():
    if request.method == "GET":
        symptoms = knowledge.get("symptoms", [])
        return render_template("diagnose.html", symptoms=symptoms)
    selected_symptoms = request.form.getlist("symptoms")
    result = diagnose(selected_symptoms, knowledge)
    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
