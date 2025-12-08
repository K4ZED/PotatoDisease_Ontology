from dataclasses import dataclass
from typing import List, Dict, Any
from rdflib import Graph, Namespace, RDF

POT = Namespace("http://example.org/potato#")


@dataclass
class Symptom:
    id: str
    uri: str
    name: str
    description: str
    category: str
    indicates: List[str]


@dataclass
class Disease:
    id: str
    uri: str
    name: str
    description: str
    disease_type: str
    severity: str
    agent_note: str
    control_actions: List[str]


@dataclass
class ControlAction:
    id: str
    uri: str
    name: str
    description: str


def load_knowledge(path: str = "PotatoDisease.ttl") -> Dict[str, Any]:
    graph = Graph()
    graph.parse(path, format="turtle")

    symptom_classes = [POT.LeafSymptom, POT.StemSymptom, POT.TuberSymptom]
    disease_classes = [
        POT.FungalDisease,
        POT.BacterialDisease,
        POT.VirusDisease,
        POT.NematodeDisease,
        POT.ViroidDisease,
        POT.AccidentalDisorder,
        POT.MineralDeficiencyDisorder,
        POT.ExternalPhysiologicalDisorder,
        POT.InternalPhysiologicalDisorder,
    ]

    symptoms: List[Symptom] = []
    for cls in symptom_classes:
        for s in graph.subjects(RDF.type, cls):
            sid = s.split("#")[-1]
            name = str(next(graph.objects(s, POT.hasName), sid))
            desc = str(next(graph.objects(s, POT.hasDescription), ""))
            category = cls.split("#")[-1]
            indicates = [o.split("#")[-1] for o in graph.objects(s, POT.indicatesDisease)]
            symptoms.append(Symptom(sid, str(s), name, desc, category, indicates))

    diseases: List[Disease] = []
    for s in set(graph.subjects(RDF.type, None)):
        disease_type_uri = None
        for cls in disease_classes:
            if (s, RDF.type, cls) in graph:
                disease_type_uri = cls
                break
        if disease_type_uri is None:
            continue
        did = s.split("#")[-1]
        name = str(next(graph.objects(s, POT.hasName), did))
        desc = str(next(graph.objects(s, POT.hasDescription), ""))
        severity = str(next(graph.objects(s, POT.severityLevel), ""))
        agent_note = str(next(graph.objects(s, POT.hasAgentNote), ""))
        control_actions = [o.split("#")[-1] for o in graph.objects(s, POT.hasControlAction)]
        diseases.append(
            Disease(
                did,
                str(s),
                name,
                desc,
                disease_type_uri.split("#")[-1],
                severity,
                agent_note,
                control_actions,
            )
        )

    controls: List[ControlAction] = []
    for s in graph.subjects(RDF.type, POT.ControlAction):
        cid = s.split("#")[-1]
        name = str(next(graph.objects(s, POT.hasName), cid))
        desc = str(next(graph.objects(s, POT.hasDescription), ""))
        controls.append(ControlAction(cid, str(s), name, desc))

    symptoms_by_id = {s.id: s for s in symptoms}
    diseases_by_id = {d.id: d for d in diseases}
    controls_by_id = {c.id: c for c in controls}

    return {
        "graph": graph,
        "symptoms": symptoms,
        "diseases": diseases,
        "controls": controls,
        "symptoms_by_id": symptoms_by_id,
        "diseases_by_id": diseases_by_id,
        "controls_by_id": controls_by_id,
    }
