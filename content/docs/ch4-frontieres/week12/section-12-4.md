---
title: "12.4 Ce qu'une recherche exige d'un environnement, et pourquoi Gymnasium ne le donne pas"
weight: 5
---

## Repartir d'un état choisi, ce qu'aucune interface standard n'autorise

Voici la section la plus transposable de la semaine. Elle ne contient aucune équation et une seule idée, et cette idée vous servira chaque fois que vous voudrez planifier dans quoi que ce soit.

Relisez la boucle de la recherche. À chaque passage, nous descendons de la racine vers une feuille, puis nous **recommençons depuis la racine**. Au passage suivant, nous descendons une autre branche, c'est-à-dire que nous rejouons le jeu depuis la même position dans une autre direction. Des centaines de fois. Cela veut dire que la recherche a besoin de pouvoir dire à son modèle du monde : « place-toi dans **cette** position, celle que je te décris, et dis-moi ce qui arrive si je joue ce coup ».

Reprenez maintenant l'interface que ce cours emploie depuis la semaine 1. Vous disposez de `reset()`, qui vous place dans un état initial tiré par l'environnement, et de `step(action)`, qui avance d'un pas depuis l'état courant. Vous ne disposez de **rien** qui permette de dire dans quel état vous voulez être. Vous ne pouvez pas revenir en arrière, vous ne pouvez pas sauvegarder une position et y revenir, vous ne pouvez pas poser un état arbitraire.

> [!IMPORTANT]
 **Pouvoir prédire le résultat d'une action est une exigence beaucoup plus forte que celle que satisfont nos onze semaines d'environnements, et la différence n'est pas la prédiction : c'est la possibilité de choisir l'état de départ.** L'interface standard d'un environnement d'apprentissage par renforcement est une interface de **trajectoire** : elle vous laisse avancer, et seulement avancer. Une recherche arborescente a besoin d'une interface d'**accès aléatoire**. Chaque fois que vous voudrez planifier dans un environnement, c'est cette question qu'il faudra poser en premier, avant toute considération d'algorithme : puis-je replacer ce monde dans un état de mon choix ? Si la réponse est non, aucune recherche n'est possible, quelle que soit la qualité de votre réseau.

{{% comment %}}SOURCE: LAPAN ch.20 p.609{{% /comment %}}

La conséquence pratique est qu'on écrit le modèle du jeu **à la main**, comme un module de fonctions pures, sans état interne et sans objet d'environnement. C'est un travail modeste pour un jeu de plateau, et c'est le prix d'entrée de la méthode.

---

## La mémoire est la ressource rare, d'où une position en soixante-trois bits

Deuxième conséquence, moins évidente, et qui explique une décision de conception qui paraît sinon maniaque.

Pendant une recherche, nous gardons en mémoire tous les nœuds créés, chacun avec ses trois listes de statistiques. Plus nous en gardons, meilleure est l'approximation de la distribution de coups que la recherche produira. La mémoire est donc **la ressource qui limite la qualité du résultat**, ce qui est une situation inhabituelle dans ce cours, où la ressource rare a toujours été le temps de calcul ou l'échantillon.

{{% comment %}}SOURCE: LAPAN ch.20 p.609-610{{% /comment %}}

D'où l'encodage. Une position complète de Puissance 4, c'est-à-dire une grille de six lignes sur sept colonnes avec l'identité du propriétaire de chaque jeton, tient dans **soixante-trois bits**, donc dans un seul mot machine de soixante-quatre bits. Un entier par position : c'est une clé de dictionnaire parfaite, comparable, copiable, et qui ne coûte rien à mémoriser. À côté de cette forme compacte, le module garde une forme **décodée** et lisible par un humain, sept listes correspondant aux sept colonnes, utilisée pour toute la logique de jeu et pour l'affichage.

{{% comment %}}SOURCE: LAPAN ch.20 p.609-610{{% /comment %}}

---

## Cinq fonctions, quatre constantes, et un match nul qui ne se signale pas

Le modèle de jeu entier tient en **cinq fonctions**, et je vous les donne avec les noms que le laboratoire emploie, parce que vous allez les écrire :

