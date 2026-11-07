# %% [markdown]
# # SCI1070 — Semaine 5 : le réseau Q profond, et ce que chaque réparation répare
#
# | Volet | Ce que vous y faites | Statut |
# | --- | --- | --- |
# | A | un DQN complet sur `CartPole-v1`, des cinq pièces à la convergence | implémentation |
# | B | **l'ablation : réseau cible et tampon, retirés un par un** | **évalué** |
# | C | évaluer un agent de Pong à partir de poids fournis | récompense |
# | D | facultatif | — |
#
# **Budget de calcul, et il explique la forme du laboratoire.** Un DQN complet sur
# CartPole ou LunarLander tient en **moins de quinze minutes** sur un T4, celui que
# Colab accorde gratuitement : vous l'entraînerez donc pour de vrai, du premier pas à
# la convergence. Un DQN sur Pong demande **une à trois heures** : il est hors de
# portée d'une session, et le volet C **n'entraîne rien**.
#
# > **Un conseil avant de lancer quoi que ce soit.** Activez l'accélérateur graphique
# > dans Colab **avant** d'exécuter la première cellule, et vérifiez-le par la ligne
# > ci-dessous. Chaque session de ce laboratoire où un étudiant se plaint d'une
# > lenteur commence par cette ligne, et elle affiche `False` neuf fois sur dix.

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

import collections

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

peripherique = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("torch.cuda.is_available() :", torch.cuda.is_available(), "| périphérique :", peripherique)

GAMMA = 0.99
BATCH_SIZE = 64
REPLAY_SIZE = 10_000
REPLAY_START_SIZE = 1_000
LEARNING_RATE = 1e-3
SYNC_TARGET_FRAMES = 500
EPSILON_DEBUT, EPSILON_FIN, EPSILON_TRAMES = 1.0, 0.02, 10_000
SEUIL_RESOLU = 475

Transition = collections.namedtuple(
    "Transition", ["obs", "action", "recompense", "termine", "obs_suivante"])

# %% [markdown]
# ---
# # Volet A : un DQN complet sur CartPole
#
# **Objectif.** Écrire un réseau Q profond entier, des cinq pièces jusqu'à la boucle,
# et faire converger `CartPole-v1`.
#
# CartPole n'a besoin d'**aucune** machinerie Atari : pas d'enveloppes d'image, pas de
# convolutions, pas d'empilement de trames, puisque l'observation contient déjà la
# vitesse et la vitesse angulaire. Vous réutilisez le petit réseau de la section 5.5,
# deux couches cachées de 128 unités.

# %%
class TamponDeRejeu:
    def __init__(self, capacite):
        ...        # À COMPLÉTER : une seule ligne, et elle contient maxlen

    def __len__(self):
        return len(self.memoire)

    def ajouter(self, transition):
        self.memoire.append(transition)

    def echantillonner(self, taille_lot):
        ...        # À COMPLÉTER : tirage uniforme, puis cinq tableaux NumPy

# %%
class ReseauQ(nn.Module):
    """Deux couches cachées de 128 unités. Une sortie par action, aucune non-linéarité
    après la dernière couche."""

    def __init__(self, n_obs: int, n_actions: int):
        super().__init__()
        ...        # À COMPLÉTER : le réseau de la section 5.5

    def forward(self, x):
        ...        # À COMPLÉTER

# %%
def calculer_perte(lot, reseau, reseau_cible, gamma, peripherique):
    obs, actions, recompenses, termines, obs_suivantes = lot

    obs_t = torch.as_tensor(obs, dtype=torch.float32).to(peripherique)
    obs_suiv_t = torch.as_tensor(obs_suivantes, dtype=torch.float32).to(peripherique)
    actions_t = torch.as_tensor(actions, dtype=torch.int64).to(peripherique)
    recompenses_t = torch.as_tensor(recompenses, dtype=torch.float32).to(peripherique)
    termines_t = torch.as_tensor(termines, dtype=torch.bool).to(peripherique)

    valeurs_action = ...      # À COMPLÉTER : gather sur la dimension des actions
    with torch.no_grad():
        valeurs_suivantes = ...   # À COMPLÉTER : le max, et sur QUEL réseau ?
        ...                       # À COMPLÉTER : le masque terminal
    cibles = ...
    return nn.MSELoss()(valeurs_action, cibles)

# %% [markdown]
# ### Les quatre points de contrôle
#
# Chacun se vérifie en une assertion, et ils attrapent quatre des cinq bogues
# classiques de la semaine. **Écrivez-les dans votre carnet.**

# %%
# 1. gather prélève bien UNE valeur par ligne du lot.
assert valeurs_action.shape == (BATCH_SIZE,)

# 2. La cible ne porte AUCUN gradient. C'est le semi-gradient, vérifié.
assert not cibles.requires_grad

# 3. Les deux réseaux sont distincts en mémoire, et identiques après synchro.
assert reseau is not reseau_cible
reseau_cible.load_state_dict(reseau.state_dict())
assert torch.equal(next(reseau.parameters()), next(reseau_cible.parameters()))

