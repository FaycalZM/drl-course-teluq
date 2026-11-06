---
title: "Semaine 13 : Modèles du monde et RL hors ligne"
weight: 13
bookCollapseSection: true
---

# Semaine 13 : Modèles du monde et RL hors ligne

Pendant douze semaines, nos agents ont appris en agissant : pour savoir qu'une action mène à une catastrophe, il fallait la jouer. Cette semaine retire l'interaction, deux fois et dans deux sens différents. D'abord l'agent apprend un modèle du monde et fait son anticipation **dedans**, ce qui fait passer un même résultat de cent mille épisodes à quelques centaines ; le planificateur de cette architecture est, après dix semaines d'absence, la **méthode d'entropie croisée de la semaine 3**. Puis la semaine franchit une bascule : cesser de replanifier, et apprendre une politique à l'intérieur de trajectoires imaginées, avec un gradient qui traverse la dynamique apprise. Enfin elle supprime la collecte elle-même : un jeu de données figé, produit par quelqu'un d'autre, auquel on n'ajoutera jamais rien, et la rencontre avec le problème qui définit tout un sous-domaine, celui d'une erreur qui **grandit** parce que l'optimiseur la cherche. La semaine ne porte aucun jalon.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** apprendre un modèle permet de remplacer l'interaction par du calcul, à condition de mettre la dynamique dans un espace latent avec un chemin déterministe pour la mémoire et un chemin stochastique pour l'incertitude ; et dès qu'on retire la collecte, un optimiseur branché sur un estimateur que rien ne contredit hors des données devient une recherche de ses propres erreurs, ce qui fait croître l'erreur au lieu de la diluer et ce qu'aucune quantité de données supplémentaires ne corrige.

---
## Description générale

La semaine commence par du vocabulaire, et ce n'est pas une formalité. Trois régimes de collecte se distinguent par une seule question, qui collecte et quand : sur politique, la politique apprend sur ses propres données et les jette ; hors politique avec tampon vivant, les données s'accumulent et chaque nouvelle politique en ajoute ; hors ligne, le jeu de données est collecté une fois, par une politique de comportement possiblement inconnue, jamais modifié, et l'entraînement n'interagit pas du tout avec l'environnement. « Hors politique » et « hors ligne » ne sont donc pas synonymes : le premier qualifie un algorithme, le second énonce un problème. Et le jeu de données figé porte le même symbole que le tampon de rejeu de la semaine 5, délibérément, parce que l'identité du symbole est la leçon : même contenu, même code, et une boucle d'alimentation coupée.

La première moitié apprend un modèle du monde. Elle part de quatre difficultés nommées, dont les deux dernières sont celles qui mordent, puisqu'elles sont exploitées par l'optimiseur qu'on branche derrière : un modèle qui échoue à représenter plusieurs futurs, et un modèle trop confiant hors de sa distribution d'entraînement. Trois arguments justifient d'essayer malgré tout, dont le principal est l'efficacité en échantillons, parce qu'un modèle est entraîné sur un signal beaucoup plus riche qu'une valeur et que les récompenses n'ont plus besoin d'être propagées par des remontées de Bellman.

La dynamique est apprise dans un espace latent de dimension trente, et non dans l'espace des images, pour une raison de coût autant que de principe. Vient alors l'argument le plus élégant de la semaine, qui tient en deux refus et une réconciliation : un chemin purement déterministe ne peut représenter qu'un seul futur et se fait exploiter par le planificateur, un chemin purement stochastique ne retient rien sur plusieurs pas, et l'état du modèle est donc scindé en deux parts qui avancent ensemble. La semaine enseigne la réserve honnête qui accompagne cet argument, à savoir qu'un modèle purement stochastique pourrait en principe annuler certaines variances mais que l'optimisation ne trouve pas cette solution, et elle ferme le débat par l'ablation : sans la part stochastique, l'agent n'apprend pas du tout.

L'objectif d'entraînement est une borne variationnelle en deux termes, une reconstruction et une complexité, et la semaine montre que sous des gaussiennes de variance unité la reconstruction se code comme une erreur quadratique moyenne, c'est-à-dire comme du code déjà écrit en semaine 2. Elle insiste sur deux détails de conception qui commandent le reste : l'encodeur filtre et ne lisse pas, parce qu'au moment de planifier il n'y a pas de futur disponible, et toute l'information sur les observations doit passer par son échantillonnage, sans quoi un raccourci déterministe permet de reconstruire sans rien apprendre.

