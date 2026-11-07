# %% [markdown]
# # SCI1070 — Semaine 8 : le gradient de politique, et sa variance
#
# | Volet | Ce que vous y faites |
# | --- | --- |
# | A | REINFORCE avec et sans référence, et **la variance du gradient mesurée** |
# | B | A2C vectorisé sur CartPole, trois termes de perte, dix quantités journalisées |
#
# Le laboratoire est **formatif**. Pas de jalon cette semaine, le prochain est en
# semaine 10 : utilisez cette respiration pour écrire du code **soigné** plutôt que
# du code pressé. Le volet B est l'implémentation de référence que vous réutiliserez
# en semaines 9 et 10.
#
# **Ce que le laboratoire n'implémente pas, et pourquoi.** A3C, la version à processus
# multiples de la section 8.10, n'est pas au programme : les processus multiples sont
# limités dans un carnet partagé. Le volet B utilise des **environnements vectorisés
# synchrones**, qui règlent le problème 4 de la section 8.5 sans un seul processus
# supplémentaire. **La section 8.10 se lit, se discute et ne s'exécute pas**, et c'est
# une décision assumée.
#
# > **Je ne vous donne aucun chiffre à atteindre pour A2C sur CartPole, et c'est
# > volontaire.** Les nombres cités cette semaine sont ancrés : 384 épisodes pour
# > REINFORCE sur CartPole, huit millions de trames pour A2C sur un jeu Atari. Aucun
# > ne s'applique à A2C sur CartPole, et je ne vais pas interpoler entre les deux pour
# > vous donner une cible rassurante et fausse. J'attends une mesure **relative et
# > reproductible** : votre nombre de pas à la résolution, sur au moins trois graines,
# > avec son intervalle, comparé à votre propre REINFORCE sur les **mêmes** graines.

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
import torch.nn.functional as F
import matplotlib.pyplot as plt

from sci1070.protocole import intervalle, se_recouvrent
from sci1070.courbes import bande, tracer_bande
from sci1070.graines import fixer_graines

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
GRAINES = [0, 1, 2]
print("périphérique :", device)

# %% [markdown]
# ---
# # Volet A : REINFORCE avec et sans référence
#
# **Objectif.** Produire **une** figure : la variance du gradient de politique au
# cours de l'entraînement, deux courbes, avec et sans référence, sur les mêmes
# graines.

# %% [markdown]
# ### Étape 1 — REINFORCE, avec un seul interrupteur
#
# Votre code comporte un indicateur `reference` qui active ou désactive la
# soustraction d'une référence, et **rien d'autre ne doit changer** entre les deux
# modes. C'est une étude d'ablation à une variable, comme en semaine 6.

# %%
class ReseauPolitique(nn.Module):
    def __init__(self, n_obs, n_actions, n_cache=128):
        super().__init__()
        ...        # À COMPLÉTER : sorties BRUTES, le softmax vient au moment du tirage

    def forward(self, x):
        ...        # À COMPLÉTER

# %% [markdown]
# ### Étape 2 — la référence
#
# La **moyenne glissante** des retours actualisés observés depuis le début de
# l'exécution. **Deux lignes suffisent** : un compteur de pas et une somme cumulée.

# %%
class MoyenneGlissante:
    """La référence du volet. Deux lignes, et c'est tout ce qu'il faut."""

    def __init__(self):
        self.somme, self.n = 0.0, 0

    def ajouter(self, x: float) -> None:
        ...        # À COMPLÉTER

    @property
    def valeur(self) -> float:
        ...        # À COMPLÉTER

# %% [markdown]
# ### Étape 3, le cœur du volet — isoler le gradient de politique
#
# La manœuvre de la section 8.6 : rétropropager **ce terme seul** avec
# `retain_graph=True`, lire les gradients **avant** de rétropropager l'entropie, puis
# laisser l'optimiseur avancer sur la somme.
#
# Journalisez à chaque mise à jour la **variance**, la **norme \(L_2\)** et le
# **maximum absolu** de ce gradient.

