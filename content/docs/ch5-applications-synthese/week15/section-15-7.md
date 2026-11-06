---
title: "15.7 Quatre résultats négatifs derrière nous, et deux de plus ici"
weight: 8
---

## Pourquoi cette section arrive comme un patron et non comme une surprise

Faisons l'inventaire avant d'ajouter quoi que ce soit, parce que c'est l'inventaire qui donne son sens à cette section.

La **semaine 10** a rapporté une méthode d'optimisation du second ordre qui, dans la mise en œuvre mesurée, ne battait pas ses concurrentes plus simples, avec deux explications candidates que rien ne permettait de séparer. La **semaine 11** a établi qu'un classement de méthodes d'exploration **ne se transfère pas** d'un environnement à un autre, après quatre semaines pendant lesquelles chaque méthode battait la précédente. La **semaine 12** a rapporté un entraînement de quinze heures dont les deux meilleurs modèles étaient les points de contrôle numéro dix et numéro quinze sur près de deux cents. La **semaine 13** a montré une courbe de désapprentissage qui persiste quand on multiplie le jeu de données par mille.

Quatre semaines, quatre résultats négatifs, et chacun rapporté avec son protocole. En voici deux de plus, et ils sont les plus intéressants des six.

> [!IMPORTANT]
 **L'énoncé que ces six cas établissent ensemble, et c'est la phrase la plus utile de cette semaine pour votre rapport final.** Un résultat négatif **rapporté avec précision** vaut plus qu'un résultat positif **rapporté vaguement**. Ce n'est pas une consolation pour les expériences qui échouent : c'est une description de ce qui est utilisable. Un résultat négatif accompagné de sa configuration, de son matériel, de son temps de calcul et de ce qui reste inexpliqué permet à quelqu'un d'autre de décider s'il doit essayer. Un résultat positif sans intervalle, sans graines et sans protocole ne permet rien du tout, pas même de savoir s'il se reproduira sur la machine de son auteur la semaine suivante.

---

## Le cinquième : une reproduction qui a échoué, rapportée en entier

Voici le cinquième, un **échec de reproduction** (*failed reproduction*), et c'est la dernière mesure que ce cours vous montrera. Je la donne en entier, avec ses chiffres, parce que c'est précisément sa complétude qui la rend utile.

**Ce qui a été tenté.** Reproduire le résultat publié du solveur de cube de la section 15.5. Et le premier obstacle est à lui seul une leçon : la publication **ne donnait pas d'informations sur des aspects très importants de la méthode**, à savoir les hyperparamètres d'entraînement, la profondeur de brouillage employée pendant l'entraînement, et la convergence obtenue. Il a donc fallu chercher les hyperparamètres.

{{% comment %}}SOURCE: LAPAN ch.21 p.666{{% /comment %}}

**Ce qui a été obtenu, d'abord.** Des résultats **très différents** des résultats publiés, et un constat de nature : la convergence de la méthode d'origine est **très instable**. Même avec un petit pas d'apprentissage et de grands lots, l'entraînement finit par **diverger**, la composante de perte sur la valeur **croissant exponentiellement**.

La **Figure 15-5** est la photographie de ce phénomène, et je vous demande de la lire attentivement parce qu'elle est le portrait d'un défaut précis. À gauche, la perte sur la politique : elle descend de 0,08 à 0,04 en une heure et demie, ce qui a l'air d'un apprentissage normal, puis **remonte au-dessus de 0,10**. À droite, la perte sur la valeur : elle reste à peu près nulle pendant **deux heures**, ce qui a l'air parfait, puis part **verticalement au-delà de 400**.

{{< bookfig src="15-05.png" week="15" >}}

{{% comment %}}SOURCE: LAPAN ch.21 p.666-667 (image){{% /comment %}}

**Le diagnostic, et c'est pour lui que la notation de la section 15.5 a été posée.** Relisez l'équation 15-E1 :

$$
y_v(s) \;=\; \max_{a} \Big( v\big(\mathcal{T}(s,a)\big) \,+\, R\big(\mathcal{T}(s,a)\big) \Big)
$$

