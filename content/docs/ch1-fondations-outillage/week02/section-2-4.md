---
title: "2.4 Les briques de `torch.nn`"
weight: 5
---

## Un module, deux gestes, et le réseau du laboratoire

Nous savons créer des tenseurs et obtenir des gradients. Il serait parfaitement possible d'écrire un réseau avec cela seulement, en multipliant des matrices à la main. Personne ne le fait, et pour trois bonnes raisons : les briques de `torch.nn` sont conçues pour la pratique, elles acceptent les **mini-lots** sans qu'on ait à y penser, leurs valeurs par défaut sont raisonnables, et **leurs poids sont correctement initialisés**. Ce dernier point ne vous dira rien avant la section 2.6 ; retenez pour l'instant qu'il vous épargne un piège sérieux.

{{% comment %}}SOURCE: LAPAN ch.3 p.94{{% /comment %}}

Première convention à intégrer, et elle surprend toujours : une **couche linéaire** (*linear layer*) est un objet qu'on **appelle comme une fonction**.

```python
import torch
import torch.nn as nn

l = nn.Linear(2, 5)            # 2 entrées, 5 sorties : W et b sont créés et initialisés
v = torch.tensor([1.0, 2.0])
print(l(v))                    # on applique l'instance, on n'appelle pas une méthode
```

{{% comment %}}SOURCE: LAPAN ch.3 p.94{{% /comment %}}

Toutes les classes de `torch.nn` héritent de `nn.Module`, qui est la classe de base d'un **module** (*module*) et qui fournit cinq services dont vous vous servirez constamment : `parameters()`, un itérateur sur toutes les variables qui demandent des gradients ; `zero_grad()`, qui remet à zéro les gradients de tous ces paramètres ; `to(device)`, qui déplace le module entier sur un périphérique ; `state_dict()` et `load_state_dict()`, pour sauvegarder et recharger les poids.

{{% comment %}}SOURCE: LAPAN ch.3 p.94{{% /comment %}}

> [!WARNING]
 **Attention à l'orthographe de cette méthode, elle est écrite fautivement dans beaucoup de documents.** La méthode s'appelle **`zero_grad()`**, au singulier et sans `s`. Si vous écrivez `zero_grads()`, Python vous répondra par une erreur d'attribut, et vous perdrez dix minutes à chercher une faute de logique là où il n'y a qu'une faute de frappe.

{{% comment %}}SOURCE: LAPAN ch.3 p.94, p.96{{% /comment %}}

---

## Le conteneur séquentiel

Quand un réseau est une simple file de couches, il existe un raccourci : le **conteneur séquentiel** (*sequential container*), qui enchaîne les blocs dans l'ordre où on les donne.

```python
classifieur = nn.Sequential(
    nn.Linear(2, 5),
    nn.ReLU(),
    nn.Linear(5, 20),
    nn.ReLU(),
    nn.Linear(20, 10),
    nn.Dropout(p=0.3),
    nn.Softmax(dim=1),
)
```

{{% comment %}}SOURCE: LAPAN ch.3 p.95{{% /comment %}}

Deux détails de ce fragment valent chacun une soirée de débogage économisée.

Le premier est **`dim=1`**. La fonction softmax doit normaliser sur les dix classes, et pas sur les exemples du lot. Or la **dimension 0 est celle du lot**, comme nous l'avons vu en section 2.2 ; les classes sont donc en dimension 1. Écrire `dim=0` par distraction donne un programme qui tourne, qui n'émet aucun avertissement, et qui apprend quelque chose d'absurde.

{{% comment %}}SOURCE: LAPAN ch.3 p.95{{% /comment %}}

Le second est **le `Softmax` final lui-même**, et c'est un idiome de **classifieur**. Le réseau du laboratoire, lui, aura la forme de \(Q(s,a)\) : une sortie par action, et ces sorties sont des **valeurs**, pas des probabilités. Elles peuvent être négatives, elles n'ont aucune raison de sommer à un. Le réseau du laboratoire s'arrête donc sur une couche linéaire nue, sans softmax et sans sigmoïde. Retenez la forme, c'est celle de tous les réseaux de valeur du cours :

```python
q_net = nn.Sequential(
    nn.Linear(n_obs, 64),
    nn.ReLU(),
    nn.Linear(64, 64),
    nn.ReLU(),
    nn.Linear(64, n_actions),     # une valeur par action, scores bruts
)
```

{{% comment %}}SOURCE: LAPAN ch.3 p.95{{% /comment %}}

---

## Écrire son propre module : exactement deux gestes

`Sequential` ne suffit plus dès qu'un réseau fait autre chose qu'une file : deux têtes, une entrée qui se divise, un traitement conditionnel. Il faut alors écrire sa propre classe, et la bonne nouvelle est qu'il n'y a que **deux gestes** à faire.

Le premier geste consiste à **affecter les sous-modules à des attributs de classe**, dans `__init__`. L'affectation suffit : `nn.Module` les enregistre automatiquement, et ils apparaîtront dans `parameters()` sans que vous ayez rien à appeler. Si vous construisez vos couches par programme, dans une boucle, la méthode `add_module()` fait le même enregistrement explicitement. Le second geste consiste à **redéfinir `forward()`**, la **méthode forward** (*forward method*), qui décrit le chemin des données.

