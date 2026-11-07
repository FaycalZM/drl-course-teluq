---
title: "15.8 Un nom n'est pas une preuve"
weight: 9
---

## Trois cas, et la même erreur de lecture

Cette section est courte et c'est, je crois, le cadeau le plus directement utile que cette semaine fait à votre rapport final. Elle réunit trois cas où **le nom donné à une méthode ne correspond pas à ce que le code fait**, et où la vérification prend trois minutes à quelqu'un qui a suivi ce cours.

Je les énonce comme des faits du cours, sans désigner personne, parce que ce n'est pas un procès : dans les trois cas, l'erreur est **naturelle**, elle vient d'un mot qui paraît dire ce qu'on croit qu'il dit, et vous la commettrez à votre tour si vous ne connaissez pas le réflexe. Le réflexe est à la fin de la section.

---

## Premier cas : un nom qui dit « asynchrone » et un code qui est synchrone

Vous rencontrerez l'agent de clic de la section 15.4 décrit comme une méthode **asynchrone**. Il ne l'est pas, et la vérification tient en deux observations.

**Première observation, l'architecture.** Il y a **une** classe de réseau : deux couches convolutives, un aplatissement, puis **une** couche linéaire pour la politique et **une** couche linéaire pour la valeur. Un tronc partagé, deux têtes, un optimiseur. C'est l'architecture de la semaine 8.

{{% comment %}}SOURCE: LAPAN ch.14 p.441 (image){{% /comment %}}

**Seconde observation, le parallélisme.** Huit navigateurs tournent en même temps, lancés dans huit sous-processus par le vectoriseur d'environnements de Gymnasium, celui dont le nom contient le mot « asynchrone ».

Et c'est là que la lecture dérape, donc disons précisément ce que ce vectoriseur fait. **Il parallélise le pas d'environnement, pas le gradient.** Les huit navigateurs avancent d'un pas chacun dans leur propre sous-processus, leurs huit transitions sont rassemblées dans un lot, et ce lot alimente **une seule mise à jour synchrone** d'**un seul** jeu de poids. C'est exactement ce que la semaine 8 appelait un **environnement vectorisé** (*vectorized environment*), et c'est la forme que ce cours a retenue dès la semaine 8, pour une raison de faisabilité qu'elle avait donnée.

Une méthode de gradient de politique véritablement asynchrone fait tout autre chose, et la semaine 8 l'a décrite : **plusieurs travailleurs**, chacun détenant **sa propre copie** du réseau, chacun calculant ses propres gradients sur ses propres trajectoires, et les poussant **sans se synchroniser** dans un jeu de paramètres partagé. Il y a donc plusieurs copies du réseau, et les mises à jour arrivent dans un ordre que personne ne contrôle.

Ici : **un** réseau, **une** mise à jour par lot, **aucune** copie concurrente. L'agent de la section 15.4 est un **acteur-critique à avantage avec environnements vectorisés**, c'est-à-dire la méthode de la semaine 8. Le mot « asynchrone » du nom de la classe qualifie les **environnements**, et il a été lu comme qualifiant l'algorithme.

