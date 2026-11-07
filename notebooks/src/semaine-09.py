# %% [markdown]
# # SCI1070 — Semaine 9 : politique déterministe, et la surestimation mesurée
#
# | Volet | Ce que vous y faites |
# | --- | --- |
# | A | la boucle en neuf étapes de la section 9.3, sur `Pendulum-v1` |
# | B | **la surestimation, mesurée par vous** : le nombre que la section 9.5 n'a pas donné |
# | C | l'ablation des trois correctifs, et les deux bruits d'exploration |
# | Démo | un robot simulé, rendu hors écran, exporté en vidéo |
#
# Les trois volets partagent **un seul programme**. Formatif : rien n'y est noté, et
# le prochain jalon est en semaine 10.
#
# **La tâche de mesure est `Pendulum-v1`, nommée avec son identifiant exact.** Contrôle
# classique, sans moteur physique externe, **une seule dimension d'action**, un couple
# dans \([-2,2]\), un épisode de quelques secondes. Le pendule inversé de MuJoCo,
# `InvertedPendulum-v5`, serait un mauvais choix : il **sature**, et une ablation
# menée dessus ne mesurerait rien.
#
# **Je ne vous donne aucun score à atteindre, et c'est volontaire.** Tous les nombres
# cités cette semaine portent sur d'autres tâches. Interpoler entre eux pour vous
# donner une cible rassurante serait inventer un chiffre. Commencez par une
# **exécution pilote** d'une seule graine pour fixer votre propre cible, et
# annoncez-la dans votre rapport.
#
# > **Trois pièges, et ils coûtent chacun une soirée.**
# >
# > 1. **Les deux optimiseurs.** La rétropropagation de la perte de l'acteur traverse
# >    le critique et y dépose des gradients. Sans remise à zéro explicite, votre
# >    critique apprend à **maximiser sa propre sortie**.
# > 2. **L'évaluation avec bruit.** Si vous mesurez avec le bruit d'exploration
# >    activé, vous mesurez votre réglage de bruit autant que votre politique.
# > 3. **L'échelle de l'action.** `Pendulum-v1` attend un couple dans \([-2,2]\) et
# >    votre acteur sort une tangente hyperbolique dans \([-1,1]\). Multipliez par la
# >    demi-étendue **une fois, au bon endroit**, ou votre agent n'aura jamais accès
# >    qu'à la moitié de son autorité et vous chercherez le bogue dans votre perte.

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

# La tâche, nommée exactement. Et sa demi-étendue, qui est le piège nº3.
env_mesure = gym.make("Pendulum-v1")
DEMI_ETENDUE = float(env_mesure.action_space.high[0])
print("Pendulum-v1 | action dans "
      f"[{env_mesure.action_space.low[0]}, {env_mesure.action_space.high[0]}]"
      f" | demi-étendue = {DEMI_ETENDUE}")
env_mesure.close()

# %% [markdown]
# ---
# # Volet A : la boucle déterministe
#
# **Étape 1 — les deux réseaux.** Gardez les tailles **400 et 300** : elles sont
# petites et ce n'est pas là que votre temps se joue.

# %%
class Acteur(nn.Module):
    """De l'observation vers UNE action, déterministe. Tanh en sortie."""

    def __init__(self, n_obs, n_actions, demi_etendue):
        super().__init__()
        ...        # À COMPLÉTER : 400, 300, puis tanh.
                   # Piège nº3 : où multipliez-vous par la demi-étendue ? UNE seule fois.

    def forward(self, obs):
        ...        # À COMPLÉTER


class Critique(nn.Module):
    """Deux entrées : l'observation ET l'action. Une sortie scalaire."""

    def __init__(self, n_obs, n_actions):
        super().__init__()
        ...        # À COMPLÉTER : l'action entre dans le réseau, elle n'est pas un indice

    def forward(self, obs, action):
        ...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — le tampon de rejeu.** Vous l'avez écrit en semaine 5. La **seule**
# différence est que le champ `action` est désormais un vecteur de flottants et non un
# entier, donc un tableau de forme `(capacite, n_actions)` et non `(capacite,)`.

# %%
class TamponContinu:
    ...        # À COMPLÉTER : le tampon de la semaine 5, avec actions continues

# %% [markdown]
# **Étape 3 — le bruit d'exploration.** Gaussien **non corrélé**, d'amplitude
# constante exprimée en fraction de la demi-étendue. Ajoutez une phase de **démarrage
# uniforme** : pendant les premiers pas, ignorez l'acteur et appelez
# `env.action_space.sample()`.
#
# Journalisez l'écart quadratique moyen entre l'action envoyée et l'action proposée :
# c'est votre **amplitude effective après écrêtage**, et elle n'est pas celle que vous
# avez réglée.

