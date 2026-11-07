# %% [markdown]
# # SCI1070 — Semaine 12 : un seul objet, Puissance 4, tenu de bout en bout
#
# | Partie | Ce que vous y faites |
# | --- | --- |
# | Échauffement | le modèle de jeu en cinq fonctions, et trois vérifications |
# | A | la recherche, **testée sans réseau entraîné** |
# | B | l'auto-jeu complet, et le tournoi des points de contrôle |
# | C | trois constantes, et la mesure qui commande chacune |
# | D | lecture et analyse multi-agent, **aucun entraînement** |
# | Références | le joueur aléatoire, et la recherche sans entraînement |
#
# **Ce que le laboratoire ne fait pas, et je préfère une omission déclarée à une
# omission silencieuse.** Il ne vous fait pas entraîner d'agents dans un monde
# multi-agent (le paquet à cœur compilé n'a **pas** été vérifié dans une session Colab
# gratuite, et les entraînements coûtent une à deux heures de processeur graphique),
# ni reproduire la méthode à modèle appris de la section 12.6 (quinze heures pour un
# résultat qui, section 12.8, **ne converge pas**).
#
# > **Votre critère de progrès cette semaine n'est pas une perte, c'est un tournoi.**
# > Déclarez-le avant de lancer quoi que ce soit : « je sauvegarde un point de
# > contrôle à chaque promotion, et à la fin je fais jouer chaque point de contrôle
# > contre tous les autres, cent parties chacun ». Si vous déclarez à la place
# > « j'arrête quand la perte descend sous telle valeur », **vous n'arrêterez jamais**,
# > et vous passerez votre soirée à régler un pas d'apprentissage qui n'est pas en
# > cause. **C'est la première fois que ce cours vous demande d'ignorer une courbe de
# > perte, et c'est volontaire.**

# %% [smoke]
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("torch") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "torch"], check=True)
if importlib.util.find_spec("sci1070") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "git+https://github.com/FaycalZM/drl-course-teluq.git#subdirectory=code"],
                   check=True)

import collections
import math

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from sci1070.protocole import intervalle
from sci1070.graines import fixer_graines

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Les quatre constantes de la section 12.4.
N_LIGNES, N_COLONNES = 6, 7
N_ALIGNES = 4
BITS_HAUTEUR = 3          # de quoi coder une hauteur de colonne de 0 à 6

print(f"{N_LIGNES} x {N_COLONNES}, {N_ALIGNES} alignés, {BITS_HAUTEUR} bits de hauteur")

# %% [markdown]
# ---
# # Échauffement : le modèle du jeu
#
# Une heure, et il n'est pas décoratif : **tout le reste repose dessus**, et la
# section 12.4 a expliqué pourquoi ce module ne peut pas être un environnement
# ordinaire.
#
# Écrivez les **cinq fonctions** de la section 12.4 : encodage, décodage, coups
# possibles, jouer un coup, afficher.

# %%
def encoder(plateau, hauteurs) -> int:
    ...        # À COMPLÉTER


def decoder(code: int):
    ...        # À COMPLÉTER


def coups_possibles(code: int) -> list[int]:
    ...        # À COMPLÉTER


def jouer(code: int, colonne: int, joueur: int):
    """Rend (nouveau_code, partie_gagnee). Ne signale PAS le match nul."""
    ...        # À COMPLÉTER


def afficher(code: int) -> None:
    ...        # À COMPLÉTER

# %% [markdown]
# ### Les trois vérifications, dans cet ordre
#
# **1. Aller-retour.** Pour mille positions tirées au hasard en jouant des coups
# légaux, décoder puis réencoder doit redonner le **même entier**. Un encodage qui
# perd de l'information produit des **collisions de nœuds dans l'arbre**, et vous ne
# le verrez jamais autrement.

# %%
rng = np.random.default_rng(0)
code_initial = encoder(*decoder(0))

for essai in range(1000):
    ...        # À COMPLÉTER : jouer des coups légaux au hasard, et vérifier
               # assert encoder(*decoder(code)) == code

# %% [markdown]
# **2. Le match nul.** Remplissez une grille entièrement sans victoire, et vérifiez
# que votre détection de fin de partie fonctionne.
#
# **Rappel de la section 12.4 : la fonction qui joue un coup ne vous signalera pas le
# match nul**, c'est à vous de constater qu'il n'y a plus de coups possibles.

