# Vérification des règles BAR-TH-177 et décisions retenues

> 31/10/2026. Complète `docs/regles_BAR-TH-177.md` (base fournie par une autre conversation).
> Les textes officiels (ecologie.gouv.fr, calculateur-cee.ademe.fr) étaient **inaccessibles** depuis
> l'environnement de développement : les recoupements ci-dessous viennent de sources publiques
> secondaires (sites de délégataires et d'information). Ils confirment les valeurs, ils ne remplacent
> pas la lecture de la fiche officielle.

## 1. Recoupé par plusieurs sources indépendantes

| Élément | Valeur codée (`audit/referentiel.py`) | Sources |
|---|---|---|
| Cep projet | < 331 kWhEP/m².an (strict) | go-kelvin.com, opera-energie.com, wilow.fr, s2ee.fr |
| Gain | ≥ 35 % sur le Cep | idem + praxis-energie.fr |
| GES | après ≤ avant | idem |
| Volume | 2 100 kWh cumac/m² × Shab après rénovation | ohm-energie.com ; offre ACT (6 300 / 4 200 kWhc/m² = ×3 / ×2) |
| Coup de pouce | ×3 sortie complète des fossiles (chauffage ET ECS), ×2 sinon | ohm-energie.com, sonergia.fr, hellio.com |
| Appoint gaz | ≤ 30 % des besoins annuels de chaleur | sonergia.fr (Coup de pouce) — pour la fiche elle-même : base de règles seule |
| Versions | vA80.2 à partir du 17/01/2026, engagements jusqu'au 31/12/2030 | opera-energie.com, banquedesterritoires.fr, hellio.com (80ᵉ arrêté) |
| Durée de vie | 30 ans | calculateur-cee.ademe.fr (extrait de recherche) |
| Seuils DPE (affichage) | Cep 70/110/180/250/330/420 ; GES 6/11/30/50/70/100 | connaissancedesenergies.org, selectra, DREAL Occitanie |

## 2. Corrigé grâce à la vérification

- **Surface** : la « surface de référence » des audits 3CL **n'est pas** la surface habitable
  (elle inclut notamment les vérandas chauffées — ANIL, Selectra). Le volume se calcule sur la
  **Shab après rénovation** : l'outil utilise la Shab si l'audit la donne, sinon la surface de
  référence **avec une alerte**, et permet de saisir la Shab.
- **Étiquette** : calculée en double seuil (Cep + GES), et seulement pour information — la fiche
  177 n'a aucun critère de classe DPE.

## 3. Décisions métier (utilisateur, 31/10/2026)

| Sujet | Décision | Codé dans |
|---|---|---|
| Réseau de chaleur déjà en place + Coup de pouce | **×2** | `regles.coefficient` |
| Audit couvrant plusieurs bâtiments | **Bloquant** : 1 audit par bâtiment | `document.detecter_batiments`, règle AU-17 |
| Étude thermique / DPE / audit non réglementaire | Reconnus ; **estimables sous réserve** seulement si toutes les données sont présentes, sinon « non estimable » | `document.classer_document`, règles AU-01/AU-02 |
| Périmètre | Lecteur d'audit qui **estime** (pas les règles de dépôt : factures, RGE, contrôles) | — |

## 4. Interprétations retenues (à faire valider si un dossier en dépend)

- **Nouveau raccordement à un réseau de chaleur** (fossile → réseau) : ×3, avec alerte « réseau
  efficace au sens de L.711-4 à confirmer ».
- **ECS déjà électrique** : n'empêche pas le ×3 (seuls les équipements fossiles doivent être remplacés).
  ECS fossile remplacée par un ballon électrique à effet Joule : pas renouvelable → ×2.
- **Chaudière gaz conservée** : non interdite par la fiche à la lettre → alerte (pas bloquant), exclut le ×3.
- **Rénovation par étapes** : seule l'étape finale (cumulée) est évaluée ; chaque étape intermédiaire
  est signalée « éligible seule » ou « non valorisable seule ».

## 5. Non vérifié — à confirmer sur les textes officiels

1. Le seuil de 30 % de couverture gaz **au niveau de la fiche** (confirmé pour le Coup de pouce).
2. Le format du numéro d'audit ADEME (non utilisé comme critère : seule sa présence est regardée).
3. La qualification exacte exigée (VII art. 2 décret 2020-26) — l'outil attend OPQIBI 1905 et alerte sinon.
4. La liste officielle des logiciels d'audit.
5. Validité 5 ans de l'audit (enchaînement de renvois, non relu).

## 6. Fiabilité de lecture (ce que l'outil fait pour ne pas se tromper)

- GES initial et GES après travaux : **deux méthodes de lecture** (ligne « Cep GES » des étiquettes,
  nombre suivi de l'unité kgCO2/m²/an) + recoupement par la réduction annoncée « (-18 kg CO₂) ».
  Résultat affiché : *2 lectures concordantes*, *1 seule lecture* ou *lectures divergentes*.
- Cep : valeur **sans déduction du photovoltaïque** retenue systématiquement.
- Gain : recalculé à partir des Cep, comparé **sans arrondi** (34,95 % affiché « 35 % » est refusé).
- Valeur non lue = champ **vide** dans l'interface (jamais 0), et verdict « non estimable ».

## 7. Tests

`tests/test_regles.py` (cas d'essai §14 de la base + cas limites), `tests/test_document.py`
(types de document, multi-bâtiments, audit réel Parc de Turin si `AUDIT_EXEMPLE_PDF` est défini).
**Limite** : la reconnaissance des études thermiques et des DPE n'a été testée que sur des textes
synthétiques ; il faut des exemples réels pour la fiabiliser.
