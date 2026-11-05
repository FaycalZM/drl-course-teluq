---
title: "2.6 Stabilité numérique et initialisation"
weight: 7
---

## Pourquoi un réseau profond peut refuser d'apprendre

Jusqu'ici, tout s'est bien passé. Cette section est celle où je vous montre ce qui casse, parce que c'est en voyant casser qu'on apprend à réparer. Et je vous le dis d'emblée : les trois pathologies qui suivent sont exactement ce que vous observerez en semaine 5, sous la forme bénigne en apparence d'une courbe de récompense qui reste plate et d'une phrase que tous les étudiants finissent par écrire, « mon réseau ne converge pas ».

Reprenons le réseau comme une composition. Un réseau à \(L\) couches calcule

$$
\mathbf{o} = f_L \circ f_{L-1} \circ \cdots \circ f_1(\mathbf{x}), \qquad
\mathbf{h}^{(l)} = f_l\!\left(\mathbf{h}^{(l-1)}\right), \qquad
\mathbf{h}^{(0)} = \mathbf{x}
$$

{{% comment %}}SOURCE: D2L ch.5 p.224{{% /comment %}}

Dérivons par rapport aux poids d'une couche intermédiaire \(l\). La règle de dérivation en chaîne de la section 2.3 donne un **produit de matrices**, une par couche traversée entre \(l\) et la sortie, multiplié par un dernier terme :

{{% comment %}}SOURCE: D2L éq. 5.4.2 p.224{{% /comment %}}

$$
\partial_{\mathbf{W}^{(l)}}\mathbf{o} = \underbrace{\partial_{\mathbf{h}^{(L-1)}}\mathbf{h}^{(L)}}_{\mathbf{M}^{(L)}} \cdots \underbrace{\partial_{\mathbf{h}^{(l)}}\mathbf{h}^{(l+1)}}_{\mathbf{M}^{(l+1)}} \underbrace{\partial_{\mathbf{W}^{(l)}}\mathbf{h}^{(l)}}_{\mathbf{v}^{(l)}}
$$

{{% comment %}}SOURCE: D2L ch.5 p.224{{% /comment %}}

Comptez les facteurs : il y en a \(L - l\). Le gradient d'une couche **profonde** traverse peu de matrices, celui d'une couche **proche de l'entrée** les traverse presque toutes. Or ces matrices n'ont aucune raison d'avoir des valeurs propres bien tempérées : certaines amplifient, d'autres contractent, et un produit de nombreux facteurs peut devenir **énorme** ou **minuscule** avec une rapidité qui surprend toujours.

{{% comment %}}SOURCE: D2L ch.5 p.225{{% /comment %}}

---

## Les deux pathologies, et un nombre qui fait peur

De là, deux modes de défaillance, et ils portent des noms que vous devez connaître. Le **gradient explosif** (*exploding gradient*) produit des mises à jour si grandes qu'elles détruisent le modèle : les poids partent à l'infini en quelques pas, et la perte affiche `nan`. Le **gradient évanescent** (*vanishing gradient*) produit des mises à jour si petites que l'apprentissage s'arrête : la perte ne bouge plus, et rien ne distingue cette situation d'un modèle qui aurait fini d'apprendre.

{{% comment %}}SOURCE: D2L ch.5 p.225{{% /comment %}}

Le coupable classique du second cas est la sigmoïde, et nous avons déjà tous les éléments pour comprendre pourquoi. Son gradient s'évanouit pour les grandes entrées **comme** pour les petites : il n'est appréciable que dans une étroite bande autour de zéro. Si les entrées d'une couche ne tombent pas dans cette bande, et il n'y a aucune raison qu'elles y tombent, le produit sur plusieurs couches s'éteint. C'est l'une des raisons pour lesquelles ReLU, plus stable, est devenue le choix par défaut dans les couches cachées.

{{% comment %}}SOURCE: D2L ch.5 p.225{{% /comment %}}

Quant à l'explosion, une expérience vaut tous les discours. Prenez cent matrices aléatoires gaussiennes de variance 1 et multipliez-les entre elles. Les coefficients du produit atteignent des ordres de grandeur de \(10^{25}\) : on relève par exemple des valeurs comme \(-2{,}9185 \times 10^{23}\) ou \(1{,}3915 \times 10^{25}\). Cent couches, aucune activation pathologique, aucune erreur de code : juste un produit de matrices.

