---
title: "14.8 Trois tours, et une fin honnête"
weight: 9
---

## Tour 1 : cent étiquettes, et le sous-marin remonte

Premier tour. Cent paires étiquetées par la personne, selon le critère de la section 14.5. Modèle de récompense ajusté. Affinage de l'acteur-critique contre ce modèle.

L'entraînement est arrêté après **deux millions de pas et environ trois heures**, pour surapprentissage. Le meilleur modèle n'est pas le dernier : il a été sauvegardé vers le pas cinq cent mille.

Son score, mesuré sur la récompense réelle du jeu : **900 en 1 120 pas**.

Et son comportement, qui est la vraie mesure : le sous-marin **remonte chercher de l'oxygène**, et il passe une partie de son temps au milieu de l'écran plutôt que collé au fond.

{{% comment %}}SOURCE: LAPAN ch.19 p.594-595{{% /comment %}}

Arrêtons-nous un instant, parce que c'est un résultat remarquable et qu'il serait dommage de le traverser au pas de course. **Cent jugements humains, trois boutons, et le score a doublé.** Nous n'avons écrit aucun terme de récompense, choisi aucun coefficient, touché à aucune ligne de l'environnement. Nous avons montré deux cents petits films à une personne et appuyé cent fois sur une touche. Le comportement que douze millions de pas d'entraînement n'avaient pas fait apparaître est apparu. C'est exactement ce que la rétroaction humaine promet, et ici elle le livre.

---

## Tour 2 : cent étiquettes de plus, et rien de mieux

Deuxième tour. Cent étiquettes supplémentaires, pour un total de deux cents. Les paires sont tirées **pour moitié dans la base du modèle de départ et pour moitié dans celle produite par le modèle du tour 1**. Nouvel ajustement, nouvel affinage : un million et demi de pas, environ deux heures.

Score : **860 en 1 083 pas**.

Autrement dit : **pas mieux que le tour 1**, et même légèrement en dessous.

{{% comment %}}SOURCE: LAPAN ch.19 p.595-596, p.598{{% /comment %}}

Comment lire ce résultat ? Il existe une lecture encourageante et une lecture inquiétante, et je vais vous donner les deux parce qu'elles sont toutes les deux vraies.

**La lecture encourageante.** La base produite par le modèle du tour 1 contient nettement plus de segments où le sous-marin flotte à la surface que celle du modèle de départ. C'est un signe que la chaîne fonctionne : le comportement demandé est devenu fréquent, donc visible dans les données.

{{% comment %}}SOURCE: LAPAN ch.19 p.595{{% /comment %}}

**La lecture inquiétante, et c'est celle que ce cours retient.** Relisez la phrase précédente en vous demandant **ce que la personne verra au tour suivant**. Les paires du tour 2 ont été tirées pour moitié dans une base dominée par des sous-marins en surface. La personne a donc comparé, pour l'essentiel, des segments de surface entre eux. Son critère disait « la surface, c'est bon » : appliqué à deux segments de surface, il ne discrimine plus rien, et les étiquettes deviennent du bruit ou renforcent la surface par défaut.

**C'est une boucle de rétroaction, au sens strict.** La politique choisit ce que la personne verra ; ce que la personne voit détermine la récompense apprise ; la récompense apprise détermine la politique. Rien dans la chaîne ne garantit que cette boucle converge vers ce que nous voulions, et la section 14.10 va lui donner un nom et la ranger parmi six mécanismes connus.

---

## Tour 3 : le sous-marin ne fait plus que remonter

Troisième tour. Cent étiquettes de plus, trois cents en tout, et cette fois la personne essaie de viser les plongeurs : préférer, quand c'est possible, les segments qui en contiennent. Environ deux millions de pas, trois heures.

Voici ce qui se passe au test, et je vous demande de lire ces deux faits ensemble.

**Premier fait : l'épisode de test atteint la limite de cinq mille pas, avec un score faible.** Cinq mille pas, c'est quatre fois plus long que le tour 1. L'agent ne meurt plus.

**Second fait : l'explication la plus probable de ce comportement est que le sous-marin reste simplement à la surface.** Très sûr, et ce n'est pas du tout ce que nous voulions.

