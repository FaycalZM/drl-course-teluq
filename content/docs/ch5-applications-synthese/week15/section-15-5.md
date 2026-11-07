---
title: "15.5 Une permutation"
weight: 6
---

## Le cas le plus dur du cours : aucune récompense avant la fin

Quatrième et dernier problème, et c'est celui pour lequel je garde le plus de place, parce qu'il pousse à l'extrême la troisième question de la semaine.

Le cube de Rubik n'est pas un jouet pour ce cours : c'est un représentant d'une famille de problèmes qui s'appelle l'**optimisation combinatoire** (*combinatorial optimization*), ou **optimisation discrète** (*discrete optimization*), et dans laquelle on trouve le voyageur de commerce, le repliement de protéines et l'allocation de ressources. Ce que ces problèmes ont en commun est précisément ce qui les rend intéressants : un **espace d'états énorme**, qui rend inenvisageable l'énumération de toutes les combinaisons.

Pour fixer l'échelle : un cube trois par trois admet \(4{,}33 \cdot 10^{19}\) états atteignables. Si l'on s'autorise à le démonter et à le remonter n'importe comment, le compte monte à \(5{,}19 \cdot 10^{20}\), et les états supplémentaires ne sont **pas résolubles** sans démonter de nouveau.

{{% comment %}}SOURCE: LAPAN ch.21 p.645-646{{% /comment %}}

**L'observation** est l'état complet : aucune observation partielle, aucun PDM partiellement observable, aucune mémoire nécessaire. C'est le seul des quatre problèmes de la semaine dans ce cas, et c'est un luxe.

**L'action** compte douze valeurs : **six faces**, chacune tournée dans **deux sens**, ce qui fait douze rotations. Une convention d'écriture usuelle note la rotation horaire par une majuscule et l'antihoraire par la minuscule correspondante. Et un point de définition dont toute la section 15.8 va dépendre : les **demi-tours**, c'est-à-dire deux rotations consécutives dans le même sens, ne sont **pas** comptés comme une action distincte. Ils coûtent **deux** actions. Retenez cette phrase, elle vaut un nombre.

{{% comment %}}SOURCE: LAPAN ch.21 p.646, p.648{{% /comment %}}

**La récompense** vaut \(+1\) sur l'état résolu et \(-1\) partout ailleurs. Un bit, une seule fois, à la toute fin d'une séquence qui peut compter vingt coups. C'est la récompense la plus parcimonieuse que ce cours ait rencontrée, et de très loin : la voiture de la semaine 11 devait atteindre un drapeau au bout d'une vallée, ce qui arrivait par hasard une fois sur quelques milliers d'épisodes ; ici, l'arrivée par hasard est de l'ordre d'une fois sur \(10^{19}\).

{{% comment %}}SOURCE: LAPAN ch.21 p.654{{% /comment %}}

---

## Deux familles de solveurs qui existaient déjà, et ce qu'elles exigent

Avant d'arriver à la méthode, il faut dire ce qui existait, parce que c'est ce qui donne son sens à la méthode.

**Première famille : la théorie des groupes.** Un cube est un objet algébrique, et il existe des algorithmes exacts qui l'exploitent. Le plus connu résout un cube quelconque en une fraction de seconde.

**Seconde famille : la recherche heuristique.** Un parcours de type A\* guidé par une heuristique construite à partir d'une grande base de motifs précalculés, qui donne des solutions **optimales**.

Les deux fonctionnent très bien et les deux ont la même propriété : elles demandent **beaucoup de connaissance humaine du domaine**. Il faut savoir ce qu'est un groupe de cube, ou savoir quels motifs tabuler. Et c'est là que la troisième approche se distingue, non par sa performance mais par son **exigence d'entrée** : la seule chose dont elle a besoin, c'est **le cube lui-même**. Pas de base de motifs, pas de théorie, pas de jeu de données d'exemples résolus : le **modèle de la dynamique**, c'est-à-dire la règle qui dit ce que fait chaque rotation.

