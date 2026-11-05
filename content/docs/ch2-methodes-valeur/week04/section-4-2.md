---
title: "4.2 L'équation de Bellman"
weight: 3
---

## Une récurrence, et tout le reste en découle

Voici ma section préférée du cours, et elle demande dix minutes d'attention honnête. Nous allons obtenir, à partir d'absolument rien de neuf, une équation qui relie la valeur d'un état à la valeur de ses successeurs. L'ingrédient unique est la récurrence du retour, établie en semaine 1 : \(G_t = R_{t+1} + \gamma G_{t+1}\). Le retour à partir de l'instant \(t\) est la récompense du pas suivant, plus le retour actualisé à partir de l'instant d'après. Rien de plus.

L'intuition d'abord, avant la dérivation. Si je sais ce que valent tous les états où je peux atterrir au prochain pas, alors je sais ce que vaut l'état où je suis : il suffit de faire la moyenne de « ce que je touche en route plus ce que vaut l'endroit où j'arrive », pondérée par les probabilités de chacun des chemins. La valeur n'est pas calculée d'un coup depuis la fin de l'épisode ; elle se calcule **de proche en proche**. C'est l'image à garder : une valeur se propage comme une rumeur, d'un état à son voisin.

Formellement, la dérivation tient en quatre lignes, et je vous les montre toutes les quatre. C'est le modèle de démonstration de ce cours : je ne vous demande pas de la refaire de mémoire, je vous demande de pouvoir justifier le passage d'une ligne à la suivante.

$$
\begin{aligned}
v_\pi(s) &\defeq \E_\pi\big[G_t \mid S_t = s\big] \\[2pt]
&= \E_\pi\big[R_{t+1} + \gamma G_{t+1} \mid S_t = s\big]
  &&\text{(récurrence du retour)} \\[2pt]
