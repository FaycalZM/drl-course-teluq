---
title: "2.2 Pourquoi une couche cachée"
weight: 3
---

## Deux couches sans activation n'en font qu'une

Nous voici à la section la plus importante de la semaine, et elle tient dans un argument de deux lignes d'algèbre. Je vais prendre le temps de l'amener, parce qu'il explique **pourquoi** un réseau profond a des fonctions d'activation, et parce que c'est le genre de vérité qu'on croit comprendre jusqu'au jour où l'on doit l'expliquer.

Partons des limites du modèle linéaire. La linéarité implique la **monotonie** : si la sortie augmente quand une entrée augmente, elle doit augmenter pour **toute** valeur de cette entrée, et toujours dans le même sens. Trois contre-exemples, en ordre croissant de gravité.

D'abord, prédire la probabilité de remboursement d'un prêt à partir du revenu. La relation est bien monotone, un revenu plus élevé ne peut pas nuire, mais elle n'est pas linéaire : passer de 0 à 50 000 $ change tout, passer de 1 000 000 $ à 1 050 000 $ ne change à peu près rien. Ensuite, prédire un risque de décès à partir de la température corporelle. Ici c'est la monotonie elle-même qui tombe : le risque augmente **au-dessus** de 37 °C, et il augmente aussi **en dessous**. Enfin, classer des photographies de chats et de chiens. Faut-il vraiment que l'intensité du pixel (13, 17) augmente toujours la probabilité « chien » ? Inversez l'image, du noir au blanc : la catégorie ne change pas, et pourtant chaque pixel a changé de valeur. Un modèle linéaire sur les pixels est condamné, et aucun prétraitement fabriqué à la main ne le sauvera, parce que le sens d'un pixel dépend de **son contexte**.

{{% comment %}}SOURCE: D2L ch.5 p.208{{% /comment %}}

La réponse à ces trois échecs est la même : empiler des couches entièrement connectées. Les \(L-1\) premières couches construisent une **représentation** des données, la dernière est un prédicteur linéaire appliqué à cette représentation. L'architecture la plus simple de cette famille s'appelle un **perceptron multicouche** (*multilayer perceptron*), et la **Figure 2-2** en montre un : quatre entrées, cinq unités dans la **couche cachée** (*hidden layer*), trois sorties.

{{< bookfig src="02-02.png" week="02" >}}

{{% comment %}}SOURCE: D2L ch.5 p.209{{% /comment %}}

> [!WARNING]
 **Attention, piège de comptage.** Ce réseau compte **deux** couches, pas trois. La couche d'entrée n'effectue aucun calcul : elle se contente de présenter les données. On compte les couches qui transforment, c'est-à-dire celles qui portent des poids. Vous verrez cette erreur dans beaucoup de descriptions d'architectures, et vous la retrouverez au quiz.

{{% comment %}}SOURCE: D2L ch.5 p.209{{% /comment %}}

---

## L'argument de l'effondrement

Écrivons ce réseau à deux couches. Notre convention, celle de l’annexe « Notation », est la suivante : les vecteurs sont des **colonnes**, et une matrice de poids multiplie à **gauche**. Pour une entrée \(\mathbf{x} \in \R^{d}\), une couche cachée de \(h\) unités et \(q\) sorties, nous avons \(\mathbf{W}^{(1)} \in \R^{h \times d}\), \(\mathbf{b}^{(1)} \in \R^{h}\), \(\mathbf{W}^{(2)} \in \R^{q \times h}\), \(\mathbf{b}^{(2)} \in \R^{q}\), le vecteur caché \(\mathbf{h} \in \R^{h}\) et la sortie \(\mathbf{o} \in \R^{q}\).

$$
\mathbf{h} = \mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}, \qquad
\mathbf{o} = \mathbf{W}^{(2)}\mathbf{h} + \mathbf{b}^{(2)}
$$

{{% comment %}}SOURCE: D2L ch.5 p.209{{% /comment %}}

Maintenant, substituons la première égalité dans la seconde. L'algèbre tient en une ligne et la conclusion est brutale.

$$
\mathbf{o} = \mathbf{W}^{(2)}\left(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\right) + \mathbf{b}^{(2)}
 = \underbrace{\mathbf{W}^{(2)}\mathbf{W}^{(1)}}_{\mathbf{W}}\,\mathbf{x} + \underbrace{\mathbf{W}^{(2)}\mathbf{b}^{(1)} + \mathbf{b}^{(2)}}_{\mathbf{b}}
 = \mathbf{W}\mathbf{x} + \mathbf{b}
$$

{{% comment %}}SOURCE: D2L ch.5 p.210{{% /comment %}}