{{% comment %}}SOURCE: LAPAN ch.21 p.647{{% /comment %}}

> [!TIP]
 **Voici un critère de choix que vous pouvez ranger immédiatement dans la carte de décision de la section 15.10.** La question n'est pas seulement « quelle méthode est la meilleure », c'est **« de quoi chaque méthode a-t-elle besoin pour commencer »**. Une méthode qui exige une base de connaissances du domaine est inapplicable sur un domaine que personne n'a étudié. Une méthode qui exige un jeu de données d'exemples résolus est inapplicable quand on n'en a pas. Une méthode qui n'exige que le simulateur est applicable partout où il y a un simulateur. Mettez cette ligne dans votre rapport : **ce que votre méthode exige en entrée est une caractéristique aussi importante que ce qu'elle produit en sortie.**

---

## Quatre critères pour choisir une représentation, et un codage naïf qui les viole

Voici maintenant un morceau que je vous recommande de recopier tel quel, parce qu'il s'applique à n'importe quel problème dont l'état n'est pas déjà un vecteur de nombres. Quatre critères pour juger une représentation d'état.

1. **Éviter la redondance.** Un état du monde doit correspondre à une et une seule représentation, et réciproquement.
2. **L'efficacité en mémoire.** La recherche va stocker des millions d'états : leur taille unitaire est multipliée par des millions.
3. **La performance des transformations.** Appliquer une action à un état est l'opération la plus répétée de tout l'algorithme.
4. **La compatibilité avec un réseau de neurones.** La représentation doit pouvoir entrer dans un réseau sans transformation coûteuse, et de préférence sous une forme que le réseau sait exploiter.

{{% comment %}}SOURCE: LAPAN ch.21 p.649-651{{% /comment %}}

Appliquons le premier critère au codage le plus évident, celui qui vient à l'esprit en trois secondes : une couleur par autocollant, six couleurs, quarante-huit autocollants mobiles. Cela donne

$$
6^{48} \approx 2{,}25 \cdot 10^{37}
$$

représentations possibles, contre \(4{,}33 \cdot 10^{19}\) états réels. Dix-sept ordres de grandeur de trop. Le codage est **massivement redondant** : l'immense majorité de ces configurations d'autocollants ne correspond à aucun cube physique.

La représentation retenue est un tenseur **20 sur 24** en **codage one-hot** (*one-hot encoding*), celui de la semaine 3, qui donne

$$
24^{20} \approx 4{,}02 \cdot 10^{27}
$$

configurations, soit encore \(10^{8}\) fois trop. Elle n'est donc pas parfaite, et la raison de ce facteur restant est jolie : on ne peut pas **faire tourner un seul coin sur lui-même** en laissant tous les autres éléments en place, alors que le codage, lui, le permet. Les contraintes physiques du cube ne sont pas toutes représentables dans un codage positionnel indépendant.

{{% comment %}}SOURCE: LAPAN ch.21 p.649-651{{% /comment %}}

---

## Pourquoi vingt et pourquoi vingt-quatre

Les deux dimensions valent une explication, parce qu'elles sont le résultat d'un raisonnement et non d'un choix d'implémentation.

Un cube trois par trois est fait de petits cubes, que j'appellerai des **cubes élémentaires** (*cubelets*) pour éviter toute confusion avec les arêtes d'un arbre de recherche de la semaine 12. Il y en a de trois sortes : huit cubes de **coin** à trois faces visibles, douze cubes de **bord** à deux faces visibles, et six cubes de **centre** à une face visible.

**Les six centres ne sont pas suivis**, et c'est la décision la plus intelligente de la représentation. Ils ne peuvent pas changer de position les uns par rapport aux autres : quelle que soit la façon dont vous tournez le cube, le centre blanc reste opposé au centre jaune. Ne pas les suivre rend donc l'état **invariant par rotation d'ensemble** (*rotation-invariant*) : les vingt-quatre orientations globales d'un même cube deviennent **un seul état**. C'est une division de l'espace par vingt-quatre, obtenue en retirant de l'information plutôt qu'en en ajoutant.

