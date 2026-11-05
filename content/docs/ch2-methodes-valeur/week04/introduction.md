---
title: "Introduction"
weight: 1
---

## Le cours acquiert enfin une fonction de valeur

Bonjour à toutes et à tous ! La semaine dernière, nous avons fabriqué un agent qui apprend vraiment, et nous l'avons regardé s'effondrer sur un lac glissant. Le diagnostic tenait en une phrase : la méthode ne savait juger qu'un épisode entier, après coup, et sur FrozenLake un épisode entier ne vaut que 0 ou 1. Rien, dans tout ce code, ne savait dire qu'une case est **meilleure** qu'une autre parce qu'elle est plus proche de l'objectif. Cette semaine, nous construisons exactement cette quantité manquante, et le module 2 s'ouvre avec elle.

Je veux vous donner tout de suite l'ordre de grandeur du gain, parce qu'il est spectaculaire et qu'il vaut mieux qu'un discours. Le même FrozenLake glissant qui demandait à la méthode de la semaine 3, après correction, de l'ordre de cinquante minutes de calcul pour atteindre 55 % de réussites, va être résolu cette semaine en **moins d'une seconde**. Pas par un réseau plus gros, pas par un meilleur optimiseur : par une table de seize nombres et une équation vieille de soixante-dix ans.

{{% comment %}}SOURCE: LAPAN ch.5 p.159{{% /comment %}}

Cette semaine est le pont avec SCI1060. Si vous avez déjà rencontré l'équation de Bellman, vous allez la retrouver, mais écrite dans la notation que ce cours tiendra jusqu'en semaine 15, et surtout **dérivée** plutôt que récitée. Si vous ne l'avez jamais vue, tout est ici, ligne à ligne. Dans les deux cas, prenez cette semaine au sérieux : presque tous les algorithmes d'apprentissage par renforcement reposent sur l'estimation de fonctions de valeur, et les onze semaines suivantes ne feront que raffiner ce que nous posons aujourd'hui.

{{% comment %}}SOURCE: SB ch.3 p.80{{% /comment %}}

Avant la première équation, un point de notation. Il n'est pas administratif : si vous le laissez flou, la semaine 5 deviendra littéralement illisible. Trois objets différents vont porter le même mot, « valeur », et il faut trois notations distinctes.

> [!IMPORTANT]
 **Je dois insister : trois niveaux, trois notations, et ils ne sont pas interchangeables.** Lisez ce tableau maintenant et revenez-y chaque fois qu'une majuscule vous surprendra. Toute la semaine 4 calcule la troisième ligne. Toute la semaine 5 consistera à remplacer la troisième ligne par la quatrième, et c'est la seule raison pour laquelle la semaine 5 existe.

| Notation | Ce qu'elle désigne | Qui la produit |
| --- | --- | --- |
| \(v_\pi(s)\), \(q_\pi(s,a)\) | la valeur **vraie** sous la politique \(\pi\) | personne : c'est la cible que l'on vise |
| \(v_*(s)\), \(q_*(s,a)\) | la valeur **vraie** sous une politique optimale | personne non plus : c'est l'idéal |
| \(V(s)\), \(Q(s,a)\) | une **estimation tabulaire**, un tableau rangé en mémoire | **cette semaine** |
| \(\hat v(s,\mathbf{w})\), \(\hat q(s,a,\mathbf{w})\) | une **approximation** paramétrée par un vecteur de poids \(\mathbf{w}\) | la semaine 5 |

Un mot enfin sur le programme de la semaine, parce que son plan n'est pas l'ordre habituel des manuels. Nous allons d'abord dire ce qu'est une valeur et pourquoi elle n'existe pas sans politique (4.1). Puis nous dériverons l'équation de Bellman (4.2), puis l'optimalité (4.3). Ensuite, et c'est le cœur pédagogique de la semaine, nous **construirons** l'itération sur la valeur : évaluation, amélioration, alternance des deux, et enfin l'alternance dont l'évaluation est tronquée à un seul balayage (4.4). Vous ne recevrez donc pas l'algorithme comme une recette : vous le verrez apparaître. Nous le mettrons ensuite au travail sur FrozenLake (4.5), nous enlèverons le modèle de l'environnement (4.6), et nous finirons par le contrôle sans modèle, Sarsa et Q-learning (4.7).

