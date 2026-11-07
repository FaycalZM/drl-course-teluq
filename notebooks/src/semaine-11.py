# %% [markdown]
# # SCI1070 — Semaine 11 : explorer, et mesurer un échec correctement
#
# | Partie | Ce que vous y faites |
# | --- | --- |
# | Échauffement | River Swim : trois comptages, cinq graines |
# | A | la méthode de référence, et **un échec correctement mesuré** |
# | B | réseaux bruités contre calendrier de \(\varepsilon\) |
# | C | une prime de nouveauté, et le piège qu'elle tend |
# | Solution courte | deux références en six lignes, **après** vos volets |
#
# Formatif : rien n'y est noté. J'en profite pour vous demander quelque chose qu'une
# semaine notée rend difficile : **laissez le volet A échouer complètement**, et
# passez du temps à regarder **comment** il échoue.
#
# **La tâche est `MountainCar-v0`, et ce n'est pas un choix de confort** : c'est la
# tâche de ce cours sur laquelle la méthode \(\varepsilon\)-gloutonne échoue
# **complètement**, ce qui en fait le seul banc d'essai honnête pour une semaine
# d'exploration. Elle est très bon marché, elle tourne sur processeur ordinaire, et un
# épisode y dure deux cents pas au maximum.
#
# **Le protocole du jalon 2 s'applique sans que je le redemande** : au moins trois
# graines, un intervalle sur chaque courbe, un critère d'arrêt déclaré d'avance. Deux
# exigences propres à cette semaine s'y ajoutent :
#
# * **Mesurez le temps jusqu'à la première atteinte du but**, et pas seulement le
#   retour final. Le Tableau 11-1 a montré que les deux grandeurs **ne classent pas
#   les méthodes dans le même ordre**.
# * **Évaluez toujours sur un environnement sans prime**, et étiquetez comme telles
#   les courbes mesurées sous enveloppe. Une courbe d'entraînement sous prime et une
#   courbe d'évaluation **ne sont pas la même grandeur**.

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)
if importlib.util.find_spec("sci1070") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "git+https://github.com/FaycalZM/drl-course-teluq.git#subdirectory=code"],
                   check=True)

import collections

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from sci1070.protocole import intervalle, se_recouvrent
from sci1070.courbes import tracer_bande
from sci1070.graines import fixer_graines

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
GRAINES = [0, 1, 2]

# La distinction qui est TOUTE l'information de cette semaine (piège nº1).
env = gym.make("MountainCar-v0")
print("MountainCar-v0 | obs", env.observation_space.shape, "| actions", env.action_space.n)
print("limite de pas :", gym.registry["MountainCar-v0"].max_episode_steps)
print("termine = le drapeau est atteint  |  tronque = les 200 pas sont écoulés")
env.close()

# %% [markdown]
# ---
# # Échauffement : reproduisez les trois nombres de River Swim
#
# Dix minutes, et ce n'est pas décoratif : il vous donne la mesure de la semaine dans
# vos propres mains.
#
# Reprenez le fragment de la section 11.2, complétez-le, et reproduisez les trois
# comptages : **100 pas, 1 000 pas, 10 000 pas**, dix pas par épisode, agent purement
# aléatoire. **Vérifiez par addition** que chaque ligne somme bien au nombre de pas.

# %%
class RiverSwim:
    """Une chaîne d'états. Le courant pousse vers la gauche ; le but est à droite."""

    def __init__(self, n_etats: int = 6):
        self.n_etats = n_etats

    def reset(self):
        ...        # À COMPLÉTER : où commence-t-on ?

    def step(self, action):
        ...        # À COMPLÉTER : le fragment de la section 11.2


def compter_visites(n_pas, n_etats=6, longueur_episode=10, graine=0):
    """Rend un tableau de comptages, un par état. Il doit sommer à n_pas."""
    ...        # À COMPLÉTER


for n_pas in [100, 1_000, 10_000]:
    visites = compter_visites(n_pas)
    assert visites.sum() == n_pas, "la ligne ne somme pas au nombre de pas"
    print(f"{n_pas:6d} pas : {visites}  (somme {visites.sum()})")

