---
title: "4.3 Optimalité"
weight: 4
---

## Il existe toujours une meilleure politique, et elles partagent la même valeur

Nous savons évaluer une politique. Nous voulons la meilleure. Il faut donc d'abord dire ce que « meilleure » signifie, et la définition est plus subtile qu'il n'y paraît, parce qu'une politique peut être meilleure dans certains états et pire dans d'autres.

La convention est la suivante : on dit que \(\pi \ge \pi'\) lorsque \(v_\pi(s) \ge v_{\pi'}(s)\) **pour tout** état \(s\). C'est un **ordre partiel** : deux politiques quelconques ne sont pas forcément comparables. Et pourtant, le résultat qui suit est remarquablement fort.

Pour un processus de décision markovien fini, il existe **toujours au moins une politique optimale**, c'est-à-dire une politique supérieure ou égale à toutes les autres en tout état. Il peut en exister plusieurs. Mais toutes partagent la **même** fonction de valeur d'état et la **même** fonction de valeur d'action, et c'est ce qui autorise une notation sans indice de politique.

{{% comment %}}SOURCE: SB ch.3 p.84{{% /comment %}}

$$
v_*(s) \defeq \max_\pi v_\pi(s),
\qquad\qquad
q_*(s,a) \defeq \max_\pi q_\pi(s,a)
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.15 p.84, éq. 3.16 p.85{{% /comment %}}

Ces deux fonctions sont les valeurs **vraies** sous une **politique optimale** (*optimal policy*), que l'on note \(\pi_*\). Elles sont reliées par une identité qui se lit comme une phrase : la valeur optimale d'une action est la récompense qu'elle rapporte plus la valeur optimale de là où elle vous dépose.

$$
q_*(s,a) = \E\big[R_{t+1} + \gamma\, v_*(S_{t+1}) \mid S_t = s, A_t = a\big]
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.17 p.85{{% /comment %}}

---

## Les deux équations d'optimalité

Prenons l'intuition avant la formule, et prenons-la dans le cas le plus simple possible : un environnement **déterministe**. Je suis dans un état, j'ai quelques actions, chacune rapporte une récompense connue \(r_a\) et m'amène dans un état dont je connais la valeur \(V_a\). Si je joue optimalement, que vaut mon état actuel ? La meilleure des promesses disponibles :

$$
V_0 = \max_a \big( r_a + \gamma\, V_a \big)
$$

Voilà toute l'idée, et elle tient dans un \(\max\). Dans le cas général, l'environnement n'est pas déterministe : une action ne mène pas à un état mais à une distribution d'états. Il suffit alors de remplacer « la promesse de l'action \(a\) » par « l'espérance de la promesse de l'action \(a\) », et l'on obtient l'**équation d'optimalité de Bellman** (*Bellman optimality equation*) pour \(v_*\).

{{% comment %}}SOURCE: LAPAN ch.5 p.147-148{{% /comment %}}

$$
\begin{aligned}
v_*(s) &= \max_{a \in \mathcal{A}(s)}
  \E\big[R_{t+1} + \gamma\, v_*(S_{t+1}) \mid S_t = s, A_t = a\big] \\[2pt]
