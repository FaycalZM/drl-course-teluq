---
title: "Semaine 9 : Espaces d'action continus"
weight: 9
bookCollapseSection: true
---

# Semaine 9 : Espaces d'action continus

Depuis la semaine 4, toutes nos méthodes se terminaient par la même opération : une maximisation sur les actions. Cette semaine, cette opération devient **indisponible**, parce qu'on n'énumère pas un couple moteur. L'action cesse d'être un entier et devient un vecteur de réels, et il faut reconstruire sur ce terrain tout ce qui en dépendait : la politique doit désormais **produire** l'action, le critique doit la **recevoir** en entrée, et l'exploration, qui vivait dans le choix, doit être remise à la main dans l'espace d'actions. Vous verrez la route facile, qui réutilise la semaine 8 presque sans la toucher, puis la route déterministe, qui est plus efficace et plus fragile, puis la mesure qui explique sa fragilité, et les trois correctifs indépendants qui y répondent.

> [!IMPORTANT]
 **Une politique déterministe n'explore rien, et un critique qu'un acteur escalade se trompe vers le haut : les deux faits demandent chacun une réparation explicite.**

---
## Description générale

La semaine se lit comme une suite de conséquences, et chaque section sait à quelle perte elle répond.

Elle commence par constater la perte : l'action devient un vecteur de réels, et la maximisation sur les actions ne devient pas coûteuse, elle devient **impossible**. Découper l'intervalle en tranches n'est pas la sortie de secours qu'on croit, parce que \(k\) niveaux sur \(n\) dimensions font \(k^n\) actions : trois niveaux sur les huit moteurs d'un robot quadrupède en font déjà 6 561, et c'est la dimension, non la résolution, qui porte l'exposant.

Vient alors la route facile, et elle est rassurante : l'acteur-critique de la semaine 8 fonctionne déjà, à **une** modification près. Le réseau ne produit plus des probabilités mais les **paramètres d'une loi normale**, une moyenne et une variance par dimension d'action, et on tire l'action dans cette loi. La log-densité gaussienne remplace le logarithme du softmax, l'entropie prend une forme fermée qui ne dépend que de la variance, et le reste de l'algorithme est inchangé. Cette méthode obtient un mauvais score sur le robot, pour une raison qu'il faut savoir attribuer : ce n'est pas sa représentation de la politique qui échoue, c'est son régime d'échantillonnage, sur politique et avare en réutilisation. Elle traîne aussi un défaut discret que la semaine nomme, celui d'une log-densité calculée sur une action écrêtée comme si elle ne l'avait pas été.

La route déterministe est la promotion du comportement de test au rang de comportement d'entraînement. L'acteur rend l'action, le critique reçoit l'état **et** l'action et renvoie un seul nombre, et la composition des deux réseaux donne une fonction dérivable que l'acteur escalade : c'est le **gradient de politique déterministe**, une simple règle de dérivation en chaîne. La méthode devient hors politique, donc le tampon de rejeu et les réseaux cibles de la semaine 5 reviennent, avec la synchronisation douce de la semaine 6. Le gain est net, treize fois le score de la route facile avec moitié moins de trames, et le prix est l'exploration : une politique déterministe n'explore **rien**, et il faut ajouter du bruit aux actions. La semaine établit sur trois constats indépendants que le processus corrélé traditionnellement employé pour ce bruit n'est pas nécessaire, et qu'un bruit gaussien simple suffit.

La semaine se termine sur un défaut mesuré et sur trois réparations. Le critique de cette famille **surestime**, et ce n'est pas une anomalie : le mécanisme est celui que la semaine 6 a vu du côté discret, l'acteur jouant ici le rôle de la maximisation en avançant pas à pas vers les erreurs favorables du critique. Une boucle de rétroaction s'installe, où un critique inexact produit une politique médiocre que ce même critique note haut. Les trois réparations sont **trois changements indépendants** : prendre le minimum entre deux critiques jumeaux, ce qui est une sous-estimation volontaire ; ne mettre à jour l'acteur qu'une fois sur deux ; et lisser la cible en bruitant l'action cible. L'étude d'ablation qui les mesure séparément est la partie la plus instructive de la semaine, et elle réserve deux surprises : retirer l'un des trois **améliore** une tâche, et sur cette même tâche le simple réglage de la méthode de base apporte plus que n'importe lequel des trois correctifs.

