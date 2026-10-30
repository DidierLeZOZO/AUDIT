import io
import os

import pytest

from audit.controles import ALERTE, ERREUR, classes_gagnees, controler, siren_valide
from audit.parser import Auditeur, Batiment, Etape, Scenario, Travail, parse_audit_pdf


def _bat(**kw):
    base = dict(adresse="1 rue X", beneficiaire="Y", surface_m2=100, cep_initial=200, etiquette_initiale="D",
                auditeur=Auditeur(raison_sociale="Z", siren="799222823", date_audit="01/01/2026"))
    return Batiment(**{**base, **kw})


def _sc(cep_apres=90, eco=55, travaux=None, etiq="B"):
    t = travaux if travaux is not None else [Travail("Murs", "Isolation", "R ≥ 4", "10 m²")]
    return [Scenario("s1", "Scénario 1", [Etape("Étape unique", cep_apres=cep_apres, economie_pct=eco,
                                                 etiquette_apres=etiq, travaux=t)])]


def niveaux(b, s):
    return {c.niveau for c in controler(b, s)}


def test_cas_sain():
    assert controler(_bat(), _sc()) == []


def test_siren():
    assert siren_valide("799222823") and not siren_valide("799222824") and not siren_valide("123")


def test_non_reglementaire_et_cep():
    assert ERREUR in niveaux(_bat(non_reglementaire=True), _sc())
    assert ERREUR in niveaux(_bat(), _sc(cep_apres=250))       # CEP après ≥ avant
    assert ERREUR in niveaux(_bat(), _sc(travaux=[]))
    assert ALERTE in niveaux(_bat(), _sc(eco=20))              # économie incohérente avec le CEP
    assert ALERTE in niveaux(_bat(), _sc(travaux=[Travail("Murs", "x", "", "")]))  # quantité manquante


def test_classes():
    assert classes_gagnees("C", "B") == 1 and classes_gagnees("G", "C") == 4 and classes_gagnees(None, "B") is None


EXEMPLE = os.environ.get("AUDIT_EXEMPLE_PDF")


@pytest.mark.skipif(not EXEMPLE or not os.path.exists(EXEMPLE or ""), reason="PDF client non versionné (AUDIT_EXEMPLE_PDF)")
def test_audit_reel_pleiades():
    b, scs = parse_audit_pdf(io.BytesIO(open(EXEMPLE, "rb").read()))
    assert (b.cep_initial, b.cef_initial, b.surface_m2) == (169, 138, 2636.85)
    assert [len(s.etapes) for s in scs] == [1, 2]
    assert scs[0].etapes[0].cep_apres == 78 and b.non_reglementaire
