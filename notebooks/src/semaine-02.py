# %% [markdown]
# # SCI1070 — Semaine 2 : l'instrument, et comment le régler
#
# Un seul carnet, trois niveaux, et un fil unique : **construire le réseau des
# semaines 4 à 15, et le regarder apprendre**.
#
# | Section du cours | Ce que vous y faites |
# | --- | --- |
# | 2.3 | rejouer la session autograd, et voir la contagion de `requires_grad` |
# | 2.5 | faire tourner la boucle d'entraînement en huit lignes |
# | Laboratoire, niveau 1 | le réseau en forme de \(Q(s,a)\), la boucle, TensorBoard |
# | Laboratoire, niveau 2 | sigmoïde, symétrie, Xavier, abandon de neurones |
# | Laboratoire, niveau 3 | le même réseau en convolutif |
#
# Le réseau a la forme de \(Q(s,a)\) : une entrée qui est un vecteur d'état, **une
# sortie par action**, scores bruts sans softmax. Les cibles, elles, sont fournies,
# fixes et parfaitement sages — nous faisons de la régression. D'où viennent les
# vraies cibles d'un réseau de valeurs est la question des semaines 4 et 5, et je
# vous demande de la laisser de côté aujourd'hui.
#
# **Trois règles partout :** un seul `torch.device` construit au début du carnet, un
# `item()` sur toute valeur journalisée, un `zero_grad()` par lot.
#
# Budget de calcul : **quelques minutes au total**, processeur graphique facultatif.

# %% [smoke]
import importlib.util
import subprocess
import sys

for paquet, module in [("torch", "torch"), ("tensorboard", "tensorboard")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# Un seul device, construit ici, utilisé partout. C'est la première des trois règles.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("torch", torch.__version__, "| device", device)

# %% [markdown]
# ---
# ## Section 2.3 — la session autograd
#
# Quatre choses à regarder, et la troisième est celle qui surprend : **`requires_grad`
# est contagieux**. Un tenseur calculé à partir d'un tenseur qui demande un gradient
# en demande un aussi, sans que vous l'ayez dit.

# %% [smoke]
v1 = torch.tensor([1.0, 1.0], requires_grad=True)
v2 = torch.tensor([2.0, 2.0])

v_sum = v1 + v2              # tensor([3., 3.], grad_fn=<AddBackward0>)
v_res = (v_sum * 2).sum()    # tensor(12., grad_fn=<SumBackward0>)

print("feuilles      :", v1.is_leaf, v2.is_leaf, "| non-feuilles :", v_sum.is_leaf, v_res.is_leaf)
print("requires_grad :", v1.requires_grad, v2.requires_grad, "| contagion :", v_sum.requires_grad)

v_res.backward()

print("v1.grad :", v1.grad)      # tensor([2., 2.])
print("v2.grad :", v2.grad)      # vide : v2 n'a jamais demandé de gradient

# %% [markdown]
# **Vérifiez le 2 à la main.** \(v_{res} = \sum 2(v_1 + v_2)\), donc
# \(\partial v_{res} / \partial v_1 = 2\) pour chaque composante. Le chiffre que
# PyTorch imprime est celui que vous auriez dérivé au crayon, et c'est la seule
# façon de faire confiance à un gradient : le vérifier une fois sur un cas trivial.

# %% [markdown]
# ---
# ## Section 2.5 — la boucle en huit lignes
#
# Les huit lignes ci-dessous sont **toute** la boucle d'entraînement de PyTorch. Elles
# ne changeront plus jusqu'à la semaine 15 ; seul le contenu des cibles changera.
#
# La démonstration tourne ici sur un réseau volontairement trivial, pour qu'elle soit
# exécutable tout de suite : le réseau en forme de \(Q(s,a)\) est l'exercice 2.A, et
# il vous attend plus bas.

# %% [smoke]
demo = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 2)).to(device)
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(demo.parameters(), lr=1e-3)

