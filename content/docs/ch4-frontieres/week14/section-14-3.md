---
title: "14.3 Pourquoi comparer plutôt qu'annoter"
weight: 4
---

## Trois bénéfices, et le deuxième est celui qu'on oublie

Une objection légitime, avant d'aller plus loin : pourquoi comparer deux segments plutôt que demander directement à la personne de noter chaque action ? Trois réponses, et elles ne sont pas de même poids.

**Premier bénéfice : le nombre d'étiquettes.** Un entraînement sérieux compte des millions d'interactions. Noter chaque action, ou même une action sur cent, est hors de prix. La comparaison, elle, se contente de quelques centaines de jugements, parce que chaque jugement contraint cinquante pas d'un coup et parce que le modèle de récompense généralise entre les segments qu'il a vus et ceux qu'il n'a pas vus.

**Deuxième bénéfice, et c'est celui que je veux que vous reteniez : les exemples négatifs.** Une démonstration humaine, qui est l'autre grande façon d'injecter du savoir humain dans un agent, ne contient que des exemples positifs. Elle dit « fais ceci » et elle ne dit jamais « ne fais pas cela », parce qu'un démonstrateur compétent ne fait pas les erreurs qu'il faudrait montrer. La comparaison, elle, en contient par construction : chaque paire désigne un gagnant **et un perdant**, et le perdant est un exemple négatif gratuit. C'est une différence structurelle entre les deux sources de savoir, et non une question de commodité.

**Troisième bénéfice : reconnaître sans savoir faire.** Il existe des comportements qu'une personne identifie immédiatement comme bons sans être capable de les produire. Prenez un corps simulé à quatre pattes dont on veut qu'il marche. Jugez deux clips de ce corps en mouvement : vous saurez dire lequel ressemble le plus à une marche, en une seconde. Maintenant pilotez-le vous-même, articulation par articulation, pour en produire une démonstration : vous n'y arriverez pas. La comparaison ne demande que la compétence de reconnaissance, qui est beaucoup plus répandue que la compétence d'exécution.

{{% comment %}}SOURCE: LAPAN ch.19 p.576{{% /comment %}}

---

## La boucle telle qu'elle a été conçue : trois processus en parallèle

Mettons maintenant la chaîne complète en image. Dans sa forme d'origine, elle fait tourner **trois processus en parallèle**, et c'est ce parallélisme qui en fait une boucle plutôt qu'une succession d'étapes.

Le premier processus est l'**apprentissage par renforcement** : un acteur-critique joue, reçoit ses récompenses du modèle courant \(\hat r\), et dépose dans une base de données des segments prélevés au hasard dans ce qu'il vient de jouer.

Le deuxième est l'**étiquetage** : des personnes tirent des paires de segments dans la base, les comparent, et y écrivent leurs étiquettes.

Le troisième est l'**ajustement du modèle de récompense** : périodiquement, \(\hat r\) est réentraîné sur l'ensemble des paires étiquetées disponibles, et la nouvelle version est renvoyée au premier processus.

{{% comment %}}SOURCE: LAPAN ch.19 p.576{{% /comment %}}

Chacun des trois lit ce que les autres écrivent, et la base de données est le point de rendez-vous. La **Figure 14-1** montre cette structure : les deux processus d'apprentissage, la base qui les relie, la personne qui lit des paires et écrit un jugement, et les étiquettes portées sur les flèches, qui disent exactement ce qui circule entre chaque paire de nœuds.

{{< bookfig src="14-01.png" week="14" >}}

Regardez la flèche qui va de l'apprentissage par renforcement vers la base. Elle est la plus discrète de la figure et c'est la plus lourde de conséquences : **les segments que la personne jugera demain sont produits par la politique d'aujourd'hui**. Nous y reviendrons en section 14.8, où elle cessera d'être discrète.

---

## Et la version que nous allons suivre : trois étapes en série

La chaîne que ce cours va détailler ne fait pas tourner trois processus en parallèle. Elle les met **en série**, et c'est un choix de simplification tout à fait défendable pour une première construction. Les trois étapes sont alors :

1. **Entraîner** un acteur-critique sur la récompense réelle de l'environnement, en enregistrant au passage des segments dans une base.
2. **Étiqueter** cent paires de segments à la main, par une interface web.
3. **Ajuster** le modèle de récompense sur ces étiquettes, puis **affiner** la politique contre ce modèle, en enregistrant de nouveaux segments.

Et on recommence à l'étape 2 avec la nouvelle base. C'est une boucle, elle aussi, mais une boucle dont on tourne les tours à la main.

