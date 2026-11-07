# %% [markdown]
# # SCI1070 — Semaine 13 : quatre mécanismes, isolés et mesurés
#
# | Volet | Ce que vous y faites | Durée |
# | --- | --- | --- |
# | A | les trois estimateurs de retour, **comme fonctions pures** | dix minutes |
# | B | la semaine 3, sur une dynamique **analytique** | quelques minutes |
# | C | un gradient qui traverse **deux couches de dynamique** | vingt lignes |
# | D | **une politique qui désapprend**, puis qui cesse de désapprendre | le plus important |
#
# **Rien de ce que cette semaine décrit n'est reproductible, et je ne vais pas faire
# semblant.** Dix à vingt heures de calcul par tâche pour la première moitié, quinze
# heures par tâche et par graine pour la section 13.11, cinq millions de pas
# d'environnement. C'est hors d'atteinte d'une session gratuite, et de très loin.
#
# Le laboratoire fait donc le choix opposé : il **isole quatre mécanismes** et les
# mesure séparément, chacun en quelques minutes. Pour chacun, je vous dis **ce que la
# mesure établit et ce qu'elle n'établit pas**.
#
# > **Aucun des quatre volets n'a été exécuté par ce cours**, et vous devez le savoir
# > avant de commencer. Les sections établissent que chaque construction est correcte
# > et soutenue ; elles n'établissent pas qu'une courbe précise sortira de votre
# > session. Les volets sont écrits comme des **consignes**, jamais comme des
# > résultats attendus. **Si votre résultat diffère, la bonne réaction n'est pas de
# > régler jusqu'à ce qu'il ressemble à une attente : c'est de dire ce que vous avez
# > obtenu et d'expliquer ce que cela mesure.**

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

from sci1070.protocole import intervalle
from sci1070.courbes import tracer_bande
from sci1070.graines import fixer_graines

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
GRAINES = [0, 1, 2]
GAMMA = 0.99

# %% [markdown]
# ---
# # Volet A : les trois estimateurs, comme fonctions pures
#
# **Objectif.** Écrire les trois estimateurs de la section 13.10 et **voir** ce que
# leurs équations disent, sans modèle, sans environnement et sans entraînement. Il
# coûte dix minutes et il rend les trois équations **définitivement** claires.

# %%
def V_R(recompenses, valeurs, gamma=GAMMA):
    """L'estimateur sans amorçage. Ne doit JAMAIS lire `valeurs`."""
    ...        # À COMPLÉTER


def V_N(recompenses, valeurs, n, gamma=GAMMA):
    """L'estimateur à n pas."""
    ...        # À COMPLÉTER


def V_lambda(recompenses, valeurs, lam, gamma=GAMMA):
    """La moyenne pondérée. Une récurrence, et elle se décale facilement d'un indice."""
    ...        # À COMPLÉTER

# %% [markdown]
# ### Les trois identités, et elles attrapent la totalité des bogues possibles

# %%
rng = np.random.default_rng(0)
r = torch.as_tensor(rng.normal(size=40), dtype=torch.float32)
v = torch.as_tensor(rng.normal(size=40), dtype=torch.float32)

# 1. V_N avec n = 1 doit valoir la cible à un pas de la semaine 5, en chaque position.
cible_un_pas = r[:-1] + GAMMA * v[1:]
assert torch.allclose(V_N(r, v, n=1)[:-1], cible_un_pas, atol=1e-5)

# 2. V_lambda(0) = V_N(1), et V_lambda(1) = V_N(H).
#    Si l'un des deux cas limites est faux, votre récurrence est décalée d'un indice.
assert torch.allclose(V_lambda(r, v, lam=0.0), V_N(r, v, n=1), atol=1e-5)
assert torch.allclose(V_lambda(r, v, lam=1.0), V_N(r, v, n=len(r)), atol=1e-5)

# 3. V_R ne doit JAMAIS dépendre du tenseur de valeurs.
assert torch.allclose(V_R(r, v), V_R(r, torch.full_like(v, 1000.0)))
print("les trois identités passent")

# %% [markdown]
# ### Étape 2 — l'expérience qui porte l'argument de la section 13.11
#
# Fabriquez une trajectoire synthétique de **quarante pas** où **toute la récompense
# arrive au pas trente**, et zéro partout ailleurs. Donnez à vos fonctions un critique
# **parfait**, c'est-à-dire des valeurs égales au vrai retour actualisé restant, que
# vous pouvez calculer à la main **puisque vous avez construit les récompenses**.

