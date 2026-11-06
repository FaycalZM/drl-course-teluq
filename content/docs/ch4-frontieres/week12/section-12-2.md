---
title: "12.2 Le jeu de plateau : des règles simples et un adversaire inconnu"
weight: 3
---

## Ce qu'un jeu de plateau inverse par rapport à un jeu vidéo

Depuis la semaine 5, nos environnements de référence sont des jeux vidéo : une image en entrée, quelques actions, et des règles internes dont nous ne savons rien. Un jeu de plateau inverse exactement cette situation, et c'est pourquoi il est le bon terrain pour une première méthode avec modèle.

Les règles d'un jeu de plateau sont **simples et compactes** : quelques lignes suffisent à dire ce qui est permis, quand la partie s'arrête, et qui a gagné. La position est entièrement **observable** : rien n'est caché, il n'y a pas d'état interne que vous ne verriez pas. Ce qui rend ces jeux difficiles est ailleurs, et c'est double : le **nombre de positions** possibles, et surtout un **adversaire dont la stratégie est inconnue et qui essaie de vous battre**.

{{% comment %}}SOURCE: LAPAN ch.20 p.602{{% /comment %}}

Cette double propriété, observabilité et règles explicites, rend possible une chose qu'aucun de nos environnements précédents n'autorisait : l'**analyse d'une position**. Analyser une position, c'est énumérer les coups légaux, évaluer la position qui résulte de chacun, et retenir le meilleur. Essayez de faire cela sur une image de jeu vidéo : vous ne pouvez pas, parce que vous n'avez aucun moyen de savoir à quoi ressemblera l'image suivante si vous appuyez à gauche. L'analyse d'une position **exige un modèle du jeu**, et c'est la raison pour laquelle cette semaine commence par les jeux de plateau.

{{% comment %}}SOURCE: LAPAN ch.20 p.602{{% /comment %}}

---

## Minimax, facteur de branchement, élagage

Trois mots de vocabulaire suffisent pour la suite, et je les donne dans l'ordre où ils se posent.

**Minimax** décrit la façon de descendre un arbre de jeu à deux joueurs : nous maximisons, l'adversaire minimise, et l'on alterne à chaque niveau en parcourant les états successifs du jeu. Je ne vais pas en écrire la formule, et ce n'est pas par paresse : l'écrire ouvrirait une demi-heure sur l'élagage alpha-bêta, qui est un beau sujet et qui n'est pas celui de cette semaine. Retenez le principe d'alternance, parce qu'il va ressurgir sous une forme très concrète dans la section 12.3, sous la figure d'un signe qui s'inverse.

{{% comment %}}SOURCE: LAPAN ch.20 p.603{{% /comment %}}

Le **facteur de branchement** (*branching factor*) est le nombre d'actions disponibles dans un état. Il n'est pas constant : au morpion, il part de neuf et descend jusqu'à zéro à mesure que la grille se remplit. Aux échecs, le joueur blanc ouvre avec vingt coups possibles. Au go, le premier joueur a trois cent soixante et une intersections à sa disposition sur un plateau de dix-neuf sur dix-neuf. Le facteur de branchement est la grandeur qui décide de la taille de l'arbre, et donc de ce qui est calculable.

{{% comment %}}SOURCE: LAPAN ch.20 p.605{{% /comment %}}

L'**élagage de l'arbre** (*tree pruning*) est la réponse classique à un arbre trop grand : on analyse jusqu'à une profondeur bornée, on s'arrête selon un critère, et l'on évalue la position atteinte avec une fonction d'évaluation **écrite à la main** par un expert du jeu. C'est la famille de méthodes qui a dominé les programmes d'échecs pendant des décennies. La recherche arborescente de Monte-Carlo est l'autre réponse, et elle est d'une nature différente : au lieu de tout analyser jusqu'à une profondeur fixe, elle **échantillonne** les chemins les plus prometteurs.

{{% comment %}}SOURCE: LAPAN ch.20 p.603, p.605{{% /comment %}}

---

## Les trois nombres qui ferment la porte de la force brute

Pourquoi ne pas simplement tout énumérer ? Parce que les nombres sont catégoriques, et ils valent la peine d'être retenus, parce qu'ils donnent une intuition de l'échelle.

| Jeu | Taille de l'arbre ou de l'espace d'états | Ce que cela autorise |
| --- | --- | --- |
| Morpion | **138** états terminaux distincts ; au plus \(9! = 362\,880\) nœuds dans l'arbre, et en pratique moins | **entièrement résoluble** : on peut tout énumérer et jouer parfaitement |
| Puissance 4 | environ \(4{,}5 \cdot 10^{12}\) états distincts | hors de portée d'une énumération, à la portée d'une recherche |
| Dames | environ \(5 \cdot 10^{20}\) nœuds dans l'arbre complet | hors de portée, et de très loin |
| Échecs, go | nettement plus grand encore | hors de portée, et c'est l'origine du sujet |

{{% comment %}}SOURCE: LAPAN ch.20 p.603, p.605, p.608{{% /comment %}}

> [!IMPORTANT]
 **Le morpion est la seule ligne de ce tableau où la question de l'apprentissage ne se pose pas.** Cent trente-huit états terminaux, c'est une table que vous pouvez écrire dans un fichier et consulter. Dès la ligne suivante, la table ferait quatre mille milliards d'entrées, et il n'y a plus que deux stratégies possibles : élaguer avec une fonction d'évaluation que quelqu'un a écrite à la main, ou **chercher intelligemment** dans un arbre que l'on ne construira jamais en entier. Toute la section 12.3 est la seconde stratégie, et elle n'a besoin de personne pour écrire la fonction d'évaluation : c'est un réseau qui l'apprend.

---
