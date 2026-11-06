---
title: "Semaine 12 : Auto-jeu, planification et multi-agent"
weight: 12
bookCollapseSection: true
---

# Semaine 12 : Auto-jeu, planification et multi-agent

Pendant onze semaines, nos agents ont appris en agissant : pour savoir qu'une action mène à une catastrophe, il fallait la jouer. Aucun n'a jamais demandé ce qui arriverait si. Cette semaine donne à l'agent un modèle du monde et l'autorise à chercher dedans avant de jouer : trois statistiques par arête, quatre phases, un signe qui s'inverse à chaque niveau de la remontée, et une partie contre soi-même pour produire ses propres données. Puis elle pose la question difficile, celle qui fait tout l'intérêt du sujet : et si le modèle devait être **appris** ? Un réseau devient trois, la recherche se déroule dans un état caché que personne ne peut interpréter, et le résultat obtenu est un échec qu'il faut savoir lire. La semaine se termine en mettant plusieurs agents dans le même monde, ce qui casse une hypothèse que ce cours tient depuis la semaine 1 sans l'avoir jamais discutée : que l'environnement reste immobile pendant que vous apprenez. La semaine ne porte aucun jalon.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** chercher dans un modèle remplace l'expérience par du calcul, à une condition que les interfaces habituelles ne remplissent pas, celle de pouvoir repartir d'un état choisi ; et dès que l'adversaire apprend aussi, il n'y a plus d'objectif fixe à descendre, ce qui rend une perte plate non pas suspecte mais attendue.

---
## Description générale

La semaine commence par une restriction volontaire. Un modèle de l'environnement achète exactement deux choses, l'efficacité en échantillons et la transférabilité d'un objectif à un autre, et la semaine refuse d'en nommer une troisième : elle construira d'ailleurs un modèle dont l'état interne est un vecteur de soixante-quatre nombres que personne ne peut interpréter, ce qui règle la question de l'interprétabilité. Elle note au passage que la frontière entre « un environnement » et « un modèle » est plus mince que le vocabulaire ne le suggère, puisque tous les simulateurs employés depuis la semaine 1 sont déjà des modèles du monde.

Le jeu de plateau arrive comme cas d'étude, et il inverse la situation des jeux vidéo : les règles sont compactes, la position est entièrement observable, et ce qui fait la difficulté est le nombre de positions et surtout un adversaire dont la stratégie est inconnue. Cette observabilité rend possible l'analyse d'une position, qui est exactement ce qu'un modèle du jeu autorise, et les ordres de grandeur ferment la porte de l'énumération : le morpion est résoluble entièrement avec ses cent trente-huit états terminaux, Puissance 4 compte environ quatre mille milliards de positions, et les dames en comptent cinq cent milliards de milliards.

La recherche arborescente occupe le cœur de la semaine. Chaque arête porte trois nombres, une probabilité a priori fournie par le réseau, un comptage de visites et une valeur moyenne, et la descente suit une utilité qui additionne la valeur observée et une prime d'exploration. La semaine insiste sur un facteur de cette prime, la racine carrée du total des visites du nœud, parce qu'une version amputée de ce facteur circule : sans lui, la prime décroît en \(1/N\) sans rien qui la pousse en retour, et la recherche dégénère silencieusement en descente gloutonne qui n'explore plus rien. Quatre phases se succèdent, sélection, expansion, évaluation et remontée, et c'est la remontée qui demande le plus d'attention, car le signe de la valeur s'inverse à chaque niveau : les deux joueurs alternent, et une position excellente pour l'un est détestable pour l'autre. C'est minimax, écrit comme une accumulation.

Le dispositif complet y ajoute l'auto-jeu. Un meilleur réseau joue les deux camps et produit les données, un apprenti s'entraîne dessus sans jouer, et une porte d'évaluation, cent parties et plus de soixante pour cent de victoires, décide de son éventuelle promotion. La semaine prend alors à son compte un fait que onze semaines d'habitudes rendent déconcertant : **la perte ne mesure rien**. Le producteur des données change à chaque promotion, donc les cibles changent, donc la courbe n'a aucune tendance ; et le taux de victoire contre le meilleur réseau reste structurellement autour d'un demi, puisque l'adversaire redevient aussi fort à chaque fois qu'il est dépassé. Le progrès existe pourtant, et il se constate par un tournoi entre points de contrôle, où les réseaux récents battent les anciens. Généralisation à retenir : quand l'adversaire est une copie de vous-même, il n'y a aucun objectif fixe à descendre.

