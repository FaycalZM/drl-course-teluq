---
title: "4.1 Une valeur n'existe pas sans politique"
weight: 2
---

## « Combien vaut cet état ? » est une question incomplète

Commençons par une mise au point qui va vous paraître pédante pendant trois minutes, puis évidente pour le reste du cours. La question « combien vaut cet état ? » n'a pas de réponse. Elle n'en a pas, parce que ce qu'un état vaut dépend entièrement de ce que l'agent va faire ensuite, et ce que l'agent va faire ensuite, c'est sa politique. Changez la politique, et la valeur change. Un état n'a pas de valeur ; il a une valeur **sous une politique**.

Reprenons donc la politique depuis sa définition. Une politique est une application qui, à chaque état, associe une distribution de probabilité sur les actions disponibles : \(\pi(a \mid s)\) est la probabilité que \(A_t = a\) sachant que \(S_t = s\). La barre verticale a une allure de conditionnement, et c'est un piège de lecture : \(\pi\) est une fonction ordinaire de deux arguments, \(a\) et \(s\), et la barre n'est qu'un rappel que la somme sur \(a\) vaut 1 pour chaque \(s\).

{{% comment %}}SOURCE: SB ch.3 p.80{{% /comment %}}

La **valeur d'un état** sous \(\pi\), notée \(v_\pi(s)\), est alors l'espérance du retour quand on part de \(s\) et qu'on suit \(\pi\) ensuite.

$$
v_\pi(s) \defeq \E_\pi\big[G_t \mid S_t = s\big]
= \E_\pi\!\left[\sum_{k=0}^{\infty} \gamma^{k} R_{t+k+1} \,\middle|\, S_t = s\right],
\qquad \text{pour tout } s \in \mathcal{S}
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.12 p.80{{% /comment %}}

La **valeur d'une action** (*action value*, aussi appelée *Q-value*) sous \(\pi\), notée \(q_\pi(s,a)\), est la même espérance, à ceci près que l'action \(a\) est imposée au premier pas, et que \(\pi\) ne reprend la main qu'ensuite.

$$
q_\pi(s,a) \defeq \E_\pi\big[G_t \mid S_t = s, A_t = a\big]
= \E_\pi\!\left[\sum_{k=0}^{\infty} \gamma^{k} R_{t+k+1} \,\middle|\, S_t = s, A_t = a\right]
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.13 p.80{{% /comment %}}

Deux remarques, et la seconde a des conséquences très concrètes dans le code du laboratoire.

D'abord, le lien avec la semaine 3. Si vous jouez un grand nombre d'épisodes et que, pour chaque état, vous faites la **moyenne des retours réellement observés** après chaque visite de cet état, cette moyenne converge vers \(v_\pi(s)\) quand le nombre de visites tend vers l'infini. C'est exactement une méthode de Monte-Carlo, et c'est la méthode à laquelle toute cette semaine va se comparer. Retenez la forme de cette phrase : *il faut des épisodes complets, et il faut en moyenner beaucoup*.

{{% comment %}}SOURCE: SB ch.3 p.80{{% /comment %}}

> [!IMPORTANT]
 **La valeur d'un état terminal, lorsqu'il y en a un, est toujours nulle.** Ce n'est pas une convention commode, c'est une conséquence de la définition : d'un état terminal, il ne part plus aucune récompense, donc le retour y vaut zéro, donc son espérance aussi. Je le souligne ici parce que c'est la ligne la plus souvent oubliée dans une implémentation tabulaire, et parce qu'elle revient trois fois dans le laboratoire. Dans le code, cela s'écrit **toujours** par une condition explicite : si l'état atteint est terminal, le terme de valeur future est remplacé par zéro, et non par la case correspondante de la table.

{{% comment %}}SOURCE: SB ch.3 p.80{{% /comment %}}

---

## Trois états, quatre politiques, quatre valeurs

