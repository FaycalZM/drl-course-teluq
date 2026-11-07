# %% [markdown]
# # SCI1070 — Semaine 14 : préférences, substituts, et ce qu'une perte mesure vraiment
#
# | Volet | Ce qu'il isole | Entraînement | Durée |
# | --- | --- | --- | --- |
# | **A** | les deux formes de la perte de préférence, et ce qui les sépare | **aucun** | cinq minutes |
# | **B** | une chaîne de préférences complète, de l'étiquette à la politique | contrôle classique | dix à quinze minutes |
# | **C** | la divergence entre substitut et récompense réelle sous pression | deux ou trois tailles | dix à quinze minutes |
# | **D** | le surapprentissage d'un modèle de récompense sur peu d'étiquettes | régression logistique | cinq minutes |
#
# **La chaîne de la première moitié de la semaine n'est pas reproductible ici.** Treize
# heures de processeur graphique, douze gigaoctets de segments en couleur, un serveur
# web à maintenir pendant l'étiquetage, et **trois cents jugements humains**. Les trois
# premières contraintes excluent une session Colab gratuite ; la quatrième exclut
# **toute** machine, puisqu'elle demande une heure de votre attention par centaine
# d'étiquettes.
#
# > **Aucun des quatre volets n'a été exécuté par ce cours.** Les sections établissent
# > que chaque construction est correcte et soutenue ; elles n'établissent pas qu'une
# > courbe précise sortira de votre session. **Si votre résultat diffère de ce que vous
# > attendiez, la bonne réaction n'est pas de régler jusqu'à ce qu'il ressemble à une
# > attente : c'est de dire ce que vous avez obtenu et d'expliquer ce que cela mesure.**
# > Après treize semaines, c'est devenu la compétence centrale de ce cours.

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

from sci1070.protocole import intervalle
from sci1070.graines import fixer_graines

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
L_SEGMENT = 50        # un segment compte 50 pas : c'est l'échelle du décalage

# %% [markdown]
# ---
# # Volet A : les deux pertes, comme fonctions pures
#
# **C'est le meilleur volet de la semaine.** Je le mets en premier parce qu'il ne
# demande **aucun entraînement**, qu'il tient en vingt lignes, et qu'il enseigne le
# point le plus tranchant de la semaine.
#
# Deux fonctions, prenant toutes deux les deux sommes de segment \(R_1, R_2\) et
# l'étiquette \((y_1, y_2)\), et renvoyant un scalaire :
#
# * **la forme énoncée** (section 14.2, réduite en 14.6) : entropie croisée binaire
#   sur le **logit unique** \(R_1 - R_2\) contre la cible \(y_1\) ;
# * **la forme réellement calculée** (section 14.6) : entropie croisée binaire sur le
#   tenseur des deux sommes **empilées** contre l'étiquette complète.
#
# **N'entraînez rien. Évaluez.**

# %%
def perte_enoncee(R1, R2, y1, y2):
    """Entropie croisée binaire sur le LOGIT UNIQUE R1 - R2, contre la cible y1."""
    ...        # À COMPLÉTER


def perte_calculee(R1, R2, y1, y2):
    """Entropie croisée binaire sur les deux sommes EMPILÉES, contre l'étiquette complète."""
    ...        # À COMPLÉTER

# %% [markdown]
# ### Étape 1 — l'invariance par décalage, et c'est la mesure centrale du volet
#
# Une paire, \(R_1 = 3\) et \(R_2 = 1\), avec \(y = (1, 0)\). Évaluez les deux pertes.
# Puis **ajoutez cinquante aux deux sommes** et réévaluez.
#
# **La première perte doit être identique au bit près, la seconde doit avoir changé.**
# Si votre première perte change, vous avez passé la mauvaise cible.
#
# **Pourquoi cinquante et non dix** : un segment compte \(L = 50\) pas, donc ajouter
# un à la récompense **par pas** ajoute cinquante à la somme. C'est l'échelle réaliste
# du décalage dont il est question.

# %%
R1, R2 = torch.tensor(3.0), torch.tensor(1.0)
y1, y2 = torch.tensor(1.0), torch.tensor(0.0)
decalage = float(L_SEGMENT)        # +1 par pas, sur 50 pas

avant = (perte_enoncee(R1, R2, y1, y2), perte_calculee(R1, R2, y1, y2))
apres = (perte_enoncee(R1 + decalage, R2 + decalage, y1, y2),
         perte_calculee(R1 + decalage, R2 + decalage, y1, y2))

