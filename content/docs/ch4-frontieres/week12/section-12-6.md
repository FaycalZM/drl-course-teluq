---
title: "12.6 Apprendre le modèle aussi : un réseau devient trois"
weight: 7
---

## Ce que le modèle de jeu faisait, et qu'il faut maintenant remplacer

Faisons le bilan de ce que la méthode précédente exige du monde, parce que c'est la liste des choses qu'il va falloir fabriquer.

Le modèle de jeu écrit à la main fournissait **trois** services à la recherche. Il donnait les **actions légales** dans une position. Il donnait l'**état suivant** après un coup. Et il donnait le **résultat final** quand la partie s'arrêtait. Ces trois services sont exacts, gratuits, et absolument indispensables : sans eux, il n'y a pas d'arbre à descendre.

{{% comment %}}SOURCE: LAPAN ch.20 p.623 (image){{% /comment %}}

Or presque aucun problème intéressant ne les offre. Personne ne peut écrire les règles exactes d'un jeu vidéo à partir de ses pixels, ni celles d'un bras robotique à partir de ses capteurs. Tant que la recherche a besoin d'un simulateur exact et réinitialisable, elle reste cantonnée aux jeux de plateau, et c'est une limitation sévère.

La méthode de cette section lève cette limitation, et c'est l'un des résultats les plus marquants du domaine. Elle supprime l'exigence d'un modèle du jeu **tout en restant une méthode avec modèle** : le modèle n'est plus donné, il est **appris**. Sous le nom de MuZero, elle a égalé puis dépassé les records de la méthode précédente au go, aux échecs et au shogi, et elle a établi l'état de l'art sur **cinquante-sept jeux Atari**, c'est-à-dire sur des environnements où aucune règle n'est disponible et où la méthode de la section 12.3 était inapplicable.

{{% comment %}}SOURCE: LAPAN ch.20 p.622-623 (image 623){{% /comment %}}

---

## Trois fonctions à la place d'un simulateur

**L'intuition.** Si nous ne disposons pas des règles, apprenons des réseaux qui rendent les mêmes services. Mais, et c'est l'idée profonde, **ne leur demandons pas de prédire l'état du monde**. Demandons-leur seulement de prédire ce dont la recherche a réellement besoin : une politique, une valeur, et une récompense. Tout le reste, y compris la représentation interne du monde, est libre.

**L'équation.** Trois fonctions remplacent le simulateur, et ce sont trois réseaux :

$$
h_\theta(o) \to s, \qquad g_\theta(s,a) \to r,\, s', \qquad f_\theta(s) \to \pi,\, v
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.623 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.624 (image){{% /comment %}}

Lisons-les une par une, parce que chacune a un rôle précis.

Le **réseau de représentation** \(h_\theta\) prend l'observation réelle \(o\), celle que l'environnement vous donne, et rend un **état caché** \(s\). Il n'est appelé qu'**une seule fois** par recherche, à la racine : c'est le seul point de contact entre la recherche et le monde réel.

Le **réseau de dynamique** \(g_\theta\) prend un état caché et une action, et rend une **récompense immédiate** et l'**état caché suivant**. C'est lui qui remplace la fonction qui jouait un coup. Il est appelé à chaque fois que la recherche descend d'un niveau.

Le **réseau de prédiction** \(f_\theta\) prend un état caché et rend une **politique** et une **valeur**. C'est exactement le réseau à deux têtes de la section 12.4, à ceci près qu'il regarde un état caché au lieu d'une position de jeu.

La **Figure 12-2** met côte à côte ce que la première méthode demande au monde et ce que la seconde met à sa place, et c'est le résumé de toute la seconde moitié de la semaine : à gauche, un réseau et une flèche qui sort de l'arbre pour aller interroger un simulateur exact ; à droite, trois réseaux et **aucune flèche qui sorte de l'arbre**.

{{< bookfig src="12-02.png" week="12" >}}

La recherche, elle, ne change pas. Quatre phases, trois statistiques par arête, une utilité à maximiser, un signe qui s'inverse : tout ce que la section 12.3 a construit reste valable, à cela près que les nœuds contiennent des états cachés au lieu de positions. La méthode d'origine fait **huit cents recherches par coup**.

