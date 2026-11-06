---
title: "11.2 River Swim : trois nombres qui suffisent"
weight: 3
---

## Une rivière à six états, et un courant qui défait tout

Je vous donne maintenant la mesure la plus petite et la plus convaincante de cette semaine. L'environnement s'appelle **River Swim**, il modélise une rivière que l'agent doit traverser, et il tient en six états.

Les voici, en ligne. Les états **1** et **6** sont les deux rives, où l'agent a pied ; les états **2**, **3**, **4** et **5** sont dans l'eau. Deux actions existent, *nager vers la droite*, c'est-à-dire vers la rive opposée et **contre** le courant, et *nager vers la gauche*, c'est-à-dire **avec** le courant.

Les transitions, maintenant, et c'est là que tout est décidé.

Depuis l'**état 1**, une seule action est disponible, *droite* : avec probabilité \(0{,}6\) l'agent part dans l'état 2, et avec probabilité \(0{,}4\) il reste sur la rive.

Depuis chacun des **états 2 à 5**, les deux actions sont disponibles, et leurs transitions sont identiques dans les quatre états. L'action *droite*, contre le courant, avance d'un état avec probabilité \(0{,}35\), laisse l'agent sur place avec probabilité \(0{,}60\), et le fait **reculer** d'un état avec probabilité \(0{,}05\) ; les trois sommes font bien \(1{,}00\). L'action *gauche*, avec le courant, recule d'un état avec probabilité \(1\) : elle réussit **toujours**, puisque le courant ramène l'agent vers la rive de départ.

Depuis l'**état 6**, enfin, une seule action est disponible, *gauche*, qui ramène l'agent dans l'état 5 avec probabilité \(1\) : la rive opposée se comporte comme la rive de départ, on ne peut qu'en repartir.

{{% comment %}}SOURCE: LAPAN ch.18 p.550-551 (images){{% /comment %}}

Reste la récompense, et elle est volontairement brutale. Entrer dans l'**état 6** rapporte **1 000**. Les déplacements entre les états 1 et 5 rapportent une petite récompense de **1**. Je mentionne cette petite récompense pour être complet, et je ne m'y arrête pas : tout l'intérêt de l'exemple est dans le 1 000 de la rive opposée, qui compense d'un seul coup tous les efforts fournis à nager contre le courant.

{{% comment %}}SOURCE: LAPAN ch.18 p.551 (image){{% /comment %}}

La **Figure 11-1** donne la structure complète, et elle porte déjà, en dessous, les trois mesures de la sous-section suivante. Regardez d'abord la chaîne et ses deux familles de flèches, puis laissez les trois histogrammes de côté : nous y reviendrons dans deux paragraphes, et ils ne veulent rien dire sans la chaîne.

{{< bookfig src="11-01.png" week="11" >}}

Un dernier élément du dispositif, qui compte pour la lecture des mesures : un **épisode dure dix pas**. Passé ce délai, l'agent est remis à l'état 1, où qu'il se trouve. Dix pas, c'est très peu, et c'est exactement le point : il faut au minimum cinq avancées pour aller de 1 à 6, et chaque avancée ne réussit qu'une fois sur trois environ.

{{% comment %}}SOURCE: LAPAN ch.18 p.551, p.553 (image p.551){{% /comment %}}

---

## Trois mesures, et la troisième est celle qu'il faut retenir

Lâchons maintenant dans cette rivière un agent **purement aléatoire**, c'est-à-dire un agent à \(\varepsilon = 1\), qui tire son action uniformément parmi celles qui sont disponibles. Comptons combien de fois il visite chaque état. Trois exécutions, de longueur croissante.

| Durée de l'exécution | État 1 | État 2 | État 3 | État 4 | État 5 | **État 6** |
| --- | --- | --- | --- | --- | --- | --- |
| **100 pas** (10 épisodes) | 40 | 39 | 17 | 3 | 1 | **0** |
| **1 000 pas** (100 épisodes) | 441 | 452 | 93 | 12 | 2 | **0** |
| **10 000 pas** (1 000 épisodes) | 4 056 | 4 506 | 1 095 | 281 | 57 | **5** |

{{% comment %}}SOURCE: LAPAN ch.18 p.552 (image){{% /comment %}}

Lisez la dernière colonne de haut en bas, et prenez le temps de la lire pour ce qu'elle est. En cent pas, la rive opposée n'est **jamais** atteinte. En mille pas, elle n'est **jamais** atteinte. En dix mille pas, elle est atteinte **cinq fois**, ce qui représente \(0{,}05~\%\) des pas effectués.

Regardez aussi la cinquième colonne, qui dit la même chose autrement : l'état 5, celui qui touche la rive opposée, est visité **une** fois en cent pas et **deux** fois en mille pas. Ce n'est pas que l'agent s'approche du but et échoue de peu : il ne s'en approche pas du tout. La masse de ses visites reste collée aux états 1 et 2, c'est-à-dire aux deux premiers pas de la rivière.

