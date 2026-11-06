---
title: "Semaine 10 : Régions de confiance : TRPO, PPO, ACKTR, SAC"
weight: 10
bookCollapseSection: true
---

# Semaine 10 : Régions de confiance : TRPO, PPO, ACKTR, SAC

Depuis la semaine 8, toutes nos méthodes prennent le pas que le gradient indique, le multiplient par un pas d'apprentissage et espèrent qu'il était assez petit. Cette semaine dit ce qui arrive quand il ne l'est pas, et pourquoi c'est beaucoup plus grave ici qu'ailleurs : **on ne se relève pas d'une mauvaise mise à jour de politique**, parce que c'est la politique abîmée qui collecte le lot dont la mise à jour suivante se nourrira. Un apprentissage supervisé tolère un mauvais pas ; ici, le mauvais pas choisit ses propres données. Réduire le pas d'apprentissage achète de la sécurité en renonçant à converger, donc il faut **contraindre** le pas et non le rétrécir. Quatre méthodes répondent à cela, et la dernière n'appartient pas du tout à la famille : elle est hors politique, elle descend de la semaine 9, et elle paie son exploration en calcul. La semaine ferme le module 3, et elle porte le jalon 3.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** la bonne question n'est pas de combien les poids ont bougé, c'est de combien la **politique** a bougé : l'écrêtage du rapport entre l'ancienne et la nouvelle politique supprime l'intérêt d'aller trop loin, là où une contrainte explicite l'interdit au prix d'une machinerie entière.

---
## Description générale

La semaine commence par un constat et une reformulation. Le constat : une politique est un objet fortement non linéaire, un petit déplacement de poids peut produire un grand déplacement de comportement, et l'erreur ne se corrige pas au pas suivant parce que le pas suivant travaille sur des données que la politique abîmée a collectées. La reformulation : il ne faut pas borner le déplacement des **paramètres**, il faut borner le déplacement de la **politique**, et cet écart se mesure par une divergence entre deux distributions. La zone où il reste sous un budget fixé est une **région de confiance**, et elle donne son nom à la famille.

Le banc d'essai vient ensuite, et il porte deux pièges de mesure que la semaine transmet tels quels, parce que le jalon 3 est le premier moment où l'étudiant compare ses propres courbes à celles d'autrui : une condition de terminaison bien intentionnée peut enfermer un entraînement dans un minimum local, et deux simulateurs du même corps n'exposent pas le même nombre d'observations, de sorte que leurs courbes ne sont pas comparables même quand elles portent le même nom. Un chiffre de banc d'essai sans sa version d'environnement n'est pas une mesure.

Vient alors la méthode que l'étudiant utilisera, **PPO**, et la semaine la présente avant la théorie qu'elle approche, en disant que l'ordre est inversé par rapport aux dates. Le rapport entre la nouvelle et l'ancienne politique remplace la log-probabilité, et c'est l'échantillonnage préférentiel de la semaine 3 qui autorise ce remplacement : le lot survit à plus d'un pas de gradient. L'écrêtage de ce rapport aplatit l'objectif **du seul côté où la mise à jour veut aller**, et cette asymétrie est la lecture qui compte. Ce que l'écrêtage fait exactement mérite une formulation précise, parce que la formulation courante est fausse : il **retire une incitation**, il ne borne pas un pas, et une politique peut encore s'éloigner trop. L'avantage, lui, devient une somme actualisée de résidus temporels dont un paramètre règle la portée, et la valeur 1 de ce paramètre redonne exactement l'avantage de la semaine 8. Le troisième apport est procédural et c'est lui qui paie : une longue trajectoire, puis plusieurs époques de minilots sur cette même trajectoire.

**TRPO** suit, et il pose le même problème sans aucune approximation : maximiser le même objectif de substitution, sous une contrainte de divergence **moyenne** sur les états visités. La semaine écrit la divergence de Kullback-Leibler correctement et met en garde contre une formule qui circule sous son nom et qui est en réalité l'entropie croisée, reconnaissable à ce qu'elle ne contient pas de quotient. Puis viennent les quatre mouvements qui rendent le problème calculable, dont le plus instructif est une décision d'ingénierie : ne jamais former l'inverse de la matrice de courbure, qui pèserait des dizaines de gigaoctets, et obtenir le seul vecteur dont on a besoin par une méthode itérative qui ne demande que des produits matrice-vecteur. Au bout, la phrase pour laquelle l'ordre a été inversé : PPO est TRPO dont le gradient conjugué et la recherche linéaire ont été remplacés par un écrêtage.

