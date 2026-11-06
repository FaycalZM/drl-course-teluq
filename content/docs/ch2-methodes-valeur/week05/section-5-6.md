---
title: "5.6 La triade fatale, et une divergence démontrée"
weight: 7
---

## Trois lignes d'arithmétique, et un poids qui part à l'infini

Nous avons maintenant tout ce qu'il faut pour construire un agent : une fonction approchée, un objectif, une règle de mise à jour semi-gradient, et des valeurs d'action. Avant de l'écrire, je veux vous montrer ce qui peut mal tourner, et je veux vous le **montrer** plutôt que vous le dire. C'est la section la plus théorique de la semaine et c'est aussi, je trouve, la plus utile : elle explique à l'avance la moitié des échecs que vous rencontrerez dans ce cours.

Le problème a deux moitiés. La première, nous la connaissons depuis la semaine 3 : apprendre hors politique signifie apprendre sur des données produites par une autre politique que celle que l'on évalue. La seconde est moins connue et c'est elle qui nous intéresse : la **distribution** des mises à jour ne correspond plus à la distribution sur politique. C'est la condition que j'ai plantée à la fin de la section 5.3, et nous allons voir ce qui se passe quand elle tombe.

{{% comment %}}SOURCE: SB ch.11 p.282{{% /comment %}}

Prenons l'exemple le plus petit possible. Deux états. Le premier a pour valeur estimée \(w\), le second \(2w\) : il n'y a donc qu'**un seul poids** dans tout le système, et les caractéristiques des deux états sont respectivement 1 et 2. Une seule action. La récompense de la transition du premier état vers le second est **nulle**.

Suivons l'arithmétique à voix haute, en partant de \(w = 10\). La transition part d'un état que l'on estime à 10 et arrive dans un état que l'on estime à 20. L'erreur TD est donc positive : la valeur de départ était trop basse, il faut l'augmenter. On met à jour, et \(w\) monte vers 11. Mais regardez ce que cela fait au second état : il vaut \(2w\), donc il vient de passer à 22. L'erreur TD suivante vaut maintenant environ 11, c'est-à-dire **plus** que la précédente, et non moins. On met à jour encore, \(w\) passe à 12,1 environ. Et ainsi de suite.

{{% comment %}}SOURCE: SB ch.11 p.282{{% /comment %}}

Voilà l'algèbre complète, et elle tient en deux lignes.

$$
\delta_t = R_{t+1} + \gamma\,\hat v(S_{t+1},\mathbf{w}_t) - \hat v(S_t,\mathbf{w}_t)
 = 0 + \gamma\,(2w_t) - w_t = (2\gamma - 1)\,w_t
$$

$$
w_{t+1} = w_t + \alpha\,\rho_t\,\delta_t\,\nabla\hat v(S_t,\mathbf{w}_t)
 = \big(1 + \alpha(2\gamma - 1)\big)\,w_t
$$

{{% comment %}}SOURCE: SB ch.11 p.282{{% /comment %}}

Deux précisions de lecture avant la conclusion. Le gradient \(\nabla\hat v(S_t,\mathbf{w}_t)\) vaut 1, puisque la valeur du premier état est \(w\) exactement. Et le facteur \(\rho_t\) est le rapport d'échantillonnage préférentiel de la semaine 3, qui corrige le fait que la transition observée a été produite par une autre politique ; la seconde égalité est écrite pour \(\rho_t = 1\), c'est-à-dire pour une transition que la politique cible aurait aussi jouée.

Maintenant, la conclusion, et elle est sans appel. La suite \((w_t)\) est **géométrique**, de raison \(1 + \alpha(2\gamma-1)\). Cette raison est strictement supérieure à 1 dès que \(\gamma > 0{,}5\), c'est-à-dire pour toutes les valeurs d'actualisation que ce cours emploie. Donc \(w_t\) croît sans borne.

> [!WARNING]
 **Attention à la phrase qui suit, parce qu'elle détruit le réflexe naturel.** La stabilité ne dépend pas du pas d'apprentissage choisi, pourvu que \(\alpha > 0\) : un pas plus petit ou plus grand modifie la **vitesse** à laquelle \(w\) part à l'infini, mais pas le **fait** qu'il y parte. Lisez cette phrase deux fois. Devant un entraînement qui explose, le premier geste de tout le monde est de diviser le pas d'apprentissage par dix. Ici, cela ne sert à rien : la raison de la suite reste supérieure à 1, et la divergence est simplement plus lente. Il n'y a pas de réglage qui sauve cette configuration ; il faut en **changer**.

