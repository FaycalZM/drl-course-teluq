---
title: "12.5 L'auto-jeu, et la perte qui ne mesure rien"
weight: 6
---

## Le meilleur réseau des deux côtés, et un apprenti qui attend son tour

**L'intuition.** Nous avons une recherche qui choisit de bons coups à condition d'avoir un réseau, et un réseau qui ne peut s'entraîner que sur des parties. Il n'y a pas de parties de maîtres, pas de base de données, rien. La seule issue est que le système se nourrisse lui-même.

C'est l'**auto-jeu**, et son dispositif tient en trois objets. Un **meilleur réseau**, qui joue les deux camps de chaque partie et produit les données. Un **apprenti**, qui est un second réseau entraîné sur ces données et qui ne joue rien. Et une **porte d'évaluation**, qui fait affronter l'apprenti et le meilleur réseau de temps en temps ; si l'apprenti gagne suffisamment, il devient le meilleur réseau, et le cycle reprend avec une politique de collecte améliorée.

Notez ce que ce dispositif implique du point de vue de la semaine 1 : pendant qu'un seul réseau joue les deux camps, l'adversaire est **parfaitement prévisible**, il n'apprend pas, et nous sommes donc dans un problème à **un seul agent** au sens strict. L'auto-jeu n'est pas de l'apprentissage multi-agent. C'est le cas que l'introduction a décrit comme absorbable dans l'environnement, et c'est pour cela qu'il tient entièrement dans le cadre des onze semaines précédentes.

---

## Des comptages de visites à une politique, et deux valeurs de température

**L'intuition.** La recherche nous laisse, à la racine, les comptages \(N(s_0,a)\). Il faut en faire deux choses différentes. Pendant l'auto-jeu, nous voulons de la **variété** dans les données, donc du hasard dans le choix du coup, au moins au début de la partie. Pendant une évaluation, nous voulons le **meilleur jeu possible**, donc aucun hasard. Un seul paramètre suffit à passer d'un régime à l'autre.

**L'équation.** La politique issue de la recherche est obtenue en élevant les comptages à une puissance et en normalisant :

$$
\pi(a \mid s) \;=\; \frac{N(s,a)^{1/\tau}}{\sum_k N(s,k)^{1/\tau}}
$$

{{% comment %}}SOURCE: LAPAN ch.20 p.616 (image){{% /comment %}}

Avec \(\tau = 1\), c'est une simple normalisation des comptages : on joue chaque coup proportionnellement au nombre de fois que la recherche l'a préféré. Avec \(\tau\) grand, la distribution s'aplatit vers l'uniforme. Et avec \(\tau \to 0\), elle se concentre entièrement sur le comptage maximal, donc sur le coup déterministe. Ce cours n'emploie que deux valeurs : \(\tau = 1\) pour les premiers coups d'une partie d'auto-jeu, et \(\tau = 0\) pour tout le reste, c'est-à-dire la suite de la partie et la totalité des parties d'évaluation.

{{% comment %}}SOURCE: LAPAN ch.20 p.607{{% /comment %}}

**Le code.** Et attention au cas \(\tau = 0\), qui n'est pas un cas limite calculable mais une branche séparée : \(1/\tau\) n'existe pas, donc on l'écrit comme le choix du maximum.

