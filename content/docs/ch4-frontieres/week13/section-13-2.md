---
title: "13.2 Pourquoi on n'apprend pas une dynamique depuis des pixels, et pourquoi on en veut une quand même"
weight: 3
---

## Quatre difficultés, et elles ne sont pas de même nature

La semaine 12 vous a laissés avec un modèle appris, et elle a été franche sur le résultat : l'entraînement n'a pas convergé. Il est donc temps de dire pourquoi apprendre un modèle d'un monde riche est **difficile**, et de le dire précisément, parce que les quatre difficultés qui suivent ne se soignent pas de la même façon.

**Première difficulté : le modèle est inexact.** C'est la difficulté évidente, et c'est la moins intéressante. Un réseau entraîné sur un échantillon fini prédit à peu près, et à peu près n'est pas exactement.

**Deuxième difficulté : les erreurs des prédictions à plusieurs pas s'accumulent.** C'est la difficulté qui change de nature avec l'horizon. Une erreur de un pour cent sur un pas devient une divergence complète sur cinquante pas, parce que la sortie fautive du pas \(t\) est l'entrée du pas \(t+1\). La semaine 12 a rencontré cela sur cinq pas de déroulement ; ici nous allons en demander douze, puis quinze, puis quarante.

**Troisième difficulté : un modèle peut échouer à représenter plusieurs futurs possibles.** C'est la difficulté la plus structurelle, et c'est celle qui commande l'architecture de la section 13.3. Si le monde a deux suites possibles et que votre modèle n'en représente qu'une, il ne se trompe pas « un peu » : il affirme un futur unique là où il y en avait deux.

**Quatrième difficulté : un modèle est volontiers trop confiant hors de sa distribution d'entraînement.** Retenez bien celle-là. Elle va revenir, dans la seconde moitié de la semaine, sous un autre nom et avec des conséquences bien plus graves : ce sera le **décalage de distribution** de la section 13.14, et le mécanisme sera **identique**, à ceci près qu'il portera sur une valeur d'action au lieu d'une transition.

{{% comment %}}SOURCE: PLANET p.1{{% /comment %}}

> [!WARNING]
 **La troisième et la quatrième difficulté sont celles qui mordent, et pour une raison qui n'a rien d'évident.** Les deux premières se corrigent par de la capacité et des données : un plus gros modèle, un meilleur entraînement, et l'erreur baisse. Les deux dernières ne se corrigent pas comme cela, parce qu'elles sont **exploitées par l'optimiseur que vous allez brancher derrière**. Un planificateur qui cherche la meilleure suite d'actions dans votre modèle cherche, par construction, les endroits où votre modèle promet beaucoup. Si le modèle promet beaucoup là où il ne sait rien, le planificateur ira exactement là. Gardez cette phrase : elle est la clé de la section 13.3 et elle est le cœur de la section 13.14.

---

## Trois raisons de vouloir un modèle malgré tout

Alors pourquoi s'y risquer ? Il y a trois arguments, et ils sont de poids inégal.

**Premier argument, et c'est le principal : l'efficacité en échantillons** (*sample efficiency*). Un modèle du monde est entraîné sur un signal beaucoup plus riche qu'une valeur. Apprendre à prédire l'image suivante, c'est apprendre quelque chose de chaque pixel de chaque transition ; apprendre une valeur, c'est apprendre un seul nombre par transition. Et surtout, les récompenses n'ont plus besoin d'être **propagées par des remontées de Bellman** le long d'une trajectoire : le modèle les prédit directement là où elles se produisent, et le planificateur les somme. Rappelez-vous ce que la semaine 5 a payé pour propager une information de récompense sur cent pas : cent mises à jour, chacune attendant la précédente. Ici, douze pas de déroulement suffisent à voir une récompense qui est à douze pas.

**Deuxième argument : la performance s'achète avec du calcul.** Un planificateur qui dispose de plus de temps explore plus de suites d'actions et joue mieux, **sans un seul épisode supplémentaire**. C'est une propriété que n'a aucune des méthodes des semaines 5 à 11 : chez elles, mieux jouer demande de s'entraîner davantage, donc d'interagir davantage.

**Troisième argument : une dynamique apprise peut être indépendante de la tâche.** Les lois du monde ne changent pas quand l'objectif change. Un modèle de dynamique entraîné sur une tâche peut donc, en principe, servir à une autre, là où une valeur ou une politique sont liées à la récompense qui les a produites.

{{% comment %}}SOURCE: PLANET p.1{{% /comment %}}

---

## Ce qui avait été atteint avant, et pourquoi la barre était basse

Un mot sur l'état antérieur de la question, parce qu'il donne la mesure de ce que la section 13.7 va rapporter.

Les modèles latents antérieurs avaient atteint l'équilibre d'un pendule inversé sur chariot et le contrôle d'un bras à deux segments, avec des récompenses **denses**. C'est peu : ce sont des problèmes à deux ou trois degrés de liberté, où la récompense dit à chaque pas si l'on s'améliore. Et les travaux à faible dimension qui obtenaient de bons résultats supposaient l'accès **à l'état vrai du système et à la fonction de récompense**, ce qui est une hypothèse énorme : elle revient à poser que l'on connaît déjà la moitié du problème.

L'objet de la première moitié de cette semaine atteint, à partir **d'images uniquement**, le niveau d'un acteur-critique distribué qui a vu mille fois plus d'épisodes. C'est pour cela que la semaine lui consacre six sections.

{{% comment %}}SOURCE: PLANET p.1{{% /comment %}}

---
