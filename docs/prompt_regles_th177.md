# Prompt à coller dans la conversation qui connaît la fiche TH-177

> Copie tout ce qui est sous la ligne `=== DÉBUT DU PROMPT ===` jusqu'à `=== FIN DU PROMPT ===`.
> Ensuite, rapporte-moi (Claude Code) le fichier .md qu'il produit, en entier.
> Si sa réponse est coupée, réponds « continue » jusqu'à la fin, puis demande-lui un fichier unique.

=== DÉBUT DU PROMPT ===

# Contexte et objectif

Tu es mon expert des Certificats d'Économies d'Énergie (CEE) en France. Dans cette conversation, tu as déjà analysé en détail la fiche d'opération standardisée de **rénovation globale « TH-177 »** (à confirmer par toi : intitulé exact, secteur concerné, texte de référence, version en vigueur). **Je veux que tu me restitues TOUT ce que tu sais à son sujet, de la façon la plus complète, précise et exploitable possible.**

Ce que tu produis va servir de **base de règles** à un logiciel que je construis avec un autre assistant (Claude Code). Ce logiciel doit :
1. lire un audit énergétique PDF,
2. vérifier automatiquement la conformité du dossier aux règles de la fiche,
3. générer un fichier Excel d'export permettant de traiter directement le dossier CEE.

Plus tes règles sont complètes, exactes et testables, moins le logiciel laissera passer d'erreurs. **Une règle oubliée = un dossier refusé.** Sois exhaustif plutôt que synthétique.

# Ce que fait déjà mon outil (pour que tu saches sur quoi tes règles vont se brancher)

L'outil prend en entrée **un audit énergétique réglementaire au format PDF** (logiciels rencontrés : LICIEL, Climawin, Pleiades, DPEWIN, ANALYSIMMO ; structure de l'arrêté du 4 mai 2022). Il fait une **extraction par règles (regex), sans IA**, puis laisse l'utilisateur corriger à la main. Il extrait :

