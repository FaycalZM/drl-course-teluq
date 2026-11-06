---
title: "13.4 La borne variationnelle, et ses deux termes"
weight: 5
---

## Ce qu'on maximise quand on ne peut pas maximiser ce qu'on veut

Nous avons une architecture. Il nous faut un objectif, et il y a une difficulté à contourner.

Ce qu'on voudrait maximiser est clair : la **vraisemblance** des observations effectivement rencontrées, sachant les actions jouées. Si le modèle attribue une forte probabilité à ce qui est arrivé, il a compris quelque chose du monde. Le problème est que cette vraisemblance demande de sommer sur toutes les suites de latents possibles, ce qui est hors de portée.

**L'intuition.** On remplace donc une quantité impossible à calculer par une **borne inférieure** qu'on sait calculer, et on maximise la borne. Et cette borne a la bonne propriété d'être lisible : elle se décompose en deux termes qui s'opposent, exactement comme dans un auto-encodeur variationnel. Le premier terme demande au latent de **permettre de reconstruire** ce qu'on a vu. Le second lui demande de rester **proche de ce que le modèle aurait prédit sans voir**. Le premier pousse à tout retenir, le second pousse à ne retenir que ce qui est prévisible. L'équilibre entre les deux est le modèle.

**L'équation.** Les deux termes sont nommés dans l'équation elle-même.

$$
\ln p_\theta(o_{1:T} \mid a_{1:T}) \;\ge\; \sum_{t=1}^{T} \Big(
\underbrace{\E_{e_\theta(z_t \mid o_{\le t},\, a_{<t})}\big[\ln p_\theta(o_t \mid z_t)\big]}_{\text{reconstruction}}
\;-\;
\underbrace{\E_{e_\theta(z_{t-1} \mid o_{\le t-1},\, a_{<t-1})}\Big[\KL\big[\,e_\theta(z_t \mid o_{\le t}, a_{<t}) \;\big\|\; p_\theta(z_t \mid z_{t-1}, a_{t-1})\,\big]\Big]}_{\text{complexité}}
\Big)
$$

{{% comment %}}SOURCE: PLANET éq. 3 p.4 (vérifié sur image de page){{% /comment %}}

Le terme de **reconstruction** est une log-vraisemblance : sachant le latent produit par l'encodeur, quelle probabilité le modèle d'observation donne-t-il à l'image qu'on a réellement reçue ? Le terme de **complexité** est une divergence de Kullback-Leibler entre deux lois sur le même latent : celle de l'encodeur, qui a vu l'observation, et celle de la transition, qui ne l'a pas vue. Il mesure donc exactement **la surprise** du modèle : combien d'information l'observation a-t-elle apportée que la transition n'avait pas anticipée ?

L'équation est écrite pour les observations seules. Les termes de récompense s'y ajoutent **par analogie**, à l'identique, avec \(p_\theta(r_t \mid z_t)\) à la place de \(p_\theta(o_t \mid z_t)\). Je ne les réécris pas : la structure est la même, et l'écrire deux fois n'apprend rien.

{{% comment %}}SOURCE: PLANET p.4{{% /comment %}}

Les deux espérances externes sont estimées par **un seul échantillon reparamétré**. Un. C'est la reparamétrisation de la semaine 10, employée ici pour exactement la même raison : rendre le tirage dérivable, afin que le gradient atteigne les paramètres de la loi qui a produit l'échantillon.

{{% comment %}}SOURCE: PLANET p.4{{% /comment %}}

---

## Trois gaussiennes, et une équivalence qui rend tout cela familier

Avant d'écrire le code, il faut dire quelles lois sont employées, parce que ce choix transforme une histoire probabiliste en code que vous avez déjà écrit.

La **transition** est une gaussienne dont la moyenne et la variance sortent d'un réseau à propagation avant. Le modèle d'**observation** est une gaussienne dont la moyenne est produite par un réseau déconvolutif et dont la covariance est l'**identité**. Le modèle de **récompense** est une gaussienne scalaire de **variance unité**.

> [!IMPORTANT]
 **Et voici la phrase qui convertit toute cette section en code que vous connaissez : sous une variance unité, la log-vraisemblance gaussienne est une erreur quadratique moyenne, à une constante additive près.** Développez : \(-\ln \mathcal{N}(x \mid \hat{x}, 1) = \tfrac{1}{2}(x - \hat{x})^2 + \text{const}\). La constante ne dépend d'aucun paramètre, donc le gradient l'ignore. Maximiser le terme de reconstruction de la borne variationnelle, c'est donc **minimiser une erreur quadratique moyenne entre l'image reçue et l'image reconstruite**, et minimiser une erreur quadratique entre la récompense reçue et la récompense prédite. Vous savez écrire cela depuis la semaine 2. Tout ce que la borne variationnelle ajoute, en pratique, c'est le second terme.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

---

## Un encodeur qui filtre et qui ne lisse pas, et une contrainte structurelle

Deux détails de conception méritent chacun un paragraphe, parce qu'ils se perdent facilement et qu'ils commandent le reste.

