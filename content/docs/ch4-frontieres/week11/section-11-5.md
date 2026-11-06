---
title: "11.5 MountainCar, et l'échec complet de la méthode ε-gloutonne"
weight: 6
---

## Une voiture au fond d'une vallée, et des dizaines d'actions à coordonner

Nous passons de la rivière à une tâche réelle, mesurable, et que vous allez faire tourner vous-mêmes dans le laboratoire. Elle s'appelle **MountainCar**, et à première vue elle ressemble beaucoup au pendule inversé que vous connaissez depuis la semaine 1 : deux nombres d'observation, trois actions, un épisode court. La ressemblance s'arrête là. Du point de vue de l'exploration, cette tâche est redoutable.

Le décor : une voiture est immobilisée au **fond d'une vallée**, entre deux collines. Le but est un drapeau placé en haut de la colline de droite. Le moteur de la voiture est trop faible pour gravir la pente directement, et c'est tout le problème.

{{% comment %}}SOURCE: LAPAN ch.18 p.555 (image){{% /comment %}}

Pour atteindre le sommet, les actions doivent être appliquées **d'une façon particulière** : il faut faire osciller la voiture d'avant en arrière, en poussant dans le sens du mouvement à chaque fois, pour accumuler assez d'énergie. Autrement dit, il faut exécuter des **dizaines d'actions coordonnées** dans le bon ordre avant que quoi que ce soit se produise. Ce n'est pas le genre de coordination qu'un enchaînement d'actions aléatoires produit, et vous reconnaissez exactement la structure de River Swim : une région intéressante accessible seulement par une longue séquence, et un environnement qui annule le progrès dès que la séquence est interrompue.

{{% comment %}}SOURCE: LAPAN ch.18 p.556{{% /comment %}}

Voici l'interface, qui est celle que le laboratoire utilisera :

| Élément | Valeur |
| --- | --- |
| Identifiant | `MountainCar-v0` |
| Observation | deux nombres, **position** et **vitesse**, `Box([-1.2, -0.07], [0.6, 0.07], (2,), float32)` |
| Actions | trois, `Discrete(3)` : 0 pousser à gauche, 1 ne rien faire, 2 pousser à droite |
| Récompense | **\(-1\) à chaque pas**, sans exception |
| Fin d'épisode | troncature à **200 pas**, d'où un retour de **\(-200\)** par défaut |
| Meilleure politique connue | un retour total **autour de \(-80\)** |

{{% comment %}}SOURCE: LAPAN ch.18 p.556, p.557{{% /comment %}}

Arrêtons-nous sur la récompense, parce qu'elle est le cœur de la difficulté et qu'elle est contre-intuitive. L'agent reçoit **\(-1\) à chaque pas**, quoi qu'il fasse. Il n'y a donc **aucun gradient de récompense** qui indiquerait de monter plutôt que de descendre, de pousser plutôt que d'attendre : tant que le drapeau n'est pas atteint, toutes les politiques se valent exactement, et toutes valent \(-200\). La récompense ne devient informative qu'au moment où un épisode se termine **avant** la troncature, c'est-à-dire au moment où le but a été atteint. Avant ce moment, l'agent optimise une constante.

> [!IMPORTANT]
 **Je dois insister, parce que c'est la définition la plus nette d'une récompense parcimonieuse que ce cours puisse vous donner.** Ici, la récompense ne distingue pas les bonnes des mauvaises actions : elle distingue uniquement les épisodes qui ont atteint le but de ceux qui ne l'ont pas atteint. Tant que le but n'a jamais été atteint, le jeu de données de l'agent est **entièrement plat** : des millions de transitions portant toutes la même récompense. Un réseau entraîné là-dessus apprendra parfaitement bien que tout vaut \(-200\), sa perte diminuera, ses gradients seront propres, son entraînement sera stable, et il n'aura rien appris. **Un entraînement sain qui n'apprend rien** : voilà le symptôme à reconnaître, et c'est le pire de tous, parce qu'il n'alerte aucun des diagnostics que les dix premières semaines vous ont donnés.

Un dernier élément du protocole, et il gouverne tous les chiffres de la section 11.6. Une exécution est déclarée **réussie** lorsque le **retour de test moyen dépasse \(-130\)**. C'est un seuil **déclaré**, pas une propriété de la tâche : il est à mi-chemin entre l'échec complet (\(-200\)) et la meilleure politique connue (\(-80\)), et il est mesuré sur l'environnement **sans prime**, conformément à la règle de la section 11.4. Je le donne ici pour que vous sachiez, en lisant le tableau de la section 11.6, ce que le mot « résolue » veut dire exactement.

{{% comment %}}SOURCE: LAPAN ch.18 p.559, p.564 (images){{% /comment %}}

---

## La mesure de référence : jamais une seule fois

Lançons maintenant la méthode que le cours connaît le mieux : un réseau Q profond avec une politique \(\varepsilon\)-gloutonne, exactement comme en semaine 5, avec le calendrier de décroissance habituel. Le \(\varepsilon\) part de \(1{,}0\) et descend à \(0{,}02\) sur les **cent mille premiers pas** d'entraînement.