La semaine ne porte **aucun jalon** : le prochain est en semaine 10, qui ferme le module 3.

---
## Mots-clés de la semaine

espace d'actions continu · espace de type `Box` · vecteur d'action · maximisation indisponible · discrétisation par dimension · robotique simulée · politique gaussienne · tête de moyenne · tête de variance · log-densité gaussienne · entropie différentielle · écrêtage de l'action · politique déterministe · gradient de politique déterministe · DDPG · critique à deux entrées · composition de réseaux · hors politique · tampon de rejeu · réseau cible · acteur cible · synchronisation douce · exploration par bruit ajouté à l'action · bruit gaussien non corrélé · processus d'Ornstein-Uhlenbeck · agent à état · démarrage uniforme · évaluation sans bruit · surestimation des valeurs d'action · biais de maximisation · boucle de rétroaction · erreur de différence temporelle résiduelle · protocole de mesure de la surestimation · TD3 · critiques jumeaux · double Q écrêté · sous-estimation volontaire · mise à jour retardée de la politique · deux échelles de temps · lissage de la politique cible · écrêtage du bruit · étude d'ablation · banc d'essai saturé · graines multiples avec intervalle

---
## En prévision de la semaine suivante

La semaine 10 ferme le module 3, et elle part d'une question que celle-ci a laissée ouverte. Nous avons passé une semaine entière à empêcher une mise à jour d'aller trop loin : un réseau cible pour ralentir la cible, un délai pour ralentir la politique, un minimum pour borner l'optimisme, un bruit écrêté pour lisser un pic. Toutes ces précautions sont des réponses indirectes à une même question, celle de savoir **de combien** une politique a le droit de changer en un pas. La semaine 10 la pose de front, en mesurant directement l'écart entre la politique avant et la politique après, et en construisant des méthodes qui contraignent cet écart au lieu de le subir. Vous y verrez aussi la dernière grande famille de méthodes à actions continues, celle qui reprend la discussion sur le bruit de cette semaine et la transforme en un terme de l'objectif lui-même, de sorte que l'exploration n'est plus ajoutée après coup mais récompensée. C'est la semaine qui réunit tout le module 3, et elle porte un jalon.

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF moins 31 pour LAPAN, conformément à
MAP-lapan.md, comme dans le dossier et les notes de phase 1. Toutes les pages citées
ci-dessous sont des indices PDF. Les deux autres sources ne se paginent pas : une page RST
s'ancre par son nom de section (SPINUP ddpg/..., SPINUP td3/...), le papier par sa section
(arXiv:1802.09477 §N), et les équations copiées de son LaTeX portent en plus le numéro
d'équation du fichier source (tex éq. N), conformément à D44.

SEMAINE À TROIS SOURCES, CHACUNE AVEC UN SEUL MÉTIER, EXACTEMENT COMME LE DOSSIER LE PRÉVOIT.
LAPAN ch. 15 fournit la matière de l'implémentation et les deux mesures de référence, et porte
les sections 9.1, 9.2, 9.3 et la première moitié de 9.4. Les deux pages RST sous licence
ouverte fournissent les énoncés propres (la mort de l'argmax, les équations de DDPG, les trois
correctifs en trois lignes) et interviennent en introduction, 9.1, 9.3, 9.4 et 9.6.
arXiv:1802.09477 fournit la démonstration, la mesure et l'étude d'ablation, et porte 9.5, 9.6
et le protocole du laboratoire. Aucun nouveau papier, aucun chunk hors manifeste.

INTRODUCTION. a*(s) = argmax_a q*(s,a) comme l'opération que la semaine perd, et le coût
inacceptable d'un optimiseur par pas (SPINUP ddpg/background) -> ouverture, équation 09-E1 et
les deux conséquences de câblage de l'encadré [!IMPORTANT]. L'avertissement sur les trois
écrêtages vient du glossaire du projet, pas d'une source.

