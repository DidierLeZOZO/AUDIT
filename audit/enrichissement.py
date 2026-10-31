"""Compléments d'extraction nécessaires à la fiche BAR-TH-177 (GES, énergies, équipements, surfaces).

Principe de fiabilité : chaque valeur décisive est cherchée par plusieurs méthodes indépendantes.
- « concordant » : au moins deux méthodes trouvent la même valeur ;
- « unique »     : une seule méthode a trouvé (plausible, à relire) ;
- « divergent »  : les méthodes ne sont pas d'accord (valeur prioritaire retenue, à vérifier).
Structure ciblée : le modèle de rapport de l'arrêté du 4 mai 2022 (intitulés communs aux logiciels).
"""
from __future__ import annotations

import re
from collections import Counter

from .parser import Batiment, Etape, Scenario, Travail, _num
from .referentiel import classe_dpe

NB = r"(\d+(?:[.,]\d+)?)"
RE_UNITE_GES = r"kg\s*(?:[ée]q\.?\s*)?CO\s*[₂2]\s*(?:[ée]q\.?)?\s*/\s*m\s*[²2]"

ENERGIES = [  # ordre = priorité de reconnaissance (motifs longs d'abord)
    ("reseau", r"r[ée]seau\s+de\s+chaleur|r[ée]seau\s+urbain|chauffage\s+urbain|\bRCU\b"),
    ("gaz", r"gaz\s+naturel|\bgaz\b|\bGPL\b|propane|butane"),
    ("fioul", r"fioul|\bfuel\b"),
    ("charbon", r"charbon"),
    ("bois", r"\bbois\b|granul[ée]s?|plaquettes?|b[ûu]ches?|biomasse"),
    ("solaire", r"solaire"),
    ("electricite", r"[ée]lectri(?:que|cit[ée])"),
]
RE_ENERGIE = re.compile("|".join(f"(?P<{k}>{m})" for k, m in ENERGIES), re.I)
# PAC, y compris chauffe-eau thermodynamique (CET) pour l'ECS
RE_PAC = re.compile(r"pompe\s+[àa]\s+chaleur|\bPAC\b|thermodynamique|\bCET\b", re.I)


def _fmt(v: float) -> str:
    return f"{v:g}"


def _decider(cands: list[tuple[str, float]], tol: float = 0.0) -> tuple[float | None, str | None]:
    """cands = [(méthode, valeur)] par ordre de priorité -> (valeur retenue, fiabilité)."""
    if not cands:
        return None, None
    ref = cands[0][1]
    methodes_ok = {m for m, v in cands if abs(v - ref) <= tol}
    if len({m for m, _ in cands}) == 1:
        return ref, "unique"
    if all(abs(v - ref) <= tol for _, v in cands):
        return ref, "concordant" if len(methodes_ok) >= 2 else "unique"
    return ref, "divergent"


# ---------------------------------------------------------------------------------------------
# GES
# ---------------------------------------------------------------------------------------------
def _ges_apres_cep(zone: str, cep: float | None) -> list[float]:
    """Ligne « <CEP> <GES> » : présentation des étiquettes du modèle de rapport (« 169 25* »)."""
    if cep is None:
        return []
    return [_num(m.group(1)) for m in re.finditer(rf"(?m)^\s*{re.escape(_fmt(cep))}\s+{NB}\s*\*?\s*$", zone)]


def _ges_avant_unite(zone: str) -> list[float]:
    """Nombre suivi de l'unité kgCO2/m²/an (même ligne ou ligne suivante), hors réductions « -18 »."""
    out = []
    for m in re.finditer(rf"(?<![-−\d.,]){NB}\s*\*?\s*\n?\s*{RE_UNITE_GES}", zone, re.I):
        avant = zone[max(0, m.start() - 3): m.start()]
        if "-" in avant or "(" in avant:
            continue
        out.append(_num(m.group(1)))
    return out