g = torch.Generator().manual_seed(0)
lots = [(torch.randn(32, 4, generator=g), torch.randn(32, 2, generator=g)) for _ in range(20)]

for batch_x, batch_y in lots:                                       # 1
    batch_x_t = batch_x.to(device)                                  # 2
    batch_y_t = batch_y.to(device)                                  # 3

    out_t = demo(batch_x_t)                                         # 4
    loss_t = loss_function(out_t, batch_y_t)                        # 5
    loss_t.backward()                                               # 6
    optimizer.step()                                                # 7
    optimizer.zero_grad()                                           # 8

print(f"perte du dernier lot : {loss_t.item():.4f}")

# %% [markdown]
# **Retenez l'ordre des lignes 6, 7 et 8**, parce que l'exercice 2.B vous le
# redemandera sans les numéros. Et notez le `.item()` de la dernière ligne : c'est la
# deuxième des trois règles. Journaliser `loss_t` au lieu de `loss_t.item()` garde
# vivant tout le graphe de calcul du lot, et votre mémoire s'en va en quelques
# centaines d'itérations.

# %% [markdown]
# ---
# # Laboratoire — Niveau 1 : implémentation guidée
#
# **Objectif.** Écrire le réseau, la boucle, et l'instrumentation. À la fin de ce
# niveau, vous avez une courbe de perte qui descend dans TensorBoard.

# %% [markdown]
# ### Exercice 2.A — le réseau de la forme de \(Q(s,a)\)
#
# Trois trous à combler.

# %%
class ReseauQ(nn.Module):
    def __init__(self, n_obs: int, n_actions: int, n_cache: int = 64):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            ...,                      # À COMPLÉTER : sans ceci, les trois couches n'en font qu'une
            nn.Linear(n_cache, n_cache),
            nn.ReLU(),
            ...,                      # À COMPLÉTER : la couche de sortie, et pas de softmax
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return ...                    # À COMPLÉTER : un seul appel suffit


net = ReseauQ(n_obs=4, n_actions=2).to(device)
print(net)
print(net(torch.randn(8, 4, device=device)).shape)   # attendu : torch.Size([8, 2])

# %% [markdown]
# ### Exercice 2.B — les données et la boucle
#
# Les cibles sont fabriquées par une fonction fixe **que je vous donne**, et qui n'a
# rigoureusement aucun sens physique : c'est volontaire, elle est là pour être non
# linéaire et reproductible.

# %% [smoke]
def fabriquer_donnees(n: int, graine: int = 0):
    """n états à 4 composantes, et 2 cibles par état. Rien d'autre qu'une régression."""
    g = torch.Generator().manual_seed(graine)
    x = torch.randn(n, 4, generator=g)
    y = torch.stack([
        torch.sin(x[:, 0]) + 0.5 * x[:, 2],
        torch.cos(x[:, 1]) - 0.5 * x[:, 3],
    ], dim=1)
    return x, y


x_train, y_train = fabriquer_donnees(4096, graine=0)
x_valid, y_valid = fabriquer_donnees(1024, graine=1)
print(x_train.shape, y_train.shape, "|", x_valid.shape, y_valid.shape)

# %%
loss_function = ...        # À COMPLÉTER : la perte de régression de la section 2.5
optimizer = ...            # À COMPLÉTER : Adam sur les paramètres du réseau, lr = 1e-3

for epoque in range(30):
    for debut in range(0, len(x_train), 64):
        batch_x_t = x_train[debut:debut + 64].to(device)
        batch_y_t = y_train[debut:debut + 64].to(device)

        out_t = net(batch_x_t)
        loss_t = loss_function(out_t, batch_y_t)
        ...                # À COMPLÉTER : les trois lignes qui manquent, dans le bon ordre

# %% [markdown]
# ### Exercice 2.C — l'instrumentation
#
# Ajoutez un `SummaryWriter`, enregistrez `perte/entrainement` à chaque lot et
# `perte/validation` à chaque époque, puis ouvrez TensorBoard. Nommez l'exécution
# avec `comment=`.

