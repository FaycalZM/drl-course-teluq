---
title: "14.15 Deux axes, un exemple placé sur les deux"
weight: 16
---

## Pourquoi une liste de neuf serait la pire erreur de la semaine

Nous avons maintenant deux classifications sur la table, et je veux consacrer une section entière à ne pas les confondre, parce que c'est la confusion la plus naturelle et la plus coûteuse de la semaine.

**Axe A, l'écart.** Trois types : erreur de pondération, erreur d'ontologie, erreur de portée. Cet axe décrit **en quoi le substitut diffère de ce qu'on voulait**. C'est une propriété de la paire formée par \(P\) et \(T\), et elle est déterminée au moment de la conception, avant qu'aucun agent ne tourne.

**Axe B, le mécanisme d'exploitation.** Six causes : buts partiellement observés, systèmes compliqués, récompenses abstraites, loi de Goodhart, boucles de rétroaction, auto-récompense. Cet axe décrit **par quel moyen un agent tire parti de l'écart**. C'est une propriété de la situation dans laquelle l'agent est placé, et elle dépend de ce dont l'agent est capable.

Les deux axes sont **indépendants**, et cette indépendance n'est pas une élégance formelle : elle a des conséquences concrètes. Un même type d'écart se fait exploiter par des mécanismes différents selon le système. Un même mécanisme exploite des types d'écart différents selon le cas. Et surtout, un cas réel se décrit par **un** type sur l'axe A, éventuellement deux, et par **plusieurs** mécanismes sur l'axe B, simultanément.

> [!WARNING]
 **Trois plus six ne font pas neuf, et voici ce qu'on perd en les additionnant.** Une liste de neuf items suggère qu'on choisit un item et qu'on a fini de diagnostiquer. Or le diagnostic correct d'un cas réel comporte toujours deux parties, et les deux parties se traitent différemment : **le type d'écart dit à qui le problème revient** (un poids à changer, une définition à refaire, une instrumentation à étendre), et **les mécanismes disent ce qu'il faut surveiller** (une perception, une complexité, une fonction apprise, une corrélation, une boucle, un accès au calcul de la récompense). Si vous ne retenez qu'un item de neuf, vous aurez au mieux la moitié du diagnostic et vous ne saurez pas laquelle.

---

## Le tour 3 sur l'axe A : un type, et un second en arrière-plan

Appliquons la grille à notre propre cas, celui de la section 14.8 : le sous-marin parqué à la surface. C'est l'exercice de la semaine, et c'est pour lui que la **Figure 14-4** existe.

**Type principal : l'erreur d'ontologie.** Ce que nous voulions dire par « bien jouer » a été opérationnalisé en « survit et gère son oxygène », parce que c'est ce que la personne a récompensé. Ce sont **deux désidérata différents pour le même concept**, et c'est la définition exacte du type 2. Ce n'est pas un poids mal réglé : on ne corrigerait pas le tour 3 en multipliant la récompense par un coefficient. C'est le choix de ce qui est mesuré qui diffère de ce qu'on voulait.

**Type secondaire : l'erreur de portée.** Le substitut est évalué sur des segments de **cinquante pas**, soit environ trois secondes. Un sauvetage de plongeur demande six collectes puis une remontée, ce qui ne tient pas dans cinquante pas. Le désidérata « sauver des plongeurs » est donc mesuré sur un **domaine restreint dans le temps** où il ne peut pas apparaître, ce qui est la définition du type 3. Autrement dit : même avec un étiquetage parfait, la longueur de segment choisie rendait ce comportement inatteignable.

{{% comment %}}SOURCE: types PAN p.4 ; longueur de segment LAPAN ch.19 p.580 ; critère d'étiquetage LAPAN ch.19 p.587 ; résultat LAPAN ch.19 p.596-597{{% /comment %}}

Notez que ce second point est un diagnostic constructif et non un reproche : il indique une correction précise et bon marché. Allonger les segments coûte du stockage et du temps de lecture pour la personne, et rien d'autre.

---

## Le tour 3 sur l'axe B : quatre mécanismes à la fois