Lisez le résultat plutôt que de le contempler. Une fonction affine d'une fonction affine est une fonction affine. Il existe donc **un modèle à une seule couche**, de paramètres \(\mathbf{W} = \mathbf{W}^{(2)}\mathbf{W}^{(1)}\) et \(\mathbf{b} = \mathbf{W}^{(2)}\mathbf{b}^{(1)} + \mathbf{b}^{(2)}\), qui calcule **exactement** la même fonction que notre réseau à deux couches. Nous avons payé une couche de plus, des millions de paramètres supplémentaires, et nous n'avons rien gagné du tout.

> [!IMPORTANT]
 **Je dois insister : c'est la ligne autour de laquelle toute la semaine est construite.** Sans fonction d'activation, la profondeur **n'achète rien**. Pas « peu de choses » : rien, au sens mathématique strict. C'est la raison d'être de chaque `nn.ReLU()` que vous écrirez dans ce cours, et si un jour un réseau refuse obstinément d'apprendre autre chose qu'une tendance linéaire, la première chose à vérifier est la présence des activations entre les couches.

---

## La fonction d'activation, et le fait d'être un approximateur universel

Le remède est minuscule et il change tout : appliquer après la transformation affine une **fonction d'activation** (*activation function*) non linéaire, élément par élément. Nous la noterons \(\phi\), et les valeurs qu'elle produit s'appellent des activations.

$$
\mathbf{h} = \phi\!\left(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\right), \qquad
\mathbf{o} = \mathbf{W}^{(2)}\mathbf{h} + \mathbf{b}^{(2)}
$$

{{% comment %}}SOURCE: D2L ch.5 p.210{{% /comment %}}

Comme \(\phi\) n'est pas affine, l'effondrement de la section précédente est impossible, et la couche cachée se met enfin à servir. Pour aller plus profond, on répète le motif sans rien changer : \(\mathbf{h}^{(1)} = \phi_1\!\left(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\right)\), puis \(\mathbf{h}^{(2)} = \phi_2\!\left(\mathbf{W}^{(2)}\mathbf{h}^{(1)} + \mathbf{b}^{(2)}\right)\), et ainsi de suite. Un réseau profond, c'est cette ligne répétée.

{{% comment %}}SOURCE: D2L ch.5 p.210{{% /comment %}}

Un résultat classique, démontré à la fin des années 1980, dit qu'une **seule** couche cachée suffit : avec assez d'unités et les bons poids, un perceptron multicouche à une couche cachée peut représenter n'importe quelle fonction. On dit qu'il est un **approximateur universel** (*universal approximator*). L'analogie que je trouve la plus juste est celle du langage C : C peut exprimer n'importe quel programme calculable, ce qui ne vous dit rigoureusement rien sur la difficulté d'**écrire** le programme qui vous intéresse.

{{% comment %}}SOURCE: D2L ch.5 p.210{{% /comment %}}

> [!NOTE]
 **Notez bien cette intuition, elle évite une erreur de raisonnement très commune.** Capacité de représentation et capacité d'apprentissage sont deux choses différentes. Le théorème garantit que les bons poids **existent** ; il ne dit rien sur la façon de les trouver, et c'est précisément là que se passe toute la difficulté. En pratique, un réseau plus profond est souvent beaucoup plus compact qu'un réseau très large à une seule couche, et plus facile à entraîner : voilà pourquoi nous empilons.

{{% comment %}}SOURCE: D2L ch.5 p.211{{% /comment %}}

---

## Trois activations, et le chiffre 0,25

Trois fonctions d'activation suffisent à tout ce que fait ce cours. La **Figure 2-3** les trace avec leurs dérivées ; gardez-la sous les yeux pendant la lecture des trois paragraphes qui suivent.

{{< bookfig src="02-03.png" week="02" >}}

L'**unité linéaire rectifiée** (*rectified linear unit*, ReLU) est la plus simple qu'on puisse imaginer : elle garde les valeurs positives et met les négatives à zéro.

$$
\mathrm{ReLU}(x) = \max(x, 0)
$$

{{% comment %}}SOURCE: D2L ch.5 p.211{{% /comment %}}

Sa dérivée vaut 0 pour une entrée négative et 1 pour une entrée positive. En zéro, elle n'est pas dérivable, et la convention retenue est la dérivée à gauche, donc 0. C'est exactement cette dérivée en escalier qui explique son succès : elle **annule** le gradient ou le **laisse passer intact**, sans jamais le rétrécir. Retenez cette phrase, la section 2.6 en fera son argument central.

{{% comment %}}SOURCE: D2L ch.5 p.212{{% /comment %}}

Une variante mérite d'être nommée, la **pReLU**, qui ajoute un terme linéaire pour que l'information continue de passer même quand l'argument est négatif.

