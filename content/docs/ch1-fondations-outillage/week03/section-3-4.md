---
title: "3.4 CartPole, la double lecture"
weight: 5
---

## L'architecture, et pourquoi la sortie n'est pas une probabilité

Passons au code. L'architecture est d'une simplicité provocante : **une** couche cachée de 128 neurones avec ReLU, et une couche de sortie qui donne un score par action. Le nombre 128 est parfaitement arbitraire, et vous le ferez varier au laboratoire pour vous en convaincre. Trois constantes gouvernent la méthode : la taille de la couche cachée, le nombre d'épisodes par lot, et le percentile.

{{% comment %}}SOURCE: LAPAN ch.4 p.122-123{{% /comment %}}

```python
import torch
import torch.nn as nn

HIDDEN_SIZE = 128
BATCH_SIZE = 16
PERCENTILE = 70


class ReseauPolitique(nn.Module):
    """Observation -> scores bruts, un par action. Pas de softmax ici."""

    def __init__(self, n_obs: int, n_actions: int, n_cache: int = HIDDEN_SIZE):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            nn.ReLU(),
            nn.Linear(n_cache, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pipe(x)
```

{{% comment %}}SOURCE: LAPAN ch.4 p.123{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s\) | observation présentée à la politique | `x`, de forme `(lot, n_obs)` |
| \(\theta\) | paramètres de la politique | `net.parameters()` |
| sorties brutes | scores non normalisés, un par action | la valeur renvoyée par `forward` |
| \(\pi_\theta(a \mid s)\) | la politique elle-même | obtenue en appliquant un softmax à ces scores |

La dernière ligne du tableau mérite une explication, et c'est le premier point de contrôle du laboratoire. Le réseau ne produit **pas** une distribution de probabilité : il produit des **sorties brutes** (*logits*), c'est-à-dire des valeurs non normalisées qui peuvent être négatives et dont la somme n'a aucune raison de valoir 1.

> [!IMPORTANT]
 **Je dois insister, parce que c'est ici que la semaine 2 commence à payer.** Calculer un softmax, qui prend des exponentielles, puis une entropie croisée, qui prend le logarithme de ces probabilités, est **numériquement moins stable** que de faire les deux d'un coup. C'est exactement pourquoi `nn.CrossEntropyLoss` combine softmax et entropie croisée en une seule expression, plus stable, et **exige des valeurs brutes en entrée**. La contrepartie est une discipline à tenir : chaque fois que vous voulez de vraies probabilités, par exemple pour tirer une action, c'est **à vous** d'appliquer le softmax. Oubliez-le et votre agent échantillonnera des actions selon des nombres qui ne sont pas des probabilités, sans qu'aucune erreur ne soit levée.

{{% comment %}}SOURCE: LAPAN ch.4 p.123{{% /comment %}}

---

## Échantillonner une action

Le softmax, nous l'appliquons donc nous-mêmes, et à un seul endroit : au moment de décider. Deux détails de PyTorch sont ici obligatoires, et tous deux viennent de la semaine 2.

```python
import numpy as np

softmax = nn.Softmax(dim=1)          # dim=1 : la dimension 0 est celle du lot


def choisir_action(net: ReseauPolitique, obs: np.ndarray) -> int:
    obs_v = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)   # 1 x n_obs
    probs_v = softmax(net(obs_v))
    probs = probs_v.data.numpy()[0]                               # retour au monde NumPy
    return int(np.random.choice(len(probs), p=probs))
```

{{% comment %}}SOURCE: LAPAN ch.4 p.124-125{{% /comment %}}

Le premier détail est `unsqueeze(0)`. Tout `nn.Module` attend un **lot** en entrée : les quatre nombres de l'observation de CartPole doivent donc devenir un tenseur de forme 1 × 4, un lot d'un seul élément. Le second détail est le couple `.data` puis `.numpy()` : les tenseurs produits par le réseau suivent les gradients, et nous n'en avons aucun besoin pour tirer une action. On se détache du graphe, on convertit, et l'indice `[0]` sort l'unique ligne du lot sous la forme d'un vecteur de probabilités.

{{% comment %}}SOURCE: LAPAN ch.4 p.125{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s\) | observation courante | `obs`, puis `obs_v` de forme 1 × 4 |
| \(\pi_\theta(a \mid s)\) | distribution sur les actions | `probs` |
| \(a \sim \pi_\theta(\cdot \mid s)\) | action tirée selon cette distribution | `np.random.choice(len(probs), p=probs)` |

---

## Collecter un lot, et le bogue silencieux

Nous avons besoin de deux structures minuscules et d'un générateur. Une étape d'épisode retient l'observation et l'action ; un épisode retient son retour total et sa liste d'étapes. C'est tout ce que la méthode mémorise.