Le planificateur est alors la méthode d'entropie croisée de la semaine 3, et la semaine prend le temps de dire pourquoi une méthode mise de côté comme un jouet convient ici : la dimension du problème a changé de nature, le signal n'est plus rare, et l'évaluation est redevenue bon marché. Elle est employée en commande prédictive, replanifiée à chaque pas, avec une loi sur les suites d'actions remise à zéro après chaque observation pour éviter les optima locaux. Aucune image n'est jamais produite, puisque la récompense est une fonction du latent, et c'est ce qui rend mille candidats abordables. Les résultats suivent : en moins de cent épisodes, un acteur-critique entraîné sur cent mille épisodes depuis l'état proprioceptif est dépassé, et la ligne plafond du tableau, qui est le même planificateur sur le vrai simulateur, se fait battre sur une tâche par le modèle appris, ce qui n'est pas une coquille et que la semaine prend le temps d'expliquer. Le prix est de dix à vingt heures de calcul par tâche.

La bascule arrive ensuite, et elle repose sur deux objections : un horizon fini rend l'agent myope, et une recherche sans dérivée jette un gradient qu'un réseau offre gratuitement. Le même modèle reçoit donc une question nouvelle. Comme la dynamique latente définit un processus de décision complètement observé, tout l'arsenal des semaines 8 à 10 redevient applicable à l'intérieur du modèle : un acteur et un critique sont entraînés sur des trajectoires imaginées, branchées sur des états réels encodés depuis les données. Trois estimateurs de retour imaginé sont donnés, dont le premier ignore tout au-delà de l'horizon et sert d'ablation, et dont le troisième est littéralement le retour \(\lambda\) de la semaine 7 appliqué à des trajectoires qui n'ont jamais eu lieu. Le gradient de l'acteur remonte alors une chaîne dont chaque lien est un réseau, et traverse donc quinze transitions apprises, là où un acteur-critique continu de la semaine 9 ne maximise qu'une valeur d'action immédiate. L'ablation qui porte l'argument n'est pas une courbe d'efficacité en échantillons mais un balayage de l'horizon d'imagination, de dix à quarante, et la semaine explique pourquoi : la thèse à établir est que le critique rend la profondeur inutile, donc il faut faire varier la profondeur.

La seconde moitié retire l'environnement. Le jeu de données devient le jeu d'entraînement de la politique, et le démenti arrive dans le même paragraphe : la politique sera jugée sur ce qu'elle obtient en interagissant réellement. On entraîne comme un apprentissage supervisé et on juge comme un apprentissage par renforcement. La recette qui semble suffire tient en deux modifications du code de la semaine 5, préremplir le tampon et supprimer la collecte, et la semaine montre que ce code tourne, que sa perte descend, et que la politique obtenue peut être arbitrairement mauvaise.

Un argument quantitatif précède le diagnostic : même en donnant l'action optimale en chaque état du jeu de données, apprendre sur la distribution de quelqu'un d'autre coûte une erreur en \(H^2\) au lieu de \(H\), et le mécanisme du carré vaut mieux que la borne, puisqu'il compte \(H\) occasions d'entrer hors distribution coûtant chacune \(O(H)\) erreurs. La semaine garde la réserve qui va avec : cet argument porte sur le clonage de comportement et non sur l'apprentissage par renforcement hors ligne.

Puis vient le centre de la semaine. Il y a deux décalages de distribution et un seul tue. Celui des états agit au déploiement et se borne, au moins en principe. Celui des actions agit pendant l'entraînement, parce que la cible de Bellman exige la valeur d'une action tirée dans la politique apprise et non dans les données. Et l'erreur grandit en trois temps : la cible dépend de valeurs hors distribution qui peuvent être très fausses ; la politique est explicitement optimisée pour maximiser cette quantité, donc elle apprend à aller là où l'estimation est erronément grande ; et en ligne cela se corrige dès qu'on essaie, alors que hors ligne aucune correction n'est possible et que les erreurs s'accumulent à chaque itération. La semaine résume cela en une phrase qu'elle propose de retenir : un optimiseur est une recherche des erreurs de son propre estimateur. La mesure qui doit inquiéter est une courbe de désapprentissage où le retour monte puis s'effondre tandis que la valeur estimée grimpe, et où multiplier les données par mille ne change rien, ce qui distingue le phénomène d'un surapprentissage statistique.