| Fonction | Ce qu'elle fait |
| --- | --- |
| `encoder(colonnes)` | de la forme lisible vers l'entier compact |
| `decoder(position)` | de l'entier compact vers la forme lisible |
| `coups_possibles(position)` | la liste des colonnes non pleines, c'est-à-dire les coups légaux |
| `jouer(position, colonne, joueur)` | la nouvelle position, et si le coup est gagnant |
| `afficher(position)` | la grille en texte, pour jouer contre votre propre réseau |

Et quatre constantes, qui sont tout le paramétrage du jeu : six lignes, sept colonnes, quatre jetons alignés pour gagner, et le nombre de bits réservés à la hauteur de chaque colonne.

{{% comment %}}SOURCE: LAPAN ch.20 p.609-610{{% /comment %}}

> [!WARNING]
 **Le match nul ne vous sera pas signalé, et c'est le piège d'implémentation de cette section.** La fonction qui joue un coup vous dit si ce coup est **gagnant**. Elle ne vous dit pas si la partie est finie par épuisement, parce que la grille pleine n'est pas un événement du coup joué : c'est un état du plateau. Un match nul se détecte donc **après** le coup, en appelant la fonction des coups possibles et en constatant que la liste est vide. Si vous l'oubliez, vos parties nulles seront comptées comme des parties en cours, votre boucle d'auto-jeu tournera indéfiniment sur une grille pleine, et vous chercherez le bogue dans la recherche alors qu'il est dans le jeu.

{{% comment %}}SOURCE: LAPAN ch.20 p.610{{% /comment %}}

---

## Le réseau à deux têtes, et ce qu'il doit à la semaine 8

Le réseau de cette méthode vous est déjà familier, et c'est le moment de le dire : c'est l'architecture de l'acteur-critique de la semaine 8. Un tronc commun, puis **deux têtes** :

- une **tête de politique** (*policy head*), qui rend une distribution sur les actions, donc ici un logit par colonne ;
- une **tête de valeur** (*value head*), qui rend un seul nombre, l'estimation du résultat de la partie **du point de vue du joueur qui doit jouer**.

{{% comment %}}SOURCE: LAPAN ch.20 p.606-607{{% /comment %}}

Deux précisions, et chacune évite un contresens.

**La valeur n'est pas actualisée.** Il n'y a pas de \(\gamma\) dans cette méthode, et ce n'est pas un oubli. Le go, les échecs et Puissance 4 sont **déterministes** : le résultat d'une partie, une fois la suite de coups fixée, est certain, et il n'y a aucune raison de préférer une victoire proche à une victoire lointaine. Dans un jeu **stochastique**, le backgammon par exemple, où un dé intervient entre votre coup et ses conséquences, il faudrait réintroduire une actualisation, parce qu'une victoire annoncée à dix coups y est beaucoup moins sûre qu'une victoire annoncée au coup suivant.

{{% comment %}}SOURCE: LAPAN ch.20 p.607{{% /comment %}}

**L'entrée est faite de deux plans, et ce détail rend le réseau indépendant du joueur.** On ne donne pas au réseau une grille avec des 1 pour les jetons rouges et des \(-1\) pour les jaunes. On lui donne **deux** grilles de six sur sept : la première porte les jetons **du joueur courant**, la seconde ceux de son adversaire. Le réseau ne sait donc jamais s'il regarde la position du rouge ou celle du jaune, et il n'a pas à le savoir : il voit toujours « mes jetons, ses jetons ». Un seul réseau sert donc les deux camps, et tout le travail de symétrie est fait par l'encodage de l'entrée plutôt que par le réseau. Gardez ce procédé en tête : la section 12.10 vous en montrera une version qui permet à une seule politique de servir **deux groupes d'agents opposés** dans un monde multi-agent.

{{% comment %}}SOURCE: LAPAN ch.20 p.616 (image){{% /comment %}}

Pour le reste, l'architecture est sans surprise : un tronc de six couches de convolution résiduelles, la tête de politique rendant sept logits, la tête de valeur rendant un flottant. Rien dans ce réseau n'est nouveau après la semaine 8, et c'est une bonne nouvelle : la difficulté de la méthode est dans la recherche et dans la production des données, pas dans le réseau.

{{% comment %}}SOURCE: LAPAN ch.20 p.616 (image){{% /comment %}}

---
