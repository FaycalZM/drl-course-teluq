---
title: "5.4 Le gradient qui n'en est pas un"
weight: 5
---

## Descendre une erreur, un exemple à la fois

Nous avons un objectif. Il nous faut une méthode pour le diminuer, et c'est ici que la semaine 2 revient au premier plan.

Posons le cadre proprement, parce que toute la section en dépend. \(\mathbf{w}\) est un vecteur colonne de \(d\) composantes réelles, et \(\hat v(s,\mathbf{w})\) est une fonction **différentiable** de \(\mathbf{w}\) pour tout état \(s\). Cette hypothèse de différentiabilité n'est pas décorative : c'est elle qui autorise tout le reste, et c'est elle qu'un réseau de neurones satisfait par construction.

{{% comment %}}SOURCE: SB ch.9 p.222{{% /comment %}}

L'intuition de la descente de gradient stochastique tient en une ligne, et vous l'avez déjà écrite en semaine 2 : on ajuste le vecteur de poids après chaque exemple, d'une petite quantité, dans la direction qui réduirait le plus l'erreur sur cet exemple. Un exemple, un petit pas. Formellement, en supposant pour l'instant que la valeur vraie \(v_\pi(S_t)\) nous est donnée :

$$
\begin{aligned}
\mathbf{w}_{t+1} &\defeq \mathbf{w}_t - \tfrac{1}{2}\alpha\nabla
  \big[\, v_\pi(S_t) - \hat v(S_t,\mathbf{w}_t) \,\big]^2 \\[4pt]
&= \mathbf{w}_t + \alpha\big[\, v_\pi(S_t) - \hat v(S_t,\mathbf{w}_t) \,\big]
   \nabla\hat v(S_t,\mathbf{w}_t)
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.9 éq. 9.4-9.5 p.223{{% /comment %}}

Le passage de la première ligne à la seconde est une simple dérivation du carré : le facteur 2 du carré annule le \(\tfrac12\), le signe moins s'inverse, et le gradient de la parenthèse se réduit à \(-\nabla\hat v\) puisque \(v_\pi(S_t)\) ne dépend pas de \(\mathbf{w}\). **Retenez cette dernière proposition**, parce que la sous-section suivante ne fait rien d'autre que l'invalider.

Le symbole \(\nabla\) désigne, comme en semaine 2, le vecteur des dérivées partielles par rapport à chaque composante du vecteur de poids :

$$
\nabla f(\mathbf{w}) \defeq \Big(
\frac{\partial f(\mathbf{w})}{\partial w_1},
\frac{\partial f(\mathbf{w})}{\partial w_2},
\ldots,
\frac{\partial f(\mathbf{w})}{\partial w_d}
\Big)^{\!\top}
$$

{{% comment %}}SOURCE: SB ch.9 éq. 9.6 p.223{{% /comment %}}

Pourquoi un **petit** pas, et non un pas qui annulerait l'erreur sur l'exemple courant ? Parce que ce n'est pas ce que nous cherchons. Nous ne cherchons pas, et nous n'espérons pas trouver, une fonction de valeur dont l'erreur serait nulle en tout état : nous cherchons une approximation qui **équilibre** les erreurs entre les différents états. Un pas qui corrigerait entièrement l'erreur sur un exemple la reporterait sur les autres, à cause du couplage de la section 5.2. Les résultats de convergence, d'ailleurs, supposent que \(\alpha\) décroît au cours du temps.

{{% comment %}}SOURCE: SB ch.9 p.223{{% /comment %}}

Évidemment, \(v_\pi(S_t)\) ne nous est pas donné : s'il l'était, nous n'aurions rien à apprendre. Remplaçons-le donc par une **cible générique** \(U_t\), c'est-à-dire par n'importe quelle approximation de \(v_\pi(S_t)\) dont nous disposons réellement.

$$
\mathbf{w}_{t+1} \defeq \mathbf{w}_t + \alpha
\big[\, U_t - \hat v(S_t,\mathbf{w}_t) \,\big]\nabla\hat v(S_t,\mathbf{w}_t)
$$

{{% comment %}}SOURCE: SB ch.9 éq. 9.7 p.224{{% /comment %}}

Et voici la condition qui décide de tout. Si \(U_t\) est une estimation **non biaisée**, c'est-à-dire si \(\E[U_t \mid S_t = s] = v_\pi(S_t)\) pour chaque \(t\), alors la convergence de \(\mathbf{w}_t\) vers un optimum local est **garantie**, sous les conditions usuelles de décroissance de \(\alpha\).