```python
import numpy as np


def politique_depuis_comptages(comptages, tau: float):
    """Transforme les comptages de visites de la racine en politique.

    tau = 1 : proportionnel aux comptages (ouvertures d'auto-jeu).
    tau = 0 : deterministe sur le comptage maximal (le reste du temps).
    """
    comptages = np.asarray(comptages, dtype=np.float64)

    if tau == 0.0:
        # Branche separee : 1/tau n'existe pas. Ce n'est pas un cas limite,
        # c'est un autre calcul.
        politique = np.zeros_like(comptages)
        politique[int(np.argmax(comptages))] = 1.0
        return politique

    puissances = comptages ** (1.0 / tau)
    return puissances / puissances.sum()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(N(s,a)\) | comptages de visites à la racine, après la recherche | `comptages` |
| \(\tau\) | température ; **ni le \(\tau\) de la semaine 9, ni un pas d'apprentissage** | `tau` |
| \(N(s,a)^{1/\tau}\) | comptages tempérés | `puissances` |
| \(\pi(a \mid s)\) | politique issue de la recherche | la valeur rendue |
| \(\tau = 0\) | branche déterministe, \(\argmax_a N(s,a)\) | le `if tau == 0.0` |

---

## Les triplets d'entraînement, et la perspective du joueur du pas \(t\)

Nous pouvons maintenant dire exactement ce qu'une partie d'auto-jeu laisse derrière elle. Pour chaque coup de la partie, un **triplet** :

$$
(s_t, \;\pi_t, \;r_t)
$$

où \(s_t\) est la position, \(\pi_t\) la politique que la recherche a produite dans cette position, et \(r_t\) le résultat de la partie **vu par le joueur qui devait jouer au pas \(t\)**.

{{% comment %}}SOURCE: LAPAN ch.20 p.607{{% /comment %}}

Ce dernier point est le même piège de signe que la remontée, à une autre échelle, et il se résout de la même façon : on parcourt l'historique **à l'envers** en retournant le résultat à chaque pas. Le joueur du dernier coup voit le résultat tel quel ; celui du coup précédent voit son opposé ; et ainsi jusqu'à l'ouverture.

```python
def triplets_d_une_partie(historique, resultat_final):
    """historique : [(etat, politique_mcts), ...] dans l'ordre des coups joues.
    resultat_final : +1 si le joueur du DERNIER coup a gagne, 0 si match nul.

    Rend [(s_t, pi_t, r_t), ...], chaque r_t vu par le joueur du pas t.
    """
    triplets = []
    r = resultat_final
    for etat, politique in reversed(historique):
        triplets.append((etat, politique, r))
        r = -r              # un coup en arriere, donc l'autre joueur
    triplets.reverse()
    return triplets
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s_t\) | position au pas \(t\), encodée | `etat` |
| \(\pi_t\) | politique issue de la recherche à ce pas | `politique` |
| \(r_t\) | résultat vu par le joueur du pas \(t\) | `r` |
| \(r_t \leftarrow -r_{t+1}\) | changement de camp d'un pas au précédent | `r = -r` |

La perte d'entraînement découle directement de ces triplets, et elle a **deux termes**, un par tête : une **erreur quadratique** entre la sortie de la tête de valeur et le résultat réel \(r_t\), et une **entropie croisée** entre la distribution rendue par la tête de politique et la politique \(\pi_t\) issue de la recherche. Le réseau apprend donc deux choses à la fois : à prédire qui va gagner, et à imiter ce que la recherche a trouvé. Ce second point mérite d'être savouré : le réseau apprend à produire d'emblée, en un seul passage avant, la distribution qu'il avait fallu mille recherches pour obtenir.

