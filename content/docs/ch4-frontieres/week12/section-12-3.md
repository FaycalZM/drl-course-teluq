---
title: "12.3 La recherche arborescente : trois statistiques, quatre phases, un signe qui s'inverse"
weight: 4
---

## Trois composantes qui tiennent ensemble, et trois nombres sur chaque arête

Avant la mécanique, l'architecture d'ensemble, parce qu'elle vous servira de charpente pendant trois sections. La méthode que nous construisons tient en **trois composantes**, et aucune ne fonctionne sans les deux autres :

1. la **recherche arborescente de Monte-Carlo** (*Monte Carlo tree search*, désormais MCTS), qui décide quel coup jouer dans une position donnée ;
2. l'**auto-jeu**, où le **meilleur joueur actuel** joue contre lui-même pour produire des données ;
3. l'**entraînement** d'un réseau **apprenti** sur ces données, apprenti qui remplace le meilleur joueur le jour où il parvient à le battre.

{{% comment %}}SOURCE: LAPAN ch.20 p.603-604{{% /comment %}}

Cette combinaison a un nom et une histoire, et je vous les donne en deux phrases parce que l'échelle du résultat fait partie de ce qu'il faut savoir. Sous le nom d'AlphaGo Zero, elle a atteint le niveau du jeu de go **sans aucune connaissance humaine du jeu autre que ses règles** : pas de parties de maîtres, pas de fonction d'évaluation écrite par un expert, pas d'ouvertures mémorisées. La même méthode a ensuite été appliquée aux échecs et au shogi, où elle a battu Stockfish, un programme que des experts humains ont mis plus d'une décennie à construire.

{{% comment %}}SOURCE: LAPAN ch.20 p.603-604{{% /comment %}}

Entrons dans la recherche. L'arbre que nous construisons a des **nœuds** (*nodes*) qui sont des positions de jeu, et des **arêtes** (*edges*) qui sont des coups. Chaque arête \((s,a)\) porte **trois nombres**, et ces trois nombres sont tout ce que la recherche mémorise :

- une **probabilité a priori** (*prior probability*) \(P(s,a)\), que le réseau fournit : c'est son avis, avant toute recherche, sur l'intérêt du coup \(a\) dans la position \(s\) ;
- un **comptage de visites** (*visit count*) \(N(s,a)\), le nombre de fois que la recherche a emprunté cette arête ;
- une **valeur d'action** \(Q(s,a)\), la moyenne des valeurs remontées à travers cette arête.

{{% comment %}}SOURCE: LAPAN ch.20 p.606 (image){{% /comment %}}

> [!WARNING]
 **\(Q(s,a)\) change de sens ici, et c'est la confusion la plus coûteuse de la semaine.** Depuis la semaine 4, \(Q\) et \(q_\pi\) désignent la valeur d'une action sous une politique : une grandeur définie par une espérance, que l'on cherche à estimer. Dans un arbre de recherche, \(Q(s,a)\) est **une moyenne empirique locale**, calculée sur les quelques dizaines de valeurs qui sont remontées à travers cette arête pendant cette recherche-ci, et effacée quand la recherche s'achève. Elle n'estime aucune politique fixée, puisque la politique de descente change à chaque visite. Gardez les deux objets séparés dans votre tête, et vous lirez les trois prochaines sections sans effort.

---

## Descendre l'arbre : l'utilité de sélection, et le terme qu'il ne faut surtout pas perdre

**L'intuition.** Nous sommes dans un nœud et il faut choisir une arête à descendre. Deux considérations s'opposent, et ce sont exactement celles de la semaine 11 : d'un côté, descendre le coup qui a le mieux marché jusqu'ici, c'est-à-dire celui de plus grand \(Q(s,a)\) ; de l'autre, donner une chance à un coup que le réseau juge prometteur mais que la recherche a peu visité. Il nous faut donc une quantité unique, à maximiser, qui mélange la valeur observée et une prime d'exploration. Appelons-la l'**utilité** \(U(s,a)\).

