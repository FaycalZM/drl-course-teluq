---
title: "Semaine 8 : De REINFORCE à A2C"
weight: 8
bookCollapseSection: true
---

# Semaine 8 : De REINFORCE à A2C

Pendant sept semaines, toutes nos méthodes ont appris un **nombre**, la valeur d'un état ou d'un couple état-action, et en ont déduit un comportement par un \(\argmax\) sur les actions. Cette semaine ouvre le module 3 et change d'objet : la **politique** devient ce que l'on apprend, directement, sous la forme d'un réseau qui produit une distribution de probabilité sur les actions. La valeur ne disparaît pas, elle change de rôle : de but, elle devient outil. Vous verrez pourquoi ce changement est légitime, ce qu'il permet qu'aucune méthode fondée sur la valeur ne permettait, les quatre choses qui se gâtent quand on l'applique naïvement, et l'architecture qui les règle une par une.

> [!IMPORTANT]
 **La valeur cesse d'être ce que l'on apprend et devient ce qui rend supportable l'apprentissage de la politique.**

---
## Description générale

La semaine se lit comme une démonstration en cinq temps, et chaque section sait à quelle question elle répond.

Elle commence par **paramétrer la politique** : un réseau qui produit des préférences, un softmax qui en fait une distribution, et un échantillonnage qui remplace l'\(\argmax\). Cinq avantages justifient ce détour, dont un seul est décisif : il existe des problèmes dont la politique optimale est **stochastique**, et une méthode qui choisit par \(\argmax\) ne peut pas l'écrire, quelle que soit la qualité de son estimation. L'exemple du couloir court le démontre en cinq lignes, avec ses trois nombres.

Vient ensuite la seule mathématique de la semaine, le **théorème du gradient de politique**. Son intérêt n'est pas sa forme mais ce qu'il ne contient pas : aucune dérivée de la dynamique de l'environnement. Deux substitutions, qui sont la même idée appliquée deux fois, le transforment en une quantité estimable à partir d'une trajectoire jouée. **REINFORCE** est ce résultat écrit comme un algorithme, et il résout CartPole en moins de quatre cents épisodes, contre six cent quarante pour la méthode d'entropie croisée de la semaine 3.

La semaine bascule alors sur son point central : **quatre problèmes, chacun nommé**. Les épisodes complets exigés, la variance élevée du gradient, l'exploration qui s'éteint, la corrélation des échantillons. Les quatre sections suivantes y répondent une par une, dans cet ordre. Une **référence** soustraite du retour laisse l'espérance du gradient inchangée, par un argument qui tient en trois égalités, et abaisse sa variance de deux à trois ordres de grandeur. La référence naturelle est la valeur de l'état, ce qui transforme l'échelle du gradient en **avantage** ; et dès que cette valeur **amorce**, elle cesse d'être une référence et devient un **critique**. L'ensemble porte le nom d'**A2C** : un acteur, un critique, un tronc commun, et une perte à trois termes dont le premier n'est pas une erreur, le deuxième en est une, et le troisième est une prime à l'indécision écrite au signe négatif.

Deux franchises, enfin, parce qu'elles sont la vraie matière de la semaine. La quantité minimisée dans le code n'est pas une perte : elle n'a ni cible ni plancher, sa valeur ne renseigne sur rien, et seul son gradient a un sens. Et une méthode de gradient de politique **n'est pas** une amélioration des méthodes de la semaine 6 : elle consomme de l'ordre de dix fois plus d'interactions avec l'environnement, et elle achète en échange une politique stochastique et la porte des actions continues. La semaine se termine sur la comparaison des architectures parallèles, lue et discutée, tandis que le laboratoire construit la version vectorisée, qui obtient la décorrélation sans processus supplémentaire.

La semaine **ouvre le module 3** et ne porte **aucun jalon** : le prochain est en semaine 10.

---
## Mots-clés de la semaine