# %%
def statistiques_du_gradient(reseau) -> dict:
    """Les trois statistiques, lues sur les gradients actuellement accumulés."""
    g = torch.cat([p.grad.flatten() for p in reseau.parameters() if p.grad is not None])
    return {"variance": float(g.var()), "norme_l2": float(g.norm()),
            "max_abs": float(g.abs().max())}


def reinforce(reference: bool, graine: int, max_pas=150_000, gamma=0.99):
    """Rend (pas_a_la_resolution, courbe_variance, courbe_retour)."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : REINFORCE, l'indicateur `reference` étant le SEUL
               # interrupteur. Étape 3 ci-dessus pour la lecture du gradient.

# %% [markdown]
# ### Deux vérifications arithmétiques **avant** de conclure
#
# Avec un horizon de déroulement de 10 pas et \(\gamma = 0{,}99\), votre référence doit
# converger vers \(1 + 0{,}99 + \dots + 0{,}99^9\), et vos échelles \(G_t - b\) doivent
# osciller **autour de zéro**. Si l'un des deux n'est pas vérifié, corrigez le bogue
# avant d'interpréter la moindre courbe.

# %% [smoke]
gamma, horizon = 0.99, 10
attendu = sum(gamma ** i for i in range(horizon))
print(f"la référence doit converger vers {attendu:.4f}")
assert abs(attendu - 9.5618) < 1e-3

# %%
# À COMPLÉTER : vérifiez les deux. Votre référence s'approche-t-elle de 9,56 ?
# Vos échelles oscillent-elles autour de zéro ?
...

# %% [markdown]
# ### Étape 4 — la figure
#
# Les deux courbes de variance sur le même graphique, en **échelle logarithmique en
# ordonnée**, parce que l'écart attendu est de deux à trois ordres de grandeur et
# qu'une échelle linéaire l'écraserait.

# %%
resultats = {}
for ref in [False, True]:
    resultats[ref] = [reinforce(reference=ref, graine=g) for g in GRAINES]

fig, ax = plt.subplots(figsize=(8, 5))
for ref, etiquette in [(False, "sans référence"), (True, "avec référence")]:
    courbes = ...        # À COMPLÉTER : les courbes de variance, une par graine
    tracer_bande(ax, np.arange(len(courbes[0])), courbes, etiquette=etiquette)
ax.set_yscale("log")
ax.set_xlabel("mise à jour"); ax.set_ylabel("variance du gradient de politique")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %%
# Les deux nombres de pas à la résolution, avec leur intervalle sur vos graines.
for ref, etiquette in [(False, "sans référence"), (True, "avec référence")]:
    pas = [r[0] for r in resultats[ref]]
    moyenne, bas, haut = intervalle(pas)
    print(f"{etiquette:18s} {moyenne:9.0f} pas   [{bas:.0f}, {haut:.0f}]")

print("\nles deux intervalles se recouvrent :",
      se_recouvrent([r[0] for r in resultats[False]], [r[0] for r in resultats[True]]))

# %% [markdown]
# **Répondez par écrit à deux questions.** L'écart que vous mesurez est-il du même
# ordre que celui annoncé en section 8.6 ? Et la version avec référence résout-elle
# le problème **en moins de pas**, sur vos graines ? (Ce n'est pas la même question
# que la première, et les deux réponses peuvent diverger.)
#
# **Attendu du volet A.** La figure, les deux nombres de pas à la résolution avec leur
# intervalle, et un paragraphe de lecture.

# %% [markdown]
# ---
# # Volet B : A2C vectorisé sur CartPole
#
# **Objectif.** Écrire A2C de bout en bout, avec tronc commun, cible à \(N\) pas et
# perte à trois termes, sur un ensemble d'environnements vectorisés.

# %% [markdown]
# ### Étape 1 — les environnements
#
# **Attention aux deux attributs** qui servent à dimensionner le réseau : les espaces
# d'un ensemble vectorisé sont eux-mêmes des espaces de **lots**, et ce sont
# `single_observation_space` et `single_action_space` qui décrivent **un**
# environnement.

# %% [smoke]
N_ENVS = 16

envs = gym.vector.SyncVectorEnv(
    [lambda: gym.make("CartPole-v1") for _ in range(N_ENVS)]
)
taille_obs = envs.single_observation_space.shape[0]   # 4, et non (16, 4)
n_actions = int(envs.single_action_space.n)           # 2, et non (16,)

print("observation d'UN environnement :", taille_obs, "| actions :", n_actions)
print("observation du LOT             :", envs.observation_space.shape)
obs, info = envs.reset(seed=0)
print("après reset :", obs.shape)
envs.close()

# %% [markdown]
# ### Étape 2 — la cible à \(N\) pas, la fonction la plus délicate du volet
#
# Le piège est la gestion des transitions **terminales** : si vous ajoutez la valeur
# estimée d'un état terminal, vous promettez à l'agent une récompense future qui
# n'existe pas. La façon propre est de collecter les indices des transitions non
# terminales, de n'évaluer le critique que sur celles-là, et d'ajouter le terme à ces
# indices seulement.
#
# Cette fonction vous est donnée entière, parce que son intérêt est dans ce qu'elle
# évite, pas dans sa frappe.

# %% [smoke]
def preparer_lot(lot, reseau, gamma: float, n_pas: int, device):
    """(etats, actions, cibles) a partir d'un lot de transitions premier-dernier.

    Chaque transition porte deja la somme actualisee de ses n_pas recompenses ;
    il ne reste qu'a ajouter la queue estimee, et SEULEMENT si elle existe.
    """
    etats, actions, cibles = [], [], []
    derniers_etats, idx_non_terminaux = [], []

    for i, exp in enumerate(lot):
        etats.append(exp.etat)
        actions.append(exp.action)
        cibles.append(exp.recompense_actualisee)
        if exp.dernier_etat is not None:        # l'episode continue
            idx_non_terminaux.append(i)
            derniers_etats.append(exp.dernier_etat)

    etats_t = torch.as_tensor(np.asarray(etats), dtype=torch.float32, device=device)
    actions_t = torch.as_tensor(actions, dtype=torch.int64, device=device)
    cibles = np.asarray(cibles, dtype=np.float32)

    if derniers_etats:
        derniers_t = torch.as_tensor(np.asarray(derniers_etats),
                                     dtype=torch.float32, device=device)
        with torch.no_grad():                   # le critique est INTERROGE, pas entraine ici
            v_derniers = reseau(derniers_t)[1].squeeze(-1).cpu().numpy()
        cibles[idx_non_terminaux] += (gamma ** n_pas) * v_derniers

    return etats_t, actions_t, torch.as_tensor(cibles, device=device)


print("preparer_lot est fournie : lisez-la, ne la réécrivez pas")

# %% [markdown]
# ### Étape 3 — la boucle
#
# Assemblez la perte à trois termes de la section 8.8, additionnez les trois,
# rétropropagez **une seule fois**, écrêtez la norme du gradient, et avancez.
#
# **N'oubliez ni le `detach()` ni le `eps` d'Adam : ce sont les deux lignes qui
# décident si ce volet fonctionne.**

# %%
class ReseauA2C(nn.Module):
    """Tronc commun, deux têtes : la politique et la valeur."""

    def __init__(self, n_obs, n_actions, n_cache=128):
        super().__init__()
        ...        # À COMPLÉTER : le tronc, puis deux têtes.
                   # forward rend un COUPLE (logits, valeur).

    def forward(self, x):
        ...        # À COMPLÉTER


def a2c(graine, n_envs=N_ENVS, n_pas=4, gamma=0.99, entropie=0.01,
        ecretage=0.5, sans_entropie=False, sans_ecretage=False, max_pas=200_000):
    """Rend (pas_a_la_resolution, journal) où journal porte les dix quantités."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : la boucle complète.
               # Les trois interrupteurs servent à l'ablation de l'étape 5.

