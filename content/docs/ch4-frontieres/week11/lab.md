---
title: "Laboratoire"
weight: 9
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté, puisque le jalon 3 s'est fermé la semaine dernière et que le jalon 4 est en semaine 14. J'en profite pour vous demander quelque chose qu'une semaine notée rend difficile : **laissez le volet A échouer complètement**, et passez du temps à regarder comment il échoue. C'est la seule façon d'acquérir le réflexe de la section 11.7.

Les trois volets partagent **une seule tâche** et **un seul programme**, variantes activées en ligne de commande, comme depuis le jalon 1. La tâche est `MountainCar-v0`, et ce choix n'est pas un choix de confort : c'est la tâche de ce cours sur laquelle la méthode \(\varepsilon\)-gloutonne échoue **complètement**, ce qui en fait le seul banc d'essai honnête pour une semaine d'exploration. Elle est par ailleurs très bon marché, elle tourne sur processeur ordinaire, et un épisode y dure deux cents pas au maximum.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

**Le protocole de mesure est celui du jalon 2, et il s'applique sans que je le redemande** : au moins **trois graines** par configuration, un **intervalle** sur chaque courbe, et un **critère d'arrêt déclaré d'avance**. Deux exigences propres à cette semaine s'y ajoutent, et elles viennent directement des sections 11.4 et 11.6 :

- **Mesurez le temps jusqu'à la première atteinte du but**, et pas seulement le retour final. Le Tableau 11-1 a montré que les deux grandeurs ne classent pas les méthodes dans le même ordre, et c'est l'observation que je veux vous voir reproduire.
- **Évaluez toujours sur un environnement sans prime**, et étiquetez comme telles les courbes mesurées sous enveloppe. Une courbe d'entraînement sous prime et une courbe d'évaluation ne sont pas la même grandeur.

---

## Échauffement : reproduisez les trois nombres de River Swim

Avant de toucher à MountainCar, un échauffement de dix minutes, et il n'est pas décoratif : il vous donne la mesure de la semaine dans vos propres mains.

Reprenez le fragment de la section 11.2, complétez-le, et reproduisez les trois comptages : 100 pas, 1 000 pas, 10 000 pas, dix pas par épisode, agent purement aléatoire. Vérifiez **par addition** que chaque ligne somme bien au nombre de pas, puis répondez à trois questions dans votre carnet.

1. Combien de visites de l'état 6 obtenez-vous en 10 000 pas, et sur **cinq graines** différentes, quelle est l'amplitude de ce nombre ? Le tableau de la section 11.2 donne 5 : vous allez voir ce qu'une graine fait à un comptage de cette taille.
2. Que devient ce comptage si vous portez la longueur d'épisode de 10 à 50 pas, tout le reste étant inchangé ? Dites **pourquoi** avant de lancer l'expérience, puis comparez votre prédiction au résultat.
3. Que devient-il si vous passez de six états à dix ? C'est l'extrapolation de la section 11.2, et elle coûte un paramètre à changer.

{{< colab url="TODO" label="Échauffement : River Swim, trois comptages et cinq graines" >}}

---

## Volet A : la méthode de référence, et un échec correctement mesuré

**Objectif.** Faire tourner un réseau Q profond avec une politique \(\varepsilon\)-gloutonne sur `MountainCar-v0`, et **documenter son échec** comme un résultat.

**Étape 1.** Reprenez votre réseau Q profond du jalon 2. Le réseau de cette tâche est minuscule : deux entrées, une couche cachée de 128, trois sorties. Gardez votre calendrier de \(\varepsilon\) habituel, de \(1{,}0\) à \(0{,}02\).

**Étape 2.** Installez les **deux instruments** de la section 11.5 avant de lancer quoi que ce soit : le compteur cumulé d'atteintes du but, et la position maximale atteinte par épisode. Vérifiez que vous distinguez bien `termine` de `tronque` : sur cette tâche, `termine` signifie que le drapeau a été atteint et `tronque` signifie que les deux cents pas sont écoulés. Les confondre rend votre compteur d'atteintes du but égal au nombre d'épisodes, et vous croirez avoir résolu la tâche en trois minutes.