Et maintenant le même cas sur l'autre axe. Quatre des six mécanismes sont présents, et je les prends dans l'ordre de la section 14.10.

**Buts partiellement observés.** Notre modèle \(\hat r\) voit un clip de cinquante images. Il ne voit **jamais le score**, ni le nombre de plongeurs transportés, ni aucune variable interne du jeu. Il note donc une apparence, et nous optimisons cette apparence.

**Récompenses abstraites.** \(\hat r\) est une fonction **apprise** sur un espace de plus de cent mille dimensions, ajustée sur trois cents comparaisons. C'est précisément le cas que la section 14.10 signale comme vulnérable dès qu'il existe une direction où la fonction prend des valeurs anormalement élevées. Et la surface était cette direction.

**Loi de Goodhart.** Remonter à la surface était **réellement corrélé** à bien jouer, sous la politique du modèle de départ : un agent qui remonte survit plus longtemps, donc tire plus, donc marque plus. La corrélation existait et elle était vraie. Elle a été détruite par l'optimisation de la mesure elle-même, ce qui est l'énoncé littéral de la loi.

**Boucles de rétroaction.** La base de segments du tour 1 contient nettement plus de sous-marins en surface que celle du modèle de départ, et la moitié des paires du tour 2 y a été tirée. **La politique a donc choisi ce que la personne allait voir.** C'est une boucle au sens strict du cinquième mécanisme, et c'est la flèche discrète de la Figure 14-1 qui la porte.

{{% comment %}}SOURCE: mécanismes AMODEI p.8-9 ; déplacement de la base LAPAN ch.19 p.595{{% /comment %}}

---

## Deux cases vides, et elles valent autant que les quatre pleines

Deux mécanismes sur six sont **absents**, et le dire est aussi informatif que de nommer les quatre autres, parce que cela montre que la grille discrimine au lieu de tout expliquer.

**L'auto-récompense est absente.** L'agent n'a aucun accès aux poids de \(\hat r\), ni au processus qui calcule la récompense. Il ne peut pas modifier son évaluateur ; il peut seulement se placer là où son évaluateur se trompe. C'est une distinction importante, et elle nous dit où la frontière passe : le sous-marin à la surface **n'est pas** un cas d'auto-récompense, même si le résultat se ressemble.

**Les systèmes compliqués sont absents.** L'agent est un petit acteur-critique convolutif. Il n'a pas la capacité de sortir du cadre du jeu, d'exécuter du code arbitraire ou d'exploiter un défaut de l'émulateur. Il n'a trouvé qu'une stratégie dans l'espace des stratégies du jeu, et c'est tout.

{{% comment %}}SOURCE: AMODEI p.9{{% /comment %}}

La **Figure 14-4** porte cette lecture : les trois types d'écart sur un axe, les six mécanismes sur l'autre, le tour 3 marqué sur une ligne et quatre colonnes, et les deux cases restées visiblement vides.

{{< bookfig src="14-04.png" week="14" >}}

---

## Le même type, d'autres mécanismes : la preuve que les axes sont indépendants

Je ferme la section par la vérification qui établit l'indépendance, parce qu'une affirmation d'indépendance sans contre-exemple reste une affirmation.

Reprenons le cas de l'insertion routière de la section 14.14. Sur l'axe A, c'est **le même type que notre sous-marin** : une erreur d'ontologie, deux définitions de la congestion là où nous avions deux définitions de « bien jouer ».

Sur l'axe B, les mécanismes sont **différents**. On y trouve la loi de Goodhart, comme chez nous, et des buts partiellement observés, parce que le substitut ne mesure la circulation qu'à travers des capteurs de vitesse. Mais il n'y a **pas de récompense abstraite**, puisque le substitut est une formule écrite à la main et non un réseau. Et il n'y a **pas de boucle de rétroaction** sur un étiqueteur humain, puisqu'il n'y a pas d'étiqueteur du tout.

{{% comment %}}SOURCE: PAN p.4, p.6{{% /comment %}}

Deux cas, le même type d'écart, deux ensembles de mécanismes différents. Les axes sont donc bien indépendants, et c'est exactement pour cela que les fusionner en une liste de neuf détruirait de l'information.

---
