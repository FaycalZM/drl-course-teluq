# %% [markdown]
# # SCI1070 — Semaine 10 : PPO, ses trois boutons, et le compromis mesuré
#
# | Volet | Ce que vous y faites |
# | --- | --- |
# | A | PPO écrit de bout en bout sur `Pendulum-v1` |
# | B | régler \(\epsilon\), \(\lambda\) et les époques, avec graines et intervalles |
# | C | une méthode hors politique sur la **même** tâche, et le compromis en deux figures |
#
# Formatif. Ce qui est noté cette semaine, c'est le **jalon 3**, qui vient juste après
# et qui réutilise votre code du volet A. **Faites donc le laboratoire d'abord, sans
# exception** : le jalon suppose que PPO tourne déjà chez vous.
#
# **La tâche est `Pendulum-v1`, et c'est celle de la semaine 9.** Un épisode y dure
# quelques secondes, l'espace d'actions a **une seule dimension**, et aucun moteur
# physique externe n'est à installer. Les chiffres du tableau 10-1 portent sur des
# exécutions de huit à vingt heures chacune. Ce sont des **repères à décrire**, jamais
# des tâches à donner.
#
# **Les récompenses de cette tâche sont négatives : votre courbe monte vers zéro**, et
# une valeur prédite positive est un bogue de signe, pas un apprentissage optimiste.
#
# > **Quatre pièges, et chacun coûte une soirée.**
# >
# > 1. **Le détachement de l'ancienne log-probabilité.** Si `anciennes_logprob` n'est
# >    pas détachée à la collecte, votre rapport a un gradient dans son dénominateur
# >    et vous n'optimisez pas ce que vous avez écrit.
# > 2. **Le décalage d'un élément.** Les avantages sont plus courts d'une transition
# >    que la trajectoire, et une erreur d'indexation ici **ne lève aucune exception**.
# > 3. **L'échelle de l'action.** Multipliez par la demi-étendue, une fois, au bon
# >    endroit.
# > 4. **L'évaluation avec tirage.** Un score mesuré en tirant dans la politique
# >    n'est pas le score de votre politique. L'évaluation se fait **sur la moyenne**.

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

import time

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
print("périphérique :", device)

# %% [markdown]
# ---
# # Volet A : PPO de bout en bout
#
# **Étape 1 — les deux réseaux.** Gardez-les **séparés**, avec **deux optimiseurs** :
# c'est ce qui vous permettra d'avoir deux pas d'apprentissage, et le jalon vous le
# demandera. Gardez aussi l'écart-type **global**, un simple `nn.Parameter`, pour ce
# volet : le volet C introduira la version fonction de l'état.

# %%
class ActeurGaussien(nn.Module):
    def __init__(self, n_obs, n_actions, demi_etendue):
        super().__init__()
        ...        # À COMPLÉTER : la moyenne par un réseau, l'écart-type par un
                   # nn.Parameter GLOBAL (log_std), et la demi-étendue au bon endroit

    def forward(self, obs):
        ...        # À COMPLÉTER : rend (moyenne, ecart_type)

    def distribution(self, obs):
        moyenne, ecart_type = self(obs)
        return torch.distributions.Normal(moyenne, ecart_type)


class Critique(nn.Module):
    def __init__(self, n_obs):
        super().__init__()
        ...        # À COMPLÉTER

    def forward(self, obs):
        ...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — la collecte.** Quelques centaines à deux mille transitions suffisent.
# **Mémorisez la log-densité de chaque action au moment où vous la jouez, et
# détachez-la.** C'est la seule donnée supplémentaire que PPO demande par rapport à la
# semaine 8, et **tout en dépend**.

# %%
def collecter(env, acteur, n_transitions):
    """Rend (obs, actions, recompenses, termines, anciennes_logprob)."""
    ...        # À COMPLÉTER. Piège nº1 : .detach() sur les log-probabilités, ICI.

# %% [markdown]
# **Étape 3 — l'avantage généralisé**, en une passe arrière, puis la normalisation :
# moyenne retirée, division par l'écart-type.

# %%
def avantage_generalise(recompenses, valeurs, termines, gamma=0.99, lam=0.95):
    """Une passe arrière. Le tableau rendu est PLUS COURT d'un élément (piège nº2)."""
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 4 — la boucle d'époques et de minilots**, avec la perte écrêtée. Partez de
# \(\epsilon = 0{,}2\), \(\lambda = 0{,}95\) et **dix** époques : ce sont les réglages
# de référence, et le volet B les fera varier.

