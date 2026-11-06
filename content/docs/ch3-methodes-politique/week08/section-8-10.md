---
title: "8.10 Synchrone, asynchrone"
weight: 11
---

## Le troisième A, et ce qu'il ajoute vraiment

Il existe une variante d'A2C dont le nom ajoute une lettre : **A3C**, pour **acteur-critique à avantage asynchrone**. L'algorithme d'apprentissage est **le même** : mêmes trois termes de perte, même avantage, même critique. Ce que la troisième lettre ajoute est une **véritable interaction asynchrone** avec les environnements, c'est-à-dire plusieurs processus qui jouent et calculent en même temps au lieu de se relayer dans une seule boucle. C'est l'une des architectures les plus employées en pratique, et c'est aussi la raison pour laquelle cette section existe alors que son contenu ne sera pas exécuté dans le laboratoire.

{{% comment %}}SOURCE: LAPAN ch.12 p.373{{% /comment %}}

Je le dis donc tout de suite, pour que vous lisiez cette section dans le bon état d'esprit : **cette section se lit et se discute, elle ne s'exécute pas dans un carnet partagé.** Les processus multiples y sont limités, et une implémentation à quatre processus et huit environnements chacun n'y tient pas. Vous saurez à la fin de la section ce que chaque architecture coûte et ce qu'elle rapporte, et votre laboratoire utilisera la version vectorisée de la section 8.9, qui règle le problème 4 sans processus.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

---

## Deux architectures, et la comparaison est tout le contenu

Il y a deux façons de distribuer A2C sur plusieurs processus, et elles diffèrent par **ce qui circule sur les flèches**. La **Figure 8-6** et la **Figure 8-7** sont volontairement identiques en disposition : regardez uniquement les étiquettes des flèches et l'endroit où la perte est calculée.

