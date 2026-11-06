---
title: "15.1 Trois objets, quatre problèmes"
weight: 2
---

## Trois questions à poser avant d'ouvrir un éditeur de code

Voici la méthode, et elle est courte. Devant un problème dont personne ne vous a dit s'il relève de l'apprentissage par renforcement, posez trois questions dans cet ordre.

**Qu'est-ce qu'une observation ?** Autrement dit : quelle est la quantité d'information que votre agent reçoit à chaque pas, sous quelle forme, et à quel prix. Un vecteur de dix nombres et une capture d'écran en couleur ne posent pas le même problème ; un paragraphe de texte n'est ni l'un ni l'autre.

**Qu'est-ce qu'une action ?** Combien y en a-t-il, sont-elles discrètes ou continues, ont-elles un **ordre naturel**, et l'agent les choisit-il dans une liste ou les **produit-il** ? Cette dernière distinction va se révéler la plus lourde de conséquences de toute la semaine.

**Quand arrive une récompense ?** À chaque pas, à la fin de l'épisode, ou une seule fois à la toute fin d'une séquence de vingt coups ? Et surtout : **qui l'a écrite ?**

Les trois questions se posent toujours dans cet ordre, et la troisième est la plus importante, pour une raison que la semaine 14 a établie et que cette semaine va mesurer sur quatre cas : **la récompense est la seule des trois qui soit conçue plutôt qu'observée**. Une observation, vous la recevez ; un espace d'actions, vous le découvrez ; une récompense, quelqu'un l'écrit. Et dans les quatre problèmes ci-dessous, c'est la colonne de la récompense qui varie le plus.

---

## Le tableau des quatre problèmes

Voici les quatre problèmes de la semaine, réduits aux trois questions, plus une quatrième ligne qui dit ce qui rend chacun difficile. Lisez-le en colonnes pour comprendre un problème, et en **lignes** pour comprendre la semaine. C'est aussi, en une page, ce que la **Figure 15-1** dessine.

| | **Un marché** | **Un paragraphe** | **Une page rendue** | **Une permutation** |
| --- | --- | --- | --- | --- |
| **Observation** | les \(N\) dernières barres de prix, dix par défaut ; un indicateur de position détenue ; le profit relatif courant. Haut, bas et clôture réécrits en **pourcentages de l'ouverture** {{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}} | **du texte**, jusqu'à 200 jetons sur un vocabulaire de 1 250. L'inventaire **n'est pas montré** : l'état après avoir pris un objet est indiscernable de l'état d'avant. C'est un **PDM partiellement observable** {{% comment %}}SOURCE: LAPAN ch.13 p.393-394{{% /comment %}} | un **dictionnaire** : un énoncé textuel, une capture d'écran en couleur de 160 pixels de large sur 210 de haut, et les éléments de l'arbre DOM avec leurs attributs. Trois angles d'attaque dans une seule observation {{% comment %}}SOURCE: LAPAN ch.14 p.433, p.435{{% /comment %}} | l'**état complet**, aucune observation partielle : un tenseur de 20 sur 24 en codage one-hot, 1 920 octets, plus une forme compacte de 160 octets pour le stockage {{% comment %}}SOURCE: LAPAN ch.21 p.649-651{{% /comment %}} |
| **Action** | trois : ne rien faire, acheter, clôturer. Pas de vente à découvert, pas de positions multiples {{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}} | une **phrase**, jusqu'à 8 jetons, que l'agent **produit** au lieu de la choisir. La liste des **commandes admissibles** ramène le choix à une douzaine par état {{% comment %}}SOURCE: LAPAN ch.13 p.393-394{{% /comment %}} | en principe le clavier entier, la souris libre, la molette. Réduit à une **grille de cellules de 10 pixels** sur la zone active, soit **256 clics discrets** {{% comment %}}SOURCE: LAPAN ch.14 p.437{{% /comment %}} | douze : six faces, deux sens, en **quarts de tour**. Les majuscules tournent dans le sens horaire, les minuscules dans l'autre {{% comment %}}SOURCE: LAPAN ch.21 p.646, p.648{{% /comment %}} |
| **Récompense** | le mouvement de chaque barre pendant la détention, **ou bien** le mouvement entier au moment de clôturer : deux schémas, en points de pourcentage, commission de 0,1 % à l'aller comme au retour {{% comment %}}SOURCE: LAPAN ch.10 p.306, p.314{{% /comment %}} | parcimonieuse, à la fin de la quête, et rendue **dense sur demande** : un réglage de l'environnement donne \(+1\) à chaque pas qui va dans la bonne direction {{% comment %}}SOURCE: LAPAN ch.13 p.394-395{{% /comment %}} | propre à la tâche, et elle **décroît avec le temps d'horloge**. Le même clic correct vaut **0,7936** en 2,07 s avec le navigateur dessiné et **0,9918** en 0,09 s sans interface {{% comment %}}SOURCE: LAPAN ch.14 p.436{{% /comment %}} | \(+1\) sur l'état résolu, \(-1\) partout ailleurs. **Un bit, à la toute fin** {{% comment %}}SOURCE: LAPAN ch.21 p.654{{% /comment %}} |
| **Ce qui le rend difficile** | le signal est minuscule devant un aller-retour qui coûte 0,2 % ; l'agent ne tient au-dessus de \(-0{,}2\) % que pendant quatre heures de marché {{% comment %}}SOURCE: LAPAN ch.10 p.322-323{{% /comment %}} | une exploration au hasard a une probabilité de \(1/1250^{40}\), soit environ \(1/10^{123}\), de tomber sur la bonne suite de jetons {{% comment %}}SOURCE: LAPAN ch.13 p.393{{% /comment %}} | 256 actions, soit **128 fois** l'espace de CartPole ; et l'agent est **sans mémoire**, donc une tâche en deux étapes brise la propriété de Markov {{% comment %}}SOURCE: LAPAN ch.14 p.452{{% /comment %}} | \(4{,}33 \cdot 10^{19}\) états atteignables ; un mois d'entraînement en voit environ **0,0000005 %** {{% comment %}}SOURCE: LAPAN ch.21 p.645, p.656{{% /comment %}} |

