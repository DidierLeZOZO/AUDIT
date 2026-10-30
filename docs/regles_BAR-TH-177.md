# Base de règles — fiche CEE BAR-TH-177 (rénovation globale d'un bâtiment résidentiel collectif)

> Version du document : 30/10/2026. Rédigé à partir des textes officiels relus le 30/10/2026 (liens en fin de document).
> Légende de confiance : **[CERTAIN]** = texte officiel lu ce jour · **[PROBABLE]** = texte officiel lu indirectement ou mémoire solide · **[INCERTAIN]** = à vérifier · **[PRATIQUE]** = usage EDF/Odicée/Promotelec, pas une règle · **[INTERPRÉTATION]** = lecture personnelle du texte.

---

## ⚠️ À LIRE AVANT TOUT : corrections sur les hypothèses de l'outil

Ces points remettent en cause des choix déjà codés. À traiter avant d'ajouter des règles.

1. **Le code exact est BAR-TH-177**, pas « TH-177 ». Intitulé : « Rénovation globale d'un bâtiment résidentiel collectif (France métropolitaine) ». **Secteur : résidentiel collectif uniquement** (≥ 3 foyers fiscaux distincts rattachés à des logements distincts). Une maison individuelle relève de **BAR-TH-174**, un appartement seul de **BAR-TH-175**. Si l'outil reçoit un audit de maison individuelle, il doit refuser la fiche 177. [CERTAIN]

2. **La fiche BAR-TH-177 n'utilise PAS les classes DPE comme critère d'éligibilité.** Aucun gain de classe, aucune étiquette finale minimale. Les 4 critères sont : Cep projet < 331 kWhEP/m².an, gain ≥ 35 % sur le Cep, GES après ≤ GES avant, restrictions sur les chaudières fossiles installées. Le calcul « nombre de classes gagnées » de l'outil est donc **hors sujet pour l'éligibilité 177** (utile seulement pour info / reporting). [CERTAIN]

3. **Déduire l'étiquette du seul CEP est faux en général.** L'étiquette DPE est le **double seuil** Cep + GES (la plus mauvaise des deux lettres). Sans effet sur l'éligibilité 177 (point 2), mais l'affichage de l'outil sera faux pour tout bâtiment dont la lettre GES est plus mauvaise. [PROBABLE — arrêté du 31/03/2021, non relu ce jour]

4. **La note GES est OBLIGATOIRE et BLOQUANTE.** « GES après ≤ GES avant » est un critère d'éligibilité de la fiche. L'outil ne l'extrait pas : il doit l'extraire (kgCO2eq/m².an, avant et pour chaque scénario). [CERTAIN]

5. **« Rénovation par étapes » : la fiche 177 ne connaît pas les étapes.** L'opération = les travaux réellement réalisés, qui doivent correspondre à un scénario de l'audit satisfaisant les 4 critères. Une étape intermédiaire qui n'atteint pas 35 % n'est pas valorisable seule. Les règles « première étape = +2 classes » de l'arrêté du 4 mai 2022 concernent le **contenu de l'audit**, pas l'éligibilité CEE. [CERTAIN pour la fiche ; INTERPRÉTATION pour la conséquence]

6. **La fiche 177 n'impose AUCUNE performance minimale par poste** (pas de R minimal, pas d'Uw, pas de SCOP). Seule exigence par poste : l'entreprise est **RGE** pour la catégorie de travaux. Les seuils R/Uw/Sw que l'outil extrait servent au contrôle de cohérence avec l'audit (contrôle après travaux : quantités et performances conformes au scénario), pas à un seuil réglementaire propre. [CERTAIN]

7. **Le volume ne dépend ni de la zone climatique, ni des classes, ni de l'énergie** : forfait **2 100 kWh cumac/m² × Shab après rénovation**, multiplié par 3 ou 2 si Coup de pouce. [CERTAIN]

8. **Un audit « non réglementaire » est non conforme au texte**, pas seulement « à confirmer ». La fiche exige un audit conforme à l'art. 8 de l'arrêté du 17/11/2020, qui renvoie au contenu de l'audit réglementaire (arrêté du 4 mai 2022) et impose sa transmission à la plateforme ADEME (d'où le n° ADEME). [CERTAIN pour les renvois ; INTERPRÉTATION pour « sans n° ADEME = non conforme »]

9. **Coefficient électricité : 2,3 → 1,9 (01/01/2026) → 1,7 (01/01/2027).** Le Cep d'un même bâtiment chauffé à l'électricité change selon la date de l'audit. Le gain et le seuil 331 doivent être appréciés sur des Cep **issus du même calcul**. L'outil doit lire la date d'établissement et ne jamais mélanger Cep initial d'un audit et Cep projet d'un autre. [CERTAIN pour les dates]

### Points où ma propre base de travail (instructions du projet) contredit le texte — je le dis une fois

- **Réseau de chaleur déjà en place → « pas de Coup de pouce, ×1 »** : le texte (art. 3-5-3 IV) ne dit pas ça. Le CdP donne **×3** si remplacement de **tous** les équipements fossiles par un système renouvelable, **×2 « dans le cas d'autres travaux »**. Un bâtiment déjà sur réseau qui fait une rénovation globale éligible est un « autre travaux » → **×2** si le demandeur est signataire de la charte et que les conditions de la charte sont respectées. La condition « retirer le poste RCU de l'audit » n'est pas dans le texte : c'est une exigence de pratique, à confirmer avec le pilote EDF. [CERTAIN sur le texte ; INTERPRÉTATION sur l'application]
- **« Conserver du gaz > 30 % = inéligible »** : la fiche interdit l'**installation** d'un système incluant au moins une chaudière gaz couvrant > 30 % des besoins. Elle ne vise pas textuellement la **conservation** d'une chaudière existante (contrairement à MaPrimeRénov' qui vise aussi la conservation). Garder la chaudière gaz existante n'est donc pas interdit par la fiche si gain ≥ 35 % et GES en baisse — mais exclut le ×3. Remplacer une chaudière gaz par une chaudière gaz = installation à 100 % → inéligible. [INTERPRÉTATION — à faire valider]
- **Taux de couverture gaz** : défini comme **chaleur fournie** par les chaudières gaz / **besoins annuels de chaleur** des usages couverts. Ce n'est pas un ratio de Cep. Un calcul sur les Cep est une approximation. [CERTAIN]

---

## 0. Identification de la fiche

| Élément | Valeur | Confiance / source |
|---|---|---|
| Code | BAR-TH-177 | CERTAIN — fiche officielle |
| Intitulé | Rénovation globale d'un bâtiment résidentiel collectif (France métropolitaine) | CERTAIN |
| Dénomination | Rénovation thermique globale d'un bâtiment résidentiel collectif existant. « L'approche globale consiste à déterminer et à mettre en œuvre un bouquet de travaux optimal sur le plan technico-économique. » | CERTAIN |
| Secteur | Bâtiments résidentiels collectifs existants en France métropolitaine | CERTAIN |
| Bénéficiaires visés | Propriétaires de bâtiments résidentiels collectifs : bailleurs sociaux, syndicats de copropriétaires, autres propriétaires (monopropriété) | CERTAIN (page ministère CdP) |
| Durée de vie conventionnelle | 30 ans | CERTAIN |
| Contrôle | **100 % des opérations, sur le lieu de l'opération**, par organisme d'inspection accrédité, à compter des engagements du 01/11/2024 | CERTAIN — arrêté du 28/09/2021, annexe II |

### Historique des textes

| Date | Texte | Effet | Confiance |
|---|---|---|---|
| 06/09/2024 (JO 17/09/2024) | Arrêté « 63e » (NOR ECOR2416035A) | Supprime **BAR-TH-145**, crée **BAR-TH-177**, crée l'art. 3-5-3 (Coup de pouce), la charte IV-6 et le référentiel de contrôle E ter | CERTAIN |
| 18/11/2024 (JO 20/11/2024) | Arrêté modificatif | Remplace la fiche (ajout d'une date de fin), corrige le référentiel E ter (ajout du contrôle à l'achèvement), règles de remplissage du tableau récapitulatif pour 174/175/177 | CERTAIN |
| 07/01/2026 (JO 16/01/2026, NOR ECOR2600569A) | Arrêté « 80e » | Nouvelle version **vA80.2**, prolonge le Coup de pouce (charte IV-8), réseau de chaleur « efficace au sens de L.711-4 » au lieu de « majoritairement EnR&R », ajoute l'attestation ADEME de modification des classes | CERTAIN |

### Versions et périodes (clé = **date d'engagement**)

| Version | Engagements | Fin de la fiche | Particularité |
|---|---|---|---|
| BAR-TH-145 | jusqu'au 31/10/2024 (dérogation 28/02/2025 pour copro avec AG avant 01/01/2025 ou PC/DP déposé avant 01/11/2024) | — | Ancienne fiche, formule (Cefi − Cefp) × Shab × B. Hors périmètre de l'outil. |
| **vA63.1** | du 01/11/2024 (ou 01/03/2025 en cas de dérogation) au **16/01/2026** | Texte : engagements jusqu'au 31/10/2029 (remplacée de fait par vA80.2) | — |
| **vA80.2** | **à partir du 17/01/2026** | **engagements jusqu'au 31/12/2030** | Attestation ADEME de modification des classes (arrêté du 13/08/2025) |

**Différences vA63.1 → vA80.2 sur le fond [CERTAIN, comparaison des deux textes]** : (1) date de fin 31/10/2029 → 31/12/2030 ; (2) ajout de la possibilité de compléter l'audit par l'attestation de l'art. 4 de l'arrêté du 13/08/2025 (les classes de l'attestation se substituent à celles de l'audit). **Seuils, pièces, formule : identiques.**

**Changement annoncé à surveiller [CERTAIN sur le fait, INCERTAIN sur la conséquence]** : l'arrêté du 19/08/2026 (JO 26/08/2026) passe le coefficient électricité à 1,7 au **01/01/2027** et **abroge à cette date l'arrêté du 13/08/2025**, celui auquel la vA80.2 renvoie pour l'attestation. Une vA80.2 lue au pied de la lettre renverra donc à un texte abrogé à partir du 01/01/2027. Je ne sais pas si une nouvelle version de la fiche est prévue. À surveiller.

---

## 1. Conditions d'éligibilité du bâtiment et du bénéficiaire

### 1.1 Texte de la fiche [CERTAIN]
- Bâtiment **résidentiel collectif existant**, France métropolitaine.
- « Les bâtiments d'habitation collectifs éligibles à la présente fiche sont ceux disposant d'**au moins trois foyers fiscaux distincts rattachés à des logements distincts**. »
- Partie A de l'attestation : case « Bâtiment résidentiel collectif **existant depuis plus de 2 ans** à la date d'engagement de l'opération : □ Oui □ Non ». → ancienneté minimale 2 ans (case cochée Non = inéligible).
- Copropriété (loi du 10/07/1965) : accord de la copropriété autorisant les travaux ; n° d'immatriculation demandé en partie A.

### 1.2 Ce que la fiche n'exige PAS [CERTAIN]
Pas de zone climatique, pas de surface min/max, pas de nombre de logements maximal, pas d'énergie de chauffage imposée avant travaux, pas de classe DPE initiale minimale, pas de condition de revenus des occupants.

### 1.3 Conditions supplémentaires SI Coup de pouce (art. 3-5-3 III, arrêté du 29/12/2014) [CERTAIN]
- Bâtiment résidentiel collectif au sens du CdP : « au moins **75 % des lots principaux** ou à défaut 75 % des tantièmes sont dédiés à l'**habitation principale** de leurs occupants » ; seuil ramené à **65 %** pour les copropriétés de **20 lots d'habitation ou moins**.
- Copropriété : syndicat **immatriculé** au registre des copropriétés (art. L.711-1 CCH).
- Date d'engagement **postérieure** à la date de prise d'effet de la charte signée par le demandeur.

### 1.4 Bâtiment mixte (tertiaire + logements)
Fiche : JE NE SAIS PAS si une part de tertiaire est tolérée hors CdP (le texte dit seulement « bâtiment résidentiel collectif »). CdP : critère des 75 % de lots/tantièmes en résidence principale ci-dessus. Shab = surface **habitable** (résidentielle) uniquement.

### 1.5 Bâtiment déjà rénové
Pas de règle spécifique. Il doit seulement atteindre les 4 critères sur la base de son état initial réel (constaté au contrôle avant travaux). [CERTAIN par absence]