{{% comment %}}SOURCE: D2L ch.5 p.212{{% /comment %}}

La **fonction sigmoïde** (*sigmoid*) écrase \(\R\) tout entier dans l'intervalle ouvert \((0, 1)\).

$$
\sigma(x) = \frac{1}{1 + \exp(-x)}
$$

{{% comment %}}SOURCE: D2L ch.5 p.212{{% /comment %}}

C'est une approximation lisse et dérivable d'une fonction à seuil, et sa motivation historique est biologique : un neurone décharge ou ne décharge pas. Elle garde aujourd'hui un usage précis, sur les unités de sortie, quand on veut lire la sortie comme une probabilité en classification binaire. Dans les couches cachées, elle a été très largement remplacée par ReLU, et sa dérivée dit pourquoi.

$$
\frac{d}{dx}\,\sigma(x) = \frac{\exp(-x)}{\left(1 + \exp(-x)\right)^{2}} = \sigma(x)\left(1 - \sigma(x)\right)
$$

{{% comment %}}SOURCE: D2L ch.5 p.213{{% /comment %}}

> [!IMPORTANT]
 **Retenez ce nombre, il revient dans deux sections.** Cette dérivée atteint son maximum en \(x = 0\), et ce maximum vaut **0,25**. Elle tend vers 0 des deux côtés, pour les grandes valeurs positives **comme** pour les grandes valeurs négatives. Multipliez une douzaine de facteurs tous inférieurs à 0,25 et il ne reste rien : \(0{,}25^{12}\) vaut environ \(6 \times 10^{-8}\). C'est le germe exact du gradient évanescent de la section 2.6.

{{% comment %}}SOURCE: D2L ch.5 p.213{{% /comment %}}

La **tangente hyperbolique** (*hyperbolic tangent*) écrase, elle, dans \((-1, 1)\), et sa courbe est symétrique par rapport à l'origine.

$$
\tanh(x) = \frac{1 - \exp(-2x)}{1 + \exp(-2x)}, \qquad
\frac{d}{dx}\tanh(x) = 1 - \tanh^{2}(x)
$$

{{% comment %}}SOURCE: D2L ch.5 p.213-214{{% /comment %}}

Sa dérivée atteint un maximum de **1** en zéro, quatre fois mieux que la sigmoïde, ce qui en fait un choix défendable dans une couche cachée ; elle s'écrase néanmoins aux deux extrémités, comme la sigmoïde. Nous la retrouverons en semaine 9, quand il faudra produire une action continue bornée.

---

## La double lecture : du symbole au code

Voilà la première table de correspondance de la semaine. À gauche les symboles que nous venons de poser, à droite ce que vous tapez.

```python
import torch
import torch.nn as nn

x = torch.randn(8, 4)              # un lot de 8 exemples, 4 entrées chacun

couche_cachee = nn.Linear(4, 5)    # W(1) et b(1), 5 unités cachées
activation = nn.ReLU()             # phi
couche_sortie = nn.Linear(5, 3)    # W(2) et b(2), 3 sorties

h = activation(couche_cachee(x))   # h = phi(W(1) x + b(1))
o = couche_sortie(h)               # o = W(2) h + b(2)
print(h.shape, o.shape)            # torch.Size([8, 5]) torch.Size([8, 3])
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathbf{x}\) | le vecteur d'entrée, ou un lot de vecteurs d'entrée | `x` |
| \(d\), \(h\), \(q\) | nombre d'entrées, d'unités cachées, de sorties | `4`, `5`, `3` |
| \(\mathbf{W}^{(1)}, \mathbf{b}^{(1)}\) | poids et biais de la couche cachée | `couche_cachee.weight`, `couche_cachee.bias` |
| \(\phi\) | la fonction d'activation | `activation`, soit `nn.ReLU()` |
| \(\mathbf{h}\) | les activations cachées | `h` |
| \(\mathbf{W}^{(2)}, \mathbf{b}^{(2)}\) | poids et biais de la couche de sortie | `couche_sortie.weight`, `couche_sortie.bias` |
| \(\mathbf{o}\) | la sortie du réseau | `o` |

Une seule chose à comprendre dans ce fragment, et elle vous servira tout le cours : les équations sont écrites pour **un** vecteur colonne \(\mathbf{x}\), alors que le code travaille sur un lot entier. La dimension 0 d'un tenseur est **toujours** celle du lot, et les couches de `nn` sont faites pour cela : elles appliquent la même transformation à chacun des huit exemples, d'où les formes `[8, 5]` et `[8, 3]`. Souvenez-vous de cette convention, nous la retrouverons en section 2.4 sous une forme beaucoup moins amicale.

{{% comment %}}SOURCE: LAPAN ch.3 p.94{{% /comment %}}