&= \max_{a \in \mathcal{A}(s)} \sum_{s',r} p(s',r \mid s,a)
  \big[\, r + \gamma\, v_*(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.18-3.19 p.85{{% /comment %}}

Comparez-la, symbole par symbole, à l'équation de Bellman de la section 4.2. Une seule chose a changé : la somme \(\sum_a \pi(a \mid s)\), qui **moyennait** sur les actions selon la politique, est devenue un \(\max_a\), qui **sélectionne** la meilleure. C'est la seule différence, et c'est tout le passage de « évaluer une politique donnée » à « caractériser la meilleure politique possible ». Notez au passage que \(\pi\) a disparu de l'équation : l'optimalité ne se réfère plus à aucune politique.

Il existe une équation jumelle pour \(q_*\), et je vous demande de regarder très précisément **où** s'y trouve le \(\max\).

$$
\begin{aligned}
q_*(s,a) &= \E\!\left[R_{t+1} + \gamma \max_{a'} q_*(S_{t+1},a')
  \,\middle|\, S_t = s, A_t = a\right] \\[2pt]
&= \sum_{s',r} p(s',r \mid s,a)
  \Big[\, r + \gamma \max_{a'} q_*(s',a') \,\Big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.20 p.85{{% /comment %}}

Le \(\max\) est **à l'intérieur** du crochet, et il porte sur \(a'\), l'action du pas **suivant**. Ce n'est pas un détail cosmétique : l'action \(a\) du pas courant est imposée, elle n'est pas maximisée, et c'est la définition même d'une valeur d'action. Si vous placez ce \(\max\) à l'extérieur, vous écrivez autre chose, et vous vous en apercevrez cruellement en semaine 6, où un \(\max\) mal placé est l'origine d'un biais célèbre.

La **Figure 4-3** met les deux diagrammes de sauvegarde côte à côte, celui de \(v_*\) et celui de \(q_*\). Repérez l'arc qui enjambe les branches : c'est la notation graphique du \(\max\), et sa position sur le diagramme répond exactement à la question du paragraphe précédent.

{{< bookfig src="04-03.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.3 p.86{{% /comment %}}

Un mot sur le statut mathématique de ces équations. Pour un processus de décision markovien fini, l'équation d'optimalité de Bellman pour \(v_*\) est un **système de \(n\) équations à \(n\) inconnues**, où \(n\) est le nombre d'états, et il admet une solution unique. En principe, donc, on peut résoudre, et la politique optimale s'en déduit. Gardez le mot « en principe » : la fin de cette section explique pourquoi il porte tout le poids de la phrase.

{{% comment %}}SOURCE: SB ch.3 p.86{{% /comment %}}

---

## Pourquoi la gourmandise redevient optimale

Nous arrivons au résultat le plus utile de la section, et il règle la dette ouverte en 4.1.

**Toute politique gloutonne par rapport à \(v_*\) est optimale.** Une **politique gloutonne** (*greedy policy*) est une politique qui, dans chaque état, choisit l'action qui maximise la quantité qu'on lui donne, sans regarder plus loin. Nous avons vu en 4.1 qu'être glouton sur la récompense immédiate est un piège. Pourquoi être glouton sur \(v_*\) ne l'est-il pas ?

Parce que \(v_*\) **contient déjà** tout le futur. La valeur optimale d'un état tient compte, par construction, de toutes les conséquences de toutes les actions, sur tout l'horizon. Un regard d'un seul pas sur \(v_*\) est donc déjà un regard sur l'infini : la myopie a été payée d'avance, une fois pour toutes, au moment de calculer \(v_*\). Un choix glouton à un pas devient alors un choix optimal à long terme. Voilà pourquoi la gourmandise était un piège en 4.1 et devient un théorème ici : ce n'est pas la gourmandise qui a changé, c'est **la quantité sur laquelle elle s'exerce**.

{{% comment %}}SOURCE: SB ch.3 p.86{{% /comment %}}

Avec \(q_*\), on fait encore mieux, et c'est le résultat charnière de toute la semaine.

> [!IMPORTANT]
 **Je dois insister : cette phrase est le pivot de la semaine, et presque de tout le cours.** Avec \(v_*\), agir optimalement demande un regard d'un pas en avant : pour comparer deux actions, il faut savoir où chacune mène, donc connaître la dynamique de l'environnement. Avec \(q_*\), il n'y a **même plus de regard en avant** : l'agent lit sa table, prend \(\argmax_a q_*(s,a)\), et c'est fini. La fonction de valeur d'action **met en cache le résultat de toutes les recherches à un pas**, et elle permet donc à l'agent d'agir optimalement **sans rien savoir des dynamiques de l'environnement**. Souligner cette ligne. C'est elle qui explique pourquoi tout ce cours, de la semaine 5 à la semaine 15, apprend des \(Q\) plutôt que des \(V\), et pourquoi l'agent de la section 4.5, qui a besoin de la dynamique, est le dernier du cours à y avoir droit.

{{% comment %}}SOURCE: SB ch.3 p.86-87{{% /comment %}}

La **Figure 4-4** montre la solution optimale du monde en grille de la section 4.2 : à gauche \(v_*\), à droite \(\pi_*\). Mettez-la côte à côte avec la Figure 4-2, qui donnait \(v_\pi\) sous la politique aléatoire, et faites la comparaison case par case : c'est le même environnement, et toutes les valeurs ont monté. Remarquez aussi, sur la carte de droite, les cases où plusieurs flèches sont dessinées : ce sont les états où plusieurs actions atteignent le maximum, et où plusieurs politiques optimales coexistent.

{{< bookfig src="04-04.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.3 p.87{{% /comment %}}

---

## Trois hypothèses, et pourquoi la solution directe est une illusion

Nous avons une caractérisation complète de l'optimalité et un système d'équations qui l'exprime. Pourquoi, alors, les onze semaines qui suivent ne consistent-elles pas à résoudre ce système ? Parce que la résolution directe repose sur trois hypothèses, et qu'elles ne tiennent presque jamais toutes les trois.

1. **La dynamique de l'environnement est connue avec exactitude.** Il faut \(p(s',r \mid s,a)\), pour tout quadruplet, et numériquement juste.
2. **On dispose d'assez de calcul** pour mener la résolution à terme.
3. **La propriété de Markov est vérifiée**, c'est-à-dire que l'état porte réellement toute l'information utile.

{{% comment %}}SOURCE: SB ch.3 p.88{{% /comment %}}

> [!WARNING]
 **Attention, c'est la deuxième hypothèse qui tombe la première, et elle tombe très vite.** Le backgammon a de l'ordre de \(10^{20}\) états. Le jeu est pourtant parfaitement connu, parfaitement markovien, et ses règles **sont** la dynamique : les hypothèses 1 et 3 sont satisfaites sans effort. Et cela ne sert à rien, parce qu'un balayage de \(10^{20}\) états ne se fait pas, aujourd'hui ni dans mille ans. Retenez la forme de cet échec : ce n'est pas un échec de modélisation, c'est un échec d'échelle, et il est déjà présent, en miniature, dans la table de seize cases du laboratoire de cette semaine.

{{% comment %}}SOURCE: SB ch.3 p.88{{% /comment %}}

Nous avons donc deux manières de nous libérer, et elles correspondent exactement aux deux moitiés de la semaine. On peut garder l'hypothèse 1 et renoncer à résoudre d'un coup : c'est la **programmation dynamique** (*dynamic programming*), et c'est la section 4.4. Ou bien on peut renoncer à l'hypothèse 1, apprendre par interaction, et accepter de ne travailler que sur des échantillons : c'est l'apprentissage par différences temporelles, et c'est la section 4.6.

{{% comment %}}SOURCE: LAPAN ch.5 p.149{{% /comment %}}

---

## Q avant V, et la raison est purement pratique

Avant de passer aux algorithmes, je veux justifier un choix qui va structurer tout le cours : nous apprendrons des valeurs d'action plus souvent que des valeurs d'état. L'argument est pratique et il tient en deux lignes.

Pour agir à partir d'une table de \(Q\), l'agent n'a besoin **que de la table**. Il lit la ligne de l'état courant et prend le plus grand nombre. Pour agir à partir d'une table de \(V\), il doit, pour chaque action, savoir dans quels états elle risque de le mener et avec quelles probabilités, donc **connaître la dynamique**, que nous ne connaissons presque jamais à l'avance. Le \(Q\) coûte plus cher en mémoire, une case par couple état-action au lieu d'une case par état, et il achète en échange l'autonomie.

{{% comment %}}SOURCE: LAPAN ch.5 p.152{{% /comment %}}

Prenons un exemple numérique, parce qu'il va rendre le \(Q\) palpable et qu'il préfigure exactement le glissement de FrozenLake. Un état central \(s_0\), entouré de quatre états terminaux. Quatre actions : haut, bas, gauche, droite. L'environnement est glissant de la façon suivante : l'action demandée est exécutée avec une probabilité de 33 %, et l'agent part dans l'une ou l'autre des deux directions **perpendiculaires**, chacune avec 33 % également. Prenons \(\gamma = 1\). Les quatre états terminaux rapportent respectivement 1 en haut, 2 à gauche, 3 en bas et 4 à droite, et comme ils sont terminaux, leurs valeurs valent exactement ces récompenses. La **Figure 4-5** dessine ce petit diagramme de transitions.

{{< bookfig src="04-05.png" week="04" >}}

{{% comment %}}SOURCE: LAPAN ch.5 p.150-151{{% /comment %}}

Calculons \(Q(s_0, \text{haut})\). Demander « haut » donne : 33 % d'aller en haut, donc d'encaisser 1 ; 33 % de glisser à gauche, donc 2 ; 33 % de glisser à droite, donc 4. Les quatre valeurs se calculent de la même façon.

| Action demandée | Somme des trois issues possibles | \(Q(s_0, a)\) |
| --- | --- | --- |
| haut | \(0{,}33 \times (1 + 2 + 4)\) | **2,31** |
| gauche | \(0{,}33 \times (2 + 1 + 3)\) | **1,98** |
| droite | \(0{,}33 \times (4 + 1 + 3)\) | **2,64** |
| bas | \(0{,}33 \times (3 + 2 + 4)\) | **2,97** |

{{% comment %}}SOURCE: LAPAN ch.5 p.150-151{{% /comment %}}

La valeur de l'état s'obtient alors par un \(\max\) sur cette colonne : \(V(s_0) = 2{,}97\), et l'action gloutonne est « bas ».

Prenez trente secondes sur ce résultat, parce qu'il est contre-intuitif et instructif. L'action « bas » ne mène où elle promet qu'une fois sur trois. Deux fois sur trois, l'agent part sur le côté. Et c'est **quand même** la meilleure action, parce que ses deux glissements possibles mènent vers les deux états les plus valeureux. Une valeur d'action n'évalue pas une intention : elle évalue une intention **dans un environnement bruité**, glissements compris. C'est précisément pour cela qu'on ne peut pas la deviner à l'œil.

> [!NOTE]
 **Notez bien une convention de notation, parce que vous allez rencontrer l'autre ailleurs.** Dans ce cours, les minuscules \(v_\pi\) et \(q_\pi\) désignent les valeurs **vraies** et les majuscules \(V\) et \(Q\) des **estimations**. Vous croiserez, dans la littérature et dans beaucoup d'implémentations, les majuscules employées là où nous écrivons les minuscules, et un \(V\) qui désigne en réalité \(v_*\). Ce n'est pas une faute de leur part, c'est une autre convention, mais elle rend invisible la distinction la plus importante de la semaine 5. La page « Notation » du cours fait foi : au moindre doute, demandez-vous si le symbole que vous lisez désigne une cible ou un tableau en mémoire. Dans l'exemple ci-dessus, j'ai écrit \(Q\) et \(V\) en majuscules parce que les quatre nombres sont bien, déjà, une estimation calculée.