# 4. Le masque terminal a bien mis des zéros, et pas des valeurs de table.
assert float(valeurs_suivantes[termines_t].abs().sum()) == 0.0

# %% [markdown]
# ### La boucle
#
# Elle est paramétrée dès maintenant : le volet B va la rappeler **trois fois** en ne
# changeant qu'une chose, et une boucle recopiée trois fois est la façon la plus sûre
# de faire diverger ce qu'on croit comparer.

# %%
def entrainer_dqn(sans_reseau_cible=False, sans_tampon=False, graine=0,
                  max_trames=150_000, env_id="CartPole-v1"):
    """Rend (trames, retours_par_episode, trames_par_episode)."""
    ...        # À COMPLÉTER : la boucle complète.
               #   `sans_reseau_cible`  -> la cible passe par `reseau`, pas `reseau_cible`
               #   `sans_tampon`        -> le lot est fait des 64 DERNIÈRES transitions,
               #                           dans l'ordre, sans aucun tirage
               # Comptez les TRAMES, pas les épisodes.


trames, retours, trames_cumulees = entrainer_dqn()

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(trames_cumulees, retours, linewidth=0.6)
axes[0].set_title("brut : un DQN est bruité")
lisse = np.convolve(retours, np.ones(10) / 10, mode="valid")
axes[1].plot(trames_cumulees[9:], lisse)
axes[1].set_title("lissé sur dix épisodes : il apprend quand même")
for ax in axes:
    ax.set_xlabel("trames")      # des TRAMES, jamais des épisodes
    ax.set_ylabel("retour de l'épisode")
    ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# %% [markdown]
# **Attentes du volet A.**
#
# * Résolu en **quelques dizaines de milliers de trames**, en moins de quinze minutes
#   et le plus souvent en beaucoup moins.
# * Les deux courbes sont instructives : la brute montre à quel point un DQN est
#   bruité, la lissée montre qu'il apprend quand même.
# * Attendez-vous à voir le retour **redescendre** après un premier succès, parfois
#   brutalement. Ce n'est pas un bogue, c'est le régime de la section 5.9, et vous le
#   commenterez en une phrase.
# * **Comptez les trames, pas les épisodes.** Si votre axe horizontal est en épisodes,
#   votre courbe compare des épisodes de 20 pas avec des épisodes de 500 pas.

# %% [markdown]
# ---
# # Volet B, évalué : l'ablation
#
# **Objectif. Mesurer, et non croire.** La section 5.7 affirme que le réseau cible et
# le tampon de rejeu sont nécessaires. Vous allez les **retirer**, un par un, et
# regarder ce qui se passe.
#
# Trois configurations, **le même code**, **la même graine**, le même nombre de
# trames, et trois courbes sur un seul graphique.
#
# | Configuration | La seule chose qui change | Ce que vous retirez |
# | --- | --- | --- |
# | **(1) complète** | rien | la référence du volet A |
# | **(2) sans réseau cible** | `reseau_cible` remplacé par `reseau` dans la perte | la cible cesse d'être figée |
# | **(3) sans tampon** | le lot est fait des 64 **dernières** transitions, dans l'ordre | l'indépendance des données |

# %%
# Configuration (2) : une seule ligne change dans tout le programme.
#     valeurs_suivantes = reseau(obs_suiv_t).max(1)[0]      # au lieu de reseau_cible

# Configuration (3) : le tampon devient une fenêtre glissante, sans tirage.
def dernieres_transitions(memoire, taille_lot):
    """AUCUN tirage : les transitions les plus récentes, dans l'ordre."""
    return list(memoire)[-taille_lot:]

# %%
configurations = {
    "(1) complète": dict(),
    "(2) sans réseau cible": dict(sans_reseau_cible=True),
    "(3) sans tampon": dict(sans_tampon=True),
}

resultats = {}
for nom, options in configurations.items():
    resultats[nom] = entrainer_dqn(graine=0, **options)    # LA MÊME GRAINE

# %%
fig, ax = plt.subplots(figsize=(8, 5))
for nom, (trames, retours, cumul) in resultats.items():
    lisse = np.convolve(retours, np.ones(10) / 10, mode="valid")   # lissage IDENTIQUE
    ax.plot(cumul[9:], lisse, label=nom)
ax.set_xlabel("trames"); ax.set_ylabel("retour, lissé sur dix épisodes")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %%
# Le tableau à trois lignes : trames pour atteindre une moyenne de 200, ou « jamais ».
for nom, (trames, retours, cumul) in resultats.items():
    lisse = np.convolve(retours, np.ones(10) / 10, mode="valid")
    atteint = np.argmax(lisse >= 200) if (lisse >= 200).any() else None
    quand = f"{cumul[9:][atteint]:,} trames" if atteint is not None else "jamais atteint"
    print(f"{nom:24s} {quand}")

