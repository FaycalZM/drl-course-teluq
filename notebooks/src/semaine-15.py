# %% [markdown]
# # SCI1070 — Semaine 15 : caractériser un problème, et le dire honnêtement
#
# | Application | Statut dans ce cours |
# | --- | --- |
# | **Le marché** | **déjà fait**, en semaine 7. Cette semaine le relit et ne le refait pas |
# | **Le paragraphe** | **s'exécute**, avec trois réserves (plateforme, versions, paiement) |
# | **La page rendue** | **facultative, non notée, hors du carnet** : il faut un navigateur piloté |
# | **La permutation** | **démonstration seulement** : six jours de calcul pour l'entraînement d'origine |
#
# > **Pourquoi ce tableau est en tête du laboratoire et non en note de bas de page.**
# > Pendant treize semaines, ce cours a distingué ce qui s'exécute de ce qui se
# > raconte, et vous a dit **chaque fois** de quel côté vous étiez. Une dernière
# > semaine qui annoncerait quatre laboratoires exécutables et n'en livrerait aucun
# > annulerait ce travail d'un coup. Il y a **un** volet qui tourne de bout en bout,
# > **un** volet de démonstration où vous lisez des mesures fournies, et **deux**
# > volets facultatifs. **C'est l'état réel des choses, et le savoir fait partie de ce
# > que cette semaine enseigne.**

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium>=1.0", "gymnasium"), ("torch", "torch")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)
if importlib.util.find_spec("sci1070") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "git+https://github.com/FaycalZM/drl-course-teluq.git#subdirectory=code"],
                   check=True)

import numpy as np
import torch
import matplotlib.pyplot as plt

print("prêt")

# %% [markdown]
# ---
# # Volet A : mesurer ce qu'une liste de commandes admissibles fait à un problème
#
# **C'est le volet principal, le seul qui tourne de bout en bout, et il est court.** Il
# ne contient **aucun entraînement**, et c'est voulu : la semaine porte sur la
# **caractérisation d'un problème**, pas sur l'optimisation d'un agent.
#
# > **Réserve de plateforme, et elle est réelle.** Le paquet ne prend en charge que
# > Linux et macOS. Il s'installe dans Colab **parce que Colab tourne sous Linux** ;
# > sur une machine Windows il demande un conteneur. Il tourne donc dans le carnet et
# > **pas forcément sur votre machine**.

# %%
# Plusieurs paquets de la chaîne sont épinglés : si vous changez une version, vous
# changez d'expérience.
if sys.platform.startswith("linux") or sys.platform == "darwin":
    if importlib.util.find_spec("textworld") is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "textworld"],
                       check=True)
    import textworld
    import textworld.gym
    print("textworld disponible")
else:
    print(f"plateforme {sys.platform} : le paquet ne s'installe pas ici.")
    print("Ouvrez ce carnet dans Colab pour le volet A.")

# %% [markdown]
# **Étape 1 — engendrer un jeu.** Une quête de **longueur 5**, avec une graine fixée
# **et notée**. Fixez aussi le thème et le scénario, et écrivez dans votre carnet les
# **cinq paramètres** que vous avez choisis : c'est votre protocole, et **sans lui
# votre mesure de l'étape 4 ne sera comparable à rien**.

# %%
# Mes cinq paramètres, notés avant de lancer :
#   graine     : ...
#   longueur   : 5
#   thème      : ...
#   scénario   : ...
#   options    : ...
...        # À COMPLÉTER : engendrer le jeu

# %% [markdown]
# **Étape 2 — écrire l'adaptateur, et c'est la pièce qui prend le plus de temps.**
#
# L'environnement renvoie **quatre** valeurs au lieu des cinq que Gymnasium attend, et
# **ne déclare ni espace d'observations ni espace d'actions**.
#
# **Documentez en commentaire la décision que vous avez prise** sur l'indicateur de
# troncature manquant : le mettez-vous toujours à faux, ou le déduisez-vous d'un
# compteur de pas que vous tenez vous-même ? **Les deux choix sont défendables, et le
# non-choix n'en est pas un.**

# %%
# Ma décision sur `tronque`, et pourquoi : ...
class AdaptateurTexte:
    """Enveloppe un environnement textuel pour qu'il ressemble à du Gymnasium."""

    def __init__(self, env):
        ...        # À COMPLÉTER

    def reset(self, seed=None, options=None):
        ...        # À COMPLÉTER : rendre (obs, info)

    def step(self, action):
        ...        # À COMPLÉTER : rendre CINQ valeurs


# Testez sur un épisode complet joué au hasard, et vérifiez qu'il termine.
...        # À COMPLÉTER

# %% [markdown]
# **Étape 3 — inspecter ce que l'environnement accepte de montrer.** Demandez les
# champs d'information un par un et affichez-les pour **trois états successifs** :
# description de la pièce, inventaire, nom du lieu, faits du monde, dernière action,
# commandes admissibles, suite d'actions gagnante.
#
# **Répondez à une question en une phrase : lesquels de ces champs un environnement
# industriel vous donnerait-il ?**

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Étape 4 — la mesure du volet.** Pour chacun des **vingt premiers états** traversés,
# comptez la longueur de la liste de commandes admissibles. Puis calculez, et
# comparez, **trois** nombres : la taille de l'espace de production par pas, soit
# \(1250^8\) ; la **médiane** de vos longueurs ; et **le rapport des deux**.

