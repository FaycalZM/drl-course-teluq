---
title: "1.10 Les enveloppes : modifier un environnement sans le réécrire"
weight: 11
---

## Ajouter une couche plutôt que réécrire le monde

Dernière section, et elle répond à un besoin très concret. Vous voudrez **accumuler les N dernières observations** dans un tampon pour les donner ensemble à l'agent, parce qu'une seule image ne suffit pas à connaître l'état d'un jeu dynamique : sur une image fixe, impossible de dire si la balle monte ou descend. Vous reconnaissez le problème de la section 1.2, l'observation n'est pas l'état, et la solution de la section 1.3, agrandir l'espace d'états. Vous voudrez aussi **recadrer ou prétraiter** des pixels, et **normaliser les récompenses** dont l'échelle rend l'entraînement instable. Dans les trois cas la structure est la même : **envelopper** un environnement existant et y ajouter une logique. Pas le réécrire : l'envelopper.

{{% comment %}}SOURCE: LAPAN ch.2 p.75{{% /comment %}}

C'est ce que fait la classe `Wrapper`. Elle **hérite de `Env`** et son constructeur prend un seul paramètre, l'`Env` à envelopper. Vous redéfinissez les méthodes que vous voulez étendre (typiquement `step()` ou `reset()`) et **vous devez appeler la méthode originale de la classe parente**, sinon la chaîne est rompue et l'environnement enveloppé ne reçoit jamais rien. Deux propriétés permettent de s'orienter dans la pile : `env` donne l'environnement immédiatement enveloppé, qui peut lui-même être une enveloppe, et `unwrapped` donne l'`Env` nu. Pour les cas courants, trois sous-classes de filtrage dispensent d'écrire autre chose qu'une fonction de transformation, et la **Figure 1-7** en montre la hiérarchie : `ObservationWrapper`, où l'on redéfinit `observation(obs)` ; `RewardWrapper`, où l'on redéfinit `reward(rew)` pour mettre la récompense à l'échelle ; et `ActionWrapper`, où l'on redéfinit `action(a)`, qui transforme l'action sur son trajet vers l'environnement enveloppé.

{{< bookfig src="01-07.png" week="01" >}}

{{% comment %}}SOURCE: LAPAN ch.2 p.76{{% /comment %}}

## Une enveloppe qui referme une boucle ouverte en section 1.1

Écrivons celle qui me plaît le plus pédagogiquement. Souvenez-vous du dilemme exploration-exploitation : un agent qui suit sa politique sans jamais s'en écarter reste enfermé dans ce qu'il connaît déjà. Remède : remplacer, de temps en temps, l'action de l'agent par une action au hasard, avec une probabilité \(\varepsilon\), disons 10 %.

```python
import random
import gymnasium as gym

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


env = EpsilonRandomAction(gym.make("CartPole-v1"))
```

{{% comment %}}SOURCE: LAPAN ch.2 p.75-77{{% /comment %}}

Treize lignes, et vous venez de lire l'une des méthodes les plus pratiques et les plus puissantes pour traiter le dilemme exploration-exploitation. Son effet est de faire **dériver l'agent hors des sentiers battus de sa politique**, sans rien changer à l'agent lui-même, qui n'a même pas conscience d'être perturbé. Vous retrouverez cette idée sous le nom de politique \(\varepsilon\)-gloutonne en semaine 4, puis au cœur de DQN en semaine 5. Prenez un agent complètement obtus, qui joue toujours l'action 0, et faites-le tourner sous cette enveloppe : vous verrez passer quelques actions aléatoires et la récompense grimpera un peu, pour un gain très petit mais gratuit.

{{% comment %}}SOURCE: LAPAN ch.2 p.75, p.78{{% /comment %}}

> [!TIP]
 **La propriété qui rend tout cela puissant :** comme `Wrapper` hérite de `Env` et expose la même interface, une enveloppe peut en envelopper une autre : on **imbrique les enveloppes aussi profondément qu'on veut**. En semaine 5, notre environnement Atari sera une pile de cinq ou six enveloppes posées sur l'environnement nu, chacune faisant une chose et une seule.

{{% comment %}}SOURCE: LAPAN ch.2 p.77{{% /comment %}}

## Voir ce que fait l'agent, depuis Colab

Deux enveloppes méritent une mention spéciale, car elles résolvent un problème très concret de ce cours : nous travaillons sur une machine distante sans écran. `HumanRendering` ouvre une fenêtre interactive : pratique sur votre machine, inutile sur Colab. `RecordVideo` écrit un fichier vidéo dans un dossier, qu'elle crée au besoin, et c'est celle-là qui nous intéresse : elle est précisément faite pour une machine distante sans interface graphique.

Les deux exigent que l'environnement ait été créé avec le mode de rendu adéquat, afin que `render()` renvoie des pixels au lieu d'afficher quoi que ce soit :

```python
env = gym.make("CartPole-v1", render_mode="rgb_array")
env = gym.wrappers.RecordVideo(env, video_folder="video")
```

{{% comment %}}SOURCE: LAPAN ch.2 p.78-79{{% /comment %}}

Vous utiliserez ce motif chaque fois que vous voudrez montrer un résultat plutôt que le décrire, et je vous y encourage : un agent qu'on regarde se tromper apprend beaucoup à celui qui l'a écrit. Notez l'ordre des deux lignes : l'enveloppe se pose **sur** un environnement déjà construit en mode `rgb_array`, et l'inverse ne fonctionne pas.

Gymnasium livre enfin une collection d'enveloppes bien plus large que ces quelques exemples : prétraitement standardisé des jeux d'arcade, normalisation des récompenses, empilement d'images, vectorisation pour faire tourner plusieurs environnements en parallèle, limitation du nombre de pas, celle-là même qui produit la troncature de la section 1.8. La liste complète est dans la documentation, et c'est l'un des rares endroits où je vous recommande d'aller flâner.

{{% comment %}}SOURCE: LAPAN ch.2 p.80{{% /comment %}}
