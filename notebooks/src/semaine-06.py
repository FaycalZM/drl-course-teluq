# %% [markdown]
# # SCI1070 — Semaine 6 : quatre réparations, et laquelle sert vraiment
#
# | Volet | Ce que vous y faites | Statut |
# | --- | --- | --- |
# | A | lire la bibliothèque, et **prédire sa sortie avant de l'exécuter** | 10 minutes |
# | B | le socle commun, et la courbe de référence sur CartPole | implémentation |
# | C | **l'ablation à quatre variantes, trois graines** | **évalué** |
# | D | mille états témoins, et la contrainte de moyenne nulle | méthode |
# | E | couches bruitées et tampon priorisé | facultatif |
#
# Le **volet C est, littéralement, la moitié du jalon 2** de la semaine prochaine.
# Ce que vous produisez cette semaine, vous le rendrez à nouveau, augmenté, dans huit
# jours. **Nommez vos fichiers et vos exécutions comme si vous deviez les relire**,
# parce que vous devrez les relire.
#
# > **La mise en garde la plus importante du laboratoire.** Je ne vous donne, dans
# > aucun volet, le nombre de trames que vous devez obtenir, et ce n'est pas un oubli.
# > Tous les chiffres de cette semaine viennent d'exécutions sur Atari avec des
# > hyperparamètres réglés variante par variante. Ils ne prédisent **rien** de ce que
# > fait une variante sur CartPole en trois minutes. Les attentes sont donc
# > **qualitatives** : un ordre entre les courbes, un signe, une forme. Si l'**ordre**
# > de vos courbes est stable sur trois graines, vous avez un résultat.

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

import collections
from dataclasses import dataclass
from typing import Optional

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

peripherique = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("périphérique :", peripherique)

# %% [markdown]
# ---
# # Volet A : lire la bibliothèque, et prédire sa sortie
#
# **Objectif.** Vérifier que vous avez compris la transition premier-dernier, **sans
# entraîner quoi que ce soit**. Dix minutes, et c'est le meilleur rapport de tout le
# laboratoire entre ce que l'exercice apprend et ce qu'il coûte.
#
# C'est la **seule** semaine du cours où une bibliothèque d'agents est un objet
# d'étude plutôt qu'une solution courte. On la lit ; on ne s'appuie pas dessus.

# %%
# Deux lignes, et les deux précautions comptent (section 6.1). PTAN 0.8 fige
# torch==2.3.1, qui n'a plus de roue pour les Python récents : sans `--no-deps`,
# l'installation s'arrête avant d'avoir rien installé. Et son premier import charge
# stable_baselines3, qu'elle ne déclare pas dans ses dépendances.
ptan_disponible = False
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "stable_baselines3"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "ptan==0.8", "--no-deps"], check=True)
    import ptan.experience as ptan_experience
    ptan_disponible = True
    print("ptan chargé, ExperienceSourceFirstLast :",
          hasattr(ptan_experience, "ExperienceSourceFirstLast"))
except Exception as exc:
    # Pas bloquant : le volet porte sur le MÉCANISME, pas sur le paquet, et la
    # réimplémentation de la section 6.3 est juste en dessous.
    print("ptan indisponible ici :", type(exc).__name__, exc)
    print("-> utilisez la réimplémentation de la section 6.3, ci-dessous.")

# %% [markdown]
# ### L'environnement jouet de la section 6.3
#
# Une observation qui compte de 0 à 4, une récompense **égale à l'action jouée**, un
# épisode de dix pas exactement, et un agent qui joue toujours l'action 1.

# %% [smoke]
class JouetCompteur(gym.Env):
    """Observation 0..4, récompense = action, épisode de dix pas."""

    def __init__(self):
        self.observation_space = gym.spaces.Discrete(5)
        self.action_space = gym.spaces.Discrete(3)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pas = 0
        return 0, {}

    def step(self, action):
        self.pas += 1
        obs = self.pas % 5
        return obs, float(action), False, self.pas == 10, {}