**ACKTR** occupe la section la plus courte et la plus inhabituelle. La méthode promet la courbure du second ordre à un coût praticable ; ce qui a été mesuré est une instabilité sur les quatre configurations du banc d'essai, avec deux explications possibles que rien ne permet de séparer, un réglage insuffisant ou des erreurs dans l'adaptation d'un optimiseur tiers. La semaine rapporte ce résultat négatif tel quel, dit ce qu'il démontre et ce qu'il ne démontre pas, et en fait le modèle de ce que le jalon 3 demande.

**SAC** ferme la série, et elle vient de la semaine 9 et non de la semaine 8 : hors politique, tampon de rejeu, double Q écrêté. Sa nouveauté est que la prime d'entropie entre dans l'**objectif** lui-même, au même rang que la récompense, ce qui change les fonctions de valeur et les cibles, et ce qui la distingue de la prime d'entropie de la semaine 8, simple terme ajouté à une perte. Deux choix de politique portent le reste : un écart-type **fonction de l'état**, sans lequel l'idée perd son sens, et une action écrasée par une tangente hyperbolique, qui supprime le besoin d'écrêter et qui demande en échange une correction de densité facile à oublier.

Le module se ferme sur une mesure. Un tableau compare les cinq méthodes sur quatre configurations, et aucune ne gagne partout : une méthode excelle sur un corps et s'enferme dans un minimum local sur l'autre, et le plus mauvais chiffre de la famille sur politique est expliqué, par le texte même qui le rapporte, par une graine de départ malheureuse. La semaine apprend à lire ce tableau : une case sans nombre est une décision de rapport et non une absence d'expérience, et une colonne doit parfois être attribuée à autre chose que son titre, ce qui est le cas ici puisque les quatre chiffres de la dernière ligne ont été produits par un code sans terme d'entropie, donc par une autre méthode que celle qui les signe. Reste le compromis, et il est chiffré : la méthode hors politique atteint un même niveau avec deux fois moins d'observations, et consomme dix fois moins d'observations dans le même temps de calcul. La question à se poser avant de choisir une méthode n'est donc pas laquelle est la meilleure, c'est **ce qui est rare chez vous, le calcul ou les observations**.

La semaine porte le **jalon 3**, qui vaut 25 % de la note et qui clôt le module 3 : une méthode de politique qui apprend, une analyse de la variance de son gradient, et une comparaison avec le réseau Q profond du jalon 2 sur l'efficacité d'échantillon, la stabilité et le temps d'horloge, sur plusieurs graines avec intervalles.

---
## Mots-clés de la semaine

effondrement de la performance · pas irrécupérable · instabilité de la mise à jour de politique · espace des paramètres contre espace des politiques · région de confiance · divergence de Kullback-Leibler · entropie croisée · budget de divergence · environnements de locomotion · comparaison des simulateurs physiques · réseaux séparés pour l'acteur et le critique · variance globale de la politique · terminaison précoce par contrôle de santé · PPO · rapport entre la nouvelle et l'ancienne politique · échantillonnage préférentiel · écrêtage · objectif écrêté · retrait d'incitation · arrêt précoce sur la divergence · estimation généralisée de l'avantage · résidu temporel · normalisation de l'avantage · époques multiples sur une même trajectoire · TRPO · objectif de substitution · fréquence de visite actualisée des états · contrainte sur la divergence KL · divergence moyenne contre divergence maximale · expansion de Taylor · gradient naturel · méthode du gradient conjugué · produit hessienne-vecteur · recherche linéaire par rebroussement · ACKTR · optimisation du second ordre · approximation de la courbure par factorisation de Kronecker · information de Fisher · échec de reproduction · SAC · régularisation par l'entropie · coefficient d'entropie · reparamétrisation · politique à écart-type dépendant de l'état · correction de jacobien · double Q écrêté · comparaison des méthodes de contrôle continu · case non rapportée · graines multiples avec intervalle · efficacité d'échantillon contre temps d'horloge

---
## En prévision de la semaine suivante

