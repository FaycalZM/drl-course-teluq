---
title: "Module 3 : Méthodes à base de politique"
weight: 3
bookCollapseSection: true
---

# Module 3 : Méthodes à base de politique

Toutes les méthodes du module 2 se terminent par la même opération : une maximisation sur les actions. Cette opération suppose qu'on puisse les énumérer, et c'est précisément le mur sur lequel le module précédent s'arrête, car on n'énumère pas un couple moteur. Ce module change donc l'objet appris : la **politique** devient ce que l'on apprend, directement, sous la forme d'un réseau qui produit une distribution de probabilité sur les actions. La valeur ne disparaît pas pour autant ; elle change de rôle, et de but elle devient outil.

Ce changement achète deux choses, et il faut les séparer. Une politique stochastique d'abord : il existe des problèmes dont la politique optimale est stochastique, et aucune méthode qui choisit par \(\argmax\) ne peut l'écrire, quelle que soit la qualité de son estimation des valeurs. Les actions continues ensuite, parce que rien, dans le théorème du gradient de politique, n'exige que les actions soient énumérables : c'est ce qui ouvre la robotique simulée, où une action est un vecteur de couples articulaires. Et le changement se paie : une méthode de gradient de politique consomme de l'ordre de dix fois plus d'interactions avec l'environnement que les méthodes du module 2.

Reste un danger propre à cette famille, et le module se termine dessus. On ne se relève pas d'une mauvaise mise à jour de politique, parce que c'est la politique abîmée qui collecte le lot dont la mise à jour suivante se nourrira : le mauvais pas choisit ses propres données. Réduire le pas d'apprentissage achète alors de la sécurité en renonçant à converger, donc il faut **contraindre** le déplacement de la politique au lieu de le rétrécir. C'est de là que sort la méthode que vous emploierez le plus souvent par la suite, et ce n'est pas la plus savante des quatre : c'est celle qui remplace une machinerie entière par un écrêtage.

> [!IMPORTANT]
 **La bonne question n'est pas de combien les poids ont bougé, c'est de combien la politique a bougé.** Une politique est un objet fortement non linéaire : un petit déplacement de paramètres peut produire un grand déplacement de comportement, et l'erreur ne se corrige pas au pas suivant, puisque le pas suivant travaille sur des données que la politique abîmée a collectées.

---
## Deux lignées, qui se rejoignent dans la dernière semaine

{{< mermaid >}}
graph TD
  M2["Module 2 : un maximum sur les actions"] -->|"et si on ne peut pas les énumérer ?"| W8["Semaine 8 : de REINFORCE à A2C"]
  W8 -->|"l'action devient un vecteur"| W9["Semaine 9 : actions continues"]
  W8 -->|"PPO et TRPO"| W10["Semaine 10 : régions de confiance"]
  W9 -->|"SAC"| W10
  W10 --> J3["Jalon 3"]
  J3 --> M4["Module 4 : les hypothèses tombent"]
{{< /mermaid >}}

La semaine 10 réunit deux filiations distinctes, et le diagramme en garde la trace parce que la confusion est fréquente. Les méthodes à région de confiance (*trust region*) descendent directement de la semaine 8 : sur politique, un lot collecté puis consommé. La dernière méthode du module descend de la semaine 9 : hors politique, tampon de rejeu, critiques jumeaux. Elles répondent à la même question, de combien une politique a le droit de changer en un pas, mais elles n'appartiennent pas à la même famille, et le compromis qu'elles proposent n'est pas le même.

---
## Ce que vous saurez faire en entrant dans le module 4

- paramétrer une politique par un réseau et échantillonner l'action, puis démontrer en cinq lignes pourquoi un \(\argmax\) ne peut pas écrire une politique optimale stochastique ;
- écrire REINFORCE, puis A2C, en nommant les quatre problèmes du premier et la réparation qui répond à chacun ;
- expliquer pourquoi la quantité minimisée dans le code n'est pas une perte, et dire ce qu'il faut regarder à la place ;
- écrire une politique gaussienne pour un espace d'actions continu : tête de moyenne, tête de variance, log-densité, entropie en forme fermée ;
- écrire un acteur-critique déterministe avec son bruit d'exploration, et mesurer la surestimation de son critique au lieu de la supposer ;
- implanter l'objectif écrêté avec l'estimation généralisée de l'avantage, et dire exactement ce que l'écrêtage fait et ce qu'il ne fait pas ;
- choisir entre une méthode sur politique et une méthode hors politique en répondant d'abord à une question : chez vous, qu'est-ce qui est rare, le calcul ou les observations ?
- lire un tableau de banc d'essai sans se faire prendre : une case laissée vide est une décision de rapport, une colonne peut être attribuée à autre chose que son titre, et un chiffre sans sa version d'environnement n'est pas une mesure.

---
## Le travail évalué de ce module

Le **jalon 3** referme le module et vaut 25 % de la note finale : une méthode de politique qui apprend, une analyse de la variance de son gradient, et une comparaison honnête avec le réseau Q profond du jalon 2 sur l'efficacité d'échantillon, la stabilité et le temps d'horloge.

[Ouvrir le jalon 3 →]({{< relref "/docs/ch3-methodes-politique/jalon-3" >}})

{{% comment %}}
Page de module rédigée en phase 4, à partir des trois pages d'accueil de semaine
(week08 à week10) et de course.yaml. Elle remplace le squelette de phase 1, qui affichait
« Contenu en préparation » et dupliquait la liste des semaines que la barre latérale
produit déjà.

Les deux filiations du diagramme sont celles que la page d'accueil de la semaine 10
distingue explicitement : PPO et TRPO viennent de la semaine 8, SAC vient de la
semaine 9. Le renvoi au jalon pointe vers la page de jalon du module, qui relaie vers
l'énoncé unique dans week10/jalon-3.md.
{{% /comment %}}
