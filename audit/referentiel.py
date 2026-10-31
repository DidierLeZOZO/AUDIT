"""Référentiel BAR-TH-177 : tous les seuils, coefficients et dates en un seul endroit.

Chaque valeur porte sa source et son niveau de vérification. Base complète et discussion :
docs/regles_BAR-TH-177.md ; vérifications faites de notre côté : docs/verification_regles.md.
Si un texte change, c'est ICI qu'on modifie (et on ajuste le test correspondant).
"""
from __future__ import annotations

from datetime import date

FICHE = "BAR-TH-177"
INTITULE = "Rénovation globale d'un bâtiment résidentiel collectif (France métropolitaine)"

# --- Critères d'éligibilité (fiche, identiques vA63.1 / vA80.2) -----------------------------
SEUIL_CEP_PROJET = 331.0     # Cep projet STRICTEMENT inférieur (kWhEP/m².an, 5 usages, sans déduction PV)
GAIN_CEP_MIN = 0.35          # (Cep initial - Cep projet) / Cep initial, comparé SANS arrondi
TAUX_COUVERTURE_GAZ_MAX = 0.30  # chaudière(s) gaz installée(s), hors raccordement réseau de chaleur

# --- Volume -----------------------------------------------------------------------------------
FORFAIT_KWHC_PAR_M2 = 2100   # kWh cumac / m² de surface habitable APRÈS rénovation
COEF_HORS_CDP = 1
COEF_CDP_AUTRES = 2          # Coup de pouce « autres travaux » (dont réseau de chaleur déjà en place)
COEF_CDP_SORTIE_FOSSILE = 3  # Coup de pouce : tous les équipements chauffage ET ECS fossiles -> renouvelable

# --- Audit ------------------------------------------------------------------------------------
VALIDITE_AUDIT_ANS = 5
DELAI_RAPPORT_APRES_VISITE_JOURS = 31
ANCIENNETE_BATIMENT_MIN_ANS = 2
NB_FOYERS_MIN = 3            # foyers fiscaux distincts ; l'audit ne donne que le nb de logements (proxy)
TOLERANCE_GAIN_ANNONCE_PTS = 1.0  # le % affiché par l'audit est arrondi à l'unité

# --- Versions de la fiche (clé = date d'engagement) ------------------------------------------
VERSIONS_FICHE = [
    (date(2024, 11, 1), date(2026, 1, 16), "vA63.1"),
    (date(2026, 1, 17), date(2030, 12, 31), "vA80.2"),
]

# --- Coefficient de conversion de l'électricité en énergie primaire (date d'établissement) ---
COEF_ELEC = [
    (date(1900, 1, 1), date(2025, 12, 31), 2.3),
    (date(2026, 1, 1), date(2026, 12, 31), 1.9),
    (date(2027, 1, 1), date(2100, 1, 1), 1.7),
]

# --- Étiquette DPE (affichage uniquement : PAS un critère de la fiche 177) -------------------
# Double seuil : la classe retenue est la plus mauvaise des deux (énergie / climat).
DPE_SEUILS = [("A", 70, 6), ("B", 110, 11), ("C", 180, 30), ("D", 250, 50), ("E", 330, 70), ("F", 420, 100)]

# --- Énergies ------------------------------------------------------------------------------
FOSSILES = {"gaz", "fioul", "charbon"}
RENOUVELABLES = {"reseau", "bois", "solaire", "pac"}   # « reseau » : sous réserve d'un réseau efficace
LIBELLES_ENERGIE = {
    "gaz": "Gaz", "fioul": "Fioul", "charbon": "Charbon", "electricite": "Électricité (effet Joule)",
    "pac": "Pompe à chaleur", "reseau": "Réseau de chaleur", "bois": "Bois / biomasse",
    "solaire": "Solaire", None: "Non déterminé",
}

# --- Niveau de vérification de chaque élément (affiché dans l'interface) --------------------
# « vérifié » = recoupé par plusieurs sources publiques le 31/10/2026 (textes officiels non
# accessibles depuis l'environnement de développement) ; « base » = issu de la base de règles
# seule ; « décision » = arbitrage métier de l'utilisateur.
VERIFICATION = {
    "SEUIL_CEP_PROJET": "vérifié",
    "GAIN_CEP_MIN": "vérifié",
    "GES": "vérifié",
    "FORFAIT": "vérifié",
    "COEF_3": "vérifié",
    "COEF_2_RESEAU_EXISTANT": "décision",
    "TAUX_GAZ": "vérifié (Coup de pouce) / base (fiche)",
    "UN_AUDIT_PAR_BATIMENT": "décision",
    "DPE_SEUILS": "vérifié",
    "SURFACE": "vérifié : surface de référence ≠ surface habitable",
    "VALIDITE_5_ANS": "base",
    "QUALIFICATION_AUDITEUR": "base",
}


def version_fiche(d: date | None) -> str | None:
    if d is None:
        return None
    for debut, fin, v in VERSIONS_FICHE:
        if debut <= d <= fin:
            return v
    return None


def coef_electricite(d: date | None) -> float | None:
    if d is None:
        return None
    for debut, fin, v in COEF_ELEC:
        if debut <= d <= fin:
            return v
    return None


def classe_dpe(cep: float | None, ges: float | None = None) -> str | None:
    """Classe DPE double seuil ; sans GES, classe énergie seule (alors potentiellement trop favorable)."""
    if cep is None:
        return None

    def lettre(val: float, idx: int) -> str:
        for l, *seuils in DPE_SEUILS:
            if val <= seuils[idx]:
                return l
        return "G"

    l_cep = lettre(cep, 0)
    if ges is None:
        return l_cep
    return max(l_cep, lettre(ges, 1))  # « A » < « G » : max = la plus mauvaise
