---
title: "13.7 Ce qui est démontré, ce que cela coûte, et une ligne de tableau à lire à voix haute"
weight: 8
---

## Six tâches, des images, et un seul jeu de réglages

Le dispositif de mesure, d'abord, parce qu'un résultat ne vaut que par le protocole qui le produit.

**Sous le nom de PlaNet**, l'agent des six sections précédentes a été mesuré sur six tâches de contrôle continu : un pendule inversé à relancer sur son chariot, un bras à amener sur une cible, un guépard à faire courir, un doigt à faire tourner un objet, une balle à attraper dans une tasse, et un bipède à faire marcher. **À partir d'images de 64 sur 64 en trois canaux, uniquement.** Pas d'angles, pas de vitesses, pas de positions : des pixels. Et le **même jeu d'hyperparamètres sur les six tâches**, à la seule exception de la répétition d'action.

{{% comment %}}SOURCE: PLANET p.6{{% /comment %}}

Les résultats, maintenant, et je les donne dans l'ordre où ils sont concluants.

**En moins de cent épisodes**, cet agent dépasse A3C, l'acteur-critique asynchrone de la semaine 8, entraîné depuis l'**état proprioceptif** pendant **cent mille épisodes**, et cela sur les six tâches. Lisez bien les deux avantages que l'on accorde à l'adversaire : mille fois plus de données, et un accès direct à l'état du système au lieu d'images.

**Après cinq cents épisodes**, il égale D4PG, l'acteur-critique distribué que la semaine 9 a rencontré, entraîné depuis les pixels pendant cent mille épisodes, sur toutes les tâches **sauf** celle du doigt.

**Et sur la course du guépard, il dépasse la performance finale de ce même adversaire de 26 %.**

Les gains en efficacité d'échantillon, tâche par tâche, valent à peu près 250, 40, 500 et plus, 300, 100 et 90. Autrement dit : entre quarante et cinq cents fois moins d'épisodes pour le même niveau de jeu.

{{% comment %}}SOURCE: PLANET p.6-7{{% /comment %}}

---

## La ligne plafond, et ce qu'elle démontre exactement

Voici le tableau des scores après mille épisodes, et surtout la ligne que je vous demande de lire à voix haute.

| Tâche | Agent avec modèle appris, 1 000 épisodes | Planification sur le **vrai simulateur**, 0 épisode |
| --- | --- | --- |
| pendule sur chariot, relance | 821 | 850 |
| bras, cible facile | 832 | 964 |
| guépard, course | **662** | **656** |
| doigt, rotation | 700 | 825 |
| tasse, attraper | 930 | 993 |
| marcheur, marche | 951 | 994 |

{{% comment %}}SOURCE: PLANET p.7{{% /comment %}}

La colonne de droite est une **ligne plafond** (*ceiling row*) : c'est le même planificateur, la même méthode d'entropie croisée avec les mêmes réglages, mais appliquée à la **vraie dynamique du simulateur** au lieu du modèle appris. Elle ne demande aucun épisode d'entraînement, puisqu'elle n'apprend rien. Elle mesure donc une chose et une seule : **ce que ce planificateur obtiendrait si le modèle était parfait**.

> [!IMPORTANT]
 **Et maintenant la troisième ligne du tableau, celle du guépard : 662 pour le modèle appris, 656 pour le vrai simulateur.** Le modèle appris fait **mieux** que la vérité. Ce n'est pas une coquille, et ce n'est pas un hasard de graine : c'est ce que le tableau publié contient. Prenez le temps de comprendre pourquoi c'est possible, parce que c'est l'une des observations les plus instructives de la semaine. La ligne plafond n'est un plafond que si le planificateur est parfait, et il ne l'est pas : la méthode d'entropie croisée sur douze pas est une recherche **approchée**, et elle peut très bien mieux réussir dans un modèle légèrement **lissé** que dans une dynamique exacte, chaotique et pleine de détails qu'elle n'a pas le budget d'exploiter. Un modèle appris est, en un sens précis, une version **simplifiée** du monde, et une recherche courte peut préférer cela. Retenez la généralisation : un modèle approché n'est pas seulement une dégradation du monde, c'est aussi, parfois, un problème d'optimisation plus facile.

Deux ablations de conception complètent le tableau, et chacune établit une chose distincte. D'abord, **la collecte en ligne aide partout, et elle est nécessaire** sur le pendule, le doigt et le marcheur : un modèle entraîné une fois pour toutes sur des épisodes aléatoires ne suffit pas, parce que les régions intéressantes du monde ne sont visitées que par un agent déjà compétent. Ensuite, **la recherche itérative bat le tirage brut** : prendre la meilleure de mille suites tirées au hasard, sans les dix itérations de rajustement, est moins bon sur toutes les tâches. Les dix itérations ne sont donc pas décoratives.

{{% comment %}}SOURCE: PLANET p.8{{% /comment %}}

Un dernier résultat, pour sa valeur de curiosité : **un seul agent, entraîné sur les six tâches à la fois sans qu'on lui dise laquelle il joue**, les résout toutes, plus lentement que les spécialistes. C'est l'argument de la transférabilité de la section 13.2, mesuré pour une fois plutôt que postulé.

{{% comment %}}SOURCE: PLANET p.13{{% /comment %}}

---

## Le prix, et pourquoi je le mets dans la page

Dix à vingt heures de calcul sur un processeur graphique de centre de données, **par tâche**. Et ce coût est présenté comme **favorable** par rapport aux deux adversaires du tableau, ce qui est exact : ils demandent plus de temps de calcul, et mille fois plus d'interactions.

Les deux nombres ne mesurent pas la même chose, et c'est tout le sujet. L'efficacité en échantillons et l'efficacité en calcul sont deux ressources distinctes, et cette méthode **échange massivement la seconde contre la première**. Elle a raison de le faire quand l'interaction est chère. Elle aurait tort si elle était gratuite.

> [!NOTE]
 **La raison pour laquelle le laboratoire de cette semaine ne reproduit rien de ce tableau.** Vingt heures de processeur graphique par tâche, sur six tâches, c'est cent vingt heures, soit bien au-delà de toute session gratuite. Le laboratoire fait donc le choix inverse : il isole **quatre mécanismes** et les mesure séparément, chacun en quelques minutes. Et pour le planificateur, il a la meilleure licence possible : la ligne plafond du tableau ci-dessus **est** un planificateur sur une dynamique exacte, sans aucun modèle appris. Le volet B du laboratoire reproduit la **forme** de cette ligne sur un système analytique jouet, ce qui isole la recherche de l'apprentissage, et ce qui est très exactement la semaine 3 qui revient.

---

## La phrase qui annonce la seconde moitié de la semaine

Je termine cette section sur une observation que je trouve remarquable, et qui va nous servir de charnière.

La méthode que nous venons de décrire a un défaut connu, admis, et nommé par ses propres concepteurs : **son planificateur ne voit rien au-delà de son horizon**. Douze pas, et le monde s'arrête. Une récompense située à quinze pas est invisible, et aucune quantité de calcul supplémentaire ne la rendra visible, parce que le problème n'est pas la qualité de la recherche mais la **longueur** de ce qu'elle regarde.

Et la suite proposée est d'une simplicité désarmante : pour améliorer la performance finale, **on pourrait apprendre une fonction de valeur qui approxime la somme des récompenses au-delà de l'horizon de planification**.

{{% comment %}}SOURCE: PLANET p.8{{% /comment %}}

C'est exactement ce que fait la seconde moitié de la première moitié de cette semaine. La section 13.8 part de là.

---
