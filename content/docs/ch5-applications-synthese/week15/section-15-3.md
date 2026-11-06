---
title: "15.3 Un paragraphe"
weight: 4
---

## Quand l'observation est une langue et l'action une phrase

Passons au deuxième problème, et au premier des trois que ce cours n'a pas encore traités. Il s'agit de **fiction interactive** (*interactive fiction*) : un jeu textuel, du genre de ceux où l'on lit une description de pièce et où l'on tape une commande.

L'outil est **TextWorld**, publié en juin 2018 par un laboratoire de recherche industriel. Trois choses le rendent utilisable pour l'apprentissage par renforcement, et chacune mérite d'être nommée. C'est une interface de style Gym, donc familière. C'est un **générateur** de quêtes paramétrable, et non une collection de jeux figés : on lui demande un scénario, un thème, des adjectifs sur les objets, un nombre de quêtes parallèles, une **longueur de quête** et une graine aléatoire. Et il permet de **regarder l'état interne** du jeu, ce qui, nous allons le voir, est la condition pour que quoi que ce soit apprenne. Les expériences dont cette section rapporte les chiffres travaillent à une longueur de quête de **cinq**.

{{% comment %}}SOURCE: LAPAN ch.13 p.390-391{{% /comment %}}

**L'observation est du texte.** Pas une représentation du texte, pas des caractéristiques extraites du texte : du texte, jusqu'à 200 jetons sur un vocabulaire de 1 250 mots. C'est déjà une nouveauté dans ce cours, qui a vu des vecteurs, des images et des tenseurs booléens, mais jamais une séquence de symboles discrets de longueur variable.

Et il y a une seconde nouveauté, plus lourde : l'observation **ne montre pas l'inventaire**. Vous prenez une pomme, la description de la pièce ne change pas, et l'état après avoir pris la pomme est **indiscernable** de l'état d'avant. C'est la définition d'un **PDM partiellement observable**, que la semaine 5 avait posé en passant, et cette fois ce n'est pas une subtilité théorique : c'est une propriété qui rend le problème insoluble sans mémoire ou sans accès à l'état interne.

{{% comment %}}SOURCE: LAPAN ch.13 p.393-394{{% /comment %}}

---

## L'action est produite, et c'est le changement de classe

Voici le point que je veux que vous reteniez de cette section, parce qu'il va revenir à la section 15.9 et parce qu'il est le vrai contenu de la colonne « action » de la semaine.

**L'agent ne choisit pas une action, il la produit.** Une commande est une phrase, jusqu'à huit jetons pris dans le vocabulaire de 1 250. Faites le calcul pour une quête de cinq actions, soit \(5 \times 8 = 40\) jetons à produire dans le bon ordre :

$$
\Pr[\text{séquence correcte}] \;=\; \frac{1}{1250^{40}} \;\approx\; \frac{1}{10^{123}}
$$

{{% comment %}}SOURCE: LAPAN ch.13 p.393 (image){{% /comment %}}

Un sur dix puissance cent vingt-trois. Mettez ce nombre en regard de la semaine 11, où nous avons passé une semaine entière à construire des primes de nouveauté pour qu'un agent trouve un but qu'une politique \(\varepsilon\)-gloutonne ne trouvait pas en deux cents épisodes. Aucune méthode d'exploration n'approche de cet ordre de grandeur. Il n'y a pas d'ingénierie de l'exploration qui sauve ce problème.

**Et une précision que ce cours ajoute, parce qu'elle est nécessaire et qu'elle se perd facilement.** Le nombre \(1250^{40}\) n'est **pas** l'espace d'actions. C'est l'espace des **solutions complètes** à cinq actions. L'espace d'actions **par pas**, celui dans lequel l'agent choisit à chaque tour, est \(1250^{8} \approx 6 \cdot 10^{24}\). Les deux nombres disent deux choses différentes, et il faut les séparer, parce que toute la suite repose sur la réduction du **second**.

{{% comment %}}SOURCE: LAPAN ch.13 p.394 (image){{% /comment %}}

---

## Deux béquilles, et il faut les appeler ainsi

Comment rend-on cela apprenable ? Avec **deux interventions sur l'environnement**, pas sur l'agent. Je les appelle des béquilles, et c'est le mot juste : sans elles, rien n'apprend du tout, et elles ne sont pas des astuces d'implémentation mais des changements de problème.

**Première béquille : les commandes admissibles** (*admissible commands*). L'environnement, interrogé, fournit à chaque état la liste des commandes qui ont un sens à cet endroit. Cette liste compte **une douzaine d'entrées**. L'espace d'actions par pas passe donc de \(6 \cdot 10^{24}\) à une douzaine, c'est-à-dire d'un espace de production à un espace de **choix** : on est revenu à un espace d'actions discret de la taille de ceux des semaines 4 à 8, et un réseau Q profond s'y applique.

**Seconde béquille : la récompense intermédiaire** (*intermediate reward*). La récompense naturelle de la tâche arrive à la fin de la quête, une seule fois. Un réglage de l'environnement la rend dense : \(+1\) à chaque pas qui va dans la bonne direction. C'est, en une ligne de configuration, l'inverse exact du problème que la semaine 11 attaquait avec de l'exploration dirigée.

{{% comment %}}SOURCE: LAPAN ch.13 p.394-395{{% /comment %}}

> [!IMPORTANT]
 **Je veux que vous voyiez ces deux béquilles pour ce qu'elles sont, parce que c'est l'une des leçons les plus transférables de la semaine.** Aucune des deux n'améliore l'agent. Toutes les deux **changent le problème**, et elles le changent en demandant à l'environnement de révéler ce qu'il sait : les coups qui ont un sens, et la direction du but. Dans la vie, un environnement ne sait pas forcément ces choses, et quand il les sait, il ne les donne pas forcément. La question à poser à tout résultat obtenu sur une tâche de ce genre est donc : **quelles informations l'environnement a-t-il fournies en plus de l'observation et de la récompense ?** Si la réponse comprend la liste des coups utiles et la direction du but, le résultat ne porte pas sur le problème que son nom suggère.