# %% [markdown]
# **Trois questions dans votre carnet.**
#
# 1. Combien de visites de l'**état 6** obtenez-vous en 10 000 pas, et **sur cinq
#    graines**, quelle est l'amplitude de ce nombre ? Le tableau de la section 11.2
#    donne 5 : vous allez voir ce qu'une graine fait à un comptage de cette taille.
# 2. Que devient ce comptage si vous portez la longueur d'épisode de 10 à 50 pas ?
#    **Dites pourquoi avant de lancer**, puis comparez votre prédiction au résultat.
# 3. Que devient-il si vous passez de six états à dix ? C'est l'extrapolation de la
#    section 11.2, et elle coûte un paramètre à changer.

# %%
# Question 1 : cinq graines, et l'amplitude du comptage du dernier état.
derniers = [compter_visites(10_000, graine=g)[-1] for g in range(5)]
print("état final, cinq graines :", derniers)
print(f"amplitude : {max(derniers) - min(derniers)} sur une valeur attendue autour de 5")

# %%
# Questions 2 et 3. Écrivez votre prédiction AVANT d'exécuter.
# Prédiction (question 2) : ...
# Prédiction (question 3) : ...
...        # À COMPLÉTER

# %% [markdown]
# ---
# # Volet A : la méthode de référence, et un échec correctement mesuré
#
# **Objectif.** Faire tourner un réseau Q profond \(\varepsilon\)-glouton sur
# `MountainCar-v0`, et **documenter son échec comme un résultat**.
#
# > **Ce volet est le seul de tout le cours dont le résultat attendu est un échec, et
# > je veux que vous le rapportiez comme une mesure.** Pas comme un problème à régler,
# > pas comme un bogue à chercher : **comme une mesure**. Si après cent mille pas
# > votre compteur d'atteintes du but affiche zéro, votre volet A est **réussi**. Et
# > s'il affiche un nombre non nul, c'est également un résultat intéressant : regardez
# > votre graine, votre calendrier de \(\varepsilon\), et si vous n'avez pas par
# > mégarde ajouté une récompense quelque part.

# %% [markdown]
# **Étape 2 — installez les deux instruments AVANT de lancer quoi que ce soit.**
#
# Le compteur cumulé d'atteintes du but, et la position maximale atteinte par épisode.
#
# **Vérifiez que vous distinguez bien `termine` de `tronque`.** Les confondre rend
# votre compteur d'atteintes du but égal au nombre d'épisodes, et **vous croirez avoir
# résolu la tâche en trois minutes**.

# %% [smoke]
# La preuve que la distinction compte : un agent aléatoire, dix épisodes.
env = gym.make("MountainCar-v0")
buts, tronques = 0, 0
for k in range(10):
    obs, _ = env.reset(seed=k)
    while True:
        obs, r, termine, tronque, _ = env.step(env.action_space.sample())
        if termine or tronque:
            buts += int(termine)
            tronques += int(tronque)
            break
env.close()
print(f"sur dix épisodes aléatoires : {buts} atteinte(s) du but, {tronques} troncature(s)")
print("-> si votre compteur affiche 10, vous comptez les troncatures")

# %%
class Instruments:
    """Les deux instruments de la section 11.5. Installés avant l'entraînement."""

    def __init__(self):
        self.buts_cumules = 0
        self.positions_max = []
        self.premier_but_au_pas = None

    def episode(self, positions, termine, pas_entrainement):
        ...        # À COMPLÉTER

