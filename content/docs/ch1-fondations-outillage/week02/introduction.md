---
title: "Introduction"
weight: 1
---

## La ligne « décider » attend son réseau

Bonjour à toutes et à tous ! Souvenez-vous de l'agent de la semaine dernière. Sa méthode `step()` tenait en quatre gestes, observer, décider, agir, encaisser, et la ligne « décider » était un tirage au sort. Nous avons mesuré ce que cela donne : quelques dizaines de pas sur CartPole, contre 195 pour un environnement considéré comme résolu. Cette semaine, nous n'allons pas remplir cette ligne, nous allons **fabriquer l'objet qui va la remplir**.

Cet objet est un réseau de neurones, et je veux que vous le voyiez comme un instrument avant de le voir comme une théorie. Imaginez une table de mixage avec quelques millions de boutons. Vous ne savez pas à quoi sert chaque bouton, mais vous disposez d'un indicateur qui vous dit à quel point le son produit s'écarte du son voulu, et d'un mécanisme qui vous souffle, pour **chaque** bouton, dans quel sens le tourner pour que l'écart diminue un peu. Tournez tous les boutons d'un petit pas dans ce sens, recommencez quelques milliers de fois, et l'instrument finit par jouer. L'indicateur s'appelle la fonction de perte, le mécanisme s'appelle la rétropropagation, la table de mixage s'appelle le réseau, et PyTorch est l'atelier où l'on assemble les trois.

{{% comment %}}SOURCE: LAPAN ch.3 p.82{{% /comment %}}

Je dois être franche sur une chose : il n'y a **aucun apprentissage par renforcement dans cette semaine**. Pas d'agent, pas d'épisode, pas de récompense. C'est entièrement assumé. Les progrès récents de notre discipline viennent en grande partie de son mariage avec l'**apprentissage profond** (*deep learning*), et ce mariage suppose qu'on sache construire et entraîner un réseau. Nous ne pouvons pas brancher un outil que nous n'avons pas. La semaine 3 branchera celui-ci sur CartPole ; aujourd'hui, nous le construisons, nous le regardons apprendre sur des cibles fournies d'avance, et nous installons les deux ou trois gestes que vous allez répéter pendant treize semaines.

{{% comment %}}SOURCE: D2L ch.5 p.207{{% /comment %}}

Le réseau que nous allons construire n'est pas quelconque, et c'est le fil conducteur du laboratoire : il a la **forme** de celui des semaines 4 à 15. Une entrée qui est un vecteur d'état, une sortie qui donne **une valeur par action**. Vous le verrez s'entraîner proprement sur des cibles que je vous fournirai. D'où viennent les vraies cibles, et pourquoi elles ne tiennent pas tranquilles : c'est l'affaire des semaines 4 et 5, et vous aurez le droit d'être impatients.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Créer un tenseur de trois façons différentes, choisir son type d'élément et le déplacer sur un périphérique de calcul.
- Distinguer une opération en place d'une opération fonctionnelle, et dire ce que la première fait gagner et risquer.
- Démontrer en deux lignes pourquoi deux couches linéaires empilées **sans** fonction d'activation n'en valent qu'une.
- Écrire ReLU, la sigmoïde et la tangente hyperbolique avec leurs dérivées, et dire laquelle plafonne à 0,25.
- Lire les attributs `is_leaf`, `requires_grad` et `grad` d'un tenseur, et prédire lequel portera un gradient après `backward()`.
- Relier la règle de dérivation en chaîne, écrite couche par couche, à l'unique appel `backward()` qui la réalise.
- Écrire un module personnalisé en deux gestes et expliquer pourquoi on n'appelle jamais `forward()` directement.
- Écrire la boucle d'entraînement en huit lignes et justifier la remise à zéro des gradients par leur accumulation.
- Nommer les deux pathologies du gradient, expliquer la brisure de symétrie, appliquer la formule d'initialisation de Xavier.
- Distinguer erreur de généralisation et écart de généralisation, régler un arrêt précoce, dire ce que `model.eval()` change à l'abandon de neurones.
- Calculer la forme de sortie d'une couche de convolution et la taille du vecteur aplati qui en sort.
- Instrumenter un entraînement avec TensorBoard et comparer deux exécutions sur le même graphique.
- Construire un réseau de la forme de \(Q(s,a)\), une sortie par action, et l'entraîner sur des cibles fournies.

---

## Prérequis et outils

La semaine 1 pour la notation du cours et l'habitude de Colab, et une pratique courante de Python : classes, héritage, annotations de type, NumPy. **Aucune connaissance préalable de PyTorch n'est supposée** ; en revanche, cette semaine suppose que vous acceptiez de taper du code au fur et à mesure, parce qu'un tenseur se comprend sous les doigts plus vite que dans un paragraphe.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets ; un GPU accélère le laboratoire mais n'est jamais nécessaire, chaque exercice tient en quelques minutes |
| **PyTorch** | la bibliothèque de tenseurs, de différentiation automatique et de réseaux du cours |
| **TensorBoard** | la fenêtre sur un entraînement en cours ; livré avec PyTorch, aucun paquet supplémentaire |
| **Page « Notation » du cours** | la table unique des symboles, étendue cette semaine aux poids et aux pertes |
| **Page « Glossaire » du cours** | les équivalences français ⇄ anglais retenues, très nourries cette semaine |

Comme en semaine 1, installez `torch` **sans épingler de numéro de version** : tout ce que nous écrivons ici est stable depuis plusieurs années, et le `requirements.txt` du cours reste la seule référence de versions.

> [!TIP]
 **Un conseil de méthode avant de commencer.** Gardez un carnet Colab ouvert à côté de cette page et tapez les fragments à mesure que vous les lisez. Ils sont tous courts, tous indépendants, et aucun ne demande plus de deux secondes de calcul. Les neuf fragments de cette semaine sont la version exécutable de la table des symboles.
