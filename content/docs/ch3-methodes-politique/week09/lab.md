---
title: "Laboratoire"
weight: 8
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté. Il n'y a pas de jalon cette semaine, le prochain est en semaine 10, qui ferme le module 3.

Les trois volets suivent la semaine, et ils partagent **un seul programme**. Le volet A écrit la boucle de la section 9.3 et la fait apprendre. Le volet B y ajoute quinze lignes et **mesure la surestimation**, c'est-à-dire produit le nombre que la section 9.5 a refusé de vous donner. Le volet C ouvre trois interrupteurs dans le même programme et reproduit la **forme** du Tableau 9-2 sur une tâche qui tient dans un carnet. Puis une démonstration, non mesurée, fait marcher un robot.

Deux décisions de conception du laboratoire, et je vous dois les deux raisons.

**La tâche de mesure est `Pendulum-v1`, nommée avec son identifiant exact.** C'est un environnement de contrôle classique de Gymnasium, sans moteur physique externe à installer, à **une seule dimension d'action**, un couple dans \([-2,2]\), et dont un épisode dure quelques secondes. Le pendule inversé de MuJoCo, `InvertedPendulum-v1`, serait un mauvais choix pour la raison chiffrée donnée en fin de section 9.6 : il sature, et une ablation menée dessus ne mesurerait rien.

**Je ne vous donne aucun score à atteindre, et c'est volontaire.** Tous les nombres que cette semaine a cités portent sur d'autres tâches : un robot quadrupède à huit moteurs sur cinq ou neuf millions de trames, et quatre tâches de locomotion à un million de pas. Aucun ne s'applique à ce que vous allez exécuter. Interpoler entre eux pour vous donner une cible rassurante serait inventer un chiffre, et je m'y refuse. Ce que j'attends est donc une mesure **relative** et **reproductible** : votre propre score, obtenu sur au moins trois graines, avec son intervalle, et comparé à vos propres autres configurations sur les mêmes graines. Commencez par une **exécution pilote** d'une seule graine pour fixer votre propre cible, et annoncez-la dans votre rapport : c'est exactement ce qu'on fait quand aucune référence extérieure n'existe.

{{% comment %}}SOURCE: index/notes/week-09.md gap 3{{% /comment %}}

> [!WARNING]
 **Trois pièges de ce laboratoire, et ils coûtent chacun une soirée.** Premier piège, **les deux optimiseurs** : la rétropropagation de la perte de l'acteur traverse le critique et y dépose des gradients ; sans remise à zéro explicite, votre critique apprend à maximiser sa propre sortie. Deuxième piège, **l'évaluation avec bruit** : si vous mesurez avec le bruit d'exploration activé, vous mesurez votre réglage de bruit autant que votre politique, et vos comparaisons entre configurations perdent tout sens. Troisième piège, **l'échelle de l'action** : `Pendulum-v1` attend un couple dans \([-2,2]\) et votre acteur sort une tangente hyperbolique dans \([-1,1]\). Multipliez par la demi-étendue de l'espace d'actions, une fois, au bon endroit, ou votre agent n'aura jamais accès qu'à la moitié de son autorité et vous chercherez le bogue dans votre fonction de perte.

---

## Volet A : la boucle déterministe sur `Pendulum-v1`

**Objectif.** Écrire la boucle en neuf étapes de la section 9.3, de bout en bout, et la faire apprendre.

**Étape 1.** Les deux réseaux, acteur et critique, repris des fragments de la section 9.3. Gardez les tailles 400 et 300 : elles sont petites et ce n'est pas là que votre temps se joue.

**Étape 2.** Le tampon de rejeu. Vous l'avez écrit en semaine 5 ; la seule différence est que le champ `action` est désormais un vecteur de flottants et non un entier, donc un tableau de forme `(capacite, n_actions)` et non `(capacite,)`.

**Étape 3.** Le bruit d'exploration **gaussien non corrélé**, d'amplitude constante, exprimée en fraction de la demi-étendue de l'espace d'actions. Ajoutez une phase de **démarrage uniforme** : pendant les premiers pas, ignorez l'acteur et appelez `env.action_space.sample()`. Journalisez l'écart quadratique moyen entre l'action envoyée et l'action proposée, qui est votre amplitude effective après écrêtage de l'action.

**Étape 4.** Les deux pas d'optimisation, chacun avec son optimiseur, puis la synchronisation douce. Vérifiez par une assertion, une fois, que les gradients du critique sont bien nuls au moment où vous appelez son optimiseur.

**Étape 5.** L'évaluation, **sans bruit**, sur dix épisodes, tous les quelques milliers de pas.

