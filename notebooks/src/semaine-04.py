# %% [markdown]
# # SCI1070 — Semaine 4 : tabulaire, et ce que chaque agent a le droit de regarder
#
# | Volet | Ce que vous y faites | Statut |
# | --- | --- | --- |
# | A | itération sur la valeur, trois tables, sur `FrozenLake-v1` | échauffement |
# | B | Q-learning tabulaire sur le **même** environnement, sans modèle | échauffement |
# | C | **la falaise, Sarsa contre Q-learning** | **évalué** |
# | D | TD(0) contre Monte-Carlo, sur des valeurs vraies connues | facultatif |
#
# Le laboratoire est **formatif** : la semaine 4 ne porte aucun jalon, le prochain est
# en semaine 7. Mais le **volet C** est l'exercice évalué, celui dont j'attends un
# rendu écrit et sur lequel porteront les questions du quiz.
#
# **Budget de calcul : quelques secondes par exécution, sur processeur central.** Tout
# est tabulaire cette semaine, et il n'y a pas une ligne de PyTorch dans ce carnet.
# Si l'un de vos exercices demande un processeur graphique, ce n'est pas votre
# matériel qui est en cause, c'est l'exercice : relisez l'énoncé.

# %% [smoke]
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("gymnasium") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "gymnasium[toy-text]>=1.0"], check=True)

import collections

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

GAMMA = 0.9
print("gymnasium", gym.__version__)

# %% [markdown]
# ---
# # Volet A : avec modèle, l'itération sur la valeur
#
# **Objectif.** Réimplémenter l'agent de la section 4.5 à partir de ses trois tables,
# et résoudre `FrozenLake-v1`. À la fin de ce volet, votre agent affiche « Résolu ! »
# et vous savez dire **en combien de tours**.
#
# **Les constantes sont celles de la section 4.5** : `GAMMA = 0.9`, 100 pas aléatoires
# par tour, 20 épisodes de test, arrêt lorsque le retour moyen de test dépasse **0,80**.

# %%
class AgentTabulaire:
    def __init__(self, env):
        self.env = env
        self.etat, _ = env.reset()
        ...                 # À COMPLÉTER : les trois tables. Lesquelles, et clés par quoi ?

    def jouer_n_pas_aleatoires(self, n: int = 100):
        """Remplit les tables de récompenses et de transitions. Aucune valeur ici."""
        for _ in range(n):
            action = self.env.action_space.sample()
            nouvel_etat, recompense, termine, tronque, _ = self.env.step(action)
            ...             # À COMPLÉTER : nourrir les deux tables, puis avancer
            self.etat, _ = self.env.reset() if (termine or tronque) else (nouvel_etat, None)

    def valeur_action(self, etat, action):
        compteurs = self.transitions[(etat, action)]
        total = sum(compteurs.values())
        if total == 0:
            return 0.0
        return sum(
            ...             # À COMPLÉTER : une ligne, et elle contient c_i / total
            for cible, compte in compteurs.items()
        )

    def meilleure_action(self, etat):
        return max(range(self.env.action_space.n),
                   key=lambda a: self.valeur_action(etat, a))

    def balayage(self):
        for etat in range(self.env.observation_space.n):
            self.valeurs[etat] = ...     # À COMPLÉTER : où passe le max du balayage ?

# %% [markdown]
# ### Les trois points de contrôle
#
# Chacun se vérifie en une ligne, et chacun attrape une erreur réelle.

# %%
env = gym.make("FrozenLake-v1")
agent = AgentTabulaire(env)
agent.jouer_n_pas_aleatoires(100)

# 1. Les probabilités estimées d'un couple (état, action) somment bien à 1.
cpt = agent.transitions[(0, 1)]
total = sum(cpt.values())
assert total == 0 or abs(sum(c / total for c in cpt.values()) - 1.0) < 1e-9

# 2. Un seul balayage par tour, et pas une convergence. Comptez les appels :
#    exactement un par tour. (Instrumentez `balayage` si vous voulez en être sûr.)

# 3. La valeur d'un état jamais visité reste nulle, et ne lève aucune erreur.
assert agent.valeur_action(15, 0) == 0.0 or agent.transitions[(15, 0)]
print("trois points de contrôle passés")

