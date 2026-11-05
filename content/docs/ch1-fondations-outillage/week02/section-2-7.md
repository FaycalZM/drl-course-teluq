---
title: "2.7 Généralisation, arrêt précoce, abandon de neurones"
weight: 8
---

## Ajuster n'est pas apprendre

Une section de réflexes, pas de théorie. Je vais vous donner trois gestes et une mise en garde, et je vais résister à la tentation de développer, parce que ce cours n'est pas un cours d'apprentissage supervisé.

Commençons par remettre l'objectif en place. Ajuster les données d'entraînement n'a **jamais** été le but : ce n'était qu'un objectif intermédiaire. Ce que nous voulons, ce sont des régularités qui tiennent sur des exemples **nouveaux**, issus de la même population. C'est la **généralisation** (*generalization*), et c'est la seule chose qui compte.

{{% comment %}}SOURCE: D2L ch.5 p.229{{% /comment %}}

Une phrase d'honnêteté, et je n'en dirai pas plus : la théorie de l'apprentissage profond n'est **pas réglée**, ni sur la raison pour laquelle on parvient à optimiser ces modèles, ni sur celle pour laquelle le résultat généralise. Vous travaillez avec un outil qui fonctionne mieux que nos explications, et il faut le savoir sans en être paralysé.

{{% comment %}}SOURCE: D2L ch.5 p.229-230{{% /comment %}}

---

## Trois définitions à ne pas confondre

Trois termes voisins, trois sens distincts. L'**erreur de généralisation** (*generalization error*) est l'erreur vraie du modèle sur la population sous-jacente ; comme elle n'est pas calculable, on l'estime sur des données tenues à l'écart de l'entraînement. L'**écart de généralisation** (*generalization gap*) est la **différence** entre la qualité de l'ajustement sur les données d'entraînement et celle sur les données de test. Et un écart important porte un nom qui n'est pas un verdict moral mais une description : le **surapprentissage** (*overfitting*).

{{% comment %}}SOURCE: D2L ch.5 p.230{{% /comment %}}

Pourquoi faudrait-il des hypothèses pour généraliser ? Parce qu'aucun algorithme d'apprentissage ne généralise bien sur **toutes** les distributions possibles : c'est le théorème dit de l'absence de repas gratuit. Tout modèle s'appuie donc sur un **biais inductif** (*inductive bias*), c'est-à-dire sur une famille d'hypothèses privilégiée. Celui d'un perceptron multicouche profond est facile à énoncer : construire une fonction compliquée en composant des fonctions plus simples. Retenez cette phrase, nous la retrouverons mot pour mot en section 2.8 avec un autre biais inductif.

{{% comment %}}SOURCE: D2L ch.5 p.230{{% /comment %}}

Et voici le retournement propre à l'apprentissage profond. Nos modèles sont assez expressifs pour ajuster **chaque** exemple d'entraînement, même quand il y en a des millions, y compris lorsque les étiquettes sont tirées au hasard : on parle de **surparamétrisation** (*overparameterization*) et d'**interpolation des données d'entraînement** (*interpolating the training data*). Les bornes classiques de complexité, dimension de Vapnik-Chervonenkis ou complexité de Rademacher, ne peuvent donc pas expliquer pourquoi ces modèles généralisent : elles prédisent le pire, et le pire n'arrive pas. Plus troublant encore, rendre le modèle **plus** expressif, en ajoutant des couches, des unités ou des époques, fait souvent **baisser** l'erreur de généralisation ; ce comportement non monotone porte un nom, la **double descente** (*double descent*).

{{% comment %}}SOURCE: D2L ch.5 p.230-231{{% /comment %}}

---

## Premier geste : l'arrêt précoce

Puisque contraindre les poids est difficile, contraignons le **temps**. L'**arrêt précoce** (*early stopping*) consiste à limiter le nombre d'époques plutôt que l'amplitude des paramètres. Le protocole tient en trois lignes : on surveille l'erreur sur un jeu de validation, typiquement une fois par époque ; on note la meilleure valeur obtenue ; et l'on arrête quand elle n'a pas diminué de plus de \(\epsilon\) pendant un certain nombre d'époques. Ce nombre d'époques de patience s'appelle le **critère de patience** (*patience criterion*).