{{< bookfig src="15-01.png" week="15" >}}

---

## La ligne qui porte toute la semaine

Relisez le tableau en lignes et regardez où se trouve la variation.

La ligne « observation » varie en **forme** : un vecteur de nombres, du texte, un dictionnaire hétérogène, un tenseur booléen. C'est une variation d'ingénierie, parfois lourde, mais c'est la même question posée quatre fois et elle a quatre réponses de même nature.

La ligne « action » varie en **nature**, et c'est déjà plus intéressant. Trois actions discrètes ; une phrase produite sur un vocabulaire ; un clic dans un espace continu sans ordre naturel ; douze rotations. Le passage du troisième au deuxième cas change la classe du problème, pas seulement sa taille.

Mais c'est la ligne « récompense » qui porte la semaine, et voici pourquoi. **Deux des quatre problèmes ont dû la modifier pour devenir apprenables.** La tâche textuelle a activé une récompense intermédiaire que son environnement savait fabriquer ; le cube a renoncé à l'explorer et **engendre ses données à l'envers**, depuis l'état résolu. Un troisième, le marché, a vu sa récompense **écrite à la main**, et elle a été écrite de deux façons incompatibles entre lesquelles il a fallu trancher. Et le quatrième, la page rendue, a une récompense que personne n'a voulue dépendante de la machine, et qui l'est.

> [!IMPORTANT]
 **Voici la thèse de cette semaine, et vous pouvez la recopier dans votre rapport final.** Des trois objets d'un processus de décision markovien, l'observation et l'action sont des **contraintes du problème** : vous les découvrez, vous les représentez, vous payez le prix de cette représentation. La récompense n'est pas une contrainte, c'est une **décision**, et elle est la seule des trois que vous prenez. C'est pour cela que c'est elle qui varie le plus d'un problème à l'autre, et c'est pour cela que la question « qui a écrit cette récompense » est la première à poser à un système que vous n'avez pas construit.

Il reste une conséquence pratique, et elle est la raison pour laquelle le tableau est en tête de semaine et non en conclusion. Les quatre colonnes ne sont pas quatre études de cas que vous liriez pour la culture. Ce sont **quatre exemples travaillés de la même procédure**, et vos livrables finaux vous demandent d'en produire une cinquième, pour un problème de votre choix. Gardez cette colonne vide en tête pendant les quatre sections qui suivent.

---
