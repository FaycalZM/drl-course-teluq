---
title: "12.7 Entraîner un modèle qu'on ne peut pas vérifier"
weight: 8
---

## Comment un épisode est produit, et où il est rangé

La boucle de données est plus simple que celle de l'auto-jeu, et il n'y a plus de porte d'évaluation : on joue, on range, on entraîne.

Dans une position réelle, on construit la racine avec \(h_\theta\), on lance la recherche, on en tire la politique par les comptages de visites exactement comme en section 12.5, on choisit une action, et **on avance l'environnement réel d'un pas**. Puis on recommence depuis la nouvelle position. L'épisode complet, avec pour chaque pas l'observation, l'action jouée, la politique issue de la recherche et la récompense reçue, part dans un tampon de rejeu.

{{% comment %}}SOURCE: LAPAN ch.20 p.624 (image){{% /comment %}}

Notez la division du travail : la recherche se déroule **entièrement** dans les états cachés, sans toucher au monde ; le monde n'est touché qu'une fois par coup réellement joué. C'est exactement l'inverse de la section 12.3, où chaque passage de recherche interrogeait le modèle du jeu des dizaines de fois.

---

## Un déroulement de cinq pas depuis un décalage aléatoire

**L'intuition.** Le modèle doit apprendre à prédire plusieurs pas d'affilée, et pas seulement un. Si nous ne l'entraînions que sur un pas, rien ne garantirait que son état caché reste utilisable après trois applications de la dynamique, et la recherche descend bien plus profond que cela. Nous allons donc l'entraîner sur des **chaînes** : prendre un épisode, se placer à un instant quelconque, et demander au modèle de prédire les cinq pas suivants d'affilée, à partir d'une seule observation réelle.

C'est le **déroulement** (*unrolling*) de la semaine 6, dans un autre contexte : un **déroulement sur cinq pas**, depuis un **décalage** tiré au hasard dans l'épisode. Le décalage aléatoire est ce qui garantit que le modèle voit des débuts, des milieux et des fins de partie.

{{% comment %}}SOURCE: LAPAN ch.20 p.624-625 (images){{% /comment %}}

Une conséquence d'implémentation à anticiper, parce qu'elle surprend : le lot d'entraînement n'est **pas un tenseur**. C'est une **liste de tenseurs**, un par pas du déroulement, car au pas \(k\) les actions, les politiques cibles et les récompenses cibles diffèrent d'un élément du lot à l'autre. On empile par pas, pas par épisode.

{{% comment %}}SOURCE: LAPAN ch.20 p.637{{% /comment %}}

---

## Trois cibles empilées, et une seule chose contre laquelle le modèle est vérifié

**L'équation.** À chaque pas du déroulement, le modèle produit trois quantités et chacune a sa cible :

$$
\mathcal{L} \;=\; \sum_{k=0}^{K-1} w_k \Big[ \underbrace{-\,\pi^{\mathrm{MCTS}}_k \cdot \log \pi_k}_{\text{politique}} \;+\; \underbrace{(v_k - z_k)^2}_{\text{valeur}} \;+\; \underbrace{(r_k - u_k)^2}_{\text{récompense}} \Big]
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.639{{% /comment %}}

Trois cibles, trois provenances, et il faut les distinguer avec soin :

- \(\pi^{\mathrm{MCTS}}_k\) est la **politique issue de la recherche** au pas correspondant de l'épisode, c'est-à-dire les fréquences de visite de la racine. La perte est une entropie croisée, comme en section 12.5.
- \(z_k\) est la **somme actualisée des récompenses jusqu'à la fin de l'épisode** depuis ce pas. C'est un retour observé, et la perte est une erreur quadratique.
- \(u_k\) est la **récompense immédiate observée** à ce pas, et c'est la cible de la tête de récompense de la dynamique, encore en erreur quadratique.

**Le code.** La passe avant est une chaîne, et elle mérite d'être lue lentement.

