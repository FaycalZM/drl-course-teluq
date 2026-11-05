---
title: "Introduction"
weight: 1
---

## Ça marche, puis ça ne marche plus, et c'est le « plus » qui est la leçon

Bonjour à toutes et à tous ! Deux semaines de préparatifs, et nous y voilà : aujourd'hui, un agent apprend. La semaine 1 nous a donné la boucle, observer, décider, agir, encaisser, avec une ligne « décider » qui tirait au sort. La semaine 2 nous a donné l'objet capable de remplir cette ligne. Cette semaine, nous les branchons l'un sur l'autre, et le bâton de CartPole va tenir debout.

La méthode s'appelle la **méthode d'entropie croisée** (*cross-entropy method*, CEM), et je vous la donne tout de suite, en une phrase : jouez seize épisodes avec la politique actuelle, gardez les meilleurs, apprenez au réseau à les imiter, recommencez. Rien de plus. Imaginez un apprenti qui filme seize de ses tentatives, qui en retient les cinq meilleures, qui les rejoue au ralenti en se disant « voilà ce qu'il faut faire », puis qui refilme seize tentatives. Au bout de quelques dizaines de cycles, les cinq meilleures d'aujourd'hui sont meilleures que les seize d'hier. C'est tout le mécanisme, et son implémentation en PyTorch tient en moins de cent lignes.

{{% comment %}}SOURCE: LAPAN ch.4 p.118, p.122{{% /comment %}}

Cette méthode est beaucoup moins célèbre que celles des semaines suivantes, et elle a pourtant deux qualités que je tiens à nommer. Elle est remarquablement robuste aux changements d'hyperparamètres, ce qui en fait une méthode de référence idéale, le premier essai que l'on lance sur un problème nouveau pour savoir à quoi s'attendre. Et elle est assez simple pour que vous puissiez la tenir entière dans votre tête, ce qui ne sera plus vrai à partir de la semaine 6.

{{% comment %}}SOURCE: LAPAN ch.4 p.118, p.122{{% /comment %}}

Maintenant la partie intéressante. Cette méthode converge bien dans les environnements simples : ceux qui ne demandent pas d'apprendre une politique complexe en plusieurs étapes, et dont les épisodes sont **courts avec des récompenses fréquentes**. Lisez cette clause deux fois, parce qu'elle contient déjà la seconde moitié de la semaine. Nous allons prendre le code qui résout CartPole, sans y changer une ligne, et le lancer sur un environnement qui viole exactement cette clause. Il ne va rien apprendre du tout. Et nous allons comprendre pourquoi, non pas par une intuition vague, mais par une dérivation en quatre lignes que vous pourrez refaire vous-même sur vos propres chiffres.

{{% comment %}}SOURCE: LAPAN ch.4 p.118{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur ce point d'organisation.** La semaine 3 ferme le module 1 et porte le **jalon 1**, qui vaut 25 % de la note. Le livrable n'est pas une réimplémentation de CEM : c'est l'**analyse de l'échec** sur FrozenLake. Vous lancerez l'agent inchangé, vous tracerez la distribution des retours, vous expliquerez l'effondrement à partir de cette distribution, puis vous appliquerez les correctifs et vous commenterez le plateau. Ce qui est évalué est un raisonnement, et un raisonnement ne se recopie pas.

Un dernier mot sur la place de cette semaine. CEM n'estime la valeur de rien : elle ne demande jamais « combien vaut cet état », elle se contente de comparer des épisodes entiers entre eux. C'est délibéré. Je veux que vous ressentiez, dans vos propres courbes, ce qui manque à une méthode qui ne sait juger qu'une fois l'épisode terminé. La semaine 4 ouvre sur les fonctions de valeur, et sa première question sera « à quoi servent les valeurs, au juste ? ». Vous aurez déjà la réponse dans les doigts.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Placer une méthode sur les trois axes de la taxonomie, avec ou sans modèle, fondée sur la politique ou sur la valeur, sur politique ou hors politique, et justifier chacune des trois positions.
- Énoncer la différence entre politique cible et politique de comportement, et dire pourquoi « sur politique » est le cas particulier où les deux coïncident.
- Justifier, critère par critère, que CEM appartient à la famille de Monte-Carlo.
- Écrire les cinq étapes de la méthode et exprimer le seuil des élites comme un percentile des retours du lot.
- Expliquer pourquoi la dernière couche du réseau n'applique **pas** de softmax, et relier cette décision à `nn.CrossEntropyLoss` et à l'argument de stabilité numérique de la semaine 2.
- Dire quelle observation entre dans le jeu d'entraînement, et décrire ce que produit l'autre choix.
- Entraîner CEM sur CartPole jusqu'à un retour moyen supérieur à 475, et dire combien de lots cela demande en ordre de grandeur.
- Déduire d'une distribution de retours à deux valeurs que le filtrage par percentile sélectionne le lot entier.
- Nommer les trois limites de la méthode et associer chaque correctif à la limite qu'il attaque.
- Appliquer les cinq correctifs sur FrozenLake, mesurer le gain, et commenter le plateau atteint.
- Dire ce que désigne \(H(x)\) dans la justification théorique, et d'où vient le mot « entropie croisée » dans le nom de la méthode.

---

## Prérequis et outils

Les semaines 1 et 2, et rien d'autre. De la semaine 1 : la boucle d'interaction, `reset()` et `step()`, les espaces d'observations et d'actions, les enveloppes, la frontière de récompense. De la semaine 2 : le module `nn.Module`, le conteneur séquentiel, ReLU, la fonction de perte d'entropie croisée, Adam, la boucle d'entraînement en huit lignes et la règle `item()`. Si l'une de ces briques est floue, relisez-la aujourd'hui plutôt que demain : cette semaine ne redéfinit rien, elle assemble.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets ; **le processeur central suffit**, le processeur graphique n'apporte rien ici |
| **Gymnasium** | `CartPole-v1`, `FrozenLake-v1`, et une enveloppe d'observation écrite par vous |
| **PyTorch** | le réseau de politique, la perte d'entropie croisée, Adam |
| **TensorBoard** | les trois courbes à surveiller : perte, retour moyen du lot, seuil des élites |
| **Page « Notation » du cours** | la table des symboles, décisive cette semaine pour la lettre \(H\) |
| **Page « Glossaire » du cours** | les équivalences français et anglais, très nourries cette semaine |

> [!TIP]
 **Un conseil de méthode.** Gardez un carnet ouvert à côté de cette page et tapez les fragments au fur et à mesure. Ils s'emboîtent : le réseau, puis l'échantillonnage d'une action, puis le générateur de lots, puis le filtre, puis la boucle. À la fin de la section 3.4, vous aurez un agent complet, et vous l'aurez écrit ligne à ligne plutôt que collé d'un bloc.
