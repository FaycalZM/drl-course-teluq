---
title: "2.3 Gradients, graphe de calcul, rétropropagation"
weight: 4
---

## Une seule ligne de code pour toute la règle de dérivation en chaîne

Nous arrivons au cœur de la semaine, et j'applique ici la **double lecture** du cours : l'intuition, puis l'équation, puis le code et la table qui relie les deux. Prenez cette section lentement. Ce qu'elle contient est la raison pour laquelle l'apprentissage profond est devenu praticable.

---

## 1. L'intuition

Reprenons la table de mixage de l'introduction. Pour tourner les boutons dans le bon sens, il faut savoir, pour chacun d'eux, de combien la perte augmenterait ou diminuerait si on le bougeait d'un cheveu. C'est exactement ce qu'est un **gradient** (*gradient*) : une collection de dérivées partielles, une par paramètre, qui dit pour chaque bouton le sens et la vigueur de l'effet.

Avant la **différentiation automatique** (*automatic differentiation*), ce calcul était à la charge du programmeur : on dérivait la composition à la main, on appliquait la règle de dérivation en chaîne, on implémentait le résultat, et on priait. C'est la raison pour laquelle, pendant des années, changer une architecture était un projet et non une expérience. La différentiation automatique est la fonctionnalité qui a fait basculer le domaine, et vous allez voir qu'elle tient en un appel de méthode.

{{% comment %}}SOURCE: LAPAN ch.3 p.89{{% /comment %}}

L'image à garder est celle de la **Figure 2-4** : un même graphe parcouru dans les deux sens. Les données descendent, couche après couche, jusqu'à la perte, qui les compare à la cible ; puis les gradients remontent, de la perte vers les couches, en sens inverse. Un aller, un retour, et chaque poids sait quoi faire.

{{< bookfig src="02-04.png" week="02" >}}

{{% comment %}}SOURCE: LAPAN ch.3 p.90{{% /comment %}}

Pour que ce retour soit possible, il faut garder trace de ce qui a été calculé à l'aller. Deux écoles se sont affrontées là-dessus, et comme vous lirez du code des deux, autant savoir. Dans un **graphe statique**, on définit le calcul à l'avance, puis la bibliothèque l'optimise avant de l'exécuter : c'était l'approche de TensorFlow avant sa version 2 et de Theano. Dans un **graphe de calcul** (*computation graph*) **dynamique**, aucune déclaration préalable : la bibliothèque enregistre les opérations **au fur et à mesure** qu'elles s'exécutent et déroule cet historique à la demande. C'est l'approche de PyTorch et de Chainer, parfois appelée gradients « de carnet », par analogie avec les notes qu'on prend au vol.

{{% comment %}}SOURCE: LAPAN ch.3 p.90{{% /comment %}}

Le graphe statique est généralement plus rapide, puisque la bibliothèque voit le calcul entier avant de l'exécuter. Le graphe dynamique est plus expressif et beaucoup plus pythonique : vous pouvez mettre une boucle `while` ou un `if` au milieu de votre réseau, et les gradients suivront. Les deux mondes se sont d'ailleurs rapprochés : PyTorch sait compiler un modèle à la volée en noyaux optimisés avec `torch.compile`, et TensorFlow a adopté un mode d'exécution immédiate.

{{% comment %}}SOURCE: LAPAN ch.3 p.90-91{{% /comment %}}

> [!NOTE]
 **Notez bien cette intuition :** le graphe dynamique n'est pas un détail d'implémentation pour notre cours, c'est une commodité quotidienne. En apprentissage par renforcement, la longueur d'un épisode varie, le nombre de pas d'un lot varie, et certaines méthodes changent de calcul selon la valeur d'un drapeau. Avec un graphe construit à l'exécution, tout cela s'écrit en Python ordinaire.

---

## 2. L'équation

Écrivons maintenant ce que la machine fait, sur le plus petit réseau intéressant : une couche cachée, un seul exemple, et un terme de pénalité sur les poids pour que le calcul soit complet. La **propagation avant** (*forward propagation*) consiste à calculer et à **stocker** les variables intermédiaires, de l'entrée vers la sortie.

