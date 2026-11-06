---
title: "Introduction"
weight: 1
---

## La table devient une fonction, et trois sécurités tombent d'un coup

Bonjour à toutes et à tous ! La semaine 4 s'est terminée sur une dette, et je l'avais annoncée comme telle. Nos tables ont une ligne par état : seize lignes pour FrozenLake, quarante-huit pour la falaise, et **aucune** pour CartPole. Quatre nombres réels en guise d'observation, et la table n'existe plus. Cette semaine paie la dette, et la réponse n'est pas « une table plus grande ». La table devient une **fonction**, cette fonction est un réseau de neurones, et nous obtenons à la fin un agent qui apprend à jouer à un jeu vidéo en regardant les pixels de l'écran.

Je veux être honnête tout de suite sur le prix de ce remplacement, parce que c'est ce qui distingue cette semaine d'un simple tutoriel. En passant de la table à la fonction, trois choses qui étaient sûres en semaine 4 cessent de l'être **en même temps**. Les valeurs des états n'étaient pas couplées : elles le deviennent. La mise à jour écrivait dans une case : elle descendra un gradient qui, en réalité, n'est pas tout à fait un gradient. Et l'ensemble peut, de façon démontrable, **diverger**. Nous verrons la divergence se produire sur trois lignes d'arithmétique, puis nous verrons les quatre réparations d'ingénierie qui font tenir l'édifice en pratique.

{{% comment %}}SOURCE: LAPAN ch.6 p.164{{% /comment %}}

L'ordre de la semaine est donc l'ordre d'un argument, et non une liste de sujets. La table échoue, et elle échoue pour une raison qui se compte (5.1). La table devient une fonction, avec un objectif à minimiser (5.2 et 5.3). Le gradient de cet objectif est délibérément tronqué (5.4). Le même geste se refait pour les valeurs d'action (5.5). Cette combinaison peut diverger, et on peut le prouver (5.6). Trois réparations la rendent utilisable (5.7). Nous l'implémentons (5.8). Et nous finissons par ce qu'elle coûte et par les cas où elle ne converge pas du tout (5.9).

La méthode que nous construisons porte un nom : le **réseau Q profond** (*deep Q-network*, DQN). Elle a été publiée en deux temps, et la différence entre les deux vaut d'être retenue : une première version sur sept jeux Atari, **sans réseau cible**, puis une seconde sur quarante-neuf jeux, avec le réseau cible et des résultats comparables à ceux d'un joueur humain. Le réseau cible de la section 5.7 est donc exactement ce qui a transformé une démonstration en méthode.

{{% comment %}}SOURCE: LAPAN ch.6 p.175-176{{% /comment %}}

Avant la première équation, un point de notation, et il est obligatoire. Deux écritures vont désigner la même chose, et si vous ne les identifiez pas maintenant, les sections 5.6 et 5.8 vous paraîtront parler de deux objets différents.

> [!IMPORTANT]
 **Je dois insister : \(\mathbf{w}\) et \(\theta\) sont les mêmes poids, écrits dans deux dialectes.** Le formalisme des valeurs approchées écrit \(\hat v(s,\mathbf{w})\) et \(\hat q(s,a,\mathbf{w})\), avec un **vecteur de poids** (*weight vector*) \(\mathbf{w} \in \R^d\). Le vocabulaire des réseaux Q profonds écrit \(Q_\theta(s,a)\) pour le réseau et \(Q_{\theta^-}(s',a')\) pour sa copie figée. Règle de ce cours, et elle ne changera plus : les sections qui raisonnent sur le formalisme écrivent \(\mathbf{w}\), les sections qui écrivent du PyTorch écrivent \(\theta\) et \(\theta^-\), et **ils désignent le même tableau de nombres**. C'est le même geste que la semaine 4 a fait pour l'échelle \(v_\pi\) / \(V\) / \(\hat v\) : une seule chose, plusieurs notations selon ce dont on parle.

| Notation | Ce qu'elle désigne | Où elle vit |
| --- | --- | --- |
| \(v_\pi(s)\), \(q_\pi(s,a)\) | les valeurs **vraies** sous \(\pi\) | la cible que l'on vise, jamais calculée |
| \(V(s)\), \(Q(s,a)\) | les **estimations tabulaires**, une case par état | la semaine 4 |
| \(\hat v(s,\mathbf{w})\), \(\hat q(s,a,\mathbf{w})\) | les **valeurs approchées**, \(d\) poids pour tous les états | les sections 5.2 à 5.6 |
| \(Q_\theta(s,a)\), \(Q_{\theta^-}(s',a')\) | le réseau et sa copie figée, les mêmes poids | les sections 5.7 à 5.9 |

