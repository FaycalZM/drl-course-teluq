---
title: "Jalon 4 : une extension avancée, et le dernier jalon du cours (25 %)"
weight: 19
---

## Ce qui est évalué, et pourquoi ce jalon est différent des trois autres

Le jalon 4 clôt le module 4 et vaut **25 %** de la note du cours.

Les trois premiers jalons vous imposaient une méthode : une méthode d'entropie croisée au jalon 1, un réseau Q profond avec extensions au jalon 2, une méthode de politique au jalon 3. **Celui-ci vous laisse choisir**, parmi cinq routes tirées des semaines 11 à 14, et c'est le seul du cours où la question « laquelle choisir » fait partie du travail.

Ce que je vous demande tient en une phrase : **une extension avancée de votre agent, choisie et justifiée, mesurée honnêtement, et reproductible par quelqu'un d'autre que vous.** Les trois exigences comptent, et je vais être explicite sur la dernière, parce qu'elle change de poids cette semaine.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

> [!IMPORTANT]
 **Après treize semaines, c'est sur la reproductibilité que je serai le plus strict, et voici pourquoi.** Le jalon 2 a installé les graines multiples et les intervalles. Le jalon 3 a ajouté le protocole écrit. Cette semaine vous a montré trois résultats dont la portée dépend entièrement du protocole : un tableau de quatre lignes à une exécution chacune, un score de détection obtenu par une seule personne étiquetant sans être à l'aveugle, et des seuils relevés au pixel sur une figure. Dans les trois cas, le chiffre seul induit en erreur et le chiffre avec son protocole informe. **Je note la seconde chose.** Concrètement : un résultat modeste, mesuré sur plusieurs graines, avec ses graines listées, ses hyperparamètres, son matériel, sa durée et son critère d'arrêt fixé d'avance, vaut plus de points qu'un résultat impressionnant dont je ne peux pas savoir d'où il vient. Et un résultat négatif correctement établi vaut autant qu'un résultat positif.

---

## Le jalon en un coup d'œil

Une seule chose distingue la forme de ce jalon des trois autres, et le schéma la place en tête : **la justification vient avant le code**. Les trois premiers jalons vous donnaient la méthode ; celui-ci vous demande d'abord de dire laquelle et pourquoi, et ce paragraphe est noté à part précisément pour que vous l'écriviez avant de commencer plutôt qu'après avoir fini.

{{< mermaid >}}
graph TD
  J["Étape 1 : la justification, et elle vient avant le code"] -->|"une route sur cinq, un environnement"| X["L'extension, et elle fonctionne"]
  X -->|"mêmes graines, même boucle d'évaluation"| K["Comparaison avec votre agent du jalon 3"]
  X --> G["La grille de diagnostic, appliquée à votre agent"]
  K --> A["L'analyse, et ce qu'elle ne permet pas de conclure"]
  G --> A
  A --> REP["L'annexe de reproductibilité : 4 points, le poste le plus lourd"]
{{< /mermaid >}}

Remarquez où aboutit le schéma. Dans les trois jalons précédents, la dernière case était l'analyse ; ici c'est l'annexe, et ce déplacement est le sujet de l'encadré ci-dessus.

---

## Les cinq routes, et vous en choisissez une

Les cinq valent le même nombre de points. Choisissez selon ce qui vous intéresse et selon ce que votre environnement permet, pas selon ce qui semble le plus difficile.

**Route 1 : l'exploration dirigée.** Ajoutez à votre agent un mécanisme d'exploration de la semaine 11, et mesurez ce qu'il achète sur un environnement à récompense parcimonieuse. L'exigence propre à cette route est la comparaison avec une exploration non dirigée sur la **même** tâche et les mêmes graines : sans cela, vous mesurez votre environnement et non votre mécanisme.

