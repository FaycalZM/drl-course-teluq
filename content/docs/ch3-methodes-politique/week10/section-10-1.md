---
title: "10.1 Le banc d'essai, et ce qu'il interdit de comparer"
weight: 2
---

## Deux corps simulés, et tous les chiffres de la semaine mesurés sur eux

Avant les méthodes, le banc d'essai. Je commence par là pour une raison qui n'est pas de confort : les quatre méthodes de cette semaine sont comparées, à la fin, dans un seul tableau, et ce tableau ne veut rien dire si l'on ne sait pas sur quoi il a été mesuré.

Deux problèmes de locomotion, donc deux corps simulés. Le premier est un **guépard à deux pattes**, qui doit courir dans un plan vertical. Le second est une **fourmi à quatre pattes**, en trois dimensions, qui doit avancer sans tomber. Dans les deux cas, l'observation est un vecteur de caractéristiques articulaires, positions, vitesses et angles ; l'action est un vecteur de commandes, une par articulation ; et la récompense paie la distance parcourue en facturant l'énergie dépensée. C'est exactement la forme du robot quadrupède de la semaine 9, avec des corps différents, et c'est le banc d'essai standard de ce domaine. La **Figure 10-3** montre les deux corps.

{{< bookfig src="10-03.png" week="10" >}}

{{% comment %}}SOURCE: LAPAN ch.16 p.493{{% /comment %}}

Un détail d'outillage, qui a une conséquence immédiate pour vous. Ces deux corps existent dans **deux moteurs physiques différents**, et les deux sont installables aujourd'hui. Le premier est PyBullet, dont la dernière version date de 2022 et qui demande un peu de travail pour cohabiter avec l'interface actuelle : c'est le chemin que la semaine 9 a déjà refusé pour le laboratoire, et pour la même raison. Le second est MuJoCo, qui s'installe comme une extension de Gymnasium par `gymnasium[mujoco]` et qui livre `HalfCheetah-v4` et `Ant-v4` sans aucune plomberie. C'est le chemin maintenu, et c'est celui à prendre si vous voulez reproduire quoi que ce soit de cette section.

{{% comment %}}SOURCE: LAPAN ch.16 p.493-494{{% /comment %}}

> [!NOTE]
 **Pourquoi je vous raconte un banc d'essai que le laboratoire n'utilisera pas.** Les chiffres de cette section et du tableau de la section 10.6 sont là pour une seule chose : vous donner des **ordres de grandeur réels**, parce que c'est le genre de chiffre que l'on n'a jamais quand on en a besoin. Vous verrez dans un instant qu'une seule exécution sur ce banc d'essai coûte entre huit et vingt heures de calcul. C'est un repère, et c'est tout ce que c'est. Le laboratoire et le jalon 3 mesureront sur `Pendulum-v1`, où un entraînement tient en quelques minutes, et je le dirai à nouveau au moment de fixer le budget de calcul.

---

## Trois écarts avec l'A2C de la semaine 8, et ils comptent pour votre code

L'acteur-critique employé sur ce banc d'essai est celui de la semaine 8 avec une tête gaussienne, c'est-à-dire exactement la méthode de la section 9.2. Mais trois choix d'implémentation diffèrent, et je veux que vous les voyiez comme trois décisions et non comme trois détails, parce que vous reprendrez les trois dans le laboratoire.

**Premier écart : seize environnements en parallèle.** L'expérience est collectée par seize copies de l'environnement interrogées ensemble, au lieu d'une seule. C'est la réponse au problème 4 de la semaine 8, appliquée sérieusement : seize corps simulés dans seize états différents fournissent un lot dont les transitions sont beaucoup moins corrélées entre elles.

**Deuxième écart : l'acteur et le critique sont deux réseaux séparés, sans aucun poids commun.** La semaine 8 présentait les deux câblages possibles, tronc commun ou réseaux séparés, et expliquait que le tronc commun économise du calcul. Ici le choix est l'autre, et il a une conséquence directe : il faut **deux optimiseurs**, avec deux pas d'apprentissage distincts, et vous verrez en section 10.2 qu'ils diffèrent d'un facteur dix.

**Troisième écart, et c'est le plus instructif : la variance de la politique ne dépend pas de l'observation.** En semaine 9, le réseau produisait deux vecteurs, une moyenne et une variance, tous deux fonctions de l'état. Ici, la moyenne reste une fonction de l'état, mais l'écart-type est un **unique paramètre du modèle**, un vecteur appris de la taille de l'espace d'actions, identique dans tous les états. On le stocke comme le logarithme de l'écart-type, ce qui garantit la positivité sans aucune activation, et on l'appelle traditionnellement `logstd`.

