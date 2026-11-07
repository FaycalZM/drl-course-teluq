---
title: "6.1 La même boucle, cinq fois"
weight: 2
---

## Cinq semaines à réécrire la même boucle

Comptons ce que nous avons écrit la semaine dernière. Environ deux cents lignes de code d'entraînement, et une cinquantaine de lignes d'enveloppes d'environnement. Pour un seul agent, sur un seul jeu. Et si vous relisez les semaines 3, 4 et 5 à la suite, vous verrez revenir, trois fois, la même séquence : une boucle sur les pas, une mémoire de transitions, un calcul de perte, un pas d'optimiseur, un suivi de la récompense moyenne.

{{% comment %}}SOURCE: LAPAN ch.7 p.203{{% /comment %}}

Tout réécrire soi-même est une excellente chose **pendant qu'on apprend**, et c'est précisément ce que ce cours vous a fait faire pendant cinq semaines. Passé ce stade, le bénéfice s'inverse : on réécrit le même code encore et encore, et la répétition est l'endroit où vivent les bogues.

Il vaut la peine de comprendre d'où vient cette répétition, parce qu'elle n'est pas un accident de style. Elle vient de la **généralité** des méthodes d'apprentissage par renforcement. Le code écrit pour CartPole s'applique à Atari au prix de retouches mineures, puisque la méthode ne connaît de l'environnement que son interface. Cette généralité est une qualité du domaine, et sa conséquence pratique est qu'un code réutilisé a toutes les chances d'être meilleur que le vôtre réécrit pour la troisième fois : plus rapide, mieux testé, plus lisible, mieux documenté.

{{% comment %}}SOURCE: LAPAN ch.7 p.203{{% /comment %}}

Entre deux extrêmes, il faut choisir. D'un côté la bibliothèque clé en main, qui résout votre problème en dix lignes tant que votre problème est celui qu'elle prévoit, et contre laquelle vous vous battez dès que vous voulez autre chose ; Stable-Baselines3, que vous avez déjà croisée en semaine 3 et en semaine 5, est de cette famille. De l'autre côté, tout écrire de zéro à chaque projet, ce qui est long, fastidieux et source d'erreurs. Entre les deux vivent les bibliothèques de **briques** : elles ne vous donnent pas un algorithme, elles vous donnent les objets avec lesquels un algorithme s'écrit.

{{% comment %}}SOURCE: LAPAN ch.7 p.204{{% /comment %}}

PTAN, que nous allons lire, est de cette famille intermédiaire. Elle s'installe en deux lignes, `pip install stable_baselines3` puis `pip install ptan==0.8 --no-deps`, et la version est épinglée parce que ses interfaces ont bougé d'une version à l'autre. Les deux précautions ne sont pas décoratives. PTAN 0.8 fige `torch==2.3.1`, qui n'a plus de roue pour les versions récentes de Python, de sorte qu'une installation ordinaire s'arrête avant d'avoir rien installé ; et son premier import charge `stable_baselines3`, qu'elle ne déclare pas dans ses dépendances.

{{% comment %}}SOURCE: LAPAN ch.7 p.203{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur ce que cette première moitié de semaine attend de vous, parce que ce n'est pas ce que vous croyez.** Vous n'avez pas à retenir les noms de classes de PTAN. Vous n'aurez plus à les écrire après vendredi : les laboratoires des semaines 7 à 15 sont en PyTorch et Gymnasium simples, et c'est un choix de ce cours. Le but d'un cours comme celui-ci n'est pas de vous apprendre à vous servir des bibliothèques existantes : c'est de vous donner l'intuition des méthodes et la capacité de les réimplémenter de zéro le jour où il le faut. Les bibliothèques passent ; le découpage qu'elles proposent, lui, reste. Ce que je vous demande de retenir de la section 6.2 est donc une **liste de cinq objets** et, pour chacun, une phrase disant ce qu'il cache. Un étudiant qui ne réouvrira jamais PTAN doit pouvoir réciter cette liste dans six mois.

{{% comment %}}SOURCE: LAPAN ch.8 p.227{{% /comment %}}

Et il y a une raison supplémentaire de la lire, qui est propre à cette semaine. Les cinq réparations que nous allons étudier sont des **substitutions** : on remplace un tampon par un autre, une couche par une autre, une tête de sortie par deux. Une substitution n'est bon marché que si la pièce qu'on remplace était une pièce. Tant que tout est écrit à plat dans une seule fonction d'entraînement, chaque variante est une réécriture, et le laboratoire de cette semaine serait quatre programmes distincts plutôt qu'une expérience.

---