La prime d'exploration doit avoir trois propriétés. Elle doit être **proportionnelle à l'avis du réseau** \(P(s,a)\), parce que c'est la seule information disponible avant d'avoir visité. Elle doit **décroître quand l'arête est visitée**, sinon la recherche n'exploite jamais. Et elle doit **croître quand le nœud dans son ensemble est beaucoup visité**, pour une raison qui n'est pas évidente et qui est la clé de toute l'affaire : plus on a dépensé de visites dans ce nœud, plus il serait absurde de n'en avoir jamais essayé une des branches.

**L'équation.** Voici l'utilité, avec ses deux termes :

$$
U(s,a) \;=\; Q(s,a) \;+\; c_{\text{puct}}\,P(s,a)\,\frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.612 (image){{% /comment %}}

Lisez le second terme de droite à gauche. Au dénominateur, \(1 + N(s,a)\) : la prime se divise par le nombre de visites de **cette** arête, donc elle fond quand on l'emprunte. Au numérateur, \(\sqrt{\sum_b N(s,b)}\), la racine carrée du **total** des visites du nœud, toutes arêtes confondues : la prime grandit quand le nœud est travaillé. Devant, \(P(s,a)\), l'avis du réseau, qui concentre l'exploration là où elle a des chances de servir. Et \(c_{\text{puct}}\) est la constante qui fixe le taux de change entre les deux termes. Sa valeur usuelle est \(1{,}0\), et je préfère vous dire franchement qu'elle est rarement réglée : elle pourrait l'être pour augmenter l'exploration, et ce cours ne l'a pas fait.

{{% comment %}}SOURCE: LAPAN ch.20 p.611-612 (image 612){{% /comment %}}

> [!WARNING]
 **Vous rencontrerez cette utilité écrite sans sa constante et sans sa racine carrée, et cette forme est fausse.** La version abrégée, \(Q(s,a) + P(s,a)/(1 + N(s,a))\), a l'air d'une simple simplification à une constante multiplicative près. Elle ne l'est pas, et voici exactement ce qu'elle produit. Sans \(\sqrt{\sum_b N(s,b)}\), la prime décroît comme \(1/N(s,a)\) et **rien ne la pousse en retour**. Au bout de quelques dizaines de visites, elle est négligeable devant les écarts de \(Q\), et la sélection devient un \(\argmax_a Q(s,a)\) pur : une descente **gloutonne**, qui approfondit indéfiniment la première branche qui a eu de la chance et n'explore plus rien. La recherche continue de tourner, elle ne plante pas, elle ne prévient pas, et elle ne cherche plus. Le facteur manquant n'est pas une constante de proportionnalité : c'est un facteur qui **croît avec le nombre total de visites du nœud**, et c'est toute la raison pour laquelle le terme d'exploration ne s'éteint pas quand la recherche s'approfondit.

**Le code.** Voici la descente, avec le masquage des coups illégaux inclus parce qu'il doit se faire au même endroit.

