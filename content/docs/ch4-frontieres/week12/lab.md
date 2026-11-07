---
title: "Laboratoire"
weight: 13
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté, puisque le jalon 4 est en semaine 14. Il est construit autour d'**un seul objet**, Puissance 4, que vous allez tenir de bout en bout : le modèle du jeu, la recherche, le réseau, l'auto-jeu, et à la fin une partie contre votre propre réseau, ce qui est la seule évaluation que vous apprécierez vraiment.

**Je vous annonce tout de suite ce que le laboratoire ne fait pas, parce que je préfère une omission déclarée à une omission silencieuse.** Il ne vous fait **pas** entraîner d'agents dans un monde multi-agent, et il ne vous fait pas non plus reproduire la méthode à modèle appris de la section 12.6. Les deux raisons sont pratiques et je les mets sur la table :

- le monde multi-agent de la section 12.10 demande un paquet à cœur compilé, à version épinglée, dont ce cours **n'a pas vérifié** l'installation dans une session Colab gratuite, et les entraînements dont la section 12.10 rapporte les résultats coûtent une à deux heures de processeur graphique, soit plus qu'une session gratuite ;
- la méthode à modèle appris demande quinze heures pour produire un résultat qui, section 12.8, **ne converge pas** : ce n'est pas un bon usage de votre semaine.

Le volet D remplace donc l'entraînement multi-agent par un exercice de **lecture et d'analyse**, qui vaut d'être fait pour lui-même : vous y lirez une interface, une conception d'observation et un résultat, et vous y exercerez précisément le jugement que la section 12.11 demande.

**Le protocole de mesure du jalon 2 s'applique sans que je le redemande** : au moins trois graines par configuration, un intervalle sur chaque courbe, et un critère déclaré d'avance. Avec une précision propre à cette semaine, qui vient de la section 12.5 :

> [!IMPORTANT]
 **Votre critère de progrès cette semaine n'est pas une perte, c'est un tournoi.** Déclarez-le avant de lancer quoi que ce soit : « je sauvegarde un point de contrôle à chaque promotion, et à la fin je fais jouer chaque point de contrôle contre tous les autres, cent parties chacun ». Si vous déclarez à la place « j'arrête quand la perte descend sous telle valeur », vous n'arrêterez jamais, et vous passerez votre soirée à régler un pas d'apprentissage qui n'est pas en cause. La section 12.5 explique pourquoi. C'est la première fois que ce cours vous demande d'ignorer une courbe de perte, et c'est volontaire.

---

## Échauffement : le modèle du jeu, et un horizon que vous dérivez vous-même

Une heure, et il n'est pas décoratif : tout le reste repose dessus, et la section 12.4 a expliqué pourquoi ce module ne peut pas être un environnement ordinaire.

Écrivez les **cinq fonctions** de la section 12.4 : encodage, décodage, coups possibles, jouer un coup, afficher. Travaillez avec les quatre constantes, six lignes, sept colonnes, quatre jetons alignés, et le nombre de bits de hauteur de colonne. Puis trois vérifications, dans cet ordre :

1. **Aller-retour.** Pour mille positions tirées au hasard en jouant des coups légaux, vérifiez que décoder puis réencoder redonne le même entier. Un encodage qui perd de l'information produit des collisions de nœuds dans l'arbre, et vous ne le verrez jamais autrement.
2. **Le match nul.** Remplissez une grille entièrement sans victoire, et vérifiez que votre détection de fin de partie fonctionne. Rappel de la section 12.4 : la fonction qui joue un coup ne vous signalera **pas** le match nul, c'est à vous de constater qu'il n'y a plus de coups possibles.
3. **L'horizon de coups, et vous le dérivez.** Ne recopiez aucune expression. Calculez vous-même le nombre **minimal** de coups joués pour qu'une partie puisse être gagnée, à partir du nombre de jetons à aligner, puis le nombre **maximal** de coups d'une partie, à partir de la taille du plateau. Écrivez les deux nombres dans votre carnet avant de choisir votre horizon, et justifiez votre choix en une phrase. La section 12.7 explique ce qui arrive quand on se trompe du mauvais côté.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Échauffement : le modèle de jeu en cinq fonctions, et trois vérifications" >}}

