"""Reconnaissance du type de document et du nombre de bâtiments couverts.

Piège fréquent : des bailleurs transmettent une étude thermique (Th-C-E ex), un DPE ou un audit
« non réglementaire » à la place d'un audit réglementaire. On les reconnaît par faisceau
d'indices (chaque indice trouvé est conservé pour être montré à l'utilisateur).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

AUDIT_REGLEMENTAIRE = "audit_reglementaire"
AUDIT_NON_REGLEMENTAIRE = "audit_non_reglementaire"
ETUDE_THERMIQUE = "etude_thermique"
DPE = "dpe"
INCONNU = "inconnu"

LIBELLES = {
    AUDIT_REGLEMENTAIRE: "Audit énergétique réglementaire",
    AUDIT_NON_REGLEMENTAIRE: "Audit énergétique NON réglementaire",
    ETUDE_THERMIQUE: "Étude thermique (pas un audit)",
    DPE: "DPE (pas un audit)",
    INCONNU: "Type de document non reconnu",
}

# (motif, poids) — le poids exprime la force de l'indice
SIGNES_AUDIT = [
    (r"Sc[ée]nario\s*(?:n\s*[°º]\s*)?\d?\s*[«\"“]?\s*r[ée]novation\s+en\s+une\s+fois", 2),
    (r"Sc[ée]nario\s*(?:n\s*[°º]\s*)?\d?\s*[«\"“]?\s*r[ée]novation\s+par\s+[ée]tapes", 2),
    (r"R[ée]sultats\s+apr[èe]s\s+travaux", 1),
    (r"Informations\s+auditeur", 1),
    (r"Parcours\s+(?:en\s+(?:1|une)\s+[ée]tape|par\s+[ée]tapes)", 1),
    (r"D[ée]tails?\s+des\s+travaux\s+[ée]nerg[ée]tiques", 1),
]
SIGNES_NON_REGLEMENTAIRE = [
    r"audit\s+[ée]nerg[ée]tique\s+non\s+r[ée]glementaire",
    r"ne\s+constitue\s+pas\s+un\s+audit\s+[ée]nerg[ée]tique\s+au\s+sens",
    r"NON\s+[ÉE]MIS\s+ADEME",
    r"audit\s+(?:[ée]nerg[ée]tique\s+)?incitatif",
    r"^\s*non\s+r[ée]glementaire\s*$",
]
SIGNES_ETUDE = [
    (r"Th\s*-?\s*C\s*-?\s*E\s*-?\s*ex", 3),
    (r"\bRT\s*(?:existant|ex\b|globale)", 2),
    (r"[ée]tude\s+thermique", 2),
    (r"\bCep\s*[-_ ]?\s*r[ée]f\b|\bCepref\b", 2),
    (r"\bCep\s*[-_ ]?\s*max\b", 2),
    (r"\bUb[aâ]t\b", 1),
    (r"\bBbio\b", 1),
    (r"\bTic\s*(?:r[ée]f|max)?\b", 1),
]
SIGNES_DPE_TITRE = r"diagnostic\s+de\s+performance\s+[ée]nerg[ée]tique"
SIGNES_DPE = [
    (r"N\s*[°º]\s*(?:de\s+)?DPE\s*:?\s*\d", 2),
    (r"Recommandations\s+d['’]am[ée]lioration\s+de\s+la\s+performance", 2),
    (r"pack\s+(?:de\s+travaux\s+)?(?:n\s*[°º]\s*)?[12]\b", 1),
    (r"travaux\s+essentiels", 1),
    (r"Ce\s+document\s+(?:vous\s+)?permet\s+de\s+savoir", 1),
]


@dataclass
class TypeDocument:
    code: str
    confiance: str                     # forte | moyenne | faible
    methode: str | None = None         # « 3CL-DPE » | « Th-C-E ex » | None
    indices: list[str] = field(default_factory=list)

    @property
    def libelle(self) -> str:
        return LIBELLES[self.code]

    @property
    def est_audit_reglementaire(self) -> bool:
        return self.code == AUDIT_REGLEMENTAIRE


def _extrait(texte: str, m: re.Match, marge: int = 50) -> str:
    a, b = max(0, m.start() - marge), min(len(texte), m.end() + marge)
    return "…" + re.sub(r"\s+", " ", texte[a:b]).strip() + "…"


def _score(texte: str, signes, indices: list[str]) -> int:
    total = 0
    for motif, poids in signes:
        m = re.search(motif, texte, re.I | re.M)
        if m:
            total += poids
            indices.append(_extrait(texte, m))
    return total


def classer_document(texte: str, num_audit: str | None = None) -> TypeDocument:
    tete = texte[:1500]
    ind_audit: list[str] = []
    ind_etude: list[str] = []
    ind_dpe: list[str] = []
    s_audit = _score(texte, SIGNES_AUDIT, ind_audit)
    s_etude = _score(texte, SIGNES_ETUDE, ind_etude)
    s_dpe = _score(texte, SIGNES_DPE, ind_dpe)
    titre_dpe = re.search(SIGNES_DPE_TITRE, tete, re.I)
    if titre_dpe:
        s_dpe += 3
        ind_dpe.insert(0, _extrait(tete, titre_dpe))

    m3cl = re.search(r"3\s*CL", texte)
    mthc = re.search(r"Th\s*-?\s*C\s*-?\s*E\s*-?\s*ex", texte, re.I)
    methode = "3CL-DPE" if m3cl else ("Th-C-E ex" if mthc else None)

    non_regl = [_extrait(texte, m) for p in SIGNES_NON_REGLEMENTAIRE
                if (m := re.search(p, texte, re.I | re.M))]

    # 1) Étude thermique : méthode Th-C-E ex sans 3CL, ou faisceau d'indices fort sans structure d'audit
    if (mthc and not m3cl) or (s_etude >= 4 and s_audit < 3):
        return TypeDocument(ETUDE_THERMIQUE, "forte" if mthc else "moyenne", methode, ind_etude)
    # 2) DPE : titre DPE en tête de document et pas de structure d'audit
    if s_dpe >= 4 and s_audit < 3:
        return TypeDocument(DPE, "forte" if titre_dpe else "moyenne", methode or "3CL-DPE", ind_dpe)
    # 3) Audit (structure imposée par l'arrêté du 4 mai 2022)
    if s_audit >= 3:
        if non_regl:
            return TypeDocument(AUDIT_NON_REGLEMENTAIRE, "forte", methode, non_regl + ind_audit[:2])
        conf = "forte" if num_audit else "moyenne"
        ind = ind_audit[:3]
        if mthc:
            ind.append("Mentionne aussi Th-C-E ex : vérifier la méthode de calcul.")
        return TypeDocument(AUDIT_REGLEMENTAIRE, conf, methode, ind)
    if non_regl:
        return TypeDocument(AUDIT_NON_REGLEMENTAIRE, "moyenne", methode, non_regl)
    return TypeDocument(INCONNU, "faible", methode, ind_audit + ind_etude + ind_dpe)


# ---------------------------------------------------------------------------------------------
# Nombre de bâtiments couverts — règle métier : 1 audit = 1 bâtiment, sans exception.
# ---------------------------------------------------------------------------------------------
_BAT = r"\b(?i:b[âa]t(?:iment)?\.?)"
RE_NB_BATIMENTS = re.compile(r"nombre\s+de\s+b[âa]timents?\s*:?\s*(\d+)", re.I)
RE_BATIMENTS_PLURIEL = re.compile(
    r"\b(?i:b[âa]timents|b[âa]ts\.?)\s+([A-Z]|\d{1,2})\s*(?:,|et|à|a|-|/|&)\s*([A-Z]|\d{1,2})\b")
# identifiant suivi d'un séparateur (exclut « Ubat W/(m².K) », « bâtiment L'… »)
# singulier suivi d'une plage ou d'une liste : « Bât. 1 à 4 », « Bâtiment A et B » (pas « A, 12 rue »)
RE_BATIMENT_PLAGE = re.compile(_BAT + r"\s+([A-Z]|\d{1,2})\s+(?:à|au|et)\s+([A-Z]|\d{1,2})\b")
RE_ID_BATIMENT = re.compile(_BAT + r"\s+([A-Z]|\d{1,2})(?=[\s,.;:)]|$)")


@dataclass
class Couverture:
    multiple: bool                     # bloquant
    batiment: str | None = None        # identifiant du bâtiment audité (ex. « A »)
    autres_mentions: list[str] = field(default_factory=list)  # autres bâtiments cités (alerte)
    indices: list[str] = field(default_factory=list)


def detecter_batiments(texte: str, adresse: str | None) -> Couverture:
    tete = texte[:3000]
    indices: list[str] = []
    multiple = False

    m = RE_NB_BATIMENTS.search(texte)
    if m and int(m.group(1)) > 1:
        multiple = True
        indices.append(_extrait(texte, m))
    for zone in filter(None, (adresse, tete)):
        m = RE_BATIMENTS_PLURIEL.search(zone) or RE_BATIMENT_PLAGE.search(zone)
        if m:
            multiple = True
            indices.append(_extrait(zone, m))
            break

    principal = None
    if adresse:
        m = RE_ID_BATIMENT.search(adresse)
        principal = m.group(1) if m else None
    cites = []
    for m in RE_ID_BATIMENT.finditer(texte):
        ident = m.group(1)
        if ident != principal and ident not in cites:
            cites.append(ident)
            indices.append(_extrait(texte, m))
    return Couverture(multiple, principal, cites, indices)