```python
import math
import numpy as np

C_PUCT = 1.0   # constante d'exploration de l'utilite, valeur par defaut


def choisir_arete(stats, etat, coups_legaux):
    """Rend l'action d'utilite maximale, coups illegaux ecartes.

    stats[etat] donne quatre listes de meme longueur que l'espace d'actions :
    probabilites a priori P, comptages de visites N, sommes des valeurs W,
    valeurs moyennes Q. La descente n'a besoin que de P, N et Q.
    """
    probabilites, comptages, _sommes, valeurs_moyennes = stats[etat]

    # Le facteur qu'on perd le plus souvent : la racine du TOTAL des visites.
    total_racine = math.sqrt(sum(comptages))

    utilite = [
        q + C_PUCT * p * total_racine / (1.0 + n)
        for q, p, n in zip(valeurs_moyennes, probabilites, comptages)
    ]

    # Les coups illegaux sont mis a -inf AVANT l'argmax : on ne filtre jamais
    # apres, sinon les indices ne correspondent plus a l'espace d'actions.
    utilite = [u if a in coups_legaux else -np.inf for a, u in enumerate(utilite)]
    return int(np.argmax(utilite))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q(s,a)\) | moyenne des valeurs remontées à travers l'arête (**statistique de recherche**) | `valeurs_moyennes[a]`, `q` |
| \(P(s,a)\) | probabilité a priori donnée par la tête de politique | `probabilites[a]`, `p` |
| \(N(s,a)\) | comptage de visites de l'arête | `comptages[a]`, `n` |
| \(\sum_b N(s,b)\) | total des visites du nœud, toutes arêtes confondues | `sum(comptages)` |
| \(\sqrt{\sum_b N(s,b)}\) | le facteur qui empêche la prime de s'éteindre | `total_racine` |
| \(c_{\text{puct}}\) | constante d'exploration | `C_PUCT` |
| \(U(s,a)\) | utilité de sélection | `utilite[a]` |
| \(\argmax_a U(s,a)\) | l'arête descendue | `np.argmax(utilite)` |

---

## Les quatre phases, et le signe qui s'inverse à chaque niveau

**L'intuition.** Une recherche est faite de centaines de **passages** identiques, chacun en quatre phases. On descend de la racine jusqu'à une **feuille** (*leaf*) en suivant l'utilité : c'est la **sélection**. Arrivé à la feuille, on crée ses enfants et on demande au réseau son avis sur eux : c'est l'**expansion**. Le réseau donne du même coup une estimation de la valeur de la position : c'est l'**évaluation**. Puis on remonte le chemin parcouru en inscrivant cette valeur dans chaque arête traversée : c'est la **remontée** (*backup*).

Un passage se termine de deux façons et de deux façons seulement. Soit on atteint un **état terminal** du jeu, c'est-à-dire une partie finie, et la valeur de la feuille est le résultat réel de la partie, sans aucun réseau. Soit on atteint un état **jamais exploré**, et alors le réseau fournit les probabilités a priori de ses coups et une estimation de sa valeur ; un nœud est créé, avec \(N(s,a) \leftarrow 0\), \(P(s,a) \leftarrow\) la sortie de la tête de politique, et \(Q(s,a) \leftarrow 0\) pour chacune de ses arêtes.

{{% comment %}}SOURCE: LAPAN ch.20 p.606 (image){{% /comment %}}

C'est la quatrième phase qui demande de l'attention, et je vais la détailler, parce que c'est le détail que l'on rate en écrivant son premier MCTS. La **Figure 12-1** montre les quatre phases sur un arbre de deux niveaux, et elle met le signe sur les flèches du retour plutôt que dans sa légende, parce que c'est là qu'il se joue.

{{< bookfig src="12-01.png" week="12" >}}

**L'équation.** La remontée met trois quantités à jour sur chaque arête du chemin, puis change le camp :

$$
N(s,a) \mathrel{+}= 1, \qquad W(s,a) \mathrel{+}= v, \qquad Q(s,a) = \frac{W(s,a)}{N(s,a)}, \qquad v \leftarrow -v
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.615{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.606 (image){{% /comment %}}

\(W(s,a)\) est la **somme** des valeurs remontées à travers l'arête, et \(Q(s,a)\) en est la moyenne. Je garde \(W\) explicite parce que c'est ainsi que l'on met une moyenne à jour sans la recalculer : on accumule la somme, on incrémente le compteur, on divise. Dans le code, ce sont deux tableaux distincts, et oublier d'en maintenir un des deux produit une moyenne silencieusement fausse.

Et maintenant le signe. Pourquoi \(v \leftarrow -v\) à chaque niveau ? Parce que **les deux joueurs alternent**, et que la valeur d'une position est toujours exprimée du point de vue du joueur qui doit jouer dans cette position. Une position excellente pour moi est, du point de vue de mon adversaire, une position détestable : le même nombre, avec le signe opposé. Quand nous remontons le chemin, nous changeons de joueur à chaque niveau, donc nous changeons de signe à chaque niveau. C'est minimax, exactement, mais écrit comme une accumulation au lieu d'une alternance de minimums et de maximums : au lieu de minimiser une fois sur deux, nous maximisons toujours une quantité dont nous retournons le signe une fois sur deux.

Le premier changement de signe mérite une phrase à lui, parce qu'il surprend. La valeur rendue par la feuille est celle du joueur qui doit jouer **dans** la feuille, et ce joueur est l'adversaire de celui qui a joué le coup menant à cette feuille. La valeur inscrite dans la dernière arête du chemin est donc **l'opposée** de la valeur de la feuille. D'où l'initialisation du code ci-dessous, qui commence par retourner le signe avant la première inscription.

**Le code.**

```python
def remonter(stats, chemin, valeur_feuille):
    """Remonte la valeur d'une feuille jusqu'a la racine en inversant le signe.

    chemin : la liste des couples (etat, action) parcourus a l'ALLER, de la
             racine vers la feuille.
    valeur_feuille : la valeur de la feuille, du point de vue du joueur qui
             doit jouer DANS la feuille.
    """
    # La derniere arete du chemin a ete jouee par l'adversaire de ce joueur :
    # c'est pourquoi on commence par retourner le signe.
    valeur = -valeur_feuille

    for etat, action in reversed(chemin):
        probabilites, comptages, sommes, valeurs_moyennes = stats[etat]
        comptages[action] += 1                                   # N(s,a) += 1
        sommes[action] += valeur                                 # W(s,a) += v
        valeurs_moyennes[action] = sommes[action] / comptages[action]   # Q = W / N
        valeur = -valeur        # un niveau de plus, donc l'autre joueur
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(v\) | valeur remontée, au niveau courant | `valeur` |
| valeur de la feuille | évaluation par la tête de valeur, ou résultat réel si la partie est finie | `valeur_feuille` |
| \(N(s,a)\) | comptage de visites | `comptages[action]` |
| \(W(s,a)\) | somme des valeurs remontées | `sommes[action]` |
| \(Q(s,a) = W/N\) | moyenne, celle que lit l'utilité | `valeurs_moyennes[action]` |
| \(v \leftarrow -v\) | changement de camp, une fois par niveau | `valeur = -valeur` |
| le chemin \((s_0,a_0),\dots,(s_L,a_L)\) | les arêtes traversées à l'aller | `chemin`, parcouru par `reversed` |

