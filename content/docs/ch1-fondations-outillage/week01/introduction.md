---
title: "Introduction"
weight: 1
---

## Une souris, un labyrinthe, et quinze semaines devant nous

Bonjour à toutes et à tous ! Vous arrivez avec SCI1060 derrière vous : récompenses et tables de valeurs vous sont familières. Cette semaine ne va pas réapprendre ce vocabulaire, elle va le rendre **précis** (avec l'exactitude dont nous aurons besoin pendant quatorze semaines), puis le brancher sur l'outil qui nous accompagnera jusqu'au bout, l'interface Gymnasium.

Une image d'abord, car tout en découle. Une souris-robot est lâchée dans un labyrinthe : de la nourriture quelque part, récompense positive ; des plaques électrifiées ailleurs, récompense négative. Et voici le détail qui fait la richesse du problème : la souris peut accepter une petite décharge maintenant si c'est le seul chemin vers une réserve abondante plus loin. Encaisser une perte immédiate pour un gain différé : voilà, en une phrase, la difficulté centrale de notre discipline. On pourrait coder le plan du labyrinthe, mais l'effort est considérable et le résultat devient inutilisable dès qu'on déplace une cloison. C'est pour cela que nous n'allons pas *programmer* un comportement : nous allons l'*apprendre*.

{{% comment %}}SOURCE: LAPAN ch.1 p.36-37{{% /comment %}}

Ce n'est pas un échauffement : les symboles fixés ici (\(S_t\), \(A_t\), \(R_{t+1}\), \(G_t\), \(\gamma\), \(\pi\)) ne changeront plus jusqu'à la semaine 15, et la distinction minuscule de la section 1.8 entre `terminated` et `truncated` fera la différence entre un agent qui apprend et un agent qui semble apprendre.

Voici la cible de la semaine. Un agent qui tire ses actions au hasard sur CartPole ne tient que **quelques dizaines de pas** ; le même environnement est considéré comme *résolu* à partir d'une récompense moyenne de **195 sur 100 épisodes consécutifs**, un ordre de grandeur plus haut. Nous ne comblerons pas cet écart cette semaine : nous allons le **mesurer**, et c'est vous qui produirez le chiffre de départ, au laboratoire.

{{% comment %}}SOURCE: LAPAN ch.2 p.74-75{{% /comment %}}

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Situer l'apprentissage par renforcement face aux deux autres paradigmes, et énoncer les trois difficultés qui lui sont propres.
- Distinguer **état** et **observation** sur un cas concret, et dire laquelle des deux l'agent reçoit.
- Construire la matrice de transition d'une chaîne de Markov à quatre états à partir de transitions observées.
- Calculer à la main la valeur d'état d'un processus de Markov avec récompense pour \(\gamma = 0\), et expliquer ce qui diverge à \(\gamma = 1\).
- Écrire une politique sous sa forme probabiliste et justifier pourquoi une politique fixée ramène un processus de décision markovien à un processus de Markov avec récompense.
- Instancier un environnement Gymnasium, lire ses deux espaces, décomposer les cinq valeurs de `step()`.
- Expliquer pourquoi `terminated` et `truncated` ne doivent jamais être confondus, et ce que coûte la confusion.
- Mesurer un agent aléatoire sur CartPole et comparer le résultat à la frontière de récompense de 195.
- Écrire une enveloppe (*wrapper*) et la chaîner sur un environnement existant.
- Choisir, et justifier, un environnement pour votre projet de session.

## Prérequis et outils

SCI1060 pour le vocabulaire de l'apprentissage par renforcement classique, et une pratique courante de Python : classes, héritage, annotations de type, NumPy. **Cette semaine ne contient aucun réseau de neurones** ; aucun GPU n'est requis et les exécutions se comptent en minutes.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets du laboratoire ; aucun GPU nécessaire |
| **Gymnasium** (`gymnasium.farama.org`) | l'interface d'environnements du cours. Sa documentation est aussi le **catalogue officiel** des environnements : c'est là que vous choisirez celui de votre projet |
| **Page « Notation » du cours** | la table unique des symboles |
| **Page « Glossaire » du cours** | les équivalences français ⇄ anglais retenues |

Installez `gymnasium` **sans épingler de numéro de version** : l'interface décrite ici est stable depuis plusieurs années.
