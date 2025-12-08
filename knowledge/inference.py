from typing import List, Dict, Any
from .ontology_loader import Symptom, Disease, ControlAction


def diagnose(selected_symptom_ids: List[str], knowledge: Dict[str, Any]) -> Dict[str, Any]:
    symptoms_by_id: Dict[str, Symptom] = knowledge.get("symptoms_by_id", {})
    diseases_by_id: Dict[str, Disease] = knowledge.get("diseases_by_id", {})
    controls_by_id: Dict[str, ControlAction] = knowledge.get("controls_by_id", {})

    matched_symptoms: List[Symptom] = []
    disease_scores: Dict[str, int] = {}
    disease_symptoms: Dict[str, List[Symptom]] = {}

    for sid in selected_symptom_ids:
        symptom = symptoms_by_id.get(sid)
        if not symptom:
            continue
        matched_symptoms.append(symptom)
        for did in symptom.indicates:
            disease_scores[did] = disease_scores.get(did, 0) + 1
            if did not in disease_symptoms:
                disease_symptoms[did] = []
            disease_symptoms[did].append(symptom)

    ranked_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

    diseases_result: List[Dict[str, Any]] = []
    control_ids_ordered: List[str] = []

    for did, score in ranked_diseases:
        disease = diseases_by_id.get(did)
        if not disease:
            continue
        diseases_result.append(
            {
                "id": disease.id,
                "name": disease.name,
                "description": disease.description,
                "disease_type": disease.disease_type,
                "severity": disease.severity,
                "agent_note": disease.agent_note,
                "score": score,
                "symptoms": disease_symptoms.get(did, []),
                "control_actions": disease.control_actions,
            }
        )
        for cid in disease.control_actions:
            if cid not in control_ids_ordered:
                control_ids_ordered.append(cid)

    controls_result: List[Dict[str, Any]] = []
    for cid in control_ids_ordered:
        control = controls_by_id.get(cid)
        if not control:
            continue
        controls_result.append(
            {
                "id": control.id,
                "name": control.name,
                "description": control.description,
            }
        )

    return {
        "selected_symptoms": matched_symptoms,
        "diseases": diseases_result,
        "controls": controls_result,
    }
