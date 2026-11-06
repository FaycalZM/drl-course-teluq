---
title: "13.10 Trois façons d'estimer un retour imaginé, dont une que vous connaissez par cœur"
weight: 11
---

## Le même problème que la semaine 7, dans un monde inventé

Une trajectoire imaginée s'arrête au pas \(t+H\). Que vaut l'état où l'on se trouve à ce moment ? La question est **exactement** celle de la semaine 7, et elle admet exactement les mêmes trois réponses. Je vais les donner dans l'ordre croissant d'intelligence, et la troisième vous sera familière au point d'en être émouvante.

**Premier estimateur : on somme les récompenses imaginées et on s'arrête là.**

$$
V_{\mathrm{R}}(Z_k) \;\doteq\; \E_{p_\theta,\, \pi_\phi}\!\left[\sum_{j=k}^{t+H} r_j\right]
$$

{{% comment %}}SOURCE: DREAMER éq. 4 p.4{{% /comment %}}

L'indice \(\mathrm{R}\) rappelle qu'il ne somme que des récompenses, et je précise, puisque cette semaine l'exige : **ce n'est pas la répétition d'action**, c'est une étiquette. Cet estimateur n'utilise **aucun critique**, donc il ne voit rien au-delà de \(t+H\). C'est précisément l'objection de la section 13.8, écrite sous forme d'équation, et c'est pour cela qu'il sert d'**ablation** : quand on veut mesurer ce que le critique apporte, on le remplace par celui-ci.

> [!NOTE]
 **Et un détail de transcription que je signale parce qu'il surprend : tel qu'il est publié, cet estimateur ne porte aucun facteur d'actualisation.** Pas de \(\gamma\). Les deux estimateurs suivants, eux, en portent un, et le critique de la section 13.9 est défini avec. Ce cours recopie la forme publiée sans y glisser discrètement un \(\gamma\) qui n'y est pas : sur un horizon de quinze pas avec un facteur proche de un, l'écart est faible, mais une équation recopiée doit l'être fidèlement, et un lecteur qui comparerait doit retrouver ce qu'il a sous les yeux.

**Deuxième estimateur : on somme \(n\) pas de récompenses, puis on amorce sur le critique.**

$$
V_{\mathrm{N}}^{\,n}(Z_k) \;\doteq\; \E_{p_\theta,\, \pi_\phi}\!\left[\sum_{j=k}^{h-1} \gamma^{\,j-k} r_j \;+\; \gamma^{\,h-k}\, \hat v_\psi(Z_h)\right],
\qquad h = \min(k + n,\; t + H)
$$

{{% comment %}}SOURCE: DREAMER éq. 5 p.4{{% /comment %}}

C'est la **cible à \(n\) étapes** de la semaine 6, appliquée à une trajectoire imaginée. Le \(\min\) est le détail à ne pas rater : il **écrête l'amorçage à l'horizon**. Si \(k + n\) dépasse \(t+H\), on amorce à \(t+H\) et pas plus loin, parce qu'au-delà la trajectoire n'existe pas. Avec \(n = 1\), c'est une cible à un pas ; avec \(n = H\), on retrouve presque le premier estimateur, à ceci près qu'il reste un terme de valeur au bout.

**Troisième estimateur, et c'est une vieille connaissance.**

$$
V_\lambda(Z_k) \;\doteq\; (1-\lambda) \sum_{n=1}^{H-1} \lambda^{\,n-1}\, V_{\mathrm{N}}^{\,n}(Z_k) \;+\; \lambda^{\,H-1}\, V_{\mathrm{N}}^{\,H}(Z_k)
$$

{{% comment %}}SOURCE: DREAMER éq. 6 p.4{{% /comment %}}

> [!IMPORTANT]
 **Regardez cette équation et nommez-la : c'est le retour \(\lambda\) de la semaine 7.** La même moyenne exponentiellement pondérée de toutes les cibles à \(n\) étapes, le même poids \((1-\lambda)\lambda^{n-1}\), le même terme résiduel qui récupère la masse restante au dernier pas disponible. Vous l'avez écrite pour des trajectoires **réelles**, et elle est ici appliquée à des trajectoires **qui n'ont jamais eu lieu**. La valeur retenue est \(\lambda = 0{,}95\), ce qui donne un poids majoritaire aux cibles longues tout en gardant un peu de l'amorçage court. Je trouve cette continuité instructive : treize semaines après, le même objet sert dans un contexte qui n'existait pas encore quand nous l'avons rencontré. Rien d'autre à apprendre ici : si vous savez écrire un retour \(\lambda\), vous savez écrire cet estimateur.

---

## Le code des trois estimateurs, et pourquoi c'est le premier volet du laboratoire

**Le code.** Les trois, comme fonctions pures sur des tenseurs. Aucune dépendance à un modèle, aucune dépendance à un environnement : des récompenses, des valeurs, et deux scalaires.

```python
import torch


def retour_recompenses(recompenses):
    """V_R : la somme des recompenses imaginees, SANS actualisation,
    et sans aucune valeur au bout. Aveugle au-dela de l'horizon."""
    return recompenses.flip(0).cumsum(0).flip(0)


def retour_n_pas(recompenses, valeurs, gamma, n):
    """V_N^n : n pas de recompenses, puis amorcage sur le critique.
    L'amorcage est ecrete a l'horizon : c'est le min(k + n, t + H)."""
    horizon = recompenses.shape[0]
    sorties = []
    for k in range(horizon):
        h = min(k + n, horizon)                       # l'ecretage
        total = sum(gamma ** (j - k) * recompenses[j] for j in range(k, h))
        if h < horizon:
            total = total + gamma ** (h - k) * valeurs[h]
        sorties.append(total)
    return torch.stack(sorties)


def retour_lambda(recompenses, valeurs, gamma, lam):
    """V_lambda : le retour lambda de la semaine 7, calcule a l'envers.
    Forme recursive, equivalente a la moyenne ponderee et bien moins chere."""
    horizon = recompenses.shape[0]
    sortie = torch.zeros_like(recompenses)
    accumulateur = valeurs[-1]
    for k in reversed(range(horizon)):
        suivante = valeurs[k + 1] if k + 1 < horizon else valeurs[-1]
        cible = recompenses[k] + gamma * ((1 - lam) * suivante + lam * accumulateur)
        sortie[k] = cible
        accumulateur = cible
    return sortie
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(r_k\) | récompenses prédites le long de la trajectoire imaginée | `recompenses` |
| \(\hat v_\psi(Z_k)\) | valeurs prédites par le critique | `valeurs` |
| \(V_{\mathrm{R}}\) | somme nue, sans \(\gamma\) et sans valeur | `retour_recompenses` |
| \(V_{\mathrm{N}}^{\,n}\) | cible à \(n\) pas, amorcée et écrêtée | `retour_n_pas` |
| \(h = \min(k+n, t+H)\) | l'écrêtage de l'amorçage à l'horizon | `h = min(k + n, horizon)` |
| \(V_\lambda\) | le retour \(\lambda\) de la semaine 7 | `retour_lambda` |
| \(\lambda = 0{,}95\) | pondération entre cibles courtes et longues | `lam` |

Ces trois fonctions sont le **volet A du laboratoire**, et c'est délibéré : elles ne demandent ni modèle, ni environnement, ni entraînement. Vous les écrivez, vous leur donnez des récompenses synthétiques, et vous voyez en une minute ce que les équations disent. En particulier, vous verrez que \(V_{\mathrm{R}}\) est rigoureusement plat sur une tâche où toute la récompense arrive après l'horizon, tandis que les deux autres ne le sont pas.

---