# %%
def tester(agent, env_test, episodes: int = 20) -> float:
    """20 épisodes avec la politique GLOUTONNE. Rend le retour moyen."""
    total = 0.0
    for _ in range(episodes):
        etat, _ = env_test.reset()
        while True:
            etat, recompense, termine, tronque, _ = env_test.step(agent.meilleure_action(etat))
            total += float(recompense)
            if termine or tronque:
                break
    return total / episodes


env_test = gym.make("FrozenLake-v1")
agent = AgentTabulaire(gym.make("FrozenLake-v1"))

transitions_consommees = 0
for tour in range(1, 1001):
    agent.jouer_n_pas_aleatoires(100)
    transitions_consommees += 100
    agent.balayage()

    score = tester(agent, env_test)
    print(f"tour {tour:3d} : retour de test {score:.3f}")
    if score > 0.80:
        print(f"Résolu ! en {tour} tours, {transitions_consommees} transitions")
        break

# %%
# La table des valeurs à la fin : seize nombres, à lire comme une grille 4 x 4.
print(np.round(np.array([agent.valeurs[s] for s in range(16)]).reshape(4, 4), 3))

# %% [markdown]
# **Attentes du volet A.**
#
# * L'environnement est résolu en **10 à 100 tours**, le plus souvent autour de la
#   dizaine, en **moins d'une seconde**.
# * Les premiers tours affichent un retour de test de **0,000**. Ce n'est pas un
#   bogue : tant qu'aucun épisode n'a atteint l'objectif, il n'existe aucune
#   récompense non nulle dans la table, donc rien à apprendre. Dites-le dans votre
#   carnet en une phrase, avec le mot **« exploration »** dedans.
# * Les seize nombres doivent dessiner une **pente croissante** du départ vers
#   l'objectif, et les trous doivent valoir zéro. Sinon, le coupable est presque
#   toujours la gestion de l'état terminal.
# * **Ajoutez une ligne de commentaire sur la ligne où votre code lit la dynamique de
#   l'environnement.** Ce commentaire est le vrai livrable de ce volet.

# %% [markdown]
# ---
# # Volet B : sans modèle, Q-learning tabulaire
#
# **Objectif.** Résoudre **exactement le même** environnement avec un agent qui ne
# construit **aucune** table de transitions, et comparer.
#
# **Deux réglages diffèrent de la falaise**, et ce n'est pas un détail :
# `gamma = 0.9` — l'environnement a un objectif à atteindre, pas une marche à
# minimiser — et un `alpha` plus petit, de l'ordre de **0,1**, parce que le glissement
# rend chaque transition très bruitée.

# %%
def q_learning(env, episodes: int, alpha: float = 0.1, gamma: float = 0.9,
               epsilon: float = 0.1, graine: int = 0):
    """Rend (Q, retours_par_episode, transitions_consommees)."""
    rng = np.random.default_rng(graine)
    Q = collections.defaultdict(float)      # clé : (état, action)
    ...        # À COMPLÉTER : la boucle de la section 4.7.
               # Rappel : la cible de Q-learning prend un max sur les actions de l'état
               # suivant, et cette action n'est PAS celle que l'agent va jouer.


Q_b, retours_b, transitions_b = q_learning(gym.make("FrozenLake-v1"), episodes=20_000)

# Mesurez la performance comme au volet A : 20 épisodes de test avec la politique
# GLOUTONNE, et non epsilon-gloutonne.
...        # À COMPLÉTER : le test glouton, et le nombre de transitions pour atteindre 0,80

# %% [markdown]
# **Attentes du volet B.**
#
# * Q-learning y arrive aussi, et il lui faut **beaucoup plus d'épisodes** que de
#   tours au volet A. C'est le résultat attendu et il ne faut pas le lire comme un
#   échec.
# * La comparaison que je vous demande d'écrire n'est **pas** « lequel gagne ». Elle
#   est : **qu'est-ce que chacun des deux a le droit de regarder ?** Trois lignes dans
#   votre carnet — une pour l'agent A, une pour l'agent B, une pour la conséquence.
# * Une mesure utile et gratuite : comptez le nombre de **transitions consommées** par
#   chacun des deux agents avant d'atteindre 0,80. C'est la bonne unité de comparaison,
#   et pas le nombre de tours ni le temps de calcul.