Reste le compte des vingt-quatre colonnes : huit coins fois trois orientations possibles font vingt-quatre, et douze bords fois deux orientations font également vingt-quatre. Et le compte des vingt lignes : vingt autocollants suivis, huit pris sur la face du haut, huit sur celle du bas, et quatre sur les côtés.

{{% comment %}}SOURCE: LAPAN ch.21 p.650-651{{% /comment %}}

---

## Deux représentations plutôt qu'une, et c'est une décision de conception à imiter

Dernier point de représentation, et c'est celui que je vous demande de retenir pour votre propre projet.

Il n'y a pas **une** représentation de l'état dans ce système, il y en a **deux**, et elles coexistent. Le tenseur 20 sur 24 en nombres flottants, qui pèse **1 920 octets**, sert à **entrer dans le réseau**. Et une forme compacte, une simple permutation, qui pèse **160 octets**, sert à **stocker** les millions d'états que la recherche manipule.

{{% comment %}}SOURCE: LAPAN ch.21 p.651{{% /comment %}}

Douze fois moins de mémoire, pour exactement la même information. Quand votre recherche garde deux millions d'états en vie, la différence entre 1,9 kilooctet et 160 octets par état est la différence entre quatre gigaoctets et trois cent vingt mégaoctets, c'est-à-dire entre « ça ne tient pas » et « ça tient ». Et la règle générale est celle-ci : **la représentation qui entre dans un réseau et la représentation qui se stocke n'ont aucune raison d'être la même.** Écrivez les deux, écrivez la conversion, testez la conversion dans les deux sens, et ne cherchez pas un compromis unique.

---

## La réponse à la récompense parcimonieuse, et ce n'est pas une méthode d'exploration

Nous arrivons à l'idée la plus astucieuse de la semaine, et je veux l'annoncer avant de l'écrire, parce qu'elle est contre-intuitive pour qui vient de la semaine 11.

Le problème est : la récompense n'arrive qu'à la fin, et la fin est inaccessible au hasard. Quatorze semaines de ce cours vous ont appris à répondre à ce problème par de l'**exploration** : une prime de nouveauté, un comptage d'états, une distillation de réseau aléatoire. Toutes ces réponses consistent à **mieux chercher le but**.

La réponse employée ici ne cherche pas le but. Elle **part du but**.

Voici l'idée, et elle tient en une phrase. On prend le cube **résolu**, on lui applique \(N\) rotations tirées au hasard, ce nombre \(N\) étant la **profondeur de brouillage** (*scramble depth*), et on entraîne sur les états ainsi produits. Puisqu'on est parti du but et qu'on sait combien de coups on a joués, **chaque état d'entraînement a une distance au but connue**. Le problème « aucune récompense avant la fin » **ne se présente jamais pendant l'entraînement**, parce qu'on n'a jamais eu à atteindre la fin : on en vient.

Cette méthode s'appelle l'**itération autodidacte** (*autodidactic iteration*), ADI en abrégé.

{{% comment %}}SOURCE: LAPAN ch.21 p.654 (image){{% /comment %}}

> [!IMPORTANT]
 **Voici la condition d'applicabilité de ce procédé, et c'est elle qu'il faut emporter, pas le cube.** Il faut deux choses, et elles sont rares ensemble. **Un :** connaître l'**état but**, explicitement, et pas seulement savoir le reconnaître. **Deux :** disposer d'une **dynamique inversible**, c'est-à-dire pouvoir s'éloigner du but en appliquant la même mécanique qui servira à s'en rapprocher. Quand ces deux conditions sont réunies, **n'engendrez pas vos données en explorant, engendrez-les à reculons**, et la récompense parcimonieuse disparaît du problème. Cela vaut pour tout casse-tête, pour beaucoup de problèmes de montage et de démontage, pour des problèmes de planification de mouvement, et cela ne vaut pas du tout pour un jeu d'arcade, dont on ne sait pas écrire l'état gagnant. Posez-vous la question avant de construire une prime de nouveauté : **est-ce que je connais mon état but, et est-ce que je peux marcher à l'envers ?**

