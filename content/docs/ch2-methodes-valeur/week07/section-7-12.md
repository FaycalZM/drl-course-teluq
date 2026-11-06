---
title: "7.12 Le résultat, lu avec scepticisme"
weight: 13
---

## Ce que montrent les courbes d'entraînement

Commençons par les bonnes nouvelles, puisqu'il y en a, et finissons par les mauvaises, puisqu'elles sont plus instructives.

Sur les données d'entraînement, la récompense moyenne croît **lentement mais régulièrement**, et son rythme de progression ralentit après environ **300 000 épisodes**. Les courbes se lisent brutes et lissées par une moyenne mobile simple sur **15 points**, ce qui est une convention raisonnable sur ce genre de signal.

{{% comment %}}SOURCE: LAPAN ch.10 p.319{{% /comment %}}

Deuxième mesure, sur les mêmes données d'entraînement mais avec l'exploration désactivée, \(\varepsilon = 0\) : la même conclusion. L'agent apprend bien à augmenter son profit, et ce n'est pas un artefact de l'exploration aléatoire.

{{% comment %}}SOURCE: LAPAN ch.10 p.320{{% /comment %}}

Troisième mesure, et c'est la plus intéressante des trois : la **longueur des épisodes augmente** après environ 100 000 épisodes. Souvenez-vous du réglage : l'épisode se termine à la première clôture, donc la longueur d'un épisode **est** la durée de détention. Cette courbe dit donc quelque chose de très concret sur le comportement : l'agent apprend que **garder** l'action peut être rentable, et il allonge ses positions. C'est une statistique comportementale, pas une métrique de performance, et c'est exactement le genre de mesure qu'il faut instrumenter quand on veut comprendre un agent plutôt que le classer.

{{% comment %}}SOURCE: LAPAN ch.10 p.320{{% /comment %}}

Quatrième mesure, l'ensemble d'états témoins de la semaine 6 : la valeur que le réseau s'attribue sur ces états **ne cesse de monter**. Le réseau devient de plus en plus optimiste sur ces états à mesure de l'entraînement. Gardez cette phrase, elle va servir dans deux paragraphes.

{{% comment %}}SOURCE: LAPAN ch.10 p.321{{% /comment %}}

---

## Le retournement : l'année jamais vue

Tout ce qui précède a été obtenu sur les **données d'entraînement**. Posons maintenant la seule question qui compte : est-ce que cela fonctionne sur des données jamais vues ?

Non.

Sur l'année tenue à l'écart, la récompense **n'a aucune tendance à la hausse**, et sa version lissée **décroît** à partir de la première heure d'entraînement. Notez la coïncidence temporelle, parce qu'elle est le diagnostic : la récompense de validation commence à se dégrader **au moment même** où la longueur des épisodes d'entraînement se mettait à grandir. L'agent n'apprenait pas à détenir plus longtemps en général, il apprenait à détenir plus longtemps **sur cette année-là**.

{{% comment %}}SOURCE: LAPAN ch.10 p.321{{% /comment %}}

Le diagnostic porte un nom que vous connaissez depuis la semaine 2 : **surapprentissage**. Et il est daté : il commence après environ **un million d'itérations** d'entraînement. Avant cela, pendant les **quatre premières heures**, la récompense de validation reste au-dessus de \(-0{,}2\,\%\), ce qui veut dire que l'agent couvre au moins ses frais.

{{% comment %}}SOURCE: LAPAN ch.10 p.322{{% /comment %}}

Ce seuil de \(-0{,}2\,\%\) est le \(-2\kappa\) de la section 7.10, c'est-à-dire le coût d'un aller-retour. On entend parfois dire qu'un agent qui dépasse ce seuil fait « mieux qu'un singe qui achète et vend au hasard ». C'est exact et c'est très faible, et je préfère vous le dire franchement : **ce point de comparaison ne vaut presque rien**. Il signifie seulement que l'agent ne détruit pas de valeur **plus vite que ses propres frais de transaction**. Ce n'est pas un seuil de rentabilité, c'est un seuil de non-absurdité.

{{% comment %}}SOURCE: LAPAN ch.10 p.322{{% /comment %}}

