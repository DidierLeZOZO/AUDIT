"""Tableau de bord — point d'entrée.   Lancer : streamlit run app.py

Ajouter un outil : créer outils/mon_outil.py, puis l'inscrire dans registre.py.
Apparence : .streamlit/config.toml (thème) et ui/style.css (habillage commun).
"""
from pathlib import Path

import streamlit as st

from audit.parser import PARSER_VERSION
from registre import OUTILS, par_categorie, rechercher
from ui import appliquer_style, carte_outil, en_tete

st.set_page_config(page_title="Pilotage CEE", page_icon="🏢", layout="wide")
st.logo(str(Path(__file__).parent / "assets" / "logo.svg"), size="large")
appliquer_style()


def accueil() -> None:
    en_tete("Pilotage CEE", "Vos outils de suivi et d'audit au même endroit.", "🏠")

    q = st.text_input("Rechercher un outil", placeholder="🔍  audit, odicee, relance, pdf…",
                      label_visibility="collapsed")
    trouves = rechercher(q)
    if not trouves:
        st.info(f"Aucun outil ne correspond à « {q} ».")
    cols = st.columns(4)
    for i, o in enumerate(trouves):
        with cols[i % 4]:
            carte_outil(o)

    with st.expander("Ajouter un nouvel outil"):
        st.markdown("1. Créer `outils/mon_outil.py` (script Streamlit ordinaire).\n"
                    "2. L'inscrire dans `registre.py` : le menu, l'accueil et la recherche se mettent à jour.\n"
                    "3. Pour un outil HTML autonome, copier le modèle de `outils/suivi_cee.py`.")


pages = {"": [st.Page(accueil, title="Accueil", icon="🏠", default=True)]}
for cat, outils in par_categorie().items():
    pages[cat] = [st.Page(o.fichier, title=o.titre, icon=o.icone, url_path=o.url_path) for o in outils]
nav = st.navigation(pages)

with st.sidebar:
    st.html(f'<div class="side-foot">🔒 Les fichiers déposés sont traités en mémoire, jamais stockés.<br>'
            f'{len(OUTILS)} outils · analyseur {PARSER_VERSION}</div>')

nav.run()
