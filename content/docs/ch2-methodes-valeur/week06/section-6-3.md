---
title: "6.3 La source d'expérience, et la transition premier-dernier"
weight: 4
---

## Une seule itération, sept gestes cachés

La **source d'expérience** (*experience source*) est l'abstraction centrale de la bibliothèque, et c'est celle qui mérite le plus d'attention, pour une raison simple : c'est la seule qui cache des choses que vous ne sauriez probablement pas qu'il faut écrire.

Ce qu'elle cache, en vrac : jouer dans **plusieurs environnements à la fois**, prétraiter les trajectoires avant de les livrer, et, dans ses versions récentes, s'appuyer sur les environnements vectorisés de Gymnasium, qui sont le sujet de la semaine 7. Vue de l'extérieur, c'est une boîte noire sur laquelle on itère, et qui rend des transitions.

{{% comment %}}SOURCE: LAPAN ch.7 p.211{{% /comment %}}

Il en existe trois variantes, et deux nous intéressent. La première rend des sous-trajectoires de \(n\) pas, avec **tous** les pas intermédiaires. La deuxième ne rend que le **premier et le dernier** état, avec l'accumulation correcte des récompenses entre les deux, ce qui économise beaucoup de mémoire dès que \(n\) dépasse 1 ; c'est elle qui va nous occuper. La troisième sert une famille de méthodes de la semaine 8 et nous la laisserons de côté.

{{% comment %}}SOURCE: LAPAN ch.7 p.211{{% /comment %}}

Voici les **sept** gestes que cache une seule itération sur une source d'expérience. Je les écris parce que vous en avez écrit cinq la semaine dernière, que vous en avez probablement oublié un, et que le septième est celui qui donne son nom à la section.

1. Réinitialiser l'environnement, ou les environnements, s'il le faut.
2. Demander à l'agent l'action à jouer pour l'observation courante.
3. Exécuter un pas dans l'environnement.
4. Transmettre à l'agent l'état suivant, et son état interne s'il en a un.
5. Rendre la transition, une fois qu'il y a assez de pas pour en former une.
6. À la fin d'un épisode, **émettre la queue** des transitions incomplètes, puis réinitialiser.
7. Continuer indéfiniment.

{{% comment %}}SOURCE: LAPAN ch.7 p.213{{% /comment %}}

Le geste nº6 est celui que presque tout le monde écrit mal la première fois. À la fin d'un épisode, il reste dans la file des sous-trajectoires qui n'ont pas atteint leur longueur nominale, et il faut les livrer quand même, plus courtes que demandé. Une source d'expérience rend donc des tuples **plus courts** que la longueur demandée en fin d'épisode, et un code qui suppose une longueur fixe plante ou, pire, apprend sur des données tronquées sans rien signaler.

{{% comment %}}SOURCE: LAPAN ch.7 p.214{{% /comment %}}

Deux détails d'interface, avant l'essentiel. Une transition élémentaire porte quatre champs : l'état, l'action, la récompense, et **un seul drapeau** pour la fin d'épisode, qui vaut vrai en cas de terminaison comme en cas de troncature. La semaine 1 avait distingué ces deux cas avec soin, et une bibliothèque qui les fusionne fait un choix : pour le calcul d'une cible, les deux produisent le même masque. Et lorsque plusieurs environnements sont servis par la même source, ils le sont à tour de rôle, ce qui impose qu'ils soient des **instances indépendantes**. Passer deux fois le même objet environnement donne un mélange d'observations dont rien, dans le flot de sortie, ne révèle qu'il est faux.

{{% comment %}}SOURCE: LAPAN ch.7 p.214, p.215{{% /comment %}}

---

## La transition premier-dernier, et pourquoi elle vaut sa propre sous-section

Nous y sommes. Cette sous-section est courte, et c'est celle sur laquelle la section 6.6 repose entièrement.

L'intuition tient dans une observation sur la perte de la semaine 5. Pour écrire une approximation de Bellman à un pas, il faut un quadruplet \((s, a, r, s')\), **d'un seul coup**. Pas une sous-trajectoire à parcourir, pas une liste de récompenses à sommer au moment du calcul de la perte : un quadruplet, prêt à être empilé dans un lot. Et pour le DQN à n étapes, il faut la même chose, avec une seule différence : l'état suivant est l'état après \(n\) pas, et la récompense est le total actualisé accumulé sur ces \(n\) pas.

{{% comment %}}SOURCE: LAPAN ch.7 p.215{{% /comment %}}

D'où la **transition premier-dernier** (*first-last transition*), qui est exactement cet objet. Quatre champs, et le quatrième est celui qui compte :