```python
class ReseauQ(nn.Module):
    """Un réseau de la forme de Q(s, a) : une sortie par action."""

    def __init__(self, n_obs: int, n_actions: int, n_cache: int = 64):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            nn.ReLU(),
            nn.Linear(n_cache, n_cache),
            nn.ReLU(),
            nn.Linear(n_cache, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pipe(x)


net = ReseauQ(n_obs=4, n_actions=2)
print(net)                       # nn.Module sait se décrire
sortie = net(torch.randn(8, 4))  # on appelle l'instance, jamais net.forward(...)
print(sortie.shape)              # torch.Size([8, 2])
```

{{% comment %}}SOURCE: LAPAN ch.3 p.96-97{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister : n'appelez jamais `forward()` directement.** Appelez l'instance, comme à la dernière ligne du fragment. `nn.Module` redéfinit `__call__()`, et cette redéfinition fait un certain nombre de choses **avant** d'appeler votre `forward()` : c'est là que se branchent les crochets et que se décide le comportement propre à l'entraînement ou à l'évaluation. Court-circuiter `__call__()` en appelant `forward()` à la main peut donc **donner des résultats faux**, sans message d'erreur. C'est une règle, pas une préférence de style.

{{% comment %}}SOURCE: LAPAN ch.3 p.97{{% /comment %}}

Deux remarques pour finir sur `nn.Module`. Il redéfinit aussi `__str__()` et `__repr__()`, ce qui fait de `print(net)` un outil d'inspection très commode : la structure complète s'affiche, couche par couche, avec les dimensions. Et comme `forward()` est appelée **à chaque lot**, rien n'interdit d'y mettre du contrôle de flux dépendant des données : un `if` sur une forme, une boucle sur une longueur variable. C'est le graphe dynamique de la section 2.3 qui rend cela possible.

{{% comment %}}SOURCE: LAPAN ch.3 p.97-98{{% /comment %}}

Cette même machinerie passe sans changement d'une transformation linéaire à une couche à un réseau résiduel de mille et une couches. C'est très exactement le même objet, avec plus d'attributs ; il n'y a pas de « vrai » PyTorch qui serait réservé aux grands modèles.

{{% comment %}}SOURCE: LAPAN ch.3 p.96{{% /comment %}}

> [!NOTE]
 **Une remarque sur l'outillage, à ranger pour la semaine 6.** Il existe des bibliothèques qui enveloppent la boucle d'entraînement elle-même, pour vous dispenser de l'écrire : vous en croiserez le nom tôt ou tard. Ce cours s'en passe volontairement, parce que les treize semaines qui viennent consistent à **modifier** cette boucle, et qu'on ne modifie bien que ce qu'on a écrit. Nous reviendrons sur la question des bibliothèques spécialisées en semaine 6, quand nous en étudierons une comme objet d'étude.

{{% comment %}}SOURCE: LAPAN ch.3 p.82{{% /comment %}}

---

## Le pont vers la notation du cours

Un mot de notation, et il vaut pour tout le reste du cours. Dans la notation du cours, \(\mathbf{w}\) désigne **le vecteur de tous les paramètres** d'un approximateur de valeur, c'est-à-dire l'ensemble des \(\mathbf{W}^{(l)}\) et des \(\mathbf{b}^{(l)}\) de toutes les couches, mis bout à bout ; \(\mathbf{W}^{(l)}\) désigne la matrice d'**une** couche. En code, ces deux niveaux ont deux adresses différentes.

| Notation | Signification | Code |
| --- | --- | --- |
| \(\mathbf{w}\) | tous les paramètres du réseau, d'un seul bloc | `net.parameters()` |
| \(\mathbf{W}^{(1)}\) | la matrice de poids de la première couche | `net.pipe[0].weight` |
| \(\mathbf{b}^{(1)}\) | le biais de la première couche | `net.pipe[0].bias` |
| \(\hat{v}(s, \mathbf{w})\) | la valeur d'état **approchée** par ce réseau | `net(state)` pour un réseau à une sortie |
| \(Q_\theta(s, a)\) | le réseau de valeurs d'action | `net(state)`, une sortie par action |

Les deux dernières lignes sont les plus importantes, et ce sont celles que nous ne pouvons pas encore remplir honnêtement. Souvenez-vous de la semaine 1 : nous avions \(v_\pi(s)\), la valeur **vraie** d'un état sous une politique. La semaine 4 en construira une **estimation** rangée dans un tableau, \(V(s)\). À partir de la semaine 5, le tableau devient impraticable et nous le remplacerons par le réseau de cette section : c'est le \(\hat{v}(s,\mathbf{w})\) de la table, et c'est à ce moment-là que tout ce que vous apprenez cette semaine devient de l'apprentissage par renforcement. Le réseau du laboratoire est déjà de la bonne forme ; il ne lui manque que de bonnes cibles.
