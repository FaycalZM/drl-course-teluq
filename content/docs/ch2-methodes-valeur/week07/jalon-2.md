---
title: "Jalon 2 : accélérer et comparer, honnêtement (25 %)"
weight: 16
---

## Ce qui est évalué, et pourquoi les deux moitiés de la semaine sont dans le même jalon

Le jalon 2 clôt le module 2 et vaut **25 %** de la note du cours. **Remise : fin de la semaine 7.**

Ce que je vous demande tient en une phrase : **un réseau Q profond, au moins deux extensions, une comparaison qui tient debout, et une accélération mesurée.** La comparaison vient de la semaine 6, l'accélération de la première moitié de celle-ci, et les deux sont dans le même jalon parce qu'elles sont les deux faces d'une seule compétence : savoir produire un chiffre, et savoir dire ce qu'il vaut.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

Ce qui est nouveau, et je veux que ce soit parfaitement clair avant que vous commenciez : **à partir de ce jalon, toute comparaison repose sur plusieurs graines aléatoires avec des intervalles de confiance.** Les semaines 3 à 6 comparaient des exécutions uniques. Ce n'est plus accepté, et la raison est entièrement contenue dans la section 7.2 : une exécution unique ne permet de décider de rien. Si votre volet C de la semaine 6 comparait quatre variantes sur une graine chacune, votre premier travail de ce jalon est de le refaire correctement, et c'est précisément la correction que ce jalon existe pour obtenir.