Entre les deux, une section isole la contrainte la plus transposable de la semaine. Une recherche doit pouvoir dire à son modèle « place-toi dans cette position », des centaines de fois par coup, et l'interface standard d'un environnement d'apprentissage par renforcement ne le permet pas : elle laisse avancer, et seulement avancer. D'où un modèle de jeu écrit à la main, en cinq fonctions, et un encodage de position en soixante-trois bits, car la mémoire est ici la ressource qui limite la qualité du résultat.

La seconde moitié apprend le modèle. Trois réseaux remplacent le simulateur exact : une représentation qui transforme l'observation réelle en état caché, une dynamique qui avance d'un pas dans l'espace caché en prédisant une récompense, et une prédiction qui rend une politique et une valeur. La recherche ne touche plus jamais le monde. Rien n'oblige l'état caché à ressembler à une position, et il ne ressemble à rien : deux états cachés ne sont pas même comparables, de sorte que l'arbre cesse d'être un dictionnaire indexé par l'état pour devenir un graphe d'objets. L'entraînement se fait par un déroulement de cinq pas depuis un décalage aléatoire, avec trois cibles empilées, et c'est le seul endroit où le modèle appris est entraîné : par ses conséquences, jamais contre un état réel. La semaine signale deux constantes qu'il ne faut pas recopier, dont un horizon de coups qui, par une priorité d'opérateurs, vaut cinq là où onze était voulu, alors qu'une partie de Puissance 4 ne peut pas être gagnée en moins de sept coups.

Le résultat de cette seconde méthode, mesuré, est un échec : quinze heures d'entraînement, et les deux meilleurs réseaux sont les points de contrôle numéro dix et numéro quinze sur près de deux cents. La semaine le rapporte comme la semaine 10 avait rapporté un résultat comparable, et elle délimite la conclusion : une mise en œuvre, un petit jeu, des hyperparamètres non réglés, et rien de tout cela ne dit quoi que ce soit sur la méthode, qui détient par ailleurs l'état de l'art sur cinquante-sept jeux vidéo. L'écart entre une méthode et sa reproduction est la leçon de cette section.

La semaine se termine avec plusieurs agents dans le même monde, et une distinction qui décide de tout : des agents hors de votre contrôle qui n'apprennent pas s'absorbent dans l'environnement et ne changent rien, tandis que des agents qui apprennent en même temps que vous changent tout. Le cours doit inventer la notation de ce cas, car il n'en existe aucune, et le nombre d'agents y porte un indice de temps parce qu'il diminue en cours d'épisode pendant que l'épisode continue. L'expérience concrète est une forêt de prédateurs et de proies où quarante tigres poursuivent deux cent quatre cerfs, avec une interface faite de cinq dictionnaires et une observation égocentrée relative au groupe qui permet à une seule politique de servir deux groupes opposés. La méthode d'apprentissage, elle, est celle de la semaine 5, appliquée sans y changer une ligne : ce qui devient multi-agent est l'environnement, et c'est à la fois la leçon et le plafond. Un épisode purement aléatoire laisse trois proies mangées sur deux cent quatre ; une heure d'entraînement en fait manger cent cinquante-cinq, ce que la semaine reconstruit par deux divisions à partir de la structure de la récompense. Une configuration où un prédateur isolé ne peut rien obtenir fait apparaître des chasses en couple, et la semaine sépare avec soin ce qui est certain, à savoir que la règle rend le couple obligatoire, de ce qui est seulement observé. Enfin, les deux groupes apprennent en même temps, les courbes perdent toute tendance, et la semaine nomme le phénomène : la non-stationnarité, qu'elle distingue de la triade fatale de la semaine 5 comme un mécanisme différent produisant la même signature, à cette différence près qu'aucun réseau cible ne peut figer ce qui bouge dans les poids de quelqu'un d'autre.

---
## Mots-clés de la semaine

