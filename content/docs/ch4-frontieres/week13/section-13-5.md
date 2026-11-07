---
title: "13.5 Planifier dans le latent : la semaine 3 revient, et elle revient par la grande porte"
weight: 6
---

## Un retour que j'attendais depuis dix semaines

Je voudrais marquer un temps d'arrêt, parce que ce qui suit est, de mon point de vue, le meilleur argument en faveur de la structure de ce cours.

Souvenez-vous de la semaine 3. C'était la première méthode que nous ayons écrite, avant toute valeur, avant tout gradient de politique, avant le moindre réseau cible. La **méthode d'entropie croisée** : on tire un paquet de candidats, on les évalue, on garde les meilleurs, on ajuste la loi de tirage sur ces meilleurs, et on recommence. Quatre lignes, aucune théorie, et nous l'avons quittée sur un constat sévère : elle ne tient pas sur un problème à récompense rare, et la semaine 3 l'a montrée échouer. Depuis, dix semaines de machinerie de plus en plus sophistiquée.

Et voici le planificateur de l'architecture que nous venons de construire : c'est **la méthode d'entropie croisée**. Pas une variante lointaine, pas une cousine : la même boucle, avec les mêmes quatre lignes, appliquée à des suites d'actions au lieu de jeux de poids, et évaluée dans un modèle appris au lieu de l'environnement réel.

Cela vaut la peine de comprendre pourquoi elle convient ici alors qu'elle ne convenait pas là. Trois raisons. D'abord, **la dimension du problème a changé de nature** : en semaine 3 nous lui demandions d'optimiser les poids d'un réseau, c'est-à-dire des dizaines de milliers de paramètres ; ici nous lui demandons une suite de douze actions de quelques composantes, soit quelques dizaines de nombres. Ensuite, **le signal n'est plus rare** : nous évaluons un plan dans un modèle qui prédit une récompense à chaque pas, et non le résultat binaire d'un épisode complet. Enfin, **l'évaluation est redevenue bon marché** : évaluer mille plans dans un modèle latent coûte mille passes d'un petit réseau, et non mille épisodes réels.

Le choix tient aussi à deux propriétés de cette méthode que je veux nommer. Sa **robustesse** : elle n'a pas de pas d'apprentissage à régler, pas de gradient à faire exploser, pas d'instabilité à surveiller. Et un fait mesuré qui est, accessoirement, la licence du laboratoire de cette semaine : **avec la vraie dynamique du simulateur, elle résout toutes les tâches considérées**. Autrement dit, quand le modèle est parfait, ce planificateur suffit. Tout ce qui manque ensuite est dans le modèle, pas dans la recherche.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

> [!TIP]
 **La leçon de méthode, et elle vaut au-delà de cette semaine.** Une méthode n'est jamais bonne ou mauvaise dans l'absolu : elle est bonne ou mauvaise **sur une structure de problème**. La méthode d'entropie croisée est inadaptée à l'optimisation des poids d'un réseau sous récompense rare, et excellente pour l'optimisation d'une courte suite d'actions sous récompense dense. Si vous retenez cela, vous avez gagné quelque chose de plus durable que n'importe quel algorithme de ce cours.

---

## Replanifier à chaque pas, et tout oublier à chaque observation

Le planificateur n'est pas appelé une fois par épisode. Il est appelé **à chaque pas**, et il recommence de zéro. C'est de la **commande prédictive** (*model-predictive control*) : on planifie sur un **horizon de planification** (*planning horizon*) \(H\), on joue **seulement la première action** du plan trouvé, on reçoit une nouvelle observation, et on replanifie entièrement. Le plan n'est jamais exécuté jusqu'au bout ; il sert à décider d'un seul pas. L'intérêt est évident : le plan s'adapte à ce qui arrive, et les erreurs du modèle aux pas lointains n'ont pas le temps de se payer, puisqu'on ne les jouera jamais.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

**L'objet que le planificateur optimise est une loi sur les suites d'actions**, et non une action. Elle est gaussienne et diagonale, donc entièrement décrite par une moyenne et un écart-type par pas et par composante :

$$
a_{t:t+H} \sim \mathcal{N}\big(\mu_{t:t+H},\; \sigma^2_{t:t+H}\,\mathbb{I}\big)
$$

> [!IMPORTANT]
 **Et voici le détail que l'on omet presque toujours en le résumant : cette loi est remise à moyenne nulle et variance unité après chaque nouvelle observation.** Le planificateur ne réutilise **pas** le plan du pas précédent comme point de départ. Cela semble du gaspillage, puisque le plan du pas précédent était probablement bon et que rien n'a beaucoup changé en un pas. La raison est précise : réutiliser la loi précédente enferme la recherche dans un **optimum local**. Une loi déjà concentrée autour d'un plan ne propose plus que des variantes de ce plan, et si le monde vient de rendre ce plan mauvais, le planificateur mettra plusieurs pas à s'en apercevoir, voire ne s'en apercevra jamais. On préfère payer dix itérations de recherche à chaque pas et garder une recherche qui **reste capable de changer d'avis**.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

---

## L'algorithme complet, et le fait qu'aucune image n'est jamais produite

**L'équation.** Voici le planificateur en entier. Il s'écrit comme un algorithme plutôt que comme une formule, et c'est honnête : c'est un algorithme.

Initialiser la loi sur les suites d'actions, puis répéter \(I\) fois :

$$
\mu_{t:t+H} \leftarrow 0, \qquad \sigma_{t:t+H} \leftarrow 1
$$

$$
a^{(j)}_{t:t+H} \sim \mathcal{N}\big(\mu_{t:t+H},\, \sigma^2_{t:t+H}\mathbb{I}\big), \qquad j = 1 \dots J
$$