Reste la question du nombre de passages, et elle décide du coût. La méthode d'origine en fait **mille à deux mille par coup joué**, et c'est à ce prix que le résultat suivant devient vrai : une fois la recherche terminée, les comptages de visites \(N(s,a)\) à la **racine** constituent, à eux seuls, la distribution de probabilité sur les actions. Non pas les valeurs \(Q\), non pas les probabilités a priori \(P\) du réseau : les **comptages**. Une arête très visitée est une arête que l'utilité a préférée des centaines de fois, ce qui agrège tout ce que la recherche a appris.

{{% comment %}}SOURCE: LAPAN ch.20 p.606 (image){{% /comment %}}

> [!TIP]
 **Mille recherches par coup, c'est ce que vous n'allez pas faire, et c'est très bien.** Le laboratoire de cette semaine descend ce nombre à **dix** recherches par coup, en traitant huit feuilles par passage de réseau. La méthode continue de fonctionner, moins bien, et c'est précisément ce qui la rend enseignable sur une session gratuite : la section 12.5 vous donnera ce que l'on obtient en une heure avec ces réglages, et ce n'est pas rien.

---

## Trois mécanismes transposables, et le coût honnête du troisième

Trois détails d'implémentation méritent d'être enseignés pour eux-mêmes, parce qu'on les retrouve bien au-delà de cette méthode.

**Premier mécanisme : du bruit, à la racine seulement.** Si la recherche part toujours des mêmes probabilités a priori, deux parties d'auto-jeu dans la même position se ressemblent trop, et les données d'entraînement perdent leur variété. On perturbe donc la racine, et **uniquement** la racine :

$$
P'(s_0,a) \;=\; 0{,}75\,P(s_0,a) \;+\; 0{,}25\,\eta_a, \qquad \boldsymbol\eta \sim \mathrm{Dir}(\alpha_{\mathrm{Dir}})
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.612 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.633 (image){{% /comment %}}

Trois quarts de l'avis du réseau, un quart de bruit tiré selon une loi de Dirichlet. Le bruit ne descend pas dans l'arbre : à l'intérieur de la recherche, les probabilités a priori restent celles du réseau, car un bruit injecté à chaque niveau détruirait la cohérence de la descente au lieu de diversifier les parties. C'est, en une ligne, la leçon de la semaine 11 sur l'exploration dirigée : on perturbe **une fois**, au point de décision, et non à chaque pas.

