---
title: "8.8 A2C"
weight: 9
---

## Un acteur, un critique, et deux façons de les câbler

Donnons enfin les noms, parce qu'ils sont justes et qu'ils aident à penser.

Le réseau qui représente la politique est l'**acteur** (*actor*) : c'est lui qui agit, c'est lui qui dit quoi faire. Le réseau de valeur est le **critique** (*critic*) : il n'agit jamais, il commente, et il commente en répondant à une seule question, « à quel point cet état était-il prometteur ? », par le nombre \(\hat v(s,\mathbf{w})\). L'acteur propose, le critique évalue, et l'écart entre ce qui est arrivé et ce que le critique annonçait est le signal d'apprentissage de l'acteur. L'ensemble porte le nom d'**acteur-critique à avantage** (*advantage actor-critic*), abrégé **A2C**.

{{% comment %}}SOURCE: LAPAN ch.12 p.360{{% /comment %}}

Il y a deux manières de câbler ces deux réseaux, et la décision d'architecture **est** la différence entre les deux images qui suivent. La première solution consiste à garder **deux réseaux indépendants** : les observations entrent dans les deux, l'un sort une distribution \(\pi(a\mid s,\theta)\), l'autre sort un nombre \(\hat v(s,\mathbf{w})\), et ils ne partagent rien. C'est ce que montre la **Figure 8-3**.

{{< bookfig src="08-03.png" week="08" >}}

La seconde solution consiste à leur donner un **tronc commun** (*shared body*) suivi de **deux têtes** : les premières couches sont partagées, puis le chemin se sépare en une tête qui produit les probabilités d'action et une tête qui produit une seule valeur. C'est ce que montre la **Figure 8-4**, et c'est la même manœuvre que l'architecture duale de la semaine 6, à ceci près que les deux têtes ne calculent plus deux morceaux d'une même quantité mais deux quantités de nature différente.

{{< bookfig src="08-04.png" week="08" >}}

{{% comment %}}SOURCE: LAPAN ch.12 p.360{{% /comment %}}

Le tronc commun est la solution employée en pratique, pour deux raisons d'efficacité et de convergence qu'il vaut la peine de séparer. L'efficacité d'abord : sur une entrée d'image, les couches de convolution représentent l'essentiel du coût de calcul et l'essentiel des paramètres, et les calculer une fois au lieu de deux divise la facture par deux. La convergence ensuite, et c'est l'argument le plus intéressant : les caractéristiques de bas niveau utiles pour **décider** sont largement les mêmes que celles utiles pour **évaluer**. Détecter la balle et la raquette sert aux deux têtes. Le tronc commun les apprend donc une fois, avec le double de signal d'entraînement, et il les apprend mieux.

{{% comment %}}SOURCE: LAPAN ch.12 p.360{{% /comment %}}

> [!IMPORTANT]
 **\(\theta\) et \(\mathbf{w}\) apparaissent pour la première fois sur la même page, et je vous demande de les tenir séparés même quand le code les mélange.** \(\theta\) désigne les paramètres de l'**acteur**, ceux dont dépend \(\pi(a\mid s,\theta)\). \(\mathbf{w}\) désigne les poids du **critique**, ceux dont dépend \(\hat v(s,\mathbf{w})\). Ils ont leur propre gradient, leur propre objectif, et en principe leur propre pas d'apprentissage. Avec un tronc commun, ils désignent des ensembles de poids qui **se recouvrent physiquement** : les paramètres du tronc appartiennent aux deux. Cela ne les confond pas pour autant, parce que les deux mises à jour restent distinctes : le gradient de la perte de politique ne doit jamais remonter dans la tête de valeur, ni le gradient de la perte de valeur dans la tête de politique. C'est très exactement la raison pour laquelle le code contiendra un `detach()`, et c'est pourquoi je place cet encadré avant le code et non après.

---

## La boucle d'entraînement, en six étapes