print(f"forme énoncée  : {float(avant[0]):.6f} -> {float(apres[0]):.6f}")
print(f"forme calculée : {float(avant[1]):.6f} -> {float(apres[1]):.6f}")
assert torch.isclose(avant[0], apres[0]), "la forme énoncée ne doit PAS bouger"
assert not torch.isclose(avant[1], apres[1]), "la forme calculée DOIT bouger"

# %% [markdown]
# ### Étape 2 — la paire « les deux sont bons »
#
# Reprenez \(y = (0{,}5\,;0{,}5)\) et cherchez, pour chacune des deux pertes,
# l'ensemble des couples \((R_1, R_2)\) qui la minimisent. Faites-le **numériquement**,
# par une grille sur \([-10, 10]^2\) et une carte de couleur : c'est plus parlant
# qu'une dérivation.
#
# Vous devez voir, pour la première, **une vallée le long de la diagonale**
# \(R_1 = R_2\) ; pour la seconde, **un unique minimum à l'origine**.

# %%
grille = torch.linspace(-10, 10, 201)
A, B = torch.meshgrid(grille, grille, indexing="ij")
demi = torch.tensor(0.5)

cartes = {}
for nom, perte in [("forme énoncée", perte_enoncee), ("forme calculée", perte_calculee)]:
    cartes[nom] = ...        # À COMPLÉTER : évaluer la perte sur toute la grille

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, (nom, carte) in zip(axes, cartes.items()):
    im = ax.pcolormesh(grille, grille, carte.T, shading="auto")
    ax.set_title(nom); ax.set_xlabel("$R_1$"); ax.set_ylabel("$R_2$")
    ax.plot([-10, 10], [-10, 10], "w--", linewidth=1)
    fig.colorbar(im, ax=ax)
plt.tight_layout(); plt.show()

# %% [markdown]
# **Dites en une phrase** ce que la seconde apprend au modèle sur deux segments que la
# personne trouvait **tous les deux excellents**.

# %% [markdown]
# ### Étape 3 — les cibles absolues contradictoires
#
# Trois segments fictifs : un **mauvais**, un **moyen**, un **bon**. Deux paires :
# moyen contre mauvais, étiquetée en faveur du moyen ; et moyen contre bon, étiquetée
# en faveur du bon.
#
# Pour chacune des deux pertes, calculez le gradient par rapport à la somme du segment
# **moyen** dans les deux paires, et dites s'ils pointent **dans le même sens ou en
# sens contraires**.

# %%
...        # À COMPLÉTER : six lignes, et c'est la deuxième conséquence de la section 14.6

# %% [markdown]
# ### Étape 4 — la dérive d'échelle
#
# Fixez \(y = (1,0)\) et une paire telle que \(R_1 > R_2\). Multipliez les deux sommes
# par deux, puis par cinq, puis par dix, et tracez chaque perte en fonction du facteur.
#
# **La seconde doit décroître continûment sans que l'ordre des segments change**, ce
# qui est la troisième conséquence de la section 14.6.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet établit** : que les deux objectifs **ne dépendent pas des mêmes
# quantités**, et exactement en quoi. **Ce qu'il n'établit pas** : que l'un des deux
# produit un meilleur agent. Pour cela il faudrait entraîner, et nous n'avons pas de
# machine pour cela cette semaine. **Dites-le dans votre conclusion.**

# %% [markdown]
# ---
# # Volet B : une chaîne de préférences complète, à un millième du coût
#
# Reconstruire les quatre pièces sur une tâche assez petite pour tenir dans une
# session. **Une seule pièce est remplacée, et c'est la bonne : la personne est
# remplacée par une règle que vous écrivez vous-même.**

# %% [markdown]
# **Étape 1 — l'environnement et l'enregistreur.** L'enveloppe de la section 14.4,
# longueur de segment de l'ordre de **vingt à trente pas**, probabilité de
# déclenchement réglée pour obtenir **quelques centaines** de segments en quelques
# minutes. **Gardez le compteur** : vous devez savoir combien de segments vous avez.

# %%
class EnregistreurSegments(gym.Wrapper):
    def __init__(self, env, longueur=25, probabilite=0.02):
        super().__init__(env)
        ...        # À COMPLÉTER
        self.n_segments = 0        # le compteur, et il sert

    def step(self, action):
        ...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — l'étiqueteur scripté, et c'est la pièce qui demande de la réflexion.**
