"""Composants d'interface partagés par tous les outils (un seul endroit pour changer l'allure)."""
from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

CSS = Path(__file__).with_name("style.css")


def appliquer_style() -> None:
    """À appeler une fois, dans app.py, avant la navigation."""
    st.html(f"<style>{CSS.read_text(encoding='utf-8')}</style>")


def theme_sombre() -> bool:
    try:
        return st.context.theme.type == "dark"
    except Exception:
        return False


def badge(texte: str, ton: str = "") -> str:
    """Pastille HTML (ton : ok | warn | bad | acc | vide)."""
    return f'<span class="tag {ton}">{escape(texte)}</span>'


def pastille_etiquette(lettre: str | None) -> str:
    l = (lettre or "").strip().upper()[:1]
    cls = l if l in "ABCDEFG" and l else "unk"
    return f'<span class="dpe {cls}">{escape(l or "?")}</span>'


def en_tete(titre: str, sous_titre: str = "", icone: str = "", tags: list[str] | None = None) -> None:
    ico = f'<div class="ico">{escape(icone)}</div>' if icone else ""
    sub = f"<p>{escape(sous_titre)}</p>" if sous_titre else ""
    t = f'<div class="tags">{"".join(tags)}</div>' if tags else ""
    st.html(f'<div class="hero">{ico}<div><h1>{escape(titre)}</h1>{sub}</div>{t}</div>')


def etapes(libelles: list[tuple[str, str]], actuelle: int) -> None:
    """Fil d'étapes. `actuelle` : index (0-based) de l'étape en cours."""
    items = []
    for i, (titre, detail) in enumerate(libelles):
        etat = "done" if i < actuelle else "now" if i == actuelle else ""
        n = "✓" if i < actuelle else str(i + 1)
        items.append(f'<div class="st {etat}"><span class="n">{n}</span>'
                     f'<div><b>{escape(titre)}</b><small>{escape(detail)}</small></div></div>')
    st.html(f'<div class="stepper">{"".join(items)}</div>')


def carte_outil(o) -> None:
    with st.container(border=True):
        st.html('<span class="card-marker"></span>')
        statut = badge("Bêta", "warn") if o.statut == "beta" else ""
        st.html(f'<div class="card-cat">{escape(o.categorie)}</div>'
                f'<div style="font-size:1.15rem;font-weight:700;margin:.2rem 0">{escape(o.icone)} {escape(o.titre)} {statut}</div>')
        st.html(f'<div class="card-desc">{escape(o.description)}</div>')
        if o.entree or o.sortie:
            st.html(f'<div class="card-io">⬇️ {escape(o.entree)}<br>⬆️ {escape(o.sortie)}</div>')
        st.page_link(o.fichier, label="Ouvrir l'outil", icon="➡️", width="stretch")