Deux familles de réponses ferment la semaine, et elles diffèrent par ce qu'elles exigent de savoir. Contraindre la politique ferme la faille à la source mais demande de connaître la politique de comportement ; la semaine montre qu'une contrainte de divergence de Kullback-Leibler est le mauvais outil, avec un contre-exemple limpide où la politique de comportement est uniforme, et que la bonne notion est le support et non la densité. Pessimiser la valeur n'exige aucune connaissance de la politique de comportement et s'applique même sans politique explicite ; son intuition est un ancrage, puisque l'erreur de Bellman tient les valeurs des actions présentes dans les données et que la pénalité ne peut donc rabaisser que ce qui n'est tenu par rien. Ses deux limites sont nommées : une pessimisation est d'autant plus coûteuse qu'elle est nécessaire, et l'accumulation d'erreur en \(H^2\) est inévitable dans le pire cas.

La semaine se termine sur le pont qu'elle ne franchit pas, l'apprentissage hors ligne avec modèle, où le même mécanisme se déplace de la valeur d'action vers la transition : c'est la troisième apparition du même phénomène en une seule semaine, et la défense est à chaque fois la même, des déroulements courts branchés sur des états que les données contiennent. Et elle répond en terminant à l'objection qu'un lecteur attentif aura formée, en expliquant par quel mécanisme une politique peut dépasser les données qui l'ont entraînée : la recomposition de morceaux de trajectoires, que la remontée de Bellman effectue sans se préoccuper de savoir qui a produit chaque morceau.

---
## Mots-clés de la semaine

interaction comme ressource rare · régime sur politique · régime hors politique à tampon vivant · régime hors ligne · apprentissage par renforcement hors ligne · politique de comportement · jeu de données figé · modèle du monde · processus de décision markovien partiellement observable · état latent · dynamique latente · modèle à espace d'états récurrent · chemin déterministe · chemin stochastique · encodeur · modèle d'observation · modèle de récompense · borne variationnelle · terme de reconstruction · terme de complexité · nats libres · loi de filtrage · raccourci déterministe · méthode d'entropie croisée · commande prédictive · horizon de planification · loi sur les suites d'actions · élites · répétition d'action · boucle de collecte · épisodes d'amorçage · ligne plafond · efficacité en échantillons · horizon d'imagination · trajectoire imaginée · acteur · critique · reparamétrisation · gradient analytique · gradient à travers la dynamique · modèle gelé · retour \(\lambda\) sur trajectoires imaginées · estimateur sans valeur · balayage d'horizon · gradient traversant · prédiction du facteur d'actualisation · requête contrefactuelle · clonage de comportement · décalage de distribution · décalage des états · décalage des actions · action hors distribution · erreur d'extrapolation · erreur qui grandit · désapprentissage · triade fatale poussée à la limite · contrainte de politique · pénalité de politique · divergence de Kullback-Leibler inadaptée · régression supervisée pondérée · contrainte de support · métrique de probabilité intégrale · pénalité conservatrice · ancrage par l'erreur de Bellman · log-somme-exponentielle · borne inférieure en espérance · pessimisme · exploitation du modèle · déroulement court · recomposition de trajectoires

---
## En prévision de la semaine suivante

La semaine 13 a retiré l'interaction, et elle l'a fait sans jamais toucher à la récompense : elle est restée exactement ce que la semaine 1 avait posé, un nombre fourni par l'environnement, pris pour acquis. La semaine 14 s'attaque précisément à cette hypothèse, qui est la dernière grande hypothèse de ce cours à n'avoir jamais été discutée : **d'où vient la récompense, et que se passe-t-il quand personne ne sait l'écrire ?** Vous verrez ce qu'un agent fait d'une récompense mal spécifiée, et la réponse est instructive : il l'optimise parfaitement, ce qui est le problème. Et vous verrez comment on construit un signal d'apprentissage à partir de **jugements humains** plutôt que d'une formule.

Deux choses de cette semaine vous y serviront directement. La première est le réflexe de la section 13.12 : demander toujours qui a produit les données sur lesquelles un chiffre est calculé. La seconde est le mécanisme de la section 13.14, et vous allez le retrouver sous un autre nom : un optimiseur branché sur un estimateur que rien ne contredit trouve les erreurs de cet estimateur. Remplacez « estimateur de valeur » par « modèle de la préférence humaine », et vous avez l'essentiel du problème de la semaine 14 avant même de l'ouvrir.

