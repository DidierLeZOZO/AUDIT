"""Point d'entrée unique : PDF -> texte -> objets extraits -> type de document -> bâtiments couverts."""
from __future__ import annotations

import io
from dataclasses import dataclass

from .document import Couverture, TypeDocument, classer_document, detecter_batiments
from .enrichissement import enrichir, scenario_depuis_etiquettes
from .parser import Batiment, Scenario, parse_texte, reflow_pdf_text


@dataclass
class Analyse:
    texte: str
    document: TypeDocument
    couverture: Couverture
    batiment: Batiment
    scenarios: list[Scenario]


def analyser_texte(texte: str) -> Analyse:
    b, scs = parse_texte(texte)
    enrichir(texte, b, scs)
    if not scs:  # étude thermique, DPE… : pas de scénarios au format audit
        sc = scenario_depuis_etiquettes(texte, b)
        scs = [sc] if sc else []
    doc = classer_document(texte, b.auditeur.reference_audit)
    return Analyse(texte, doc, detecter_batiments(texte, b.adresse), b, scs)


def analyser_pdf(pdf: bytes | io.BytesIO) -> Analyse:
    return analyser_texte(reflow_pdf_text(pdf.getvalue() if hasattr(pdf, "getvalue") else pdf))