def ges_initial(texte: str, cep_initial: float | None) -> tuple[float | None, str | None]:
    fin = re.search(r"Montants?\s+et\s+consommations\s+annuels", texte, re.I)
    zone = texte[: fin.start() if fin else 4000]
    cands = [("ligne CEP/GES", v) for v in _ges_apres_cep(texte[: (fin.end() + 6000) if fin else 8000], cep_initial)]
    cands += [("unité kgCO2", v) for v in _ges_avant_unite(zone)]
    return _decider(cands)


def ges_etape(e: Etape, ges_init: float | None) -> tuple[float | None, str | None]:
    i = e.bloc.lower().find("ésultats après travaux")
    zone = e.bloc[i: i + 1500] if i != -1 else e.bloc
    cands = [("ligne CEP/GES", v) for v in _ges_apres_cep(zone, e.cep_apres)]
    cands += [("unité kgCO2", v) for v in _ges_avant_unite(zone)]
    m = re.search(rf"\(\s*[-−]\s*{NB}\s*{RE_UNITE_GES}", zone, re.I)
    if m and ges_init is not None:
        cands.append(("initial − réduction", ges_init - _num(m.group(1))))
    # la réduction est souvent arrondie : tolérance de 1,5 kg
    return _decider(cands, tol=1.5)


# ---------------------------------------------------------------------------------------------
# Énergies (tableau « usage chauffage / eau chaude / … ») et équipements installés
# ---------------------------------------------------------------------------------------------
def _tokens_energie(ligne: str) -> list[str]:
    return [m.lastgroup for m in RE_ENERGIE.finditer(ligne)]


def energies_tableau(zone: str) -> tuple[str | None, str | None]:
    """Ligne des énergies sous l'en-tête « usage chauffage eau chaude … » : 1re = chauffage, 2e = ECS."""
    m = re.search(r"usage\s+chauffage\s+eau\s+chaude[^\n]*\n", zone, re.I)
    if not m:
        return None, None
    for ligne in zone[m.end():].split("\n")[:4]:
        if re.search(r"\d", ligne):
            continue
        toks = _tokens_energie(ligne)
        if toks:
            return toks[0], (toks[1] if len(toks) > 1 else None)
    return None, None


def energie_description(texte: str) -> str | None:
    """Repli : énergie de la 1re mention d'un générateur de chauffage."""
    m = re.search(r"(chaudi[èe]re[^\n]{0,40}|pompe\s+[àa]\s+chaleur|r[ée]seau\s+de\s+chaleur|\bRCU\b|"
                  r"convecteurs?|radiateurs?\s+[ée]lectriques?|po[êe]le[^\n]{0,30})", texte, re.I)
    if not m:
        return None
    frag = m.group(0)
    if RE_PAC.search(frag):
        return "pac"
    if re.search(r"convecteur|radiateurs?\s+[ée]lectrique", frag, re.I):
        return "electricite"
    toks = _tokens_energie(frag)
    return toks[0] if toks else None


def equipements(travaux: list[Travail]) -> list[str]:
    """Équipements installés d'après les postes Chauffage / ECS d'une étape."""
    out: list[str] = []
    for t in travaux:
        if t.poste not in ("Chauffage", "Eau chaude sanitaire"):
            continue
        txt = " ".join((t.nature_courte, t.caracteristiques, t.description))
        if RE_PAC.search(txt):
            out.append("pac_hybride" if re.search(r"hybride", txt, re.I) else "pac")
        if re.search(r"raccordement|sous[- ]?station", txt, re.I) and re.search(r"RCU|r[ée]seau", txt, re.I):
            out.append("reseau")
        for m in re.finditer(r"chaudi[èe]re[^.\n]{0,60}", txt, re.I):
            toks = [k for k in _tokens_energie(m.group(0)) if k != "electricite"]
            out.append(f"chaudiere_{toks[0]}" if toks else "chaudiere_inconnue")
        if re.search(r"solaire", txt, re.I):
            out.append("solaire")
    return list(dict.fromkeys(out))


def _energie_depuis_equipements(eq: list[str]) -> str | None:
    for e in eq:
        if e in ("pac", "pac_hybride"):
            return "pac"
        if e == "reseau":
            return "reseau"
        if e.startswith("chaudiere_") and e != "chaudiere_inconnue":
            return e.removeprefix("chaudiere_")
    return None