Et le **jalon 4** s'y rattache. La section 13.16 vous a donné le lien : les données que votre projet a collectées constituent un jeu de données figé, et toute évaluation d'une politique sur elles est un problème hors ligne. Relisez vos propres mesures des semaines précédentes avec cette grille, et notez celles dont vous ne pourriez plus défendre le protocole.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 14{{% /comment %}}

{{% comment %}}
Pagination : indices PDF, SANS décalage (D35). Les trois sources de la semaine sont des
prépublications arXiv, dont le numéro imprimé est égal à l'indice PDF, contrairement à LAPAN
(imprimé = PDF moins 31) et à SUTTON & BARTO. Aucune conversion n'a été faite ni n'est à faire.

PREMIÈRE SEMAINE SANS AUCUN CHAPITRE DE MANUEL. Trois articles, et rien d'autre. Passe de
lecture mesurée : 12 chunks (dont deux partiels) plus trois résumés d'article, soit environ
31 500 jetons, plus environ 9 000 jetons de LaTeX lus sous source-assets/papers/tex/ (D44),
pour un total d'environ 40 000, au plafond de D41. Le LaTeX n'était pas optionnel : TOUTES les
équations de la semaine en sont recopiées, aucune n'est reprise d'un chunk, et l'extraction de
ces trois documents est justement endommagée aux endroits qui comptent (fractions, indices,
bornes de sommation). Détail complet dans index/notes/week-13.md.

PREMIÈRE SOURCE (PLANET, arXiv 1811.04551) : porte les sections 13.2 à 13.7.
- p.1 : les quatre difficultés d'un apprentissage de dynamique (§13.2), les trois bénéfices
  d'un modèle (§13.2), et l'état antérieur de la question (§13.2).
- p.2 : le PDM partiellement observable, éq. 1 (§13.3, 13-E1) ; la boucle de collecte,
  algorithme 1 (§13.6, 13-E7), dont la sommation des récompenses répétées et le compte en
  plafond de T sur la répétition d'action.
- p.3 : le modèle latent, éq. 2 (§13.3, 13-E2) ; le modèle d'observation qui entraîne mais ne
  planifie pas, et l'absence de réseau de politique et de valeur (§13.3) ; la distinction
  typographique entre vraie dynamique et modèle appris, que la page rend par un indice de
  paramètres (§13.3) ; les trois gaussiennes et l'équivalence vraisemblance-EQM (§13.4) ; la
  loi de filtrage contre la loi de lissage (§13.4) ; CEM, sa robustesse, le fait qu'elle
  résout toutes les tâches sur la vraie dynamique, la commande prédictive, la réinitialisation
  de la loi, une trajectoire par candidat et l'absence de génération d'image (§13.5).
- p.4 : la borne variationnelle, éq. 3 (§13.4, 13-E5) ; le modèle scindé, éq. 4 (§13.3,
  13-E4) ; l'argument des deux chemins et sa réserve honnête sur les variances nulles
  (§13.3) ; la contrainte structurelle de l'encodeur (§13.4). Page rasterisée et ouverte
  (index/pages/planet/0004.png) pour vérifier éq. 3, éq. 4 et la structure du graphe.
- p.6-7 : le protocole, les six tâches, les gains d'efficacité, les 26 % sur le guépard, le
  tableau 1 et sa LIGNE PLAFOND, le coût de 10 à 20 heures par tâche (§13.7) ; l'ablation des
  deux parts du modèle, dont « sans la part stochastique l'agent n'apprend pas » et les deux
  explications candidates (§13.3).
- p.8 : l'ablation de conception (collecte en ligne, CEM itératif contre tirage brut) et la
  phrase de travaux futurs qui annonce la seconde moitié de la semaine (§13.7).
- p.12-13 : tous les hyperparamètres, les nats libres, la répétition d'action par domaine
  (§13.5, §13.6) ; l'agent unique sur six tâches (§13.7).