**Étape 3.** Lancez trois graines, et arrêtez-vous à cent mille pas d'entraînement. Tracez la courbe de récompense, qui sera plate, et la courbe de position maximale, qui ne le sera pas.

**Étape 4.** Rédigez trois phrases dans votre carnet : combien de fois le but a été atteint, ce que la position maximale a fait pendant l'entraînement, et à quel pas d'entraînement votre \(\varepsilon\) a cessé d'explorer. La troisième phrase est celle qui compte : c'est elle qui explique pourquoi l'échec est permanent et non seulement lent.

{{< colab url="TODO" label="Volet A : réseau Q profond ε-glouton sur MountainCar-v0, et ses deux instruments" >}}

> [!NOTE]
 **Ce volet est le seul de tout le cours dont le résultat attendu est un échec, et je veux que vous le rapportiez comme une mesure.** Pas comme un problème à régler, pas comme un bogue à chercher : comme une mesure. Si après cent mille pas votre compteur d'atteintes du but affiche zéro, votre volet A est **réussi**. Et si par hasard il affiche un nombre non nul, c'est également un résultat intéressant et je veux que vous l'expliquiez : regardez votre graine, votre calendrier de \(\varepsilon\), et si vous n'avez pas par mégarde ajouté une récompense quelque part.

---

## Volet B : des réseaux bruités contre un calendrier de ε

**Objectif.** Remplacer le calendrier de \(\varepsilon\) par les réseaux bruités de la semaine 6, et mesurer la différence sur la **découverte** du but.

**Étape 1.** Reprenez la classe `CoucheBruitee` de la section 6.9, **sans la réécrire**, et remplacez la dernière couche de votre réseau du volet A. Retirez entièrement le calendrier de \(\varepsilon\) : l'agent devient purement glouton sur une sortie bruitée.

**Étape 2.** Ajoutez l'appel explicite de tirage du bruit à chaque itération d'entraînement, comme le fragment de la section 11.6. Vérifiez, en imprimant deux passes avant sur la même observation, que les sorties **diffèrent** : si elles sont identiques, votre bruit n'est pas retiré et vous mesurez un réseau ordinaire.

**Étape 3.** Trois graines, et les deux mêmes instruments qu'au volet A. Comparez au volet A sur deux grandeurs : le **premier pas d'entraînement auquel le but est atteint**, et la position maximale moyenne sur les dix mille premiers pas.

**Étape 4, et c'est le réglage à explorer.** Faites varier la **fréquence de tirage du bruit** : à chaque itération, puis une fois sur dix, puis une fois sur cent. Vous mesurez ici, directement, l'idée centrale de la section 11.3 : la **cohérence** de la politique de collecte. Prédisez le sens de l'effet avant de lancer, puis commentez l'écart.

{{< colab url="TODO" label="Volet B : réseaux bruités contre calendrier de ε, et la fréquence de tirage du bruit" >}}

---

## Volet C : une prime de nouveauté, et le piège qu'elle tend

**Objectif.** Ajouter une prime de distillation de réseau aléatoire, mesurer son effet, et **vérifier dans votre propre code** la mise en garde de la section 11.4.

**Étape 1.** Écrivez l'enveloppe. Partez du fragment de la section 11.3 pour la structure, et utilisez la prime de distillation plutôt que le comptage : deux réseaux, la référence figée à trois couches et le prédicteur à une seule, la prime en **erreur quadratique** comme ce cours l'écrit. Conservez la récompense extrinsèque et la prime séparément dans `info`.

**Étape 2.** Entraînez le prédicteur. Une ligne suffit à la perte, et un piège vous attend : la prime doit être **détachée** du graphe avant d'entrer dans la récompense, sinon vous propagez un gradient de la politique à travers votre mesure de nouveauté.