# %%
...        # À COMPLÉTER : une grille pleine sans alignement, et l'assertion

# %% [markdown]
# **3. L'horizon de coups, et vous le dérivez.** **Ne recopiez aucune expression.**
# Calculez vous-même le nombre **minimal** de coups joués pour qu'une partie puisse
# être gagnée, à partir du nombre de jetons à aligner, puis le nombre **maximal** de
# coups d'une partie, à partir de la taille du plateau.
#
# Écrivez les deux nombres dans votre carnet **avant** de choisir votre horizon, et
# justifiez votre choix en une phrase. La section 12.7 explique ce qui arrive quand on
# se trompe du mauvais côté.

# %%
coups_min = ...        # À COMPLÉTER : dérivé de N_ALIGNES, pas recopié
coups_max = ...        # À COMPLÉTER : dérivé de N_LIGNES et N_COLONNES
HORIZON = ...          # À COMPLÉTER, et justifiez-le en une phrase

print(f"minimum {coups_min} coups, maximum {coups_max} coups, horizon retenu {HORIZON}")

# %% [markdown]
# ---
# # Volet A : la recherche, testée sans réseau entraîné
#
# **Objectif.** Écrire la recherche de la section 12.3 et la **tester en isolation**,
# avant qu'un réseau ne vienne brouiller le diagnostic.
#
# **Étape 1.** Les quatre phases : sélection par l'utilité, expansion d'une feuille,
# évaluation, **remontée avec inversion de signe**. Utilisez un réseau **non entraîné**
# comme fonction d'évaluation : ses sorties sont du bruit, **et c'est très bien pour
# ce volet**.

# %%
class Recherche:
    def __init__(self, c_puct=1.0, alpha_dirichlet=0.3, utilite_amputee=False):
        self.c_puct = c_puct
        self.alpha_dirichlet = alpha_dirichlet
        self.utilite_amputee = utilite_amputee      # pour l'étape 3
        self.visites = collections.defaultdict(lambda: np.zeros(N_COLONNES))
        self.valeurs = collections.defaultdict(lambda: np.zeros(N_COLONNES))
        self.priors = {}

    def utilite(self, code):
        ...        # À COMPLÉTER : la bonne utilité, et la version amputée (sans racine
                   # carrée, sans constante) sous le drapeau `utilite_amputee`

    def rechercher(self, code, joueur, reseau, n_recherches):
        ...        # À COMPLÉTER : sélection, expansion, évaluation, remontée.
                   # L'inversion de signe à la remontée est le test nº3 ci-dessous.

# %% [markdown]
# ### Étape 2 — trois tests qui valent mieux qu'une heure d'entraînement
#
# Chacun attrape un bogue précis.

# %%
# LE TEST DU TOTAL. Après n recherches, la somme des comptages à la racine vaut
# exactement n. Moins : vous perdez des passages. Plus : vous comptez deux fois.
reseau_neuf = ...        # À COMPLÉTER : le réseau du volet B, NON entraîné
recherche = Recherche()
n = 200
recherche.rechercher(code_initial, joueur=0, reseau=reseau_neuf, n_recherches=n)
assert recherche.visites[code_initial].sum() == n, "le total des visites n'est pas n"

# %%
# LE TEST DE LA VICTOIRE IMMÉDIATE. Une position où vous gagnez en un coup : avec
# assez de recherches pour que chaque colonne soit visitée, le comptage maximal doit
# être celui du coup gagnant.
...        # À COMPLÉTER

# %%
# LE TEST DU SIGNE, et c'est celui qui attrape l'erreur de la section 12.3.
# Une position où c'est l'ADVERSAIRE qui gagne au coup suivant, quoi que vous jouiez :
# la valeur remontée à la racine doit être NÉGATIVE.
# Si elle est positive, vous avez oublié une inversion de signe, et votre agent
# jouera avec enthousiasme vers sa propre défaite.
...        # À COMPLÉTER