# %%
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(comment="-niveau1")

pas = 0
for epoque in range(30):
    net.train()
    for debut in range(0, len(x_train), 64):
        batch_x_t = x_train[debut:debut + 64].to(device)
        batch_y_t = y_train[debut:debut + 64].to(device)

        out_t = net(batch_x_t)
        loss_t = loss_function(out_t, batch_y_t)
        ...                # À COMPLÉTER : les trois mêmes lignes qu'à l'exercice 2.B

        writer.add_scalar("perte/entrainement", loss_t.item(), pas)   # le .item() : règle 2
        pas += 1

    net.eval()
    with torch.no_grad():
        perte_valid = loss_function(net(x_valid.to(device)), y_valid.to(device))
    writer.add_scalar("perte/validation", perte_valid.item(), epoque)

writer.close()

# %%
# Dans Colab, ces deux lignes ouvrent TensorBoard dans le carnet lui-même.
%load_ext tensorboard
%tensorboard --logdir runs

# %% [markdown]
# **Attentes du niveau 1.**
#
# * `print(net)` affiche bien **cinq** blocs : trois couches linéaires et deux
#   activations. Si vous n'en voyez que trois, vous avez oublié l'activation de
#   l'exercice 2.A, et la suite du laboratoire sera instructive pour une mauvaise
#   raison.
# * La sortie a la forme `[8, 2]` : **deux** valeurs par état, une par action, et la
#   dimension 0 est celle du lot.
# * La perte d'entraînement descend franchement sur les premières époques, puis
#   ralentit. La perte de validation suit, à un léger décalage près : vous venez de
#   voir un écart de généralisation, **mesuré et non raconté**.
# * Si la perte reste obstinément plate, vérifiez dans cet ordre : l'activation
#   manquante, l'ordre des trois lignes de la boucle, le `zero_grad()`.

# %% [markdown]
# ---
# # Laboratoire — Niveau 2 : hyperparamètres et sensibilité
#
# **Objectif.** Reproduire, sur votre propre courbe, trois résultats que vous venez de
# lire. Quatre exécutions comparées dans TensorBoard, et une phrase de conclusion
# pour chacune.
#
# Pour que les quatre exécutions soient comparables, enfermez l'entraînement dans une
# fonction et ne changez **qu'une chose** d'un appel à l'autre.

# %%
def entrainer(construire_reseau, epoques: int = 30, comment: str = "", graine: int = 0):
    """Entraîne un réseau fourni par `construire_reseau()` et rend les deux courbes."""
    torch.manual_seed(graine)
    reseau = construire_reseau().to(device)
    perte = nn.MSELoss()
    optim = torch.optim.Adam(reseau.parameters(), lr=1e-3)

    courbe_train, courbe_valid = [], []
    for epoque in range(epoques):
        reseau.train()
        pertes = []
        for debut in range(0, len(x_train), 64):
            bx = x_train[debut:debut + 64].to(device)
            by = y_train[debut:debut + 64].to(device)
            l = perte(reseau(bx), by)
            l.backward()
            optim.step()
            optim.zero_grad()
            pertes.append(l.item())
        courbe_train.append(float(np.mean(pertes)))

        reseau.eval()
        with torch.no_grad():
            courbe_valid.append(perte(reseau(x_valid.to(device)), y_valid.to(device)).item())

    return reseau, np.array(courbe_train), np.array(courbe_valid)

# %% [markdown]
# ### 1. Remplacer ReLU par la sigmoïde, partout, sans rien changer d'autre
#
# Relevez le nombre d'époques nécessaires pour atteindre la perte que ReLU atteint en
# **dix** époques. Rapprochez votre observation du chiffre **0,25** de la section 2.2 :
# avec trois couches, le gradient qui arrive à la première est multiplié par trois
# facteurs inférieurs à 0,25.

# %%
def reseau_relu():
    return ...        # À COMPLÉTER : votre ReseauQ de l'exercice 2.A