---

## Volet A : la recherche, testée sans réseau entraîné

**Objectif.** Écrire la recherche de la section 12.3 et la **tester en isolation**, avant qu'un réseau ne vienne brouiller le diagnostic.

**Étape 1.** Écrivez les quatre phases : sélection par l'utilité, expansion d'une feuille, évaluation, remontée avec inversion de signe. Utilisez un réseau **non entraîné** comme fonction d'évaluation : ses sorties sont du bruit, et c'est très bien pour ce volet.

**Étape 2, trois tests qui valent mieux qu'une heure d'entraînement.** Chacun attrape un bogue précis.

- **Le test du total.** Après \(n\) recherches depuis une position, la somme des comptages de visites à la racine doit valoir exactement \(n\). Si elle vaut moins, vous perdez des passages ; si elle vaut plus, vous comptez deux fois.
- **Le test de la victoire immédiate.** Placez une position où vous gagnez en un coup. Avec assez de recherches pour que chaque colonne soit visitée au moins une fois, le comptage maximal doit être celui du coup gagnant. Si ce n'est pas le cas, votre détection de fin de partie ou votre remontée est fautive.
- **Le test du signe, et c'est celui qui attrape l'erreur de la section 12.3.** Placez une position où c'est l'**adversaire** qui gagne au coup suivant, quoi que vous jouiez. La valeur remontée à la racine doit être **négative**. Si elle est positive, vous avez oublié une inversion de signe, et votre agent jouera avec enthousiasme vers sa propre défaite.

**Étape 3, et c'est l'expérience la plus instructive du laboratoire.** Implémentez **volontairement** la mauvaise utilité, celle sans racine carrée et sans constante, et comparez-la à la bonne sur une seule mesure : le **nombre de colonnes distinctes** visitées au moins dix fois à la racine, après deux cents recherches. Puis commentez l'écart. C'est l'avertissement de la section 12.3, reproduit dans votre code, et c'est la façon de ne plus jamais l'oublier.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Volet A : la recherche, trois tests d'isolation, et l'utilité amputée mesurée" >}}

---

## Volet B : l'auto-jeu, et une perte qui ne descendra pas

**Objectif.** Faire tourner la boucle complète pendant une heure et obtenir un adversaire jouable.

**Étape 1.** Écrivez le réseau à deux têtes de la section 12.4 : entrée à **deux plans** de six sur sept, un tronc de convolutions résiduelles, une tête de politique à sept logits, une tête de valeur à un flottant. Vérifiez l'invariance au joueur en passant la même position vue des deux camps : les sorties doivent être cohérentes avec l'échange des plans, et non identiques.

**Étape 2.** Écrivez la boucle d'auto-jeu : le meilleur réseau joue les deux camps, \(\tau = 1\) pour les premiers coups puis \(\tau = 0\), les triplets partent dans le tampon, et le résultat est retourné en remontant l'historique. Les réglages économiques de la section 12.5 : **dix** recherches par coup, huit feuilles par passage de réseau.

**Étape 3.** Écrivez la porte : cent parties contre le meilleur réseau, promotion au-dessus de soixante pour cent, point de contrôle enregistré à chaque promotion. Comptez les promotions, c'est votre instrument le plus utile.

**Étape 4.** Lancez une heure, et visez environ 2 500 parties d'auto-jeu. Pendant que cela tourne, tracez trois choses et prédisez-les **avant** de les regarder : la perte totale, le taux de victoire de l'apprenti, et le nombre cumulé de promotions. Notez vos prédictions dans votre carnet, puis comparez. Deux des trois courbes vous diront la vérité et une vous mentira.

**Étape 5, le tournoi.** Faites jouer vos points de contrôle les uns contre les autres, cent parties par couple, et dressez le tableau. C'est votre seule mesure de progrès valide. Dites en une phrase si l'ordre du tournoi suit l'ordre chronologique, et commentez les exceptions.