# %% [markdown]
# ### Étape 3, l'expérience la plus instructive du laboratoire
#
# Implémentez **volontairement** la mauvaise utilité, celle **sans racine carrée et
# sans constante**, et comparez-la à la bonne sur **une seule** mesure : le nombre de
# **colonnes distinctes visitées au moins dix fois** à la racine, après deux cents
# recherches.
#
# C'est l'avertissement de la section 12.3, reproduit dans votre code, et c'est la
# façon de ne plus jamais l'oublier.

# %%
for amputee in [False, True]:
    r = Recherche(utilite_amputee=amputee)
    r.rechercher(code_initial, 0, reseau_neuf, 200)
    distinctes = int((r.visites[code_initial] >= 10).sum())
    etiquette = "utilité amputée" if amputee else "utilité correcte"
    print(f"{etiquette:18s} : {distinctes} colonne(s) visitée(s) au moins dix fois")

# %% [markdown]
# ---
# # Volet B : l'auto-jeu, et une perte qui ne descendra pas
#
# **Étape 1 — le réseau à deux têtes.** Entrée à **deux plans** de six sur sept, un
# tronc de convolutions résiduelles, une tête de politique à **sept logits**, une tête
# de valeur à **un** flottant.
#
# **Vérifiez l'invariance au joueur** en passant la même position vue des deux camps :
# les sorties doivent être **cohérentes avec l'échange des plans**, et non identiques.

# %%
class ReseauJeu(nn.Module):
    def __init__(self, n_blocs=3, n_filtres=64):
        super().__init__()
        ...        # À COMPLÉTER : deux plans en entrée, deux têtes en sortie

    def forward(self, x):
        ...        # À COMPLÉTER : rend (logits_politique, valeur)

# %%
# La vérification d'invariance : la même position, vue des deux camps.
...        # À COMPLÉTER

# %% [markdown]
# **Étape 2 — la boucle d'auto-jeu.** Le meilleur réseau joue les deux camps,
# \(\tau = 1\) pour les premiers coups puis \(\tau = 0\), les triplets partent dans le
# tampon, et **le résultat est retourné en remontant l'historique**.
#
# Réglages économiques de la section 12.5 : **dix** recherches par coup, **huit**
# feuilles par passage de réseau.

# %%
def jouer_une_partie(reseau, recherche, tau_coups=10, n_recherches=10):
    """Rend la liste des triplets (etat, politique_cible, resultat)."""
    ...        # À COMPLÉTER.
               # PIÈGE Nº1 : si vous ne retournez pas le résultat en remontant
               # l'historique, la moitié de vos cibles de valeur ont le signe inverse
               # et votre tête de valeur apprend zéro partout.

# %% [markdown]
# **Étape 3 — la porte.** Cent parties contre le meilleur réseau, promotion au-dessus
# de **soixante pour cent**, point de contrôle enregistré à chaque promotion.
# **Comptez les promotions : c'est votre instrument le plus utile.**

# %%
import copy

def porte(apprenti, meilleur, recherche, n_parties=100, seuil=0.60):
    """Rend (taux_de_victoire, promu). La copie des poids est le piège nº3."""
    ...        # À COMPLÉTER
               # PIÈGE Nº3 : si vous promouvez en gardant une RÉFÉRENCE au même objet,
               # apprenti et meilleur deviennent le même réseau, l'auto-jeu continue
               # de tourner, et la porte s'ouvre désormais au hasard.
               # copy.deepcopy, ou load_state_dict sur un objet distinct.

# %% [markdown]
# **Étape 4.** Lancez une heure, et visez environ **2 500 parties** d'auto-jeu.
#
# Pendant que cela tourne, tracez trois choses et **prédisez-les avant de les
# regarder** : la perte totale, le taux de victoire de l'apprenti, et le nombre cumulé
# de promotions.
#
# **Deux des trois courbes vous diront la vérité et une vous mentira.** Notez vos
# prédictions maintenant.

# %%
# Prédiction, perte totale          : ...
# Prédiction, taux de victoire      : ...
# Prédiction, promotions cumulées   : ...

...        # À COMPLÉTER : la boucle d'une heure, et les trois courbes

# %% [markdown]
# **Étape 5, le tournoi.** Faites jouer vos points de contrôle les uns contre les
# autres, cent parties par couple, et dressez le tableau. **C'est votre seule mesure
# de progrès valide.**
#
# Dites en une phrase si l'ordre du tournoi suit l'ordre chronologique, et commentez
# les exceptions.