**Quatre vérifications arithmétiques avant d'interpréter la moindre courbe.** Premièrement, l'action envoyée à l'environnement doit toujours être dans \([-2,2]\) : une assertion à l'appel de `step()`. Deuxièmement, la valeur prédite par le critique doit avoir le même **signe** que les retours que vous observez ; sur cette tâche les récompenses sont négatives, donc une valeur prédite positive est un bogue de signe, pas un apprentissage optimiste. Troisièmement, au tout début de l'entraînement, la valeur prédite doit être proche de zéro, puisque les poids sont initialisés petits. Quatrièmement, votre cible et votre prédiction doivent avoir **exactement la même forme** de tenseur : une erreur de diffusion entre `(100, 1)` et `(100,)` ne lève aucune exception et calcule une erreur quadratique entre 10 000 paires au lieu de 100.

**Attendu.** La courbe d'évaluation sur au moins trois graines avec intervalle, votre amplitude de bruit effective, et votre cible annoncée à partir de l'exécution pilote.

{{< colab url="TODO" label="Volet A : politique déterministe et critique à deux entrées sur Pendulum-v1" >}}

---

## Volet B : la surestimation, mesurée par vous

**Objectif.** Produire **une** figure à deux courbes : la valeur moyenne estimée par le critique, et le retour actualisé réellement obtenu, sur la même abscisse. L'écart entre les deux est la surestimation, et c'est le nombre que la section 9.5 ne vous a pas donné.

**Étape 1.** Au début de l'entraînement, après la phase de démarrage uniforme, tirez un ensemble d'états dans le tampon et **figez-le**. Quelques centaines suffisent sur cette tâche ; conservez-les, et ne les retirez jamais.

**Étape 2.** À chaque évaluation, calculez la valeur moyenne que le critique attribue à ces états, l'action étant celle que l'acteur propose, puis le retour actualisé moyen réellement collecté depuis ces mêmes états en suivant la politique **sans bruit**. Le fragment de code de la section 9.5 fait les deux.

**Étape 3.** Tracez les deux courbes, et répondez par écrit à trois questions. La surestimation apparaît-elle sur votre tâche ? À quel moment de l'entraînement apparaît-elle ? Et son signe est-il stable, ou votre critique sous-estime-t-il parfois ?

**Étape 4, et c'est l'étape qui transforme ce volet en expérience.** Refaites la mesure avec le **double Q écrêté** activé, toutes choses égales d'ailleurs, sur les mêmes graines. Comparez l'écart entre les deux courbes dans les deux configurations. Vous venez de reproduire, à votre échelle, la mesure décrite en section 9.5.

**Une mise en garde sur le coût.** Le retour réellement collecté demande de **jouer** des épisodes, donc du temps de simulation. Sur `Pendulum-v1` un épisode dure quelques secondes de calcul ; ne mesurez pas sur mille épisodes comme le protocole décrit en section 9.5, mesurez sur une dizaine, et dites dans votre rapport que votre moyenne porte sur dix épisodes. Une mesure bruitée et annoncée comme telle vaut infiniment mieux qu'une mesure propre et non reproductible.

**Attendu.** La figure à deux courbes, dans les deux configurations, sur au moins trois graines, et votre réponse écrite aux trois questions.

{{< colab url="TODO" label="Volet B : mesurer la surestimation du critique, avec et sans double Q écrêté" >}}

---

## Volet C : l'ablation des trois correctifs

**Objectif.** Reproduire la **forme** du Tableau 9-2 sur votre tâche : pas ses nombres, qui portent sur d'autres environnements, mais le motif de ce qui aide, de ce qui n'aide pas, et de ce qui nuit.

**Étape 1, et c'est la plus importante : un seul programme, trois interrupteurs.** Votre code doit accepter trois indicateurs indépendants, `--double-q-ecrete`, `--delai-politique` et `--lissage-cible`, et rien d'autre ne doit changer entre deux exécutions. C'est l'étude d'ablation à une variable de la semaine 6, appliquée à trois variables.

**Étape 2, les configurations.** Lancez au minimum ces cinq-là, sur les mêmes graines :

| Configuration | Double Q écrêté | Délai de politique | Lissage de la cible |
| --- | --- | --- | --- |
| Base | non | non | non |
| Base + correctif 1 | **oui** | non | non |
| Base + correctif 2 | non | **oui** | non |
| Base + correctif 3 | non | non | **oui** |
| Les trois | **oui** | **oui** | **oui** |

Et si votre budget de calcul le permet, ajoutez les trois configurations « les trois, moins un », qui sont celles où le Tableau 9-2 réserve sa surprise.

**Étape 3, le protocole, et il n'est pas négociable.** Au moins trois graines par configuration, évaluation **sans bruit**, et un intervalle autour de chaque moyenne. Si vos intervalles se recouvrent, votre conclusion est « je ne mesure pas de différence », et c'est une conclusion parfaitement acceptable que je préfère de loin à un classement inventé sur une seule exécution. Dites aussi, en une phrase, ce que trois graines vous autorisent à conclure de moins que dix.