# %%
def agir_avec_bruit(acteur, obs, env, sigma_fraction=0.1):
    """Rend (action_envoyee, action_proposee). L'écart des deux est l'amplitude effective."""
    ...        # À COMPLÉTER


def agir_sans_bruit(acteur, obs, env, device):
    """L'évaluation se fait TOUJOURS par cette fonction. Piège nº2."""
    with torch.no_grad():
        obs_t = torch.as_tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
        return acteur(obs_t).cpu().numpy()[0]

# %% [markdown]
# **Étape 4 — les deux pas d'optimisation**, chacun avec son optimiseur, puis la
# synchronisation douce. **Vérifiez par une assertion, une fois**, que les gradients
# du critique sont bien nuls au moment où vous appelez son optimiseur. C'est le
# piège nº1, et il ne lève aucune exception.

# %%
def pas_optimisation(lot, acteur, critique, acteur_cible, critique_cible,
                     opt_acteur, opt_critique, gamma=0.99, tau=0.005,
                     double_q_ecrete=False, delai_politique=False, lissage_cible=False,
                     iteration=0):
    ...        # À COMPLÉTER : les deux pertes, les deux optimiseurs, la synchro douce.
               # Les trois derniers indicateurs sont les interrupteurs du volet C :
               # écrivez-les MAINTENANT, pas plus tard.

# %% [markdown]
# ### Les quatre vérifications arithmétiques, avant d'interpréter la moindre courbe

# %% [smoke]
# 1. L'action envoyée doit TOUJOURS être dans [-2, 2].
env = gym.make("Pendulum-v1")
basse, haute = env.action_space.low, env.action_space.high
action_test = np.array([1.7], dtype=np.float32)
assert np.all(action_test >= basse) and np.all(action_test <= haute)

# 4. La cible et la prédiction doivent avoir EXACTEMENT la même forme.
#    Une diffusion entre (100, 1) et (100,) ne lève aucune exception et calcule une
#    erreur quadratique entre 10 000 paires au lieu de 100. Voici la preuve :
cible = torch.zeros(100, 1)
prediction = torch.zeros(100)
print("forme de (cible - prediction) :", (cible - prediction).shape, " <- le piège")
assert (cible - prediction).shape == (100, 100)
print("d'où la règle : squeeze(-1) sur la sortie du critique, une fois pour toutes")
env.close()

# %% [markdown]
# **2. Le signe.** La valeur prédite par le critique doit avoir le même signe que les
# retours que vous observez. Sur cette tâche les récompenses sont **négatives**, donc
# une valeur prédite positive est un bogue de signe, pas un apprentissage optimiste.
#
# **3. Le début.** Au tout début de l'entraînement, la valeur prédite doit être proche
# de zéro, puisque les poids sont initialisés petits.

# %%
...        # À COMPLÉTER : vérifiez 2 et 3 sur votre propre critique

# %% [markdown]
# **Étape 5 — l'évaluation, sans bruit, sur dix épisodes**, tous les quelques milliers
# de pas.

# %%
def entrainer(graine, max_pas=60_000, double_q_ecrete=False, delai_politique=False,
              lissage_cible=False, sigma_fraction=0.1, bruit_correle=False):
    """Rend (pas, courbe_evaluation, journal). UN programme, trois interrupteurs."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : la boucle en neuf étapes de la section 9.3


# Commencez par UNE graine, pour fixer votre propre cible, et annoncez-la.
pas_pilote, courbe_pilote, _ = entrainer(graine=0)
print("cible annoncée à partir de l'exécution pilote :", max(courbe_pilote))

# %%
courbes = [entrainer(graine=g)[1] for g in GRAINES]

fig, ax = plt.subplots(figsize=(8, 4.5))
tracer_bande(ax, np.arange(len(courbes[0])), courbes, etiquette="base")
ax.set_xlabel("évaluation"); ax.set_ylabel("retour, sans bruit, dix épisodes")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Attendu du volet A.** La courbe d'évaluation sur au moins trois graines avec
# intervalle, **votre amplitude de bruit effective**, et votre cible annoncée à partir
# de l'exécution pilote.

# %% [markdown]
# ---
# # Volet B : la surestimation, mesurée par vous
#
# **Objectif.** Produire **une** figure à deux courbes : la valeur moyenne estimée par
# le critique, et le retour actualisé **réellement obtenu**, sur la même abscisse.
# L'écart entre les deux **est** la surestimation, et c'est le nombre que la section
# 9.5 ne vous a pas donné.
#
# **Étape 1.** Après la phase de démarrage uniforme, tirez un ensemble d'états dans le
# tampon et **figez-le**. Quelques centaines suffisent ; conservez-les, et ne les
# retirez jamais.

# %%
def figer_etats_temoins(tampon, n=300, graine=0):
    """Tirés une fois, conservés pour toute l'exécution. Jamais retirés."""
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 2.** À chaque évaluation, calculez la valeur moyenne que le critique
# attribue à ces états (l'action étant celle que l'acteur propose), puis le retour
# actualisé moyen **réellement collecté** depuis ces mêmes états en suivant la
# politique **sans bruit**.
#
# > **Une mise en garde sur le coût.** Le retour réellement collecté demande de
# > **jouer** des épisodes. Ne mesurez pas sur mille épisodes comme le protocole de la
# > section 9.5 : mesurez sur une dizaine, et **dites dans votre rapport que votre
# > moyenne porte sur dix épisodes**. Une mesure bruitée et annoncée comme telle vaut
# > infiniment mieux qu'une mesure propre et non reproductible.

