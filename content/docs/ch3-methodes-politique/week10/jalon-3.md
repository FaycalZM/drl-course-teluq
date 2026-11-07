---
title: "Jalon 3 : une méthode de politique contre une méthode de valeur (25 %)"
weight: 9
---

## Ce qui est évalué, et pourquoi ce jalon regarde en arrière

Le jalon 3 clôt le module 3 et vaut **25 %** de la note du cours.

Ce que je vous demande tient en une phrase : **une méthode de politique qui apprend, une analyse de la variance de son gradient, et une comparaison honnête avec le réseau Q profond de votre jalon 2.** Les trois parties pèsent à peu près autant, et c'est la troisième qui est l'intérêt réel de ce jalon : vous allez mettre face à face les deux grandes familles du cours, sur une même tâche, avec les mêmes graines, et dire ce que chacune achète et ce qu'elle coûte.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

Ce jalon reprend sans modification l'exigence installée au jalon 2 : **toute comparaison repose sur plusieurs graines avec intervalles**. La section 10.6 vous a donné le meilleur argument possible pour cette règle, un tableau de vingt mesures dont aucune ne porte d'intervalle et dont le plus mauvais chiffre est expliqué, par celui qui le publie, par une graine malheureuse. Je n'ajouterai rien.

---

## Le jalon en un coup d'œil

Le schéma montre la pièce qui fait l'intérêt de ce jalon, et c'est la **boucle d'évaluation partagée** : vos deux agents, celui que vous écrivez cette semaine et celui que vous avez rendu au jalon 2, doivent passer par le même tunnel, avec les mêmes graines et le même critère d'arrêt. C'est cette pièce commune, et elle seule, qui rend les trois axes comparables.

{{< mermaid >}}
graph TD
  R["Votre route : actions discrètes, ou continues"] --> P["La méthode de politique, et elle apprend"]
  P --> V["Variance du gradient, deux configurations"]
  P --> X["La même boucle d'évaluation pour les deux agents"]
  Q["Votre réseau Q profond du jalon 2"] --> X
  X -->|"efficacité d'échantillon"| A["Les trois axes"]
  X -->|"stabilité"| A
  X -->|"temps d'horloge"| A
  A -->|"s'ils se contredisent, c'est le résultat"| C["L'analyse critique"]
  V --> C
{{< /mermaid >}}

Notez que la variance du gradient part de votre méthode de politique et rejoint l'analyse sans passer par la comparaison : c'est une mesure sur **une** famille, pas une comparaison entre les deux. Les deux parties se rejoignent dans votre note, pas dans un tableau commun.

---

## Les deux routes, et vous en choisissez une

La comparaison avec le jalon 2 demande que les deux méthodes tournent sur la **même** tâche, et un réseau Q profond demande un espace d'actions discret. D'où deux routes, et elles valent le même nombre de points.

**Route 1, recommandée : actions discrètes, sur `CartPole-v1`.** Vous écrivez PPO, ou l'acteur-critique à avantage de la semaine 8, pour un espace d'actions discret, et vous le comparez directement au réseau Q profond de votre jalon 2 sur la même tâche. C'est la route la moins coûteuse et la plus directe : votre code du jalon 2 est déjà mesuré sur cette tâche, et PPO fonctionne sur les actions discrètes comme sur les continues.

**Route 2 : actions continues, sur `Pendulum-v1`.** Vous écrivez PPO ou la méthode hors politique de la section 10.5, sur la tâche du laboratoire. Pour la comparaison avec le jalon 2, il vous faut alors une méthode de valeur sur cette même tâche, et la semaine 9 vous a donné la recette : **discrétisez la dimension d'action unique** en une dizaine de niveaux et lancez un réseau Q profond dessus. La semaine 9 disait explicitement que la discrétisation reste praticable sur une ou deux dimensions d'action, et c'est ici qu'elle sert. Précisez votre nombre de niveaux : il fait partie de votre protocole.

