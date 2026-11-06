---
title: "7.3 Le graphe de calcul : la victoire la moins chère"
weight: 4
---

## Trois usages du réseau, un seul a besoin de gradients

Nous commençons par l'optimisation la moins intrusive de la semaine : elle ne change aucune valeur calculée, aucun hyperparamètre, aucune structure de programme. Elle supprime simplement du travail inutile.

Rappel de la semaine 2. PyTorch construit, au fil des opérations sur les tenseurs, un **graphe de calcul** qui garde la trace de qui vient de quoi. Quand vous appelez `backward()` sur la perte finale, PyTorch parcourt ce graphe en sens inverse et remplit les gradients de chaque tenseur feuille. C'est ce mécanisme qui vous dispense d'écrire les dérivées à la main.

{{% comment %}}SOURCE: LAPAN ch.9 p.289{{% /comment %}}

Maintenant, comptons combien de fois le réseau est appelé dans une itération de réseau Q profond. Il y en a **trois**, et c'est le diagramme mental de toute la section :

1. **Les valeurs d'action de l'état courant**, pour le lot échantillonné : c'est l'entrée de la perte, et c'est de là que partira la rétropropagation.
2. **Le réseau cible sur l'état suivant**, pour construire l'approximation de Bellman.
3. **L'agent qui choisit une action** à jouer dans l'environnement.

Un seul de ces trois usages a besoin de gradients : le premier.

{{% comment %}}SOURCE: LAPAN ch.9 p.290{{% /comment %}}

Et c'est ici que deux outils qui se ressemblent beaucoup doivent être séparés nettement, parce qu'ils répondent à deux questions complètement différentes.

**`detach()` est une question de correction.** Sur la sortie du réseau cible, le détachement du graphe n'est pas une optimisation : il est indispensable. Sans lui, le gradient remonte dans le modèle **par une direction inattendue**, à travers la cible qui était censée être une constante, et le réseau Q profond peut tout simplement ne pas converger. Vous l'avez déjà écrit en semaine 5, et vous en aviez vu la raison. Quant au troisième usage, le choix de l'action, les gradients y étaient déjà interrompus, mais par un autre moyen : le passage du tenseur en tableau NumPy, qui sort du graphe.

{{% comment %}}SOURCE: LAPAN ch.9 p.290{{% /comment %}}

**`torch.no_grad()` est une question de vitesse.** Le point à comprendre est que le graphe **est construit même si vous n'appelez jamais `backward()`**. PyTorch ne devine pas votre intention : il enregistre les opérations au cas où. Cet enregistrement coûte du temps et de la mémoire, et pour les usages 2 et 3 il ne sert à rien du tout. `torch.no_grad()` dit à PyTorch de ne pas enregistrer.

{{% comment %}}SOURCE: LAPAN ch.9 p.290{{% /comment %}}

> [!WARNING]
 **Ne les échangez jamais, et je vais être précise sur ce qui casse.** Si vous mettez `no_grad()` là où il fallait `detach()`, vous obtiendrez le plus souvent le bon effet **par accident**, parce que `no_grad()` interrompt aussi le graphe, et vous aurez pris l'habitude de ne pas comprendre pourquoi votre cible est constante. Si vous faites l'inverse, `detach()` là où il fallait `no_grad()`, votre programme est **juste** et il construit un graphe entier pour le jeter aussitôt : vous payez sans rien recevoir. Le bon résumé est celui-ci : `detach()` protège un **résultat**, `no_grad()` supprime un **travail**. Qui substitue l'un à l'autre a cassé quelque chose d'invisible, et c'est la pire sorte de casse.

{{% comment %}}SOURCE: LAPAN ch.9 p.290{{% /comment %}}

Deux détails d'usage, parce qu'ils produisent des surprises. D'abord, `torch.no_grad()` s'emploie aussi bien en **décorateur** qu'en **gestionnaire de contexte**, et les deux formes sont équivalentes. Ensuite, et c'est le détail important, son effet est **borné** à la région qu'elle couvre : si vous récupérez le résultat d'une fonction décorée et que vous le multipliez, en dehors, par un tenseur qui demande des gradients, un graphe repart de là. Le tenseur produit sous `no_grad()` n'est pas marqué définitivement, il est seulement né sans parent.

