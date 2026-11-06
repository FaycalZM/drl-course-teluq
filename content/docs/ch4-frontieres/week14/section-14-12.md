---
title: "14.12 Trois types d'écart, et un seul exemple pour les trois"
weight: 13
---

## Ce qui est mesuré quand on ne peut pas mesurer ce qui compte

Changeons de grille, et donc d'axe. La section précédente demandait **par quel moyen** un agent exploite une récompense. Celle-ci demande **en quoi** cette récompense diffère de ce qu'on voulait.

Commençons par un exemple du quotidien, parce qu'il installe le vocabulaire sans aucune machinerie. Supposons que ce qui nous intéresse soit le bien-être subjectif des personnes qui utilisent un service de vidéo. C'est difficile à mesurer, cela demanderait de les interroger, et personne ne le fait à l'échelle. On mesure donc ce qui est disponible : le taux de clic et le temps de visionnement. Puis on optimise le temps de visionnement. Et le résultat observé est que la satisfaction des personnes **baisse**.

{{% comment %}}SOURCE: PAN p.1{{% /comment %}}

Nous avons donc deux quantités, et il faut les nommer sans jamais les confondre. Ce cours écrit \(P\) pour la **récompense de substitution** (*proxy reward*), celle qu'on optimise parce qu'elle est disponible, et \(T\) pour la **récompense réelle** (*true reward*), celle qui nous intéresse et qu'on n'optimise pas. La section 14.16 reviendra sur ce que ce second nom suppose, parce qu'il suppose beaucoup.

Le constat qui ouvre cette moitié de semaine est le suivant : ce phénomène a été **largement observé et jamais étudié systématiquement**. Les anecdotes abondent, les mesures manquent. La suite corrige cela sur quatre environnements, **neuf récompenses de substitution** mal spécifiées, et une capacité d'agent qu'on fait varier selon **quatre axes**. Et le résultat global tient en une phrase : les agents plus capables obtiennent souvent un meilleur \(P\) et un plus mauvais \(T\).

{{% comment %}}SOURCE: PAN p.1{{% /comment %}}

---

## Les trois types, sur un même exemple de circulation routière

Les trois types d'écart se distinguent le mieux sur un seul exemple, et je garde celui de la circulation routière pour les trois, parce que changer d'exemple à chaque type est le meilleur moyen de ne pas voir ce qui les sépare.

Le cadre : un réseau routier avec quelques véhicules autonomes parmi un trafic ordinaire, et un objectif qui ressemble à « réduire la congestion sans trop polluer ».

**Type 1 : l'erreur de pondération** (*misweighting*). Le substitut et la récompense réelle portent sur **les mêmes désidérata**, et leur importance relative diffère. On voulait pénaliser l'accélération, parce que l'accélération coûte du carburant et produit des émissions ; on a mis un coefficient trop faible devant ce terme. Rien n'a été oublié, rien n'a été mal défini : un poids est faux. C'est l'écart le plus bénin des trois en apparence, et la section 14.16 montrera que c'est pourtant celui sur lequel un détecteur obtient son meilleur score.

**Type 2 : l'erreur d'ontologie** (*ontological misspecification*). Le substitut et la récompense réelle portent sur **des désidérata différents pour le même concept**. On voulait réduire la congestion. Qu'est-ce que la congestion ? On peut la définir comme une vitesse moyenne basse, ou comme un temps de trajet moyen élevé. Ce sont deux notions différentes du même mot, et elles ne sont pas équivalentes : une vitesse moyenne élevée est compatible avec des trajets très longs pour quelques véhicules. Ici le problème n'est pas un poids, c'est le **choix de l'objet mesuré**.

**Type 3 : l'erreur de portée** (*scope misspecification*). Le substitut porte sur le **bon désidérata**, mesuré sur un **domaine restreint** dans le temps ou dans l'espace. On surveille la vitesse moyenne, mais seulement sur l'autoroute, parce que c'est là que sont les capteurs. Le résultat est prévisible : la congestion est repoussée sur les rues adjacentes, où personne ne mesure, et le substitut s'améliore.

{{% comment %}}SOURCE: PAN p.4{{% /comment %}}

| Type d'écart | Ce qui diffère entre \(P\) et \(T\) | Sur l'exemple routier |
| --- | --- | --- |
| **erreur de pondération** | l'importance relative des mêmes désidérata | la pénalité d'accélération est sous-pondérée, donc les émissions le sont |
| **erreur d'ontologie** | la définition retenue pour un même concept | la congestion mesurée en vitesse moyenne plutôt qu'en temps de trajet |
| **erreur de portée** | le domaine, en temps ou en espace, sur lequel on mesure | la vitesse surveillée sur l'autoroute et non sur les rues adjacentes |

> [!NOTE]
 **Les trois ne se prêtent pas aux mêmes parades, et c'est la raison pratique de les distinguer.** Une erreur de pondération se corrige en changeant un nombre, ce qui est au moins concevable, même si la section 14.13 montrera que l'écart grandit malgré tout. Une erreur d'ontologie demande de redéfinir ce qu'on mesure, c'est-à-dire de refaire le travail de conception, et aucune boucle d'optimisation ne peut y aider. Une erreur de portée demande d'étendre l'instrumentation à des endroits où l'on ne mesure pas, ce qui est souvent un problème de budget ou d'accès plutôt qu'un problème de modélisation. Trois types, trois natures de travail. Quand vous diagnostiquerez un écart dans votre jalon, commencez par dire lequel des trois il est : cela détermine à qui le problème revient.

---

## Le décompte, et la case qui ne s'allume pas

Il est temps de donner les chiffres, parce qu'ils disent quelque chose que les définitions ne disent pas.

Sur les quatre environnements étudiés, **neuf récompenses de substitution** ont été construites : quatre pour la circulation routière, dont deux erreurs de pondération, une erreur d'ontologie et une erreur de portée ; deux pour un modèle de politique sanitaire ; deux pour un jeu d'arcade ; et une pour un régulateur de glycémie.

Sur ces neuf, **cinq produisent effectivement un désalignement**, c'est-à-dire un cas où optimiser \(P\) dégrade \(T\). Et sur ces cinq, **quatre présentent une transition de phase**, c'est-à-dire un changement brusque plutôt qu'une dérive.

{{% comment %}}SOURCE: PAN p.4 (tableau 1){{% /comment %}}

Deux lectures de ces trois nombres, et la seconde est plus intéressante que la première.

**Première lecture : cinq sur neuf, ce n'est pas tout.** Un substitut mal spécifié ne produit pas forcément un désalignement mesurable. Les deux substituts du jeu d'arcade sont d'ailleurs la seule paire où **ni l'un ni l'autre** ne se désaligne, et la section 14.14 expliquera pourquoi, parce que c'est instructif.

**Seconde lecture : quatre transitions sur cinq désalignements.** Quand le désalignement se produit, il se produit le plus souvent **par bascule**. Ce n'est pas une dégradation progressive qu'on pourrait voir venir en surveillant une pente : c'est un seuil. Retenez ce rapport de quatre sur cinq, la section 14.13 va en faire le cœur de son argument, et la section 14.15 vous montrera qu'il a des conséquences directes sur la façon dont on surveille un système déployé.

---