$$
z^{(j)}_{t:t+H+1} \;\sim\; e_\theta(z_t \mid o_{1:t}, a_{1:t-1}) \prod_{k=t+1}^{t+H+1} p_\theta\big(z_k \mid z_{k-1}, a^{(j)}_{k-1}\big)
$$

$$
G^{(j)} \;=\; \sum_{k=t+1}^{t+H+1} \E\big[\,p_\theta(r_k \mid z^{(j)}_k)\,\big]
$$

$$
\mathcal{K} \leftarrow \operatorname{argsort}\big(\{G^{(j)}\}_{j=1}^{J}\big)_{1:K}
$$

$$
\mu_{t:t+H} = \frac{1}{K}\sum_{j \in \mathcal{K}} a^{(j)}_{t:t+H}, \qquad
\sigma_{t:t+H} = \frac{1}{K-1}\sum_{j \in \mathcal{K}} \big\lvert a^{(j)}_{t:t+H} - \mu_{t:t+H} \big\rvert
$$

puis renvoyer la **première** action \(\mu_t\).

{{% comment %}}SOURCE: PLANET alg. 2 p.12{{% /comment %}}

Reconnaissez-vous la semaine 3 ? Tirer \(J\) candidats, les évaluer, trier, garder les \(K\) meilleurs, ajuster moyenne et dispersion sur eux, recommencer. La seule nouveauté est la troisième ligne, qui dit comment on évalue : on part du latent **courant**, obtenu par l'encodeur depuis l'observation réelle, et on déroule la loi de transition **a priori** le long de la suite d'actions candidate.

Trois remarques pratiques sur cet algorithme, et chacune économise beaucoup de calcul.

**Une seule trajectoire par candidat suffit.** On pourrait, pour chaque suite d'actions, échantillonner dix trajectoires et moyenner leurs retours, afin de réduire la variance de l'évaluation. Ce n'est pas rentable : à budget de calcul égal, il vaut mieux évaluer **mille suites une fois** que cent suites dix fois. L'optimisation progresse par la diversité des candidats, pas par la précision de leur évaluation.

**Aucune image n'est jamais générée.** Regardez la quatrième ligne : le retour d'un candidat est une somme de récompenses prédites, et la récompense est une fonction **du latent**. Le décodeur d'images, qui est de loin le réseau le plus coûteux de l'architecture, n'est appelé **nulle part** dans le planificateur. C'est ce qui rend abordable un lot de mille candidats sur douze pas : douze mille passes d'un petit réseau dense, et pas une seule déconvolution.

**Les réglages, pour que vous ayez les ordres de grandeur en tête** : horizon \(H = 12\), itérations \(I = 10\), candidats \(J = 1000\), élites \(K = 100\). Mille candidats dont on garde les cent meilleurs, dix fois de suite, à chaque pas d'environnement.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}
{{% comment %}}SOURCE: PLANET p.12{{% /comment %}}

**Le code.** Le planificateur, écrit pour être lisible plutôt que rapide.

```python
import torch


@torch.no_grad()
def planifier(modele, h0, z0, dim_a, horizon=12, n_iter=10, n_cand=1000, k_elite=100):
    """Methode d'entropie croisee sur des suites d'actions, dans le latent.

    h0, z0 : etat du modele apres encodage de l'observation courante.
    Rend la PREMIERE action de la meilleure suite trouvee.
    """
    # La loi sur les suites est remise a zero a chaque appel : c'est voulu.
    mu = torch.zeros(horizon, dim_a)
    sigma = torch.ones(horizon, dim_a)

    for _ in range(n_iter):
        # 1. Tirer J suites d'actions candidates.
        bruit = torch.randn(n_cand, horizon, dim_a)
        candidats = (mu + sigma * bruit).clamp(-1.0, 1.0)

        # 2. Les evaluer en deroulant la transition a priori. Aucune image.
        h = h0.expand(n_cand, -1).contiguous()
        z = z0.expand(n_cand, -1).contiguous()
        retours = torch.zeros(n_cand)
        for k in range(horizon):
            h, prior, _ = modele.avancer(h, z, candidats[:, k], enc_obs=None)
            z = prior.sample()
            retours += modele.tete_recompense(h, z).squeeze(-1)

        # 3. Garder les K meilleures, 4. rajuster la loi sur elles.
        elites = candidats[retours.topk(k_elite).indices]
        mu = elites.mean(dim=0)
        sigma = (elites - mu).abs().sum(dim=0) / (k_elite - 1)

    return mu[0]          # commande predictive : on ne joue que le premier pas
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_{t:t+H}, \sigma_{t:t+H}\) | loi sur les suites d'actions, remise à zéro à chaque appel | `mu`, `sigma` |
| \(J\) | nombre de candidats, mille | `n_cand` |
| \(K\) | nombre d'élites, cent | `k_elite` |
| \(I\) | itérations de la recherche, dix | `n_iter` |
| \(H\) | horizon de planification, douze | `horizon` |
| \(a^{(j)}_{t:t+H}\) | les suites candidates | `candidats` |
| \(G^{(j)}\) | retour imaginé du candidat \(j\) | `retours` |
| \(\mathcal{K}\) | indices des élites | `retours.topk(k_elite).indices` |
| \(p_\theta(z_k \mid z_{k-1}, a_{k-1})\) | transition a priori, sans observation | `modele.avancer(..., enc_obs=None)` |
| \(\mu_t\) | la seule action réellement jouée | `mu[0]` |

Le `@torch.no_grad()` de la première ligne n'est pas une optimisation : c'est un **énoncé**. Cette recherche ne calcule aucun gradient, ne met à jour aucun paramètre, et ne laisse aucune trace. Elle est **sans dérivée**, et c'est exactement ce que la section 13.8 va lui reprocher.

---
