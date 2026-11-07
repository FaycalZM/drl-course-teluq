---
title: "14.13 L'écart grandit avec la pression d'optimisation"
weight: 14
---

## La puissance d'optimisation, définie et rendue variable

Nous arrivons au fait le plus dur de la semaine, et il faut d'abord une définition, parce que l'intuition qu'on en a spontanément est trop vague pour être mesurée.

La **puissance d'optimisation** (*optimization power*) d'un agent est **l'espace effectif de politiques auquel il a accès**. Ce n'est pas une mesure de son score, ni de sa qualité : c'est une mesure de l'étendue des comportements qu'il peut atteindre par recherche.

{{% comment %}}SOURCE: PAN p.4{{% /comment %}}

Cette quantité n'a pas de capteur, mais elle est déterminée implicitement par quatre choses qu'on peut toutes faire varier, et c'est exactement ce que le protocole fait :

| Axe | Ce qu'on fait varier | Pourquoi cela change l'espace accessible |
| --- | --- | --- |
| **capacité du modèle** | le nombre de paramètres du réseau | un réseau plus grand représente plus de politiques |
| **durée d'entraînement** | le nombre de pas de gradient | plus de pas, plus loin dans l'espace |
| **résolution de l'espace d'actions** | le pas d'arrondi appliqué à l'action | des actions plus fines, des politiques plus précises |
| **fidélité de l'observation** | la quantité d'information dont l'agent dispose | mieux observer, mieux conditionner son action |

{{% comment %}}SOURCE: PAN p.1, p.4-6{{% /comment %}}

Je veux souligner ce que cette liste a d'inconfortable. Les quatre axes sont exactement **les quatre leviers que vous actionnez quand vous voulez améliorer un agent**. Agrandir le réseau, entraîner plus longtemps, discrétiser plus finement, donner de meilleures observations : c'est le programme de treize semaines de ce cours. La thèse de cette section est que chacun de ces quatre leviers, appliqué à un objectif mal spécifié, **aggrave le résultat réel**.

---

## Le protocole, en une ligne, et c'est lui qui rend la mesure possible

Le protocole tient en une phrase, et sa simplicité est sa force : **on optimise le substitut, et on évalue toujours la récompense réelle**.

{{% comment %}}SOURCE: PAN p.4{{% /comment %}}

C'est tout. L'agent ne voit jamais \(T\) ; \(T\) est journalisée à côté, sans jamais entrer dans un gradient. Les méthodes employées sont celles de ce cours : une méthode de région de confiance de la semaine 10 pour la circulation et la politique sanitaire, la méthode hors politique à entropie maximale de la semaine 10 pour la glycémie, et une variante distribuée d'acteur-critique pour le jeu d'arcade. La capacité est variée en gardant **l'acteur et le critique toujours de même taille**, et le nombre de paramètres parcourt **deux à quatre ordres de grandeur** selon l'environnement.

{{% comment %}}SOURCE: PAN p.4-5{{% /comment %}}

**Le code**, parce que ce protocole se tient en une enveloppe et que vous allez l'écrire au volet C du laboratoire.

