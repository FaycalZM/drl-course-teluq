---
title: "8.2 Le théorème du gradient de politique"
weight: 3
---

## Une performance qu'on ne sait pas dériver

Nous voulons faire monter une quantité. Commençons par dire laquelle, précisément, parce que toute la section tient à cette définition.

Dans le cas épisodique, la performance d'une politique est la valeur de son état de départ :

$$
J(\theta) \defeq v_{\pi_\theta}(s_0)
$$

où \(s_0\) est un état de départ fixé. C'est une définition confortable : un seul nombre, et il mesure exactement ce qui nous intéresse, à savoir ce que rapporte la politique quand on la laisse jouer depuis le début. Nous voulons donc **maximiser** \(J(\theta)\) en déplaçant \(\theta\), et pour cela nous avons besoin de \(\nabla J(\theta)\).

{{% comment %}}SOURCE: SB ch.13 p.346{{% /comment %}}

Et c'est ici qu'apparaît la difficulté, qui n'est pas technique mais structurelle. La performance dépend de **deux** choses, et le paramètre \(\theta\) agit sur les deux.

La première est le **choix des actions**, et celle-là ne pose aucun problème : l'effet de \(\theta\) sur les probabilités d'action est directement calculable à partir de la paramétrisation, c'est-à-dire par rétropropagation dans le réseau. La seconde est la **distribution des états dans lesquels ces choix sont faits**. Changez légèrement la politique, et l'agent ne visite plus les mêmes états, dans les mêmes proportions. Or l'effet de \(\theta\) sur la distribution des états passe entièrement par la **dynamique de l'environnement**, et cette dynamique nous est inconnue : c'est précisément l'hypothèse du cadre sans modèle, depuis la semaine 4.

{{% comment %}}SOURCE: SB ch.13 p.346{{% /comment %}}

Si vous prenez la dérivée naïvement, vous obtenez donc un terme que vous ne savez pas calculer, et pire, que vous ne savez même pas estimer, puisqu'il faudrait pour cela dériver une fonction du monde. Formulé ainsi, le problème paraît fermé.

> [!NOTE]
 **Reformulons la difficulté dans les termes de la semaine 2, parce que c'est là qu'elle devient tangible.** Pour qu'une rétropropagation calcule le gradient d'une quantité, cette quantité doit être au bout d'un graphe de calcul dérivable. Or entre notre réseau et la récompense observée se trouve l'environnement : une boîte noire, éventuellement un simulateur physique, éventuellement un marché. Elle n'est pas dans le graphe. Le théorème qui suit dit, en substance, qu'on peut malgré tout obtenir le gradient que l'on cherche, et que le seul objet dérivable dont on ait besoin est le réseau lui-même.

---

## Le théorème, et ce qu'il ne contient pas

Voici le résultat. C'est la seule véritable mathématique de la semaine, et tout le reste en est une conséquence ou une implémentation.

$$
\nabla J(\theta) \propto \sum_{s} \mu(s) \sum_{a} q_\pi(s,a)\, \nabla \pi(a \mid s, \theta)
$$

{{% comment %}}SOURCE: SB éq. 13.5 p.348{{% /comment %}}

Lisez maintenant ce que cette expression **ne contient pas**. Elle ne contient aucune dérivée de la dynamique de l'environnement. Elle ne contient aucune dérivée de \(\mu\), la distribution des états. Le seul gradient qui y figure est \(\nabla \pi(a\mid s,\theta)\), le gradient de la politique par rapport à ses propres paramètres, c'est-à-dire exactement la seule chose que notre réseau sait produire. Voilà pourquoi tout ce qui suit est possible : **le théorème a éliminé le terme inconnu**, et il l'a fait sans l'approcher et sans l'ignorer, par une identité exacte.

{{% comment %}}SOURCE: SB ch.13 p.348{{% /comment %}}

Trois précisions sur les symboles, et chacune est un rappel.

\(\mu(s)\) est la **distribution sur politique** (*on-policy distribution*) des états, c'est-à-dire la fraction du temps que l'agent passe en \(s\) lorsqu'il suit \(\pi\). Vous l'avez déjà rencontrée en semaine 5, comme poids de l'objectif \(\overline{VE}(\mathbf{w})\) : c'est le même objet, et c'est la même raison qui le fait apparaître, à savoir qu'une somme sur les états n'a de sens que pondérée par leur fréquence de visite.

