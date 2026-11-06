---
title: "Introduction"
weight: 1
---

## La semaine où le cours perd l'argmax

Bonjour à toutes et à tous ! Cette semaine, le cours perd une opération, et je veux que vous mesuriez tout de suite ce que cela coûte, parce que les six sections qui suivent sont six façons de vivre sans elle.

Reprenez mentalement tout ce que nous avons construit depuis la semaine 4. L'itération de valeur apprenait \(V\), puis la politique en tombait par \(\argmax_a\). Le Q-learning tabulaire apprenait une table, puis la politique en tombait par \(\argmax_a\). Le réseau Q profond a remplacé la table par un réseau, et la politique en tombait encore par \(\argmax_a\). Les cinq réparations de la semaine 6 ont amélioré la qualité du nombre sur lequel ce maximum s'exerce, et la semaine 7 en a rendu le calcul moins coûteux. Même la semaine 8, qui a changé d'objet, se mesurait encore contre une famille de méthodes dont chacune se terminait par là. L'action optimale dans un état se lit sur la fonction de valeur optimale, et elle se lit par une maximisation sur les actions :

$$
a^*(s) = \argmax_a q_*(s,a)
$$

{{% comment %}}SOURCE: SPINUP ddpg/background{{% /comment %}}

Tant que l'ensemble des actions est une liste courte, cette maximisation est gratuite. Quatre actions de manette : on calcule quatre nombres et on compare. Dix-huit actions Atari : un seul passage avant, dix-huit sorties, un maximum sur un vecteur de dix-huit, et c'était très exactement l'astuce d'architecture de la semaine 5.

Maintenant remplacez l'action par un couple à appliquer à un moteur, c'est-à-dire par un réel dans un intervalle. Il n'y a plus de liste à parcourir. Il n'y a pas dix-huit candidats, il y en a une infinité, et la maximisation cesse d'être une comparaison pour devenir un problème d'optimisation posé à l'intérieur d'un réseau profond fortement non linéaire. Ce problème-là, il faudrait le résoudre **à chaque pas de temps**, dans la boucle d'entraînement comme dans la boucle de jeu, des millions de fois. Ce n'est pas un prix élevé : c'est un prix qu'on ne paie pas.

{{% comment %}}SOURCE: SPINUP ddpg/background{{% /comment %}}

Je tiens à la formulation, parce que la nuance porte toute la semaine. La maximisation sur un espace continu n'est pas *plus difficile* qu'avant, et elle n'est pas *approchée* : elle est **indisponible**. Une méthode qui en a besoin ne ralentit pas sur un espace continu, elle ne s'écrit pas. Tout ce qui suit est donc une réponse à une question unique : que fait-on quand on ne peut plus maximiser sur les actions ?

> [!IMPORTANT]
 **La perte de l'argmax a deux conséquences, et elles structurent la semaine entière.** La première : la politique doit **produire** l'action au lieu de la déduire d'un classement, ce qui fait d'un réseau de politique non plus une commodité mais une nécessité. La seconde, plus discrète et tout aussi lourde : si nous voulons encore une valeur d'action, le critique doit **recevoir** l'action en entrée, puisqu'il ne peut plus en sortir une par action. Deux changements de câblage, et tout le reste en découle.

Voici la colonne vertébrale, en une phrase par étape, pour que vous sachiez à tout moment où vous êtes. La section 9.1 regarde ce qu'une action continue **est**, pourquoi la maximisation y meurt, et pourquoi la découper en tranches n'est pas la sortie de secours qu'on croit. La section 9.2 prend la route facile : l'A2C de la semaine 8, inchangé, avec une tête gaussienne à la place du softmax. Cela fonctionne, cela donne la mesure de référence de la semaine, et cela traîne un mensonge discret que je nommerai avant d'aller plus loin. La section 9.3 prend la route déterministe : un acteur qui rend directement l'action, un critique qui la note, et un gradient qui remonte du critique dans l'acteur. La section 9.4 porte le fait que je veux vous voir emporter : une politique déterministe n'explore **rien**, et il faut remettre l'exploration à la main. La section 9.5 mesure quelque chose de désagréable, à savoir que le critique de cette famille surestime. Et la section 9.6 donne trois correctifs qui sont **trois changements indépendants**, mesurés séparément, ce que je vais répéter plus d'une fois.