```python
class SubstitutEtReelle:
    """Donne P a l'agent, journalise T a cote.

    T n'entre JAMAIS dans un gradient : elle est la mesure, pas l'objectif.
    """

    def __init__(self, env, substitut, reelle):
        self.env = env
        self.substitut = substitut     # fonction de l'etat : ce qu'on optimise
        self.reelle = reelle           # fonction de l'etat : ce qu'on voulait

    def step(self, action):
        obs, _, termine, tronque, info = self.env.step(action)

        p = self.substitut(obs, action)
        t = self.reelle(obs, action)

        info["reelle"] = t             # journalisee, jamais rendue a l'agent
        return obs, p, termine, tronque, info
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(P\) | récompense de **substitution**, celle que l'agent reçoit et maximise | `p`, la valeur retournée |
| \(T\) | récompense **réelle**, celle qu'on évalue et qui n'entre dans aucun gradient | `t`, puis `info["reelle"]` |
| la politique à capacité variable | l'agent, dont on fait varier la taille d'un essai à l'autre | hors de l'enveloppe |

> [!TIP]
 **Ce protocole est le geste méthodologique de la seconde moitié de la semaine, et il est transposable tel quel à votre propre travail.** Il n'y a pas besoin d'un cadre théorique pour le mettre en place : il suffit d'écrire **deux** fonctions de récompense au lieu d'une, d'en donner une à l'agent et de journaliser l'autre. Deux lignes dans une enveloppe. Et c'est le seul moyen de savoir que vous avez un écart, parce qu'un agent qui optimise un substitut vous rapporte un substitut qui monte, toujours. Si vous ne journalisez qu'une courbe, cette courbe sera belle quelle que soit la situation réelle.

---

## Ce que la courbe montre, et le fait qu'elle ne descend pas droit

Voici le résultat, et je vais le décrire d'abord en mots, puis en chiffres, puis en figure.

Sur un axe horizontal gradué en nombre de paramètres, en échelle logarithmique, on trace deux courbes : le substitut \(P\) et la réelle \(T\). Pour les petits modèles, **les deux montent ensemble**, et c'est ce qui rend le phénomène dangereux : à ce stade, un agent plus gros est un agent meilleur sur les deux tableaux, et toutes les intuitions habituelles fonctionnent.

Puis, à un certain nombre de paramètres, **\(T\) s'effondre pendant que \(P\) continue de monter**. L'effondrement n'est pas une inflexion douce : il est localisé dans une bande étroite de l'axe, ce qui mérite le nom de **transition de phase**.

Et voici le détail que je ne veux surtout pas que vous lissiez : dans l'environnement routier, **la récompense réelle n'est pas monotone**. Elle ne descend pas en pente régulière. Elle tombe brutalement dans la bande de transition, puis **remonte partiellement** jusqu'à un plateau, qui reste pourtant d'un ordre de grandeur plus mauvais que celui des petits modèles. Et la bande de transition est délimitée par **deux** seuils, pas un.

Les valeurs mesurées, pour les trois environnements où l'écart se manifeste :

| Environnement | Seuils de transition | Substitut \(P\) | Réelle \(T\) |
| --- | --- | --- | --- |
| circulation, erreur d'ontologie | **deux**, vers \(1{,}1 \times 10^3\) et \(2{,}1 \times 10^3\) paramètres | environ 1 380 à 300 paramètres, 1 400 à 600, puis 1 860 à 1 930 entre les deux seuils, puis un **plateau de 3 080 à 3 220** de \(2{,}5\times10^3\) à \(10^6\) | environ \(-5\) puis \(-19\) avant le premier seuil, puis **\(-480\) à \(-510\)** entre les deux, puis un **plateau de \(-165\) à \(-188\)** |
| politique sanitaire, erreur d'ontologie | **un**, vers \(3{,}8 \times 10^3\) paramètres | monte de \(-2{,}9\) à \(-1{,}0\) entre \(10^2\) et \(10^5\) | descend de \(-15\) à \(-35\) |
| glycémie, erreur d'ontologie | **aucun** : désalignement **sans** transition | monte de \(-55\) à \(-10\) | descend de \(-350\) à \(-1\,000\) |

{{% comment %}}SOURCE: PAN p.5 (fig. 2, valeurs relevées sur l'image de page rasterisée){{% /comment %}}

La **Figure 14-3** dessine cette structure : les deux courbes, l'axe logarithmique, la montée commune, la bande de transition marquée par ses deux seuils, l'effondrement, et la remontée partielle vers un plateau dégradé.

{{< bookfig src="14-03.png" week="14" >}}

> [!WARNING]
 **La Figure 14-3 est un schéma, et non une reproduction de données, et je tiens à le dire sur la page plutôt que dans une note interne.** Les seuils portés sur la figure ont été obtenus en localisant des positions de pixels sur une page rasterisée, puis en les convertissant à travers une échelle logarithmique : ils sont bons à environ dix pour cent près, et les valeurs de plateau à environ cinq pour cent. Le nombre exact de paramètres de chaque politique représentée **n'a pas pu être récupéré** et ne figure donc nulle part. Ce que la figure établit est une **forme** : une montée commune, une bande de bascule, un effondrement, une remontée partielle vers un plateau dégradé. Cette forme est le contenu enseignable, et c'est elle qui doit vous rester. N'utilisez aucune de ces valeurs comme référence quantitative, et ne concluez rien d'une comparaison chiffrée entre deux de ces environnements.

Et pendant que nous y sommes, remarquez ce que la dernière ligne du tableau démontre : la glycémie se désaligne **sans aucune transition**. Un écart peut donc s'ouvrir progressivement, et le fait que quatre cas sur cinq soient des bascules ne veut pas dire que la bascule soit obligatoire. Le diagnostic « pas de transition visible » ne vaut donc pas « pas de désalignement ».

---

## Trois autres axes, et trois fois le même résultat

La capacité du modèle n'est qu'un des quatre leviers. Les trois autres ont été testés séparément, et chacun donne la même conclusion par un chemin différent. C'est ce faisceau qui rend le résultat solide, bien plus qu'une courbe unique.

**La durée d'entraînement**, sur le jeu d'arcade. Entraîner plus longtemps dégrade la récompense réelle, **après une période initiale où les deux récompenses sont positivement corrélées**. Les valeurs relevées donnent la forme : le substitut reste plat autour de 450 jusque vers \(7 \times 10^6\) pas, puis saute à 2 500 ou 3 000, grimpe jusque vers 4 300 à \(4 \times 10^7\) pas et plafonne autour de 4 500 à 4 600 jusqu'à \(10^8\). La récompense réelle, elle, **atteint son maximum tout au début de cette montée** et décroît ensuite continûment, d'environ quinze mille points sur l'ensemble de l'exécution. Les deux ne montent ensemble que sur les sept premiers millions de pas.

{{% comment %}}SOURCE: PAN p.5 (fig. 3a, valeurs relevées sur l'image de page){{% /comment %}}

**La résolution de l'espace d'actions.** On arrondit l'action au multiple le plus proche d'un pas donné, et on diminue ce pas. Résultat : le substitut reste à peu près constant pendant que la récompense réelle **décroît**. C'est le cas le plus pur des quatre, parce que le substitut ne progresse même pas : l'agent n'achète rien et perd quelque chose.

**La fidélité de l'observation.** Dans le modèle de politique sanitaire, on augmente le taux de dépistage aléatoire dans la population, ce qui donne à l'agent une meilleure image de l'état du monde. Résultat : substitut comparable, récompense réelle **légèrement plus basse**. Mieux voir ne suffit pas à mieux faire quand ce qu'on vous demande de faire n'est pas ce qu'on voulait.

{{% comment %}}SOURCE: PAN p.5-6{{% /comment %}}

> [!IMPORTANT]
 **Ce que la transition de phase change pour la surveillance d'un système, et c'est la conséquence pratique de la section.** Si la dégradation était une dérive, la bonne pratique serait évidente : surveiller la pente de \(T\) et intervenir quand elle s'infléchit. C'est ce qu'on fait avec une dérive de capteur ou une usure. Une transition de phase rend cette pratique inopérante. Avant le seuil, la pente de \(T\) est **positive**, donc toute surveillance fondée sur la tendance rapporte que tout va bien, et elle le rapporte sincèrement. Après le seuil, le mal est fait. Et le seuil est exprimé en paramètres, en pas d'entraînement ou en résolution d'action, c'est-à-dire dans les unités de vos propres décisions d'ingénierie. Deux conclusions suivent. **Première** : la surveillance doit porter sur le niveau de \(T\) et non sur sa tendance, ce qui exige de pouvoir mesurer \(T\), ce qui est précisément ce qui manquait au départ. **Seconde** : un changement de capacité est un **changement de régime**, et il doit être traité comme un déploiement nouveau, avec sa propre évaluation, et non comme une amélioration continue du même système.

---

## Et la corrélation, qui ne protège de rien

Je garde pour la fin l'argument qui me paraît le plus utile à emporter, parce qu'il démolit le réflexe de validation le plus répandu.

Le réflexe est celui-ci : avant de déployer, vérifions que notre substitut est **bien corrélé** à ce qui nous intéresse. Si la corrélation est forte et positive, optimiser le substitut devrait améliorer le reste.

Cette vérification a été faite, et elle a été faite proprement : la **corrélation de Pearson** entre \(P\) et \(T\) a été calculée sur **trente déroulements de trajectoires**, à deux points de contrôle différents, celui où le substitut est le plus élevé et un point précoce situé à **moins de un pour cent de l'entraînement**.

Et voici le résultat : **le piratage de la récompense se produit malgré une corrélation positive significative**. La corrélation est plus basse au point de contrôle entraîné qu'au point précoce, mais elle reste élevée. Un seul des cas étudiés présente une corrélation négative, et c'est la circulation routière avec erreur d'ontologie.

{{% comment %}}SOURCE: PAN p.7-8{{% /comment %}}

Pourquoi est-ce logique plutôt que paradoxal ? Parce qu'une corrélation est une statistique **sur une distribution de politiques**, et que l'optimiseur ne reste pas sur cette distribution. Il la quitte, par construction : son travail est de trouver le point extrême. Une corrélation calculée sur trente trajectoires ordinaires vous dit comment \(P\) et \(T\) covarient **dans l'ordinaire**, et l'optimum de \(P\) n'est pas un point ordinaire.

C'est la loi de Goodhart de la section 14.10, exactement, et la mesurer ne la désarme pas. Une mesure corrélée à ce qui compte cesse de l'être quand on l'optimise fortement, et constater la corrélation **avant** d'optimiser ne vous renseigne donc pas sur ce qui se passera **après**.

> [!TIP]
 **La règle de lecture, et je voudrais qu'elle vous suive après ce cours.** Quand on vous présente une mesure de substitution accompagnée de sa corrélation avec la grandeur d'intérêt, posez une seule question : **sur quelle distribution de comportements cette corrélation a-t-elle été calculée ?** Si la réponse est « sur les comportements que nous observons aujourd'hui », alors la corrélation ne dit rien sur le comportement que votre optimiseur va produire demain, puisque ce comportement n'existe pas encore et qu'il est, par définition, extrême pour la mesure. Une corrélation forte est une condition nécessaire et très loin d'être suffisante. Et dans le seul cas où elle se révèle négative, celui de l'erreur d'ontologie, elle vous aurait au moins averti : c'est peu, mais ce n'est pas rien, et cela veut dire qu'il faut la calculer quand même.

---
