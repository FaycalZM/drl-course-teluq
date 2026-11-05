---
title: "Semaine 4 : Équation de Bellman et apprentissage tabulaire"
weight: 4
bookCollapseSection: true
---

# Semaine 4 : Équation de Bellman et apprentissage tabulaire

Quatrième semaine, et le module 2 s'ouvre sur la quantité qui manquait à la semaine 3 : une valeur attachée à chaque état, qui dit ce que cet état promet sans qu'il faille attendre la fin de l'épisode. Le gain est spectaculaire et il vaut mieux qu'un discours : le même FrozenLake glissant qui demandait cinquante minutes de calcul à la méthode précédente est résolu cette semaine en **moins d'une seconde**, par une table de seize nombres et une équation. Nous dérivons cette équation en quatre lignes, nous en tirons l'optimalité, puis nous **construisons** l'itération sur la valeur au lieu de la réciter, et nous finissons par retirer le modèle de l'environnement. Aucun réseau de neurones dans ces sept sections : c'est une pause d'outillage, et c'est la dernière. La semaine se referme d'ailleurs sur un problème entier, que la suivante prendra en charge : toutes ces tables ont **une ligne par état**, seize pour FrozenLake en 4 × 4, quarante-huit pour la falaise, et aucune pour CartPole.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** tous les algorithmes que nous écrivons ici sont la **même équation de Bellman**, et ils ne diffèrent que par ce qui remplace l'espérance. La programmation dynamique y met la distribution exacte des successeurs, TD y met un successeur observé, et la place du \(\max\) décide du reste.

---
## Description générale

Les sections 4.1 à 4.3 posent les objets. Une valeur n'existe pas sans politique, et quatre politiques sur un environnement de trois états donnent quatre valeurs différentes ; un quatrième état suffit ensuite à faire basculer la meilleure politique, ce qui installe le piège fondateur du domaine, la **gourmandise à un pas**. La section 4.2 dérive l'**équation de Bellman** pour \(v_\pi\) en quatre lignes, à partir de la seule récurrence du retour, et la lit comme une contrainte de cohérence entre voisins plutôt que comme une formule. La section 4.3 passe à l'optimalité, écrit les deux équations d'optimalité, montre **où** se place le \(\max\) dans chacune, et règle la dette ouverte en 4.1 : être glouton redevient optimal dès que la quantité regardée contient déjà tout le futur. Elle justifie enfin le choix qui structure quatre semaines de cours, apprendre \(q\) plutôt que \(v\), parce que \(q_*\) permet d'agir **sans rien savoir des dynamiques de l'environnement**.

Les sections 4.4 et 4.5 passent aux algorithmes, et 4.4 ne les livre pas comme une recette : elle en construit quatre dans l'ordre, chacun répondant à l'insuffisance du précédent, évaluer une politique, l'améliorer, alterner les deux, puis tronquer l'évaluation à **un seul balayage**, ce qui fait apparaître l'itération sur la valeur comme inévitable plutôt que comme donnée. Une seule observation gouverne toute la section : la politique gloutonne est déjà optimale au troisième balayage alors que les valeurs sont encore fausses d'un facteur sept. La section 4.5 met tout cela au travail sur FrozenLake avec un agent à trois tables qui **estime la dynamique en comptant ses transitions**, et qui est le dernier agent du cours à avoir le droit de la regarder.

Les sections 4.6 et 4.7 retirent le modèle. TD(0) remplace le retour complet par la récompense observée plus l'estimation de l'état d'arrivée, ce qui lui donne à la fois l'absence de modèle de Monte-Carlo et l'**amorçage** de la programmation dynamique ; l'erreur TD reçoit son nom et son symbole, qu'elle gardera jusqu'en semaine 15. La section 4.7 passe au contrôle avec Sarsa et Q-learning, qui ne diffèrent que par un symbole, et avec la méthode \(\varepsilon\)-gloutonne, définie ici parce que c'est l'endroit où le cours en a besoin. Le laboratoire est **formatif**, la semaine 4 ne porte aucun jalon, et il tient en quelques secondes de processeur central : deux volets d'échauffement sur FrozenLake, avec modèle puis sans, puis le volet évalué, la **falaise**, où la méthode qui a appris la meilleure politique obtient le pire score en ligne. Un quatrième volet, facultatif, compare TD et Monte-Carlo sur un problème dont les valeurs vraies sont connues.