**Premier détail : l'encodeur est une loi de filtrage, pas une loi de lissage.** La différence est celle entre \(e_\theta(z_t \mid o_{\le t}, a_{<t})\) et une loi qui conditionnerait sur **toute** la séquence, y compris les observations **futures**. La seconde donnerait de meilleures estimations du latent, parce qu'elle en sait plus. On choisit la première, et la raison est pragmatique : le modèle est destiné à **planifier**, et au moment de planifier il n'y a pas de futur disponible. Entraîner un encodeur qui a besoin du futur produirait un modèle inutilisable en ligne. C'est, dans un autre domaine, exactement l'interdiction de la **fuite d'information** que la semaine 7 a posée sur les données financières.

{{% comment %}}SOURCE: PLANET p.3-4{{% /comment %}}

**Second détail, et c'est une contrainte structurelle : toute l'information sur les observations doit passer par l'étape d'échantillonnage de l'encodeur.** Si une information sur l'image atteint le décodeur par un autre chemin, par exemple parce que la part déterministe \(h_t\) reçoit directement l'observation encodée, alors un **raccourci déterministe** relie les entrées aux reconstructions. Le modèle apprend alors à reconstruire parfaitement sans que le latent ne contienne quoi que ce soit, le terme de divergence tombe à zéro sans rien avoir appris, et le modèle est incapable d'imaginer, puisqu'imaginer consiste précisément à se passer de l'observation. Regardez de nouveau le code de la section 13.3 : `enc_obs` entre **uniquement** dans `self.tete_post`, et jamais dans `self.cellule`. Ce n'est pas un hasard de rédaction.

{{% comment %}}SOURCE: PLANET p.4{{% /comment %}}

L'ensemble se décrit de deux façons, et les deux sont justes : c'est un **filtre de Kalman non linéaire**, où un état caché est propagé puis corrigé par une observation ; et c'est un **auto-encodeur variationnel séquentiel**, où la loi a priori du latent n'est pas fixe mais produite par la transition. Si l'une des deux lectures vous parle plus que l'autre, gardez celle-là.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

---

## Le code de la perte, et les nats libres

**Le code.** La perte complète, en comptant les trois termes et le garde-fou dont je parle juste après.

```python
import torch
import torch.nn.functional as F


def perte_du_modele(modele, obs, actions, recompenses, nats_libres=3.0, beta_kl=1.0):
    """Une passe d'entrainement du modele du monde sur un lot de tronçons.

    obs         : (B, L, C, H, W)  images du tronçon
    actions     : (B, L, dim_a)
    recompenses : (B, L)
    Rend la perte totale et les trois termes, pour les tracer separement.
    """
    B, L = obs.shape[0], obs.shape[1]
    h = torch.zeros(B, modele.dim_h, device=obs.device)
    z = torch.zeros(B, modele.dim_z, device=obs.device)

    perte_obs, perte_rec, perte_kl = 0.0, 0.0, 0.0
    enc = modele.encodeur_image(obs.flatten(0, 1)).view(B, L, -1)

    for t in range(L):
        h, prior, post = modele.avancer(h, z, actions[:, t], enc_obs=enc[:, t])
        z = post.rsample()                       # UN echantillon reparametre

        # Reconstruction : log-vraisemblance gaussienne de variance unite = EQM.
        perte_obs = perte_obs + F.mse_loss(modele.decodeur(h, z), obs[:, t])
        perte_rec = perte_rec + F.mse_loss(modele.tete_recompense(h, z).squeeze(-1),
                                           recompenses[:, t])

        # Complexite : divergence entre l'encodeur et la transition,
        # ecretee par le bas a "nats_libres" nats.
        kl = torch.distributions.kl_divergence(post, prior).sum(-1)
        perte_kl = perte_kl + kl.clamp(min=nats_libres).mean()

    totale = perte_obs + perte_rec + beta_kl * perte_kl
    return totale, (perte_obs, perte_rec, perte_kl)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\ln p_\theta(o_t \mid z_t)\) | terme de reconstruction de l'image | `F.mse_loss(modele.decodeur(...), ...)` |
| \(\ln p_\theta(r_t \mid z_t)\) | terme de reconstruction de la récompense | `perte_rec` |
| \(\KL[\,e_\theta \,\|\, p_\theta\,]\) | terme de complexité | `kl` |
| un échantillon reparamétré | la reparamétrisation de la semaine 10 | `post.rsample()` |
| trois nats libres | le garde-fou du paragraphe suivant | `kl.clamp(min=nats_libres)` |
| \(\beta_{\mathrm{KL}}\) | poids du terme de complexité | `beta_kl` |
| \(B, L\) | taille de lot et longueur de tronçon | `B`, `L` |

> [!WARNING]
 **Les nats libres (*free nats*) sont la ligne la plus facile à mal lire de ce code, et elle est indispensable.** Le terme de complexité est une divergence, donc positif, donc l'optimiseur a toujours intérêt à le réduire. S'il y parvient trop bien, l'encodeur devient égal à la transition, c'est-à-dire que le latent cesse de dépendre de l'observation : le modèle a réduit sa perte en devenant aveugle. L'écrêtage par le bas, `kl.clamp(min=3.0)`, dit : **tant que la divergence est sous trois nats, elle ne coûte rien**. Le gradient de ce terme est alors nul, et toute la pression retombe sur la reconstruction. On accorde au modèle un budget d'information gratuit, et on ne lui facture que ce qu'il dépense au-delà. Attention au sens de l'écrêtage : ce n'est **pas** un plafond, c'est un plancher sous lequel la pénalité est désactivée.

{{% comment %}}SOURCE: PLANET p.12{{% /comment %}}

---