# %% [smoke]
# L'espace de production, pour avoir l'ordre de grandeur sous les yeux avant de mesurer.
espace_production = 1250 ** 8
print(f"espace de production par pas : 1250^8 = {espace_production:.3e}")

# Le rapport que vous calculerez, pour une médiane plausible d'une douzaine :
for mediane in [5, 12, 30]:
    print(f"  médiane {mediane:3d} -> rapport ~ 10^{np.log10(espace_production / mediane):.1f}")

# %%
longueurs = []
...        # À COMPLÉTER : les vingt premiers états

plt.hist(longueurs, bins=15)
plt.xlabel("longueur de la liste de commandes admissibles")
plt.ylabel("nombre d'états")
plt.show()

print("médiane :", np.median(longueurs))
print(f"rapport : 10^{np.log10(espace_production / np.median(longueurs)):.1f}")

# %% [markdown]
# **Étape 5 — l'autre béquille.** Activez la **récompense intermédiaire** et rejouez
# le même épisode au hasard, en journalisant la récompense à chaque pas. Comparez le
# nombre de pas récompensés avec et sans.
#
# **Dites en deux phrases lequel des deux réglages, la liste admissible ou la
# récompense intermédiaire, change la *classe* du problème, et lequel ne change que sa
# *difficulté*.**

# %%
...        # À COMPLÉTER

# %% [markdown]
# **Ce que ce volet établit** : que la réduction d'espace d'actions est **mesurable,
# et de combien**. **Ce qu'il n'établit pas** : quoi que ce soit sur la performance
# d'un agent, puisque vous n'en entraînez aucun. **Dites-le dans votre conclusion.**

# %% [markdown]
# ---
# # Volet B : lire une divergence, et poser l'ancre qui la répare
#
# Volet de **démonstration**. Vous n'entraînez rien : vous recevez des journaux et
# vous les lisez. C'est le volet qui vous prépare le plus directement à la lecture
# critique que les livrables finaux demandent.

# %% [smoke]
from sci1070.donnees import charger_journal, journaux_disponibles

print("journaux fournis :", journaux_disponibles())

journal = charger_journal("cube-sans-ancre")
print(journal.description)
print(f"{len(journal.pas)} points, de {journal.pas[0]} à {journal.pas[-1]} pas de gradient")

# %% [markdown]
# **Étape 1 — le diagnostic.** Tracez les **deux** pertes fournies, politique et
# valeur, **sur le même axe de temps**.
#
# Puis répondez à trois questions : à quel moment la perte de **valeur** quitte-t-elle
# son plateau, que fait la perte de **politique** à ce moment-là, et **laquelle des
# deux courbes aurait déclenché une alerte si vous n'aviez surveillé qu'elle** ?

# %% [smoke]
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(journal.pas, journal.perte_politique, label="perte de politique")
ax.plot(journal.pas, journal.perte_valeur, label="perte de valeur")
ax.set_yscale("log")
ax.set_xlabel("pas de gradient"); ax.set_ylabel("perte")
ax.legend(); ax.grid(alpha=0.3)
ax.set_title(journal.titre)
plt.show()

# %%
# Vos trois réponses :
#   1. la perte de valeur quitte son plateau vers le pas ...
#   2. au même moment, la perte de politique ...
#   3. celle qui aurait déclenché une alerte : ...
...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — l'explication, et elle s'écrit sans code.** En trois ou quatre phrases :
# pourquoi la cible de valeur de la section 15.5 **ne fixe aucune échelle**, et
# pourquoi **l'état résolu est le seul endroit de l'espace où une valeur est connue**.
#
# **Mentionnez la semaine 14** : c'est le même mécanisme sur un autre objet.

# %% [markdown]
# **Étape 3 — le correctif, écrit comme une fonction pure.** Implémentez les **deux**
# variantes de la cible de valeur, celle de la section 15.5 et celle de la section
# 15.7, comme deux fonctions prenant les valeurs des enfants, les indicateurs de but,
# et un booléen disant si l'état courant est résolu.
#
# **N'entraînez rien.** Évaluez les deux sur **trois cas construits à la main** : un
# état loin du but, un état à une rotation du but, et **l'état résolu lui-même**.
#
# Montrez **numériquement** que les deux fonctions coïncident sur les deux premiers et
# **diffèrent sur le troisième**.

# %%
def cible_sans_ancre(valeurs_enfants, indicateurs_but, est_resolu):
    """La cible de la section 15.5. Aucune échelle n'y est fixée."""
    ...        # À COMPLÉTER


def cible_avec_ancre(valeurs_enfants, indicateurs_but, est_resolu):
    """La cible de la section 15.7. L'état résolu ancre l'échelle."""
    ...        # À COMPLÉTER