{{% comment %}}SOURCE: LAPAN ch.9 p.290-291{{% /comment %}}

Dans une bibliothèque bien faite, ces deux gestes sont déjà en place et vous ne les voyez pas : l'agent et le calcul de perte de la semaine 6 les contenaient tous les deux. C'est précisément pour cela qu'il faut les connaître. Dès que vous écrivez votre propre agent, ou votre propre environnement comme au volet B de cette semaine, **il devient très facile de les oublier**, et rien ne vous le dira.

{{% comment %}}SOURCE: LAPAN ch.9 p.291{{% /comment %}}

```python
# 1. L'usage qui a besoin du graphe : les valeurs d'action de l'etat courant.
q_lot = reseau(etats).gather(1, actions.unsqueeze(-1)).squeeze(-1)

# 2. La cible. DEUX gestes distincts, et ils ne font pas la meme chose.
with torch.no_grad():                    # VITESSE : aucun graphe n'est construit
    q_suivant = reseau_cible(etats_suivants).max(dim=1)[0]
    q_suivant[termines] = 0.0
cible = recompenses + gamma * q_suivant  # deja hors du graphe
# Si la cible etait calculee HORS du bloc, il faudrait ecrire .detach() :
# CORRECTION, pour empecher le gradient de remonter par la cible.

perte = nn.functional.mse_loss(q_lot, cible)
perte.backward()

# 3. Le choix de l'action : aucun gradient, et on le dit explicitement.
@torch.no_grad()
def choisir(reseau, observations, epsilon, rng):
    q = reseau(observations)                 # un seul passage avant pour tout le lot
    gloutonnes = q.argmax(dim=1).cpu().numpy()
    aleatoires = rng.integers(0, q.shape[1], size=len(gloutonnes))
    masque = rng.random(len(gloutonnes)) < epsilon
    return np.where(masque, aleatoires, gloutonnes)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta(S_t, A_t)\) | valeur d'action estimée, **avec** gradient | `q_lot` |
| \(Q_{\theta^-}(S_{t+1}, a')\) | réseau cible sur l'état suivant | `reseau_cible(etats_suivants)` |
| \(U_t = R_{t+1} + \gamma \max_{a'} Q_{\theta^-}(S_{t+1}, a')\) | cible de la mise à jour | `cible` |
| \(\gamma\) | facteur d'actualisation | `gamma` |
| \(\varepsilon\) | taux d'exploration | `epsilon` |
| région sans gradient | suppression du graphe, pour la vitesse | `torch.no_grad()` |
| rupture du graphe | protection de la cible, pour la correction | `.detach()` |

Et maintenant, le gain mesuré, qui est une leçon d'humilité. Sur ce réseau de convolution de taille modeste, l'écart est d'environ **10 trames par seconde**, c'est-à-dire quelques pour cent. Sur des réseaux plus complexes, notamment récurrents, la même modification a été observée à **50 %** de gain. La leçon honnête est donc que la taille de ce gain est une propriété **du modèle**, pas une constante : vous ne saurez ce que `no_grad()` vous rapporte sur votre code qu'en le mesurant sur votre code.

{{% comment %}}SOURCE: LAPAN ch.9 p.292{{% /comment %}}

> [!NOTE]
 **Gardez ce chiffre en tête, parce que la section 7.6 va le contredire.** Dans le tableau récapitulatif, la variante **sans** `no_grad()` perd 4,3 % de débit et gagne 2,3 % de temps : elle est plus **lente** en trames par seconde et plus **rapide** à résoudre le jeu. Les deux indicateurs pointent en sens opposé, sur une modification qui, par construction, ne peut rien changer au calcul effectué. C'est l'exemple parfait d'un écart plus petit que la dispersion entre exécutions, et c'est pour cela que la section 7.2 vient avant celle-ci.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

---