§9.1. Valeurs en nombre infini, 13,5 contre 13,512 degrés, limites physiques mais ensemble de
valeurs très vaste, et monde physique plus souvent continu que discret (LAPAN p.463) ->
premier titre. Interface Box, step() recevant un vecteur NumPy, espaces mixtes par Tuple
(p.464) -> fragment de code et tableau de symboles. Équation d'optimalité avec max_a' et
impossibilité de l'évaluation exhaustive (SPINUP ddpg/key-equations, ddpg/background) ->
09-E2 et « Où meurt l'argmax ». Hypothèse de dérivabilité en a et substitution
max_a q = q(s, mu(s)) (SPINUP ddpg/key-equations) -> la ligne qui annonce §9.3, écrite
directement, sans identifiant, parce qu'elle est une approximation posée et non une formule à
reproduire au symbole près. Minitaur : 28 observations, 8 moteurs, récompense = distance moins
énergie, 1000 pas, seuil 15 (p.465-466) -> « Le robot de la semaine » et Figure 9-2. MuJoCo
commercial puis ouvert en 2022, livré par gymnasium[mujoco], contre le pin pybullet + gym
figé de la source (p.464-465) -> paragraphe d'outillage, AVEC LA CONSÉQUENCE DE COURS
EXPLICITE : le laboratoire ne reprend pas ce pin.

LACUNE 1 DES NOTES, TRAITÉE EN LA NOMMANT. L'argument combinatoire contre la discrétisation
(k^n, 3^8 = 6561, 5^8 = 390625, 10^8) n'existe dans AUCUN item du kit. Il est présenté comme
le raisonnement du cours, par une phrase qui le dit en autant de mots (« L'argument qui suit
est le mien »), et il s'appuie uniquement sur des faits ancrés : ensemble de valeurs
pratiquement infini (p.463), évaluation exhaustive impossible (SPINUP), huit dimensions
d'action (p.464-466). L'écho sourcé sur la mise en cases des OBSERVATIONS est cité comme
acquis des semaines 4 et 5 du cours, jamais comme source.

§9.2. Tête de valeur inchangée, seule la représentation de la politique est touchée (p.466).
Sortie d'une action nue possible mais mauvaise, surtout pour l'exploration ; réseau renvoyant
mu et sigma^2, vecteur de N normales non corrélées (p.467) -> premier titre et encadré sur le
coût de l'indépendance. Densité normale et sa log-densité (p.467, répétée p.470), transcrites
de l'image de page vérifiée -> 09-E3 et 09-E4, avec le renommage x -> a et l'ajout de la
somme sur les dimensions, qui est du cours. Entropie différentielle ln sqrt(2 pi e sigma^2)
(p.467) et sa forme de code -(ln(2 pi var) + 1)/2 (p.471) -> 09-E5 et l'encadré de signe.
Trois têtes, HID_SIZE 128, Tanh sur mu, Softplus sur var, rien sur la valeur (p.468) ->
fragment réécrit. Tirage np.random.normal puis np.clip (p.469) -> fragment agir(). Test sans
échantillonnage, moyenne utilisée directement (p.469) -> LE PONT VERS §9.3, souligné comme
tel. Garde var.clamp(min=1e-3) (p.470) -> une phrase. Hyperparamètres gamma 0,99, 2 pas, lots
de 32, pas 5e-5, beta 1e-4, test tous les 1000 (p.470) -> paragraphe de réglage. Résultat 9 M
trames / 16 h / 0,35, cause attribuée à l'environnement unique, faiblesse des méthodes de
gradient de politique (p.471), rejeu 0,312 et vidéo de 2 secondes (p.473) -> « Ce que cela
donne ». Le bogue silencieux action écrêtée contre log-densité non tronquée (p.469-470, et
« Piège méthodologique » du résumé de chapitre) -> dernier titre de la section, avec les deux
sorties honnêtes ; la seconde est annoncée comme la porte de la semaine 10 sans nommer la
méthode.

