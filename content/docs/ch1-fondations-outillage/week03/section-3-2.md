---
title: "3.2 CEM est une méthode de Monte-Carlo"
weight: 3
---

## Un nom nouveau pour une famille connue

Une méthode présentée seule a toujours l'air d'un cas particulier inventé pour l'occasion. CEM n'en est pas un : elle appartient à une famille parfaitement identifiée, celle des méthodes de Monte-Carlo, et montrer la correspondance maintenant vous évitera de la redécouvrir en semaine 8, quand les méthodes de gradient de politique reposeront sur le même principe.

Une **méthode de Monte-Carlo** (*Monte Carlo method*) ne demande que de l'**expérience** : des suites échantillonnées d'états, d'actions et de récompenses, obtenues par interaction réelle ou simulée avec un environnement. Apprendre à partir d'expérience réelle ne suppose **aucune connaissance préalable de la dynamique** de l'environnement, et permet pourtant d'atteindre un comportement optimal. C'est l'axe « sans modèle » de la section précédente, énoncé par le formalisme plutôt que par la pratique. Et lorsqu'un modèle est tout de même utilisé, il suffit qu'il sache engendrer des transitions échantillonnées : nul besoin des distributions de probabilité complètes qu'exigerait une méthode de programmation dynamique.

{{% comment %}}SOURCE: SB ch.5 p.113{{% /comment %}}

La définition tient alors en une ligne : ce sont des façons de résoudre le problème de l'apprentissage par renforcement **en moyennant des retours échantillonnés**. Trois conséquences, toutes visibles dans le code de la section 3.4. La famille est définie pour les **tâches épisodiques** seulement, en supposant que tout épisode finit par se terminer. Les estimations et les politiques ne changent **qu'à l'achèvement d'un épisode** : l'incrément est l'épisode, pas le pas de temps. Et le terme désigne spécifiquement les méthodes fondées sur des retours **complets**, par opposition à celles qui apprennent à partir de retours partiels, dont la semaine 4 fera son affaire.

{{% comment %}}SOURCE: SB ch.5 p.113{{% /comment %}}

---

## La correspondance, critère par critère

| Le critère de la famille | Ce que fait CEM |
| --- | --- |
| de l'expérience seulement, aucune dynamique | sans modèle par construction : le réseau ne voit que des observations |
| moyenner des retours **complets** | chaque épisode est noté par son retour **total** |
| tâches épisodiques uniquement | première limite de la méthode : les épisodes doivent être finis, et de préférence courts |
| mise à jour à l'achèvement de l'épisode | une mise à jour par lot de seize épisodes terminés |

{{% comment %}}SOURCE: SB ch.5 p.113 ; LAPAN ch.4 p.119, p.121-123, p.126, p.135{{% /comment %}}

Il y a une quatrième propriété, et je la formule sans lui donner son nom technique, qui appartient à la semaine 4 : rien, dans CEM, n'estime une valeur à partir d'une **autre estimation**. Chaque chiffre qui entre dans la décision de garder ou de jeter un épisode a été réellement observé, additionné depuis le début de l'épisode jusqu'à sa fin. Le mécanisme qui consiste à estimer à partir d'une estimation existe, il porte un nom, il est l'une des deux grandes idées de ce cours, et vous le rencontrerez la semaine prochaine.

{{% comment %}}SOURCE: summaries/sb/ch05.md §5.1 p.114-118{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur ce que cette correspondance vous achète.** Elle n'est pas décorative. Les trois limites que nous rencontrerons en section 3.5 ne sont pas des défauts de CEM : ce sont les limites de toute la famille, lisibles dès la définition. « Tâches épisodiques » devient « les épisodes doivent finir ». « Moyenner des retours complets » devient « il faut que les retours se distinguent les uns des autres ». Une méthode qui ne sait juger qu'après coup ne peut rien dire d'un épisode dont la récompense ne dit rien. Tout l'échec de la seconde moitié de la semaine est déjà contenu dans ce tableau.