---
## Mots-clés de la semaine

valeur d'un état · valeur d'une action · état terminal · équation de Bellman · diagramme de sauvegarde · mise à jour de Bellman · politique optimale · équation d'optimalité de Bellman · politique gloutonne · programmation dynamique · évaluation de politique · problème de prédiction · balayage de l'espace d'états · mise à jour sur place · mise à jour en espérance · amélioration de politique · théorème d'amélioration de politique · itération sur la politique · itération généralisée de politique · itération sur la valeur · itération sur Q · apprentissage tabulaire · estimation des probabilités de transition · discrétisation de l'espace d'états · efficacité d'échantillon · amorçage · apprentissage par différences temporelles · TD(0) · mise à jour par échantillon · erreur TD · pas d'apprentissage · méthode epsilon-gloutonne · Sarsa · Q-learning · Q-learning tabulaire · mise à jour de Q-learning · grille ventée · marche au bord de la falaise

---
## En prévision de la semaine suivante

Nous butons sur une chose précise, et elle est arithmétique plutôt que conceptuelle. Nos tables ont une ligne par état, et il faut avoir visité un état pour lui donner une valeur. Tant que les états se comptent par dizaines, tout va bien, et vous venez de le vérifier trois fois. Mais l'écran d'un jeu vidéo, les quatre nombres réels de CartPole, la position d'un bras robotisé : ces espaces n'ont pas des dizaines d'états, ils en ont plus que vous ne pourrez jamais en visiter, et la plupart ne seront vus **qu'une seule fois**. Une table ne peut rien faire de cela, pour une raison qui n'est pas une question de taille mémoire : une table **ne généralise pas**. Rien, dans une table, ne dit que deux cases voisines devraient porter des valeurs voisines. La semaine 5 remplace donc la table par une fonction, \(\hat v(s,\mathbf{w})\) et \(\hat q(s,a,\mathbf{w})\), et cette fonction sera un réseau de neurones. Tout ce que vous avez écrit cette semaine survivra : la cible TD, l'erreur TD, le \(\max\) de Q-learning, l'état terminal à zéro. Une seule ligne changera, et c'est la dernière du tableau de la section 4.7 : au lieu d'écrire dans une case, nous descendrons un gradient. Préparez-vous, parce que cette seule ligne apporte avec elle toutes les instabilités du cours.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (D35). Imprimé = PDF − 31 pour LAPAN et PDF − 22 pour SB,
conformément à MAP-lapan.md et MAP-sb.md, comme dans le dossier et les notes de phase 1.
Toutes les pages citées ci-dessous sont des indices PDF.

PREMIÈRE SEMAINE À DEUX SOURCES DU COURS. Le chapitre du manuel ne contient ni Q-learning ni
méthode epsilon-gloutonne, que le plan promet pour cette semaine : le supplément porte donc la
moitié du contenu (sections 4.1 à 4.4, 4.6, 4.7) et le manuel l'autre moitié (4.1, 4.3, 4.5).
La jonction est écrite pour être invisible : aucune section n'est « la section du manuel » ou
« la section du supplément », et les deux voix sont retranscrites dans la notation unique de
notation.md.

SUTTON & BARTO ch. 3 « Finite Markov Decision Processes » : « presque tous les algorithmes
d'AR impliquent l'estimation de fonctions de valeur », politique comme application vers des
distributions, la barre de π n'est pas un conditionnement, v_π → EQ 04-E1, q_π → EQ 04-E2,
valeur nulle d'un état terminal, lien Monte-Carlo par moyenne des retours observés (80) ;
dérivation de l'équation de Bellman en quatre lignes → EQ 04-E3, lecture « valeur de l'état de
départ = valeur actualisée de l'état suivant espéré + récompense espérée en chemin », unicité de
la solution, convention des diagrammes de sauvegarde, cercle vide et cercle plein, un état peut
être son propre successeur (81-82) ; monde en grille 5 × 5, dynamiques exceptionnelles A → A′ et
B → B′, politique équiprobable et γ = 0,9, table de 8,8 à −2,0, v_π(A) < 10 et v_π(B) > 5,
résolution par système linéaire, fig. 3.2 → FIG 04-02, chiffres de la case centrale 0,7 avec
voisines 2,3 / 0,4 / −0,4 / 0,7 (82) ; ordre partiel sur les politiques, existence d'au moins une
politique optimale, v_* et q_* partagés → EQ 04-E4 (84) ; q_* en fonction de v_* → EQ 04-E5,
équations d'optimalité pour v_* → EQ 04-E6 et pour q_* → EQ 04-E7, max intérieur au crochet dans
la seconde (85) ; système de n équations à n inconnues, solution unique, toute politique
gloutonne par rapport à v_* est optimale, diagrammes de sauvegarde de l'optimalité
fig. 3.4 → FIG 04-03 (86) ; q_* évite même le regard à un pas, « met en cache le résultat de
toutes les recherches à un pas », agir sans rien savoir de la dynamique, solution optimale du
monde en grille fig. 3.5 → FIG 04-04 (86-87) ; trois hypothèses de la solution directe,
backgammon et ses 10^20 états (88).