---

## 2. Exigences sur l'audit énergétique

### 2.1 Obligation et référentiel [CERTAIN — fiche vA63.1 et vA80.2]
« Un audit énergétique est réalisé **préalablement aux travaux** de rénovation globale du bâtiment. Cet audit respecte les dispositions de l'**article 8 de l'arrêté du 17 novembre 2020** […]. Il est établi par une personne répondant aux conditions mentionnées au **VII de l'article 2 du décret du 14 janvier 2020** relatif à la prime de transition énergétique. »

### 2.2 Ce qu'implique l'art. 8 de l'arrêté du 17/11/2020 (version consolidée, lue ce jour) [CERTAIN]
I. L'audit (logement, partie de bâtiment ou bâtiment d'habitation) :
1. est réalisé conformément aux **articles 2, 3 et 4 de l'arrêté du 4 mai 2022** (contenu de l'audit réglementaire) ;
2. est réalisé conformément aux **quatre premiers alinéas et au dernier alinéa de l'art. 2 du décret 2022-780** (→ missions, au moins une visite, **interdiction de sous-traiter**, **validité 5 ans**, tenue à disposition) ;
3. sans DPE antérieur, le propriétaire n'a pas à remettre le récapitulatif DPE ;
4. l'auditeur respecte les conditions d'**indépendance et d'impartialité** de l'art. L.126-28-1 CCH ;
5. l'auditeur **transmet l'audit à la plateforme ADEME** (art. L.126-32 / R.126-30 CCH).

II. Bâtiment d'habitation **en copropriété (loi 1965)** : dérogations :
1. l'auditeur peut faire **une seule proposition** de travaux, qui n'est pas tenue d'atteindre la rénovation performante ;
2. le syndic fournit consommations des parties communes, carnet d'entretien, contrat d'exploitation, clés de répartition, factures de travaux, plans, DPE éventuel ;
3. au moins une visite (saison de chauffe si possible), accompagnée du syndic et du conseil syndical ; **échantillonnage des logements** selon les règles du DPE immeuble (annexe 1 de l'arrêté du 31/03/2021).

### 2.3 Contenu minimal (arrêté du 4 mai 2022, art. 2 à 4) [CERTAIN]
- État initial selon la **méthode conventionnelle du DPE (3CL)**, schéma de répartition des déperditions, info sur les dispositifs de pilotage.
- **Au moins deux propositions** de travaux (sauf copropriété, cf. 2.2 II.1) :
  - 1° **parcours par étapes** : 1re étape = gain d'au moins **deux classes** + traitement de **deux postes d'isolation** ; étape finale = rénovation performante ;
  - 2° **parcours en une seule étape** = rénovation performante.
  - Dérogation (art. 3) si contraintes techniques/architecturales/patrimoniales/coût : traitement des 6 postes et au minimum classe C (si E avant), D (si F), E (si G).
- Pour **chaque étape** : Cep et Cef par usage et totaux (kWhEP/m²/an, kWhEF/m²/an) **avec et sans déduction du PV autoconsommé** ; GES (kgCO2eq/m²/an) ; classes énergie et GES ; économies EP/EF et GES évités en absolu et en % ; impact sur la facture ; coût TTC ; aides ; descriptif des travaux avec performances et surfaces d'isolant.
- Ventilation : si renouvellement d'air insuffisant, travaux proposés **dès la 1re étape**.
- Livrables : **rapport de synthèse PDF** (dont **nom et version du logiciel**) transmis dans le mois suivant la visite + **récapitulatif XML** standardisé.
- Logiciels : validés selon l'**art. 3 de l'arrêté du 31/03/2021** (liste officielle publiée sur rt-re-batiment.developpement-durable.gouv.fr). Je **ne sais pas** lesquels de LICIEL, Climawin, Pleiades, DPEWIN, ANALYSIMMO figurent sur la liste « audit » à jour → à vérifier sur la liste officielle.

### 2.4 Exigences propres à la fiche 177 sur le rapport [CERTAIN]
Le rapport de synthèse (et sa mise à jour éventuelle) est **daté et signé** par le prestataire, et mentionne :
- Cep initial, Cep projet, Cef initial, Cef projet (kWh/m².an), **sans déduction de la production d'électricité autoconsommée ou exportée**, en précisant les usages ;
- rejet de CO2 avant et après (kgeqCO2/m².an) ;
- **Shab après rénovation** (m²) ;
- gain énergétique ;
- **nom et numéro de version du logiciel**.
Fichier source **.xml (ou équivalent)** obligatoire.

### 2.5 Qui peut réaliser l'audit
- Fiche : « personne répondant aux conditions du **VII de l'art. 2 du décret 2020-26** ». Je **n'ai pas relu** ce VII ce jour → contenu exact **À VÉRIFIER**.
- Décret 2022-780 art. 1 (audit réglementaire), pour un bâtiment **à plusieurs logements hors copropriété** : professionnels titulaires d'un signe de qualité du **I de l'art. 1 du décret 2018-416** (la qualification **OPQIBI 1905** « Audit énergétique des bâtiments (tertiaires et/ou habitations collectives) » en est un) ou architectes/sociétés d'architecture ayant suivi la formation. Les **diagnostiqueurs DPE** ne sont admis que pour un audit **à l'échelle d'un seul logement**. [CERTAIN pour le décret 2022-780 ; INTERPRÉTATION pour l'application à la 177 via le renvoi]
- **OPQIBI 1911** = maisons individuelles → inadaptée au collectif. [PROBABLE]
- Indépendance : l'auditeur ne peut sous-traiter tout ou partie de l'audit ; visite physique par une personne de l'entreprise d'audit (art. 3-5-3 IV pour le CdP + décret 2022-780). L'organisme de contrôle ne peut pas contrôler une opération dont il a réalisé l'audit (charte IV-8). [CERTAIN]
- [PRATIQUE] EDF exige nommément OPQIBI 1905.