méthode fondée sur la politique · politique paramétrée · préférence numérique · paramétrisation softmax · sorties brutes · échantillonnage de l'action · représentation lisse · optimum stochastique · couloir court · théorème du gradient de politique · distribution sur politique · mesure de performance · forme échantillonnée · méthode toutes actions · REINFORCE · vecteur d'éligibilité · méthode de Monte-Carlo · perte de politique · signe de la montée de gradient · attribution du mérite · épisodes complets exigés · variance du gradient · exploration insuffisante · corrélation des échantillons · référence · référence dépendante de l'état · avantage · amorçage · acteur · critique · acteur-critique · A2C · tronc commun · deux têtes · erreur de différence temporelle · retour à \(N\) pas · déroulement de l'équation de Bellman · détachement du graphe · écrêtage du gradient · entropie d'une politique · prime d'entropie · coefficient d'entropie · environnements vectorisés · efficacité d'échantillon · sur politique · A3C · parallélisme de données · parallélisme de gradients · divergence de Kullback-Leibler

---
## En prévision de la semaine suivante

La semaine 9 ouvre la porte que celle-ci a seulement montrée : les **espaces d'actions continus**. Rien dans le théorème du gradient de politique n'exigeait que les actions soient énumérables, et c'est la différence décisive avec les méthodes du module 2, qui reposaient toutes sur un \(\max\) ou un \(\argmax\) sur les actions. Vous y remplacerez le softmax sur un ensemble fini par une distribution continue, ce qui demande de paramétrer non plus des probabilités mais les paramètres d'une loi ; vous y verrez les environnements de robotique simulée, où une action est un vecteur de couples articulaires ; et vous y rencontrerez une méthode qui combine une politique déterministe et un critique, ce qui est une troisième façon d'assembler les deux objets de cette semaine.

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF − 31 pour LAPAN et PDF − 22 pour SB,
conformément à MAP-lapan.md et MAP-sb.md, comme dans le dossier et les notes de phase 1.
Toutes les pages citées ci-dessous sont des indices PDF.

SEMAINE À TROIS SOURCES, CHACUNE AVEC UN SEUL MÉTIER, ET LE DOSSIER LE DIT AINSI.
SB ch. 13 fournit la seule mathématique de la semaine (théorème, REINFORCE, référence, pas
acteur-critique) et porte les sections 8.2, 8.6 et 8.7 ; LAPAN ch. 11 et ch. 12 fournissent
l'implémentation, les quatre modes de défaillance et l'architecture qui les répare, et portent
les sections 8.1, 8.3, 8.4, 8.5, 8.8, 8.9, 8.10 et le laboratoire ; la page vpg de Spinning Up
fournit la forme de la boucle, la formule de la montée de gradient et le paragraphe
exploration-exploitation, et intervient en 8.3, 8.5 et 8.7. Aucun nouveau papier.

SB ch. 13 §13.1 « Policy Approximation and its Advantages » (344-346) : exigence de
dérivabilité de pi(a|s,theta) et gradient fini, exigence pratique que la politique ne devienne
jamais déterministe (344) → §8.1 premier paragraphe formel ; paramétrisation par préférences
numériques h(s,a,theta) et softmax, éq. 13.2, préférences par réseau profond ou linéaires en
caractéristiques, éq. 13.3 (344) → §8.1, softmax écrit directement en KaTeX ; AVANTAGE 1,
l'approximation peut approcher le déterminisme, impossibilité pour epsilon-glouton, et le
contre-argument du softmax sur les valeurs d'action qui convergent vers des valeurs distantes
d'une quantité finie (344) → §8.1 avantage 1, repris intégralement ; AVANTAGE 2, probabilités
arbitraires et optimum stochastique, bluff au poker (345) → §8.1 avantage 2 ; EXEMPLE 13.1 LE
COULOIR COURT, trois états non terminaux, récompense −1 par pas, actions inversées dans le
deuxième état, carte de caractéristiques identique pour les trois états, epsilon = 0,1 donnant
pire que −44 (toujours à droite) et pire que −82 (toujours à gauche), meilleure politique
stochastique à p ≈ 0,59 et valeur ≈ −11,6 (345) → §8.1, LES TROIS NOMBRES CONSERVÉS, et c'est
l'argument que le dossier demandait d'utiliser ; AVANTAGES 3 et 4, politique parfois plus simple
à approcher (Tetris cité), paramétrisation comme lieu d'injection de connaissance préalable
(345-346) → §8.1 ; AVANTAGE 5, variation continue des probabilités contre bascule brutale de
l'argmax, et garanties de convergence plus fortes (346) → §8.1 avantage 5.

