---
title: "Module 4 : Frontières (exploration, auto-jeu, modèles du monde, alignement)"
weight: 4
bookCollapseSection: true
---

# Module 4 : Frontières (exploration, auto-jeu, modèles du monde, alignement)

Le module 3 a passé trois semaines à rendre l'optimisation d'une politique stable, et il l'a fait sur des problèmes confortables. L'exploration y était traitée comme un détail d'implémentation : un \(\varepsilon\) qui décroît, du bruit ajouté à l'action, une prime d'entropie posée à côté d'une perte. Ces mécanismes ont tous le même effet, pousser l'agent à essayer des actions au hasard autour de ce qu'il fait déjà, et cela suffit tant que la récompense est dense. C'est pourquoi aucune des dix premières semaines n'a eu à poser la question.

Ce module retire, une par une, quatre hypothèses dont tout le cours a vécu sans jamais les discuter : que la récompense arrive assez souvent pour qu'un hasard local la rencontre, que l'environnement reste immobile pendant que vous apprenez, que vous pouvez interagir avec lui autant que vous voulez, et que quelqu'un a su écrire la récompense. Chaque retrait met une famille de méthodes hors service et en fait apparaître une autre : une exploration qui rend la nouveauté désirable au lieu de perturber une action, une recherche dans un modèle avant d'agir, un apprentissage à l'intérieur d'un modèle appris puis sans aucune collecte, et une récompense ajustée sur des jugements humains plutôt qu'écrite à la main.

C'est aussi le module où la lecture d'un résultat change de nature, et c'est peut-être ce qu'il vous laissera de plus durable. Un entraînement peut être parfaitement sain et ne rien apprendre : perte qui descend, gradients propres, courbe de récompense plate comme une règle. Une perte peut cesser d'être informative sans être suspecte pour autant, dès que l'adversaire est une copie de vous-même. Et un classement de méthodes ne se transfère pas d'un environnement à un autre : vous verrez la même méthode arriver bonne dernière sur une tâche et première sur la suivante, les deux mesures étant justes. Trois de ces quatre semaines rapportent un résultat négatif mesuré, et la quatrième se termine sur un agent qui a optimisé parfaitement ce qu'on lui avait demandé, ce qui est exactement le problème.

> [!WARNING]
 **Un entraînement sain qui n'apprend rien ne lève aucune alerte.** Sous une récompense parcimonieuse, le choix de la méthode d'apprentissage cesse d'avoir le moindre effet : rien ne s'apprend d'un jeu de données où la chose à apprendre ne se produit jamais. La question à poser avant toutes les autres est donc celle-ci : votre agent rencontre-t-il jamais la récompense qui compte ?

---
## Quatre hypothèses, retirées une par une

{{< mermaid >}}
graph TD
  M3["Module 3 : une boîte à outils complète"] -->|"la récompense est dense"| W11["Semaine 11 : exploration avancée"]
  W11 -->|"l'environnement est immobile"| W12["Semaine 12 : auto-jeu et multi-agent"]
  W12 -->|"on peut interagir à volonté"| W13["Semaine 13 : modèles du monde, hors ligne"]
  W13 -->|"la récompense est donnée"| W14["Semaine 14 : RLHF et alignement"]
  W14 --> J4["Jalon 4"]
  J4 --> M5["Module 5 : choisir"]
{{< /mermaid >}}

Chaque flèche porte l'hypothèse que la semaine située à sa pointe retire. Les quatre retraits ne sont pourtant pas interchangeables, car chaque semaine garde un acquis de la précédente : le modèle appris de la semaine 12 devient le monde imaginé de la semaine 13, et le mécanisme central de la semaine 13, un optimiseur branché sur un estimateur que rien ne contredit finit par trouver les erreurs de cet estimateur, est déjà l'essentiel du problème de la semaine 14, où l'estimateur en question est un modèle de la préférence humaine.

---
## Ce que vous saurez faire en entrant dans le module 5

- reconnaître un entraînement sain qui n'apprend rien, et distinguer un échec d'exploration d'un échec de méthode ;
- ajouter une prime d'exploration, par comptage de visites ou par erreur de prédiction, et dire pourquoi elle redéfinit le processus de décision que l'agent résout ;
- écrire une recherche arborescente de Monte-Carlo : trois statistiques par arête, quatre phases, et le signe de la valeur qui s'inverse à chaque niveau de la remontée ;
- conduire un entraînement par auto-jeu, et établir le progrès par un tournoi entre points de contrôle là où aucune courbe ne le montre ;
- distinguer « hors politique » de « hors ligne », et expliquer pourquoi, sans collecte, l'erreur d'un estimateur grandit au lieu de se diluer, quelle que soit la quantité de données ;
- ajuster un modèle de récompense sur des jugements par paires, puis optimiser une politique contre lui en gardant la récompense de la tâche comme simple métrique ;
- reconnaître une transition de phase dans le piratage de la récompense (*reward hacking*), et expliquer pourquoi une forte corrélation entre un substitut et l'intention ne protège de rien ;
- délimiter un résultat négatif : ce qu'il établit, ce qu'il n'établit pas, et pourquoi une reproduction qui échoue ne dit rien de la méthode.

---
## Le travail évalué de ce module

Le **jalon 4** referme le module et vaut 25 % de la note finale : une extension avancée de votre agent, choisie parmi cinq routes tirées de ces quatre semaines, justifiée avant d'être codée, mesurée honnêtement et reproductible par quelqu'un d'autre que vous. C'est le dernier jalon du cours, et le seul où le choix de la méthode fait partie du travail noté.

[Ouvrir le jalon 4 →]({{< relref "/docs/ch4-frontieres/jalon-4" >}})

{{% comment %}}
Page de module rédigée en phase 4, à partir des quatre pages d'accueil de semaine
(week11 à week14) et de course.yaml. Elle remplace le squelette de phase 1, qui affichait
« Contenu en préparation » et dupliquait la liste des semaines que la barre latérale
produit déjà.

Les étiquettes du diagramme sont les quatre hypothèses retirées, chacune vérifiée sur la
page d'accueil de la semaine concernée. Les trois résultats négatifs mesurés sont ceux
des semaines 11, 12 et 13 ; la semaine 14 se termine sur un sous-marin parqué en surface,
qui n'est pas un échec d'optimisation. Le renvoi au jalon pointe vers la page de jalon du
module, qui relaie vers l'énoncé unique dans week14/jalon-4.md.
{{% /comment %}}
