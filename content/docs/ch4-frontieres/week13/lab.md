---
title: "Laboratoire"
weight: 18
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté, puisque le jalon 4 est en semaine 14.

Et il est construit sur un principe que je veux énoncer avant les consignes, parce qu'il est inhabituel dans ce cours. **Rien de ce que cette semaine décrit n'est reproductible**, et je ne vais pas faire semblant. Dix à vingt heures de calcul par tâche pour la première moitié, environ quinze heures par tâche et par graine pour la section 13.11, cinq millions de pas d'environnement : c'est hors d'atteinte d'une session gratuite, et de très loin. Les deux implémentations de référence sont par ailleurs écrites dans une version d'un cadriciel qui ne s'installe plus, et ce cours réécrit son code de toute façon.

Le laboratoire fait donc le choix opposé, et je le crois plus instructif : il **isole quatre mécanismes** et les mesure séparément, chacun en quelques minutes. Pour chacun, je vous dis **ce que la mesure établit et ce qu'elle n'établit pas**, parce que c'est la compétence que les semaines 10, 12 et celle-ci ont en commun.

> [!IMPORTANT]
 **Aucun des quatre volets n'a été exécuté par ce cours**, et vous devez le savoir avant de commencer. Les sections de la semaine établissent que chaque construction est **correcte et soutenue** par ce qu'elles décrivent ; elles n'établissent pas qu'une courbe précise sortira de votre session. Les volets sont donc écrits comme des **consignes**, jamais comme des résultats attendus, et là où je donne un ordre de grandeur, je dis d'où il vient. Si votre résultat diffère, la bonne réaction n'est pas de régler jusqu'à ce qu'il ressemble à une attente : c'est de dire ce que vous avez obtenu et d'expliquer ce que cela mesure.

**Le protocole de mesure du jalon 2 s'applique sans que je le redemande** : au moins trois graines par configuration, un intervalle sur chaque courbe, et un critère déclaré d'avance. Il mord particulièrement au volet D, où la quantité intéressante est le **moment** où une courbe se retourne, et où une graine unique ne dit rien.

---

## Volet A : les trois estimateurs, comme fonctions pures

**Objectif.** Écrire les trois estimateurs de retour imaginé de la section 13.10 et **voir** ce que leurs équations disent, sans modèle, sans environnement et sans entraînement. C'est le volet le plus court et c'est celui par lequel il faut commencer : il coûte dix minutes et il rend les trois équations définitivement claires.

**Étape 1.** Écrivez les trois fonctions de la section 13.10 : \(V_{\mathrm{R}}\), \(V_{\mathrm{N}}^{\,n}\) et \(V_\lambda\). Ce sont des fonctions pures de deux tenseurs, un vecteur de récompenses et un vecteur de valeurs, plus deux scalaires. Vérifiez d'abord trois identités, parce qu'elles attrapent la totalité des bogues possibles :

1. \(V_{\mathrm{N}}^{\,n}\) avec \(n = 1\) doit valoir la cible à un pas de la semaine 5, en chaque position.
2. \(V_\lambda\) avec \(\lambda = 0\) doit valoir \(V_{\mathrm{N}}^{\,1}\), et avec \(\lambda = 1\) doit valoir \(V_{\mathrm{N}}^{\,H}\). Si l'un des deux cas limites est faux, votre récurrence est décalée d'un indice.
3. \(V_{\mathrm{R}}\) ne doit **jamais** dépendre du tenseur de valeurs. Passez-lui des valeurs aberrantes, par exemple mille partout, et vérifiez que sa sortie ne change pas.

**Étape 2, l'expérience qui porte l'argument de la section 13.11.** Fabriquez une trajectoire synthétique de quarante pas où **toute la récompense arrive au pas trente**, et zéro partout ailleurs. Donnez à vos fonctions un critique **parfait**, c'est-à-dire des valeurs égales au vrai retour actualisé restant, que vous pouvez calculer à la main puisque vous avez construit les récompenses. Puis tracez, en fonction de l'horizon \(H\) de dix à quarante, l'estimation rendue par chacun des trois estimateurs au pas initial.