{{% comment %}}SOURCE: source-assets/raw-content/week-09.md §9.1{{% /comment %}}

---

## Le budget de calcul, fixé ici et non laissé à votre appréciation

Je tranche ce point explicitement, comme au jalon 2, parce que l'exigence de plusieurs graines et la contrainte d'un processeur graphique partagé se contredisent si on les laisse toutes les deux ouvertes.

**Toutes les mesures tournent sur une tâche de contrôle classique**, `CartPole-v1` ou `Pendulum-v1` selon votre route. Pas de jeu Atari, et surtout pas le banc d'essai de la section 10.1 : une seule de ses exécutions coûte entre huit et vingt heures, et cinq graines de trois configurations y représenteraient plusieurs semaines de machine.

**Ordre de grandeur attendu** : deux à trois heures de calcul au total, et tout le reste du temps dans la lecture de vos propres chiffres.

**Ce qui ne rapporte aucun point supplémentaire** : un entraînement de plusieurs heures, une tâche plus grosse, un nombre de graines supérieur à cinq, ou l'implémentation de TRPO ou d'ACKTR. Le temps économisé est à dépenser dans l'analyse, qui est la partie notée.

---

## Les étapes du livrable

**Étape 1, un socle unique et des drapeaux.** Un seul programme, les variantes activées en ligne de commande, comme aux jalons 1 et 2. Votre méthode de politique et votre réseau Q profond peuvent être deux programmes distincts, puisqu'ils viennent de deux jalons, mais la **boucle d'évaluation** doit être la même pour les deux : même nombre d'épisodes de test, même absence de hasard à l'évaluation, même jeu de graines, même critère d'arrêt fixé d'avance.

**Étape 2, la méthode de politique apprend, et vous le montrez.** Une courbe d'évaluation sur au moins trois graines, avec intervalle, et votre cible annoncée à partir d'une exécution pilote. Si votre méthode ne converge pas, c'est l'étape à régler avant toutes les autres : les étapes 3 et 4 n'ont aucun sens sur une méthode qui n'apprend pas.

**Étape 3, l'analyse de la variance du gradient.** C'est la partie proprement nouvelle de ce jalon, et elle prolonge directement la mesure de variance de la semaine 8. Vous mesurez la **dispersion de l'estimateur du gradient de politique** entre minilots, et vous la comparez entre au moins **deux** configurations. Trois comparaisons sont acceptables, et vous en choisissez une au moins :

- avec et sans **normalisation de l'avantage**, toutes choses égales ;
- entre **deux valeurs de \(\lambda\)**, par exemple 0, 0,95 et 1, ce qui mesure directement l'arbitrage biais-variance de la section 10.2 ;
- entre votre méthode de politique **avec** et **sans** critique, c'est-à-dire la mesure de la semaine 8 refaite sur votre tâche.

Le protocole de mesure est celui de la semaine 8 : à chaque mise à jour, vous aplatissez le gradient en un vecteur, vous en calculez la norme, et vous journalisez l'écart-type de cette norme sur une fenêtre glissante. Dites explicitement ce que vous mesurez, parce que la variance d'un gradient est une grandeur qui a plusieurs définitions raisonnables et que la vôtre doit être lisible.

{{% comment %}}SOURCE: source-assets/raw-content/week-08.md §8.6{{% /comment %}}

**Étape 4, la comparaison avec le jalon 2, sur trois axes et pas un.** C'est le cœur du jalon. Vous comparez votre méthode de politique et votre réseau Q profond sur :

- l'**efficacité d'échantillon** : combien d'interactions avec l'environnement pour atteindre votre cible, avec intervalle ;
- la **stabilité** : combien d'exécutions sur vos graines n'ont pas atteint la cible, rapporté séparément de la moyenne, et l'amplitude de votre intervalle ;
- le **temps d'horloge** : combien de secondes pour atteindre la cible, sur le même matériel, avec le matériel indiqué.

