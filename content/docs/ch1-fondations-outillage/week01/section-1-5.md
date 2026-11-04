---
title: "1.5 Du MRP au processus de décision markovien : actions et politique"
weight: 6
---

## Le moment où l'agent prend la main

Troisième et dernier étage. Nous ajoutons les **actions**, et l'agent cesse d'être un spectateur. La différence tient en une phrase, à lire lentement : l'agent **n'observe plus passivement** les transitions d'état, il peut **choisir activement une action** à chaque transition. C'est tout, et c'est aussi tout le cours.

## L'espace d'actions transforme la matrice en pavé

Un **processus de décision markovien** (*Markov decision process*) est un processus de Markov avec récompense auquel on ajoute un **espace d'actions** (*action space*) fini \(\mathcal{A}\). La conséquence est mécanique : les probabilités dépendent désormais de l'action, donc il ne faut plus une matrice mais une pile de matrices, une par action. Un pavé de dimensions \(|\mathcal{S}| \times |\mathcal{S}| \times |\mathcal{A}|\), indexé par l'état de départ \(i\) en hauteur, l'état d'arrivée \(j\) en largeur et l'action \(k\) en profondeur. La **Figure 1-5** montre ce passage de la matrice au pavé mieux que n'importe quelle description.

{{< bookfig src="01-05.png" week="01" >}}

En notation du cours :

$$
p(s' \mid s, a) \defeq \Pr\{S_{t+1} = s' \mid S_t = s,\, A_t = a\}
$$

La matrice de récompense subit le même traitement, et la formulation mérite d'être retenue telle quelle : la récompense dépend désormais non seulement de l'état où l'agent arrive, mais aussi de **l'action qui l'y a conduit**. Nous la noterons \(r(s, a, s')\).

{{% comment %}}SOURCE: LAPAN ch.1 p.53-56{{% /comment %}}

L'exemple qui rend ce pavé concret, et qui introduit la stochasticité, est un robot sur une grille 3 × 3, avec trois actions : tourner à gauche, tourner à droite, avancer. Combien d'états ? Neuf ? Non : l'état doit être autosuffisant pour décrire le futur, et avancer depuis une case ne mène pas au même endroit selon l'orientation. C'est donc le couple (position, orientation), soit \(3 \times 3 \times 4 = \mathbf{36}\) états. Ajoutons la réalité des moteurs imparfaits : le mouvement demandé se produit dans 90 % des cas, et dans 10 % des cas une roue patine et la position reste inchangée. Depuis (1,1) orienté vers le haut, *avancer* mène à (0,1) vers le haut avec probabilité 0,9 et laisse le robot sur place avec probabilité 0,1.

{{% comment %}}SOURCE: LAPAN ch.1 p.55{{% /comment %}}

> [!NOTE]
 **Notez bien cette intuition :** la stochasticité du monde n'est pas une nuisance que nos méthodes devront tolérer, c'est une information rangée **dans le modèle**, à l'intérieur du pavé \(p(s' \mid s, a)\), que l'agent **ne voit jamais**. Ce qu'on peut faire en décidant de l'apprendre explicitement, c'est la semaine 13, celle des modèles du monde.

## La politique

Il reste à nommer l'objet que tout le cours va chercher à construire. Une **politique** (*policy*) est un ensemble de règles qui définit le comportement de l'agent. Quatre politiques pour notre robot, pour voir que l'éventail est large : avancer aveuglément ; contourner les obstacles en vérifiant si le dernier *avancer* a échoué ; tourner systématiquement à droite, ce qui fait tourner le robot en rond ; ou choisir au hasard, ce qui donne un robot ivre. Sur le même processus de décision markovien, elles produisent des retours radicalement différents : voilà pourquoi en trouver une bonne est un problème intéressant.

Formellement, une politique est une **distribution de probabilité sur les actions, pour chaque état** :

$$
\pi(a \mid s) \defeq \Pr\{A_t = a \mid S_t = s\}
$$

Pourquoi une probabilité et non une simple fonction de \(s\) vers \(a\) ? Pour introduire explicitement de l'**aléa** dans le comportement. Et vous savez déjà pourquoi nous en aurons besoin : sans aléa, pas d'exploration. Une politique **déterministe** reste parfaitement représentable, comme le cas particulier où une action a la probabilité 1 et les autres 0.

{{% comment %}}SOURCE: LAPAN ch.1 p.56{{% /comment %}}

## La valeur d'état, mise à niveau : le pont vers la semaine 3

Maintenant que \(\pi\) existe, je tiens la promesse de la section 1.4. La valeur d'un état n'est pas une propriété de l'état seul : elle dépend de ce que l'agent va **faire** ensuite. D'où la notation définitive du cours, où l'indice \(\pi\) et l'espérance \(\E_\pi\) disent la même chose de deux manières, l'espérance étant prise sur les trajectoires engendrées **sous cette politique** :

$$
v_\pi(s) \defeq \E_\pi\!\left[G_t \mid S_t = s\right]
$$

> [!IMPORTANT]
 **Et voici le pont, retenez-le, il est réutilisé dès la semaine 3 :** si la politique est **fixée** et ne change pas, notre processus de décision markovien **redevient un processus de Markov avec récompense**. On réduit en effet le pavé de transition et la matrice de récompense en les moyennant avec les probabilités de la politique, ce qui fait disparaître la dimension des actions : l'étage que nous venons de construire s'effondre proprement d'un cran.

{{% comment %}}SOURCE: LAPAN ch.1 p.56{{% /comment %}}

Cette remarque n'est pas une curiosité : c'est elle qui rend légitime de parler de « la valeur d'un état sous \(\pi\) ». Le \(v(s)\) de la section 1.4 et le \(v_\pi(s)\) de la section 1.5 ne sont pas deux objets différents : le premier est le second, dans le cas où la politique est figée.
