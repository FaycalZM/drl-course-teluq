---
title: "Accueil"
layout: "page"
---

# SCI1070 : Apprentissage par Renforcement Profond

Bienvenue. Ce cours prolonge SCI1060 : nous y remplaçons les tables de valeurs par des
réseaux de neurones, et nous suivons le chemin complet qui mène d'un premier agent
rudimentaire aux méthodes qui font aujourd'hui la recherche et l'industrie.

## Ce que nous allons faire, et pourquoi cela demande quinze semaines

Bonjour à toutes et à tous ! Je suis heureuse de vous accueillir dans ce cours, et je veux
commencer par la chose qui m'y plaît le plus. En apprentissage par renforcement classique,
vous avez appris à remplir un tableau : une case par état, un nombre par case, et une règle
qui améliore ce nombre jusqu'à ce qu'il cesse de bouger. Cela fonctionne remarquablement
bien, et cela s'arrête net le jour où les états ne se comptent plus. Un écran de jeu, une
série de prix, l'image rendue par une caméra : il n'y a pas de tableau assez grand, et il
n'y en aura jamais.

L'idée de ce cours tient en une phrase : remplacer le tableau par une **fonction apprise**.
Un réseau de neurones ne mémorise pas une valeur par état, il en calcule une pour un état
qu'il n'a jamais vu. Cette seule substitution ouvre tout ce que vous avez vu passer dans
l'actualité de la discipline, et elle coûte cher : trois certitudes de l'apprentissage
tabulaire tombent en même temps, et une bonne partie du cours consiste à constater la chute,
puis à construire ce qui tient quand même debout.

> [!IMPORTANT]
 **Ce cours ne vous présentera pas une parade de réussites.** Vous y verrez une méthode
 diverger sur trois lignes d'arithmétique, un agent parfaitement entraîné qui n'apprend
 rien, un classement de méthodes qui s'inverse d'un environnement à l'autre, et une
 récompense exploitée par l'agent même qui l'optimise. Ce n'est pas du pessimisme
 pédagogique : c'est la seule façon de vous rendre capables de juger un résultat, le vôtre
 comme celui des autres. Un échec correctement mesuré vaut, dans ce cours, autant qu'une
 réussite.

---

## La philosophie : l'intuition d'abord

Je ne vous demanderai jamais d'avaler une équation avant d'en avoir l'image. Chaque méthode
du cours est donc présentée **trois fois de suite**, et nous appelons cela la **double
lecture**.

D'abord l'idée, en mots, avec une image mentale : quel problème cette méthode résout, et
pourquoi quelqu'un a eu besoin de l'inventer. Ensuite l'équation, dans une notation unique
que nous ne changerons pas de la semaine 1 à la semaine 15, chaque symbole étant défini là
où il apparaît pour la première fois. Enfin le code qui la réalise, suivi d'un tableau à
trois colonnes qui met en vis-à-vis le symbole, sa signification et le nom de la variable
qui le porte.

Cette répétition est délibérée, et voici ce qu'elle vous achète. Vous pouvez suivre ce cours
en ne lisant bien qu'un seul des trois volets : quelqu'un qui raisonne en images tiendra par
l'intuition, quelqu'un qui vient des mathématiques tiendra par les équations, quelqu'un qui
apprend en tapant tiendra par le code. Aucun des trois chemins n'est un rabais. Mais si vous
lisez les trois, vous gagnez autre chose, parce que **chacun attrape ce que les deux autres
cachent** : l'intuition dit pourquoi, et tait les conditions de validité ; l'équation dit
exactement quoi, et ne dit pas où se trouve le piège d'implémentation ; le code, lui, est
l'endroit où se logent les erreurs qui ne lèvent aucune exception, et il ne vous dira jamais
de lui-même qu'il calcule la mauvaise quantité. Le tableau de correspondance est la couture
entre les trois, et c'est la page que vous relirez le plus souvent.

> [!TIP]
 **Lisez avec un carnet ouvert à côté.** Les laboratoires du cours sont construits pour
 que vous changiez une valeur et observiez ce qui se passe, et la plupart des exercices
 tournent en quelques minutes sans matériel particulier. Un cours d'apprentissage par
 renforcement qu'on se contente de lire ne laisse pas grand-chose : c'est en voyant une
 courbe refuser de monter qu'on apprend ce qu'elle mesure.

---

## La carte du voyage : cinq modules

Quinze semaines, cinq modules, et un fil qui ne se rompt pas : chaque module retire un
obstacle que le précédent a nommé.

Le [module 1]({{< relref "/docs/ch1-fondations-outillage" >}}) construit l'outillage, un
cadre mathématique précis d'un côté et PyTorch de l'autre, puis les branche l'un sur l'autre
pour obtenir un premier agent qui apprend, et dont la méthode n'utilise **aucune fonction de
valeur**.

Le [module 2]({{< relref "/docs/ch2-methodes-valeur" >}}) apprend des valeurs, écrit la même
équation quatre fois, de seize nombres à des pixels d'écran, puis se termine contre un
problème que personne n'a préparé pour nous, une série de prix, où le signal utile est plus
petit que le coût d'un aller-retour.