FORMULE DÉLIBÉRÉMENT NON REPRISE. La prime d'entropie écrite sans signe, sans somme et sans
coefficient en LAPAN p.466 contredit le code de la p.471 ; le cours s'appuie sur sa propre
page de la semaine 8 et n'en reproduit aucune trace.

§9.3. Filiation 2014 (résultat théorique) et 2015 (version profonde), SANS nom d'auteur
(p.473 ; SPINUP ddpg/references). Acteur rendant l'action, déterminisme par construction
(p.474). Critique à deux entrées et un scalaire, explicitement contre le choix d'efficacité du
DQN discret (p.474) -> LEÇON D'ARCHITECTURE DE LA SEMAINE et Figure 9-3. Composition des deux
réseaux, « des fonctions » (p.474). Théorème du gradient de politique déterministe et
équivalence avec le gradient stochastique (p.474), équation COPIÉE du .tex (tex éq. 1) ->
09-E6. DDPG apprend conjointement Q et la politique, hors politique, par Bellman
(SPINUP ddpg/background) ; applicable aux seuls espaces continus (ddpg/quick-facts).
Objectif de l'acteur avec w tenu constant (SPINUP ddpg/key-equations) -> 09-E7 ; perte telle
que codée (p.481) -> 09-E11 ; le piège des gradients déposés dans le critique et les deux
optimiseurs (p.479-481) -> encadré [!WARNING]. Critique optionnel en semaine 8 parce que
l'échantillonnage barre la rétropropagation, critique = objectif ici (p.475) -> paragraphe de
contraste, qui est la vraie frontière entre les deux semaines. Cible de Bellman, acteur cible
nourrissant le critique cible, q_last[dones] = 0 (p.480 ; SPINUP ddpg/pseudocode) -> 09-E8 en
forme à deux cas ; erreur quadratique de Bellman (ddpg/key-equations) -> 09-E9. Légitimité du
hors politique, l'équation de Bellman indifférente à la provenance des transitions
(ddpg/key-equations) -> reformulé en voix propre. Tampon 100 000, arbitrage de taille, deux
réseaux cibles, un seul pas de déroulement (p.479-480 ; ddpg/key-equations). Synchronisation
douce, pire sans elle en continu (p.481), et LES TROIS CONVENTIONS rho = alpha = 1 - tau
(ddpg/key-equations ; §3 du papier ; p.481) -> 09-E10 et encadré de conversion. Réseaux
400-300 avec Tanh, critique en Y (p.476-477) -> fragments et Figure 9-3. Boucle en sept
étapes : il n'y a PAS de pseudocode dans le manuel (lacune 4 des notes), la boîte est écrite
en français d'après SPINUP ddpg/pseudocode et la narration p.479-481. Résultats 5 M / ~20 h /
4,5, rejeu 3,03, vidéo 11 s, chute vers l'avant, 30 % de gain par processeur graphique
(p.481-484). D4PG comme horizon de famille, 51 atomes sur [-10,10], 3,5 M / 20 h / 17,912
contre un seuil de 15 (p.484-488), donné comme contexte et non comme méthode enseignée.