**Bâtiment** : adresse, bénéficiaire / propriétaire, surface de référence (m²), nombre de logements, date de visite, CEP initial (kWhEP/m²/an), CEF initial (kWhEF/m²/an), étiquette DPE initiale (lettre lue dans le texte, sinon **déduite du seul CEP** avec les seuils 70/110/180/250/330/420 ; la note GES n'est PAS extraite), mention éventuelle « audit non réglementaire ».

**Auditeur** : raison sociale, SIREN, date d'établissement de l'audit, référence / n° d'audit, logiciel utilisé et version.

**Scénarios de travaux** (un audit en contient souvent 2 : « rénovation en une fois » et « rénovation par étapes »), chacun avec une ou plusieurs **étapes**. Pour chaque étape : CEP et CEF après travaux, % d'économie d'énergie, étiquette après travaux (lue ou déduite du CEP), et la liste des **postes de travaux**.

**Postes de travaux reconnus** : murs, planchers bas, toiture / combles, menuiseries (portes et fenêtres), ventilation, chauffage, eau chaude sanitaire. Pour chacun : nature des travaux (phrase courte), caractéristiques techniques extraites (R en m².K/W, épaisseur, Uw, Sw, COP/SCOP, volume de ballon…) et quantité (m² ou nombre d'unités).

**Contrôles déjà codés** (incohérences internes uniquement, AUCUNE règle d'éligibilité CEE) : audit déclaré non réglementaire, CEP après ≥ CEP avant, économie annoncée incohérente avec le CEP, étiquette incohérente avec le CEP, SIREN invalide, champs manquants, scénario sans travaux, quantité manquante sur un poste d'isolation ou de menuiserie. Il calcule aussi le nombre de classes DPE gagnées.

**Sorties** : (a) un Excel « Liste des travaux et entreprises » par scénario (travaux préconisés / travaux réalisés), (b) un PDF récapitulatif pour le bailleur avec fiche de travaux à compléter.

**Ce qui manque et que tes règles doivent combler** : toutes les règles d'éligibilité et de calcul de la fiche TH-177, aujourd'hui absentes du logiciel.

# Ce que je te demande de produire

Un **document Markdown unique, long et structuré** (si ta réponse est trop longue, découpe en parties numérotées « Partie 1/N… » et je te dirai « continue »). Couvre **chacun** des chapitres ci-dessous. Si un chapitre ne s'applique pas ou si tu ne sais pas, écris-le explicitement.

## 0. Identification de la fiche
- Intitulé exact, code exact (confirme que « TH-177 » est le bon code, ou corrige-moi), secteur (maison individuelle / résidentiel collectif / tertiaire), type de bénéficiaire visé.
- Arrêté de création, arrêtés modificatifs successifs, **dates d'entrée en vigueur** et **dates de fin de validité**, périodes de transition, version actuellement applicable aujourd'hui.
- Pour chaque règle ci-dessous : **à quelle période (date d'engagement ou de fin de travaux) elle s'applique**, car les règles ont changé dans le temps.

## 1. Conditions d'éligibilité du bâtiment et du bénéficiaire
Type de bâtiment, usage, ancienneté minimale, nombre de logements ou surface min/max, zone climatique, énergie de chauffage avant travaux, statut du demandeur (bailleur social, copropriété, propriétaire occupant…), situation de précarité éventuelle, bâtiments exclus, cas des bâtiments déjà rénovés.

## 2. Exigences sur l'audit énergétique
Obligatoire ou non, **qui** peut le réaliser (qualification, RGE, indépendance vis-à-vis de l'entreprise de travaux), **contenu minimal**, audit **réglementaire vs non réglementaire** (conséquences exactes), **validité** (durée, date de visite, date d'établissement), nombre et type de scénarios exigés, **scénario « en une fois » vs « par étapes »** (règles propres à chacun), nombre d'étapes maximal, délai maximal entre étapes, logiciels / moteurs de calcul acceptés, mentions obligatoires, signature.

## 3. Exigences de performance
- Gain de classes DPE exigé, étiquette finale minimale, rôle du CEP **et** de la note GES (laquelle fixe l'étiquette), seuils chiffrés, % de gain énergétique, consommation finale maximale, exigences par énergie.
- Exigences **par étape** dans une rénovation par étapes.
- Comment est calculée / contrôlée l'étiquette avant et après (méthode 3CL-DPE, version, arrondis).
- Exclusions liées aux énergies fossiles (chaudière fioul / gaz / charbon avant ou après travaux), raccordement réseau de chaleur, pompe à chaleur, etc.

## 4. Travaux : obligatoires, interdits, conditions techniques
Pour chaque poste (murs, planchers bas, toiture / combles, menuiseries, ventilation, chauffage, eau chaude sanitaire, éclairage, autres) :
- travail **obligatoire / facultatif / interdit**, nombre minimal de postes d'isolation, combinaisons exigées ;
- **caractéristiques minimales** : résistance thermique R, Uw, Sw, COP / SCOP / ETAS, classe d'efficacité, type de ventilation, labels, certifications, marquage CE, ACERMI, Qualit'EnR, etc. avec **valeurs chiffrées et unités** ;
- règles sur la **surface** ou la quantité traitée (proportion minimale du bâtiment isolée…) ;
- les **travaux induits** et leur statut ;
- ce qui est **non éligible** même s'il figure dans l'audit.

## 5. Calcul du volume de CEE (montant en kWh cumac)
- **Formule exacte** et toutes les variables (surface, nombre de logements, zone climatique, classe avant / après, énergie de chauffage, facteur correctif…).
- Tous les **tableaux de valeurs / forfaits** (par zone climatique, par saut de classe, par type de bâtiment…), **colonne par colonne**.
- Bonifications / coups de pouce applicables, conditions et cumuls, majorations pour précarité ou bailleur social.
- **Au moins 3 exemples chiffrés complets**, du bâtiment aux kWh cumac, avec le détail de chaque étape de calcul.

## 6. Pièces du dossier et mentions obligatoires
Liste exhaustive des documents (audit, devis, factures, attestation sur l'honneur, preuves d'engagement, certificats, photos, etc.), **mentions obligatoires** sur chacun, **cohérence exigée entre les pièces** (noms, adresses, dates, montants, références), signatures, délais de conservation, ce qui est exigé du bénéficiaire et du professionnel.

## 7. Dates et délais
Date d'engagement (qu'est-ce qui la fixe ?), date de fin de travaux, ordre chronologique obligatoire des événements (audit → devis → engagement → travaux → facture), **délais maximaux** (audit avant engagement, durée des travaux, délai de dépôt après fin de travaux), règles d'antériorité, conséquences d'un dépassement, règles spécifiques en rénovation par étapes.

## 8. Rôle actif et incitatif, cumul d'aides, contrôles
Rôle actif et incitatif : définition et preuves. Cumul avec MaPrimeRénov', aides locales, éco-PTZ, autres fiches CEE (lesquelles sont incompatibles ?). Contrôles réalisés (sur site, sur pièces), taux et motifs de contrôle.

## 9. Cas particuliers et ambiguïtés
Copropriétés, bâtiments mixtes, logements vacants, extensions, bâtiments partiellement traités, changement d'énergie, travaux démarrés avant l'audit, scénarios multiples, tout ce qui est **flou ou sujet à interprétation**. Indique l'interprétation retenue par l'administration (PNCEE) quand tu la connais.

## 10. Motifs de refus et erreurs fréquentes
Liste des **motifs de rejet / non-conformité les plus courants** pour cette fiche, classés par fréquence ou gravité si tu peux, avec ce qui les provoque et comment les détecter en amont.

## 11. Règles TESTABLES par le logiciel (section essentielle)
Reformule **toutes** les règles précédentes sous forme de **règles automatisables**. Pour chaque règle, fournis dans un tableau :
`ID | Énoncé court | Source (texte, article, version, date) | Période d'application | Gravité (BLOQUANT / ALERTE / INFO) | Données d'entrée nécessaires | Test (formule ou pseudo-code non ambigu) | Message à afficher à l'utilisateur`
Puis fournis **le même jeu de règles en YAML**, directement exploitable en code.

## 12. Données à extraire de l'audit et à saisir
Déduis de tes règles la **liste complète des champs** dont le logiciel a besoin (en plus de ceux que je liste plus haut) : pour chacun, nom, type, unité, où le trouver dans un audit, s'il est dans l'audit ou à saisir à part. Signale en particulier ce qui n'est **pas** dans un audit classique (ex. note GES, énergie de chauffage avant travaux, zone climatique, dates d'engagement, qualifications, devis).

## 13. Export Excel pour traiter le dossier
Si tu connais les informations demandées par les plateformes de dépôt (par exemple celles des obligés / mandataires type EDF-ODICEE, ou le portail de l'administration) pour déposer un dossier de cette fiche : liste les **champs et pièces exigés**, dans l'ordre, avec les formats attendus. **Indique clairement ce dont tu es sûr et ce que tu supposes.** Je te donnerai ensuite le format exact de mon export.

## 14. Jeux d'essai
Fournis **au moins 5 cas de test** (2 conformes, 3 non conformes pour des raisons différentes) décrits par leurs données d'entrée et le résultat attendu règle par règle, pour que je puisse vérifier mon logiciel.

# Règles de fond (très importantes)

1. **N'invente rien.** Si tu n'es pas certain d'un chiffre, d'un seuil, d'une date ou d'un article, écris « **JE NE SAIS PAS** » ou « **À VÉRIFIER** » plutôt que de deviner. Une valeur fausse est pire qu'une valeur manquante.
2. Pour chaque fait important, indique ton **niveau de confiance** (certain / probable / incertain) et la **source** : texte officiel (arrêté, article, version et date), site du ministère, PNCEE, Légifrance, ou « mémoire non sourcée ». Fournis les liens quand tu les as.
3. **Distingue clairement** : (a) ce que dit le texte officiel, (b) la pratique des obligés ou des instructeurs, (c) ton interprétation.
4. Précise systématiquement la **période de validité** de chaque règle ; signale tout ce qui a **changé récemment** et ce qui est **annoncé** pour bientôt.
5. **Cite les seuils, formules et tableaux en entier**, sans les résumer ni écrire « etc. ». Je préfère un document trop long qu'incomplet.
6. Si ma description de l'outil laisse croire à une erreur sur la fiche (mauvais code, mauvais secteur, hypothèse fausse), **dis-le-moi d'abord**, avant de rédiger.
7. Termine par une section « **Ce que tu n'as pas pu couvrir ou dont tu doutes** » et une liste de **questions** que tu aurais besoin de me poser pour affiner les règles.

Commence par me confirmer en quelques lignes ce que tu comprends de la fiche TH-177 (code, intitulé, secteur, version applicable) et de mon outil, puis rédige le document complet.

=== FIN DU PROMPT ===