**Étape 6, la récompense.** Jouez contre votre réseau, à la main, dans le terminal. Attendez-vous au niveau annoncé en section 12.5 : en dessous de celui d'un enfant, une stratégie rudimentaire, une erreur grossière un coup sur deux. Notez trois erreurs qu'il commet, et dites pour chacune si vous pensez qu'elle vient du réseau ou du nombre de recherches.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Volet B : auto-jeu complet, une heure, 2 500 parties, et le tournoi des points de contrôle" >}}

> [!WARNING]
 **Quatre pièges de ce volet, et chacun coûte une soirée.** Premier piège, **le signe du résultat dans les triplets** : si vous ne retournez pas le résultat en remontant l'historique, la moitié de vos cibles de valeur ont le signe inverse, et votre tête de valeur apprend la moyenne des deux, c'est-à-dire zéro partout. Deuxième piège, **le masquage des coups illégaux après l'argmax** au lieu d'avant : vos indices se décalent et votre agent joue un coup pour un autre. Troisième piège, **la promotion sans copie des poids** : si vous promouvez l'apprenti en gardant une référence au même objet, apprenti et meilleur réseau deviennent le même réseau, l'auto-jeu continue de tourner, et la porte s'ouvre désormais au hasard. Quatrième piège, **le match nul non détecté**, déjà signalé à l'échauffement : votre boucle d'auto-jeu tournera indéfiniment sur une grille pleine.

---

## Volet C : trois constantes, et ce que chacune commande

**Objectif.** Cesser de traiter un hyperparamètre comme un nombre magique.

**Étape 1, la constante d'exploration.** Faites varier \(c_{\text{puct}}\) sur trois valeurs séparées par un facteur dix, par exemple \(0{,}1\), \(1{,}0\) et \(10\). Mesurez, pour chacune, le nombre de colonnes distinctes explorées à la racine et le niveau du réseau obtenu après vingt minutes, sur trois graines. Dites laquelle est la meilleure **pour cette mesure-là**, et rappelez-vous la leçon de la semaine 11 sur les classements locaux.

**Étape 2, la concentration de Dirichlet.** Comparez \(\alpha_{\mathrm{Dir}} = 0{,}03\) et \(\alpha_{\mathrm{Dir}} = 0{,}3\) sur sept colonnes, et faites-le d'abord **sans aucun entraînement** : tirez mille vecteurs de Dirichlet pour chacune des deux valeurs, et pour chacun calculez le poids maximal du vecteur. Donnez la moyenne de ces maximums. Vous allez voir, en trois lignes de code, pourquoi la section 12.3 dit qu'un tirage à concentration trop faible est presque unitaire, et pourquoi cela ne fait pas du tout ce que le bruit de racine est censé faire.

**Étape 3, votre horizon.** Reprenez le nombre que vous avez dérivé à l'échauffement, et vérifiez expérimentalement qu'aucune de vos parties d'auto-jeu n'est coupée avant la fin. Comptez les parties tronquées par l'horizon : si ce compteur n'est pas nul, votre horizon est trop court et une partie de vos cibles de valeur ne correspond à aucun résultat réel.

**Étape 4.** Une phrase de conclusion par constante, dans votre carnet, de la forme « cette constante commande *telle grandeur du problème*, et on la règle en regardant *telle mesure* ». C'est l'objectif réel du volet.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Volet C : trois constantes, et la mesure qui commande chacune" >}}

---

## Volet D : lecture et analyse d'un monde multi-agent, sans entraînement

**Objectif.** Exercer, sur un cas réel, le jugement des sections 12.9 à 12.11. Ce volet se fait **sans aucun calcul lourd** : il demande de la lecture, deux divisions et de l'écriture.

**Question 1, l'interface.** Reprenez la boucle d'épisode de la section 12.10 et dites, en trois phrases, ce qui empêche d'y brancher une enveloppe d'environnement ordinaire. Puis réécrivez la boucle de la semaine 5 que vous avez déjà, et marquez d'un commentaire **chaque ligne** qu'il faudrait changer.