§9.4. Prix du déterminisme et bruit ajouté aux actions (p.475) ; mode de défaillance explicite,
variété d'actions insuffisante en début d'entraînement (SPINUP ddpg/exploration) -> premier
titre, qui porte LE FAIT À EMPORTER. mu(s) + epsilon N (p.475) -> 09-E12, avec la collision
epsilon contre le epsilon-glouton de la semaine 5 signalée. Processus d'Ornstein-Uhlenbeck,
particule brownienne massive sous frottement, hyperparamètres 0 / 0,15 / 0,2 et epsilon 1,0
(p.475, p.478) -> 09-E13 et 09-E14, TRANSCRITES de l'image de page : le terme sigma N de la
forme discrète manquait dans l'extraction du chunk et a été récupéré sur la page. Les trois
paramètres sont RENOMMÉS kappa, x barre, sigma_OU, avec la justification écrite dans le texte,
parce que theta, mu et sigma sont déjà pris par l'acteur, ses paramètres et l'écart-type
gaussien. Agent à état, initial_state(), None pour différer le dimensionnement, parenté avec
un environnement partiellement observable (p.478-479) -> paragraphe du coût d'architecture.
TRADITION ET NON NÉCESSITÉ, TROIS ANCRES INDÉPENDANTES, chacune reformulée en voix propre et
aucune citée entre guillemets : résultats récents en faveur du bruit non corrélé, retenu pour
sa simplicité (SPINUP ddpg/exploration) ; bruit non corrélé employé faute de gain mesurable,
exploration N(0; 0,1) (§6.1) ; les deux bruits essayés pour D4PG avec le même résultat, donc
le plus simple conservé, epsilon 0,3 (p.484, p.486). La règle de méthode « la complexité se
paie par une mesure » est du cours. Démarrage uniforme sur start_steps
(SPINUP ddpg/exploration) et politique purement exploratoire 1000 / 10000 pas selon la tâche
(§6.1) ; aucun bruit à l'évaluation (ddpg/exploration ; p.469) ; décroissance possible mais
non pratiquée, échelle gardée constante (ddpg/exploration).

§9.5. Résumé de la revendication (Abstract) -> annonce, en voix propre. Biais de maximisation,
erreur centrée produisant une surestimation propagée par Bellman, erreurs d'approximation
inévitables (§4) -> 09-E15, COPIÉE du .tex, avec epsilon RENOMMÉ eta par le cours et la raison
du renommage écrite dans un encadré. Maximisation cachée dans le pas de gradient, preuve pour
un pas assez petit (§4.1, tex éq. 7) -> 09-E16. Boucle de rétroaction, action médiocre notée
haut et renforcée (§4.1), et la ligne de diagnostic « les valeurs divergent quand la politique
est mauvaise » (§5.2) -> le paragraphe central et l'encadré [!WARNING] sur les deux courbes à
tracer ensemble. PROTOCOLE DE MESURE : 10 000 états, substitut de la valeur vraie par le retour
actualisé moyen sur 1000 épisodes depuis des états du tampon, deux tâches de locomotion, un
million de pas, verdict d'un biais très clair réduit par le double Q écrêté (§4.1) -> « Comment
on mesure une surestimation » plus le fragment de code, qui est la recette du volet B.
Deux mesures complémentaires, transplantations du double DQN et du double Q-learning
(§4.2) -> deux phrases. Variance : résidu delta, forme télescopée, variance qui croît avec
gamma, garantie limitée au mini-lot (§5.1, tex éq. 11-12) -> 09-E23. Étude du réseau cible,
tau = 1 / 0,1 / 0,01, politique figée contre politique apprise, divergence avec une cible
rapide (§5.2) -> dernier titre, qui prépare le correctif 2.

LACUNE 2 DES NOTES, TRAITÉE EN LA NOMMANT, ET C'EST LA DÉCISION ÉDITORIALE LA PLUS IMPORTANTE
DE LA SEMAINE. Aucun texte utilisable ne chiffre l'ampleur de la surestimation : elle n'existe
que dans des figures que la semaine ne peut pas publier. Le cours écrit donc un titre entier,
« Le nombre que je ne vous donnerai pas », qui dit la limite, refuse l'interpolation sur un axe
de figure, et renvoie à la route honnête retenue, à savoir la mesure produite par l'étudiant au
volet B. L'indication d'axe suggérée par l'extraction mutilée (ordres de 400 et 500, échelle
log de 10^2 à 10^4) N'EST PAS CITÉE, nulle part, sous aucune forme. Le commentaire « 3 trials »
trouvé dans le fichier LaTeX n'est pas cité non plus : la campagne de mesure est décrite sans
nombre d'exécutions, puisque la légende publiée n'en donne aucun.