```python
from dataclasses import dataclass


@dataclass
class EtapeEpisode:
    observation: np.ndarray     # celle qui a SERVI À CHOISIR l'action
    action: int


@dataclass
class Episode:
    retour: float               # total non actualisé de l'épisode
    etapes: list[EtapeEpisode]


def engendrer_lots(env, net: ReseauPolitique, taille_lot: int):
    lot: list[Episode] = []
    etapes: list[EtapeEpisode] = []
    retour = 0.0
    obs, _ = env.reset()

    while True:
        action = choisir_action(net, obs)
        next_obs, reward, terminated, truncated, _ = env.step(action)
        retour += float(reward)
        etapes.append(EtapeEpisode(observation=obs, action=action))

        if terminated or truncated:
            lot.append(Episode(retour=retour, etapes=etapes))
            retour, etapes = 0.0, []
            next_obs, _ = env.reset()
            if len(lot) == taille_lot:
                yield lot
                lot = []

        obs = next_obs
```

{{% comment %}}SOURCE: LAPAN ch.4 p.124-126{{% /comment %}}

> [!WARNING]
 **Attention : voici le bogue silencieux de la semaine, et c'est le quatrième point de contrôle.** On enregistre l'observation **qui a servi à choisir l'action**, pas celle que l'environnement renvoie **en conséquence** de cette action. Dans le fragment ci-dessus, c'est `obs` qui entre dans `EtapeEpisode`, jamais `next_obs`. Si vous vous trompez, le jeu d'entraînement est décalé d'un pas : vous apprenez au réseau à jouer, dans chaque état, l'action qui convenait à l'état **précédent**. Et le plus pénible est que l'entraînement continue de tourner, la perte descend, les courbes ont l'air normales, l'agent apprend simplement beaucoup moins bien. Aucune exception, aucun message : d'où le mot « silencieux ».

{{% comment %}}SOURCE: LAPAN ch.4 p.125{{% /comment %}}

Un mot sur la structure de ce générateur, parce qu'elle rend concret l'axe « sur politique » de la section 3.1. La collecte et l'entraînement se déroulent **en même temps**, dans un seul fil d'exécution : à chaque `yield`, l'appelant reprend la main, fait un pas d'optimisation, puis redemande un lot. Le réseau qui produit le lot suivant n'est donc **déjà plus** celui qui a produit le précédent. C'est précisément ce que la méthode exige : elle est de la classe sur politique, et l'utilisation de données fraîches est indispensable à son bon fonctionnement. Une méthode hors politique n'aurait pas besoin de cette gymnastique, et c'est exactement la liberté que la semaine 5 ira chercher.

{{% comment %}}SOURCE: LAPAN ch.4 p.126{{% /comment %}}

---

## Filtrer les élites

Le filtre est le cœur de la méthode, et il tient en une dizaine de lignes. Il calcule le seuil, écarte les épisodes qui sont dessous, et aplatit tout ce qui reste en deux tenseurs prêts pour l'entraînement.

```python
def filtrer_elites(lot: list[Episode], percentile: float):
    retours = [ep.retour for ep in lot]
    seuil = float(np.percentile(retours, percentile))
    moyenne = float(np.mean(retours))              # journalisation seulement

    obs_elites: list[np.ndarray] = []
    act_elites: list[int] = []
    for ep in lot:
        if ep.retour < seuil:                      # strictement dessous : on jette
            continue                               # une ÉGALITÉ est donc conservée
        obs_elites.extend(e.observation for e in ep.etapes)
        act_elites.extend(e.action for e in ep.etapes)

    obs_v = torch.tensor(np.vstack(obs_elites), dtype=torch.float32)
    act_v = torch.tensor(act_elites, dtype=torch.long)
    return obs_v, act_v, seuil, moyenne
```

{{% comment %}}SOURCE: LAPAN ch.4 p.127{{% /comment %}}

Trois remarques, et la troisième est à marquer d'une croix dans votre carnet. D'abord, le retour moyen du lot est calculé pour la **journalisation seulement** : il ne sert à rien dans l'algorithme, uniquement à vous dire où vous en êtes. Ensuite, l'aplatissement : un épisode élite de 180 pas apporte 180 paires (observation, action) au jeu d'entraînement, pas une seule. Enfin, la condition. Elle est écrite « si le retour est **strictement inférieur** au seuil, on jette », ce qui veut dire qu'un épisode **exactement égal** au seuil est **conservé**. Sur CartPole, ce choix n'a aucune conséquence visible. Notez-le tout de même : c'est la charnière de la section suivante.

{{% comment %}}SOURCE: LAPAN ch.4 p.127{{% /comment %}}

Ce que le filtre produit est un ensemble d'élites, \(\mathcal{E}\), composé de paires (observation, action). L'entraînement minimise alors la log-vraisemblance négative de ces paires, c'est-à-dire exactement la **perte d'entropie croisée** (*cross-entropy loss*) de la semaine 2 :