- NON LU et exclu volontairement : planet/03 (dépassement latent, un régulateur que l'agent
  final n'emploie pas), planet/05 et planet/06 (bibliographie).

DEUXIÈME SOURCE (DREAMER, arXiv 1912.01603) : porte les sections 13.8 à 13.11.
- FRONTIÈRE AVEC LA PREMIÈRE SOURCE, vérifiée et tenue : le modèle du monde, la scission, la
  borne variationnelle, les nats libres, la boucle de collecte, la répétition d'action,
  l'argument « imaginer sans décoder », CEM et le banc d'essai appartiennent à la PREMIÈRE
  source et ne sont enseignés QU'UNE FOIS (§13.3 à §13.7). La seconde les réemploie sans les
  modifier et le dit explicitement (p.6). §13.8 ouvre en le disant au lecteur.
- p.1-2 : les deux objections (horizon fini, optimisation sans dérivée sur une dynamique
  dérivable) et les trois composantes d'un agent (§13.8).
- p.3 : le PDM imaginé est complètement observé, les trajectoires branchées sur des états
  réels, et la forme d'une itération en six lignes (§13.9).
- p.4 : acteur et valeur, éq. 2 (13-E8) ; action reparamétrée, éq. 3 (13-E9) ; les trois
  estimateurs, éq. 4, 5 et 6 (13-E10, 13-E11, 13-E12) ; le BALAYAGE D'HORIZON, qui est
  l'ablation portant l'argument et non une courbe d'efficacité (§13.10, §13.11).
- p.5 : objectifs de l'acteur et du critique, éq. 7 et 8 (13-E13, 13-E14) ; la chaîne de
  dépendances et le gradient analytique ; le contraste à trois familles avec les semaines 8
  à 11 ; le modèle GELÉ pendant l'apprentissage du comportement ; gradient traversant et
  prédiction du facteur d'actualisation (§13.11).
- p.5-7 : la comparaison à trois objectifs de représentation. DÉCISION D'ENSEIGNEMENT : deux
  phrases et AUCUNE équation (§13.11), conformément à l'arbitrage de la passe de lecture. Son
  annexe B (le goulot d'étranglement informationnel) n'a pas été lue, seul son verdict.
- p.7-9 : les comportements à courte vue sans valeur, le score moyen de 823 après 5 millions
  de pas, les coûts horaires (§13.11).
- p.16 : la limite honnête sur les jeux à actions discrètes et les environnements 3D, reprise
  telle quelle et non décorée (§13.11).
- DEUX ERREURS D'AUTEUR VÉRIFIÉES SUR LE LaTeX ET NON REPRODUITES : la section de résultats
  écrit « all 19 tasks » dans une phrase qui dit aussi « 16 of 20 tasks, with 4 ties » alors
  que l'article annonce 20 tâches (la page écrit 20, le chiffre de référence, et ne cite
  aucun des deux comptes) ; et deux budgets de pas différents apparaissent pour les mêmes
  références entre une légende et des légendes internes de figures (la page retient 10^8,
  soutenu par le tableau de résultats). Une troisième, une information mutuelle écrite avec
  une virgule au lieu d'un point-virgule, ne concerne qu'une équation que la semaine
  n'enseigne pas.
- NON LU : related work, conclusion, références, et cinq annexes.

TROISIÈME SOURCE (OFFLINE, arXiv 2005.01643) : porte l'introduction et les sections 13.1,
13.12 à 13.16. C'est une revue de domaine, et le résumé d'article a servi de niveau de lecture
pour tout ce que les chunks ci-dessous ne couvrent pas.
- p.2 et p.7-8 : les trois régimes de collecte (§13.1, figure 13-04) ; le terme parapluie
  « hors politique » et le qualificatif qu'il a fallu lui ajouter ; le rejet du vocabulaire
  par lots et la raison de ce rejet (§13.1) ; la définition hors ligne en quatre conditions,
  l'analogie du jeu d'entraînement et son démenti, la loi des données (§13.12) ; la recette
  « préremplir le tampon, mettre la collecte à zéro » et la phrase « toutes ces méthodes ne
  sont pas efficaces », qui est la charnière de la seconde moitié (§13.12).
- p.5 : l'équation de Bellman pour une politique, éq. 3 (§13.12, 13-E23), posée comme la
  cible que toute la seconde moitié attaque.
- p.9-10 : l'exploration mise hors sujet et l'hypothèse de couverture, dont la note de bas de
  page admettant que sa formalisation est un problème ouvert ; les requêtes
  contrefactuelles ; théorèmes 2.1 et 2.2 (13-E15, 13-E16) et le MÉCANISME du carré, qui est
  ce que la page enseigne plutôt que la borne ; la réserve des auteurs eux-mêmes, à savoir
  que l'exemple porte sur le clonage de comportement (§13.13).
- p.18-19 : les deux décalages ; la borne d'état (13-E3) et le fait qu'elle est très lâche ;
  le décalage des actions, qui agit pendant l'entraînement ; la CHAÎNE EN TROIS TEMPS de la
  croissance de l'erreur, dont « la politique est explicitement optimisée pour maximiser la
  quantité fautive » ; la courbe de désapprentissage et le fait que mille fois plus de
  données n'y change rien ; les trois formulations du même obstacle (§13.14).
- p.19-24 : la famille des contraintes de politique, la remarque structurelle sur la seule
  entrée hors distribution, les deux axes de conception, la paire contrainte et la paire à
  pénalité (13-E17, 13-E18), la f-divergence (13-E19) et sa faiblesse, la forme implicite et
  sa régression pondérée, la CRITIQUE DE LA DIVERGENCE KL avec le contre-exemple de la
  politique uniforme, la contrainte de SUPPORT (13-E20) et l'inadaptation des f-divergences à
  une comparaison de supports, les métriques de probabilité intégrales en une phrase ; puis
  la famille conservatrice, l'objectif modifié et les trois pénalités (13-E21a, 13-E21b,
  13-E21c), l'ARGUMENT D'ANCRAGE, la lecture de la log-somme-exponentielle, et les deux
  limites (§13.15).
