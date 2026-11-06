---
title: "7.11 Les modèles et la boucle, délibérément ennuyeux"
weight: 12
---

## L'algorithme est devenu une configuration

Cette section est courte, et sa brièveté **est** son enseignement. Je vous préviens donc avant de commencer : si vous la trouvez ennuyeuse, c'est exactement l'effet recherché.

Deux architectures sont proposées, et toutes les deux sont **duales** au sens de la semaine 6. Toutes les deux sont entraînées par **double DQN** avec un dépliage de Bellman à **deux étapes**. Le reste du processus est celui d'un réseau Q profond classique. Autrement dit : **tout ce qui est algorithmique dans cette moitié de semaine, vous l'avez construit la semaine dernière, et rien n'y est modifié.**

{{% comment %}}SOURCE: LAPAN ch.10 p.316{{% /comment %}}

Le premier modèle est entièrement connecté et travaille sur l'observation plate. Il a une particularité qui vaut d'être notée : ses deux branches, celle de la valeur et celle de l'avantage, sont **complètement indépendantes** depuis l'entrée. Il n'y a pas de tronc commun. Chacune est une pile de trois couches linéaires avec des unités linéaires rectifiées entre elles ; l'une se termine sur une sortie unique, l'autre sur une sortie par action. Puis la recombinaison duale habituelle :

$$
Q(s,a) = V(s) + A(s,a) - \frac{1}{|\mathcal{A}|}\sum_{a'} A(s,a')
$$

Vous avez démontré en semaine 6 pourquoi la soustraction de la moyenne est indispensable, et pourquoi sans elle la décomposition n'existe pas. Rien n'a changé.

{{% comment %}}SOURCE: LAPAN ch.10 p.317{{% /comment %}}

Le second modèle travaille sur la représentation en matrice, et il commence par un **extracteur partagé** de deux couches de convolution à une dimension, de noyau 5 et de 128 canaux, suivi d'un aplatissement. La taille après aplatissement est obtenue par un passage avant à blanc sur un tenseur factice, ce qui est le réflexe d'implémentation de la semaine 2 : on ne calcule pas cette dimension à la main, on la demande à la bibliothèque. Puis deux têtes à deux couches, et la même recombinaison duale.

{{% comment %}}SOURCE: LAPAN ch.10 p.317-318{{% /comment %}}

```python
# modeles.py : rien de nouveau depuis la semaine 6, et c'est le propos.
import torch
import torch.nn as nn

class DqnDuelPlat(nn.Module):
    def __init__(self, taille_obs, n_actions):
        super().__init__()
        def branche(sortie):
            return nn.Sequential(
                nn.Linear(taille_obs, 512), nn.ReLU(),
                nn.Linear(512, 512), nn.ReLU(),
                nn.Linear(512, sortie))
        self.valeur = branche(1)              # V(s)
        self.avantage = branche(n_actions)    # A(s, .)

    def forward(self, x):
        v = self.valeur(x)
        a = self.avantage(x)
        return v + (a - a.mean(dim=1, keepdim=True))   # <- la contrainte, une ligne

class DqnDuelConv1D(nn.Module):
    def __init__(self, forme, n_actions):
        super().__init__()
        self.extracteur = nn.Sequential(
            nn.Conv1d(forme[0], 128, kernel_size=5), nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=5), nn.ReLU(),
            nn.Flatten())
        with torch.no_grad():                  # un passage A BLANC pour la dimension
            taille = self.extracteur(torch.zeros(1, *forme)).shape[1]
        self.valeur = nn.Sequential(nn.Linear(taille, 512), nn.ReLU(),
                                    nn.Linear(512, 1))
        self.avantage = nn.Sequential(nn.Linear(taille, 512), nn.ReLU(),
                                      nn.Linear(512, n_actions))

    def forward(self, x):
        h = self.extracteur(x)
        v = self.valeur(h)
        a = self.avantage(h)
        return v + (a - a.mean(dim=1, keepdim=True))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(V(s)\) | tête de valeur d'état | `self.valeur` |
| \(A(s,a)\) | tête d'avantage | `self.avantage` |
| \(\frac{1}{|\mathcal{A}|}\sum_{a'} A(s,a')\) | contrainte de moyenne nulle | `a.mean(dim=1, keepdim=True)` |
| \(Q(s,a)\) | valeur d'action recombinée | la valeur rendue par `forward` |
| \(b\) | barres dans la fenêtre, donc largeur du tenseur 1-D | `forme[1]` |
| noyau de convolution | 5 barres de contexte par couche | `kernel_size=5` |

Les réglages d'entraînement, maintenant, et je les donne en bloc parce qu'ils serviront de valeurs par défaut au laboratoire : le taux d'exploration décroît **linéairement de 1,0 à 0,1 sur le premier million de pas** ; le tampon de rejeu contient **100 000** transitions et est pré-rempli avec **10 000** avant le premier apprentissage ; la valeur moyenne attribuée par le réseau à un **ensemble fixe d'états témoins** est mesurée tous les **1 000 pas**, exactement comme au volet D de la semaine 6 ; et une validation complète est lancée tous les **100 000 pas**, sur **100 épisodes**, à la fois sur les données d'entraînement et sur les cotations jamais vues, en enregistrant le profit moyen, le nombre moyen de barres et la proportion du temps pendant laquelle une action était détenue.

{{% comment %}}SOURCE: LAPAN ch.10 p.318{{% /comment %}}

> [!TIP]
 **Ce que je veux que vous reteniez de cette section, et ce n'est pas une architecture.** Après six semaines, la couche algorithmique de ce projet est devenue une **configuration**. Deux lignes pour le double DQN, un paramètre pour le dépliage à deux étapes, une classe de réseau au choix. Toute la réflexion de cette moitié de semaine s'est dépensée dans les sections 7.8 à 7.10, c'est-à-dire dans la **formulation du problème**. C'est très exactement la répartition de l'effort que vous rencontrerez en pratique sur un problème appliqué, et c'est une bonne nouvelle : cela veut dire que ce que vous avez appris pendant six semaines est devenu un outil que vous n'avez plus à repenser.

---
