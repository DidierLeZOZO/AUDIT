"""Moteur de règles BAR-TH-177 : estimation de l'éligibilité et du volume à partir d'un audit.

Les identifiants (ID-01, AU-02, PE-01…) renvoient à docs/regles_BAR-TH-177.md.
Niveaux :
- BLOQUANT : critère non rempli -> non éligible ;
- MANQUANT : donnée indispensable absente -> non estimable ;
- RESERVE  : non conforme à la lettre du texte mais estimable (ex. étude thermique complète) ;
- ALERTE   : à vérifier par un humain ; INFO / OK : pour information.
Pour ajouter une règle : écrire un `_res(...)` dans la bonne fonction, avec son id et sa source.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime

from . import referentiel as R
from .document import (AUDIT_NON_REGLEMENTAIRE, AUDIT_REGLEMENTAIRE, DPE, ETUDE_THERMIQUE, Couverture,
                       TypeDocument)
from .enrichissement import type_batiment
from .parser import Batiment, Etape, Scenario

OK, INFO, ALERTE, RESERVE, MANQUANT, BLOQUANT = "ok", "info", "alerte", "reserve", "manquant", "bloquant"
ELIGIBLE, SOUS_RESERVE, NON_ELIGIBLE, NON_ESTIMABLE = "eligible", "reserve", "non_eligible", "non_estimable"
LIBELLE_VERDICT = {
    ELIGIBLE: "Éligible", SOUS_RESERVE: "Éligible sous réserve",
    NON_ELIGIBLE: "Non éligible", NON_ESTIMABLE: "Non estimable",
}
POSTES_QUANTITE = {"Murs", "Plancher", "Planchers bas", "Toiture / Combles", "Menuiseries"}


@dataclass
class Resultat:
    id: str
    titre: str
    niveau: str
    message: str
    source: str = ""


@dataclass
class Hypotheses:
    """Ce que l'audit ne dit pas et que l'utilisateur fixe."""
    coup_de_pouce: bool = True
    surface_saisie: float | None = None     # Shab après rénovation saisie (prioritaire)
    aujourd_hui: date = field(default_factory=date.today)


@dataclass
class EvalScenario:
    id: str
    nom: str
    verdict: str
    resultats: list[Resultat]
    gain: float | None
    coef: int
    coef_raison: str
    surface: float | None
    volume_kwhc: float
    etapes: list[tuple[str, str]] = field(default_factory=list)   # (libellé, verdict de l'étape seule)


@dataclass
class Evaluation:
    document: TypeDocument
    couverture: Couverture
    generaux: list[Resultat]
    scenarios: list[EvalScenario]

    @property
    def meilleur(self) -> EvalScenario | None:
        ok = [s for s in self.scenarios if s.verdict in (ELIGIBLE, SOUS_RESERVE)]
        return max(ok, key=lambda s: (s.verdict == ELIGIBLE, s.volume_kwhc), default=None)


def _d(s: str | None) -> date | None:
    try:
        return datetime.strptime(s, "%d/%m/%Y").date() if s else None
    except ValueError:
        return None


def siren_valide(siren: str | None) -> bool:
    s = re.sub(r"\s", "", siren or "")
    if not re.fullmatch(r"\d{9}", s):
        return False
    t = 0
    for i, c in enumerate(reversed(s)):
        d = int(c) * (2 if i % 2 else 1)
        t += d - 9 if d > 9 else d
    return t % 10 == 0


# ---------------------------------------------------------------------------------------------
# Règles générales : document, auditeur, bâtiment
# ---------------------------------------------------------------------------------------------
def _document(doc: TypeDocument, couv: Couverture, b: Batiment, h: Hypotheses) -> list[Resultat]:
    out = []
    src_art8 = "Fiche §3 ; arrêté du 17/11/2020 art. 8"
    if doc.code == AUDIT_REGLEMENTAIRE:
        out.append(Resultat("AU-01", "Type de document", OK if doc.confiance == "forte" else ALERTE,
                            "Audit énergétique réglementaire." if doc.confiance == "forte" else
                            "Structure d'audit réglementaire, mais n° d'audit ADEME non trouvé : à vérifier.", src_art8))
    elif doc.code == AUDIT_NON_REGLEMENTAIRE:
        out.append(Resultat("AU-02", "Type de document", RESERVE,
                            "Le document se déclare « audit non réglementaire » : non conforme à la lettre de la fiche "
                            "(audit réglementaire transmis à l'ADEME exigé). Estimation donnée sous réserve.", src_art8))
    elif doc.code == ETUDE_THERMIQUE:
        out.append(Resultat("AU-01", "Type de document", RESERVE,
                            f"Étude thermique ({doc.methode or 'méthode non 3CL'}), pas un audit. Valorisable seulement "
                            "si toutes les données sont présentes ; valeurs issues d'une autre méthode que le 3CL-DPE.", src_art8))
    elif doc.code == DPE:
        out.append(Resultat("AU-01", "Type de document", RESERVE,
                            "DPE, pas un audit. Valorisable seulement si Cep/GES avant ET après travaux sont donnés.", src_art8))
    else:
        out.append(Resultat("AU-01", "Type de document", RESERVE,
                            "Type de document non reconnu : vérifier qu'il s'agit bien d'un audit énergétique.", src_art8))

    if couv.multiple:
        out.append(Resultat("AU-17", "Un audit par bâtiment", BLOQUANT,
                            "Le document couvre plusieurs bâtiments : il faut un audit par bâtiment.", "Règle métier"))
    elif couv.autres_mentions:
        out.append(Resultat("AU-17", "Un audit par bâtiment", ALERTE,
                            f"Bâtiment audité : {couv.batiment or '?'} ; le document cite aussi le(s) bâtiment(s) "
                            f"{', '.join(couv.autres_mentions)}. Vérifier que les valeurs ne portent que sur un bâtiment.",
                            "Règle métier"))
    else:
        out.append(Resultat("AU-17", "Un audit par bâtiment", OK, "Un seul bâtiment détecté.", "Règle métier"))

    if doc.methode == "3CL-DPE":
        out.append(Resultat("AU-03", "Méthode de calcul", OK, "Méthode 3CL-DPE.", "Arrêté du 4/05/2022 art. 2"))
    elif doc.code != ETUDE_THERMIQUE:
        out.append(Resultat("AU-03", "Méthode de calcul", ALERTE, "Méthode 3CL-DPE non mentionnée.", "Arrêté du 4/05/2022 art. 2"))

    a = b.auditeur
    if a.logiciel and a.version_logiciel:
        out.append(Resultat("AU-07", "Logiciel et version", OK, f"{a.logiciel} {a.version_logiciel}.", "Fiche §3"))
    else:
        out.append(Resultat("AU-07", "Logiciel et version", ALERTE,
                            "Nom ou version du logiciel absent (mention obligatoire du rapport).", "Fiche §3"))
    q = (a.qualification or "").upper()
    if "1905" in q:
        out.append(Resultat("AU-09", "Qualification auditeur", OK, f"{a.qualification} (collectif).", "Décret 2022-780"))
    elif "1911" in q:
        out.append(Resultat("AU-09", "Qualification auditeur", ALERTE,
                            "OPQIBI 1911 = maisons individuelles : inadaptée au collectif.", "Décret 2022-780"))
    else:
        out.append(Resultat("AU-09", "Qualification auditeur", ALERTE,
                            f"Qualification {'« ' + a.qualification + ' » ' if a.qualification else ''}non reconnue "
                            "ou absente : vérifier (OPQIBI 1905 attendue pour un collectif).", "Décret 2022-780"))
    if not a.siren:
        out.append(Resultat("AU-10", "SIREN du bureau d'études", ALERTE, "SIREN absent.", "Partie A"))
    elif not siren_valide(a.siren):
        out.append(Resultat("AU-10", "SIREN du bureau d'études", ALERTE, f"SIREN « {a.siren} » invalide.", "Partie A"))

    etab = _d(b.date_etablissement)
    visite = _d(b.date_visite)
    if etab:
        fin = etab.replace(year=etab.year + R.VALIDITE_AUDIT_ANS) if not (etab.month == 2 and etab.day == 29) \
            else date(etab.year + R.VALIDITE_AUDIT_ANS, 2, 28)
        if fin < h.aujourd_hui:
            out.append(Resultat("AU-11", "Validité de l'audit", ALERTE,
                                f"Audit expiré depuis le {fin:%d/%m/%Y} (validité {R.VALIDITE_AUDIT_ANS} ans).", "Décret 2022-780"))
        coef = R.coef_electricite(etab)
        out.append(Resultat("AU-19", "Coefficient électricité", INFO,
                            f"Audit établi le {etab:%d/%m/%Y} : coefficient électricité {coef:g}. Cep initial et projet "
                            "doivent venir du même calcul.", "Arrêtés du 13/08/2025 et 19/08/2026"))
    if etab and visite and (etab - visite).days > R.DELAI_RAPPORT_APRES_VISITE_JOURS:
        out.append(Resultat("AU-13", "Délai visite → rapport", ALERTE,
                            f"Rapport établi {(etab - visite).days} jours après la visite ({b.date_visite}) : "
                            "le rapport doit être transmis dans le mois.", "Arrêté du 4/05/2022 art. 4"))
    return out


def _batiment(b: Batiment, h: Hypotheses) -> list[Resultat]:
    out = []
    t = type_batiment(b)
    if t == "collectif":
        out.append(Resultat("ID-01", "Bâtiment collectif", OK, f"« {b.type_bien} ».", "Fiche §1"))
    elif t == "maison":
        out.append(Resultat("ID-01", "Bâtiment collectif", BLOQUANT, "Maison individuelle : relève de BAR-TH-174.", "Fiche §1"))
    elif t == "appartement":
        out.append(Resultat("ID-01", "Bâtiment collectif", BLOQUANT, "Appartement seul : relève de BAR-TH-175.", "Fiche §1"))
    else:
        out.append(Resultat("ID-01", "Bâtiment collectif", ALERTE, "Type de bien non lu : vérifier qu'il s'agit d'un collectif.", "Fiche §1"))

    n = b.nb_logements
    if n is None:
        out.append(Resultat("ID-02", "≥ 3 foyers fiscaux", ALERTE, "Nombre de logements non lu.", "Fiche §3"))
    elif n < R.NB_FOYERS_MIN:
        out.append(Resultat("ID-02", "≥ 3 foyers fiscaux", BLOQUANT, f"{n} logement(s) : il faut au moins 3 foyers fiscaux distincts.", "Fiche §3"))
    else:
        out.append(Resultat("ID-02", "≥ 3 foyers fiscaux", OK, f"{n} logements (foyers fiscaux à justifier au dépôt).", "Fiche §3"))

    cp = b.code_postal
    if cp and cp[:3] in ("971", "972", "973", "974", "975", "976", "977", "978"):
        out.append(Resultat("ID-03", "France métropolitaine", BLOQUANT, f"Code postal {cp} : hors métropole.", "Fiche §1"))
    elif not cp:
        out.append(Resultat("ID-03", "France métropolitaine", ALERTE, "Code postal non lu.", "Fiche §1"))

    if b.annee_construction and b.annee_construction > h.aujourd_hui.year - R.ANCIENNETE_BATIMENT_MIN_ANS:
        out.append(Resultat("ID-04", "Bâtiment de plus de 2 ans", BLOQUANT,
                            f"Construit en {b.annee_construction} : moins de 2 ans à l'engagement.", "Partie A"))

    if h.surface_saisie:
        out.append(Resultat("SU-01", "Surface habitable après rénovation", OK, f"Saisie : {h.surface_saisie:g} m².", "Fiche §5"))
    elif b.shab:
        out.append(Resultat("SU-01", "Surface habitable après rénovation", OK, f"Lue dans l'audit : {b.shab:g} m².", "Fiche §5"))
    elif b.surface_m2:
        out.append(Resultat("SU-01", "Surface habitable après rénovation", ALERTE,
                            f"Seule la surface de RÉFÉRENCE est donnée ({b.surface_m2:g} m²) : elle n'est pas égale à la "
                            "surface habitable. Volume estimé sur cette base, à confirmer.", "Fiche §5"))
    else:
        out.append(Resultat("SU-01", "Surface habitable après rénovation", MANQUANT, "Aucune surface trouvée.", "Fiche §5"))
    if b.mention_extension:
        out.append(Resultat("SU-03", "Surface ajoutée", ALERTE,
                            "Extension / surélévation / combles aménagés évoqués : Shab après rénovation et DP à vérifier.", "Fiche §3"))

    if not b.cep_initial:
        out.append(Resultat("DA-CEP", "Cep initial", MANQUANT, "Cep initial introuvable.", "Fiche §3"))
    if b.ges_initial is None:
        out.append(Resultat("DA-GES", "GES initial", MANQUANT, "GES initial introuvable (critère GES impossible).", "Fiche §3"))
    elif b.fiabilite.get("ges_initial") == "divergent":
        out.append(Resultat("DA-GES", "GES initial", ALERTE, f"Lectures divergentes ; {b.ges_initial:g} retenu : à vérifier.", ""))
    if b.energie_chauffage is None:
        out.append(Resultat("DA-ENR", "Énergie de chauffage avant travaux", ALERTE,
                            "Non déterminée : restriction des chaudières et coefficient Coup de pouce à vérifier.", ""))
    return out


# ---------------------------------------------------------------------------------------------
# Règles par scénario
# ---------------------------------------------------------------------------------------------
def _criteres(b: Batiment, e: Etape) -> tuple[list[Resultat], float | None]:
    """P1 à P3 pour un état après travaux donné (étape finale ou intermédiaire)."""
    out, gain = [], None
    if not e.cep_apres:
        out.append(Resultat("DA-CEP", "Cep projet", MANQUANT, "Cep après travaux introuvable.", "Fiche §3"))
    else:
        ok = e.cep_apres < R.SEUIL_CEP_PROJET
        out.append(Resultat("PE-01", f"Cep projet < {R.SEUIL_CEP_PROJET:g}", OK if ok else BLOQUANT,
                            f"Cep projet {e.cep_apres:g} kWhEP/m².an.", "Fiche §3"))
        if b.cep_initial:
            gain = (b.cep_initial - e.cep_apres) / b.cep_initial
            ok = gain >= R.GAIN_CEP_MIN
            out.append(Resultat("PE-02", f"Gain ≥ {R.GAIN_CEP_MIN:.0%}", OK if ok else BLOQUANT,
                                f"Gain {gain:.2%} = ({b.cep_initial:g} − {e.cep_apres:g}) / {b.cep_initial:g}.", "Fiche §3"))
            if e.economie_pct and abs(gain * 100 - e.economie_pct) > R.TOLERANCE_GAIN_ANNONCE_PTS:
                out.append(Resultat("PE-03", "Gain annoncé", ALERTE,
                                    f"L'audit annonce {e.economie_pct:g} %, le calcul donne {gain:.1%} : une valeur est mal lue ?", ""))
    if e.cep_avec_pv is not None:
        out.append(Resultat("AU-15", "Sans déduction PV", INFO,
                            f"Valeur sans déduction du PV retenue ({e.cep_apres:g}) ; avec déduction : {e.cep_avec_pv:g}.", "Fiche §3"))
    if e.ges_apres is None:
        out.append(Resultat("DA-GES", "GES après travaux", MANQUANT, "GES après travaux introuvable.", "Fiche §3"))
    elif b.ges_initial is not None:
        ok = e.ges_apres <= b.ges_initial
        out.append(Resultat("PE-04", "GES après ≤ GES avant", OK if ok else BLOQUANT,
                            f"GES {b.ges_initial:g} → {e.ges_apres:g} kgCO2eq/m².an.", "Fiche §3"))
        if e.fiabilite.get("ges_apres") == "divergent":
            out.append(Resultat("DA-GES", "GES après travaux", ALERTE, "Lectures divergentes : à vérifier.", ""))
    return out, gain


def _chaudieres(b: Batiment, installes: list[str], e: Etape) -> list[Resultat]:
    out = []
    src = "Fiche §3 (hors raccordement réseau de chaleur)"
    if e.energie_chauffage == "reseau" or "reseau" in installes:
        out.append(Resultat("PE-05", "Chaudières fossiles installées", OK, "Raccordement à un réseau de chaleur : restriction non applicable.", src))
        return out
    for eq in installes:
        if eq in ("chaudiere_fioul", "chaudiere_charbon"):
            out.append(Resultat("PE-05", "Chaudières fossiles installées", BLOQUANT,
                                f"Installation d'une chaudière {eq.split('_')[1]} : inéligible.", src))
        elif eq == "chaudiere_gaz":
            if "pac_hybride" in installes:
                out.append(Resultat("PE-06", "Gaz ≤ 30 % des besoins", ALERTE,
                                    "PAC hybride avec appoint gaz : taux de couverture gaz ≤ 30 % à justifier.", src))
            else:
                out.append(Resultat("PE-06", "Gaz ≤ 30 % des besoins", BLOQUANT,
                                    "Installation d'une chaudière gaz (couverture présumée > 30 %) : inéligible.", src))
        elif eq == "chaudiere_inconnue":
            out.append(Resultat("PE-06", "Chaudières fossiles installées", ALERTE,
                                "Chaudière installée dont l'énergie n'est pas identifiée : vérifier.", src))
    if not any(r.id in ("PE-05", "PE-06") for r in out) and e.energie_chauffage is None and not installes:
        out.append(Resultat("PE-05", "Chaudières fossiles installées", ALERTE,
                            "Énergie de chauffage après travaux inconnue : restriction non vérifiable.", src))
    if not any(r.id in ("PE-05", "PE-06") for r in out):
        out.append(Resultat("PE-05", "Chaudières fossiles installées", OK, "Aucune chaudière charbon / fioul / gaz installée.", src))
    if e.energie_chauffage in R.FOSSILES and not any(x.startswith("chaudiere") for x in installes):
        out.append(Resultat("PE-07", "Équipement fossile conservé", ALERTE,
                            f"Chauffage {R.LIBELLES_ENERGIE[e.energie_chauffage].lower()} conservé : non interdit par la fiche "
                            "à la lettre, mais exclut le ×3. À faire valider.", "Interprétation"))
    return out


def coefficient(b: Batiment, fin: Etape, installes: list[str], h: Hypotheses) -> tuple[int, str, list[Resultat]]:
    src = "Arrêté du 29/12/2014 art. 3-5-3 IV"
    if not h.coup_de_pouce:
        return R.COEF_HORS_CDP, "Hors Coup de pouce", []
    if b.energie_chauffage is None:
        return R.COEF_CDP_AUTRES, "Énergie initiale inconnue : ×2 retenu par prudence", [
            Resultat("VO-02", "Coefficient", ALERTE, "Énergie de chauffage initiale inconnue : ×3 non vérifiable, ×2 retenu.", src)]
    if b.energie_chauffage == "reseau":
        return R.COEF_CDP_AUTRES, "Réseau de chaleur déjà en place : ×2", []
    fossiles = {u: en for u, en in (("chauffage", b.energie_chauffage), ("ECS", b.energie_ecs)) if en in R.FOSSILES}
    if not fossiles:
        return R.COEF_CDP_AUTRES, "Aucun équipement fossile à remplacer : ×2 (autres travaux)", []
    apres = {"chauffage": fin.energie_chauffage, "ECS": fin.energie_ecs}
    restants = [u for u in fossiles if apres.get(u) not in R.RENOUVELABLES]
    if restants:
        detail = ", ".join(f"{u} {R.LIBELLES_ENERGIE.get(apres.get(u), 'non déterminé').lower()}" for u in restants)
        return R.COEF_CDP_AUTRES, f"Fossile non remplacé par du renouvelable ({detail}) : ×2", []
    notes = []
    if "reseau" in (apres["chauffage"], apres["ECS"]):
        notes.append(Resultat("VO-02", "Coefficient ×3", ALERTE,
                              "Nouveau raccordement à un réseau de chaleur : ×3 si le réseau est « efficace » (L.711-4). À confirmer.", src))
    if "pac_hybride" in installes:
        notes.append(Resultat("VO-02", "Coefficient ×3", ALERTE, "PAC hybride : appoint fossile ≤ 30 % à justifier pour le ×3.", src))
    return R.COEF_CDP_SORTIE_FOSSILE, "Tous les équipements fossiles (chauffage + ECS) remplacés par du renouvelable : ×3", notes


def _surface(b: Batiment, h: Hypotheses) -> float | None:
    return h.surface_saisie or b.shab or b.surface_m2


def _verdict(resultats: list[Resultat]) -> str:
    niveaux = {r.niveau for r in resultats}
    if BLOQUANT in niveaux:
        return NON_ELIGIBLE
    if MANQUANT in niveaux:
        return NON_ESTIMABLE
    if RESERVE in niveaux:
        return SOUS_RESERVE
    return ELIGIBLE


def evaluer_scenario(b: Batiment, sc: Scenario, generaux: list[Resultat], h: Hypotheses) -> EvalScenario:
    fin = sc.etapes[-1]
    installes = list(dict.fromkeys(x for e in sc.etapes for x in e.equipements_installes))
    res, gain = _criteres(b, fin)
    res += _chaudieres(b, installes, fin)
    for e in sc.etapes:
        for t in e.travaux:
            if t.poste in POSTES_QUANTITE and not t.quantite:
                res.append(Resultat("TR-05", "Quantités", ALERTE, f"{e.libelle} · {t.poste} : quantité manquante.",
                                    "Arrêté du 4/05/2022"))
    if not any(e.travaux for e in sc.etapes):
        res.append(Resultat("TR-00", "Travaux", ALERTE, "Aucun poste de travaux détecté.", ""))

    coef, raison, notes = coefficient(b, fin, installes, h)
    res += notes
    surface = _surface(b, h)
    verdict = _verdict(generaux + res)
    volume = R.FORFAIT_KWHC_PAR_M2 * surface * coef if verdict in (ELIGIBLE, SOUS_RESERVE) and surface else 0.0

    etapes = []
    if len(sc.etapes) > 1:
        for e in sc.etapes[:-1]:
            r, g = _criteres(b, e)
            v = _verdict(r)
            etapes.append((e.libelle, "éligible seule" if v == ELIGIBLE else
                           f"non valorisable seule ({g:.0%} de gain)" if g is not None else "non estimable seule"))
        res.append(Resultat("PE-09", "Étapes", INFO,
                            "La fiche ne valorise que les travaux réalisés : seule l'étape finale (cumulée) est évaluée. "
                            + " ; ".join(f"{l} : {v}" for l, v in etapes), "Interprétation"))
    return EvalScenario(sc.id, sc.nom.replace("\n", " "), verdict, res, gain, coef, raison, surface, volume, etapes)


def evaluer(doc: TypeDocument, couv: Couverture, b: Batiment, scenarios: list[Scenario],
            h: Hypotheses | None = None) -> Evaluation:
    h = h or Hypotheses()
    generaux = _document(doc, couv, b, h) + _batiment(b, h)
    return Evaluation(doc, couv, generaux, [evaluer_scenario(b, sc, generaux, h) for sc in scenarios])