SB ch. 13 §13.2 « The Policy Gradient Theorem » (346-349) : J(theta) = v_{pi_theta}(s_0),
gamma = 1 dans le texte (346) → §8.2 ; LA DIFFICULTÉ, la performance dépend du choix des
actions ET de la distribution des états, l'effet sur les actions est calculable et l'effet sur
la distribution est une fonction inconnue de l'environnement (346) → §8.2 première
sous-section, reformulée dans les termes du graphe de calcul de la semaine 2 (encadré [!NOTE],
ajout du cours) ; CE QUE LE THÉORÈME DONNE, une expression analytique sans dérivée de la
distribution d'états (348) → §8.2, la phrase autour de laquelle la section est construite ;
preuve encadrée p. 347, calcul élémentaire plus déroulement répété de nabla v_pi, NON
REPRODUITE sur instruction des notes, résumée en une phrase ; propto et non =, constante =
longueur moyenne d'épisode, absorbée dans alpha, égalité dans le cas continu (348) → §8.2 ;
mu = distribution sur politique, le même objet que l'objectif VE de la semaine 5 (348) ;
éq. 13.5 (théorème), 13.6 (somme sur les états devenue espérance), 13.7 (méthode toutes
actions), et la dérivation non numérotée de p. 349 (forme échantillonnée) → EQ 08-E1, 08-E2,
08-E3, 08-E4. LES QUATRE TRANSCRITES DEPUIS L'IMAGE DE PAGE, et E1, E2, E4 reproduites au
caractère près ; E3 écrite en ligne et non affichée, comme les notes le demandaient.

SB ch. 13 §13.3 « REINFORCE: Monte Carlo Policy Gradient » (349-351) : éq. 13.8 et l'identité
nabla ln x = nabla x / x (349) → EQ 08-E5, transcrite de l'image ; lecture intuitive de
l'incrément, proportionnel au retour et inversement proportionnel à la probabilité de l'action
pour que la fréquence de sélection ne décide pas (349) → §8.3, développée en deux paragraphes ;
VECTEUR D'ÉLIGIBILITÉ et le fait qu'il soit le SEUL endroit où la paramétrisation intervient
(349) ; méthode de Monte-Carlo, cas épisodique seulement, mises à jour faites après coup (349) ;
le facteur gamma^t de l'encadré absent de l'éq. 13.8, et l'exercice 13.2 qui demande de les
réconcilier (350) → §8.2 dernière sous-section, CONVENTION TRANCHÉE PAR LE COURS, écrite comme
une décision du cours et non comme un désaccord entre textes (gap 6 des notes) ; convergence
vers un optimum local sous les conditions d'approximation stochastique, et forte variance
(351) → §8.3, la phrase d'avertissement REFORMULÉE en voix du cours (D45).

SB ch. 13 §13.4 « REINFORCE with Baseline » (351-353) : éq. 13.10 (théorème avec référence),
l'égalité en trois temps qui annule le terme soustrait, éq. 13.11 (mise à jour) → EQ 08-E6,
08-E6b, 08-E7, transcrites de l'image ; la référence peut être une variable aléatoire, pourvu
qu'elle ne varie pas avec a (351) ; généralisation stricte de REINFORCE, espérance inchangée et
effet important sur la variance (351) ; pourquoi la référence doit varier avec l'état, états où
toutes les actions valent beaucoup et états où toutes valent peu, le cas du bandit (351) ;
v̂(S_t,w) comme choix naturel, w appris par les méthodes des chapitres précédents (351) ; DEUX
PAS D'APPRENTISSAGE, alpha^theta et alpha^w, le second relativement facile à régler et le
premier « beaucoup moins clair », dépendant de l'amplitude des récompenses et de la
paramétrisation (352) → §8.6 deuxième sous-section ; fig. 13.2, alpha^theta = 2^-9 et
alpha^w = 2^-6 contre REINFORCE à son meilleur pas 2^-13, convergence en ~100 épisodes contre
une montée encore inachevée à 400, référence scalaire v̂(s,w) = w (352-353) → FIG 08-02.