### 2.6 Validité
**5 ans** (décret 2022-780 art. 2, rendu applicable par l'art. 8 I.2). [PROBABLE — enchaînement de renvois]
Ordre : audit **avant** les travaux ; contrôle de l'audit **avant** les travaux (référentiel E ter I).

### 2.7 Audit réglementaire / non réglementaire
| Document | Statut 177 | Confiance |
|---|---|---|
| Audit conforme arrêté 4 mai 2022, n° ADEME, XML | Conforme | CERTAIN |
| « Audit non réglementaire », « audit incitatif 3CL 2021 », sans n° ADEME | Non conforme à l'art. 8 (pas de transmission ADEME, contenu possiblement incomplet) | INTERPRÉTATION forte |
| DPE (même collectif), « [NON ÉMIS ADEME] » | Non conforme (ce n'est pas un audit) | CERTAIN |
| Étude thermique Th-C-E ex / RT existant | Non conforme (méthode ≠ 3CL-DPE) | INTERPRÉTATION forte |
| [PRATIQUE] | EDF a parfois toléré/examiné au cas par cas → décision pilote EDF | — |

### 2.8 Mise à jour
« Lorsque les travaux mis en œuvre diffèrent des travaux préconisés, l'audit énergétique est **mis à jour** sur la base des travaux effectivement réalisés. » La mise à jour est datée et signée. [CERTAIN]

---

## 3. Exigences de performance

### 3.1 Les 4 critères (fiche, identiques vA63.1 / vA80.2) [CERTAIN]
| # | Critère | Formule |
|---|---|---|
| P1 | Cep projet **< 331** kWhEP/m².an (strictement inférieur) | 5 usages : chauffage, refroidissement, ECS, éclairage, auxiliaires (chauffage, refroidissement, ECS, ventilation) ; rapporté à la surface de référence des logements |
| P2 | Gain **≥ 35 %** | (Cep initial − Cep projet) / Cep initial, mêmes usages |
| P3 | GES après **≤** GES avant | kgCO2eq/m².an rapportés à la surface de référence |
| P4 | Hors raccordement réseau de chaleur : pas d'**installation** de chaudière charbon ou fioul, ni d'un système incluant **au moins une chaudière gaz** dont le **taux de couverture > 30 %** | taux = chaleur fournie par l'ensemble des chaudières gaz / besoins annuels de chaleur des usages couverts par le système |

Plus : consommations **sans déduction** du PV autoconsommé ou exporté. Aucune exigence sur Cef (seulement à déclarer).

### 3.2 Classes DPE [CERTAIN pour la fiche]
Aucune exigence. Rappel pour l'affichage (arrêté du 31/03/2021, **non relu ce jour**, [PROBABLE]) — double seuil, classe = la plus mauvaise des deux :

| Classe | Cep (kWhEP/m².an) | GES (kgCO2eq/m².an) |
|---|---|---|
| A | ≤ 70 | ≤ 6 |
| B | ≤ 110 | ≤ 11 |
| C | ≤ 180 | ≤ 30 |
| D | ≤ 250 | ≤ 50 |
| E | ≤ 330 | ≤ 70 |
| F | ≤ 420 | ≤ 100 |
| G | > 420 | > 100 |

Ajustements « petites surfaces » (< 40 m²) : concernent les logements, je ne sais pas s'ils s'appliquent au DPE d'immeuble → ne pas coder.

### 3.3 Par étape
La fiche ne valorise qu'**une** opération = l'ensemble des travaux réalisés comparé à l'état initial. Si le maître d'ouvrage ne réalise que la 1re étape d'un parcours, il faut que **cette étape seule** satisfasse P1-P4. [INTERPRÉTATION]

### 3.4 Coefficient électricité et cohérence des Cep [CERTAIN pour les dates]
| Audit établi | Coef. EP électricité |
|---|---|
| jusqu'au 31/12/2025 | 2,3 |
| 01/01/2026 → 31/12/2026 | 1,9 |
| à partir du 01/01/2027 | 1,7 |
Les audits antérieurs restent valables ; une attestation ADEME peut actualiser les **classes**. Pour la 177 vA80.2, seules les **classes** de l'attestation se substituent à celles de l'audit ; **le texte ne dit pas que les Cep sont substitués**. → les critères P1/P2 se calculent sur les Cep de l'audit. [CERTAIN pour la lettre du texte ; conséquence = INTERPRÉTATION]

### 3.5 Énergies fossiles, réseaux, PAC
- Chaudière charbon/fioul **installée** → inéligible (hors réseau de chaleur). [CERTAIN]
- Chaudière gaz **installée** couvrant > 30 % des besoins du système → inéligible. Ex. remplacement chaudière gaz par chaudière gaz à condensation → inéligible. [CERTAIN]
- PAC hybride (appoint gaz) : éligible si couverture gaz ≤ 30 % (à démontrer : note de dimensionnement / calcul de l'audit). [CERTAIN pour le seuil]
- Raccordement à un réseau de chaleur : exclu de la restriction P4 (« hors raccordement »). [CERTAIN]
- Conservation d'une chaudière fossile existante : non visée par P4 → voir avertissement en tête. [INTERPRÉTATION]
- CdP : changement d'équipement de chauffage/ECS réalisé **au profit d'un raccordement à un réseau de chaleur efficace** (vA80.2 / charte IV-8 ; « majoritairement EnR&R » sous la charte IV-6), sauf justification du gestionnaire d'impossibilité technique ou économique (ou attestation « pas de réseau » du demandeur). En plus, pour le CdP : pas de **chauffe-eau** charbon/fioul. [CERTAIN]

---

## 4. Travaux : obligatoires, interdits, conditions techniques

### 4.1 Texte de la fiche [CERTAIN]
- Aucun poste obligatoire, aucun nombre minimal de postes, aucune performance minimale par poste.
- Bouquet « optimal technico-économique » déterminé par l'audit.
- « Pour chaque catégorie de travaux […] mentionnée aux 1° à 16° du I de l'art. 1er du décret 2014-812, le professionnel réalisant l'opération est titulaire d'un **signe de qualité (RGE)** » correspondant (17° « offre globale » ou la catégorie des travaux réalisés).
- La preuve de réalisation (facture) mentionne **la liste des travaux réalisés avec leurs niveaux de performance**.

### 4.2 Interdits [CERTAIN]
Uniquement P4 (chaudière charbon/fioul ; système avec chaudière gaz > 30 %), hors réseau de chaleur.

### 4.3 Contrôle à l'achèvement (référentiel E ter II) [CERTAIN]
Non satisfaisant si :
1. travaux réalisés ≠ scénario de l'audit éligible (CdP ou fiche) ;
2. écart **en quantité et en qualité** (performances thermiques et énergétiques) entre matériaux/équipements posés et le scénario retenu ou les factures ;
3. non-qualités manifestes ; l'inspecteur peut s'appuyer sur les référentiels geste par geste de l'annexe III **sauf** A.1 point 3 (R minimal des combles/planchers), B.1.1.1 (critères liés aux fiches murs), C.I.A (PAC), D.I.A (biomasse), F.I.A → les seuils propres aux fiches unitaires ne s'appliquent pas.

→ Pour l'outil : la règle utile est **« performance et quantité posées ≥ celles du scénario de l'audit »**, pas un seuil réglementaire.

### 4.4 Travaux induits
Fiche : rien. Ne pas inventer.

### 4.5 Non éligible même si dans l'audit
- Postes déjà valorisés par une autre fiche CEE d'engagement égal ou postérieur (non-cumul, §8).
- Équipements de chauffage **non fixes** pris en compte dans l'audit → contrôle non satisfaisant (E ter I.1 6). [CERTAIN]

---

## 5. Calcul du volume de CEE

### 5.1 Formule [CERTAIN]
```
Volume (kWh cumac) = 2 100 × Shab × C
```
- **Shab** = surface habitable du bâtiment **après rénovation** (m²). Surfaces nouvelles (combles/caves aménagés, extension) : DP de travaux à fournir.
- **C** = 1 hors Coup de pouce ; Coup de pouce (art. 3-5-3 IV) :
  - **C = 3** : « travaux incluant le remplacement de **tous** les équipements de chauffage **et** de production d'ECS au charbon, fioul ou gaz par un système de chauffage ou d'ECS **renouvelable** » ; appoint fossile toléré dans le respect de la fiche et de l'article (donc ≤ 30 % gaz) ;
  - **C = 2** : « dans le cas d'autres travaux ».
- Pas de zone climatique, pas de classe, pas d'énergie, pas de nombre de logements dans la formule.
- Pas de tableau de valeurs : un seul forfait (2 100 kWh cumac/m²).

### 5.2 Bonification / cumul [CERTAIN]
- Bonification CdP non cumulable avec celles des art. 3-6, 3-7, 3-7-1 et 4 à 6-1 de l'arrêté du 29/12/2014.
- Précarité / logements sociaux : l'art. 3-1 IV classe une fraction du volume « au bénéfice des ménages en précarité » pour les logements conventionnés / HLM. **Ce n'est pas un multiplicateur** ; je ne sais pas comment Odicée le traite → à vérifier.
- Prime minimale CdP affichée par le ministère (page MAJ 01/07/2026) : **41 €/m²** (remplacement de tous les équipements fossiles par un système renouvelable) et **27 €/m²** (autres), Shab après rénovation. Je ne retrouve pas ce tableau dans le texte de la charte IV-8 que j'ai relu → **À VÉRIFIER** si le plancher vaut pour les engagements ≥ 17/01/2026.

### 5.3 Exemples
Prix indicatif 7 €/MWh cumac = hypothèse commerciale, pas une règle.

**Exemple 1 — ×3**
Bâtiment 48 logements, Shab après travaux 3 020 m². Chauffage + ECS gaz collectifs remplacés par PAC collective air/eau sans appoint fossile. Cep 245 → 128 ; GES 52 → 9.
- P1 : 128 < 331 ✓ ; P2 : (245−128)/245 = 47,76 % ✓ ; P3 : 9 ≤ 52 ✓ ; P4 : aucune chaudière installée ✓.
- C = 3 (tous les équipements fossiles chauffage ET ECS remplacés par du renouvelable).
- 2 100 × 3 020 = 6 342 000 kWh cumac = 6 342 MWhc ; × 3 = **19 026 MWhc** (≈ 133 182 € à 7 €).

**Exemple 2 — réseau de chaleur existant, ×2**
Bâtiment déjà raccordé à un réseau de chaleur, Shab 4 500 m². ITE + menuiseries + VMC. Cep 210 → 125 (40,48 %), GES 38 → 24.
- P1-P4 ✓ (pas de chaudière installée).
- Aucun équipement fossile remplacé → pas ×3 ; « autres travaux » → C = 2 si demandeur signataire de la charte.
- 2 100 × 4 500 = 9 450 MWhc ; × 2 = **18 900 MWhc**. Sans CdP : 9 450 MWhc.

**Exemple 3 — hors Coup de pouce, ×1**
Shab 1 250 m², demandeur non signataire de la charte (ou CdP non retenu). Cep 300 → 190 (36,67 %), GES 60 → 35.
- 2 100 × 1 250 = **2 625 MWhc**.

**Exemple 4 — inéligible gain**
Cep 260 → 172 : (260−172)/260 = 33,85 % < 35 % → **0 kWh cumac**.

**Exemple 5 — inéligible gaz**
Remplacement chaudière gaz collective par chaudière gaz à condensation + isolation. Gain 41 %, GES en baisse. Système installé avec chaudière gaz couvrant 100 % > 30 % → **inéligible**, 0 kWh cumac.

**Exemple 6 — PAC hybride ×2 ou ×3 ?**
Chaudière gaz remplacée par PAC + appoint gaz couvrant 22 %, ECS gaz conservée. P4 ✓ (22 % ≤ 30 %). ECS gaz non remplacée → « tous les équipements… ECS » non remplacés → **C = 2**, pas 3. Si l'ECS est aussi basculée sur la PAC/renouvelable avec appoint gaz ≤ 30 % → C = 3. [INTERPRÉTATION sur l'appoint]

---

## 6. Pièces du dossier et mentions obligatoires

### 6.1 Documents justificatifs spécifiques (fiche) [CERTAIN]
1. **Rapport de synthèse de l'audit** (+ mise à jour éventuelle), daté et signé : Cep/Cef avant-après (sans déduction PV), gain, GES avant-après, Shab après, nom + version du logiciel ; complété le cas échéant (vA80.2) par l'attestation ADEME de modification des classes.
2. **Fichier source de l'audit .xml** (ou équivalent).
3. **Liste des travaux préconisés** (niveaux de performance) **et correspondance avec les travaux réalisés**, **datée et signée** par : le bénéficiaire, l'auditeur, **chaque** professionnel réalisant ou assurant la maîtrise d'œuvre.
4. **Liste des entreprises** ayant réalisé les travaux : nature des travaux + référence de qualification/certification.
5. **Attestations fiscales d'au moins 3 foyers fiscaux distincts** rattachés à des logements distincts.
6. **DP de travaux** pour toute surface habitable supplémentaire (aménagement de cave/combles, extension).
7. Copropriété : **accord de la copropriété** autorisant les travaux.

### 6.2 Pièces générales de toute opération CEE [PROBABLE — arrêté du 4/09/2014, non relu ce jour]
Attestation sur l'honneur (partie A spécifique + parties communes signées bénéficiaire et professionnel), preuve de l'engagement (devis accepté / OS / marché), preuve de réalisation (facture), preuve du rôle actif et incitatif (cadre contribution / offre), tableau récapitulatif du dépôt.

### 6.3 Pièces Coup de pouce [CERTAIN — art. 3-5-3 et charte]
- Offre du signataire acceptée **avant** la signature du (premier) devis.
- Réponse écrite du bénéficiaire acceptant/refusant l'**AMO** et les solutions de financement (copro : délibération d'AG).
- En cas de changement de chauffage/ECS non raccordé au réseau : **justification de l'impossibilité de raccordement** (cas 1 attestation du demandeur « pas de réseau sur la commune ni limitrophes » ; cas 2a attestation du gestionnaire « raccordement impossible » ; cas 2b attestation du gestionnaire « réseau non majoritairement EnR&R » — modèles page ministère).
- Rapports de contrôle (avant / achèvement) + synthèse des contrôles.

### 6.4 Partie A de l'attestation sur l'honneur — vA80.2 (champs * obligatoires) [CERTAIN]
Date d'engagement* · date de preuve de réalisation · référence facture · nom du site / copropriété* · adresse*, complément, CP*, ville* · bâtiment existant > 2 ans* (O/N) · Shab après rénovation* · nb logements distincts* · nb foyers fiscaux distincts* · copropriété loi 1965* (O/N) · n° d'immatriculation copro* · audit préalable conforme art. 8* (O/N) · Cep initial*, Cep projet*, Cef initial*, Cef projet* · gain %* · « hors raccordement, changements conduisant à chaudière charbon/fioul ou système gaz > 30 % »* (O/N — **doit être Non**) · type d'équipements chauffage/ECS avant* et après* · GES après ≤ avant* (O/N — **doit être Oui**) · BE audit : raison sociale*, SIREN*, date de l'audit*, référence de l'audit* · logiciel : nom + éditeur*, date et n° de version* · par professionnel : nom*, prénom* du représentant, raison sociale*, SIRET*, domaine des travaux*, référence de qualification* + date.

### 6.5 Tableau récapitulatif du dépôt PNCEE (arrêté du 4/09/2014 annexe 6, modifié le 18/11/2024) [CERTAIN]
- Date de facture / d'achèvement = **date de la dernière facture** ou dernière date d'achèvement.
- SIREN/raison sociale du professionnel = celui qui a **mis en œuvre ou assuré la maîtrise d'œuvre** ; à défaut, celui qui a réalisé les **travaux les plus coûteux**, signataire de l'attestation.
- Commentaires = **liste des références des fiches** correspondant aux différents postes de travaux.

### 6.6 Cohérences à vérifier [INTERPRÉTATION, issue du contrôle]
Adresse travaux identique sur audit / attestation / factures / contrôle ; Shab audit vs déclarée (écart > 10 % = non satisfaisant au contrôle) ; SIREN BE = SIREN de l'attestation ; référence audit = n° ADEME ; dates (§7) ; travaux facturés = scénario de l'audit en quantité et performance ; RGE valide à la date d'engagement.

### 6.7 Conservation
JE NE SAIS PAS la durée exacte applicable (à vérifier dans le code de l'énergie / arrêté du 4/09/2014).

---

## 7. Dates et délais

| Événement | Règle | Confiance |
|---|---|---|
| Date d'engagement | Date d'acceptation du devis (exemple donné par la partie A) ; [PRATIQUE] marché public : notification / OS | CERTAIN (exemple) / PRATIQUE |
| Version de fiche | Déterminée par la date d'engagement (≤ 16/01/2026 → vA63.1 ; ≥ 17/01/2026 → vA80.2) | CERTAIN |
| Fin de la fiche | Engagements jusqu'au 31/12/2030 (vA80.2) | CERTAIN |
| Audit | Avant les travaux ; validité 5 ans | CERTAIN / PROBABLE |
| Rapport d'audit | Transmis dans le mois suivant la visite | CERTAIN (arrêté 4 mai 2022 art. 4) |
| Contrôle de l'audit | « En fin de phase d'audit et **avant la réalisation des travaux** » | CERTAIN |
| Contrôle à l'achèvement | Uniquement après avis **satisfaisant** sur l'audit | CERTAIN (art. 7 I bis arrêté 28/09/2021) |
| CdP : engagement | Postérieur à la prise d'effet de la charte du demandeur ; offre CdP avant le 1er devis | CERTAIN |
| CdP charte IV-6 | Engagements jusqu'au 31/12/2025, achèvement ≤ 31/12/2027 | CERTAIN |
| CdP charte IV-8 | Engagements ≥ 17/01/2026 ; plus de date limite d'achèvement | CERTAIN |
| Trou 01/01/2026 → 16/01/2026 | L'ancien art. 3-5-3 I limitait les engagements au 31/12/2025, le nouveau s'applique aux engagements ≥ 17/01/2026 → **a priori pas de bonification** pour les engagements de cette fenêtre | INTERPRÉTATION — à confirmer |
| Dépôt | Délai maximal entre achèvement et dépôt : je crois 12 mois (règle générale CEE) | INCERTAIN — À VÉRIFIER |
| Date d'achèvement déclarée | Dernière facture | CERTAIN |

Ordre obligatoire : **audit (visite → rapport) → contrôle de l'audit + visite avant travaux → (offre CdP) → engagement → travaux → mise à jour de l'audit si écart → factures → contrôle à l'achèvement → dépôt**.
Pièges : engagement antérieur à la date de l'audit ; travaux démarrés avant le contrôle avant travaux (contrôle impossible → bloquant en pratique) ; RGE expiré à la date d'engagement.

---

## 8. Rôle actif et incitatif, cumul, contrôles

### 8.1 Rôle actif et incitatif
Règle générale CEE (art. R.221-22 code de l'énergie) : contribution du demandeur antérieure au déclenchement de l'opération. Pour le CdP : offre conforme à la charte, acceptée avant la signature du devis ; AMO et solutions de financement proposées ; dans la charte IV-8, obligation de promouvoir le raccordement réseau et la chaleur renouvelable. [CERTAIN pour le CdP ; PROBABLE pour la règle générale]

### 8.2 Cumul [CERTAIN]
- **Non cumulable** avec d'autres fiches dont la date d'engagement est **égale ou postérieure**, pour : chauffage ou régulation, ECS, ventilation, isolation de l'enveloppe, isolation du réseau hydraulique chauffage/ECS, GTB/automatisation — **dès lors que ces travaux sont valorisés au titre de la 177**.
- CdP non cumulable avec les autres incitations CEE, notamment les aides Anah valorisant les CEE des travaux subventionnés.
- Cumulable (page ministère) avec MaPrimeRénov', éco-PTZ. Une seule prime CEE par opération.

### 8.3 Contrôles [CERTAIN]
- **100 % sur le lieu de l'opération** (annexe II arrêté du 28/09/2021, engagements ≥ 01/11/2024), organisme d'inspection accrédité ISO/CEI 17020 type A, choisi par le demandeur, indépendant (ne peut avoir réalisé l'audit).
- **Contrôle 1 — avant travaux (E ter I)** :
  - I.1 contenu de l'audit — non satisfaisant si : (1) logiciel non conforme (nom + version toujours cités au rapport) ; (2) Cep/Cef avant-après absents ; (3) écart de **Shab > 10 %** : (déclarée − mesurée)/mesurée × 100 ; (4) confort thermique après < avant (notamment dimensionnement du générateur) ; (5) **PV déduit** des consommations ; (6) chauffage **non fixe** pris en compte.
  - I.2 (CdP) / I.3 (hors CdP) : au moins un scénario respecte Cep < 331, gain fiche, GES en baisse (+ pour CdP : pas de charbon/fioul, pas de gaz > 30 %, pas de hausse GES) ; sinon non satisfaisant.
  - I.4 visite : écart manifeste avec l'état initial de l'audit sur (14) isolation des parois et surfaces ; (15) menuiseries et surfaces ; (16) nature des combles ; (17) chauffage/ECS de la génération à l'émission ; (18) ventilation ; (19) refroidissement.
- **Contrôle 2 — à l'achèvement (E ter II)** : cf. §4.3.
- Résultats : satisfaisant / non satisfaisant / non vérifiable ; mesures correctives avant dépôt ; un second rapport peut être établi après correction de l'audit.
- Seuil de non-satisfaction par lot (art. 6 IV) : 14 % (dépôts 2026), 12 % (2027), 10 % (≥ 2028).

---

## 9. Cas particuliers et ambiguïtés

| Cas | Ce que dit le texte | Statut |
|---|---|---|
| Copropriété | Accord de copro ; n° d'immatriculation ; audit à une seule proposition possible ; CdP : AG vote travaux + AMO | CERTAIN |
| Bailleur social syndic sans tous les lots | Rien de spécifique ; [PRATIQUE] attestation des copropriétaires autorisant le syndic à instruire et percevoir | PRATIQUE |
| Plusieurs bâtiments | Une opération par **bâtiment** (attestation par adresse) ; un audit par bâtiment | INTERPRÉTATION forte |
| Échantillonnage | Échantillonnage des **logements** d'un bâtiment admis (règles DPE immeuble) ; un audit d'un bâtiment ne couvre pas un autre bâtiment | CERTAIN / INTERPRÉTATION |
| Extension / surfaces nouvelles | Shab après rénovation ; DP obligatoire pour les surfaces ajoutées | CERTAIN |
| Logements vacants | Le critère porte sur ≥ 3 foyers fiscaux ; JE NE SAIS PAS comment l'instructeur traite un bâtiment majoritairement vacant | INCERTAIN |
| Travaux ≠ audit | Mise à jour de l'audit obligatoire ; le contrôle à l'achèvement compare au scénario retenu | CERTAIN |
| Travaux démarrés avant contrôle | Contrôle avant travaux impossible → l'opération ne peut pas avoir de contrôle E ter I conforme | INTERPRÉTATION forte |
| Plusieurs scénarios dans l'audit | Il suffit qu'un scénario soit éligible au contrôle I ; les travaux doivent correspondre à un scénario éligible | CERTAIN |
| Réseau existant + CdP | ×2 selon le texte ; condition « retirer le poste RCU » = pratique à confirmer | voir en tête |
| Conservation gaz | Non visée par P4 | INTERPRÉTATION |
| Gain dans la charte | Note 2 de la charte IV-8 calcule le taux sur chauffage, refroidissement et ECS seulement, alors que la fiche dit 5 usages | Incohérence textuelle — la fiche prévaut pour l'éligibilité ; signaler |
| Attestation ADEME (vA80.2) | Substitue les **classes**, pas les Cep | CERTAIN (lettre) |
| Arrêté du 13/08/2025 abrogé au 01/01/2027 | Renvoi de la vA80.2 devient caduc | INCERTAIN — suivre |
| Mixte tertiaire | Fiche muette ; CdP : 75 %/65 % des lots en résidence principale | INCERTAIN pour la fiche |
| Note de calcul Th-C-E ex au lieu d'un audit 3CL | Méthode non conforme à l'arrêté du 4 mai 2022 | INTERPRÉTATION forte |

Positions PNCEE publiées sur ces cas : JE NE SAIS PAS (pas de FAQ PNCEE consultée).

---

## 10. Motifs de refus et erreurs fréquentes (classés par gravité)

Classement fondé sur les dossiers rencontrés et le référentiel de contrôle, pas sur des statistiques officielles.

1. **Document ≠ audit réglementaire** (DPE, étude thermique, « audit non réglementaire », pas de n° ADEME, pas de XML) → bloquant.
2. **Auditeur non qualifié** (certification diagnostiqueur, OPQIBI 1911 au lieu de 1905, numéro de certificat au lieu de qualification).
3. **Travaux démarrés avant le contrôle avant travaux** / OS dont la date de fin est déjà passée.
4. **Gaz > 30 %** : chaudière gaz remplacée par chaudière gaz ; hybridation où l'ECS reste 100 % gaz.
5. **Gain < 35 %** une fois recalculé (gain affiché arrondi ou calculé sur Cef, sur une étape, ou PV déduit).
6. **Cep avec déduction du PV**.
7. **Écart de Shab > 10 %** ; Shab avant au lieu d'après ; surfaces non habitables incluses.
8. **Audit non signé / non daté**, métadonnées incohérentes (PDF créé sous Word).
9. **Valeurs par bâtiment absentes** (audit global pour plusieurs bâtiments).
10. **Travaux réalisés ≠ scénario** sans mise à jour de l'audit.
11. **RGE** absent, hors domaine ou expiré à la date d'engagement ; mandataire de groupement déclaré au lieu du titulaire RGE.
12. **Coefficient CdP mal choisi** (×3 alors que l'ECS fossile reste ; ×1 ou ×3 sur réseau existant).
13. **Chronologie** : engagement avant audit ; engagement avant prise d'effet de la charte ; devis signé avant l'offre CdP.
14. **Pièces CdP manquantes** : réponse AMO, justification réseau de chaleur.
15. **Cumul** avec une autre fiche (ex. raccordement BAR-TH-137 + 177 sur les mêmes travaux).
16. **Adresse** : siège du bailleur au lieu de l'adresse des travaux.

---

## 11. Règles testables

Conventions : dates ISO ; `null` = donnée absente ; `version` = `A63.1` si `date_engagement ≤ 2026-01-16`, `A80.2` si `≥ 2026-01-17`. Gravité : BLOQUANT = dossier non déposable / inéligible ; ALERTE = à vérifier humainement ; INFO = signalement.

### 11.1 Tableau

| ID | Énoncé | Source | Période | Gravité | Entrées | Test | Message |
|---|---|---|---|---|---|---|---|
| ID-01 | Fiche = collectif | Fiche §1 | toutes | BLOQUANT | type_batiment | `type_batiment == "collectif"` | « Bâtiment non collectif : BAR-TH-174 (maison) ou 175 (appartement), pas 177. » |
| ID-02 | ≥ 3 foyers fiscaux distincts | Fiche §3 | toutes | BLOQUANT | nb_foyers_fiscaux | `nb_foyers_fiscaux >= 3` | « Moins de 3 foyers fiscaux distincts : inéligible. » |
| ID-03 | France métropolitaine | Fiche §1 | toutes | BLOQUANT | code_postal | `not cp.startswith(("971","972","973","974","976"))` | « Hors métropole : fiche non applicable. » |
| ID-04 | Bâtiment existant > 2 ans | Partie A | toutes | BLOQUANT | date_construction, date_engagement | `date_engagement - date_construction > 2 ans` ; si date_construction null → ALERTE | « Bâtiment de moins de 2 ans à l'engagement. » |
| ID-05 | Version de fiche | Arrêtés 06/09/2024, 07/01/2026 | toutes | INFO | date_engagement | voir convention | « Version applicable : vA… » |
| ID-06 | Engagement dans la période | Fiche vA80.2 | toutes | BLOQUANT | date_engagement | `2024-11-01 <= date_engagement <= 2030-12-31` (dérogations 145 : ALERTE) | « Date d'engagement hors période de la fiche. » |
| AU-01 | Audit présent | Fiche §3 | toutes | BLOQUANT | type_document | `type_document == "audit"` | « Aucun audit énergétique : non éligible. » |
| AU-02 | Audit réglementaire | Art. 8 arr. 17/11/2020 | toutes | BLOQUANT | mention_non_reglementaire, num_ademe | `not mention_non_reglementaire and num_ademe != null` | « Audit non réglementaire ou sans n° ADEME : non conforme à l'art. 8. » |
| AU-03 | Méthode 3CL-DPE | Arr. 4/05/2022 art. 2 | toutes | BLOQUANT | methode_calcul | `methode_calcul contient "3CL"` | « Méthode de calcul non conforme (3CL-DPE exigée). » |
| AU-04 | Fichier XML présent | Fiche §3 | toutes | BLOQUANT | xml_present | `xml_present == true` | « Fichier source XML de l'audit manquant. » |
| AU-05 | XML = PDF | INTERPRÉTATION | toutes | ALERTE | xml.cep_initial, pdf.cep_initial, xml.shab, pdf.shab | `abs(xml.cep_i - pdf.cep_i) <= 1 and abs(xml.shab - pdf.shab)/pdf.shab <= 0.01` | « Le XML ne correspond pas au rapport (mauvais fichier ?). » |
| AU-06 | Rapport daté et signé | Fiche §3 | toutes | BLOQUANT | date_audit, signature | `date_audit != null and signature == true` | « Rapport d'audit non daté ou non signé. » |
| AU-07 | Logiciel nom + version | Fiche §3 ; E ter I.1 1) | toutes | BLOQUANT | logiciel_nom, logiciel_version | both not null | « Nom ou version du logiciel absent. » |
| AU-08 | Logiciel validé | Arr. 31/03/2021 art. 3 | toutes | ALERTE | logiciel_nom, liste_officielle | `logiciel_nom in liste_officielle_audit` | « Logiciel absent de la liste officielle à jour : vérifier. » |
| AU-09 | Auditeur qualifié collectif | Fiche ; décret 2022-780 art. 1 | toutes | BLOQUANT | qualif_auditeur | `qualif_auditeur in {"OPQIBI 1905", <équivalent I art.1 décret 2018-416>, "architecte formé"}` ; certification diagnostiqueur ou 1911 → KO | « Qualification de l'auditeur non adaptée au bâtiment collectif. » |
| AU-10 | SIREN auditeur valide | — | toutes | BLOQUANT | siren_be | Luhn sur 9 chiffres | « SIREN du BE invalide. » |
| AU-11 | Audit < 5 ans à l'engagement | Décret 2022-780 art. 2 | toutes | BLOQUANT | date_audit, date_engagement | `date_engagement <= date_audit + 5 ans` | « Audit expiré à la date d'engagement. » |
| AU-12 | Audit avant engagement | Fiche §3 (« préalablement ») | toutes | BLOQUANT | date_audit, date_engagement | `date_audit <= date_engagement` | « Engagement antérieur à l'audit. » |
| AU-13 | Rapport ≤ 1 mois après visite | Arr. 4/05/2022 art. 4 | toutes | ALERTE | date_visite, date_audit | `date_audit - date_visite <= 31 j` | « Rapport établi plus d'un mois après la visite. » |
| AU-14 | Valeurs obligatoires | Fiche §3 ; E ter I.1 2) | toutes | BLOQUANT | cep_i, cep_p, cef_i, cef_p, ges_i, ges_p, shab | tous not null | « Valeur obligatoire absente de l'audit : {champ}. » |
| AU-15 | Pas de déduction PV | Fiche ; E ter I.1 5) | toutes | BLOQUANT | pv_deduit | `pv_deduit == false` (si l'audit donne 2 valeurs, prendre celle sans déduction) | « Consommations avec déduction du PV : utiliser les valeurs sans déduction. » |
| AU-16 | Chauffage fixe | E ter I.1 6) | toutes | BLOQUANT | chauffage_non_fixe | `== false` | « L'audit compte un chauffage non fixe. » |
| AU-17 | Audit par bâtiment | INTERPRÉTATION | toutes | BLOQUANT | nb_batiments_couverts, valeurs_par_batiment | `nb == 1 or valeurs_par_batiment == true` | « Audit global sans valeurs par bâtiment. » |
| AU-18 | Copro : une proposition admise | Art. 8 II.1 | toutes | INFO | copro, nb_scenarios | si `copro` : `nb_scenarios >= 1` sinon `>= 2` | « Hors copropriété, l'audit doit comporter au moins 2 propositions. » |
| AU-19 | Cohérence coefficient élec | Arr. 13/08/2025, 19/08/2026 | toutes | ALERTE | date_audit, cep_i, cep_p | Cep i et p issus du même audit ; afficher coef selon date (2,3 / 1,9 / 1,7) | « Cep initial et projet doivent venir du même calcul. » |
| PE-01 | Cep projet < 331 | Fiche §3 | toutes | BLOQUANT | cep_p | `cep_p < 331` | « Cep projet ≥ 331 kWhEP/m².an : inéligible. » |
| PE-02 | Gain ≥ 35 % recalculé | Fiche §3 | toutes | BLOQUANT | cep_i, cep_p | `(cep_i - cep_p)/cep_i >= 0.35` (pas d'arrondi avant comparaison) | « Gain {x} % < 35 % : inéligible. » |
| PE-03 | Gain annoncé = gain recalculé | — | toutes | ALERTE | gain_annonce, cep_i, cep_p | `abs(gain_annonce - gain_calc) <= 0.5 pt` | « Gain annoncé incohérent avec les Cep. » |
| PE-04 | GES après ≤ avant | Fiche §3 | toutes | BLOQUANT | ges_i, ges_p | `ges_p <= ges_i` | « Émissions de GES en hausse : inéligible. » |
| PE-05 | Pas de chaudière charbon/fioul installée | Fiche §3 | toutes | BLOQUANT | equipements_installes, raccordement_rcu | si `not raccordement_rcu` : aucune chaudière d'énergie ∈ {charbon, fioul} | « Installation d'une chaudière charbon/fioul : inéligible. » |
| PE-06 | Gaz installé ≤ 30 % | Fiche §3 | toutes | BLOQUANT | equipements_installes, taux_couverture_gaz | si chaudière gaz installée et `not raccordement_rcu` : `taux_couverture_gaz <= 0.30` ; si taux null → ALERTE « à justifier » | « Chaudière gaz couvrant {x} % > 30 % : inéligible. » |
| PE-07 | Gaz conservé | INTERPRÉTATION | toutes | ALERTE | equipements_conserves | chaudière gaz/fioul conservée → alerte | « Équipement fossile conservé : non interdit par la fiche à la lettre, exclut le ×3 ; faire valider. » |
| PE-08 | Scénario retenu éligible | E ter I.2/I.3 | toutes | BLOQUANT | scenarios[] | `any(PE-01..PE-06 ok for s in scenarios)` | « Aucun scénario de l'audit n'est éligible. » |
| PE-09 | Étape intermédiaire | INTERPRÉTATION | toutes | INFO | etape.gain | si étape non finale et gain < 35 % | « Étape {n} non valorisable seule. » |
| TR-01 | RGE par catégorie | Fiche §3 | toutes | BLOQUANT | entreprises[].qualif, .domaine, .validite | pour chaque catégorie 1°-16° du décret 2014-812 : qualif RGE correspondante (ou 17°) valide à date_engagement | « Entreprise {x} sans RGE valide pour {domaine}. » |
| TR-02 | Travaux = scénario | E ter II 1)-2) | toutes | BLOQUANT (au dépôt) | travaux_realises, scenario_retenu | chaque poste réalisé ⊂ scénario ; quantité ≥ ; performance ≥ ; sinon audit mis à jour requis | « Travaux différents du scénario : mise à jour de l'audit obligatoire. » |
| TR-03 | Facture mentionne performances | Fiche §3 | toutes | BLOQUANT (au dépôt) | facture.postes[].performance | not null pour chaque poste | « Preuve de réalisation sans niveaux de performance. » |
| TR-04 | Liste préconisés/réalisés signée | Fiche §3 | toutes | BLOQUANT (au dépôt) | signatures | bénéficiaire + auditeur + chaque pro/MOE | « Liste travaux préconisés/réalisés non signée par tous. » |
| TR-05 | Quantités d'isolant/menuiseries | Arr. 4/05/2022 art. 2 III 9° | toutes | ALERTE | poste.quantite | not null pour isolation/menuiserie | « Surface d'isolant/menuiserie absente du scénario. » |
| SU-01 | Shab après rénovation | Fiche §5 | toutes | BLOQUANT | shab, shab_type | `shab_type == "apres"` | « La Shab doit être celle après rénovation. » |
| SU-02 | Shab cohérente | E ter I.1 3) | toutes | ALERTE | shab_declaree, shab_mesuree | `abs(decl - mes)/mes <= 0.10` | « Écart de Shab > 10 % : contrôle non satisfaisant. » |
| SU-03 | DP si surface ajoutée | Fiche §3 | toutes | BLOQUANT (au dépôt) | shab_apres, shab_avant, dp_presente | si `shab_apres > shab_avant` : `dp_presente` | « Surface ajoutée sans déclaration préalable. » |
| CO-01 | Copro : accord | Fiche §3 | toutes | BLOQUANT | copro, accord_copro | si copro : accord_copro | « Accord de copropriété manquant. » |
| CO-02 | Copro : immatriculation | Partie A ; art. 3-5-3 III | toutes | BLOQUANT | copro, num_immat | si copro : not null | « N° d'immatriculation de la copropriété manquant. » |
| VO-01 | Volume | Fiche §5 ; art. 3-5-3 IV | toutes | INFO | shab, coef | `vol_kwhc = 2100 * shab * coef` | « Volume : {vol} kWh cumac. » |
| VO-02 | Coefficient ×3 | Art. 3-5-3 IV | CdP | BLOQUANT si ×3 déclaré à tort | energie_ch_avant, energie_ecs_avant, systeme_apres | `coef == 3` ⇔ CdP et tous les équipements chauffage ET ECS charbon/fioul/gaz remplacés par un système renouvelable (appoint fossile ≤ 30 %) | « Coefficient 3 non justifié : {raison}. » |
| VO-03 | Coefficient ×2 | Art. 3-5-3 IV | CdP | INFO | — | CdP et non ×3 → 2 | « Coup de pouce : coefficient 2 (autres travaux). » |
| VO-04 | Hors CdP ×1 | Fiche | — | INFO | cdp | `not cdp → coef = 1` | — |
| CP-01 | Charte en vigueur | Art. 3-5-3 I ; charte | CdP | BLOQUANT | date_engagement, charte, date_effet_charte | IV-6 : engagement ≤ 2025-12-31 et achèvement ≤ 2027-12-31 ; IV-8 : engagement ≥ 2026-01-17 ; engagement > date_effet_charte | « Engagement hors période du Coup de pouce / avant prise d'effet de la charte. » |
| CP-02 | Fenêtre 01-16/01/2026 | INTERPRÉTATION | CdP | ALERTE | date_engagement | `2026-01-01 <= d <= 2026-01-16` | « Engagement dans la fenêtre sans charte applicable : à confirmer. » |
| CP-03 | 75 % / 65 % résidence principale | Art. 3-5-3 III | CdP | BLOQUANT | part_rp, copro, nb_lots_hab | `part_rp >= 0.75` ou (copro et nb_lots_hab <= 20 et part_rp >= 0.65) | « Moins de 75 % (65 %) des lots en résidence principale. » |
| CP-04 | Raccordement réseau ou justificatif | Art. 3-5-3 III | CdP | BLOQUANT | changement_chauffage_ecs, raccordement_rcu, justif_rcu | si changement et not raccordement : justif_rcu in {cas1, cas2a, cas2b} | « Changement de chauffage sans raccordement ni justification d'impossibilité. » |
| CP-05 | Pas de chauffe-eau charbon/fioul | Art. 3-5-3 III | CdP | BLOQUANT | equipements_installes | aucun chauffe-eau charbon/fioul | « Chauffe-eau charbon/fioul installé : CdP exclu. » |
| CP-06 | AMO proposée et réponse écrite | Art. 3-5-3 V | CdP | BLOQUANT (au dépôt) | reponse_amo | not null (copro : PV d'AG) | « Réponse écrite AMO / financement manquante. » |
| CP-07 | Offre CdP avant devis | Charte | CdP | BLOQUANT | date_offre, date_engagement | `date_offre < date_engagement` | « Devis signé avant l'offre Coup de pouce. » |
| CT-01 | Contrôle avant travaux | Arr. 28/09/2021 annexe II, E ter I | ≥ 01/11/2024 | BLOQUANT | date_controle_1, date_debut_travaux | `date_controle_1 < date_debut_travaux` | « Pas de contrôle avant travaux possible : travaux déjà démarrés. » |
| CT-02 | Audit satisfaisant avant contrôle 2 | Art. 7 I bis | ≥ 01/11/2024 | BLOQUANT | resultat_controle_1 | `== "satisfaisant"` | « Contrôle à l'achèvement impossible sans avis satisfaisant sur l'audit. » |
| CT-03 | Contrôleur ≠ auditeur | Charte IV-6/IV-8 | toutes | BLOQUANT | siren_controleur, siren_be | `!=` | « L'organisme de contrôle a réalisé l'audit. » |
| CU-01 | Non-cumul | Fiche §2 | toutes | BLOQUANT | autres_operations[] | aucune opération CEE d'engagement ≥ sur les mêmes postes | « Cumul interdit avec {fiche}. » |
| AD-01 | Adresse ≠ siège | PRATIQUE | toutes | ALERTE | adresse_audit, adresse_siege_beneficiaire | `adresse_audit != adresse_siege` | « Adresse de l'audit = siège du bailleur : vérifier l'adresse des travaux. » |
| DA-01 | Ordre chronologique | Fiche / E ter | toutes | BLOQUANT | dates | `visite <= audit <= engagement <= debut_travaux <= derniere_facture` | « Chronologie incohérente : {détail}. » |
| DA-02 | Délai de dépôt | INCERTAIN | toutes | ALERTE | date_achevement, date_depot | `date_depot <= date_achevement + 12 mois` (à vérifier) | « Délai de dépôt possiblement dépassé. » |

### 11.2 YAML

```yaml
version_referentiel: "2026-10-30"
fiche: BAR-TH-177
conventions:
  version_fiche:
    - {si: "date_engagement <= 2026-01-16", alors: "A63.1"}
    - {si: "date_engagement >= 2026-01-17", alors: "A80.2"}
  coef_electricite:
    - {jusqu_au: "2025-12-31", valeur: 2.3}
    - {du: "2026-01-01", au: "2026-12-31", valeur: 1.9}
    - {du: "2027-01-01", valeur: 1.7}
rules:
  - id: ID-01
    enonce: "Bâtiment résidentiel collectif"
    source: "BAR-TH-177 §1"
    gravite: BLOQUANT
    entrees: [type_batiment]
    test: "type_batiment == 'collectif'"
    message: "Bâtiment non collectif : BAR-TH-174 (maison) ou 175 (appartement), pas 177."
  - id: ID-02
    enonce: "Au moins 3 foyers fiscaux distincts"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [nb_foyers_fiscaux]
    test: "nb_foyers_fiscaux >= 3"
    message: "Moins de 3 foyers fiscaux distincts : inéligible."
  - id: ID-03
    enonce: "France métropolitaine"
    source: "BAR-TH-177 §1"
    gravite: BLOQUANT
    entrees: [code_postal]
    test: "not code_postal[:3] in ['971','972','973','974','976']"
    message: "Hors métropole : fiche non applicable."
  - id: ID-04
    enonce: "Bâtiment existant depuis plus de 2 ans"
    source: "Annexe 1 partie A"
    gravite: BLOQUANT
    entrees: [date_construction, date_engagement]
    test: "date_construction is None ? ALERTE : years_between(date_construction, date_engagement) > 2"
    message: "Bâtiment de moins de 2 ans à la date d'engagement."
  - id: ID-06
    enonce: "Engagement dans la période de la fiche"
    source: "Arrêtés 06/09/2024 et 07/01/2026"
    gravite: BLOQUANT
    entrees: [date_engagement]
    test: "'2024-11-01' <= date_engagement <= '2030-12-31'"
    message: "Date d'engagement hors période de la fiche."
  - id: AU-01
    enonce: "Le document est un audit énergétique"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [type_document]
    test: "type_document == 'audit'"
    message: "Aucun audit énergétique : non éligible."
  - id: AU-02
    enonce: "Audit réglementaire avec n° ADEME"
    source: "Arrêté 17/11/2020 art. 8 I.1 et I.5"
    gravite: BLOQUANT
    entrees: [mention_non_reglementaire, num_ademe]
    test: "not mention_non_reglementaire and num_ademe is not None"
    message: "Audit non réglementaire ou sans n° ADEME : non conforme à l'art. 8."
  - id: AU-03
    enonce: "Méthode 3CL-DPE"
    source: "Arrêté 04/05/2022 art. 2"
    gravite: BLOQUANT
    entrees: [methode_calcul]
    test: "'3CL' in methode_calcul"
    message: "Méthode de calcul non conforme (3CL-DPE exigée)."
  - id: AU-04
    enonce: "Fichier XML source présent"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [xml_present]
    test: "xml_present == true"
    message: "Fichier source XML de l'audit manquant."
  - id: AU-05
    enonce: "XML cohérent avec le PDF"
    source: "Interprétation"
    gravite: ALERTE
    entrees: [xml.cep_initial, pdf.cep_initial, xml.shab, pdf.shab]
    test: "abs(xml.cep_initial - pdf.cep_initial) <= 1 and abs(xml.shab - pdf.shab) / pdf.shab <= 0.01"
    message: "Le XML ne correspond pas au rapport (mauvais fichier ?)."
  - id: AU-06
    enonce: "Rapport daté et signé"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [date_audit, signature]
    test: "date_audit is not None and signature == true"
    message: "Rapport d'audit non daté ou non signé."
  - id: AU-07
    enonce: "Nom et version du logiciel"
    source: "BAR-TH-177 §3 ; arrêté 28/09/2021 annexe III E ter I.1 1)"
    gravite: BLOQUANT
    entrees: [logiciel_nom, logiciel_version]
    test: "logiciel_nom and logiciel_version"
    message: "Nom ou version du logiciel absent."
  - id: AU-08
    enonce: "Logiciel sur la liste officielle"
    source: "Arrêté 31/03/2021 art. 3"
    gravite: ALERTE
    entrees: [logiciel_nom]
    test: "logiciel_nom in LISTE_OFFICIELLE_AUDIT"
    message: "Logiciel absent de la liste officielle à jour : vérifier."
  - id: AU-09
    enonce: "Auditeur qualifié pour le collectif"
    source: "BAR-TH-177 §3 ; décret 2022-780 art. 1 1°"
    gravite: BLOQUANT
    entrees: [qualif_auditeur]
    test: "qualif_auditeur in QUALIFS_COLLECTIF  # OPQIBI 1905, équivalents décret 2018-416 I, architecte formé"
    message: "Qualification de l'auditeur non adaptée au bâtiment collectif."
  - id: AU-10
    enonce: "SIREN auditeur valide"
    gravite: BLOQUANT
    entrees: [siren_be]
    test: "luhn(siren_be) and len(siren_be) == 9"
    message: "SIREN du BE invalide."
  - id: AU-11
    enonce: "Audit de moins de 5 ans à l'engagement"
    source: "Décret 2022-780 art. 2 via arrêté 17/11/2020 art. 8 I.2"
    gravite: BLOQUANT
    entrees: [date_audit, date_engagement]
    test: "date_engagement <= add_years(date_audit, 5)"
    message: "Audit expiré à la date d'engagement."
  - id: AU-12
    enonce: "Audit antérieur à l'engagement"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [date_audit, date_engagement]
    test: "date_audit <= date_engagement"
    message: "Engagement antérieur à l'audit."
  - id: AU-13
    enonce: "Rapport sous un mois après la visite"
    source: "Arrêté 04/05/2022 art. 4"
    gravite: ALERTE
    entrees: [date_visite, date_audit]
    test: "days_between(date_visite, date_audit) <= 31"
    message: "Rapport établi plus d'un mois après la visite."
  - id: AU-14
    enonce: "Valeurs obligatoires présentes"
    source: "BAR-TH-177 §3 ; E ter I.1 2)"
    gravite: BLOQUANT
    entrees: [cep_initial, cep_projet, cef_initial, cef_projet, ges_initial, ges_projet, shab]
    test: "all(v is not None for v in entrees)"
    message: "Valeur obligatoire absente de l'audit : {champ}."
  - id: AU-15
    enonce: "Consommations sans déduction du PV"
    source: "BAR-TH-177 §3 ; E ter I.1 5)"
    gravite: BLOQUANT
    entrees: [pv_deduit]
    test: "pv_deduit == false"
    message: "Consommations avec déduction du PV : utiliser les valeurs sans déduction."
  - id: AU-16
    enonce: "Pas de chauffage non fixe"
    source: "E ter I.1 6)"
    gravite: BLOQUANT
    entrees: [chauffage_non_fixe]
    test: "chauffage_non_fixe == false"
    message: "L'audit compte un chauffage non fixe."
  - id: AU-17
    enonce: "Valeurs par bâtiment"
    source: "Interprétation"
    gravite: BLOQUANT
    entrees: [nb_batiments_couverts, valeurs_par_batiment]
    test: "nb_batiments_couverts == 1 or valeurs_par_batiment"
    message: "Audit global sans valeurs par bâtiment."
  - id: AU-18
    enonce: "Nombre de propositions"
    source: "Arrêté 04/05/2022 art. 2 II ; arrêté 17/11/2020 art. 8 II.1"
    gravite: INFO
    entrees: [copro, nb_scenarios]
    test: "nb_scenarios >= (1 if copro else 2)"
    message: "Hors copropriété, l'audit doit comporter au moins 2 propositions."
  - id: AU-19
    enonce: "Cep initial et projet issus du même calcul"
    source: "Arrêtés 13/08/2025 et 19/08/2026"
    gravite: ALERTE
    entrees: [source_cep_initial, source_cep_projet]
    test: "source_cep_initial == source_cep_projet"
    message: "Cep initial et projet doivent venir du même audit."
  - id: PE-01
    enonce: "Cep projet < 331"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [cep_projet]
    test: "cep_projet < 331"
    message: "Cep projet ≥ 331 kWhEP/m².an : inéligible."
  - id: PE-02
    enonce: "Gain ≥ 35 %"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [cep_initial, cep_projet]
    test: "(cep_initial - cep_projet) / cep_initial >= 0.35"
    message: "Gain {gain} % < 35 % : inéligible."
  - id: PE-03
    enonce: "Gain annoncé cohérent"
    gravite: ALERTE
    entrees: [gain_annonce, cep_initial, cep_projet]
    test: "abs(gain_annonce - 100*(cep_initial-cep_projet)/cep_initial) <= 0.5"
    message: "Gain annoncé incohérent avec les Cep."
  - id: PE-04
    enonce: "GES après ≤ GES avant"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [ges_initial, ges_projet]
    test: "ges_projet <= ges_initial"
    message: "Émissions de GES en hausse : inéligible."
  - id: PE-05
    enonce: "Pas de chaudière charbon/fioul installée hors réseau"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [equipements_installes, raccordement_rcu]
    test: "raccordement_rcu or not any(e.type=='chaudiere' and e.energie in ['charbon','fioul'] for e in equipements_installes)"
    message: "Installation d'une chaudière charbon/fioul : inéligible."
  - id: PE-06
    enonce: "Chaudière gaz installée : couverture ≤ 30 %"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [equipements_installes, taux_couverture_gaz, raccordement_rcu]
    test: |
      if raccordement_rcu: OK
      elif not any(e.type=='chaudiere' and e.energie=='gaz' for e in equipements_installes): OK
      elif taux_couverture_gaz is None: ALERTE
      else: taux_couverture_gaz <= 0.30
    message: "Chaudière gaz couvrant {taux} % > 30 % : inéligible."
  - id: PE-07
    enonce: "Équipement fossile conservé"
    source: "Interprétation"
    gravite: ALERTE
    entrees: [equipements_conserves]
    test: "not any(e.energie in ['gaz','fioul','charbon'] for e in equipements_conserves)"
    message: "Équipement fossile conservé : pas interdit à la lettre, exclut le ×3 ; faire valider."
  - id: PE-08
    enonce: "Au moins un scénario éligible"
    source: "E ter I.2 / I.3"
    gravite: BLOQUANT
    entrees: [scenarios]
    test: "any(all_ok(s, ['PE-01','PE-02','PE-04','PE-05','PE-06']) for s in scenarios)"
    message: "Aucun scénario de l'audit n'est éligible."
  - id: PE-09
    enonce: "Étape intermédiaire non valorisable seule"
    source: "Interprétation"
    gravite: INFO
    entrees: [etape.gain, etape.finale]
    test: "etape.finale or etape.gain >= 0.35"
    message: "Étape {n} non valorisable seule (gain < 35 %)."
  - id: TR-01
    enonce: "RGE par catégorie de travaux"
    source: "BAR-TH-177 §3 ; décret 2014-812"
    gravite: BLOQUANT
    entrees: [entreprises]
    test: "all(e.qualif_rge and e.domaine_couvert and e.validite_debut <= date_engagement <= e.validite_fin for e in entreprises)"
    message: "Entreprise {nom} sans RGE valide pour {domaine}."
  - id: TR-02
    enonce: "Travaux réalisés conformes au scénario"
    source: "E ter II 1) et 2)"
    gravite: BLOQUANT
    entrees: [travaux_realises, scenario_retenu, audit_mis_a_jour]
    test: "conforme(travaux_realises, scenario_retenu) or audit_mis_a_jour"
    message: "Travaux différents du scénario : mise à jour de l'audit obligatoire."
  - id: TR-03
    enonce: "Facture avec niveaux de performance"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [facture_postes]
    test: "all(p.performance for p in facture_postes)"
    message: "Preuve de réalisation sans niveaux de performance."
  - id: TR-04
    enonce: "Liste préconisés/réalisés signée par tous"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [signataires_liste]
    test: "{'beneficiaire','auditeur'} <= signataires_liste and all(p in signataires_liste for p in professionnels)"
    message: "Liste travaux préconisés/réalisés non signée par tous."
  - id: TR-05
    enonce: "Quantités sur postes isolation/menuiserie"
    source: "Arrêté 04/05/2022 art. 2 III 9°"
    gravite: ALERTE
    entrees: [postes]
    test: "all(p.quantite for p in postes if p.type in ['murs','planchers_bas','toiture','menuiseries'])"
    message: "Surface d'isolant/menuiserie absente du scénario."
  - id: SU-01
    enonce: "Shab après rénovation"
    source: "BAR-TH-177 §5"
    gravite: BLOQUANT
    entrees: [shab_type]
    test: "shab_type == 'apres'"
    message: "La Shab doit être celle après rénovation."
  - id: SU-02
    enonce: "Écart de Shab ≤ 10 %"
    source: "E ter I.1 3)"
    gravite: ALERTE
    entrees: [shab_declaree, shab_mesuree]
    test: "abs(shab_declaree - shab_mesuree) / shab_mesuree <= 0.10"
    message: "Écart de Shab > 10 % : contrôle non satisfaisant."
  - id: SU-03
    enonce: "DP si surface ajoutée"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [shab_avant, shab_apres, dp_presente]
    test: "shab_apres <= shab_avant or dp_presente"
    message: "Surface ajoutée sans déclaration préalable."
  - id: CO-01
    enonce: "Accord de copropriété"
    source: "BAR-TH-177 §3"
    gravite: BLOQUANT
    entrees: [copro, accord_copro]
    test: "not copro or accord_copro"
    message: "Accord de copropriété manquant."
  - id: CO-02
    enonce: "Immatriculation de la copropriété"
    source: "Partie A ; art. 3-5-3 III"
    gravite: BLOQUANT
    entrees: [copro, num_immatriculation]
    test: "not copro or num_immatriculation"
    message: "N° d'immatriculation de la copropriété manquant."
  - id: VO-01
    enonce: "Calcul du volume"
    source: "BAR-TH-177 §5 ; arrêté 29/12/2014 art. 3-5-3 IV"
    gravite: INFO
    entrees: [shab, coef]
    test: "volume_kwhc = 2100 * shab * coef"
    message: "Volume : {volume_kwhc} kWh cumac."
  - id: VO-02
    enonce: "Coefficient 3 justifié"
    source: "Arrêté 29/12/2014 art. 3-5-3 IV"
    gravite: BLOQUANT
    entrees: [cdp, equipements_ch_avant, equipements_ecs_avant, systeme_apres]
    test: |
      coef == 3 implies (
        cdp
        and all(e.energie in ['charbon','fioul','gaz'] and e.remplace for e in equipements_ch_avant + equipements_ecs_avant if e.energie in ['charbon','fioul','gaz'])
        and any(e.energie in ['charbon','fioul','gaz'] for e in equipements_ch_avant + equipements_ecs_avant)
        and systeme_apres.renouvelable
        and (systeme_apres.appoint_gaz_taux or 0) <= 0.30
      )
    message: "Coefficient 3 non justifié : {raison}."
  - id: VO-03
    enonce: "Coefficient 2 (CdP autres travaux)"
    gravite: INFO
    test: "cdp and not cond_coef3 -> coef = 2"
  - id: VO-04
    enonce: "Coefficient 1 hors CdP"
    gravite: INFO
    test: "not cdp -> coef = 1"
  - id: CP-01
    enonce: "Charte applicable à la date d'engagement"
    source: "Arrêté 29/12/2014 art. 3-5-3 I ; chartes IV-6 / IV-8"
    gravite: BLOQUANT
    entrees: [cdp, charte, date_engagement, date_achevement, date_effet_charte]
    test: |
      not cdp or (
        date_engagement > date_effet_charte and (
          (charte == 'IV-6' and date_engagement <= '2025-12-31' and date_achevement <= '2027-12-31')
          or (charte == 'IV-8' and date_engagement >= '2026-01-17')))
    message: "Engagement hors période du Coup de pouce ou avant prise d'effet de la charte."
  - id: CP-02
    enonce: "Fenêtre 1er-16 janvier 2026"
    source: "Interprétation"
    gravite: ALERTE
    entrees: [cdp, date_engagement]
    test: "not (cdp and '2026-01-01' <= date_engagement <= '2026-01-16')"
    message: "Engagement dans la fenêtre sans charte applicable : à confirmer."
  - id: CP-03
    enonce: "75 % (65 %) des lots en résidence principale"
    source: "Arrêté 29/12/2014 art. 3-5-3 III"
    gravite: BLOQUANT
    entrees: [cdp, part_rp, copro, nb_lots_habitation]
    test: "not cdp or part_rp >= 0.75 or (copro and nb_lots_habitation <= 20 and part_rp >= 0.65)"
    message: "Moins de 75 % (65 %) des lots en résidence principale."
  - id: CP-04
    enonce: "Raccordement réseau efficace ou justificatif"
    source: "Arrêté 29/12/2014 art. 3-5-3 III"
    gravite: BLOQUANT
    entrees: [cdp, changement_chauffage_ecs, raccordement_rcu, justif_rcu]
    test: "not (cdp and changement_chauffage_ecs and not raccordement_rcu) or justif_rcu in ['cas1','cas2a','cas2b']"
    message: "Changement de chauffage sans raccordement ni justification d'impossibilité."
  - id: CP-05
    enonce: "Pas de chauffe-eau charbon/fioul"
    source: "Arrêté 29/12/2014 art. 3-5-3 III"
    gravite: BLOQUANT
    entrees: [cdp, equipements_installes]
    test: "not cdp or not any(e.type=='chauffe_eau' and e.energie in ['charbon','fioul'] for e in equipements_installes)"
    message: "Chauffe-eau charbon/fioul installé : Coup de pouce exclu."
  - id: CP-06
    enonce: "Réponse écrite AMO et financement"
    source: "Arrêté 29/12/2014 art. 3-5-3 V"
    gravite: BLOQUANT
    entrees: [cdp, reponse_amo]
    test: "not cdp or reponse_amo"
    message: "Réponse écrite AMO / financement manquante."
  - id: CP-07
    enonce: "Offre CdP avant le premier devis"
    source: "Charte ; page ministère"
    gravite: BLOQUANT
    entrees: [cdp, date_offre_cdp, date_engagement]
    test: "not cdp or date_offre_cdp < date_engagement"
    message: "Devis signé avant l'offre Coup de pouce."
  - id: CT-01
    enonce: "Contrôle avant travaux"
    source: "Arrêté 28/09/2021 annexe II et annexe III E ter I"
    gravite: BLOQUANT
    entrees: [date_controle_avant, date_debut_travaux]
    test: "date_controle_avant is not None and date_controle_avant < date_debut_travaux"
    message: "Pas de contrôle avant travaux possible : travaux déjà démarrés."
  - id: CT-02
    enonce: "Audit satisfaisant avant contrôle à l'achèvement"
    source: "Arrêté 28/09/2021 art. 7 I bis"
    gravite: BLOQUANT
    entrees: [resultat_controle_avant]
    test: "resultat_controle_avant == 'satisfaisant'"
    message: "Contrôle à l'achèvement impossible sans avis satisfaisant sur l'audit."
  - id: CT-03
    enonce: "Contrôleur distinct de l'auditeur"
    source: "Chartes IV-6 / IV-8"
    gravite: BLOQUANT
    entrees: [siren_controleur, siren_be]
    test: "siren_controleur != siren_be"
    message: "L'organisme de contrôle a réalisé l'audit."
  - id: CU-01
    enonce: "Non-cumul avec d'autres fiches"
    source: "BAR-TH-177 §2"
    gravite: BLOQUANT
    entrees: [autres_operations]
    test: "not any(o.date_engagement >= date_engagement and o.domaine in DOMAINES_177 for o in autres_operations)"
    message: "Cumul interdit avec {fiche}."
  - id: AD-01
    enonce: "Adresse des travaux ≠ siège du bailleur"
    source: "Pratique"
    gravite: ALERTE
    entrees: [adresse_audit, adresse_siege_beneficiaire]
    test: "normalize(adresse_audit) != normalize(adresse_siege_beneficiaire)"
    message: "Adresse de l'audit = siège du bailleur : vérifier l'adresse des travaux."
  - id: DA-01
    enonce: "Ordre chronologique"
    gravite: BLOQUANT
    entrees: [date_visite, date_audit, date_engagement, date_debut_travaux, date_derniere_facture]
    test: "date_visite <= date_audit <= date_engagement <= date_debut_travaux <= date_derniere_facture"
    message: "Chronologie incohérente : {détail}."
  - id: DA-02
    enonce: "Délai de dépôt (À VÉRIFIER)"
    gravite: ALERTE
    entrees: [date_achevement, date_depot]
    test: "date_depot <= add_months(date_achevement, 12)"
    message: "Délai de dépôt possiblement dépassé (règle à confirmer)."
```

---

## 12. Données à extraire de l'audit et à saisir

Légende origine : **A** = dans l'audit (PDF/XML) · **S** = à saisir / autre pièce.

| Champ | Type | Unité | Où | Origine |
|---|---|---|---|---|
| type_document | enum audit/DPE/étude | — | titre, en-tête, mention « non réglementaire », « NON ÉMIS ADEME » | A |
| num_ademe | texte (13 car.) | — | en-tête « N° audit » | A |
| methode_calcul / moteur | texte | — | page logiciel / mentions | A |
| logiciel_nom, editeur, version, date_version | texte/date | — | rapport (obligatoire) | A |
| date_visite, date_audit | date | — | en-tête | A |
| signature | bool | — | dernière page (cachet/signature) | A (visuel) |
| be_raison_sociale, be_siren | texte | — | page auditeur ; XML | A |
| qualif_auditeur, numero_qualif | texte | — | page auditeur (souvent absent) | A ou S (certificat OPQIBI) |
| adresse travaux | texte | — | page de garde ; **vérifier ≠ siège** | A (à recouper avec le bailleur) |
| type_batiment | enum | — | « immeuble collectif » / XML | A |
| nb_logements | entier | — | descriptif / XML | A + S (pièce bailleur) |
| nb_foyers_fiscaux | entier | — | — | S (bailleur social : [PRATIQUE] = logements conventionnés) |
| date_construction | année | — | descriptif | A |
| shab_avant, shab_apres | réel | m² | « surface de référence » ; vérifier s'il y a extension | A |
| cep_initial, cep_projet (par scénario/étape) | réel | kWhEP/m².an | état initial ; totaux scénario ; **valeur SANS PV** | A |
| cef_initial, cef_projet | réel | kWhEF/m².an | « énergie finale », « EP (EF) » | A |
| **ges_initial, ges_projet** | réel | kgCO2eq/m².an | étiquette climat, totaux scénario | A |
| pv_deduit / valeurs avec-sans PV | bool + réels | — | tableaux « avec/sans autoconsommation » | A |
| classes énergie et GES avant/après | lettre | — | étiquettes (info) | A |
| gain_annonce | % | — | page scénarios | A |
| energie_ch_avant, energie_ecs_avant + générateurs | enum + texte | — | descriptif systèmes | A |
| equipements_installes (type, énergie, rôle base/appoint) | liste | — | descriptif scénario | A |
| equipements_conserves | liste | — | descriptif scénario | A |
| taux_couverture_gaz | % | — | rarement explicite → note de dimensionnement | A ou S |
| raccordement_rcu, nom réseau, taux EnR&R réseau | bool/texte/% | — | descriptif ; taux souvent absent | A ou S (gestionnaire) |
| chauffage_non_fixe | bool | — | descriptif (appoints mobiles) | A |
| postes de travaux + performances + quantités | liste | m², W/m².K, m².K/W, SCOP… | pages détaillées scénario | A |
| scenario_retenu | id | — | — | S (bailleur) |
| copro, num_immatriculation, accord_copro | bool/texte | — | — | S |
| part_rp (résidence principale) | % | — | — | S (CdP) |
| date_engagement, date_debut_travaux, dates factures | date | — | devis/OS/marché, factures | S |
| entreprises (SIRET, domaine, RGE, validité) | liste | — | — | S (attestations RGE) |
| cdp, charte, date_effet_charte, date_offre_cdp | — | — | — | S (EDF) |
| reponse_amo, justif_rcu | doc | — | — | S |
| date_controle_avant, resultat | date/enum | — | rapport organisme | S |
| autres_operations CEE | liste | — | — | S |
| xml_present, xml.* | — | — | fichier .xml | A |

À noter : **zone climatique inutile** pour le calcul 177 (le champ peut exister dans Odicée, voir §13).

---

## 13. Export Excel / Odicée

### 13.1 Sûr : champs de la partie A officielle (vA80.2)
Ordre de l'annexe 1 (§6.4). Formats : dates jj/mm/aaaa ; Cep/Cef en kWh/m².an ; gain en % ; O/N en cases.

### 13.2 Ce que je connais du fichier « Import lots de travaux » Odicée (A80.2) — [PRATIQUE, issu de nos dossiers, non vérifié sur la plateforme]
Une ligne par bâtiment, colonnes A → BN. Cellules marquées « X » dans le fichier d'origine : à laisser vides.

| Col. | Champ | Remarque |
|---|---|---|
| C | Nom du site* | |
| D, E | N°, voie* | adresse des travaux |
| H, I | CP*, ville* | |
| J | ID lot | |
| K | Nb logements | |
| L | Logements conventionnés | |
| M | Département | |
| N | ID pro 1 | |
| R, S | Coup de pouce, version CdP | |
| AB | SurfaceHabitable | Shab après |
| AC | nb_logements_distincts | = K |
| AD | nb_foyers_distincts | [PRATIQUE] = L pour un bailleur social |
| AE | relève copro | 0/1 |
| AF | immatriculation | |
| AG | audit_prealable | 1 |
| AH, AI | Cep avant / après | |
| AJ, AK | Cef avant / après | |
| AL | gain | |
| AM | hors_raccordement (chaudière fossile installée ?) | doit être 0 / Non |
| AN, AO | équipements avant / après | |
| AP | GES en baisse | 1 |
| AQ, AR | raison sociale / SIREN BE | |
| AS | date audit | |
| AT | référence audit | idéalement n° ADEME |
| AU, AV, AW | logiciel + éditeur, version, date de version | |
| AX | version fiche | A80.2 |
| AY | BAR-TH-177 | |
| AZ | type_travaux | énumération inconnue → à tester au téléversement |
| BA | is_pac_inclue | true si PAC installée |
| BB | nature_travaux | minuscules, séparés par des virgules (chauffage, eclairage, isolation, menuiserie, ecs, refroidissement, ventilation) — orthographe exacte À VÉRIFIER |
| BD / BN | volumes | Odicée peut recalculer |
| BE | energieChauffage | |
| BG | coefficient_zone | n'existe pas dans la fiche ; usage Odicée inconnu |
| BH, BI | respect_prerequis | |
| BJ | version CdP | |
| BL | pourcent_energie | signification exacte inconnue |

Vides obligatoires (« X ») : ID site, SIRET, ID pro 2, commentaire, complément d'adresse, montants €, coûts HT/TTC, TVA, aides.

### 13.3 Formulaire Odicée (bloc de saisie par scénario) — [PRATIQUE]
Cep initial · Cep projet · Cef initial · Cef projet · Gain % · nature des travaux (cases) · PAC air/eau, air/air ou eau/eau O/N · taux EnR&R après travaux · équipements avant · équipements après · Shab · nb logements · nb foyers fiscaux · date audit · référence · logiciel (nom + éditeur) · version.

---

## 14. Jeux d'essai

Toutes dates ISO. « ✓ » = règle passée, « ✗ » = échec, « — » = non applicable.

### Cas 1 — conforme, Coup de pouce ×3
- Collectif, 48 lgts, 48 foyers, CP 21000, construit 1972, non copro.
- Audit réglementaire n° ADEME 2621E0012345X, 3CL, Pleiades v6.x, XML ok, signé, BE OPQIBI 1905, visite 2026-02-03, audit 2026-02-20.
- Shab avant = après = 3 020. Cep 245 → 128 ; Cef 220 → 62 ; GES 52 → 9 ; sans PV.
- Avant : chaudière gaz collective (chauffage + ECS). Après : PAC collective air/eau, pas d'appoint fossile. Pas de réseau sur la commune (attestation cas 1).
- CdP charte IV-8 prise d'effet 2026-01-20 ; offre 2026-03-01 ; engagement 2026-03-15 ; contrôle avant 2026-04-02 satisfaisant ; travaux 2026-05-01 → dernière facture 2026-12-10 ; entreprises RGE valides ; AMO refusée par écrit.
- Attendu : tous ✓ ; version A80.2 ; coef 3 ; volume = 19 026 000 kWh cumac.

### Cas 2 — conforme, réseau existant, CdP ×2
- Collectif 60 lgts, raccordé réseau de chaleur (conservé). Shab 4 500. Cep 210 → 125 ; GES 38 → 24.
- Travaux ITE + menuiseries + VMC. CdP IV-8, engagement 2026-06-01, audit 2026-04-10.
- Attendu : PE ✓ ; VO-02 : coef 3 refusé (aucun équipement fossile remplacé) ; coef 2 ; volume 18 900 000 kWh cumac ; CP-04 — (pas de changement de chauffage).

### Cas 3 — non conforme : gain insuffisant
- Cep 260 → 172 (gain 33,85 %), GES 55 → 40, reste conforme.
- Attendu : PE-02 ✗ BLOQUANT « Gain 33,85 % < 35 % » ; PE-08 ✗ si aucun autre scénario ; volume 0.

### Cas 4 — non conforme : chaudière gaz installée
- Chaudière gaz remplacée par chaudière gaz à condensation, ECS gaz. Cep 280 → 165 (41 %), GES 60 → 40.
- Attendu : PE-06 ✗ (couverture gaz 100 %) ; volume 0.

### Cas 5 — non conforme : document et chronologie
- Document « audit non réglementaire », pas de n° ADEME, pas de XML, BE certifié diagnostiqueur DPE uniquement. Audit 2026-05-10 ; engagement 2026-04-01 ; travaux démarrés 2026-04-15 ; aucun contrôle avant travaux.
- Attendu : AU-02 ✗, AU-04 ✗, AU-09 ✗, AU-12 ✗, DA-01 ✗, CT-01 ✗.

### Cas 6 — non conforme : GES en hausse + PV déduit
- Fioul → chaudière bois granulés (pas de restriction P4) mais GES 40 → 45 (cas d'école) ; Cep projet affiché 95 avec déduction PV, 118 sans.
- Attendu : PE-04 ✗ ; AU-15 ✗ tant que la valeur sans PV n'est pas retenue ; recalcul PE-01/PE-02 avec 118.

### Cas 7 — limite : PAC hybride
- Chaudière gaz → PAC + appoint gaz 25 % ; ECS gaz conservée. Cep 230 → 140 (39,1 %), GES 50 → 28. CdP IV-8.
- Attendu : PE-06 ✓ (25 % ≤ 30 %) ; PE-07 ALERTE (ECS gaz conservée) ; VO-02 : coef 3 refusé (ECS fossile non remplacée) → coef 2.

### Cas 8 — limite : écart de surface et Cep à 331
- Cep projet = 331,0 ; Shab déclarée 2 300, mesurée au contrôle 2 050 (écart 12,2 %).
- Attendu : PE-01 ✗ (331 n'est pas < 331) ; SU-02 ALERTE (> 10 %).

---

## Ce que je n'ai pas pu couvrir ou dont je doute

1. **VII de l'art. 2 du décret 2020-26** (qualification exacte exigée par la fiche) : non relu. OPQIBI 1905 est une qualification admise, je ne peux pas lister les équivalents.
2. **Liste officielle des logiciels d'audit** à jour : non consultée.
3. **Prime minimale 41/27 €/m²** sous la charte IV-8 : affichée par le ministère, absente du texte de charte que j'ai lu.
4. **Délai de dépôt** après achèvement et **durée d'archivage** : non vérifiés.
5. **Fenêtre 01-16/01/2026** pour le CdP : interprétation, pas de texte explicite.
6. **Conservation d'une chaudière gaz** et **réseau existant ×2** : lecture du texte, pas de position PNCEE trouvée.
7. **Abrogation de l'arrêté du 13/08/2025 au 01/01/2027** : conséquence sur le renvoi de la vA80.2 inconnue.
8. **Champs Odicée** (AZ, BB, BG, BL) : énumérations et sens non vérifiés sur la plateforme.
9. **Classes DPE** (tableau §3.2) : de mémoire (arrêté du 31/03/2021), non relu.
10. **Fraction précarité** (art. 3-1 IV) pour les logements sociaux : je ne sais pas comment elle est traitée en BAR-TH-177 par Odicée.
11. Positions et FAQ du **PNCEE** : non consultées.

## Questions pour affiner les règles

1. Le scénario retenu par le bailleur est-il une donnée saisie dans l'outil, ou faut-il le déduire (ex. scénario le plus valorisable éligible) ?
2. L'outil doit-il gérer plusieurs bâtiments par audit (audit global) ou refuser d'emblée ?
3. Comment récupérer la qualification de l'auditeur quand elle n'est pas dans l'audit : saisie manuelle ou pièce jointe ?
4. Pour le réseau de chaleur existant, quelle position retiens-tu : ×2 (texte) ou ×1 (ancienne pratique) ? Le pilote EDF a-t-il tranché ?
5. Le taux de couverture gaz : l'outil le saisit-il, ou faut-il l'estimer à partir des besoins de l'audit (approximation à signaler) ?
6. Veux-tu que l'outil applique les règles « au dépôt » (factures, signatures, contrôles) ou seulement la phase audit/éligibilité pour l'instant ?
7. Peux-tu me donner le fichier « Import lots de travaux » Odicée vierge avec une ligne exemple validée, pour fixer les énumérations ?
8. Faut-il intégrer les règles BAR-TH-145 (dossiers sous dérogation) ou ignorer tout engagement avant le 01/11/2024 ?

---

## Sources (consultées le 30/10/2026)

- Fiche BAR-TH-177 vA80.2 : https://www.ecologie.gouv.fr/sites/default/files/documents/BAR-TH-177%20vA80-2%20%C3%A0%20compter%20du%2017-01-2026_0.pdf
- Partie A vA80.2 : https://www.ecologie.gouv.fr/sites/default/files/documents/BAR-TH-177%20vA80-2%20%C3%A0%20compter%20du%2017-01-2026%20-%20Partie%20A.pdf
- Fiche BAR-TH-177 vA63.1 : https://www.ecologie.gouv.fr/sites/default/files/documents/BAR-TH-177%20vA63-1%20%C3%A0%20compter%20du%2001-11-2024_4.pdf
- Page ministère Coup de pouce (MAJ 01/07/2026) : https://www.ecologie.gouv.fr/politiques-publiques/coup-pouce-renovation-performante-batiment-residentiel-collectif
- Charte IV-8 (engagements ≥ 17/01/2026) : https://www.ecologie.gouv.fr/sites/default/files/documents/Mod%C3%A8le%20-%20Charte%20Coup%20de%20pouce%20R%C3%A9novation%20performante%20de%20b%C3%A2timents%20r%C3%A9sidentiels%20collectifs%20%C3%A0%20compter%20du%2017-01-2026.pdf
- Arrêté du 07/01/2026 : https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053373748 et https://aida.ineris.fr/reglementation/arrete-070126-modifiant-fiches-bar-th-174-bar-th-175-bar-th-177-prolongeant
- Arrêté du 06/09/2024 (création, référentiel E ter, transitoires) : https://aida.ineris.fr/reglementation/arrete-060924-modifiant-coup-pouce-renovation-performante-batiment-residentiel
- Arrêté du 18/11/2024 (E ter corrigé, tableau récapitulatif) : https://aida.ineris.fr/reglementation/arrete-181124-modifiant-larrete-22-decembre-2014-definissant-operations
- Arrêté du 29/12/2014 consolidé (art. 3-5-3) : https://aida.ineris.fr/reglementation/arrete-291214-relatif-modalites-dapplication-dispositif-certificats-deconomies
- Arrêté du 28/09/2021 consolidé (contrôles, annexe II 100 %) : https://aida.ineris.fr/reglementation/arrete-280921-relatif-controles-cadre-dispositif-certificats-deconomies-denergie
- Arrêté du 17/11/2020 consolidé (art. 8) : https://aida.ineris.fr/reglementation/arrete-171120-relatif-caracteristiques-techniques-modalites-realisation-travaux
- Arrêté du 04/05/2022 consolidé (contenu de l'audit) : https://aida.ineris.fr/reglementation/arrete-040522-definissant-france-metropolitaine-contenu-laudit-energetique
- Décret 2022-780 consolidé (auditeurs, validité) : https://aida.ineris.fr/reglementation/decret-ndeg-2022-780-040522-relatif-a-laudit-energetique-mentionne-a-larticle-126-28
- Arrêté du 19/08/2026 (coefficient 1,7 au 01/01/2027) : https://aida.ineris.fr/node/46366 et https://www.ecologie.gouv.fr/presse/dpe-audits-energetiques-publication-larrete-abaissant-facteur-conversion-lelectricite-17-1er
- Arrêté du 13/08/2025 (coefficient 1,9 au 01/01/2026) : https://www.ffbatiment.fr/actualites-batiment/actualite/dpe-audit-energetiques-baisse-coefficient-conversion-electricite
