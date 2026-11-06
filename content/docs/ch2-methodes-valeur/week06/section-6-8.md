---
title: "6.8 Défaut nº3, une seule tête : l'architecture duale"
weight: 9
---

## Deux têtes, et la contrainte sans laquelle la séparation n'existe pas

Troisième défaut, et c'est le seul des cinq qui ne touche **ni** la perte, **ni** le tampon, **ni** l'exploration. Il touche l'architecture du réseau, et rien d'autre dans le programme ne bouge.

Reprenons le défaut tel que je l'avais énoncé. Rien, dans un réseau à une sortie par action, ne lui permet de dire « cet état est mauvais quoi que je fasse » une fois pour toutes. Imaginez une situation de jeu où la balle est perdue : toutes les actions valent à peu près la même chose, c'est-à-dire pas grand-chose. Notre réseau doit apprendre cette mauvaise nouvelle **séparément pour chaque action**, et il doit la réapprendre pour chaque état voisin. C'est du gâchis, et c'est un gâchis structurel.

L'idée de la réparation part d'une identité que vous connaissez depuis la semaine 4, sous un autre nom. La valeur d'une action se décompose en la valeur de l'état plus un terme :

$$
Q(s,a) \;=\; V(s) + A(s,a)
$$

Cette égalité est une **définition** : \(A(s,a)\) est simplement l'écart, ce que l'action \(a\) rapporte de plus, ou de moins, que la moyenne de ce que vaut l'état. Ce terme s'appelle l'**avantage** (*advantage*), il peut être positif ou négatif, et son amplitude n'est bornée par rien.

{{% comment %}}SOURCE: LAPAN ch.8 p.264{{% /comment %}}

L'idée de l'**architecture duale** (*dueling architecture*) est de rendre cette séparation **explicite dans le réseau**. Au lieu d'une tête qui produit \(\lvert\mathcal{A}\rvert\) valeurs d'action, on en met deux, branchées sur le même corps : l'une produit **un seul nombre**, la valeur de l'état, l'autre produit un vecteur de la taille de l'ensemble des actions, les avantages. Les bénéfices annoncés sont une meilleure stabilité, une convergence plus rapide, et de meilleurs résultats sur Atari.

{{% comment %}}SOURCE: LAPAN ch.8 p.264, p.265{{% /comment %}}

La **Figure 6-4** met les deux architectures l'une au-dessus de l'autre : même corps de convolutions, puis un seul chemin dans le cas ordinaire, deux chemins recombinés dans le cas duel.