{{% comment %}}SOURCE: D2L ch.5 p.226{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que c'est le crochet vers la semaine 5.** Ces deux pathologies ne sont pas des curiosités de théorie. Elles expliquent la moitié des échecs d'entraînement que vous rencontrerez, et elles sont **silencieuses** : rien ne plante, la boucle tourne, la perte semble simplement « ne pas vouloir ». Quand nous entraînerons un réseau profond sur des images en semaine 5, nous retrouverons les trois mêmes suspects, auxquels s'ajouteront des causes propres à l'apprentissage par renforcement que je ne peux pas encore vous présenter honnêtement.

---

## La brisure de symétrie : le piège que personne ne voit venir

Voici maintenant un problème d'une autre nature, qui n'a rien à voir avec l'amplitude des gradients et tout à voir avec leur **uniformité**.

Les unités cachées d'une couche sont **interchangeables**. Permutez-les, permutez en conséquence les poids qui entrent et qui sortent, et vous obtenez exactement le même réseau : c'est une symétrie de permutation, et elle est parfaitement réelle. Que se passe-t-il alors si l'on initialise tous les poids de \(\mathbf{W}^{(1)}\) à la même constante \(c\) ?

Déroulons. À l'aller, chaque unité cachée reçoit la même combinaison des mêmes entrées, donc produit **la même activation**. Au retour, la rétropropagation attribue à chaque poids de la couche **le même gradient**. Donc la mise à jour est identique pour toutes les unités, qui restent égales. Et cela ne s'arrête jamais : la couche conserve, pour toujours, le comportement d'une couche à **une seule unité**. Vous avez payé 64 unités et vous en utilisez une.

{{% comment %}}SOURCE: D2L ch.5 p.226{{% /comment %}}

> [!WARNING]
 **Attention : la descente de gradient stochastique par mini-lots ne brise pas cette symétrie.** C'est contre-intuitif, puisque les lots sont tirés au hasard, mais l'aléa du tirage ne change rien : à chaque pas, toutes les unités de la couche reçoivent encore le même gradient, parce qu'elles ont encore les mêmes poids. L'aléa doit être **dans l'initialisation**. Curiosité qui annonce la section suivante : l'abandon de neurones, lui, **briserait** la symétrie, puisqu'il désactive les unités indépendamment les unes des autres.

{{% comment %}}SOURCE: D2L ch.5 p.226{{% /comment %}}

C'est pour cela que l'**initialisation des paramètres** (*parameter initialization*) est un sujet et non un détail. Sans schéma explicite, PyTorch applique une initialisation aléatoire par défaut, qui « fonctionne souvent bien en pratique pour des problèmes de taille modérée », ce qui est précisément la situation du laboratoire de cette semaine. Mais « souvent bien » n'est pas « toujours », et il vaut la peine de comprendre ce que fait le schéma standard.

{{% comment %}}SOURCE: D2L ch.5 p.227{{% /comment %}}

---

## L'initialisation de Xavier, en trois pas

L'**initialisation de Xavier** (*Xavier initialization*) répond à une question précise : comment tirer les poids pour que **l'amplitude des signaux ne change pas** en traversant une couche ? Faisons le calcul, il tient en trois pas.

Prenons une couche entièrement connectée **sans non-linéarité**, à \(n_{\mathrm{in}}\) entrées. Sa sortie \(i\) est une somme pondérée :

$$
o_i = \sum_{j=1}^{n_{\mathrm{in}}} w_{ij}\,x_j
$$

Supposons les poids \(w_{ij}\) tirés indépendamment, de moyenne nulle et de variance \(\sigma^{2}\), et les entrées \(x_j\) de moyenne nulle et de variance \(\sigma_x^{2}\), indépendantes des poids. Alors l'espérance de la sortie est nulle, et sa variance se calcule exactement :

$$
\E[o_i] = 0, \qquad
\mathrm{Var}[o_i] = n_{\mathrm{in}}\,\sigma^{2}\,\sigma_x^{2}
$$

{{% comment %}}SOURCE: D2L ch.5 p.227{{% /comment %}}

Premier pas : pour que la variance du signal soit **inchangée** en traversant la couche, il faut \(n_{\mathrm{in}}\sigma^{2} = 1\). Deuxième pas : le même raisonnement, mené sur le chemin du retour, demande que les gradients ne changent pas d'amplitude non plus, et il donne \(n_{\mathrm{out}}\sigma^{2} = 1\). Troisième pas : ces deux conditions ne peuvent pas être satisfaites en même temps, sauf si la couche a autant d'entrées que de sorties. On adopte donc un **compromis**, et c'est là toute la trouvaille.

{{% comment %}}SOURCE: D2L ch.5 p.227-228{{% /comment %}}

{{% comment %}}SOURCE: D2L éq. 5.4.6 et 5.4.7 p.228{{% /comment %}}

$$
\tfrac{1}{2}\left(n_{\mathrm{in}} + n_{\mathrm{out}}\right)\sigma^{2} = 1
\quad\text{ou, de façon équivalente,}\quad
\sigma = \sqrt{\frac{2}{n_{\mathrm{in}} + n_{\mathrm{out}}}}
$$

$$
U\!\left(-\sqrt{\frac{6}{n_{\mathrm{in}} + n_{\mathrm{out}}}},\ \sqrt{\frac{6}{n_{\mathrm{in}} + n_{\mathrm{out}}}}\right)
$$

{{% comment %}}SOURCE: D2L ch.5 p.228{{% /comment %}}

La variante gaussienne tire donc les poids de moyenne nulle et de variance \(2/(n_{\mathrm{in}} + n_{\mathrm{out}})\). La variante uniforme demande un calcul de plus : comme la loi \(U(-a, a)\) a pour variance \(a^{2}/3\), il suffit de résoudre \(a^2/3 = 2/(n_{\mathrm{in}} + n_{\mathrm{out}})\) pour obtenir les bornes données ci-dessus.

{{% comment %}}SOURCE: D2L ch.5 p.228{{% /comment %}}

Écrivons-le une fois à la main, pour voir la formule à l'œuvre. En pratique, PyTorch fournit des fonctions d'initialisation prêtes à l'emploi et vous n'écrirez pas ce fragment, mais je veux que vous ayez vu le lien entre la formule et les deux nombres qu'elle consomme.

```python
import math

with torch.no_grad():                      # on modifie des poids, pas de gradient ici
    for p in net.parameters():
        if p.dim() > 1:                    # les matrices de poids, pas les biais
            n_out, n_in = p.shape          # les deux nombres de la formule
            limite = math.sqrt(6.0 / (n_in + n_out))
            p.uniform_(-limite, limite)    # opération en place : section 2.1
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(n_{\mathrm{in}}\) | nombre d'entrées de la couche | `n_in`, soit `in_features` |
| \(n_{\mathrm{out}}\) | nombre de sorties de la couche | `n_out`, soit `out_features` |
| \(\sigma^{2}\) | variance des poids tirés | implicite : fixée par `limite` |
| \(\sigma_x^{2}\) | variance des entrées de la couche | aucune variable : c'est une hypothèse sur les données |
| \(a\) | borne de la loi uniforme | `limite` |

> [!NOTE]
 **Une honnêteté intellectuelle qui mérite d'être dite.** Toute cette dérivation suppose la couche **linéaire**, sans activation, hypothèse que nos réseaux violent systématiquement puisque c'est tout l'objet de la section 2.2. Et pourtant Xavier fonctionne très bien en pratique. C'est une situation fréquente en apprentissage profond : un raisonnement approximatif donne une recette robuste. Sachez quand vous utilisez une recette, c'est tout ce que je demande.

{{% comment %}}SOURCE: D2L ch.5 p.228{{% /comment %}}

Résumons la section en trois phrases, et ce sont trois phrases de quiz. L'initialisation aléatoire est **indispensable** pour briser la symétrie entre unités. L'initialisation de Xavier rend la variance d'une sortie indépendante du nombre d'**entrées** et la variance d'un gradient indépendante du nombre de **sorties**. ReLU atténue le gradient évanescent, parce que sa dérivée ne rétrécit jamais le gradient qu'elle laisse passer.

{{% comment %}}SOURCE: D2L ch.5 p.228{{% /comment %}}
