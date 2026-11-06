---
title: "Introduction"
weight: 1
---

## Douze semaines d'agents qui devaient agir pour apprendre

Bonjour à toutes et à tous ! Je veux ouvrir cette semaine par un inventaire, parce qu'il va rendre visible une dépendance que nous n'avons jamais mise en question.

Depuis la semaine 4, chacune de nos méthodes a appris de la même façon : l'agent agit, l'environnement répond, et quelque chose se met à jour. La semaine 5 a remplacé la table par un réseau, la semaine 8 a paramétré la politique, la semaine 9 est passée aux actions continues, la semaine 10 a borné le pas de mise à jour, la semaine 11 a payé la nouveauté, la semaine 12 a donné un modèle à l'agent et l'a autorisé à chercher dedans avant de jouer. Douze semaines, et une constante absolue : **pour apprendre, il a fallu agir**. Même la semaine 12, qui planifiait, jouait encore, collectait encore, et avait besoin de l'environnement à chaque pas.

Cette semaine retire l'interaction. Deux fois, et dans deux sens différents.

**Premier retrait.** L'agent apprend un **modèle du monde** (*world model*) à partir de ses observations brutes, puis fait son travail d'anticipation **à l'intérieur** de ce modèle. L'environnement réel n'est plus consulté pour évaluer une idée : il est consulté pour fournir des données au modèle, quelques centaines de fois au lieu de quelques millions. C'est la première moitié de la semaine, et elle se termine sur une bascule : une fois le modèle en place, faut-il encore planifier à chaque pas, ou peut-on apprendre une politique **dans** les **trajectoires imaginées** (*imagined trajectory*) qu'il produit ?

**Second retrait, et il est plus radical.** On supprime la collecte. Pas « on en fait moins » : on la supprime. Un **jeu de données figé** (*static dataset*), produit par quelqu'un d'autre, auquel on n'ajoutera jamais une transition, et une politique à en extraire sans pouvoir essayer quoi que ce soit. C'est l'**apprentissage par renforcement hors ligne** (*offline reinforcement learning*), et c'est là que la semaine rencontre le problème qui définit le sous-domaine tout entier : la politique que vous apprenez veut faire des choses que les données ne contiennent pas, et **rien dans le jeu de données ne peut vous dire ce qui arriverait**.

---

## Deux mots que ce cours vous demande de ne plus confondre

Avant toute chose, une mise au point de vocabulaire. Elle prend trois paragraphes et elle vous évitera de lire la seconde moitié de la semaine de travers.

Depuis la semaine 3, ce cours distingue une méthode **sur politique** (*on-policy*) d'une méthode **hors politique** (*off-policy*). Une méthode hors politique apprend sur une politique à partir de données produites par une autre : c'est le Q-learning de la semaine 4, c'est le tampon de rejeu de la semaine 5, ce sont les critiques de valeur d'action des semaines 9 et 11. Rien de tout cela ne cesse pour autant de collecter. L'agent continue de jouer, continue d'ajouter des transitions à son tampon, et continue de corriger ses estimations avec ce qu'il vient d'observer.

« Hors ligne » ne veut pas dire cela. Une méthode hors ligne **ne collecte plus jamais**. Le jeu de données existe avant l'agent, il est complet le jour où l'entraînement commence, et il est exactement le même le jour où l'entraînement finit.

> [!IMPORTANT]
 **Hors politique et hors ligne ne sont pas synonymes, et la confusion est la première cause de contresens sur cette semaine.** Hors politique est un **qualificatif d'algorithme** : il dit qu'une méthode sait exploiter des transitions dont l'action vient d'une autre politique que la politique courante. Hors ligne est un **énoncé de problème** : il dit qu'aucune interaction n'aura lieu pendant l'entraînement. Toute méthode hors ligne doit être hors politique, puisque les données viennent forcément de quelqu'un d'autre. L'inverse est faux, et c'est là que tout se joue : la quasi-totalité des méthodes hors politique que vous connaissez continuent de collecter, et la seconde moitié de cette semaine est consacrée à ce qui leur arrive quand on leur retire ce droit. La réponse courte est : elles cassent, et elles cassent d'une manière que vous n'avez encore jamais vue dans ce cours.

{{% comment %}}SOURCE: OFFLINE p.7-8{{% /comment %}}

