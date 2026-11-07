---
title: "14.7 Optimiser contre un modèle de récompense"
weight: 8
---

## Une enveloppe qui remplace la récompense, et une normalisation glissante

Nous avons un modèle de récompense ajusté. Il faut maintenant que l'agent s'entraîne contre lui, et la beauté de cette construction est qu'il n'y a **rien à changer dans l'algorithme**.

**Intuition.** On interpose une enveloppe entre l'environnement brut et les enveloppes de prétraitement. À chaque pas, elle jette la récompense fournie par le jeu et la remplace par la prédiction du modèle sur le couple formé de l'observation précédente et de l'action qui vient d'être jouée. La récompense réelle n'est pas perdue : elle est conservée **comme métrique**, dans les informations auxiliaires, pour que l'on puisse mesurer ce que l'agent obtient réellement pendant qu'il optimise autre chose.

Notez immédiatement ce que cette dernière phrase décrit : **on optimise une quantité et on évalue l'autre**. C'est le protocole exact que la seconde moitié de la semaine va généraliser et mesurer, et il est déjà là, dans une ligne de code de la première moitié.

**Le problème d'échelle, et la normalisation qui le traite.** La section 14.6 a montré que la récompense prédite n'est définie ni en échelle ni en décalage de façon fiable. Or un acteur-critique y est sensible : ses pas de gradient sont proportionnels à l'avantage, et son critique doit apprendre une valeur dont l'ordre de grandeur change. On centre et on réduit donc la prédiction sur une **fenêtre glissante des cent dernières valeurs**.

**L'équation.**

$$
\tilde r_t = \frac{\hat r_t - \hat\mu_{100}}{\hat\sigma_{100}}
$$

où \(\hat\mu_{100}\) et \(\hat\sigma_{100}\) sont la moyenne et l'écart-type des cent dernières prédictions du modèle.

{{% comment %}}SOURCE: LAPAN ch.19 p.592-593{{% /comment %}}

**Le code.**