Les trois axes peuvent se contredire, et s'ils se contredisent chez vous, **c'est le résultat le plus intéressant de votre rapport**. Vous avez vu au jalon 2 un cas où le débit et le temps pointaient en sens opposé ; vous avez vu en section 10.6 un cas où l'efficacité d'échantillon et le temps d'horloge pointent en sens opposé d'un facteur dix. C'est le genre de constat que je note.

**Étape 5, l'analyse.** Une mesure, une déduction, une conclusion. Trois choses doivent y figurer : au moins un cas où deux de vos trois axes se contredisent, ou la mention explicite qu'il n'y en a pas eu ; le traitement des écarts dont les intervalles se recouvrent, déclarés comme des non-résultats ; et une réponse à la question de la section 10.6, celle de savoir ce qui est rare chez vous.

---

## Livrables, barème et contraintes

| Élément évalué | Forme | Points |
| --- | --- | --- |
| **1.** Méthode de politique complète et correcte : rapport détaché, avantage généralisé en une passe, objectif écrêté, plusieurs époques | carnet Colab, sorties visibles | 4 |
| **2.** Elle **apprend**, montré sur au moins trois graines avec intervalle, cible annoncée depuis une exécution pilote | carnet, une courbe | 3 |
| **3.** Le diagnostic de la semaine : divergence moyenne par époque et fraction d'échantillons écrêtés, avec une phrase de lecture | carnet, une figure | 2 |
| **4.** Analyse de la variance du gradient entre au moins deux configurations, avec la définition de la grandeur mesurée écrite | carnet, une figure plus un paragraphe | 4 |
| **5.** Comparaison avec le réseau Q profond du jalon 2 sur les **trois** axes, mêmes graines, même boucle d'évaluation, matériel indiqué | tableau | 5 |
| **6.** Nombre d'exécutions n'ayant pas atteint la cible, rapporté séparément de la moyenne, pour chaque méthode | tableau ou note | 2 |
| **7.** Analyse critique : une mesure, une déduction, une conclusion ; au moins une contradiction entre deux axes, ou sa mention explicite ; les recouvrements d'intervalles déclarés comme non-résultats | note de 1 à 2 pages | 3 |
| **8.** Reproductibilité : graines listées, hyperparamètres, critère d'arrêt fixé d'avance, matériel, durée totale, et la route choisie | annexe d'une demi-page | 2 |
| **Total** | | **25** |

**Ce qui n'est pas demandé**, et que je ne noterai pas : battre un score particulier, obtenir un facteur d'efficacité donné, implémenter TRPO ou ACKTR, ou tourner sur un banc d'essai de locomotion. Un **résultat nul correctement établi** vaut mieux qu'un écart impressionnant obtenu sur une seule exécution, et il sera noté comme tel.

> [!IMPORTANT]
 **Un conseil de rédaction, et c'est le même qu'aux jalons 1 et 2, avec un ajout qui vient de la section 10.4.** Écrivez votre note comme si vous expliquiez à un collègue ce que vos mesures permettent de conclure et ce qu'elles ne permettent pas. Pas de récit chronologique de vos essais : une mesure, une déduction, une conclusion. Et l'ajout : si quelque chose n'a pas fonctionné chez vous, **écrivez-le, et dites que vous ne savez pas pourquoi si vous ne le savez pas.** La section 10.4 de cette semaine est exactement cela, et c'est la section dont je pense qu'elle vous servira le plus longtemps. Je ne veux pas lire « prometteur mais délicat » ; je veux lire ce que vous avez mesuré, avec quel réglage, et quelles sont les deux ou trois explications que vous n'avez pas pu distinguer.

{{% comment %}}SOURCE: source-assets/raw-content/week-07.md §Jalon 2{{% /comment %}}

---

## Remise

{{< remise cle="jalon-3" >}}