@dataclass
class TransitionPremierDernier:
    """Ce que consomme la perte d'un DQN, à un pas comme à n étapes."""
    etat: object
    action: int
    recompense: float                  # ACCUMULÉE sur les n pas, et actualisée
    etat_final: Optional[object]       # None SI l'épisode s'est terminé


env_jouet = JouetCompteur()
obs, _ = env_jouet.reset(seed=0)
print("trois pas du jouet :", [env_jouet.step(1)[:3] for _ in range(3)])

# %% [markdown]
# ### Ce que je vous demande, et dans cet ordre
#
# **D'abord, écrivez sur une feuille** les douze premières transitions que la source
# d'expérience va produire avec `steps_count=2`, avec leurs **quatre champs**.
# Ensuite seulement, exécutez. Puis comparez, et expliquez en une phrase chacun des
# écarts, s'il y en a.
#
# N'exécutez pas la cellule suivante avant d'avoir écrit vos douze lignes. Le volet
# perd tout son intérêt si vous lisez la réponse d'abord.

# %%
# À COMPLÉTER : la source d'expérience, avec steps_count=2, et l'affichage des douze
# premières transitions. Avec ptan si vous l'avez ; sinon en repliant vous-même la
# trajectoire, d'après `premier_dernier` de la section 6.3.
...

# %% [markdown]
# **Trois questions à traiter en une ligne chacune.**
#
# 1. Pourquoi la plupart des transitions portent-elles une récompense de **2** ?
# 2. Que vaut le champ d'état final à la fin d'un épisode, et **pourquoi ce choix de
#    représentation plutôt qu'un drapeau** ?
# 3. Avec `steps_count=2`, deux transitions sortent coup sur coup en fin d'épisode
#    avec des récompenses différentes. Laquelle est laquelle, et pourquoi la seconde
#    est-elle plus petite ?
#
# **Attendu.** Vos prédictions, la sortie réelle, et vos trois réponses. **Pas de
# courbe, pas d'entraînement.**

# %% [markdown]
# ---
# # Volet B : le socle commun, et la référence sur CartPole
#
# **Objectif.** Réorganiser votre code de la semaine 5 en un **socle importable**, et
# produire la courbe de référence contre laquelle les quatre variantes seront lues.
#
# Deux fichiers, et c'est le point du volet : un `commun.py` qui contient la structure
# d'hyperparamètres, le réseau, le tampon, le dépliage d'un lot, la perte de
# référence, le calendrier de \(\varepsilon\) et la boucle d'entraînement ; et un
# `executer.py` de trente lignes qui choisit une variante par un argument de ligne de
# commande.
#
# `%%writefile` écrit une vraie cellule dans un vrai fichier : vous pourrez ensuite
# lancer `python executer.py reference` depuis un terminal, et c'est exactement ce
# qu'on vous demandera au jalon.

# %%
%%writefile commun.py
"""Socle commun de la semaine 6. Importé par executer.py, jamais recopié."""
import collections

import numpy as np
import torch
import torch.nn as nn

HYPERPARAMETRES = {
    "gamma": 0.99,
    "taille_lot": 64,
    "taille_tampon": 10_000,
    "tampon_initial": 1_000,
    "pas_apprentissage": 1e-3,
    "synchro_cible": 500,
    "epsilon_debut": 1.0,
    "epsilon_fin": 0.02,
    "epsilon_trames": 10_000,
    "seuil_resolu": 475,
}


class Reseau(nn.Module):
    ...        # À COMPLÉTER : votre réseau de la semaine 5


class ReseauDuel(nn.Module):
    ...        # À COMPLÉTER : deux têtes, et la soustraction de la moyenne (section 6.8).
               # Réduisez la largeur des couches cachées pour tenir le budget de
               # paramètres du point de contrôle 3.


