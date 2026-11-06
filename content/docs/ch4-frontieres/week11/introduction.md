---
title: "Introduction"
weight: 1
---

## La récompense que votre agent ne verra jamais

Bonjour à toutes et à tous ! Nous ouvrons aujourd'hui le module 4, et je veux le commencer par un aveu sur les dix semaines qui précèdent : toutes nos méthodes ont exploré **par accident**.

Faites le compte avec moi. Depuis la semaine 4, nos méthodes de valeur jouent une action au hasard avec probabilité \(\varepsilon\), et ce \(\varepsilon\) décroît selon un calendrier écrit à la main. La semaine 6 a remplacé ce calendrier par du bruit appris sur les poids. La semaine 8 a posé une prime d'entropie à côté d'une perte pour empêcher une distribution de s'effondrer sur une seule action. La semaine 9 a ajouté du bruit à une action continue, avec une amplitude réglée à la main. La semaine 10 a déplacé la même entropie dans l'objectif lui-même. Cinq mécanismes, cinq semaines, et un point commun qu'aucune de ces semaines n'a nommé : **aucun d'entre eux ne décide où aller**. Ils perturbent une action autour de ce que l'agent fait déjà, et ils espèrent.

Tant que la récompense est dense, cela suffit. Un pendule mal orienté paie moins qu'un pendule bien orienté, à chaque pas, dès le premier épisode : le signal est partout, et il suffit de le suivre. C'est pourquoi les dix premières semaines de ce cours n'ont jamais eu à poser la question de l'exploration autrement que comme un réglage.

Maintenant, changez la tâche. Supposez une **récompense parcimonieuse** (*sparse reward*), c'est-à-dire une tâche où l'agent ne reçoit quelque chose d'intéressant qu'au terme d'une longue séquence d'actions correctes. Deux régimes sont alors possibles, et le second est celui qui m'intéresse cette semaine. Dans le premier, l'agent rencontre la récompense positive rarement, une fois toutes les quelques dizaines d'épisodes : l'apprentissage est lent, mais il a lieu. Dans le second, l'agent ne la rencontre **jamais**.

{{% comment %}}SOURCE: LAPAN ch.18 p.548-549{{% /comment %}}

> [!IMPORTANT]
 **Voici la phrase charnière de la semaine, et elle met en jeu tout ce que le cours a construit jusqu'ici.** Si votre agent ne voit jamais une bonne récompense, vous pouvez disposer de la méthode d'apprentissage par renforcement la plus efficace du domaine : la seule chose qu'elle apprendra est qu'il n'existe aucun moyen d'obtenir une bonne récompense. Sans bons échantillons, il n'y a rien à apprendre, et le choix de la méthode **cesse d'avoir une importance**. C'est la seule situation de ce cours où le soin apporté à l'algorithme ne rachète rien du tout, et ce n'est pas un cas de laboratoire : c'est le régime d'un grand nombre de problèmes qui nous intéressent en pratique.

{{% comment %}}SOURCE: LAPAN ch.18 p.549{{% /comment %}}

Je vous demande de mesurer la différence avec les quatre semaines précédentes. Les semaines 8 à 10 comparaient des méthodes entre elles, et la question était toujours « laquelle apprend le mieux ». Cette semaine, la question est antérieure : **y a-t-il quelque chose à apprendre dans les données que l'agent produit ?** Aucune perte, aucun gradient, aucune région de confiance ne répond à celle-là.

Et une précision qui évite un contresens : l'exploration ne sert pas seulement les tâches à récompense parcimonieuse. Même avec une récompense dense, une meilleure exploration donne une convergence plus rapide et un entraînement plus stable, pour une raison simple : l'échantillon est plus varié, donc moins corrélé, et nous savons depuis la semaine 5 ce que la corrélation des données coûte. L'exploration est donc une amélioration partout, et une **condition de possibilité** là où la récompense est rare.

{{% comment %}}SOURCE: LAPAN ch.18 p.549{{% /comment %}}

Reste à dire ce qu'est une bonne exploration, et je vais le faire par la négative, parce que c'est la définition la plus utile que je connaisse. L'**exploration efficace** (*effective exploration*) est celle où l'agent **ne perd pas de temps** dans des états qu'il a déjà vus et qui lui sont familiers. Au lieu de reprendre les mêmes actions encore et encore, il doit chercher une expérience **nouvelle**. Retenez cette formulation : elle ne parle ni de hasard ni de probabilité, elle parle de nouveauté, et c'est exactement ce qui va distinguer les méthodes de cette semaine de l'\(\varepsilon\)-glouton.

