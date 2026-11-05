---
title: "2.1 Tenseurs et périphérique de calcul"
weight: 2
---

## Le seul objet que PyTorch manipule

Commençons par la brique de base, car tout le reste en est fait. Un **tenseur** (*tensor*) est un tableau multidimensionnel, et rien de plus mystérieux que cela : un nombre est un tenseur à zéro dimension, un vecteur un tenseur à une dimension, une matrice un tenseur à deux dimensions, et au-delà on parle simplement de tenseur de dimension *n*. La **Figure 2-1** montre cette progression, et c'est la seule image dont vous avez besoin pour le reste du cours.

{{< bookfig src="02-01.png" week="02" >}}

{{% comment %}}SOURCE: LAPAN ch.3 p.83{{% /comment %}}

Une mise en garde en passant, parce que le mot est emprunté et que l'emprunt est inexact : le tenseur de l'apprentissage profond n'a qu'une parenté partielle avec le tenseur de l'algèbre tensorielle, qui est une application entre espaces vectoriels. Dans tout ce cours, « tenseur » voudra dire « tableau multidimensionnel sur lequel je peux calculer un gradient ».

{{% comment %}}SOURCE: LAPAN ch.3 p.83{{% /comment %}}

---

## Les types d'élément, et le piège du float64

Un tenseur a une forme, mais aussi un **type d'un tenseur** (*tensor type*) : le type de ses éléments, identique pour tous. PyTorch en reconnaît treize, qui se rangent en quatre familles.

| Famille | Combien | Détail |
| --- | --- | --- |
| flottants | 4 | **deux** variantes de 16 bits (`float16` et `bfloat16`), puis 32 bits et 64 bits |
| complexes | 3 | 32, 64 et 128 bits |
| entiers | 5 | 8 bits signé, 8 bits non signé, puis 16, 32 et 64 bits signés |
| booléens | 1 | les masques |

{{% comment %}}SOURCE: LAPAN ch.3 p.84{{% /comment %}}

Quatre familles, treize types. À quoi s'ajoutent quatre types dits **quantifiés**, qui réutilisent les représentations précédentes pour stocker des valeurs discrétisées. Trois classes portent des noms que vous croiserez souvent : `torch.FloatTensor` pour le flottant 32 bits, `torch.ByteTensor` pour l'entier 8 bits non signé, `torch.LongTensor` pour l'entier 64 bits signé.

{{% comment %}}SOURCE: LAPAN ch.3 p.84{{% /comment %}}

Il existe exactement **trois façons de créer** un tenseur, et je vous conseille de les connaître toutes les trois, parce qu'elles ne mènent pas au même type d'élément.

```python
import numpy as np
import torch

# 1. Appeler le constructeur du type voulu : on donne la forme, pas le contenu.
a = torch.FloatTensor(3, 2)
a.zero_()                       # on initialise explicitement, voir ci-dessous

# 2. Demander à PyTorch de remplir.
b = torch.zeros(3, 2)
c = torch.ones(2, 3)

# 3. Convertir un tableau NumPy ou une liste Python.
d = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
e = torch.tensor(np.zeros((3, 2), dtype=np.float32))     # type imposé à la source
f = torch.tensor(np.zeros((3, 2)), dtype=torch.float32)  # ou converti à l'arrivée
```

{{% comment %}}SOURCE: LAPAN ch.3 p.84{{% /comment %}}

Deux remarques sur ce fragment, et toutes deux ont déjà coûté des soirées à des étudiants. La première concerne la ligne 1 : les versions récentes remplissent de zéros la mémoire réservée par le constructeur, alors que des versions plus anciennes la laissaient dans l'état où elle se trouvait. **Ne vous appuyez jamais sur ce comportement** : écrivez l'initialisation, elle coûte une ligne.

{{% comment %}}SOURCE: LAPAN ch.3 p.84{{% /comment %}}

La seconde concerne les lignes 3. Un tableau créé par `np.zeros(shape=(3, 2))` est en flottant **64 bits**, parce que c'est la convention de NumPy ; le tenseur obtenu par conversion hérite de ce type et vous vous retrouvez avec un `dtype=torch.float64`. En apprentissage profond, la double précision est un surcoût sans contrepartie : la pratique courante est le 32 bits, et parfois le 16 bits. Deux corrections possibles, les deux dernières lignes du fragment : typer le tableau NumPy à la source, ou passer `dtype=` à `torch.tensor`.

{{% comment %}}SOURCE: LAPAN ch.3 p.86{{% /comment %}}

> [!WARNING]
 **Attention : erreur fréquente ici !** Vous rencontrerez beaucoup de code qui écrit `torch.from_numpy(tableau)`. Cette fonction existe toujours, par compatibilité, mais elle est **dépréciée** au profit de `torch.tensor()`. Dans ce cours, nous écrirons toujours `torch.tensor()`, et vous saurez reconnaître l'autre dans un extrait trouvé en ligne.

