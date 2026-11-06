---
title: "13.6 La boucle de collecte, et l'agent complet"
weight: 7
---

## Quinze lignes qui referment la première moitié

Nous avons un modèle et un planificateur. Il manque la boucle qui les fait vivre ensemble, et elle est courte.

**L'intuition.** On ne peut pas entraîner le modèle avant d'avoir des données, et on ne peut pas collecter de bonnes données avant d'avoir un modèle. On alterne donc, en commençant par un amorçage aléatoire : quelques épisodes joués au hasard donnent de quoi entraîner un premier modèle, qui donne de quoi collecter de meilleurs épisodes, qui donnent de quoi améliorer le modèle. C'est la même structure qu'un apprentissage actif, et c'est tout l'agent.

**L'équation.** L'algorithme complet, en trois temps.

Initialisation : collecter \(S\) épisodes avec une politique aléatoire et les placer dans \(\mathcal{D}\). Puis, indéfiniment :

$$
\theta \leftarrow \theta - \alpha\, \nabla_\theta \mathcal{L}(\theta)
\quad\text{sur } C \text{ pas, par lots } \big\{(o_t, a_t, r_t)_{t=i}^{i+L}\big\}_{b=1}^{B} \sim \mathcal{D}
$$

$$
a_t = \text{planifier}\big(e_\theta(z_t \mid o_{\le t}, a_{<t})\big) + \epsilon,
\qquad \epsilon \sim \mathcal{N}(0,\, 0{,}3)
\quad\text{sur } \lceil T / \text{action\_repeat} \rceil \text{ pas}
$$