# %% [markdown]
# **Attentes du volet B, et c'est ce que je corrigerai.**
#
# * Les trois courbes sur un même graphique, axes nommés, légende, axe horizontal en
#   **trames**, **lissage identique pour les trois**. Sans cette dernière précaution,
#   la comparaison ne veut rien dire.
# * **Une demi-page écrite**, et c'est le cœur de l'exercice. Pour chacune des deux
#   ablations : quelle hypothèse de la section 5.2 ou 5.7 vous venez de violer, ce que
#   vous observez dans la courbe, et pourquoi la seconde découle de la première. Les
#   mots que j'attends sont **« non stationnaire »**, **« corrélées »** et
#   **« distribution »**.
# * **Un tableau à trois lignes** : trames pour atteindre une moyenne de 200, ou la
#   mention « jamais atteint ».
# * **Une mise en garde que vous écrivez vous-même**, en une phrase : pourquoi une
#   seule exécution par configuration ne suffit-elle pas à conclure ? La réponse est
#   dans la section 5.9, et elle vaut un chiffre.
#
# **Facultatif, et instructif.** Une quatrième configuration où vous retirez
# `.detach()` et `torch.no_grad()` de la cible. **Prédisez le résultat avant de
# lancer**, écrivez votre prédiction, puis comparez. C'est la façon la plus rapide de
# vérifier que la section 5.4 est comprise.

# %%
...        # À COMPLÉTER, facultatif : la quatrième configuration, et votre prédiction écrite

# %% [markdown]
# ---
# # Volet C : jouer à Pong, à partir de poids fournis
#
# **Objectif.** Voir ce que la méthode produit, et écrire la boucle d'évaluation qui
# le montre. **Rien n'est entraîné dans ce volet** : les poids vous sont fournis,
# parce qu'un entraînement complet demanderait une à trois heures.
#
# **Ce que vous écrivez.** Toute la chaîne d'enveloppes de la section 5.8, le réseau
# de la section 5.8, le chargement des poids, et la boucle d'évaluation.

# %%
# Atari demande deux paquets de plus. ale-py embarque les ROMs depuis la version 0.9.
for paquet, module in [("ale-py>=0.10", "ale_py"), ("opencv-python", "cv2")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

import ale_py
gym.register_envs(ale_py)

# Les poids fournis, et d'où ils viennent : voir notebooks/POIDS.md du dépôt du cours.
import urllib.request
from pathlib import Path

POIDS = Path("pong_poids.dat")
URL_POIDS = ("https://raw.githubusercontent.com/FaycalZM/drl-course-teluq/"
             "main/notebooks/poids/pong_poids.dat")
if not POIDS.exists():
    urllib.request.urlretrieve(URL_POIDS, POIDS)
print("poids :", POIDS, POIDS.stat().st_size // 1024, "Ko")

# %%
# À COMPLÉTER : la chaîne d'enveloppes de la section 5.8, dans le bon ordre.
# L'empilement de trames est le DERNIER maillon. Si vous le placez ailleurs, votre
# agent obtiendra -21 à tous les épisodes avec des poids réputés bons.
env = ...

# À COMPLÉTER : le réseau DQN de la section 5.8 (convolutions + tete).
class DQN(nn.Module):
    ...

# %%
reseau = DQN(env.observation_space.shape, env.action_space.n).to(peripherique)
reseau.load_state_dict(torch.load("pong_poids.dat", map_location=peripherique))
reseau.eval()                       # décision 1 : mode évaluation

N_EPISODES = 10
retours = []
for _ in range(N_EPISODES):
    obs, _ = env.reset()
    retour, termine, tronque = 0.0, False, False
    while not (termine or tronque):
        obs_t = torch.as_tensor(obs).unsqueeze(0).to(peripherique)
        with torch.no_grad():                        # décision 2 : aucun gradient
            action = int(reseau(obs_t).argmax(dim=1).item())   # PUREMENT glouton
        obs, recompense, termine, tronque, _ = env.step(action)
        retour += float(recompense)
    retours.append(retour)

print(f"retour moyen sur {N_EPISODES} épisodes : {np.mean(retours):.1f}")

# %% [markdown]
# **Attentes du volet C.**
#
# * Un retour moyen **positif** sur une dizaine d'épisodes, et proche de la borne du
#   jeu si les poids correspondent à un entraînement mené à son terme.
# * **La question que je veux voir traitée en trois lignes** : pourquoi l'évaluation
#   se fait-elle avec \(\varepsilon = 0\), alors que l'entraînement gardait
#   \(\varepsilon = 0{,}01\) ? La semaine 4 vous a donné la réponse, sur la falaise, et
#   je veux la retrouver ici avec les mots **« politique apprise »** et **« politique
#   jouée »**.
# * **La vérification qui attrape le bogue classique du volet** : si votre agent
#   obtient **−21 à tous les épisodes** avec des poids réputés bons, le problème est
#   dans la **chaîne d'enveloppes**, pas dans les poids. Vérifiez dans l'ordre : la
#   forme de l'observation, l'ordre des axes, l'appui sur FIRE, puis la position de
#   l'enveloppe d'empilement, qui doit être la **dernière**.
#
# **Facultatif** : enregistrez une vidéo d'un épisode avec l'enveloppe d'enregistrement
# de Gymnasium et regardez jouer votre agent. Cela prend trois lignes, et c'est le
# moment le plus satisfaisant de la semaine.

# %%
...        # À COMPLÉTER, facultatif : RecordVideo sur un épisode
