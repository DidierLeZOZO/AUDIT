"""Outil « Audit énergétique — rénovation globale » : lecture d'un audit et estimation BAR-TH-177.

Extraction par règles (sans IA) dans `audit/` ; règles de la fiche dans `audit/regles.py` et
`audit/referentiel.py`. Ce fichier ne contient que l'interface.
"""
import copy
import io
from html import escape

import pandas as pd
import streamlit as st

from audit import referentiel as R
from audit.analyse import analyser_pdf
from audit.excel_export import generer_excel
from audit.parser import PARSER_VERSION, Travail
from audit.pdf_export import generate_pdf
from audit.regles import (ALERTE, BLOQUANT, INFO, LIBELLE_VERDICT, MANQUANT, OK, RESERVE, Hypotheses, evaluer)
from audit.synthese import tableau_comparatif
from ui import badge, en_tete, etapes, pastille_etiquette

COL_POSTE, COL_NATURE, COL_CARAC, COL_QTE = (
    "Poste", "Nature (phrase courte)", "Caractéristiques / Marque et référence", "Surface / Quantité")
ICONES = {BLOQUANT: "⛔", MANQUANT: "❓", RESERVE: "⚠️", ALERTE: "⚠️", INFO: "ℹ️", OK: "✅"}
ORDRE = {BLOQUANT: 0, MANQUANT: 1, RESERVE: 2, ALERTE: 3, INFO: 4, OK: 5}
ENERGIES = [None, "gaz", "fioul", "charbon", "electricite", "pac", "reseau", "bois", "solaire"]
EQUIPEMENTS = {
    "reseau": "Raccordement réseau de chaleur", "pac": "Pompe à chaleur", "pac_hybride": "PAC hybride (appoint gaz)",
    "chaudiere_gaz": "Chaudière gaz", "chaudiere_fioul": "Chaudière fioul", "chaudiere_charbon": "Chaudière charbon",
    "chaudiere_bois": "Chaudière bois / biomasse", "chaudiere_inconnue": "Chaudière (énergie ?)", "solaire": "Solaire",
}
FIAB = {"concordant": "2 lectures concordantes", "unique": "1 seule lecture", "divergent": "lectures divergentes",
        "absent": "non trouvé", "tableau": "tableau des consommations", "description": "description des équipements",
        "travaux": "déduit des travaux"}


@st.cache_data(show_spinner=False, max_entries=5)
def analyser(pdf_bytes: bytes, version_parser: str):
    """Mise en cache ; `version_parser` invalide le cache quand le parseur évolue."""
    return analyser_pdf(io.BytesIO(pdf_bytes))


def _s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)


def _n(v, suffixe="") -> str:
    return "—" if v is None else f"{v:,.0f}".replace(",", " ") + suffixe if abs(v) >= 1000 else f"{v:g}{suffixe}"


def _num_input(col, label, valeur, key, **kw):
    """Champ numérique vide quand la valeur n'a pas été lue (0 ≠ inconnu)."""
    return col.number_input(label, value=None if valeur is None else float(valeur), step=1.0,
                            placeholder="non lu", key=key, **kw)


def _ligne_resultat(r) -> str:
    src = f'<span class="src">· {escape(r.id)}{" · " + escape(r.source) if r.source else ""}</span>'
    return (f'<div class="ctl {r.niveau}"><span class="i">{ICONES[r.niveau]}</span>'
            f'<div><b>{escape(r.titre)}</b> — {escape(r.message)}{src}</div></div>')


def _crit(titre: str, r, valeur: str | None = None) -> str:
    """Tuile de critère : valeur courte, message complet au survol."""
    if r is None:
        return f'<div class="crit na"><div class="t">{escape(titre)}</div><div class="v">non évalué</div></div>'
    cls = "ok" if r.niveau == OK else "ko" if r.niveau in (BLOQUANT, MANQUANT) else ""
    ico = "✓" if r.niveau == OK else "✗" if r.niveau == BLOQUANT else "?" if r.niveau == MANQUANT else "!"
    txt = valeur if valeur and r.niveau != MANQUANT else r.message.split(" : ")[0].rstrip(".")
    return (f'<div class="crit {cls}" title="{escape(r.message)}"><div class="t">{escape(titre)}</div>'
            f'<div class="v">{ico} {escape(txt)}</div></div>')