---

## Les deux cibles d'entraînement, et la notation qu'il faut poser avant

Passons à l'équation, et je redis d'abord les deux renommages annoncés en introduction, parce qu'ils tombent tous les deux à l'intérieur de ce qui suit.

**La transition s'écrit \(\mathcal{T}(s,a)\)** : l'état atteint depuis \(s\) en jouant l'action \(a\). Ce cours ne l'écrit pas \(A(s,a)\), parce que \(A_t\) est l'action et \(A^\pi(s,a)\) l'avantage.

**La valeur de l'état atteint s'écrit \(v(\mathcal{T}(s,a))\)**, et surtout pas avec la forme d'une valeur d'action. Ce n'est pas \(q(s,a)\) : c'est la fonction de valeur \(v\), évaluée en un **autre état**.

Et **\(R(s)\) est un indicateur de but** : \(+1\) si \(s\) est le cube résolu, \(-1\) sinon. Pas un retour, pas une récompense actualisée.

**L'intuition.** Le réseau a deux têtes, comme celui de la semaine 12 : une tête de valeur qui dit « à quel point cet état est-il bon », et une tête de politique qui dit « quelle rotation jouer ici ». Il faut une cible pour chacune. Pour un état \(s\) donné, on regarde ses douze enfants, on évalue chacun, on garde le meilleur : la **valeur du meilleur enfant** est la cible de la tête de valeur, et **l'identité de ce meilleur enfant** est la cible de la tête de politique. C'est, à la lettre, un pas d'itération de la valeur de la semaine 4, avec un réseau à la place du tableau.

**Les équations.** La cible de la tête de valeur :

$$
y_v(s) \;=\; \max_{a} \Big( v\big(\mathcal{T}(s,a)\big) \,+\, R\big(\mathcal{T}(s,a)\big) \Big)
$$

{{% comment %}}SOURCE: LAPAN ch.21 p.654 (image){{% /comment %}}

Et la cible de la tête de politique, qui est le même calcul dont on garde l'**indice** plutôt que la valeur :

$$
y_p(s) \;=\; \argmax_{a} \Big( v\big(\mathcal{T}(s,a)\big) \,+\, R\big(\mathcal{T}(s,a)\big) \Big)
$$

{{% comment %}}SOURCE: LAPAN ch.21 p.654 (image){{% /comment %}}

La cible de politique est donc un vecteur à douze composantes valant **1 à la position du maximum et 0 partout ailleurs**, c'est-à-dire exactement une étiquette de classification, qu'on ajuste par entropie croisée comme en semaine 4.

Lisez le contenu de la parenthèse avec attention, parce que la section 15.7 va s'y installer : on additionne la **valeur prédite de l'état atteint** et l'**indicateur de but de l'état atteint**. Deux quantités de natures différentes, et l'une des deux est produite par le réseau qu'on entraîne.

**Le code.** Voici le calcul des deux cibles pour un lot d'états brouillés. Il est écrit pour être lu, pas pour être exécuté : il n'y a pas d'entraînement dans cette semaine.