&= \sum_a \pi(a \mid s) \sum_{s'} \sum_r p(s',r \mid s,a)
   \Big[\, r + \gamma\, \E_\pi\big[G_{t+1} \mid S_{t+1} = s'\big] \Big] \\[2pt]
&= \sum_a \pi(a \mid s) \sum_{s',r} p(s',r \mid s,a)
   \big[\, r + \gamma\, v_\pi(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.3 éq. 3.14 p.81{{% /comment %}}

Reprenons ces lignes une par une.

La **première** est la définition, recopiée sans modification.

La **deuxième** applique la récurrence du retour sous l'espérance. C'est le seul pas de calcul de toute la dérivation.

La **troisième** fait le travail. Elle remplace l'espérance par la somme explicite sur tout ce qui peut arriver : l'agent choisit une action \(a\) avec probabilité \(\pi(a \mid s)\), puis l'environnement répond par un couple (état suivant \(s'\), récompense \(r\)) avec probabilité \(p(s',r \mid s,a)\). On somme donc sur les **triplets** \((a, s', r)\), chacun pesé par le produit \(\pi(a \mid s)\, p(s',r \mid s,a)\). C'est la seule ligne qui demande un peu de patience, et c'est la seule qui utilise la dynamique de l'environnement.

La **quatrième** referme la boucle : par définition, \(\E_\pi[G_{t+1} \mid S_{t+1} = s']\) n'est rien d'autre que \(v_\pi(s')\). La valeur réapparaît à droite, et l'équation devient récursive.

C'est l'**équation de Bellman** (*Bellman equation*) pour \(v_\pi\), et voici sa lecture en français : *la valeur de l'état de départ doit être égale à la valeur actualisée de l'état suivant espéré, plus la récompense espérée en chemin*. Lisez cette phrase deux fois. Elle dit qu'une valeur n'est pas une quantité isolée mais une **contrainte de cohérence** entre voisins.

{{% comment %}}SOURCE: SB ch.3 p.81{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur un fait qui n'est pas visible à l'œil nu dans l'équation.** Pour une politique \(\pi\) donnée et un processus de décision markovien fini, \(v_\pi\) est la **solution unique** de son équation de Bellman. Unique : il n'y a pas plusieurs fonctions de valeur cohérentes parmi lesquelles choisir. C'est ce qui transforme l'équation en **méthode** : si vous trouvez, par n'importe quel moyen, une fonction qui satisfait l'équation partout, vous avez trouvé \(v_\pi\), point final. Toute la section 4.4 n'est qu'une façon patiente de converger vers cette solution unique.

{{% comment %}}SOURCE: SB ch.3 p.81{{% /comment %}}

---

## Le diagramme de sauvegarde

Les équations de cette semaine ont toutes la même forme : on regarde en avant d'un pas, on fait une moyenne, on ramène le résultat sur l'état de départ. Il existe une notation graphique pour cette forme, et elle va nous servir cinq fois d'ici la fin du cours. On l'appelle un **diagramme de sauvegarde** (*backup diagram*), parce qu'il dessine le mouvement de l'information : du futur vers le présent, vers l'arrière.

La convention est simple et vaut la peine d'être mémorisée.

- Un **cercle vide** représente un état.
- Un **cercle plein** représente un couple état-action.
- Les flèches descendent vers l'avant dans le temps et la valeur remonte vers la racine.

Un diagramme de sauvegarde n'est pas un graphe de transitions. Il ne cherche pas à décrire l'environnement : il décrit une **opération de mise à jour**. C'est pourquoi un même état peut y apparaître comme son propre successeur : si l'action « foncer dans le mur » laisse l'agent où il est, la flèche revient au même état, et c'est parfaitement licite dans un diagramme de sauvegarde alors que ce serait étrange dans un dessin de l'environnement.

{{% comment %}}SOURCE: SB ch.3 p.81-82{{% /comment %}}

---

## Le monde en grille 5 × 5, résolu

Une équation ne devient convaincante qu'une fois résolue sur un cas concret. Prenons un monde en grille de cinq cases sur cinq. Quatre actions, haut, bas, gauche, droite, toutes déterministes : l'agent se déplace d'une case dans la direction demandée. Deux règles particulières, et ce sont elles qui rendent l'exemple intéressant.

- Une action qui ferait sortir l'agent de la grille **ne le déplace pas** et rapporte **−1**.
- Deux cases spéciales, que j'appellerai A et B, ignorent la direction demandée : depuis A, **toute** action rapporte **+10** et téléporte l'agent en A′ ; depuis B, toute action rapporte **+5** et téléporte en B′.
- Toutes les autres transitions rapportent 0.

Résolvons l'équation de Bellman pour la **politique aléatoire équiprobable**, celle qui tire chacune des quatre actions avec probabilité un quart, avec \(\gamma = 0{,}9\). La **Figure 4-2** montre à gauche les deux dynamiques exceptionnelles, et à droite la table des valeurs obtenue.

{{< bookfig src="04-02.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.3 p.82{{% /comment %}}

Les valeurs vont de **8,8** sur la case A jusqu'à **−2,0** dans le coin inférieur droit. Deux observations méritent qu'on s'y arrête, parce qu'elles montrent que l'équation « comprend » quelque chose que l'œil ne voit pas.

La première : \(v_\pi(A) = 8{,}8\), alors qu'atteindre A rapporte immédiatement **+10**. La valeur est donc **inférieure** à la récompense immédiate. Pourquoi ? Parce que la téléportation dépose l'agent en A′, qui se trouve près du bord ; sous une politique aléatoire, un agent proche du bord passe son temps à se cogner et à encaisser des −1. Le +10 est bien réel, mais ce qui suit le +10 le mange en partie.

La seconde, symétrique : \(v_\pi(B) = 5{,}3\), alors qu'atteindre B ne rapporte que +5. Cette fois B′ est bien placée, loin des bords, et ce qui suit la récompense l'augmente.

{{% comment %}}SOURCE: SB ch.3 p.82{{% /comment %}}

Voilà la leçon : une fonction de valeur n'est pas un barème de récompenses, c'est une évaluation de **position**. Elle sait qu'un gros gain suivi d'une mauvaise position vaut moins qu'un petit gain suivi d'une bonne position. C'est exactement la quantité qui manquait à l'agent de la semaine 3.

Un mot sur la façon dont cette table a été obtenue, parce que c'est la charnière vers la section 4.4. Elle n'a pas été apprise par essais : elle a été calculée en **résolvant le système linéaire** que l'équation de Bellman définit. Vingt-cinq états donnent vingt-cinq équations à vingt-cinq inconnues, et l'algèbre linéaire sait faire. Retenez cette possibilité et retenez aussi qu'elle ne passera pas l'échelle : nous y revenons dans deux sections.

> [!TIP]
 **Une vérification à faire vous-même, elle prend une ligne et elle vaut mieux qu'une relecture.** Dans une telle table, prenez la case centrale, qui porte la valeur **+0,7**, et ses quatre voisines, qui portent **+2,3** (en haut), **+0,4** (à droite), **−0,4** (en bas) et **+0,7** (à gauche). La case centrale n'est au bord de rien et n'est ni A ni B : toutes ses transitions rapportent 0. L'équation de Bellman s'y réduit donc à \(v_\pi(\text{centre}) = \gamma \times \frac{1}{4}\,(2{,}3 + 0{,}4 - 0{,}4 + 0{,}7)\), soit \(0{,}9 \times \frac{3{,}0}{4} = 0{,}675\), que l'arrondi affiche à **0,7**. Vous venez de vérifier une équation de Bellman à la main. Faites-le une fois : plus jamais ensuite vous ne lirez cette formule comme un symbole opaque.

{{% comment %}}SOURCE: SB ch.3 p.82{{% /comment %}}