# ---------------------------------------------------------------------------------------------
# En-tête + dépôt
# ---------------------------------------------------------------------------------------------
en_tete("Audit énergétique — rénovation globale",
        f"Lecture d'un audit et estimation {R.FICHE} : éligibilité, coefficient, volume de CEE.",
        "🏢", tags=[badge("Sans IA", "acc"), badge("🔒 En mémoire", "ok")])

uploaded = st.file_uploader("Audit énergétique (PDF)", type=["pdf"], label_visibility="collapsed",
                            help="Un PDF = un bâtiment. Taille max 50 Mo.")

if uploaded is None:
    etapes([("Déposer", "le PDF de l'audit"), ("Vérifier", "verdict, alertes, corrections"),
            ("Exporter", "Excel et PDF bailleur")], actuelle=0)
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown("**Ce qui est estimé**")
        st.caption(f"Les 4 critères {R.FICHE} (Cep projet < {R.SEUIL_CEP_PROJET:g}, gain ≥ {R.GAIN_CEP_MIN:.0%}, "
                   "GES non dégradé, pas de chaudière fossile installée), le coefficient Coup de pouce et le volume "
                   f"({R.FORFAIT_KWHC_PAR_M2} kWh cumac/m² × surface habitable).")
    with c2.container(border=True):
        st.markdown("**Pièges reconnus**")
        st.caption("Étude thermique (Th-C-E ex), DPE, audit « non réglementaire », audit couvrant plusieurs "
                   "bâtiments. Valorisation sous réserve seulement si toutes les données sont présentes.")
    with c3.container(border=True):
        st.markdown("**Ce qui reste à vous**")
        st.caption("Relire les valeurs signalées « 1 seule lecture » ou divergentes, et confirmer la surface "
                   "habitable : l'audit donne souvent la surface de référence, qui n'est pas la même.")
    st.stop()

with st.spinner("Analyse du document…"):
    try:
        # Copie profonde : les objets en cache ne doivent pas être modifiés par les champs éditables.
        an = copy.deepcopy(analyser(uploaded.getvalue(), PARSER_VERSION))
    except Exception as exc:  # PDF scanné, chiffré, corrompu…
        st.error(f"Lecture du PDF impossible ({type(exc).__name__}). Le fichier est peut-être scanné "
                 "(image sans texte), protégé ou corrompu.")
        st.stop()

if not an.texte.strip():
    st.error("Le PDF ne contient pas de texte (document scanné ?) : lecture impossible sans reconnaissance de caractères.")
    st.stop()

batiment, scenarios = an.batiment, an.scenarios
fkey = f"{uploaded.name}_{uploaded.size}"   # réinitialise les champs quand un autre PDF est chargé

# Zones remplies en fin de script, quand toutes les corrections sont connues
zone_verdict = st.container()

with st.expander("⚙️ Hypothèses de calcul (ce que l'audit ne dit pas)", expanded=False):
    h1, h2, h3 = st.columns(3)
    cdp = h1.toggle("Coup de pouce (charte signée)", value=True, key=f"cdp_{fkey}",
                    help="×3 : tous les équipements fossiles de chauffage ET d'ECS remplacés par du renouvelable. "
                         "×2 : autres travaux (dont réseau de chaleur déjà en place). Sans Coup de pouce : ×1.")
    surface_defaut = batiment.shab or batiment.surface_m2
    surface = _num_input(h2, "Surface habitable après rénovation (m²)", surface_defaut, f"shab_{fkey}",
                         help="Base du volume. Pré-remplie avec la surface habitable lue, sinon la surface de "
                              "référence de l'audit (à corriger si vous connaissez la Shab).")
    prix = _num_input(h3, "Prix de valorisation (€/MWh cumac)", None, f"prix_{fkey}",
                      help="Facultatif : affiche une estimation en euros.")
