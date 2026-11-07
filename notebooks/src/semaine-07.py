# %% [markdown]
# # SCI1070 — Semaine 7 : mesurer avant de changer, tester avant d'entraîner
#
# | Volet | Ce que vous y faites |
# | --- | --- |
# | A | profiler et accélérer votre socle, **avec graines et intervalles** |
# | B | écrire l'environnement de négociation, et vérifier sa récompense par des assertions |
#
# Le laboratoire est **formatif**, mais lisez ceci avant de commencer : le **volet A
# est la matière du jalon 2**, remis à la fin de cette même semaine. Ce que vous
# mesurez ici, vous le rendrez dans quelques jours, mis en forme. **Nommez vos
# fichiers, vos graines et vos exécutions comme si vous deviez les relire**, parce que
# vous devrez les relire.
#
# **Budget de calcul, fixé explicitement.** Tout le volet A tourne sur `CartPole-v1`.
# Les durées de 30 à 52 minutes données dans la semaine viennent de Pong sur une carte
# dédiée ; multipliées par les variantes et les graines, elles font une dizaine
# d'heures, hors de portée d'une semaine sur un processeur graphique partagé. Sur
# CartPole une exécution se compte en minutes, et vous pourrez donc faire la seule
# chose qui compte : **répéter**.
#
# > **Un avertissement sur les chiffres.** Je ne vous donne, dans aucun volet, le
# > débit ou la durée que vous devez obtenir. Les 229 trames par seconde, les
# > 52 minutes, les +72,5 % viennent d'une machine précise sur un jeu précis. Ils ne
# > prédisent **rien** de ce que votre code fera sur CartPole dans un carnet partagé.
# > Ce que j'attends est **relatif** : des rapports, un classement, un signe, et un
# > intervalle autour de chacun. Si vos nombres absolus ne ressemblent pas aux miens,
# > c'est normal. **Si vos rapports sont stables sur vos graines, vous avez un
# > résultat.**

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

# Le code fourni du cours. À partir de cette semaine, le protocole de mesure ne se
# recopie plus d'un carnet à l'autre : il est dans le paquet, et il est testé.
if importlib.util.find_spec("sci1070") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "git+https://github.com/FaycalZM/drl-course-teluq.git#subdirectory=code"],
                   check=True)

import time

import gymnasium as gym
import numpy as np
import torch
import matplotlib.pyplot as plt

from sci1070.protocole import mesurer, intervalle, se_recouvrent
from sci1070.graines import fixer_graines

print("sci1070 chargé")

# %% [markdown]
# ---
# # Volet A : mesurer, puis changer une seule chose
#
# **Objectif.** Produire un tableau d'accélération de la forme du Tableau 7-1, sur
# **votre** code et **votre** matériel, avec des intervalles.
#
# ### Étape 0, et elle précède toute exécution
#
# Écrivez dans votre carnet, **avant de lancer quoi que ce soit**, trois choses : le
# **critère d'arrêt**, les **deux indicateurs** que vous allez relever, et la **liste
# de vos graines**.
#
# Cet ordre n'est pas décoratif. **Un critère d'arrêt choisi après avoir vu les
# courbes n'est plus un critère, c'est une justification.**

# %%
# Écrivez-les ici, maintenant, et ne les modifiez plus.
CRITERE_ARRET = 475          # moyenne sur les 100 derniers épisodes, sur CartPole-v1
INDICATEURS = ("trames par seconde", "temps d'horloge jusqu'au seuil")
GRAINES = [0, 1, 2, 3, 4]    # k >= 3, 5 de préférence

print(f"critère : {CRITERE_ARRET} | indicateurs : {INDICATEURS} | graines : {GRAINES}")

# %% [markdown]
# ### Étape 1, la version de référence
#
# Partez de votre socle de la semaine 6, **sans le modifier**. Mesurez-le sur
# \(k \ge 3\) graines, 5 de préférence, et rapportez pour chacun des deux indicateurs
# la moyenne **et** l'intervalle.
#
# Vérifiez en même temps que la version de référence **apprend** : c'est la règle
# « correction avant vitesse », et elle s'applique au livrable lui-même.

