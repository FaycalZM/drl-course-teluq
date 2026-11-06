---
title: "9.1 L'action devient un vecteur"
weight: 2
---

## D'un entier à un vecteur de réels

Jusqu'ici, une action était un **entier**. Un indice dans une liste finie : 0 pour gauche, 1 pour droite, et `env.step(2)` était un appel parfaitement explicite. Toute l'ingénierie des semaines 5 à 7 reposait là-dessus, jusqu'au nombre de sorties du réseau.

Une action continue est autre chose. Elle prend une valeur dans un intervalle, et cet intervalle contient une infinité d'éléments. Si vous commandez l'angle d'une articulation, vous pouvez demander 13,5 degrés, ou 13,512 degrés, et les deux commandes ne produiront pas le même mouvement. Il existe bien des limites physiques, une articulation ne tournant pas à 720 degrés, mais entre les deux bornes l'ensemble des valeurs atteignables reste immense. C'est un **espace d'actions continu** (*continuous action space*), et ce n'est pas un cas exotique : dès que l'agent parle à un monde physique, une commande continue est bien plus probable qu'un menu de choix discrets. Un volant, un accélérateur, un couple moteur, une tension, un débit : rien de tout cela ne s'énumère.

{{% comment %}}SOURCE: LAPAN ch.15 p.463{{% /comment %}}

L'interface, elle, est très simple, et c'est une bonne nouvelle. Là où un espace discret était décrit par un objet `Discrete(n)`, un espace continu est décrit par un objet `Box`, qui porte trois informations : une borne inférieure, une borne supérieure et une **forme**. L'espace d'actions du robot que nous allons rencontrer dans un instant s'écrit `Box(low=-1, high=1, shape=(8,))` : huit nombres réels, chacun entre \(-1\) et \(1\). La méthode `step()` ne reçoit donc plus un entier mais un vecteur NumPy de huit composantes, et chacune des huit sera appliquée à un moteur différent au même instant. Et si un problème demande à la fois un choix discret et une commande continue, par exemple tirer ou ne pas tirer tout en orientant une tourelle, les espaces se composent dans un espace de type `Tuple` qui agrège des sous-espaces de natures différentes.

{{% comment %}}SOURCE: LAPAN ch.15 p.464{{% /comment %}}

