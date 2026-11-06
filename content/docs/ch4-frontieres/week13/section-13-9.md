---
title: "13.9 Un acteur et un critique dans l'imagination"
weight: 10
---

## Une phrase qui rouvre trois semaines d'un coup

Voici la phrase qui rend la suite possible, et je veux que vous mesuriez ce qu'elle débloque.

**La dynamique latente (*latent dynamics*) définit un processus de décision markovien qui est complètement observé**, parce que les états du modèle sont markoviens. Relisez. Le problème de départ était partiellement observable, et c'est ce qui a imposé l'architecture de la section 13.3. Mais à l'intérieur du modèle, l'observabilité partielle **a déjà été absorbée par l'encodeur** : le couple \((h_k, Z_k)\) contient tout ce que le modèle sait, et le futur imaginé n'en dépend que de lui.

{{% comment %}}SOURCE: DREAMER p.3{{% /comment %}}

Conséquence immédiate et considérable : **à l'intérieur du modèle, tout l'arsenal des semaines 8 à 10 redevient applicable tel quel**. Acteur, critique, valeur d'état, retour à plusieurs pas, reparamétrisation : rien n'a besoin d'être réinventé pour le cas partiellement observable, parce qu'il n'y a plus de cas partiellement observable. On a payé ce privilège une fois, dans l'architecture du modèle, et on l'encaisse maintenant.

---

## Comment une trajectoire imaginée commence, et comment elle avance

Un détail de construction, et il est plus important qu'il n'en a l'air.

Une trajectoire imaginée **ne part pas de rien**. Elle part d'un état du modèle \(Z_t\) obtenu en encodant une séquence **réelle**, tirée des données déjà collectées. Autrement dit : l'imagination est **branchée sur du vécu**. On prend un instant qui a réellement eu lieu, on en calcule le latent, et à partir de là on invente \(H\) pas, \(H\) étant ici l'**horizon d'imagination** (*imagination horizon*). Cela tient le modèle près des régions qu'il connaît, et ce sera exactement l'argument de la section 13.16 dans le cas hors ligne.

Ensuite, trois lois suffisent à avancer : la transition apprise, le modèle de récompense, et l'acteur.

$$
Z_k \sim p_\theta(Z_k \mid Z_{k-1}, a_{k-1}), \qquad
r_k \sim p_\theta(r_k \mid Z_k), \qquad
a_k \sim \pi_\phi(a_k \mid Z_k)
$$

{{% comment %}}SOURCE: DREAMER p.3{{% /comment %}}

Notez que le modèle d'**observation** n'apparaît pas. Comme pour le planificateur de la section 13.5, imaginer ne consiste jamais à produire des images : on reste dans le latent du début à la fin.

---

## L'acteur, le critique, et les trois jeux de paramètres

**L'intuition.** Deux réseaux, et vous les connaissez tous les deux. Un **acteur**, qui propose une action en regardant un état latent, et qu'on entraîne à maximiser le retour imaginé. Un **critique**, qui chiffre ce que vaut un état latent, et qu'on entraîne à prédire le retour imaginé. Chacun poursuit une cible que l'autre déplace : l'acteur maximise une estimation que le critique révise, le critique poursuit une valeur que l'acteur modifie en changeant de comportement. C'est de l'**itération de politique**, et elle a la forme de la semaine 8, à cela près qu'elle tourne entièrement dans un monde inventé.

**L'équation.** L'acteur et le critique, avec leurs paramètres respectifs.

$$
a_k \sim \pi_\phi(a_k \mid Z_k), \qquad
\hat v_\psi(Z_k) \;\approx\; \E_{p_\theta,\, \pi_\phi}\!\left[\sum_{j=k}^{t+H} \gamma^{\,j-k} r_j\right]
$$

{{% comment %}}SOURCE: DREAMER éq. 2 p.4{{% /comment %}}

Avant d'aller plus loin, le tableau des trois jeux de paramètres, promis dans l'introduction. Ce cours en avait deux ; cette moitié de semaine en a trois, et c'est la seule fois où cela arrive.