{{% comment %}}SOURCE: LAPAN ch.14 p.441 (image){{% /comment %}} {{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

Pour l'anecdote mesurée, et parce qu'elle montre que la méthode fonctionne très bien sous son vrai nom : sur la tâche élémentaire de clic, cet agent atteint une récompense moyenne de **0,9 en huit minutes**.

{{% comment %}}SOURCE: LAPAN ch.14 p.441 (image){{% /comment %}}

---

## Deuxième cas : une borne de confiance supérieure qui n'en est pas une

Vous rencontrerez la règle de descente de la section 15.5 présentée sous le nom de **borne de confiance supérieure**, dans sa variante historique. Ce n'en est pas une, et la semaine 12 vous a donné de quoi le voir en dix secondes.

La borne de confiance supérieure classique est une formule de bandit, et elle a deux propriétés caractéristiques. Son terme d'exploration est en \(\sqrt{\ln N / n}\), avec un **logarithme**. Et elle ne contient **aucune probabilité a priori** : c'est tout son intérêt, elle ne suppose rien et n'a besoin de rien d'autre que des comptages.

Regardez maintenant le terme d'exploration de la section 15.5 :

$$
U(s_t, a) \;=\; c \, P(s_t, a) \, \frac{\sqrt{\sum_{a'} N(s_t, a')}}{1 + N(s_t, a)}
$$

Pas de logarithme : une racine carrée de la **somme** des visites. Et un facteur \(P(s_t, a)\), la **probabilité a priori** fournie par la tête de politique du réseau. Ce sont les deux signatures de la variante que la semaine 12 a enseignée sous son vrai nom, celle qui pondère l'exploration par l'avis d'un réseau. Ce cours la nomme comme la semaine 12 l'a nommée, et renvoie à la page de la semaine 12 plutôt que de la redériver.

{{% comment %}}SOURCE: LAPAN ch.21 p.656 (image), p.657 (image){{% /comment %}} {{% comment %}}SOURCE: source-assets/raw-content/week-12.md §12.4{{% /comment %}}

Et une troisième petite chose, dans la même règle, qui est une erreur de notation et non de nom, mais qui relève du même réflexe. La **perte virtuelle**, ce correctif temporaire qui empêche plusieurs descentes parallèles d'emprunter la même arête, se retranche de \(W(s_t, a)\), c'est-à-dire de la statistique de valeur de l'arête. Elle ne peut pas se retrancher de \(A_t\) : \(A_t\) est **l'action choisie**, c'est-à-dire un indice entre 0 et 11, et retrancher une perte d'un indice n'a aucun sens. Lire une notation suffit parfois à repérer un énoncé impossible.

{{% comment %}}SOURCE: LAPAN ch.21 p.657 (image){{% /comment %}}

---

## Troisième cas : une borne vraie, dans la mauvaise métrique

Le troisième cas est le plus intéressant des trois, parce que le nombre cité est **exact** et que la conclusion qu'on en tire est néanmoins fausse. Et il y a **deux raisons indépendantes** à cela, dont la seconde enseigne davantage que la première.

**Rappelons d'abord le fait connu.** On a établi en 2010 que **vingt** rotations suffisent à résoudre n'importe quel état d'un cube trois par trois. Ce nombre est célèbre sous le nom de **nombre de Dieu** (*God's number*).

Ce résultat est exact, et il est énoncé dans une métrique précise : la **métrique des demi-tours** (*half-turn metric*), dans laquelle un demi-tour, c'est-à-dire une rotation d'un quart de tour suivie d'une seconde dans le même sens, compte pour **un seul coup**. C'est la métrique naturelle du résultat parce que c'est celle dans laquelle le calcul a été mené.

**Maintenant regardons l'implémentation de la section 15.5.** Elle a **douze actions**, et nous avons noté dans cette section la phrase qui décide de tout : les demi-tours ne sont pas des actions distinctes, ils coûtent **deux** actions. L'implémentation compte donc dans la **métrique des quarts de tour** (*quarter-turn metric*).

{{% comment %}}SOURCE: LAPAN ch.21 p.646{{% /comment %}}

Et dans la métrique des quarts de tour, la borne n'est pas vingt. **Elle est 26**, et ce résultat a été établi en 2014. Ce cours l'énonce en son propre nom, parce que c'est le nombre dont son propre modèle a besoin : un solveur à douze actions qui compte un demi-tour pour deux coups ne peut pas saturer à vingt, puisque vingt n'est pas une borne dans ses unités.

**Première raison, donc : les unités.** Une borne de vingt et un compteur en quarts de tour ne se parlent pas. La borne dans les unités du compteur vaut 26.

**Seconde raison, et c'est elle qu'il faut emporter.** Même avec le bon nombre, la prédiction serait fausse, et pour une raison qui n'a rien à voir avec les métriques.

On rencontre le raisonnement suivant : puisqu'aucun cube ne demande plus de vingt coups, un solveur devrait **saturer** au-delà d'une profondeur de brouillage de vingt, c'est-à-dire résoudre aussi bien les cubes brouillés par cinquante coups que ceux brouillés par vingt. Le raisonnement confond deux quantités différentes.

**Une profondeur de brouillage n'est pas une longueur de solution optimale.** Brouiller un cube par \(d\) rotations tirées au hasard produit un état dont la solution optimale fait **au plus** \(d\) coups, et le plus souvent **moins** : les rotations tirées au hasard **s'annulent** entre elles. Tournez une face dans un sens puis dans l'autre, vous avez dépensé deux coups de brouillage et vous êtes à zéro coup du but. Plus \(d\) est grand, plus la distribution des distances réelles au but se concentre, et elle se concentre vers une valeur qui n'a rien à voir avec \(d\).

Par conséquent, une courbe de taux de résolution en fonction de la profondeur de brouillage ne mesure **pas** la relation entre la performance du solveur et la difficulté théorique. Elle mesure la **portée du solveur** sur la distribution d'états que le brouillage produit. Une saturation, si elle apparaît, est une propriété du solveur et de la distribution ; une absence de saturation ne contredit aucune borne.

> [!IMPORTANT]
 **L'énoncé général dont ce cas est une instance, et c'est celui que je veux que vous appliquiez à vos propres mesures.** **Une borne théorique ne contraint une mesure que si les deux sont exprimées dans les mêmes unités.** Ici elles ne le sont ni dans la même **métrique**, puisque l'une compte les demi-tours pour un et l'autre pour deux, ni dans la même **quantité**, puisque l'une parle de longueur de solution optimale et l'autre de profondeur de brouillage. Deux désaccords d'unités empilés, et le résultat est une prédiction fausse à l'intérieur d'un modèle par ailleurs correct, commise par quelqu'un de rigoureux. C'est exactement l'erreur de mesure que le jalon 4 vous demandait d'éviter. Avant de comparer un chiffre mesuré à un chiffre théorique, écrivez les unités des deux, à côté, explicitement. Si vous ne pouvez pas les écrire, la comparaison n'a pas lieu.

---

## La phrase à emporter, et elle tient en une ligne

Trois cas, et le même réflexe les traite tous les trois.

> [!TIP]
 **Le nom d'une méthode dans un texte n'est pas une preuve de ce que fait le code.** Ni le nom d'une classe, ni le titre d'une section, ni la légende d'une figure. La preuve, c'est le code et ce sont les définitions des symboles. Et la bonne nouvelle, c'est que vous avez maintenant de quoi vérifier : si vous savez compter les réseaux et repérer une mise à jour synchrone, vous identifiez une méthode de gradient de politique en trente secondes ; si vous savez qu'une probabilité a priori dans un terme d'exploration change la nature de la règle, vous identifiez une variante de recherche arborescente aussi vite ; et si vous écrivez les unités de ce que vous comparez, aucune borne ne vous fera dire de bêtise. **Vérifiez trois choses dans n'importe quel système qu'on vous présente : combien de réseaux, quelle est la règle de mise à jour, et dans quelles unités sont les nombres.**

Et une remarque de méthode, pour que cette section ne soit pas lue comme une invitation à la défiance. Dans les trois cas ci-dessus, le **code est correct** et les **mesures sont correctes**. Ce qui est en défaut, c'est l'étiquette collée dessus. C'est une excellente nouvelle pour un praticien : cela veut dire que lire le code répare le problème, et que le travail de quelqu'un reste utilisable même quand sa prose se trompe de nom. L'attitude juste n'est pas de se méfier des textes, c'est de les **compléter** par l'objet dont ils parlent.

---
