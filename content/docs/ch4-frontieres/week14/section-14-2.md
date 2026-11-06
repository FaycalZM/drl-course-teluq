---
title: "14.2 Demander « laquelle est meilleure ? », et rien de plus"
weight: 3
---

## La substitution, et elle tient en une phrase

Voici l'idée, et elle est d'une simplicité qui désarme : **on garde l'algorithme et on remplace la récompense.**

Tout ce que vous avez appris reste en place. L'acteur-critique de la semaine 8 reste l'acteur-critique de la semaine 8 ; la boucle d'interaction reste la même ; les enveloppes, les lots, le gradient, l'entropie, tout est inchangé. La seule chose qui change est l'origine du nombre : au lieu de venir de l'environnement, il vient d'un réseau \(\hat r(O_t, A_t)\) qui a été ajusté sur des données **déduites de préférences humaines**.

{{% comment %}}SOURCE: LAPAN ch.19 p.575{{% /comment %}}

Notez le mot « déduites », parce qu'il porte toute la difficulté intéressante. Personne ne fournit de récompense. On fournit des **comparaisons**, et il faut en déduire un nombre par pas de temps. C'est un problème d'inférence, et la section 14.6 montrera qu'il est sous-déterminé d'une manière précise.

---

## Le datum : deux segments et une étiquette

Précisons ce qu'on demande exactement à la personne, parce que la forme de la question détermine tout le reste.

Un **segment d'épisode** (*episode segment*) est une suite de longueur fixe de couples observation-action, prélevée dans le déroulement d'un épisode. Écrivons-la

$$
\zeta = \big( (o_1, a_1), (o_2, a_2), \dots, (o_L, a_L) \big)
$$

avec \(L\) la longueur, la même pour tous les segments. Dans la chaîne que nous allons suivre, \(L = 50\), c'est-à-dire environ trois secondes de jeu.

On en prélève **deux**, on les montre côte à côte, et on pose une seule question : laquelle de ces deux séquences est la meilleure ? La personne dispose de quatre réponses : la première, la seconde, **les deux sont bonnes**, ou **je ne peux pas juger**.

{{% comment %}}SOURCE: LAPAN ch.19 p.575{{% /comment %}}

L'**étiquette** (*label*) code cette réponse sous la forme d'un couple \((y_1, y_2)\) :

| Réponse de la personne | \(y_1\) | \(y_2\) | Ce que ça veut dire pour le modèle |
| --- | --- | --- | --- |
| le premier segment est meilleur | 1 | 0 | toute la masse sur \(\zeta^1\) |
| le second segment est meilleur | 0 | 1 | toute la masse sur \(\zeta^2\) |
| les deux sont bons | 0,5 | 0,5 | aucune préférence, et c'est une information |
| je ne peux pas juger | aucune | aucune | la paire est **écartée**, elle n'entre pas dans \(D\) |

{{% comment %}}SOURCE: LAPAN ch.19 p.575{{% /comment %}}

L'ensemble des triplets \((\zeta^1, \zeta^2, y)\) ainsi obtenus forme le jeu d'étiquettes \(D\), et c'est le seul contact de toute la chaîne avec un jugement humain.

> [!NOTE]
 **La quatrième réponse n'est pas un détail d'interface, et je veux que vous notiez ce qu'elle fait.** « Je ne peux pas juger » retire la paire des données. C'est raisonnable du point de vue de la personne, qui n'a pas à inventer un avis qu'elle n'a pas. Mais du point de vue du jeu de données, cela signifie que **les cas ambigus sont absents par construction**, et donc que le modèle n'apprendra jamais à être incertain : il n'aura vu que des cas où quelqu'un savait trancher. Gardez cette remarque en tête ; nous la retrouverons en section 14.16 sous une forme beaucoup moins anodine, appliquée non pas à un modèle de récompense mais à l'évaluation d'un détecteur.

---

## Le modèle de préférence : de deux sommes à une probabilité

Il nous faut maintenant un lien entre « cette personne préfère ce segment » et « ce réseau prédit ces nombres ». Voici l'hypothèse, et c'est la seule de la section.

**Intuition.** Supposons que la personne juge un segment à l'aune de la récompense totale qu'il contient. Alors plus la somme des récompenses du premier segment dépasse celle du second, plus la personne devrait préférer le premier, et plus l'écart est petit, plus son choix devrait ressembler à un tirage au sort. On veut donc une fonction qui transforme un écart de sommes en une probabilité de préférence : grande quand l'écart est grand et positif, proche d'un demi quand l'écart est nul.

