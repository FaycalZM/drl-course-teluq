---
title: "1.9 Session CartPole et agent aléatoire"
weight: 10
---

## Un chariot, un bâton, et le chiffre que vous allez mesurer

Assez de théorie : rencontrons l'environnement qui va nous accompagner jusqu'à la semaine 6, et mesurons notre point de départ.

CartPole appartient au groupe des problèmes de commande classique : une plateforme mobile, un bâton fixé à sa base par une articulation libre ; le bâton tend à tomber et la seule chose possible est de déplacer la plateforme vers la gauche ou vers la droite, à chaque pas, pour le rattraper. Mais ce qui en fait un excellent premier problème n'est pas sa mécanique, c'est son cadrage : il faut apprendre à équilibrer le bâton **sans connaître la signification des nombres observés**, uniquement en recevant la récompense. Nous, humains, savons qu'un des quatre nombres est un angle ; l'agent, lui, ne le sait pas. L'observation est faite de quatre flottants (position du chariot, sa vitesse, angle du bâton, sa vitesse angulaire) et la récompense vaut **1 à chaque pas de temps**, l'épisode se poursuivant tant que le bâton ne tombe pas. Conséquence élégante : une récompense accumulée plus grande signifie **exactement** un équilibre tenu plus longtemps.

{{% comment %}}SOURCE: LAPAN ch.2 p.71-72{{% /comment %}}

```pycon
>>> import gymnasium as gym
>>> e = gym.make("CartPole-v1")
>>> obs, info = e.reset()
>>> obs
array([ 0.02100407, 0.02762252, -0.01519943, -0.0103739 ], dtype=float32)
>>> info
{}
>>> e.action_space
Discrete(2)
>>> e.observation_space
Box([-4.8000002e+00 -3.4028235e+38 -4.1887903e-01 -3.4028235e+38], [4.8000002e+00
3.4028235e+38 4.1887903e-01 3.4028235e+38], (4,), float32)
```

Lisons, car tout ce que nous avons construit est là. L'observation initiale est un vecteur de quatre flottants proches de zéro : le chariot démarre à peu près au centre, à peu près immobile, le bâton à peu près vertical ; `info` est vide, comme annoncé. `action_space` vaut `Discrete(2)` : deux actions mutuellement exclusives, **0 pousse la plateforme à gauche, 1 la pousse à droite**. Voilà notre \(\mathcal{A}\), et il a deux éléments. `observation_space` est un `Box` de forme `(4,)`, les deux listes donnant les bornes basses puis les bornes hautes : position du chariot de −4,8 à 4,8 ; vitesse du chariot de −∞ à +∞ ; angle du bâton de −0,418 à 0,418 **radian** ; vitesse angulaire de −∞ à +∞.

{{% comment %}}SOURCE: LAPAN ch.2 p.71-73{{% /comment %}}

> [!TIP]
 **Pourquoi ces 3,4 × 10³⁸ qui font peur ?** Ce ne sont pas des valeurs atteignables, mais les extrema du type `float32`, que Python utilise pour représenter l'infini dans un `Box` stocké en simple précision. Deux des quatre composantes de CartPole sont donc **non bornées**, ce qui est normal pour une vitesse.

Et maintenant, l'objet le plus important de la semaine : **un pas**.

```pycon
>>> e.step(0)
(array([-0.01254663, -0.22985364, -0.01435183, 0.24902613], dtype=float32), 1.0, False,
False, {})
```

Décomposons ce quintuplet avec la table de la section 1.8 : la nouvelle observation ; `1.0`, la récompense, qui vaut toujours 1 ; `False`, `terminated`, le bâton n'est pas tombé ; `False`, `truncated`, la limite de temps n'est pas atteinte ; `{}`, le dictionnaire `info`. C'est l'intégralité de ce que l'agent reçoit du monde, à chaque pas, pendant tout l'entraînement.

Les deux espaces savent produire un élément aléatoire. `e.observation_space.sample()` renvoie un vecteur de quatre nombres pris dans les bornes (sans usage pratique, un état tiré au hasard ne correspondant à rien). `e.action_space.sample()` renvoie 0 ou 1 et sert, lui, **quand on ne sait pas quelle action choisir** : exactement la situation d'un agent au début de son entraînement, et celle de l'agent que nous écrivons maintenant.

{{% comment %}}SOURCE: LAPAN ch.2 p.73{{% /comment %}}