{{% comment %}}SOURCE: D2L ch.5 p.232{{% /comment %}}

Pourquoi cela marche-t-il ? Pour une raison empirique assez jolie : les réseaux apprennent **d'abord** les données proprement étiquetées, et ne se mettent qu'**ensuite** à interpoler les exemples mal étiquetés. Arrêter tôt, c'est donc s'arrêter entre les deux. Avantage secondaire mais réel, surtout sur Colab : on économise du temps et de l'argent.

{{% comment %}}SOURCE: D2L ch.5 p.232{{% /comment %}}

Une nuance pour éviter d'en faire un dogme. Si les étiquettes sont parfaitement propres et les classes bien séparées, l'arrêt précoce n'apporte presque rien. S'il y a du bruit d'étiquetage ou une variabilité intrinsèque dans les données, il devient crucial. Gardez la question en tête : **mes cibles sont-elles bruitées ?** En apprentissage par renforcement, la réponse sera oui, et pour des raisons que vous découvrirez en semaine 4.

{{% comment %}}SOURCE: D2L ch.5 p.232-233{{% /comment %}}

---

## Deuxième geste : la dégradation des poids

La **dégradation des poids** (*weight decay*) ajoute à l'objectif une pénalité sur la taille des poids. C'est exactement le terme \(\Omega\) de la section 2.3, dont nous avions dit que sa dérivée valait \(\lambda\mathbf{W}^{(l)}\). Avec une norme \(\ell_2\) on parle de **régularisation ridge** (*ridge*), avec une norme \(\ell_1\) de **lasso**, qui tend à mettre des poids exactement à zéro.

{{% comment %}}SOURCE: D2L ch.5 p.233{{% /comment %}}

En code, cela ne coûte même pas une ligne : c'est un argument de l'optimiseur.

```python
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-4)
```

Une réserve, cependant, et elle est importante : aux intensités habituellement utilisées en apprentissage profond, la dégradation des poids **n'empêche pas** l'interpolation des données d'entraînement. Son bénéfice n'est donc peut-être réel qu'en combinaison avec l'arrêt précoce. Voilà pourquoi je vous présente ces deux gestes ensemble, et pourquoi je vous demande de ne jamais considérer qu'un `weight_decay` non nul « règle » le surapprentissage.

{{% comment %}}SOURCE: D2L ch.5 p.233{{% /comment %}}

---

## Troisième geste : l'abandon de neurones

Le troisième geste est le plus étrange, et c'est mon préféré. Il part d'un résultat classique de la théorie de l'estimation : entraîner un modèle avec du **bruit injecté dans les entrées** est équivalent à une forme de régularisation. L'idée de l'**abandon de neurones** (*dropout*) est d'appliquer ce résultat non pas aux entrées, mais aux couches **internes** : à chaque itération, avant de calculer la couche suivante, on met à zéro une fraction des unités de la couche courante.

{{% comment %}}SOURCE: D2L ch.5 p.234{{% /comment %}}

La justification donnée par les auteurs de la méthode est différente et complémentaire : elle casse la **co-adaptation** entre couches, c'est-à-dire ces arrangements fragiles où une unité ne fonctionne que parce qu'une autre compense exactement son biais. Si une unité peut disparaître à tout moment, les autres ne peuvent plus compter sur elle.

{{% comment %}}SOURCE: D2L ch.5 p.235{{% /comment %}}

La **Figure 2-7** montre le même réseau avant et après : deux unités cachées ont disparu pour cette itération, et elles seront peut-être présentes à la suivante.

{{< bookfig src="02-07.png" week="02" >}}

{{% comment %}}SOURCE: D2L ch.5 p.235{{% /comment %}}

Reste un détail technique qui est en réalité l'idée centrale. Si l'on se contente de mettre des unités à zéro, on **biaise** la couche vers le bas : sa sortie moyenne diminue d'autant. On veut injecter du bruit **sans biais**, c'est-à-dire de telle sorte que la valeur espérée de la couche soit celle qu'elle aurait eue sans bruit. D'où la transformation suivante, appliquée à chaque activation \(h\), avec une probabilité d'abandon \(p\) :