Cent mille pas, sur cette tâche, c'est **deux à trois minutes** de calcul et environ **cinq cents épisodes**. Voici le résultat, et je vous demande de le lire deux fois : **l'état but n'a pas été atteint une seule fois.**

{{% comment %}}SOURCE: LAPAN ch.18 p.556-557{{% /comment %}}

Ce n'est pas la partie grave. La partie grave est ce qui se passe **ensuite** : à ce stade, le \(\varepsilon\) a fini de décroître, donc l'agent ne fera **plus d'exploration du tout**. Il jouera désormais gloutonnement une fonction de valeur apprise sur un jeu de données où le but n'apparaît jamais, c'est-à-dire une fonction qui vaut à peu près la même chose partout. L'échec n'est donc pas lent : il est **permanent**. Le calendrier qui devait organiser le passage de l'exploration à l'exploitation a fermé la porte avant que quoi que ce soit ait été trouvé.

{{% comment %}}SOURCE: LAPAN ch.18 p.557{{% /comment %}}

Essayons alors la réponse naïve, celle que tout le monde propose en premier : explorons **beaucoup plus longtemps**. Une variante existe, qui maintient \(\varepsilon = 1\), c'est-à-dire un agent purement aléatoire, **jusqu'à ce qu'un seul épisode fasse mieux que \(-200\)**, puis qui décroît sur un million de trames. C'est le dispositif le plus favorable qu'on puisse imaginer : l'exploration ne se referme pas avant d'avoir trouvé quelque chose.

Résultat : cette version a tourné **cinq heures**. Après **cinq cent mille épisodes**, elle n'avait toujours pas rencontré un seul exemple du but, et l'exécution a été abandonnée.

{{% comment %}}SOURCE: LAPAN ch.18 p.558{{% /comment %}}

> [!WARNING]
 **Voici la phrase qui justifie cette semaine entière, et c'est une phrase sur les méthodes, pas sur cette tâche.** Quelle que soit la méthode d'apprentissage dont vous disposez, **sans une exploration appropriée, vous pouvez simplement échouer à entraîner**. Pas échouer à battre un record, pas échouer à converger vite : échouer à entraîner. Cinq heures de calcul, un demi-million d'épisodes, et un jeu de données qui ne contient aucune information sur la tâche à résoudre. Remarquez que l'on aurait pu remplacer ici le réseau Q profond par n'importe laquelle des méthodes des semaines 6 à 10, les plus sophistiquées comprises : elles auraient toutes appris, avec une efficacité d'échantillon exemplaire, que tout vaut \(-200\).

{{% comment %}}SOURCE: LAPAN ch.18 p.557{{% /comment %}}

Avant de passer aux correctifs, je vous donne l'instrument qui rend cet échec **visible**, parce que la courbe de récompense, elle, ne montre rien : c'est une ligne plate à \(-200\) et elle le restera. Deux lignes de journal suffisent, et je vous les demanderai dans le laboratoire.

```python
# Les DEUX diagnostics propres a cette semaine. La courbe de recompense ne
# sert a rien ici : elle vaut -200 partout, pour toutes les methodes, jusqu'au
# jour ou l'une d'elles trouve le but.
atteintes_du_but = 0          # combien de fois le but a ete atteint, EN TOUT
position_max_episode = -1.2   # la position la plus a droite vue dans l'episode

# ... dans la boucle, apres chaque pas :
position_max_episode = max(position_max_episode, float(obs[0]))
if termine:                   # termine, et NON tronque : c'est le but
    atteintes_du_but += 1

# ... a la fin de chaque episode :
journal.add_scalar("exploration/atteintes_du_but", atteintes_du_but, episode)
journal.add_scalar("exploration/position_max", position_max_episode, episode)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| atteinte du but | épisode **terminé** et non tronqué | `termine` |
| troncature à 200 pas | fin d'épisode sans atteinte du but | `tronque` |
| couverture de l'espace d'états | la position la plus à droite atteinte | `position_max_episode` |
| progrès avant le premier succès | la seule quantité qui bouge avant la découverte | `exploration/position_max` |

> [!TIP]
 **Pourquoi la position maximale est le bon instrument, et pourquoi je vous l'impose dans le laboratoire.** Sur une tâche à récompense parcimonieuse, la récompense ne mesure rien avant le premier succès, et une courbe plate ne vous dit pas si vous êtes à deux doigts du but ou à l'autre bout de l'espace d'états. Il faut donc instrumenter la **couverture** plutôt que la performance, et choisir pour cela une grandeur qui bouge : ici, la position la plus à droite atteinte dans l'épisode. Elle n'entre dans aucun apprentissage, elle ne modifie pas le problème, et elle vous dira dès les premières minutes si votre méthode d'exploration pousse la voiture plus haut que la précédente. Transposez le principe : sur une tâche parcimonieuse, demandez-vous toujours **quelle grandeur mesurable progresse avant le premier succès**.

---