{{< bookfig src="06-04.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.265{{% /comment %}}

---

## Sans la contrainte, la décomposition n'existe pas

Cette sous-section est la plus importante de la section, et elle tient en un exemple à quatre nombres.

Supposons que le réseau duel doive représenter, pour un état donné, les quatre valeurs d'action \(Q(s,\cdot) = [1, 2, 3, 4]\). Posons la question : que vont produire ses deux têtes ?

Première réponse possible : \(V(s) = 0\) et \(A(s,\cdot) = [1, 2, 3, 4]\). La somme est juste, les quatre valeurs d'action sont exactes, la perte est nulle, le réseau est content. Et c'est **complètement faux**, au sens où la quantité notée \(V(s)\) n'est pas la valeur de l'état : la valeur de l'état n'est pas zéro, puisque toutes les actions y rapportent entre 1 et 4.

Deuxième réponse possible : \(V(s) = 100\) et \(A(s,\cdot) = [-99, -98, -97, -96]\). Somme juste, perte nulle, et absurdité complète.

Il y a donc une **infinité** de décompositions compatibles avec les mêmes valeurs d'action, et rien dans la perte ne distingue la bonne. On dit que la décomposition n'est pas **identifiable**. Et un réseau qui n'est pas contraint prendra n'importe laquelle de ces solutions, ce qui ruine tout le bénéfice attendu : si \(V(s)\) n'est pas la valeur de l'état, apprendre \(V(s)\) une fois pour toutes n'apprend rien d'utile.

{{% comment %}}SOURCE: LAPAN ch.8 p.265{{% /comment %}}

La réparation consiste à ajouter **une** contrainte, et une seule suffit : on exige que la moyenne des avantages sur les actions soit nulle. C'est la **contrainte de moyenne nulle de l'avantage** (*zero-mean advantage constraint*), et elle porte à elle seule tout l'intérêt de la méthode. Avec cette contrainte, la décomposition de \([1,2,3,4]\) devient unique : \(V(s) = 2{,}5\) et \(A(s,\cdot) = [-1{,}5,\, -0{,}5,\, 0{,}5,\, 1{,}5]\). La valeur de l'état est devenue la **moyenne** de ses valeurs d'action, et les avantages sont devenus des écarts à cette moyenne, ce qui est exactement le sens que le mot « avantage » doit avoir.

{{% comment %}}SOURCE: LAPAN ch.8 p.265{{% /comment %}}

On impose la contrainte en soustrayant la moyenne à l'intérieur du réseau, ce qui ramène mécaniquement la moyenne des avantages à zéro. L'équation que le réseau calcule n'est donc plus une simple somme, c'est :

$$
Q(s,a) \;=\; V(s) + A(s,a) - \frac{1}{N}\sum_{k} A(s,k)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.265{{% /comment %}}

où \(N\) est le nombre d'actions et où la somme porte sur toutes les actions \(k\).

> [!IMPORTANT]
 **Je dois insister : l'architecture duale sans la soustraction de la moyenne n'est pas une architecture duale, c'est un réseau à deux têtes qui ne sépare rien.** Si vous ne retenez qu'une phrase de cette section, prenez celle-là. La partie intéressante de la méthode n'est pas d'avoir deux chemins, c'est la contrainte qui rend le découpage unique. Et c'est un schéma de raisonnement que vous reverrez partout en apprentissage automatique : dès qu'on écrit une quantité comme une somme de deux quantités apprises, il faut dire ce qui empêche l'une d'absorber l'autre.

---

## Le code, et la dimension qui porte l'équation

Voici le réseau. Il tient en une quinzaine de lignes et une seule mérite un paragraphe.

```python
class ReseauDuel(nn.Module):
    """Deux têtes à partir du même corps, et la contrainte au point de jonction."""

    def __init__(self, taille_obs: int, n_actions: int, largeur: int = 128,
                 largeur_tete: int = None):
        super().__init__()
        # Les têtes sont MOITIÉ moins larges que le corps : deux chemins, et
        # un nombre total de paramètres comparable au réseau de référence.
        largeur_tete = largeur_tete or largeur // 2
        self.corps = nn.Sequential(
            nn.Linear(taille_obs, largeur), nn.ReLU(),
        )
        # Tête de VALEUR : une seule sortie, quel que soit le nombre d'actions.
        self.tete_valeur = nn.Sequential(
            nn.Linear(largeur, largeur_tete), nn.ReLU(),
            nn.Linear(largeur_tete, 1),
        )
        # Tête d'AVANTAGE : une sortie par action.
        self.tete_avantage = nn.Sequential(
            nn.Linear(largeur, largeur_tete), nn.ReLU(),
            nn.Linear(largeur_tete, n_actions),
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        corps = self.corps(obs)
        valeur = self.tete_valeur(corps)            # (lot, 1)
        avantage = self.tete_avantage(corps)        # (lot, n_actions)
        # dim=1 est l'axe des ACTIONS : une moyenne par échantillon du lot.
        return valeur + avantage - avantage.mean(dim=1, keepdim=True)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(V(s)\) | la valeur de l'état, un scalaire | `valeur`, forme `(lot, 1)` |
| \(A(s,\cdot)\) | les avantages, un par action | `avantage`, forme `(lot, n_actions)` |
| \(\frac{1}{N}\sum_k A(s,k)\) | la moyenne des avantages | `avantage.mean(dim=1, keepdim=True)` |
| \(N\) | nombre d'actions | la taille de `dim=1` |
| \(Q(s,a)\) | la valeur d'action recomposée | la valeur de retour |

Le paragraphe promis porte sur `dim=1`, et c'est la ligne la plus facile à écrire de travers de toute la semaine. Le tenseur des avantages a la forme `(lot, n_actions)` : la dimension 0 est celle des échantillons du lot, la dimension 1 est celle des actions. Moyenner sur la dimension 1, c'est produire **une** moyenne par échantillon, c'est-à-dire exactement le \(\frac{1}{N}\sum_k A(s,k)\) de l'équation, qui dépend de l'état. Moyenner sur la dimension 0 produirait une moyenne par action sur tout le lot, ce qui n'a aucun sens dans l'équation et ce qui, pourtant, s'écrit en changeant un caractère. Le `keepdim=True` conserve une dimension de taille 1 pour que la soustraction se diffuse correctement sur les actions.

{{% comment %}}SOURCE: LAPAN ch.8 p.267{{% /comment %}}

Un dernier détail, et c'est un détail de **méthode expérimentale** qui mérite d'être copié. Une architecture duale a deux chemins, donc plus de paramètres qu'un réseau ordinaire à largeur égale, et une comparaison naïve attribuerait à la méthode un gain qui ne serait que celui d'un réseau plus gros. La pratique consiste donc à **réduire la largeur des couches cachées** de chaque chemin, de façon que le nombre total de paramètres reste comparable : sur l'architecture Atari de la semaine 5, cela veut dire passer de 512 à 256 dans les deux chemins. Le fragment ci-dessus applique le même principe à l'échelle de CartPole, avec des têtes deux fois moins larges que le corps, et le volet B du laboratoire vous fera vérifier le résultat par une assertion. La comparaison devient alors **équitable par construction**, et c'est tout l'intérêt de la manœuvre.

{{% comment %}}SOURCE: LAPAN ch.8 p.266{{% /comment %}}

Les résultats, enfin. La convergence est plus rapide que celle de la référence, et le réglage des hyperparamètres n'a rien apporté de plus, ce qui est plutôt bon signe : la méthode n'a pas besoin d'être choyée. Et il existe un diagnostic analogue à celui de la section 6.7, qui consiste à suivre, sur un ensemble d'états fixé, la moyenne des avantages et la moyenne de la valeur. La **Figure 6-5** le montre : l'avantage moyen reste collé à zéro, à quelques centièmes près, tandis que la valeur, elle, croît franchement pendant l'entraînement.

{{< bookfig src="06-05.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.267-268{{% /comment %}}

C'est la contrainte rendue visible. Et c'est une vérification que je vous recommande d'ajouter à tout réseau duel que vous écrirez : si l'avantage moyen dérive loin de zéro, la soustraction est mal branchée, et vous le saurez en une courbe plutôt qu'en trois jours.

---