La concentration \(\alpha_{\mathrm{Dir}}\) demande un mot, parce qu'elle décide de ce que le bruit fait réellement. Un tirage de Dirichlet avec \(\alpha_{\mathrm{Dir}} \ll 1\) sur sept catégories est presque **unitaire** : il met la quasi-totalité du quart de budget de bruit sur **une seule colonne tirée au hasard**, au lieu de l'étaler sur les sept. Ce n'est pas ce qu'on veut : on veut élargir l'avis du réseau, pas forcer un coup au hasard. La règle d'usage est que \(\alpha_{\mathrm{Dir}}\) varie **à l'inverse du facteur de branchement** du jeu, environ \(0{,}03\) au go, \(0{,}15\) au shogi, \(0{,}3\) aux échecs dont le facteur de branchement tourne autour de trente-cinq. Puissance 4 a un facteur de branchement de **sept**. Pour ce jeu, ce cours emploie donc \(\alpha_{\mathrm{Dir}} = 0{,}3\), et je vous dis dans la même phrase que cette valeur n'a pas été réglée pour ce jeu-là : c'est celle des deux valeurs en circulation qui est cohérente avec son facteur de branchement, et c'est tout ce que je peux en garantir.

> [!NOTE]
 **Une valeur transplantée reste une valeur transplantée.** Vous verrez \(\alpha_{\mathrm{Dir}} = 0{,}03\) appliqué à Puissance 4, et cette valeur est celle du go, c'est-à-dire d'un jeu où chaque position offre des centaines de coups légaux. Sur sept colonnes, elle ne fait pas ce qu'elle est censée faire. Le réflexe à prendre n'est pas d'apprendre la bonne valeur par cœur, c'est de **savoir quelle grandeur du jeu la commande** : ici le facteur de branchement, et vous pouvez le compter vous-même avant de lancer le premier entraînement.

**Deuxième mécanisme : les coups illégaux mis à \(-\infty\) avant l'argmax.** Vous l'avez vu dans le code de la descente. L'important est le mot « avant » : on ne retire pas les coups illégaux de la liste, on leur donne une utilité \(-\infty\) et on laisse l'argmax faire son travail. La raison est l'alignement des indices : si vous filtrez la liste, l'indice que rend l'argmax n'est plus un numéro d'action, et vous jouerez un coup pour un autre. C'est un bogue silencieux, qui ne fait pas planter le programme et qui rend l'agent incompréhensible.

{{% comment %}}SOURCE: LAPAN ch.20 p.612-614 (image 612){{% /comment %}}

**Troisième mécanisme : la recherche par petits lots, et son coût.** Un passage de réseau sur une seule feuille gaspille un processeur graphique. On collecte donc **plusieurs feuilles** avant d'appeler le réseau, puis on les étend toutes d'un coup, avec un seul passage avant. Le laboratoire utilise huit feuilles par passage.

{{% comment %}}SOURCE: LAPAN ch.20 p.612-614 (image 612){{% /comment %}}

Ce gain a un coût, et je veux l'énoncer clairement parce que c'est le genre de détail qu'une page d'enseignement escamote volontiers. Un lot de recherches est **moins efficace pour l'exploration** que le même nombre de recherches menées l'une après l'autre. La raison est simple : les recherches d'un même lot partent toutes du même arbre, et le premier lot, lui, ne peut étendre que la racine, puisque rien d'autre n'existe encore. Les informations qu'une recherche aurait apportées à la suivante arrivent donc toutes en retard. Le compromis retenu est de faire **plusieurs petits lots** plutôt qu'un seul grand, ce qui garde l'essentiel du gain de calcul en limitant la perte d'exploration.

{{% comment %}}SOURCE: LAPAN ch.20 p.613{{% /comment %}}

Un dernier détail, minuscule et utile : les **états terminaux ne sont jamais rangés dans les statistiques**. On ne leur crée pas de nœud, donc ils sont toujours des feuilles, et une partie finie est donc toujours réévaluée par son résultat réel plutôt que par une moyenne mémorisée. Cela simplifie le code et supprime une catégorie entière de bogues.

{{% comment %}}SOURCE: LAPAN ch.20 p.613{{% /comment %}}

---
