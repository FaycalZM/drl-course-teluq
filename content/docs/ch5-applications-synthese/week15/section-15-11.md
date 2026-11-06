---
title: "15.11 Les limites honnêtes"
weight: 12
---

## Six limites, et aucune ne se corrige par un meilleur algorithme

Cette section est la dernière des sections de contenu du cours, et je veux qu'elle soit honnête plutôt que rassurante. Voici six limites, établies par les mesures de ce cours lui-même, et pas une seule ne se répare en changeant de méthode.

**Un : presque tous les chiffres que vous avez lus sont des exécutions uniques.** Le tableau de la semaine 10 comptait vingt cases, cinq méthodes, et pas un seul intervalle. Les résultats des quatre applications de cette semaine sont des exécutions uniques. Ce n'est pas un reproche : chaque case coûte entre huit et vingt heures de calcul, et dix graines par case représenteraient des mois de machine. Mais la conséquence est que **ces tableaux ne permettent pas de classer les méthodes**, et c'est exactement pourquoi vos jalons mesuraient sur des tâches assez petites pour que dix graines tiennent dans une soirée.

**Deux : un classement de méthodes ne se transfère pas.** La semaine 11 l'a établi sur l'exploration, en renversant son propre classement d'un environnement à l'autre. Cela vaut pour toutes les familles : le classement que vous établirez sur votre tâche est vrai sur votre tâche.

**Trois : l'instrument de mesure peut être défectueux.** La section 15.4 en a trouvé un cas à l'intérieur d'un jeu de référence maintenu, où la récompense dépend du temps d'horloge et donc de la machine. Vous ne découvrirez ce genre de chose qu'en mesurant l'environnement avant de mesurer l'agent.

**Quatre : un résultat publié peut ne pas être reproductible, et sans que personne soit en faute.** La section 15.7 en a montré deux formes : une publication incomplète, où les hyperparamètres manquent ; et deux rapports de bonne foi d'une même expérience qui ne concordent pas.

**Cinq : le nom d'une méthode n'est pas une preuve.** La section 15.8 en a montré trois cas, tous dans des documents sérieux.

**Six, et c'est celle de la semaine 14 : la récompense est une spécification.** Rien dans ce cours ne vous dit laquelle écrire, et la semaine 14 a montré que l'écart entre ce que vous demandez et ce que vous voulez **grandit** quand votre agent devient meilleur. Après quatorze semaines à améliorer des optimiseurs, c'est la limite la plus profonde du lot.

---

## Et quatre choses que ce cours n'a pas faites

Je dois aussi dire ce que le cours a laissé de côté, pour que vous ne preniez pas son programme pour le domaine.

**Il n'a pas construit les quatre applications de cette semaine.** Il les a décrites, et le laboratoire dit précisément laquelle s'exécute. Quatre applications ne sont pas un panorama industriel : ce sont quatre exemples travaillés, choisis pour être différents les uns des autres.

**Il n'a presque rien dit du coût humain d'un déploiement.** Les semaines 14 et 15 ont posé la question « qui écrit la récompense » et « qui étiquette » ; elles ne les ont pas résolues, et elles n'ont rien dit du travail de maintenance qui suit une mise en service.

**Il n'a pas mesuré l'empreinte de calcul comme une variable de conception.** Le tableau de coût de la section 15.6 est un inventaire, pas une analyse. Six jours de processeur graphique pour une reproduction est un chiffre qui mérite une place dans un rapport, et ce cours s'est contenté de le constater.

**Et il a été écrit à un moment particulier.** La section 15.9 est datée, au sens le plus littéral : le rapport entre ce qu'un modèle de langue fait sans entraînement et ce qu'un agent entraîné fait avec évolue vite, et la bonne réponse de cette année n'est pas garantie d'être celle de l'année prochaine. Ce que je vous ai donné et qui ne se démode pas, ce sont les **trois questions** de la section 15.1 et la discipline de mesure. Les méthodes, elles, vieilliront.

---

## Le protocole, une dernière fois, et il est celui du cours

Et je finis cette section par le protocole, parce que c'est ce que je vous demande d'appliquer dans vos livrables et parce qu'il est le seul remède aux six limites ci-dessus.

Il est le même depuis le **jalon 2** et il tient en trois points. **Plusieurs graines aléatoires** par configuration, et les graines sont listées. **Un intervalle de confiance** autour de chaque chiffre que vous comparez, et jamais une comparaison de deux exécutions uniques. Et un **protocole écrit avant l'exécution** : la tâche, le critère d'arrêt, le nombre de pas, et ce qui compte comme une réussite. Le jalon 3 a ajouté l'exigence que ce protocole soit dans le dépôt, et le jalon 4 a ajouté que les mêmes règles s'appliquent à la lecture des résultats des autres.

Il existe des outils pour la partie statistique de ce travail, et le plus employé dans le domaine s'appelle **`rliable`** : il implémente les estimateurs robustes et les intervalles par rééchantillonnage que l'on attend aujourd'hui d'une comparaison de méthodes d'apprentissage par renforcement. Je le **nomme**, et c'est tout ce que je fais : le protocole que ce cours exige est celui de ses propres consignes de jalon, il s'écrit en une trentaine de lignes de NumPy, et aucun outil n'est imposé. Ne cherchez pas dans ce cours une référence sur cet outil, vous n'y en trouverez pas.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

> [!IMPORTANT]
 **Et voici la raison de fond pour laquelle ce cours a installé ce protocole dès le jalon 2, raison que les sections 15.7 et 15.8 viennent de rendre démontrable.** Les deux résultats négatifs de cette semaine ne viennent pas d'une mauvaise méthode ni d'un mauvais code : ils viennent d'un **nombre qui n'a pas été enregistré**, et d'une **unité qui n'a pas été écrite**. Les deux défauts sont gratuits à corriger, et les deux rendent un travail par ailleurs sérieux inutilisable par quelqu'un d'autre. Le protocole n'est pas une contrainte académique ajoutée à la fin : c'est la seule partie de votre travail dont la valeur ne dépend pas de la méthode que vous avez choisie.

---