# %% [smoke]
# La trajectoire jouet, et le critique parfait qui va avec. Fournis, parce que leur
# intérêt est dans ce qu'ils démontrent, pas dans leur frappe.
T, PAS_RECOMPENSE = 40, 30
recompenses = torch.zeros(T)
recompenses[PAS_RECOMPENSE] = 1.0

# Le vrai retour actualisé restant, depuis chaque pas. Calculable à la main.
valeurs_parfaites = torch.tensor(
    [GAMMA ** (PAS_RECOMPENSE - t) if t <= PAS_RECOMPENSE else 0.0 for t in range(T)],
    dtype=torch.float32)

print("récompense au pas", PAS_RECOMPENSE)
print("valeur parfaite au pas 0 :", float(valeurs_parfaites[0]))
print("valeur parfaite au pas 29 :", float(valeurs_parfaites[29]))

# %%
# Tracez, en fonction de l'horizon H de dix à quarante, l'estimation rendue par
# chacun des trois estimateurs AU PAS INITIAL.
horizons = range(10, 41)
...        # À COMPLÉTER : les trois courbes

fig, ax = plt.subplots(figsize=(8, 4.5))
...        # À COMPLÉTER
ax.axvline(PAS_RECOMPENSE, linestyle="--", linewidth=1,
           label=f"la récompense arrive au pas {PAS_RECOMPENSE}")
ax.set_xlabel("horizon H"); ax.set_ylabel("estimation au pas initial")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Ce que vous devriez voir** : \(V_{\mathrm{R}}\) reste **exactement nul** jusqu'à
# \(H = 30\) puis se réveille brutalement, pendant que les deux autres donnent une
# estimation correcte **dès \(H = 10\)**. C'est la figure du balayage d'horizon de la
# section 13.11, en version jouet et en dix lignes.
#
# **Étape 3, à écrire dans votre carnet.** En trois phrases : **ce que cette
# expérience établit et ce qu'elle n'établit pas**. Elle établit que
# \(V_{\mathrm{R}}\) est aveugle au-delà de l'horizon, et que l'amorçage sur une
# valeur lève cette cécité. Elle **n'établit pas** que l'agent complet de la section
# 13.11 apprend mieux : **votre critique était parfait, et un critique parfait est
# précisément ce qu'on n'a pas.**

# %% [markdown]
# ---
# # Volet B : la semaine 3, sur une dynamique analytique
#
# **Objectif.** Faire tourner le planificateur de la section 13.5 sur une dynamique
# **exacte**, ce qui l'isole complètement du modèle appris. C'est la **ligne plafond**
# du tableau de la section 13.7, et c'est la méthode d'entropie croisée de la semaine
# 3 qui revient.
#
# **Pourquoi c'est légitime, et c'est l'ancrage le plus solide des quatre volets.** La
# ligne plafond est exactement cela : la même méthode, les mêmes quatre réglages,
# appliquée à la vraie dynamique, sans aucun modèle appris et avec zéro épisode
# d'entraînement. **Vous ne reproduisez pas une approximation de ce résultat : vous
# reproduisez la même chose, sur un système plus petit.**

# %%
class DoubleIntegrateur:
    """Une masse ponctuelle sur une ligne. État (x, xdot), action = accélération."""

    def __init__(self, dt=0.05):
        self.dt = dt

    def reset(self, etat=None):
        ...        # À COMPLÉTER

    def pas(self, etat, action):
        """Un pas d'Euler. Rend (nouvel_etat, recompense). Exact, réinitialisable, gratuit."""
        ...        # À COMPLÉTER : recompense = -x^2 - 0.1 * xdot^2

# %%
def planifier(dynamique, etat, H=12, I=10, J=1000, K=100, rng=None):
    """La fonction de la section 13.5, les appels au modèle remplacés par la dynamique."""
    ...        # À COMPLÉTER : c'est votre boucle de la semaine 3, et vous allez
               # constater qu'elle pilote correctement un système dynamique.

# %% [markdown]
# ### Étape 3 — les trois mesures qui font le volet
#
# **La réinitialisation de la loi.** Comparez deux versions : celle qui remet \(\mu\)
# et \(\sigma\) à zéro et un **à chaque pas**, et celle qui repart de la loi trouvée au
# pas précédent. Mesurez le retour sur trois graines, et **surtout** mesurez ce qui se
# passe quand vous **perturbez brusquement l'état au pas cent**. C'est l'argument de
# l'optimum local de la section 13.5, et il devient visible **exactement là**.

# %%
...        # À COMPLÉTER : les deux versions, et la perturbation au pas 100