> [!IMPORTANT]
 **La comparaison qui manque, et c'est une leçon de méthode que j'attends au jalon.** Le point de comparaison qu'un lecteur attend, dans toute étude de rendement, est l'**achat-conservation** (*buy-and-hold*) sur la même période : acheter une action à la première barre, ne rien faire, vendre à la dernière, payer la commission deux fois. Cette stratégie ne demande aucun apprentissage, aucun réseau, aucune heure de processeur graphique, et elle **n'est pas calculée** dans l'étude que nous venons de lire. C'est une lacune, et elle est importante : sur une année où le titre monte de 30 %, un agent qui finit à \(+10\,\%\) a en réalité **détruit** de la valeur par rapport à ne rien faire du tout. Savoir **nommer la comparaison manquante** d'un résultat est une compétence professionnelle, et c'est aussi un exercice de laboratoire honnête et peu coûteux : dix lignes de code.

{{% comment %}}SOURCE: LAPAN ch.10 p.322{{% /comment %}}

Un dernier point de procédure avant les figures, et il explique l'aveu de la fin de section. Les modèles sont sauvegardés sur **deux critères distincts** : lorsque la valeur moyenne sur les états témoins atteint un nouveau maximum, **ou** lorsque la récompense de validation bat son record. Retenez le second : il va coûter cher.

{{% comment %}}SOURCE: LAPAN ch.10 p.322{{% /comment %}}

---

## La commission, qui est tout le résultat

Nous arrivons à la paire de figures la plus instructive de la semaine, et je vous demande de les regarder dans l'ordre.

Pour les produire, on rejoue un modèle sauvegardé sur un fichier de cotations et on trace le **profit cumulé** en pourcentage. Le script de relecture prend le fichier de cotations, le modèle, le nombre de barres (qui doit être le même qu'à l'entraînement, sinon le réseau reçoit une observation de la mauvaise taille), et surtout une option de **commission**. C'est cette option qui rend l'expérience suivante possible.

{{% comment %}}SOURCE: LAPAN ch.10 p.322{{% /comment %}}

{{< bookfig src="07-06.png" week="07" >}}

La **Figure 7-6** porte deux panneaux, avec la commission de 0,1 % par opération activée. À gauche, l'année d'**entraînement** : le profit cumulé monte presque sans interruption jusqu'à environ **+150 %** sur quelque 31 000 barres. C'est un résultat qui a l'air magnifique. À droite, l'année **tenue à l'écart** : la courbe descend de 0 jusqu'à un creux proche de **−80 %** vers la barre 17 000, et termine autour de **−60 %**. Ce n'est pas « un peu moins bon ». C'est une perte massive.

Un mot sur l'expérience elle-même avant de passer à la suite, parce qu'elle contredit ce que la section 7.9 vient d'établir et que vous allez le lire sur les panneaux. L'ajustement porte ici sur l'année **la plus récente** et la période tenue à l'écart est **la plus ancienne** : l'ordre du temps est inversé, exactement celui que je vous ai demandé de ne jamais choisir. Ne lisez donc pas ces deux panneaux comme une validation. Lisez-les comme une **démonstration de surapprentissage** : la courbe de gauche et celle de droite viennent des mêmes poids, et l'écart entre les deux est réel quel que soit le sens dans lequel on a coupé les années. Un protocole correct n'aurait pas sauvé ce modèle ; il aurait simplement rendu le chiffre de gauche inutilisable comme argument, ce qu'il est de toute façon.

{{% comment %}}SOURCE: LAPAN ch.10 p.322, image ; p.323{{% /comment %}}

{{< bookfig src="07-07.png" week="07" >}}

Et maintenant la **Figure 7-7**, qui est la raison d'être de la paire. **Le même modèle**, sur **la même année tenue à l'écart**, avec les **mêmes poids**, et une seule chose changée : la commission est mise à **zéro**. La courbe oscille entre environ \(-10\,\%\) et \(+15\,\%\) pendant les 20 000 premières barres, puis monte pour terminer près de **+48 %**.

{{% comment %}}SOURCE: LAPAN ch.10 p.323, image{{% /comment %}}

Prenez une seconde pour mesurer ce que vous venez de lire. **Environ −60 % avec les frais, environ +48 % sans les frais.** Même politique, même année, mêmes poids, aucune ligne de code d'apprentissage modifiée. Le signe du résultat a changé.

