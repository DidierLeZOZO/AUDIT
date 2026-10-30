"""Outil « Audit énergétique — rénovation globale » : extraction par règles, sans IA.

Page du tableau de bord (voir app.py). Logique métier dans le paquet `audit/`.
"""
import copy
import io
import re

import pandas as pd
import streamlit as st

from audit.excel_export import generer_excel
from audit.parser import PARSER_VERSION, Travail, parse_audit_pdf
from audit.pdf_export import generate_pdf
from audit.synthese import tableau_comparatif


@st.cache_data(show_spinner=False, max_entries=5)
def analyser_audit(pdf_bytes: bytes, version_parser: str):
    """Mise en cache ; `version_parser` invalide le cache quand le parseur évolue."""
    return parse_audit_pdf(io.BytesIO(pdf_bytes))


def _s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)


COL_POSTE, COL_NATURE, COL_CARAC, COL_QTE = (
    "Poste", "Nature (phrase courte)", "Caractéristiques / Marque et référence", "Surface / Quantité")

st.title("🏢 Audit énergétique — rénovation globale")
st.caption(
    "Extraction 100 % par règles (regex), aucun appel IA. Dépose un audit réglementaire (PDF) : "
    "l'outil détecte les scénarios, leurs CEP/CEF avant/après et les postes de travaux, puis génère "
    "la fiche « Liste des travaux et entreprises » (Excel) et le PDF bailleur.")

with st.expander("ℹ️ Fiabilité de l'extraction"):
    st.markdown(
        "- Testé sur LICIEL, Climawin, Pleiades, DPEWIN, ANALYSIMMO (structure de l'arrêté du 4 mai 2022).\n"
        "- L'étiquette A→G est parfois un dessin vectoriel illisible : récupérée via « atteindre la lettre X », "
        "sinon calculée depuis le CEP.\n"
        "- L'étiquette déduite du seul CEP peut être **trop favorable** : l'étiquette DPE est la plus mauvaise "
        "des notes énergie (CEP) et climat (GES). À vérifier si elle conditionne l'éligibilité.\n"
        "- **Tout est éditable avant export** : relis toujours le résultat.")

uploaded = st.file_uploader("Audit énergétique (PDF)", type=["pdf"])
if uploaded is None:
    st.info("Dépose un fichier PDF d'audit énergétique pour lancer l'analyse.")
    st.stop()

pdf_source = uploaded.getvalue()
with st.spinner("Analyse de l'audit…"):
    try:
        # Copie profonde : les objets en cache ne doivent pas être modifiés par les champs éditables.
        batiment, scenarios = copy.deepcopy(analyser_audit(pdf_source, PARSER_VERSION))
    except Exception as exc:  # PDF scanné, chiffré, corrompu…
        st.error(f"Lecture du PDF impossible : {exc}")
        st.stop()

if not scenarios:
    st.error("Aucun scénario détecté : la mise en page diffère des formats déjà gérés. "
             "Il faudra adapter les regex de `audit/parser.py`.")
    st.stop()

# Préfixe de clés lié au fichier : réinitialise les widgets quand un autre PDF est chargé.
fkey = f"{uploaded.name}_{uploaded.size}"

# --- Bâtiment -------------------------------------------------------------------------------
st.header("📋 Bâtiment")
c1, c2 = st.columns(2)
with c1:
    batiment.adresse = st.text_input("Adresse", batiment.adresse or "", key=f"adresse_{fkey}")
    batiment.beneficiaire = st.text_input("Bénéficiaire / Propriétaire", batiment.beneficiaire or "", key=f"benef_{fkey}")
    batiment.surface_m2 = st.number_input("Surface de référence (m²)", value=float(batiment.surface_m2 or 0), step=1.0, key=f"surface_{fkey}")
