# %% [markdown]
# # SCI1070 — Semaine 3 : l'entropie croisée, et où elle casse
#
# Un seul carnet, trois niveaux, un fil unique : **écrire CEM de bout en bout sur
# CartPole, puis le pousser jusqu'à ce qu'il casse**.
#
# | Niveau | Ce que vous y faites |
# | --- | --- |
# | 1 | les cinq étapes de la section 3.3, et les quatre points de contrôle |
# | 2 | percentile, taille de lot, capacité, et le bogue silencieux |
# | 3 | prédire **avant** de lancer, sur votre environnement de la semaine 1 |
#
# Le laboratoire est **formatif**. Le travail évalué de la semaine est le jalon 1,
# qui vient juste après et qui suppose ce carnet terminé.
#
# Budget de calcul : **quelques minutes sur processeur central**. Le processeur
# graphique n'apporte strictement rien ici — les réseaux sont minuscules et le temps
# passe dans la simulation, pas dans le calcul matriciel.

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

from collections import namedtuple

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.nn.functional import softmax

EtapeEpisode = namedtuple("EtapeEpisode", ["observation", "action"])
Episode = namedtuple("Episode", ["retour", "etapes"])

HIDDEN_SIZE = 128
BATCH_SIZE = 16
PERCENTILE = 70

print("gymnasium", gym.__version__, "| torch", torch.__version__)

# %% [markdown]
# ---
# # Niveau 1 : implémentation guidée
#
# **Objectif.** Écrire les cinq étapes de la section 3.3 et résoudre CartPole. À la
# fin de ce niveau, votre agent affiche « Résolu ! » et vous savez dire à quelle
# itération.
#
# **Les quatre points de contrôle** traversent tout le niveau, et chacun se vérifie
# en une ligne :
#
# 1. la sortie du réseau est **linéaire**, sans softmax ;
# 2. `choisir_action` reçoit bien un lot de taille 1 ;
# 3. le seuil est un **percentile des retours du lot**, jamais une constante ;
# 4. l'observation enregistrée est **celle qui a servi à choisir l'action**.

# %% [markdown]
# ### Exercice 3.A — le réseau et l'échantillonnage
#
# Deux trous à combler. Le premier demande deux décisions : combien de sorties, et
# **rien après** ?

# %%
class ReseauPolitique(nn.Module):
    def __init__(self, n_obs: int, n_actions: int, n_cache: int = HIDDEN_SIZE):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            nn.ReLU(),
            ...,          # À COMPLÉTER : la couche de sortie. Combien de sorties, et rien après ?
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pipe(x)


def choisir_action(net, obs):
    obs_v = ...           # À COMPLÉTER : un tenseur float32, et la dimension de lot
    probs = softmax(net(obs_v), dim=1).data.numpy()[0]
    assert abs(probs.sum() - 1.0) < 1e-5, "ceci n'est pas une distribution"
    return int(np.random.choice(len(probs), p=probs))

# %% [markdown]
# ### Exercice 3.B — le générateur de lots
#
# Écrivez `engendrer_lots`. Une seule contrainte, et c'est le **point de contrôle 4** :
# l'observation enregistrée dans `EtapeEpisode` doit être celle qui a servi à choisir
# l'action. L'assertion coûte une ligne et vous épargnera une soirée.

# %%
def engendrer_lots(env, net, taille_lot: int = BATCH_SIZE):
    """Produit indéfiniment des lots de `taille_lot` épisodes complets."""
    lot, etapes = [], []
    obs, _ = env.reset()
    retour = 0.0

    while True:
        action = choisir_action(net, obs)
        next_obs, recompense, termine, tronque, _ = env.step(action)
        retour += float(recompense)

        etapes.append(EtapeEpisode(observation=obs, action=action))
        # Point de contrôle 4 : on enregistre obs, jamais next_obs.
        assert etapes[-1].observation is obs, "on enregistre obs, jamais next_obs"

        ...        # À COMPLÉTER : fermer l'épisode, l'ajouter au lot, rendre le lot plein,
                   # et surtout : faire avancer obs. Attention à l'ordre de ces deux lignes.

# %% [markdown]
# ### Exercice 3.C — le filtre et la boucle
#
# Écrivez `filtrer_elites` puis la boucle d'entraînement. Deux points de contrôle
# s'y vérifient : le seuil est bien un **percentile des retours du lot** et non une
# constante écrite en dur, et la perte reçoit bien des **sorties brutes**.

# %%
def filtrer_elites(lot, percentile: int = PERCENTILE):
    """Rend (observations, actions, seuil, retour_moyen) pour les épisodes retenus."""
    retours = [ep.retour for ep in lot]
    seuil = ...        # À COMPLÉTER : point de contrôle 3, un percentile, pas une constante
    ...                # À COMPLÉTER : ne garder que les épisodes au-dessus du seuil,
                       # et aplatir leurs étapes en deux tenseurs

# %%
env = gym.make("CartPole-v1")
net = ReseauPolitique(env.observation_space.shape[0], env.action_space.n)
objective = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)