hyp = Hypotheses(coup_de_pouce=cdp, surface_saisie=surface if surface != surface_defaut else None)

tab_elig, tab_bat, tab_sc, tab_cmp = st.tabs(
    [f"✅ Éligibilité {R.FICHE}", "📋 Bâtiment & auditeur", "🔍 Scénarios & export", "📊 Comparatif"])

# ---------------------------------------------------------------------------------------------
# Onglet Bâtiment & auditeur
# ---------------------------------------------------------------------------------------------
with tab_bat:
    st.subheader("Bâtiment")
    c1, c2, c3 = st.columns(3)
    batiment.adresse = c1.text_input("Adresse", batiment.adresse or "", key=f"adresse_{fkey}")
    batiment.beneficiaire = c1.text_input("Bénéficiaire / Propriétaire", batiment.beneficiaire or "", key=f"benef_{fkey}")
    batiment.type_bien = c1.text_input("Type de bien", batiment.type_bien or "", key=f"type_{fkey}")
    nb = _num_input(c2, "Nombre de logements", batiment.nb_logements, f"nblog_{fkey}")
    batiment.nb_logements = int(nb) if nb is not None else None
    batiment.surface_m2 = _num_input(c2, "Surface de référence (m²)", batiment.surface_m2, f"surface_{fkey}")
    batiment.code_postal = c2.text_input("Code postal", batiment.code_postal or "", key=f"cp_{fkey}") or None
    batiment.cep_initial = _num_input(c3, "Cep initial (kWhEP/m².an)", batiment.cep_initial, f"cepi_{fkey}")
    batiment.cef_initial = _num_input(c3, "Cef initial (kWhEF/m².an)", batiment.cef_initial, f"cefi_{fkey}")
    batiment.ges_initial = _num_input(c3, "GES initial (kgCO2eq/m².an)", batiment.ges_initial, f"gesi_{fkey}")
    e1, e2, e3 = st.columns(3)
    batiment.energie_chauffage = e1.selectbox("Énergie de chauffage avant travaux", ENERGIES,
                                              index=ENERGIES.index(batiment.energie_chauffage), key=f"ench_{fkey}",
                                              format_func=lambda k: R.LIBELLES_ENERGIE[k])
    batiment.energie_ecs = e2.selectbox("Énergie ECS avant travaux", ENERGIES, index=ENERGIES.index(batiment.energie_ecs),
                                        key=f"enecs_{fkey}", format_func=lambda k: R.LIBELLES_ENERGIE[k])
    batiment.etiquette_initiale = R.classe_dpe(batiment.cep_initial, batiment.ges_initial)
    e3.caption("Étiquette initiale (double seuil Cep + GES, information seulement)")
    e3.html(pastille_etiquette(batiment.etiquette_initiale))

    st.subheader("Auditeur")
    aud = batiment.auditeur
    a1, a2, a3 = st.columns(3)
    aud.raison_sociale = a1.text_input("Raison sociale", aud.raison_sociale or "", key=f"aud_rs_{fkey}")
    aud.siren = a1.text_input("Numéro SIREN", aud.siren or "", key=f"aud_siren_{fkey}")
    aud.qualification = a1.text_input("Qualification", aud.qualification or "", key=f"aud_q_{fkey}") or None
    aud.date_audit = a2.text_input("Date de l'audit", aud.date_audit or "", key=f"aud_date_{fkey}")
    batiment.date_visite = a2.text_input("Date de visite", batiment.date_visite or "", key=f"visite_{fkey}") or None
    aud.reference_audit = a2.text_input("Référence (n° ADEME)", aud.reference_audit or "", placeholder="Non indiquée",
                                        key=f"aud_ref_{fkey}")
    aud.logiciel = a3.text_input("Logiciel", aud.logiciel or "", key=f"aud_log_{fkey}")
    aud.version_logiciel = a3.text_input("Version", aud.version_logiciel or "", placeholder="Non indiquée", key=f"aud_ver_{fkey}")
    batiment.date_etablissement = batiment.date_etablissement or aud.date_audit