$$
\mathbf{z} = \mathbf{W}^{(1)}\mathbf{x}, \qquad
\mathbf{h} = \phi(\mathbf{z}), \qquad
\mathbf{o} = \mathbf{W}^{(2)}\mathbf{h}, \qquad
L = l(\mathbf{o}, y), \qquad
J = L + \Omega
$$

{{% comment %}}SOURCE: D2L ch.5 p.220-221{{% /comment %}}

Quatre remarques sur ces cinq égalités. Les biais sont omis pour alléger, ce qui ne change rien au raisonnement. \(L\) est la **perte** sur cet exemple, comparaison entre la sortie \(\mathbf{o}\) et la cible \(y\). \(\Omega\) est un terme de pénalité qui ne dépend **que des poids**, et dont nous n'aurons besoin que d'une propriété, sa dérivée \(\partial\Omega/\partial\mathbf{W}^{(l)} = \lambda\mathbf{W}^{(l)}\) ; nous le retrouverons en section 2.7 sous le nom de dégradation des poids. Enfin \(J = L + \Omega\) est la **fonction objectif** (*objective function*), la quantité réellement minimisée, et c'est elle, pas \(L\), que la rétropropagation dérive.

{{% comment %}}SOURCE: D2L ch.5 p.221{{% /comment %}}

Ces cinq égalités forment un graphe, et c'est celui de la **Figure 2-5**. Sa lecture mérite trente secondes d'attention, car c'est la convention que toute la littérature utilise : les **carrés sont des variables**, les **cercles sont des opérations**, l'entrée se trouve en bas à gauche, la sortie en haut à droite, et les flèches vont vers la droite et vers le haut.

{{< bookfig src="02-05.png" week="02" >}}

{{% comment %}}SOURCE: D2L ch.5 p.221{{% /comment %}}

La **rétropropagation** (*backpropagation*) parcourt ce graphe **en sens inverse** et applique la **règle de dérivation en chaîne** (*chain rule*), en stockant au passage les dérivées partielles intermédiaires. Pour deux fonctions enchaînées, elle s'écrit avec un opérateur \(\mathrm{prod}\) :

$$
\frac{\partial Z}{\partial X} = \mathrm{prod}\!\left(\frac{\partial Z}{\partial Y}, \frac{\partial Y}{\partial X}\right)
$$

{{% comment %}}SOURCE: D2L ch.5 p.221{{% /comment %}}

\(\mathrm{prod}\) multiplie ses arguments après avoir fait les transpositions et les réordonnancements nécessaires ; pour des vecteurs, c'est simplement une multiplication matricielle. Cette notation existe pour une raison très pratique : elle évite de couvrir la page de transposées, ce qui obscurcirait la seule chose à voir, à savoir que **chaque dérivée se construit à partir de la précédente**.

{{% comment %}}SOURCE: D2L ch.5 p.221-222{{% /comment %}}

Voici la chaîne complète pour notre réseau, de la fin vers le début.

{{% comment %}}SOURCE: D2L éq. 5.3.8 à 5.3.14 p.222{{% /comment %}}

$$
\frac{\partial J}{\partial L} = 1 \quad\text{et}\quad \frac{\partial J}{\partial \Omega} = 1
$$

$$
\frac{\partial J}{\partial \mathbf{o}} = \mathrm{prod}\!\left(\frac{\partial J}{\partial L}, \frac{\partial L}{\partial \mathbf{o}}\right) = \frac{\partial L}{\partial \mathbf{o}} \in \R^{q}
$$

$$
\frac{\partial \Omega}{\partial \mathbf{W}^{(1)}} = \lambda \mathbf{W}^{(1)} \quad\text{et}\quad \frac{\partial \Omega}{\partial \mathbf{W}^{(2)}} = \lambda \mathbf{W}^{(2)}
$$