# %% [markdown]
# ---
# # Volet C, évalué : la falaise, Sarsa contre Q-learning
#
# **Objectif.** Rendre **visible** la différence entre sur politique et hors politique,
# et savoir l'expliquer. FrozenLake ne peut pas le faire : son glissement mélange les
# deux effets, et sa récompense unique à l'objectif ne laisse rien apparaître. La
# falaise, elle, le montre en une figure.
#
# **Écrivez l'environnement vous-même.** Il existe sous le nom `CliffWalking-v1` dans
# la famille des environnements en texte de Gymnasium, mais une grille de 4 × 12 tient
# en vingt lignes de Python et vous apprendrez davantage à l'écrire qu'à l'importer.

# %%
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

# %% [markdown]
# **Protocole.** `alpha = 0.5`, `gamma = 1.0` (non actualisé), `epsilon = 0.1`,
# **500 épisodes**, et les deux méthodes sur le même environnement et le même nombre
# d'épisodes.
#
# Écrivez **une seule** fonction pour les deux méthodes : elles ne diffèrent que par
# la composition de la cible, et les écrire séparément est la façon la plus sûre de
# laisser un `max` au mauvais endroit.

# %%
def controle_td(env, methode: str, episodes=500, alpha=0.5, gamma=1.0,
                epsilon=0.1, graine=0):
    """`methode` vaut "sarsa" ou "q-learning". Rend (Q, retours_par_episode)."""
    assert methode in ("sarsa", "q-learning")
    rng = np.random.default_rng(graine)
    Q = collections.defaultdict(float)

    ...        # À COMPLÉTER : une boucle, deux cibles.
               # Sarsa a besoin de A_{t+1}, l'action RÉELLEMENT jouée au pas suivant.
               # Q-learning prend un max, et ne joue pas forcément l'action du max.
               # cible_future = ...  <- c'est la SEULE ligne qui change entre les deux

    return Q, retours


falaise = Falaise()
Q_sarsa, r_sarsa = controle_td(falaise, "sarsa")
Q_qlearn, r_qlearn = controle_td(falaise, "q-learning")

# %%
def lisser(x, fenetre=10):
    return np.convolve(np.asarray(x, dtype=float), np.ones(fenetre) / fenetre, mode="valid")


fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(lisser(r_sarsa), label="Sarsa (sur politique)")
ax.plot(lisser(r_qlearn), label="Q-learning (hors politique)")
ax.set_xlabel("épisode"); ax.set_ylabel("somme des récompenses de l'épisode")
ax.set_ylim(-120, 0)
ax.legend(); ax.grid(alpha=0.3)
ax.set_title("La falaise : la meilleure politique obtient le pire score en ligne")
plt.show()

# %%
def dessiner_politique(Q, env):
    """Une flèche par case, obtenue par argmax_a Q(s,a). Dessin en caractères."""
    fleches = {env.HAUT: "^", env.BAS: "v", env.GAUCHE: "<", env.DROITE: ">"}
    ...        # À COMPLÉTER : dix lignes, et c'est la deuxième figure du volet


print("Sarsa :");       dessiner_politique(Q_sarsa, falaise)
print("\nQ-learning :"); dessiner_politique(Q_qlearn, falaise)

# %% [markdown]
# ### La mesure qui tranche, et elle coûte dix lignes
#
# Rejouez les deux politiques apprises de façon **purement gloutonne**,
# \(\varepsilon = 0\), sur cent épisodes chacune, et comparez les scores. Puis
# commentez : **laquelle gagne maintenant, et pourquoi le classement s'inverse-t-il ?**

# %%
def jouer_glouton(Q, env, episodes=100, max_pas=1000):
    ...        # À COMPLÉTER : aucune exploration, juste argmax_a Q(s,a)


print("Sarsa, glouton      :", jouer_glouton(Q_sarsa, falaise))
print("Q-learning, glouton :", jouer_glouton(Q_qlearn, falaise))