**Étape 3.** Deux environnements, pas un. L'environnement d'**entraînement** porte l'enveloppe ; l'environnement d'**évaluation** ne la porte pas. Si vous évaluez sous enveloppe, vos retours de test seront systématiquement meilleurs que la réalité, et vous ne pourrez les comparer à rien.

**Étape 4.** Faites varier \(c\) sur trois valeurs séparées par un facteur dix, sur trois graines, avec intervalle. Rapportez pour chaque valeur : le temps jusqu'au premier but, le retour d'évaluation final, et la **valeur atteinte** par votre critère, pas seulement le verdict de franchissement. Le millième de point de la section 11.6 est là pour vous rappeler pourquoi.

**Étape 5.** Et une dernière mesure, qui est le volet C en une image : tracez la **perte du prédicteur** le long de l'entraînement, et marquez sur le même axe le moment de la première atteinte du but. Dites ce que vous voyez. La section 11.6 annonce une croissance de cette perte au moment où le comportement change : vérifiez si cela se produit chez vous, et dites-le franchement si ce n'est pas le cas.

{{< colab url="TODO" label="Volet C : prime de distillation de réseau aléatoire, trois valeurs de c, trois graines" >}}

> [!WARNING]
 **Quatre pièges de ce laboratoire, et chacun coûte une soirée.** Premier piège, **`termine` contre `tronque`** : sur cette tâche, la distinction est toute l'information, et la confondre invalide chacune de vos mesures. Deuxième piège, **le coefficient \(c\) appliqué deux fois**, une fois dans l'enveloppe et une fois dans la boucle ; votre prime est alors multipliée par \(c\) une fois de trop, elle peut être des dizaines de fois trop grande, et votre agent devient un touriste. Troisième piège, **l'évaluation sous enveloppe** : vos deux courbes montent ensemble, tout a l'air de fonctionner, et vous ne mesurez plus la tâche. Quatrième piège, **le réseau de référence qui apprend** : si vous oubliez `requires_grad_(False)` ou si vous passez ses paramètres à l'optimiseur, les deux réseaux convergent l'un vers l'autre, la prime tombe à zéro partout, et votre méthode redevient exactement celle du volet A, en plus lente.

---

## La solution courte, et ce qu'elle vous apprend

Comme depuis la semaine 9, je vous donne la solution courte, à employer **après** avoir écrit la vôtre et jamais avant.

```python
# Une reference que vous n'avez pas ecrite, pour situer la votre.
# A executer APRES vos trois volets.
from stable_baselines3 import DQN, PPO
import gymnasium as gym

env = gym.make("MountainCar-v0")

# 1. La methode de valeur : attendez-vous a ce qu'elle n'arrive a rien.
dqn = DQN("MlpPolicy", env, verbose=0).learn(total_timesteps=100_000)

# 2. La methode de politique, SANS exploration dirigee : elle devrait au
#    moins trouver le but, comme la section 11.6 le rapporte.
ppo = PPO("MlpPolicy", env, verbose=0).learn(total_timesteps=200_000)
```

{{< colab url="TODO" label="Solution courte : deux références en six lignes, à lancer après vos volets" >}}

> [!NOTE]
 **Les deux budgets de pas de ce fragment ne sont pas des cibles, et ils ne prédisent rien.** Je les mets pour que le fragment tourne en quelques minutes, c'est tout. Les chiffres du Tableau 11-1 portent sur un autre code, d'autres hyperparamètres et des dizaines de milliers d'épisodes ; ils vous donnent des ordres de grandeur et ils ne vous donnent pas une attente. Comme en semaine 10, la cible à atteindre est **la vôtre** : faites une exécution pilote, lisez ce qu'elle obtient, annoncez-le dans votre carnet comme votre référence, et comparez toutes vos configurations à cette référence sur les mêmes graines.

---
