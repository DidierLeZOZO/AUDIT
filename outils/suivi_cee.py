"""Outil « Suivi CEE » : page HTML autonome (100 % local dans le navigateur) intégrée telle quelle.

Pour mettre à jour l'outil : remplacer outils/html/Outil_Suivi_CEE.html.
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from registre import OUTILS
from ui import badge, en_tete, theme_sombre

HTML = Path(__file__).parent / "html" / "Outil_Suivi_CEE.html"

outil = next(o for o in OUTILS if o.url_path == "suivi_cee")
en_tete(outil.titre, "Dépose l'export ODICEE : l'outil prépare les classeurs de suivi et les mails de relance.",
        outil.icone, tags=[badge("🔒 100 % dans votre navigateur", "ok")])
html = HTML.read_text(encoding="utf-8")

# L'outil se croit « dans un aperçu » dès qu'il est dans un cadre (window.self !== window.top) et
# refuse alors d'enregistrer. Le cadre Streamlit autorise les téléchargements : on désactive
# cette seule garde dans la copie servie (le fichier source reste intact).
GARDE = "const IN_PREVIEW = !IN_CLAUDE && (() =>"
assert GARDE in html, "Outil_Suivi_CEE.html a changé : adapter la garde dans outils/suivi_cee.py"
html = html.replace(GARDE, "const IN_PREVIEW = false && (() =>", 1)

# Aligne l'outil sur le thème du tableau de bord (ses variables CSS sont surchargées, son code reste intact).
sombre = theme_sombre()
html = html.replace("<html lang=\"fr\">", f'<html lang="fr" data-theme="{"dark" if sombre else "light"}">', 1)
ACCENT = ("--accent:#4FC3B2;--accent-ink:#06201C;--accent-soft:#12302D;--bg:#0E1719;--surface:#172327;" if sombre
          else "--accent:#0F766E;--accent-ink:#fff;--accent-soft:#E3F3F0;--bg:#F6F8F9;")
# Injecté en toute fin de page : les <style> de l'outil sont dans le <body>, le dernier gagne.
fin = html.rfind("</body>")
assert fin != -1, "Outil_Suivi_CEE.html : balise </body> introuvable"
html = html[:fin] + f"<style>:root,:root[data-theme]{{{ACCENT}}}</style>" + html[fin:]

components.html(html, height=1100, scrolling=True)