> [!NOTE]
 **Notez bien ce point d'organisation.** La semaine 5 ne porte **aucun jalon** : le prochain est en semaine 7, et le laboratoire de cette semaine est formatif, comme celui de la semaine 4. En revanche il demande, pour la première fois du cours, un **processeur graphique** : prévoyez une session Colab avec accélérateur. Le volet principal tient en moins de quinze minutes sur un T4, et le volet le plus spectaculaire, celui qui joue à Pong, ne s'entraîne pas du tout : il **évalue** des poids fournis, parce qu'entraîner ce même agent demanderait une à trois heures.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Chiffrer, sur Atari et sur CartPole, pourquoi une table est hors de question, et dire laquelle des deux ressources, la mémoire ou les échantillons, manque la première.
- Écrire la forme approchée \(\hat v(s,\mathbf{w})\) et dire ce que signifie \(d \ll \lvert\mathcal{S}\rvert\) pour la valeur d'un état jamais visité.
- Relire une mise à jour d'apprentissage par renforcement comme un exemple supervisé \(s \mapsto u\), et nommer les deux exigences qu'un problème supervisé ordinaire ne connaît pas.
- Écrire l'objectif \(\overline{VE}(\mathbf{w})\) et expliquer ce que la pondération \(\mu(s)\) impose, que le cas tabulaire n'imposait pas.
- Dériver la mise à jour de descente de gradient stochastique sur une valeur, et dire précisément quel passage cesse d'être valide lorsque la cible est amorcée.
- Définir une **méthode semi-gradient** et désigner, dans un fragment de PyTorch, la ligne qui la réalise.
- Écrire la mise à jour semi-gradient pour \(\hat q(s,a,\mathbf{w})\) et son cas terminal, et dire à quelle ligne de code ce cas terminal correspond.
- Faire tourner à la main l'exemple à deux états et montrer que le poids part à l'infini pour **tout** pas d'apprentissage positif.
- Énoncer les trois ingrédients de la triade fatale, et les pointer un par un dans le code d'un DQN.
- Dire pourquoi le contre-exemple de Baird est accablant alors même que la fonction de valeur vraie y est exactement représentable.
- Expliquer ce que répare le tampon de rejeu, et quel ingrédient de la triade il **introduit** du même mouvement.
- Expliquer ce que répare le réseau cible, et pourquoi la période de synchronisation est un hyperparamètre et non un détail.
- Expliquer pourquoi quatre trames sont empilées, et pourquoi cette réparation ne concerne pas la triade mais la propriété de Markov.
- Écrire la perte d'un DQN sur un lot, en désignant le rôle de `gather`, du masque terminal et du détachement du graphe.
- Justifier le choix d'**une sortie par action** plutôt qu'un réseau prenant \((s,a)\) en entrée.
- Donner l'ordre de grandeur du coût d'entraînement sur Pong, en trames et en heures, et dire ce qu'il faut faire lorsqu'un entraînement ne montre aucune dynamique positive.
- Implémenter un DQN complet sur CartPole, le faire converger, puis mesurer ce que l'on perd en retirant le réseau cible, puis le tampon.

---

## Prérequis et outils

De la semaine 1 : le processus de décision markovien, la propriété de Markov, l'interface `reset()` / `step()`, et la distinction entre `terminated` et `truncated`. De la semaine 2 : PyTorch, les réseaux, les couches de convolution et le pas de la convolution, l'autodifférenciation, le graphe de calcul et le **détachement du graphe**, la fonction de perte quadratique, l'optimiseur. De la semaine 3 : les axes sur politique et hors politique. De la semaine 4 : TD(0), l'erreur TD, Q-learning, la méthode \(\varepsilon\)-gloutonne, l'amorçage, et la règle « un état terminal vaut zéro », que nous allons retrouver trois fois cette semaine sous trois écritures différentes.

Cette semaine ne redémontre ni la rétropropagation ni la convolution : elle les emploie. Si le graphe de calcul de la semaine 2 vous paraît lointain, c'est la section 5.4 qui vous le rappellera de la façon la plus utile possible, puisque tout le sens de la méthode y tient à une seule ligne de PyTorch.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets, **avec accélérateur graphique** cette semaine |
| **Gymnasium** | `CartPole-v1`, `LunarLander-v3`, et les environnements Atari pour le volet d'évaluation |
| **PyTorch** | le réseau, l'optimiseur, et les deux façons de bloquer un gradient |
| **NumPy** | le tampon de rejeu et la mise en lot des transitions |
| **Matplotlib** | vos courbes de retour, et les trois courbes de l'ablation |
| **Page « Notation » du cours** | décisive cette semaine pour \(\mathbf{w}\), \(\theta\), \(\theta^-\) et \(\mu(s)\) |
| **Page « Glossaire » du cours** | dix-sept termes nouveaux y entrent cette semaine |

> [!TIP]
 **Un conseil de méthode, et il est différent de celui de la semaine 4.** Cette semaine, les équations sont peu nombreuses et c'est le **code** qui porte les pièges. Prenez l'habitude, devant chaque fragment, de poser une seule question : *quelles quantités sont différenciées, et lesquelles sont tenues pour des constantes ?* Dans un agent tabulaire, cette question n'existait pas. Ici, elle est la différence entre un algorithme qui apprend et un algorithme qui court après sa propre queue. Si vous ne gardez qu'une habitude de cette semaine, gardez celle-là.

---