Première architecture, celle de la **Figure 8-6**, le **parallélisme de données** (*data parallelism*). Plusieurs processus enfants parlent chacun à un ou plusieurs environnements et expédient leurs transitions \((s, r, a, s')\) à un unique processus d'entraînement, qui calcule les pertes et effectue le pas de descente de gradient. Les poids mis à jour doivent ensuite être **rediffusés** à tous les enfants, sans quoi ils continueraient à jouer une politique périmée.

{{< bookfig src="08-06.png" week="08" >}}

Seconde architecture, celle de la **Figure 8-7**, le **parallélisme de gradients** (*gradient parallelism*). Chaque processus enfant calcule la perte **et les gradients** sur ses propres échantillons, puis expédie les **gradients** au processus central, qui les additionne et effectue un seul pas de descente. Les poids mis à jour repartent vers tous les enfants, exactement comme dans le premier cas, et pour la même raison : garder les données sur politique.

{{< bookfig src="08-07.png" week="08" >}}

{{% comment %}}SOURCE: LAPAN ch.12 p.375{{% /comment %}}

**Pourquoi cette différence compte, et c'est un argument de coût et non d'élégance.** Décomposons ce que fait une itération d'A2C. L'opération lourde est l'étape d'entraînement : un passage avant pour calculer la perte, puis un passage arrière pour obtenir les gradients. L'opération **légère** est le pas de descente lui-même, qui consiste à ajouter aux poids des gradients mis à l'échelle, et qui est une poignée d'additions vectorielles. Dans le parallélisme de données, tout le lourd reste dans le processus central, qui devient le goulot d'étranglement dès qu'on ajoute des enfants. Dans le parallélisme de gradients, le lourd est distribué chez les enfants et le central ne fait plus que du léger. C'est cela, et seulement cela, qui rend la seconde architecture extensible.

{{% comment %}}SOURCE: LAPAN ch.12 p.376{{% /comment %}}

---

## Ce qui survit sur une seule machine

Voici la conclusion pratique, et elle justifie précisément le choix du laboratoire.

Si vous disposez d'une douzaine de processeurs graphiques ou plus, répartis sur plusieurs machines, le parallélisme de gradients est le bon choix : il est le seul à passer l'échelle. Avec **un seul** processeur graphique, les deux architectures se comportent de façon **comparable**, et le parallélisme de données est alors **plus simple à implémenter**, pour une raison très concrète : vous ne manipulez jamais de valeurs de gradient à la main. Vous échangez des tableaux de transitions, qui sont des données ordinaires, au lieu d'échanger des tenseurs de gradients, dont il faut gérer l'accumulation, la remise à zéro et la correspondance avec les paramètres.

{{% comment %}}SOURCE: LAPAN ch.12 p.376{{% /comment %}}

Quelques ordres de grandeur, pour que vous sachiez ce qui est en jeu. Le passage d'un ensemble d'environnements vectorisés **synchrone** à un ensemble **asynchrone** est un remplacement direct, une ligne de code, et sur cinquante environnements il fait passer le débit à environ **2 000 trames par seconde**, soit un facteur deux par rapport à la version séquentielle. Une implémentation A3C à parallélisme de gradients, avec quatre processus enfants gérant chacun huit environnements, atteint de **500 à 600 trames par seconde par enfant**, soit de **2 000 à 2 400** au total, et résout le jeu en huit à dix millions d'observations, c'est-à-dire environ une heure et demie. Le parallélisme de gradients y est **légèrement** plus rapide que le parallélisme de données, ce qui confirme la conclusion ci-dessus : sur une seule machine, l'écart ne justifie pas la complexité.

{{% comment %}}SOURCE: LAPAN ch.12 p.377{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.12 p.384{{% /comment %}}

Un mot sur les deux tailles de lot d'une implémentation à parallélisme de gradients, parce qu'elles remplacent la taille de lot unique à laquelle vous êtes habitués et que leur rôle n'est pas symétrique. Le premier nombre est la quantité d'échantillons que **chaque enfant** accumule avant de calculer ses gradients, par exemple 64. Le second est le nombre d'**enfants** dont les gradients sont additionnés avant un pas de descente, par exemple 2. Chaque pas d'optimisation consomme donc le produit des deux. Le premier est **grand**, parce que le calcul de la perte et la rétropropagation sont coûteux et qu'il faut les amortir. Le second doit rester **petit**, et pour une raison qui est le fil rouge de toute la semaine : plus on additionne de gradients avant de mettre à jour, plus les derniers gradients ont été calculés avec une politique différente de celle qu'on est en train de corriger, et plus on s'éloigne de la contrainte sur politique.

{{% comment %}}SOURCE: LAPAN ch.12 p.378-379{{% /comment %}}

> [!WARNING]
 **Trois détails d'exploitation du multiprocessus, et ils ne sont pas facultatifs.** Premièrement, la méthode de démarrage des processus doit être fixée explicitement à `spawn` : c'est la seule compatible avec les tenseurs résidant sur un processeur graphique. Deuxièmement, il faut limiter le nombre de fils d'exécution de la bibliothèque de calcul sous-jacente, en posant `OMP_NUM_THREADS=1` dans l'environnement avant de démarrer les enfants. Sans cela, la bibliothèque lance un fil par cœur **dans chaque processus**, ces fils se disputent les mêmes cœurs que les processus que vous avez créés, et la mesure donne une perte de performance d'un facteur **trois à quatre**. Troisièmement, les processus enfants doivent être arrêtés et attendus dans un bloc `finally`, faute de quoi un plantage du parent laisse derrière lui des processus zombies qui retiennent la mémoire du processeur graphique, et le prochain lancement échoue pour une raison qui n'a aucun rapport apparent avec votre erreur.

{{% comment %}}SOURCE: LAPAN ch.12 p.381-383{{% /comment %}}

Une dernière curiosité technique, pour ceux que la mécanique intéresse : le réseau peut être placé en **mémoire partagée**, de sorte que tous les processus voient les mêmes paramètres. Les **gradients**, en revanche, restent **locaux** à chaque processus, parce que chacun calcule les siens sur ses propres échantillons. C'est cette asymétrie, paramètres partagés et gradients privés, qui dispense d'une synchronisation explicite des tampons de gradient, et c'est elle qui rend l'implémentation praticable.

{{% comment %}}SOURCE: LAPAN ch.12 p.381-382{{% /comment %}}

---
