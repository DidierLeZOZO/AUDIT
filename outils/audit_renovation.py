"""Outil « Audit énergétique — rénovation globale » : extraction par règles, sans IA.

Page du tableau de bord (voir app.py). Logique métier dans le paquet `audit/` ;
ce fichier ne contient que l'interface.
"""
import copy
import io
import re
from html import escape

import pandas as pd
import streamlit as st

from audit.controles import ERREUR, INFO, classes_gagnees, controler, resume
from audit.excel_export import generer_excel
from audit.parser import PARSER_VERSION, Travail, parse_audit_pdf
from audit.pdf_export import generate_pdf
from audit.synthese import tableau_comparatif
from ui import badge, en_tete, etapes, pastille_etiquette

COL_POSTE, COL_NATURE, COL_CARAC, COL_QTE = (
    "Poste", "Nature (phrase courte)", "Caractéristiques / Marque et référence", "Surface / Quantité")
ICONES = {ERREUR: "⛔", "alerte": "⚠️", INFO: "✅"}


@st.cache_data(show_spinner=False, max_entries=5)
def analyser_audit(pdf_bytes: bytes, version_parser: str):
    """Mise en cache ; `version_parser` invalide le cache quand le parseur évolue."""
    return parse_audit_pdf(io.BytesIO(pdf_bytes))


def _s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)


def _flux_etiquette(avant, apres) -> str:
    return (f'<span class="dpe-flow">{pastille_etiquette(avant)}<span class="arr">→</span>'
            f'{pastille_etiquette(apres)}</span>')


# ---------------------------------------------------------------------------------------------
# En-tête + dépôt du fichier
# ---------------------------------------------------------------------------------------------
en_tete("Audit énergétique — rénovation globale",
        "Dépose un audit réglementaire : scénarios, travaux et cohérence sont extraits, puis exportés.",
        "🏢", tags=[badge("Sans IA", "acc"), badge("🔒 En mémoire", "ok")])

uploaded = st.file_uploader("Audit énergétique (PDF)", type=["pdf"], label_visibility="collapsed",
                            help="Un seul PDF à la fois. Taille max 50 Mo.")

if uploaded is None:
    etapes([("Déposer", "le PDF de l'audit"), ("Vérifier", "contrôles + corrections"),
            ("Exporter", "Excel et PDF bailleur")], actuelle=0)
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown("**Ce qui est extrait**")
        st.caption("Bâtiment, CEP/CEF avant-après, étiquettes, économies, auditeur, "
                   "postes de travaux avec caractéristiques et quantités.")
    with c2.container(border=True):
        st.markdown("**Formats testés**")
        st.caption("LICIEL, Climawin, Pleiades, DPEWIN, ANALYSIMMO (structure de l'arrêté du 4 mai 2022). "
                   "Un autre format peut demander d'ajuster `audit/parser.py`.")
    with c3.container(border=True):
        st.markdown("**Ce qui reste à vous**")
        st.caption("Relire : l'étiquette déduite du CEP seul peut être trop favorable (le GES compte aussi). "
                   "Tout est modifiable avant export.")
    st.stop()

pdf_source = uploaded.getvalue()
with st.spinner("Analyse de l'audit…"):
    try:
        # Copie profonde : les objets en cache ne doivent pas être modifiés par les champs éditables.
        batiment, scenarios = copy.deepcopy(analyser_audit(pdf_source, PARSER_VERSION))
    except Exception as exc:  # PDF scanné, chiffré, corrompu…
        st.error(f"Lecture du PDF impossible ({type(exc).__name__}). Le fichier est peut-être scanné "
                 f"(image sans texte), protégé ou corrompu.")
        st.stop()

if not scenarios:
    st.error("Aucun scénario détecté : la mise en page diffère des formats déjà gérés. "
             "Il faudra adapter les regex de `audit/parser.py`.")
    st.stop()

# Préfixe de clés lié au fichier : réinitialise les widgets quand un autre PDF est chargé.
fkey = f"{uploaded.name}_{uploaded.size}"

# Zones remplies en fin de script (elles reflètent les corrections faites plus bas).
zone_etapes = st.container()
zone_kpi = st.container()
zone_controles = st.container()

tab_bat, tab_sc, tab_cmp = st.tabs(["📋 Bâtiment & auditeur", "🔍 Scénarios & export", "📊 Comparatif"])