Le français demande une précaution supplémentaire, et la page « Glossaire » du cours l'a déjà tranchée. **« En ligne » et « hors ligne » ne traduisent jamais « sur politique » et « hors politique »** : ces deux expressions sont réservées, dans ce cours, au sens de cette semaine, c'est-à-dire à la présence ou à l'absence d'interaction. Si vous lisez ailleurs « apprentissage hors ligne » pour désigner un apprentissage hors politique avec collecte, c'est un glissement, et il vous coûtera une lecture.

---

## Un symbole qui ne change pas de lettre, et qui change de statut

Voici maintenant le piège que je préfère désamorcer dès l'ouverture, parce qu'il est de mon fait et non du vôtre.

Le jeu de données figé de la seconde moitié de cette semaine s'écrit \(\mathcal{D}\). C'est **exactement** le symbole que la semaine 5 a donné au tampon de rejeu, et je ne vais pas le renommer. Non par paresse : parce que **l'identité du symbole est la leçon de la semaine**.

Regardez les deux objets côte à côte. Même symbole, même contenu (des quadruplets état, action, récompense, état suivant), même usage dans la boucle d'entraînement (on y tire un lot, on calcule une cible, on descend un gradient). Et un statut exactement opposé : le tampon de la semaine 5 est **alimenté en continu** par l'agent qui apprend dessus, tandis que le jeu de la semaine 13 est **figé avant que l'agent existe**. Toute la difficulté de la seconde moitié de la semaine vient de cette seule différence, et de rien d'autre. Si vous retenez une image de cette semaine, retenez celle-là : c'est le même code, c'est le même symbole, et la boucle d'alimentation a été coupée.

{{% comment %}}SOURCE: notation.md §3 ter{{% /comment %}}

---

## Ce que vous allez lire

Voici la colonne vertébrale de la semaine, une phrase par section.

La section 13.1 pose le vocabulaire sur trois régimes de collecte, et explique pourquoi l'interaction est la ressource qu'il faut économiser. La section 13.2 dit pourquoi on n'apprend pas une dynamique directement depuis des pixels, en quatre difficultés nommées, et pourquoi on en veut une quand même, en trois arguments. La section 13.3 construit l'objet central de la première moitié : un **état latent** (*latent state*) où l'on met la dynamique, avec un chemin déterministe pour la mémoire et un chemin stochastique pour l'incertitude, parce qu'aucun des deux ne suffit seul. La section 13.4 donne l'objectif qui entraîne tout cela, une **borne variationnelle** (*variational bound*) en deux termes. La section 13.5 est un moment de ce cours que j'attends depuis dix semaines : le planificateur de cette architecture est la **méthode d'entropie croisée de la semaine 3**. La section 13.6 referme l'agent avec sa boucle de collecte. La section 13.7 rapporte ce qui est démontré, et ce que cela coûte en heures de calcul.

La section 13.8 est la charnière : deux objections au fait de replanifier à chaque pas, et une question nouvelle posée au même modèle. La section 13.9 met un acteur et un critique **dans l'imagination** du modèle, ce qui rouvre les semaines 8 à 10 à l'intérieur d'un monde appris. La section 13.10 donne trois façons d'estimer un retour imaginé, dont l'une est littéralement le retour \(\lambda\) de la semaine 7. La section 13.11 montre où va le gradient de l'acteur, et c'est un endroit où aucun gradient de ce cours n'est encore allé.

La section 13.12 retire l'environnement et pose le problème hors ligne. La section 13.13 explique pourquoi ce n'est pas de l'apprentissage supervisé, avec un argument quantitatif. La section 13.14 est le centre de la semaine : le **décalage de distribution** (*distributional shift*), et une erreur qui **grandit** au lieu de se diluer. La section 13.15 donne les deux familles de réponses. La section 13.16 nomme le pont que cette semaine ne franchit pas, et la route vers la semaine 14.

---

## Les symboles de la semaine, et six collisions à trancher

Cette semaine est la plus coûteuse du cours en notation, et je préfère payer la facture tout de suite plutôt que de me battre contre mes propres lettres pendant quarante pages. Les arbitrages ci-dessous sont inscrits dans la page « Notation » du cours ; je les reprends ici parce qu'ils mordent dès la section 13.3.

**Première collision, et c'est la plus importante : l'état latent n'est pas un état.** Toute la première moitié de la semaine manipule un vecteur appris, produit par un encodeur, qui joue le rôle d'un état dans un modèle. Ce n'est pas \(S_t\), l'état de l'environnement, et ce n'est pas \(O_t\), l'observation. Je l'écris \(Z_t\), et \(S_t\) comme \(O_t\) gardent leur sens des semaines 1 et 7. Cette seule décision lève la pire ambiguïté possible : sans elle, la même lettre désignerait l'état du monde et la représentation que le modèle s'en fait.