```python
import torch

def cibles_adi(reseau, etats, transitions, est_resolu):
    """Calcule y_v et y_p pour un lot d'etats obtenus par brouillage.

    etats       : (B, 20, 24)      le lot d'etats, codage one-hot
    transitions : (B, 12, 20, 24)  les 12 etats atteints depuis chaque etat du lot
    est_resolu  : fonction qui renvoie un booleen par etat
    """
    B, A = transitions.shape[0], transitions.shape[1]
    enfants = transitions.reshape(B * A, 20 * 24)

    with torch.no_grad():
        # v(T(s,a)) : la tete de valeur seule, sur les 12 enfants de chaque etat
        v_enfants = reseau(enfants, valeur_seule=True).reshape(B, A)
        # R(T(s,a)) : +1 sur le cube resolu, -1 partout ailleurs
        r_enfants = torch.where(est_resolu(enfants).reshape(B, A), 1.0, -1.0)

        total = v_enfants + r_enfants          # le contenu de la parenthese
        y_v, y_p = total.max(dim=1)            # la valeur, puis l'indice

    return y_v, y_p                            # (B,) et (B,) indices dans [0, 12)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{T}(s,a)\) | l'état atteint depuis \(s\) par l'action \(a\) | `transitions[:, a]` |
| \(v(\mathcal{T}(s,a))\) | la valeur de l'état **atteint**, pas une valeur d'action | `v_enfants` |
| \(R(\mathcal{T}(s,a))\) | l'indicateur de but de l'état atteint, \(+1\) ou \(-1\) | `r_enfants` |
| \(\max_a(\cdot)\) | la cible de la tête de valeur | `y_v` |
| \(\argmax_a(\cdot)\) | la cible de la tête de politique, un indice | `y_p` |
| \(N\) | la profondeur de brouillage appliquée au cube résolu | `profondeur_brouillage` |
| le tenseur 20 sur 24 | la représentation d'entrée du réseau | `etats`, `enfants` |

{{% comment %}}SOURCE: LAPAN ch.21 p.653-654 (image){{% /comment %}}

---

## Le réseau, cité de la semaine 12, et pourquoi la politique seule ne suffit pas

Le réseau est un **réseau à deux têtes**, et c'est celui de la semaine 12 : un corps dense partagé, de 4 096 puis 2 048 unités avec une activation exponentielle linéaire, puis deux têtes. La tête de politique sort douze logits ; la tête de valeur sort un scalaire. Et un détail d'implémentation qui n'en est pas un : le passage avant accepte un drapeau qui permet d'évaluer **la tête de valeur seule**, ce qui est exactement ce que le code ci-dessus fait douze fois par état.

{{% comment %}}SOURCE: LAPAN ch.21 p.653-654 (image){{% /comment %}}

Une fois ce réseau entraîné, la tentation est de l'employer directement : à chaque état, demander la tête de politique et jouer l'action qu'elle recommande. **Cela ne fonctionne pas**, et la raison est à la fois mesurée et instructive.

Le réseau n'apprend pas l'action **optimale** : il apprend une **direction**. Dit autrement, il a vu, pour chaque état d'entraînement, quelle action menait à l'enfant le mieux évalué, et il a appris à reproduire ce choix local. Un enchaînement de choix localement bons n'est pas un chemin globalement bon, surtout dans un espace où un coup peut annuler le précédent.

Et il y a la raison de fond, chiffrée : après un mois d'entraînement, ce réseau a vu environ **0,0000005 %** de l'espace d'états. Cinq dix-millionièmes de pour cent. Il est illusoire d'attendre d'une fonction ajustée sur une fraction aussi infime qu'elle soit exacte au coup près sur un état quelconque.

{{% comment %}}SOURCE: LAPAN ch.21 p.656 (image){{% /comment %}}

La réponse est donc de **chercher**, et de se servir du réseau comme guide de la recherche, ce qui est précisément ce que la semaine 12 a construit.

---

## La règle de descente, et c'est celle de la semaine 12

Je ne redéris pas cette règle : la semaine 12 l'a dérivée, discutée, et vous en a montré la version abrégée fausse. Je la **cite**, et je nomme les deux différences.

**D'abord les deux collisions de notation, parce qu'elles sont dans la formule.** Le \(U\) de la semaine 12 était l'**utilité complète**, valeur plus prime. Le \(U\) ci-dessous est la **prime d'exploration seule**. Et le \(W\) de la semaine 12 était une **somme** de valeurs remontées ; le \(W\) ci-dessous est un **maximum** sur le sous-arbre.

L'action descendue depuis un nœud est

$$
A_t \;=\; \argmax_{a} \Big( U(s_t, a) \,+\, W(s_t, a) \Big),
\qquad
U(s_t, a) \;=\; c \, P(s_t, a) \, \frac{\sqrt{\sum_{a'} N(s_t, a')}}{1 + N(s_t, a)}
$$

{{% comment %}}SOURCE: LAPAN ch.21 p.657 (image){{% /comment %}}

Comparez terme à terme avec l'équation 12-E1 de la semaine 12. Le terme de prime est **identique** : la constante d'exploration, la probabilité a priori fournie par le réseau, la racine du total des visites du nœud au numérateur, et un plus le nombre de visites de cette arête au dénominateur. La seule différence est ce à quoi on ajoute cette prime : une **moyenne** des valeurs remontées en semaine 12, un **maximum** ici.

**Cette différence est réelle et elle est défendable.** Une moyenne est le bon estimateur quand le résultat d'une descente est incertain : un adversaire peut répondre, un dé peut tomber autrement, et ce qu'on veut savoir est l'espérance. Un maximum est le bon estimateur quand rien ne peut vous empêcher de rejouer le meilleur chemin que vous avez trouvé. C'est exactement la situation d'un casse-tête **déterministe à un seul joueur** : si une suite de rotations mène à l'état résolu, elle y mènera toujours. Dans ce cadre, moyenner serait diluer une bonne nouvelle avec de mauvaises nouvelles sans intérêt.

> [!NOTE]
 **Et voici un réflexe que je veux vous laisser pour la lecture de deux descriptions d'une même méthode.** Deux formules peuvent avoir la même forme et ne pas décrire le même algorithme, parce que la **définition** d'un de leurs symboles diffère. Ici, la différence entre une moyenne et un maximum n'apparaît nulle part dans l'équation : elle est dans la phrase qui définit \(W\), trois lignes plus haut ou trois pages plus loin. Quand vous comparez deux variantes d'une méthode, **comparez les définitions des symboles avant de comparer les équations**, et méfiez-vous particulièrement des remontées, des normalisations et des bornes de sommation, qui sont les trois endroits où les auteurs ne se recopient pas.

Un dernier détail de cette recherche, qui est une petite leçon à lui seul. Quand la recherche a trouvé l'état résolu, il reste à **extraire** la solution de l'arbre, et il y a deux façons de faire. La façon naïve suit le chemin parcouru depuis la racine. La façon correcte cherche le **plus court chemin dans l'arbre** jusqu'au nœud but, par un parcours en largeur. La seconde donne des solutions environ **dix fois plus courtes**, et la raison est mécanique : la recherche est stochastique, donc le chemin qu'elle a effectivement suivi contient des **cycles**, des allers-retours qui s'annulent. Le chemin emprunté par une recherche n'est pas la solution qu'elle a trouvée.

{{% comment %}}SOURCE: LAPAN ch.21 p.657 (image), p.670{{% /comment %}}

---

## Ce que la méthode obtient, avec son coût

Pour clore ce problème, les chiffres publiés, qui sont le point de comparaison de la section 15.7.

L'entraînement a demandé **44 heures sur trois processeurs graphiques**, pendant lesquelles environ **8 milliards d'états** ont été traités, à une cadence d'environ **50 000 cubes par seconde**. Le protocole d'évaluation : **640 cubes** brouillés par **1 000 coups**, une limite d'une heure par cube. Dans ces conditions, la méthode à réseau et un solveur algébrique classique résolvent **tous** les cubes. Le temps médian du solveur classique est d'**une seconde** ; celui de la méthode à réseau est d'environ **dix minutes**. En revanche, la méthode à réseau égale ou améliore la **longueur de solution** du solveur classique dans **55 %** des cas.

{{% comment %}}SOURCE: LAPAN ch.21 p.657-658{{% /comment %}}

La conclusion qu'il faut en tirer est mesurée, et je la formule comme je la pense : ce n'est pas assez pour affirmer qu'un réseau fait significativement mieux, et c'est assez pour affirmer qu'il ne fait pas moins bien. Six cents fois plus lent, et une longueur de solution comparable, en n'ayant eu besoin que du simulateur. Mettez les trois ensemble, et vous avez une évaluation honnête.

---
