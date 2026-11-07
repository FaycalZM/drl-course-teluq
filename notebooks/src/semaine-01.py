# %% [markdown]
# # SCI1070 — Semaine 1 : l'agent, l'environnement, et la mesure de référence
#
# Ce carnet couvre toute la semaine 1 :
#
# | Section du cours | Ce que vous y faites |
# | --- | --- |
# | 1.6 | exécuter l'agent-jouet et sa boucle en quatre temps |
# | 1.9 | mesurer l'agent aléatoire sur `CartPole-v1` |
# | Laboratoire, niveau 1 | porter le jouet à l'interface Gymnasium, écrire `evaluer`, enchaîner une enveloppe |
# | Laboratoire, niveau 2 | balayer \(\varepsilon\), et décider combien d'épisodes rend une moyenne crédible |
# | Laboratoire, niveau 3 | choisir l'environnement de votre projet, par la mesure |
#
# **Aucun réseau de neurones, aucun GPU.** Chaque cellule s'exécute en quelques
# secondes, et ce budget dérisoire est une information en soi : il vous autorise à
# *répéter* une mesure cent fois plutôt qu'à la commenter une fois.
#
# **Les deux règles de la semaine, partout :** une graine passée à `reset(seed=...)`,
# et les **cinq** valeurs de `step()` dépaquetées.
#
# ---
#
# ### Comment lire les `...`
#
# Les lignes marquées `# À COMPLÉTER` sont **à vous**. Elles ne sont pas un oubli :
# écrire ce code *est* l'exercice, et vous ne trouverez les réponses nulle part dans
# ce dépôt. Une cellule laissée avec ses `...` lèvera une erreur — c'est voulu, cela
# vous dit exactement où vous en êtes.

# %% [markdown]
# ## Installation
#
# Colab fournit déjà NumPy et Matplotlib. Il ne fournit pas toujours Gymnasium.

# %% [smoke]
# On n'utilise pas « !pip » : la forme ci-dessous est du Python valide, donc elle
# tourne aussi bien dans Colab que dans un interpréteur local ou un test.
import importlib.util
import subprocess
import sys

for paquet, module in [("gymnasium[classic-control]>=1.0", "gymnasium")]:
    if importlib.util.find_spec(module) is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paquet], check=True)

import random

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

print("gymnasium", gym.__version__)
print("numpy    ", np.__version__)

# %% [markdown]
# ---
# ## Section 1.6 — l'agent-jouet, et l'ordre des quatre opérations
#
# L'environnement le plus bête qui soit : il distribue une récompense aléatoire
# pendant dix pas, **quoi que fasse l'agent**. Il n'y a rien à y apprendre, et c'est
# précisément ce qui rend la boucle lisible.
#
# Regardez l'ordre des quatre opérations de `step()`, parce que **cet ordre ne
# changera plus jamais** dans ce cours : observer, décider à partir des observations,
# soumettre l'action, encaisser la récompense.

# %% [smoke]
class ToyEnv:
    """Récompense aléatoire pendant dix pas, quoi que fasse l'agent."""

    def __init__(self):
        self.steps_left = 10

    def observe(self) -> list[float]:
        return [0.0, 0.0, 0.0]

    def available_actions(self) -> list[int]:
        return [0, 1]

    def act(self, action: int) -> float:
        if self.is_terminated():
            raise RuntimeError("l'épisode est fini")
        self.steps_left -= 1
        return random.random()

    def is_terminated(self) -> bool:
        return self.steps_left == 0


class ToyAgent:
    def __init__(self):
        self.total_reward = 0.0

    def step(self, env: ToyEnv) -> None:
        obs = env.observe()                                 # 1. observer
        action = random.choice(env.available_actions())     # 2. décider
        reward = env.act(action)                            # 3. agir
        self.total_reward += reward                         # 4. encaisser


random.seed(0)
env, agent = ToyEnv(), ToyAgent()
while not env.is_terminated():
    agent.step(env)
print(f"Récompense totale : {agent.total_reward:.4f}")

# %% [markdown]
# Cet agent est **obtus** : il appelle `env.observe()` puis jette l'observation. La
# variable `obs` est pourtant là, à sa place. Tout ce que nous ferons pendant quatorze
# semaines consistera à remplacer la ligne 2 par quelque chose qui **utilise** la
# ligne 1.
#
# Dix pas, dix tirages uniformes : la récompense totale tourne autour de 5.
#
# > **Faites-le tourner plusieurs fois sans la graine.** L'écart entre deux exécutions
# > est la première chose que ce cours vous demande de ne jamais ignorer.