{{% comment %}}SOURCE: SB ch.11 p.282{{% /comment %}}

Douze lignes suffisent à le constater, et le constater vaut mieux qu'un paragraphe de ma part.

```python
GAMMA, ALPHA = 0.99, 0.1        # avec ALPHA = 0.001 : la pente change, pas l'issue
w = 10.0

for k in range(15):
    # hat v(s1, w) = w et hat v(s2, w) = 2w ; la récompense est nulle.
    delta = (2 * GAMMA - 1) * w            # l'erreur TD, écrite à la main
    w = w + ALPHA * delta                  # UNE mise à jour semi-gradient
    print(f"k = {k:2d}   w = {w:12.3f}")

print(f"raison de la suite : {1 + ALPHA * (2 * GAMMA - 1):.4f}")
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(w\) | le poids unique du système | `w` |
| \(\hat v(s_1,\mathbf{w}) = w\), \(\hat v(s_2,\mathbf{w}) = 2w\) | les deux valeurs approchées | implicites dans le calcul de `delta` |
| \(\delta_t = (2\gamma - 1)w_t\) | l'erreur TD | `delta` |
| \(\alpha\) | pas d'apprentissage | `ALPHA` |
| \(1 + \alpha(2\gamma - 1)\) | la raison de la suite géométrique | `1 + ALPHA * (2 * GAMMA - 1)` |

Reste à comprendre **pourquoi** l'apprentissage hors politique autorise cela, et une image comptable le dit mieux qu'une démonstration. Sur politique, un état ne peut soutenir la valeur de celui qui le précède qu'en créant une attente plus élevée, et cette attente devra elle-même être satisfaite : la facture finit toujours par être présentée. Hors politique, on peut faire une promesse, puis, après avoir joué une action que la politique cible n'aurait **jamais** jouée, oublier la promesse et être quitte. La boucle de rétroaction qui corrigeait l'excès a été coupée.

{{% comment %}}SOURCE: SB ch.11 p.283{{% /comment %}}

---

## Le contre-exemple de Baird : tout est favorable, et cela diverge quand même

L'exemple à deux états est convaincant mais on peut lui opposer qu'il est tordu, que la représentation \(w\) et \(2w\) est maladroite, que la valeur vraie n'y est peut-être pas représentable. Le **contre-exemple de Baird** (*Baird's counterexample*) répond à toutes ces objections d'un coup, et c'est pour cela qu'il est resté.

Voici le processus. Sept états, deux actions. L'action en pointillés mène, avec probabilité égale, vers l'un des six états du haut. L'action en trait plein mène vers le septième état. La politique de comportement \(b\) joue les pointillés avec probabilité \(6/7\) et le trait plein avec probabilité \(1/7\), ce qui fait que la distribution des états suivants sous \(b\) est **uniforme** sur les sept états. La politique cible \(\pi\), elle, joue **toujours** le trait plein, donc sa distribution sur politique se concentre entièrement sur le septième état. Toutes les récompenses sont nulles, et \(\gamma = 0{,}99\).

La **Figure 5-2** montre ce processus, avec l'expression linéaire de la valeur estimée écrite à l'intérieur de chaque état.

{{< bookfig src="05-02.png" week="05" >}}

{{% comment %}}SOURCE: SB ch.11 p.283{{% /comment %}}

Regardez maintenant tout ce qui est **favorable** dans cette tâche, parce que c'est là que l'exemple devient accablant.

Puisque toutes les récompenses sont nulles, la valeur vraie est \(v_\pi(s) = 0\) pour tout état. Cette fonction est **exactement représentable** par l'approximation linéaire employée : il suffit de prendre \(\mathbf{w} = \mathbf{0}\). La solution existe donc, elle est atteignable, et elle est même d'une simplicité insultante. Il y a huit poids pour sept états non terminaux, donc plus de paramètres que d'états. Et les vecteurs de caractéristiques des états forment un ensemble **linéairement indépendant**, ce qui est la condition la plus confortable qu'une approximation linéaire puisse espérer.

{{% comment %}}SOURCE: SB ch.11 p.284{{% /comment %}}

Et malgré tout cela, les poids divergent vers l'infini, et l'instabilité se produit pour **tout** pas d'apprentissage positif, aussi petit soit-il. La **Figure 5-3** montre les poids au fil des mises à jour, avec \(\alpha = 0{,}01\) et un vecteur initial \((1,1,1,1,1,1,10,1)^\top\).

{{< bookfig src="05-03.png" week="05" >}}

{{% comment %}}SOURCE: SB ch.11 p.284{{% /comment %}}

Et ce n'est pas tout, car on pourrait encore soupçonner l'échantillonnage : peut-être le bruit des transitions tirées au hasard est-il responsable ? Non. La divergence se produit tout autant sous la mise à jour **en espérance** de la programmation dynamique, celle qui balaie tous les états à chaque pas, sans aucun tirage et sans aucune asynchronie.

$$
\mathbf{w}_{k+1} \defeq \mathbf{w}_k + \frac{\alpha}{\lvert\mathcal{S}\rvert}
 \sum_{s} \Big(
 \E_\pi\big[\, R_{t+1} + \gamma\,\hat v(S_{t+1},\mathbf{w}_k) \mid S_t = s \,\big]
 - \hat v(s,\mathbf{w}_k) \Big)\nabla\hat v(s,\mathbf{w}_k)
$$

{{% comment %}}SOURCE: SB ch.11 éq. 11.9 p.284{{% /comment %}}

Lisez bien le facteur \(\alpha / \lvert\mathcal{S}\rvert\) et la somme sur **tous** les états : c'est une mise à jour synchrone, en espérance, qui traite l'espace entier d'un seul coup. Aucun hasard, aucune transition manquée, aucune corrélation temporelle. Et les poids s'en vont quand même. Le coupable n'est donc ni le bruit, ni l'ordre des mises à jour.

Qui est-ce alors ? La réponse récolte exactement ce que j'avais planté en section 5.3, et elle tient en une ligne : si l'on modifie seulement la **distribution** des mises à jour de la programmation dynamique, en passant de la distribution uniforme à la distribution **sur politique**, alors la convergence est garantie. Une seule chose change, la provenance des états mis à jour, et le problème disparaît. C'est \(\mu\), et rien d'autre.

{{% comment %}}SOURCE: SB ch.11 p.284{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister : notez le nom de ce qui sauve la convergence, parce que la section 5.7 va le détruire en toute connaissance de cause.** Ce qui sauve la programmation dynamique dans le contre-exemple de Baird, c'est de mettre à jour les états **dans la proportion où la politique cible les visite**. Or le tampon de rejeu, l'outil le plus utile de cette semaine, consiste précisément à mettre à jour des états tirés au hasard dans un stock de vieilles transitions, produites par des politiques antérieures. Nous allons donc, les yeux ouverts, renoncer à la seule condition connue qui garantisse la stabilité, parce qu'elle nous coûte trop cher en échantillons. C'est un marché, il est explicite, et il faut savoir qu'on le passe.

Deux phrases encore, et elles donnent le statut **honnête** de la méthode que nous allons écrire. Premièrement : il existe des contre-exemples semblables à celui de Baird qui montrent la divergence pour **Q-learning**. Deuxièmement : il est peut-être possible de garantir la convergence de Q-learning pourvu que la politique de comportement reste suffisamment proche de la politique cible, par exemple lorsqu'elle est \(\varepsilon\)-gloutonne. Dans ce régime précis, aucune divergence de Q-learning n'a jamais été rapportée, et aucune analyse théorique ne vient pour autant l'exclure.

{{% comment %}}SOURCE: SB ch.11 p.285{{% /comment %}}

Voilà où nous en sommes, et je vous le dis sans l'enjoliver : **pas de preuve de convergence, pas de preuve de divergence**, et une pratique empirique qui marche presque toujours. C'est l'état de la question, et une partie de votre travail d'ingénieur consistera à vivre avec.

Une dernière information, parce qu'elle nomme la seule famille d'approximateurs qui est à l'abri. La stabilité est garantie pour les approximateurs qui n'**extrapolent** pas, c'est-à-dire ceux dont la prédiction en un point reste une moyenne de valeurs observées : on les appelle des **moyenneurs** (*averagers*), et le plus proche voisin ou la régression localement pondérée en sont des exemples. Cette garantie ne couvre en revanche aucune des méthodes réellement employées, pavages de caractéristiques compris, et **surtout pas les réseaux de neurones artificiels**. Notre outil est nommé, et il est exclu de la garantie.

{{% comment %}}SOURCE: SB ch.11 p.286{{% /comment %}}

---

## La triade fatale, et l'audit de notre futur agent

Nous pouvons enfin nommer la configuration dangereuse. Le risque d'instabilité et de divergence apparaît lorsque l'on combine **trois** ingrédients, et cette combinaison porte un nom : la **triade fatale** (*deadly triad*).

1. **L'approximation de la fonction de valeur** : une façon puissante et extensible de généraliser à partir d'un espace d'états beaucoup plus grand que les ressources de mémoire et de calcul disponibles.
2. **L'amorçage** : des cibles de mise à jour qui contiennent des estimations existantes, au lieu de reposer exclusivement sur des récompenses réelles et des retours complets.
3. **L'apprentissage hors politique** : s'entraîner sur une distribution de transitions autre que celle produite par la politique cible.

{{% comment %}}SOURCE: SB ch.11 p.286{{% /comment %}}

Et voici la règle qu'il faut retenir : si **deux** de ces trois éléments sont présents, mais pas les trois, alors l'instabilité peut être évitée. Deux sur trois, c'est sûr. Trois sur trois, c'est le domaine où les contre-exemples vivent.

{{% comment %}}SOURCE: SB ch.11 p.286{{% /comment %}}

Faisons alors l'audit de l'agent que nous allons écrire en section 5.8, ligne par ligne. C'est un exercice que je vous demanderai de refaire au quiz, et il tient en trois phrases.

| Ingrédient | Dans notre futur DQN | Verdict |
| --- | --- | --- |
| approximation de la fonction de valeur | un réseau de convolution qui lit les pixels et sort une valeur par action | **présent** |
| amorçage | la cible vaut \(r + \gamma \max_{a'} Q_{\theta^-}(s',a')\), donc elle contient une estimation | **présent** |
| apprentissage hors politique | les lots sont tirés d'un tampon rempli par des politiques \(\varepsilon\)-gloutonnes antérieures | **présent** |

> [!WARNING]
 **Attention, voilà la thèse de la semaine : notre DQN possède les trois ingrédients.** Il n'est pas « à peu près dans la zone de risque », il est **exactement** dedans, sur les trois axes à la fois, et chacun des trois y est pour une raison que nous avons choisie et que nous ne voulons pas abandonner. Les sections 5.7 et 5.8 ne vont pas supprimer le danger : elles vont le **gérer**, par de l'ingénierie. Et la section 5.9 vous montrera, chiffres en main, que cette gestion échoue environ une fois sur dix.

Deux idées fausses à écarter avant de refermer la section, parce qu'elles vous viendront naturellement.

Le danger n'est pas dû au **contrôle** ni à l'itération généralisée de politique : il apparaît déjà dans le problème de prédiction, c'est-à-dire quand on se contente d'évaluer une politique fixée, comme dans le contre-exemple de Baird. Et il n'est pas dû à l'**apprentissage** ni à l'incertitude sur l'environnement, puisqu'il se produit tout aussi fortement dans les méthodes de planification comme la programmation dynamique, où l'environnement est entièrement connu.

{{% comment %}}SOURCE: SB ch.11 p.286{{% /comment %}}

Reste la question pratique : si les trois ensemble sont dangereux, lequel abandonner ?

L'**approximation de la fonction de valeur** : jamais. Nous avons besoin de méthodes qui passent à l'échelle, et c'est tout l'objet de cette semaine. Ce n'est pas négociable.

L'**amorçage** : c'est possible, et le prix est connu. Il faut alors attendre la fin des épisodes, donc perdre en efficacité d'échantillon et en coût de calcul. C'est une capacité à laquelle on ne renonce qu'à contrecœur, et ce cours ne la lâchera jamais.

L'apprentissage **hors politique** : c'est possible aussi, et le remède tient en quatre mots, employer Sarsa plutôt que Q-learning. Le prix, en revanche, est élevé : on renonce à apprendre plusieurs prédictions en parallèle à partir d'un seul flux d'expérience, et donc à réutiliser des données anciennes.

{{% comment %}}SOURCE: SB ch.11 p.286-287{{% /comment %}}

La semaine 5 fait le choix inverse des trois : elle **garde tout**, et elle gère le danger par de l'ingénierie. Les quatre réparations de la section suivante sont ce que cela veut dire concrètement.

---