**Deuxième collision : \(q\) n'est pas une loi de probabilité dans ce cours.** Depuis la semaine 4, \(q\) est une valeur d'action. L'encodeur de cette semaine s'écrit donc \(e_\theta\), et jamais \(q\). De même, l'acteur de la section 13.9 s'écrit \(\pi_\phi\), parce que c'est une politique, et le critique \(\hat v_\psi\), parce que c'est la fonction de valeur \(\hat v(s,\mathbf{w})\) de la semaine 7 avec un autre nom de paramètres.

**Troisième collision : trois jeux de paramètres au lieu de deux.** Ce cours écrit \(\theta\) pour les paramètres d'une politique et \(\mathbf{w}\) pour ceux d'une valeur. La première moitié de la semaine en a besoin de trois : \(\theta\) pour le **modèle du monde**, \(\phi\) pour l'**acteur**, \(\psi\) pour le **critique**. Je le déclare une fois, en tableau, à l'ouverture de la section 13.9, et je m'y tiens. Dans la seconde moitié, où il n'y a plus de modèle du tout, la valeur d'action reprend les paramètres \(\mathbf{w}\) du cours et s'écrit \(Q_{\mathbf{w}}\).

**Quatrième collision : il faut deux distributions d'états à la fois.** La page « Notation » n'en avait qu'une, \(\mu(s)\), la distribution sur politique des états. La seconde moitié de la semaine en exige deux simultanément : celle que visite la politique apprise, \(d^\pi(s)\), et celle que couvre le jeu de données, que j'écris \(d^{\mathcal{D}}(s)\). Ce second symbole est une création de ce cours, et il est choisi pour une raison précise : il rend visible le mot **couverture**, qui est exactement ce que la figure centrale de la semaine dessine.

**Cinquième collision, et c'est la plus sournoise : \(R\) n'est pas un retour cette semaine.** Dans la littérature de la première moitié, \(R\) désigne la **répétition d'action**, un entier entre 2 et 8, et il désigne aussi le retour d'un candidat dans un planificateur. Je **n'écrirai jamais un \(R\) nu** cette semaine : un retour s'écrit \(G\), comme depuis la semaine 1, et la répétition d'action s'écrit en mots, ou `action_repeat` dans le code.

**Sixième collision : le temps imaginé.** Les trajectoires imaginées de la section 13.9 ont besoin d'un indice de temps, et \(\tau\) porte déjà deux sens dans ce cours (le coefficient de mise à jour douce de la semaine 9, la température sur les comptages de visites de la semaine 12). Le temps **à l'intérieur de l'imagination** s'écrit donc \(k\).

Et un détail qui n'est pas une collision mais une continuité à surveiller : la semaine 12 a écrit \(f_\theta\) pour un réseau de **prédiction**. Cette semaine, \(f_\theta\) est la part **récurrente** de la transition du modèle, c'est-à-dire la cellule qui fait avancer la mémoire. Les deux objets n'ont rien à voir, ils sont séparés d'une semaine, et je le signale avant la première équation qui s'en sert.

---

## L'inventaire complet des symboles nouveaux

Voici tout ce que la semaine introduit, dans l'ordre d'apparition. Aucun de ces symboles ne vous est demandé de mémoire : chacun est redéfini devant vous à sa première apparition dans une section.