SUTTON & BARTO ch. 4 « Dynamic Programming » : définition de la programmation dynamique comme
l'ensemble des algorithmes supposant un modèle parfait, utilité pratique limitée et fondement
théorique essentiel, « toutes ces méthodes peuvent se lire comme des tentatives d'obtenir le
même effet que la programmation dynamique, avec moins de calcul et sans supposer un modèle
parfait » (95) ; clé de lecture « on obtient les algorithmes de programmation dynamique en
transformant les équations de Bellman en affectations », évaluation de politique et problème de
prédiction, existence et unicité si γ < 1 ou terminaison garantie, système de |S| équations
linéaires, évaluation itérative → EQ 04-E8, mise à jour en espérance (96-97) ; balayage, deux
tableaux contre un seul, mise à jour sur place plus rapide et sensible à l'ordre des états,
« c'est la version sur place qu'on a en tête », critère d'arrêt sur le plus grand changement,
encadré de pseudocode → EQ 04-E9 (97) ; exemple 4.1, grille 4 × 4, quatorze états non terminaux,
récompense −1 par transition, non actualisé, terminal dessiné deux fois mais unique, v_π égal à
l'opposé du nombre espéré de pas (98) ; fig. 4.1 → FIG 04-06, chiffres k = 0, 1, 2, 3, 10, ∞
et politique gloutonne optimale dès k = 3 (99) ; q_π en fonction de v_π → EQ 04-E10, théorème
d'amélioration de politique → EQ 04-E11, deux lignes de la démonstration par déroulement (100) ;
politique gloutonne → EQ 04-E12, égalités tranchées arbitrairement, argument de clôture par
l'équation d'optimalité, politiques stochastiques et répartition libre entre actions
maximisantes (101) ; chaîne E/I de l'itération sur la politique, convergence en un nombre fini
d'itérations, reprise de la fonction de valeur précédente, encadré de pseudocode à trois blocs →
EQ 04-E15 (PLACEHOLDER, voir ci-dessous) (102) ; itération sur la politique très rapide en
pratique, optimum après une seule itération sur la grille 4 × 4 (103-104) ; troncature de
l'évaluation sans perte de garantie, cas particulier d'un seul balayage, itération sur la valeur
→ EQ 04-E13, « combine l'amélioration et l'évaluation tronquée », équation d'optimalité
transformée en règle de mise à jour, identique à EQ 04-E8 au max près, séparation entre la
boucle qui produit V et la passe finale qui produit π, encadré → EQ 04-E14 (105) ; itération
généralisée de politique, granularité libre, stabilisation à l'optimum seulement (108, lu dans
index/summaries/sb/ch04.md).

