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


def _f(v) -> str:
    return "—" if v is None else f"{v:g}"


def tableau_comparatif(b: Batiment, scenarios: list[Scenario], ev=None) -> dict[str, dict]:
    """`ev` (audit.regles.Evaluation, facultatif) ajoute verdict, coefficient et volume."""
    verdicts = {s.id: s for s in ev.scenarios} if ev else {}
    data = {}
    for sc in scenarios:
        fin = sc.etapes[-1]
        multi = len(sc.etapes) > 1
        col = {"Étape(s)": " → ".join(e.libelle for e in sc.etapes)}
        if sc.id in verdicts:
            from .regles import LIBELLE_VERDICT
            v = verdicts[sc.id]
            col["Verdict BAR-TH-177"] = LIBELLE_VERDICT[v.verdict]
            col["Coefficient"] = f"×{v.coef}"
            col["Volume (MWh cumac)"] = f"{v.volume_kwhc / 1000:,.0f}".replace(",", " ")
        col.update({
            "Cep avant → après (kWhEP/m².an)": f"{_f(b.cep_initial)} → {_f(fin.cep_apres)}",
            "Gain Cep": f"{(1 - fin.cep_apres / b.cep_initial):.1%}" if b.cep_initial and fin.cep_apres else "—",
            "GES avant → après (kgCO2/m².an)": f"{_f(b.ges_initial)} → {_f(fin.ges_apres)}",
            "Cef avant → après (kWhEF/m².an)": f"{_f(b.cef_initial)} → {_f(fin.cef_apres)}",
            "Étiquette avant → après": f"{b.etiquette_initiale or '?'} → {fin.etiquette_apres or '?'}",
        })
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