# ---------------------------------------------------------------------------------------------
# Onglet Scénarios : corrections + export
# ---------------------------------------------------------------------------------------------
with tab_sc:
    if not scenarios:
        st.info("Aucun scénario de travaux lisible dans ce document.")
    sous_tabs = st.tabs([sc.nom.replace("\n", " ") for sc in scenarios]) if scenarios else []
    for tab, sc in zip(sous_tabs, scenarios):
        with tab:
            for ei, e in enumerate(sc.etapes):
                k = f"{fkey}_{sc.id}_{ei}"
                with st.container(border=True):
                    st.markdown(f"**{e.libelle}**")
                    m1, m2, m3, m4 = st.columns(4)
                    e.cep_apres = _num_input(m1, "Cep après", e.cep_apres, f"cep_{k}")
                    e.cef_apres = _num_input(m2, "Cef après", e.cef_apres, f"cef_{k}")
                    e.ges_apres = _num_input(m3, "GES après", e.ges_apres, f"ges_{k}")
                    e.economie_pct = _num_input(m4, "Gain annoncé %", e.economie_pct, f"eco_{k}")
                    n1, n2, n3 = st.columns([1, 1, 2])
                    e.energie_chauffage = n1.selectbox("Chauffage après", ENERGIES, index=ENERGIES.index(e.energie_chauffage),
                                                       key=f"ench_{k}", format_func=lambda x: R.LIBELLES_ENERGIE[x])
                    e.energie_ecs = n2.selectbox("ECS après", ENERGIES, index=ENERGIES.index(e.energie_ecs),
                                                 key=f"enecs_{k}", format_func=lambda x: R.LIBELLES_ENERGIE[x])
                    e.equipements_installes = n3.multiselect("Équipements installés", list(EQUIPEMENTS),
                                                             default=[x for x in e.equipements_installes if x in EQUIPEMENTS],
                                                             key=f"eq_{k}", format_func=EQUIPEMENTS.get)
                    e.etiquette_apres = R.classe_dpe(e.cep_apres, e.ges_apres)

                    st.caption("Travaux détectés — modifiables, lignes ajoutables (➕) ou supprimables.")
                    df_in = pd.DataFrame(
                        [{COL_POSTE: t.poste, COL_NATURE: t.nature_courte,
                          COL_CARAC: t.caracteristiques, COL_QTE: t.quantite} for t in e.travaux],
                        columns=[COL_POSTE, COL_NATURE, COL_CARAC, COL_QTE], dtype=object)
                    edited = st.data_editor(df_in, num_rows="dynamic", width="stretch", hide_index=True, key=f"travaux_{k}")
                    e.travaux = [
                        Travail(poste=_s(r[COL_POSTE]), nature_courte=_s(r[COL_NATURE]),
                                caracteristiques=_s(r[COL_CARAC]), quantite=_s(r[COL_QTE]))
                        for r in edited.to_dict("records") if _s(r[COL_POSTE]) or _s(r[COL_NATURE])
                    ]

            with st.container(border=True):
                st.markdown("**Exporter ce scénario**")
                colA, colB = st.columns(2)
                prefill = colB.checkbox(
                    "Pré-remplir les « travaux réalisés »", value=False, key=f"prefill_{fkey}_{sc.id}",
                    help="Désactivé par défaut : l'audit ne dit rien des travaux réellement réalisés.")
                colA.download_button("📄 PDF bailleur", data=generate_pdf(batiment, scenarios, scenario_choisi_id=sc.id),
                                     file_name=f"Fiche_travaux_{sc.id}.pdf", mime="application/pdf",
                                     key=f"dlpdf_{sc.id}", width="stretch")
                colB.download_button("📥 Excel « Liste des travaux »",
                                     data=generer_excel(batiment, sc, prefill_realises=prefill),
                                     file_name=f"Liste_travaux_{sc.id}.xlsx",
                                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                     key=f"dl_{sc.id}", width="stretch", type="primary")