# %% [markdown]
# **Attentes du volet C, et c'est ce que je corrigerai.**
#
# * Les deux courbes se séparent nettement : **Sarsa se stabilise autour de −25,
#   Q-learning autour de −50.** Si les vôtres se superposent, vérifiez d'abord votre
#   `cible_future` : c'est presque toujours là qu'un `max` s'est glissé dans Sarsa ou
#   qu'il a disparu de Q-learning.
# * Les deux chemins gloutons sont **différents** : Q-learning longe le bord, Sarsa
#   prend par le haut.
# * **La réponse écrite, une demi-page, et c'est le cœur de l'exercice.** Expliquez,
#   à partir de **vos** courbes et de **vos** deux chemins, pourquoi la méthode qui a
#   appris la meilleure politique obtient le pire score en ligne. Votre raisonnement
#   doit faire apparaître trois choses : la **composition de la cible** de chaque
#   méthode, la distinction entre **politique apprise et politique jouée**, et le rôle
#   de \(\varepsilon\).
# * Et le classement **s'inverse** quand vous rejouez en glouton. Dites pourquoi.

# %% [markdown]
# ---
# # Volet D, facultatif : TD(0) contre Monte-Carlo sur des valeurs vraies connues
#
# **Objectif ouvert.** Comparer TD(0) et Monte-Carlo sur un problème dont on connaît
# les valeurs **exactes**, et donc mesurer une **erreur** et non seulement une
# performance. C'est rare, et cela vaut la peine d'en profiter.
#
# Une marche aléatoire à cinq états : une ligne de cinq cases, un départ au centre,
# deux terminaisons aux extrémités, un pas à gauche ou à droite avec probabilité un
# demi, une récompense de 1 à la terminaison de droite et 0 partout ailleurs, sans
# actualisation.

# %% [smoke]
# Les valeurs vraies se calculent à la main, et c'est votre vérité de référence.
VALEURS_VRAIES = np.array([1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6])
print("valeurs vraies :", np.round(VALEURS_VRAIES, 4))


def marche_aleatoire(rng):
    """Rend la liste des états visités et la récompense finale. Cinq états : 0..4."""
    etat = 2
    visites = [etat]
    while True:
        etat += 1 if rng.random() < 0.5 else -1
        if etat < 0:
            return visites, 0.0
        if etat > 4:
            return visites, 1.0
        visites.append(etat)


rng = np.random.default_rng(0)
visites, r = marche_aleatoire(rng)
print("un épisode :", visites, "récompense finale", r)

# %%
# À COMPLÉTER : TD(0) de la section 4.6, et Monte-Carlo à alpha constant, sur le
# même environnement. Puis une courbe d'erreur quadratique moyenne par rapport à
# VALEURS_VRAIES, en fonction du nombre d'épisodes, pour TROIS valeurs d'alpha par
# méthode.
...

# %% [markdown]
# **Critères de réussite du volet D.**
#
# * Les deux méthodes implémentées sur le même environnement.
# * Une courbe d'**erreur quadratique moyenne** par rapport aux valeurs vraies, en
#   fonction du nombre d'épisodes, pour **trois** valeurs de \(\alpha\) par méthode.
# * Une phrase sur laquelle des deux descend le plus vite, et une phrase sur ce que
#   \(\alpha\) change pour chacune.
#
# > **Mon message pour ce laboratoire.** Vous venez d'écrire trois agents qui
# > résolvent le même genre de problème, et le travail intéressant n'est aucun des
# > trois : c'est de savoir dire, pour chacun, **de quelle information il se nourrit**.
# > L'agent du volet A lit une dynamique qu'il a fabriquée. Celui du volet B ne lit
# > qu'une suite de transitions. Celui du volet C ne lit la même suite de transitions
# > que deux fois, avec deux cibles différentes, et en tire deux politiques
# > différentes. C'est cette lecture-là que je vous demanderai encore en semaine 7,
# > puis en semaine 10, et à la fin du cours vous la ferez d'un coup d'œil sur du code
# > que vous n'avez pas écrit.
