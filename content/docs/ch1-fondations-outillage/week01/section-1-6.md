---
title: "1.6 L'anatomie d'un agent, sans bibliothèque"
weight: 7
---

## Derrière le rideau : la boucle d'interaction écrite à la main

Avant de brancher ce cadre sur une bibliothèque, écrivons la boucle d'interaction **à la main**, sans aucune abstraction : dans quelques pages, Gymnasium va cacher tout ce que nous allons écrire ici, et je veux que vous sachiez ce qu'il y a derrière le rideau.

Notre environnement-jouet distribuera des récompenses **aléatoires** pendant un nombre borné de pas, **quoi que fasse l'agent**. C'est absurde comme modèle du monde, et c'est exactement ce que nous voulons : en retirant tout contenu à l'environnement, nous isolons la **structure** de l'interaction. Son unique état interne est un compteur de pas restants, initialisé à 10 ; et comme il n'a pas de véritable état à exposer, l'observation qu'il renvoie est toujours un vecteur nul.

{{% comment %}}SOURCE: LAPAN ch.2 p.59{{% /comment %}}

```python
import random

class ToyEnv:
    """Environnement minimal : récompense aléatoire pendant un nombre borné
    d'interactions, indépendamment de l'action reçue."""

    def __init__(self, horizon: int = 10):
        self.remaining = horizon          # le seul état interne

    def observe(self) -> list[float]:
        return [0.0, 0.0, 0.0]            # aucun état réel à exposer

    def available_actions(self) -> list[int]:
        return [0, 1]

    def is_terminated(self) -> bool:
        return self.remaining == 0

    def act(self, action: int) -> float:
        if self.is_terminated():
            raise RuntimeError("épisode terminé : il faut réinitialiser")
        self.remaining -= 1
        return random.random()
```

{{% comment %}}SOURCE: LAPAN ch.2 p.59-60{{% /comment %}}

Quatre méthodes, et chacune correspond à un élément de la section 1.2 : `observe()` est le canal des observations, `available_actions()` décrit l'espace d'actions, `act()` est le canal des actions **et** celui des récompenses, `is_terminated()` signale la fin de l'épisode. Pourquoi un signal de fin explicite ? Parce qu'un épisode peut être fini (une partie d'échecs) ou infini : la sonde Voyager 2, lancée il y a plus de quarante-six ans, poursuit sa mission. Aucune règle universelle n'en décide : c'est l'environnement qui doit le dire, à chaque pas.

{{% comment %}}SOURCE: LAPAN ch.2 p.60{{% /comment %}}

Voici l'agent. Regardez surtout l'ordre des quatre opérations de sa méthode `step()`, parce que **cet ordre ne changera plus jamais** dans ce cours : observer, décider à partir des observations, soumettre l'action, encaisser la récompense.

```python
class ToyAgent:
    def __init__(self):
        self.total_reward = 0.0

    def step(self, env: ToyEnv) -> None:
        obs = env.observe()                                 # 1. observer
        action = random.choice(env.available_actions())     # 2. décider
        reward = env.act(action)                            # 3. agir
        self.total_reward += reward                         # 4. encaisser


env, agent = ToyEnv(), ToyAgent()
while not env.is_terminated():
    agent.step(env)
print(f"Récompense totale : {agent.total_reward:.4f}")
```

{{% comment %}}SOURCE: LAPAN ch.2 p.60-61{{% /comment %}}

Cet agent est obtus : il appelle `env.observe()` puis **jette l'observation**. C'est volontaire et honnête : avec un environnement dont les récompenses ne dépendent pas des actions, il n'y aurait de toute façon rien à apprendre. Mais la variable `obs` est là, à sa place : tout ce que nous ferons pendant quatorze semaines consistera à remplacer la ligne 2 par quelque chose qui **utilise** la ligne 1. Dix pas, dix tirages uniformes : la récompense totale tourne autour de 5, une exécution donnant par exemple `Récompense totale : 5.8832`.

{{% comment %}}SOURCE: LAPAN ch.2 p.61{{% /comment %}}

{{< colab url="TODO" label="Exécuter l'agent-jouet dans Colab" >}}

La morale de la section : remplacez cet environnement par un modèle physique complexe et cet agent par un grand réseau de neurones, **le motif de base ne changera pas**. À chaque pas, l'agent prend des observations, fait ses calculs, choisit une action ; le résultat est une récompense et une nouvelle observation. Tout ce qui suit (DQN, A2C, PPO, SAC) est une façon de plus en plus sophistiquée de remplir la ligne « décider ».

{{% comment %}}SOURCE: LAPAN ch.2 p.62{{% /comment %}}