{{% comment %}}SOURCE: LAPAN ch.18 p.549{{% /comment %}}

> [!NOTE]
 **Une limite que je préfère énoncer tout de suite.** Il existe une définition formelle de l'efficacité d'une exploration, avec des bornes et des garanties, et **elle est hors de portée de ce cours**. Je ne peux pas vous en donner un énoncé qui tienne la rigueur que les autres sections ont reçue, et je ne vais pas vous en servir une version diluée qui vous laisserait croire que vous la maîtrisez. Ce que je vous donne à la place est entièrement vérifiable : une définition par la négative, une mesure, trois familles de méthodes et sept résultats chiffrés. Je reviendrai sur cette limite en section 11.3, à l'endroit exact où elle mord.

---

## Ce que vous allez lire, et pourquoi la semaine se termine par un renversement

Voici la colonne vertébrale, une phrase par section, et un avertissement à la fin que je préfère vous donner maintenant plutôt que dans vingt pages.

La section 11.1 instruit le procès de l'\(\varepsilon\)-glouton. Deux accusations circulent contre lui ; la première est fausse et je vous montrerai pourquoi en une équation, la seconde est la bonne et elle organise toute la semaine : le défaut de l'\(\varepsilon\)-glouton n'est pas d'être aléatoire, c'est d'être **incohérent**. La section 11.2 mesure ce défaut sur une rivière à six états, et trois nombres y suffisent. La section 11.3 présente les trois familles de méthodes qui répondent au problème, et une image les sépare par leur **point d'attache**. La section 11.4 pose la question que ces trois familles évitent, et c'est une question que je prends à mon compte : qu'est-ce qu'une récompense fabriquée par l'agent fait au problème que l'agent est censé résoudre ? La section 11.5 installe la tâche de mesure, une voiture au fond d'une vallée, et y constate l'échec **complet** de notre méthode de référence. La section 11.6 donne six mesures sur cette tâche, reconstruit le tableau de comparaison et en tire deux observations réutilisables. Et la section 11.7 renverse le classement.

> [!WARNING]
 **Lisez la section 11.7, et ne vous arrêtez pas à la section 11.6.** Les quatre dernières semaines vous ont habitués à une progression : chaque méthode battait la précédente, et le tableau de fin de semaine donnait un gagnant. Cette semaine ne se termine pas ainsi. Sur la tâche de la section 11.6, l'\(\varepsilon\)-glouton est la plus mauvaise des six configurations mesurées, et de très loin, puisqu'il ne trouve même pas le but. Sur la tâche de la section 11.7, c'est la **meilleure** des méthodes essayées. Les deux mesures sont justes toutes les deux. Je ne vais pas adoucir cette contradiction, parce qu'elle est la chose la plus utile que cette semaine a à vous apprendre : la conclusion honnête d'une comparaison est parfois que la comparaison était **locale**.

{{% comment %}}SOURCE: LAPAN ch.18 p.569{{% /comment %}}

---

## Deux mots que je vous demande d'adopter, et quatre symboles à surveiller

Cette semaine introduit peu d'équations, six en tout, et c'est fidèle au sujet : l'essentiel de l'exploration est une question de conception et de mesure, pas de formule. En revanche elle introduit deux mots que je vais employer sans arrêt, et quatre symboles dont trois pourraient entrer en collision avec des symboles déjà pris.

**Premier mot, et c'est l'opposition centrale de la semaine.** Une exploration est **non dirigée** (*undirected exploration*) quand l'agent se contente d'espérer que le hasard lui apporte quelque chose de nouveau : il ne cherche pas, il tire au sort. Une exploration est **dirigée** (*directed exploration*) quand une quantité, dans l'agent, pousse activement vers ce qui n'a pas encore été vu. L'\(\varepsilon\)-glouton est non dirigé ; les trois familles de la section 11.3 sont dirigées, chacune à sa façon. Je coine ce couple ici et je m'y tiendrai jusqu'au bout de la semaine.