La semaine 11 ouvre le module 4, et elle prend pour sujet ce que les trois semaines du module 3 ont traité comme un détail d'implémentation : **l'exploration**. Faites le compte de ce que le cours a employé jusqu'ici pour explorer. Un \(\varepsilon\) qui décroît, depuis la semaine 4. Un bruit ajouté à l'action, en semaine 9, avec une amplitude réglée à la main. Une prime d'entropie posée à côté d'une perte en semaine 8, puis la même prime déplacée dans l'objectif en semaine 10. Ces quatre mécanismes ont un point commun : ils poussent l'agent à essayer des actions **au hasard, autour de ce qu'il fait déjà**. Tant que la récompense est dense, cela suffit, et c'est pourquoi aucune de nos dix semaines n'a eu à se poser la question. La semaine 11 installe une tâche où la récompense est **rare**, où l'agent peut jouer des millions de pas sans jamais la rencontrer, et où le hasard local n'a aucune chance de la trouver. Sur une telle tâche, toutes nos méthodes échouent, et elles échouent sans aucun symptôme : la perte est saine, le gradient est propre, et la courbe de récompense est une ligne plate. Vous y verrez donc une autre idée de l'exploration, qui ne consiste plus à perturber une action mais à rendre la **nouveauté** elle-même désirable, et vous mesurerez la différence sur la seule tâche du cours qu'aucune de vos méthodes actuelles ne résout.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 11{{% /comment %}}

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF moins 31 pour LAPAN, conformément à
MAP-lapan.md, comme dans le dossier et les notes de phase 1. Toutes les pages citées
ci-dessous sont des indices PDF. Spinning Up ne se pagine pas : une page RST s'ancre par son
nom de section (SPINUP ppo/key-equations, SPINUP trpo/key-equations, SPINUP sac/key-equations),
et ses équations sont COPIÉES de son LaTeX sous licence MIT, jamais retapées, conformément au
traitement que D44 donne au LaTeX des papiers.

SEMAINE À DEUX SOURCES, CHACUNE AVEC UN SEUL MÉTIER, EXACTEMENT COMME LE DOSSIER LE PRÉVOIT.
LAPAN ch. 16 fournit le dilemme d'ouverture, le banc d'essai, les résultats mesurés, le tableau
de comparaison et le compromis qui ferme le module ; il porte l'introduction, §10.1, les
résultats de §10.2, §10.3 et §10.4, et §10.6. Les trois pages RST sous licence ouverte,
ppo, trpo et sac, délibérément laissées fermées en semaines 8 et 9, fournissent les ÉNONCÉS
corrects : la lecture par morceaux de l'objectif écrêté, la formulation sous contrainte de
TRPO, la chaîne d'approximation, et la totalité de SAC. Sans elles, deux des quatre méthodes de
la semaine ne seraient pas enseignables. Aucun nouveau papier, aucun chunk hors manifeste.

NEUF PAGES RASTÉRISÉES PENDANT LA PASSE DE LECTURE (lapan 500, 501, 503, 507, 508, 514, 515,
517, 520), SEPT OUVERTUES. Toutes les équations transcrites de ce chapitre viennent des images
de pages et non des chunks, parce que l'extraction de ce chapitre est particulièrement abîmée.
La rédaction n'est jamais retournée aux chunks pour une formule : les notes de phase 1 portent
les formes corrigées, et c'est là que la rédaction les a prises.

TROIS ERREURS IMPRIMÉES DANS LA SOURCE, CORRIGÉES ICI, ET LA CORRECTION EST SIGNALÉE UNE FOIS
DANS LA PAGE. (1) P.500 imprime gamma^(T-t+1) sur r_{T-1} là où l'exposant correct est T-t-1 ;
(2) p.501 imprime (gamma lambda)^(T-t+1) sur le dernier résidu, même correction ; (3) p.503
imprime en prose « le facteur d'actualisation gamma^lambda », lambda en exposant, à deux lignes
d'un code qui calcule gamma * gae_lambda. La passe de lecture a vérifié sur les images que ces
trois erreurs sont bien dans le livre et non dans l'extraction. Le cours enseigne les formes
corrigées et donne, dans un encadré [!WARNING] de §10.2, le contrôle arithmétique qui permet à
l'étudiant de retrouver le bon exposant de tête, ce qui est plus utile qu'une correction
silencieuse puisqu'un étudiant lisant d'autres textes rencontrera les formes fautives.