{{% comment %}}SOURCE: SB ch.13 p.348{{% /comment %}}

\(q_\pi(s,a)\) est la valeur d'action **vraie** sous \(\pi\), et non une estimation. Ne vous précipitez pas pour conclure qu'il faut donc apprendre \(q_\pi\) avant de pouvoir utiliser le théorème : l'étape suivante va le faire disparaître.

Et le signe \(\propto\), qui n'est pas une négligence. Dans le cas épisodique, la relation est une proportionnalité et la constante omise est la **longueur moyenne d'un épisode**. Elle est strictement positive, donc elle ne change ni la direction du gradient ni le signe d'aucune de ses composantes : elle est absorbée dans le pas d'apprentissage \(\alpha\), qu'on règle de toute façon empiriquement. Dans le cas continu, la constante vaut 1 et la relation devient une égalité. Le cours garde le \(\propto\), parce qu'il est exact et qu'il rappelle au lecteur qu'il n'y a jamais eu besoin de connaître cette constante.

{{% comment %}}SOURCE: SB ch.13 p.348{{% /comment %}}

Un mot sur la preuve, et ce sera le seul. Elle tient en une page, elle n'utilise que du calcul différentiel élémentaire, et son unique ressort est le **déroulement répété** de la récursion sur \(\nabla v_\pi(s)\), celle que vous avez vue en semaine 4 sous le nom d'équation de Bellman. Je ne la reproduis pas ici, parce que la recopier n'apprendrait rien de plus que ce que l'énoncé dit déjà : le terme inconnu disparaît parce que la récursion se télescope.

{{% comment %}}SOURCE: SB ch.13 p.347{{% /comment %}}

---

## Du théorème à l'échantillon : deux substitutions, et rien d'autre

Le théorème est exact et inutilisable tel quel. Il demande une somme sur **tous** les états, pondérée par une distribution \(\mu\) que nous ne connaissons pas, et une somme sur **toutes** les actions, pondérée par une valeur \(q_\pi\) que nous ne connaissons pas non plus. Deux étapes suffisent à en faire quelque chose de calculable, et ces deux étapes sont de la **même nature**. Je vais vous la donner d'abord en français, parce que c'est la phrase à retenir de toute la section :

**une somme pondérée par une probabilité est une espérance, et une espérance s'échantillonne.**

Première substitution, sur les **états**. La somme \(\sum_s \mu(s)(\cdots)\) est, par définition de \(\mu\), l'espérance de \((\cdots)\) sous la distribution des états visités. Or il existe une façon très simple d'échantillonner cette distribution : **suivre la politique**. En jouant \(\pi\), l'agent visite les états exactement dans les proportions \(\mu\), sans que nous ayons à les calculer.

$$
\nabla J(\theta) \propto \sum_{s}\mu(s)\sum_a q_\pi(s,a)\nabla\pi(a\mid s,\theta) = \E_\pi\!\left[\sum_a q_\pi(S_t,a)\,\nabla\pi(a \mid S_t,\theta)\right]
$$

{{% comment %}}SOURCE: SB éq. 13.6 p.348{{% /comment %}}

À ce stade, une pause est instructive. On **pourrait** s'arrêter ici et construire un algorithme : il resterait une somme sur les actions, calculable puisque les actions sont énumérables, à condition de disposer d'une estimation \(\hat q(S_t,a,\mathbf{w})\) de la valeur de chacune. La mise à jour serait \(\theta_{t+1} \defeq \theta_t + \alpha \sum_a \hat q(S_t,a,\mathbf{w})\,\nabla \pi(a \mid S_t,\theta)\), qui porte le nom de **méthode toutes actions**, parce qu'elle regarde toutes les actions à chaque pas. Elle est correcte, et nous ne la suivrons pas : REINFORCE n'utilisera que \(A_t\), l'action **réellement prise**, ce qui lui évite d'avoir à estimer \(q\) pour les autres.

{{% comment %}}SOURCE: SB éq. 13.7 p.348{{% /comment %}}
{{% comment %}}SOURCE: SB ch.13 p.348{{% /comment %}}

Seconde substitution, sur les **actions**, et elle emploie exactement la même idée que la première. La somme \(\sum_a (\cdots)\) n'est pas encore pondérée par une probabilité, alors fabriquons-en une : multiplions et divisons par \(\pi(a\mid S_t,\theta)\). La somme devient une espérance sous \(\pi\), que l'on échantillonne en remplaçant \(a\) par l'action tirée \(A_t \sim \pi\). Et \(q_\pi\) disparaît au passage, parce que \(\E_\pi[G_t \mid S_t, A_t] = q_\pi(S_t,A_t)\) : la valeur d'action est, par définition, l'espérance du retour, et un retour observé en est donc un échantillon non biaisé.

