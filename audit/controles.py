"""Contrôles de cohérence sur ce qui a été extrait (et éventuellement corrigé à la main).

Chaque règle est une petite fonction : pour en ajouter une, l'écrire et l'ajouter à REGLES.
Aucun contrôle n'affirme une règle d'éligibilité CEE : ils ne détectent que des incohérences
internes ou des champs manquants.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from .parser import Batiment, Scenario, cep_to_etiquette

ERREUR, ALERTE, INFO = "erreur", "alerte", "ok"
ORDRE = {ERREUR: 0, ALERTE: 1, INFO: 2}
LETTRES = "ABCDEFG"
POSTES_AVEC_QUANTITE = {"Murs", "Plancher", "Planchers bas", "Toiture / Combles", "Menuiseries"}


@dataclass(frozen=True)
class Controle:
    niveau: str      # ERREUR | ALERTE | INFO
    message: str
    ou: str = ""     # zone concernée (affichée en petit)


def siren_valide(siren: str | None) -> bool:
    """9 chiffres + clé de Luhn."""
    s = re.sub(r"\s", "", siren or "")
    if not re.fullmatch(r"\d{9}", s):
        return False
    total = 0
    for i, c in enumerate(reversed(s)):
        d = int(c) * (2 if i % 2 else 1)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


def classes_gagnees(avant: str | None, apres: str | None) -> int | None:
    if avant and apres and avant.upper() in LETTRES and apres.upper() in LETTRES:
        return LETTRES.index(avant.upper()) - LETTRES.index(apres.upper())
    return None


def _batiment(b: Batiment, scs: list[Scenario]) -> list[Controle]:
    out = []
    if b.non_reglementaire:
        out.append(Controle(ERREUR, "Le document se déclare « Audit énergétique non réglementaire » : "
                                    "à ne pas utiliser pour un dossier exigeant un audit réglementaire.", "Document"))
    for champ, val in (("Adresse", b.adresse), ("Bénéficiaire", b.beneficiaire)):
        if not (val or "").strip():
            out.append(Controle(ALERTE, f"{champ} non renseigné(e) : apparaîtra vide dans l'Excel.", "Bâtiment"))
    if not b.surface_m2 or b.surface_m2 <= 0:
        out.append(Controle(ALERTE, "Surface de référence absente ou nulle.", "Bâtiment"))
    if not b.cep_initial or b.cep_initial <= 0:
        out.append(Controle(ERREUR, "CEP initial absent : impossible de comparer les scénarios.", "Bâtiment"))
    else:
        calc = cep_to_etiquette(b.cep_initial)
        if b.etiquette_initiale and calc and b.etiquette_initiale.upper() != calc:
            out.append(Controle(ALERTE, f"Étiquette initiale saisie ({b.etiquette_initiale}) ≠ étiquette calculée "
                                        f"depuis le CEP ({calc}). Normal si le GES est plus défavorable, sinon à vérifier.", "Bâtiment"))
    return out


def _auditeur(b: Batiment, scs: list[Scenario]) -> list[Controle]:
    a = b.auditeur
    out = []
    if not (a.raison_sociale or "").strip():
        out.append(Controle(ALERTE, "Raison sociale de l'auditeur manquante.", "Auditeur"))
    if not a.siren:
        out.append(Controle(ALERTE, "SIREN de l'auditeur manquant.", "Auditeur"))
    elif not siren_valide(a.siren):
        out.append(Controle(ERREUR, f"SIREN « {a.siren} » invalide (9 chiffres et clé de contrôle).", "Auditeur"))
    if not a.date_audit:
        out.append(Controle(ALERTE, "Date d'établissement de l'audit manquante.", "Auditeur"))
    return out


def _scenarios(b: Batiment, scs: list[Scenario]) -> list[Controle]:
    out = []
    for sc in scs:
        nom = sc.nom.replace("\n", " ")
        for i, e in enumerate(sc.etapes, 1):
            ou = nom + (f" · {e.libelle}" if len(sc.etapes) > 1 else "")
            if not e.travaux:
                out.append(Controle(ERREUR, "Aucun poste de travaux détecté.", ou))
            if not e.cep_apres:
                out.append(Controle(ERREUR, "CEP après travaux manquant.", ou))
                continue
            if b.cep_initial and e.cep_apres >= b.cep_initial:
                out.append(Controle(ERREUR, f"CEP après ({e.cep_apres:g}) ≥ CEP avant ({b.cep_initial:g}) : "
                                            "le scénario n'améliore rien, valeur mal lue ?", ou))
            elif b.cep_initial and e.economie_pct:
                reel = (1 - e.cep_apres / b.cep_initial) * 100
                if abs(reel - e.economie_pct) > 5:
                    out.append(Controle(ALERTE, f"Économie annoncée {e.economie_pct:g} % mais le CEP donne "
                                                f"{reel:.0f} % : l'un des deux est mal lu (ou l'économie porte sur autre chose).", ou))
            calc = cep_to_etiquette(e.cep_apres)
            if e.etiquette_apres and calc and e.etiquette_apres.upper() != calc:
                out.append(Controle(ALERTE, f"Étiquette après ({e.etiquette_apres}) ≠ étiquette calculée du CEP ({calc}).", ou))
            for t in e.travaux:
                if t.poste in POSTES_AVEC_QUANTITE and not t.quantite:
                    out.append(Controle(ALERTE, f"{t.poste} : surface/quantité manquante.", ou))
    return out


REGLES: list[Callable[[Batiment, list[Scenario]], list[Controle]]] = [_batiment, _auditeur, _scenarios]


def controler(b: Batiment, scs: list[Scenario]) -> list[Controle]:
    res = [c for regle in REGLES for c in regle(b, scs)]
    res.sort(key=lambda c: ORDRE[c.niveau])
    return res


def resume(controles: list[Controle]) -> dict[str, int]:
    return {n: sum(c.niveau == n for c in controles) for n in (ERREUR, ALERTE)}