**L'équation.** Notons d'abord la somme prédite sur chaque segment :

$$
R_i = \sum_{t=1}^{L} \hat r\big(o^i_t, a^i_t\big), \qquad i \in \{1, 2\}
$$

La probabilité que le premier segment soit préféré s'écrit alors comme une exponentielle normalisée sur les deux sommes :

$$
\hat P\big[\zeta^1 \succ \zeta^2\big] = \frac{\exp \sum_{t} \hat r(o^1_t, a^1_t)}{\exp \sum_{t} \hat r(o^1_t, a^1_t) + \exp \sum_{t} \hat r(o^2_t, a^2_t)}
$$

{{% comment %}}SOURCE: LAPAN ch.19 p.575 (éq. transcrite depuis l'image de page){{% /comment %}}

Trois remarques sur cette équation, et chacune compte pour la suite.

**La somme, et non la moyenne.** Le modèle note des couples observation-action individuels, mais la préférence porte sur un segment entier. C'est la **somme** sur les \(L\) pas qui entre dans la comparaison, ce qui veut dire que le signal d'apprentissage est réparti sur cinquante pas sans qu'on sache lequel d'entre eux était décisif. C'est l'attribution de crédit, le problème de toujours, et ici elle est portée par le gradient de la somme.

**La symétrie.** Par construction, \(\hat P[\zeta^2 \succ \zeta^1] = 1 - \hat P[\zeta^1 \succ \zeta^2]\). Il n'y a qu'un seul nombre libre dans cette comparaison, pas deux.

**Et l'essentiel, que nous allons exploiter en section 14.6 :** cette probabilité ne dépend que de la **différence** \(R_1 - R_2\). Ajoutez une constante à \(\hat r\) partout, et les deux sommes augmentent du même montant, et rien ne change.

---

## La perte, et ce qu'elle contraint exactement

**Intuition.** Nous avons une étiquette observée \((y_1, y_2)\) et une probabilité prédite. Ajuster l'une sur l'autre est un problème de classification binaire, et la perte qui convient est celle de la semaine 2 : l'entropie croisée.

**L'équation.**

$$
\mathrm{perte}(\hat r) = - \sum_{(\zeta^1, \zeta^2, y) \in D} \Big[\, y_1 \log \hat P\big[\zeta^1 \succ \zeta^2\big] + y_2 \log \hat P\big[\zeta^2 \succ \zeta^1\big] \Big]
$$

{{% comment %}}SOURCE: LAPAN ch.19 p.575 (éq. transcrite depuis l'image de page){{% /comment %}}

Lisez-la une fois avec chaque étiquette possible, c'est le meilleur moyen de la comprendre.

Si \(y = (1, 0)\), seul le premier terme survit et la perte vaut \(-\log \hat P[\zeta^1 \succ \zeta^2]\) : on pousse la probabilité du premier segment vers 1, donc \(R_1 - R_2\) vers le haut. Si \(y = (0, 1)\), c'est l'inverse. Et si \(y = (0{,}5\,;0{,}5)\), les deux termes pèsent autant, et la perte est minimale quand les deux probabilités valent un demi, c'est-à-dire quand **\(R_1 = R_2\)**. Retenez cette dernière lecture : la section 14.6 va montrer que le code ne fait pas cela du tout.

> [!IMPORTANT]
 **La propriété la plus importante de cette perte est une invariance, et elle explique une étape que vous verrez en section 14.7.** Comme la probabilité ne dépend que de \(R_1 - R_2\), ajouter une constante \(c\) à \(\hat r\) en tous ses points ajoute \(Lc\) à \(R_1\) **et** à \(R_2\), laisse leur différence intacte, et donc **ne change pas la perte d'un iota**. Conséquence : cette perte ne détermine la récompense qu'**à une constante additive près**. Elle ne dit pas si un segment moyen vaut zéro, dix ou mille, elle dit seulement lequel vaut plus que lequel. Ce n'est pas un défaut, c'est exactement ce que des comparaisons peuvent apprendre, et c'est la raison pour laquelle on normalise la récompense prédite avant de la donner à l'agent. Nous écrirons cette normalisation en section 14.7.

---