# %%
def ppo(graine, eps=0.2, lam=0.95, epoques=10, n_transitions=2048,
        max_pas=200_000, gamma=0.99):
    """Rend (observations, courbe_evaluation, diagnostic)."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : la boucle en treize étapes de la section 10.2.
               # `diagnostic` porte, par époque, la moyenne de ln r_t et la fraction
               # d'échantillons écrêtés.

# %% [markdown]
# ### Les trois vérifications arithmétiques, avant d'interpréter la moindre courbe
#
# **La première est la plus rentable du cours.** Au tout premier minilot de la
# première époque, le rapport doit valoir **exactement 1** pour tous les échantillons,
# à la précision machine près, puisque la politique n'a pas encore bougé. Si ce n'est
# pas le cas, vous avez un bogue dans la mémorisation de l'ancienne log-densité, et
# **vous le trouverez en trente secondes plutôt qu'en trois heures**.

# %% [smoke]
# La forme que doit avoir cette vérification, sur un cas fabriqué.
anciennes_logprob = torch.tensor([-1.2, -0.7, -2.1])
nouvelles_logprob = anciennes_logprob.clone()          # la politique n'a pas bougé
ratio = torch.exp(nouvelles_logprob - anciennes_logprob)
print("rapport au premier minilot :", ratio)
assert torch.allclose(ratio, torch.ones_like(ratio)), "bogue dans l'ancienne log-densité"

# La deuxième : avantages normalisés, moyenne nulle et écart-type un.
a = torch.randn(512) * 3.7 + 1.4
a_norm = (a - a.mean()) / (a.std() + 1e-8)
print(f"après normalisation : moyenne {a_norm.mean():.2e}, écart-type {a_norm.std():.4f}")
assert abs(float(a_norm.mean())) < 1e-5 and abs(float(a_norm.std()) - 1) < 1e-3

# %%
# 3. La longueur du tableau d'avantages vaut exactement la longueur de la trajectoire
#    moins un. Vérifiez-le sur VOTRE fonction.
...        # À COMPLÉTER

# %% [markdown]
# ### Le diagnostic de la semaine, et il est à produire ici
#
# Journalisez, pour chaque époque, **deux** quantités : la moyenne de
# \(\ln r_t(\theta)\) sur le minilot, qui estime la divergence entre la politique
# courante et celle de la collecte, et la **fraction des échantillons écrêtés**.
#
# C'est votre **seul** diagnostic honnête : la perte de PPO ne vous dit rien sur la
# santé de votre entraînement, puisqu'elle est l'opposé d'un objectif que l'écrêtage
# aplatit volontairement.

# %%
observations, courbe_pilote, diagnostic = ppo(graine=0)
print("cible annoncée à partir de l'exécution pilote :", max(courbe_pilote))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
...        # À COMPLÉTER : ln r_t à gauche, fraction écrêtée à droite, par époque
for ax in axes:
    ax.set_xlabel("numéro d'époque"); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# %%
courbes = [ppo(graine=g)[1] for g in GRAINES]

fig, ax = plt.subplots(figsize=(8, 4.5))
tracer_bande(ax, np.arange(len(courbes[0])), courbes, etiquette="PPO, référence")
ax.set_xlabel("évaluation"); ax.set_ylabel("retour, sans tirage, dix épisodes")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Attendu du volet A.** La courbe d'évaluation sur au moins trois graines avec
# intervalle, votre cible annoncée, et la figure du diagnostic avec **une phrase de
# lecture** : à partir de quelle époque votre dixième époque ne sert-elle plus à rien ?

# %% [markdown]
# ---
# # Volet B : régler les trois boutons
#
# **Un seul programme, trois drapeaux**, et rien d'autre ne change entre deux
# exécutions. C'est l'étude à une variable des semaines 6 et 7, appliquée une
# troisième fois, et c'est **la condition pour que vos écarts veuillent dire quelque
# chose**.

# %%
CONFIGURATIONS = {
    "Référence":                dict(eps=0.2, lam=0.95, epoques=10),
    "Bande étroite":            dict(eps=0.1, lam=0.95, epoques=10),
    "Bande large":              dict(eps=0.4, lam=0.95, epoques=10),
    "Avantage à un pas":        dict(eps=0.2, lam=0.0,  epoques=10),
    "Avantage de la semaine 8": dict(eps=0.2, lam=1.0,  epoques=10),
    "Une seule époque":         dict(eps=0.2, lam=0.95, epoques=1),
    "Vingt époques":            dict(eps=0.2, lam=0.95, epoques=20),
}

resultats = {}
for nom, options in CONFIGURATIONS.items():
    scores = [...]        # À COMPLÉTER : un score final par graine, LES MÊMES graines
    resultats[nom] = scores
    moyenne, bas, haut = intervalle(scores)
    print(f"{nom:26s} {moyenne:8.1f}   [{bas:.1f}, {haut:.1f}]   n={len(scores)}")

# %%
ref = resultats["Référence"]
for nom in list(CONFIGURATIONS)[1:]:
    recouvre = se_recouvrent(ref, resultats[nom])
    verdict = "je ne mesure pas de différence" if recouvre else "séparé de la référence"
    print(f"{nom:26s} {verdict}")

# %% [markdown]
# **Les quatre questions auxquelles votre rapport répond.**
#
# 1. La **bande étroite** ralentit-elle l'apprentissage chez vous, et de combien ?
# 2. La **bande large** provoque-t-elle une instabilité visible, et **à quel moment** ?
# 3. Que se passe-t-il à \(\lambda = 1\), et le résultat est-il cohérent avec
#    l'affirmation de la section 10.2 selon laquelle vous retrouvez alors l'avantage
#    de la semaine 8 ?
# 4. La plus intéressante : **au-delà de combien d'époques votre score cesse-t-il de
#    s'améliorer**, et ce seuil correspond-il à ce que votre diagnostic du volet A
#    annonçait ?
#
# **Attendu.** Le tableau des sept configurations avec graines et intervalles, vos
# quatre réponses, et une phrase disant **lequel des trois boutons a eu le plus
# d'effet** sur votre tâche.

# %% [markdown]
# ---
# # Volet C : une méthode hors politique sur la même tâche
#
# **Objectif.** Reproduire, à l'échelle d'un carnet, la **forme** de l'argument de la
# section 10.6 : **moins d'observations, plus de calcul**.
#
# **Deux routes honnêtes, et je ne tranche pas pour vous.** La route courte reprend
# votre code de la semaine 9 et y ajoute les deux changements de la section 10.5 : le
# terme d'entropie dans la cible et dans l'objectif de l'acteur, et un écart-type
# **fonction de l'état** avec la correction de jacobien de la tangente hyperbolique.
# La route encore plus courte prend l'implémentation de la bibliothèque haut niveau et
# concentre votre travail sur la mesure. **La seconde est parfaitement acceptable, à
# une condition : dites-le.**

# %%
# La solution courte, pour verifier votre implementation et pour le volet C.
# A executer APRES avoir ecrit la votre, jamais avant.
import time

from stable_baselines3 import PPO, SAC

RESULTATS = {}

for nom, Classe, pas in [("sur politique", PPO, 60_000),
                         ("hors politique", SAC, 20_000)]:
    debut = time.perf_counter()
    modele = Classe("MlpPolicy", "Pendulum-v1", seed=0, verbose=0)
    modele.learn(total_timesteps=pas)
    RESULTATS[nom] = (pas, time.perf_counter() - debut)
    # Puis evaluer SANS tirage, sur plusieurs graines, et tracer les DEUX axes :
    # retour contre observations, et retour contre temps d'horloge.

for nom, (pas, duree) in RESULTATS.items():
    print(f"{nom:>16} : {pas} observations en {duree:.0f} s")

# %% [markdown]
# > **Les deux budgets de pas ci-dessus ne sont pas des cibles, et le rapport entre
# > eux n'est pas une prédiction.** Je les donne pour que le fragment tourne, et je
# > m'attends à ce que vous les changiez. Le point du volet est précisément de
# > **mesurer** combien d'observations chaque méthode demande chez vous. Si vous
# > trouvez qu'il en faut autant aux deux, c'est un résultat : votre tâche est
# > peut-être trop petite pour que l'efficacité d'échantillon se voie, et le dire est
# > une meilleure conclusion qu'un chiffre arrangé.

# %% [markdown]
# ### Étape 2 — les deux mesures, dans **deux figures différentes**
#
# Ce sont les deux axes de la Figure 10-4, et vous allez voir qu'ils **ne racontent
# pas la même histoire**.

# %%
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
...        # À COMPLÉTER
           # gauche  : retour en fonction des OBSERVATIONS consommées
           # droite  : retour en fonction du TEMPS D'HORLOGE, même matériel
axes[0].set_xlabel("observations consommées")
axes[1].set_xlabel("temps d'horloge (s)")
axes[0].set_ylabel("retour, sans tirage")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### Étape 4 — la vérification d'honnêteté
#
# Indiquez votre matériel, et indiquez **combien de mises à jour de réseau chaque
# méthode effectue par observation collectée**. Ce rapport est l'explication mécanique
# de tout ce que vos deux figures montrent, et **il tient en un nombre**.

# %%
...        # À COMPLÉTER : le nombre de mises à jour par observation, pour les deux

# %% [markdown]
# **Les trois questions de l'étape 3.** Laquelle des deux atteint votre cible avec le
# **moins d'observations** ? Laquelle l'atteint en **le moins de temps** ? Et la
# question qui ferme le module : sur **votre** matériel et pour **votre** tâche,
# laquelle choisiriez-vous, et **qu'est-ce qui est rare chez vous** ?
#
# **Attendu.** Les deux figures, sur au moins trois graines, vos trois réponses, votre
# matériel, et le nombre de mises à jour par observation pour chacune des deux.
#
# > **Mon message pour ce laboratoire.** Faites les volets dans l'ordre, et résistez à
# > la tentation de sauter au volet C, qui est le plus spectaculaire. La perte de PPO
# > ne vous dit **rien** sur la santé de votre entraînement, puisqu'elle est l'opposé
# > d'un objectif que l'écrêtage aplatit volontairement. Votre seul diagnostic honnête
# > est le couple que le volet A demande de tracer. Le volet B n'est interprétable
# > qu'avec ce diagnostic sous les yeux, parce qu'il explique pourquoi une époque
# > supplémentaire cesse d'apporter quoi que ce soit. Et le volet C n'est
# > interprétable qu'après le volet B, parce qu'**une comparaison entre deux méthodes
# > dont l'une est mal réglée ne mesure que le réglage**.