# Les deux assertions du point de contrôle 1.
assert isinstance(objective, nn.CrossEntropyLoss)
assert not isinstance(net.pipe[-1], nn.Softmax), "la dernière couche est linéaire"

seuils, retours_moyens, pertes = [], [], []

for iteration, lot in enumerate(engendrer_lots(env, net)):
    obs_v, actions_v, seuil, retour_moyen = filtrer_elites(lot)

    ...        # À COMPLÉTER : les cinq lignes de la mise à jour. Sorties BRUTES dans la perte.

    seuils.append(seuil)
    retours_moyens.append(retour_moyen)
    print(f"{iteration:3d} : retour moyen {retour_moyen:6.1f}, seuil {seuil:6.1f}")

    if retour_moyen > 475:
        print("Résolu !")
        break

# %%
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(retours_moyens, label="retour moyen du lot")
ax.plot(seuils, label="seuil des élites")
ax.set_xlabel("itération"); ax.set_ylabel("retour")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Attentes du niveau 1.**
#
# * Le retour moyen du **premier** lot est de l'ordre de quelques dizaines, ce qui
#   doit vous rappeler la mesure de la semaine 1 : c'est la même politique aléatoire,
#   obtenue cette fois par des poids tirés au hasard.
# * Le seuil des élites **monte** itération après itération. C'est la courbe la plus
#   informative des trois, et c'est elle qui restera désespérément plate sur
#   FrozenLake, au jalon.
# * « Résolu ! » apparaît entre la **trentième et la soixantième** itération, donc
#   entre 480 et 960 épisodes joués. Si vous êtes très au-delà, relisez d'abord le
#   point de contrôle 4.
# * La perte ne descend **pas** régulièrement, et c'est normal : le jeu
#   d'entraînement change à chaque itération, et il devient plus difficile à mesure
#   que les élites se ressemblent. **Une perte qui remonte alors que le retour monte
#   n'est pas un bogue.**

# %% [markdown]
# ---
# # Niveau 2 : hyperparamètres et sensibilité
#
# **Objectif.** Vérifier sur vos propres courbes la robustesse annoncée de la méthode,
# et trouver les deux réglages qui la cassent. Prévoyez quatre à six exécutions
# comparées, et **une phrase de conclusion pour chacune**.
#
# Enfermez d'abord une exécution complète dans une fonction : sans cela, les quatre
# balayages ci-dessous deviennent du copier-coller, et un copier-coller qui diverge
# est exactement ce qui rend un tableau de résultats inexploitable.

# %%
def executer(percentile=PERCENTILE, taille_lot=BATCH_SIZE, n_cache=HIDDEN_SIZE,
             enregistrer_next_obs=False, max_iterations=100, graine=0):
    """Rend (iterations, episodes_joues, courbe_retour, courbe_seuil, taille_jeu_a_10)."""
    ...        # À COMPLÉTER : reprendre le niveau 1, paramétré. Le drapeau
               # `enregistrer_next_obs` sert au point 4 ci-dessous.

# %% [markdown]
# ### 1. Le percentile
#
# Faites varier `PERCENTILE` sur **30, 50, 70, 90** en gardant tout le reste. Relevez
# le nombre d'itérations jusqu'à résolution, et la **taille du jeu d'entraînement à
# l'itération 10**. Expliquez le compromis : un percentile élevé donne des exemples
# meilleurs, mais **combien** ?

# %%
for p in [30, 50, 70, 90]:
    ...        # À COMPLÉTER : une ligne de tableau par percentile

# %% [markdown]
# ### 2. La taille du lot
#
# Faites varier `BATCH_SIZE` sur **4, 16, 64**. Comptez cette fois en **épisodes
# joués**, pas en itérations, sinon la comparaison est trompeuse.

# %%
for b in [4, 16, 64]:
    ...        # À COMPLÉTER : et rapportez des ÉPISODES, pas des itérations

# %% [markdown]
# ### 3. La capacité du réseau
#
# Passez `HIDDEN_SIZE` de 128 à **8**, puis à **512**. La méthode est annoncée robuste
# aux hyperparamètres : dites si vos mesures le confirment, et **où se situe la limite**.

# %%
for h in [8, 128, 512]:
    ...        # À COMPLÉTER

# %% [markdown]
# ### 4. Le bogue silencieux, délibérément
#
# Enregistrez `next_obs` au lieu de `obs`, relancez **à l'identique**, et comparez les
# deux courbes de retour moyen. Décrivez ce que vous voyez en une phrase qui n'emploie
# pas le mot « bogue », mais qui dit **ce que le réseau a appris**.

# %%
...        # À COMPLÉTER : les deux exécutions, et la figure qui les superpose