Comment un terme de coût peut-il faire cela ? Par simple accumulation. L'agent négocie **souvent**, et chaque aller-retour coûte 0,2 point. Un agent qui fait cent allers-retours sur l'année paie vingt points de pourcentage de frais ; mille allers-retours en paient deux cents. L'écart entre les deux figures n'est pas une erreur de prédiction : c'est le **coût cumulé de sa propre fréquence de négociation**. La stratégie n'échoue pas parce qu'elle prédit mal, elle échoue parce qu'elle n'est pas assez rentable **par opération** pour payer ses opérations.

{{% comment %}}SOURCE: LAPAN ch.10 p.322-323, images{{% /comment %}}

> [!WARNING]
 **La leçon généralisable, et elle sort entièrement de la finance.** Un terme de coût peut **inverser le signe** d'un résultat sans changer la politique d'un iota. Par conséquent, toute comparaison qui omet le terme de coût mesure **un autre problème** que celui qui vous intéresse. Vous rencontrerez la même structure partout : un agent de recommandation qui ignore le coût d'une sollicitation, un agent de contrôle qui ignore l'usure de l'actionneur, un agent de dialogue qui ignore le coût d'un appel à un modèle. Si votre récompense omet un coût réel, vous optimisez consciencieusement la mauvaise quantité, et vos courbes seront superbes.

Et il faut tenir l'autre moitié de la lecture, parce que la conclusion facile serait de dire « sans commission ça marche ». Il y a des journées de repli, et surtout **la commission n'est pas le seul problème** : notre simulation d'ordres est très primitive et ne tient compte ni de l'écart achat-vente, ni du dérapage à l'exécution. Le résultat à commission nulle n'est donc pas un résultat « propre » : c'est un résultat auquel il manque simplement un coût de moins.

{{% comment %}}SOURCE: LAPAN ch.10 p.323{{% /comment %}}

---

## Choisir sur la validation, et pourquoi c'est tricher

Reste une tentation, et elle est forte : parmi tous les modèles sauvegardés, prendre celui qui a obtenu la **meilleure récompense de validation**. Faisons-le, et regardons les chiffres, parce qu'ils sont éloquents.

Avec ce modèle choisi au mieux, et la commission activée : sur l'année d'entraînement, le profit cumulé termine autour de **+33 %**, après un pic voisin de **+55 %**. Et sur l'année tenue à l'écart, la courbe passe par un creux près de **−38 %** et termine autour de **−10 %**. Autrement dit : même en choisissant le meilleur modèle d'après les données de validation, l'agent **perd de l'argent hors échantillon** dès qu'on compte les frais.

{{% comment %}}SOURCE: LAPAN ch.10 p.323, image{{% /comment %}}

Et il y a pire, du point de vue méthodologique. Choisir le modèle d'après ses résultats de validation, c'est **tricher** : en utilisant les résultats de validation pour sélectionner, on **ruine l'idée même de validation**. Il ne reste plus aucun jeu de données capable de dire ce que ce modèle fera sur des données nouvelles. Tout ce que ces courbes peuvent établir, c'est qu'il **existe** des modèles qui se comportent à peu près correctement sur des données qu'ils n'ont pas vues ; elles ne disent pas comment en trouver un.

{{% comment %}}SOURCE: LAPAN ch.10 p.324{{% /comment %}}

C'est exactement l'argument du troisième bloc de la section 7.9, et vous voyez maintenant pourquoi je l'avais annoncé. La règle propre, celle que je vous demande d'appliquer au jalon 2 et dans tout travail ultérieur, tient en une phrase : **on sélectionne sur la validation, on rapporte sur un bloc de test qui n'a jamais servi à sélectionner.**

Dernier résultat, et sa modestie est exemplaire. Le modèle à convolution, qui travaille sur la représentation en matrice, permet d'agrandir la fenêtre de contexte sans faire exploser la taille du réseau, puisque les filtres sont partagés : la valeur par défaut passe de 10 à **50 barres**. Résultat : une dynamique d'entraînement **presque identique**, une récompense de validation **légèrement supérieure**, et un surapprentissage qui **commence plus tard**. Voilà exactement la taille de conclusion que ces données autorisent. Ni plus, ni moins. Si votre rapport de jalon contient des conclusions de cette forme, vous aurez bien travaillé.

{{% comment %}}SOURCE: LAPAN ch.10 p.324{{% /comment %}}

---