def perte_reference(lot, reseau, reseau_cible, gamma, peripherique, n=1):
    ...        # À COMPLÉTER : votre perte de la semaine 5, avec gamma ** n


def perte_double(lot, reseau, reseau_cible, gamma, peripherique, n=1):
    ...        # À COMPLÉTER : trois lignes de différence. L'action vient du réseau
               # ENTRAÎNÉ, son évaluation vient du réseau CIBLE.


def entrainer(perte, classe_reseau, n, graine, max_trames=150_000):
    ...        # À COMPLÉTER : la boucle, paramétrée. Rend (trames, retours).

# %%
%%writefile executer.py
"""Trente lignes : choisir une variante, la lancer, enregistrer la courbe."""
import argparse
import json

import commun

# Une variante est un triplet (perte, classe de réseau, n).
VARIANTES = {
    "reference": (commun.perte_reference, commun.Reseau,     1),
    "n-etapes":  (commun.perte_reference, commun.Reseau,     3),  # seul n change
    "double":    (commun.perte_double,    commun.Reseau,     1),  # seule la perte
    "duel":      (commun.perte_reference, commun.ReseauDuel, 1),  # seul le réseau
}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("variante", choices=sorted(VARIANTES))
    p.add_argument("--graine", type=int, required=True)   # JAMAIS de défaut implicite
    args = p.parse_args()

    perte, classe, n = VARIANTES[args.variante]
    trames, retours = commun.entrainer(perte, classe, n, graine=args.graine)

    nom = f"{args.variante}-g{args.graine}.json"
    with open(nom, "w", encoding="utf-8") as f:
        json.dump({"trames": list(map(int, trames)), "retours": list(map(float, retours))}, f)
    print("écrit :", nom)

# %% [markdown]
# ### Les trois points de contrôle
#
# Ils attrapent les trois bogues de **structure** de ce volet.

# %%
import commun

# 1. Le socle est importé, pas recopié : une seule source de vérité.
assert commun.HYPERPARAMETRES["gamma"] == 0.99

# 2. Toutes les variantes partagent la MÊME graine, passée explicitement.
graine = 0
assert graine is not None

# 3. Le réseau duel a un nombre de paramètres COMPARABLE à la référence.
reseau_reference = ...      # À COMPLÉTER
reseau_duel = ...           # À COMPLÉTER
n_ref = sum(p.numel() for p in reseau_reference.parameters())
n_duel = sum(p.numel() for p in reseau_duel.parameters())
assert 0.8 < n_duel / n_ref < 1.25        # sinon la comparaison est truquée
print(f"référence {n_ref} paramètres, duel {n_duel} ({n_duel / n_ref:.2f}x)")

# %% [markdown]
# **Attentes du volet B.**
#
# * La référence résout CartPole, et vous notez combien de trames il lui faut, en
#   moyenne sur **trois graines**.
# * Une courbe de retour par épisode, lissée sur dix épisodes, avec l'axe horizontal
#   en **trames** et non en épisodes.
# * La troisième assertion doit passer. Si elle échoue, réduisez la largeur des
#   couches cachées du réseau duel, comme la section 6.8 l'explique.

# %% [markdown]
# ---
# # Volet C, évalué : l'ablation à quatre variantes
#
# **Objectif.** Mesurer ce que chaque réparation apporte **sur votre problème**, et
# non sur celui des figures de cette page.
#
# Quatre configurations, le même socle, les mêmes hyperparamètres, les **mêmes trois
# graines**, le même nombre maximal de trames, le même lissage.
#
# | Configuration | La seule chose qui change | Le défaut visé |
# | --- | --- | --- |
# | **(1) référence** | rien | la ligne de base |
# | **(2) n étapes**, \(n = 3\) | `steps_count=3` et `gamma ** 3` dans la perte | nº5, la cible à un pas |
# | **(3) double** | trois lignes dans la perte | nº1, le \(\max\) qui surestime |
# | **(4) duel** | la classe du réseau, et rien d'autre | nº3, une seule tête |

