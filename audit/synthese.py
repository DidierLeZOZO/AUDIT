"""Tableau comparatif des scénarios (une colonne par scénario)."""
from __future__ import annotations

from .parser import Batiment, Scenario

# (libellé affiché, postes du parseur regroupés sous ce libellé)
TRAVAUX_TYPES = [
    ("Murs", ["Murs"]),
    ("Plancher bas", ["Plancher", "Planchers bas"]),
    ("Toiture / Combles", ["Toiture / Combles"]),
    ("Menuiseries", ["Menuiseries"]),
    ("Ventilation", ["Ventilation"]),
    ("Chauffage", ["Chauffage"]),
    ("Eau chaude sanitaire", ["Eau chaude sanitaire"]),
]


def tableau_comparatif(b: Batiment, scenarios: list[Scenario]) -> dict[str, dict]:
    data = {}
    for sc in scenarios:
        fin = sc.etapes[-1]
        multi = len(sc.etapes) > 1
        col = {
            "Étape(s)": " → ".join(e.libelle for e in sc.etapes),
            "CEP avant (kWhEP/m²/an)": b.cep_initial,
            "CEP après": fin.cep_apres,
            "CEF avant (kWhEF/m²/an)": b.cef_initial,
            "CEF après": fin.cef_apres,
            "Étiquette avant": b.etiquette_initiale,
            "Étiquette après": fin.etiquette_apres,
            "Économie": f"{fin.economie_pct:g}%" if fin.economie_pct is not None else "—",
        }
        for label, postes in TRAVAUX_TYPES:
            etapes = [i for i, e in enumerate(sc.etapes, 1) if any(t.poste in postes for t in e.travaux)]
            if not etapes:
                col[label] = "❌"
            elif multi:
                col[label] = "✅ (Étape " + ", ".join(map(str, etapes)) + ")"
            else:
                col[label] = "✅"
        data[sc.nom.replace("\n", " ")] = col
    return data