# %% [markdown]
# ### Étape 4 — les dix quantités à journaliser
#
# Cette liste est à la fois le tableau de bord du volet et la **liste de diagnostic de
# la semaine**. A2C n'a **aucune** perte dont la valeur vous dise si les choses se
# passent bien : ces dix courbes sont votre seule fenêtre.
#
# 1. l'**avantage** moyen
# 2. la **valeur** moyenne prédite par le critique
# 3. la **récompense** moyenne par épisode
# 4, 5, 6. les **trois termes de perte**, séparément
# 7. la **perte totale**
# 8, 9, 10. les **trois statistiques de gradient** (norme \(L_2\), maximum absolu, variance)
#
# Plus l'**entropie** de la politique, qui n'est pas dans la perte sous cette forme et
# qui est votre meilleur indicateur du problème 3.

# %%
journaux = {g: a2c(graine=g) for g in GRAINES}

fig, axes = plt.subplots(2, 5, figsize=(20, 7))
for ax, quantite in zip(axes.ravel(), [
        "avantage", "valeur", "recompense", "perte_politique", "perte_valeur",
        "perte_entropie", "perte_totale", "grad_norme_l2", "grad_max_abs", "grad_variance"]):
    ...        # À COMPLÉTER : la bande sur les trois graines, pour chaque quantité
    ax.set_title(quantite); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# %% [markdown]