# %%
GRAINES = [0, 1, 2]        # LES MÊMES pour les quatre variantes

resultats = {}
for variante in ["reference", "n-etapes", "double", "duel"]:
    resultats[variante] = [
        ...        # À COMPLÉTER : une exécution par graine, via commun.entrainer
        for g in GRAINES
    ]

# %% [markdown]
# **La figure.** Trois graines, donc la **médiane** par configuration avec
# l'intervalle entre les exécutions extrêmes en bande claire. Une courbe par graine
# superposée fait un plat de spaghettis illisible.

# %%
def mediane_et_extremes(courbes):
    """Rend (médiane, minimum, maximum) point par point, sur un axe commun."""
    ...        # À COMPLÉTER : attention, les exécutions n'ont pas la même longueur.
               # Tronquez explicitement à la plus courte plutôt que d'agréger des
               # points qui ne se correspondent pas.


fig, ax = plt.subplots(figsize=(9, 5))
for variante, courbes in resultats.items():
    ...        # À COMPLÉTER : médiane en trait plein, bande claire entre les extrêmes
ax.set_xlabel("trames"); ax.set_ylabel("retour, lissé sur dix épisodes")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %%
# Le tableau à quatre lignes : trames pour atteindre 400, et l'écart meilleure/pire graine.
...        # À COMPLÉTER

# %% [markdown]
# ### Le piège à vérifier explicitement, et il vaut des points
#
# Montrez par un **test** que la configuration (2) utilise bien \(\gamma^3\) dans sa
# perte et non \(\gamma\). C'est l'erreur qui invalide le plus souvent cette
# expérience, et **elle ne lève aucune exception**.

# %%
# Une façon de le prouver : un lot fabriqué à la main, dont on connaît la cible exacte.
# Si la perte utilise gamma au lieu de gamma ** n, le nombre attendu ne tombe pas.
...        # À COMPLÉTER

# %% [markdown]
# **Attentes du volet C, et c'est ce que je corrigerai.**
#
# * **Les quatre courbes sur un seul graphique**, axes nommés, légende, axe horizontal
#   en trames, lissage identique, médiane et bande.
# * **Un tableau à quatre lignes** : trames pour atteindre une moyenne de 400 ou
#   « jamais atteint », et l'écart entre la meilleure et la pire des trois graines.
# * **Une page écrite, et c'est le cœur de l'exercice.** Pour chacune des trois
#   variantes : quel défaut nommé en section 5.9 elle répare, par quel mécanisme, ce
#   que vous observez, et **si l'écart que vous mesurez est plus grand ou plus petit
#   que la dispersion entre vos graines**. Les mots attendus : **« surestimation »**,
#   **« identifiable »**, **« dépliage »**, **« dispersion »**.
# * **Une phrase que je veux lire textuellement** : dites ce qui, dans votre
#   protocole, garantit que vous mesurez la variante et non autre chose.

# %% [markdown]
# ---
# # Volet D : rendre visibles deux effets invisibles
#
# **Objectif.** Reproduire, sur CartPole, les deux protocoles de mesure des sections
# 6.7 et 6.8. C'est le volet qui vous apprendra le plus sur la manière dont on
# **démontre** quelque chose dans ce domaine.
#
# **Protocole 1, la surestimation.** Avant l'entraînement, collectez **mille états
# témoins** en jouant une politique aléatoire, et mettez-les de côté. Pendant
# l'entraînement, toutes les mille trames, calculez la moyenne de
# \(\max_a Q_\theta(s,a)\) sur ces mille états. Faites-le pour les configurations
# (1) et (3), et tracez les deux courbes ensemble.

# %%
def collecter_aleatoirement(env, n: int) -> np.ndarray:
    """n observations d'une politique uniforme. Elles ne servent JAMAIS à apprendre."""
    obs_list, obs, _ = [], *env.reset(seed=0)
    while len(obs_list) < n:
        obs_list.append(np.asarray(obs, dtype=np.float32))
        obs, _, termine, tronque, _ = env.step(env.action_space.sample())
        if termine or tronque:
            obs, _ = env.reset()
    return np.asarray(obs_list[:n])