| Symbole | Ce qu'il désigne | Première section |
| --- | --- | --- |
| \(d^\pi(s)\) | distribution des états visités par la politique apprise | 13.1 |
| \(d^{\mathcal{D}}(s)\) | distribution des états **couverts par le jeu de données** ; création de ce cours | 13.1 |
| \(\pi_\beta(a \mid s)\) | **politique de comportement**, celle qui a produit les données ; c'est le \(b(a\mid s)\) de la semaine 4 | 13.1 |
| \(O_t\) | observation, ici une image de 64 sur 64 en trois canaux | 13.3 |
| \(Z_t\) | **état latent** appris, part stochastique | 13.3 |
| \(h_t\) | part déterministe et récurrente de l'état du modèle | 13.3 |
| \(f_\theta\) | la cellule récurrente qui avance \(h_t\) ; **pas le réseau de prédiction de la semaine 12** | 13.3 |
| \(p_\theta\) | une loi **apprise** du modèle du monde ; l'indice \(\theta\) est ce qui la distingue de la vraie dynamique \(p\) | 13.3 |
| \(e_\theta(z \mid h, o)\) | **encodeur**, la loi qui produit le latent à partir de l'observation | 13.3 |
| \(\beta_{\mathrm{KL}}\) | poids du terme de divergence dans la borne variationnelle | 13.4 |
| \(H\) | horizon : de **planification** en 13.5, d'**imagination** en 13.9, de tâche en 13.13 | 13.5 |
| \(I, J, K\) | itérations, candidats et élites du planificateur | 13.5 |
| \(\mu_{t:t+H}, \sigma_{t:t+H}\) | moyenne et écart-type de la loi sur les **suites d'actions** | 13.5 |
| \(G^{(j)}\) | retour imaginé du candidat \(j\) | 13.5 |
| \(S, C, B, L\) | épisodes d'amorçage, intervalle de collecte, taille de lot, longueur de tronçon | 13.6 |
| \(k\) | indice de temps **dans l'imagination** | 13.9 |
| \(r_k\) | récompense **prédite par le modèle** au pas imaginé \(k\) ; ce n'est pas une récompense reçue | 13.9 |
| \(\pi_\phi(a \mid z)\) | acteur, une politique de l'état latent | 13.9 |
| \(\hat v_\psi(z)\) | critique, la valeur d'état du latent | 13.9 |
| \(V_{\mathrm{R}}, V_{\mathrm{N}}^{n}, V_\lambda\) | les trois estimateurs de retour imaginé | 13.10 |
| \(Q_{\mathbf{w}}(s,a)\) | valeur d'action apprise de la moitié hors ligne | 13.12 |
| \(\mathcal{B}\) | lot tiré dans \(\mathcal{D}\) | 13.12 |
| \(\epsilon_{\text{gen}}\) | erreur de généralisation d'un apprentissage supervisé | 13.13 |
| \(\epsilon_{\text{c}}\) | budget d'une contrainte de divergence | 13.14 |
| \(\varepsilon_{\text{s}}\) | seuil de support, sous lequel une action est jugée absente des données | 13.15 |
| \(\alpha_{\text{cons}}\) | poids d'une contrainte ou d'une pénalité conservatrice | 13.15 |
| \(\nu(a \mid s)\) | loi d'actions **adverse** de la pénalité conservatrice | 13.15 |
| \(\mathcal{H}(\cdot)\) | entropie d'une loi | 13.15 |
| \(\epsilon_m, \epsilon_\pi\) | erreur de modèle et écart de politique, dans la borne de clôture | 13.16 |

> [!NOTE]
 **Trois de ces lignes sont des créations de ce cours, et vous avez le droit de le savoir.** \(d^{\mathcal{D}}(s)\) ne se rencontre pas ailleurs : l'usage est d'écrire la distribution des données avec le nom de la politique qui les a produites, ce qui suppose qu'on la connaisse, alors que le cas intéressant est précisément celui où on ne la connaît pas. \(\nu(a\mid s)\) est un renommage, parce que \(\mu\) porte déjà trois sens dans ce cours et qu'une loi d'actions adverse en serait un quatrième. Et l'indice \(k\) du temps imaginé est un troisième choix du cours, pour la raison donnée ci-dessus.