Vous devriez voir \(V_{\mathrm{R}}\) rester **exactement nul** jusqu'à \(H = 30\) puis se réveiller brutalement, pendant que les deux autres donnent une estimation correcte **dès \(H = 10\)**. C'est la figure du balayage d'horizon de la section 13.11, en version jouet et en dix lignes, et c'est la démonstration la plus économique de ce que le critique achète.

**Étape 3, et c'est la partie à écrire dans votre carnet.** Dites, en trois phrases, **ce que cette expérience établit et ce qu'elle n'établit pas**. Elle établit que \(V_{\mathrm{R}}\) est aveugle au-delà de l'horizon, et que l'amorçage sur une valeur lève cette cécité. Elle **n'établit pas** que l'agent complet de la section 13.11 apprend mieux : votre critique était parfait, et un critique parfait est précisément ce qu'on n'a pas.

{{< colab url="TODO" label="Volet A : les trois estimateurs de retour, et l'horizon balayé sur une trajectoire synthétique" >}}

---

## Volet B : la semaine 3, sur une dynamique analytique

**Objectif.** Faire tourner le planificateur de la section 13.5 sur une dynamique **exacte et analytique**, ce qui l'isole complètement du modèle appris. C'est la **ligne plafond** du tableau de la section 13.7, reproduite dans sa forme sur un système jouet, et c'est la méthode d'entropie croisée de la semaine 3 qui revient.

**Pourquoi c'est légitime, et c'est l'ancrage le plus solide des quatre volets.** La ligne plafond du tableau de la section 13.7 est exactement cela : la même méthode d'entropie croisée, avec les mêmes quatre réglages, appliquée à la vraie dynamique d'un simulateur, sans aucun modèle appris et avec zéro épisode d'entraînement. Et elle résout toutes les tâches. Vous ne reproduisez donc pas une approximation de ce résultat : vous reproduisez **la même chose, sur un système plus petit**.

**Étape 1, le système.** Prenez un système à dynamique analytique, écrit par vous en cinq lignes : un double intégrateur, c'est-à-dire une masse ponctuelle sur une ligne, d'état \((x, \dot x)\), d'action l'accélération bornée dans \([-1,1]\), et de récompense \(-x^2 - 0{,}1\,\dot x^2\) à chaque pas. Avancez-le par un pas d'Euler. Vous avez maintenant un environnement exact, réinitialisable, dérivable et gratuit.

**Étape 2, le planificateur.** Écrivez la fonction `planifier` de la section 13.5, en remplaçant les appels au modèle par votre dynamique analytique. Gardez les quatre réglages de la section 13.5 : \(H = 12\), \(I = 10\), \(J = 1000\), \(K = 100\). Jouez un épisode de deux cents pas en commande prédictive, c'est-à-dire en replanifiant à chaque pas et en ne jouant que la première action.

**Étape 3, les trois mesures qui font le volet.** Chacune isole un énoncé précis des sections 13.5 et 13.7.

- **La réinitialisation de la loi.** Comparez deux versions : celle qui remet \(\mu\) et \(\sigma\) à zéro et un à chaque pas, et celle qui repart de la loi trouvée au pas précédent. Mesurez le retour de l'épisode sur trois graines, et surtout mesurez ce qui se passe quand vous **perturbez brusquement l'état** au pas cent. C'est l'argument de l'optimum local de la section 13.5, et il devient visible exactement là.
- **Les itérations contre le tirage brut.** Comparez \(I = 10\) itérations à \(I = 1\) avec le même nombre total de candidats tirés. C'est l'ablation de la section 13.7, et elle est entièrement reproductible ici.
- **L'horizon.** Faites varier \(H\) de 3 à 30, et tracez le retour. Vous devriez voir une saturation, et sur un système aussi simple elle arrive tôt. Dites pourquoi, en une phrase, et en reliant à la section 13.11.

