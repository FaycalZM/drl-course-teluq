---
title: "Laboratoire"
weight: 12
---

Trois niveaux, un seul carnet. **Aucun réseau de neurones, aucun GPU : chaque exercice s'exécute en quelques secondes**, et ce budget dérisoire est une information en soi, puisqu'il vous autorise à *répéter* une mesure cent fois plutôt qu'à la commenter une fois. Deux règles partout : une graine passée à `reset(seed=...)`, et les **cinq** valeurs de `step()` dépaquetées.

## Niveau 1 : Implémentation guidée

**Objectif.** Faire passer l'environnement-jouet de la section 1.6 à l'interface Gymnasium, puis mesurer l'agent aléatoire sur CartPole et poser une enveloppe sur celui-ci.

**Exercice 1.A : l'environnement-jouet, version `gym.Env`.** Quatre trous à combler.

```python
import gymnasium as gym
import numpy as np
from gymnasium.spaces import Box, Discrete


class ToyEnv(gym.Env):
 """Récompense aléatoire pendant `horizon` pas, quoi que fasse l'agent."""

 def __init__(self, horizon: int = 10):
 self.action_space = ... # À COMPLÉTER : deux actions mutuellement exclusives
 self.observation_space = ... # À COMPLÉTER : trois réels dans [0, 1]
 self.horizon = horizon

 def reset(self, seed=None, options=None):
 super().reset(seed=seed) # initialise self.np_random
 self.remaining = self.horizon
 return np.zeros(3, dtype=np.float32), {}

 def step(self, action):
 self.remaining -= 1
 reward = float(self.np_random.random())
 terminated = ... # À COMPLÉTER : ce jouet a-t-il un état terminal ?
 truncated = ... # À COMPLÉTER : et une limite de pas ?
 return np.zeros(3, dtype=np.float32), reward, terminated, truncated, {}
```

**Exercice 1.B : mesurer la politique uniforme.** Une fonction qui ne sait **rien** de l'environnement reçu ; vous la réutiliserez telle quelle au niveau 3. L'argument `politique` isole la ligne « décider » de la section 1.6.

```python
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
 if ...: # À COMPLÉTER : les deux drapeaux, pas un seul
 break
 longueurs.append(pas)
 return np.array(longueurs)


L = evaluer(gym.make("CartPole-v1"))
print(f"{L.mean():.1f} pas en moyenne, écart-type {L.std(ddof=1):.1f}, max {L.max()}")
```

**Exercice 1.C : chaîner une enveloppe.** Avec `EpsilonRandomAction` (section 1.10), comparez trois mesures de 100 épisodes : la politique uniforme nue, la même enveloppée avec \(\varepsilon = 0{,}3\), puis un agent **obtus** (`politique=lambda obs: 0`, toujours pousser à gauche) avec et sans l'enveloppe.

**Attentes.**

* Dans `ToyEnv`, c'est `truncated` qui passe à `True`, jamais `terminated` : l'horizon est une limite de pas que *nous* imposons, pas un état terminal du modèle. Si vous avez écrit l'inverse, relisez la section 1.8.
* Sur CartPole, une moyenne à deux chiffres, **un ordre de grandeur sous la frontière de 195** : vous venez de produire vous-même le chiffre de référence du cours. Relevez aussi l'écart-type, qui n'est pas négligeable devant la moyenne : comptez un tiers à une moitié. Nous l'exploitons au niveau suivant.
* L'enveloppe \(\varepsilon\)-aléatoire ne change **rien** de mesurable à la politique uniforme : remplacer un tirage uniforme par un autre tirage uniforme n'a aucun effet. Sur l'agent obtus, le gain est net. Retenez la dissymétrie : l'exploration profite d'abord aux mauvaises politiques.

{{< colab url="TODO" label="Niveau 1 : environnement-jouet, agent aléatoire, enveloppe" >}}

## Niveau 2 : Hyperparamètres et sensibilité

**Objectif.** Cette semaine n'entraîne rien : le seul hyperparamètre disponible est l'\(\varepsilon\) de l'enveloppe, et la seule quantité à régler est **le nombre d'épisodes qu'il faut pour qu'une moyenne soit crédible**. Installez l'habitude maintenant : tous les résultats des quatorze semaines suivantes seront des moyennes.

**Protocole, en deux parties.**

