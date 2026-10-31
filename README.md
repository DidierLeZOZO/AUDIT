# Audit énergétique — rénovation globale (Streamlit)

Analyse d'un audit énergétique réglementaire (PDF), sans IA : extraction par regex, correction manuelle, export Excel et PDF bailleur.

## Lancer en local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Héberger (gratuit)
Streamlit Community Cloud : https://share.streamlit.io → « New app » → ce dépôt, branche à déployer, fichier `app.py`.
Attention : un dépôt public rend le code public ; les PDF déposés ne sont jamais stockés (traités en mémoire).

## Où modifier quoi
| Besoin | Fichier |
|---|---|
| Nouveau logiciel d'audit / regex cassée | `audit/parser.py` (penser à changer `PARSER_VERSION`) |
| Ajouter un outil | créer `outils/mon_outil.py` + une ligne dans `registre.py` (menu, accueil, recherche automatiques) |
| Apparence (couleurs, arrondis) | `.streamlit/config.toml` (thème clair/sombre) |
| Habillage commun (cartes, étapes, pastilles) | `ui/style.css`, `ui/composants.py` |
| Seuils et coefficients BAR-TH-177 | `audit/referentiel.py` (un seul endroit) |
| Règles d'éligibilité BAR-TH-177 | `audit/regles.py` (ids = `docs/regles_BAR-TH-177.md`) |
| Reconnaissance étude thermique / DPE / multi-bâtiments | `audit/document.py` |
| Lecture GES, énergies, équipements | `audit/enrichissement.py` |
| Interface de l'outil audit | `outils/audit_renovation.py` |
| Colonnes du comparatif | `audit/synthese.py` |
| Excel (cellules, lignes) | `audit/excel_export.py` |
| PDF bailleur | `audit/pdf_export.py` |
| Gabarit Excel | `audit/donnees/Liste_des_travaux_et_entreprises_Modèle.xlsx` |

## Gabarit Excel
Le gabarit fourni est un **substitut** (je n'avais pas votre original). Pour utiliser le vôtre, remplacez le fichier : il doit avoir
C4 bénéficiaire, F4 scénario, C5 adresse, F5 date, et les travaux à partir de la ligne 9 (colonnes B-D préconisés, E-G réalisés).
`python -m audit.gabarit` régénère le substitut.

## Tests
```bash
pytest
# avec un vrai PDF (non versionné) :
AUDIT_EXEMPLE_PDF=/chemin/audit.pdf pytest
```
