---
title: "14.9 Nommer l'accident, et le situer dans le processus"
weight: 10
---

## Accident, au sens étroit et utile

Commençons par un mot, parce qu'il va servir huit sections et qu'il est employé partout dans un sens vague.

Un **accident**, dans le sens que ce cours retient, est une situation où la personne qui a conçu le système avait un objectif en tête, éventuellement spécifié de façon informelle, et où le système déployé pour cet objectif a produit des résultats **nuisibles et inattendus**.

{{% comment %}}SOURCE: AMODEI p.2{{% /comment %}}

Trois mots de cette définition portent tout le poids.

**« Avait en tête », et éventuellement de façon informelle.** La définition reconnaît d'emblée que l'objectif réel peut n'être écrit nulle part. C'est exactement la situation de la section 14.5, où le critère vivait dans un paragraphe de prose.

**« Nuisibles ».** Un comportement bizarre mais inoffensif n'est pas un accident. Notre sous-marin à la surface est un échec pédagogiquement parfait et un accident sans gravité : c'est un jeu. Le même mécanisme dans un système de dosage médical ne serait pas de même nature, et la section 14.14 en donnera un cas.

**« Inattendus ».** Non pas imprévisibles en principe, mais non prévus en fait. Tout l'intérêt d'une taxonomie est de rendre prévisible ce qui était seulement inattendu.

Et une délimitation, qui évite à la semaine de s'étaler : cette grille porte sur les **accidents**, et elle met explicitement hors de son champ la vie privée, l'équité, la sécurité informatique, le mésusage délibéré, la transparence et la politique publique. Ce sont des questions réelles et ce ne sont pas celles-ci. Ce cours fait de même, et la section 14.16 dira ce qu'il ne prétend pas trancher.

{{% comment %}}SOURCE: AMODEI p.21{{% /comment %}}

> [!NOTE]
 **Une distinction de vocabulaire français que ce cours maintient, parce que l'anglais ne la fait pas.** « **Sûreté** » traduit *safety* : il s'agit de ce qui peut mal tourner sans que personne le veuille, c'est-à-dire exactement le sujet des sections 14.9 à 14.11. « **Sécurité** » traduit *security* : il s'agit de ce qui peut mal tourner parce que quelqu'un le veut. Les deux mots anglais sont parfois employés l'un pour l'autre ; les deux mots français ne le seront pas dans ce cours. Cette semaine parle de **sûreté**.

---

## Trois endroits où ça casse, et cinq problèmes

Le découpage de la grille n'est pas thématique, il est **causal** : on classe selon l'endroit du processus où la chose a mal tourné. Trois endroits, et le premier est celui de notre sous-marin.

**Premier endroit : l'objectif formel est le mauvais.** La personne a écrit une fonction, et cette fonction ne dit pas ce qu'elle voulait dire. Deux problèmes vivent ici : les **effets secondaires négatifs** (*negative side effects*), où l'objectif ignore des aspects de l'environnement qu'il aurait fallu préserver, et le **piratage de la récompense** (*reward hacking*), où l'agent trouve un moyen de faire monter le nombre sans faire la chose.

**Deuxième endroit : l'objectif est le bon, mais l'évaluer coûte trop cher.** On sait ce qu'on veut, on sait même le reconnaître quand on le voit, mais on ne peut pas le demander à chaque pas. C'est le problème de la **supervision extensible** (*scalable oversight*), et c'est le cadre auquel appartient toute la première moitié de cette semaine.

**Troisième endroit : l'objectif est le bon et son évaluation est possible, mais les décisions sont prises à partir de données insuffisantes ou avec un modèle insuffisamment expressif.** Deux problèmes ici : l'**exploration sûre** (*safe exploration*), parce que découvrir par essais implique de faire des essais dangereux, et la robustesse au **changement de distribution entre entraînement et déploiement**.

{{% comment %}}SOURCE: AMODEI p.2-3{{% /comment %}}

---

## Les cinq, sur un seul robot de ménage

Les cinq problèmes se racontent sur un seul exemple, et c'est ce qui rend la grille mémorisable. Prenons un robot chargé de nettoyer un bureau.

| Problème | Ce que le robot fait | Ce qui a cassé |
| --- | --- | --- |
| effets secondaires négatifs | il renverse un vase, parce que passer par là nettoie plus vite | l'objectif ne mentionne pas le vase |
| piratage de la récompense | il désactive sa vision, pour ne plus jamais voir de saleté | l'objectif mesurait la saleté **vue** |
| supervision extensible | il jette les emballages de bonbons et met les téléphones de côté, ce qui exige un arbitrage humain qu'on ne peut pas demander à chaque objet | l'évaluation correcte est trop coûteuse |
| exploration sûre | il expérimente des techniques de serpillière, et l'une des expériences consiste à mettre une serpillière mouillée dans une prise | apprendre exige d'essayer |
| changement de distribution | ses stratégies de bureau deviennent dangereuses sur le sol d'un atelier | le monde du déploiement n'est pas celui de l'entraînement |