Le [module 3]({{< relref "/docs/ch3-methodes-politique" >}}) apprend directement la
politique, ce qui achète les politiques stochastiques et surtout les **actions continues**,
et se termine sur la question qui gouverne toute cette famille : de combien une politique a
le droit de changer en un seul pas.

Le [module 4]({{< relref "/docs/ch4-frontieres" >}}) retire, une semaine à la fois, les
hypothèses dont les dix premières semaines ont vécu sans les discuter : que la récompense
arrive assez souvent, que l'environnement reste immobile, qu'on peut interagir à volonté, et
que quelqu'un a su écrire la récompense.

Le [module 5]({{< relref "/docs/ch5-applications-synthese" >}}) n'enseigne plus aucune
méthode : il apprend à **choisir** entre celles des quatorze semaines précédentes, à partir
de trois questions que l'on pose à n'importe quel problème.

Le [plan du cours]({{< relref "/docs" >}}) détaille le contenu de chaque module et la forme
d'une semaine.

---

## L'évaluation : un projet continu, et un seul critère au bout

Il n'y a **aucun examen terminal**. Votre note vient à 100 % d'un **projet continu** : un
environnement que vous choisissez en semaine 1 et que vous ne quittez plus, sur lequel vous
construirez successivement les quatre grandes familles de méthodes du cours. Ce projet est
évalué en quatre **jalons de 25 %**, aux semaines 3, 7, 10 et 14, puis par les **livrables
finaux**, qui portent sur l'ensemble de la trajectoire plutôt que sur une semaine : un
rapport, une présentation et un dépôt.

Chaque jalon a son critère propre, et vous les trouverez sur sa page. Mais il y en a un qui
les traverse tous, qui pèse le plus lourd au bout, et que je préfère vous dire dès
aujourd'hui, parce qu'il change la façon de travailler dès la première semaine :
**quelqu'un d'autre peut l'exécuter**. Pas « le code est propre », pas « les résultats sont
bons » : une personne qui ne vous connaît pas, munie de votre dépôt et de votre rapport,
obtient quelque chose de comparable à ce que vous rapportez, ou sait exactement pourquoi
elle ne l'obtient pas.

> [!WARNING]
 **Ce critère se gagne au fil des semaines, jamais à la fin.** Les graines aléatoires que
 vous n'avez pas notées, l'hyperparamètre écrit en dur au milieu d'une cellule, la mesure
 dont vous ne savez plus sur quelle machine elle a été prise : rien de tout cela ne se
 reconstitue au moment du rapport. Tenez un journal où vit le nombre, dès le premier
 laboratoire, et le dernier livrable ne vous demandera presque aucun travail
 supplémentaire.

---

## Ce qu'il vous faut pour commencer

SCI1060 pour le vocabulaire de l'apprentissage par renforcement, et une pratique courante de
Python : classes, héritage, annotations de type, NumPy. L'aisance avec PyTorch n'est **pas**
un prérequis, la semaine 2 est là pour cela.

Côté matériel, un navigateur suffit. Les laboratoires s'exécutent dans Google Colab, et la
grande majorité d'entre eux n'a besoin d'aucun processeur graphique ; là où il en faut un,
l'accélérateur gratuit de Colab est dimensionné pour le travail demandé, et la page du
laboratoire vous annonce son budget de calcul avant que vous ne commenciez. Les
environnements viennent de Gymnasium, dont la documentation en ligne vous servira aussi de
catalogue au moment de choisir celui de votre projet. Gardez enfin deux pages du cours
ouvertes en permanence : la **notation**, qui est la table unique des symboles, et le
**glossaire**, qui fixe les équivalences français et anglais retenues.

Prêts ? La semaine 1 commence par une souris dans un labyrinthe, et finit par votre premier
chiffre mesuré.

[Entrer dans le cours →]({{< relref "/docs" >}})

{{% comment %}}
Page d'accueil rédigée en phase 4. Elle remplace le squelette de phase 1, qui affichait
« Contenu en préparation » et dont le commentaire demandait quatre pièces : accroche de la
professeure, philosophie « intuition d'abord », carte du voyage en cinq modules, modalités
d'évaluation. Les quatre sont écrites en prose continue, dans l'ordre demandé.

Sources internes au dépôt, aucune source externe : les cinq phrases de modules sont reprises
des cinq pages d'accueil de module (docs/ch1 à ch5), le barème vient de course.yaml
(assessment : 100 %, quatre jalons de 25 %, semaines 3/7/10/14, final_exam false) et le
critère unique du dernier paragraphe d'évaluation vient de
week15/livrables-finaux.md. La description de la double lecture suit D10 et la formulation
déjà employée dans section-1-8.md et section-2-3.md (« l'intuition, l'équation, puis le code
et la table qui relie les deux »).

Non signée, délibérément : aucune page de content/ ne porte de signature, les quinze
introductions de semaine parlant à la première personne sans se signer. Le gabarit du cours
LLM signe sa page d'accueil ; ne pas inventer ici une forme que le reste du site n'a pas.

Aucune référence bibliographique visible (D17/D18) : les seules ressources nommées sont des
outils (Colab, Gymnasium) et des pages du cours.
{{% /comment %}}