méthode avec modèle · efficacité en échantillons · transférabilité entre objectifs · jeu de plateau · minimax · facteur de branchement · élagage de l'arbre · recherche arborescente de Monte-Carlo · nœud · arête · feuille · probabilité a priori · comptage de visites · statistique de recherche · utilité de sélection · constante d'exploration · sélection · expansion · évaluation · remontée de la valeur · inversion du signe · bruit de Dirichlet à la racine · concentration de Dirichlet · masquage des coups illégaux · recherche par petits lots · accès à un état arbitraire · modèle de jeu écrit à la main · encodage compact d'une position · réseau à deux têtes · tête de politique · tête de valeur · invariance au joueur · auto-jeu · température sur les comptages · triplets d'entraînement · porte d'évaluation · perte sans information · tournoi entre points de contrôle · réseau de représentation · réseau de dynamique · réseau de prédiction · état caché · modèle appris · déroulement sur cinq pas · cibles empilées · priorité d'opérateurs · reproduction contre méthode · apprentissage par renforcement multi-agent · action jointe · politique partagée · population volatile · observation égocentrée · relatif au groupe · prédateur-proie · inanition · collaboration imposée · comportement émergent · non-stationnarité

---
## En prévision de la semaine suivante

La semaine 12 a appris un modèle pour **chercher dedans** : trois réseaux, un arbre, et une décision prise avant d'agir. La semaine 13 garde le modèle appris et change ce qu'on en fait. Au lieu de planifier avec lui, l'agent va **apprendre à l'intérieur de lui** : la politique ne sera plus entraînée sur l'expérience réelle mais sur une expérience imaginée par le modèle, ce qui déplace la question de l'efficacité en échantillons que la section 12.1 a posée comme première motivation. Vous verrez pourquoi cette idée oblige à traiter sérieusement une chose que cette semaine a pu ignorer, l'erreur du modèle et son accumulation le long d'une trajectoire imaginée. Et la semaine 13 posera une seconde question, plus radicale encore que celle de cette semaine : que peut-on apprendre d'un jeu de données déjà collecté, sans interagir du tout avec l'environnement ? Gardez en tête la leçon de la section 12.8 : vous allez rencontrer des méthodes dont les résultats annoncés sont impressionnants, et la question à se poser en les lisant est toujours la même, sur quoi et par qui elles ont été mesurées.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 13{{% /comment %}}

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF moins 31 pour LAPAN, conformément à
MAP-lapan.md, comme dans le dossier et les notes de phase 1. Toutes les pages citées
ci-dessous sont des indices PDF.

SEMAINE À DEUX CHAPITRES, ET ILS NE SONT PAS ÉGAUX. LAPAN ch. 20 porte la semaine et a été lu
presque entier (12 items : un résumé de chapitre et onze chunks) ; LAPAN ch. 22 a été lu depuis
son résumé plus trois chunks seulement (D41), parce qu'il n'a AUCUNE équation, AUCUNE méthode
nouvelle, et que son chunk d'implémentation est bâti entièrement sur PTAN, que ce cours
n'enseigne qu'en semaine 6 et n'adopte jamais (D12). Total mesuré de la passe de lecture :
environ 27 200 tokens, 14 chunks et deux résumés de chapitre, sous la cible de ~35 000.
Aucun chunk hors manifeste. ch20/20-09, ch20/20-11 et ch22/22-03 n'ont PAS été lus comme
chunks ; les pages 625, 633 et 634, qui tombent dans les deux premiers, ont été ouvertes comme
IMAGES pour les trois vérifications d'erreurs et pour rien d'autre.

DOUZE PAGES RASTÉRISÉES ET OUVERTES PENDANT LA PASSE DE LECTURE (lapan 606, 612, 616, 623, 624,
625, 633, 634, 681, 683, 688, 690). Toutes les équations, toutes les constantes et tous les
nombres de cette page viennent des arbitrages de index/notes/week-12.md, rendus sur ces images,
et JAMAIS d'un chunk ni d'un résumé de chapitre. La rédaction n'est retournée à aucune page.

SIX CORRECTIONS DE FOND, ET CHACUNE EST PORTÉE PAR LA PAGE SANS QUE L'ÉTUDIANT APPRENNE QU'UNE
SOURCE EXISTE (D45).

(1) L'UTILITÉ DE SÉLECTION, §12.3. La p.606 imprime, en mathématiques affichées,
Q(s,a) + P(s,a)/(1+N(s,a)) : ni c_puct, ni la racine du total des visites. Ce n'est pas un
artefact d'extraction, c'est ce que la page dit, et la vérification 1 des notes l'a établi sur
l'image. La forme enseignée est celle du CODE de la p.612 (total_sqrt = m.sqrt(sum(counts)) et
value + self.c_puct*prob*total_sqrt/(1+count), avec c_puct: float = 1.0 jamais réglé). La page
écrit la forme correcte, puis dit dans un [!WARNING] que la version amputée « circule » et
décrit exactement ce qu'elle produit (prime en 1/N, descente gloutonne silencieuse). Aucune
attribution, aucun guillemet : la mise en garde est à la première personne du cours.

