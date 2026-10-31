"""Moteur BAR-TH-177 : cas d'essai de docs/regles_BAR-TH-177.md §14 + cas limites."""
from datetime import date

import pytest

from audit.document import AUDIT_NON_REGLEMENTAIRE, AUDIT_REGLEMENTAIRE, Couverture, TypeDocument
from audit.parser import Auditeur, Batiment, Etape, Scenario, Travail
from audit.referentiel import classe_dpe, version_fiche
from audit.regles import (ALERTE, BLOQUANT, ELIGIBLE, NON_ELIGIBLE, NON_ESTIMABLE, SOUS_RESERVE, Hypotheses,
                          evaluer, siren_valide)

DOC_OK = TypeDocument(AUDIT_REGLEMENTAIRE, "forte", "3CL-DPE")
UN_BAT = Couverture(False, "A")
H = Hypotheses(aujourd_hui=date(2026, 10, 31))


def bat(**kw):
    base = dict(adresse="12 rue X 21000 Dijon", code_postal="21000", type_bien="immeuble collectif", nb_logements=48,
                cep_initial=245, ges_initial=52, shab=3020, energie_chauffage="gaz", energie_ecs="gaz",
                date_visite="03/02/2026", date_etablissement="20/02/2026",
                auditeur=Auditeur(raison_sociale="BE", siren="799222823", logiciel="Pleiades",
                                  version_logiciel="6.26", qualification="OPQIBI 1905"))
    return Batiment(**{**base, **kw})


def scen(cep=128, ges=9, ch="pac", ecs="pac", eq=("pac",), etapes=None):
    e = Etape("Étape unique", cep_apres=cep, ges_apres=ges, energie_chauffage=ch, energie_ecs=ecs,
              equipements_installes=list(eq), travaux=[Travail("Murs", "ITE", "R ≥ 4", "100 m²")])
    return Scenario("s1", "Scénario 1", etapes or [e])


def ev(b=None, s=None, doc=DOC_OK, couv=UN_BAT, h=H):
    return evaluer(doc, couv, b or bat(), [s or scen()], h).scenarios[0]


def ids(r, niveau):
    return {x.id for x in r.resultats if x.niveau == niveau}


def test_cas1_conforme_x3():
    r = ev()
    assert r.verdict == ELIGIBLE and r.coef == 3 and r.volume_kwhc == 19_026_000


def test_cas2_reseau_existant_x2():
    r = ev(bat(cep_initial=210, ges_initial=38, shab=4500, energie_chauffage="reseau", energie_ecs="reseau"),
           scen(cep=125, ges=24, ch="reseau", ecs="reseau", eq=()))
    assert r.verdict == ELIGIBLE and r.coef == 2 and r.volume_kwhc == 18_900_000


def test_cas3_gain_insuffisant():
    r = ev(bat(cep_initial=260, ges_initial=55), scen(cep=172, ges=40))
    assert r.verdict == NON_ELIGIBLE and "PE-02" in ids(r, BLOQUANT) and r.volume_kwhc == 0


def test_cas4_chaudiere_gaz_installee():
    r = ev(bat(cep_initial=280, ges_initial=60), scen(cep=165, ges=40, ch="gaz", ecs="gaz", eq=("chaudiere_gaz",)))
    assert r.verdict == NON_ELIGIBLE and "PE-06" in ids(r, BLOQUANT)


def test_cas6_ges_en_hausse():
    r = ev(bat(energie_chauffage="fioul", ges_initial=40), scen(cep=118, ges=45, ch="bois", eq=("chaudiere_bois",)))
    assert "PE-04" in ids(r, BLOQUANT)


def test_cas7_pac_hybride_ecs_gaz_conservee():
    r = ev(bat(cep_initial=230, ges_initial=50), scen(cep=140, ges=28, ch="pac", ecs="gaz", eq=("pac_hybride", "chaudiere_gaz")))
    assert r.verdict == ELIGIBLE and "PE-06" in ids(r, ALERTE) and r.coef == 2


def test_cas8_cep_331_strict():
    r = ev(bat(cep_initial=600, ges_initial=90), scen(cep=331.0, ges=60))
    assert "PE-01" in ids(r, BLOQUANT)
    assert "PE-01" not in ids(ev(bat(cep_initial=600, ges_initial=90), scen(cep=330.9, ges=60)), BLOQUANT)


def test_gain_35_pile_et_sans_arrondi():
    assert "PE-02" not in ids(ev(bat(cep_initial=200), scen(cep=130)), BLOQUANT)       # 35,00 %
    assert "PE-02" in ids(ev(bat(cep_initial=200), scen(cep=130.1)), BLOQUANT)         # 34,95 % (affiché « 35 % »)


def test_document_non_reglementaire_sous_reserve():
    r = ev(doc=TypeDocument(AUDIT_NON_REGLEMENTAIRE, "forte", "3CL-DPE"))
    assert r.verdict == SOUS_RESERVE and r.volume_kwhc > 0


def test_un_audit_par_batiment_bloquant():
    assert ev(couv=Couverture(True)).verdict == NON_ELIGIBLE


def test_maison_et_petit_collectif():
    assert ev(bat(type_bien="maison individuelle")).verdict == NON_ELIGIBLE
    assert ev(bat(nb_logements=2)).verdict == NON_ELIGIBLE


def test_donnees_manquantes_non_estimable():
    assert ev(s=scen(ges=None)).verdict == NON_ESTIMABLE
    assert ev(bat(ges_initial=None)).verdict == NON_ESTIMABLE


def test_coefficients():
    assert ev(h=Hypotheses(coup_de_pouce=False, aujourd_hui=date(2026, 10, 31))).coef == 1
    assert ev(bat(energie_chauffage="electricite", energie_ecs="electricite")).coef == 2      # rien de fossile
    assert ev(s=scen(ch="electricite", ecs="electricite", eq=())).coef == 2                  # gaz -> effet Joule
    r = ev(s=scen(ch="reseau", ecs="reseau", eq=("reseau",)))
    assert r.coef == 3 and "VO-02" in ids(r, ALERTE)                                         # nouveau réseau
    assert ev(bat(energie_chauffage=None)).coef == 2


def test_surface_de_reference_alerte():
    r = evaluer(DOC_OK, UN_BAT, bat(shab=None, surface_m2=2000), [scen()], H)
    assert any(x.id == "SU-01" and x.niveau == ALERTE for x in r.generaux)
    assert r.scenarios[0].volume_kwhc == 2100 * 2000 * 3


def test_dom_et_batiment_recent():
    assert ev(bat(code_postal="97400")).verdict == NON_ELIGIBLE
    assert ev(bat(annee_construction=2025)).verdict == NON_ELIGIBLE


def test_etapes_intermediaires():
    e1 = Etape("Première étape", cep_apres=200, ges_apres=40, energie_chauffage="gaz", energie_ecs="gaz")
    e2 = Etape("Deuxième étape", cep_apres=120, ges_apres=9, energie_chauffage="pac", energie_ecs="pac", equipements_installes=["pac"])
    r = ev(s=Scenario("s2", "Scénario 2", [e1, e2]))
    assert r.verdict == ELIGIBLE and "non valorisable seule" in r.etapes[0][1]


def test_referentiel():
    assert classe_dpe(100, 40) == "D" and classe_dpe(100, None) == "B" and classe_dpe(421, 5) == "G"
    assert version_fiche(date(2026, 1, 16)) == "vA63.1" and version_fiche(date(2026, 1, 17)) == "vA80.2"
    assert siren_valide("799222823") and not siren_valide("799222824")