# %%
def une_execution(configuration, graine, seuil):
    """Rend (trames_par_seconde, temps_jusqu_au_seuil). UNE exécution, UNE graine."""
    fixer_graines(graine)
    ...        # À COMPLÉTER : votre socle de la semaine 6, instrumenté.
               # Deux compteurs : les trames consommées, et le temps d'horloge.
               # Rappel de la section 7.2 : le compteur compte les PAS DE L'AGENT,
               # donc quatre fois moins que les trames brutes d'une pile Atari.


debits_ref, temps_ref = mesurer("référence", GRAINES, seuil=CRITERE_ARRET,
                                execution=une_execution)

for nom, x in [("débit (trames/s)", debits_ref), ("temps (s)", temps_ref)]:
    moyenne, bas, haut = intervalle(x)
    print(f"{nom:22s} {moyenne:8.1f}   [{bas:.1f}, {haut:.1f}]   n={len(x)}")

# %% [markdown]
# ### Étape 2, une modification à la fois
#
# Appliquez **une seule** modification, remesurez sur **les mêmes graines**, inscrivez
# la ligne dans votre tableau, puis passez à la suivante. Trois modifications tiennent
# confortablement dans ce laboratoire.
#
# 1. **`torch.no_grad()` sur les deux usages sans gradient** du réseau, la cible et le
#    choix de l'action. Si votre code de la semaine 6 les avait déjà, mesurez
#    l'inverse : **retirez-les**, et voyez ce que vous obtenez.
# 2. **\(N\) environnements vectorisés**, avec la taille de lot mise à l'échelle et les
#    deux constantes recalibrées (le calendrier de \(\varepsilon\) et la fenêtre du
#    compteur de débit). Balayez \(N\) de 1 à 4 et tracez les deux indicateurs en
#    fonction de \(N\) : **c'est la plus belle courbe du laboratoire, parce qu'elle ne
#    va pas dans le même sens pour les deux.**
# 3. **La couche que personne ne profile.** Sur CartPole il n'y a pas de pile Atari à
#    alléger. Chronométrez séparément, sur mille pas, le temps passé dans
#    l'environnement, dans la préparation des tenseurs, dans le passage avant, et dans
#    l'optimiseur. Puis attaquez la plus grosse part.

# %%
# Le chronométrage par couche, qui est l'outil de la modification 3.
def profiler_par_couche(env_id="CartPole-v1", pas=1000):
    """Rend un dictionnaire {couche: secondes} sur `pas` pas d'agent."""
    ...        # À COMPLÉTER : quatre compteurs, time.perf_counter().
               # Dans la plupart des implémentations écrites en semaine 5, vous
               # trouverez une conversion de tableau en tenseur refaite à chaque pas,
               # ou un aller-retour inutile entre processeur central et graphique.


for couche, secondes in sorted(profiler_par_couche().items(), key=lambda kv: -kv[1]):
    print(f"{couche:28s} {secondes:7.3f} s")

# %%
# Le tableau, avec sa colonne de graines et sa colonne d'intervalle.
variantes = {
    "référence": None,
    "sans no_grad": None,
    "N=2 vectorisé": None,
    "N=4 vectorisé": None,
    "tenseurs préalloués": None,
}

lignes = []
for nom in variantes:
    ...        # À COMPLÉTER : mesurer(nom, GRAINES, CRITERE_ARRET, une_execution),
               # puis une ligne avec moyenne, intervalle, et le rapport à la référence

# %% [markdown]
# ### La courbe en fonction de \(N\)
#
# Deux axes, parce que les deux indicateurs **ne vont pas dans le même sens**. C'est
# tout le propos de la section 7.6 : le débit mesure l'efficacité de votre
# **programme**, le temps à la résolution mesure celle de votre **agent**, et c'est le
# second qui est l'objectif.