$$
\frac{\partial J}{\partial \mathbf{W}^{(2)}} = \mathrm{prod}\!\left(\frac{\partial J}{\partial \mathbf{o}}, \frac{\partial \mathbf{o}}{\partial \mathbf{W}^{(2)}}\right) + \mathrm{prod}\!\left(\frac{\partial J}{\partial \Omega}, \frac{\partial \Omega}{\partial \mathbf{W}^{(2)}}\right) = \frac{\partial J}{\partial \mathbf{o}} \mathbf{h}^{\top} + \lambda \mathbf{W}^{(2)}
$$

$$
\frac{\partial J}{\partial \mathbf{h}} = \mathrm{prod}\!\left(\frac{\partial J}{\partial \mathbf{o}}, \frac{\partial \mathbf{o}}{\partial \mathbf{h}}\right) = \mathbf{W}^{(2)\top} \frac{\partial J}{\partial \mathbf{o}}
$$

$$
\frac{\partial J}{\partial \mathbf{z}} = \mathrm{prod}\!\left(\frac{\partial J}{\partial \mathbf{h}}, \frac{\partial \mathbf{h}}{\partial \mathbf{z}}\right) = \frac{\partial J}{\partial \mathbf{h}} \odot \phi'(\mathbf{z})
$$

$$
\frac{\partial J}{\partial \mathbf{W}^{(1)}} = \mathrm{prod}\!\left(\frac{\partial J}{\partial \mathbf{z}}, \frac{\partial \mathbf{z}}{\partial \mathbf{W}^{(1)}}\right) + \mathrm{prod}\!\left(\frac{\partial J}{\partial \Omega}, \frac{\partial \Omega}{\partial \mathbf{W}^{(1)}}\right) = \frac{\partial J}{\partial \mathbf{z}} \mathbf{x}^{\top} + \lambda \mathbf{W}^{(1)}
$$

{{% comment %}}SOURCE: D2L ch.5 p.222{{% /comment %}}

Ne cherchez pas à mémoriser ces sept lignes : cherchez à voir leur **mécanique**. On part de \(\partial J/\partial L = 1\), ce qui est trivialement vrai, et chaque ligne suivante réutilise la précédente, en la multipliant par la dérivée locale de l'opération qu'on vient de franchir. Les dimensions suivent : \(\partial J/\partial\mathbf{h}\) et \(\partial J/\partial\mathbf{z}\) vivent dans \(\R^{h}\), \(\partial J/\partial\mathbf{W}^{(2)}\) dans \(\R^{q \times h}\) et \(\partial J/\partial\mathbf{W}^{(1)}\) dans \(\R^{h \times d}\), c'est-à-dire que **le gradient d'une matrice de poids a exactement la forme de cette matrice**. C'est pour cela que l'on peut écrire, en code, « poids moins pas d'apprentissage fois gradient ».

De toute cette chaîne, une seule ligne vous servira tous les jours, et c'est celle qui traverse l'activation :

$$
\frac{\partial J}{\partial \mathbf{z}} = \frac{\partial J}{\partial \mathbf{h}} \odot \phi'(\mathbf{z})
$$