**Route 2 : l'auto-jeu.** Prenez un jeu à deux joueurs et faites apprendre un agent contre lui-même, selon la semaine 12. L'exigence propre : une mesure contre un adversaire **fixe** en plus de la mesure contre soi-même, parce qu'un score d'auto-jeu monte toujours et ne dit rien à lui seul.

**Route 3 : le multi-agent.** Deux agents ou plus dans un même environnement, selon la semaine 12. L'exigence propre : la **non-stationnarité** doit être mesurée et pas seulement mentionnée, par exemple en évaluant une politique gelée contre des adversaires de plusieurs époques d'entraînement.

**Route 4 : un modèle du monde.** Apprenez une dynamique et servez-vous-en, selon la semaine 13. L'exigence propre : un compte en **interactions avec l'environnement**, puisque c'est la ressource que cette famille prétend économiser, et une mesure de l'accumulation d'erreur du modèle sur un déroulement.

**Route 5 : une chaîne de préférences réduite.** Reprenez les volets B et C de cette semaine et montez-les d'un cran. L'exigence propre, et elle est la plus intéressante : votre critère d'étiquetage doit être **écrit en une phrase dans votre rapport**, et vous devez montrer un comportement de l'agent qui satisfait votre critère **sans** satisfaire votre intention, ou expliquer pourquoi vous n'y êtes pas parvenu. C'est le tour 3 de la section 14.8 reproduit à votre échelle, et c'est la route qui demande le moins de calcul et le plus de réflexion.

Les routes 1 à 4 ne sont **pas** réenseignées ici : elles renvoient aux semaines qui les portent, et c'est voulu. Ce jalon ne vous demande pas d'apprendre une méthode nouvelle, il vous demande de porter l'une de celles que vous avez déjà rencontrées jusqu'à une mesure défendable.

---

## Le budget de calcul, fixé ici et non laissé à votre appréciation

Je tranche ce point explicitement, comme aux jalons 2 et 3, parce que l'exigence de plusieurs graines et la contrainte d'un processeur graphique partagé se contredisent si on les laisse toutes les deux ouvertes.

**Toutes les mesures tournent sur une tâche assez petite pour que trois à cinq graines tiennent dans une soirée.** Une tâche de contrôle classique, un monde en grille, un petit jeu à deux joueurs. Pas de jeu Atari en couleur pleine résolution, et surtout pas la chaîne complète de la première moitié de cette semaine, dont le coût mesuré est de treize heures de processeur graphique plus trois cents jugements humains.

**Ordre de grandeur attendu** : deux à quatre heures de calcul au total, et tout le reste du temps dans la lecture de vos propres chiffres.

**Ce qui ne rapporte aucun point supplémentaire** : un entraînement plus long, une tâche plus grosse, plus de cinq graines, ou l'implémentation d'une seconde route. Le temps économisé est à dépenser dans l'analyse et dans l'annexe de reproductibilité, qui sont les parties notées.

---

## Les étapes du livrable

**Étape 1, la justification du choix, et elle vient avant le code.** Une demi-page qui dit quelle route vous prenez, sur quel environnement, et **pourquoi cette route sur cet environnement**. Un mécanisme d'exploration dirigée sur une tâche à récompense dense ne mesure rien ; un modèle du monde sur un environnement dont le simulateur coûte une microseconde ne démontre rien. Je note ce paragraphe, et il est le plus facile du jalon.

**Étape 2, l'extension fonctionne, et vous le montrez.** Une courbe d'évaluation sur au moins trois graines, avec intervalle, et une cible annoncée à partir d'une exécution pilote. Si votre extension ne fonctionne pas, c'est l'étape à régler avant toutes les autres.

**Étape 3, la comparaison avec votre agent du jalon 3.** Même tâche, mêmes graines, **même boucle d'évaluation**. Sur deux axes au minimum, parmi l'efficacité d'échantillon, la stabilité, le temps d'horloge et la performance finale. Si deux de vos axes se contredisent, c'est le résultat le plus intéressant de votre rapport, et il faut le dire.

