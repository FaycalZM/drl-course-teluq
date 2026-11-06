---
title: "6.4 Le réseau cible comme objet, et la synchronisation douce"
weight: 5
---

## Une copie, ou un mélange

Le dernier des cinq objets est celui que vous connaissez le mieux, puisque la section 5.7 lui a consacré une réparation entière. Son travail est de **synchroniser deux réseaux de même architecture**, et il le fait de deux façons.

{{% comment %}}SOURCE: LAPAN ch.7 p.219{{% /comment %}}

La première est la copie, et c'est très exactement la ligne de la semaine 5 : tous les \(N\) pas, les poids du réseau entraîné écrasent ceux de la cible. C'est le mode des espaces d'actions discrets, Atari et CartPole compris.

La seconde est nouvelle, et c'est pour elle que cette section existe. Au lieu de copier, on **mélange** : à chaque pas, chaque paramètre de la cible se rapproche un peu de son homologue du réseau entraîné, sans jamais l'atteindre d'un coup. Cette **synchronisation douce** (*soft sync*) est le mode du contrôle continu, où l'on veut que la transition entre les paramètres des deux réseaux soit lisse, et vous la retrouverez en semaine 11.

{{% comment %}}SOURCE: LAPAN ch.7 p.219{{% /comment %}}

L'équation, paramètre par paramètre. \(w_i\) est le \(i\)-ième paramètre de la cible, \(s_i\) celui du réseau entraîné :

$$
w_i \;\leftarrow\; \alpha_{\mathrm{sync}}\,w_i \;+\; (1 - \alpha_{\mathrm{sync}})\,s_i
$$

{{% comment %}}SOURCE: LAPAN ch.7 p.219{{% /comment %}}

Vérifions sur un nombre, parce que le sens du coefficient est l'unique piège de cette section. Avec \(\alpha_{\mathrm{sync}} = 0{,}1\), un paramètre de cible valant 1,2039 et un paramètre source valant 2,2039 donnent 2,1039, c'est-à-dire \(0{,}1 \times 1{,}2039 + 0{,}9 \times 2{,}2039\). Le coefficient pèse donc l'**ancienne** valeur de la cible, et \(1 - \alpha_{\mathrm{sync}}\) pèse la nouvelle. Une valeur petite donne une synchronisation **rapide**.

{{% comment %}}SOURCE: LAPAN ch.7 p.221{{% /comment %}}

> [!WARNING]
 **Attention, et c'est une dette que je paie maintenant pour ne pas la laisser à la semaine 11.** La convention la plus répandue pour une synchronisation douce est l'inverse de celle-ci. Elle s'écrit avec un coefficient \(\tau\) qui pèse les **nouveaux** poids, soit \(\theta^- \leftarrow \tau\,\theta + (1-\tau)\,\theta^-\), et la valeur usuelle y est de l'ordre de \(\tau = 0{,}005\), c'est-à-dire une cible qui bouge très lentement. Les deux écritures sont liées par \(\alpha_{\mathrm{sync}} = 1 - \tau\). Retenez-le sous cette forme : **un \(\alpha_{\mathrm{sync}}\) proche de 0 et un \(\tau\) proche de 1 font la même chose, une copie presque brutale.** Si vous lisez un jour un code où une synchronisation douce de coefficient 0,001 rend un agent instable, commencez par vérifier laquelle des deux conventions ce code emploie.

{{% comment %}}SOURCE: notation.md §6{{% /comment %}}

Le code, maintenant, et je le donne en PyTorch simple parce que c'est sous cette forme que vous l'écrirez en semaine 11.

```python
import copy
import torch.nn as nn

class ReseauCible:
    """Deux réseaux de même architecture, et l'invariant qui les relie."""

    def __init__(self, reseau: nn.Module):
        self.reseau = reseau                          # une RÉFÉRENCE
        self.cible = copy.deepcopy(reseau)            # une COPIE PROFONDE

    def synchroniser(self) -> None:
        """Le mode de la semaine 5 : une copie franche, tous les N pas."""
        self.cible.load_state_dict(self.reseau.state_dict())

    def synchroniser_doucement(self, alpha_sync: float) -> None:
        """Le mode continu : un mélange, à chaque pas."""
        assert 0.0 < alpha_sync <= 1.0
        etat = self.reseau.state_dict()
        etat_cible = self.cible.state_dict()
        for nom, valeur in etat_cible.items():
            # alpha_sync pèse l'ANCIENNE cible, (1 - alpha_sync) la source.
            etat_cible[nom] = alpha_sync * valeur + (1 - alpha_sync) * etat[nom]
        self.cible.load_state_dict(etat_cible)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\theta\) | les poids du réseau entraîné | `self.reseau`, une référence |
| \(\theta^-\) | les poids de la cible | `self.cible`, une copie profonde |
| \(\theta^- \leftarrow \theta\) | la synchronisation de la semaine 5 | `synchroniser()` |
| \(w_i \leftarrow \alpha_{\mathrm{sync}} w_i + (1-\alpha_{\mathrm{sync}}) s_i\) | la synchronisation douce | `synchroniser_doucement(...)` |
| \(\alpha_{\mathrm{sync}}\) | poids de l'**ancienne** cible | `alpha_sync` |
| \(\tau = 1 - \alpha_{\mathrm{sync}}\) | la convention de la semaine 11 | absent ici, et c'est le piège |

Deux remarques sur ce fragment.

La première porte sur la copie profonde. L'objet tient une **référence** au réseau entraîné et une **copie indépendante** pour la cible. Si vous remplacez la copie profonde par une affectation, les deux noms désignent le même réseau, la cible suit instantanément l'entraîné, et vous avez supprimé la réparation de la semaine 5 sans qu'aucune exception ne soit levée. C'est, mot pour mot, la configuration nº2 de l'ablation de la semaine dernière, mais obtenue par accident.

{{% comment %}}SOURCE: LAPAN ch.7 p.220{{% /comment %}}

La seconde est une mise en garde sur le coût. Une synchronisation douce touche **tous** les paramètres à **chaque** pas, alors qu'une copie ne coûte rien pendant mille pas puis coûte une seule recopie. Sur un petit réseau cela ne se voit pas ; sur le réseau convolutif de la semaine 5, cela se mesure. Ce n'est pas une raison de l'éviter, c'est une raison de savoir ce qu'on paie.

---