L'agent aléatoire tient alors en une boucle, et c'est exactement celle de la section 1.8 : tirer une action, appeler `step()`, accumuler la récompense, s'arrêter quand `terminated` **ou** `truncated` passe à `True`.

```python
import gymnasium as gym

env = gym.make("CartPole-v1")
obs, info = env.reset(seed=0)

total_reward = 0.0
total_steps = 0

while True:
 action = env.action_space.sample() # politique uniforme : notre référence
 obs, reward, terminated, truncated, info = env.step(action)
 total_reward += reward
 total_steps += 1
 if terminated or truncated:
 break

print(f"Épisode terminé en {total_steps} pas, récompense totale {total_reward:.2f}")
```

{{% comment %}}SOURCE: LAPAN ch.2 p.74{{% /comment %}}

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-01.ipynb" label="Mesurer l'agent aléatoire dans Colab" >}}

Ce programme mesure **un** épisode, et c'est déjà instructif. Mais un épisode ne prouve rien. Le laboratoire reprend cette boucle pour en faire une fonction, la lance sur cent épisodes et en tire une moyenne avec son écart-type ; c'est là que le chiffre de référence du cours sera établi.

Comme la récompense vaut 1 par pas, la récompense accumulée **est** la longueur de l'épisode, mesure particulièrement lisible. Une politique uniforme ne tient que quelques dizaines de pas ; le chiffre exact dépend de la graine et de la version de l'environnement, et c'est précisément pourquoi je ne vous l'annonce pas. Il nous faut en revanche un point de comparaison stable, et il existe : chaque environnement possède une **frontière de récompense** (*reward boundary*), la récompense moyenne qu'un agent doit obtenir sur **100 épisodes consécutifs** pour que l'environnement soit considéré comme résolu. Pour CartPole, elle est de **195**.

{{% comment %}}SOURCE: LAPAN ch.2 p.74-75{{% /comment %}}

> [!IMPORTANT]
 **Voilà votre point de départ : quelques dizaines de pas contre 195.** Un ordre de grandeur, qui sera franchi sous vos yeux : la méthode d'entropie croisée fera la plus grande partie du chemin en semaine 3, DQN finira le travail en semaine 5. Aujourd'hui, je vous demande seulement de **produire ce nombre vous-même**, au laboratoire : un chiffre qu'on a obtenu soi-même ne s'oublie pas.

Avec `reset()`, `step()`, les deux espaces et `sample()`, vous disposez d'environ **deux tiers** de l'interface de base et de la totalité des fonctions nécessaires pour commencer à écrire des agents. Le dernier tiers, les enveloppes, fait l'objet de la section suivante.

{{% comment %}}SOURCE: LAPAN ch.2 p.75{{% /comment %}}

## Préparer le jalon 1 : choisir votre environnement de projet

L'évaluation de ce cours est un projet continu, et son premier jalon, en semaine 3, suppose que vous ayez **choisi un environnement** et su justifier ce choix. La ressource à utiliser est **la documentation de Gymnasium**, et elle seule : c'est le catalogue officiel, il est à jour, et il est organisé par familles. On y trouve la commande classique comme CartPole, les jeux d'arcade, la physique articulée, et la possibilité de définir le vôtre. Méfiez-vous des listes d'environnements trouvées dans des livres ou des billets de blogue : elles vieillissent très vite et les noms changent. Pour choisir, posez-vous cinq questions, celles auxquelles cette semaine vous a appris à répondre.

1. **Quel est l'espace d'observations ?** Un `Box` de petite dimension se traite dès la semaine 3 ; des pixels exigent les techniques de la semaine 5 et un GPU.
2. **Quel est l'espace d'actions ?** `Discrete` ouvre tout le module 2 ; un `Box` d'actions continues vous mène directement en semaine 9 : beau projet, mais projet plus long.
3. **Les épisodes sont-ils longs ?** Un épisode de 10 000 pas multiplie le coût de chaque expérience.
4. **Y a-t-il une limite de temps**, donc une troncature ? Si oui, votre code devra la traiter séparément.
5. **Quel est le coût de calcul sur Colab ?** Un environnement qui demande huit heures de GPU n'est pas un projet de session.

Un dernier conseil, et il vaut pour les quatorze semaines : la tentation sera grande de choisir l'environnement le plus spectaculaire du catalogue. Prenez-en d'abord un qui tourne en trente secondes, faites-le fonctionner de bout en bout, **puis** augmentez l'ambition. J'ai vu beaucoup plus de projets échouer par environnement trop lourd que par algorithme trop simple.