La valeur prédite par le réseau est **toujours** ajoutée à l'indicateur de but, **y compris lorsque l'état atteint est l'état résolu**. Or l'état résolu est le seul endroit de tout l'espace où la valeur est connue : elle devrait valoir quelque chose de fixe, puisqu'il n'y a plus rien à faire. En l'additionnant à son tour à une prédiction du réseau, on retire cette ancre. Et sans ancre, **rien ne fixe l'échelle de la fonction de valeur** : les valeurs renvoyées par le réseau peuvent valoir n'importe quoi, \(-100\), un million, ou trois virgule quatorze, sans que la perte s'en aperçoive, puisque seule leur **différence** entre deux enfants décide de l'argmax. Avec un objectif quadratique moyen par-dessus, c'est une situation intenable pour un entraînement.

{{% comment %}}SOURCE: LAPAN ch.21 p.667 (image){{% /comment %}}

> [!NOTE]
 **Vous avez déjà vu ce mécanisme, et c'était en semaine 14.** La semaine 14 a montré une perte de modèle de récompense **invariante par décalage additif** : elle ne contraignait que la différence de deux sommes, donc la récompense n'était déterminée qu'à une constante près. C'est le même défaut, sur un autre objet. Une fonction apprise dont l'objectif ne contraint que des **différences** n'a pas de niveau, et une valeur sans niveau diverge dès que quelque chose, dans la chaîne, se met à récompenser la croissance. Le réflexe à retenir : devant une perte qui ne regarde que des écarts, **cherchez l'ancre**, et si vous n'en trouvez pas, posez-la vous-même.

**Le correctif, et il tient en une ligne.** Il suffit de forcer la cible à **zéro sur l'état but** :