**Étape 4, ce que le volet n'établit pas**, et je veux la phrase dans votre carnet : rien de ceci ne dit quoi que ce soit sur la qualité d'un **modèle appris**. Votre dynamique est exacte. Vous avez mesuré le **planificateur**, et uniquement lui.

{{< colab url="TODO" label="Volet B : la méthode d'entropie croisée sur une dynamique analytique, et trois ablations" >}}

> [!TIP]
 **Savourez ce volet pour ce qu'il est.** Vous allez rouvrir le carnet de la semaine 3, y recopier une boucle de quinze lignes que vous aviez écrite quand ce cours commençait, et constater qu'elle pilote correctement un système dynamique en commande prédictive. La semaine 3 avait quitté cette méthode sur un échec, et c'était un échec réel. Dix semaines plus tard, elle est le planificateur d'une architecture de pointe. Ce n'est pas une anecdote : c'est l'argument le plus fort que je puisse vous donner en faveur du fait d'apprendre les méthodes simples **avant** les compliquées.

---

## Volet C : un gradient qui traverse deux couches de dynamique

**Objectif.** Montrer, en vingt lignes, que le gradient de l'acteur de la section 13.11 **arrive réellement** jusqu'à \(\phi\) en traversant des transitions apprises. Ce volet démontre l'existence d'un chemin de dérivation, et **rien d'autre** : il n'entraîne aucun agent.

**Étape 1, le dispositif minimal.** Fabriquez deux réseaux de transition jouets, \(T_1\) et \(T_2\), chacun prenant un état et une action et rendant un état, chacun à deux couches denses et à **poids gelés**. Fabriquez un acteur reparamétré comme celui de la section 13.9, avec la `tanh` et le bruit tiré à l'extérieur. Et fabriquez une tête de récompense, également gelée, qui rend un scalaire depuis un état.

**Étape 2, le déroulement et le gradient.** Partez d'un état initial, appliquez l'acteur, passez par \(T_1\), appliquez l'acteur de nouveau, passez par \(T_2\), lisez une récompense, et prenez la somme des deux récompenses comme objectif. Appelez `backward`, et regardez `acteur.parameters()[0].grad`.

**Étape 3, les trois comparaisons qui font tout le volet.** Elles sont la raison d'être de ce volet, et chacune tient en une ligne de code modifiée.

1. **Le cas correct.** Notez la norme du gradient de l'acteur.
2. **Remplacez `rsample` par `sample`** dans le tirage du latent, ou retirez la reparamétrisation de l'acteur en tirant l'action dans une loi au lieu de l'écrire comme fonction du bruit. Mesurez de nouveau. Le gradient doit **s'effondrer ou disparaître**, et c'est le bogue silencieux annoncé en section 13.9.
3. **Coupez le graphe après la première transition** avec un `detach`. Le gradient doit rester non nul, mais ne plus porter que l'information du premier pas. Mesurez la différence, et commentez ce que l'acteur a perdu.

**Étape 4, la comparaison qui vaut la peine.** Faites la même mesure sur un acteur de la semaine 9, c'est-à-dire un acteur reparamétré qui maximise une valeur d'action apprise **au pas courant**, sans aucune transition dans le chemin. Comparez les deux chemins de dérivation, et écrivez en deux phrases ce que la méthode de cette semaine ajoute. C'est la ligne du milieu du tableau de la section 13.11, mise à l'épreuve dans votre code.

**Ce que ce volet n'établit pas**, et c'est important : il ne montre **pas** que ce gradient entraîne un bon agent. Un chemin de dérivation peut exister et être totalement inutile, si le modèle qu'il traverse est faux. Ce volet montre que le mécanisme fonctionne mécaniquement ; la section 13.11 vous dit, elle, à quel prix en calcul il fonctionne réellement.

{{< colab url="TODO" label="Volet C : le gradient de l'acteur à travers deux couches de dynamique, et trois comparaisons" >}}