# %%
...        # À COMPLÉTER : la matrice du tournoi

# %% [markdown]
# **Étape 6, la récompense.** Jouez contre votre réseau, **à la main**, dans le
# terminal. Attendez-vous au niveau annoncé en section 12.5 : en dessous de celui d'un
# enfant, une stratégie rudimentaire, une erreur grossière un coup sur deux.
#
# Notez **trois** erreurs qu'il commet, et dites pour chacune si vous pensez qu'elle
# vient **du réseau** ou **du nombre de recherches**.

# %%
...        # À COMPLÉTER : la boucle de jeu interactive

# %% [markdown]
# > **Quatre pièges de ce volet, et chacun coûte une soirée.**
# >
# > 1. **Le signe du résultat dans les triplets.** Sans retournement en remontant
# >    l'historique, votre tête de valeur apprend zéro partout.
# > 2. **Le masquage des coups illégaux après l'argmax** au lieu d'avant : vos indices
# >    se décalent et votre agent joue un coup pour un autre.
# > 3. **La promotion sans copie des poids.**
# > 4. **Le match nul non détecté** : votre boucle d'auto-jeu tournera indéfiniment
# >    sur une grille pleine.

# %% [markdown]
# ---
# # Volet C : trois constantes, et ce que chacune commande
#
# **Objectif. Cesser de traiter un hyperparamètre comme un nombre magique.**

# %% [markdown]
# **Étape 1, la constante d'exploration.** Faites varier \(c_{\text{puct}}\) sur trois
# valeurs séparées par un facteur dix. Mesurez, pour chacune, le nombre de colonnes
# distinctes explorées à la racine **et** le niveau du réseau obtenu après vingt
# minutes, sur trois graines.
#
# Dites laquelle est la meilleure **pour cette mesure-là**, et rappelez-vous la leçon
# de la semaine 11 sur les classements locaux.

# %%
for c in [0.1, 1.0, 10.0]:
    ...        # À COMPLÉTER : les deux mesures, sur trois graines

# %% [markdown]
# **Étape 2, la concentration de Dirichlet.** Comparez \(\alpha_{\mathrm{Dir}} = 0{,}03\)
# et \(0{,}3\) sur sept colonnes, et faites-le d'abord **sans aucun entraînement** :
# tirez mille vecteurs pour chacune, et pour chacun calculez le **poids maximal** du
# vecteur. Donnez la moyenne de ces maximums.
#
# Vous allez voir, **en trois lignes de code**, pourquoi un tirage à concentration
# trop faible est presque unitaire, et pourquoi cela ne fait pas du tout ce que le
# bruit de racine est censé faire.

# %% [smoke]
rng = np.random.default_rng(0)
for alpha in [0.03, 0.3]:
    tirages = rng.dirichlet(np.full(N_COLONNES, alpha), size=1000)
    print(f"alpha = {alpha:5.2f} : poids maximal moyen {tirages.max(axis=1).mean():.3f}")
print("\n-> à 0,03 le vecteur est presque unitaire : il DÉSIGNE une colonne")
print("   au lieu de perturber doucement les sept, ce qui n'est pas le rôle")
print("   du bruit de racine.")

# %% [markdown]
# **Étape 3, votre horizon.** Reprenez le nombre dérivé à l'échauffement, et vérifiez
# **expérimentalement** qu'aucune de vos parties d'auto-jeu n'est coupée avant la fin.
#
# Comptez les parties tronquées par l'horizon : **si ce compteur n'est pas nul**, votre
# horizon est trop court et une partie de vos cibles de valeur ne correspond à aucun
# résultat réel.

# %%
...        # À COMPLÉTER : le compteur de parties tronquées, qui doit valoir zéro

# %% [markdown]
# **Étape 4.** **Une phrase de conclusion par constante**, dans votre carnet, de la
# forme « cette constante commande *telle grandeur du problème*, et on la règle en
# regardant *telle mesure* ». **C'est l'objectif réel du volet.**

