---
title: "14.1 Une récompense n'est pas un fait, c'est une spécification"
weight: 2
---

## Trois activités dans un seul nombre, et le piège qui en découle

Posons le cas sur lequel toute la première moitié de la semaine va travailler, parce qu'il est assez petit pour être compris en un paragraphe et assez riche pour contenir le problème entier.

Un jeu d'arcade des années quatre-vingt. Vous pilotez un sous-marin et le jeu vous note sur **trois activités simultanées**. Première activité : tirer sur les poissons et les sous-marins ennemis, ce qui rapporte des points immédiatement. Deuxième activité : récupérer des plongeurs et les ramener à la surface, ce qui rapporte beaucoup plus, mais **seulement après en avoir collecté six et être remonté**. Troisième activité : éviter de se faire toucher, ce qui ne rapporte rien et dont la violation termine l'épisode.

Et par-dessus ces trois activités, une contrainte de ressource : **l'oxygène est limité**. Une jauge en bas de l'écran descend, et si elle atteint zéro le sous-marin meurt. Remonter à la surface la remplit.

{{% comment %}}SOURCE: LAPAN ch.19 p.574{{% /comment %}}

Regardez maintenant ce que ce découpage fait au signal d'apprentissage, et demandez-vous ce qu'un agent peut en tirer.

**Tirer sur les poissons est facile à apprendre.** La récompense arrive au pas suivant le tir, elle est fréquente, et la relation de cause à effet tient dans un pas de temps. Quelques heures d'entraînement suffisent, et notre agent de départ y excellera.

**Sauver un plongeur est presque impossible à apprendre.** Le bonus n'arrive qu'après une séquence longue, structurée et conditionnelle : six collectes, puis une remontée. Un agent qui en collecte cinq et meurt ne reçoit rien ; un agent qui en collecte six et ne remonte pas ne reçoit rien non plus. Le signal est **parcimonieux** (*sparse*) au sens de la semaine 3, et il est parcimonieux d'une manière particulièrement cruelle, parce qu'il faut réussir une conjonction pour recevoir le premier indice qu'elle existe.

**Et la jauge d'oxygène n'est reliée à rien.** C'est le point que je veux que vous reteniez. Rien, absolument rien dans la récompense ne dit à l'agent que sa mort subite a un rapport avec ces quelques pixels en bas de l'écran. Un réseau convolutif n'a aucune notion préalable de ce qu'est une jauge. Il voit une image, il reçoit un nombre, et au moment où il meurt le nombre ne lui apprend que ceci : l'épisode est terminé.

La conséquence est mesurée, et elle est nette : la grande majorité des épisodes d'entraînement plafonnent à **quelques centaines de points et environ cinq cents pas de jeu**, et la cause est toujours la même, l'asphyxie.

{{% comment %}}SOURCE: LAPAN ch.19 p.574{{% /comment %}}

---

## Et une personne qui n'a jamais vu ce jeu comprend les deux en quelques minutes

Voici le contraste qui ouvre la semaine, et il est plus instructif que n'importe quel argument théorique.

Mettez devant ce jeu quelqu'un qui n'y a jamais joué. En quelques minutes, sans qu'on lui explique les règles, cette personne aura compris deux choses que notre agent ne découvrira pas en douze millions de pas : qu'il faut remonter quand la barre du bas devient courte, et qu'amener des plongeurs à la surface rapporte gros.

{{% comment %}}SOURCE: LAPAN ch.19 p.574{{% /comment %}}

Ce n'est pas que cette personne est meilleure en optimisation. C'est qu'elle dispose d'un préalable que l'agent n'a pas : elle sait ce qu'est une jauge, elle sait ce qu'est manquer d'air, et elle sait qu'un personnage qu'on transporte est à sauver. La différence n'est pas dans l'algorithme, elle est dans **ce qui a été spécifié**.

> [!TIP]
 **Le test à vous poser devant toute récompense, et il vaut au-delà de cette semaine.** Pour chaque comportement que vous attendez de l'agent, demandez-vous : **quel pas de temps porte le signal qui l'enseigne, et quelle est sa fréquence ?** Dans le cas du sous-marin, la réponse est « le pas suivant, très souvent » pour le tir, « après une conjonction de sept événements » pour le sauvetage, et « aucun signal, jamais » pour la gestion de l'oxygène. Trois réponses, trois difficultés d'apprentissage radicalement différentes, et un seul nombre pour les porter toutes les trois. Ce test prend trente secondes et il vous dira, avant tout entraînement, quel comportement votre agent n'apprendra pas.

---

## Le cercle vicieux du réglage, et pourquoi ce cours le refuse

Il existe une réponse immédiate à ce problème, et elle est tentante : **ajoutez un bonus d'oxygène**. Donnez un petit quelque chose quand la jauge remonte, une pénalité quand elle descend trop, et l'agent apprendra. C'est le **façonnage de la récompense** (*reward shaping*), et cela marche souvent.

Mais regardez où cela vous mène. Vous avez ajouté un terme pour l'oxygène ; il faudra maintenant choisir son coefficient par rapport aux points de tir. Trop fort, et l'agent passe sa partie à faire des allers-retours vers la surface. Trop faible, et il meurt encore. Vous réglez ; puis vous vous apercevez qu'il ne sauve toujours pas de plongeurs, et vous ajoutez un terme pour cela aussi ; et il faut un nouveau coefficient. **Vous êtes en train d'écrire la solution à la main**, terme par terme, coefficient par coefficient, dans le fichier de l'environnement.

C'est ce que j'appellerai le **cercle vicieux du réglage** : chaque terme ajouté crée un arbitrage à régler, chaque arbitrage réglé révèle un comportement manquant, et le fichier de l'environnement finit par contenir la stratégie que l'agent était censé découvrir.

{{% comment %}}SOURCE: LAPAN ch.19 p.574{{% /comment %}}

Et c'est exactement ce que l'apprentissage par renforcement promettait d'éviter. La promesse de la semaine 1 était : décrivez **le but**, pas la méthode. Si nous devons décrire la méthode dans la récompense, nous avons seulement déplacé le travail d'ingénierie, et nous l'avons déplacé dans l'endroit le plus fragile du système.

> [!WARNING]
 **Je vais contester cette formulation dans la seconde moitié de la semaine, et je préfère vous le dire tout de suite.** La proposition qui suit est celle-ci : apprendre la récompense à partir de jugements humains nous **dispense** du réglage de bas niveau. La première moitié de la semaine va démontrer que c'est en grande partie vrai, et avec peu d'étiquettes. La seconde moitié va démontrer que la formulation est trop forte : le réglage ne disparaît pas, il **se déplace** dans le protocole d'étiquetage, c'est-à-dire dans le choix de ce qu'on montre, de qui juge et selon quel critère. Vous verrez cela très concrètement en section 14.5, où un seul paragraphe de description contient toute la spécification de l'expérience, et en section 14.8, où l'agent exploite exactement ce que ce paragraphe avait laissé ouvert.

---