$$
\mathcal{L}(\theta) = -\frac{1}{|\mathcal{E}|} \sum_{(s,a) \in \mathcal{E}} \log \pi_\theta(a \mid s)
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.123, p.128{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\psi_i\) | seuil des élites à l'itération \(i\) | `seuil`, soit `np.percentile(retours, percentile)` |
| \(p\) | percentile qui définit le seuil | `PERCENTILE = 70` |
| \(\mathcal{E}\) | ensemble des paires élites | `obs_v`, `act_v` |
| \(\left[G \ge \psi_i\right]\) | indicateur de sélection | le `if ep.retour < seuil: continue` |
| \(\mathcal{L}(\theta)\) | perte sur les élites | `objective(logits_v, act_v)` |

---

## La boucle, et les quatre points de contrôle

Il ne reste qu'à assembler. Le montage complet tient en une quinzaine de lignes, et vous reconnaîtrez la boucle d'entraînement de la semaine 2, à l'identique.

```python
import gymnasium as gym
import torch.optim as optim

env = gym.make("CartPole-v1")
net = ReseauPolitique(env.observation_space.shape[0], env.action_space.n)
objective = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.01)

for iteration, lot in enumerate(engendrer_lots(env, net, BATCH_SIZE)):
    obs_v, act_v, seuil, moyenne = filtrer_elites(lot, PERCENTILE)

    optimizer.zero_grad()
    logits_v = net(obs_v)
    loss_v = objective(logits_v, act_v)
    loss_v.backward()
    optimizer.step()

    print(f"{iteration}: perte={loss_v.item():.3f}, "
          f"retour moyen={moyenne:.1f}, seuil={seuil:.1f}")

    if moyenne > 475:
        print("Résolu !")
        break
```

{{% comment %}}SOURCE: LAPAN ch.4 p.128-129{{% /comment %}}

Lisez la ligne de la perte avec attention, parce qu'elle contient toute la méthode : elle calcule l'entropie croisée entre la sortie du réseau et **les actions que l'agent a effectivement jouées** dans les épisodes élites. Elle ne compare pas le réseau à une vérité extérieure, elle le compare à son propre passé, filtré. Minimiser cette perte revient à renforcer ces actions élites qui ont conduit à de bons retours.

{{% comment %}}SOURCE: LAPAN ch.4 p.128{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(N\) | épisodes par itération | `BATCH_SIZE = 16` |
| \(\alpha\) | pas d'apprentissage | `lr=0.01` |
| \(\nabla_\theta \mathcal{L}\) | gradient de la perte | `loss_v.backward()` |
| moyenne du lot | retour moyen, surveillance seulement | `moyenne` |

Le critère d'arrêt demande une justification, et c'est le premier point de contrôle du laboratoire. On s'arrête quand le retour moyen dépasse **475**. Pourquoi 475 ? Parce que la version de CartPole employée ici est considérée comme résolue lorsque la récompense moyenne des 100 derniers épisodes dépasse 475, et parce qu'un épisode y est plafonné à 500 pas. Vous avez rencontré le chiffre 195 en semaine 1, pour un critère plus ancien ; retenez surtout la **forme** du critère plutôt que le nombre : un seuil de résolution est toujours une moyenne sur plusieurs dizaines d'épisodes, jamais un record isolé.

{{% comment %}}SOURCE: LAPAN ch.4 p.129{{% /comment %}}

Une exécution de référence commence à un retour moyen de 25,2 à l'itération 0, ce qui est l'ordre de grandeur que vous aviez mesuré en semaine 1 pour une politique uniforme, et franchit 475 à l'itération 43. En règle générale, il ne faut pas plus de cinquante lots, et le plus souvent **entre 30 et 60 lots**, à seize épisodes par lot. Je précise l'unité parce qu'elle se confond vite : il s'agit bien de lots, donc de 480 à 960 épisodes joués, et de 30 à 60 pas d'optimisation. Quelques minutes sur un processeur central, sans la moindre carte graphique.

{{% comment %}}SOURCE: LAPAN ch.4 p.129-130{{% /comment %}}

> [!TIP]
 **Pour voir votre agent plutôt que de le lire.** Créez l'environnement avec `render_mode="rgb_array"` et enveloppez-le dans `gym.wrappers.RecordVideo(env, video_folder="video")` : vous obtiendrez un fichier vidéo par épisode. Lancez-le une fois au début de l'entraînement et une fois à la fin. Quinze secondes de vidéo valent mieux qu'une courbe pour comprendre ce que votre politique a réellement appris, et c'est l'un des rares moments du cours où la pédagogie et le plaisir coïncident parfaitement.

{{% comment %}}SOURCE: LAPAN ch.4 p.131{{% /comment %}}