# %%
@torch.no_grad()
def valeur_estimee(critique, acteur, etats_temoins) -> float:
    ...        # À COMPLÉTER


def retour_reel(acteur, env, etats_temoins, gamma=0.99, episodes=10) -> float:
    ...        # À COMPLÉTER : jouer SANS bruit, et actualiser

# %% [markdown]
# **Étape 4, et c'est elle qui transforme ce volet en expérience.** Refaites la mesure
# avec le **double Q écrêté** activé, toutes choses égales d'ailleurs, **sur les mêmes
# graines**. Comparez l'écart entre les deux courbes dans les deux configurations.

# %%
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
for ax, ecrete in zip(axes, [False, True]):
    ...        # À COMPLÉTER : les deux courbes, estimée et réelle, sur les mêmes graines
    ax.set_title("avec double Q écrêté" if ecrete else "sans")
    ax.set_xlabel("évaluation"); ax.grid(alpha=0.3); ax.legend()
axes[0].set_ylabel("valeur")
plt.show()

# %% [markdown]
# **Répondez par écrit à trois questions.** La surestimation apparaît-elle sur votre
# tâche ? À quel moment de l'entraînement apparaît-elle ? Et son signe est-il
# **stable**, ou votre critique sous-estime-t-il parfois ?
#
# **Attendu.** La figure à deux courbes, dans les deux configurations, sur au moins
# trois graines, et votre réponse écrite aux trois questions.

# %% [markdown]
# ---
# # Volet C : l'ablation des trois correctifs
#
# **Objectif.** Reproduire la **forme** du Tableau 9-2 sur votre tâche : pas ses
# nombres, qui portent sur d'autres environnements, mais le motif de ce qui aide, de
# ce qui n'aide pas, et de **ce qui nuit**.
#
# **Étape 1, la plus importante : un seul programme, trois interrupteurs.** Rien
# d'autre ne doit changer entre deux exécutions.

# %%
CONFIGURATIONS = {
    "Base":                dict(double_q_ecrete=False, delai_politique=False, lissage_cible=False),
    "Base + correctif 1":  dict(double_q_ecrete=True,  delai_politique=False, lissage_cible=False),
    "Base + correctif 2":  dict(double_q_ecrete=False, delai_politique=True,  lissage_cible=False),
    "Base + correctif 3":  dict(double_q_ecrete=False, delai_politique=False, lissage_cible=True),
    "Les trois":           dict(double_q_ecrete=True,  delai_politique=True,  lissage_cible=True),
}

# Si votre budget le permet, ajoutez les trois « les trois, moins un » : c'est là que
# le Tableau 9-2 réserve sa surprise.

resultats = {}
for nom, options in CONFIGURATIONS.items():
    scores = [...]        # À COMPLÉTER : un score final par graine, évaluation SANS bruit
    resultats[nom] = scores
    moyenne, bas, haut = intervalle(scores)
    print(f"{nom:22s} {moyenne:8.1f}   [{bas:.1f}, {haut:.1f}]   n={len(scores)}")

# %%
# La règle d'interprétation : si les intervalles se recouvrent, votre conclusion est
# « je ne mesure pas de différence ». C'est une conclusion parfaitement acceptable,
# et je la préfère de loin à un classement inventé sur une seule exécution.
base = resultats["Base"]
for nom in list(CONFIGURATIONS)[1:]:
    print(f"{nom:22s} se recouvre avec Base : {se_recouvrent(base, resultats[nom])}")