cas = {
    "loin du but":        (torch.tensor([0.1, 0.2, 0.05]), torch.tensor([0., 0., 0.]), False),
    "à une rotation":     (torch.tensor([0.1, 0.9, 0.05]), torch.tensor([0., 1., 0.]), False),
    "l'état résolu":      (torch.tensor([0.3, 0.3, 0.30]), torch.tensor([0., 0., 0.]), True),
}

for nom, (v, g, resolu) in cas.items():
    a = float(cible_sans_ancre(v, g, resolu))
    b = float(cible_avec_ancre(v, g, resolu))
    marque = "DIFFÈRENT" if abs(a - b) > 1e-9 else "coïncident"
    print(f"{nom:18s} sans ancre {a:8.4f} | avec ancre {b:8.4f}   {marque}")

# %% [markdown]
# **Étape 4 — la lecture des mesures fournies.** Les deux tableaux de la section 15.7
# donnent les résultats sur le cube deux par deux et sur le trois par trois.
#
# Écrivez **trois phrases** : ce que le correctif a amélioré, **de combien**, et
# pourquoi la **profondeur 13 ne doit pas être comparée directement à la profondeur de
# brouillage de 1 000** du protocole publié. **La troisième phrase est celle qui
# compte**, et c'est la section 15.8 qui vous en donne les mots.

# %% [markdown]
# **Ce que ce volet établit** : que vous savez diagnostiquer une fonction de valeur
# sans ancre et écrire le correctif. **Ce qu'il n'établit pas** : que le correctif
# résout le problème, puisque la mesure fournie montre justement **qu'il ne le résout
# pas sur le cube complet**.

# %% [markdown]
# ---
# # Volet C : facultatif et non noté, et il demande un navigateur
#
# **Ce volet ne tourne pas dans un carnet, et il n'est pas noté.** Je le propose parce
# qu'il contient la mesure la plus frappante de la semaine et qu'elle se refait en
# cinq minutes sur une machine de bureau.
#
# **Prérequis, et ils sont réels.** Une installation locale, un navigateur, un binaire
# de pilotage **dont la version correspond à celle du navigateur**, et le paquet du
# jeu de référence. **Si l'une des quatre conditions manque, passez ce volet : il
# n'enlève rien à votre évaluation.**

# %%
# À exécuter sur votre machine de bureau, pas ici.
#
# Étape 1 : sur la tâche de clic élémentaire, émettez le MÊME clic correct deux fois,
#           une fois avec le navigateur dessiné à l'écran, une fois sans interface.
#           Journalisez les TROIS valeurs : récompense fournie, récompense brute,
#           temps écoulé.
#
# Étape 2 : répétez chaque condition dix fois, et donnez moyenne et écart des deux
#           récompenses fournies. Vous devez obtenir DEUX POPULATIONS QUI NE SE
#           RECOUVRENT PAS, pour une récompense brute identique.
...        # À COMPLÉTER, hors carnet

# %% [markdown]
# **Étape 3, et c'est la question du volet.** En deux phrases : **qu'est-ce qu'un
# score publié sur ce jeu de référence mesure exactement**, et **que faudrait-il
# publier à côté pour qu'il soit comparable** ?

# %% [markdown]
# ---
# # Volet D : la lecture, et elle ne demande ni machine ni paiement
#
# Rien à exécuter. La transcription de la section 15.9 est dans la page : le
# dispositif, les cinq commandes de la partie résolue, le compte de **neuf sur vingt**,
# les quatre catégories d'échec et le coût.
#
# **Ce que je vous demande**, et c'est un exercice d'**écriture** plutôt que de code :
#
# 1. Rédigez **un paragraphe de dix lignes** qui rapporte ce résultat **honnêtement**.
#    Il doit contenir le chiffre, le protocole, les **quatre réserves** de la section
#    15.9, et la conclusion que le résultat autorise.
# 2. Rédigez le même paragraphe **malhonnêtement**, c'est-à-dire **en gardant tous les
#    chiffres exacts** mais en omettant ce qu'il faut pour que la conclusion paraisse
#    plus large qu'elle n'est.
#
# Mettez les deux côte à côte et **gardez-les**. C'est le meilleur entraînement que je
# connaisse à la relecture de son propre rapport, et **c'est le dernier exercice que
# ce cours vous propose**.

# %% [markdown]
# ---
# ## Pas de solution courte cette semaine, et c'est délibéré
#
# Les quatorze semaines précédentes se terminaient sur une solution courte de
# bibliothèque. Cette semaine n'en a pas, pour une raison qui est elle-même
# l'enseignement de la semaine : **aucune bibliothèque ne caractérise un problème à
# votre place.**
#
# Il n'existe pas de fonction qui vous dise de quelle nature est votre action, qui a
# écrit votre récompense, et laquelle des quatorze semaines s'applique. **C'est le
# seul travail de ce cours qui ne s'automatise pas, et c'est pour cela qu'il est la
# dernière chose qu'il vous apprend.**