Le symbole \(\odot\) est le produit terme à terme. Lisez cette égalité comme une **porte** : le gradient qui arrive de la couche supérieure est multiplié, composante par composante, par la dérivée de l'activation à l'endroit où l'on se trouvait à l'aller. Si \(\phi'\) vaut 1, la porte est grande ouverte et le gradient passe intact. Si \(\phi'\) vaut 0, la porte est fermée. Et si \(\phi'\) vaut 0,25, le gradient perd les trois quarts de son amplitude **à chaque couche traversée**. Vous venez de comprendre d'avance toute la section 2.6.

{{% comment %}}SOURCE: D2L ch.5 p.222{{% /comment %}}

Deux conséquences avant de passer au code. D'abord, l'aller et le retour sont **interdépendants** : le terme de pénalité a besoin des poids courants, et la ligne qui calcule \(\partial J/\partial\mathbf{W}^{(2)}\) a besoin du \(\mathbf{h}\) produit à l'aller. On ne peut donc pas jeter les variables intermédiaires après la propagation avant : il faut les garder jusqu'à la fin de la rétropropagation.

{{% comment %}}SOURCE: D2L ch.5 p.223{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que cela explique une erreur que vous rencontrerez : l'entraînement consomme beaucoup plus de mémoire que la prédiction.** Toutes les valeurs intermédiaires doivent être retenues jusqu'à ce que les gradients soient calculés, et leur volume est à peu près proportionnel au produit de la **profondeur** du réseau par la **taille du lot**. D'où cette règle empirique : un réseau plus profond entraîné avec de plus grands lots atteint le premier la limite de mémoire. En semaine 5, quand nous tirerons des lots de transitions dans un tampon, ce produit sera le premier chiffre à surveiller.

{{% comment %}}SOURCE: D2L ch.5 p.223{{% /comment %}}

---

## 3. Le code

Maintenant, la partie que je préfère. Tout ce que nous venons d'écrire, PyTorch le fait en une ligne. Voici une session complète, à taper telle quelle, et qui n'utilise que des tenseurs à deux composantes pour que vous puissiez vérifier chaque nombre de tête.

```python
import torch

v1 = torch.tensor([1.0, 1.0], requires_grad=True)
v2 = torch.tensor([2.0, 2.0])

v_sum = v1 + v2              # tensor([3., 3.], grad_fn=<AddBackward0>)
v_res = (v_sum * 2).sum()    # tensor(12., grad_fn=<SumBackward0>)

v1.is_leaf, v2.is_leaf             # (True, True)
v_sum.is_leaf, v_res.is_leaf       # (False, False)
v1.requires_grad, v2.requires_grad # (True, False)
v_sum.requires_grad                # True : la propriété est contagieuse

v_res.backward()

v1.grad    # tensor([2., 2.])
v2.grad    # vide : v2 n'a jamais demandé de gradient
```

{{% comment %}}SOURCE: LAPAN ch.3 p.91-93{{% /comment %}}

La **Figure 2-6** montre le graphe que ces quatre lignes ont construit sans que nous le demandions : deux feuilles, une addition, une multiplication par deux, une somme.

{{< bookfig src="02-06.png" week="02" >}}

{{% comment %}}SOURCE: LAPAN ch.3 p.92{{% /comment %}}

Chaque tenseur porte trois attributs liés aux gradients, et il faut les connaître tous les trois. `grad` contient le gradient calculé, sous la forme d'un tenseur de **même forme** que le tenseur lui-même. `is_leaf` vaut `True` si le tenseur a été construit par l'utilisateur, et `False` s'il a un parent dans le graphe. `requires_grad` dit si l'on veut des gradients pour ce tenseur, et sa valeur par défaut dans les constructeurs est **`False`** : il faut la demander explicitement, comme nous l'avons fait pour `v1`.

{{% comment %}}SOURCE: LAPAN ch.3 p.91{{% /comment %}}

Deux règles à retenir comme des règles, parce qu'elles expliquent la quasi-totalité des surprises.

**Première règle : `requires_grad` est contagieux.** Dès qu'une seule des entrées d'une opération demande des gradients, tous les nœuds situés en aval en demandent aussi. Dans notre session, `v2` ne demande rien, et pourtant `v_sum` demande, parce que `v1` demandait. C'est pour cela qu'il n'y a jamais besoin de marquer les couches intermédiaires d'un réseau : il suffit que les poids soient marqués, ce que `nn` fait pour vous.

{{% comment %}}SOURCE: LAPAN ch.3 p.92{{% /comment %}}

**Seconde règle : les gradients ne sont stockés que sur les feuilles** qui ont `requires_grad=True`. C'est une décision d'économie de mémoire, et elle est parfaitement rationnelle : seuls les paramètres ont besoin de leur gradient pour être mis à jour. Si vous voulez quand même le gradient d'un tenseur intermédiaire, demandez-le avec `retain_grad()` avant l'appel à `backward()`.

{{% comment %}}SOURCE: LAPAN ch.3 p.93{{% /comment %}}

Et maintenant, lisons la valeur, car c'est là que l'équation et le code se touchent. Notre calcul est \(v_{res} = \sum_i 2\,(v1_i + v2_i)\). Dérivons à la main : \(\partial v_{res} / \partial v1_i = 2\) pour chaque composante. C'est bien ce que le code affiche, `tensor([2., 2.])`, et voici la lecture en français : **augmenter n'importe quelle composante de `v1` d'une unité augmente `v_res` de deux**. Un gradient, ce n'est jamais rien d'autre que cela.

{{% comment %}}SOURCE: LAPAN ch.3 p.93{{% /comment %}}

Pourquoi ce choix de ne garder que les gradients des paramètres ? Parce qu'un réseau réel a des millions de paramètres et des centaines d'opérations intermédiaires, et que la seule quantité dont l'optimiseur a besoin est \(\partial J/\partial(\text{poids})\). Les gradients par rapport aux **entrées** restent calculables à la demande, et ils ont de vrais usages, qui ne sont pas au programme de ce cours : fabriquer des exemples adverses, ou apprendre des représentations d'entrée.

{{% comment %}}SOURCE: LAPAN ch.3 p.93{{% /comment %}}

> [!TIP]
 **Le lien à faire, et c'est tout l'objet de la double lecture.** Le `grad_fn=<AddBackward0>` affiché par `v_sum` **est** la trace de l'opération à franchir au retour. Chaque nœud du graphe mémorise la fonction qui saura calculer sa dérivée locale, et `backward()` les enchaîne en remontant. Le \(\phi'(\mathbf{z})\) de notre équation n'apparaîtra **jamais** dans votre code : il est dans le `grad_fn` de la sortie de l'activation. Autrement dit, les sept lignes de la chaîne et l'unique ligne `v_res.backward()` sont le même objet, vu de deux côtés.

{{% comment %}}SOURCE: LAPAN ch.3 p.92{{% /comment %}}

---

## La table de correspondance de la section

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathbf{z}\) | pré-activation de la couche cachée | `z = couche_cachee(x)` |
| \(\mathbf{h}\) | activations cachées | `h = torch.relu(z)` |
| \(\mathbf{o}\) | sortie du réseau | `out_t = net(batch_x_t)` |
| \(y\) | la cible | `batch_y_t` |
| \(L\) | la perte sur le lot | `loss_t` |
| \(J\) | la fonction objectif, perte plus pénalité | `loss_t` également, quand la pénalité est confiée à l'optimiseur |
| \(\partial J / \partial \mathbf{W}^{(1)}\) | gradient par rapport à un paramètre | `couche_cachee.weight.grad`, rempli par `loss_t.backward()` |
| \(\phi'(\mathbf{z})\) | dérivée de l'activation | jamais écrite : elle est dans le `grad_fn` |
| \(\odot\) | produit terme à terme | `*`, avec diffusion |
| \(\lambda\) | force de la pénalité sur les poids | `weight_decay=` de l'optimiseur |

Et trois gestes qui n'ont pas de symbole, mais qui méritent chacun leur ligne, parce que ce sont les trois que vous taperez le plus souvent jusqu'à la semaine 15.

| Geste | Ce qu'il veut dire | Code |
| --- | --- | --- |
| « ce tenseur est une feuille, et je veux son gradient » | il a été créé par moi, pas calculé | `t.is_leaf`, `t.requires_grad` |
| « donne-moi le nombre Python » | sortir du graphe pour journaliser | `t.item()` |
| « gèle cette valeur en constante » | couper le lien avec le graphe parent | `t.detach()` |

Le troisième, `detach()`, est introduit en section 2.8 et utilisé dès la semaine 5. Retenez seulement, pour l'instant, qu'il existe un geste qui transforme un résultat de calcul en simple nombre, du point de vue des gradients.

{{% comment %}}SOURCE: LAPAN ch.3 p.109{{% /comment %}}

{{< colab url="TODO" label="Rejouer la session autograd dans Colab" >}}
