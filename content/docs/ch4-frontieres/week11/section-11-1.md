---
title: "11.1 Ce qu'on reproche à la méthode ε-gloutonne, et ce qu'il faut lui reprocher"
weight: 2
---

## Dix semaines de hasard injecté, résumées en deux lignes

Avant d'instruire le procès, récapitulons l'accusé, parce que le cours a employé deux formes de hasard et qu'elles se ressemblent plus qu'il n'y paraît.

Dans les **méthodes de valeur**, depuis la semaine 4, l'agent joue l'action de valeur maximale, sauf avec probabilité \(\varepsilon\) où il tire une action uniformément au hasard. Dans les **méthodes de politique**, depuis la semaine 8, la politique est déjà une distribution et l'on y ajoute une prime d'entropie, c'est-à-dire un terme qui pénalise une distribution trop concentrée et qui empêche donc la politique de s'effondrer sur une seule action. Ce terme domine au début de l'entraînement, puis le gradient de politique prend le dessus, et son coefficient demande un réglage pour fonctionner correctement.

{{% comment %}}SOURCE: LAPAN ch.18 p.549-550 (image){{% /comment %}}

Les deux mécanismes font pourtant la même chose, et je veux que cette phrase reste en tête pour toute la section : **pour explorer, nous introduisons du hasard dans nos actions**. La seule différence entre les deux familles est l'endroit où ce hasard est injecté, directement dans le choix de l'action pour l'une, dans la forme de la distribution pour l'autre.

{{% comment %}}SOURCE: LAPAN ch.18 p.550 (image){{% /comment %}}

Deux reproches sérieux sont adressés à cette façon de faire. Je vais les traiter séparément, parce que le premier est **faux** et que le second est le sujet de la semaine.

---

## La première accusation, et l'équation qui la réfute

Voici l'accusation telle qu'elle circule, et je la formule honnêtement avant de la démonter.

Dans une méthode de valeur, dit-elle, les actions aléatoires prises en cours de trajectoire introduisent un **biais** dans l'estimation des valeurs d'action. L'argument continue ainsi : l'équation de Bellman suppose que la valeur de l'état suivant est obtenue par l'action de valeur maximale, autrement dit que la suite de la trajectoire est produite par un comportement optimal ; mais avec une politique \(\varepsilon\)-gloutonne, l'agent joue parfois une action quelconque, ce morceau de trajectoire est stocké dans le tampon de rejeu, il y reste longtemps, et tant qu'il y est l'agent apprend de mauvaises valeurs.

{{% comment %}}SOURCE: LAPAN ch.18 p.550 (image){{% /comment %}}

Cette accusation est fausse pour la cible à un pas, et il faut une seule équation pour le voir. Reprenons la cible de la semaine 5, avec \(\Qtm\) le réseau cible :

$$
Y_t \;\defeq\; R_{t+1} + \gamma \max_{a'} \Qtm(S_{t+1}, a')
$$

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.6{{% /comment %}}
{{% comment %}}SOURCE: source-assets/notation.md{{% /comment %}}

Maintenant, cherchez dans cette équation l'action que l'agent a **réellement jouée** au pas \(t\). Elle n'y est pas. Le membre de droite contient la récompense observée, l'état suivant observé, et un **maximum sur les actions disponibles dans cet état suivant**. L'action \(A_t\) sert à décider quelle sortie du réseau on corrige, elle ne sert pas à construire la valeur vers laquelle on la corrige. Que \(A_t\) ait été choisie gloutonnement, au hasard, par un générateur de nombres aléatoires ou par un étudiant appuyant sur une touche, la cible est la même.