def reseau_sigmoide():
    return ...        # À COMPLÉTER : le même, ReLU remplacée par nn.Sigmoid()


_, train_relu, _ = entrainer(reseau_relu, comment="-relu")
_, train_sig, _ = entrainer(reseau_sigmoide, comment="-sigmoide")

cible = train_relu[9]       # la perte que ReLU atteint en dix époques
atteint = np.argmax(train_sig <= cible) if (train_sig <= cible).any() else None
print(f"ReLU à 10 époques : {cible:.4f}")
print(f"la sigmoïde l'atteint à l'époque : {atteint}")

# %% [markdown]
# ### 2. Briser la brisure de symétrie
#
# Initialisez **tous** les poids d'une couche cachée à la même constante, par exemple
# 0,1, et entraînez. Puis affichez, après entraînement, les poids de cette couche.
# Que constatez-vous, et **combien d'unités distinctes** votre couche de 64 unités
# contient-elle réellement ?

# %%
def reseau_constant():
    reseau = ...          # À COMPLÉTER : votre ReseauQ
    # À COMPLÉTER : mettre tous les poids d'une couche cachée à 0.1
    return reseau


reseau, train_cst, _ = entrainer(reseau_constant, comment="-constant")

# Une façon de compter les unités réellement distinctes : arrondir, puis dédupliquer
# les lignes de la matrice de poids.
couche = ...              # À COMPLÉTER : la couche cachée que vous avez initialisée
poids = couche.weight.detach().cpu().numpy()
distinctes = np.unique(np.round(poids, 6), axis=0).shape[0]
print(f"{distinctes} unité(s) distincte(s) sur {poids.shape[0]}")

# %% [markdown]
# ### 3. Xavier contre l'initialisation par défaut
#
# Appliquez le fragment de la section 2.6, relancez, superposez les deux courbes.
# **Attendez-vous à une différence modeste, et sachez dire pourquoi :** le réseau est
# petit et peu profond.

# %%
def reseau_xavier():
    reseau = ...          # À COMPLÉTER : votre ReseauQ, avec l'initialisation de la section 2.6
    return reseau


_, train_defaut, _ = entrainer(reseau_relu, comment="-defaut")
_, train_xavier, _ = entrainer(reseau_xavier, comment="-xavier")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(train_defaut, label="initialisation par défaut")
ax.plot(train_xavier, label="Xavier")
ax.set_xlabel("époque"); ax.set_ylabel("perte d'entraînement")
ax.set_yscale("log"); ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ### 4. Abandon de neurones, et l'erreur commise exprès
#
# Ajoutez `nn.Dropout(p=0.3)` après chaque activation et comparez les deux courbes,
# entraînement et validation. Faites ensuite l'erreur **exprès** : évaluez la
# validation **sans** appeler `net.eval()`, et regardez ce que devient la courbe.

# %%
def reseau_dropout():
    return ...        # À COMPLÉTER : votre ReseauQ avec nn.Dropout(p=0.3) après chaque activation


_, train_drop, valid_drop = entrainer(reseau_dropout, comment="-dropout")
_, train_sans, valid_sans = entrainer(reseau_relu, comment="-sans-dropout")

# L'erreur commise exprès : la validation SANS net.eval().
# À COMPLÉTER : refaites la boucle de validation en laissant le réseau en mode train,
# et comparez la courbe obtenue à `valid_drop`.

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(valid_sans, label="validation, sans abandon")
ax.plot(valid_drop, label="validation, abandon p=0,3")
ax.set_xlabel("époque"); ax.set_ylabel("perte de validation")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# **Attentes du niveau 2.**
#
# * Avec la **sigmoïde**, la convergence est nettement plus lente, et la différence
#   s'accentue si vous ajoutez une quatrième couche. C'est le gradient évanescent,
#   sur un réseau de trois couches et un ordinateur portable.
# * Avec l'**initialisation constante**, les 64 unités de la couche restent égales
#   entre elles du début à la fin : la couche travaille comme si elle avait **une
#   seule** unité, et la perte plafonne très haut. Vous venez de reproduire la
#   brisure de symétrie manquée.
# * Sur ce problème, l'**abandon de neurones dégrade** la perte d'entraînement et
#   n'améliore pas la validation : les données sont propres, abondantes et sans bruit
#   d'étiquetage. C'est le résultat attendu, et c'est le meilleur antidote à l'idée
#   qu'une technique de régularisation serait bonne en soi.
# * Sans `net.eval()`, la courbe de validation devient **bruitée et systématiquement
#   pessimiste**. Notez l'écart : c'est le coût d'une ligne oubliée.