Deux franchises d'entrée, parce qu'elles sont la vraie matière de la semaine. La première : il n'y aura pas de classement à la fin. Vous verrez une méthode simple qui donne un mauvais score, une méthode plus savante qui donne un bon score après vingt heures de calcul, et une étude d'ablation qui montre qu'une bonne partie de l'écart entre les deux vient du **réglage** et non des idées. La seconde : il y a un nombre que je ne vous donnerai pas, celui de l'ampleur de la surestimation, et je vous dirai en section 9.5 pourquoi je préfère vous le faire mesurer plutôt que de l'interpoler sur une courbe.

> [!WARNING]
 **Le mot « écrêtage » désigne cette semaine trois opérations différentes, et je les écrirai donc toujours en entier.** L'**écrêtage de l'action** force une action tirée au hasard à rentrer dans les bornes de l'environnement, en section 9.2. L'**écrêtage du bruit** borne à \(\pm c\) le bruit ajouté à une action cible, en section 9.6. Et le **double Q écrêté** désigne la prise du minimum entre deux critiques, également en section 9.6. Rien ne les apparente, sinon le verbe. Vous avez déjà rencontré l'écrêtage de la récompense en semaine 5 et l'écrêtage du gradient en semaine 8 : cela fait cinq usages du même mot dans le cours, dont aucun ne s'écrit « écrêtage » tout court. Le mot seul est réservé à la semaine 10.

{{% comment %}}SOURCE: source-assets/glossaire.md{{% /comment %}}

Une dernière note de notation, et elle vous évitera une demi-heure de confusion. Cette semaine, j'écris \(\ln\) pour le logarithme naturel, là où la semaine 8 écrivait \(\log\) : c'est le même logarithme, et la forme \(\ln\) est plus lisible dans les densités gaussiennes qui arrivent en section 9.2. Et surveillez la lettre \(\mu\) : sans indice, \(\mu(s)\) reste la distribution sur politique des états de la semaine 8 ; **avec** indice, \(\mu_\theta(s)\) est le nouvel objet de la semaine, l'acteur. L'indice tranche, et la page « Notation » du cours le dit depuis le début.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Expliquer pourquoi la maximisation sur les actions est **indisponible** sur un espace continu, et non simplement coûteuse, et nommer les deux changements de câblage qui en découlent.
- Décrire l'interface d'un espace d'actions continu, dire ce que `env.step()` reçoit désormais, et lire les bornes et la forme d'un espace de type `Box`.
- Chiffrer, sur un robot à huit moteurs, le nombre d'actions produites par une discrétisation à \(k\) niveaux par dimension, et dire laquelle des deux grandeurs en jeu, la résolution ou la dimension, rend l'approche impraticable.
- Transformer l'A2C de la semaine 8 en méthode à actions continues en ne changeant **qu'une** chose, et dire précisément laquelle.
- Écrire la log-densité d'une politique gaussienne multivariée à composantes indépendantes, et dire ce que l'hypothèse d'indépendance fait perdre.
- Écrire l'entropie différentielle d'une loi normale, et expliquer le signe sous lequel elle apparaît dans une perte minimisée.
- Nommer le biais introduit lorsqu'on évalue la densité d'une loi non tronquée sur une action écrêtée, dire où il se manifeste, et proposer deux façons de s'en débarrasser.
- Expliquer en quoi l'acteur déterministe est le comportement de test d'une politique gaussienne promu au rang de comportement d'entraînement.
- Écrire le gradient de politique déterministe, identifier dans la formule le facteur qui provient du critique et celui qui provient de l'acteur, et dire quelle règle de dérivation les relie.
- Expliquer pourquoi le critique, qui n'était qu'une référence en semaine 8, **est** l'objectif en semaine 9, et nommer l'opération dont la disparition permet au gradient de traverser.
- Écrire la cible du critique dans sa forme à deux cas, et dire quel réseau fournit l'action qui y figure.
- Justifier qu'une méthode à politique déterministe est hors politique, et nommer les deux objets des semaines 5 et 6 qui reviennent de ce fait.
- Écrire la synchronisation douce d'un réseau cible et convertir entre les trois conventions numériques qui circulent pour son paramètre.
- Énoncer, sans hésiter, pourquoi une politique déterministe n'explore rien, et dire où le bruit d'exploration doit être placé.
- Écrire la forme continue et la forme discrète du processus d'Ornstein-Uhlenbeck, dire ce que la corrélation temporelle apporte en principe, et dire ce qu'elle coûte en implémentation.
- Donner trois raisons indépendantes de préférer un bruit gaussien non corrélé, et formuler la règle de méthode qu'elles illustrent.
- Expliquer pourquoi une phase de démarrage aléatoire est nécessaire avec un acteur déterministe, et pourquoi l'évaluation se fait sans bruit.
- Reproduire l'argument du biais de maximisation, et dire pourquoi une erreur d'approximation de moyenne nulle produit malgré tout une surestimation systématique.
- Expliquer où se cache la maximisation dans une mise à jour acteur-critique, et décrire la boucle de rétroaction entre un critique inexact et une politique dégradée.
- Décrire un protocole de mesure de la surestimation, et dire par quoi on remplace la valeur vraie, qui est inconnue.
- Énoncer les trois correctifs de la section 9.6 séparément, et pour chacun dire quel problème précis il traite.
- Expliquer pourquoi la prise du minimum entre deux critiques est une **sous-estimation volontaire**, et pourquoi une sous-estimation est préférable à une surestimation.
- Écrire la cible complète qui combine les trois correctifs, et distinguer ce que les équations écrivent de ce que les implémentations ajoutent.
- Lire une étude d'ablation sans la sur-interpréter : dire ce que l'ajout d'un seul correctif produit en général, nommer la tâche où le retrait d'un correctif **améliore** le résultat, et nommer la tâche où le simple réglage suffit à combler l'essentiel de l'écart.
- Expliquer pourquoi une tâche sur laquelle six méthodes obtiennent toutes le score maximal ne peut pas servir de banc d'essai à une étude d'ablation.