{{% comment %}}SOURCE: LAPAN ch.16 p.494{{% /comment %}}

```python
import torch
import torch.nn as nn

TAILLE_CACHEE = 64


class ActeurGaussien(nn.Module):
    """Moyenne fonction de l'etat, ecart-type GLOBAL et appris."""

    def __init__(self, taille_obs: int, n_actions: int):
        super().__init__()
        self.mu = nn.Sequential(
            nn.Linear(taille_obs, TAILLE_CACHEE), nn.Tanh(),
            nn.Linear(TAILLE_CACHEE, TAILLE_CACHEE), nn.Tanh(),
            nn.Linear(TAILLE_CACHEE, n_actions), nn.Tanh(),
        )
        # UN parametre pour tout l'espace d'etats. Pas de couche, pas d'entree :
        # c'est le logarithme de l'ecart-type, donc exp() le rend positif.
        self.logstd = nn.Parameter(torch.zeros(n_actions))

    def forward(self, obs):
        return self.mu(obs)


class CritiqueEtat(nn.Module):
    """Etat -> UN scalaire. Aucun poids partage avec l'acteur."""

    def __init__(self, taille_obs: int):
        super().__init__()
        self.pile = nn.Sequential(
            nn.Linear(taille_obs, TAILLE_CACHEE), nn.ReLU(),
            nn.Linear(TAILLE_CACHEE, TAILLE_CACHEE), nn.ReLU(),
            nn.Linear(TAILLE_CACHEE, 1),
        )

    def forward(self, obs):
        return self.pile(obs)
```

