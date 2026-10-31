"""Reconnaissance du type de document et des audits multi-bâtiments.
Attention : textes synthétiques (écrits d'après la structure connue de ces documents),
sauf le test sur l'audit réel qui nécessite AUDIT_EXEMPLE_PDF."""
import io
import os

import pytest

from audit.analyse import analyser_pdf, analyser_texte
from audit.document import (AUDIT_NON_REGLEMENTAIRE, AUDIT_REGLEMENTAIRE, DPE, ETUDE_THERMIQUE, classer_document,
                            detecter_batiments)
from audit.regles import NON_ESTIMABLE, SOUS_RESERVE, evaluer

AUDIT = """Audit énergétique
N° audit : A2531E0012345X
Scénario 1 « rénovation en une fois »
Parcours en 1 étape
Informations auditeur
Détail des travaux énergétiques
Résultats après travaux
méthode 3CL-DPE 2021"""
DPE_TXT = """DIAGNOSTIC DE PERFORMANCE ÉNERGÉTIQUE (immeuble)
N°DPE : 2369E0123456X
Établi le : 12/03/2024  Valable jusqu'au : 11/03/2034
Ce document vous permet de savoir si votre logement est économe en énergie
Recommandations d'amélioration de la performance
Les travaux essentiels  Pack 1  Pack 2
Méthode 3CL-DPE 2021"""
ETUDE = """Étude thermique réglementaire RT existant globale
Méthode de calcul : Th-C-E ex
Type de bien : immeuble collectif
Nombre de logements : 24
Surface habitable : 1 820 m²
Cep initial = 262,4 kWhep/m².an
Cep projet = 151,2 kWhep/m².an
Cep réf = 170 kWhep/m².an
Ubât = 0,62 W/m².K
GES initial : 48 kgCO2/m².an
GES projet : 20 kgCO2/m².an"""


def test_types():
    assert classer_document(AUDIT, "A2531E0012345X").code == AUDIT_REGLEMENTAIRE
    assert classer_document(AUDIT + "\nAudit énergétique non réglementaire").code == AUDIT_NON_REGLEMENTAIRE
    assert classer_document(DPE_TXT).code == DPE
    assert classer_document(ETUDE).code == ETUDE_THERMIQUE


def test_etude_complete_estimable_sous_reserve_sinon_non_estimable():
    a = analyser_texte(ETUDE)
    r = evaluer(a.document, a.couverture, a.batiment, a.scenarios).scenarios[0]
    assert r.verdict == SOUS_RESERVE and r.surface == 1820
    a = analyser_texte(ETUDE.replace("GES projet : 20 kgCO2/m².an", ""))
    assert evaluer(a.document, a.couverture, a.batiment, a.scenarios).scenarios[0].verdict == NON_ESTIMABLE


@pytest.mark.parametrize("adresse,multiple", [
    ("Bâtiments A, B et C 12 rue X", True), ("Bât. 1 à 4 rue Y", True), ("Bâtiment A et B", True),
    ("Bâtiment A, 12 rue des Lilas", False), ("Bâtiment A - 12 rue X", False), ("Résidence Z bâtiment C", False),
])
def test_batiments(adresse, multiple):
    assert detecter_batiments(adresse, adresse).multiple is multiple


def test_nombre_de_batiments_et_faux_positifs():
    assert detecter_batiments("nombre de bâtiments : 3", None).multiple
    c = detecter_batiments("Ubat W/(m².K) 0,68\nAt Bat m² 2625", "Bâtiment A 1 rue X")
    assert not c.multiple and c.autres_mentions == []


EXEMPLE = os.environ.get("AUDIT_EXEMPLE_PDF")


@pytest.mark.skipif(not EXEMPLE or not os.path.exists(EXEMPLE or ""), reason="PDF client non versionné (AUDIT_EXEMPLE_PDF)")
def test_audit_reel_pleiades_parc_de_turin():
    a = analyser_pdf(open(EXEMPLE, "rb").read())
    b = a.batiment
    assert a.document.code == AUDIT_NON_REGLEMENTAIRE and not a.couverture.multiple and a.couverture.autres_mentions == ["B"]
    assert (b.cep_initial, b.ges_initial, b.energie_chauffage, b.energie_ecs) == (169, 25, "gaz", "electricite")
    assert b.fiabilite["ges_initial"] == "concordant" and b.auditeur.qualification == "OPQIBI 1905"
    s1, s2 = a.scenarios
    assert (s1.etapes[0].cep_apres, s1.etapes[0].ges_apres, s1.etapes[0].energie_chauffage) == (78, 8, "reseau")
    assert [(e.cep_apres, e.ges_apres) for e in s2.etapes] == [(83, 9), (78, 8)]
    ev = evaluer(a.document, a.couverture, b, a.scenarios)
    assert [s.verdict for s in ev.scenarios] == [SOUS_RESERVE, SOUS_RESERVE]
    assert ev.scenarios[0].coef == 3 and round(ev.scenarios[0].volume_kwhc) == 16_612_155
