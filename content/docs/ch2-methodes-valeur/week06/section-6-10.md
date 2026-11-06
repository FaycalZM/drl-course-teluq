---
title: "6.10 Défaut nº2, le tirage uniforme : le tampon de rejeu priorisé"
weight: 11
---

## S'entraîner davantage sur ce qui surprend, et payer le biais que cela crée

Dernière réparation, et c'est la plus intrusive des cinq : elle touche le tampon, la perte, et la boucle qui les relie.

Reprenons le deuxième défaut. Le tampon de rejeu de la semaine 5 tire **uniformément**. Une transition dont le réseau prédit parfaitement la valeur et une transition qui le prend complètement au dépourvu ont exactement la même chance d'être rejouées. Nous dépensons donc l'essentiel de nos pas d'apprentissage sur des données dont le réseau n'a plus rien à apprendre.

Rappelons-nous d'où vient ce tirage uniforme, parce que c'est une justification sérieuse et que nous allons la contredire : la descente de gradient stochastique suppose des données indépendantes et identiquement distribuées, et le tirage uniforme dans un grand tampon est la façon la plus simple d'en approcher. La méthode de cette section remet en cause cette politique d'échantillonnage, et il faut comprendre qu'elle remet en cause une hypothèse, pas une commodité.

{{% comment %}}SOURCE: LAPAN ch.8 p.257{{% /comment %}}

Le principe du **tampon de rejeu priorisé** (*prioritized replay buffer*) tient en une phrase, et je vous propose de la retenir sous cette forme : « s'entraîner plus sur ce qui surprend ». La surprise, ici, se mesure : c'est la perte que la transition produit dans la mise à jour de Bellman. Une transition dont l'erreur TD est grande est une transition dont le réseau a encore à apprendre ; on la rejouera plus souvent. Le nombre qui porte cette mesure s'appelle la **priorité d'un échantillon** (*sample priority*).

Et la limite de ce principe, immédiatement, parce qu'elle est le reste de la section. Si l'on se concentre sur un petit sous-ensemble du tampon, on perd l'indépendance des données et on finit par surapprendre ce sous-ensemble. Le tirage priorisé est donc un réglage entre deux échecs, et son équation est écrite pour permettre ce réglage :

$$
P(i) \;=\; \frac{p_i^{\,\alpha_{\mathrm{PER}}}}
                {\sum_k p_k^{\,\alpha_{\mathrm{PER}}}}
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.257{{% /comment %}}

\(p_i\) est la priorité de la transition \(i\), et \(\alpha_{\mathrm{PER}}\) est l'exposant qui règle l'agressivité du procédé. Regardez ses deux bornes, parce qu'elles sont la meilleure façon de lire cette formule. Avec \(\alpha_{\mathrm{PER}} = 0\), toutes les puissances valent 1, la probabilité devient uniforme, et on retrouve **exactement** le tampon de la semaine 5. Avec \(\alpha_{\mathrm{PER}} = 1\), la probabilité est proportionnelle à la priorité, et le tirage est maximalement agressif. La valeur de départ usuelle est 0,6, c'est-à-dire plus près de l'uniforme que du proportionnel.