**Étape 4, la grille de diagnostic de cette semaine, appliquée à votre propre agent.** C'est la partie proprement nouvelle du jalon, elle est courte et je la veux explicite. Trois questions :

- Quelle est la récompense que votre agent **optimise**, et quelle est celle que vous voudriez qu'il maximise ? Si vous pensez que ce sont les mêmes, dites-le et argumentez-le, c'est une réponse acceptable.
- Si elles diffèrent, de quel **type d'écart** s'agit-il parmi les trois de la section 14.12 ?
- Quels **mécanismes** de la section 14.10 sont présents dans votre situation, et lesquels sont absents ? Deux mécanismes nommés et deux absences justifiées suffisent.

**Étape 5, l'analyse.** Une mesure, une déduction, une conclusion. Et deux choses que je veux trouver : les écarts dont les intervalles se recouvrent, déclarés comme des non-résultats ; et au moins une phrase sur ce que vos mesures **ne permettent pas** de conclure.

**Étape 6, l'annexe de reproductibilité, et c'est celle qui pèse le plus lourd de tout le cours.** Voyez le barème.

---

## Livrables, barème et contraintes

| Élément évalué | Forme | Points |
| --- | --- | --- |
| **1.** Justification de la route et de l'environnement : pourquoi cette extension est mesurable sur cette tâche | une demi-page | 2 |
| **2.** Extension implémentée et correcte, selon l'exigence propre à votre route | carnet Colab, sorties visibles | 5 |
| **3.** Elle **fonctionne**, montré sur au moins trois graines avec intervalle, cible annoncée depuis une exécution pilote | carnet, une courbe | 4 |
| **4.** Comparaison avec votre agent du jalon 3 sur au moins deux axes, mêmes graines, même boucle d'évaluation | tableau | 4 |
| **5.** Grille de diagnostic de la semaine appliquée à votre agent : récompense optimisée contre récompense voulue, type d'écart, deux mécanismes présents et deux absents | une page | 3 |
| **6.** Analyse critique : une mesure, une déduction, une conclusion ; les recouvrements d'intervalles déclarés comme non-résultats ; une phrase sur ce que les mesures ne permettent pas de conclure | note de 1 à 2 pages | 3 |
| **7.** **Reproductibilité** : graines listées, hyperparamètres complets, critère d'arrêt fixé d'avance, matériel, durée totale, versions des bibliothèques, et un dépôt qui tourne depuis un clone | annexe d'une page plus le dépôt | 4 |
| **Total** | | **25** |

**Ce qui n'est pas demandé**, et que je ne noterai pas : battre un score de référence, implémenter deux routes, reproduire une mesure de cette semaine, ou atteindre un seuil annoncé quelque part. Un **résultat nul correctement établi** vaut mieux qu'un écart impressionnant obtenu sur une seule exécution.

> [!IMPORTANT]
 **Un dernier conseil de rédaction, et c'est le même depuis le jalon 1 avec un ajout qui vient de cette semaine.** Écrivez votre note comme si vous expliquiez à un collègue ce que vos mesures permettent de conclure et ce qu'elles ne permettent pas. Pas de récit chronologique de vos essais : une mesure, une déduction, une conclusion. Et l'ajout de la semaine 14 : **dites qui a décidé de la grandeur que vous rapportez.** Si vous avez choisi de rapporter la performance finale plutôt que l'efficacité d'échantillon, c'est une décision, et elle oriente la conclusion. Si vous avez choisi un critère d'arrêt, c'est une décision, et la section 14.8 vous a montré qu'elle peut faire la différence entre le meilleur et le pire résultat d'une même exécution. Les trois résultats que cette semaine a examinés de près tiraient leur fragilité de décisions de ce genre, jamais d'une erreur de calcul.

{{% comment %}}SOURCE: source-assets/raw-content/week-10.md §Jalon 3{{% /comment %}}

---

## Remise

{{< remise cle="jalon-4" >}}