LA DIVERGENCE KL. La p.508 énonce, sous le nom de divergence KL et en formule centrée,
-somme p_i log q_i, qui est l'entropie croisée. Vérifié verbatim sur l'image pendant la passe
de lecture : le signe moins est hors de la somme et seul log q_i apparaît. Le cours n'en
transcrit RIEN : il écrit sa propre forme, somme p_i ln(p_i / q_i), depuis notation.md §3 et
depuis sa propre page de la semaine 3, et il consacre un encadré [!IMPORTANT] à la distinction
entre les deux quantités, au test de reconnaissance (une KL contient un quotient) et à la
conséquence pratique (une entropie croisée ne vaut pas zéro quand les deux lois coïncident,
donc elle ne peut pas servir de budget). L'encadré ne nomme ni auteur ni ouvrage : il dit que
la formule circule, y compris dans des textes imprimés, ce qui est vrai et vérifiable, et il
énonce la bonne forme en voix propre.

LA CONTRAINTE EST UNE MOYENNE, PAS UN MAXIMUM. La p.508 imprime la contrainte avec une barre,
donc comme une divergence moyenne, et la prose voisine l'appelle « maximum ». La formule est
juste, le mot est faux. Le cours écrit MOYENNE, suit trpo/key-equations, consacre un encadré
[!WARNING] à la différence entre les deux contraintes, et n'emploie jamais le mot « maximale »
dans ce contexte.