> [!NOTE]
 **Notez bien ce point d'organisation.** La semaine 4 ne porte **aucun jalon** : le prochain est en semaine 7. Le laboratoire est donc formatif, et il est court, parce que tout y tient sur un processeur central en quelques secondes. Profitez de cette semaine sans échéance pour solidifier les équations : à partir de la semaine 5, chaque méthode sera une variation sur celles-ci, et une variation sur une base floue ne tient pas.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Distinguer \(v_\pi\), \(V\) et \(\hat v(s,\mathbf{w})\), et dire laquelle des trois quantités cette semaine calcule.
- Définir \(v_\pi(s)\) et \(q_\pi(s,a)\), et justifier sur un exemple à quatre politiques pourquoi l'indice \(\pi\) n'est pas décoratif.
- Dériver l'équation de Bellman pour \(v_\pi\) en quatre lignes, à partir de la seule récurrence du retour.
- Lire un diagramme de sauvegarde et dire ce que chacun de ses deux types de nœuds représente.
- Écrire les deux équations d'optimalité de Bellman et dire exactement où se place le \(\max\) dans chacune.
- Expliquer pourquoi une politique gloutonne par rapport à \(v_*\) est optimale, alors que la gourmandise à un pas de la section 4.1 était un piège.
- Dire en une phrase ce que \(q_*\) permet de faire que \(v_*\) ne permet pas, et faire apparaître dans cette phrase le mot « dynamique ».
- Énoncer les trois hypothèses de la programmation dynamique, et dire laquelle tombe la première sur un problème de taille réelle.
- Dériver l'itération sur la valeur comme une itération sur la politique dont l'évaluation est tronquée à un seul balayage, et pointer le seul symbole qui sépare les deux mises à jour.
- Distinguer une mise à jour en espérance d'une mise à jour par échantillon, et nommer la famille de méthodes qui emploie chacune des deux.
- Écrire la mise à jour TD(0) et l'erreur TD, et dire à quel instant \(\delta_t\) devient disponible.
- Écrire les mises à jour de Sarsa et de Q-learning, et nommer la seule différence entre les deux.
- Définir la méthode \(\varepsilon\)-gloutonne et dire ce qu'elle coûte lorsque l'apprentissage a déjà convergé.
- Expliquer, sur la falaise, pourquoi la méthode qui a appris la meilleure politique obtient le pire score en ligne.
- Reconnaître, dans un agent qu'on vous présente, s'il lit la dynamique de son environnement, et désigner la ligne où il le fait.
- Implémenter l'itération sur la valeur avec trois tables sur FrozenLake, et dépasser un retour moyen de test de 0,80.

---

## Prérequis et outils

De la semaine 1 : le processus de décision markovien, la dynamique à quatre arguments \(p(s',r \mid s,a)\), la récurrence du retour \(G_t = R_{t+1} + \gamma G_{t+1}\), et l'interface `reset()` / `step()`. De la semaine 3 : FrozenLake et son glissement, les méthodes de Monte-Carlo, et les axes sur politique / hors politique et avec modèle / sans modèle. Cette semaine ne redémontre ni la dynamique ni le retour : elle les cite et construit par-dessus.

Un avertissement agréable sur l'outillage : **cette semaine ne demande pratiquement pas PyTorch**. Tout tient dans des tableaux de nombres, et le vocabulaire de NumPy suffit. C'est une pause, et c'est aussi un repère : la semaine 5 réintroduira les réseaux, et vous verrez alors très précisément ce que le réseau remplace.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets ; **le processeur central suffit largement**, le processeur graphique n'apporte rigoureusement rien ici |
| **Gymnasium** | `FrozenLake-v1`, et un petit environnement de falaise que vous écrirez vous-même |
| **NumPy** | les tables de valeurs, les balayages, les \(\argmax\) |
| **Matplotlib** | les deux courbes de la falaise, et c'est tout le tracé de la semaine |
| **PyTorch** | facultatif cette semaine ; il revient en force la semaine prochaine |
| **Page « Notation » du cours** | la table des symboles, décisive cette semaine pour \(v_\pi\), \(V\), \(\hat v\) et pour \(\vartheta\) |
| **Page « Glossaire » du cours** | les équivalences français et anglais, très nourries cette semaine |

> [!TIP]
 **Un conseil de méthode, et il vaut pour toute la semaine.** Gardez une feuille de papier à côté de cette page, et pour chaque équation que vous croisez, écrivez à la main **à quoi la flèche ou l'égalité vous engage**. La vingtaine d'équations de cette semaine sont presque toutes la même, à une différence près : un \(\max\), un indice, une flèche d'affectation au lieu d'un signe égal. La compréhension, ici, ne consiste pas à retenir quinze formules mais à savoir, devant chacune, nommer la seule chose qui a changé.