{{% comment %}}SOURCE: LAPAN ch.20 p.607{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.619{{% /comment %}}

---

## La porte : cent parties, soixante pour cent

L'apprenti ne devient jamais le meilleur réseau par ancienneté. Il doit passer une **porte**, et ses deux nombres sont simples : **cent parties** contre le meilleur réseau actuel, et **plus de soixante pour cent** de victoires. Au-dessous, il continue de s'entraîner et le meilleur réseau continue de produire les données. Au-dessus, ses poids sont recopiés dans le meilleur réseau, un point de contrôle est enregistré, et la collecte reprend avec le nouveau joueur.

{{% comment %}}SOURCE: LAPAN ch.20 p.619{{% /comment %}}

La **Figure 12-3** montre cette boucle en entier, et la flèche qu'il faut regarder est celle qui part de la promotion et revient sur la distribution des données : c'est elle qui explique toute la sous-section suivante.

{{< bookfig src="12-03.png" week="12" >}}

Pourquoi soixante pour cent et pas cinquante et un ? Parce qu'à cinquante et un pour cent sur cent parties, vous ne savez rien : l'écart est dans le bruit, et vous promouvriez un réseau équivalent la moitié du temps. Soixante pour cent sur cent parties est une marge assez large pour que la promotion signifie quelque chose, et assez basse pour que le système progresse à un rythme raisonnable. C'est un **seuil de décision statistique**, et il a la même nature que le critère d'arrêt déclaré d'avance que le jalon 2 exige de vous.

---

## La perte ne mesure rien, et je ne vais pas l'adoucir

Nous arrivons à la chose la plus importante de cette section, et peut-être de la semaine. Je la dis d'abord en une phrase, puis je la justifie, puis je vous donne les mesures.

**En auto-jeu, la courbe de perte ne contient aucune information sur le progrès de l'agent, et son absence de tendance est le comportement attendu plutôt qu'une panne.**

Voici pourquoi. Depuis la semaine 2, vous regardez descendre des pertes, et cela a un sens parce que la cible est **fixe** : les étiquettes ne changent pas, la fonction à approcher ne bouge pas, et une perte qui descend signifie que vous vous en approchez. En auto-jeu, la cible est fabriquée par le meilleur réseau. Chaque fois que l'apprenti franchit la porte, **le producteur des données change**, donc la distribution des positions change, donc les politiques \(\pi_t\) à imiter changent, donc les résultats \(r_t\) à prédire changent. Vous n'êtes pas en train de descendre une fonction : vous êtes en train de poursuivre une cible qui se déplace chaque fois que vous progressez, et qui se déplace **parce que** vous progressez.

Le taux de victoire a le même problème, et pour la même raison. Vous mesurez l'apprenti contre le **meilleur réseau actuel**, c'est-à-dire contre une version de lui-même d'il y a quelques centaines de parties. Quand il devient meilleur, il est promu, et l'adversaire redevient aussi fort que lui. Le taux de victoire contre le meilleur réseau est donc structurellement **ramené autour d'un demi**, indéfiniment, et il le restera même si le niveau absolu du jeu monte sans arrêt.

Les mesures confirment exactement cela. Deux entraînements complets, avec deux pas d'apprentissage séparés par deux ordres de grandeur, \(0{,}1\) et \(0{,}001\), chacun poursuivi **dix heures** et quarante mille parties, soit une vingtaine d'heures pour les deux. Résultat : le taux de victoire contre le meilleur réseau oscille autour de \(0{,}5\), avec des pointes à \(0{,}8\) ou \(0{,}9\), et la perte totale ne montre **aucune tendance nette** sur toute la durée.

{{% comment %}}SOURCE: LAPAN ch.20 p.619-620{{% /comment %}}

> [!IMPORTANT]
 **Généralisez cette observation, parce qu'elle vaut bien au-delà des jeux de plateau : quand l'adversaire est une copie de vous-même, il n'y a aucun objectif fixe à descendre.** Toute la pratique que vous avez accumulée depuis onze semaines, lire une perte, repérer un plateau, soupçonner un pas d'apprentissage trop grand, suppose une cible immobile. Dès que la cible est produite par le système lui-même, cette pratique devient non seulement inutile mais **trompeuse** : vous pouvez passer une soirée à régler les hyperparamètres d'une courbe plate qui serait restée plate avec les meilleurs réglages du monde. C'est la première fois dans ce cours que je vous demande de **ne pas** diagnostiquer une perte. Ce ne sera pas la dernière : la section 12.11 vous montrera le même phénomène pour une autre raison, et c'est là que nous lui donnerons son nom.

---

## Ce qu'un tournoi entre points de contrôle mesure, lui

Si la perte et le taux de victoire ne disent rien, comment sait-on que quelque chose s'apprend ? Par la seule mesure qui ait un sens ici : un **tournoi entre points de contrôle**. On prend les réseaux enregistrés à différents moments de l'entraînement, on les fait s'affronter deux à deux, et l'on regarde si les plus récents battent les plus anciens.

La réponse est oui, et elle est nette : la qualité de jeu monte avec l'indice du point de contrôle. Le pas d'apprentissage le plus faible donne une progression plus **régulière**, et quand on met en tournoi les dix meilleurs réseaux de chacun des deux entraînements, **neuf des dix premiers** appartiennent à l'entraînement au pas \(0{,}001\). Le progrès existe donc, il est mesurable, et il n'était simplement pas dans la courbe que nous avions l'habitude de regarder.

{{% comment %}}SOURCE: LAPAN ch.20 p.621-622{{% /comment %}}

> [!TIP]
 **Ce que vous obtiendrez dans le laboratoire, chiffré, pour que vous ne visiez ni trop haut ni trop bas.** Avec **dix** recherches par coup au lieu de mille, en traitant huit feuilles par passage de réseau, et après environ **une heure** d'entraînement et **2 500** parties d'auto-jeu, vous obtiendrez un adversaire avec lequel il est agréable de jouer. Soyons précis sur le niveau : il est **en dessous de celui d'un enfant**, il manifeste une stratégie rudimentaire, et il fait une erreur grossière un coup sur deux. C'est exactement ce qu'il faut pour que la méthode soit visible, et je préfère vous donner ce niveau franchement plutôt que de vous laisser croire que vous allez battre un adulte attentif.

{{% comment %}}SOURCE: LAPAN ch.20 p.619{{% /comment %}}

---