# ---------------------------------------------------------------------------------------------
# Identification du bâtiment
# ---------------------------------------------------------------------------------------------
def identification(texte: str, b: Batiment) -> None:
    tete = texte[:4000]
    m = re.search(r"type\s+de\s+bien\s*:?[ \t]*([^\n]+)", tete, re.I)
    b.type_bien = m.group(1).strip() if m else None
    if b.adresse:
        m = re.search(r"\b(\d{5})\b", b.adresse)
        b.code_postal = m.group(1) if m else None
    m = re.search(r"ann[ée]e\s+de\s+construction\s*:?\s*(\d{4})", tete, re.I)
    b.annee_construction = int(m.group(1)) if m else None
    m = re.search(r"date\s+d['’]\s*[ée]tablissement\s*:?\s*(\d{2}/\d{2}/\d{4})", tete, re.I)
    b.date_etablissement = m.group(1) if m else (b.auditeur.date_audit if b.auditeur else None)
    m = re.search(r"surface\s+habitable[^\n\d]{0,40}?:?\s*([\d\s.,]+)\s*m", texte, re.I)
    b.shab = _num(m.group(1)) if m else None
    b.mention_extension = bool(re.search(
        r"sur[ée]l[ée]vation|extension\s+(?:du\s+b[âa]timent|de\s+\d)|am[ée]nagement\s+des\s+combles|"
        r"combles\s+am[ée]nag[ée]s\s+apr[èe]s", texte, re.I))
    if b.auditeur and not b.auditeur.qualification:
        m = re.search(r"Qualification\s*:?[ \t]*(OPQIBI\s*\d{4}|[^\n]{3,40})", texte, re.I)
        b.auditeur.qualification = re.split(r"\s{2,}|\s+(?:tel|email|logiciel)\b", m.group(1), flags=re.I)[0].strip() if m else None


def type_batiment(b: Batiment) -> str | None:
    """collectif | maison | appartement | None, d'après le champ « type de bien »."""
    t = (b.type_bien or "").lower()
    if re.search(r"collectif|immeuble|copropri", t):
        return "collectif"
    if "maison" in t:
        return "maison"
    if "appartement" in t:
        return "appartement"
    return None