# %% [markdown]
# **Les itérations contre le tirage brut.** Comparez \(I = 10\) itérations à \(I = 1\)
# **avec le même nombre total de candidats tirés**. C'est l'ablation de la section
# 13.7, et elle est entièrement reproductible ici.

# %%
...        # À COMPLÉTER : I=10 avec J=1000, contre I=1 avec J=10000

# %% [markdown]
# **L'horizon.** Faites varier \(H\) de 3 à 30, et tracez le retour. Vous devriez voir
# une **saturation**, et sur un système aussi simple elle arrive tôt. Dites pourquoi,
# en une phrase, et **en reliant à la section 13.11**.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Étape 4, ce que le volet n'établit pas**, et je veux la phrase dans votre carnet :
# **rien de ceci ne dit quoi que ce soit sur la qualité d'un modèle appris.** Votre
# dynamique est exacte. Vous avez mesuré le **planificateur**, et uniquement lui.
#
# > **Savourez ce volet pour ce qu'il est.** Vous allez rouvrir le carnet de la
# > semaine 3, y recopier une boucle de quinze lignes que vous aviez écrite quand ce
# > cours commençait, et constater qu'elle pilote correctement un système dynamique en
# > commande prédictive. La semaine 3 avait quitté cette méthode sur un échec, et
# > c'était un échec réel. Dix semaines plus tard, elle est le planificateur d'une
# > architecture de pointe. **C'est l'argument le plus fort que je puisse vous donner
# > en faveur du fait d'apprendre les méthodes simples avant les compliquées.**

# %% [markdown]
# ---
# # Volet C : un gradient qui traverse deux couches de dynamique
#
# **Objectif.** Montrer, en vingt lignes, que le gradient de l'acteur de la section
# 13.11 **arrive réellement** jusqu'à \(\phi\) en traversant des transitions apprises.
# Ce volet démontre **l'existence d'un chemin de dérivation, et rien d'autre** : il
# n'entraîne aucun agent.

# %%
def geler(module):
    for p in module.parameters():
        p.requires_grad_(False)
    return module


# Deux réseaux de transition jouets, à poids GELÉS, et une tête de récompense gelée.
T1 = ...        # À COMPLÉTER : (etat, action) -> etat, deux couches denses, gelé
T2 = ...        # À COMPLÉTER
tete_recompense = ...        # À COMPLÉTER : etat -> scalaire, gelée


class ActeurReparametre(nn.Module):
    """Celui de la section 13.9 : tanh, et le bruit tiré À L'EXTÉRIEUR."""

    def __init__(self, n_etat, n_action):
        super().__init__()
        ...        # À COMPLÉTER

    def forward(self, etat, bruit):
        ...        # À COMPLÉTER : l'action est une FONCTION du bruit, pas un tirage

# %% [markdown]
# ### Étape 3 — les trois comparaisons qui font tout le volet
#
# Chacune tient en **une ligne de code modifiée**.

# %%
def norme_du_gradient_acteur(detacher_apres_t1=False, sans_reparametrisation=False):
    """Déroule deux pas, lit la récompense, rétropropage, et rend la norme."""
    ...        # À COMPLÉTER : état initial -> acteur -> T1 -> acteur -> T2 -> récompense,
               # objectif = somme des deux récompenses, backward, puis la norme du
               # gradient de acteur.parameters()


# 1. Le cas correct.
n_correct = norme_du_gradient_acteur()

# 2. Sans reparamétrisation : rsample remplacé par sample, ou l'action tirée dans une
#    loi au lieu d'être écrite comme fonction du bruit.
#    Le gradient doit S'EFFONDRER OU DISPARAÎTRE : c'est le bogue silencieux de 13.9.
n_sans_repar = norme_du_gradient_acteur(sans_reparametrisation=True)

# 3. Graphe coupé après la première transition.
#    Non nul, mais ne portant plus que l'information du premier pas.
n_detache = norme_du_gradient_acteur(detacher_apres_t1=True)

print(f"correct            : {n_correct:.6f}")
print(f"sans reparamétrage : {n_sans_repar:.6f}   <- doit s'effondrer")
print(f"détaché après T1   : {n_detache:.6f}   <- non nul, mais amputé")