§9.6. Les trois correctifs en trois lignes et la phrase de synthèse (SPINUP td3/background) ->
squelette de la section et liste numérotée. Fragilité aux hyperparamètres et mode de
défaillance par surestimation exploitée par la politique (td3/background) -> paragraphe
« pourquoi la boucle en a besoin ». Correctif 1 : échec de la transplantation du double DQN
faute d'indépendance entre réseaux trop semblables, insuffisance du double Q-learning complet
par partage du tampon et croisement des cibles, borne supérieure par le minimum (§4.2) ->
09-E17 copiée du .tex (tex éq. 10) ; sous-estimation préférable car non propagée par la mise à
jour de politique (§4.2) -> LECTURE 1, enseignée comme un choix volontaire ; espérance du
minimum décroissante avec la variance, préférence pour les estimations peu dispersées
(§4.2) -> LECTURE 2 ; acteur unique, y2 = y1, aucun biais ajouté si le second critique est
au-dessus (§4.2 ; SPINUP td3/key-equations) -> LECTURE 3 et fragment de code. Correctif 2 :
politique mise à jour moins souvent que la valeur, d fixé, algorithme à deux échelles de temps
comme la convergence linéaire le réclame, gain de performance ET de temps malgré un acteur
entraîné deux fois moins (§5.2, §6.2) -> deux remarques, dont celle sur les cibles mises à
jour DANS la branche retardée. Correctif 3 : surapprentissage d'un pic étroit, régularisation
du voisinage, parenté avec SARSA et SARSA espéré, bruit cible indépendant du bruit
d'exploration (§5.3) -> 09-E18 et 09-E19, copiées du .tex (tex éq. 13 et 14), plus les trois
précisions. Cible complète (§6, tex éq. 15) -> 09-E20. Forme des implémentations, action cible
écrêtée aux bornes et facteur terminal (SPINUP td3/key-equations) -> 09-E21 et 09-E22,
copiées du RST.

LES QUATRE DIVERGENCES SONT ENSEIGNÉES, NON FONDUES, ET LE TABLEAU LES DONNE EN QUATRE LIGNES
avec la position du cours sur chacune : écrêtage de l'action cible absent des équations et
ajouté par les implémentations (§5.3 et Algorithm 1 contre td3/key-equations) ; facteur
terminal absent des équations, nécessaire, et rendu par la forme à deux cas de la semaine 5
(td3/key-equations ; LAPAN p.480) ; ce que compte le délai, pas d'environnement contre indice
de mise à jour, le laboratoire tranchant pour les mises à jour du critique (Algorithm 1 contre
td3/pseudocode) ; sens du paramètre de synchronisation douce. L'accord sur les deux points
non divergents, cibles mises à jour dans la branche retardée et acteur optimisé contre Q1
seul, est enseigné comme un accord. Algorithme complet (Algorithm 1 p.5 ; td3/pseudocode) ->
09-E24, ÉCRIT EN FRANÇAIS en dix étapes, jamais collé depuis le bloc algorithmic du RST, que
KaTeX ne rendrait pas. Hyperparamètres complets, dont le critique recevant l'action dès la
première couche contrairement à l'implémentation historique (§6.1) -> paragraphe de réglage et
dernière précision d'architecture. Protocole : 1 M pas, évaluation tous les 5000 pas, dix
épisodes sans bruit, DIX GRAINES (§6.1) -> présenté comme la preuve que le protocole de la
semaine 7 n'est pas une invention du cours. Tableau 1 p.7 -> Tableau 9-1 ; Tableau 2 p.8 ->
Tableau 9-2, reproduit en entier, les deux étant du fait et non de l'expression. Lecture
prudente de l'étude sur elle-même (§6.2) donnée AVANT les trois lectures du cours, pour
interdire la sur-interprétation. LECTURE 1 : retrait du double Q écrêté, 4185 -> 850 sur Ant,
4565 -> 2579 sur Walker2d, mais 9533 -> 9793 sur HalfCheetah, et Ant qui profite de toute
réduction de surestimation (§6.2, Table 2). LECTURE 2 : le réglage seul, 8401 contre 3163 sur
HalfCheetah, bat l'apport de n'importe quel correctif isolé. LECTURE 3 : les deux
transplantations ne sont ni absurdes ni dominantes, et leur colonne Ant est l'écho expérimental
de la mesure de §4.2. Saturation d'InvertedPendulum à 1000,00 pour six méthodes (Table 1 p.7)
-> encadré final, qui donne la raison expérimentale du choix de Pendulum-v1 annoncée en §9.1.