(2) L'HORIZON DE COUPS, §12.7. `max_moves: int = game.GAME_COLS * game.GAME_ROWS >> 2 + 1`
s'évalue en Python à (42) >> (2+1) = 5, là où (42 >> 2) + 1 = 11 était visé, car + lie plus fort
que >>. La page donne l'évaluation, l'intention, le correctif (deux parenthèses) et surtout
l'argument qui compte : une partie de Puissance 4 ne peut pas être gagnée en moins de SEPT
coups joués, donc 5 est sous le minimum absolu du jeu. Conformément au point 2 des lacunes des
notes, le laboratoire fait DÉRIVER l'horizon par l'étudiant et ne réutilise pas l'expression,
même corrigée, parce que son unique site d'emploi est dans le chunk 20-11 non lu.

(3) L'ORDRE D'EXPANSION D'UN NŒUD, §12.6. Les p.633-634 appliquent models.pred au `parent.h`
AVANT models.dynamics, ce qui produit une désalignement à TROIS branches : priors en
pi(.|s^k), valeur retournée v(s^k), tandis que node.h et node.r valent correctement s^{k+1} et
r^{k+1} ; `backpropagate` faisant `value = node.r + discount * value`, la récompense et la
valeur viennent de deux indices différents et la somme télescopique est cassée. La page
enseigne UNIQUEMENT l'ordre correct (dynamique puis prédiction sur l'état caché du nœud) et ne
reproduit pas la forme fautive, conformément au point 3 des lacunes. Elle explique en plus
pourquoi l'erreur survit : la racine, qui n'a pas de parent, est forcément correcte, donc
l'endroit que l'on inspecte fonctionne. (La page ne mentionne pas `make_expanded_root()` :
l'argument est reformulé comme une propriété de la racine, ce qui est vrai indépendamment du
code et évite de désigner une source.)

(4) LA CONCENTRATION DE DIRICHLET, §12.3. p.612 imprime [0.03]*GAME_COLS et p.625
dirichlet_alpha: float = 0.3 POUR LE MÊME JEU À SEPT COLONNES. La page tranche 0,3, donne la
raison (alpha_Dir varie à l'inverse du facteur de branchement : 0,03 au go, 0,15 au shogi,
0,3 aux échecs dont le branchement est ~35 ; Puissance 4 vaut 7), dit ce que 0,03 fait
concrètement sur sept catégories (tirage presque unitaire, un quart de budget de bruit versé
sur une colonne au hasard), et dit qu'AUCUNE des deux valeurs n'a été réglée pour ce jeu. Les
poids de mélange 0,75 / 0,25 sont identiques sur les deux pages, donc écrits sans réserve.
Le volet C fait mesurer la différence en trois lignes, sans entraînement.

(5) LE COÛT EN SANTÉ D'UN PAS, §12.10. La p.681, qui est DANS un chunk lu (ch22/22-02),
imprime 0,1 ; la p.688 imprime 0,5 et toute son arithmétique exige 0,5 trois fois (8 santé = 16
pas, 10 santé = 20 pas, 2480/16 = 155 proies, soit ~76 %), et la course aléatoire de la p.682,
où les tigres meurent à 21 pas, le confirme indépendamment (10 / 0,5 = 20). LA PAGE EMPLOIE 0,5
PARTOUT et ne cite jamais 0,1. Le tableau des règles de survie de §12.10 et l'arithmétique des
155 proies reposent tous deux sur cette valeur.