```python
import torch.nn.functional as F


def perte_du_deroulement(reseaux, observation, actions, cibles, K=5):
    """Une seule application de h_theta, puis K fois {f_theta, g_theta}.

    cibles.politique[k], cibles.valeur[k], cibles.recompense[k] : les trois
    cibles du pas k, construites depuis l'episode range dans le tampon.
    """
    etat = reseaux.representation(observation)          # h_theta, UNE SEULE FOIS
    perte_totale = 0.0

    for k in range(K):
        logits, valeur = reseaux.prediction(etat)       # f_theta(s^k)

        perte_k = F.cross_entropy(logits, cibles.politique[k]) \
                + F.mse_loss(valeur.squeeze(-1), cibles.valeur[k])

        a = une_parmi_n(actions[k], reseaux.nb_actions)
        recompense, etat = reseaux.dynamique(etat, a)   # g_theta : s^{k+1}, r^{k+1}

        perte_k = perte_k + F.mse_loss(recompense.squeeze(-1), cibles.recompense[k])

        poids = 1.0 if k == 0 else 0.5                  # voir l'avertissement
        perte_totale = perte_totale + poids * perte_k

    return perte_totale
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(K\) | longueur du déroulement, cinq pas | `K=5` |
| \(h_\theta(o)\) | une seule application, sur l'observation réelle | `reseaux.representation(observation)` |
| \(s^k\) | état caché courant, reconduit par la boucle | `etat` |
| \(\pi_k\), \(v_k\) | politique et valeur prédites au pas \(k\) | `logits`, `valeur` |
| \(r_k\) | récompense prédite par la dynamique | `recompense` |
| \(\pi^{\mathrm{MCTS}}_k\) | cible de politique, fréquences de visite | `cibles.politique[k]` |
| \(z_k\) | cible de valeur, retour observé jusqu'à la fin | `cibles.valeur[k]` |
| \(u_k\) | cible de récompense, récompense immédiate observée | `cibles.recompense[k]` |
| \(w_k\) | pondération, \(1\) au premier pas et \(0{,}5\) ensuite | `poids` |

> [!IMPORTANT]
 **C'est le seul endroit de toute la méthode où le modèle appris est effectivement entraîné, et il n'est jamais confronté à un état réel.** Relisez la boucle : nulle part on ne compare \(s^{k+1}\) produit par la dynamique à l'état réel du jeu au pas suivant. Nulle part on ne demande au modèle de reconstruire une position. Le modèle n'est tenu que par ses **conséquences** : si les politiques, les valeurs et les récompenses prédites sont justes, l'état caché est bon, quoi qu'il contienne. C'est une idée très puissante et une idée dangereuse, et les deux faces vont ensemble. Puissante, parce qu'elle libère la méthode de tout besoin de comprendre le monde. Dangereuse, parce que vous n'avez **aucun diagnostic** disponible : quand le modèle se trompe, vous ne pouvez pas inspecter sa prédiction d'état pour voir ce qu'il a mal compris, puisqu'elle ne veut rien dire.

---

## Deux constantes qu'il ne faut pas recopier

Les hyperparamètres de cette méthode tiennent dans une petite classe de données : le nombre d'actions, la concentration de Dirichlet \(\alpha_{\mathrm{Dir}} = 0{,}3\) de la section 12.3, l'actualisation \(\gamma = 1\), la longueur de déroulement \(K = 5\), et un horizon maximal de coups par partie. Deux de ces valeurs demandent un avertissement, et chacune enseigne quelque chose.

{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}

**Première constante : l'horizon de coups, et une priorité d'opérateurs.** Vous rencontrerez cet horizon écrit comme une expression arithmétique du genre « un quart des cases du plateau, plus un », sous la forme `LIGNES * COLONNES >> 2 + 1`. En Python, `+` est **plus prioritaire** que `>>`. Cette expression se lit donc `(LIGNES * COLONNES) >> (2 + 1)`, c'est-à-dire \(42 \gg 3 = 5\), alors que l'intention était `(LIGNES * COLONNES >> 2) + 1`, c'est-à-dire \((42 \gg 2) + 1 = 11\). Le correctif tient en deux parenthèses.

> [!WARNING]
 **Le problème n'est pas l'écart de six, c'est que cinq est en dessous du minimum absolu du jeu.** Une partie de Puissance 4 ne peut pas être gagnée en moins de **sept** coups joués : quatre par le gagnant, trois par le perdant, dans le meilleur des cas imaginables. Un horizon de cinq coups coupe donc **toutes** les parties avant qu'aucune victoire ne soit possible, dans le jeu même que l'on prétend entraîner. Onze, au moins, est plausible comme plafond. C'est pour cette raison que ce cours vous demande de **redériver** une constante publiée au lieu de la recopier : pas par méfiance de principe, mais parce que la vérification est ici l'affaire de trente secondes de raisonnement sur le jeu, et qu'elle attrape une erreur qu'aucun test ne signalerait. Le laboratoire vous fera calculer vous-même l'horizon dont vous avez besoin, à partir de la taille du plateau et du nombre de jetons à aligner.

{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}

**Deuxième constante : la pondération \(0{,}5\), qui n'est pas ce qu'elle a l'air d'être.** Dans l'équation ci-dessus, les pas \(1\) à \(4\) du déroulement voient leur perte multipliée par \(0{,}5\), tandis que le pas \(0\) garde son poids entier. L'intention est de ne pas laisser les pas lointains, dont les prédictions sont forcément moins fiables, dominer l'apprentissage.

Je dois ici être honnête sur une différence que l'on présente parfois comme une équivalence. La méthode d'origine met à l'échelle le **gradient** à l'intérieur de la récurrence, et non la perte. Ce n'est pas la même opération : une mise à l'échelle placée **dans** la récurrence se **compose** à travers les pas de dynamique, de sorte que la contribution d'un pas lointain est atténuée une fois par pas traversé, alors qu'une constante \(0{,}5\) appliquée à la perte de chacun des pas \(1\) à \(4\) les atténue tous **de la même quantité**. Les deux dispositifs ont le même esprit et des effets différents. Ce cours écrit la version simple, parce que c'est elle que vous allez implémenter, et vous dit en même temps qu'elle n'est pas équivalente à l'autre.

{{% comment %}}SOURCE: LAPAN ch.20 p.625 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.639{{% /comment %}}

---

## Et une optimisation de la section 12.3 qui ne se transporte pas

Un détail pour finir, qui est un bon exercice de lucidité sur les optimisations.

La section 12.3 groupait plusieurs feuilles pour les étendre en un seul passage de réseau. Ici, ce n'est **pas possible**, et la raison n'est pas une question d'effort d'implémentation : la recherche de cette méthode est **déterministe**, de sorte que deux recherches lancées depuis le même arbre descendraient exactement le même chemin et aboutiraient à la même feuille. Il n'y a donc rien à grouper. L'astuce de la première méthode reposait sur la diversité des chemins, et cette diversité a disparu.

{{% comment %}}SOURCE: LAPAN ch.20 résumé, p.635{{% /comment %}}

---