{{% comment %}}SOURCE: LAPAN ch.8 p.257{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur la notation, et c'est la troisième fois cette semaine : cet exposant n'est pas le pas d'apprentissage.** Il s'écrit \(\alpha_{\mathrm{PER}}\), avec son indice, partout et toujours. Dans le code, le pas d'apprentissage s'appelle `learning_rate` et vaut \(10^{-4}\) ; l'exposant du tampon s'appelle `prob_alpha` et vaut 0,6. Les deux vivent dans le même bloc d'hyperparamètres, et c'est précisément pour cette semaine que la page « Notation » du cours porte cette règle.

{{% comment %}}SOURCE: notation.md §5{{% /comment %}}

Un détail d'initialisation, qui est en réalité une décision de conception. Quelle priorité donner à une transition qui vient d'arriver et dont on n'a donc jamais calculé la perte ? On lui donne la priorité **maximale** du tampon. Toute transition neuve est ainsi garantie d'être tirée rapidement au moins une fois, après quoi sa vraie priorité remplace cette valeur provisoire. C'est une ligne de code et cela évite qu'une transition rare reste indéfiniment au fond du tampon.

{{% comment %}}SOURCE: LAPAN ch.8 p.257, p.259{{% /comment %}}

---

## Le biais, et les poids qui le paient

Nous venons de casser quelque chose, et il faut le réparer dans la même section.

En tirant les transitions selon \(P(i)\) plutôt qu'uniformément, nous avons changé la **distribution** des données sur lesquelles la descente de gradient travaille. Nos gradients ne sont plus des estimations non biaisées du gradient que nous voulions descendre : ils sont systématiquement tirés vers les transitions difficiles. C'est un biais, il est introduit volontairement, et il faut le compenser pour que la descente de gradient stochastique garde un sens.

{{% comment %}}SOURCE: LAPAN ch.8 p.257{{% /comment %}}

La compensation est de l'**échantillonnage préférentiel**, celui de la semaine 3, et vous allez reconnaître la structure : puisque nous avons tiré selon la mauvaise distribution, nous repondérons chaque échantillon par le rapport entre celle que nous voulions et celle que nous avons utilisée. Chaque transition du lot reçoit donc un **poids de correction du biais** (*importance-sampling weight*) qui multiplie sa contribution à la perte :

$$
w_i \;=\; \big(N \cdot P(i)\big)^{-\beta}
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.257, p.260{{% /comment %}}

Ici \(N\) est le nombre de transitions actuellement dans le tampon, et \(\beta\) est un second exposant, qui règle la **force de la correction**. Lisez-le comme vous avez lu \(\alpha_{\mathrm{PER}}\), par ses bornes. Avec \(\beta = 0\), tous les poids valent 1 : aucune correction, le biais reste entier. Avec \(\beta = 1\), le biais est **entièrement** compensé, et l'espérance du gradient redevient celle du tirage uniforme.

{{% comment %}}SOURCE: LAPAN ch.8 p.257{{% /comment %}}

D'où une question que je vous invite à vous poser avant de lire la réponse : si \(\beta = 1\) corrige tout, pourquoi ne pas commencer là ? Parce qu'en pratique la convergence est meilleure en partant d'une correction partielle et en l'amenant progressivement à 1. Au début de l'entraînement, le gradient est de toute façon très bruité et le biais est le moindre des problèmes ; vers la fin, il devient le problème principal. D'où un calendrier, et il est de la même famille que celui de \(\varepsilon\) sauf qu'il monte au lieu de descendre :

$$
\beta_k \;=\; \min\!\big(1{,}0,\; 0{,}4 + k\,(1 - 0{,}4)/10^{5}\big)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.258-259{{% /comment %}}

Soit 0,4 au départ, puis une montée linéaire jusqu'à 1 sur cent mille trames. Nous venons donc de supprimer trois hyperparamètres en section 6.9 et d'en ajouter trois ici : l'exposant de priorité, le \(\beta\) de départ et la durée de sa montée. C'est un bon moment pour remarquer que la quantité de réglage est, dans ce domaine, à peu près conservée.

Un dernier détail sur les poids, et il explique une ligne du code qui suit. Les poids d'un lot sont **normalisés par leur maximum**, ce qui place le plus grand d'entre eux à 1. La correction ne peut donc que **réduire** la contribution d'une transition, jamais l'amplifier. C'est un choix prudent : il garantit que la repondération ne fait jamais grossir un gradient, et donc qu'elle ne déstabilise pas l'entraînement par le haut.

{{% comment %}}SOURCE: LAPAN ch.8 p.260{{% /comment %}}

---

## Le code, et pourquoi la perte doit être écrite à la main

Deux pièces changent dans le socle commun, et je les donne dans l'ordre où vous les écrirez.

```python
import numpy as np

class TamponPriorise:
    """Tampon priorisé naïf : tirage en O(N), largement suffisant sur CartPole."""

    def __init__(self, capacite: int, alpha_per: float = 0.6):
        self.capacite, self.alpha_per = capacite, alpha_per
        self.tampon: list = []
        self.position = 0
        self.priorites = np.zeros((capacite,), dtype=np.float32)

    def ajouter(self, transition) -> None:
        # Une transition NEUVE reçoit la priorité maximale : elle sera tirée vite.
        priorite_max = self.priorites.max(initial=1.0)
        if len(self.tampon) < self.capacite:
            self.tampon.append(transition)
        else:
            self.tampon[self.position] = transition
        self.priorites[self.position] = priorite_max
        self.position = (self.position + 1) % self.capacite

    def echantillonner(self, taille_lot: int, beta: float):
        n = len(self.tampon)
        probas = self.priorites[:n] ** self.alpha_per
        probas /= probas.sum()                           # P(i)
        indices = np.random.choice(n, taille_lot, p=probas)
        poids = (n * probas[indices]) ** (-beta)         # w_i
        poids /= poids.max()        # le plus grand poids vaut 1 : on ne fait que réduire
        return ([self.tampon[i] for i in indices], indices,
                np.asarray(poids, dtype=np.float32))

    def mettre_a_jour_priorites(self, indices, priorites) -> None:
        for indice, priorite in zip(indices, priorites):
            self.priorites[indice] = priorite
```

```python
def calculer_perte_priorisee(lot, poids, reseau, reseau_cible, gamma, peripherique):
    """Rend DEUX choses : la perte à rétropropager et les nouvelles priorités."""
    etats, actions, recompenses, termines, etats_finaux = deplier_lot(lot)
    # ... mise en tenseurs identique à la section 6.5 ...
    poids_t = torch.as_tensor(poids).to(peripherique)

    valeurs_action = reseau(etats_t).gather(
        1, actions_t.unsqueeze(-1)).squeeze(-1)
    with torch.no_grad():
        valeurs_finales = reseau_cible(etats_f_t).max(1)[0]
        valeurs_finales[termines_t] = 0.0
    cibles = recompenses_t + gamma * valeurs_finales

    # nn.MSELoss() NE SAIT PAS pondérer : le carré est écrit à la main.
    ecarts = valeurs_action - cibles
    pertes = poids_t * ecarts ** 2

    # La MÊME quantité, deux usages distincts :
    #   la moyenne PONDÉRÉE descend le gradient ;
    #   l'écart NON pondéré, détaché, devient la nouvelle priorité.
    nouvelles_priorites = ecarts.detach().abs() + 1e-5
    return pertes.mean(), nouvelles_priorites
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(p_i\) | priorité de la transition \(i\) | `self.priorites[indice]` |
| \(\alpha_{\mathrm{PER}}\) | exposant de priorité, 0,6 | `self.alpha_per` |
| \(P(i)\) | probabilité de tirage | `probas` |
| \(N\) | taille courante du tampon | `n = len(self.tampon)` |
| \(\beta\) | exposant de correction, 0,4 vers 1 | `beta` |
| \(w_i\) | poids de correction du biais | `poids` |
| \(\max_i w_i = 1\) | la normalisation par le maximum | `poids /= poids.max()` |
| \(\delta_i\) | l'erreur TD d'une transition | `ecarts` |
| \(\mathcal{L}(\theta) = \frac{1}{\lvert B\rvert}\sum_i w_i\delta_i^2\) | la perte pondérée | `pertes.mean()` |
| \(\alpha\) | pas d'apprentissage | `learning_rate`, et **jamais** `alpha_per` |

Trois remarques, et elles portent toutes sur la seconde fonction.

**Pourquoi le carré est écrit à la main.** La perte quadratique de PyTorch ne prend pas de poids par échantillon : elle moyenne ou somme, sans pondération. Dès qu'un échantillon doit peser moins qu'un autre, il faut donc écrire l'expression soi-même. C'est deux lignes, et c'est le genre de moment où la semaine 2 paie : vous savez que `nn.MSELoss()` n'est pas magique, et vous savez écrire ce qu'elle calcule.

{{% comment %}}SOURCE: LAPAN ch.8 p.261{{% /comment %}}

**Pourquoi la fonction rend deux choses.** La boucle d'entraînement doit, après le pas d'optimiseur, écrire les nouvelles priorités dans le tampon aux indices tirés. Il lui faut donc, en plus du scalaire à rétropropager, la quantité par échantillon. C'est une petite contagion de l'interface, et elle est intéressante en soi : la priorisation est la seule des cinq réparations qui ne se contente pas de modifier une pièce, elle fait circuler une information **en retour** du calcul de la perte vers le tampon. Voilà pourquoi je l'ai gardée pour la fin.

{{% comment %}}SOURCE: LAPAN ch.8 p.258, p.260-261{{% /comment %}}

**Pourquoi la priorité n'est pas la perte.** Regardez bien les deux dernières lignes. La quantité rétropropagée est la moyenne des carrés **pondérés**. La quantité écrite dans le tampon est l'écart **non pondéré**, en valeur absolue, détaché du graphe. Les deux viennent du même vecteur et elles ne doivent pas être confondues : le poids corrige un biais de tirage, il ne mesure pas la surprise. Une transition fortement pondérée à la baisse parce qu'elle est souvent tirée n'est pas pour autant une transition peu surprenante, et si l'on écrit la perte pondérée dans les priorités, le tampon se met à se corriger lui-même en boucle. Enfin, le \(10^{-5}\) ajouté garantit qu'une transition parfaitement prédite n'obtient pas une priorité nulle, c'est-à-dire ne disparaît pas à jamais du tirage.

{{% comment %}}SOURCE: LAPAN ch.8 p.261{{% /comment %}}

---

## Ce que cela gagne, et un avertissement sur la perte

Les résultats de cette section sont ceux qui demandent le plus de précautions de lecture, et c'est pour cela qu'ils arrivent après le code.

Sur le jeu de référence, le tampon priorisé met à peu près le **même temps absolu** à résoudre l'environnement que la version ordinaire. Mais il lui faut **moins d'itérations d'apprentissage et moins d'épisodes**. Autrement dit, la méthode est plus efficace en échantillons et ce gain est entièrement mangé par son coût de calcul, qui est le tirage en \(O(N)\) du tampon naïf. C'est exactement l'argument qui justifie l'arbre de segments dont je vous ai parlé en section 6.2 : il ne change rien à la méthode, il récupère le gain. Après réglage, 330 parties, avec \(\alpha_{\mathrm{PER}} = 0{,}6\) comme meilleure valeur, c'est-à-dire la valeur usuelle.

{{% comment %}}SOURCE: LAPAN ch.8 p.262, p.263{{% /comment %}}

> [!WARNING]
 **Attention, et c'est l'avertissement le plus important de la section, parce qu'il va au-delà du tampon priorisé.** Quand on active la priorisation, la courbe de perte devient visiblement plus basse, et c'est très satisfaisant à regarder. Ne concluez rien de cette courbe. La valeur de la perte, pendant un entraînement par renforcement, **n'est pas l'objectif à optimiser** : on peut obtenir une perte très faible et, faute d'exploration, une politique finale très loin de l'optimum. Un réseau qui prédit parfaitement les valeurs d'une mauvaise politique a une perte minuscule et ne vaut rien. La seule courbe qui décide est celle du **retour**. Gardez cette phrase pour les dix semaines qui restent : en apprentissage supervisé, la perte est l'objectif ; en apprentissage par renforcement, la perte est un diagnostic.

{{% comment %}}SOURCE: LAPAN ch.8 p.263{{% /comment %}}

---