# ---------------------------------------------------------------------------------------------
# Onglet 1 : bâtiment + auditeur
# ---------------------------------------------------------------------------------------------
with tab_bat:
    st.subheader("Bâtiment")
    c1, c2 = st.columns(2)
    with c1:
        batiment.adresse = st.text_input("Adresse", batiment.adresse or "", key=f"adresse_{fkey}")
        batiment.beneficiaire = st.text_input("Bénéficiaire / Propriétaire", batiment.beneficiaire or "", key=f"benef_{fkey}")
        batiment.surface_m2 = st.number_input("Surface de référence (m²)", value=float(batiment.surface_m2 or 0), step=1.0, key=f"surface_{fkey}")
    with c2:
        batiment.cep_initial = st.number_input("CEP initial (kWhEP/m²/an)", value=float(batiment.cep_initial or 0), step=1.0, key=f"cepi_{fkey}")
        batiment.cef_initial = st.number_input("CEF initial (kWhEF/m²/an)", value=float(batiment.cef_initial or 0), step=1.0, key=f"cefi_{fkey}")
        batiment.etiquette_initiale = st.text_input("Étiquette initiale (A-G)", batiment.etiquette_initiale or "", key=f"etqi_{fkey}")

    st.subheader("Auditeur")
    aud = batiment.auditeur
    a1, a2, a3 = st.columns(3)
    with a1:
        aud.raison_sociale = st.text_input("Raison sociale", aud.raison_sociale or "", key=f"aud_rs_{fkey}")
        aud.siren = st.text_input("Numéro SIREN", aud.siren or "", key=f"aud_siren_{fkey}")
    with a2:
        aud.date_audit = st.text_input("Date de l'audit énergétique", aud.date_audit or "", key=f"aud_date_{fkey}")
        aud.reference_audit = st.text_input("Référence de l'audit énergétique", aud.reference_audit or "",
                                            placeholder="Non indiquée", key=f"aud_ref_{fkey}")
    with a3:
        aud.logiciel = st.text_input("Nom du logiciel", aud.logiciel or "", key=f"aud_log_{fkey}")
        aud.version_logiciel = st.text_input("N° de version", aud.version_logiciel or "",
                                             placeholder="Non indiqué", key=f"aud_ver_{fkey}")