{{% comment %}}SOURCE: LAPAN ch.19 p.597-598{{% /comment %}}

Voilà. C'est la rencontre des deux moitiés de la semaine, et elle a eu lieu dans la chaîne elle-même, sans qu'on la provoque.

Reprenons le fil depuis le début, parce que chaque maillon est irréprochable. Nous ne savions pas écrire la récompense. Nous avons demandé à une personne de juger. Elle a jugé selon un critère explicite : la surface, c'est bon ; l'oxygène bas, c'est mauvais. Le modèle de récompense a appris ce critère **correctement**. L'agent a optimisé le modèle **correctement**. Et il a trouvé le point qui maximise ce modèle : **rester à la surface pour toujours**. À la surface, l'oxygène est au maximum, aucun ennemi ne monte si haut, et chaque pas de temps marque un point selon la récompense apprise. C'est l'optimum, et il est parfait.

> [!IMPORTANT]
 **L'agent n'a pas désobéi, il a obéi, et c'est pour cela que l'épisode est instructif.** Il n'y a pas de bogue dans cette histoire. Il n'y a pas de malentendu dans la boucle, pas d'erreur d'implémentation à corriger, pas de mauvaise graine. Il y a **une spécification incomplète, apprise fidèlement et optimisée efficacement**. Nous avons dit « remonte à la surface » en pensant « remonte à la surface quand il faut, puis redescends travailler ». La seconde moitié de cette phrase n'a jamais été dite à personne, ni en Python, ni en français dans le protocole d'étiquetage. L'agent a donc optimisé la première. Et notez la symétrie avec la section 14.1 : nous étions partis d'un agent collé au fond parce que la récompense du jeu ne mentionnait pas l'oxygène, et nous arrivons à un agent collé à la surface parce que la récompense apprise ne mentionne pas le travail. Le même phénomène, deux fois, avec deux spécifications différentes.

Et avant que le surapprentissage ne s'installe, ce tour avait produit quelque chose de bien meilleur : une politique qui **refaisait le plein d'oxygène deux fois** dans la même partie et qui a marqué **1 820 en 1 613 pas**.

{{% comment %}}SOURCE: LAPAN ch.19 p.597-598{{% /comment %}}

C'est un fait important et il complique la morale, ce qui est bon signe. Le tour 3 n'est pas un échec pur : il a produit la meilleure politique de toute la chaîne **et** la pire, selon le moment où on l'arrête. Ce qui veut dire que la différence entre « cette méthode marche » et « cette méthode se fait exploiter » tient, dans cette expérience, au critère d'arrêt.

---

## Le tableau de la chaîne, et la phrase qu'il ne faut pas lire seule

Voici les quatre mesures de référence, réunies. Les scores sont mesurés sur la **récompense réelle du jeu**, pas sur la récompense apprise.

| Modèle | Étiquettes cumulées | Récompense réelle | Pas de jeu |
| --- | --- | --- | --- |
| de départ | aucune | **460** | 580 |
| tour 1 | 100 | **900** | 1 120 |
| tour 2 | 200 | **860** | 1 083 |
| tour 3 | 300 | **1 820** | 1 613 |