{{% comment %}}SOURCE: notation.md §3 ter{{% /comment %}}

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Distinguer **trois régimes de collecte** (sur politique, hors politique avec tampon vivant, hors ligne avec jeu figé) et dire, pour chacun, qui a produit les données et si l'on en produit encore.
- Expliquer pourquoi « hors politique » et « hors ligne » ne sont pas synonymes, et donner un exemple de méthode hors politique qui n'est pas hors ligne.
- Dire ce que le tampon de rejeu de la semaine 5 et le jeu de données de cette semaine ont de rigoureusement identique, et quelle est la seule différence entre eux.
- Nommer les **quatre difficultés** d'un apprentissage de dynamique à partir d'observations brutes, et les **trois arguments** qui justifient de s'y risquer malgré tout.
- Écrire le processus de décision markovien **partiellement observable** en quatre lois, et dire laquelle d'entre elles l'agent cherche.
- Expliquer pourquoi la dynamique est apprise dans un espace latent plutôt que dans l'espace des observations.
- Dire ce qu'un chemin **purement stochastique** oublie, ce qu'un chemin **purement déterministe** ne peut pas représenter, et ce que le planificateur fait de cette seconde faiblesse.
- Énoncer la réserve honnête sur l'argument précédent : ce qu'un modèle stochastique pourrait faire en principe, et ce que l'optimisation ne trouve pas.
- Citer le résultat d'ablation qui ferme l'argument, et dire laquelle des deux parts est la plus critique.
- Écrire les trois composantes apprises du modèle et son encodeur, et dire **laquelle ne sert jamais à planifier**.
- Dire pourquoi cette architecture n'a ni réseau de politique ni réseau de valeur, et ce qui tient le rôle de la politique.
- Écrire la borne variationnelle, nommer ses **deux termes**, et dire ce que chacun pénalise.
- Expliquer pourquoi une vraisemblance gaussienne de variance unité se code comme une erreur quadratique moyenne.
- Dire ce que les « nats libres » font au terme de divergence, et à quel problème ils répondent.
- Décrire la contrainte structurelle de l'encodeur, et dire ce qui se passe si une information sur l'observation contourne son échantillonnage.
- Écrire le planificateur par **méthode d'entropie croisée** dans l'espace latent, et dire ce qu'il réinitialise à chaque nouvelle observation, et pourquoi.
- Expliquer pourquoi ce planificateur ne génère **jamais d'image**, et ce que cela permet.
- Dire pourquoi une seule trajectoire par candidat suffit, et où va le budget de calcul économisé.
- Décrire la boucle de collecte complète avec ses quatre réglages, et dire ce que la **répétition d'action** achète.
- Rapporter le gain d'efficacité en échantillons, lire la **ligne plafond** d'un tableau de résultats, et dire ce qu'elle démontre exactement.
- Nommer le coût en heures de calcul, et expliquer pourquoi cette semaine ne reproduit rien.
- Énoncer les **deux objections** au fait de replanifier à chaque pas, et dire laquelle porte sur le coût et laquelle sur le gradient.
- Expliquer en une phrase pourquoi le processus de décision à l'intérieur du modèle est **complètement observable**, et quelles semaines cela rouvre.
- Écrire l'acteur et le critique du modèle, et dire comment ils sont entraînés l'un contre l'autre.
- Écrire la forme reparamétrée d'une action, et dire ce que la reparamétrisation autorise.
- Écrire les **trois estimateurs de retour imaginé**, dire lequel est aveugle au-delà de l'horizon, et lequel est le retour \(\lambda\) de la semaine 7.
- Dire quelle ablation établit que l'estimation de valeur est ce qui achète l'horizon, et pourquoi ce n'est pas une courbe d'efficacité en échantillons.
- Décrire la **chaîne de dépendances** que le gradient de l'acteur remonte, et dire en quoi elle diffère de celle d'un acteur-critique des semaines 9 et 10.
- Dire ce qui, pendant cette phase, est **gelé**, et pourquoi c'est ce qui rend le calcul traitable.
- Définir l'apprentissage par renforcement **hors ligne** en quatre conditions, et dire laquelle est la plus facile à oublier.
- Expliquer la recette qui transforme n'importe quelle méthode hors politique en méthode hors ligne, et dire pourquoi elle ne suffit pas.
- Expliquer pourquoi un problème hors ligne n'est pas un problème d'apprentissage supervisé, avec le mot **contrefactuel**.
- Comparer les deux bornes du clonage de comportement, dire laquelle est quadratique, et reconstruire le raisonnement qui produit le carré.
- Nommer et distinguer les **deux décalages de distribution**, dire lequel agit au moment du test et lequel agit pendant l'entraînement, et lequel des deux est fatal.
- Expliquer, en trois étapes, pourquoi l'erreur **grandit** au lieu de se diluer, et pourquoi l'optimiseur est une recherche des erreurs de son propre estimateur.
- Décrire la courbe de **désapprentissage** et dire pourquoi augmenter la taille du jeu de données n'y change rien.
- Faire le lien avec la triade fatale de la semaine 5, et dire en quoi cette semaine pousse sa troisième jambe à la limite.
- Décrire les **deux familles de réponses**, et dire ce que chacune suppose de connu sur la politique de comportement.
- Écrire la paire contrainte, dire pourquoi la variante à pénalité place son terme **dans la cible**, et ce que le facteur \(\gamma\) y fait.
- Expliquer pourquoi une contrainte de divergence de Kullback-Leibler est le mauvais outil, avec le contre-exemple de la politique de comportement uniforme.
- Écrire la divergence de **support**, et dire ce qu'elle autorise que la précédente interdisait.
- Écrire la pénalité conservatrice qui fonctionne, dire ce que l'erreur de Bellman **ancre**, et lire la forme fermée en log-somme-exponentielle.
- Dire en quoi la pénalité à deux termes n'est plus une borne inférieure ponctuelle, et ce qu'elle reste malgré tout.
- Nommer les deux limites de la pessimisation, dont l'accumulation en \(H^2\).
- Décrire le mécanisme d'**exploitation du modèle** dans le cas hors ligne, et dire de quel objet de la section 13.14 il est la copie exacte.
- Dire pourquoi des déroulements **courts**, branchés sur des états présents dans les données, limitent l'accumulation.
- Expliquer, avec l'idée de recomposition de trajectoires, comment une politique peut être meilleure que les données qui l'ont entraînée.
- Nommer le lien entre la moitié hors ligne de cette semaine et le jalon 4.