#
# Deux contraintes, et elles sont pédagogiques :
#
# * votre critère ne doit **pas** être la récompense de l'environnement, sinon vous
#   n'apprenez rien de nouveau ;
# * il doit être **exprimable en une phrase de français**, comme celui de la
#   section 14.5.
#
# Écrivez votre phrase en commentaire au-dessus de la fonction, et **prévoyez le cas
# « les deux sont bons »** quand les deux segments se ressemblent à une tolérance près.

# %%
# Mon critère, en une phrase : ...
def etiqueter(segment_1, segment_2, tolerance=0.05):
    """Rend (y1, y2). Pense au cas (0,5 ; 0,5) : les deux sont bons."""
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 3 — le modèle de récompense.** Un réseau dense à deux couches suffit, vous
# n'avez pas d'images. Entraînez-le avec la perte de l'étape 1 du volet A, c'est-à-dire
# la **forme énoncée**, et gardez **vingt pour cent** des paires de côté.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Étape 4 — la politique contre le modèle.** L'enveloppe de substitution de la
# section 14.7, avec la **normalisation glissante sur cent valeurs**.
#
# **Journalisez les deux récompenses**, celle du modèle et celle de l'environnement,
# sur deux courbes.

# %%
class SubstitutRecompense(gym.Wrapper):
    """La récompense de l'environnement est REMPLACÉE par celle du modèle."""

    def __init__(self, env, modele, fenetre=100):
        super().__init__(env)
        ...        # À COMPLÉTER : la normalisation glissante sur cent valeurs

    def step(self, action):
        obs, recompense_env, termine, tronque, info = self.env.step(action)
        ...        # À COMPLÉTER
        info["recompense_environnement"] = float(recompense_env)   # journalisée, pas utilisée
        return obs, recompense_modele, termine, tronque, info

# %% [markdown]
# **Étape 5 — la variante semi-supervisée.** Rendez la récompense de l'environnement
# visible sur **un épisode sur dix tirés au hasard**, et employez le modèle sur les
# neuf autres.
#
# Comparez à **deux** références : la politique entraînée sur la récompense complète,
# et celle entraînée en **ignorant purement et simplement** les épisodes non
# étiquetés. La seconde doit apprendre nettement plus lentement, et **dire pourquoi
# est la question de l'étape**.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet établit** : que les quatre pièces se branchent, et que votre
# critère écrit en une phrase produit un comportement **identifiable**. **Ce qu'il
# n'établit pas** : quoi que ce soit sur l'efficacité de la rétroaction humaine,
# puisque **votre étiqueteur est déterministe, sans bruit, sans fatigue et sans
# contradiction, c'est-à-dire exactement ce qu'une personne n'est pas**.

# %% [markdown]
# ---
# # Volet C : faire diverger le substitut et la récompense réelle, délibérément
#
# C'est le volet qui produit, à votre échelle, la forme de la Figure 14-3, et celui
# dont le code sert le plus directement au jalon 4.
#
# **Étape 1 — les deux récompenses.** La **réelle** est celle que vous considérez
# comme l'intention ; le **substitut** en diffère par une **erreur de portée**, c'est
# à dire qu'il mesure le même désidérata sur une **partie seulement** de l'espace
# d'états ou de la durée de l'épisode.
#
# **Dites explicitement, en commentaire, lequel des trois types de la section 14.12
# vous avez construit.**

# %%
# Type construit (section 14.12) : ...
def recompense_reelle(etat, action, info):
    ...        # À COMPLÉTER


def recompense_substitut(etat, action, info):
    """Le MÊME désidérata, mesuré sur une partie seulement de l'espace."""
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — deux ou trois tailles.** Entraînez le même algorithme sur le **substitut
# seul**, avec deux ou trois tailles de réseau séparées par un **ordre de grandeur en
# nombre de paramètres**. Mêmes graines, même nombre de pas, même pas d'apprentissage.
# **La seule variable est la capacité.**

# %%
for n_cache in [16, 128, 1024]:
    ...        # À COMPLÉTER