# Les états témoins ne servent JAMAIS à l'apprentissage.
etats_temoins = torch.as_tensor(
    collecter_aleatoirement(gym.make("CartPole-v1"), 1000)).to(peripherique)


@torch.no_grad()
def valeur_moyenne_temoins(reseau) -> float:
    return float(reseau(etats_temoins).max(dim=1)[0].mean())


print("états témoins :", tuple(etats_temoins.shape))

# %%
# À COMPLÉTER : rejouer les configurations (1) et (3) en relevant
# valeur_moyenne_temoins toutes les mille trames, puis tracer les deux courbes.
...

# %% [markdown]
# **Protocole 2, la contrainte duale.** Sur un ensemble d'états fixé, suivez pendant
# l'entraînement la **moyenne des avantages** produits par votre réseau duel, et la
# moyenne de sa **tête de valeur**. Tracez les deux.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Attentes du volet D.**
#
# * Deux graphiques, et **trois phrases** sur chacun.
# * Sur le premier : la version ordinaire s'attribue-t-elle, à un moment, des valeurs
#   qu'elle finit par démentir ? Et, question plus importante : **pouvez-vous le
#   conclure sur une seule graine ?**
# * Sur le second : la moyenne des avantages doit rester **proche de zéro**. Donnez son
#   amplitude. Si elle dérive franchement, votre soustraction est mal branchée, et ce
#   volet vient de vous faire gagner une soirée.
# * **Une remarque sur la méthode, en deux phrases** : pourquoi ces deux mesures
#   sont-elles indispensables, alors que la courbe de retour ne montre ni l'une ni
#   l'autre ?

# %% [markdown]
# ---
# # Volet E, facultatif : les deux réparations les plus intrusives
#
# **Piste 1, les réseaux bruités.** Écrivez la couche bruitée de la section 6.9,
# remplacez les deux couches linéaires de la tête, et **supprimez** tout le code de la
# stratégie \(\varepsilon\)-gloutonne : le sélecteur, le calendrier, les trois
# hyperparamètres. Vérifiez que `reseau.eval()` rend bien l'agent déterministe, et
# tracez le rapport signal sur bruit de vos deux couches.
#
# **Piste 2, le tampon priorisé.** Écrivez le tampon naïf de la section 6.10 et la
# perte pondérée. Puis **le seul réglage qui compte** : comparez
# \(\alpha_{\mathrm{PER}} = 0\) et \(\alpha_{\mathrm{PER}} = 0{,}6\), et vérifiez que
# la première valeur reproduit **exactement** la courbe de la configuration (1), aux
# fluctuations de tirage près. Si elle ne la reproduit pas, votre tampon a un bogue,
# et ce test est le plus rapide pour le trouver.

# %%
...        # À COMPLÉTER : piste 1 et / ou piste 2

# %% [markdown]
# > **Mon message pour ce laboratoire.** La semaine dernière, le volet évalué vous
# > demandait de retirer une pièce pour voir ce qu'elle faisait. Cette semaine, il
# > vous demande d'en ajouter quatre et de dire laquelle sert. C'est le même geste,
# > dans l'autre sens, et c'est le geste central de tout ce domaine.
# >
# > Vous allez trouver, je le crois, que sur CartPole les écarts entre variantes sont
# > du même ordre que l'écart entre deux graines de la même variante. Ce serait un
# > **excellent** résultat, et il ne faut surtout pas le cacher : il signifie que vous
# > avez mesuré votre dispersion avant de conclure, ce que beaucoup de publications de
# > ce domaine ont longtemps omis de faire. **Un résultat nul correctement établi vaut
# > mieux qu'un écart impressionnant obtenu sur une seule exécution.**