{{% comment %}}SOURCE: LAPAN ch.9 p.287-288{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---

## Le budget de calcul, fixé ici et non laissé à votre appréciation

Je tranche ce point explicitement, parce que l'exigence de plusieurs graines et la contrainte d'un processeur graphique partagé se contredisent si on les laisse toutes les deux ouvertes.

**L'étude comparative tourne sur `CartPole-v1`.** Pas sur un jeu Atari. Cinq graines pour quatre variantes à l'échelle d'Atari représentent une dizaine d'heures de calcul et ne tiennent pas dans une semaine sur Colab ; à l'échelle de CartPole, une variante converge en quelques minutes, et trois variantes sur cinq graines représentent moins d'une heure. Le choix est donc fait pour vous, et il est le même que celui de la semaine 6.

**L'accélération, elle, se mesure sur ce que vous profilez vous-même**, c'est-à-dire sur votre propre socle de code, sur votre propre environnement et sur votre propre matériel. Je n'impose ni environnement ni plateforme pour cette partie : j'impose que la version de référence et les variantes soient mesurées **à l'identique**, sur les mêmes graines, avec le seuil d'arrêt fixé d'avance, et que votre matériel soit indiqué.

**Ce qui ne rapporte aucun point supplémentaire** : une exécution à l'échelle d'Atari, un entraînement de plusieurs heures, un nombre de graines supérieur à cinq. Le temps économisé est à dépenser dans l'analyse, qui est la partie notée.

**Ordre de grandeur attendu** : deux à trois heures de calcul au total, et le reste du temps en lecture de vos propres chiffres.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

---

## Les étapes du livrable

**Étape 1, un socle unique.** Un seul code, et les variantes activées par un **drapeau de ligne de commande**. Vous aviez déjà cette contrainte en semaine 6, et je la répète parce qu'elle est la condition de possibilité de tout le reste : quatre scripts écrits séparément ne se comparent pas, puisque rien ne garantit qu'ils partagent l'initialisation, l'ordre des tirages ou le prétraitement. Les deux extensions au minimum sont à choisir dans la liste de la semaine 6 : cible à \(n\) étapes, double DQN, architecture duale, réseaux bruités, tampon de rejeu priorisé.

{{% comment %}}SOURCE: LAPAN ch.6 p.227-232{{% /comment %}}

**Étape 2, la version de référence, et elle apprend.** Mesurez-la d'abord, montrez qu'elle converge, et **ensuite** seulement appliquez quoi que ce soit. Cette contrainte d'ordre fait partie du livrable : si une accélération fait cesser la convergence, vous la rapportez comme un **échec de l'accélération**, vous ne l'omettez pas. Une accélération qui casse l'apprentissage est un résultat, et c'est même un des plus utiles.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

**Étape 3, la comparaison.** Au moins **3 graines** par variante, **5 de préférence**, **le même jeu de graines** pour toutes les variantes. Les courbes se tracent en **moyenne avec une plage ombrée**, jamais comme une exécution unique. Et vous rapportez, pour chaque variante, le **nombre d'exécutions qui n'ont pas convergé**, séparément de la moyenne.

{{% comment %}}SOURCE: LAPAN ch.9 p.287-288, p.302{{% /comment %}}

**Étape 4, le tableau d'accélération.** Pas un adjectif, un tableau. Colonnes exigées : variante, débit en trames par seconde, \(\Delta_{\text{FPS}}\) en pourcentage, temps d'horloge jusqu'au **seuil fixé d'avance**, \(\Delta_T\) en pourcentage, nombre de graines, intervalle. Et le **matériel**, écrit quelque part sur la page.

{{% comment %}}SOURCE: LAPAN ch.9 p.288, p.302{{% /comment %}}

**Étape 5, l'analyse.** Une mesure, une déduction, une conclusion. Trois choses doivent y figurer : au moins un cas où les deux indicateurs se contredisent (ou la mention explicite qu'il n'y en a pas eu), le traitement des écarts dont les intervalles se recouvrent, et ce que vous changeriez si vous disposiez de dix fois le budget.

> [!TIP]
 **Deux exemples travaillés, offerts, pour que vous voyiez à quoi ressemble une bonne lecture.** Premier exemple : dans le Tableau 7-1, la ligne sans `torch.no_grad()` donne \(-4{,}3\,\%\) de débit et \(-2{,}3\,\%\) de temps. Les deux indicateurs pointent en sens opposé, les deux écarts sont petits, et la version de référence elle-même varie de 227 à 229 trames par seconde selon la mesure. La bonne conclusion n'est pas « retirer `no_grad()` accélère la résolution », c'est : **il n'y a pas de différence mesurable sur ce réseau, et la seule façon de le savoir était de répéter.** Second exemple : avec une seule trame empilée, Pong est encore résolu, mais **3 exécutions sur 8 n'ont pas convergé**. Une moyenne sur huit exécutions, présentée seule, cache un taux d'échec de 37 %. La bonne conclusion est que cette variante est **instable**, et aucun chiffre moyen ne pouvait le dire. Ces deux exemples sont la raison d'être de toute l'étape 3.

{{% comment %}}SOURCE: LAPAN ch.9 p.294, p.299, p.302{{% /comment %}}

---

## Livrables, barème et contraintes

| Élément évalué | Forme | Points |
| --- | --- | --- |
| **1.** Socle de code unique, les variantes activées par un drapeau, réseau Q profond plus au moins deux extensions | carnet Colab, sorties visibles | 3 |
| **2.** Version de référence mesurée **et** montrée convergente avant toute accélération | carnet, une courbe | 3 |
| **3.** Courbes comparatives en moyenne avec intervalle, même jeu de graines pour toutes les variantes | carnet, une figure par comparaison | 5 |
| **4.** Tableau d'accélération complet : variante, FPS, ΔFPS, temps au seuil, ΔTemps, graines, intervalle, matériel | tableau | 4 |
| **5.** Le désaccord entre les deux indicateurs : un cas commenté, ou la mention explicite qu'il n'y en a pas eu | note, un paragraphe | 2 |
| **6.** Nombre d'exécutions non convergées, rapporté séparément de la moyenne, pour chaque variante | tableau ou note | 2 |
| **7.** Analyse critique : une mesure, une déduction, une conclusion ; les écarts dont les intervalles se recouvrent déclarés comme non-résultats | note de 1 à 2 pages | 4 |
| **8.** Reproductibilité : graines listées, hyperparamètres, seuil d'arrêt fixé d'avance, matériel, durée totale | annexe d'une demi-page | 2 |

**Ce qui n'est pas demandé**, et que je ne noterai pas : battre un score particulier, obtenir une accélération d'un facteur donné, atteindre une performance d'état de l'art, ou exécuter quoi que ce soit à l'échelle d'Atari. Un **résultat nul correctement établi** vaut mieux qu'un écart impressionnant obtenu sur une seule exécution, et il sera noté comme tel.

> [!IMPORTANT]
 **Un conseil de rédaction, et c'est le même qu'au jalon 1.** Écrivez votre note comme si vous expliquiez à un collègue ce que vos mesures permettent de conclure et ce qu'elles ne permettent pas. Pas de récit chronologique de vos essais : une mesure, une déduction, une conclusion. Et si votre conclusion est « ces deux variantes ne se distinguent pas sur trois graines », écrivez-la ainsi, sans excuse. C'est la phrase la plus difficile à écrire dans ce domaine, et c'est celle que je cherche.

{{% comment %}}SOURCE: raw-content/week-03.md §Jalon 1{{% /comment %}}

---