| Paramètres | Ce qu'ils paramètrent | L'équivalent dans ce cours |
| --- | --- | --- |
| \(\theta\) | tout le **modèle du monde** : cellule récurrente, loi a priori, encodeur, décodeur, tête de récompense | aucun équivalent avant la semaine 12 |
| \(\phi\) | l'**acteur** \(\pi_\phi(a \mid z)\) | le \(\theta\) de la politique des semaines 8 à 10 |
| \(\psi\) | le **critique** \(\hat v_\psi(z)\) | le \(\mathbf{w}\) de la valeur des semaines 7 à 10 |

> [!WARNING]
 **Trois jeux de paramètres, et une seule règle à retenir : ils ne descendent jamais le même gradient.** Le modèle \(\theta\) est entraîné par la borne variationnelle de la section 13.4, sur des données réelles. L'acteur \(\phi\) est entraîné à maximiser un retour imaginé. Le critique \(\psi\) est entraîné à prédire ce même retour imaginé. Trois objectifs, trois optimiseurs, et surtout : **le modèle du monde est gelé pendant qu'on apprend le comportement**. J'y reviens en section 13.11, parce que c'est ce qui rend l'ensemble calculable.

---

## La forme de l'acteur, et la reparamétrisation de la semaine 10

L'acteur est une gaussienne passée dans une tangente hyperbolique, ce qui borne l'action dans \([-1, 1]\). Vous avez déjà écrit exactement cela en semaine 9, pour la politique stochastique à entropie maximale, et en semaine 10 pour la raison qui suit.

**L'équation.** L'action est une fonction **déterministe** de la sortie du réseau et d'un bruit tiré indépendamment :

$$
a_k = \tanh\!\big(\mu_\phi(Z_k) + \sigma_\phi(Z_k)\,\epsilon\big), \qquad \epsilon \sim \mathcal{N}(0,\, \mathbb{I})
$$

{{% comment %}}SOURCE: DREAMER éq. 3 p.4{{% /comment %}}

Et voici ce que cette écriture achète, qui est tout le sujet de la section 13.11 : parce que \(\epsilon\) est tiré **en dehors** du réseau, le chemin de \(\phi\) à \(a_k\) ne contient aucun tirage aléatoire. Le gradient peut donc **traverser l'échantillonnage**, ce qui serait impossible si l'on écrivait « tirer \(a_k\) dans la loi \(\pi_\phi\) ». C'est la **reparamétrisation**, et elle est ici la condition d'existence de la méthode, pas une astuce de variance.

---

## Le code des deux réseaux et du déroulement imaginé

**Le code.** L'acteur, le critique, et la fonction qui produit une trajectoire imaginée. Notez l'absence de `no_grad` : ici, tout est dérivable, et c'est voulu.