Une cible satisfait cette condition sans effort : le retour de Monte-Carlo. Puisque \(G_t\) est par définition une réalisation de la variable dont \(v_\pi(S_t)\) est l'espérance, il est non biaisé, et la méthode obtenue, le **Monte-Carlo par gradient**, converge.

$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha\big[\, G_t - \hat v(S_t,\mathbf{w}) \,\big]
\nabla\hat v(S_t,\mathbf{w})
$$

{{% comment %}}SOURCE: SB ch.9 p.224{{% /comment %}}

---

## La rupture : la cible contient les poids

Nous arrivons au paragraphe le plus important de la semaine. Je vais vous en donner la logique entière, parce que c'est elle qui explique une ligne de PyTorch que des milliers de gens recopient sans la comprendre.

Que se passe-t-il si, au lieu du retour complet, nous prenons une cible **amorcée**, du genre de celles de la semaine 4 : \(R_{t+1} + \gamma\,\hat v(S_{t+1},\mathbf{w}_t)\) ?

Ces cibles dépendent toutes de la **valeur courante du vecteur de poids** \(\mathbf{w}_t\). Il en découle deux conséquences, et la seconde est fatale au raisonnement précédent. Premièrement, elles sont **biaisées** : leur espérance n'est pas \(v_\pi(S_t)\), puisqu'elles contiennent une estimation. Deuxièmement, et c'est le point décisif, **elles ne produisent pas une véritable méthode de descente de gradient**. Pourquoi ? Parce que le passage de la première à la seconde ligne de notre dérivation reposait sur le fait que la cible **ne dépend pas de \(\mathbf{w}_t\)**. Si la cible en dépend, ce passage n'est tout simplement pas valide : il manque un morceau, celui qui vient de la dérivation de la cible elle-même.

Que fait-on alors ? On garde la formule, et on assume le morceau manquant. Voici donc l'énoncé exact de ce que nous ferons pendant tout le reste du cours, et je vous demande de le retenir sous cette forme : **une telle mise à jour tient compte de l'effet d'une modification du vecteur de poids \(\mathbf{w}_t\) sur l'estimation, et elle ignore son effet sur la cible.** Elle ne contient donc qu'une partie du gradient, la partie qui nous arrange, et c'est exactement pour cette raison que nous appelons ces méthodes des **méthodes semi-gradient**.

{{% comment %}}SOURCE: SB ch.9 p.224{{% /comment %}}

La **méthode semi-gradient** la plus simple est le TD(0) semi-gradient, qui prend \(U_t \defeq R_{t+1} + \gamma\,\hat v(S_{t+1},\mathbf{w})\) et donne :