- p.26-29 : l'exploitation du modèle en régime hors ligne, la borne (13-E22) et sa lecture,
  les déroulements courts branchés sur des états des données, et la recomposition de
  trajectoires avec le nom du banc d'essai (§13.16).
- UN PASSAGE N'EST JAMAIS CITÉ : à la p.22 du chunk offline/17, une légende de figure est
  entrelacée colonne par colonne avec le corps du texte, ce qui produit une phrase
  inintelligible. La phrase correcte a été lue dans main.tex l.776 et c'est elle qui est
  rendue en §13.15. La passe de lecture l'a signalé ; la rédaction ne s'en est pas approchée.
- UNE ERREUR D'AUTEUR CORRIGÉE DANS LA PAGE, et elle est dans leur propre LaTeX (l.668) : les
  états hors distribution au moment du test y sont écrits sous la distribution de la
  politique de COMPORTEMENT, alors que le sens exige celle de la politique APPRISE. §13.14
  écrit la version correcte et signale au lecteur, sans nommer de source, que la forme
  inverse circule.
- NON LU, environ 52 000 jetons : la moitié évaluation de la revue (échantillonnage
  préférentiel, gradient hors politique, échantillonnage préférentiel marginalisé), ses
  applications, ses références, et sa section sur l'apprentissage hors ligne AVEC modèle. Ce
  dernier point est le pont de §13.16 : la section n'avance donc rien au-delà de 13-E22 et
  des deux paragraphes qui l'entourent, qui ont été lus dans main.tex l.848-858.

NOTATION. La semaine a exigé une section entière de notation.md (§3 ter), écrite AVANT la
rédaction : le latent est Z_t et non s_t, l'encodeur est e_theta parce que q est une valeur
d'action dans ce cours, l'acteur est pi_phi et le critique v_psi, la semaine déclare DEUX
distributions d'états (d^pi et d^D, la seconde étant une création du cours), le temps imaginé
s'écrit k parce que tau porte déjà deux sens (semaines 9 et 12), AUCUN R nu n'est écrit parce
que les deux premières sources l'emploient pour la répétition d'action, l'adversaire de la
pénalité conservatrice est renommé nu, et alpha, beta, epsilon sont indicés. La page déclare
les six collisions dans son introduction, avant la première équation concernée, et D garde son
symbole de la semaine 5 DÉLIBÉRÉMENT, parce que l'identité du symbole est la leçon. Deux
permutations de lettres sont imposées par ces règles et signalées dans la page : l'indice de
temps imaginé passe de tau à k, et l'exposant du nombre de pas avant amorçage passe de k à n.