# %% [markdown]
# ---
# # Laboratoire — Niveau 3 : le même réseau en convolutif
#
# **Objectif ouvert.** Refaire le niveau 1 avec des **images** en entrée, et un corps
# convolutif. Les cibles restent fournies et la perte reste l'erreur quadratique
# moyenne : rien ne change au protocole, tout change à la forme des données.
#
# **Les données, à fabriquer vous-même.** Des images d'un seul canal, 28 × 28, noires,
# avec un carré blanc de 4 × 4 posé à une position tirée au hasard. La cible est le
# couple de coordonnées du centre du carré, normalisé dans \([-1, 1]\). Respectez la
# convention des canaux : vos tenseurs ont la forme `(N, 1, 28, 28)`.

# %%
def fabriquer_images(n: int, graine: int = 0):
    """(N, 1, 28, 28) et (N, 2). Le carré blanc, et le centre normalisé dans [-1, 1]."""
    g = torch.Generator().manual_seed(graine)
    images = torch.zeros(n, 1, 28, 28)
    cibles = torch.zeros(n, 2)
    # À COMPLÉTER : poser un carré 4x4 à une position tirée au hasard, et remplir la cible.
    ...
    return images, cibles

# %% [markdown]
# **Avant d'écrire la première couche dense**, calculez au crayon la forme de sortie
# de chaque couche convolutive, puis vérifiez-la. Les deux doivent coïncider.

# %%
corps = ...        # À COMPLÉTER : deux couches convolutives, réduction par le PAS, pas par agrégation

# La vérification : faites passer un zéro et lisez la forme obtenue.
print(corps(torch.zeros(1, 1, 28, 28)).shape)

# %%
def compter(modele) -> int:
    return sum(p.numel() for p in modele.parameters())


# À COMPLÉTER : un perceptron multicouche sur les MÊMES images aplaties, avec un
# nombre de paramètres comparable. Comptez les deux, c'est la moitié de la démonstration.
convolutif = ...
dense = ...

# %% [markdown]
# **Ce que vous livrez au niveau 3.**
#
# * La forme de sortie de chaque couche convolutive, **calculée puis vérifiée**. La
#   taille du vecteur aplati est un nombre que vous donnez, pas une constante magique
#   trouvée par essais.
# * Les deux courbes dans TensorBoard, et le nombre de paramètres des deux modèles.
# * Un paragraphe qui répond à une question précise : lequel des deux généralise mieux
#   sur des positions de carré **jamais vues à l'entraînement**, et quel principe de la
#   section 2.8 l'explique.
#
# La comparaison la plus parlante n'est pas « le convolutif gagne », c'est
# **« le convolutif gagne avec dix fois moins de paramètres »**.
#
# > **Mon message pour ce laboratoire :** vous n'entraînez pas un agent, et c'est
# > normal. Vous fabriquez l'instrument, vous apprenez à le régler, et vous installez
# > les réflexes qui vous éviteront, les treize semaines suivantes, de confondre un
# > bogue de PyTorch avec un échec d'apprentissage par renforcement. Quand votre agent
# > de la semaine 5 refusera d'apprendre, la première question sera : « est-ce que le
# > réseau, lui, apprend ? » Cette semaine vous donne les moyens d'y répondre en cinq
# > minutes.
