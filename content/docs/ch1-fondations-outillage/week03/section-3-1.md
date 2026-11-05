---
title: "3.1 Les trois axes de la taxonomie"
weight: 2
---

## Trois questions à poser à n'importe quelle méthode

Avant de rencontrer une quinzaine de méthodes en douze semaines, je veux vous donner la grille qui les range. Elle tient en trois questions, et vous les poserez à chaque nouvel algorithme du cours. Construit-il un modèle de l'environnement ? Apprend-il une politique ou des valeurs ? A-t-il besoin de données fraîches ? Ces trois axes forment ce que nous appellerons la **taxonomie des méthodes d'apprentissage par renforcement** (*taxonomy of RL methods*), et le mérite de CEM est d'avoir sur les trois une position parfaitement nette.

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

---

## Premier axe : avec ou sans modèle

Une **méthode sans modèle** (*model-free*) ne construit aucune représentation de l'environnement ni de sa récompense. Elle relie directement les observations aux actions, ou à des quantités liées aux actions. Elle ne se demande jamais « que se passera-t-il si je pousse à gauche », elle se demande seulement « que dois-je faire ici ».

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

Une **méthode avec modèle** (*model-based*) fait exactement ce que la précédente refuse : elle prédit la prochaine observation, ou la prochaine récompense, ou les deux, et elle choisit son action à partir de cette prédiction. Le plus souvent, elle itère la prédiction sur plusieurs pas, ce qui revient à imaginer plusieurs futurs avant de bouger.

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

Le découpage n'est pas idéologique, il est pratique. Les méthodes purement avec modèle sont la norme dans les environnements déterministes, les jeux de plateau en particulier, où les règles du jeu *sont* le modèle et où personne n'a besoin de l'apprendre. Dès que l'environnement devient riche, construire un bon modèle devient très difficile, et les méthodes sans modèle sont alors plus faciles à entraîner. L'essentiel de ce cours est sans modèle ; les méthodes d'auto-jeu et les modèles du monde de la fin du cours mélangeront les deux familles, et vous verrez alors ce que le mélange coûte et rapporte.

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

---

## Deuxième axe : la politique ou la valeur

Une **méthode fondée sur la politique** (*policy-based*) approche directement la politique, c'est-à-dire ce que l'agent doit faire à chaque pas, en général sous la forme d'une distribution de probabilité sur les actions disponibles. Le réseau reçoit une observation et répond « 70 % à gauche, 30 % à droite ».

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

Une **méthode fondée sur la valeur** (*value-based*) procède autrement : elle calcule la valeur de chaque action possible et prend la meilleure. Je m'arrête ici volontairement, parce que le mot « valeur » mérite deux semaines entières et que je ne veux pas vous en donner une version abrégée. Retenez la forme de la phrase, pas son contenu : la semaine 4 la remplira.

{{% comment %}}SOURCE: LAPAN ch.4 p.119{{% /comment %}}

---

## Troisième axe : sur politique ou hors politique

Le troisième axe est celui que les textes utilisent le plus souvent sans jamais le définir. Prenons le temps de le poser correctement, parce qu'il gouverne tout le module 2.

Une méthode **hors politique** (*off-policy*) est capable d'apprendre à partir de données historiques : des trajectoires produites par une version antérieure de l'agent, enregistrées lors d'une démonstration humaine, ou simplement vues par le même agent plusieurs épisodes auparavant. Une méthode **sur politique** (*on-policy*) exige au contraire des données fraîches, engendrées par la politique que l'on est en train de mettre à jour ; l'entraîner sur des données anciennes donne un résultat faux. C'est évidemment beaucoup moins économe en données, et c'est acceptable quand l'environnement est léger et rapide, ce qui est exactement le cas de CartPole.

{{% comment %}}SOURCE: LAPAN ch.4 p.120{{% /comment %}}

La définition formelle est plus précise encore, et elle vaut la peine d'être mémorisée telle quelle. Une méthode sur politique évalue ou améliore **la politique qui sert à décider** ; une méthode hors politique évalue ou améliore une politique **différente de celle qui a engendré les données**. D'où deux politiques dans le second cas : celle dont on cherche à apprendre, la politique cible, et celle qui produit effectivement le comportement, la politique de comportement. On apprend alors à partir de données qui sont « à côté » de la politique visée, ce que le terme anglais rend littéralement.

{{% comment %}}SOURCE: SB ch.5 §5.4 p.122, §5.5 p.125{{% /comment %}}

> [!NOTE]
 **Notez bien cette façon de présenter l'axe, elle évite une confusion durable.** Les méthodes hors politique sont souvent de plus grande variance et plus lentes à converger, mais elles sont plus puissantes et plus générales, et **les méthodes sur politique en sont le cas particulier où la politique cible et la politique de comportement sont la même**. Ce n'est donc pas une opposition entre deux camps : c'est un cas général et son cas dégénéré. Une fois cela en tête, la position de CEM devient évidente.

{{% comment %}}SOURCE: SB ch.5 §5.5 p.125{{% /comment %}}

La liberté du hors politique n'est pas gratuite. Elle suppose une condition de couverture : toute action que la politique cible peut prendre doit aussi être prise de temps en temps par la politique de comportement. Autrement dit, si \(\pi(a \mid s) > 0\), alors il faut \(b(a \mid s) > 0\). Une politique de comportement qui n'essaie jamais une action ne pourra jamais rien nous apprendre sur elle. Retenez cette ligne : c'est elle qui transformera, en semaine 5, un tampon de données en objet délicat plutôt qu'en réserve gratuite. C'est aussi ce qui permet à un agent d'apprendre d'un contrôleur qui n'apprend pas, ou d'un expert humain, et nous y reviendrons à la fin du cours.

{{% comment %}}SOURCE: SB ch.5 §5.5 p.125{{% /comment %}}

---

## Où se range CEM, et ce que cela implique

| Axe | La question posée | CEM | La conséquence concrète |
| --- | --- | --- | --- |
| modèle | prédit-elle le futur ? | **sans modèle** | rien dans le code ne connaît les règles de CartPole |
| cible de l'apprentissage | politique ou valeurs ? | **fondée sur la politique** | la sortie du réseau **est** \(\pi(a \mid s)\) |
| fraîcheur des données | peut-elle réutiliser du vieux ? | **sur politique** | un lot est périmé dès qu'on a fait un pas d'optimisation |

{{% comment %}}SOURCE: LAPAN ch.4 p.119-120{{% /comment %}}

La troisième ligne est celle qui coûte, et nous allons la voir à l'œuvre dans le code de la section 3.4 : la collecte des épisodes et l'entraînement se déroulent dans le même fil d'exécution, et le réseau change à chaque lot. Le lot que vous venez d'utiliser ne resservira jamais. Gardez ce gâchis en tête, il a un nom et un prix que la semaine 6 chiffrera.

{{% comment %}}SOURCE: LAPAN ch.4 p.120, p.126{{% /comment %}}