---

## Volet D : une politique qui désapprend, puis qui cesse de désapprendre

**Objectif.** Reproduire **qualitativement** la courbe de désapprentissage de la section 13.14 sur un problème minuscule, puis ajouter la pénalité conservatrice de la section 13.15 et constater ce que cela change. C'est le volet le plus important des quatre, et c'est celui qui mène au jalon 4.

**Pourquoi c'est faisable en quelques minutes, et l'ancrage est précis.** L'axe des abscisses de la courbe de la section 13.14 va de zéro à **mille pas de gradient**. Mille pas de gradient sur un réseau à deux couches, c'est quelques secondes. Et la recette hors ligne est celle de la section 13.12 : préremplir le tampon, supprimer la ligne de collecte. Vous disposez donc des deux bouts.

**Étape 1, fabriquer le jeu de données figé, et c'est la seule fois où vous appelez Gymnasium.** Prenez un environnement continu simple, par exemple un pendule. Écrivez une **politique de comportement** \(\pi_\beta\) médiocre mais pas absurde : par exemple un contrôleur proportionnel grossier, plus un bruit gaussien généreux. Collectez cinquante mille transitions avec elle, et **enregistrez-les sur disque**. Puis fermez l'environnement, et notez l'heure : à partir de maintenant et jusqu'à l'évaluation finale, **vous n'avez plus le droit d'appeler `env.step`**.

Collectez en outre trois jeux de tailles différentes, par exemple mille, dix mille et cinquante mille transitions, avec la **même** politique de comportement. Vous en aurez besoin à l'étape 3.

**Étape 2, désapprendre.** Entraînez un acteur-critique continu de la semaine 9, par la recette de la section 13.12 : tampon prérempli, aucune collecte. Pendant mille à cinq mille pas de gradient, enregistrez **trois** quantités, et c'est le choix de ces trois quantités qui fait le volet :

- le **retour réel** de la politique courante, mesuré en la déployant dans l'environnement tous les cent pas de gradient. Oui, cela appelle `env.step` : c'est une **mesure**, pas un entraînement, et la distinction est exactement celle de la section 13.12. Un praticien hors ligne ne disposerait pas de cette mesure, et c'est d'ailleurs un problème majeur du domaine ;
- la **valeur d'action moyenne estimée** sur un lot du jeu de données, en échelle logarithmique ;
- l'**erreur de Bellman**, c'est-à-dire la perte que vous êtes en train de minimiser.

Tracez les trois sur le même axe des abscisses. Et prédisez-les **avant** de les regarder, comme en semaine 12. Ce que vous devriez voir : un retour qui monte puis redescend, une valeur estimée qui monte sans arrêt, et une erreur de Bellman qui **descend sagement** pendant toute la durée de l'expérience. La troisième courbe est le piège, et c'est pour cela que je vous la fais tracer : **votre perte vous dira que tout va bien pendant que votre agent se dégrade**.

**Étape 3, l'expérience qui doit vous marquer.** Refaites exactement l'étape 2 sur les trois tailles de jeu de données de l'étape 1. Multipliez donc les données par cinquante. Puis répondez par écrit à une question : **le retournement de la courbe a-t-il disparu ?** La section 13.14 annonce que non, sur un facteur mille. Dites ce que vous observez sur un facteur cinquante, et dites quelle **autre** quantité, elle, s'est bien améliorée avec les données. Il y en a une, et la trouver est l'objet de la question.

**Étape 4, cesser de désapprendre.** Ajoutez la pénalité conservatrice de la section 13.15 à votre perte de valeur d'action, et refaites l'étape 2 pour trois valeurs de \(\alpha_{\text{cons}}\) séparées par un facteur dix. Mesurez, pour chacune : le **moment** du retournement, s'il a lieu, et le **meilleur retour** atteint. Vous devriez voir un compromis : trop peu de pénalité et le retournement revient, trop de pénalité et le meilleur retour s'écrase vers celui de la politique de comportement. C'est, mesuré sur votre machine, l'énoncé des deux limites de la section 13.15.

