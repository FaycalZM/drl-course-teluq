---
title: "1.7 L'API Gymnasium : Env et Space"
weight: 8
---

## Une convention commune, pour que vos agents se réutilisent

Si chaque laboratoire du cours définissait son propre environnement avec ses propres noms de méthodes, aucun agent ne serait réutilisable d'une semaine à l'autre. Il nous faut une convention commune, et elle existe. OpenAI a publié Gym en 2017 et l'interface est devenue le standard de fait ; en 2021, l'équipe a transféré le développement à la **Fondation Farama** sous le nom de **Gymnasium**, une bifurcation qui conserve la même interface : un remplacement direct, au sens où il suffit en général d'écrire `import gymnasium as gym` pour que du code existant fonctionne. Une immense quantité de tutoriels en ligne commence encore par `import gym` ; dans ce cours, ce sera **toujours** `import gymnasium as gym`.

{{% comment %}}SOURCE: LAPAN ch.2 p.64{{% /comment %}}

Quelle que soit sa complexité, un environnement doit rendre quatre services : dire quelles actions sont permises, décrire la forme et les bornes des observations, exécuter une action (`step()`), se réinitialiser (`reset()`). Les deux premiers ne sont pas des opérations mais des **descriptions**. Or les actions peuvent être discrètes ou continues et bornées (un volant tourne de −720° à +720°, une pédale d'accélérateur va de 0 à 1), et il faut pouvoir en combiner plusieurs, puisqu'une voiture a un volant **et** une pédale. La même remarque vaut pour les observations, qui peuvent elles aussi être discrètes : l'état d'une ampoule, donné comme un booléen. Puisque actions et observations ont le même besoin (décrire un ensemble de valeurs possibles), on les décrit avec **la même abstraction**.

{{% comment %}}SOURCE: LAPAN ch.2 p.64-65{{% /comment %}}

---

## La classe `Space`

Cette abstraction est la classe `Space`, dont la **Figure 1-6** donne la hiérarchie. Elle expose une propriété et trois méthodes, toutes abstraites et réimplémentées par chaque sous-classe : `shape`, la forme de l'espace, avec la même signification que pour un tableau NumPy ; `sample()`, qui renvoie un élément tiré au hasard ; `contains(x)`, qui teste l'appartenance ; et `seed()`, qui fixe la graine du générateur aléatoire, propagée aux sous-espaces, ce qui rend une exécution reproductible.

{{< bookfig src="01-06.png" week="01" >}}

La hiérarchie compte trois sous-classes, dont deux nous suffiront presque tout le cours. **`Discrete(n)`** décrit un ensemble de `n` éléments mutuellement exclusifs, numérotés de 0 à `n − 1`, un argument optionnel `start` permettant de décaler la numérotation : quatre directions, c'est `Discrete(n=4)`. **`Box(low, high, shape, dtype)`** décrit un tenseur de réels de dimension quelconque, chaque coordonnée étant comprise entre `low` et `high`. Et **`Tuple`**, la troisième, compose plusieurs espaces en un seul.

```python
import numpy as np
from gymnasium.spaces import Box, Discrete, Tuple

# Une pédale d'accélérateur : un seul réel entre 0 et 1.
pedal = Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)

# Un écran de jeu Atari : hauteur, largeur, trois plans de couleur.
screen = Box(low=0, high=255, shape=(210, 160, 3), dtype=np.uint8)

# Tuple emboîte plusieurs espaces : les trois commandes continues
# d'une voiture, un clignotant à trois positions, un klaxon à deux.
car = Tuple((
    Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32),
    Discrete(n=3),
    Discrete(n=2),
))
```

{{% comment %}}SOURCE: LAPAN ch.2 p.66-67{{% /comment %}}

Arrêtons-nous sur l'écran Atari, car le chiffre est instructif : 210 × 160 × 3 octets, cela fait **100 800 octets par observation**, pour une seule image. Multipliez par le nombre de pas d'un épisode, puis par le nombre d'épisodes d'un entraînement, et vous comprenez pourquoi les semaines 5 et 7 consacreront du temps à réduire les observations avant de les stocker.

La voiture du dernier exemple montre à quoi sert `Tuple` : un véhicule a des commandes continues **et** des interrupteurs, et il faut bien décrire les deux à la fois. En pratique l'espace composé est rare : nous nous servirons de `Box` et de `Discrete` pendant tout le cours, et c'est aussi ce que fait la quasi-totalité du code que vous lirez. Mais vous le rencontrerez dans la documentation, aux côtés d'autres sous-classes plus spécialisées (`Sequence`, `Text`, `Graph`), et je préfère que vous sachiez à quoi il correspond plutôt que de le découvrir dans un message d'erreur.

Retenez enfin le point qui rend l'interface utile : tout environnement Gymnasium expose **exactement deux** membres de type `Space`, `action_space` et `observation_space`. C'est cette uniformité, et elle seule, qui permet d'écrire un agent **indépendant de l'environnement** : du code qui lit `env.action_space` sans savoir s'il pilote un pendule ou un jeu d'arcade. Vos projets en vivront.

{{% comment %}}SOURCE: LAPAN ch.2 p.67{{% /comment %}}
