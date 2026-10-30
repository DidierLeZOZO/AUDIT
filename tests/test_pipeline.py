"""Test de bout en bout sur un PDF synthétique (format type LICIEL) : parse -> Excel -> PDF."""
import io

import openpyxl
import pytest
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from audit.excel_export import generer_excel
from audit.parser import parse_audit_pdf
from audit.pdf_export import generate_pdf
from audit.securite import neutraliser

LIGNES = """Adresse : 12 rue des Lilas 31000 Toulouse

Type de bien : maison
Propriétaire : M. Dupont
Surface de référence : 120 m²
Montants et consommations annuels d'énergie
(kWh/m²/an)
222  (96 )
EP EF
Scénario 1 « rénovation en une fois »
Détail des travaux énergétiques
Murs
Isolation des murs par l'extérieur. R >= 4,4 m².K/W Th35 130 mm
Surface concernée = 80 m²
Chauffage
Pompe à chaleur air/eau. SCOP >= 4.6
Résultats après travaux
- 60 %
(kWh/m²/an)
90  (40 )
EP EF
aides financières possibles
"""


@pytest.fixture(scope="module")
def pdf_bytes():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    y = 800
    for ligne in LIGNES.splitlines():
        c.drawString(40, y, ligne)
        y -= 14
    c.save()
    return buf.getvalue()


def test_parse(pdf_bytes):
    b, scs = parse_audit_pdf(io.BytesIO(pdf_bytes))
    assert b.surface_m2 == 120 and b.beneficiaire == "M. Dupont"
    assert b.cep_initial == 222
    assert scs, "aucun scénario détecté"
    postes = [t.poste for e in scs[0].etapes for t in e.travaux]
    assert "Murs" in postes and "Chauffage" in postes


def test_exports(pdf_bytes):
    b, scs = parse_audit_pdf(io.BytesIO(pdf_bytes))
    ws = openpyxl.load_workbook(io.BytesIO(generer_excel(b, scs[0], prefill_realises=True))).active
    assert ws["C5"].value.startswith("12 rue")
    assert "Murs" in ws["B9"].value and ws["E9"].value == ws["B9"].value
    assert len(PdfReader(io.BytesIO(generate_pdf(b, scs, scs[0].id))).pages) >= 2


def test_neutralise_formule():
    assert neutraliser("=1+1") == "'=1+1" and neutraliser("abc") == "abc"