# ### Étape 5 — l'ablation, et elle est rapide
#
# Relancez trois fois en retirant **un** élément à la fois : sans le terme d'entropie,
# sans l'écrêtage du gradient, et avec **un seul** environnement au lieu de \(N\). Pour
# chacun, dites ce qui change dans les courbes et **à quel problème de la section 8.5**
# ce changement correspond. C'est l'exercice qui transforme le tableau de la section
# 8.5 en savoir pratique.

# %%
ablations = {
    "complet": dict(),
    "sans entropie": dict(sans_entropie=True),
    "sans écrêtage": dict(sans_ecretage=True),
    "un seul environnement": dict(n_envs=1),
}
...        # À COMPLÉTER : une ligne de tableau par ablation, sur les MÊMES graines

# %% [markdown]
# ### Diagnostic facultatif, et je vous le recommande vivement
#
# Mesurez la **divergence de Kullback-Leibler** entre la politique **avant** et
# **après** chaque pas d'optimisation. C'est trois lignes : gardez les probabilités
# avant le pas, recalculez les log-probabilités après, et formez
# \(\sum_a \pi_{\text{avant}}(\log\pi_{\text{avant}} - \log\pi_{\text{après}})\).
#
# Une exécution saine reste **en dessous de \(10^{-3}\)**. Des pics élevés sont un
# mauvais signe : le pas a déplacé la politique **trop loin**, et un réseau très non
# linéaire en grande dimension réagit mal à cela.
#
# **Retenez cette quantité : elle est le sujet de la semaine 10.**

# %%
def kl_avant_apres(logits_avant, logits_apres):
    """La divergence KL d'un pas d'optimisation, sur un lot."""
    p_avant = F.softmax(logits_avant, dim=1)
    log_avant = F.log_softmax(logits_avant, dim=1)
    log_apres = F.log_softmax(logits_apres, dim=1)
    return float((p_avant * (log_avant - log_apres)).sum(dim=1).mean())


...        # À COMPLÉTER : la journaliser à chaque pas, et la tracer

# %% [markdown]
# **Attendu du volet B.** La courbe de récompense sur au moins trois graines avec
# intervalle, les dix quantités journalisées, le tableau de vos trois ablations, et la
# comparaison avec votre REINFORCE du volet A **sur les mêmes graines**.
#
# > **Mon message pour ce laboratoire.** Le volet A mesure une variance et le volet B
# > construit un algorithme, et c'est dans cet ordre que je vous demande de les faire,
# > même si le volet B est le plus intéressant. La raison est celle de toute la
# > semaine : vous n'avez, dans A2C, **aucune** perte dont la valeur vous dise si les
# > choses se passent bien. Le seul moyen de savoir ce qui se passe est de savoir à
# > quoi ressemble une variance normale, une entropie normale, une norme de gradient
# > normale. Le volet A vous donne ces repères sur un algorithme simple. **Sans eux,
# > le volet B est une boîte noire qui monte ou ne monte pas.**