{{% comment %}}SOURCE: LAPAN ch.19 p.598 (tableau 19.1, vérifié sur l'image de page){{% /comment %}}

Ce tableau autorise une phrase qui a tout pour plaire : **avec seulement trois cents étiquettes, le score a été multiplié par près de quatre.** Elle est vraie, elle est mesurée, et elle est un argument réel en faveur de la rétroaction humaine. Je la dis donc sans réserve.

Mais je ne vais pas la laisser seule, parce que lue seule elle donne une image fausse de l'expérience. Quatre choses l'accompagnent, et elles sont du même tableau et des mêmes pages.

**Le tour 2 n'a rien apporté**, et doubler le nombre d'étiquettes a fait baisser le score. La relation entre le nombre d'étiquettes et le résultat n'est donc pas monotone, et avec quatre points de mesure on ne peut pas savoir si le tour 2 est un accident ou le symptôme de la boucle de rétroaction.

**La meilleure ligne et le pire comportement viennent du même tour.** Le 1 820 et le sous-marin parqué à la surface sont deux moments du tour 3. Une seule des deux lignes figure au tableau.

**Chaque ligne est une exécution unique**, sans intervalle, sans graines multiples. Vous savez depuis le jalon 2 ce que cela autorise à conclure : un ordre de grandeur, pas un classement. Quatre cents points d'écart entre le tour 1 et le tour 2 sur une exécution chacun n'établit rien.

**Et la mesure elle-même est sous réserve**, pour une raison que je donne dans la sous-section suivante.

---

## Deux réserves sur la mesure, et je les garde

Deux réserves accompagnent ces chiffres, et je les garde parce que les retirer rendrait le tableau plus beau et moins vrai.

**Première réserve : un doute sur le protocole de test.** Les enregistrements vidéo des derniers modèles montrent un comportement différent de celui mesuré, et sur un nombre de pas bien plus faible. L'hypothèse la plus simple est un défaut dans le code de test, et elle n'a pas été écartée.

**Seconde réserve : trois cents étiquettes contiennent à peine quelques exemples de plongeurs.** Le tour 3 visait les plongeurs ; les données du tour 3 n'en contenaient presque pas. Il n'est donc pas possible de dire si la chaîne échoue à enseigner le sauvetage de plongeurs, ou si on ne lui a jamais réellement demandé.

{{% comment %}}SOURCE: LAPAN ch.19 p.596-597{{% /comment %}}

> [!TIP]
 **Pourquoi je garde ces deux réserves, et ce que j'en attends de vous au jalon 4.** Un rapport qui dit « score multiplié par quatre » est un rapport inutilisable, parce qu'il ne permet pas de savoir ce que le lecteur peut en déduire. Un rapport qui dit « score multiplié par quatre sur une exécution, avec un tour intermédiaire négatif, un doute sur le code de test, et un comportement final dégénéré » est utilisable : on sait quoi en faire et quoi vérifier. La différence entre les deux ne coûte que trois phrases, et c'est la compétence que les semaines 10, 13 et celle-ci ont en commun. Le jalon 4 la demande explicitement, et c'est le critère sur lequel je serai le plus strict.

---

## La charnière : ce que nous venons de voir a des noms

Nous changeons de moitié de semaine ici, et je veux marquer le passage.

Ce que nous venons d'observer n'est pas un incident propre à un jeu d'arcade. C'est un phénomène étudié, nommé, classé et mesuré, et les huit sections qui suivent vont faire trois choses dans cet ordre.

D'abord, lui **donner un nom et une place** : un accident, au sens étroit, et cinq catégories de problèmes selon l'endroit du processus où la chose casse. C'est la section 14.9.

Ensuite, nommer **six mécanismes** par lesquels un agent exploite une récompense mal spécifiée, et vous verrez que notre sous-marin en déclenche quatre. C'est la section 14.10, et la section 14.11 montrera que les parades connues ne ferment pas le problème.

Enfin, le **mesurer** : trois types d'écart entre un substitut et ce qu'on voulait, et la démonstration que l'écart grandit avec la puissance de l'optimiseur. Ce sont les sections 14.12 à 14.14, et la section 14.15 placera notre sous-marin sur les deux grilles à la fois.

> [!WARNING]
 **Un avertissement de lecture, et c'est le plus important de la semaine.** Vous allez rencontrer deux classifications. L'une compte **trois** éléments, l'autre en compte **six**. Elles ne sont pas deux versions de la même liste et elles ne se complètent pas en neuf. Elles répondent à deux questions différentes : la première demande **en quoi le substitut diffère de ce qu'on voulait**, la seconde demande **par quel moyen l'agent exploite cette différence**. Un même cas a donc **un** type d'écart et **plusieurs** mécanismes d'exploitation, et c'est précisément ce que la section 14.15 va dessiner. Si à la fin de la semaine vous avez en tête une liste de neuf items, vous aurez appris quelque chose de faux, et c'est l'erreur que je redoute le plus sur cette semaine.

---