# %% [markdown]
# ---
# # Volet D : lecture et analyse d'un monde multi-agent
#
# **Aucun calcul lourd** : de la lecture, deux divisions et de l'écriture. Ce volet
# exerce, sur un cas réel, le jugement des sections 12.9 à 12.11.
#
# **Question 1, l'interface.** Reprenez la boucle d'épisode de la section 12.10 et
# dites, en **trois phrases**, ce qui empêche d'y brancher une enveloppe
# d'environnement ordinaire. Puis réécrivez la boucle de la semaine 5 que vous avez
# déjà, et **marquez d'un commentaire chaque ligne** qu'il faudrait changer.
#
# **Question 2, la population volatile.** Un agent meurt au pas 37 d'un épisode qui en
# compte 300. Dites précisément ce qui arrive à ses entrées dans les cinq
# dictionnaires **au pas 37**, puis **au pas 38**, et ce que votre tampon de rejeu doit
# ranger dans chacun des deux cas. Puis dites ce qui **casse** si vous itérez sur la
# liste des agents sans la figer.
#
# **Question 3, l'observation.** Une politique partagée sert deux groupes opposés.
# Dites quel choix d'encodage rend cela possible, et **où ce cours a déjà utilisé le
# même procédé, dans une section précédente de cette semaine**. Puis dites ce que
# cette politique partagée **interdit** aux agents d'un même groupe.
#
# **Question 4, l'arithmétique.** À partir des quatre nombres de la section 12.10,
# refaites le calcul des cent cinquante-cinq proies chassées, et dites **quelle
# hypothèse sur la récompense le rend possible**. Puis refaites-le pour un score de
# test de **60** au lieu de 82, et dites si la conclusion **change de nature**.
#
# **Question 5, et c'est la question qui compte.** Un rapport affirme que des agents
# ont « appris à collaborer » parce qu'ils chassent par deux. Rédigez, en un
# paragraphe, la réponse de la section 12.11 : ce qui est **certain**, ce qui est
# **observé**, d'où vient chaque affirmation, et **la question unique qu'il faut poser
# pour trancher**.
#
# **Question 6.** Deux courbes sans tendance, l'une venant d'un entraînement par
# auto-jeu et l'autre d'un entraînement de deux groupes simultanés. Dites en quoi les
# **causes** diffèrent, et ce qui, dans chaque cas, serait ou ne serait pas une
# réponse technique utile.

# %%
# Vos six réponses, dans ce carnet. Ce volet n'exécute rien, et c'est voulu.
...

# %% [markdown]
# ---
# # Il n'y a pas de solution courte cette semaine, et c'est intéressant
#
# Les bibliothèques de haut niveau que ce cours emploie sont construites autour d'une
# interface d'environnement **à un seul agent**, avec un `reset()` et un `step()`. Or
# **rien de cette semaine n'est un environnement de ce genre** : la première moitié a
# besoin d'un modèle de jeu **interrogeable depuis un état arbitraire**, ce que cette
# interface interdit, et la seconde moitié rend **cinq dictionnaires** au lieu de cinq
# valeurs. C'est la section 12.4, vécue depuis l'outillage.

# %%
# Deux adversaires de reference, a battre avant de se rejouir de quoi que ce soit.
#
# 1. Le joueur aleatoire : il joue une colonne legale au hasard.
#    Votre reseau entraine doit le battre de maniere ecrasante. S'il ne le
#    fait pas, ne reglez rien : relisez vos trois tests du volet A.
#
# 2. La recherche seule, avec votre reseau NON entraine.
#    Dix recherches par coup, un reseau aux poids initiaux. C'est exactement
#    l'etat de votre systeme a l'episode zero, et c'est le bon point de
#    comparaison pour une heure d'entrainement : il mesure ce que
#    l'entrainement a ajoute, et non ce que la recherche faisait deja.

...        # À COMPLÉTER : les deux matchs, cent parties chacun

# %% [markdown]
# > **Le second adversaire est le plus intéressant des deux, et c'est une mesure que
# > l'on oublie presque toujours.** Une recherche arborescente, même avec un réseau
# > complètement aléatoire, **joue déjà quelque chose** : elle détecte les victoires
# > et les défaites immédiates, parce que celles-ci sont des états **terminaux**,
# > évalués par le résultat réel de la partie et non par le réseau. Une partie de la
# > force de votre système final vient donc de la **recherche** et non de
# > l'entraînement. **Si vous ne mesurez pas cela, vous attribuerez à votre réseau un
# > mérite qui revient à votre arbre.**