C'est exactement ce que veut dire **hors politique** (*off-policy*), et c'est la propriété que la semaine 3 a nommée, que la semaine 5 a exploitée et que la semaine 6 a disséquée. Une transition stockée \((s, a, r, s')\) est une donnée d'entraînement **valide quelle que soit la politique qui a choisi \(a\)**, et c'est précisément pour cette raison qu'un réseau Q profond a le droit d'avoir un tampon de rejeu. Si les actions aléatoires du passé biaisaient la cible, le tampon lui-même serait indéfendable, et avec lui les semaines 5, 6 et 9.

Voici la même chose en code, et je vous demande de regarder le tableau qui suit plus attentivement que d'habitude : il contient une ligne sans variable, et cette ligne est tout l'argument.

```python
import torch


def cible_q_un_pas(etats_suivants, recompenses, termines,
                   reseau_cible, gamma: float) -> torch.Tensor:
    """La cible a un pas. L'action JOUEE n'apparait nulle part ici."""
    with torch.no_grad():
        q_suivants = reseau_cible(etats_suivants)        # (lot, n_actions)
        meilleur_q = q_suivants.max(dim=1).values        # max SUR LES ACTIONS
        meilleur_q[termines] = 0.0                       # rien apres la fin
    return recompenses + gamma * meilleur_q
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(R_{t+1}\) | récompense observée sur la transition | `recompenses` |
| \(S_{t+1}\) | état suivant observé | `etats_suivants` |
| \(\Qtm\) | réseau cible de la semaine 5 | `reseau_cible` |
| \(\max_{a'}\) | maximum **sur les actions** disponibles en \(S_{t+1}\) | `.max(dim=1).values` |
| \(\gamma\) | facteur d'actualisation | `gamma` |
| \(Y_t\) | cible de la mise à jour | valeur de retour |
| \(A_t\) | action réellement jouée au pas \(t\) | **aucune : elle n'entre pas dans le calcul** |

> [!IMPORTANT]
 **Je dois insister, parce que c'est un contrôle que vous pouvez appliquer seuls à n'importe quelle méthode que vous lirez après ce cours.** Pour savoir si la politique de collecte peut biaiser une mise à jour, écrivez la cible et cherchez-y l'action jouée. Si l'action jouée n'apparaît que comme un **index** du côté gauche, celui de la prédiction que l'on corrige, la cible est indifférente à la politique de collecte et il n'y a pas de biais à craindre de ce côté. Si elle apparaît aussi à **droite**, dans la construction de la cible, alors la politique de collecte entre dans la mise à jour et le biais est réel. Ce contrôle prend trente secondes, il ne demande aucune théorie, et il tranche la question posée plus haut sans discussion.

---

## Où le biais existe vraiment, et ce que le cours a déjà payé pour lui

Je dois maintenant concéder la moitié honnête de l'accusation, parce qu'elle existe et parce que vous l'avez déjà rencontrée.

Dès que la cible ne porte plus sur un seul pas, l'action jouée **entre** dans le membre de droite. Voici la cible à \(n\) étapes de la section 6.6, écrite dans la notation du cours :

$$
G_{t:t+n} \;\defeq\; R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{\,n-1} R_{t+n}
 \;+\; \gamma^{\,n} \max_{a} \Qtm(S_{t+n}, a)
$$

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.6{{% /comment %}}

Regardez les récompenses intermédiaires \(R_{t+2}, \dots, R_{t+n}\). Elles ont été obtenues en jouant les actions que la **politique de comportement** a choisies, et le \(\max\) qui aurait dû se trouver devant chacune d'elles a été supprimé par l'approximation de la section 6.6 : on y suppose que l'action jouée à chaque pas intermédiaire était la bonne. Si cette politique jouait au hasard une fois sur cinq, cette supposition est fausse une fois sur cinq, et la cible est biaisée. La semaine 6 l'avait dit dans ces termes : le dépliage de Bellman rend un réseau Q profond **partiellement sur politique**, et la consigne pratique en découlait, être modeste dans le choix de \(n\).

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.6{{% /comment %}}

Voilà donc le compte exact. Le biais reproché à l'\(\varepsilon\)-glouton n'existe pas pour la cible à un pas, il existe pour une cible dépliée, il est proportionnel au nombre de pas dépliés, et ce cours l'a identifié, nommé et payé cinq semaines avant d'arriver ici. Ce n'est pas la raison pour laquelle nous changeons de méthode d'exploration aujourd'hui.

> [!NOTE]
 **Pourquoi je prends le temps de corriger une accusation plutôt que de l'omettre.** Cette affirmation circule, formulée exactement comme je l'ai formulée plus haut, y compris dans des textes sérieux, et vous la rencontrerez. Si je me contentais de ne pas la répéter, vous la liriez ailleurs et vous n'auriez aucun moyen de la trancher. En la posant, en l'examinant et en la rejetant pour le cas à un pas, je vous laisse autre chose qu'une opinion : une équation et un contrôle de trente secondes. C'est la même discipline que la semaine 10 a appliquée à une divergence mal écrite, et elle vaut mieux qu'un silence.

---

## La vraie accusation : une politique qui change à chaque pas

Passons au reproche qui tient, et qui organise toute la semaine.

Avec des actions aléatoires injectées dans la trajectoire, **la politique de collecte change à chaque pas**. À une fréquence fixée par la valeur de \(\varepsilon\), ou par le coefficient de la prime d'entropie, la trajectoire ne cesse de basculer d'une politique aléatoire à la politique courante, puis de revenir. Ce que l'agent exécute n'est donc jamais une politique : c'est une alternance de deux politiques, tirée au sort pas par pas.

{{% comment %}}SOURCE: LAPAN ch.18 p.550 (image){{% /comment %}}

Et voici la conséquence, qui est le cœur de la semaine. Cette alternance produit une **mauvaise couverture de l'espace d'états** (*state space coverage*) dès qu'il faut **plusieurs pas** pour atteindre une région isolée. Non pas parce que le hasard est mauvais, mais parce qu'une région isolée ne s'atteint que par une **séquence d'actions coordonnées**, et qu'une politique qui se retire au sort à chaque pas ne peut pas mener une séquence à son terme.

{{% comment %}}SOURCE: LAPAN ch.18 p.550 (image){{% /comment %}}

L'image que je vous propose pour fixer cela est celle d'un nageur qui veut traverser une rivière. Traverser demande vingt brasses dans la même direction. Notre nageur décide de sa direction **à chaque brasse**, et une fois sur cinq il la tire au sort. Il ne traversera pas, et son échec n'a rien à voir avec sa force : il est entièrement contenu dans le fait qu'il reprend sa décision vingt fois au lieu de la prendre une fois. Nous allons mesurer exactement cela dans la section suivante, et la rivière n'est pas une métaphore.

> [!TIP]
 **Le mot que je veux que vous reteniez de cette section, et il organise tout ce qui suit.** En agissant au hasard, l'agent **ne cherche pas** à explorer son environnement : il espère simplement que des actions aléatoires lui apporteront quelque chose de nouveau. C'est ce que j'appelle une exploration **non dirigée**. Toutes les méthodes de la section 11.3 ont en commun de remplacer cet espoir par une **pression**, c'est-à-dire par une quantité calculée qui pousse l'agent vers ce qu'il n'a pas vu. Le défaut de l'\(\varepsilon\)-glouton n'est donc pas le hasard, c'est l'**incohérence** : il n'a aucun moyen de porter une intention sur plus d'un pas.

{{% comment %}}SOURCE: LAPAN ch.18 p.553{{% /comment %}}

---