{{% comment %}}SOURCE: D2L éq. 5.6.1 p.235{{% /comment %}}

$$
h' = \begin{cases}
0 & \text{avec probabilité } p \\[4pt]
\dfrac{h}{1-p} & \text{sinon}
\end{cases}
$$

{{% comment %}}SOURCE: D2L ch.5 p.235{{% /comment %}}

Vérifiez l'espérance, c'est immédiat : avec probabilité \(p\) la valeur est 0, avec probabilité \(1-p\) elle vaut \(h/(1-p)\), donc \(\E[h'] = (1-p) \cdot h/(1-p) = h\). Le facteur \(1/(1-p)\) n'est pas un ajustement cosmétique, c'est **la raison pour laquelle l'abandon de neurones est une injection de bruit** (*noise injection*) et non une mutilation du réseau.

{{% comment %}}SOURCE: D2L ch.5 p.235{{% /comment %}}

Écrivons-le à la main une fois, puis utilisons la version de la bibliothèque.

```python
def abandon_manuel(X: torch.Tensor, p: float) -> torch.Tensor:
    """Version explicite, pour voir l'équation : masque, puis correction de biais."""
    if p == 1.0:
        return torch.zeros_like(X)
    masque = (torch.rand(X.shape) > p).float()   # 1 pour les survivants
    return masque * X / (1.0 - p)


# En pratique, une couche après chaque couche entièrement connectée :
reseau = nn.Sequential(
    nn.Linear(n_obs, 256), nn.ReLU(), nn.Dropout(p=0.2),
    nn.Linear(256, 256), nn.ReLU(), nn.Dropout(p=0.5),
    nn.Linear(256, n_sorties),
)
```

{{% comment %}}SOURCE: D2L ch.5 p.236-238{{% /comment %}}

Deux réglages usuels dans ce fragment. On met souvent une probabilité d'abandon **plus faible près de l'entrée** qu'en profondeur, l'information d'entrée étant plus précieuse ; et les valeurs de travail classiques pour un réseau à deux couches cachées de 256 unités sont deux abandons à 0,5, avec un pas d'apprentissage de 0,1.

{{% comment %}}SOURCE: D2L ch.5 p.236-237{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, c'est l'erreur la plus fréquente sur l'abandon de neurones : il est désactivé au moment du test.** Pendant l'entraînement, on veut du bruit ; pendant l'évaluation, on veut une prédiction déterministe. En PyTorch, cela se commande par `model.eval()` avant d'évaluer et `model.train()` avant de reprendre l'entraînement, et c'est l'une des choses que fait l'appel `__call__()` de la section 2.4 sans que vous le voyiez. Dans une implémentation faite à la main, le garde-fou s'écrit `if self.training:`. Oubliez-le et vos courbes de validation deviendront bruitées sans raison apparente.

{{% comment %}}SOURCE: D2L ch.5 p.236-237{{% /comment %}}

Une exception existe, et elle est documentée : on garde parfois l'abandon **actif** au moment du test, on fait plusieurs prédictions, et on regarde leur dispersion comme une mesure heuristique d'**incertitude**. C'est un usage délibéré, pas un oubli, et il faut savoir le reconnaître dans du code.

{{% comment %}}SOURCE: D2L ch.5 p.236{{% /comment %}}

---

## La mise en garde qui vaut pour tout le reste du cours

> [!WARNING]
 **Attention, et c'est la phrase la plus importante de la section.** Tout ce que vous venez de lire suppose une **distribution de données fixe** : un jeu d'entraînement et un jeu de test tirés de la même population, une fois pour toutes. En apprentissage par renforcement, les données sont produites par la politique de l'agent, et **la politique change pendant l'entraînement**. La distribution des données bouge donc avec le modèle, et le mot « surapprentissage » n'y désigne plus tout à fait la même chose. Je le dis une fois, ici, pour que vous ne transposiez pas mécaniquement les réflexes de cette section ; la semaine 7 est celle où cette différence devient coûteuse, sur une étude de cas où elle se mesure en argent.