# %% [markdown]
# **Étape 3 — les deux courbes.** Vous cherchez la forme de la section 14.13 : une
# montée commune, puis une séparation.
#
# **Et je vous préviens tout de suite, parce que c'est le point où l'honnêteté du
# volet se joue : il est très possible que vous n'obteniez aucune séparation.** Les
# transitions mesurées en 14.13 apparaissent sur des plages de capacité de **deux à
# quatre ordres de grandeur**, et vous en couvrez **un**. Si vous ne voyez rien, ce
# n'est pas un échec du volet : **c'est un résultat**, et il se rapporte ainsi, avec
# l'écart d'échelle comme explication candidate.

# %%
...        # À COMPLÉTER : substitut et récompense réelle, pour chaque taille

# %% [markdown]
# **Étape 4 — la corrélation, et c'est l'étape que je préfère.** Calculez la
# corrélation de Pearson entre le substitut et la récompense réelle sur une trentaine
# de déroulements, à **deux** points de contrôle : un très précoce, et celui du
# **meilleur substitut**.
#
# Vous devriez trouver une corrélation **positive aux deux points**, même si votre
# plus grand modèle s'est dégradé. C'est la plus utile des quatre mesures, parce
# qu'elle vous apprend à **ne pas faire confiance à une corrélation**.

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet établit** : le protocole, et la forme des courbes si vous la
# voyez. **Ce qu'il n'établit pas** : un seuil, ni une valeur. Les seuils de la
# section 14.13 sont des mesures relevées sur des figures et **ne sont pas des
# références**.

# %% [markdown]
# ---
# # Volet D : le surapprentissage d'un modèle de récompense
#
# Le plus court des quatre, et le plus directement utile si vous choisissez la
# cinquième route du jalon.
#
# **Étape 1.** Reprenez le modèle du volet B et les étiquettes de votre étiqueteur.
# Faites varier le nombre d'étiquettes : **cinquante, deux cents, mille**.
#
# **Étape 2.** Pour chaque taille, gardez **vingt pour cent** de côté, entraînez avec
# un **arrêt anticipé sur cette partition réservée** après **quatre époques sans
# amélioration**, et journalisez les deux pertes à chaque époque.

# %%
for n_etiquettes in [50, 200, 1000]:
    ...        # À COMPLÉTER : les deux courbes de perte, et l'époque d'arrêt

# %% [markdown]
# **Étape 3 — deux questions.** À partir de combien d'étiquettes l'écart entre les
# deux pertes **cesse-t-il de croître** ? Et à quelle époque votre arrêt se
# déclenche-t-il, comparé à l'ordre de grandeur d'**une douzaine d'époques** mentionné
# en section 14.6 ?
#
# **Étape 4, facultative et instructive.** Ajoutez du bruit dans votre étiqueteur :
# avec une probabilité de **dix pour cent**, il se trompe. Refaites la mesure. **C'est
# le seul volet du laboratoire qui approche de la condition réelle d'un étiquetage
# humain.**

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet établit** : l'ordre de grandeur du régime de données dans lequel un
# modèle de récompense cesse de surapprendre, **sur votre tâche**. **Ce qu'il
# n'établit pas** : rien de transférable à une tâche visuelle, où le modèle de la
# section 14.6 avait **plus de cent mille dimensions d'entrée et trois cents
# exemples**.

# %% [markdown]
# ---
# # La solution courte, et pourquoi elle ne dispense pas du volet A
#
# Une référence pour comparer votre code, et elle vaut surtout pour les volets B et C :
# une implémentation de bibliothèque d'une méthode de région de confiance, branchée
# sur **l'enveloppe de substitution que vous aurez écrite**. L'enveloppe reste votre
# travail, puisque c'est elle qui porte toute la semaine ; l'algorithme peut venir
# d'ailleurs.

# %%
# A executer APRES avoir ecrit la votre, jamais avant.
from stable_baselines3 import PPO

# L'enveloppe de substitution est la VOTRE : c'est elle qui porte la semaine.
env_substitut = ...        # À COMPLÉTER : votre SubstitutRecompense du volet B
modele = PPO("MlpPolicy", env_substitut, seed=0, verbose=0)
modele.learn(total_timesteps=50_000)
# Puis evaluer sur la recompense REELLE, pas sur le substitut.

# %% [markdown]
# > **En revanche, le volet A n'a aucune solution courte, et c'est délibéré : aucune
# > bibliothèque ne vous dira de quoi une perte dépend.** Il faut l'évaluer soi-même,
# > et cela prend cinq minutes.
