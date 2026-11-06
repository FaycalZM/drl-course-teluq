---
title: "15.6 Ce qui a transféré, et ce qui n'a pas transféré"
weight: 7
---

## Quatre applications, quatre méthodes du cours, aucune nouveauté

Faisons le compte, parce qu'il est le premier résultat de la semaine et qu'il est meilleur que je ne l'aurais cru avant de l'établir.

| Application | Méthode employée | Semaine du cours | Modifiée ? |
| --- | --- | --- | --- |
| Le marché | réseau Q profond | semaine 5, accéléré en semaine 7 | non |
| Le paragraphe | réseau Q profond | semaine 5 | entrée en couple, tête à une sortie |
| La page rendue | acteur-critique à avantage, environnements vectorisés | semaine 8 | non |
| La permutation | recherche arborescente de Monte-Carlo guidée par un réseau à deux têtes | semaine 12 | remontée par maximum |

Quatre applications, et **aucune méthode nouvelle**. Cette ligne est le meilleur argument que je puisse vous donner en faveur du programme que vous venez de suivre : les quatre domaines les plus éloignés que ce cours pouvait aller chercher réemploient tous une méthode enseignée entre les semaines 5 et 12, et les deux modifications de la colonne de droite sont des adaptations de **forme d'entrée** et de **règle de remontée**, pas des méthodes.

Dit autrement : votre inventaire de méthodes est, pour l'essentiel, complet. Ce qui ne l'est pas, c'est votre jugement sur **laquelle employer**, et c'est le sujet de la section 15.10.

---

## Trois choses qui n'ont pas transféré, et la troisième est la plus utile

Maintenant l'autre colonne, et elle est plus instructive.

**Un : les enveloppes n'ont pas transféré.** C'est le constat le plus immédiat et le plus coûteux en heures. La tâche textuelle ne respecte pas la convention de Gymnasium et exige un adaptateur écrit à la main. La page rendue exige une enveloppe de clic sur mesure, qui transforme un indice entre 0 et 255 en une position de curseur et un événement de clic. Le cube exige deux représentations d'état et la conversion entre elles. Dans les quatre cas, le code que vous avez écrit dans les semaines 1 à 13 se réemploie **au niveau de la méthode** et pas du tout **au niveau de l'interface**. Budgétez l'interface.

**Deux : la généralisation n'a pas transféré.** Et là, il faut être précis, parce que c'est le résultat négatif le plus silencieux des quatre applications. Sur la tâche textuelle, un agent entraîné sur **un** jeu le résout en trois minutes et cent vingt épisodes, et sa récompense de **validation est nulle** : il ne résout aucun autre jeu. Entraîné sur vingt jeux pendant deux heures, il plafonne en validation à **2 sur 6** et occupe les cinquante pas de la limite de temps, ce qui est la signature d'un agent qui se promène à peu près au hasard. La meilleure variante essayée atteint le maximum en deux heures et demie, puis **se dégrade** : elle surapprend et désapprend. Et une variante qui emploie des **plongements de phrase** (*sentence embeddings*) préentraînés apprend **plus vite par épisode** et **valide moins bien**.

{{% comment %}}SOURCE: LAPAN ch.13 p.412-420{{% /comment %}}

Prenez une minute sur cette dernière phrase, parce qu'elle contredit un réflexe très répandu. Un composant préentraîné a accéléré l'apprentissage et dégradé la généralisation. Les deux mesures sont bonnes. Si vous ne regardez que la courbe d'entraînement, vous concluez que le préentraînement aide ; si vous regardez la validation, vous concluez l'inverse. **C'est le même protocole que la semaine 7 a imposé au marché, et c'est le même piège.**

**Trois : les chiffres publiés n'ont pas transféré**, et c'est l'objet de la section 15.7 tout entière.

---

## Le tableau de coût du cours, et je le mets ici parce que c'est la dernière occasion

Avant d'aller aux résultats négatifs, voici un objet que je dois à votre projet final : le coût en calcul de ce que ce cours a décrit, rassemblé en un seul endroit. Ce ne sont pas des références, ce sont des **ordres de grandeur**, et c'est précisément le genre de chiffre qu'on n'a jamais quand on en a besoin.

| Ce qui est mesuré | Coût mesuré | Semaine |
| --- | --- | --- |
| Un réseau Q profond sur le plus simple des jeux d'arcade | 1 à 3 heures sur un bon processeur graphique | 5 |
| Un agent de courtage sur une année de barres à la minute | quelques minutes, données fournies | 7 |
| Une exécution sur le banc d'essai de contrôle continu | 8 à 20 heures, **par exécution et par méthode** | 10 |
| La même méthode hors politique, 5 millions de transitions | 9 à 13 heures | 10 |
| Un auto-jeu complet, deux pas d'apprentissage comparés | 2 fois 10 heures, 40 000 parties | 12 |
| Une méthode à modèle appris sur un petit jeu de plateau | 15 heures, 3 400 épisodes, et elle ne converge pas | 12 |
| Un modèle du monde sur une tâche de contrôle visuel | 10 à 20 heures **par tâche**, et environ 15 par tâche et par graine | 13 |
| Une chaîne complète de rétroaction humaine | environ 13 heures, 12 Go de segments, 300 jugements humains | 14 |
| L'agent textuel de la section 15.3, vingt jeux | 14 heures, 8 000 épisodes | 15 |
| L'agent de clic de la section 15.4, tâche élémentaire | environ 8 minutes pour une récompense moyenne de 0,9 | 15 |
| Le même agent sur un tic-tac-toe, avec démonstrations | 2 heures pour une récompense moyenne de 0,05 | 15 |
| Le cube trois par trois, entraînement complet | environ 20 heures, et environ **6 jours** pour refaire l'entraînement d'origine sur un seul processeur graphique | 15 |
| Le même problème réduit à un cube deux par deux | 1 à 2 heures | 15 |
| Le grand modèle de langue de la section 15.9, vingt jeux | 450 000 jetons, 0,20 dollar, **aucun entraînement** | 15 |

{{% comment %}}SOURCE: source-assets/raw-content/week-05.md §5.9{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-10.md §10.1, §10.6{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-12.md §12.5, §12.8{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-13.md §13.7{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-14.md §14.4{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.13 p.414, p.426{{% /comment %}} {{% comment %}}SOURCE: LAPAN ch.14 p.441, p.456-457{{% /comment %}} {{% comment %}}SOURCE: LAPAN ch.21 p.668-670{{% /comment %}}

> [!TIP]
 **Trois lectures de ce tableau, et chacune est une consigne pour votre rapport.** **Un :** l'unité naturelle du coût d'une expérience d'apprentissage par renforcement est la **dizaine d'heures de processeur graphique par exécution**, ce qui veut dire que dix graines par configuration représentent des semaines de machine. C'est la raison pour laquelle les tableaux publiés ont souvent une exécution par case, et c'est la raison pour laquelle votre jalon 3 mesurait sur une tâche assez petite pour que dix graines tiennent dans une soirée. **Deux :** le choix de la taille de la tâche est un **choix de méthode**, pas une facilité. C'est lui qui rend votre conclusion possible ou impossible. **Trois :** regardez la dernière ligne et la ligne du cube côte à côte. Six jours de calcul d'un côté, vingt centimes de l'autre. Les deux ne font pas la même chose, et la section 15.9 dira exactement quoi, mais l'écart de trois ordres de grandeur dans le coût est un fait de 2024 dont votre rapport doit tenir compte au moment de choisir son approche.

---