| Champ | Ce qu'il contient |
| --- | --- |
| état | le **premier** état de la sous-trajectoire |
| action | l'action jouée **dans ce premier état** |
| récompense | la récompense **accumulée** sur les \(n\) pas |
| état final | l'état après \(n\) pas, et **`None` si l'épisode s'est terminé** |

{{% comment %}}SOURCE: LAPAN ch.7 p.216{{% /comment %}}

Lisez la dernière ligne deux fois. Le cas terminal n'est pas signalé par un drapeau à côté de l'état : il est encodé **dans** l'état final, par son absence. C'est le masque terminal de la semaine 5, déplacé dans la structure de données. Et c'est, avec l'accumulation de la récompense, la totalité de ce qu'il faut pour que le passage à \(n\) étapes ne coûte rien.

Le meilleur moyen de s'en convaincre est de regarder la trace. Prenons un environnement jouet, et il est délibérément ennuyeux : l'observation est un compteur qui va de 0 à 4, la récompense est égale à l'action jouée, et l'épisode fait toujours exactement dix pas. L'agent, lui, joue toujours la même action. Tout y est prévisible, ce qui est exactement ce qu'on veut d'un banc d'essai.

{{% comment %}}SOURCE: LAPAN ch.7 p.212{{% /comment %}}

```python
from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class TransitionPremierDernier:
    """Ce que consomme la perte d'un DQN, à un pas comme à n étapes."""
    etat: np.ndarray
    action: int
    recompense: float          # ACCUMULÉE sur les n pas, et actualisée
    etat_final: Optional[np.ndarray]   # None SI l'épisode s'est terminé


def premier_dernier(trajectoire, gamma: float, n: int):
    """Replie n transitions élémentaires en une seule transition."""
    total = 0.0
    for decalage, pas in enumerate(trajectoire[:n]):
        total += (gamma ** decalage) * pas.recompense      # accumulation
    dernier = trajectoire[n - 1]
    return TransitionPremierDernier(
        etat=trajectoire[0].etat,
        action=trajectoire[0].action,
        recompense=total,
        # Le cas terminal est encodé par l'ABSENCE d'état final.
        etat_final=None if dernier.fin_episode else dernier.etat_suivant,
    )
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s_t\) | le premier état de la sous-trajectoire | `etat` |
| \(a_t\) | l'action jouée dans cet état | `action` |
| \(\sum_{k=0}^{n-1}\gamma^k r_{t+k}\) | la récompense accumulée | `recompense` |
| \(s_{t+n}\) | l'état après \(n\) pas | `etat_final` |
| \(\hat q(\text{terminal},\cdot) = 0\) | le cas terminal | `etat_final=None` |
| \(n\) | la profondeur de repliement | `n`, et `steps_count` dans la bibliothèque |

Avec \(n = 2\) et un agent qui joue toujours l'action 1, la trace est d'une régularité instructive : la plupart des transitions portent une récompense de 2, puisque deux pas à 1 ont été accumulés. Et au moment où l'épisode se termine, deux transitions sortent coup sur coup avec `etat_final=None`, la première portant encore 2 et la seconde seulement 1. La queue est **payée**, et elle est payée juste : la dernière transition n'a qu'un pas derrière elle, donc elle n'a qu'une récompense.

{{% comment %}}SOURCE: LAPAN ch.7 p.217{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, et c'est l'énoncé que la section 6.6 va encaisser.** Puisque la récompense est déjà accumulée et que le cas terminal est déjà encodé, le passage d'un DQN à un pas à un DQN à \(n\) étapes ne demande rien d'autre que de dire \(n\) à la source d'expérience et d'actualiser avec \(\gamma^n\) au lieu de \(\gamma\) dans la perte. Deux paramètres. Aucune ligne de logique. Gardez cette phrase : nous allons la vérifier dans quatre sections, et vous verrez que la seconde moitié, le \(\gamma^n\), est le piège le plus coûteux de la semaine.

{{% comment %}}SOURCE: LAPAN ch.7 p.215-217 ; ch.8 p.244{{% /comment %}}

Et puisque ces petits détails sont très faciles à implémenter de travers quand on fait soi-même toute la gestion des trajectoires, le volet A du laboratoire vous demandera de **prédire** cette trace avant de l'exécuter. C'est cinq minutes de travail et c'est, de tout le laboratoire, l'exercice dont le rapport entre ce qu'il apprend et ce qu'il coûte est le meilleur.

{{% comment %}}SOURCE: LAPAN ch.7 p.217{{% /comment %}}

---