```python
import torch
import torch.nn as nn


class Acteur(nn.Module):
    """pi_phi(a | z) : gaussienne reparametree, bornee par une tanh."""

    def __init__(self, dim_etat, dim_a):
        super().__init__()
        self.corps = nn.Sequential(
            nn.Linear(dim_etat, 300), nn.ELU(),
            nn.Linear(300, 300), nn.ELU(),
            nn.Linear(300, 2 * dim_a))

    def forward(self, etat):
        moyenne, brut = self.corps(etat).chunk(2, dim=-1)
        ecart = torch.nn.functional.softplus(brut) + 1e-4
        bruit = torch.randn_like(moyenne)               # epsilon, tire DEHORS
        return torch.tanh(moyenne + ecart * bruit)      # le gradient traverse


class Critique(nn.Module):
    """v_psi(z) : la valeur d'etat du latent."""

    def __init__(self, dim_etat):
        super().__init__()
        self.corps = nn.Sequential(
            nn.Linear(dim_etat, 300), nn.ELU(),
            nn.Linear(300, 300), nn.ELU(),
            nn.Linear(300, 1))

    def forward(self, etat):
        return self.corps(etat).squeeze(-1)


def imaginer(modele, acteur, h0, z0, horizon=15):
    """Deroule H pas dans le modele, en partant d'un etat REEL encode.

    Rend les etats imagines et les recompenses predites, AVEC leur graphe
    de calcul : c'est ce graphe que la section 13.11 va remonter.
    """
    h, z = h0, z0
    etats, recompenses = [], []
    for _ in range(horizon):
        etat = torch.cat([h, z], dim=-1)                # l'etat du modele
        a = acteur(etat)                                # pi_phi(a | z)
        h, prior, _ = modele.avancer(h, z, a, enc_obs=None)
        z = prior.rsample()                             # rsample, pas sample
        etats.append(torch.cat([h, z], dim=-1))
        recompenses.append(modele.tete_recompense(h, z).squeeze(-1))
    return torch.stack(etats), torch.stack(recompenses)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\pi_\phi(a \mid z)\) | l'acteur ; une **politique**, jamais une valeur d'action | `Acteur` |
| \(\hat v_\psi(z)\) | le critique ; le \(\hat v(s,\mathbf{w})\) de la semaine 7 | `Critique` |
| \((h_k, Z_k)\) | l'état du modèle, les deux parts concaténées | `etat` |
| \(\epsilon \sim \mathcal{N}(0,\mathbb{I})\) | le bruit de la reparamétrisation | `torch.randn_like(moyenne)` |
| \(\tanh(\mu_\phi + \sigma_\phi \epsilon)\) | l'action bornée | la valeur rendue par `Acteur.forward` |
| \(r_k\) | récompense **prédite**, non reçue | `recompenses` |
| \(H\) | horizon d'**imagination**, quinze | `horizon` |
| \(Z_t\) initial | latent d'un instant **réel**, tiré des données | `z0` |

> [!WARNING]
 **Deux lignes de ce code décident si la méthode fonctionne, et elles se ressemblent beaucoup.** `z = prior.rsample()` et non `prior.sample()` : la première version fait passer le gradient à travers le tirage du latent, la seconde le coupe net. Et `bruit = torch.randn_like(moyenne)` à l'intérieur du `forward` de l'acteur, plutôt qu'un appel à une loi `Normal(...).sample()` : même raison. Si vous écrivez `sample` au lieu de `rsample` à l'un de ces deux endroits, le code tourne, la perte descend, et **l'acteur n'apprend rien de la dynamique** : il ne reçoit plus qu'un gradient sur le premier pas. C'est un bogue silencieux, et c'est le plus coûteux de cette section.

---

## La forme d'une itération, en six lignes

Pour finir, l'enchaînement complet d'une itération, que les sections 13.10 et 13.11 vont détailler ligne par ligne.

1. Tirer \(B\) séquences de longueur \(L\) dans \(\mathcal{D}\).
2. Calculer les états du modèle le long de ces séquences réelles, avec l'encodeur.
3. Mettre \(\theta\) à jour par l'objectif de la section 13.4, qui est un apprentissage de **représentation**.
4. **Imaginer** \(\{(Z_k, a_k)\}_{k=t}^{t+H}\) à partir de chaque état réel \(Z_t\) obtenu à l'étape 2.
5. Prédire les récompenses et les valeurs le long de ces trajectoires imaginées, et en calculer l'estimateur de retour de la section 13.10.
6. Monter le gradient sur \(\phi\), descendre le gradient sur \(\psi\).

Puis seulement, interagir avec l'environnement réel pour collecter un épisode de plus.

{{% comment %}}SOURCE: DREAMER p.3{{% /comment %}}

Remarquez le rapport des volumes : l'étape 4 produit, à partir d'un lot de cinquante séquences de cinquante pas, **deux mille cinq cents** trajectoires imaginées de quinze pas chacune, soit près de quarante mille transitions d'entraînement du comportement, obtenues sans toucher l'environnement. C'est, chiffrée, la raison d'être de toute la première moitié de la semaine.

---