```python
import gymnasium as gym
import numpy as np

env = gym.make("Pendulum-v1")

print(env.action_space)            # Box(-2.0, 2.0, (1,), float32)
print(env.action_space.shape)      # (1,)  -> UNE dimension d'action
print(env.action_space.low)        # [-2.]
print(env.action_space.high)       # [ 2.]

# L'action n'est plus un entier : c'est un tableau de la forme shape.
action = np.array([0.37], dtype=np.float32)
obs, recompense, termine, tronque, info = env.step(action)

# Et le tirage au hasard d'une action valide ne se fait plus avec randint :
action_au_hasard = env.action_space.sample()   # respecte low, high et shape
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{A}\) | ensemble des actions, désormais un pavé de \(\R^n\) | `env.action_space` |
| \(n\) | nombre de dimensions d'action | `env.action_space.shape[0]` |
| \(a_{\min}\), \(a_{\max}\) | bornes de l'intervalle, par dimension | `action_space.low`, `action_space.high` |
| \(a \in \R^n\) | une action, vecteur de réels | `action`, tableau NumPy |

> [!NOTE]
 **Deux réflexes à prendre tout de suite.** Premier réflexe : lisez `shape` avant d'écrire la dernière couche de votre acteur. En espace discret, le nombre de sorties valait `action_space.n` ; ici il vaut `action_space.shape[0]`, et confondre les deux produit une erreur de dimension à la première action jouée, ce qui est le meilleur des cas. Second réflexe : lisez `low` et `high`. Beaucoup d'environnements continus normalisent leurs commandes dans \([-1,1]\), ce qui s'accorde parfaitement avec une tangente hyperbolique en sortie de réseau, mais ce n'est pas une règle : `Pendulum-v1` accepte un couple dans \([-2,2]\), et un acteur borné à \([-1,1]\) y perd la moitié de son autorité sans qu'aucun message d'erreur ne vous le dise.

---

## Où meurt l'argmax

Reprenons maintenant la maximisation de l'introduction, et regardons-la de près dans les deux régimes. La **Figure 9-1** met les deux côte à côte, et c'est l'image de la semaine : à gauche, l'opération que nous faisions ; à droite, ce qu'il en reste.

{{< bookfig src="09-01.png" week="09" >}}

Du côté discret, l'équation d'optimalité de Bellman pour les valeurs d'action s'écrit, et se calcule :

$$
q_*(s,a) = \E_{s' \sim p}\left[\, r(s,a) + \gamma \max_{a'} q_*(s',a') \,\right]
$$

{{% comment %}}SOURCE: SPINUP ddpg/key-equations{{% /comment %}}

Le terme \(\max_{a'}\) y est une opération de coût fini et connu : \(k\) évaluations, ou une seule évaluation à \(k\) sorties, puis une comparaison. C'est ce terme que le réseau Q profond calculait sur son réseau cible, à chaque élément de chaque lot, depuis la semaine 5.

Du côté continu, le même terme demande de maximiser une fonction non convexe sur un pavé de \(\R^n\). On ne peut pas évaluer l'espace de façon exhaustive, et poser le problème à un algorithme d'optimisation générique en ferait un sous-programme très coûteux, qu'il faudrait relancer chaque fois que l'agent veut agir, c'est-à-dire des millions de fois par entraînement. Ce n'est pas acceptable, et c'est la raison d'être de toute la semaine.

{{% comment %}}SOURCE: SPINUP ddpg/background{{% /comment %}}

La sortie de secours tient en une hypothèse, et je veux que vous la voyiez comme une hypothèse et non comme un théorème. Si \(q_*(s,a)\) est **dérivable par rapport à \(a\)**, alors le maximum sur les actions peut être **approché** par la valeur prise en un point bien choisi, fourni par une fonction apprise \(\mu_\theta\) :

$$
\max_a q(s,a) \;\approx\; q\!\left(s, \mu_\theta(s)\right)
$$

{{% comment %}}SOURCE: SPINUP ddpg/key-equations{{% /comment %}}

Lisez cette ligne lentement, parce qu'elle contient la section 9.3 en entier. La maximisation n'est pas résolue : elle est **remplacée** par un passage avant dans un second réseau, dont tout le métier est de proposer, pour chaque état, une action de grande valeur. Le signe \(\approx\) n'est pas décoratif. Rien ne garantit que \(\mu_\theta(s)\) soit l'argument du maximum, et la section 9.5 vivra précisément du fait qu'il ne l'est pas.

> [!IMPORTANT]
 **Deux lectures de la même ligne, et la seconde est celle qui organise la semaine.** Première lecture, optimiste : nous venons de remplacer une optimisation impraticable par une multiplication de matrices. Seconde lecture, exacte : nous venons de remplacer un **maximum** par l'**estimation** d'un maximum, et nous allons devoir apprendre cette estimation en même temps que la valeur qu'elle maximise. Les deux apprentissages se nourrissent l'un de l'autre, et la section 9.5 montrera que cette boucle a une direction préférée, qui est la surestimation.

---

## Pourquoi discrétiser n'est pas la réponse

À ce point, presque tout le monde propose la même idée, et c'est une bonne idée à avoir : puisque nos méthodes savent traiter un ensemble fini d'actions, découpons l'intervalle en tranches et retombons sur du discret. Trois niveaux de couple par moteur, par exemple : plein arrière, rien, plein avant.

Trois faits avant de faire le calcul : l'ensemble des valeurs possibles est pratiquement infini, on ne peut pas l'évaluer exhaustivement, et le robot de cette semaine commande huit moteurs.

Un espace d'actions à \(n\) dimensions, découpé en \(k\) niveaux par dimension, produit \(k^n\) actions composites, parce qu'il faut un indice pour chaque **combinaison** de niveaux. Pour huit moteurs :

- \(k = 3\), soit trois niveaux par moteur : \(3^8 = 6\,561\) actions ;
- \(k = 5\) : \(5^8 = 390\,625\) actions ;
- \(k = 10\), ce qui serait encore une résolution grossière pour un couple : \(10^8 = 100\,000\,000\) actions.

Vous voyez immédiatement où cela casse. Mais regardez surtout **lequel des deux nombres** fait le dégât. Passer de trois à cinq niveaux, c'est améliorer la résolution d'un facteur modeste, et cela multiplie le nombre d'actions par soixante. La dimension est en exposant, et c'est elle qui tue : la même découpe à trois niveaux donne 9 actions pour deux moteurs, ce qui est parfaitement praticable, et 6 561 pour huit, ce qui ne l'est plus. Un réseau Q profond à 6 561 sorties n'est pas seulement lourd, il est **statistiquement** intenable : chaque sortie doit être estimée à partir des transitions où cette combinaison exacte a été jouée, et il n'y en aura presque aucune.

Et il y a un second coût, moins visible et plus grave : la résolution que vous avez sacrifiée. Un quadrupède auquel on demande de marcher avec trois niveaux de couple par moteur ne résout pas une version approchée du problème de marche, il résout un **autre** problème, plus brutal, dont la solution ne se raffine pas en diminuant le pas de la grille.

Nous avons déjà rencontré cette leçon, du côté des observations : en semaines 4 et 5, le cours a montré que découper un espace d'observations continu en cases crée plus de problèmes qu'il n'en résout, et c'est ce constat qui a justifié le passage à l'approximation de fonction. Le même raisonnement s'applique maintenant du côté des actions, avec une aggravation : les observations, on les subit, alors que les actions, on les produit, et c'est la dernière couche du réseau qui porte le coût.

{{% comment %}}SOURCE: index/notes/week-09.md gap 1 : raisonnement propre au cours{{% /comment %}}

> [!TIP]
 **Quand la discrétisation est-elle une bonne idée ? Quand \(n\) est petit.** Je ne veux pas que vous reteniez « discrétiser, c'est mal ». Sur une dimension d'action unique, comme le couple du pendule du laboratoire, découper en onze niveaux et lancer un réseau Q profond de la semaine 6 est une solution raisonnable, rapide à écrire, et c'est même un point de comparaison honnête. La règle à retenir est donc dimensionnelle : la discrétisation reste praticable sur une ou deux dimensions d'action, et elle devient absurde dès que la dimension dépasse quelques unités. Le reste de la semaine traite le second cas.

---

## Le robot de la semaine, et l'outillage qui va avec

Assez d'abstraction : voici la tâche qui a motivé tout ce pan de l'histoire du domaine. Un robot quadrupède simulé, de la taille d'un gros jouet, qui doit apprendre à avancer. La **Figure 9-2** le montre dans son simulateur.

{{< bookfig src="09-02.png" week="09" >}}

Ses chiffres disent tout de la différence avec Atari. L'observation est un vecteur de **28 nombres** : vitesses, positions et accélérations des différentes parties du corps. L'action est un vecteur de **8 nombres**, un par moteur. La récompense est la distance parcourue **moins** l'énergie dépensée, ce qui est une belle récompense composite : elle interdit la solution brutale qui consisterait à tout mettre à fond. Un épisode est limité à 1 000 pas, et la tâche est considérée comme résolue à partir d'un retour de 15.

{{% comment %}}SOURCE: LAPAN ch.15 p.465-466{{% /comment %}}

Regardez l'écart avec le module 2 : 28 nombres en entrée au lieu d'une pile d'images, donc des réseaux entièrement connectés de taille modeste et aucune convolution. L'« intelligence visuelle » n'est pas le sujet ici ; la coordination de huit commandes simultanées l'est.

Un mot d'outillage, parce qu'il a des conséquences pratiques immédiates pour vous. Le simulateur physique qui sert de référence dans ce domaine, MuJoCo, a longtemps été un logiciel commercial payant ; il a été racheté puis ouvert en 2022, et il s'installe aujourd'hui comme une simple roue Python. Gymnasium livre ses environnements de robotique par `gymnasium[mujoco]`, et ce chemin est le chemin maintenu.

{{% comment %}}SOURCE: LAPAN ch.15 p.464-465{{% /comment %}}

**Le laboratoire ne suivra donc pas la pile historique de ce domaine, et je vous dois la raison.** Le robot de la Figure 9-2 tourne sur un autre moteur physique, PyBullet, qui n'a jamais été porté vers l'interface de Gymnasium : l'utiliser impose d'installer à côté de Gymnasium une version figée de l'ancienne bibliothèque `gym`, c'est-à-dire de faire cohabiter deux interfaces incompatibles dans le même carnet. Pour une semaine dont le sujet est l'espace d'actions et non la plomberie, le prix est trop élevé. Nous mesurerons donc sur `Pendulum-v1`, qui est un environnement de contrôle classique de Gymnasium, sans moteur physique externe, à **une seule dimension d'action**, et dont un épisode dure quelques secondes. Et nous garderons un robot MuJoCo pour la **démonstration** finale, rendu hors écran et exporté en vidéo, parce que voir un corps apprendre à se déplacer vaut le détour, mais sans jamais lui demander de porter une mesure.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

> [!NOTE]
 **Nommer l'environnement exactement, et pas « le pendule ».** Il existe dans l'écosystème au moins deux pendules : `Pendulum-v1`, du contrôle classique, qui demande de redresser puis de maintenir une tige à partir d'une position quelconque, et `InvertedPendulum-v1`, qui est un environnement MuJoCo. Ils n'ont ni la même dynamique, ni la même échelle de récompense, ni la même difficulté. Toutes les mesures de cette semaine se font sur `Pendulum-v1`, et je donnerai en section 9.6 la raison expérimentale, chiffrée, pour laquelle le second serait un très mauvais choix.

---