LA LIGNE SAC DU TABLEAU EST ATTRIBUÉE À CE QUI A TOURNÉ. Vérifié sur les images p.515 et p.517 :
la variance de la politique n'est pas paramétrée par l'état, et le code du pas d'acteur ne
contient pas le terme d'entropie et prend le PREMIER critique, ce que le texte reconnaît en
autant de mots deux paragraphes avant le titre « Results ». Les quatre nombres de cette ligne
(1 765, 7 063, 630 et une case non rapportée), la mesure d'efficacité (900 après 0,5 M
observations contre plus de 1 M) et les coûts (5 M en 10 h, 9 à 13 h par exécution) viennent
donc d'un DDPG à double Q écrêté sans terme d'entropie. Le Tableau 10-1 nomme cette ligne
« Méthode hors politique mesurée » et renvoie à une note qui l'explique en entier ; le chiffre
7 063 n'est jamais présenté comme un résultat de SAC, et la note 2 dit pourquoi. Le compromis
de §10.6 survit à cette attribution, et la page dit pourquoi : moins d'observations et plus de
calcul est une propriété du hors politique à tampon de rejeu, c'est-à-dire d'une famille, et
c'est bien cette famille qui a tourné. AUCUN autre chiffre de SAC n'est cité, et aucun n'est
inventé : la lacune 5 des notes est traitée en la nommant dans la note 2 (« si vous cherchez un
résultat publié pour la méthode de la section 10.5 elle-même, il existe, mais il n'est pas dans
ce que cette semaine a lu, et je ne vais pas l'inventer »).

INTRODUCTION. Le dilemme vitesse contre sécurité et la non-linéarité de la politique (p.492) ;
LA PHRASE CHARNIÈRE, on ne se relève pas d'une mauvaise mise à jour parce que la mauvaise
politique fournit les échantillons suivants (p.492-493) -> encadré [!IMPORTANT], reformulé en
voix propre ; le refus du petit pas d'apprentissage, qui ralentirait la convergence (p.493) ;
le nom de la famille et l'idée de contraindre en mesurant une divergence (p.493) ; la
formulation plus nette de l'espace des politiques contre l'espace des paramètres
(SPINUP trpo/background) -> encadré [!TIP] ; et la question-thèse de la semaine
(SPINUP ppo/background) -> une phrase, posée une fois. L'inversion de l'ordre PPO/TRPO est
annoncée dans un encadré [!WARNING] avec les deux dates (p.500, p.509). Les trois collisions de
notation et la libération du mot « écrêtage » viennent de notation.md et du glossaire du
projet, pas d'une source.

§10.1. Deux corps, observation articulaire, action par articulation, récompense = distance
moins énergie (p.493) -> premier titre et Figure 10-3. PyBullet déprécié et MuJoCo livré par
gymnasium[mujoco] (p.493-494) -> paragraphe d'outillage, AVEC LA CONSÉQUENCE DE COURS : le
laboratoire ne reprend pas le moteur historique, exactement comme en semaine 9. Trois écarts
avec l'A2C de la semaine 8, seize environnements, réseaux séparés, logstd global (p.494) ->
deuxième titre, fragment réécrit et tableau de symboles. Architecture 64/64, Tanh pour
l'acteur, ReLU pour le critique (p.495) ; tirage mu + exp(logstd) * rnd puis clip (p.496) ->
second fragment. Le contrôle de santé de la fourmi qui bloque l'entraînement dans un minimum
local, et la parade (p.498) ; 26 observations contre 17, et l'avertissement sur la
comparabilité (p.494, p.498) -> les deux pièges, puis la RÈGLE DE LECTURE, qui est du cours.
Débits 1600/5100 et 1400/2500, 100 M pas en 20 h, 4500 en 90 M pas, maximum publié 4000-5000
(p.497-498) ; scores de référence 2189 / 4718 / 2425 / 5380 et la courbe plate pendant 100 M
pas (p.499) -> dernier titre et encadré [!IMPORTANT] sur le critère d'arrêt.
ERREUR DE SOURCE NON REPRODUITE : p.494 écrit que c'est le CRITIQUE qui estime la moyenne et la
variance des actions. C'est l'acteur. La page écrit la chose correcte sans commentaire.

§10.2. Filiation 2017 et inversion assumée (p.500) ; le changement en une phrase, le rapport à
la place de la log-probabilité (p.500) ; l'échantillonnage préférentiel comme origine, et le
renvoi à la méthode d'entropie croisée de la semaine 3 (p.500) ; le danger de la maximisation
nue (p.500) ; la bande [1-eps, 1+eps] et le rôle de eps (p.500). Équations 10-E1, 10-E2, 10-E3,
10-E4 TRANSCRITES des images p.500 et p.505, avec les renommages du cours (A_t -> Adv_t,
r_t -> R_{t+1}, V -> v_w) ; 10-E5 à 10-E9 COPIÉES de ppo/key-equations, dont la forme par
morceaux g(eps, Adv) dont la Figure 10-01 est tracée. LA LECTURE PAR MORCEAUX, le plafond pour
un avantage positif et le plancher pour un avantage négatif (SPINUP ppo/key-equations) ->
l'asymétrie, qui est la lecture de la figure. LE RETRAIT D'INCITATION, et non la borne sur le
pas (ppo/key-equations) -> encadré [!IMPORTANT], reformulé en voix propre et donné comme la
formulation à adopter. La réserve honnête, une politique peut encore s'éloigner trop, d'où
l'arrêt précoce sur la divergence (ppo/key-equations) -> dernier titre de la section.
PPO-Penalty nommée UNE FOIS et non enseignée (ppo/background). Faits de cadrage, sur politique,
actions discrètes ou continues (ppo/quick-facts).
GAE : 10-E10 et 10-E11 transcrites des images p.500 et p.501 AVEC L'EXPOSANT CORRIGÉ, 10-E12
transcrite et RENOMMÉE de sigma_t en delta_t ; la phrase « lambda = 1 redonne l'A2C » (p.501)
est le pont, et il est argumenté depuis LA PAGE DE LA SEMAINE 8 (déroulement à N pas, §8.9), pas
depuis une source : la lacune 4 des notes est traitée ainsi. 10-E13 copiée de ppo/pseudocode.
10-E14 ÉCRITE EN FRANÇAIS en treize étapes d'après ppo/pseudocode et la narration p.501-505 ; le
bloc algorithmic du RST n'est jamais collé, KaTeX ne le rendrait pas (acquis de la semaine 9).
Implémentation : passe arrière de l'avantage en une fois (p.502), normalisation de l'avantage
(p.504), rapport par exp(logprob - old_logprob) sur un old_logprob DÉTACHÉ (p.504-505), perte
-min(...).mean() (p.505), perte de la dernière transition de la trajectoire (p.504), et les
hyperparamètres vérifiés sur l'image p.501 -> fragments et tableaux de symboles.
ERREUR DE SOURCE CORRIGÉE DANS LA PAGE : p.502 écrit qu'à un pas terminal « il n'y a pas de
récompense antérieure à prendre en compte », alors que ce qui disparaît est la VALEUR DE L'ÉTAT
SUIVANT. L'encadré [!NOTE] rétablit la bonne lecture, sans citer la source, et explique la
conséquence de code (supprimer la récompense du pas terminal supprimerait le signal le plus
informatif de l'épisode).
Résultats : 1800 entraînement / 2500 test en 25 M pas et 8 h contre la référence en 110 M pas
et 20 h, l'échec sur MuJoCo arrêté à 50 M pas et 12 h avec le guépard retourné sur le dos, et
la fourmi battue sur les deux moteurs presque deux fois plus vite (p.505-507) -> avant-dernier
titre et encadré [!IMPORTANT] sur le maximum local, qui plante l'argument des graines.

§10.3. 2015, et l'aveu que l'article est dense en mathématiques (p.507) -> ouverture. 10-E15 à
10-E17 et 10-E22 à 10-E25 COPIÉES de trpo/key-equations : la maximisation sous contrainte, l'
objectif de substitution visiblement identique à 10-E3, la divergence moyenne sur les états
visités, l'expansion de Taylor, le gradient naturel, la recherche linéaire et le produit
hessienne-vecteur. 10-E18 ÉCRITE DIRECTEMENT depuis notation.md §3. 10-E19 à 10-E21
TRANSCRITES des images p.507 et p.508 : la fréquence de visite actualisée, la forme originale de
l'objectif de substitution avec son tilde, et le rendement actualisé espéré. La remarque que
l'objectif et la contrainte sont tous deux nuls au point de départ, gradient compris
(trpo/key-equations) -> la phrase qui rend la formulation naturelle. g EST le gradient de
politique de la semaine 8 (trpo/key-equations) -> dit comme un cadeau d'économie, et c'est
exact. Le refus d'inverser H, le gradient conjugué et son unique besoin (trpo/key-equations) ->
le titre « Pourquoi un gradient conjugué », avec le calcul d'ordre de grandeur (10^10
coefficients pour 10^5 paramètres), QUI EST DU COURS et n'est tiré d'aucune source. Fragment de
code ÉCRIT POUR LE COURS : objectif de substitution sans écrêtage, KL analytique entre deux
gaussiennes diagonales, produit hessienne-vecteur par double dérivation avec amortissement ; la
source ne montre que deux fonctions et précise que son implémentation reprend celle d'un dépôt
tiers (p.508-509), ce que la page dit en voix propre, sans URL et sans nom de dépôt.
LA PHRASE DE LA SEMAINE, PPO est TRPO avec le gradient conjugué et la recherche linéaire
remplacés par un écrêtage (p.509) -> son propre titre, et c'est la récompense de l'ordre
inversé. Résultats 2419 / 5753 / 834 / 993 et le minimum local « debout sans bouger »
(p.510-511) -> dernier titre et encadré [!IMPORTANT] sur ce qu'une exécution unique autorise.

§10.4. 2017, second ordre et région de confiance combinés (p.512) ; le second ordre en un
paragraphe, hessienne prohibitive, approximations nécessaires (p.512) ; K-FAC nommée, datée, et
DÉCLARÉE HORS PORTÉE comme la source le fait (p.512) -> encadré [!NOTE] qui assume la limite,
parce que la lacune 3 des notes est réelle : aucun matériel du cours ne développe K-FAC.
10-E26 ÉCRITE DIRECTEMENT, en deux lignes, pour nommer l'information de Fisher et le gradient
naturel. Ce qui a tourné : optimiseur K-FAC d'un dépôt tiers, adapté, un backward()
supplémentaire pour collecter l'information de Fisher, critique entraîné comme dans la méthode
de référence, et aucune implémentation PyTorch native (p.512) -> esquisse de code ANNONCÉE COMME
NON EXÉCUTABLE et tableau de symboles. LE VERDICT, instabilité sur les deux environnements et
les deux moteurs, cause non établie entre réglage et bogues d'adaptation (p.513) -> rapporté
tel quel, sans adoucissement, comme le dossier l'exige. Scores 250 / 3100 / 1820 et aucune
amélioration sur la fourmi MuJoCo (p.513-514, p.520). Le dernier titre, sur ce qu'un échec de
reproduction démontre et ne démontre pas, est DU COURS, et il est explicitement relié au
jalon 3.

§10.5. Filiation et standing (p.514) ; le placement propre, politique stochastique optimisée
hors politique, pont avec les approches de type DDPG, reprise du double Q écrêté, lissage
obtenu gratuitement par la stochasticité (SPINUP sac/background) -> premier titre, qui renvoie
à LA PAGE DE LA SEMAINE 9 pour le double Q écrêté et ne le redérive pas. La régularisation par
l'entropie comme changement d'OBJECTIF, prime à chaque pas, exploration accélérée et optimum
local évité (sac/background, sac/key-equations ; p.514) -> deuxième titre, avec la DISTINCTION
EXPLICITE d'avec la prime d'entropie de la semaine 8, qui est du cours. 10-E27 à 10-E32 COPIÉES
de sac/key-equations : entropie, problème régularisé, valeur d'état, report de Bellman, cible
des deux critiques, politique reparamétrée et objectif de l'acteur. L'arbitraire du partage de
la prime entre v et q est signalé, comme la source le signale. Les trois différences avec TD3
(terme d'entropie dans la cible, action suivante tirée dans la politique COURANTE, aucun
lissage explicite) -> encadré [!IMPORTANT], présenté comme la passation entre les deux semaines.
Les deux différences de politique, tanh qui change la loi et log écart-type SORTIE DU RÉSEAU,
avec la mesure selon laquelle un écart-type indépendant de l'état ne fonctionne pas
(sac/key-equations) -> le verdict annoncé dès §10.1 sur le logstd global. La reparamétrisation
et le min sur les deux critiques dans l'objectif de l'acteur, contrairement à TD3
(sac/key-equations). alpha, ses deux variantes dont la variante à entropie contrainte préférée,
la moyenne jouée à l'évaluation et le démarrage uniforme (sac/quick-facts, sac/exploration).
Faits de cadrage : hors politique, actions continues seulement, variante discrète existante,
pas de parallélisation (sac/quick-facts). Fragment de code ÉCRIT POUR LE COURS, avec la
CORRECTION DE JACOBIEN de la tanh, qui n'est dans aucune équation de la section et qui est
indispensable : l'encadré [!WARNING] le dit et relie le piège au « mensonge discret » de §9.2.
TROIS ÉQUATIONS DE LA SOURCE DÉLIBÉRÉMENT NON ENSEIGNÉES : les quatre réseaux et les trois
cibles de p.515 décrivent la version ANCIENNE de la méthode, celle qui apprend en plus un
réseau de valeur d'état, écrivent V(s,a) deux fois pour un réseau qui ne prend que l'état, et
donnent un objectif d'acteur sur Q_1 seul. La page enseigne la formulation moderne et mentionne
en une phrase que la version à quatre réseaux existe et qu'elle est plus ancienne, ce qui est
la différence entre une erreur et une date.
ERREUR DE SOURCE NON REPRODUITE : p.514 imprime le problème régularisé avec argmax_a là où la
maximisation porte sur la politique. 10-E28 porte argmax_pi.

§10.6. Tableau 16.1 RETYPÉ comme tableau Markdown du cours, cellule par cellule depuis l'image
p.520, le gras du meilleur par colonne conservé, les deux cases dashées remplacées par
« non rapporté » et renvoyées à une note. Ce n'est pas une omission mais une décision : un
tableau de résultats mesurés est du FAIT et non de l'EXPRESSION, et les tableaux ne sont jamais
des images (D19). Recoupement des vingt cases avec les scores donnés méthode par méthode
(p.499, p.507, p.511, p.519). La conclusion de la source sur son propre tableau, aucune méthode
gagnante, A2C et PPO réguliers, et LA PARENTHÈSE SUR LA GRAINE (p.520) -> encadré [!IMPORTANT]
qui en fait l'argument des graines multiples. Les deux cases non rapportées, documentées par la
prose de p.513 (aucune amélioration) et p.518-519 (politique qui tient à peine debout) -> la
note 1 et la RÈGLE DE LECTURE sur les trois situations qu'une case vide peut cacher, qui est du
cours. La note 2 traite l'attribution, voir plus haut. Efficacité mesurée, 900 après 0,5 M
contre plus de 1 M ; coûts, 5 M en 10 h contre 50 M pour la référence, et 9 à 13 h par
exécution ; LA RÈGLE QUI FERME LE MODULE, observations bon marché contre observations coûteuses
(p.517) -> Figure 10-04 et encadré [!IMPORTANT]. Le dernier titre, sur ce que vingt cases sans
intervalle démontrent, est du cours et prépare le barème du jalon.

LABORATOIRE. Trois volets sur `Pendulum-v1`, un seul socle, trois drapeaux (COURSE-PLAN §2
wk 10 : régler eps, lambda et les époques, puis une méthode hors politique sur le même
environnement ; §9.2 : semaine faisable sans réserve). Les chiffres du chapitre, 8 à 20 h par
exécution et 10 h pour 5 M transitions hors politique (p.497, p.517), sont donnés comme des
repères à décrire et JAMAIS comme une tâche. LACUNE 7 DES NOTES TRAITÉE EXPLICITEMENT : aucun
résultat publié n'existe, dans ce que la semaine a lu, pour PPO ou pour une méthode hors
politique sur une tâche de cette taille, donc le laboratoire exige une EXÉCUTION PILOTE et une
cible annoncée par l'étudiant, et la page ne cite aucun score à atteindre. Les deux budgets de
pas du fragment Stable-Baselines3 sont explicitement déclarés non prédictifs. Diagnostic propre
à la semaine, divergence moyenne par époque et fraction d'échantillons écrêtés, construit sur
l'arrêt précoce de ppo/key-equations. Code du cours en PyTorch et Gymnasium seulement, réécrit
et jamais recopié d'un dépôt (D15, et le chapitre reconnaît lui-même que ses implémentations de
TRPO et d'ACKTR viennent d'un dépôt tiers, raison supplémentaire de ne pas s'en approcher).

JALON 3. A2C/PPO, ou une méthode hors politique pour les actions continues, plus l'analyse de
variance du gradient, plus la comparaison avec le réseau Q profond du jalon 2 sur l'efficacité
d'échantillon, la stabilité et le temps d'horloge (COURSE-PLAN §10). Graines multiples avec
intervalles, acquis depuis le jalon 2. Le barème en huit lignes somme à 25. LES DEUX ROUTES
SONT UNE DÉCISION DE RÉDACTION : la comparaison avec une méthode de valeur exige un espace
d'actions discret, donc la route 1 mesure sur `CartPole-v1`, où le code du jalon 2 est déjà
mesuré, et la route 2 passe par la DISCRÉTISATION d'une dimension d'action unique, solution que
LA PAGE DE LA SEMAINE 9 (§9.1) a déjà déclarée praticable sur une ou deux dimensions. Le
protocole de mesure de variance renvoie à LA PAGE DE LA SEMAINE 8 (§8.6), pas à une source. La
structure du brief et la phrase sur le résultat nul correctement établi reprennent le jalon 2
de la semaine 7, cité comme page du cours.

CE QUE LA SEMAINE N'A PAS UTILISÉ, ET POURQUOI. Aucune courbe d'entraînement du chapitre : les
figures 16.2 à 16.20 sont toutes des tracés des exécutions de la source, exclues par la règle
posée en semaines 2 et 3. La liste « DO NOT read » du dossier a été respectée en entier :
lapan/ch17 (stratégies d'évolution) et lapan/ch18 (exploration avancée) sont restés fermés, les
chunks td3/* et td3.rst aussi, vpg.rst et ddpg.rst aussi, sb/ch13 aussi, et aucun listing de
code du chapitre 16 au-delà des trois chunks du manifeste n'a été ouvert. LE CROCHET DE LA
SEMAINE 11 N'EST PAS DÉPENSÉ : la prime d'entropie de §10.5 est présentée comme un changement
d'objectif, et jamais comme une méthode d'exploration avancée ; la page d'accueil annonce la
semaine 11 par la RÉCOMPENSE RARE et par l'idée de rendre la nouveauté désirable, sans nommer
aucun mécanisme. TD3 entre dans la semaine par la page de la semaine 9 et par elle seule.

DÉCOMPTE : 6 sections numérotées · 4 placeholders FIG (dont 3 figures du cours, deux déjà
produites et une à produire) · 0 placeholder EQ (32 équations identifiées, 10-E1 à 10-E32,
toutes écrites directement en KaTeX dans la page, et réparties ainsi d'après la colonne
« régime » des notes de phase 1 : 19 COPIÉES du LaTeX des pages RST sous licence MIT (E5, E6,
E7, E8, E9, E13, E15, E16, E17, E22, E23, E24, E25, E27, E28, E29, E30, E31, E32), 10
TRANSCRITES d'images de pages vérifiées (E1, E2, E3, E4, E10, E11, E12, E19, E20, E21), dont
trois avec une correction d'exposant ou un renommage, et 3 ÉCRITES DIRECTEMENT depuis la
notation du cours ou rendues en français (E14, E18, E26). Une équation de plus ne porte pas
d'identifiant parce qu'elle est du vocabulaire du cours et non une formule à reproduire au
symbole près : la forme analytique de la divergence entre deux gaussiennes diagonales, donnée
en commentaire dans le fragment de §10.3. L'inventaire complet, avec le régime de chacune, est
dans extraction/week-10.md)
{{% /comment %}}