**Étape 5, la référence qu'il faut absolument tracer.** Mesurez le retour de la **politique de comportement elle-même**, celle que vous avez écrite à l'étape 1. C'est l'étalon de tout ce volet : une méthode hors ligne qui ne la dépasse pas n'a rien produit, et une méthode qui tombe en dessous d'elle a activement nui. Placez cette valeur en ligne horizontale sur vos trois graphiques.

{{< colab url="TODO" label="Volet D : désapprentissage sur un jeu figé, trois tailles de données, et la pénalité conservatrice" >}}

> [!WARNING]
 **Trois pièges de ce volet, et chacun fausse la conclusion.** Premier piège, **appeler l'environnement pendant l'entraînement** : si une seule transition collectée pendant la boucle entre dans votre tampon, vous ne faites plus d'apprentissage hors ligne, et le phénomène disparaîtra en partie. Séparez physiquement les deux phases, et chargez le jeu depuis un fichier. Deuxième piège, **juger sur la perte** : elle descend, elle descendra, et elle ne mesure rien de ce qui vous intéresse. Troisième piège, **une seule graine** : le retournement arrive à des moments différents selon l'initialisation, et une graine unique produira soit une courbe spectaculaire soit une courbe plate, dans les deux cas sans valeur. Trois graines minimum, avec un intervalle, comme le jalon 2 l'exige depuis la semaine 7.

---

## La solution courte de cette semaine est un clonage de comportement

Depuis la semaine 9, chaque laboratoire se termine par une solution de référence à exécuter **après** la vôtre, pour situer votre travail. Cette semaine, elle n'est pas une bibliothèque de haut niveau, et la raison vaut mieux qu'une excuse : les bibliothèques que ce cours emploie sont construites autour d'une boucle qui **collecte**, et l'objet de la seconde moitié de la semaine est précisément de l'interdire.

La référence de cette semaine est donc une méthode, et c'est la bonne : **le clonage de comportement**, sur le même jeu de données figé.

```python
# La reference la plus honnete pour un apprentissage hors ligne, et la plus
# facile a ecrire : un apprentissage supervise pur sur le jeu figé.
#
# On apprend a predire l'action du jeu de donnees a partir de son etat,
# par une simple erreur quadratique. Aucune recompense, aucune valeur,
# aucun amorçage, donc AUCUN des problemes de la section 13.14.
#
# Ce que cette reference mesure exactement :
#  1. elle reproduit pi_beta, donc son retour est celui de pi_beta, a
#     l'erreur d'approximation pres. C'est votre PLANCHER.
#  2. si votre methode de la section 13.15 ne depasse pas ce plancher,
#     elle n'a rien extrait du jeu de donnees que l'imitation ne donnait
#     deja, et c'est un diagnostic sur vos DONNEES.
#  3. la section 13.16 explique par quel mecanisme une methode fondee sur
#     la valeur peut, elle, depasser ce plancher : la recomposition.
#
# Tracez les deux retours sur le meme graphique. L'ecart entre eux est
# la seule chose que votre travail de la semaine a produite.
```

{{< colab url="TODO" label="Référence : clonage de comportement sur le même jeu de données figé" >}}

> [!NOTE]
 **Et pourquoi cette référence est meilleure qu'une bibliothèque, dans ce cas précis.** Une référence de bibliothèque vous dit si votre code est correct. Celle-ci vous dit quelque chose de plus intéressant : **si votre problème valait la peine d'être posé**. Un jeu de données sur lequel un clonage de comportement égale votre meilleure méthode hors ligne est un jeu de données qui ne contient aucune recomposition exploitable, et aucune sophistication n'y changera rien. C'est un diagnostic sur les **données** et non sur l'algorithme, et c'est exactement le réflexe que le jalon 4 va vous demander.

---