# %% [markdown]
# **Attentes du niveau 2.**
#
# * À `PERCENTILE = 90`, chaque itération ne retient qu'**un ou deux** épisodes sur
#   seize : la mise à jour devient bruyante et l'entraînement, souvent, **plus lent**
#   plutôt que plus rapide. À 30, les exemples sont médiocres et le seuil monte
#   paresseusement. L'intervalle utile est large, et c'est précisément ce qu'on entend
#   par « robuste aux hyperparamètres ».
# * À `BATCH_SIZE = 4`, le percentile porte sur quatre nombres : le seuil devient très
#   instable d'une itération à l'autre. Vous venez de rencontrer, **sur un cas facile**,
#   le mécanisme exact qui fera échouer FrozenLake.
# * Avec huit neurones cachés, l'agent progresse puis **plafonne** : la capacité du
#   réseau finit par limiter la politique. Avec 512, le temps par itération augmente
#   sans gain notable.
# * Avec `next_obs`, l'entraînement **fonctionne encore**, plus lentement et moins
#   loin. C'est le point important de tout le niveau : un bogue qui empêche tout est
#   facile ; **un bogue qui dégrade est ce qui vous coûtera du temps dans la vraie vie**.

# %% [markdown]
# ---
# # Niveau 3 : prédire avant de lancer
#
# Reprenez l'environnement que vous avez choisi et instrumenté au niveau 3 de la
# semaine 1. **Avant d'y lancer quoi que ce soit**, prédisez par écrit si CEM va y
# fonctionner, en vous appuyant sur les trois limites de la section 3.5. Puis vérifiez.
#
# Votre page de prédiction répond à trois questions :
#
# 1. les épisodes sont-ils **finis et courts** ?
# 2. la récompense arrive-t-elle **en cours d'épisode** ou seulement à la fin ?
# 3. deux épisodes de qualité différente obtiennent-ils des **retours différents** ?

# %% [markdown]
# ### La mesure qui tranche, et elle ne demande aucun entraînement
#
# Jouez 200 épisodes avec une politique aléatoire et tracez l'**histogramme des
# retours**. Un histogramme étalé annonce que la méthode a une chance ; deux barres
# annoncent l'effondrement de la section 3.5.
#
# C'est, dans tout ce cours, le **premier diagnostic à poser sur un environnement
# inconnu**. Il coûte trente secondes et il vous dit à quelle famille de méthodes vous
# avez affaire.

# %% [smoke]
def retours_aleatoires(nom_env: str, episodes: int = 200, graine: int = 0) -> np.ndarray:
    """Les retours de la politique uniforme. Aucun entraînement, aucun réseau."""
    env = gym.make(nom_env)
    retours = []
    for k in range(episodes):
        obs, _ = env.reset(seed=graine + k)
        retour, fini = 0.0, False
        while not fini:
            obs, r, termine, tronque, _ = env.step(env.action_space.sample())
            retour += float(r)
            fini = termine or tronque
        retours.append(retour)
    env.close()
    return np.array(retours)


# Les deux cas d'école, côte à côte : l'un étalé, l'autre à deux barres.
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, nom in zip(axes, ["CartPole-v1", "FrozenLake-v1"]):
    R = retours_aleatoires(nom, episodes=200)
    ax.hist(R, bins=20)
    ax.set_title(f"{nom}\nmoyenne {R.mean():.2f}, {len(np.unique(R))} valeur(s) distincte(s)")
    ax.set_xlabel("retour de l'épisode")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Regardez les deux histogrammes avant de lire la suite.** Sur CartPole, les retours
# s'étalent : deux politiques aléatoires différentes obtiennent des scores différents,
# donc un percentile a quelque chose à classer. Sur FrozenLake, il n'y a que **deux**
# valeurs possibles, 0 et 1, et la quasi-totalité des épisodes vaut 0 — le percentile
# ne départage rien. C'est l'effondrement de la section 3.5, visible en trente secondes
# et sans une ligne d'entraînement.

# %%
# À COMPLÉTER : le même histogramme sur VOTRE environnement de la semaine 1,
# puis l'agent lancé tel quel, sans rien adapter d'autre que l'enveloppe
# d'observation si l'espace est discret.
...

# %% [markdown]
# **Ce que vous livrez au niveau 3.**
#
# * Une **page de prédiction écrite avant** la première exécution, et horodatée dans
#   le carnet.
# * L'histogramme des retours aléatoires de votre environnement.
# * L'agent lancé tel quel, et l'**écart entre votre prédiction et le résultat**,
#   expliqué.
# * Si votre environnement a un espace d'actions **continu**, dites pourquoi la méthode
#   telle que nous l'avons écrite ne s'y applique pas, en une phrase qui parle du
#   **nombre de classes du classifieur**.
#
# > **Mon message pour ce laboratoire.** Vous venez d'écrire, en moins de cent lignes,
# > un agent qui apprend réellement. Savourez-le : c'est la première fois du cours, et
# > la méthode est assez simple pour que vous en teniez chaque ligne dans votre tête.
# > Mais ne confondez pas « ça marche » avec « j'ai compris ». La compréhension, cette
# > semaine, se mesure à votre capacité d'annoncer **à l'avance** sur quel
# > environnement ce même code va échouer. C'est très exactement ce que le jalon vous
# > demande.