1. **Balayage de \(\varepsilon\).** Pour \(\varepsilon \in \{0 \,;\, 0{,}1 \,;\, 0{,}25 \,;\, 0{,}5 \,;\, 1\}\), mesurez l'agent obtus sous l'enveloppe, 200 épisodes par valeur. Tracez la moyenne en fonction de \(\varepsilon\), avec une barre d'erreur égale à \(s/\sqrt{n}\).
2. **Combien d'épisodes ?** Pour \(n \in \{5 \,;\, 10 \,;\, 30 \,;\, 100 \,;\, 300\}\), répétez la mesure de la politique uniforme avec 20 graines différentes et relevez l'**étendue** des 20 moyennes. Comparez-la à l'erreur type \(s/\sqrt{n}\) estimée, elle, sur un seul lot.

**Solution courte.** Aucune bibliothèque d'algorithmes ici : il n'y a rien à entraîner. Tout tient en trois lignes de NumPy sur le tableau renvoyé par `evaluer`.

```python
s, n = L.std(ddof=1), len(L)
print(f"erreur type : {s / np.sqrt(n):.2f} pas")
print("épisodes requis pour ±1 pas :", int(np.ceil(s ** 2))) # s/sqrt(n) <= 1
```

**Attentes.**

* La courbe en \(\varepsilon\) **monte**, de \(\varepsilon = 0\) (l'agent obtus) à \(\varepsilon = 1\), qui *est* la politique uniforme du niveau 1. N'en tirez pas « plus d'exploration, c'est mieux » : cela ne tient que parce que la politique de départ est épouvantable. Dès la semaine 4, avec une politique qui a appris quelque chose, la même courbe redescendra, d'où le \(\varepsilon\) **décroissant** de l'entraînement.
* À \(n = 5\), vos 20 moyennes s'étalent sur plusieurs pas : même expérience, deux graines, deux conclusions. À \(n = 100\), l'étendue se resserre au pas près. Vous devez retrouver l'ordre de grandeur de \(s/\sqrt{n}\) et constater que la précision ne progresse qu'en \(\sqrt{n}\) : quadrupler le coût pour diviser l'incertitude par deux.
* À écrire noir sur blanc : les **100 épisodes consécutifs** de la frontière de récompense ne sont pas un chiffre rond arbitraire. Dites, avec *votre* \(s\), quelle précision ils achètent.

{{< colab url="TODO" label="Niveau 2 : balayage d'epsilon et crédibilité d'une moyenne" >}}

## Niveau 3 : Extension créative, choisir l'environnement de votre projet

**Objectif ouvert.** Le jalon 1 de la semaine 3 suppose un environnement choisi, justifié et déjà enveloppé. Instruisez ce choix **par la mesure** plutôt que par la lecture : retenez trois candidats dans la documentation de Gymnasium (et nulle part ailleurs : les listes publiées dans les livres et les blogues vieillissent en quelques mois), puis soumettez les trois à votre `evaluer` du niveau 1.

**Critères de réussite.**

* Les trois candidats passent dans `evaluer` **sans une ligne de changement**. S'il faut l'adapter, c'est que votre code dépendait de l'environnement, et la promesse de la section 1.7 n'est pas tenue.
* Une fiche d'une demi-page par candidat, avec des nombres **mesurés** et non recopiés : les deux espaces, moyenne et écart-type de la politique uniforme, durée réelle de 1 000 pas (`time.perf_counter()`), et la réponse aux cinq questions de la section 1.9.
* Vous savez dire, pour chaque candidat, **si la troncature existe** et au bout de combien de pas. Vérifiez-le, ne le supposez pas : comptez les épisodes qui s'achèvent avec `truncated` à `True`.
* Une enveloppe écrite par vous pour le candidat retenu, et un paragraphe sur ce qu'elle apporte.

**Piste de départ.** `gym.registry` est un dictionnaire : ses clés sont les identifiants installés, et `gym.registry["CartPole-v1"].max_episode_steps` donne la limite de temps sans lancer un seul épisode. Un candidat raisonnable exécute 1 000 pas en bien moins d'une seconde.

> [!TIP]
 **Mon message :** la base d'entropie croisée et l'analyse de ses limites restent le travail de la semaine 3. Ne les anticipez pas. Ce que vous livrez ici, c'est le terrain : un environnement choisi pour des raisons chiffrées, une mesure de référence contre laquelle comparer votre premier agent, et une enveloppe qui fonctionne.

{{% comment %}}SOURCE: LAPAN ch.2 p.59-62, p.72-77{{% /comment %}}