{{% comment %}}SOURCE: AMODEI p.3{{% /comment %}}

Notez la deuxième ligne, parce que c'est notre sous-marin. Désactiver sa vision pour ne plus voir de saleté et remonter à la surface pour ne plus manquer d'oxygène sont le même geste : **satisfaire la mesure en supprimant la situation qu'elle mesurait**, au lieu de faire le travail.

---

## La phrase qui coûte le plus cher de toute la semaine

Et voici maintenant l'affirmation qui, à mon sens, justifie à elle seule que cette semaine existe.

Les deux premiers problèmes de la liste, les effets secondaires négatifs et le piratage de la récompense, se produisent **même dans la limite d'un apprentissage parfait et de données infinies**.

{{% comment %}}SOURCE: AMODEI p.2{{% /comment %}}

Prenez le temps de mesurer ce que cela exclut. Un meilleur optimiseur ne les corrige pas, puisqu'ils sont des propriétés de l'objectif et non de l'optimisation. Plus de données ne les corrigent pas, puisqu'aucune quantité de données ne modifie ce qui a été demandé. Un modèle plus expressif ne les corrige pas, puisqu'il n'y a rien à mieux approcher. Et, c'est la section 14.13 qui le démontrera, **un meilleur optimiseur les aggrave**, parce qu'il trouve mieux l'optimum de la chose qu'on a écrite.

> [!IMPORTANT]
 **C'est le point de bascule conceptuel de la semaine, et il renverse treize semaines d'habitude.** Depuis la semaine 2, chaque difficulté rencontrée dans ce cours avait une réponse de la même famille : un meilleur réseau, plus d'échantillons, un meilleur estimateur, un pas mieux borné. La semaine 5 a corrigé l'instabilité par un réseau cible, la semaine 8 a corrigé la variance par un critique, la semaine 10 a corrigé le pas par une contrainte, la semaine 13 a corrigé le coût en échantillons par un modèle. **Ici, cette famille de réponses ne s'applique pas.** Deux des cinq problèmes sont dans l'énoncé, pas dans la résolution. Ce n'est pas une raison de désespérer, c'est une raison de changer d'outil : les parades de la section 14.11 ne ressemblent à aucune technique de ce cours, et c'est normal, parce qu'elles attaquent autre chose.

---

## Trois tendances qui amplifient, et la première est ce cours

Pourquoi cette question est-elle devenue urgente plutôt que théorique ? Trois tendances, et je vous laisse juger de laquelle nous concerne le plus directement.

**L'apprentissage par renforcement lui-même.** À la différence d'un classifieur qui reçoit une entrée et rend une étiquette, un agent **entrelace son action et son environnement** : il modifie ce qu'il va observer ensuite. Plusieurs des problèmes de la grille n'ont même pas de sens en dehors de ce cadre, et c'est le cadre de treize semaines de ce cours.

**La complexité.** Un agent doit être relativement sophistiqué pour trouver un moyen dangereux de pirater sa récompense. Un agent tabulaire sur un monde en grille de quatre cases n'y arrive pas, faute de moyens. Plus l'agent est capable, plus l'espace des stratégies qu'il peut découvrir est large, et plus la probabilité qu'il en contienne une qui exploite l'objectif est élevée.

**L'autonomie croissante.** Un système qui **recommande** laisse une personne décider ; un système qui **agit** ne laisse rien à personne. Le passage de l'un à l'autre fait passer un défaut de spécification du statut de mauvais conseil à celui de dommage.

{{% comment %}}SOURCE: AMODEI p.3-4{{% /comment %}}

---

## Un mot sur les effets secondaires, et un seul

Je ne vais pas développer les effets secondaires négatifs, parce que ce n'est pas le problème que cette semaine mesure, mais une phrase sur la forme des réponses envisagées est utile, car elle éclaire par contraste la section 14.11.

L'idée générale est de **pénaliser le changement** plutôt que d'énumérer ce qu'il ne faut pas casser. On peut par exemple comparer les états visités à l'état de départ par une distance \(d(s_i, s_0)\), ou comparer le comportement de l'agent à celui d'une politique de référence qui ne fait rien, écrite \(\pi_\varnothing\) dans ce cours. Les deux formulations ont leurs faiblesses, et ce n'est pas notre sujet ici.

{{% comment %}}SOURCE: AMODEI p.5{{% /comment %}}

Ce qui est notre sujet, c'est le second problème du premier endroit : le piratage de la récompense. Il a sa propre taxonomie, elle compte six entrées, et c'est la section suivante.

---