LABORATOIRE. Ablation à cinq configurations plus trois « moins un », un seul programme et
trois interrupteurs, protocole de la semaine 7 (§6.1-6.2). Pendulum-v1 nommé avec son
identifiant exact, un couple dans [-2,2], et NON InvertedPendulum-v5 : correction du dossier
reportée par la passe de lecture, tenue ici (Table 1 p.7). Volet B = la mesure de surestimation
de §4.1 ramenée à l'échelle d'un carnet, ce qui est la route honnête retenue pour la lacune 2.
Solution courte par la bibliothèque haut niveau, qui livre les deux bruits comme deux objets
interchangeables et permet la comparaison en une ligne ; code du cours en PyTorch et Gymnasium
seulement, réécrit et jamais recopié d'un dépôt (D15). MuJoCo en roue, rendu hors écran, vidéo
dans un fichier, robot en DÉMONSTRATION et jamais en tâche mesurée (COURSE-PLAN §9.2).
L'identifiant du robot est accompagné d'une consigne de vérification, parce qu'aucune source
du kit ne fixe le suffixe de version des environnements MuJoCo de Gymnasium.
LACUNE 3 DES NOTES, TRAITÉE EXPLICITEMENT : aucun score publié n'existe pour cette famille sur
une petite tâche, donc le laboratoire exige une exécution pilote et une cible annoncée par
l'étudiant, et la page ne cite AUCUN chiffre à atteindre.

CE QUE LA SEMAINE N'A PAS UTILISÉ, ET POURQUOI. Aucune figure du papier, sur la question de
licence que le dossier tranche : un préprint autorise la redistribution de l'article, pas la
republication de ses tracés dans un cours. Les figures 1, 2, 3 et 5 n'apparaissent donc que
sous forme de prose et de nombres, et la décision n'a pas été rouverte pendant la rédaction.
Toutes les autres figures du chapitre 15 (15.2, 15.3, 15.6 à 15.12) sont des courbes
d'entraînement ou de test des exécutions de la source, exclues par la règle des semaines 2 et
3 ; 15.4 et 15.9 sont des captures d'une simulation que l'étudiant rend lui-même. La liste
« DO NOT read » du dossier a été respectée en entier : related work, conclusion et les trois
annexes du papier (preuve de convergence, dérivation du biais, note d'implémentation d'une
autre méthode) sont restés fermés, de même que la page RST de la méthode de la semaine 10,
lapan/ch16 et sb/ch13. SAC n'apparaît nulle part : ni comme méthode, ni comme nom, et les
colonnes du Tableau 9-1 qui la contiendraient ne sont pas reproduites. Le crochet de la
semaine 10 est planté deux fois, par la seconde sortie honnête du mensonge de §9.2 et par la
page d'accueil, sans jamais nommer la méthode ni son objectif.

DÉCOMPTE : 6 sections numérotées · 4 placeholders FIG (dont 2 figures produites par le cours)
· 0 placeholder EQ (24 équations identifiées, 09-E1 à 09-E24, toutes écrites directement en
KaTeX dans la page, et réparties ainsi d'après la colonne « régime » des notes de phase 1 :
7 copiées du pseudocode sous licence ouverte (E1, E2, E7, E8, E9, E21, E22), 8 copiées du
LaTeX du papier (E6, E15, E16, E17, E18, E19, E20, E23), 6 transcrites d'images de pages
vérifiées (E3, E4, E5, E12, E13, E14) et 3 écrites directement depuis le code, la notation du
cours ou l'algorithme rendu en français (E10, E11, E24). Trois formules de plus ne portent pas d'identifiant parce qu'elles sont une
approximation posée ou du vocabulaire du cours : la substitution max_a q = q(s, mu(s)) de
§9.1, la somme sur les dimensions de la log-densité gaussienne de §9.2, et la boîte en neuf
étapes de §9.3, écrite en français d'après le pseudocode sous licence ouverte. L'inventaire
complet, avec le régime de chacune, est dans extraction/week-09.md)
{{% /comment %}}