**Question 2, la population volatile.** Un agent meurt au pas 37 d'un épisode qui en compte 300. Dites précisément ce qui arrive à ses entrées dans les cinq dictionnaires au pas 37, puis au pas 38, et ce que votre tampon de rejeu doit ranger dans chacun des deux cas. Puis dites ce qui casse si vous itérez sur la liste des agents sans la figer.

**Question 3, l'observation.** Une politique partagée sert deux groupes opposés. Dites quel choix d'encodage de l'observation rend cela possible, et où ce cours a déjà utilisé le même procédé, dans une section précédente de cette semaine. Puis dites ce que cette politique partagée **interdit** aux agents d'un même groupe.

**Question 4, l'arithmétique.** À partir des quatre nombres de la section 12.10, santé initiale, coût par pas, santé rendue par une proie, et récompense par pas, refaites le calcul des cent cinquante-cinq proies chassées, et dites quelle hypothèse sur la récompense le rend possible. Puis refaites-le pour un score de test de 60 au lieu de 82, et dites si la conclusion change de nature.

**Question 5, et c'est la question qui compte.** Un rapport affirme que des agents ont « appris à collaborer » parce qu'ils chassent par deux. Rédigez, en un paragraphe, la réponse de la section 12.11 : ce qui est certain, ce qui est observé, d'où vient chaque affirmation, et la question unique qu'il faut poser pour trancher.

**Question 6.** Deux courbes sans tendance, l'une venant d'un entraînement par auto-jeu et l'autre d'un entraînement de deux groupes simultanés. Dites en quoi les causes diffèrent, et ce qui, dans chaque cas, serait ou ne serait pas une réponse technique utile.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Volet D : lecture et analyse multi-agent, six questions, aucun entraînement" >}}

---

## Il n'y a pas de solution courte cette semaine, et c'est intéressant

Depuis la semaine 9, chaque laboratoire se termine par une solution courte avec une bibliothèque de haut niveau, à exécuter **après** la vôtre, pour situer votre travail. Cette semaine, je ne peux pas vous en donner, et la raison vaut mieux qu'une excuse.

Les bibliothèques de haut niveau que ce cours emploie sont construites autour d'une interface d'environnement à un seul agent, avec un `reset()` et un `step()`. Or **rien de cette semaine n'est un environnement de ce genre** : la première moitié a besoin d'un modèle de jeu interrogeable depuis un état arbitraire, ce qui est exactement ce que cette interface interdit, et la seconde moitié rend cinq dictionnaires au lieu de cinq valeurs. C'est la section 12.4, vécue depuis l'outillage.

Votre mesure de référence sera donc faite par vous, et en voici les deux termes, qui ne coûtent rien à écrire :

```python
# Deux adversaires de reference, a battre avant de se rejouir de quoi que ce soit.
#
# 1. Le joueur aleatoire : il joue une colonne legale au hasard.
#    Votre reseau entraine doit le battre de maniere ecrasante. S'il ne le
#    fait pas, ne reglez rien : relisez vos trois tests du volet A.
#
# 2. La recherche seule, avec votre reseau NON entraine.
#    Dix recherches par coup, un reseau aux poids initiaux. C'est exactement
#    l'etat de votre systeme a l'episode zero, et c'est le bon point de
#    comparaison pour une heure d'entrainement : il mesure ce que
#    l'entrainement a ajoute, et non ce que la recherche faisait deja.
```

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-12.ipynb" label="Références : le joueur aléatoire et la recherche sans entraînement" >}}

> [!NOTE]
 **Le second adversaire est le plus intéressant des deux, et c'est une mesure que l'on oublie presque toujours.** Une recherche arborescente, même avec un réseau complètement aléatoire, **joue déjà quelque chose** : elle détecte les victoires immédiates et les défaites immédiates, parce que celles-ci sont des états terminaux, évalués par le résultat réel de la partie et non par le réseau. Une partie de la force de votre système final vient donc de la recherche et non de l'entraînement. Si vous ne mesurez pas cela, vous attribuerez à votre réseau un mérite qui revient à votre arbre.

---