$$
\mathcal{D} \leftarrow \mathcal{D} \cup \{\text{l'épisode collecté}\}
$$

{{% comment %}}SOURCE: PLANET alg. 1 p.2{{% /comment %}}

Lisez la deuxième ligne : l'action jouée dans le monde réel est celle du planificateur **plus un bruit gaussien**. C'est la seule exploration de tout l'agent. Il n'y a ni politique \(\varepsilon\)-gloutonne, ni prime d'exploration, ni réseau bruité : un bruit gaussien d'écart-type \(0{,}3\) ajouté à l'action planifiée, et rien d'autre. Après la semaine 11, qui a consacré six sections à l'exploration dirigée, c'est une sobriété qui mérite d'être remarquée, et elle a une explication : un planificateur dont le modèle est encore mauvais produit déjà des actions très variées, parce que son modèle lui promet n'importe quoi. L'exploration est, au début, un effet secondaire gratuit de l'ignorance.

---

## La répétition d'action, et ce qu'elle achète vraiment

Le troisième comptage de la deuxième ligne mérite sa propre explication, parce que c'est le réglage le plus important de tout l'agent.

La **répétition d'action** (*action repeat*) consiste à jouer la même action plusieurs pas d'environnement de suite, et à ne demander une décision qu'une fois sur `action_repeat`. Avec une répétition de 8 sur un épisode de mille pas, l'agent ne prend que cent vingt-cinq décisions. Les détails d'implémentation comptent : les récompenses des pas répétés sont **sommées**, et seule la **dernière** observation est conservée. La boucle d'un épisode compte donc \(\lceil T / \text{action\_repeat} \rceil\) pas d'agent.

Pourquoi faire cela ? Deux raisons, et la première est celle qui compte ici. Elle **raccourcit l'horizon de planification** : prévoir une seconde de temps réel demande douze pas de modèle si chaque pas en vaut huit, et quatre-vingt-seize pas sinon. Comme l'erreur d'un modèle s'accumule le long d'un déroulement, diviser par huit le nombre de pas nécessaires pour voir aussi loin est un gain direct sur la qualité du plan. Ensuite, elle **donne au modèle un signal plus net** : entre deux observations consécutives séparées de huit pas, il se passe quelque chose de visible, là qu'entre deux pas consécutifs il ne se passe presque rien et que le modèle apprend surtout à recopier son entrée.

{{% comment %}}SOURCE: PLANET p.2-3{{% /comment %}}

> [!WARNING]
 **La répétition d'action est le seul réglage qui change d'une tâche à l'autre, et c'est aussi le plus sensible.** Tous les autres hyperparamètres sont identiques sur les six tâches ; celui-là vaut 8 sur le pendule sur chariot, 4 sur le bras et sur le guépard, 4 sur la tasse, et 2 sur le doigt et sur le marcheur. Ce n'est pas arbitraire : il dépend de l'échelle de temps **physique** de la tâche. Une tâche qui demande des corrections rapides, comme garder un doigt sur une cible qui tourne, ne supporte pas qu'on la laisse huit pas sans décision. Et c'est précisément le genre de constante que la semaine 12 vous a appris à ne pas recopier : elle se dérive de l'échelle de temps du problème, pas d'un tableau.

{{% comment %}}SOURCE: PLANET p.12{{% /comment %}}

---

## Le code de la boucle, et tous les réglages en un tableau

**Le code.** L'agent complet. Quinze lignes utiles, et vous reconnaîtrez la structure d'une boucle de la semaine 5, à ceci près que ce qui s'entraîne est un modèle du monde et que ce qui agit est une recherche.

```python
def entrainer_agent(env, modele, optimiseur, n_amorce=5, intervalle=100,
                    taille_lot=50, longueur_troncon=50, action_repeat=4,
                    bruit_action=0.3, n_iterations=1000):
    """La boucle complete : amorcage aleatoire, puis alternance."""
    donnees = []                                   # D : le tampon d'episodes

    # 1. Amorcage : S episodes joues au hasard, car le modele ne sait rien.
    for _ in range(n_amorce):
        donnees.append(jouer_episode(env, politique=None,
                                     action_repeat=action_repeat))

    for _ in range(n_iterations):
        # 2. C pas d'entrainement du modele du monde sur des troncons tires.
        for _ in range(intervalle):
            lot = echantillonner_troncons(donnees, taille_lot, longueur_troncon)
            perte, _ = perte_du_modele(modele, *lot)
            optimiseur.zero_grad()
            perte.backward()
            optimiseur.step()

        # 3. UN episode collecte avec le planificateur, plus du bruit.
        donnees.append(jouer_episode(env, politique=modele,
                                     action_repeat=action_repeat,
                                     bruit=bruit_action))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{D}\) | les épisodes collectés ; **alimenté en continu**, à la différence de la section 13.12 | `donnees` |
| \(S\) | épisodes d'amorçage aléatoires, cinq | `n_amorce` |
| \(C\) | pas d'entraînement entre deux épisodes, cent | `intervalle` |
| \(B\) | nombre de tronçons par lot, cinquante | `taille_lot` |
| \(L\) | longueur d'un tronçon, cinquante pas | `longueur_troncon` |
| `action_repeat` | répétition d'action, de 2 à 8 ; **jamais écrit \(R\) dans ce cours** | `action_repeat` |
| \(\epsilon \sim \mathcal{N}(0, 0{,}3)\) | bruit d'exploration sur l'action | `bruit_action` |
| \(\alpha\) | pas d'apprentissage, \(10^{-3}\), optimiseur Adam | dans `optimiseur` |

Et voici, pour que vous les ayez en un seul endroit, les réglages restants : cellule récurrente de **200 unités** ; toutes les autres fonctions sont des réseaux à **deux couches denses de 200 unités** avec activation ReLU ; le latent est une **gaussienne diagonale de dimension 30** ; Adam avec un pas de \(10^{-3}\) ; lots de **50 tronçons de 50 pas** ; **3 nats libres**. Les trois réglages dont l'influence est la plus forte sont la répétition d'action, le poids \(\beta_{\mathrm{KL}}\) du terme de divergence, et le pas d'apprentissage.

{{% comment %}}SOURCE: PLANET p.12{{% /comment %}}

---