{{% comment %}}SOURCE: LAPAN ch.20 p.623-624 (images){{% /comment %}}

---

## Un état caché qui ne ressemble à rien, et pourquoi c'est permis

Nous arrivons au point que je veux que vous reteniez de cette section, parce qu'il est contre-intuitif et que personne ne le dit assez franchement.

**Rien n'oblige \(s^k\) à ressembler à une position de jeu.** Absolument rien. Il n'existe aucun terme de perte qui compare l'état caché à l'état réel du monde, aucune contrainte de reconstruction, aucune supervision. L'état caché est seulement le vecteur qui permet à \(f_\theta\) et \(g_\theta\) de prédire correctement la politique, la valeur et la récompense. Concrètement, c'est un vecteur de **soixante-quatre nombres flottants**, et la question « à quelle position de Puissance 4 correspond-il ? » n'a pas de réponse, pas plus pour vous que pour celui qui a écrit le réseau.

{{% comment %}}SOURCE: LAPAN ch.20 p.629{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 résumé, p.626{{% /comment %}}

> [!WARNING]
 **« État caché » n'est pas « couche cachée », et la confusion est facile.** La semaine 2 a introduit la **couche cachée** (*hidden layer*) d'un réseau : une couche interne, dont la sortie est une activation. L'**état caché** (*hidden state*) de cette semaine est un objet d'une autre nature : c'est la sortie complète d'un réseau \(h_\theta\), traitée comme **l'état d'un modèle du monde**, passée à un autre réseau, modifiée par un troisième, et stockée dans les nœuds d'un arbre. Elle est cachée en ce sens qu'elle n'est jamais comparée à quoi que ce soit d'observable, et non en ce sens qu'elle serait au milieu d'un empilement de couches.

Cette liberté a une conséquence pratique immédiate, et elle est structurelle. Dans la méthode de la section 12.3, deux chemins différents aboutissant à la même position atteignaient le **même** nœud, parce qu'une position était un entier et qu'un dictionnaire indexé par cet entier les réunissait. Ici, deux états cachés obtenus par deux chemins différents ne sont **pas comparables** : ce sont deux vecteurs de soixante-quatre flottants, dont rien ne garantit l'égalité ni même la proximité, et les comparer n'aurait aucun sens. L'arbre cesse donc d'être un dictionnaire indexé par l'état et devient un **graphe d'objets** reliés par des références, où chaque nœud porte son propre état caché. Ce n'est pas une subtilité d'implémentation : c'est la trace, dans votre code, du fait que le modèle n'a plus de sémantique.

{{% comment %}}SOURCE: LAPAN ch.20 p.629{{% /comment %}}

> [!NOTE]
 **Un mot de vocabulaire, pour que vous ne cherchiez pas une difficulté là où il n'y en a pas.** L'opération de la quatrième phase, celle qui remonte la valeur le long du chemin, s'appelle « remontée » dans la première méthode et « rétropropagation » dans la seconde. C'est **la même opération**, et ce n'est en aucun cas la rétropropagation de la semaine 2 : il n'y a ici aucun gradient, aucune dérivée, aucune mise à jour de poids. Ce cours dit **remontée** dans les deux cas, et réserve « rétropropagation » au calcul des gradients.

{{% comment %}}SOURCE: LAPAN ch.20 p.624 (image){{% /comment %}}

---

## Les trois réseaux comme objets, et le peu qu'ils ont de nouveau

**Le code.** Voici les trois réseaux, et la bonne nouvelle est dans leur brièveté : après la semaine 8, presque rien ici n'est nouveau.

```python
import torch
import torch.nn as nn

TAILLE_ETAT_CACHE = 64


class ReseauRepresentation(nn.Module):
    """h_theta : observation reelle -> etat cache.

    Le tronc est celui de la section 12.4, convolutions residuelles comprises ;
    seule la tete change, une couche lineaire vers 64 dimensions.
    """

    def __init__(self, tronc: nn.Module, taille_tronc: int):
        super().__init__()
        self.tronc = tronc
        self.sortie = nn.Linear(taille_tronc, TAILLE_ETAT_CACHE)

    def forward(self, observation):
        return self.sortie(self.tronc(observation).flatten(1))


class ReseauPrediction(nn.Module):
    """f_theta : etat cache -> (logits de politique, valeur).

    Deux tetes a deux couches chacune. C'est le reseau de la section 12.4,
    branche sur un etat cache au lieu d'une position.
    """

    def __init__(self, nb_actions: int, largeur: int = 128):
        super().__init__()
        self.tete_politique = nn.Sequential(
            nn.Linear(TAILLE_ETAT_CACHE, largeur), nn.ReLU(),
            nn.Linear(largeur, nb_actions),
        )
        self.tete_valeur = nn.Sequential(
            nn.Linear(TAILLE_ETAT_CACHE, largeur), nn.ReLU(),
            nn.Linear(largeur, 1),
        )

    def forward(self, etat_cache):
        return self.tete_politique(etat_cache), self.tete_valeur(etat_cache)


class ReseauDynamique(nn.Module):
    """g_theta : (etat cache, action) -> (recompense immediate, etat suivant).

    L'action entre en representation une-parmi-n, CONCATENEE a l'etat cache.
    """

    def __init__(self, nb_actions: int, largeur: int = 128):
        super().__init__()
        self.nb_actions = nb_actions
        self.corps = nn.Sequential(
            nn.Linear(TAILLE_ETAT_CACHE + nb_actions, largeur), nn.ReLU(),
        )
        self.tete_recompense = nn.Linear(largeur, 1)
        self.tete_etat = nn.Linear(largeur, TAILLE_ETAT_CACHE)

    def forward(self, etat_cache, action_une_parmi_n):
        x = self.corps(torch.cat([etat_cache, action_une_parmi_n], dim=1))
        return self.tete_recompense(x), self.tete_etat(x)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(h_\theta(o) \to s\) | représentation : observation réelle vers état caché | `ReseauRepresentation` |
| \(g_\theta(s,a) \to r, s'\) | dynamique : un pas simulé dans l'espace caché | `ReseauDynamique` |
| \(f_\theta(s) \to \pi, v\) | prédiction : politique et valeur depuis l'état caché | `ReseauPrediction` |
| \(s^k\) | état caché, **64 flottants sans interprétation** | `etat_cache`, `TAILLE_ETAT_CACHE` |
| \(a\) | action, en représentation une-parmi-n | `action_une_parmi_n` |
| \(r^k\) | récompense immédiate prédite | sortie de `tete_recompense` |
| \(\pi^k\), \(v^k\) | politique et valeur prédites | sorties de `ReseauPrediction` |

{{% comment %}}SOURCE: LAPAN ch.20 p.629-632{{% /comment %}}

Regardez ce que vous venez de lire : deux perceptrons multicouches à deux couches, une concaténation, et le tronc de convolutions de la section 12.4 réutilisé tel quel. C'est **tout**. La difficulté de cette méthode n'est pas dans ses réseaux, elle est dans la façon de les entraîner, et c'est la section 12.7.

---

## Étendre un nœud, et l'ordre des deux appels

Il reste une opération à écrire, et c'est celle où tout se joue : l'expansion d'un nœud. Elle demande deux appels de réseau, et **l'ordre de ces deux appels n'est pas négociable**.

**L'ordre correct.** Le nœud que nous étendons est atteint depuis son parent par une action. Donc :

1. la **dynamique d'abord** : \(g_\theta(s^{k}, a) \to r^{k+1},\, s^{k+1}\), ce qui produit l'état caché **du nœud** et la récompense de la transition qui y mène ;
2. la **prédiction ensuite**, sur cet état caché : \(f_\theta(s^{k+1}) \to \pi^{k+1},\, v^{k+1}\).

```python
def etendre(noeud, etat_cache_parent, action, reseaux):
    """Cree les enfants d'un noeud, DANS LE BON ORDRE, et rend sa valeur.

    1. la dynamique d'abord : elle produit l'etat cache DU NOEUD ;
    2. la prediction ensuite, sur CET etat cache, jamais sur celui du parent.
    """
    a = une_parmi_n(action, reseaux.nb_actions)

    recompense, etat_cache = reseaux.dynamique(etat_cache_parent, a)   # g_theta
    logits, valeur = reseaux.prediction(etat_cache)                    # f_theta

    noeud.etat_cache = etat_cache
    noeud.recompense = float(recompense)

    probabilites = torch.softmax(logits, dim=1)[0]
    for action_suivante, p in enumerate(probabilites):
        # L'enfant sera joue par l'autre camp : c'est cet attribut qui portera
        # le signe pendant la remontee.
        noeud.enfants[action_suivante] = Noeud(
            prior=float(p), joueur=not noeud.joueur
        )
    return float(valeur)
```

> [!WARNING]
 **L'ordre inverse est une erreur que l'on rencontre dans du code publié, et elle est bien pire qu'un décalage d'un pas.** Supposez que l'on appelle la prédiction **avant** la dynamique, donc sur l'état caché du **parent**. L'état caché et la récompense écrits dans le nœud restent corrects, puisqu'ils viennent de la dynamique. Mais trois choses partent en vrille en même temps. Les **probabilités a priori** inscrites dans les enfants sont \(\pi(\cdot \mid s^{k})\), celles du niveau précédent, donc à chaque profondeur le terme d'exploration de l'utilité est guidé par la politique d'un autre état. La **valeur renvoyée** est \(v(s^{k})\), en retard d'un pas. Et surtout, la remontée combine cette valeur périmée avec la récompense \(r^{k+1}\) du nœud : la récompense et la valeur à laquelle on l'ajoute **ne viennent pas du même instant**, de sorte que la somme télescopique qui doit faire de la remontée un retour est **cassée**, et non simplement décalée. Un décalage se corrige par un décalage ; ceci ne se corrige pas.

Il y a une raison pour laquelle cette erreur survit longtemps dans un code, et elle vaut d'être connue. **La racine est forcément correcte** : elle n'a pas de parent, son état caché vient de \(h_\theta\) appliqué à l'observation réelle, et la prédiction ne peut donc y être appliquée qu'au bon état. Tout fonctionne donc à la racine, qui est l'endroit que l'on inspecte, et l'erreur n'affecte que les niveaux inférieurs, que personne ne regarde. Les symptômes sont une recherche qui semble marcher mais qui apprend mal.

{{% comment %}}SOURCE: LAPAN ch.20 p.633 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.624 (image){{% /comment %}}

**La remontée change, elle aussi, et d'une façon qu'il faut voir.** Dans la méthode de la section 12.3, la remontée ne portait qu'une valeur, parce qu'un jeu de plateau ne paie rien avant la fin. Ici, la dynamique prédit une récompense à **chaque** pas, et la remontée doit donc accumuler un retour :

$$
v \leftarrow r^{k} + \gamma\, v
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.634 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}

à chaque niveau de la remontée, le signe étant toujours décidé par le camp du joueur. Pour Puissance 4, \(\gamma = 1\), ce qui est cohérent avec la section 12.4 : le jeu est déterministe et ne paie qu'à la fin. Mais le mécanisme, lui, est désormais général : avec une récompense à chaque pas et un \(\gamma < 1\), la même remontée fonctionnerait sur un jeu Atari.

```python
def remonter_avec_recompense(chemin, valeur_feuille, joueur_racine, gamma=1.0):
    """Remonte le long du chemin en accumulant les recompenses predites.

    chemin : les noeuds traverses, de la racine vers la feuille.
    """
    valeur = valeur_feuille
    for noeud in reversed(chemin):
        valeur = noeud.recompense + gamma * valeur     # r^k + gamma * v
        # Le signe depend du camp : meme camp que la racine, ou l'autre.
        noeud.somme_valeurs += valeur if noeud.joueur == joueur_racine else -valeur
        noeud.comptage += 1
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(v\) | valeur remontée au niveau courant | `valeur` |
| \(r^{k}\) | récompense prédite par la dynamique à ce nœud | `noeud.recompense` |
| \(\gamma\) | actualisation ; **vaut 1 ici** | `gamma` |
| \(W\), \(N\) | somme des valeurs et comptage du nœud | `noeud.somme_valeurs`, `noeud.comptage` |
| le signe | décidé par le camp du nœud, comme en 12.3 | le test sur `noeud.joueur` |

---