# %% [markdown]
# **Étape 4, la comparaison qui vaut la peine.** Faites la même mesure sur un acteur
# de la **semaine 9**, c'est-à-dire un acteur reparamétré qui maximise une valeur
# d'action apprise **au pas courant**, sans aucune transition dans le chemin.
#
# Comparez les deux chemins de dérivation, et écrivez en **deux phrases** ce que la
# méthode de cette semaine ajoute. C'est la ligne du milieu du tableau de la section
# 13.11, mise à l'épreuve dans votre code.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet n'établit pas**, et c'est important : il ne montre **pas** que ce
# gradient entraîne un bon agent. **Un chemin de dérivation peut exister et être
# totalement inutile, si le modèle qu'il traverse est faux.** Ce volet montre que le
# mécanisme fonctionne mécaniquement ; la section 13.11 vous dit, elle, à quel prix en
# calcul il fonctionne réellement.

# %% [markdown]
# ---
# # Volet D : une politique qui désapprend, puis qui cesse de désapprendre
#
# **C'est le volet le plus important des quatre, et celui qui mène au jalon 4.**
#
# L'axe des abscisses de la courbe de la section 13.14 va de zéro à **mille pas de
# gradient**. Mille pas sur un réseau à deux couches, c'est quelques secondes. Et la
# recette hors ligne est celle de la section 13.12 : préremplir le tampon, supprimer
# la ligne de collecte. **Vous disposez donc des deux bouts.**

# %% [markdown]
# **Étape 1 — fabriquer le jeu figé, et c'est la seule fois où vous appelez
# Gymnasium.** Une politique de comportement \(\pi_\beta\) **médiocre mais pas
# absurde** : un contrôleur proportionnel grossier, plus un bruit gaussien généreux.
#
# Collectez cinquante mille transitions, **enregistrez-les sur disque**, puis fermez
# l'environnement et **notez l'heure** : à partir de maintenant et jusqu'à
# l'évaluation finale, **vous n'avez plus le droit d'appeler `env.step`**.
#
# Collectez en outre **trois jeux** de tailles différentes, mille, dix mille et
# cinquante mille, avec la **même** politique de comportement.

# %%
def politique_comportement(obs, rng, gain=0.5, sigma=0.8):
    """Médiocre mais pas absurde : proportionnel grossier, plus bruit généreux."""
    ...        # À COMPLÉTER


def collecter_jeu(n_transitions, graine=0, chemin=None):
    """Appelle env.step. C'est la SEULE fonction du volet qui en a le droit."""
    ...        # À COMPLÉTER : collecter, puis np.savez sur disque


for n in [1_000, 10_000, 50_000]:
    collecter_jeu(n, chemin=f"jeu-{n}.npz")

# %% [markdown]
# **Étape 2 — désapprendre.** Entraînez un acteur-critique continu de la semaine 9 par
# la recette de la section 13.12 : **tampon prérempli, aucune collecte**.
#
# Enregistrez **trois** quantités, et c'est le choix de ces trois quantités qui fait
# le volet :
#
# 1. le **retour réel** de la politique courante, mesuré en la déployant tous les cent
#    pas de gradient. Oui, cela appelle `env.step` : c'est une **mesure**, pas un
#    entraînement. Un praticien hors ligne ne disposerait pas de cette mesure, et
#    c'est d'ailleurs un problème majeur du domaine ;
# 2. la **valeur d'action moyenne estimée** sur un lot du jeu, en échelle
#    logarithmique ;
# 3. l'**erreur de Bellman**, c'est-à-dire la perte que vous minimisez.
#
# **Prédisez-les avant de les regarder**, comme en semaine 12.

# %%
# Prédiction, retour réel        : ...
# Prédiction, valeur estimée     : ...
# Prédiction, erreur de Bellman  : ...

