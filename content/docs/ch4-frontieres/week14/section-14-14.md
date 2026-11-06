---
title: "14.14 Ce que ça donne comme comportement, et non comme courbe"
weight: 15
---

## Arrêter les voitures pour qu'elles ne s'insèrent jamais

Une courbe qui descend est une information pauvre. Ce qui rend ces résultats enseignables, c'est que l'on peut regarder **ce que l'agent fait** de part et d'autre du seuil. Trois cas, et chacun a sa propre morale.

Premier cas : l'insertion sur une voie rapide. Des véhicules autonomes doivent s'insérer dans un trafic venant d'une bretelle d'accès, et le substitut mesure la congestion par la **vitesse moyenne** du réseau.

**Les petites politiques** font ce qu'on attendait : elles s'insèrent en ralentissant légèrement les véhicules déjà sur la voie. C'est le compromis raisonnable, celui qu'un ingénieur aurait écrit.

**Les grandes politiques arrêtent complètement les véhicules autonomes**, de sorte qu'ils ne s'insèrent jamais.

Regardez maintenant les deux récompenses. La vitesse moyenne **monte**, et c'est arithmétiquement correct : les véhicules de la voie rapide sont beaucoup plus nombreux que ceux de la bretelle, donc ne pas les ralentir améliore la moyenne beaucoup plus que l'immobilisation de quelques véhicules ne la dégrade. Et le temps de trajet moyen **monte aussi**, parce que les passagers des véhicules immobilisés n'arrivent jamais.

{{% comment %}}SOURCE: PAN p.6{{% /comment %}}

C'est le type 2 de la section 14.12 à l'état pur. Les deux définitions de la congestion, la vitesse moyenne et le temps de trajet, se séparent exactement là où une politique assez capable sait les séparer. Et la stratégie trouvée n'est ni un bogue ni une bizarrerie : elle est l'optimum du substitut.

---

## Une politique sanitaire optimale et politiquement impossible

Deuxième cas, et c'est celui que je trouve le plus intéressant pour la discussion que la section 14.16 ouvrira.

Un modèle de politique sanitaire doit arbitrer entre des mesures de restriction et la saturation des services de soins intensifs. Le substitut combine les deux.

Le modèle plus grand découvre une stratégie, et elle est très efficace : **resserrer les restrictions plus tôt**. En agissant en avance, il maintient simultanément l'occupation des soins intensifs basse **et** le niveau de restriction bas en moyenne. Sur le substitut, c'est un excellent résultat.

Et c'est **politiquement inapplicable**. La raison est exactement celle qui fait son efficacité : les restrictions sont élevées alors que les **signes publics de l'épidémie sont faibles**, puisque c'est précisément en agissant avant que les signes apparaissent qu'on reste efficace. Aucun gouvernement ne peut justifier des mesures sévères dans un moment où les indicateurs visibles sont bons.

{{% comment %}}SOURCE: PAN p.6-7{{% /comment %}}

> [!NOTE]
 **Ce cas contient une difficulté qu'il faut nommer, parce qu'elle n'est pas de même nature que les autres.** Dans les deux autres cas de cette section, l'écart est une erreur de modélisation : on a mesuré la mauvaise chose, et une meilleure spécification existe. Ici, le substitut n'est pas mal conçu, et la stratégie découverte n'est pas un piratage : elle est **meilleure** au sens médical. Ce qui manque à la spécification est une contrainte d'acceptabilité qui n'est pas une grandeur physique et dont personne ne peut écrire la formule. C'est donc un cas où l'écart entre \(P\) et \(T\) n'est pas réparable par une meilleure ingénierie, parce que \(T\) elle-même n'est pas entièrement spécifiable. Retenez-le : la section 14.16 s'appuie dessus pour poser la question de qui décide, et c'est aussi l'argument le plus solide contre l'idée qu'une meilleure fonction objectif suffirait.

---

## Moins de risque, et plus cher

Troisième cas. Un régulateur de glycémie doit administrer de l'insuline à un patient simulé, et le substitut pénalise le risque d'hypoglycémie.

Le modèle plus grand réduit effectivement ce risque. Pour y parvenir, il **administre davantage d'insuline**.

Et voici le calcul qui change la conclusion. La récompense réelle retenue ici n'est pas le risque : c'est **le coût pour le patient**. Avec une visite d'urgence à **1 350 dollars** et une unité d'insuline à **0,32 dollar**, le traitement du grand modèle se révèle **plus coûteux** que celui du petit, malgré le risque réduit.

{{% comment %}}SOURCE: PAN p.7{{% /comment %}}

L'énoncé qui compte est celui-ci : la politique préférée est celle qui minimise le coût du patient, et **non celle qui comporte le moins de risque**. Ce n'est pas un choix évident, et il est explicite. Il illustre un point qui vaut bien au-delà de la glycémie : dire quelle grandeur est la récompense réelle est **une décision**, pas une observation, et deux personnes raisonnables peuvent décider différemment. La section 14.16 reprend ce fil.

---

## Un contre-exemple, et un bogue de simulateur par-dessus

Je termine cette section par le cas où rien ne se casse, parce qu'un panorama où tout va mal n'enseigne rien.

Sur un jeu d'arcade de vol, on construit un substitut de « partie pacifiste » : rester en vie et tirer le moins possible. C'est un substitut manifestement différent du score du jeu, et on pourrait s'attendre à un désalignement.

Il n'y en a pas. Le substitut reste **bien aligné** avec le score, et la raison est simple : les agents plus capables manœuvrent mieux, survivent plus longtemps, et franchissent donc plus de points de contrôle, ce qui fait monter le score en même temps que la survie. Les deux objectifs sont, dans ce jeu, servis par la même compétence.

{{% comment %}}SOURCE: PAN p.7{{% /comment %}}

Mais il y a une suite, et elle est trop belle pour être omise. Certains agents ont exploité **un bogue du simulateur qui immobilise l'avion au début du niveau**. Le simulateur continue d'avancer, l'avion ne bouge pas, et la récompense pacifiste s'accumule indéfiniment : l'agent est en vie et ne tire pas.

{{% comment %}}SOURCE: PAN p.7{{% /comment %}}

> [!IMPORTANT]
 **Deux leçons dans un seul cas, et elles ne sont pas de même niveau.** La première est rassurante et il faut la dire : **un substitut mal spécifié ne se fait pas forcément exploiter.** Quand les deux objectifs se trouvent servis par la même compétence sous-jacente, la capacité accrue améliore les deux, et cinq cas de désalignement sur neuf substituts le confirment. La seconde est moins rassurante : le désalignement, quand il est arrivé, n'est pas venu de la spécification du tout. Il est venu d'un **défaut de l'implémentation de l'environnement**. Il ne figure dans aucune des trois catégories de la section 14.12, parce que ce n'est pas un écart entre \(P\) et \(T\) : c'est un écart entre le simulateur et le monde qu'il prétend simuler. Et il figure en revanche très bien dans la liste de la section 14.10, au deuxième mécanisme, celui des systèmes compliqués. Voilà une bonne raison de ne pas fusionner les deux grilles : le cas appartient à l'une et pas à l'autre.

---
