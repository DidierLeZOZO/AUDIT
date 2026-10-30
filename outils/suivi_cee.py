"""Outil « Suivi CEE » : page HTML autonome (100 % local dans le navigateur) intégrée telle quelle.

Pour mettre à jour l'outil : remplacer outils/html/Outil_Suivi_CEE.html.
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

HTML = Path(__file__).parent / "html" / "Outil_Suivi_CEE.html"

st.title("📑 Suivi des dossiers CEE")
st.caption("Outil HTML intégré : lit l'export ODICEE (.xlsx) dans votre navigateur et produit les classeurs de "
           "suivi. Aucune donnée n'est envoyée au serveur.")
html = HTML.read_text(encoding="utf-8")

# L'outil se croit « dans un aperçu » dès qu'il est dans un cadre (window.self !== window.top) et
# refuse alors d'enregistrer. Le cadre Streamlit autorise les téléchargements : on désactive
# cette seule garde dans la copie servie (le fichier source reste intact).
GARDE = "const IN_PREVIEW = !IN_CLAUDE && (() =>"
assert GARDE in html, "Outil_Suivi_CEE.html a changé : adapter la garde dans outils/suivi_cee.py"
html = html.replace(GARDE, "const IN_PREVIEW = false && (() =>", 1)

components.html(html, height=1100, scrolling=True)