{{% comment %}}SOURCE: LAPAN ch.3 p.86{{% /comment %}}

---

## Opération en place ou opération fonctionnelle

Voici une distinction de vocabulaire qui a des conséquences très concrètes. Une **opération en place** (*in-place operation*) porte un **tiret bas final** : elle modifie le contenu du tenseur et renvoie l'objet lui-même. La forme **fonctionnelle**, sans tiret bas, laisse l'original intact et renvoie une copie modifiée.

```python
t = torch.ones(3)
t.zero_()            # en place : t vaut maintenant [0., 0., 0.]

u = torch.ones(3)
v = u * 0            # fonctionnelle : v est neuf, u reste [1., 1., 1.]
```

{{% comment %}}SOURCE: LAPAN ch.3 p.85{{% /comment %}}

L'opération en place est moins coûteuse, puisqu'elle évite une allocation : sur de grands tenseurs, cela compte. Son revers est une source de bogues particulièrement pénible : si deux variables désignent le même tenseur et que vous le modifiez en place, la seconde change aussi, sans que rien ne vous le signale. Mon conseil pour les treize semaines à venir : l'opération en place pour initialiser et pour accumuler, la forme fonctionnelle partout ailleurs.

{{% comment %}}SOURCE: LAPAN ch.3 p.85{{% /comment %}}

---

## Le tenseur scalaire et la méthode `item()`

Un **tenseur scalaire** (*scalar tensor*), c'est-à-dire à zéro dimension, est un objet de plein droit en PyTorch, et c'est ce que renvoient toutes les opérations de réduction.

```python
v = torch.tensor([1.0, 2.0, 3.0])
s = v.sum()        # tensor(6.) : un tenseur à zéro dimension, pas un flottant
print(s.item())    # 6.0        : le nombre Python
```

{{% comment %}}SOURCE: LAPAN ch.3 p.87{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, et ce n'est pas un détail d'API.** `item()` est le geste le plus réutilisé de tout le cours. Chaque ligne de journal que vous écrirez pendant treize semaines, chaque valeur envoyée à TensorBoard en section 2.9, chaque récompense moyenne affichée à l'écran passera par un `item()`. La raison est double : un tenseur scalaire garde un lien vers le graphe de calcul, donc l'accumuler dans une liste retient en mémoire tout ce qui a servi à le produire ; et un flottant Python s'affiche, se formate et se compare, alors qu'un tenseur fait semblant.

Pour trouver une opération, deux endroits à regarder, et c'est une bonne nouvelle : le paquet `torch`, où le tenseur est passé en argument, et la classe du tenseur, où l'opération agit sur l'objet appelé. Les noms suivent de très près ceux de NumPy, ce qui fait de votre expérience NumPy un acquis direct : `torch.stack()`, `torch.transpose()`, `torch.cat()`.

{{% comment %}}SOURCE: LAPAN ch.3 p.87{{% /comment %}}

---

## Le périphérique de calcul, et l'idiome à installer tout de suite

Un tenseur ne vit pas nulle part : il occupe la mémoire d'un **périphérique de calcul** (*device*). Historiquement, les tenseurs destinés au processeur graphique vivaient dans des classes séparées, sous `torch.cuda` : `torch.cuda.FloatTensor` est le pendant de `torch.FloatTensor`. Plus généralement, PyTorch raisonne en termes de **moteurs d'exécution** : le processeur central, CUDA pour les cartes NVIDIA, et MPS sur le matériel Apple.

{{% comment %}}SOURCE: LAPAN ch.3 p.87-88{{% /comment %}}

La méthode à retenir est `to(device)`. Elle copie le tenseur vers le périphérique demandé, et renvoie le tenseur inchangé s'il s'y trouve déjà, ce qui la rend sûre à appeler sans vérifier. Le périphérique se désigne par une chaîne (`"cpu"`, `"cuda"`, `"cuda:1"`, l'indice commençant à zéro) ou par un objet `torch.device`, et l'attribut `tensor.device` dit où un tenseur réside.

{{% comment %}}SOURCE: LAPAN ch.3 p.88{{% /comment %}}

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

x = torch.zeros(4, device=device)   # créé directement au bon endroit
y = torch.ones(4).to(device)        # ou déplacé après coup
print(x.device)                     # cpu, ou cuda:0 sur Colab avec GPU
```

L'idiome que je vous demande d'adopter dès maintenant tient en une phrase : **construisez un seul objet `torch.device` au début du programme, et appelez `to(device)` partout ailleurs**. Vos carnets deviennent alors portables entre votre machine et Colab sans une seule ligne de condition, et c'est exactement ce que fait le laboratoire.

{{% comment %}}SOURCE: LAPAN ch.3 p.89{{% /comment %}}