$$
\begin{aligned}
\nabla J(\theta) &= \E_\pi\!\left[\sum_a \pi(a\mid S_t,\theta) q_\pi(S_t,a)\frac{\nabla\pi(a\mid S_t,\theta)}{\pi(a\mid S_t,\theta)}\right] \\[6pt]
&= \E_\pi\!\left[q_\pi(S_t,A_t)\frac{\nabla\pi(A_t\mid S_t,\theta)}{\pi(A_t\mid S_t,\theta)}\right] \\[6pt]
&= \E_\pi\!\left[G_t\frac{\nabla\pi(A_t\mid S_t,\theta)}{\pi(A_t\mid S_t,\theta)}\right]
\end{aligned}
$$

{{% comment %}}SOURCE: SB p.349, dérivation non numérotée{{% /comment %}}

De la première ligne à la deuxième, on a remplacé \(a\) par l'échantillon \(A_t \sim \pi\). De la deuxième à la troisième, on a remplacé \(q_\pi(S_t,A_t)\) par \(G_t\), parce que l'un est l'espérance de l'autre. Voilà toute la dérivation. Le tableau suivant la résume en trois lignes, et c'est lui qu'il faut savoir refaire.

| | Expression | Ce qui est nouveau |
| --- | --- | --- |
| le théorème | \(\nabla J(\theta) \propto \sum_s \mu(s)\sum_a q_\pi(s,a)\nabla\pi(a\mid s,\theta)\) | exact, mais somme sur **tous** les états et **toutes** les actions ; demande \(q_\pi\) et \(\mu\), dont nous n'avons ni l'un ni l'autre |
| somme sur les états échantillonnée | \(= \E_\pi\!\left[\sum_a q_\pi(S_t,a)\nabla\pi(a\mid S_t,\theta)\right]\) | la somme sur les états devient une espérance, parce que suivre \(\pi\) visite les états exactement dans les proportions \(\mu\) |
| somme sur les actions échantillonnée | \(= \E_\pi\!\left[G_t \dfrac{\nabla\pi(A_t\mid S_t,\theta)}{\pi(A_t\mid S_t,\theta)}\right]\) | la somme sur les actions devient une espérance à son tour, et \(q_\pi\) s'efface parce qu'un retour observé en est un échantillon |

{{% comment %}}SOURCE: SB ch.13 p.348-349{{% /comment %}}

La dernière ligne est entièrement **estimable à partir d'une trajectoire jouée** : un état visité, une action tirée, un retour observé, et un gradient que PyTorch calcule. Nous avons un algorithme.

---

## Une convention d'actualisation, fixée ici et tenue toute la semaine

Un détail de formalisme, et je le tranche maintenant pour ne pas y revenir.

La mesure de performance \(J(\theta) \defeq v_{\pi_\theta}(s_0)\) et les équations ci-dessus sont écrites dans le cadre **sans actualisation**, c'est-à-dire avec \(\gamma = 1\) dans la définition de la performance. Dans le cas général actualisé, la mise à jour effectuée au pas \(t\) porte un facteur supplémentaire \(\gamma^t\), qui pèse d'autant moins les décisions tardives d'un épisode, et qui se transporte commodément sous la forme d'un facteur courant initialisé à 1 et multiplié par \(\gamma\) à chaque pas.

**La convention du cours, pour toute la semaine : les équations s'écrivent sans ce facteur \(\gamma^t\).** Le facteur d'actualisation n'apparaît donc qu'à un seul endroit, à l'intérieur du retour \(G_t\), où nous l'utilisons depuis la semaine 1. C'est le choix que fait l'immense majorité des implémentations, y compris celles que nous écrirons, et c'est pourquoi je l'adopte : une formule et un code qui se correspondent terme à terme valent mieux qu'une formule plus générale que personne n'implémente. Si vous voyez ailleurs un \(\gamma^t\) devant une mise à jour de gradient de politique, vous saurez d'où il vient et ce qu'il fait.

{{% comment %}}SOURCE: SB ch.13 p.350{{% /comment %}}
{{% comment %}}SOURCE: SB ch.13 p.354{{% /comment %}}

---