# %%
Ns = [1, 2, 3, 4]
debits_par_N, temps_par_N = {}, {}
for N in Ns:
    ...        # À COMPLÉTER

fig, ax = plt.subplots(figsize=(7, 4.5))
ax2 = ax.twinx()
...        # À COMPLÉTER : débit à gauche, temps à droite, barres d'intervalle sur les deux
ax.set_xlabel("N environnements vectorisés")
plt.show()

# %% [markdown]
# ### Étape 3, le tableau et sa lecture
#
# Rendez le tableau avec les colonnes du Tableau 7-1, augmentées d'une colonne
# « graines » et d'une colonne d'intervalle. Puis répondez par écrit à **une** question :
# **avez-vous observé un cas où le classement en débit et le classement en temps se
# contredisent ?** Si oui, lequel et pourquoi. Si non, dites-le explicitement : c'est
# aussi une réponse.
#
# Et avant d'annoncer un gain, posez-vous la question que `se_recouvrent` répond :

# %% [smoke]
# La règle d'interprétation de la section 7.2, en une ligne.
# Deux mesures qui se recouvrent ne separent pas deux variantes.
a = [228.0, 227.0, 229.0, 228.5, 227.5]      # la référence, cinq graines
b = [231.0, 230.0, 232.0, 229.5, 231.5]      # une variante « 1,5 % plus rapide »
print("les intervalles se recouvrent :", se_recouvrent(a, b))
print("-> un écart dont les intervalles se recouvrent n'est PAS un résultat")

c = [300.0, 298.0, 305.0, 301.0, 299.0]      # une variante franchement plus rapide
print("\nréférence contre +32 % :", se_recouvrent(a, c))

# %% [markdown]
# **Attendu du volet A.** Le tableau, les deux courbes en fonction de \(N\), vos
# intervalles, **votre matériel**, et un paragraphe de lecture.

# %% [markdown]
# ---
# # Volet B : écrire l'environnement, et le tester sans l'entraîner
#
# **Objectif.** Écrire l'environnement de négociation de la section 7.10 **de zéro**,
# et le vérifier par des assertions. **Aucun entraînement dans ce volet.**
#
# Vous écrivez vous-même la classe d'état et l'habillage Gym, en vous appuyant sur les
# fragments de la section 7.10 et sur votre lecture des trois décisions de la section
# 7.8. Vous ne recopiez aucun code existant d'agent de négociation : **l'écriture est
# l'exercice**.
#
# **Le jeu de données est fourni**, vous n'avez aucune donnée de marché à aller
# chercher.

# %% [smoke]
from sci1070.donnees import charger_prix, series_disponibles

print("séries fournies :", series_disponibles())

prix = charger_prix("synthetique-a")
print(f"{len(prix)} barres | clôture de {prix.cloture.min():.2f} à {prix.cloture.max():.2f}")

fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(prix.cloture, linewidth=0.8)
ax.set_xlabel("barre"); ax.set_ylabel("clôture")
ax.set_title("synthetique-a : la série sur laquelle vous travaillerez")
ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# Deux séries sont là pour vos assertions plutôt que pour un marché :
#
# * **`plate`** : rien ne bouge, jamais. C'est le cas de l'assertion 1, et le
#   fabriquer à la main est facile à rater (un centième de variation suffit à fausser
#   le nombre attendu).
# * **`escalier`** : une hausse de 10 % à chaque barre, sans aucun bruit. C'est le cas
#   à deux barres de la section 7.8, en version paramétrée, pour l'assertion 3.

# %% [smoke]
plate = charger_prix("plate")
escalier = charger_prix("escalier")
print("plate     : clôtures", plate.cloture[:4], "...")
print("escalier  : clôtures", np.round(escalier.cloture[:4], 3), "...")
print("escalier  : +%.0f %% par barre" % (100 * (escalier.cloture[1] / escalier.cloture[0] - 1)))