```python
import collections
import numpy as np
import torch


class RecompenseApprise:
    """Remplace la recompense de l'environnement par celle du modele.

    La recompense reelle n'est pas perdue : elle devient une metrique.
    """

    FENETRE = 100

    def __init__(self, env, modele):
        self.env = env
        self.modele = modele
        self.historique = collections.deque(maxlen=self.FENETRE)
        self.obs_precedente = None

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.obs_precedente = obs
        return obs, info

    def step(self, action):
        obs, r_reel, termine, tronque, info = self.env.step(action)

        with torch.no_grad():
            r_predit = self.modele(
                torch.as_tensor(self.obs_precedente).unsqueeze(0),
                torch.as_tensor([action]),
            ).item()

        self.historique.append(r_predit)
        moyenne = float(np.mean(self.historique))
        ecart = float(np.std(self.historique)) + 1e-8
        r_normalise = (r_predit - moyenne) / ecart

        info["recompense_reelle"] = r_reel      # conservee comme METRIQUE
        self.obs_precedente = obs
        return obs, r_normalise, termine, tronque, info
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(o_{t-1}\) | observation **précédente**, celle sur laquelle l'action a été choisie | `self.obs_precedente` |
| \(a_t\) | l'action qui vient d'être jouée | `action` |
| \(\hat r_t = \hat r(o_{t-1}, a_t)\) | la prédiction brute du modèle | `r_predit` |
| \(\hat\mu_{100}, \hat\sigma_{100}\) | moyenne et écart-type sur la fenêtre | `moyenne`, `ecart` |
| \(\tilde r_t\) | la récompense que l'agent reçoit réellement | `r_normalise` |
| \(R_t\) (la vraie) | la récompense du jeu, **métrique seulement** | `info["recompense_reelle"]` |

> [!NOTE]
 **Pourquoi une fenêtre glissante plutôt qu'une statistique calculée une fois pour toutes.** Parce que la politique change pendant l'entraînement, et que la distribution des observations qu'elle visite change avec elle. Une moyenne calculée au début cesserait d'être pertinente après deux cents mille pas. La fenêtre de cent valeurs suit la politique, ce qui a un effet secondaire intéressant : la récompense normalisée mesure **à quel point ce pas est bon par rapport aux cent derniers pas de cet agent**, et non par rapport à un étalon absolu. L'agent reçoit donc un signal relatif à son propre comportement récent, ce qui ressemble beaucoup à une normalisation d'avantage de la semaine 8. Et une conséquence qui mérite d'être nommée : si la politique se stabilise dans un comportement uniforme, l'écart-type de la fenêtre s'effondre et le signal devient du bruit amplifié. Retenez-la pour la section 14.8.

---

## Geler les convolutions, diviser le pas par dix

Deuxième détail d'implémentation, et il est bien plus qu'un détail.

L'affinage ne repart pas de zéro : il repart du meilleur modèle sauvegardé, celui qui vaut 460. Et dans ce régime, deux modifications sont nécessaires : les **convolutions de l'acteur-critique sont gelées**, et le **pas d'apprentissage est divisé par dix**.

Sans ces deux modifications, le constat est net et immédiat : l'acteur **désapprend très vite tout son savoir antérieur**, et la récompense tombe à presque rien.

{{% comment %}}SOURCE: LAPAN ch.19 p.591{{% /comment %}}

Les deux modifications vont ensemble et ne se séparent pas : dans une implémentation, elles tiennent à un seul drapeau de ligne de commande, celui qui fait passer l'entraînement du régime initial au régime d'affinage.

Pourquoi ? Parce que la récompense a changé de nature du jour au lendemain. L'agent avait appris une fonction de valeur pour une récompense, et on lui en donne une autre, dont l'échelle, le signe et la structure sont différents. Les premiers gradients sont donc énormes et pointent dans des directions arbitraires, et un tronc convolutif qui a mis cinq heures à apprendre à voir des poissons se détruit en quelques milliers de pas. Geler le tronc protège la **perception**, qui n'a aucune raison de changer, et laisse l'adaptation se faire dans les têtes, qui sont les seules concernées par le changement d'objectif.

---

## Et la garde qui n'est nulle part dans cette chaîne

Voici une observation que ce cours fait pour son propre compte, et je la formule comme une question avant de la formuler comme un constat.

Quand on optimise une politique contre un modèle appris, qu'est-ce qui empêche la politique de s'éloigner arbitrairement du régime où ce modèle a été ajusté ?

La réponse habituelle est une **pénalité de divergence de Kullback-Leibler** contre une politique de référence, celle d'avant l'affinage : on ajoute à l'objectif un terme qui coûte d'autant plus cher que la nouvelle politique s'écarte de l'ancienne. C'est exactement la machinerie de la semaine 10, et c'est la garde standard de tous les affinages par rétroaction humaine à grande échelle. Elle a une justification simple : le modèle de récompense n'est fiable que sur la distribution de segments qu'il a vus, donc il faut empêcher la politique de sortir de cette distribution.

**Cette garde est absente de toute la chaîne.** Il n'y a pas de pénalité de divergence, pas de politique de référence, pas de contrainte sur le déplacement de la politique. Ce qui en tient lieu, de fait, est le couple formé par le gel des convolutions et le pas divisé par dix : les deux limitent **la vitesse** à laquelle la politique peut s'éloigner, mais ni l'un ni l'autre ne limite **la distance** qu'elle finira par parcourir.

{{% comment %}}SOURCE: LAPAN ch.19 p.591 ; absence vérifiée sur ch.19 p.587-598{{% /comment %}}

> [!IMPORTANT]
 **Retenez cette asymétrie, parce qu'elle est le mécanisme de la semaine 13 sous un autre nom.** La semaine 13 a établi qu'un optimiseur branché sur un estimateur que rien ne peut contredire hors des données **cherche** les endroits où cet estimateur se trompe. Remplacez « estimateur de valeur » par « modèle de récompense » et « jeu de données figé » par « les trois cents segments étiquetés ». La structure est identique : une fonction apprise, fiable sur une région de l'espace, un optimiseur qui maximise cette fonction, et aucun mécanisme de démenti. La différence est que la semaine 13 avait deux familles de parades et que cette chaîne n'en emploie aucune. Vous savez donc déjà ce qui va se passer. La section 14.8 va simplement vous montrer combien de tours cela prend.

---
