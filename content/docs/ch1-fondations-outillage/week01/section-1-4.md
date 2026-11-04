---
title: "1.4 Processus de Markov avec récompense : retour, actualisation, valeur"
weight: 5
---

## Ce que vaut un état, et pourquoi un seul nombre sauve la somme

Deuxième étage. Nous ajoutons **un seul** ingrédient, la récompense ; états, matrice et propriété de Markov restent identiques. Elle s'ajoute sous la forme d'une seconde matrice carrée, celle de la récompense obtenue en passant de \(i\) à \(j\), qu'on peut comprimer en une liste de couples (état, récompense) lorsqu'elle ne dépend que de l'état d'arrivée. Il nous faut aussi un second ingrédient, un seul nombre : le **facteur d'actualisation** (*discount factor*) \(\gamma\), choisi dans \([0, 1]\), bornes incluses.

{{% comment %}}SOURCE: LAPAN ch.1 p.50{{% /comment %}}

---

## Le retour

Le **retour** (*return*) \(G_t\) est la quantité que l'agent cherche à maximiser. Il se définit pour un instant \(t\) donné, à l'intérieur d'un épisode :

$$
G_t \defeq R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^{k} R_{t+k+1}
$$

Lisons cette formule plutôt que de la contempler. Chaque récompense future est multipliée par \(\gamma\) élevé au **nombre de pas qui la sépare de \(t\)** : celle du pas suivant compte pleinement, celle qui arrive dix pas plus tard compte \(\gamma^{10}\) fois moins. Autrement dit, \(\gamma\) mesure **la distance à laquelle nous regardons dans le futur**. À \(\gamma = 1\) l'agent est parfaitement clairvoyant ; à \(\gamma = 0\) seule \(R_{t+1}\) subsiste, c'est la myopie absolue. Ni l'un ni l'autre n'est utilisable tel quel, d'où les valeurs de la pratique, **0,9 ou 0,99** ; \(\gamma = 1\) n'est acceptable que pour des épisodes finis et courts.

{{% comment %}}SOURCE: LAPAN ch.1 p.50-51{{% /comment %}}

---

## Du retour à la valeur d'état

Pourquoi ne pas utiliser simplement \(G_t\) comme mesure de la qualité d'un état ? Posez-vous la question avant de lire la réponse. Parce que \(G_t\) a été défini **pour une chaîne particulière que nous avons observée** : rejouez l'épisode et vous obtiendrez un autre nombre, pour le même état de départ, parfois très différent. Le retour est une variable aléatoire, pas une propriété de l'état. Pour obtenir une propriété de l'état, il faut moyenner sur toutes les chaînes possibles, c'est-à-dire prendre l'espérance. On obtient la **valeur d'état** (*state value*) :

$$
v(s) \defeq \E\!\left[G_t \mid S_t = s\right]
$$

{{% comment %}}SOURCE: LAPAN ch.1 p.51{{% /comment %}}

> [!NOTE]
 **Une remarque de notation, et elle est volontaire.** J'écris ici \(v(s)\) sans indice, alors que vous verrez partout ailleurs \(v_\pi(s)\), la notation définitive du cours ; mais à ce stade nous sommes dans un processus **sans actions**, il n'y a aucune politique, donc rien à mettre en indice. Nous ferons la mise à niveau en section 1.5, dès que \(\pi\) existera.

---

## Le calcul à la main, et le moment où tout casse

Attribuons une récompense à chaque transition de notre graphe à quatre états ; la **Figure 1-4** les porte sur les arêtes. Elles racontent une histoire que vous reconnaîtrez : rester à la maison rapporte 1, partir chercher un café rapporte 1, mais c'est travailler qui paie le mieux, puisque Computer → Computer vaut 5. Être interrompu pour bavarder coûte cher, Computer → Chat valant −3 ; revenir au travail rapporte 2 depuis une conversation et 3 depuis la machine à café ; bavarder en boucle finit par coûter, Chat → Chat valant −1.

{{< bookfig src="01-04.png" week="01" >}}

{{% comment %}}SOURCE: LAPAN ch.1 p.51{{% /comment %}}

Posons \(\gamma = 0\) : le retour se réduit à \(R_{t+1}\), donc la valeur d'un état est la moyenne des récompenses de ses transitions sortantes, pondérée par leurs probabilités. C'est le meilleur exercice au crayon de la semaine, et il tient en quatre lignes.

$$
\begin{aligned}
v(\text{Chat}) &= -1 \times 0{,}5 + 2 \times 0{,}3 + 1 \times 0{,}2 = 0{,}3 \\
v(\text{Coffee}) &= 2 \times 0{,}7 + 1 \times 0{,}1 + 3 \times 0{,}2 = 2{,}1 \\
v(\text{Home}) &= 1 \times 0{,}6 + 1 \times 0{,}4 = 1{,}0 \\
v(\text{Computer}) &= 5 \times 0{,}5 + (-3) \times 0{,}1 + 1 \times 0{,}2 + 2 \times 0{,}2 = 2{,}8
\end{aligned}
$$

{{% comment %}}SOURCE: LAPAN ch.1 p.52{{% /comment %}}

La dernière ligne agrège les quatre transitions sortantes de *Computer*. Conclusion : avec un horizon d'un seul pas, **Computer est l'état le plus précieux**, et c'est cohérent, puisque c'est de là que partent les deux récompenses les plus fortes. Refaisons maintenant le même calcul avec \(\gamma = 1\) : la valeur de chaque état devient **infinie**. La raison est structurelle et non numérique. Le graphe ne contient **aucun état puits**, aucun état sans transition sortante ; on peut donc tourner indéfiniment, et comme toutes les valeurs à court terme que nous venons de calculer sont positives, la somme non actualisée croît sans borne, pour tous les états sans exception.

{{% comment %}}SOURCE: LAPAN ch.1 p.53{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, c'est le pivot de la section :** ce résultat infini **est** la justification de \(\gamma\). On ne l'introduit pas pour satisfaire une intuition économique sur la préférence pour le présent, mais parce que, sans lui, la quantité que l'agent est censé maximiser **n'est pas définie** dans un processus sans fin : \(\gamma < 1\) est ce qui rend la somme convergente et le problème bien posé.

La réciproque est vraie et utile : dans un environnement à horizon fini et court, \(\gamma = 1\) est légitime. Au morpion, une partie dure au maximum neuf coups. Deux remarques encore, à ranger dans un coin. Le **bandit manchot** (*multi-armed bandit*) rencontré en SCI1060 est un processus de décision markovien à un seul pas : on choisit une alternative, on reçoit une récompense, l'épisode s'arrête. Et les valeurs pour un \(\gamma\) intermédiaire **ne se calculent pas à la main** : il y en aurait des centaines à propager. Des méthodes existent et constituent le cœur de la semaine 4 ; cette semaine, nous ne résolvons rien, nous posons le problème.

{{% comment %}}SOURCE: LAPAN ch.1 p.53{{% /comment %}}