# ---------------------------------------------------------------------------------------------
# Évaluation (après toutes les corrections)
# ---------------------------------------------------------------------------------------------
ev = evaluer(an.document, an.couverture, batiment, scenarios, hyp)
meilleur = ev.meilleur

with zone_verdict:
    if meilleur:
        v, titre = meilleur.verdict, f"{LIBELLE_VERDICT[meilleur.verdict]} — {meilleur.nom}"
        sous = (f"Coefficient ×{meilleur.coef} · {meilleur.coef_raison.rsplit(' : ×', 1)[0]} · "
                f"gain {meilleur.gain:.1%}".replace(".", ","))
        mwh = meilleur.volume_kwhc / 1000
        vol = f"<b>{_n(mwh)} MWhc</b><small>{_n(meilleur.surface)} m² × {R.FORFAIT_KWHC_PAR_M2} × {meilleur.coef}</small>"
        if prix:
            vol += f"<small><br>≈ {_n(mwh * prix)} € à {prix:g} €/MWhc</small>"
    else:
        pire = ev.scenarios[0].verdict if ev.scenarios else "non_estimable"
        v = pire
        titre = LIBELLE_VERDICT[pire] if ev.scenarios else "Non estimable — aucun scénario lisible"
        bloq = sorted((r for s in ev.scenarios[:1] for r in ev.generaux + s.resultats if r.niveau in (BLOQUANT, MANQUANT)),
                      key=lambda r: ORDRE[r.niveau])  # cause bloquante avant donnée manquante
        sous = bloq[0].message if bloq else "Aucun scénario de travaux trouvé dans le document."
        vol = "<b>0 MWhc</b>"
    st.html(f'<div class="verdict {v}"><div class="v-main"><div class="v-label">{escape(titre)}</div>'
            f'<div class="v-sub">{escape(sous)}</div></div><div class="v-vol">{vol}</div></div>')

    k1, k2, k3, k4 = st.columns(4)
    with k1.container(border=True):
        st.caption("Document")
        ton = "ok" if an.document.est_audit_reglementaire else "warn" if an.document.code != "inconnu" else "bad"
        st.html(badge(an.document.libelle, ton))
    with k2.container(border=True):
        st.caption("Bâtiments couverts")
        st.html(badge("⛔ Plusieurs bâtiments", "bad") if an.couverture.multiple else
                badge(f"1 bâtiment{' (' + an.couverture.batiment + ')' if an.couverture.batiment else ''}", "ok"))
    with k3.container(border=True):
        st.caption("État initial · Cep / GES")
        st.html(f'<span class="dpe-flow">{pastille_etiquette(batiment.etiquette_initiale)} '
                f'<b style="font-size:1.25rem">{_n(batiment.cep_initial)}</b><small style="opacity:.6">kWhEP</small> '
                f'<b style="font-size:1.25rem">{_n(batiment.ges_initial)}</b><small style="opacity:.6">kgCO2</small></span>')
    with k4.container(border=True):
        st.caption("Surface retenue")
        s_ret = hyp.surface_saisie or batiment.shab or batiment.surface_m2
        nature = "saisie" if hyp.surface_saisie else "habitable" if batiment.shab else "de référence ⚠️"
        st.html(f'<b style="font-size:1.25rem">{_n(s_ret)} m²</b> <small style="opacity:.7">{nature}</small>')