$$
y_v(s) \;=\;
\begin{cases}
\max_{a} \Big( v\big(\mathcal{T}(s,a)\big) + R\big(\mathcal{T}(s,a)\big) \Big) & \text{si } s \text{ n'est pas l'état résolu} \\[4pt]
0 & \text{si } s \text{ est l'état résolu}
\end{cases}
$$

{{% comment %}}SOURCE: LAPAN ch.21 p.667 (image){{% /comment %}}

Dans le code de la section 15.5, cela fait deux lignes de plus, et je les écris parce que la double lecture de cette semaine est précisément celle-là : une équation, son code, et la différence d'une ligne entre une divergence et une convergence.

```python
        total = v_enfants + r_enfants
        y_v, y_p = total.max(dim=1)

        if ancrer_le_but:
            # y_v = 0 sur l'etat resolu : c'est la seule valeur connue de l'espace,
            # et c'est elle qui fixe l'echelle de toute la fonction de valeur.
            y_v = torch.where(est_resolu(etats), torch.zeros_like(y_v), y_v)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(y_v(s) = 0\) si \(s\) est résolu | l'ancre de la fonction de valeur | `ancrer_le_but=True` |
| \(y_v(s) = \max_a(\cdots)\) sinon | la cible d'origine, conservée partout ailleurs | la branche `else` implicite |

**Ce que le correctif a acheté**, mesuré sur un cube réduit à deux par deux pour que l'expérience tienne en une ou deux heures, avec des lots de dix mille, une profondeur de brouillage de 200, mille cubes de test répartis en vingt cubes à chacune des profondeurs 1 à 50, et trente mille pas de recherche autorisés par cube :

| | Méthode d'origine | Avec la cible ancrée |
| --- | --- | --- |
| Perte finale | 0,032572 | **0,012226** |
| Cubes résolus, sur mille | 55 % | **100 %** |
| Pas de recherche nécessaires | référence | **3 à 5 fois moins** |

{{% comment %}}SOURCE: LAPAN ch.21 p.669{{% /comment %}}

> [!NOTE]
 **Attention à un chiffre qui apparaît deux fois dans ce problème pour deux choses différentes.** Le 55 % du tableau ci-dessus est un **taux de résolution** sur les mille cubes de test du cube deux par deux. Le 55 % de la fin de la section 15.5 est une **proportion de cas où la longueur de solution** égale ou améliore celle d'un solveur classique, sur le cube trois par trois, dans l'évaluation publiée. Les deux nombres sont égaux et n'ont aucun rapport. Ne les mettez jamais dans la même phrase, et de façon générale : quand deux pourcentages identiques apparaissent à quelques pages d'intervalle, vérifiez de quoi chacun est le pourcentage avant de les relier.

**Ce que le correctif n'a pas acheté, et c'est le vrai sujet de cette section.** Sur le cube **trois par trois**, après environ **vingt heures** d'entraînement, le meilleur modèle obtenu résout des cubes jusqu'à une profondeur de brouillage de **13**, et **échoue régulièrement au-delà**. La méthode d'origine, reproduite telle quelle, atteignait la profondeur **9** ; la version à cible ancrée atteint **13**. Et le jeu de test de l'évaluation publiée était brouillé par **1 000** coups.

{{% comment %}}SOURCE: LAPAN ch.21 p.670{{% /comment %}}

Posez les trois nombres ensemble : **13 contre 1 000**. Le correctif a amélioré la reproduction de 44 %, et la reproduction reste à deux ordres de grandeur du protocole d'évaluation publié.

**Pourquoi, et les trois raisons sont nommées.** Les hyperparamètres n'étaient pas publiés, donc ceux employés ne sont pas ceux d'origine. L'objectif de valeur était défectueux, et le correctif ne l'a réparé qu'en partie. Et le calcul : une recherche plafonnée à cent mille pas, **cinq brouillages aléatoires seulement par profondeur** dans l'évaluation finale, et une machine à un seul processeur graphique.

{{% comment %}}SOURCE: LAPAN ch.21 p.666, p.670{{% /comment %}}

Sur ce dernier point, deux chiffres qu'il faut garder, parce qu'ils expliquent pourquoi cette expérience n'a pas simplement été refaite dix fois. La cadence publiée était d'environ **50 000 cubes par seconde sur trois processeurs graphiques** ; la cadence obtenue était d'environ **15 000 cubes par seconde sur un seul**. Les deux sont comparables par processeur. Mais cela veut dire **presque six jours** de calcul sur une machine à un processeur graphique pour refaire l'entraînement d'origine une seule fois, ce qui exclut toute expérimentation et tout réglage d'hyperparamètres. C'est exactement pour cette raison qu'un environnement réduit, le cube deux par deux, a été écrit : non pas pour simplifier le problème, mais pour **rendre la mesure possible**.

{{% comment %}}SOURCE: LAPAN ch.21 p.668-669{{% /comment %}}

> [!IMPORTANT]
 **Voici ce que cet échec de reproduction démontre, et voici ce qu'il ne démontre pas, parce que la frontière est étroite et qu'elle est l'essentiel.** Il démontre qu'une méthode publiée sans ses hyperparamètres et sans sa courbe de convergence **n'est pas reproductible**, au sens strict : il manque l'information nécessaire. Il démontre qu'un objectif de valeur sans ancre diverge, et que le correctif améliore massivement un cas réduit. Il ne démontre **rien du tout** sur la méthode elle-même : la méthode d'origine disposait de trois processeurs graphiques pendant 44 heures, de ses propres hyperparamètres, et elle a résolu 640 cubes brouillés par mille coups. Les deux énoncés sont vrais ensemble, parce qu'ils ne portent pas sur le même objet : l'un porte sur une **reproduction**, l'autre sur une **méthode**. C'est la leçon de la semaine 12, et la voici sous sa forme la plus complète, parce que cette fois le diagnostic est donné et le correctif est écrit.

Et un mot sur la façon dont ce résultat est rapporté, qui est le modèle que je vous demande de suivre. Il n'a pas été dissimulé, il n'a pas été transformé en « prometteur mais délicat », et il n'a pas été remplacé par la seule exécution qui donnait un chiffre flatteur. Il est rapporté avec sa configuration, son matériel, sa durée, son diagnostic et l'aveu de ce qui reste inexpliqué. **Un échec de reproduction rapporté ainsi est un résultat scientifique utilisable.** Celui de votre rapport final le sera aussi, s'il est rapporté ainsi.

---

## Le sixième : deux rapports de la même expérience, et ils ne concordent pas

Le sixième est d'une autre nature, et il est plus dérangeant parce qu'il n'a pas de coupable.

La même expérience, sur la tâche de la **Figure 15-4**, a été rapportée **deux fois**, à onze pages d'intervalle. Voici les deux rapports côte à côte.

| | Premier rapport | Second rapport |
| --- | --- | --- |
| Sans démonstrations | **aucun progrès après une journée** d'entraînement | meilleure récompense moyenne de **\(-0{,}4\) après 12 heures** et 4 millions de trames, sans amélioration notable de la dynamique d'entraînement |
| Avec démonstrations | après **quelques dizaines d'exemples de clics corrects**, problème **résolu en 15 minutes** d'entraînement | **25 épisodes de démonstration**, récompense moyenne de **0,5 après 30 000 trames**, soit **8 minutes** |

{{% comment %}}SOURCE: LAPAN ch.14 p.445 (image){{% /comment %}} {{% comment %}}SOURCE: LAPAN ch.14 p.456{{% /comment %}}

Comptons les désaccords, et il y en a cinq.

**Un :** une journée contre douze heures. **Deux :** « aucun progrès » contre une valeur chiffrée de \(-0{,}4\), qui est un progrès mesurable sur une échelle qui part de plus bas. **Trois :** quinze minutes contre huit. **Quatre :** « résolu » contre une récompense moyenne de **0,5** sur une tâche dont les récompenses montent à 1, ce qui n'est pas résolu. **Cinq, le plus discret :** « quelques dizaines d'exemples de clics » n'est pas « 25 épisodes de démonstration ». Un épisode de cet agent compte sept à neuf pas, donc les deux comptes diffèrent d'environ un ordre de grandeur.

**Ce cours ne retient aucun des deux comme le chiffre.** Et je veux être très clair sur ce que cela signifie, parce que la tentation de la lecture indignée est forte et qu'elle serait une erreur.

Ce n'est pas une fraude. Ce n'est même pas une négligence. C'est ce qui arrive quand une **même expérience est décrite deux fois, à deux moments de la rédaction, sans qu'un nombre unique ait été enregistré quelque part**. La première description est écrite de mémoire en clôturant une section ; la seconde est écrite en ouvrant une autre section, peut-être à partir d'un journal, peut-être d'un autre souvenir. Les deux sont de bonne foi. Et le résultat est **inutilisable**, parce qu'aucun lecteur ne peut savoir laquelle des deux descriptions correspond à l'exécution qui a eu lieu.

> [!IMPORTANT]
 **Voici à quoi ressemble un résultat non reproductible vu de l'extérieur, et c'est l'argument le plus net de ce cours en faveur de son propre protocole.** Ce n'est pas une courbe truquée ni une barre d'erreur manquante : c'est **deux phrases qui ne disent pas la même chose**, dans un document sérieux, écrit par quelqu'un de compétent. Le remède est celui que le jalon 2 a imposé et que les jalons 3 et 4 ont renforcé, et il tient en une phrase : **le nombre vit dans le journal, pas dans la prose.** Vous écrivez votre texte à partir d'un fichier de résultats que vous n'avez pas édité à la main ; si une phrase de votre rapport contient un nombre, ce nombre est traçable jusqu'à une ligne de journal, avec sa graine, sa configuration et son horodatage. Ce n'est pas de la bureaucratie : c'est ce qui fait la différence entre les deux colonnes du tableau ci-dessus.

Et pour finir sur la mesure la plus simple à retenir de cette section : dans les deux cas, **la plage d'incertitude de la mesure est plus large que l'effet mesuré**. Un facteur deux sur le temps, un facteur dix sur le nombre de démonstrations, et une différence qualitative sur le résultat. Un effet aussi mal cerné ne peut pas être comparé à autre chose, et donc ne peut servir à aucune décision de conception. **C'est à cela que sert un protocole : non pas à rassurer un évaluateur, mais à rendre vos propres mesures utilisables par vous-même trois mois plus tard.**

---