(6) LES RÉSULTATS QUI NE REPOSENT QUE SUR UNE VIDÉO, §12.11. Le chapitre 22 porte cinq liens
vidéo (et non six, comme notre résumé de chapitre l'affirmait) et TROIS affirmations ne
reposent que sur l'un d'eux : la chasse en couple (p.691), les 53 cerfs survivants (p.690) et
les cerfs qui dérivent vers la gauche (p.693). Une vidéo n'est ni republiable ni citable (D17).
Option 1 du jugement des notes, appliquée telle quelle : la page énonce d'abord le fait
STRUCTUREL imprimé à la p.690, à savoir qu'une attaque solitaire est sans effet et donc que
toute chasse réussie est par définition un couple simultané, comme un énoncé certain du cours ;
puis elle rapporte le comportement observé EN NOMMANT SON NIVEAU DE PREUVE (une observation
visuelle d'une exécution, ni mesurée ni reproductible). Même traitement pour la dérive vers la
gauche. LES 53 CERFS SURVIVANTS NE SONT PAS PUBLIÉS : ils contrediraient de quatre unités le
calcul des 155 proies, et le seul des deux nombres qui soit une mesure est le calcul. La page ne
mentionne pas ce désaccord, qui ne s'énoncerait pas sans désigner une source.

TRACABILITÉ, SECTION PAR SECTION.

Introduction. La phrase charnière multi-agent vient de LAPAN ch.22 p.675 et sert d'ouverture
plutôt que de conclusion, afin que §12.9 n'ait plus qu'à la formaliser. La stationnarité est
citée de la semaine 1 (glossaire : « stationnarité », semaine 1) et sa rupture est annoncée
comme la vraie nouveauté de la semaine. Les trois collisions de symboles sont tranchées DANS LA
PAGE : Q comme statistique de recherche (D43 ; les notes exigent la phrase « une fois, tôt »),
tau contre le tau de mise à jour douce de la semaine 9 (vérifié dans raw-content/week-09.md),
et alpha_Dir comme quatrième sens d'alpha après le pas d'apprentissage (notation.md §4) et
alpha_PER (semaine 6). Le tableau des seize symboles annonce la section de première apparition
de chacun. Les six lignes multi-agent sont déclarées création du cours, comme notation.md §3bis
les déclare.

§12.1. Taxonomie et « 100 % sans modèle » (p.601), définition du modèle de l'environnement
(p.601), les DEUX motivations et l'argument robotique (p.602), les simulateurs déjà-modèles
(p.601-602), le prix annoncé d'avance (p.600). Le [!TIP] qui REFUSE une troisième motivation
est une position du cours, pas une affirmation du matériel : il est gagé sur §12.6, où l'état
caché est effectivement non interprétable, de sorte que le refus est démontré dans la page
elle-même.

§12.2. Inversion par rapport aux jeux vidéo et analyse de position (p.602), minimax en une
phrase et pas d'équation (p.603 ; décision des notes : écrire min/max ouvrirait l'élagage
alpha-bêta), les nombres (138 états terminaux, 9! = 362 880, 5e20 pour les dames, 4,5e12 pour
Puissance 4 : p.603, p.605, p.608), le facteur de branchement et ses exemples (p.605), l'élagage
avec évaluateur écrit à la main (p.603, p.605). Le tableau est une table Markdown du cours
(D19 : une table n'est jamais une image).

§12.3. Les trois composantes (p.603-604) ; AlphaGo Zero, le go sans connaissance humaine, puis
échecs et shogi contre Stockfish (p.603-604), énoncés comme faits du cours, SANS la référence
Nature 2017 et sans guillemets (D18, D45) ; P, N, Q par arête et la création d'un nœud à N=0,
P=p_net, Q=0 (p.606 image) ; 12-E1 depuis le CODE de la p.612 (image) ; la remontée et
l'inversion de signe (p.615, p.606 image) ; 1 000-2 000 recherches par coup et les comptages de
racine comme politique (p.606 image) ; bruit de Dirichlet à la racine seule et mélange
0,75/0,25 (p.612, p.625, p.633 images) ; masquage à -inf avant l'argmax (p.612-614, image 612) ;
MCTS par petits lots et SON COÛT HONNÊTE, moins efficace qu'en série parce que le premier lot ne
peut étendre que la racine (p.613) ; états terminaux jamais rangés dans les statistiques
(p.613). Le rapprochement avec l'exploration dirigée de la semaine 11 cite la page de la
semaine 11, jamais ch.18.

§12.4. La phrase pivot sur l'impossibilité de spécifier l'état de départ (p.609) ; la mémoire
comme ressource contraignante et les 63 bits (p.609-610) ; les cinq fonctions et les quatre
constantes, RENOMMÉES EN FRANÇAIS (D15 : aucun identifiant du dépôt n'est publié) ; le match nul
non signalé par move() et détecté par possible_moves() (p.610) ; le réseau à deux têtes, la
valeur non actualisée et la raison (déterminisme ; backgammon comme contre-exemple) (p.606-607) ;
les deux plans 6x7 et l'invariance au joueur, six couches résiduelles, sept logits, un flottant
(p.616 image). Le rappel que ce réseau est celui de la semaine 8 est une citation de la page de
la semaine 8.

§12.5. Meilleur réseau / apprenti / porte (p.603-604, p.619) ; 12-E2 et le commutateur tau
(p.616 image, p.607) ; les triplets (s_t, pi_t, r_t) et la perspective du joueur du pas t, avec
le retournement du résultat en remontant l'historique (p.607, p.618) ; perte à deux termes, EQM
sur la valeur et entropie croisée sur la politique (p.607, p.619) ; la porte 100 parties / 60 %
(p.619) ; les réglages du laboratoire, 10 recherches de mini-lot 8 par coup, une heure et 2 500
parties, niveau en dessous d'un enfant avec une erreur grossière un coup sur deux (p.619) ; le
NON-RÉSULTAT, deux entraînements à 0,1 et 0,001, DIX heures et 40 000 parties CHACUN (donc une
vingtaine d'heures pour les deux : point 10 des lacunes des notes, notre résumé de chapitre
disait 10 h pour l'ensemble), taux de victoire autour de 0,5 avec pointes à 0,8-0,9, perte sans
tendance (p.619-620) ; la qualité qui monte avec l'indice du point de contrôle et NEUF des dix
premiers au pas 0,001 dans le tournoi croisé (p.621-622). Les figures 20.3, 20.4 et 20.5 ne
sont PAS extraites : le texte porte les nombres, et onze semaines sans publier une courbe
d'entraînement de la source font précédent. L'énoncé « quand l'adversaire est une copie de
vous-même, il n'y a aucun objectif fixe à descendre » est une formulation du cours, demandée
par les notes et par le dossier.

§12.6. La levée de l'exigence d'un modèle exact, les records au go/échecs/shogi et l'état de
l'art sur 57 jeux Atari (p.622-623, image 623) ; les trois services que le modèle de jeu rendait
(p.623 image) ; 12-E4, les trois fonctions, vérifiées sur les images de p.623 et de la fig. 20.6
p.624 ; 800 recherches par coup (p.623-624 images) ; l'état caché de 64 dimensions, sans
contrainte de ressemblance, deux états non comparables, l'arbre devenu graphe d'objets (p.629,
résumé p.626) ; remontée contre rétropropagation (p.624 image) ; les trois réseaux comme objets
(p.629-632), réécrits en français et simplifiés (D15) ; l'ordre d'expansion correct (voir
correction 3) ; 12-E6, la remontée avec récompense, d'après le code de la p.634 (image) avec
gamma = 1,0 (p.625 image). L'avertissement « état caché n'est pas couche cachée » répond à la
collision signalée dans les notes contre « couche cachée » (glossaire, semaine 2).

§12.7. Génération d'épisodes, action réellement jouée dans l'environnement réel, nouvelle racine
(p.624 image) ; décalage aléatoire et déroulement de cinq pas, lot = liste de tenseurs par pas
(p.624-625 images, p.637) ; 12-E5 et ses trois cibles, dont z_k la somme actualisée jusqu'à la
fin de l'épisode et u_k la récompense immédiate (p.625 image, p.639) ; la chaîne h puis K fois
{f, g} comme SEUL endroit d'entraînement du modèle, jamais contre un état réel (p.625 image,
p.639) ; les hyperparamètres imprimés (p.625 image) ; la pondération 0,5 et la différence NON
ÉQUIVALENTE avec la mise à l'échelle du gradient de la méthode d'origine, qui se compose dans la
récurrence (p.625 image, p.639) ; impossibilité du mini-lot ici, la recherche étant déterministe
(résumé p.635). Le terme « déroulement » est celui de la semaine 6 (glossaire), pas un néologisme.

§12.8. 15 h, 3 400 épisodes, pertes sans tendance (p.640) ; près de 200 points de contrôle, les
deux premiers du tournoi étant les numéros 10 (339-41) et 15 (298-82), le troisième étant le 155
(p.640) ; mauvaise convergence et très peu de réglage, rapportés comme un diagnostic de celui
qui a mesuré et non comme une vérité du cours (p.640) ; la généralisation réelle mais non
vérifiée ici, Atari laissé en exercice (p.641). Les identifiants de points de contrôle de la
console ne sont PAS recopiés : les numéros sont rapportés en prose, comme en semaine 11 (D45).
Le parallèle avec la semaine 10 cite la page de la semaine 10.

§12.9. La phrase charnière et l'absorption dans l'environnement (p.675) ; les cadres concrets,
échecs, simulation de marché, unités de jeux de stratégie, et les applications nommées, enchères,
réseaux, objets connectés (p.674-675) ; compétitif / collaboratif et les mélanges (p.675) ; le
comportement émergent du cache-cache, barrière puis trampoline, RAPPORTÉ SANS SA RÉFÉRENCE
(Baker et al. n'est pas nommé : D18) et explicitement donné comme un plafond que la semaine NE
démontre PAS (p.675) ; la théorie des jeux déclinée, et la page la nomme comme sa propre lacune
plutôt que comme celle d'une source (p.675-676) ; la simplification de la politique partagée et
« seul l'environnement a besoin d'un prétraitement » (p.674) ; 12-E7, création du cours, ajoutée
à notation.md §3 bis avant la rédaction ; 12-E9, la cible à un pas CITÉE de raw-content/week-05.md
et jamais de LAPAN, avec les exposants d'agent ajoutés.

§12.10. Rareté des environnements multi-agents (p.676) ; MAgent / MAgent2, Farama Foundation,
`pip install magent2==0.3.3`, PettingZoo nommé et non employé (p.676-677) ; le monde, les groupes,
le cœur C++, les murs, 40 tigres et 204 cerfs sur 64x64 (p.676-679) ; l'interface à cinq
dictionnaires, reset() à une seule valeur, 244 agents à la réinitialisation, enveloppes
d'enregistrement inutilisables (p.679-681, image 681) ; la population volatile (p.681 image) ;
l'observation (9,9,5) / Discrete(9) et (3,3,5) / Discrete(5), l'agent au centre, les cinq plans,
et le fait que les plans « mon groupe / groupe adverse » permettent UNE politique pour DEUX
groupes (p.680) ; la mini-carte désactivée et l'hypothèse de la vue limitée, donnée comme
hypothèse (p.680, p.688 image) ; la conception des récompenses, +1 par pas aux deux groupes et
pression par le métabolisme (p.678, p.688 image) ; l'épisode aléatoire, inanition, 30-40 pas, 21
pas de vie, 204 vs 40 puis 201 vs 1 (p.681-683 images, p.682) ; l'heure de GPU, le score de test
82,89 et l'arithmétique des 155 proies refaite dans la page (p.688 image, p.690 image). Le coût
par pas est 0,5 (voir correction 5). La console de la p.682 n'est pas recopiée.

§12.11. `--mode double_attack` comme seule différence de configuration, attaque solitaire sans
effet, code d'entraînement inchangé (p.690 image) ; après deux heures la récompense monte encore,
jamais plus de 300 pas, perte qui ne descend pas, lecture en termes d'hyperparamètres donnée
comme hypothèse (p.691) ; les couples (voir correction 6) ; les deux groupes entraînés ensemble,
deux réseaux, filter_group=None, un tampon partagé scindé en deux lots, tigres qui plafonnent
(p.692) ; les courbes de test sans tendance et la victoire des cerfs par égalité de vitesse
(p.692-693) ; les cerfs qui vont tous à gauche, rapporté avec son niveau de preuve (p.693) ; la
liste de ce que le chapitre ne couvre pas, POMDP, exploration par comptage, mémoire, efficacité
en échantillons, convertie en inventaire des lacunes DE LA SEMAINE (résumé p.694-695). La
NON-STATIONNARITÉ est nommée par le cours : le chapitre la démontre deux fois et ne la nomme
jamais. Le rapprochement avec la triade fatale cite la page de la semaine 5 et insiste sur la
différence de mécanisme, comme le dossier l'exige.

LABORATOIRE. COURSE-PLAN §2 wk 12 offre le jeu de plateau OU le monde multi-agent ; le choix du
jeu de plateau est celui du dossier et des notes, pour deux raisons écrites dans la page :
magent2==0.3.3 est un paquet à cœur C++ épinglé dont l'installation sur Colab N'EST PAS
VÉRIFIÉE (point 8 des lacunes), et les exécutions multi-agent coûtent une à deux heures de GPU.
Le volet D est donc un exercice de lecture et d'analyse, et la page LE DIT au lieu d'omettre le
sujet. Les réglages économiques (10 recherches, mini-lot 8, une heure, 2 500 parties) viennent de
la p.619. Les trois tests d'isolation du volet A, l'ablation volontaire de l'utilité, les trois
mesures du volet C et les six questions du volet D sont une conception du cours. Tout le code du
laboratoire est RÉÉCRIT (D15), en identifiants français, et PTAN n'apparaît nulle part (D12) :
tout le code multi-agent disponible en étant bâti, aucun laboratoire ne pouvait s'y appuyer.
AUCUNE SOLUTION COURTE cette semaine, et la page donne la raison plutôt que de l'omettre : les
bibliothèques de haut niveau de ce cours supposent l'interface à un agent que §12.4 montre
inapplicable. Les deux références proposées (joueur aléatoire, recherche avec réseau non
entraîné) sont une conception du cours, et la remarque sur la force propre de la recherche
nue découle de « les états terminaux sont toujours des feuilles » (p.613).

PAS DE JALON CETTE SEMAINE (COURSE-PLAN §10). La page d'accueil est rédigée ici (D47) et la
semaine n'écrit PAS de conclusion séparée, afin qu'aucun des deux textes ne reste non publié.
Les trois routes vers le jalon 4 (auto-jeu, planification avec un modèle appris, multi-agent)
viennent de COURSE-PLAN §2 wk 14. La projection vers la semaine 13 annonce « apprendre à
l'intérieur d'un modèle » et l'apprentissage sur données déjà collectées, et NE DÉPENSE PAS
cette semaine-là : aucune méthode n'est décrite, aucun nom de méthode n'est donné, et la
distinction « planifier avec un modèle appris » contre « apprendre dans un modèle appris »
reste l'ouverture de la semaine 13 (DO NOT read du dossier : Dreamer, PlaNet, offline).

FIGURES. Quatre identifiants, trois dessins du cours et une seule extraction.
12-01 (les quatre phases et le signe qui s'inverse) et 12-02 (un réseau contre trois) sont
demandés par le dossier ; 12-03 (la boucle d'auto-jeu et sa porte) est le troisième dessin que
le dossier laissait à la passe de rédaction, et la rédaction LE RETIENT, parce que §12.5 repose
entièrement sur la boucle de rétroaction entre promotion et distribution des données.
La fig. 20.6 p.624 n'est PAS extraite : ouverte et décrite intégralement par la passe de
lecture, elle montre une profondeur 1, aucune remontée et aucun signe, donc moins que ce dont la
semaine a besoin ; 12-01 la remplace en ajoutant un second niveau et le chemin de retour.
LAPAN fig. 22.1 p.683 EST extraite comme 12-04 : le recadrage est propre (deux panneaux encadrés,
en-têtes dans l'image), c'est la seule image possible d'un monde multi-agent, et les deux
décomptes qu'elle porte (204 contre 40, puis 201 contre 1) sont de toute façon écrits dans la
prose, de sorte que §12.10 survit sans elle.
La fig. 22.8 p.693 (courbes sans tendance) est REFUSÉE, comme le dossier le préférait : onze
semaines sans publier une courbe d'entraînement de la source, et l'argument tient en prose
plus 12-01 à 12-03. La fig. 22.2 p.688 est refusée pour la même raison, ses deux nombres étant
déjà dans la prose. La fig. 20.2 (deux positions de Puissance 4) est refusée : une grille 6x7
se décrit en deux lignes. Inventaire complet dans extraction/week-12.md.

DÉCOMPTE : 11 sections numérotées · 4 placeholders FIG (12-01, 12-02, 12-03 : dessins du cours,
à produire ; 12-04 : extraction de LAPAN fig. 22.1 p.683, recadrage déjà jugé propre) ·
0 placeholder EQ (9 équations identifiées, 12-E1 à 12-E9, toutes écrites directement en KaTeX
dans la page : 12-E1 et 12-E2 TRANSCRITES d'images de page vérifiées, 12-E1 depuis le CODE de la
p.612 et non du texte de la p.606 ; 12-E3, 12-E6 et 12-E8 ÉCRITES d'après du code lu sur image ;
12-E4 ÉCRITE et vérifiée sur deux images ; 12-E5 ÉCRITE d'après les trois cibles de la p.625 et
le code de la p.639 ; 12-E7 INVENTÉE PAR LE COURS et versée dans notation.md §3 bis ; 12-E9
CITÉE de la page de la semaine 5. Minimax est volontairement SANS équation. L'inventaire complet
est dans extraction/week-12.md)
{{% /comment %}}