Voici l'algorithme complet. Comparez-le à celui de la section 8.3 : les étapes 1, 2 et 6 sont identiques, et tout ce qui a changé tient dans les étapes 3, 4 et 5.

> **A2C, acteur-critique à avantage**
>
> 1. Initialiser les paramètres du réseau avec des poids aléatoires.
> 2. Jouer **\(N\) pas** dans l'environnement avec la politique courante \(\pi(\cdot\mid s,\theta)\), en enregistrant les triplets \((s_t, a_t, r_t)\). Noter que l'on ne joue plus des épisodes entiers, mais un nombre fixe de pas.
> 3. Poser \(R \leftarrow 0\) si l'épisode s'est terminé, et \(R \leftarrow \hat v(s_t,\mathbf{w})\) sinon. C'est ici que le critique remplace la queue de trajectoire qu'on n'a pas jouée.
> 4. Pour \(i\) allant de \(t-1\) jusqu'au début du segment, **à rebours** : accumuler \(R \leftarrow r_i + \gamma R\), puis accumuler le gradient de politique sur \(\theta\) et le gradient de valeur sur \(\mathbf{w}\).
> 5. Mettre à jour les paramètres : **dans le sens** du gradient de politique, pour maximiser la performance, et **dans le sens opposé** au gradient de valeur, pour minimiser l'erreur quadratique.
> 6. Répéter à partir de l'étape 2 jusqu'à convergence.

{{% comment %}}SOURCE: LAPAN ch.12 p.361{{% /comment %}}

L'étape 5 mérite un commentaire, parce qu'elle contient la seule asymétrie de signe de tout l'algorithme. Le gradient de politique se **monte** et le gradient de valeur se **descend**, parce que l'un pointe vers une performance à maximiser et l'autre vers une erreur à minimiser. Dans le code, cette asymétrie disparaît complètement : on la fait entrer dans la définition de la perte, en négociant le signe du terme de politique, et l'optimiseur descend ensuite sur la somme sans savoir que ses deux morceaux sont de nature contraire. C'est commode, et c'est aussi pourquoi la perte totale d'A2C est un nombre dont la valeur ne veut rien dire.

L'étape 3 est la nouveauté de fond, et elle mérite son équation. Le retour sur \(N\) pas utilisé comme échelle n'est plus un retour complet : c'est la somme des \(N\) récompenses réellement reçues, plus la valeur estimée de l'état où l'on s'est arrêté, actualisée du bon nombre de pas.

$$
G^{(N)}_t = \sum_{i=0}^{N-1}\gamma^i\, r_{t+i} \;+\; \gamma^N\, \hat v(s_{t+N},\mathbf{w})
$$

{{% comment %}}SOURCE: LAPAN ch.12 p.362-363{{% /comment %}}

Et voici une conséquence pratique immédiate, qui est la meilleure preuve que le critique sert à quelque chose. Dans un gradient de politique sans critique, l'horizon de déroulement doit valoir une dizaine de pas pour que la troncature soit acceptable. Avec un critique, il peut descendre à **quatre**, parce que la queue de la trajectoire n'est plus négligée : elle est **estimée**. Vous économisez six pas de collecte par échantillon, et vous obtenez une estimation de meilleure qualité.

{{% comment %}}SOURCE: LAPAN ch.12 p.362-363{{% /comment %}}

Une dernière observation, et c'est une bonne phrase à retenir pour les examens comme pour les entretiens d'embauche : **la même quantité \(G^{(N)}_t\) sert deux fois**, et à deux fins différentes. Elle est la **cible** de la régression du critique, puisque c'est la meilleure estimation disponible de ce que l'état valait. Et elle entre dans l'**avantage** \(G^{(N)}_t - \hat v(s_t,\mathbf{w})\) qui pondère le gradient de l'acteur. Une quantité, deux emplois, et c'est ce double emploi qui rend l'implémentation si compacte.