def entrainer_hors_ligne(chemin_jeu, pas_gradient=5000, alpha_cons=0.0, graine=0):
    """Rend (retours_reels, valeurs_estimees, erreurs_bellman)."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : charger le jeu DEPUIS LE FICHIER, et ne jamais collecter

# %%
fig, ax = plt.subplots(figsize=(9, 5))
...        # À COMPLÉTER : les trois courbes sur le même axe des abscisses
ax.set_xlabel("pas de gradient")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Ce que vous devriez voir** : un retour qui **monte puis redescend**, une valeur
# estimée qui **monte sans arrêt**, et une erreur de Bellman qui **descend sagement**
# pendant toute la durée de l'expérience.
#
# **La troisième courbe est le piège, et c'est pour cela que je vous la fais tracer :
# votre perte vous dira que tout va bien pendant que votre agent se dégrade.**

# %% [markdown]
# **Étape 3, l'expérience qui doit vous marquer.** Refaites l'étape 2 sur les **trois
# tailles** de jeu. Multipliez donc les données par **cinquante**. Puis répondez par
# écrit à une question : **le retournement de la courbe a-t-il disparu ?**
#
# La section 13.14 annonce que non, sur un facteur **mille**. Dites ce que vous
# observez sur un facteur cinquante, et dites **quelle autre quantité, elle, s'est
# bien améliorée avec les données**. Il y en a une, et la trouver est l'objet de la
# question.

# %%
for n in [1_000, 10_000, 50_000]:
    ...        # À COMPLÉTER : sur trois graines, avec intervalle

# %% [markdown]
# **Étape 4, cesser de désapprendre.** Ajoutez la pénalité conservatrice de la section
# 13.15 et refaites l'étape 2 pour **trois valeurs de \(\alpha_{\text{cons}}\)
# séparées par un facteur dix**.
#
# Mesurez, pour chacune : le **moment** du retournement, s'il a lieu, et le **meilleur
# retour** atteint. Vous devriez voir un compromis : **trop peu** de pénalité et le
# retournement revient, **trop** de pénalité et le meilleur retour s'écrase vers celui
# de la politique de comportement.

# %%
for alpha_cons in [0.1, 1.0, 10.0]:
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 5, la référence qu'il faut absolument tracer.** Mesurez le retour de la
# **politique de comportement elle-même**. C'est l'étalon de tout ce volet : **une
# méthode hors ligne qui ne la dépasse pas n'a rien produit, et une méthode qui tombe
# en dessous d'elle a activement nui.** Placez cette valeur en ligne horizontale sur
# vos trois graphiques.

# %%
...        # À COMPLÉTER

# %% [markdown]
# > **Trois pièges de ce volet, et chacun fausse la conclusion.**
# >
# > 1. **Appeler l'environnement pendant l'entraînement.** Si une seule transition
# >    collectée pendant la boucle entre dans votre tampon, vous ne faites plus
# >    d'apprentissage hors ligne, et le phénomène disparaîtra en partie. **Séparez
# >    physiquement les deux phases, et chargez le jeu depuis un fichier.**
# > 2. **Juger sur la perte.** Elle descend, elle descendra, et elle ne mesure rien de
# >    ce qui vous intéresse.
# > 3. **Une seule graine.** Le retournement arrive à des moments différents selon
# >    l'initialisation : une graine unique produira soit une courbe spectaculaire
# >    soit une courbe plate, **dans les deux cas sans valeur**.

# %% [markdown]
# ---
# # La solution courte de cette semaine est un clonage de comportement
#
# Les bibliothèques que ce cours emploie sont construites autour d'une boucle qui
# **collecte**, et l'objet de la seconde moitié de la semaine est précisément de
# l'interdire. La référence est donc une **méthode**, et c'est la bonne.

# %%
# La reference la plus honnete pour un apprentissage hors ligne, et la plus
# facile a ecrire : un apprentissage supervise pur sur le jeu figé.
#
# On apprend a predire l'action du jeu de donnees a partir de son etat,
# par une simple erreur quadratique. Aucune recompense, aucune valeur,
# aucun amorçage, donc AUCUN des problemes de la section 13.14.
#
# Ce que cette reference mesure exactement :
#  1. elle reproduit pi_beta, donc son retour est celui de pi_beta, a
#     l'erreur d'approximation pres. C'est votre PLANCHER.
#  2. si votre methode de la section 13.15 ne depasse pas ce plancher,
#     elle n'a rien extrait du jeu de donnees que l'imitation ne donnait
#     deja, et c'est un diagnostic sur vos DONNEES.
#  3. la section 13.16 explique par quel mecanisme une methode fondee sur
#     la valeur peut, elle, depasser ce plancher : la recomposition.
#
# Tracez les deux retours sur le meme graphique. L'ecart entre eux est
# la seule chose que votre travail de la semaine a produite.

...        # À COMPLÉTER : le clonage de comportement, sur le MÊME jeu figé

# %% [markdown]
# > **Et pourquoi cette référence est meilleure qu'une bibliothèque, dans ce cas
# > précis.** Une référence de bibliothèque vous dit si votre **code** est correct.
# > Celle-ci vous dit quelque chose de plus intéressant : **si votre problème valait
# > la peine d'être posé.** Un jeu de données sur lequel un clonage de comportement
# > égale votre meilleure méthode hors ligne est un jeu qui ne contient **aucune
# > recomposition exploitable**, et aucune sophistication n'y changera rien. C'est un
# > diagnostic sur les **données** et non sur l'algorithme, et c'est exactement le
# > réflexe que le jalon 4 va vous demander.