# ---------------------------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------------------------
def enrichir(texte: str, b: Batiment, scenarios: list[Scenario]) -> None:
    identification(texte, b)

    b.ges_initial, f = ges_initial(texte, b.cep_initial)
    b.fiabilite["ges_initial"] = f or "absent"

    debut = re.search(r"Montants?\s+et\s+consommations\s+annuels", texte, re.I)
    ch, ecs = energies_tableau(texte[debut.start(): debut.start() + 3000] if debut else texte[:8000])
    b.fiabilite["energies_avant"] = "tableau" if ch else "absent"
    if not ch:
        vue = re.search(r"Vue\s+d['’]ensemble\s+des\s+[ée]quipements", texte, re.I)
        ch = energie_description(texte[vue.start(): vue.start() + 1500] if vue else texte[:8000])
        b.fiabilite["energies_avant"] = "description" if ch else "absent"
    b.energie_chauffage, b.energie_ecs = ch, ecs
    # étiquette : double seuil quand le GES est connu (sauf lettre explicitement écrite)
    if b.ges_initial is not None and not re.search(r"lettre\s+[A-G]\b", texte[:3000]):
        b.etiquette_initiale = classe_dpe(b.cep_initial, b.ges_initial)

    for sc in scenarios:
        for e in sc.etapes:
            e.ges_apres, f = ges_etape(e, b.ges_initial)
            e.fiabilite["ges_apres"] = f or "absent"
            e.equipements_installes = equipements(e.travaux)
            ch, ecs = energies_tableau(e.bloc)
            e.fiabilite["energies_apres"] = "tableau" if ch else "absent"
            if not ch:
                ch = _energie_depuis_equipements(e.equipements_installes)
                e.fiabilite["energies_apres"] = "travaux" if ch else "absent"
            e.energie_chauffage, e.energie_ecs = ch, ecs
            # PAC : le tableau indique « électrique » -> on précise l'équipement
            if e.energie_chauffage == "electricite" and any(x.startswith("pac") for x in e.equipements_installes):
                e.energie_chauffage = "pac"
            # PV : Cep avec déduction s'il diffère (le parseur retient déjà la valeur sans déduction)
            m_sans = re.search(r"sans\s+d[ée]duction", e.bloc, re.I)
            if m_sans:
                tot = [_num(x) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*EP\s*\(", e.bloc[:m_sans.start()])]
                if tot and e.cep_apres and min(tot[-1:]) < e.cep_apres:
                    e.cep_avec_pv = tot[-1]
            if e.ges_apres is not None and not re.search(r"lettre\s+[A-G]\b", e.bloc):
                e.etiquette_apres = classe_dpe(e.cep_apres, e.ges_apres)
        # Les étapes suivantes héritent des énergies de l'étape précédente si non lues
        for prev, cur in zip(sc.etapes, sc.etapes[1:]):
            cur.energie_chauffage = cur.energie_chauffage or prev.energie_chauffage
            cur.energie_ecs = cur.energie_ecs or prev.energie_ecs


# ---------------------------------------------------------------------------------------------
# Documents hors structure d'audit (étude thermique, DPE…) : valeurs étiquetées « Cep projet = … »
# ---------------------------------------------------------------------------------------------
_SEP = r"\s*(?:\([^)\n]{0,25}\))?\s*[:=]?\s*"
ETIQUETTES = {
    "cep_initial": rf"\bCep\s*[-_ ]?\s*(?:initial|init|avant(?:\s+travaux)?|existant|[ée]tat\s+initial){_SEP}{NB}",
    "cep_projet": rf"\bCep\s*[-_ ]?\s*(?:projet|apr[èe]s(?:\s+travaux)?|final|r[ée]nov[ée]){_SEP}{NB}",
    "ges_initial": rf"\b(?:GES|[ée]missions?\s+(?:de\s+)?(?:GES|CO\s*[₂2]))\s*[-_ ]?\s*(?:initial(?:es)?|avant(?:\s+travaux)?|existant){_SEP}{NB}",
    "ges_projet": rf"\b(?:GES|[ée]missions?\s+(?:de\s+)?(?:GES|CO\s*[₂2]))\s*[-_ ]?\s*(?:projet|apr[èe]s(?:\s+travaux)?|final){_SEP}{NB}",
    "shab": rf"\b(?:SHAB|surface\s+habitable)(?:\s+apr[èe]s\s+r[ée]novation)?{_SEP}{NB}",
}


def valeurs_etiquetees(texte: str) -> dict[str, float]:
    out = {}
    for cle, motif in ETIQUETTES.items():
        m = re.search(motif, texte, re.I)
        if m:
            out[cle] = _num(m.group(1))
    return out


def scenario_depuis_etiquettes(texte: str, b: Batiment) -> Scenario | None:
    """Construit un scénario unique « Projet » quand le document donne Cep initial / projet étiquetés."""
    v = valeurs_etiquetees(texte)
    if "cep_projet" not in v:
        return None
    b.cep_initial = b.cep_initial or v.get("cep_initial")
    if b.ges_initial is None and "ges_initial" in v:
        b.ges_initial, b.fiabilite["ges_initial"] = v["ges_initial"], "unique"
    b.shab = b.shab or v.get("shab")
    e = Etape(libelle="Projet", cep_apres=v["cep_projet"], ges_apres=v.get("ges_projet"), bloc=texte)
    e.fiabilite["ges_apres"] = "unique" if e.ges_apres is not None else "absent"
    if b.cep_initial and e.cep_apres:
        e.economie_pct = round((1 - e.cep_apres / b.cep_initial) * 100)
    e.etiquette_apres = classe_dpe(e.cep_apres, e.ges_apres)
    return Scenario(id="scenario_projet", nom="Projet (valeurs déclarées dans le document)", etapes=[e])