> [!WARNING]
 **Les trois durées sont des PAS, pas des épisodes, et je veux que vous sachiez comment le vérifier vous-même.** C'est le genre de confusion qui fait qu'une mesure se raconte dix fois plus favorable qu'elle n'est, et le contrôle tient en une addition : additionnez chaque ligne du tableau. La première donne exactement 100, la deuxième exactement 1 000, la troisième exactement 10 000. Un comptage de visites par état somme au nombre de **pas** effectués, jamais au nombre d'épisodes. Et la confirmation arrive par un second chemin : cinq visites annoncées comme \(0{,}05~\%\) du total, c'est \(5/10\,000\), donc dix mille pas. À dix pas par épisode, ces trois exécutions sont donc de **10, 100 et 1 000 épisodes**, et non de 100, 1 000 et 10 000. Si vous lisez un jour ce tableau avec « épisodes » en tête de colonne, vous attribuerez à l'agent dix fois plus d'expérience qu'il n'en a eu, sur l'unique mesure qui porte l'argument de la semaine.

{{% comment %}}SOURCE: LAPAN ch.18 p.552 (image){{% /comment %}}

---

## Pourquoi six états suffisent à mettre en échec un marcheur aléatoire

Il vaut la peine de comprendre **pourquoi** l'échec est aussi net, parce que la raison est structurelle et qu'elle se retrouvera partout dans la semaine.

Pour progresser d'un état, l'agent doit faire deux choses coup sur coup : **choisir** *droite*, ce qu'un agent aléatoire fait une fois sur deux, et **réussir**, ce qui arrive avec probabilité \(0{,}35\). Pour reculer d'un état, il suffit qu'il choisisse *gauche*, ce qu'il fait aussi une fois sur deux, et ce choix, lui, **n'échoue jamais**.

Toute l'asymétrie est là, et je la formule comme une règle à retenir : dans cet environnement, le progrès est **improbable et incertain**, alors que la régression est **tout aussi probable et parfaitement fiable**. Le courant ne punit pas lentement une mauvaise décision, il l'exécute immédiatement et sans faute. Cinq avancées consécutives sont donc nécessaires, et une seule brasse vers la gauche annule la précédente avec certitude.

Je ne vais pas vous donner la probabilité exacte d'atteindre l'état 6 en dix pas, parce que ce cours ne l'établit pas et que les trois lignes du tableau sont une mesure, ce qui vaut mieux qu'une estimation. Ce que je vous demande de retenir est le mécanisme : **ce n'est pas la longueur du chemin qui bloque l'agent aléatoire, c'est le fait que son seul moyen d'avancer est de répéter la même décision alors qu'il la retire au sort à chaque pas.** Vous reconnaissez le nageur de la section 11.1, et vous reconnaîtrez la voiture de la section 11.5.

Et maintenant l'extrapolation, qui est la raison pour laquelle cet exemple minuscule mérite une section entière. Il n'y a ici que **six** états. Imaginez la même rivière avec vingt états, ou cinquante. Puis sortez de la rivière et pensez à un jeu vidéo : il peut y avoir **des centaines de décisions à prendre** avant que quelque chose d'intéressant se produise. Si une exploration non dirigée échoue sur six états, la question n'est plus de savoir si elle échouera sur un jeu, mais de combien d'ordres de grandeur.

{{% comment %}}SOURCE: LAPAN ch.18 p.552 (image){{% /comment %}}

Voici enfin, parce que ce cours donne toujours le code à côté de l'idée, la façon dont ces trois lignes se produisent. Le fragment ne montre que ce qui compte : la table des transitions, telle que la Figure 11-1 la décrit, et un compteur de visites.

```python
import random
from collections import Counter

# Pour chaque etat, pour chaque action, la liste (probabilite, etat_suivant).
# C'est la Figure 11-1, ecrite comme une table. Les rives n'ont qu'une action.
TRANSITIONS = {
    1: {"droite": [(0.6, 2), (0.4, 1)]},
    6: {"gauche": [(1.0, 5)]},
}
for i in (2, 3, 4, 5):
    TRANSITIONS[i] = {
        "droite": [(0.35, i + 1), (0.60, i), (0.05, i - 1)],
        "gauche": [(1.00, i - 1)],
    }


def tirer(etat: int, action: str) -> int:
    """Un tirage dans la ligne (etat, action) de la table."""
    seuils, etats = zip(*TRANSITIONS[etat][action])
    return random.choices(etats, weights=seuils, k=1)[0]


def compter_visites(n_pas: int, pas_par_episode: int = 10) -> Counter:
    """Agent PUREMENT aleatoire : epsilon = 1, aucune valeur, aucun apprentissage."""
    visites, etat = Counter(), 1
    for pas in range(n_pas):
        visites[etat] += 1
        action = random.choice(list(TRANSITIONS[etat]))   # uniforme
        etat = tirer(etat, action)
        if (pas + 1) % pas_par_episode == 0:
            etat = 1                                      # fin d'episode
    return visites
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| les six états | états 1 à 6, les deux rives et l'eau | clés de `TRANSITIONS` |
| \(p = 0{,}35 / 0{,}60 / 0{,}05\) | avancer, rester, reculer en nageant à droite | `TRANSITIONS[i]["droite"]` |
| \(p = 1\) | reculer en nageant à gauche, qui réussit toujours | `TRANSITIONS[i]["gauche"]` |
| \(\varepsilon = 1\) | agent purement aléatoire | `random.choice(...)`, uniforme |
| dix pas par épisode | remise à l'état 1 tous les dix pas | `pas_par_episode` |
| \(\tilde N(s)\) | nombre de visites de l'état \(s\) | `visites[etat]`, un `Counter` |

Notez que ce compteur est **exactement** l'objet que la section 11.3 va transformer en méthode d'exploration. Ici il sert à mesurer un échec ; là il servira à le réparer. C'est la même ligne de code.

---