**Deuxième mot, et il est double.** La **récompense extrinsèque** (*extrinsic reward*) est celle que l'environnement donne : c'est la seule récompense que ce cours a connue jusqu'ici. La **récompense intrinsèque** (*intrinsic reward*) est celle que l'agent se donne à lui-même, à partir de ce qu'il sait de son propre passé. Je les écris \(R^e_t\) et \(R^i_t\), avec l'exposant en haut pour laisser l'indice au temps.

**Le coefficient de la prime s'écrit \(c\), et ce n'est ni \(\alpha\) ni \(\beta\).** Le poids de la récompense intrinsèque dans la récompense totale est un hyperparamètre, et je l'écris \(c\) pour éviter deux collisions désagréables : \(\alpha\) est le pas d'apprentissage depuis la semaine 3, et \(\beta\) est le coefficient de la prime d'entropie depuis la semaine 8. Les trois apparaîtront dans la même section en 11.6.

**Le comptage s'écrit \(\tilde N(s)\), avec un tilde, et le tilde a un sens.** \(\tilde N(s)\) est le nombre de fois que l'agent a vu l'état \(s\), ou une estimation de ce nombre quand on ne peut pas le compter exactement. Le tilde vous rappelle que ce n'est pas forcément un compteur entier : la section 11.3 en donnera une version approchée.

**Et \(\rho\), qui prend cette semaine son troisième sens dans ce cours.** La page « Notation » écrit \(\rho_{t:T-1}\) pour un rapport d'échantillonnage préférentiel depuis la semaine 3, et la semaine 10 a employé \(\rho\) pour une fréquence de visite actualisée des états. En section 11.3, et seulement là, \(\rho(s)\) désignera un **modèle de densité**, c'est-à-dire la vraisemblance que ce modèle attribue à l'état \(s\). Trois sens pour une lettre, c'est un de trop : je nommerai donc cet objet en français partout où la phrase le permet, et je n'écrirai \(\rho(s)\) que dans l'équation elle-même.

> [!TIP]
 **Un rappel de lecture qui vous servira dans toute la section 11.6.** Quand une méthode d'exploration ajoute une récompense à celle de l'environnement, la récompense **affichée pendant l'entraînement** n'est plus celle de la tâche : elle est gonflée par la prime. Seule la récompense mesurée en évaluation, sur un environnement sans prime, est à l'échelle du problème d'origine. Si vous ne retenez qu'une chose de la section 11.4, retenez celle-là, parce qu'elle décide ce que vous avez le droit de comparer à quoi.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Expliquer pourquoi l'exploration décide si un apprentissage est **possible**, et pas seulement s'il est rapide, et énoncer la phrase charnière qui le dit.
- Définir une exploration efficace **par la négative**, et dire pourquoi cette définition parle de nouveauté et non de hasard.
- Distinguer une exploration **non dirigée** d'une exploration **dirigée**, et classer les cinq mécanismes employés dans les semaines 4 à 10.
- Dire, en une équation, pourquoi les actions aléatoires d'une politique \(\varepsilon\)-gloutonne **ne biaisent pas** la cible du Q-learning à un pas, et nommer la propriété de la méthode qui le garantit.
- Dire dans quel cas, exactement, ce biais **existe** réellement, et de quelle semaine antérieure du cours il vient.
- Énoncer le vrai défaut de l'\(\varepsilon\)-glouton en une phrase, et expliquer pourquoi il interdit une séquence d'actions coordonnées.
- Décrire la structure de la rivière à six états, dire quelle action réussit toujours et laquelle échoue le plus souvent, et expliquer pourquoi cette asymétrie suffit à bloquer un agent aléatoire.
- Lire trois comptages de visites, dire en quelle **unité** ils sont exprimés, et vérifier cette unité par une addition.
- Nommer les trois familles de méthodes d'exploration dirigée et dire, pour chacune, **où** elle injecte sa pression.
- Expliquer en quoi les réseaux bruités de la semaine 6 constituent une exploration dirigée, et nommer les deux propriétés du bruit qui le justifient.
- Écrire la prime fondée sur un comptage de visites, dire ce que chacun de ses deux symboles désigne, et expliquer pourquoi la prime décroît.
- Expliquer ce qu'un hachage des états rend possible, et ce qu'un arrondi à trois décimales décide à votre place.
- Énoncer l'idée du pseudo-comptage, et dire pourquoi ce cours vous le présente comme une **esquisse**.
- Expliquer ce que mesure l'erreur de prédiction d'un réseau entraîné à imiter un réseau aléatoire figé, et pourquoi un réseau figé suffit.
- Énoncer la conséquence qu'une prime ajoutée dans une enveloppe a sur le **problème** résolu, et dire à quelles deux conditions, accidentelles, elle reste tolérable.
- Dire pourquoi une courbe d'entraînement et une courbe d'évaluation ne sont pas comparables dès qu'une prime est active.
- Décrire la tâche de la voiture dans la vallée, son espace d'observation, son espace d'actions, sa récompense et sa troncature, et dire pourquoi elle est difficile du point de vue de l'exploration.
- Rapporter le résultat de la méthode de référence sur cette tâche, et dire pourquoi son échec est **permanent** et non seulement lent.
- Énoncer les trois raisons de passer d'une méthode de valeur à une méthode de politique quand la récompense est modifiée en cours d'entraînement.
- Dire à quelle fréquence le bruit d'un réseau bruité est retiré dans une méthode hors politique, à quelle fréquence dans une méthode sur politique, et pourquoi les deux diffèrent.
- Lire un tableau de six mesures : distinguer « a trouvé le but » de « a résolu la tâche », repérer une ligne exprimée dans une autre unité que ses voisines, et dire combien d'exécutions ont résolu la tâche et par quelle famille.
- Énoncer le renversement de la section 11.7 et ce qu'il interdit de conclure d'un classement de méthodes d'exploration.
- Nommer ce que cette semaine ne couvre pas, et dire pourquoi un cours honnête nomme ses lacunes au lieu de les contourner.