FIGURES. Quatre identifiants, QUATRE dessins du cours, AUCUNE extraction. Les trois sources
sont des prépublications arXiv sans licence ouverte : la redistribution de l'article est
accordée, la republication de ses figures dans un cours ne l'est pas. C'est la position que la
semaine 9 a établie et que le dossier a reconfirmée le 06/11 pour les trois sources, en
surchargeant la recommandation d'un résumé d'article qui proposait d'extraire une figure.
13-01 (les deux chemins) redessine un argument dont la passe de lecture a relevé la structure
de graphe nœud par nœud, de sorte que le dessin n'a jamais besoin d'ouvrir la source. 13-02
(planifier contre apprendre un comportement) et 13-03 (le décalage de distribution) sont des
dessins dont aucune source ne donne l'équivalent. 13-04 (les trois régimes) est le quatrième
dessin que le dossier laissait à la passe de rédaction, et la rédaction LE RETIENT, parce que
la confusion entre hors politique et hors ligne est la première cause de contresens sur la
semaine et qu'un schéma la lève plus vite qu'un paragraphe. Inventaire complet et
spécifications de dessin dans extraction/week-13.md.

LABORATOIRE. Quatre volets, aucun exécuté par ce cours, et la page le dit. Rien de ce que la
semaine décrit n'est reproductible (10 à 20 h par tâche pour la première source, environ 15 h
par tâche et par graine pour la seconde, et deux bases de code dans un cadriciel qui ne
s'installe plus ; D15 impose de toute façon une réécriture). Les quatre volets ont chacun leur
ancrage : les trois estimateurs sont autonomes et ne demandent aucun modèle ; CEM sur une
dynamique ANALYTIQUE reproduit la forme de la ligne plafond du tableau de la première source,
qui est exactement CEM sur la vraie dynamique avec zéro épisode, et prolonge la semaine 3 ;
l'acteur reparamétré démontre l'existence d'un chemin de dérivation et la page dit qu'il ne
démontre rien de plus ; et la politique hors ligne sur jeu figé s'appuie sur deux ancrages,
la recette « préremplir et mettre la collecte à zéro » (p.8) et l'axe des abscisses de la
courbe de désapprentissage, qui va de 0 à 1 000 pas de gradient (p.19), soit des minutes.
LA SOLUTION COURTE N'EST PAS UNE BIBLIOTHÈQUE, et la page donne la raison : les bibliothèques
de ce cours sont bâties autour d'une boucle qui collecte, ce que la seconde moitié interdit.
Elle est remplacée par un CLONAGE DE COMPORTEMENT sur le même jeu figé, qui est le plancher
pertinent et qui est par ailleurs l'objet du théorème 2.1 de la troisième source.

PAS DE JALON CETTE SEMAINE (COURSE-PLAN §10). La page d'accueil est rédigée ici (D47) et la
semaine n'écrit PAS de conclusion séparée, afin qu'aucun des deux textes ne reste non publié.
Le lien avec le jalon 4 est nommé deux fois, en introduction et en §13.16 : les données déjà
collectées par le projet constituent un jeu figé, et évaluer une politique sur elles est un
problème hors ligne. La projection vers la semaine 14 annonce la question de l'origine de la
récompense et le signal construit sur des jugements humains, et NE DÉPENSE PAS cette
semaine-là : aucun modèle de préférence n'est décrit, aucun nom de méthode n'est donné, et ni
amodei/* ni pan/* n'ont été lus (DO NOT read du dossier).

DÉCOMPTE : 16 sections numérotées · 4 placeholders FIG (13-01, 13-02, 13-03, 13-04 : quatre
dessins du cours, à produire, aucun extractible pour raison de licence) · 0 placeholder EQ
(25 équations identifiées, 13-E1 à 13-E23 avec 13-E21 en trois parties, TOUTES écrites
directement en KaTeX dans la page, parce que TOUTES ont été recopiées du LaTeX des sources
pendant la passe de lecture, avec fichier et ligne enregistrés, et AUCUNE reprise d'un chunk.
Deux portent une correction de la passe de lecture qui ne doit pas être « rétablie » :
13-E10 ne porte AUCUN facteur d'actualisation, ce qui est sa forme imprimée, et 13-E14 est
imprimée avec une parenthèse fermante non appariée dans sa norme, qui est supprimée. Six
expressions de la troisième source NE PORTENT AUCUN NUMÉRO et sont donc désignées par page et
par contenu, jamais par numéro. L'inventaire complet est dans extraction/week-13.md)
{{% /comment %}}