SB ch. 13 §13.5 « Actor-Critic Methods » (353-354) : LA DISTINCTION, REINFORCE avec référence
apprend une politique ET une valeur et n'est PAS une méthode acteur-critique, parce que sa
valeur sert uniquement de référence et jamais d'amorçage ; seul l'amorçage introduit le biais et
la dépendance asymptotique à la qualité de l'approximation (353) → §8.7 troisième sous-section,
la frontière de la semaine ; pourquoi payer ce biais, réduction de variance et accélération,
contre la lenteur, la variance et l'inconfort en ligne de Monte-Carlo (353) → §8.7, rattaché
explicitement à l'arbitrage biais-variance des semaines 4, 6 et 7 (encadré [!NOTE], rapprochement
du cours) ; acteur-critique à un pas comme analogue de TD(0), Sarsa(0) et Q-learning, en ligne et
incrémental, sans traces d'éligibilité (353) ; éq. 13.12, 13.13, 13.14 → EQ 08-E8, 08-E9, 08-E10,
transcrites de l'image et AFFICHÉES EN UNE SEULE CHAÎNE DE TROIS LIGNES, la chute étant
l'apparition de delta_t ; critique par semi-gradient TD(0), traitement en ligne et états jamais
revisités (353) ; généralisations n-pas, lambda-retour, traces séparées, MENTIONNÉES EN UNE
CLAUSE et non enseignées (354) ; facteur I de l'encadré, non imprimé puisque le cours n'imprime
pas l'encadré (354).