---

## Prérequis et outils

De la **semaine 4**, la politique \(\varepsilon\)-gloutonne et le calendrier de décroissance de \(\varepsilon\) : c'est l'objet du procès de la section 11.1. De la **semaine 6**, deux choses qui reviennent intactes et que je ne redériverai pas : les **réseaux bruités** de la section 6.9, avec leur bruit gaussien factorisé et leur couche `CoucheBruitee`, et la cible à \(n\) étapes de la section 6.6, qui est exactement l'endroit où l'accusation de la section 11.1 devient vraie. De la **semaine 5**, la cible du Q-learning avec réseau cible, qui tient toute la réfutation de la section 11.1. De la **semaine 8**, la prime d'entropie et son coefficient. De la **semaine 10**, PPO : la section 11.6 l'emploie comme véhicule de mesure et **ne le réexplique pas**, donc gardez la section 10.2 à portée de main. De la **semaine 7**, enfin, le protocole de mesure à graines multiples avec intervalle, obligatoire depuis le jalon 2 et donc obligatoire dans le laboratoire de cette semaine sans que je le redemande.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les trois volets du laboratoire ; la tâche est bon marché et aucun volet ne demande de processeur graphique |
| **Gymnasium** | `MountainCar-v0` pour toutes les mesures du laboratoire, et une enveloppe maison pour la prime |
| **PyTorch** | la couche bruitée de la semaine 6, deux petits réseaux pour la distillation, et `requires_grad_(False)` sur le réseau figé |
| **NumPy** | le hachage des observations et l'arithmétique de la prime |
| **Python standard** | `collections.Counter`, qui est tout l'outillage nécessaire au comptage d'états |
| **Matplotlib** | les courbes du laboratoire, et la figure « temps jusqu'au but » que vous reproduirez à votre échelle |
| **TensorBoard** | le compteur d'atteintes du but et la position maximale par épisode, qui sont les deux diagnostics propres à cette semaine |
| **Stable-Baselines3** | la solution courte du volet A, pour disposer d'une référence que vous n'avez pas écrite vous-même |
| **Page « Notation » du cours** | le troisième sens de \(\rho\) et la séparation de \(c\), \(\alpha\) et \(\beta\) y sont tranchés |
| **Page « Glossaire » du cours** | une vingtaine de termes nouveaux, dont le couple dirigé / non dirigé |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 11{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

> [!NOTE]
 **Cette semaine ne porte aucun jalon, et c'est voulu.** Le jalon 3 s'est fermé la semaine dernière avec le module 3, et le jalon 4 vous attend en semaine 14. Le laboratoire de cette semaine est donc **formatif** : rien n'y est noté. Profitez-en pour faire quelque chose que les semaines à jalon rendent difficile, c'est-à-dire laisser une exécution échouer et regarder **comment** elle échoue. Le volet A est exactement cela : une méthode qui ne trouve jamais le but, et un instrument qui vous le montre.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---
