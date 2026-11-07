---
title: "Laboratoire"
weight: 9
---

Le laboratoire de cette semaine est **formatif** : la semaine 4 ne porte aucun jalon, le prochain est en semaine 7. Le tronc commun tient en trois volets, et l'un des trois est l'**exercice évalué** de ce laboratoire, celui dont j'attends un rendu écrit et sur lequel porteront les questions du quiz : c'est le **volet C**, la falaise. Les volets A et B sont l'échauffement, et ils sont courts. Un quatrième volet, le **volet D**, est facultatif et se trouve à la fin.

Budget de calcul, et je le donne tout de suite parce qu'il est inhabituel dans ce cours : **quelques secondes par exécution, sur processeur central**. Tout est tabulaire cette semaine. Si l'un de vos exercices demande un processeur graphique, ce n'est pas votre matériel qui est en cause, c'est l'exercice : relisez l'énoncé.

---

## Volet A : avec modèle, l'itération sur la valeur sur FrozenLake

**Objectif.** Réimplémenter l'agent de la section 4.5 à partir de ses trois tables, et résoudre `FrozenLake-v1`. À la fin de ce volet, votre agent affiche « Résolu ! » et vous savez dire en combien de tours.

**Protocole.** Les constantes sont celles de la section 4.5 : `GAMMA = 0.9`, 100 pas aléatoires par tour, 20 épisodes de test, arrêt lorsque le retour moyen de test dépasse **0,80**.

```python
class AgentTabulaire:
    def __init__(self, env):
        ...                 # À COMPLÉTER : les trois tables. Lesquelles, et clés par quoi ?

    def valeur_action(self, etat, action):
        compteurs = self.transitions[(etat, action)]
        total = sum(compteurs.values())
        if total == 0:
            return 0.0
        return sum(
            ...             # À COMPLÉTER : une ligne, et elle contient c_i / total
            for cible, compte in compteurs.items()
        )

    def balayage(self):
        for etat in range(self.env.observation_space.n):
            self.valeurs[etat] = ...     # À COMPLÉTER : où passe le max du balayage ?
```

**Trois points de contrôle, qui se vérifient chacun en une ligne.**

```python
# 1. Les probabilités estimées d'un couple (état, action) somment bien à 1.
cpt = agent.transitions[(0, 1)]
total = sum(cpt.values())
assert total == 0 or abs(sum(c / total for c in cpt.values()) - 1.0) < 1e-9

# 2. Un seul balayage par tour, et pas une convergence.
#    Comptez les appels : exactement un par tour.

# 3. La valeur d'un état jamais visité reste nulle, et ne lève aucune erreur.
assert agent.valeur_action(15, 0) == 0.0 or agent.transitions[(15, 0)]
```

**Attentes.**

* L'environnement est résolu en **quelques dizaines à quelques centaines de tours**, et l'exécution prend **moins d'une seconde** quoi qu'il arrive. Attendez-vous à une dispersion large : sur dix graines, le seuil est franchi entre le tour **37** et le tour **282**, médiane autour de **120**. Si votre première exécution en demande deux cents, votre code n'a rien d'anormal.
* **Et la raison de cette dispersion est le critère lui-même**, ce qui en fait la leçon cachée du volet. La politique optimale de `FrozenLake-v1` glissant réussit environ **trois fois sur quatre**. Dépasser 0,80 sur **vingt** épisodes de test demande donc un lot de test chanceux, et non une meilleure politique : le nombre de tours mesure surtout l'attente de cette chance. Mesurez la qualité réelle de votre politique sur **quatre cents** épisodes, et vous trouverez une valeur stable entre **0,50 et 0,74**. C'est la semaine 7 par anticipation : **une mesure sur vingt épisodes ne permet de décider de rien.**
* Les premiers tours affichent un retour de test de 0,000. Ce n'est pas un bogue : tant qu'aucun épisode n'a atteint l'objectif, il n'existe aucune récompense non nulle dans la table, donc rien à apprendre. Dites-le dans votre carnet en une phrase, avec le mot « exploration » dedans.
* Affichez la table des valeurs à la fin. Les seize nombres doivent dessiner une pente croissante du départ vers l'objectif, et les trous doivent valoir zéro. Si ce n'est pas le cas, le coupable est presque toujours la gestion de l'état terminal.
* **Ajoutez une ligne de commentaire sur la ligne où votre code lit la dynamique de l'environnement.** Ce commentaire est le vrai livrable de ce volet.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-04.ipynb" label="Volet A : itération sur la valeur avec trois tables, sur FrozenLake" >}}