LAPAN ch. 11 « Policy Gradients » : valeur centrale dans l'itération de valeur et le Q-learning,
politique obtenue par argmax (330-331) → introduction ; L'ARGUMENT DU TIGRE, l'agent a besoin
d'une décision et non de l'écart de valeur entre fuir et ne rien faire, et le Q-learning répond
indirectement (331) → introduction, REFORMULÉ ; coût de l'argmax avec beaucoup d'actions ou un
espace continu, petite optimisation dans un réseau non linéaire à chaque pas (331) →
introduction, ET C'EST LE SEUL ENDROIT OÙ LES ACTIONS CONTINUES SONT MENTIONNÉES (discipline de
crochet : la semaine 9 garde le sujet) ; convenance aux environnements stochastiques, dans
l'esprit du DQN distributionnel de la semaine 6 (332) ; la méthode d'entropie croisée EST un
gradient de politique avec Q = 1 sur les transitions élites et 0 ailleurs, REINFORCE est la même
chose avec un vrai scalaire (333-334) → introduction, filiation vers la semaine 3 ; fig. 11.1,
le réseau qui sort une distribution (332) → FIG 08-01 ; représentation lisse (332) → §8.1 ;
L = −Q(s,a) log pi(a|s) et le rôle du signe (333) → §8.3 ; recette en six étapes (334) → §8.3
encadré d'algorithme, TRADUIT ; les trois absences, exploration explicite, tampon de rejeu,
réseau cible, avec la note que le réseau cible revient (334) → §8.3 dernière sous-section, la
promesse corrigée (le critique de 8.7 amorce) ; hyperparamètres CartPole GAMMA 0,99, LR 0,01,
4 épisodes par mise à jour, réseau 128 unités (335) → §8.4 ; calc_qvals à rebours (335-336) →
§8.3 fragment de code, RÉÉCRIT (D15) ; logits et log_softmax, softmax jamais dans la passe avant
(335) → §8.1 troisième sous-section ; échantillonnage contre argmax, l'exemple 0,4 / 0,5 (336) →
§8.1 ; la mécanique de la perte ligne par ligne, logits → log_softmax → log-probabilité de
l'action prise → multiplication par l'échelle → moyenne → négation, et « ce signe moins est très
important » (338) → §8.3, REFORMULÉ EN VOIX DU COURS (D45) et étendu par l'ajout pédagogique que
les notes signalaient comme NON CITABLE (gap 1 : aucune source ne dit que le nombre n'est pas une
erreur) ; 67 857 pas et 384 épisodes, arrêt à 450 sur 100 épisodes (338) → §8.4 ; 640 épisodes
pour la méthode d'entropie croisée (341) → §8.4, comparaison avec la semaine 3 ; comparaison avec
le DQN, convergence presque identique puis effondrement au-dessus de 400 (340) → §8.4 ;
comparaison en quatre points des deux familles (341) → §8.4 tableau ; « la perte de politique
montre l'échelle et la direction moyennes du gradient » (348) → §8.3, l'appui du raisonnement de
l'encadré [!WARNING] ; entropie 0,69 → 0,52 et log 2 (348) → §8.9 ; « vérifier la taille relative
des deux » et beta constant ou décroissant linéairement (349) → §8.9, DONNÉ COMME PRATIQUE ET NON
COMME RÈGLE (gap 3 : aucune règle n'existe dans le kit) ; référence attendue à 9,56 et échelles
oscillant autour de zéro (347) → §8.6 encadré [!TIP] et volet A ; divergence KL, pics mauvais
signe, exécution saine sous 1e−3 (346, 349) → laboratoire, diagnostic facultatif, ET CROCHET VERS
LA SEMAINE 10 planté sans être expliqué ; « presque personne n'utilise le gradient de politique
nu » et la raison de le garder (344) → §8.4 encadré [!NOTE], REFORMULÉ.

LAPAN ch. 11 §« REINFORCE issues » (341-344), LE POINT DE BASCULE DE LA SEMAINE : les quatre
problèmes dans l'ordre de la source, épisodes complets exigés, variance élevée du gradient,
problèmes d'exploration, forte corrélation des échantillons → §8.5, CHACUN NOMMÉ ET RELIÉ À LA
SECTION QUI Y RÉPOND par un tableau ; problème 1, attente de la fin de l'épisode, les méthodes
se comportant mieux avec plus d'épisodes, CartPole indulgent et Pong fatal, le but de l'épisode
complet étant une estimation exacte de Q, le DQN remplaçant par Bellman à un pas, l'absence de V
et de Q dans un gradient de politique, et les DEUX SORTIES (estimer V, ou dérouler N pas)
(341-342) ; l'arithmétique 0,9^10 ≈ 0,35 et 0,9^50 ≈ 0,00515 (342) → §8.5 ; problème 2,
l'échelle dépendante de l'environnement, 5 pas contre 100 pas soit un facteur 20, un épisode
chanceux dominant le gradient, et les trois candidats de référence (342-343) ; problème 3,
convergence vers un optimum local, epsilon-glouton possible mais la prime d'entropie meilleure,
H(pi) = −somme pi log pi, maximum pour l'uniforme, soustraction de la perte qui punit la
certitude (343) → §8.5 et §8.9 ; problème 4, corrélation intra-épisode, hypothèse iid rompue,
variance élevée parce que le lot pousse dans la même direction, le tampon de rejeu INDISPONIBLE
parce que sur politique, et « la solution évidente mais malheureusement fausse » de réduire le
tampon (343-344) → §8.5 encadré [!WARNING], REFORMULÉ.

LAPAN ch. 12 « Actor-Critic Method: A2C and A3C » : variance comme sujet et Var[x] = E[(x−E[x])^2]
(355) → §8.6 ; L'EXPÉRIENCE DE PENSÉE À TROIS ACTIONS, Q1 et Q2 petits positifs et Q3 grand
négatif, puis décalage constant rendant tout positif et la mise à jour poussant LÉGÈREMENT VERS
l'action 3 alors que les récompenses relatives n'ont pas changé (356) → §8.6, l'intuition
centrale de la section ; le coût en échantillons et la DÉRIVE de la variance à mesure que l'agent
s'améliore, Pong à −21 où toutes les actions se ressemblent et où une référence de −21 fait lire
−20 comme une victoire (356) → §8.6 ; le protocole de mesure, backward(retain_graph=True) sur le
seul terme de politique, lecture de p.grad, puis backward de l'entropie, puis un seul step
(357-358) → §8.6 fragment de code, RÉÉCRIT ; LE CHIFFRE, variance deux à trois ordres de grandeur
plus basse avec référence (359) → §8.6 ; Q = V + A et l'avantage comme échelle (359) → §8.7 ;
apprendre V avec un autre réseau, entraîné comme en DQN par Bellman et erreur quadratique (359) ;
acteur et critique nommés et justifiés (360) ; fig. 12.4 et 12.5, deux réseaux puis tronc commun,
« efficacité et considérations de convergence », partage des filtres de convolution (360) →
FIG 08-03 et FIG 08-04, ET L'ENCADRÉ theta/w S'APPUIE SUR LA SECONDE ; plan d'entraînement en six
étapes (361) → §8.8 encadré d'algorithme, TRADUIT ; terme d'entropie imprimé p. 361 comme
L_H = beta somme pi_theta(s_i) log pi_theta(s_i), DEUX DÉFAUTS VÉRIFIÉS SUR L'IMAGE (argument
pi_theta(s_i) qui n'est pas une probabilité, somme interne sur les actions manquante ; et signe
d'entropie niée en contradiction avec le nom « prime » du texte voisin) → EQ 08-E12 ÉCRITE DEPUIS
LE CODE DE p. 368 ET NON DEPUIS CE DISPLAY, conformément aux notes ; ET AUCUN AVERTISSEMENT DE
COLLISION N'EST ÉCRIT : la collision H / L_H annoncée par le dossier N'EXISTE PAS dans la source,
c'est un artefact d'extraction réglé sur l'image de page pendant la phase 1, et notation.md §5 ne
tranche qu'une collision différente (l'entropie H contre la récompense d'épisode de la semaine 3,
déjà réglée) ; hyperparamètres Pong, non réglés (362) → §8.8 ; REWARD_STEPS de ~10 à 4 et
Q = somme gamma^i r_i + gamma^N V(s_N) (362-363) → EQ 08-E11 et §8.8 ; architecture Atari à trois
convolutions et deux têtes de 512, division par 255 (363) → §8.8 dernier paragraphe ; la même
quantité servant de cible au critique ET d'avantage à l'acteur (364) → §8.8 ; environnements
vectorisés, single_observation_space et single_action_space (365-366) → laboratoire volet B ;
critère d'arrêt à 18 sur 100 épisodes (366) → §8.8 ; Adam eps=1e−3 et l'absence d'explication
rigoureuse, conjecture donnée COMME CONJECTURE (366) → §8.8 troisième détail (gap 4) ;
value_t.detach() comme question de CORRECTION (368) → §8.8 premier détail ; écrêtage du gradient
(362) → §8.8 deuxième détail, l'argument sur-politique ajouté par le cours ; entropy_loss_t en
code, beta fois l'entropie niée (368) → §8.9 ; les dix quantités journalisées (369) →
laboratoire volet B ; tourniquet des environnements, « équivalent à une communication parallèle,
mais en série » (374) → §8.9, et la distinction vectorisé / multiprocessus énoncée explicitement ;
chaque transition utilisée ~32 fois par un DQN à tampon d'un million et lots de 32, davantage avec
un tampon priorisé (373) ; chaque transition utilisée UNE fois par un gradient de politique, écart
d'efficacité « d'un ordre de grandeur » (374) ; LE CONTREPOIDS, 8 millions de trames contre
1 million, soit huit fois plus, et « elles sont juste différentes » (374) → §8.9, REFORMULÉ ;
la règle de choix selon le coût de l'environnement (374) → §8.9, DONNÉE COMME RÈGLE DE DÉCISION
ET NON COMME CLASSEMENT ; A3C ajoutant une interaction asynchrone réelle (373) → §8.10 ;
fig. 12.12 et 12.13, parallélisme de données et de gradients, et ce qui circule sur les flèches
(375) → FIG 08-06 et FIG 08-07 ; fig. 12.11, un agent et plusieurs environnements (374) →
FIG 08-05 ; L'ARGUMENT DE COÛT, l'opération lourde est la perte et la rétropropagation, le pas de
descente est léger, le parallélisme de gradients sort le lourd du processus central (376) →
§8.10 ; LE CHOIX, douze GPU ou plus → gradients, un seul GPU → performances comparables et
données plus simple parce qu'on ne touche jamais aux valeurs de gradient (376) → §8.10, et c'est
ce qui justifie le choix du laboratoire ; Sync → Async en remplacement direct, 2 000 FPS et
facteur 2 (377) ; GRAD_BATCH 64 et TRAIN_BATCH 2, le premier grand pour amortir la
rétropropagation et le second petit POUR RESTER SUR POLITIQUE (378-379) → §8.10 ; spawn,
OMP_NUM_THREADS=1 et la perte d'un facteur 3 à 4, terminaison et jointure dans un finally
(381-383) → §8.10 encadré [!WARNING] ; share_memory() avec gradients locaux et paramètres
partagés (381-382) → §8.10 dernier paragraphe ; 500-600 FPS par enfant, 2 000 à 2 400 au total,
8 à 10 millions d'observations, ~1,5 h, gradients légèrement plus rapide (384) → §8.10.