SUTTON & BARTO ch. 6 « Temporal-Difference Learning » : « s'il fallait désigner une seule idée
comme centrale et nouvelle dans l'AR, ce serait sans aucun doute l'apprentissage par différences
temporelles », TD = échantillonnage de Monte-Carlo + amorçage de la programmation dynamique,
Monte-Carlo à α constant → EQ 04-E16 (141) ; TD(0) → EQ 04-E17, aussi appelé TD à un pas,
encadré de pseudocode → EQ 04-E18, les trois raisons distinctes pour lesquelles les cibles sont
des estimations (142) ; mise à jour par échantillon contre mise à jour en espérance, erreur TD →
EQ 04-E19 et son décalage d'un pas, erreur de Monte-Carlo comme somme actualisée des erreurs TD,
exacte seulement si V est figée (143) ; exemple du retour à la maison, six états, temps écoulés
0 / 5 / 20 / 30 / 40 / 43 et totaux prédits 30 / 40 / 35 / 40 / 43 / 43, variante de
l'embouteillage après 25 minutes (144-145) ; trois avantages de TD, aucun modèle, incrémental et
en ligne, insensible aux épisodes longs ou inexistants (146, lu dans
index/summaries/sb/ch06.md) ; contrôle par estimation de q_π, schéma de l'itération généralisée
de politique, compromis exploration-exploitation et partage sur politique / hors politique,
chaîne de Markov sur les couples état-action et report des théorèmes de convergence,
Sarsa → EQ 04-E20, Q(terminal, ·) = 0, origine du nom par le quintuplet, convergence sous
visites infinies et convergence de la politique vers la gloutonne, ε = 1/t (151-152) ; grille
ventée, ε = 0,1, α = 0,5, Q initialisée à zéro, politique gloutonne optimale bien avant
8 000 pas, moyenne de 17 pas contre un minimum de 15, Monte-Carlo inutilisable car la
terminaison n'est pas garantie, encadré Sarsa → EQ 04-E21 (152) ; Q-learning → EQ 04-E22,
approche directement q_* indépendamment de la politique suivie, la politique ne décide que des
couples visités, convergence sous mise à jour continue de tous les couples, encadré
→ EQ 04-E23 (153) ; exemple 6.6 de la falaise, non actualisé, −1 par transition et −100 pour la
falaise avec renvoi au départ, ε = 0,1, Q-learning apprend le chemin du bord et tombe, Sarsa
apprend le détour, performance en ligne de Q-learning pire malgré la meilleure politique
apprise, convergence des deux si ε décroît, encadrés non numérotés → FIG 04-08 et FIG 04-09,
Sarsa vers −25 et Q-learning vers −50 sur 500 épisodes, exercice 6.12 repris en question
ouverte de fin de section 4.7 (154).

