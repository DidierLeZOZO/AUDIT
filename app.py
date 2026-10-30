"""Tableau de bord — point d'entrée.   Lancer : streamlit run app.py

Ajouter un outil : créer outils/mon_outil.py (un script Streamlit ordinaire), puis
l'ajouter à la liste OUTILS ci-dessous.
"""
import streamlit as st

st.set_page_config(page_title="Tableau de bord", page_icon="🏢", layout="wide")

# (fichier, titre dans le menu, icône, description affichée sur l'accueil)
OUTILS = [
    ("outils/audit_renovation.py", "Audit rénovation globale", "🏢",
     "Analyse d'un audit énergétique PDF : scénarios, travaux, export Excel et PDF bailleur."),
    ("outils/suivi_cee.py", "Suivi CEE", "📑",
     "Export ODICEE (.xlsx) vers classeurs Excel de suivi des dossiers (outil HTML intégré)."),
    # ("outils/mon_outil.py", "Mon outil", "🧰", "Ce qu'il fait."),
]


def accueil():
    st.title("🏢 Tableau de bord")
    st.caption("Choisis un outil dans le menu de gauche ou ci-dessous.")
    cols = st.columns(3)
    for i, (chemin, titre, icone, desc) in enumerate(OUTILS):
        with cols[i % 3].container(border=True):
            st.subheader(f"{icone} {titre}")
            st.write(desc)
            st.page_link(chemin, label="Ouvrir", icon="➡️")


pages = [st.Page(accueil, title="Accueil", icon="🏠", default=True)]
pages += [st.Page(c, title=t, icon=i, url_path=c.split("/")[-1][:-3]) for c, t, i, _ in OUTILS]
st.navigation(pages).run()