{{% comment %}}SOURCE: LAPAN ch.19 p.578{{% /comment %}}

---

## Cinq choses que cette simplification abandonne, et il faut les dire

Je ne vais pas présenter cette simplification comme équivalente à la version d'origine, parce qu'elle ne l'est pas. Voici ce qui est abandonné, et c'est un excellent exercice de lecture critique que de savoir faire cette liste devant n'importe quelle réimplémentation.

**Un seul environnement au lieu de plusieurs.** Les segments proviennent d'une seule exécution, ce qui réduit leur diversité.

**Cent étiquettes par tour, et trois cents en tout.** C'est très peu, et la section 14.8 montrera précisément ce que ce « très peu » ne contient pas.

**Les actions fournies explicitement au modèle.** Le modèle de cette chaîne reçoit l'action en entrée, sous forme de vecteur à un bit actif. La formulation d'origine ne précise pas comment l'action entre, ce qui est une liberté d'implémentation ; mais la noter permet de dire que les deux architectures ne sont pas comparables ligne à ligne.

**Aucune régularisation L2 et aucun ensemble de modèles.** Deux gardes classiques contre le surapprentissage d'un modèle ajusté sur quelques centaines d'exemples, et aucune des deux n'est présente.

**L'affinage plutôt que le réentraînement.** Au lieu de repartir de zéro à chaque tour, la chaîne **affine le meilleur modèle sauvegardé**. C'est économique, et cela a un effet que nous mesurerons : la politique du tour suivant est proche de celle du tour précédent, donc les segments qu'elle produit ressemblent à ceux que la personne a déjà jugés.

{{% comment %}}SOURCE: LAPAN ch.19 p.578{{% /comment %}}

> [!TIP]
 **Ce qui précède est un cadeau pédagogique, et je veux le dire explicitement.** La plupart des réimplémentations simplifient sans dire ce qu'elles simplifient, et le lecteur découvre l'écart en comparant les résultats. Ici la liste des écarts est connue, ce qui permet quelque chose de rare : quand nous arriverons à l'échec du tour 3, nous pourrons raisonner sur les causes candidates au lieu de spéculer. Trois cents étiquettes au lieu d'un million, un environnement au lieu de seize, pas d'ensemble de modèles, et une politique affinée plutôt que réapprise : ce sont quatre explications possibles du résultat final, et elles sont sur la table avant que le résultat arrive. Faites systématiquement cette liste quand vous reprenez le code de quelqu'un, et notez-la dans votre jalon 4.

---

## Ce que cette famille de méthodes a réellement rendu possible

Deux faits pour situer, et je les mets dans cet ordre parce que l'ordre inverse donnerait une fausse impression.

**Premier fait, et il est inconfortable : sur les bancs d'essai classiques d'apprentissage par renforcement, les résultats de cette approche n'ont jamais été spectaculaires.** Parfois une méthode classique faisait mieux, parfois moins bien. Si l'on en jugeait par ces seuls bancs d'essai, on classerait la rétroaction humaine parmi les curiosités.

{{% comment %}}SOURCE: LAPAN ch.19 p.577{{% /comment %}}

**Second fait : c'est pourtant la pièce qui a rendu les grands modèles de langue utilisables**, et le changement d'échelle est là tout entier. La fabrication d'un tel modèle passe par trois étapes, dans cet ordre.

D'abord un **préentraînement** sur un corpus énorme : pour l'un des jeux de données publics de référence, environ mille deux cents milliards de jetons, soit l'équivalent d'à peu près quinze millions de livres. Le modèle apprend là à prédire le mot suivant, et rien d'autre.

Ensuite un **affinage supervisé** sur un ensemble bien plus petit et bien plus coûteux à produire : de dix mille à cent mille dialogues rédigés avec soin, qui montrent la forme attendue d'une réponse.

Enfin un **affinage par rétroaction humaine** sur de l'ordre d'**un million de paires étiquetées**. Et c'est ici qu'il faut se rappeler le premier bénéfice de la section précédente, parce qu'il explique pourquoi cette dernière étape est possible : **comparer deux dialogues est beaucoup plus simple que d'en rédiger un**. Un million de comparaisons se produit ; un million de dialogues de référence, non.

{{% comment %}}SOURCE: LAPAN ch.19 p.577{{% /comment %}}

Ce cours ne construira pas cette chaîne-là, et je vous le dis franchement : l'étape de préentraînement est hors de portée, et ce n'est pas le sujet de ce cours. Ce que nous allons construire est la même chaîne sur un objet plus petit, où chaque pièce est visible et mesurée.

---