# %% [markdown]
# ---
# ## Section 1.9 — l'agent aléatoire sur CartPole, et le chiffre de référence
#
# Un vrai environnement, et la politique la plus bête qui soit : tirer uniformément.
# Le nombre que cette cellule imprime est le **point de comparaison de tout le cours**.

# %% [smoke]
env = gym.make("CartPole-v1")
obs, info = env.reset(seed=0)

total_reward = 0.0
total_steps = 0

while True:
    action = env.action_space.sample()   # politique uniforme : notre référence
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    total_steps += 1
    if terminated or truncated:
        break

print(f"Épisode terminé en {total_steps} pas, récompense totale {total_reward:.2f}")

# %% [markdown]
# **Un épisode ne vous dit rien.** Relancez la cellule en changeant la graine : vous
# obtiendrez un nombre nettement différent. C'est exactement le problème que le
# niveau 2 du laboratoire va rendre chiffrable.

# %% [markdown]
# ---
# # Laboratoire — Niveau 1 : implémentation guidée
#
# **Objectif.** Faire passer l'environnement-jouet de la section 1.6 à l'interface
# Gymnasium, puis mesurer l'agent aléatoire sur CartPole et poser une enveloppe
# sur celui-ci.

# %% [markdown]
# ### Exercice 1.A — l'environnement-jouet, version `gym.Env`
#
# Quatre trous à combler. Le dernier est le plus intéressant des quatre : demandez-vous
# si l'horizon de ce jouet est un **état terminal du modèle** ou une **limite de pas que
# nous imposons**. La section 1.8 tranche.

# %%
from gymnasium.spaces import Box, Discrete


class ToyEnvGym(gym.Env):
    """Récompense aléatoire pendant `horizon` pas, quoi que fasse l'agent."""

    def __init__(self, horizon: int = 10):
        self.action_space = ...        # À COMPLÉTER : deux actions mutuellement exclusives
        self.observation_space = ...   # À COMPLÉTER : trois réels dans [0, 1]
        self.horizon = horizon

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)       # initialise self.np_random
        self.remaining = self.horizon
        return np.zeros(3, dtype=np.float32), {}

    def step(self, action):
        self.remaining -= 1
        reward = float(self.np_random.random())
        terminated = ...               # À COMPLÉTER : ce jouet a-t-il un état terminal ?
        truncated = ...                # À COMPLÉTER : et une limite de pas ?
        return np.zeros(3, dtype=np.float32), reward, terminated, truncated, {}


# Vérification minimale : un épisode complet doit faire exactement `horizon` pas.
e = ToyEnvGym(horizon=10)
obs, info = e.reset(seed=0)
pas = 0
while True:
    obs, r, terminated, truncated, info = e.step(e.action_space.sample())
    pas += 1
    if terminated or truncated:
        break
print(f"{pas} pas  |  terminated={terminated}  truncated={truncated}")

# %% [markdown]
# ### Exercice 1.B — mesurer la politique uniforme
#
# Une fonction qui ne sait **rien** de l'environnement reçu ; vous la réutiliserez
# telle quelle au niveau 3. L'argument `politique` isole la ligne « décider » de la
# section 1.6.

