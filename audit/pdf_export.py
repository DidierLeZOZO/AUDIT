"""PDF à transmettre au bailleur : p.1 récapitulatif des scénarios (scénario retenu
en évidence), p.2+ fiche des travaux avec champs « réalisés » remplissables."""
from __future__ import annotations

import io
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

from .excel_export import lignes_travaux
from .parser import Batiment, Scenario

PAGE = landscape(A4)
MARGE = 36
BLEU = colors.HexColor("#DDEBF7")
VERT = colors.HexColor("#E2F0D9")
_ss = getSampleStyleSheet()
CELL = ParagraphStyle("cell", parent=_ss["BodyText"], fontSize=8, leading=10)
CELL_B = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")


def _fmt(v, suffixe=""):
    if v in (None, "", 0, 0.0):
        return "—"
    return f"{v:g}{suffixe}" if isinstance(v, (int, float)) else f"{v}{suffixe}"


def _entete(c: canvas.Canvas, titre: str, b: Batiment) -> float:
    w, h = PAGE
    y = h - MARGE
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGE, y, titre)
    c.setFont("Helvetica", 9)
    y -= 16
    c.drawString(MARGE, y, f"Bénéficiaire : {b.beneficiaire or '—'}")
    y -= 12
    c.drawString(MARGE, y, f"Adresse : {b.adresse or '—'}")
    c.drawRightString(w - MARGE, y, f"Édité le {date.today():%d/%m/%Y}")
    return y - 18


def _page_recap(c, b: Batiment, scenarios: list[Scenario], choisi: str) -> None:
    y = _entete(c, "Récapitulatif des scénarios de travaux", b)
    rows = [[Paragraph(x, CELL_B) for x in
             ("Scénario", "Étapes", "CEP avant", "CEP après", "Étiquette", "Économie")]]
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), BLEU),
             ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i, sc in enumerate(scenarios, start=1):
        d = sc.etapes[-1]
        rows.append([
            Paragraph(sc.nom.replace("\n", " "), CELL_B if sc.id == choisi else CELL),
            Paragraph(" → ".join(e.libelle for e in sc.etapes), CELL),
            _fmt(b.cep_initial), _fmt(d.cep_apres),
            f"{b.etiquette_initiale or '?'} → {d.etiquette_apres or '?'}",
            _fmt(d.economie_pct, " %"),
        ])
        if sc.id == choisi:
            style.append(("BACKGROUND", (0, i), (-1, i), VERT))
    t = Table(rows, colWidths=[250, 190, 60, 60, 70, 60], repeatRows=1)
    t.setStyle(TableStyle(style))
    _, th = t.wrapOn(c, PAGE[0] - 2 * MARGE, y)
    t.drawOn(c, MARGE, y - th)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(MARGE, y - th - 14, "Scénario retenu surligné en vert.")
    c.showPage()


def _pages_fiche(c, b: Batiment, sc: Scenario) -> None:
    travaux = lignes_travaux(sc) or [{"nature": "", "carac": "", "quantite": ""}]
    largeurs = [190, 150, 60]
    tete = [Paragraph(x, CELL_B) for x in
            ("Nature (préconisé)", "Caractéristiques", "Qté", "Nature (réalisé)",
             "Marque / référence (réalisé)", "Qté")]
    ligne_h, idx = 34, 0
    while idx < len(travaux):
        y = _entete(c, f"Liste des travaux et entreprises — {sc.nom.replace(chr(10), ' ')}", b)
        n = int((y - MARGE - 24) // ligne_h)
        lot = travaux[idx: idx + n]
        rows = [tete] + [[Paragraph(t["nature"], CELL), Paragraph(t["carac"], CELL),
                          Paragraph(t["quantite"], CELL), "", "", ""] for t in lot]
        t = Table(rows, colWidths=largeurs * 2, rowHeights=[24] + [ligne_h] * len(lot))
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                               ("BACKGROUND", (0, 0), (-1, 0), BLEU), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        t.wrapOn(c, PAGE[0], y)
        t.drawOn(c, MARGE, y - 24 - ligne_h * len(lot))
        x0 = MARGE + sum(largeurs)
        for k in range(len(lot)):
            top = y - 24 - ligne_h * k
            for j, wcol in enumerate(largeurs):
                c.acroForm.textfield(
                    name=f"r{idx + k}_{j}", x=x0 + sum(largeurs[:j]) + 2, y=top - ligne_h + 2,
                    width=wcol - 4, height=ligne_h - 4, borderWidth=0, fontSize=8,
                    fieldFlags="multiline", forceBorder=False)
        idx += n
        c.showPage()


def generate_pdf(batiment: Batiment, scenarios: list[Scenario], scenario_choisi_id: str) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=PAGE)
    _page_recap(c, batiment, scenarios, scenario_choisi_id)
    choisi = next((s for s in scenarios if s.id == scenario_choisi_id), scenarios[0])
    _pages_fiche(c, batiment, choisi)
    c.save()
    return buf.getvalue()