{{% comment %}}SOURCE: LAPAN ch.12 p.364{{% /comment %}}

---

## Les trois termes de la perte, et leurs signes

Nous pouvons maintenant écrire la perte complète. Elle a trois termes, et je vous demande de pouvoir dire, pour chacun, ce qu'il pousse et dans quel sens. La barre horizontale désigne la moyenne sur le lot.

$$
\mathcal{L} \;=\;
\underbrace{-\,\overline{\Adv(s,a)\,\log\pi(a\mid s,\theta)}}_{\text{politique}}
\;+\;
\underbrace{\overline{\big(\hat v(s,\mathbf{w}) - G^{(N)}\big)^2}}_{\text{valeur, erreur quadratique}}
\;+\;
\underbrace{\beta\;\overline{\textstyle\sum_a \pi(a\mid s,\theta)\log\pi(a\mid s,\theta)}}_{\text{entropie},\;=\,-\beta\, \overline{H(\pi)}}
$$

{{% comment %}}SOURCE: LAPAN ch.12 p.361 ; ch.12 p.367-368 (code){{% /comment %}}

Terme par terme.

Le **terme de politique** est celui de la section 8.3, avec l'avantage à la place du retour. Son signe moins est l'adaptateur montée-descente, et sa valeur ne signifie rien : c'est la perte qui n'est pas une perte.

Le **terme de valeur** est une honnête erreur quadratique moyenne entre la sortie du critique et la cible \(G^{(N)}\). Celui-là, vous pouvez le lire comme une perte : s'il ne descend pas, le critique n'apprend pas, et tout le reste est compromis puisque l'avantage se calcule à partir de lui.

Le **terme d'entropie** demande qu'on suive son signe jusqu'au bout, et c'est le seul endroit de la semaine où l'on peut se tromper d'un facteur \(-1\) sans que rien ne plante. L'entropie d'une politique vaut \(H(\pi) = -\sum_a \pi \log \pi\). Le terme écrit ci-dessus vaut \(\beta \sum_a \pi\log\pi\), c'est-à-dire \(-\beta H(\pi)\) : c'est l'entropie **niée**, multipliée par un coefficient positif. Comme l'optimiseur **minimise** la somme, minimiser \(-\beta H(\pi)\) revient à **maximiser** \(H(\pi)\), c'est-à-dire à pousser la politique vers l'uniformité. Le terme est donc bien une **prime** à l'indécision, écrite sous la forme négative qu'exige une perte minimisée. Vous retrouverez souvent la même idée énoncée dans l'autre sens : puisque l'entropie est maximale pour la distribution uniforme et que nous voulons pousser l'entraînement vers ce maximum, il faut **retrancher** l'entropie de la perte. Les deux formulations décrivent le même code.