Passons à l'exemple qui règle la question en une minute. Imaginez un environnement de trois états, parfaitement déterministe. L'agent démarre dans l'état 1. De là, il a deux actions : aller **à droite**, ce qui l'amène dans l'état 2 avec une récompense de 1, ou aller **vers le bas**, ce qui l'amène dans l'état 3 avec une récompense de 2. L'épisode se termine dans les deux cas, en 2 comme en 3. Prenons \(\gamma = 1\) pour ne pas encombrer l'arithmétique.

Combien vaut l'état 1 ? La réponse dépend de la politique, et quatre politiques donnent quatre réponses.

| Politique dans l'état 1 | \(v_\pi(\text{état } 1)\) |
| --- | --- |
| toujours à droite | **1,0** |
| toujours vers le bas | **2,0** |
| moitié à droite, moitié vers le bas | **1,5** |
| 10 % à droite, 90 % vers le bas | **1,9** |

{{% comment %}}SOURCE: LAPAN ch.5 p.145-146{{% /comment %}}

Chaque ligne se vérifie en une multiplication. La troisième, par exemple, vaut \(0{,}5 \times 1 + 0{,}5 \times 2 = 1{,}5\). Et la conclusion de ce petit tableau est déjà la morale de la section : **la valeur d'un état n'est pas une propriété de l'environnement**, c'est une propriété du couple environnement et politique. D'où l'indice \(\pi\), que je ne vous laisserai pas oublier.

À ce stade, la meilleure politique semble évidente : toujours vers le bas, puisque 2 vaut mieux que 1. Gardez cette conclusion en tête pendant trente secondes.

---

## Le piège : ce qui arrive après l'état 3

Modifions l'environnement, très légèrement. L'état 3 n'est plus terminal : il mène maintenant, par une unique action, à un quatrième état, et cette transition rapporte **−20**. L'état 2, lui, reste terminal. Rien d'autre ne change : aller à droite rapporte toujours 1, aller vers le bas rapporte toujours 2. La **Figure 4-1** montre cet environnement à quatre états, et je vous invite à la regarder avant de lire les chiffres qui suivent.

{{< bookfig src="04-01.png" week="04" >}}

{{% comment %}}SOURCE: LAPAN ch.5 p.146-147{{% /comment %}}

Recalculons les quatre mêmes politiques.

| Politique dans l'état 1 | Avant (état 3 terminal) | Après (l'état 3 mène à −20) |
| --- | --- | --- |
| toujours à droite | 1,0 | **1,0** |
| toujours vers le bas | 2,0 | **−18** |
| moitié, moitié | 1,5 | **−8,5** |
| 10 % à droite, 90 % vers le bas | 1,9 | **−16,1** |

{{% comment %}}SOURCE: LAPAN ch.5 p.146-147{{% /comment %}}

La meilleure politique vient de **basculer**. « Toujours vers le bas », qui était la meilleure, est devenue la pire, et « toujours à droite », qui était la pire, est devenue la meilleure. Et notez bien ce qui a produit ce basculement : aucune des deux récompenses immédiates n'a changé. Aller vers le bas rapporte toujours 2 contre 1. Seule a changé une conséquence située **deux pas plus loin**.

> [!WARNING]
 **Attention, c'est le piège fondateur de tout le domaine, et il a un nom : la gourmandise à un pas.** Choisir l'action qui rapporte le plus **immédiatement** est une stratégie qui se trompe, et qui se trompe d'autant plus que l'horizon est long. Ici, l'écart entre le choix glouton sur la récompense immédiate et le choix réellement optimal est de 19 points sur un environnement de quatre états. Retenez bien la structure de l'erreur : elle ne vient pas d'un mauvais calcul, elle vient d'avoir regardé la mauvaise quantité. Et retenez aussi qu'à la section 4.3 nous allons rétablir la gourmandise, mais appliquée à une tout autre quantité. Toute la différence entre un piège et un théorème tiendra dans ce choix de quantité.

Ce qui nous manque, donc, est une quantité qui **contient déjà** tout le futur, de sorte qu'être glouton à son égard ne soit plus myope. C'est exactement ce que \(v_\pi\) et \(q_\pi\) sont, et il nous reste à trouver comment les calculer. La section suivante répond en une équation.