---

## Volet B : sans modèle, Q-learning tabulaire sur le même environnement

**Objectif.** Résoudre exactement le même environnement avec un agent qui ne construit **aucune** table de transitions, et comparer.

**Protocole.** Reprenez la fonction `q_learning` de la section 4.7 et lancez-la sur `FrozenLake-v1`. Attention, deux réglages diffèrent de la falaise : prenez `gamma = 0.9` (l'environnement a un objectif à atteindre, pas une marche à minimiser) et un `alpha` plus petit, de l'ordre de 0,1, parce que le glissement rend chaque transition très bruitée. Mesurez la performance comme au volet A : 20 épisodes de test avec la politique **gloutonne**, et non \(\varepsilon\)-gloutonne.

**Attentes.**

* Q-learning y arrive aussi, et il lui faut **beaucoup plus d'épisodes** que de tours au volet A. C'est le résultat attendu et il ne faut pas le lire comme un échec.
* La comparaison que je vous demande d'écrire n'est **pas** « lequel gagne ». Elle est : **qu'est-ce que chacun des deux a le droit de regarder ?** Trois lignes dans votre carnet, une pour l'agent A, une pour l'agent B, une pour la conséquence.
* Une mesure utile et gratuite : comptez le nombre de transitions consommées par chacun des deux agents avant d'atteindre 0,80. C'est la bonne unité de comparaison, et pas le nombre de tours ni le temps de calcul.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-04.ipynb" label="Volet B : Q-learning tabulaire sur FrozenLake, sans aucun modèle" >}}

---

## Volet C, évalué : la falaise, Sarsa contre Q-learning

**Objectif.** Rendre **visible** la différence entre sur politique et hors politique, et savoir l'expliquer. FrozenLake ne peut pas le faire : son glissement mélange les deux effets, et sa récompense unique à l'objectif ne laisse rien apparaître. La falaise, elle, le montre en une figure.

**Écrivez l'environnement vous-même.** Il existe sous le nom `CliffWalking-v1` dans la famille des environnements en texte de Gymnasium, mais une grille de 4 × 12 tient en vingt lignes de Python et vous apprendrez davantage à l'écrire qu'à l'importer. Voici le squelette.

```python
class Falaise:
    """Grille 4 x 12. Départ en bas à gauche, objectif en bas à droite,
    falaise sur toute la rangée du bas entre les deux."""

    HAUT, BAS, GAUCHE, DROITE = 0, 1, 2, 3

    def __init__(self, n_lignes=4, n_colonnes=12):
        self.n_lignes, self.n_colonnes = n_lignes, n_colonnes
        self.depart = (n_lignes - 1, 0)
        self.objectif = (n_lignes - 1, n_colonnes - 1)

    def index(self, case):
        ligne, colonne = case
        return ligne * self.n_colonnes + colonne

    def reset(self):
        self.case = self.depart
        return self.index(self.case), {}

    def step(self, action):
        ...        # À COMPLÉTER. Trois règles, et une seule est subtile :
                   #  1. un déplacement hors grille laisse l'agent sur place ;
                   #  2. chaque transition rapporte -1 ;
                   #  3. entrer dans la falaise rapporte -100 et RENVOIE AU DÉPART,
                   #     sans terminer l'épisode. Seul l'objectif termine.
```

**Protocole.** `alpha = 0.5`, `gamma = 1.0` (non actualisé), `epsilon = 0.1`, **500 épisodes**, et les deux méthodes sur le même environnement et le même nombre d'épisodes. Produisez deux choses.

1. **La courbe de la somme des récompenses par épisode**, les deux méthodes superposées sur le même graphique. Lissez sur une dizaine d'épisodes, sinon le bruit cache tout. Axes nommés, légende, échelle verticale visible.
2. **Le chemin glouton appris par chacune**, affiché sur la grille. Un simple dessin en caractères suffit : une flèche par case, obtenue par \(\argmax_a Q(s,a)\).

**Attentes, et c'est ce que je corrigerai.**

* Les deux courbes se séparent nettement : Sarsa se stabilise autour de **−25**, Q-learning autour de **−50**. Si les vôtres se superposent, vérifiez d'abord votre `cible_future` : c'est presque toujours là qu'un `max` s'est glissé dans Sarsa ou qu'il a disparu de Q-learning.
* Les deux chemins gloutons sont **différents** : Q-learning longe le bord, Sarsa prend par le haut.
* **La réponse écrite, une demi-page, et c'est le cœur de l'exercice.** Expliquez, à partir de **vos** courbes et de **vos** deux chemins, pourquoi la méthode qui a appris la meilleure politique obtient le pire score en ligne. Votre raisonnement doit faire apparaître trois choses : la composition de la cible de chaque méthode, la distinction entre politique apprise et politique jouée, et le rôle de \(\varepsilon\).
* **Une mesure qui tranche, et elle coûte dix lignes.** Rejouez les deux politiques apprises de façon purement **gloutonne**, \(\varepsilon = 0\), sur cent épisodes chacune, et comparez les scores. Puis commentez : laquelle gagne maintenant, et pourquoi le classement s'inverse-t-il ?

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-04.ipynb" label="Volet C, évalué : la falaise, Sarsa contre Q-learning" >}}

---

## Volet D, facultatif : TD contre Monte-Carlo sur des valeurs vraies connues

**Objectif ouvert.** Comparer TD(0) et Monte-Carlo sur un problème dont on connaît les valeurs exactes, et donc mesurer une **erreur** et non seulement une performance.

**Piste de départ.** Construisez une marche aléatoire à cinq états : une ligne de cinq cases, un départ au centre, deux terminaisons aux extrémités, un pas à gauche ou à droite avec probabilité un demi, une récompense de 1 à la terminaison de droite et de 0 partout ailleurs, sans actualisation. Les valeurs vraies de cet environnement se calculent à la main et valent \(1/6, 2/6, 3/6, 4/6, 5/6\) de gauche à droite : vous avez donc une vérité de référence, ce qui est rare.

**Critères de réussite.**

* Les deux méthodes implémentées, TD(0) de la section 4.6 et Monte-Carlo à \(\alpha\) constant, sur le même environnement.
* Une courbe d'**erreur quadratique moyenne** par rapport aux valeurs vraies, en fonction du nombre d'épisodes, pour trois valeurs de \(\alpha\) par méthode.
* Une phrase de conclusion sur laquelle des deux descend le plus vite, et une phrase sur ce que \(\alpha\) change pour chacune.

> [!TIP]
 **Mon message pour ce laboratoire.** Vous venez d'écrire trois agents qui résolvent le même genre de problème, et le travail intéressant n'est aucun des trois : c'est de savoir dire, pour chacun, **de quelle information il se nourrit**. L'agent du volet A lit une dynamique qu'il a fabriquée. Celui du volet B ne lit qu'une suite de transitions. Celui du volet C ne lit la même suite de transitions que deux fois, avec deux cibles différentes, et en tire deux politiques différentes. C'est cette lecture-là que je vous demanderai encore en semaine 7, puis en semaine 10, et à la fin du cours vous la ferez d'un coup d'œil sur du code que vous n'avez pas écrit.
