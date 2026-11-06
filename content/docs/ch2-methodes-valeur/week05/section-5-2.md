---
title: "5.2 La table devient une fonction"
weight: 3
---

## Un tableau de \(\lvert\mathcal{S}\rvert\) cases devient un vecteur de \(d\) poids

Voici le geste de la semaine, et il tient en une phrase. La fonction de valeur approchée n'est plus représentée par une table, mais par une **forme fonctionnelle paramétrée**, munie d'un vecteur de poids \(\mathbf{w} \in \R^d\). On écrit alors \(\hat v(s,\mathbf{w}) \approx v_\pi(s)\), et cette écriture contient déjà tout ce qui va suivre : la valeur d'un état n'est plus **rangée**, elle est **calculée**.

{{% comment %}}SOURCE: SB ch.9 p.219{{% /comment %}}

Cette forme paramétrée peut être n'importe quoi. Une fonction linéaire des caractéristiques de l'état, avec \(\mathbf{w}\) pour vecteur de coefficients. Un réseau de neurones multicouche, avec \(\mathbf{w}\) pour poids des connexions. Un arbre de décision, avec \(\mathbf{w}\) pour seuils de coupure. Ce cours prend le réseau, directement, et ne passe pas par la longue route classique des caractéristiques construites à la main (découpage de l'espace en blocs, pavages, bases polynomiales) : c'est un choix, il est assumé, et il n'est pas gratuit, comme la section 5.6 le montrera.

{{% comment %}}SOURCE: SB ch.9 p.219{{% /comment %}}
{{% comment %}}SOURCE: SB ch.9 §§9.4-9.10 (résumé de chapitre){{% /comment %}}

Et maintenant la phrase qui explique pourquoi cela change tout, et pourquoi cela complique tout.

> [!IMPORTANT]
 **Je dois insister : la généralisation est le but, et elle est aussi la source de toutes les difficultés de la semaine.** On a typiquement \(d \ll \lvert\mathcal{S}\rvert\), beaucoup moins de poids que d'états, et par conséquent **modifier un seul poids modifie la valeur estimée de nombreux états**. C'est exactement ce que nous demandions à la fin de la semaine 4 : une mise à jour faite en un état **se généralise** à d'autres, donc un état jamais visité reçoit quand même une valeur plausible. C'est aussi ce qui rend l'apprentissage potentiellement beaucoup plus puissant, et potentiellement beaucoup plus difficile à maîtriser et à comprendre. Gardez les deux moitiés de cette phrase ensemble : chaque fois que quelque chose ira mal cette semaine, la cause sera ce couplage.

{{% comment %}}SOURCE: SB ch.9 p.219{{% /comment %}}

Retenez la conséquence pratique, parce qu'elle est brutale. Dans une table, une mise à jour est locale : une case, une valeur, aucun effet ailleurs. Dans un réseau, il n'existe **aucune** mise à jour locale. Apprendre que cet écran-ci vaut 3 déplace, un peu, la valeur de tous les écrans que le réseau juge semblables. Quand cela marche, cela s'appelle de la généralisation. Quand cela ne marche pas, cela s'appelle de l'interférence, et nous en verrons un cas pathologique en section 5.6.

---

## Chaque mise à jour est un exemple supervisé

Voici maintenant une relecture qui vaut plus qu'un théorème, parce qu'elle transforme l'apprentissage par renforcement en quelque chose que vous savez déjà faire depuis la semaine 2.

Prenez n'importe quelle mise à jour de la semaine 4 et écrivez-la comme une paire **entrée-sortie**, notée \(s \mapsto u\), où \(s\) est l'état mis à jour et \(u\) la **cible** vers laquelle sa valeur estimée doit se déplacer. Les trois méthodes du cours s'écrivent alors sur trois lignes :

$$
\begin{aligned}
\text{Monte-Carlo :} \quad & S_t \mapsto G_t \\[2pt]
\text{TD(0) :} \quad & S_t \mapsto R_{t+1} + \gamma\,\hat v(S_{t+1},\mathbf{w}_t) \\[2pt]
\text{TD à } n \text{ pas :} \quad & S_t \mapsto G_{t:t+n}
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.9 p.220{{% /comment %}}

Les méthodes d'apprentissage automatique qui apprennent à imiter des paires entrée-sortie de cette façon s'appellent des méthodes d'**apprentissage supervisé**. Nous venons donc, en une ligne, de ramener l'estimation de valeurs à un problème que nous savons résoudre : une régression, avec un réseau, un optimiseur et une perte.

{{% comment %}}SOURCE: SB ch.9 p.220{{% /comment %}}

Sauf que non, pas tout à fait, et les deux réserves qui suivent sont **le programme de la section 5.7**. Je vous demande de les lire deux fois, parce que les réparations de cette semaine répondent à l'une et à l'autre.

La première réserve : l'apprentissage doit être **en ligne**, à partir de données acquises de façon incrémentale, pendant que l'agent interagit. Ce n'est pas le régime habituel d'un problème supervisé, où le jeu de données existe avant l'entraînement et où l'on peut le mélanger à loisir.

La seconde réserve, et c'est la plus grave : la fonction cible est **non stationnaire**. Dans un problème supervisé ordinaire, l'étiquette d'un exemple ne change pas pendant l'entraînement. Ici, regardez la deuxième ligne du bloc d'équations ci-dessus : la cible contient \(\hat v(S_{t+1},\mathbf{w}_t)\), donc elle contient les **poids**. Chaque pas d'apprentissage modifie les poids, donc modifie les cibles, donc modifie ce que le réseau doit apprendre. Une méthode d'optimisation qui ne sait pas suivre une cible mobile est donc d'emblée mal adaptée à l'apprentissage par renforcement : c'est une condition d'admission, et non un détail de réglage.

{{% comment %}}SOURCE: SB ch.9 p.220{{% /comment %}}

> [!WARNING]
 **Attention, vous venez de lire la cause de presque tous les ennuis de cette semaine.** La cible bouge parce que les poids bougent. Un réseau qui poursuit une cible qu'il déplace lui-même n'a aucune raison de converger, et nous verrons en 5.6 qu'il peut même partir à l'infini. Les deux réparations centrales de la section 5.7, le **réseau cible** et le **tampon de rejeu**, ne sont rien d'autre que deux façons de ralentir ce mouvement : l'une gèle la cible pendant mille pas, l'autre casse la corrélation entre les exemples successifs. Retenez-les dès maintenant comme des réponses à cette phrase-ci, et non comme des astuces d'implémentation.

Passons au code, parce que le remplacement de la table par la fonction se voit mieux en PyTorch qu'en prose.

```python
import torch
import torch.nn as nn

# Semaine 4 : une case par état, et il faut avoir visité la case.
#   V = np.zeros(n_etats)

# Semaine 5 : d poids, aucune case, et une réponse pour TOUT état.
class ValeurApprochee(nn.Module):
    """hat v(s, w) : de l'observation vers un scalaire."""

    def __init__(self, taille_obs: int, taille_cachee: int = 128):
        super().__init__()
        self.corps = nn.Sequential(
            nn.Linear(taille_obs, taille_cachee),
            nn.ReLU(),
            nn.Linear(taille_cachee, 1),
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        return self.corps(obs).squeeze(-1)      # forme (lot,) et non (lot, 1)


reseau = ValeurApprochee(taille_obs=4)          # CartPole : 4 nombres
d = sum(p.numel() for p in reseau.parameters())
print(f"d = {d} poids pour une infinité d'états")
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\hat v(s,\mathbf{w})\) | valeur d'état approchée | `reseau(obs)` |
| \(\mathbf{w}\) | le vecteur de poids, l'objet que l'on apprend | `reseau.parameters()` |
| \(d\) | sa dimension | `sum(p.numel() for p in ...)` |
| \(\lvert\mathcal{S}\rvert\) | le nombre d'états | aucune variable : il n'apparaît plus nulle part |
| \(s \mapsto u\) | un exemple supervisé | la paire `(obs, cible)` |

Ce fragment affiche **769**. Sept cent soixante-neuf nombres, et cette fonction a une réponse pour chacun des \(3{,}4 \times 10^{38}\) états de CartPole. Arrêtez-vous une seconde sur le rapport entre ces deux nombres : c'est toute la semaine, et c'est aussi tout le risque de la semaine. Sept cent soixante-neuf nombres ne peuvent évidemment pas représenter fidèlement \(10^{38}\) valeurs indépendantes. Ils ne le prétendent pas. Ils parient sur le fait que les valeurs ne **sont pas** indépendantes, et que des états voisins ont des valeurs voisines.

---

## L'observabilité partielle, et la seule chose que l'approximation ne sait pas faire

Une dernière propriété de ce passage à la fonction, et je la place ici parce qu'elle justifie, formellement, une réparation que la section 5.7 présentera comme un simple bricolage.

L'approximation de la fonction de valeur rend le cadre applicable à des problèmes **partiellement observables**, c'est-à-dire des problèmes où l'état n'est pas entièrement visible par l'agent. La raison est élégante : si la forme paramétrée ne **peut pas** faire dépendre la valeur de certains aspects de l'état, alors c'est exactement comme si ces aspects étaient inobservables. Ne pas pouvoir regarder et ne pas pouvoir utiliser ce qu'on regarde produisent le même agent.

Mais il y a une chose que l'approximation de la fonction de valeur ne sait **pas** faire, et il faut l'énoncer nettement : elle ne peut pas **augmenter la représentation de l'état avec le souvenir des observations passées**. Un réseau qui reçoit l'écran courant reçoit l'écran courant, point. Si l'information utile n'est pas dans cette observation, aucune architecture ne la fera apparaître.

{{% comment %}}SOURCE: SB ch.9 p.219{{% /comment %}}

Gardez cette phrase en réserve. En section 5.7, nous découvrirons qu'une image de Pong ne dit pas dans quel sens la balle se déplace, et nous empilerons quatre trames pour le savoir. Cet empilement passe souvent pour un bricolage d'ingénieur. C'en est un, mais c'en est un **nécessaire** : il n'existe aucun moyen de faire émerger du mouvement d'une image fixe, et donc aucun moyen d'éviter de le fournir dans l'observation elle-même.

---