Et il faut dire la conséquence inverse, qui est honnête et qui complète la précédente : cette révélation est une **ressource réelle**, disponible dans bien plus de situations qu'on ne le croit. Un simulateur industriel connaît ses actions légales. Un moteur de règles connaît ses coups valides. Un formulaire connaît ses champs remplissables. Avant de construire une exploration dirigée, demandez-vous si votre environnement ne vous donnerait pas la liste d'une douzaine, et faites-le dans cet ordre : c'est beaucoup moins de travail et c'est beaucoup plus efficace.

---

## L'interface qui n'est pas celle de Gymnasium, et c'est le paragraphe le plus réutilisable de la section

Voici maintenant le détail pratique de la section, et je le mets en avant parce qu'il est de ceux qui coûtent une journée à qui ne les a pas lus.

**TextWorld ne respecte pas la convention de Gymnasium**, et plus précisément il ne la respecte plus : à partir de sa version 1.6.1, la dépendance à l'ancienne bibliothèque Gym a été retirée. Trois conséquences concrètes, et elles sont toutes les trois visibles au premier appel.

**Un :** la création d'un environnement ne passe pas par la fonction d'enregistrement habituelle, mais par une fonction propre au paquet, qu'il faut connaître.

**Deux :** les environnements ne déclarent **ni espace d'observations ni espace d'actions**. Les deux valent par défaut « une chaîne de caractères ». Toute pièce de votre code qui interroge `observation_space.shape` ou `action_space.n` tombe.

**Trois, et c'est la plus coûteuse :** la fonction de pas renvoie **quatre** valeurs, sans l'indicateur de troncature que Gymnasium a introduit. Or toutes les enveloppes (*wrappers*) de ce cours, depuis la semaine 1, en attendent cinq. **Vous ne pouvez donc appliquer aucune enveloppe de Gymnasium à cet environnement**, et il faut écrire un **adaptateur** : une pièce qui reçoit les quatre valeurs et en produit cinq, en décidant ce que devient l'indicateur manquant.

{{% comment %}}SOURCE: LAPAN ch.13 p.393{{% /comment %}}

> [!TIP]
 **Pourquoi ce paragraphe est le plus réutilisable de la section, et pourquoi il est dans une semaine de synthèse.** Vous allez rencontrer cette situation à chaque projet sérieux. Un environnement qui vous intéresse existe, il est documenté, il est maintenu, et il implémente une convention **voisine** de celle que votre code attend. Le travail n'est alors pas de l'apprentissage par renforcement du tout : c'est d'écrire une couche d'adaptation, de la tester sur un épisode complet, et de savoir précisément quelles décisions vous avez prises dans cette couche. L'adaptateur de TextWorld est la pièce la plus ennuyeuse du laboratoire de cette semaine, et c'est la seule que vous réécrirez dans votre carrière.

---

## Ce que l'environnement accepte de montrer

Puisque tout repose sur ce que l'environnement révèle, voici la liste complète de ce qu'on peut lui demander en plus de l'observation : la **description de la pièce**, l'**inventaire**, le **nom du lieu**, les **faits du monde**, la **dernière action** et la **dernière commande**, les **commandes admissibles**, et la **suite d'actions gagnante**. Plus le réglage de la récompense intermédiaire déjà mentionné.

{{% comment %}}SOURCE: LAPAN ch.13 p.394{{% /comment %}}

Prenez une seconde sur l'avant-dernière et la dernière entrée de cette liste. L'environnement peut vous donner **la solution**. Cela veut dire que la frontière entre « apprendre à résoudre la tâche » et « imiter la solution fournie » est, ici, un argument booléen. Ce n'est pas un défaut de l'outil, c'est au contraire ce qui en fait un bon outil de recherche. Mais cela veut dire qu'un résultat obtenu sur cet environnement doit toujours être lu avec la liste des champs demandés sous les yeux, et vous verrez à la section 15.9 que cette liste change tout.

---

## Une conséquence d'architecture, et elle réfute la semaine 5

Un dernier point, et je le cite depuis la semaine 5 plutôt que de le reconstruire, parce que ce n'est pas une méthode nouvelle mais une adaptation d'une méthode connue.

La semaine 5 a construit un réseau Q profond avec **une sortie par action** : l'état entre, un vecteur de valeurs sort, une case par action possible, et l'on prend l'argmax. Cette architecture suppose que l'ensemble des actions est **le même à tous les états**, ce qui était vrai de CartPole, de Pong et de tout ce que nous avons fait.

Ici, c'est faux. La liste des commandes admissibles **change d'un état à l'autre**, en contenu et en longueur. Une tête à sortie fixe n'a plus de sens. L'architecture employée prend donc en entrée un **couple** formé de l'observation et d'**une** commande, et produit **une seule** valeur : la valeur de cette commande dans cet état. Chaque commande de la liste est évaluée séparément, et l'on prend le maximum sur la liste.

{{% comment %}}SOURCE: LAPAN ch.13 p.401{{% /comment %}}

C'est, à la lettre, le même algorithme que la semaine 5, avec le même tampon de rejeu, le même réseau cible et la même cible de différence temporelle. Seule la forme de l'entrée a changé, parce que la forme de l'espace d'actions a changé. Je trouve cet exemple excellent pour une raison précise : il montre qu'adapter une méthode à un problème nouveau, ce n'est souvent pas changer la méthode mais **changer l'endroit où l'on coupe entre l'entrée et la sortie**.


---