**Étape 4, la lecture.** Pour chacun des trois correctifs, répondez : sur ma tâche, ce correctif aide-t-il, ne change-t-il rien, ou nuit-il ? Et surtout, votre tâche à une dimension d'action **souffre-t-elle** du défaut de la section 9.5 ? Si votre volet B montre peu de surestimation, vous devez vous attendre à ce que le correctif 1 n'apporte rien, et l'observer serait une confirmation, pas un échec.

**Étape 5, la comparaison des deux bruits, en une ligne.** La bibliothèque haut niveau installée pour la solution courte fournit les deux bruits d'exploration de la section 9.4 comme deux objets interchangeables. Lancez la même méthode avec l'un puis l'autre, mêmes graines, et mesurez. Si vous ne trouvez aucune différence, vous venez de retrouver par vous-même ce que les trois constats de la section 9.4 annonçaient, et c'est le meilleur résultat possible pour cet exercice.

```python
# La solution courte, pour verifier votre implementation et comparer les bruits.
# A executer APRES avoir ecrit la votre, jamais avant.
import numpy as np
from stable_baselines3 import TD3
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

n_actions = 1
sigma = 0.1 * np.ones(n_actions)

bruit_simple = NormalActionNoise(mean=np.zeros(n_actions), sigma=sigma)
bruit_correle = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=sigma)

for nom, bruit in [("non correle", bruit_simple), ("correle", bruit_correle)]:
    modele = TD3("MlpPolicy", "Pendulum-v1", action_noise=bruit, seed=0, verbose=0)
    modele.learn(total_timesteps=30_000)
    # Puis evaluer SANS bruit, sur plusieurs graines, et comparer.
```

**Attendu.** Le tableau de vos cinq configurations avec graines et intervalles, votre lecture des trois correctifs, et le résultat de la comparaison des deux bruits.

{{< colab url="TODO" label="Volet C : ablation des trois correctifs et comparaison des deux bruits d'exploration" >}}

---

## Démonstration : un robot, en vidéo, sans écran

Cette partie n'est **pas** mesurée, et c'est assumé. Elle est là parce que voir un corps simulé apprendre à se déplacer vaut le détour, et parce que vous devez savoir produire une vidéo depuis un carnet sans affichage.

Le simulateur s'installe comme une roue Python, par `gymnasium[mujoco]`. Le rendu se fait **hors écran** : le carnet n'a pas d'écran, donc l'environnement est créé avec un mode de rendu qui renvoie des images en mémoire, et une enveloppe d'enregistrement écrit la suite d'images dans un fichier vidéo que vous téléchargez ensuite. Vous reconnaissez la mécanique des enveloppes de la semaine 1, appliquée à la sortie plutôt qu'à l'entrée.

```python
import gymnasium as gym

# Verifiez l'identifiant exact dans VOTRE installation : les suffixes de version
# des environnements MuJoCo changent d'une version de Gymnasium a l'autre, et
# gymnasium.pprint_registry() en donne la liste.
ID_ROBOT = "Hopper-v5"

# Rendu hors ecran : les images sont renvoyees en memoire, jamais affichees.
env = gym.make(ID_ROBOT, render_mode="rgb_array")
env = gym.wrappers.RecordVideo(env, video_folder="videos", name_prefix="demo")

obs, _ = env.reset(seed=0)
termine = tronque = False
while not (termine or tronque):
    action = agir_sans_bruit(acteur, obs, env, device)
    obs, _, termine, tronque, _ = env.step(action)
env.close()        # INDISPENSABLE : c'est close() qui finalise le fichier video.
```

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

**Attendu.** Une vidéo, et deux phrases. La première décrit ce que votre agent fait de travers, et la seconde dit ce que vous changeriez pour le corriger. Le robot qui tombe vers l'avant au bout de onze secondes, dont la section 9.3 vous a donné la mesure, est un comportement **appris** et non un échec : c'est une démarche, instable, et la décrire est un exercice d'observation que ce cours n'a pas encore demandé.

{{< colab url="TODO" label="Démonstration : un robot simulé, rendu hors écran et exporté en vidéo" >}}

> [!TIP]
 **Mon message pour ce laboratoire.** Faites les volets dans l'ordre, même si le volet C est le plus intéressant. La raison est celle de toute la semaine : vous n'avez, dans cette famille de méthodes, **aucune** perte dont la valeur vous dise si les choses se passent bien. La perte du critique peut descendre pendant que l'agent se dégrade, et la perte de l'acteur n'est que l'opposé d'une note qu'il s'attribue à lui-même. Le volet A vous donne des repères, le volet B vous donne le seul diagnostic honnête que cette semaine connaisse, et le volet C ne devient interprétable **qu'après** le volet B : savoir si votre tâche souffre de surestimation est ce qui vous permettra de dire si le premier correctif devait aider. Sans ce préalable, le volet C produit un tableau de nombres et aucune conclusion.

---