# %%
def evaluer(env, episodes: int = 100, graine: int = 0, politique=None) -> np.ndarray:
    politique = politique or (lambda obs: env.action_space.sample())
    longueurs = []
    for k in range(episodes):
        obs, info = env.reset(seed=graine + k)
        pas = 0
        while True:
            action = politique(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            pas += 1
            if ...:          # À COMPLÉTER : les deux drapeaux, pas un seul
                break
        longueurs.append(pas)
    return np.array(longueurs)


L = evaluer(gym.make("CartPole-v1"))
print(f"{L.mean():.1f} pas en moyenne, écart-type {L.std(ddof=1):.1f}, max {L.max()}")

# %% [markdown]
# ### Exercice 1.C — chaîner une enveloppe
#
# Avec `EpsilonRandomAction` de la section 1.10, comparez **trois** mesures de
# 100 épisodes : la politique uniforme nue, la même enveloppée avec
# \(\varepsilon = 0{,}3\), puis un agent **obtus** (`politique=lambda obs: 0`,
# toujours pousser à gauche) avec et sans l'enveloppe.

# %%
class EpsilonRandomAction(gym.ActionWrapper):
    """Avec la probabilité epsilon, remplace l'action de l'agent par une action
    tirée uniformément dans l'espace d'actions."""

    def __init__(self, env: gym.Env, epsilon: float = 0.1):
        super().__init__(env)
        self.epsilon = epsilon

    def action(self, action):
        if random.random() < self.epsilon:
            return self.action_space.sample()
        return action


obtus = lambda obs: 0        # noqa: E731 — toujours pousser à gauche

mesures = {
    "uniforme, nue":            evaluer(gym.make("CartPole-v1")),
    "uniforme, eps=0,3":        evaluer(EpsilonRandomAction(gym.make("CartPole-v1"), 0.3)),
    "obtus, nu":                ...,   # À COMPLÉTER
    "obtus, eps=0,3":           ...,   # À COMPLÉTER
}

for nom, L in mesures.items():
    if L is Ellipsis:
        print(f"{nom:24s} à compléter")
    else:
        print(f"{nom:24s} {L.mean():6.1f} ± {L.std(ddof=1) / np.sqrt(len(L)):.2f} pas")

# %% [markdown]
# **Attentes du niveau 1.**
#
# * Dans `ToyEnvGym`, c'est `truncated` qui passe à `True`, jamais `terminated` :
#   l'horizon est une limite de pas que *nous* imposons, pas un état terminal du
#   modèle. Si vous avez écrit l'inverse, relisez la section 1.8.
# * Sur CartPole, une moyenne à **deux chiffres**, un ordre de grandeur sous la
#   frontière de 195. Vous venez de produire vous-même le chiffre de référence du
#   cours. Relevez aussi l'écart-type : comptez un tiers à une moitié de la moyenne.
# * L'enveloppe \(\varepsilon\)-aléatoire ne change **rien** de mesurable à la
#   politique uniforme — remplacer un tirage uniforme par un autre tirage uniforme
#   n'a aucun effet. Sur l'agent obtus, le gain est net. Retenez la dissymétrie :
#   **l'exploration profite d'abord aux mauvaises politiques.**

# %% [markdown]
# ---
# # Laboratoire — Niveau 2 : combien d'épisodes rend une moyenne crédible ?
#
# Cette semaine n'entraîne rien. Le seul hyperparamètre disponible est l'\(\varepsilon\)
# de l'enveloppe, et la seule quantité à régler est **le nombre d'épisodes**.
# Installez l'habitude maintenant : tous les résultats des quatorze semaines
# suivantes seront des moyennes.

# %% [markdown]
# ### Partie 1 — balayage de \(\varepsilon\)
#
# Pour \(\varepsilon \in \{0\,;\,0{,}1\,;\,0{,}25\,;\,0{,}5\,;\,1\}\), mesurez l'agent
# obtus sous l'enveloppe, 200 épisodes par valeur. Tracez la moyenne en fonction de
# \(\varepsilon\), avec une barre d'erreur égale à \(s/\sqrt{n}\).

# %%
epsilons = [0.0, 0.1, 0.25, 0.5, 1.0]
moyennes, erreurs = [], []

for eps in epsilons:
    L = ...          # À COMPLÉTER : 200 épisodes de l'agent obtus sous l'enveloppe
    moyennes.append(L.mean())
    erreurs.append(L.std(ddof=1) / np.sqrt(len(L)))

fig, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(epsilons, moyennes, yerr=erreurs, marker="o", capsize=4)
ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel("longueur moyenne d'épisode (pas)")
ax.set_title("Agent obtus sous enveloppe, 200 épisodes par point")
ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ### Partie 2 — l'étendue de vingt moyennes
#
# Pour \(n \in \{5\,;\,10\,;\,30\,;\,100\,;\,300\}\), répétez la mesure de la politique
# uniforme avec **20 graines différentes** et relevez l'**étendue** des 20 moyennes.
# Comparez-la à l'erreur type \(s/\sqrt{n}\) estimée, elle, sur un seul lot.

# %%
for n in [5, 10, 30, 100, 300]:
    moyennes_n = [
        ...          # À COMPLÉTER : la moyenne d'un lot de n épisodes, pour la graine g
        for g in range(20)
    ]
    etendue = max(moyennes_n) - min(moyennes_n)
    un_lot = evaluer(gym.make("CartPole-v1"), episodes=n, graine=0)
    erreur_type = un_lot.std(ddof=1) / np.sqrt(n)
    print(f"n={n:4d}  étendue des 20 moyennes {etendue:6.2f}  |  s/sqrt(n) sur un lot {erreur_type:5.2f}")

# %% [markdown]
# ### La solution courte
#
# Aucune bibliothèque d'algorithmes ici : il n'y a rien à entraîner. Tout tient en
# trois lignes de NumPy sur le tableau renvoyé par `evaluer`.

# %%
s, n = L.std(ddof=1), len(L)
print(f"erreur type : {s / np.sqrt(n):.2f} pas")
print("épisodes requis pour ±1 pas :", int(np.ceil(s ** 2)))   # s/sqrt(n) <= 1

# %% [markdown]
# **Attentes du niveau 2.**
#
# * La courbe en \(\varepsilon\) **monte**, de \(\varepsilon = 0\) (l'agent obtus) à
#   \(\varepsilon = 1\), qui *est* la politique uniforme du niveau 1. N'en tirez pas
#   « plus d'exploration, c'est mieux » : cela ne tient que parce que la politique de
#   départ est épouvantable. Dès la semaine 4, avec une politique qui a appris quelque
#   chose, la même courbe **redescendra**.
# * À \(n = 5\), vos 20 moyennes s'étalent sur plusieurs pas : même expérience, deux
#   graines, deux conclusions. À \(n = 100\), l'étendue se resserre au pas près.
# * La précision ne progresse qu'en \(\sqrt{n}\) : **quadrupler le coût pour diviser
#   l'incertitude par deux.**
# * À écrire noir sur blanc dans votre carnet : les 100 épisodes consécutifs de la
#   frontière de récompense ne sont pas un chiffre rond arbitraire. Dites, avec
#   *votre* \(s\), quelle précision ils achètent.

# %% [markdown]
# ---
# # Laboratoire — Niveau 3 : choisir l'environnement de votre projet
#
# Le jalon 1 de la semaine 3 suppose un environnement **choisi, justifié et déjà
# enveloppé**. Instruisez ce choix par la mesure plutôt que par la lecture : retenez
# trois candidats dans la documentation de Gymnasium — et nulle part ailleurs, les
# listes publiées dans les livres et les blogues vieillissent en quelques mois — puis
# soumettez les trois à votre `evaluer` du niveau 1.
#
# **Le critère qui compte :** les trois candidats passent dans `evaluer` **sans une
# ligne de changement**. S'il faut l'adapter, c'est que votre code dépendait de
# l'environnement, et la promesse de la section 1.7 n'est pas tenue.

# %% [smoke]
# `gym.registry` est un dictionnaire : ses clés sont les identifiants installés, et
# `max_episode_steps` donne la limite de temps sans lancer un seul épisode.
for nom in ["CartPole-v1", "Acrobot-v1", "MountainCar-v0"]:
    spec = gym.registry[nom]
    print(f"{nom:18s} limite de pas : {spec.max_episode_steps}")

# %%
import time

candidats = ["CartPole-v1", ...]      # À COMPLÉTER : deux autres, choisis par vous

for nom in candidats:
    if nom is Ellipsis:
        continue
    env = gym.make(nom)
    t0 = time.perf_counter()
    L = evaluer(env, episodes=30)
    duree = time.perf_counter() - t0

    # Comptez les épisodes qui s'achèvent par troncature : vérifiez-le, ne le supposez pas.
    tronques = ...        # À COMPLÉTER

    print(f"{nom:18s} {L.mean():7.1f} ± {L.std(ddof=1):5.1f} pas  "
          f"| {duree:5.2f} s pour 30 épisodes "
          f"| obs {env.observation_space} | act {env.action_space}")

# %% [markdown]
# **Ce que vous livrez au niveau 3.**
#
# * Une fiche d'une demi-page par candidat, avec des nombres **mesurés** et non
#   recopiés : les deux espaces, moyenne et écart-type de la politique uniforme,
#   durée réelle de 1 000 pas (`time.perf_counter()`), et la réponse aux cinq
#   questions de la section 1.9.
# * Pour chaque candidat : **si la troncature existe**, et au bout de combien de pas.
# * Une enveloppe écrite par vous pour le candidat retenu, et un paragraphe sur ce
#   qu'elle apporte.
#
# > **N'anticipez pas la semaine 3.** La base d'entropie croisée et l'analyse de ses
# > limites restent son travail. Ce que vous livrez ici, c'est le terrain : un
# > environnement choisi pour des raisons chiffrées, une mesure de référence contre
# > laquelle comparer votre premier agent, et une enveloppe qui fonctionne.