# %% [markdown]
# **Étape 4, la lecture.** Pour chacun des trois correctifs : sur ma tâche, ce
# correctif aide-t-il, ne change-t-il rien, ou **nuit-il** ?
#
# Et surtout : votre tâche à **une** dimension d'action souffre-t-elle du défaut de la
# section 9.5 ? **Si votre volet B montre peu de surestimation, vous devez vous
# attendre à ce que le correctif 1 n'apporte rien, et l'observer serait une
# confirmation, pas un échec.**
#
# Dites aussi, en une phrase, ce que trois graines vous autorisent à conclure **de
# moins** que dix.

# %% [markdown]
# ### Étape 5 — la comparaison des deux bruits, en une ligne
#
# La bibliothèque haut niveau fournit les deux bruits de la section 9.4 comme deux
# objets **interchangeables**. Lancez la même méthode avec l'un puis l'autre, mêmes
# graines, et mesurez.
#
# **Si vous ne trouvez aucune différence, vous venez de retrouver par vous-même ce que
# les trois constats de la section 9.4 annonçaient, et c'est le meilleur résultat
# possible pour cet exercice.**

# %%
# La solution courte, pour verifier votre implementation et comparer les bruits.
# A executer APRES avoir ecrit la votre, jamais avant.
import numpy as np
from stable_baselines3 import TD3
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

n_actions = 1
sigma = 0.1 * np.ones(n_actions)

bruit_simple = NormalActionNoise(mean=np.zeros(n_actions), sigma=sigma)
bruit_correle = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=sigma)

for nom, bruit in [("non correle", bruit_simple), ("correle", bruit_correle)]:
    modele = TD3("MlpPolicy", "Pendulum-v1", action_noise=bruit, seed=0, verbose=0)
    modele.learn(total_timesteps=30_000)
    # Puis evaluer SANS bruit, sur plusieurs graines, et comparer.

# %% [markdown]
# **Attendu du volet C.** Le tableau de vos cinq configurations avec graines et
# intervalles, votre lecture des trois correctifs, et le résultat de la comparaison
# des deux bruits.

# %% [markdown]
# ---
# # Démonstration : un robot, en vidéo, sans écran
#
# Cette partie n'est **pas** mesurée, et c'est assumé. Elle est là parce que voir un
# corps simulé apprendre à se déplacer vaut le détour, et parce que vous devez savoir
# produire une vidéo depuis un carnet **sans affichage**.
#
# Vous reconnaissez la mécanique des enveloppes de la semaine 1, appliquée à la
# **sortie** plutôt qu'à l'entrée.

# %%
# Le simulateur s'installe comme une roue Python. Comptez quelques minutes.
if importlib.util.find_spec("mujoco") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "gymnasium[mujoco]"], check=True)

# %%
import gymnasium as gym

# Verifiez l'identifiant exact dans VOTRE installation : les suffixes de version
# des environnements MuJoCo changent d'une version de Gymnasium a l'autre, et
# gymnasium.pprint_registry() en donne la liste.
ID_ROBOT = "Hopper-v5"

# Rendu hors ecran : les images sont renvoyees en memoire, jamais affichees.
env = gym.make(ID_ROBOT, render_mode="rgb_array")
env = gym.wrappers.RecordVideo(env, video_folder="videos", name_prefix="demo")

obs, _ = env.reset(seed=0)
termine = tronque = False
while not (termine or tronque):
    action = agir_sans_bruit(acteur, obs, env, device)
    obs, _, termine, tronque, _ = env.step(action)
env.close()        # INDISPENSABLE : c'est close() qui finalise le fichier video.

# %% [markdown]
# **Attendu.** Une vidéo, et **deux phrases**. La première décrit ce que votre agent
# fait de travers, la seconde dit ce que vous changeriez pour le corriger.
#
# Le robot qui tombe vers l'avant au bout de onze secondes est un comportement
# **appris** et non un échec : c'est une démarche, instable, et la décrire est un
# exercice d'observation que ce cours n'a pas encore demandé.
#
# > **Mon message pour ce laboratoire.** Faites les volets **dans l'ordre**, même si
# > le volet C est le plus intéressant. Vous n'avez, dans cette famille de méthodes,
# > **aucune** perte dont la valeur vous dise si les choses se passent bien : la perte
# > du critique peut descendre pendant que l'agent se dégrade, et la perte de l'acteur
# > n'est que l'opposé d'une note qu'il s'attribue à lui-même. Le volet A vous donne
# > des repères, le volet B vous donne le seul diagnostic honnête que cette semaine
# > connaisse, et **le volet C ne devient interprétable qu'après le volet B** : savoir
# > si votre tâche souffre de surestimation est ce qui vous permettra de dire si le
# > premier correctif devait aider. Sans ce préalable, le volet C produit un tableau
# > de nombres et aucune conclusion.