# %%
def entrainer(variante="epsilon", graine=0, max_pas=100_000,
              frequence_bruit=1, c_prime=0.0):
    """UN programme, variantes en argument. `variante` ∈ {epsilon, bruite, rnd}."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : votre réseau Q profond du jalon 2.
               # Le réseau de cette tâche est minuscule : deux entrées, une couche
               # cachée de 128, trois sorties. Calendrier de epsilon de 1,0 à 0,02.


resultats_a = [entrainer("epsilon", graine=g) for g in GRAINES]

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
...        # À COMPLÉTER
           # gauche : la courbe de récompense, qui sera PLATE
           # droite : la courbe de position maximale, qui ne le sera PAS
axes[0].set_title("récompense : plate"); axes[1].set_title("position maximale : pas plate")
for ax in axes:
    ax.set_xlabel("pas d'entraînement"); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# %% [markdown]
# **Étape 4 — trois phrases dans votre carnet.** Combien de fois le but a été atteint,
# ce que la position maximale a fait pendant l'entraînement, et **à quel pas
# d'entraînement votre \(\varepsilon\) a cessé d'explorer**.
#
# **La troisième phrase est celle qui compte** : c'est elle qui explique pourquoi
# l'échec est **permanent** et non seulement lent.

# %%
...        # À COMPLÉTER : les trois nombres

# %% [markdown]
# ---
# # Volet B : des réseaux bruités contre un calendrier de ε
#
# **Étape 1.** Reprenez la classe `CoucheBruitee` de la section 6.9, **sans la
# réécrire**, et remplacez la dernière couche de votre réseau du volet A. Retirez
# **entièrement** le calendrier de \(\varepsilon\) : l'agent devient purement glouton
# sur une sortie bruitée.

# %%
class CoucheBruitee(nn.Module):
    ...        # À COMPLÉTER : celle de la section 6.9, reprise et non réécrite

# %% [markdown]
# **Étape 2.** Ajoutez l'appel explicite de **tirage du bruit** à chaque itération.
# Vérifiez, en imprimant deux passes avant sur la **même** observation, que les
# sorties **diffèrent** : si elles sont identiques, votre bruit n'est pas retiré et
# **vous mesurez un réseau ordinaire**.

# %%
# La vérification, et elle tient en quatre lignes.
reseau_bruite = ...        # À COMPLÉTER
obs_test = torch.zeros(1, 2)
sortie_1 = reseau_bruite(obs_test)
reseau_bruite.retirer_bruit()
sortie_2 = reseau_bruite(obs_test)
assert not torch.allclose(sortie_1, sortie_2), "le bruit n'est pas retiré"
print("les deux passes diffèrent : le bruit est bien retiré")

# %% [markdown]
# **Étape 3.** Trois graines, les deux mêmes instruments. Comparez au volet A sur deux
# grandeurs : le **premier pas d'entraînement auquel le but est atteint**, et la
# position maximale moyenne sur les dix mille premiers pas.

# %%
resultats_b = [entrainer("bruite", graine=g) for g in GRAINES]
...        # À COMPLÉTER : le tableau comparatif A contre B, sur les deux grandeurs

# %% [markdown]
# **Étape 4, et c'est le réglage à explorer.** Faites varier la **fréquence de tirage
# du bruit** : à chaque itération, puis une fois sur dix, puis une fois sur cent.
#
# Vous mesurez ici, directement, l'idée centrale de la section 11.3 : la **cohérence**
# de la politique de collecte. **Prédisez le sens de l'effet avant de lancer**, puis
# commentez l'écart.

# %%
# Prédiction : ...
for f in [1, 10, 100]:
    ...        # À COMPLÉTER

# %% [markdown]
# ---
# # Volet C : une prime de nouveauté, et le piège qu'elle tend
#
# **Étape 1.** Écrivez l'enveloppe. Structure du fragment de la section 11.3, mais
# prime de **distillation** plutôt que comptage : deux réseaux, la référence **figée**
# à trois couches et le prédicteur à une seule, la prime en **erreur quadratique**.
# Conservez la récompense extrinsèque et la prime **séparément** dans `info`.

# %%
class PrimeDistillation(gym.Wrapper):
    """La prime de nouveauté. L'environnement d'ÉVALUATION ne la porte jamais."""

    def __init__(self, env, c=1.0):
        super().__init__(env)
        self.c = c
        self.reference = ...        # À COMPLÉTER : trois couches, FIGÉE (piège nº4)
        self.predicteur = ...       # À COMPLÉTER : une seule couche
        ...                         # À COMPLÉTER : requires_grad_(False) sur la référence,
                                    # et NE PAS passer ses paramètres à l'optimiseur

    def step(self, action):
        obs, recompense, termine, tronque, info = self.env.step(action)
        prime = ...        # À COMPLÉTER : erreur quadratique, DÉTACHÉE (piège de l'étape 2)
        info["recompense_extrinseque"] = float(recompense)
        info["prime"] = float(prime)
        return obs, recompense + self.c * prime, termine, tronque, info

# %% [markdown]
# **Étape 3 — deux environnements, pas un.** L'environnement d'**entraînement** porte
# l'enveloppe ; l'environnement d'**évaluation** ne la porte pas. Si vous évaluez sous
# enveloppe, vos retours de test seront systématiquement meilleurs que la réalité, et
# **vous ne pourrez les comparer à rien**.

# %%
env_entrainement = PrimeDistillation(gym.make("MountainCar-v0"), c=1.0)
env_evaluation = gym.make("MountainCar-v0")        # SANS enveloppe. Jamais sous prime.

# %% [markdown]
# **Étape 4.** Faites varier \(c\) sur **trois valeurs séparées par un facteur dix**,
# sur trois graines, avec intervalle. Rapportez pour chaque valeur : le temps jusqu'au
# premier but, le retour d'évaluation final, et **la valeur atteinte par votre
# critère**, pas seulement le verdict de franchissement. Le millième de point de la
# section 11.6 est là pour vous rappeler pourquoi.

# %%
for c in [0.1, 1.0, 10.0]:
    scores = [...]        # À COMPLÉTER : trois graines
    moyenne, bas, haut = intervalle(scores)
    print(f"c = {c:5.1f} : {moyenne:8.1f}  [{bas:.1f}, {haut:.1f}]")

# %% [markdown]
# **Étape 5 — le volet C en une image.** Tracez la **perte du prédicteur** le long de
# l'entraînement, et **marquez sur le même axe le moment de la première atteinte du
# but**. Dites ce que vous voyez.
#
# La section 11.6 annonce une croissance de cette perte au moment où le comportement
# change : **vérifiez si cela se produit chez vous, et dites-le franchement si ce
# n'est pas le cas.**

# %%
...        # À COMPLÉTER : la perte du prédicteur, et la marque du premier but

# %% [markdown]
# > **Quatre pièges de ce laboratoire, et chacun coûte une soirée.**
# >
# > 1. **`termine` contre `tronque`** : sur cette tâche, la distinction est toute
# >    l'information, et la confondre invalide chacune de vos mesures.
# > 2. **Le coefficient \(c\) appliqué deux fois**, une fois dans l'enveloppe et une
# >    fois dans la boucle. Votre prime est alors des dizaines de fois trop grande, et
# >    **votre agent devient un touriste**.
# > 3. **L'évaluation sous enveloppe** : vos deux courbes montent ensemble, tout a
# >    l'air de fonctionner, et vous ne mesurez plus la tâche.
# > 4. **Le réseau de référence qui apprend** : si vous oubliez `requires_grad_(False)`
# >    ou si vous passez ses paramètres à l'optimiseur, les deux réseaux convergent
# >    l'un vers l'autre, la prime tombe à zéro partout, et **votre méthode redevient
# >    exactement celle du volet A, en plus lente**.

# %% [markdown]
# ---
# # La solution courte, et ce qu'elle vous apprend

# %%
# Une reference que vous n'avez pas ecrite, pour situer la votre.
# A executer APRES vos trois volets.
from stable_baselines3 import DQN, PPO
import gymnasium as gym

env = gym.make("MountainCar-v0")

# 1. La methode de valeur : attendez-vous a ce qu'elle n'arrive a rien.
dqn = DQN("MlpPolicy", env, verbose=0).learn(total_timesteps=100_000)

# 2. La methode de politique, SANS exploration dirigee : elle devrait au
#    moins trouver le but, comme la section 11.6 le rapporte.
ppo = PPO("MlpPolicy", env, verbose=0).learn(total_timesteps=200_000)

# %% [markdown]
# > **Les deux budgets de pas de ce fragment ne sont pas des cibles, et ils ne
# > prédisent rien.** Je les mets pour que le fragment tourne en quelques minutes,
# > c'est tout. Les chiffres du Tableau 11-1 portent sur un autre code, d'autres
# > hyperparamètres et des dizaines de milliers d'épisodes. Comme en semaine 10, la
# > cible à atteindre est **la vôtre** : faites une exécution pilote, lisez ce qu'elle
# > obtient, annoncez-le dans votre carnet comme votre référence, et comparez toutes
# > vos configurations à cette référence **sur les mêmes graines**.

# %%
# Et la mesure qui ferme la semaine : les deux grandeurs ne classent pas les méthodes
# dans le même ordre. Rapportez les DEUX.
...        # À COMPLÉTER : temps jusqu'au premier but, et retour final, pour A, B, C et SB3