{{% comment %}}SOURCE: LAPAN ch.16 p.495{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | moyenne de la politique gaussienne, bornée à \([-1,1]\) | `acteur(obs)` |
| \(\sigma\) | écart-type de la politique, **le même dans tous les états** | `torch.exp(acteur.logstd)` |
| \(\ln\sigma\) | ce que le réseau stocke réellement | `acteur.logstd` |
| \(v_{\mathbf{w}}(s)\) | valeur d'état estimée par le critique | `critique(obs)` |
| \(\theta\), \(\mathbf{w}\) | paramètres de l'acteur et poids du critique, **disjoints** | deux appels à `parameters()` |

Deux remarques d'architecture avant de passer à l'action. La tangente hyperbolique est l'activation de l'acteur, y compris en sortie, ce qui borne la moyenne à \([-1,1]\) : les commandes de ces environnements y sont normalisées. Le critique, lui, emploie des unités rectifiées et aucune activation de sortie, parce qu'une valeur d'état n'est bornée ni en haut ni en bas. Vous reconnaissez les deux règles de la semaine 9.

Agir se fait alors en deux lignes, et l'écrêtage de l'action de la semaine 9 est toujours là :

```python
import numpy as np


def agir(acteur, obs_t):
    """Tirage gaussien autour de la moyenne, puis ecretage de l'action."""
    with torch.no_grad():
        mu = acteur(obs_t).cpu().numpy()
    sigma = torch.exp(acteur.logstd).detach().cpu().numpy()
    actions = mu + sigma * np.random.normal(size=mu.shape)
    # Les bornes de l'environnement sont dures : l'ecretage de l'action reste.
    return np.clip(actions, -1.0, 1.0)
```

{{% comment %}}SOURCE: LAPAN ch.16 p.496{{% /comment %}}

> [!TIP]
 **Ce qu'une variance globale achète, et ce qu'elle interdit.** Elle achète de la stabilité et de la simplicité : un seul vecteur de paramètres à régler au lieu d'une tête entière, et aucune possibilité que le réseau décide d'écraser sa variance dans les états où il se croit sûr de lui, ce qui est le mode d'extinction de l'exploration que la semaine 9 a décrit. Elle interdit, en revanche, toute modulation de l'exploration selon la situation : l'agent ne peut pas être prudent près d'un précipice et audacieux en terrain plat, puisqu'il explore avec la même amplitude partout. Retenez ce compromis, parce qu'il reviendra comme un verdict en section 10.5 : la méthode qui ferme cette semaine rend l'écart-type **fonction de l'état**, et ce n'est pas un raffinement, c'est la condition de possibilité de son idée centrale.

---

## Deux pièges de banc d'essai, et une règle de lecture qui vaut pour le jalon 3

Voici maintenant deux faits que je veux transmettre sans les adoucir, parce que le jalon 3 est le premier moment du cours où vous comparerez vos propres courbes à des chiffres venus d'ailleurs.

**Premier piège : une condition de terminaison peut enfermer un entraînement dans un minimum local.** Dans la version MuJoCo de la fourmi, l'épisode est interrompu dès que le corps s'incline au-delà d'un certain angle : c'est un contrôle de santé, pensé pour éviter de simuler un corps qui a déjà chuté. L'effet sur l'apprentissage est brutal. En début d'entraînement, l'agent n'a aucune chance de découvrir comment tenir la fourmi sur ses pattes ; chaque épisode se termine donc presque immédiatement, l'agent n'observe jamais rien d'autre que des débuts d'épisode, et l'entraînement reste bloqué indéfiniment dans un minimum local sans aucun progrès. La parade employée sur ce banc d'essai est de **désactiver ce contrôle**, ce qui laisse l'épisode se dérouler jusqu'au bout même lorsque le corps est tombé.

{{% comment %}}SOURCE: LAPAN ch.16 p.498{{% /comment %}}

**Deuxième piège : le même corps, dans deux simulateurs, n'est pas le même problème.** La version PyBullet du guépard fournit à l'agent **26 nombres** d'observation ; la version MuJoCo en fournit **17**. Ce ne sont donc pas deux implémentations du même modèle, ce sont deux modèles différents, avec des dynamiques différentes et des échelles de récompense différentes. Deux courbes tracées dans les mêmes axes, avec le même nom d'environnement en légende, peuvent donc ne pas être comparables du tout.

{{% comment %}}SOURCE: LAPAN ch.16 p.494{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.498{{% /comment %}}

> [!WARNING]
 **La règle de lecture, et je la veux dans vos rapports à partir de cette semaine : un chiffre de banc d'essai sans sa version d'environnement n'est pas une mesure.** « 4 500 sur HalfCheetah » ne veut rien dire. « 4 500 sur `HalfCheetah-v4` sous MuJoCo, avec 17 observations, sur 90 millions de pas » est une mesure. Les deux pièges ci-dessus se combinent de la pire façon possible : ils produisent des courbes qui **ont l'air** comparables, avec les mêmes noms et les mêmes axes, et dont la comparaison est pourtant vide. Vous rencontrerez cette situation en dehors de ce cours, et le réflexe à acquérir est de chercher le numéro de version, le simulateur et la dimension de l'observation avant de regarder la hauteur des courbes.

---

## La mesure de référence, et le prix d'une mesure sur ce banc d'essai

Reste à donner les chiffres, qui serviront de ligne de base à tout le reste de la semaine.

Commençons par le prix, parce qu'il est la moitié du sujet de cette semaine. Sur le guépard, la collecte tourne à environ **1 600 transitions par seconde** sous PyBullet et **5 100 sous MuJoCo**, soit un facteur trois en faveur du second. Sur la fourmi, 1 400 contre 2 500. Une exécution de **100 millions de pas demande une vingtaine d'heures**. Sous MuJoCo, un score de 4 500 a été atteint en 90 millions de pas, soit environ cinq heures. Et pour calibrer votre jugement sur ces nombres : les travaux de recherche situent le maximum atteignable sur le guépard **autour de 4 000 à 5 000**.

{{% comment %}}SOURCE: LAPAN ch.16 p.497-498{{% /comment %}}

Les scores de la méthode de référence, c'est-à-dire l'acteur-critique à avantage de la semaine 8 avec les trois écarts ci-dessus, sont donc les suivants : **2 189** sur le guépard sous PyBullet, **4 718** sur le guépard sous MuJoCo, **2 425** sur la fourmi sous PyBullet et **5 380** sur la fourmi sous MuJoCo. Ce dernier chiffre est le meilleur résultat obtenu sur la fourmi par l'ensemble des méthodes que cette semaine compare, et il a été obtenu d'une façon qui mérite d'être connue : la courbe est restée pratiquement plate pendant les **cent premiers millions de pas**, puis a décollé.

{{% comment %}}SOURCE: LAPAN ch.16 p.499{{% /comment %}}

> [!IMPORTANT]
 **Ce dernier détail n'est pas une anecdote, c'est une leçon de patience mesurée.** Une courbe plate pendant cent millions de pas, c'est vingt heures de calcul pendant lesquelles tous les diagnostics disent que rien ne se passe. Un praticien raisonnable aurait arrêté l'exécution au bout de deux heures et conclu que la méthode ne fonctionne pas sur cette tâche. Il aurait eu tort, et il n'aurait eu aucun moyen de le savoir. Je ne vous demande pas d'en tirer la conclusion inverse, qui serait de laisser tourner tout entraînement indéfiniment : je vous demande d'en tirer qu'un **critère d'arrêt** est une décision à prendre à l'avance, à écrire dans votre rapport, et à assumer comme un choix, parce qu'il détermine une partie de vos résultats. C'est la leçon de la semaine 7, et la voici dans sa version la plus coûteuse.

---