with c2:
    batiment.cep_initial = st.number_input("CEP initial (kWhEP/m²/an)", value=float(batiment.cep_initial or 0), step=1.0, key=f"cepi_{fkey}")
    batiment.cef_initial = st.number_input("CEF initial (kWhEF/m²/an)", value=float(batiment.cef_initial or 0), step=1.0, key=f"cefi_{fkey}")
    batiment.etiquette_initiale = st.text_input("Étiquette initiale (A-G)", batiment.etiquette_initiale or "", key=f"etqi_{fkey}")

st.divider()

# --- Auditeur -------------------------------------------------------------------------------
st.header("🧾 Informations générales de l'auditeur")
aud = batiment.auditeur
manquants = [lbl for lbl, v in (
    ("Raison sociale", aud.raison_sociale), ("SIREN", aud.siren), ("Date de l'audit", aud.date_audit),
    ("Référence de l'audit", aud.reference_audit), ("Logiciel", aud.logiciel),
    ("N° de version", aud.version_logiciel)) if not v]
if manquants:
    st.caption("Non trouvé dans l'audit (à compléter si besoin) : " + ", ".join(manquants))

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
if aud.siren and not re.fullmatch(r"\d{9}", aud.siren.replace(" ", "")):
    st.warning("⚠️ Le SIREN doit comporter 9 chiffres.")

st.divider()

# --- Détail, correction, export (avant le comparatif : il doit refléter les corrections) ----
detail_zone = st.container()
st.divider()
comparatif_zone = st.container()

with detail_zone:
    st.header("🔍 Détail, correction et export")
    tabs = st.tabs([sc.nom.replace("\n", " ") for sc in scenarios])
    for tab, sc in zip(tabs, scenarios):
        with tab:
            for ei, e in enumerate(sc.etapes):
                with st.container(border=True):
                    st.markdown(f"**{e.libelle}**")
                    m1, m2, m3, m4 = st.columns(4)
                    k = f"{fkey}_{sc.id}_{ei}"
                    e.cep_apres = m1.number_input("CEP après", value=float(e.cep_apres or 0), step=1.0, key=f"cep_{k}")
                    e.cef_apres = m2.number_input("CEF après", value=float(e.cef_apres or 0), step=1.0, key=f"cef_{k}")
                    e.etiquette_apres = m3.text_input("Étiquette après", e.etiquette_apres or "", key=f"lbl_{k}")
                    e.economie_pct = m4.number_input("Économie %", value=float(e.economie_pct or 0), step=1.0, key=f"eco_{k}")

                    st.markdown("_Travaux détectés (modifiable) :_")
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

            colA, colB = st.columns(2)
            with colA:
                st.download_button(
                    "📄 Télécharger le PDF à envoyer au bailleur",
                    data=generate_pdf(batiment, scenarios, scenario_choisi_id=sc.id),
                    file_name=f"Fiche_travaux_{sc.id}.pdf", mime="application/pdf", key=f"dlpdf_{sc.id}",
                    help="Page 1 : récapitulatif des scénarios (retenu en évidence). Pages suivantes : "
                         "fiche des travaux avec champs « réalisés » remplissables.")
            with colB:
                prefill = st.checkbox(
                    "Pré-remplir les « travaux réalisés » avec les travaux préconisés",
                    value=False, key=f"prefill_{fkey}_{sc.id}",
                    help="Désactivé par défaut : l'audit ne dit rien des travaux réellement réalisés. "
                         "Pré-remplis, ils risquent d'être transmis sans vérification après chantier.")
                st.download_button(
                    f"📥 Télécharger l'Excel — {sc.nom.strip()}",
                    data=generer_excel(batiment, sc, prefill_realises=prefill),
                    file_name=f"Liste_travaux_{sc.id}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_{sc.id}")

with comparatif_zone:
    st.header("📊 Comparatif des scénarios")
    st.caption("Une colonne par scénario · ✅ / ❌ pour la présence de chaque type de travaux")
    st.dataframe(pd.DataFrame(tableau_comparatif(batiment, scenarios)).astype(str), width="stretch")