# ---------------------------------------------------------------------------------------------
# Onglet 2 : détail par scénario, correction, export
# ---------------------------------------------------------------------------------------------
with tab_sc:
    sous_tabs = st.tabs([sc.nom.replace("\n", " ") for sc in scenarios])
    for tab, sc in zip(sous_tabs, scenarios):
        with tab:
            resume_sc = st.container()  # rempli après les étapes (valeurs corrigées)

            for ei, e in enumerate(sc.etapes):
                k = f"{fkey}_{sc.id}_{ei}"
                with st.container(border=True):
                    st.markdown(f"**{e.libelle}**")
                    with st.expander("Corriger les valeurs après travaux"):
                        m1, m2, m3, m4 = st.columns(4)
                        e.cep_apres = m1.number_input("CEP après", value=float(e.cep_apres or 0), step=1.0, key=f"cep_{k}")
                        e.cef_apres = m2.number_input("CEF après", value=float(e.cef_apres or 0), step=1.0, key=f"cef_{k}")
                        e.etiquette_apres = m3.text_input("Étiquette après", e.etiquette_apres or "", key=f"lbl_{k}")
                        e.economie_pct = m4.number_input("Économie %", value=float(e.economie_pct or 0), step=1.0, key=f"eco_{k}")

                    st.caption("Travaux détectés — modifiables, lignes ajoutables (➕) ou supprimables.")
                    df_in = pd.DataFrame(
                        [{COL_POSTE: t.poste, COL_NATURE: t.nature_courte,
                          COL_CARAC: t.caracteristiques, COL_QTE: t.quantite} for t in e.travaux],
                        columns=[COL_POSTE, COL_NATURE, COL_CARAC, COL_QTE], dtype=object)
                    edited = st.data_editor(df_in, num_rows="dynamic", width="stretch",
                                            hide_index=True, key=f"travaux_{k}")
                    e.travaux = [
                        Travail(poste=_s(r[COL_POSTE]), nature_courte=_s(r[COL_NATURE]),
                                caracteristiques=_s(r[COL_CARAC]), quantite=_s(r[COL_QTE]))
                        for r in edited.to_dict("records") if _s(r[COL_POSTE]) or _s(r[COL_NATURE])
                    ]

            # Résumé du scénario (état final, après corrections)
            fin = sc.etapes[-1]
            with resume_sc:
                with st.container(border=True):
                    r1, r2, r3, r4 = st.columns(4)
                    with r1:
                        st.caption("Étiquette")
                        st.html(_flux_etiquette(batiment.etiquette_initiale, fin.etiquette_apres))
                        g = classes_gagnees(batiment.etiquette_initiale, fin.etiquette_apres)
                        if g is not None:
                            st.caption(f"{g:+d} classe(s)" if g else "aucune classe gagnée")
                    r2.metric("CEP après", f"{fin.cep_apres:g}" if fin.cep_apres else "—",
                              delta=f"{fin.cep_apres - batiment.cep_initial:g}" if fin.cep_apres and batiment.cep_initial else None,
                              delta_color="inverse", help="kWhEP/m²/an — variation par rapport à l'état initial")
                    r3.metric("Économie", f"{fin.economie_pct:g} %" if fin.economie_pct else "—")
                    r4.metric("Postes de travaux", sum(len(e.travaux) for e in sc.etapes),
                              help="Toutes étapes confondues")

            with st.container(border=True):
                st.markdown("**Exporter ce scénario**")
                colA, colB = st.columns(2)
                with colA:
                    st.caption("PDF pour le bailleur : récapitulatif des scénarios (celui-ci en évidence) "
                               "+ fiche des travaux avec champs « réalisés » remplissables.")
                    st.download_button(
                        "📄 Télécharger le PDF bailleur",
                        data=generate_pdf(batiment, scenarios, scenario_choisi_id=sc.id),
                        file_name=f"Fiche_travaux_{sc.id}.pdf", mime="application/pdf",
                        key=f"dlpdf_{sc.id}", width="stretch")
                with colB:
                    prefill = st.checkbox(
                        "Pré-remplir les « travaux réalisés »", value=False, key=f"prefill_{fkey}_{sc.id}",
                        help="Désactivé par défaut : l'audit ne dit rien des travaux réellement réalisés. "
                             "Pré-remplis, ils risquent d'être transmis sans vérification après chantier.")
                    st.download_button(
                        "📥 Télécharger l'Excel « Liste des travaux »",
                        data=generer_excel(batiment, sc, prefill_realises=prefill),
                        file_name=f"Liste_travaux_{sc.id}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"dl_{sc.id}", width="stretch", type="primary")

# ---------------------------------------------------------------------------------------------
# Onglet 3 : comparatif
# ---------------------------------------------------------------------------------------------
with tab_cmp:
    st.caption("Une colonne par scénario · ✅ / ❌ selon la présence de chaque type de travaux (valeurs corrigées).")
    st.dataframe(pd.DataFrame(tableau_comparatif(batiment, scenarios)).astype(str), width="stretch")

# ---------------------------------------------------------------------------------------------
# Zones du haut, remplies maintenant que toutes les corrections sont connues
# ---------------------------------------------------------------------------------------------
controles = controler(batiment, scenarios)
bilan = resume(controles)

with zone_etapes:
    etapes([("Déposer", uploaded.name[:34]), ("Vérifier", "contrôles + corrections"),
            ("Exporter", "onglet Scénarios")], actuelle=1 if bilan[ERREUR] else 2)

with zone_kpi:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Surface de référence", f"{batiment.surface_m2:,.0f} m²".replace(",", " ") if batiment.surface_m2 else "—",
              border=True, help=f"{batiment.nb_logements} logement(s)" if batiment.nb_logements else None)
    with k2.container(border=True):
        st.caption("Étiquette · CEP initial")
        st.html(f'<span class="dpe-flow">{pastille_etiquette(batiment.etiquette_initiale)} '
                f'<span style="font-size:1.6rem;font-weight:700">{batiment.cep_initial:g}</span>'
                f'<small style="opacity:.6">kWhEP/m²/an</small></span>' if batiment.cep_initial else "—")
    k3.metric("Scénarios détectés", len(scenarios), border=True,
              help=" · ".join(sc.nom.replace("\n", " ") for sc in scenarios))
    with k4.container(border=True):
        st.caption("Contrôles de cohérence")
        if bilan[ERREUR] or bilan["alerte"]:
            st.html('<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.5rem">'
                    + (badge(f"⛔ {bilan[ERREUR]} erreur(s)", "bad") if bilan[ERREUR] else "")
                    + (badge(f"⚠️ {bilan['alerte']} alerte(s)", "warn") if bilan["alerte"] else "") + "</div>")
        else:
            st.html('<div style="margin-top:.5rem">' + badge("✓ Aucun écart", "ok") + "</div>")

with zone_controles:
    if controles:
        with st.expander(f"Contrôles de cohérence — {bilan[ERREUR]} erreur(s), {bilan['alerte']} alerte(s)",
                         expanded=bool(bilan[ERREUR]), icon="🛡️"):
            st.html("".join(
                f'<div class="ctl {c.niveau}"><span class="i">{ICONES[c.niveau]}</span>'
                f'<div>{escape(c.message)}' + (f'<div class="where">{escape(c.ou)}</div>' if c.ou else "") + "</div></div>"
                for c in controles))
    else:
        st.html('<div class="ctl ok"><span class="i">✅</span><div>Tous les contrôles de cohérence sont passés.</div></div>')