---

## Prérequis et outils

De la **semaine 3**, deux choses, et la seconde est la surprise de la semaine : la taxonomie sur politique / hors politique, et la **méthode d'entropie croisée** (*cross-entropy method*), que vous avez écrite en semaine 3 sur un problème jouet et qui revient en section 13.5 comme planificateur d'un agent moderne. Relisez-la avant d'arriver là, vous apprécierez le moment. De la **semaine 4**, la politique de comportement \(b(a\mid s)\) et le mot « hors politique ». De la **semaine 5**, le tampon de rejeu, la cible à un pas, et la **triade fatale**, dont la section 13.14 est l'illustration la plus brutale de ce cours. De la **semaine 7**, le retour \(\lambda\) et la valeur approchée \(\hat v(s,\mathbf{w})\) : la section 13.10 réemploie le premier littéralement. Des **semaines 8 à 10**, l'acteur-critique et la **reparamétrisation** d'une politique gaussienne tronquée par une tangente hyperbolique, qui est exactement la forme employée en section 13.9. De la **semaine 12**, enfin, la distinction entre un modèle **donné** et un modèle **appris**, et l'accumulation de l'erreur le long d'un déroulement : la semaine 12 planifiait avec un modèle appris, cette semaine apprend **à l'intérieur** du modèle, ce qui n'est pas la même exigence.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les quatre volets du laboratoire ; aucun ne demande de processeur graphique, et le plus long tient en une vingtaine de minutes |
| **PyTorch** | la cellule récurrente du modèle, les trois estimateurs de retour, l'acteur reparamétré, et la valeur d'action de la moitié hors ligne |
| **NumPy** | la loi sur les suites d'actions du planificateur, et la constitution du jeu de données figé |
| **Gymnasium** | uniquement pour **produire** le jeu de données figé du volet D, puis pour évaluer la politique obtenue ; pendant l'apprentissage hors ligne, il n'est pas appelé une seule fois, et c'est tout le sujet |
| **Matplotlib** | les trois courbes du volet A, et surtout la courbe de désapprentissage du volet D |
| **Python standard** | `dataclasses` pour les hyperparamètres, et `torch.no_grad` pour la cible gelée |
| **Page « Notation » du cours** | la section ajoutée cette semaine, avec les six collisions tranchées ci-dessus |
| **Page « Glossaire » du cours** | une vingtaine de termes nouveaux, dont « état latent », à ne pas confondre avec l'« état caché » de la semaine 12 |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 13{{% /comment %}}

> [!WARNING]
 **Rien de ce que cette semaine décrit n'est reproductible, et je le dis avant de commencer plutôt qu'en note de bas de page.** Les résultats de la première moitié coûtent de dix à vingt heures de calcul sur un processeur graphique de centre de données **par tâche**, et ceux de la section 13.11 environ quinze heures **par tâche et par graine**, sur cinq millions de pas d'environnement. Une session Colab gratuite ne s'en approche pas, et aucun laboratoire de ce cours ne vous demandera d'essayer. Le laboratoire de la semaine fait donc autre chose, et il le fait honnêtement : il isole **quatre mécanismes** que l'on peut écrire, exécuter et mesurer en quelques minutes chacun, et il vous dit chaque fois ce que la mesure établit et ce qu'elle n'établit pas.

> [!NOTE]
 **Cette semaine ne porte aucun jalon, et son laboratoire est formatif.** Le jalon 4 vous attend en semaine 14. La moitié hors ligne de cette semaine y mène directement, et je nomme le lien dès maintenant pour que vous l'ayez en tête en lisant : **les données que votre projet a déjà collectées constituent un jeu de données figé**, et évaluer une politique sur elles, sans retourner dans l'environnement, est exactement un problème hors ligne. La section 13.16 y revient en terminant.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---