# %%
# À COMPLÉTER : la classe d'état et l'habillage Gym de la section 7.10.
# Rappels des réglages par défaut : b = 10 barres, commission kappa = 0,1 %,
# trois actions (Skip = 0, Buy = 1, Close = 2), et l'observation a 3b + 2 composantes.
#
# La décision qui fait tout le problème : c'est la POSITION dans l'état qui en fait
# un processus de décision markovien. Sans elle, deux instants aux dix mêmes barres
# exigent deux actions différentes, et la propriété de Markov est violée.
class EtatNegociation:
    ...


class EnvNegociation(gym.Env):
    ...

# %% [markdown]
# ### Les quatre assertions, et elles sont le cœur du volet
#
# Chacune tient en trois lignes et chacune attrape une classe d'erreur réelle. Je ne
# vous les donne pas écrites : les écrire **est** l'exercice.

# %%
# 1. LE COÛT DU VOYAGE.
#    Un achat suivi d'une clôture, SANS aucun mouvement de prix, rend exactement -2*kappa.
#    Si vous obtenez -kappa, vous avez oublié une jambe ; si vous obtenez 0, votre
#    commission n'est pas branchée.
...        # À COMPLÉTER, sur la série « plate »

# %%
# 2. LE RENDEMENT PUR.
#    Avec kappa = 0, un achat au prix c0 et une clôture au prix c1, sous le schéma A,
#    rendent exactement 100 * (c1 / c0 - 1).
...        # À COMPLÉTER

# %%
# 3. LES DEUX SCHÉMAS NE COÏNCIDENT PAS.
#    Appliquez les deux schémas à la MÊME trajectoire et montrez qu'ils s'accordent au
#    premier ordre et diffèrent au second. Le cas à deux barres à +10 % de la section
#    7.8, qui donne 20 points contre 21, est le test minimal ; faites-en une version
#    paramétrée et tracez l'écart en fonction de la durée de détention.
#    C'est la PREUVE que les deux schémas ne définissent pas le même objectif.
...        # À COMPLÉTER, sur la série « escalier »

# %%
# 4. LA FORME DE L'OBSERVATION.
#    Elle a exactement 3b + 2 composantes, et sa DERNIÈRE composante vaut 0 chaque
#    fois qu'aucune position n'est détenue. Vérifiez les deux, et sur plusieurs b.
...        # À COMPLÉTER

# %% [markdown]
# ### Deux extensions facultatives, et je les recommande toutes les deux
#
# **L'affichage**, qui n'est pas implémenté : tracez la série de prix de l'épisode et
# marquez dessus les achats et les clôtures. Dix lignes de Matplotlib, et vous
# obtiendrez la vue la plus informative de tout le volet.
#
# **La stratégie d'achat-conservation**, qui est la comparaison manquante de la
# section 7.12 : achetez à la première barre, ne faites rien, vendez à la dernière,
# payez deux commissions, et rapportez le profit. Vous aurez alors le point de
# comparaison qu'un lecteur attend, et vous pourrez enfin dire si un agent qui finit
# à +10 % a **créé ou détruit** de la valeur.

# %%
...        # À COMPLÉTER, facultatif

# %% [markdown]
# > **Mon message pour ce laboratoire.** Les deux volets vous enseignent le même geste
# > par deux chemins opposés. Au volet A, vous **mesurez avant de changer**. Au volet
# > B, vous **testez avant d'entraîner**. Dans les deux cas, vous refusez de lancer la
# > grosse machine avant d'avoir établi un point de référence vérifiable. C'est la
# > discipline la plus rentable de tout le métier, et c'est aussi la plus difficile à
# > tenir quand on est impatient de voir une courbe monter. Je vous le dis sans
# > détour : les étudiants qui prennent cette habitude cette semaine sont ceux qui
# > termineront le cours avec des résultats défendables.