# ---------------------------------------------------------------------------------------------
# Onglet Éligibilité
# ---------------------------------------------------------------------------------------------
with tab_elig:
    for s in ev.scenarios:
        with st.container(border=True):
            st.html(f'<div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap">'
                    f'<b style="font-size:1.05rem">{escape(s.nom)}</b>'
                    f'{badge(LIBELLE_VERDICT[s.verdict], {"eligible": "ok", "reserve": "warn", "non_eligible": "bad"}.get(s.verdict, ""))}</div>')
            par_id = {}
            for r in s.resultats:
                par_id.setdefault(r.id, r)
            ges = par_id.get("PE-04") or next((r for r in s.resultats if r.id == "DA-GES"), None)
            chaud = par_id.get("PE-06") if par_id.get("PE-06") and par_id["PE-06"].niveau == BLOQUANT else par_id.get("PE-05") or par_id.get("PE-06")
            fin = next(sc for sc in scenarios if sc.id == s.id).etapes[-1]
            st.html('<div class="crit-grid">'
                    + _crit(f"P1 · Cep projet < {R.SEUIL_CEP_PROJET:g}", par_id.get("PE-01") or par_id.get("DA-CEP"),
                            f"{_n(fin.cep_apres)} kWhEP/m².an")
                    + _crit(f"P2 · Gain ≥ {R.GAIN_CEP_MIN:.0%}", par_id.get("PE-02"),
                            f"{s.gain:.2%}".replace(".", ",") if s.gain is not None else None)
                    + _crit("P3 · GES non dégradé", ges, f"{_n(batiment.ges_initial)} → {_n(fin.ges_apres)} kgCO2/m².an")
                    + _crit("P4 · Chaudières fossiles", chaud) + "</div>")
            c1, c2 = st.columns([2, 1])
            c1.markdown(f"**Coefficient ×{s.coef}** — {s.coef_raison.rsplit(' : ×', 1)[0]}")
            c2.markdown(f"**{_n(s.volume_kwhc / 1000)} MWh cumac**" + (f" · ≈ {_n(s.volume_kwhc / 1000 * prix)} €" if prix else ""))
            autres = sorted((r for r in s.resultats if r.id not in ("PE-01", "PE-02", "PE-04", "PE-05") and r.niveau != OK),
                            key=lambda r: ORDRE[r.niveau])
            if autres:
                st.html("".join(_ligne_resultat(r) for r in autres))

    st.subheader("Document, auditeur et bâtiment")
    st.html("".join(_ligne_resultat(r) for r in sorted(ev.generaux, key=lambda r: ORDRE[r.niveau])))

    with st.expander("🔎 Fiabilité de la lecture et indices du type de document"):
        lignes = [("GES initial", _n(batiment.ges_initial), batiment.fiabilite.get("ges_initial", "absent")),
                  ("Énergies avant travaux", f"{R.LIBELLES_ENERGIE[batiment.energie_chauffage]} / "
                   f"{R.LIBELLES_ENERGIE[batiment.energie_ecs]}", batiment.fiabilite.get("energies_avant", "absent"))]
        for sc in scenarios:
            for e in sc.etapes:
                lignes.append((f"GES après — {sc.nom.split('«')[0].strip()} · {e.libelle}", _n(e.ges_apres),
                               e.fiabilite.get("ges_apres", "absent")))
        st.html("<table style='width:100%;font-size:.88rem'>" + "".join(
            f"<tr><td>{escape(a)}</td><td><b>{escape(b_)}</b></td><td><span class='fiab {c}'>{escape(FIAB.get(c, c))}</span></td></tr>"
            for a, b_, c in lignes) + "</table>")
        st.caption(f"Type de document : {an.document.libelle} (confiance {an.document.confiance}, "
                   f"méthode {an.document.methode or 'non identifiée'}). Indices :")
        for i in an.document.indices[:5] + an.couverture.indices[:3]:
            st.caption(f"• {i}")

    st.caption(f"Règles : docs/regles_BAR-TH-177.md · vérifications : docs/verification_regles.md · "
               f"seuils centralisés dans audit/referentiel.py · analyseur {PARSER_VERSION}")

# ---------------------------------------------------------------------------------------------
# Onglet Comparatif
# ---------------------------------------------------------------------------------------------
with tab_cmp:
    if scenarios:
        st.caption("Une colonne par scénario (valeurs corrigées).")
        st.dataframe(pd.DataFrame(tableau_comparatif(batiment, scenarios, ev)).astype(str), width="stretch")