LAPAN ch. 5 « Tabular Learning and the Bellman Equation » : le chapitre établit la préparation
requise pour le Q-learning profond (144) ; contre-exemple à trois états, r = 1 à droite et r = 2
vers le bas, quatre politiques donnant 1,0 / 2,0 / 1,5 / 1,9 (145-146) ; quatrième état et
récompense −20, fig. 5.2 → FIG 04-01, les mêmes quatre politiques donnant 1,0 / −18 / −8,5 /
−16,1, bascule de la meilleure politique (146-147) ; forme déterministe V_0 = max_a (r_a + γ V_a)
reprise comme intuition avant EQ 04-E6, passage au cas stochastique par l'espérance (147-148) ;
caractère récursif de la définition, les valeurs donnent la politique optimale gratuitement,
nom de la programmation dynamique (149) ; exemple numérique du glissement à 33 %, quatre états
terminaux, γ = 1, Q(s_0, ·) = 2,31 / 1,98 / 2,64 / 2,97 et V(s_0) = 2,97,
fig. 5.6 → FIG 04-05 (150-151, page certifiée fiable par l'indexation) ; argument pratique de Q
avant V, agir depuis Q ne demande que la table, agir depuis V demande les probabilités « que
nous connaissons rarement d'avance » (152) ; boucle à deux états, récompenses alternant 1 et 2,
γ = 0,9, 0,9^10 ≈ 0,349 et 0,9^100 ≈ 0,0000266, cinquante termes suffisent,
V(s_1) = 14,736450674121663 et V(s_2) = 15,262752483911719, procédure en trois étapes, première
limitation sur la taille de l'espace d'états et la discrétisation, EQ 04-E25 (152-153) ; seconde
limitation sur les probabilités de transition absentes de l'interface, estimation par comptage,
trois tables et exemple du compteur {4: 3, 5: 7}, l'agent lit sa propre dynamique estimée
(154) ; constantes GAMMA = 0,9 et TEST_EPISODES = 20, espaces Discrete (155, erreur d'auteur
corrigée) ; calc_action_value et fig. 5.8 → FIG 04-07 et EQ 04-E24, écrite depuis le code et non
depuis la figure dont les fractions sont inversées (156-157) ; select_action comme argmax pur,
aucune exploration dans la décision (157) ; boucle d'entraînement, 100 pas aléatoires, un
balayage, 20 épisodes de test qui nourrissent les tables, arrêt au-delà de 0,80 (158-159) ;
résolu en 11 tours en moins d'une seconde, 10 à 100 tours typiques, deux raisons de la rapidité,
espérance sur les issues estimées et mise à jour depuis une transition unique, efficacité
d'échantillon, comparaison avec la méthode de la semaine 3 en secondes contre une heure (159) ;
FrozenLake ne paie qu'à l'objectif, 8 × 8 de 150 à 1 000 tours, figs. 5.9 et 5.10 écartées
(captures TensorBoard réduites à leurs légendes par l'extraction) (160) ; itération sur Q, trois
différences de code, select_action devient une lecture de table (161-162) ; même vitesse, quatre
fois la mémoire, 18 tours, la décision n'a plus besoin des probabilités, V reste essentielle à
l'acteur-critique de la semaine 8 (162-163).

COURSE-PLAN §2 et §9.2 : aucun jalon en semaine 4, le prochain est en semaine 7 ; semaines 1 à 4
évaluées à quelques minutes sur T4, donc processeur central suffisant pour tout le laboratoire.

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossiers/week-04.md, section « DO NOT read ») :
sb/ch06/06-07 (biais de maximisation et double apprentissage, semaine 6, où le Double DQN en a
besoin), sb/ch06/06-03 (optimalité de TD(0) et mises à jour par lots), sb/ch06/06-06 (Sarsa
espérée), sb/ch06/06-08 (post-états, semaine 12), sb/ch04/04-06 et 04-07 (programmation dynamique
asynchrone, et GPI dont une seule phrase est reprise depuis le résumé), sb/ch03/03-01 à 03-06
(récompenses, retours, notation unifiée, déjà couverts en semaines 1 et 3), sb/ch05 au-delà de ce
que la semaine 3 avait lu. Aucune approximation de fonction n'apparaît dans cette semaine : ni
v̂(s,w), ni DQN, ni tampon de rejeu, ni réseau cible, ni perte de Huber. La conclusion s'arrête
délibérément sur la question que la semaine 5 répond.

ÉCARTS ASSUMÉS
- D43 : le seuil de convergence de la programmation dynamique, noté θ dans la source, s'écrit ϑ
  partout, y compris à l'intérieur des encadrés de pseudocode EQ 04-E9 et EQ 04-E14, parce qu'un
  étudiant qui recopie un encadré dans un carnet ne doit pas importer la collision avec les
  paramètres de réseau. Règle énoncée dans un encadré [!NOTE] à l'ouverture de la section 4.4.
- D43 : les majuscules V et Q de la source, employées là où le formalisme écrit v_π et q_π, et un
  V qui vaut v_* dans les équations d'optimalité, sont traduites à l'entrée. La règle est énoncée
  UNE fois, dans un encadré [!NOTE] en fin de section 4.3, et elle est formulée SANS attribution
  (« vous croiserez ailleurs… ») : aucun auteur, aucun ouvrage, aucun chapitre n'apparaît. C'est
  la correction explicite d'un écart livré en semaine 2.
- D43 : r_t devient R_t, p_{a,i→j} devient p(s'|s,a), et l'espérance glosée « sur tous les états »
  est réécrite sur les successeurs. Appliqué silencieusement à EQ 04-E24 et EQ 04-E25.
- notation.md §4 contre concepts.yaml : α s'écrit « pas d'apprentissage », forme déjà livrée en
  semaine 3 dans trois tableaux symbole ↔ variable, alors que l'entrée taux-apprentissage du
  registre porte fr: « taux d'apprentissage ». La ligne de glossaire ajoutée cette semaine retient
  « pas d'apprentissage » et enregistre « taux d'apprentissage » comme synonyme accepté, non comme
  forme à éviter. L'alignement du registre est signalé, pas effectué.
- « Efficacité d'échantillon » est employée SANS italiques de première occurrence : glossaire.md
  date le terme de la semaine 6 et rien ne doit le contredire. Même traitement que
  « méthode de Monte-Carlo » en semaine 3.
- Erreurs d'auteur NON propagées : l'agent « va à gauche » (LAPAN p. 146) est écrit « à droite »,
  ce que la figure et l'arithmétique exigent toutes deux ; les espaces de FrozenLake, annoncés
  Box (LAPAN p. 155), sont écrits Discrete(16) et Discrete(4), ce que la phrase suivante de la
  même page confirme. Les deux corrections sont silencieuses : rien dans la page n'indique à
  l'étudiant qu'une source se trompait, puisque rien dans la page n'indique qu'il y a une source.
- Correction de référence de figure reportée depuis la phase 1 : les deux panneaux de la falaise
  sont des encadrés NON NUMÉROTÉS de la p. 154, et non « fig. 6.3 p. 155 », qui est le balayage en
  α de la Sarsa espérée, section exclue du dossier. FIG 04-08 et FIG 04-09 visent la p. 154.
  De même fig. 3.2 est p. 82 (et non 80) et fig. 3.4 est p. 86 (et non 85), la solution optimale
  du monde en grille étant fig. 3.5 p. 87.
- Synthèse propre au cours, signalée comme telle : le point « cet agent a le droit de regarder la
  dynamique, et il est le dernier du cours à l'avoir » n'est énoncé explicitement par aucune
  source. Les deux moitiés y sont (le modèle parfait supposé par la programmation dynamique,
  l'estimation par comptage du manuel) ; leur rapprochement et la frontière avec la semaine 5
  sont la contribution du cours. Livré en encadré [!IMPORTANT] à l'ouverture de la section 4.5,
  comme les notes l'exigent.
- Synthèse propre au cours, deuxième occurrence : l'échelle « glouton sur la récompense immédiate
  est un piège (4.1), glouton sur v_π est meilleur (4.4), glouton sur v_* est optimal (4.3) » est
  un assemblage de trois résultats que les sources présentent séparément. Signalée dans un
  encadré [!TIP] en fin de section 4.4.
- La méthode epsilon-gloutonne (EQ 04-E26) est DÉFINIE PAR LE COURS. Aucune source lue cette
  semaine ne la définit : elle n'y apparaît qu'en condition de convergence et en « par exemple »
  dans deux encadrés de pseudocode, son traitement complet appartenant au chapitre des bandits,
  hors programme. Le cours la définit en deux lignes, sans la citer et sans aller chercher
  ailleurs, conformément à la décision de la phase 1.
- Arithmétique reconstruite, et elle est forcée : les quatre récompenses terminales de l'exemple
  du glissement à 33 % (1 en haut, 2 à gauche, 3 en bas, 4 à droite) sont les seules compatibles
  avec les quatre valeurs Q publiées, 2,31 / 1,98 / 2,64 / 2,97, et avec la règle de glissement.
  La page porteuse de ces chiffres est celle que l'indexation a certifiée fiable.
- D15 : tout le code est réécrit (noms français, annotations de type, classe refactorisée autour
  d'une méthode enregistrer(), assertions et points de contrôle ajoutés, promesse() extraite pour
  rendre visible la seule différence entre évaluation et itération sur la valeur). Rien n'est
  copié d'un dépôt de source.
- D12 : NumPy et Gymnasium uniquement. PyTorch est déclaré facultatif cette semaine, ce qui est
  exact et pédagogiquement utile : la semaine 5 réintroduira le réseau et l'étudiant verra
  précisément ce qu'il remplace. Aucune bibliothèque d'algorithmes n'est proposée : les cinq
  algorithmes de la semaine tiennent chacun en moins de vingt lignes.
- L'environnement de la falaise est ÉCRIT par l'étudiant plutôt qu'importé, bien que
  CliffWalking-v0 existe dans la famille des environnements en texte de Gymnasium. Motif explicite
  dans l'énoncé du volet C : une grille 4 × 12 tient en vingt lignes et la règle subtile (la chute
  renvoie au départ SANS terminer l'épisode) ne s'apprend qu'en l'écrivant.

DÉCOMPTE : 7 sections · 9 placeholders FIG · 1 placeholder EQ
(les équations 04-E1 à 04-E14 et 04-E16 à 04-E25 sont recopiées depuis index/notes/week-04.md,
elles-mêmes transcrites en phase 1 depuis treize pages rasterisées sous index/pages/sb/ ;
04-E26, la règle de sélection epsilon-gloutonne, est écrite directement et appartient au cours ;
seule 04-E15, l'encadré de pseudocode de l'itération sur la politique, passe par un placeholder,
parce que index/pages/sb/0102.png n'a jamais été produite.)
{{% /comment %}}