SPINNING UP, page vpg.rst, LUE DIRECTEMENT DANS LE DÉPÔT (source-assets/code/spinningup/, non
indexée, pas de chunk, pas d'entrée MAP) : formulation « pousser vers le haut les probabilités
des actions à retour élevé, vers le bas celles à retour faible » (background) → §8.3, gardée
comme résumé mnémonique ; faits rapides, sur politique, espaces discrets ET continus,
parallélisation par MPI (quick-facts) ; PARAGRAPHE EXPLORATION-EXPLOITATION, politique
progressivement moins aléatoire parce que la règle de mise à jour récompense l'exploitation, et
risque de piège dans un optimum local (exploration-vs-exploitation) → §8.5 problème 3, et c'est
la justification la plus propre de la prime d'entropie de tout le kit, venue d'une source qui
n'en utilise pas ; deux formules COPIÉES DU .rst et jamais retapées (D44), nabla J avec l'avantage
sur une trajectoire entière et theta_{k+1} = theta_k + alpha nabla J (key-equations) → §8.7 pont
entre 08-E4 et 08-E12, et §8.3 pour la mise en place du signe ; pseudocode en sept étapes
(pseudocode) → §8.7 encadré d'algorithme, TRADUIT EN FRANÇAIS ET EN NOTATION DU COURS, phi
converti en w, AUCUNE LIGNE DE CRÉDIT INVENTÉE et aucune reproduction verbatim en anglais, la
note de licence du dossier étant contraignante : la pratique du cours (traduction + commentaire
SOURCE invisible) s'applique à une source MIT exactement comme aux autres, ce qui est plus sûr et
non moins sûr.

CE QUI N'EST PAS LU, par instruction du dossier : lapan/ch11/11-05 et lapan/ch12/12-05 (les
exécutions de résultats sur Pong, dont le laboratoire produit l'équivalent) ; sb/ch13/13-01 ;
sb/ch13/13-07 et 13-08 (cas continu et paramétrisation pour actions CONTINUES, qui sont
l'ouverture de la semaine 9) ; les trois résumés de chapitre ; et les pages trpo, ppo, ddpg, td3,
sac de Spinning Up, qui sont les semaines 9 et 10. Rien dans l'argument de la semaine ne les a
réclamés.

DEUX LACUNES TRAITÉES EXPLICITEMENT ET NON CONTOURNÉES (gaps 3 et 5 des notes) : il n'existe dans
aucun outil du cours de règle pour choisir beta, et §8.9 le dit en autant de mots avant de donner
0,01 comme point de départ et le contrôle d'ordre de grandeur relatif comme seul conseil ; et il
n'existe AUCUN chiffre d'A2C sur CartPole dans le kit (les sources donnent REINFORCE sur CartPole
et A2C sur Pong), de sorte que le laboratoire demande à l'étudiant SA PROPRE mesure, sur ses
propres graines, avec intervalle, et ne cite aucune cible, comme la semaine 4 l'a fait pour son
volet tabulaire.

DÉCOMPTE : 10 sections numérotées · 7 placeholders FIG · 0 placeholder EQ (17 équations
identifiées, 08-E1 à 08-E16 plus 08-E6b, toutes écrites directement en KaTeX dans la page :
11 transcrites d'une image de page vérifiée, dont 9 reproduites au caractère près ; 3 copiées du
.rst sous licence ouverte ; 3 écrites depuis le code ou directement. Sept formules standard de
plus ne portent pas d'identifiant parce qu'elles sont du vocabulaire du cours ou une définition :
le softmax de 8.1, la définition de J(theta) en 8.2, L = −Q log pi en 8.3, la récursion
G_t = r_t + gamma G_{t+1} en 8.3, Var[x] en 8.6, H_max = log 2 en 8.9 et la divergence KL du
laboratoire. L'inventaire complet, avec le régime de chacune, est dans extraction/week-08.md)
{{% /comment %}}
