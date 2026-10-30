"""Registre des outils du tableau de bord.

Ajouter un outil = créer outils/mon_outil.py (script Streamlit ordinaire) puis ajouter une ligne ici.
Le menu, l'accueil et la recherche se mettent à jour tout seuls.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Outil:
    fichier: str
    titre: str
    icone: str
    categorie: str
    description: str
    mots_cles: tuple[str, ...] = ()
    statut: str = "stable"          # "stable" | "beta"
    entree: str = ""                # ce que l'outil attend
    sortie: str = ""                # ce qu'il produit

    @property
    def url_path(self) -> str:
        return self.fichier.rsplit("/", 1)[-1].removesuffix(".py")


OUTILS: list[Outil] = [
    Outil("outils/audit_renovation.py", "Audit rénovation globale", "🏢", "Audit & rénovation",
          "Lit un audit énergétique réglementaire, détecte les scénarios de travaux et contrôle la cohérence.",
          ("audit", "scénario", "dpe", "cep", "travaux", "bailleur", "pdf"),
          entree="Audit énergétique (PDF)", sortie="Fiche Excel + PDF bailleur"),
    Outil("outils/suivi_cee.py", "Suivi des dossiers CEE", "📑", "Suivi & dépôt",
          "Transforme l'export ODICEE en classeurs de suivi par bailleur, avec mails de relance.",
          ("odicee", "suivi", "dépôt", "relance", "dossiers", "mail", "bailleur"),
          entree="Export ODICEE (.xlsx)", sortie="Classeurs Excel de suivi"),
]


def par_categorie(outils: list[Outil] | None = None) -> dict[str, list[Outil]]:
    out: dict[str, list[Outil]] = {}
    for o in outils if outils is not None else OUTILS:
        out.setdefault(o.categorie, []).append(o)
    return out


def rechercher(requete: str) -> list[Outil]:
    q = requete.strip().lower()
    if not q:
        return list(OUTILS)
    return [o for o in OUTILS
            if q in " ".join((o.titre, o.description, o.categorie, *o.mots_cles)).lower()]