---

## Prérequis et outils

De la semaine 8, presque tout : l'acteur et le critique, le tronc commun, la perte à trois termes, la prime d'entropie, le partage \(\theta\) pour l'acteur et \(\mathbf{w}\) pour le critique, et la facture en échantillons des méthodes sur politique. La section 9.2 est littéralement l'A2C de la semaine 8 avec une tête différente, et la section 9.3 se comprend par contraste avec elle. De la semaine 6 : la **synchronisation douce** d'un réseau cible, le double DQN, et la **surestimation des valeurs d'action**, que nous allons retrouver du côté continu avec un mécanisme identique et des conséquences plus graves. De la semaine 5 : le **tampon de rejeu**, le **réseau cible**, le détachement du graphe de calcul, et la règle « un état terminal vaut zéro », qui reparaît cette semaine dans trois écritures différentes. De la semaine 7 : le protocole de mesure à graines multiples avec intervalle, obligatoire depuis le jalon 2, donc obligatoire ici sans que j'aie à le redemander. De la semaine 4 : l'erreur de différence temporelle, qui revient en section 9.5 sous un angle inattendu, celui de ce qu'elle **laisse** derrière elle à chaque mise à jour.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les trois volets du laboratoire ; le volet A tient en quelques minutes sur processeur central, le volet C en quelques dizaines de minutes |
| **Gymnasium** | `Pendulum-v1` pour toutes les mesures, et un environnement de robotique simulée pour la seule démonstration |
| **MuJoCo** | installé comme roue Python par `gymnasium[mujoco]`, rendu **hors écran** et vidéo écrite dans un fichier : c'est la démonstration du robot, jamais la tâche mesurée |
| **PyTorch** | deux optimiseurs distincts, `torch.distributions.Normal` ou la log-densité écrite à la main, `F.softplus`, `detach()`, et la copie pondérée des poids d'un réseau cible |
| **NumPy** | le vecteur d'action, le tirage du bruit, et l'accumulation du retour actualisé du volet B |
| **Matplotlib** | les deux courbes du volet B, estimation du critique contre retour réellement collecté, qui sont la seule réponse quantitative de la semaine |
| **TensorBoard** | la valeur moyenne prédite, les deux pertes séparément, et l'écart-type du bruit effectivement appliqué |
| **Stable-Baselines3** | la solution courte du laboratoire, et le moyen le moins coûteux de comparer deux bruits d'exploration en changeant une ligne |
| **Page « Notation » du cours** | \(\mu\) et \(\mu_\theta\) y sont séparés, et les trois conventions du paramètre de synchronisation douce y sont converties |
| **Page « Glossaire » du cours** | onze termes nouveaux, dont deux acceptions supplémentaires du mot « écrêtage » |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

---