{{% comment %}}SOURCE: LAPAN ch.12 p.368{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.11 p.345{{% /comment %}}

Et voici le code, qui est le cœur du laboratoire de cette semaine.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class ReseauActeurCritique(nn.Module):
    """Un tronc commun, deux tetes : une distribution, et un nombre."""

    def __init__(self, taille_obs: int, n_actions: int, largeur: int = 128):
        super().__init__()
        self.tronc = nn.Sequential(
            nn.Linear(taille_obs, largeur), nn.ReLU(),
        )
        self.tete_politique = nn.Linear(largeur, n_actions)   # LOGITS
        self.tete_valeur = nn.Linear(largeur, 1)              # un seul nombre

    def forward(self, obs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        tronc = self.tronc(obs)
        return self.tete_politique(tronc), self.tete_valeur(tronc)


def perte_a2c(reseau, etats_t, actions_t, cibles_t, beta: float = 0.01):
    """Les trois termes, dans l'ordre de l'equation, et un seul scalaire en sortie."""
    logits_t, valeur_t = reseau(etats_t)
    valeur_t = valeur_t.squeeze(-1)                       # (B, 1) -> (B,)

    # --- terme de VALEUR : une vraie erreur quadratique, cible = G^(N)
    perte_valeur_t = F.mse_loss(valeur_t, cibles_t)

    # --- terme de POLITIQUE : l'avantage ponderant la log-probabilite.
    #     detach() : le gradient de CE terme ne doit pas entrer dans le critique.
    avantage_t = cibles_t - valeur_t.detach()
    log_prob_t = F.log_softmax(logits_t, dim=1)
    lot = range(len(actions_t))
    perte_politique_t = -(avantage_t * log_prob_t[lot, actions_t]).mean()

    # --- terme d'ENTROPIE : beta fois l'entropie NIEE, donc minimiser = pousser H vers le haut.
    prob_t = F.softmax(logits_t, dim=1)
    perte_entropie_t = beta * (prob_t * log_prob_t).sum(dim=1).mean()

    return perte_politique_t, perte_valeur_t, perte_entropie_t
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\theta\) | paramètres de l'acteur | `tronc` + `tete_politique` |
| \(\mathbf{w}\) | poids du critique | `tronc` + `tete_valeur` |
| \(\pi(a\mid s,\theta)\) | politique | `prob_t` |
| \(\log\pi(a\mid s,\theta)\) | log-probabilités | `log_prob_t` |
| \(\hat v(s,\mathbf{w})\) | sortie du critique | `valeur_t` |
| \(G^{(N)}\) | retour à \(N\) pas, la cible | `cibles_t` |
| \(\Adv(s,a) = G^{(N)} - \hat v(s,\mathbf{w})\) | avantage, échelle du gradient | `avantage_t` |
| \(\mathcal{L}_\pi\) | terme de politique | `perte_politique_t` |
| \(\overline{(\hat v - G^{(N)})^2}\) | terme de valeur | `perte_valeur_t` |
| \(\mathcal{L}_H = -\beta\,\overline{H(\pi)}\) | terme d'entropie | `perte_entropie_t` |
| \(\beta\) | coefficient d'entropie | `beta` |

Je laisse la fonction renvoyer les **trois** termes séparément plutôt que leur somme, et ce n'est pas un détail de style. C'est ce qui vous permet de les journaliser séparément, de mesurer la variance du gradient de politique seul comme en section 8.6, et de vérifier leurs ordres de grandeur respectifs. Vous les additionnerez à l'appel, en une ligne.

---

## Trois détails qui coûtent chacun une journée

Ces trois points ne figurent dans aucun énoncé mathématique de la semaine, et chacun d'eux a fait perdre du temps à beaucoup de monde. Lisez-les avant d'écrire le laboratoire, pas après.

**Premier détail : `detach()` est une question de correction, pas d'efficacité.** Regardez la ligne `avantage_t = cibles_t - valeur_t.detach()`. Sans le `detach()`, l'avantage reste attaché au graphe de calcul par l'intermédiaire de `valeur_t`, et le gradient du terme de **politique** descend alors dans la tête de **valeur**. Le résultat n'est pas une inefficacité, c'est un objectif différent : votre critique se met à être optimisé pour rendre l'avantage grand, ce qui n'a aucun sens, au lieu d'être optimisé pour prédire le retour. La semaine 7 vous a appris à distinguer `detach()` de `torch.no_grad()` en demandant lequel était une question de vitesse et lequel une question de justesse. Voici l'exemple canonique du second cas.

{{% comment %}}SOURCE: LAPAN ch.12 p.368{{% /comment %}}

**Deuxième détail : l'écrêtage du gradient** (*gradient clipping*)**, et pourquoi il est plus important ici qu'en semaine 6.** Si la norme \(L_2\) du vecteur de gradient dépasse un seuil, on ramène le vecteur à ce seuil en conservant sa direction. L'effet est d'empêcher un pas d'optimisation de déplacer la politique **trop loin**. La raison pour laquelle cela compte davantage dans une méthode de gradient de politique que dans un réseau Q profond est subtile et vaut d'être comprise : si votre politique change brutalement, les données que vous collecterez ensuite viendront d'une politique très différente de celle que vous avez évaluée, et le gradient suivant sera calculé sur une distribution d'états qui n'a plus de rapport avec la précédente. Vous ne cassez pas seulement une mise à jour, vous cassez la validité de la suivante.

{{% comment %}}SOURCE: LAPAN ch.12 p.362{{% /comment %}}

**Troisième détail, le plus déroutant : le paramètre `eps` d'Adam.** Avec les réglages employés sur un jeu Atari, il faut mettre `eps=1e-3` au lieu de la valeur par défaut \(10^{-8}\). Avec la valeur par défaut, l'entraînement ne converge **pas du tout**. Il n'existe pas d'explication mathématiquement rigoureuse de ce phénomène, et je ne vais pas vous en inventer une. La conjecture raisonnable, et je vous la donne explicitement comme une conjecture, est que ce paramètre apparaît au dénominateur de la mise à jour d'Adam : diviser par une quantité de l'ordre de \(10^{-8}\) produit des pas effectifs énormes dès que le gradient est petit, et une méthode de gradient de politique, dont les gradients sont déjà très dispersés, n'y survit pas.

{{% comment %}}SOURCE: LAPAN ch.12 p.366{{% /comment %}}

> [!WARNING]
 **Un cas où un hyperparamètre d'optimiseur décide du résultat, et ce n'est pas celui qu'on surveille.** Ce qui rend cet exemple instructif n'est pas la valeur \(10^{-3}\), qui ne se transporte probablement pas à votre problème. C'est qu'un paramètre que presque personne ne touche, dont presque personne ne connaît la valeur par défaut, et qui n'apparaît dans aucune équation de cette semaine, fait la différence entre un agent qui apprend et un agent qui n'apprend pas. Quand votre A2C refuse d'apprendre, après avoir vérifié les signes et le `detach()`, regardez `eps`. Et notez-le dans le tableau d'hyperparamètres de votre rapport : un réglage non documenté est un résultat non reproductible.

Pour finir, les hyperparamètres employés sur un jeu Atari, donnés à titre d'ordre de grandeur et non de recette : \(\gamma = 0{,}99\), pas d'apprentissage \(0{,}001\), coefficient d'entropie \(\beta = 0{,}01\), taille de lot 128, cinquante environnements en parallèle, horizon de déroulement \(N = 4\), seuil d'écrêtage du gradient \(0{,}1\). Deux remarques les accompagnent. La première est qu'ils ne sont **pas réglés** : ils fonctionnent, et il reste probablement du jeu. La seconde est le critère d'arrêt employé, une récompense moyenne supérieure à 18 sur les cent derniers épisodes, alors que le maximum du jeu est 21 : au-delà de ce seuil, l'agent gagne déjà systématiquement, et le temps supplémentaire ne sert qu'à polir. Fixer son critère d'arrêt là plutôt qu'au maximum théorique est la leçon de la semaine 7, appliquée.

{{% comment %}}SOURCE: LAPAN ch.12 p.362{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.12 p.366{{% /comment %}}

Enfin, l'architecture pour une entrée d'image, pour que vous l'ayez si votre projet en a besoin : trois couches de convolution, 32 filtres de \(8 \times 8\) au pas 4, puis 64 filtres de \(4 \times 4\) au pas 2, puis 64 filtres de \(3 \times 3\) au pas 1, chacune suivie d'une activation ReLU ; un aplatissement ; puis **deux têtes** identiques en forme, chacune une couche de 512 unités avec ReLU suivie d'une sortie, l'une de taille `n_actions` et l'autre de taille 1. La passe avant renvoie le couple. Et l'entrée est divisée par 255 pour ramener les intensités dans \([0,1]\), comme en semaine 5.

{{% comment %}}SOURCE: LAPAN ch.12 p.363{{% /comment %}}

---