$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha
\big[\, R + \gamma\,\hat v(S',\mathbf{w}) - \hat v(S,\mathbf{w}) \,\big]
\nabla\hat v(S,\mathbf{w}),
\qquad\text{avec } \hat v(\text{terminal},\cdot) = 0
$$

{{% comment %}}SOURCE: SB ch.9 p.225{{% /comment %}}

Mettez cette ligne à côté du Monte-Carlo par gradient de la sous-section précédente. **Une seule chose diffère : la cible.** \(G_t\) est devenu \(R + \gamma\hat v(S',\mathbf{w})\), exactement comme en semaine 4 où \(G_t\) était devenu \(R + \gamma V(S')\). Le reste est identique au symbole près. Et pourtant la première converge vers un optimum local et la seconde n'a plus cette garantie. Je ne connais pas de meilleure illustration de ce que coûte l'amorçage.

Et que l'on gagne, car on gagne quelque chose. L'amorçage apprend **plus vite**, et il apprend de façon continue et en ligne, sans attendre la fin d'un épisode. C'est le même marché que celui de la semaine 4, avec une clause supplémentaire : cette fois, on paie aussi en robustesse de convergence.

{{% comment %}}SOURCE: SB ch.9 p.224-225{{% /comment %}}

> [!NOTE]
 **Notez bien le mot « semi-gradient », parce que ce cours l'emploiera jusqu'au bout et que vous ne le trouverez pas partout.** Il nomme très précisément ce que nous venons de faire : prendre la moitié du gradient qui nous arrange et laisser l'autre moitié de côté, en sachant ce que l'on fait. Beaucoup de présentations appellent cela « la descente de gradient sur la perte TD », ce qui est faux au sens strict, puisque la quantité descendue n'est le gradient d'aucune fonction. Dans ce cours, chaque fois que vous lirez « semi-gradient », vous pourrez traduire mentalement par : *la cible est tenue pour une constante alors qu'elle n'en est pas une*.

---

## `detach()` est le « semi » de semi-gradient

Voici maintenant la ligne de PyTorch, et je veux que les deux paragraphes qui suivent soient lus d'un seul souffle, parce qu'ils disent la même chose dans deux langues.

En formalisme : une méthode semi-gradient tient compte de l'effet d'une modification des poids sur l'estimation, **mais ignore son effet sur la cible**.

{{% comment %}}SOURCE: SB ch.9 p.224{{% /comment %}}

En PyTorch : on **détache la valeur de son graphe de calcul pour empêcher les gradients de remonter dans le réseau qui a servi à calculer l'approximation des états suivants**. Sans ce détachement, la rétropropagation de la perte affecterait à la fois la prédiction de l'état courant **et** celle de l'état suivant, alors que nous ne voulons pas toucher la prédiction de l'état suivant, puisqu'elle sert à construire la valeur de référence.

{{% comment %}}SOURCE: LAPAN ch.6 p.191-192{{% /comment %}}

Ce sont deux formulations d'une seule et même décision. Voici le fragment, et c'est le plus important de la semaine.

```python
import torch

def perte_semi_gradient(reseau, obs, recompenses, obs_suivantes, termines,
                        gamma: float = 0.99) -> torch.Tensor:
    """Un pas de TD(0) semi-gradient. Trois lignes, trois décisions."""

    estimation = reseau(obs)                      # hat v(S, w) : DIFFÉRENCIÉE

    with torch.no_grad():                         # 1er blocage : rien n'est enregistré
        valeur_suivante = reseau(obs_suivantes)   # hat v(S', w) : les MÊMES poids
        valeur_suivante[termines] = 0.0           # hat v(terminal, .) = 0

    cible = recompenses + gamma * valeur_suivante
    cible = cible.detach()                        # 2e blocage, explicite et redondant

    return ((cible - estimation) ** 2).mean()     # on ne descend que la MOITIÉ du gradient
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\hat v(S,\mathbf{w})\) | l'estimation, la quantité différenciée | `estimation` |
| \(\hat v(S',\mathbf{w})\) | la valeur de l'état suivant, **les mêmes poids** | `valeur_suivante` |
| \(\hat v(\text{terminal},\cdot) = 0\) | un état terminal vaut zéro | `valeur_suivante[termines] = 0.0` |
| \(U_t = R + \gamma\hat v(S',\mathbf{w})\) | la cible | `cible` |
| « la cible est tenue pour constante » | le **semi** de semi-gradient | `torch.no_grad()` **et** `.detach()` |
| \(\alpha\) | pas d'apprentissage | il vit dans l'optimiseur, pas dans la perte |
| \(\nabla\hat v(S,\mathbf{w})\) | le gradient effectivement calculé | ce que produit `.backward()` sur le retour |

Trois remarques sur ce fragment, et la troisième est celle que je veux que vous reteniez pour le reste du cours.

La première : regardez la ligne `valeur_suivante = reseau(obs_suivantes)`. C'est le **même réseau**, les mêmes poids, la même fonction. La cible contient donc littéralement \(\mathbf{w}\), et c'est bien pour cela qu'il faut une décision explicite à son sujet.

La deuxième : le gradient est bloqué **deux fois**. `torch.no_grad()` empêche l'enregistrement des opérations pendant le passage avant, et `.detach()` coupe le lien sur le résultat. L'un **ou** l'autre suffirait. Ce n'est pas une erreur, c'est une ceinture doublée de bretelles, et c'est une pratique raisonnable dans du code que l'on veut lire sans se demander, à chaque relecture, par où un gradient pourrait bien remonter.

> [!IMPORTANT]
 **Je dois insister : `detach()` n'est pas un détail de PyTorch, c'est le « semi » de semi-gradient.** Si un jour vous retirez cette ligne « pour que le gradient circule correctement », vous ne corrigez pas un bogue : vous **changez d'algorithme**, et l'algorithme obtenu n'est plus celui dont nous pouvons discuter le comportement. C'est la raison pour laquelle je vous demande, devant chaque fragment de cette semaine, de dire ce qui est différencié et ce qui est tenu pour constant. Un étudiant qui recopie `.detach()` sans comprendre ce qu'il déclare le recopiera pendant dix semaines, et il ne saura pas expliquer pourquoi son acteur-critique de la semaine 8 n'apprend rien. Vous, vous saurez : parce que l'endroit où le gradient s'arrête **est** la définition de la méthode.

---
