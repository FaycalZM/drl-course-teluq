---
title: "Plan du cours"
weight: 1
---

# Apprentissage par Renforcement Profond

Quinze semaines, cinq modules, un projet continu qui court du début à la fin.

| Module | Semaines | Thème |
| --- | --- | --- |
| **Module 1** | 1 à 3 | Fondations et outillage profond |
| **Module 2** | 4 à 7 | Méthodes à base de valeur |
| **Module 3** | 8 à 10 | Méthodes à base de politique |
| **Module 4** | 11 à 14 | Frontières : exploration, auto-jeu, modèles du monde, alignement |
| **Module 5** | 15 | Applications, synthèse et soutenance |

**Évaluation** : projet continu à 100 %, en quatre jalons de 25 % (semaines 3, 7, 10 et 14),
plus les livrables finaux. Aucun examen terminal.

---

## Le fil conducteur : chaque module retire un obstacle que le précédent a nommé

Ce plan n'est pas une liste de sujets que l'on aurait pu mettre dans un autre ordre. Chaque
module se termine sur une limite **mesurée**, et le module suivant existe pour la lever.
C'est la seule façon de retenir quinze semaines de méthodes : non pas comme un catalogue,
mais comme une suite de problèmes résolus un par un.

{{< mermaid >}}
graph TD
  M1["Module 1 : l'outillage, et un agent qui juge un épisode entier"]
  M2["Module 2 : une valeur par état, de seize nombres aux pixels"]
  M3["Module 3 : la politique apprise directement"]
  M4["Module 4 : quatre hypothèses retirées une par une"]
  M5["Module 5 : choisir, et rendre"]
  M1 -->|"rien ne dit qu'un état vaut mieux qu'un autre"| M2
  M2 -->|"on ne peut pas énumérer un couple moteur"| M3
  M3 -->|"et si la récompense n'arrive jamais ?"| M4
  M4 -->|"aucun classement ne se transfère"| M5
  M1 --- J1["Jalon 1 · semaine 3"]
  M2 --- J2["Jalon 2 · semaine 7"]
  M3 --- J3["Jalon 3 · semaine 10"]
  M4 --- J4["Jalon 4 · semaine 14"]
  M5 --- LIV["Livrables finaux"]
{{< /mermaid >}}

Les étiquettes des flèches sont les insuffisances réellement constatées, et pas des
transitions de rédaction. L'agent de la semaine 3 ne sait juger qu'un épisode entier, une
fois terminé : c'est ce qui rend nécessaire une valeur par état. Toutes les méthodes du
module 2 se terminent par une maximisation sur les actions, ce qui suppose qu'on puisse les
énumérer : c'est ce qui rend nécessaire l'apprentissage direct de la politique. Les dix
premières semaines supposent une récompense assez fréquente pour qu'un hasard local la
rencontre : c'est ce qui ouvre le module 4. Et aucune comparaison du module 4 ne produit un
classement transférable d'un environnement à l'autre : c'est ce qui justifie un module
entier consacré au choix.

Chaque page d'accueil de module reprend ce fil en détail, avec son propre diagramme et la
liste des capacités vérifiables que le module installe.

---

## Ce que contient une semaine

Toutes les semaines ont la même forme, et la barre latérale vous la montre en permanence.

Une **introduction** ouvre la semaine : l'accroche, les objectifs mesurables (ce que vous
saurez faire à la fin, énoncé comme une liste de vérifications), les prérequis, et les
outils nécessaires. Viennent ensuite les **sections numérotées**, de six à seize selon la
semaine, qui sont le cours proprement dit. Chaque méthode y est présentée trois fois, selon
la double lecture : l'intuition, l'équation, puis le code et le tableau qui relie les
symboles aux variables. Puis le **laboratoire**, où vous écrivez le code vous-même, et le
**quiz**, qui se corrige immédiatement dans la page et ne compte pas dans la note. Les
semaines 3, 7, 10 et 14 portent en plus la page d'un **jalon**, et la semaine 15 celle des
**livrables finaux**.

Je ne vous donne volontairement **aucun nombre d'heures par semaine**, parce qu'il serait
faux pour la plupart d'entre vous : la lecture des sections varie peu, mais le temps de
laboratoire dépend de votre aisance avec PyTorch et de ce que vous choisissez d'explorer.
Ce que je vous donne à la place est plus utile, et c'est écrit en tête de chaque
laboratoire : son **budget de calcul**, en minutes ou en heures de machine, avec la raison
du découpage. Vous saurez donc toujours, avant de commencer, si la séance tient dans une
soirée.

> [!NOTE]
 **Les semaines ne se ressemblent pas en volume, et c'est délibéré.** Une semaine qui
 installe une seule idée centrale compte six sections ; une semaine qui doit tenir ensemble
 un modèle du monde et l'apprentissage hors ligne en compte seize. Le nombre de sections
 suit la matière, jamais un gabarit.

---

## Comment fonctionnent les laboratoires

Le laboratoire est l'endroit où ce cours se joue. Les sections vous montrent le code qui
réalise une équation ; le laboratoire vous demande de l'écrire, de le casser, et de mesurer
ce qui se passe.

Il est découpé en **parties progressives** : les trois premières semaines parlent de
niveaux, de l'implémentation guidée à l'extension créative, et à partir de la semaine 4 de
volets, qui vont du plus dirigé au facultatif. La plupart des laboratoires sont
**formatifs** : rien n'y est noté, et ils préparent le jalon qui suit. Certains volets sont
explicitement marqués comme **évalués**, et d'autres comme **facultatifs** : lisez
l'étiquette avant de vous lancer, parce qu'un volet facultatif peut être le plus long.

Deux habitudes sont posées dès la première semaine et ne vous quittent plus : une **graine
aléatoire** passée explicitement à chaque réinitialisation d'environnement, et une mesure
**répétée** sur plusieurs graines plutôt qu'une exécution unique commentée. À partir du
jalon 2, toute comparaison du cours repose sur plusieurs graines et un intervalle autour de
chaque moyenne, et c'est exactement ce que les laboratoires vous font pratiquer avant.

À partir de la semaine 9, chaque laboratoire se termine par une **solution courte** : la
même tâche en quelques lignes, au moyen d'une bibliothèque de haut niveau. Elle est là pour
situer votre travail, et elle est à lire **après** avoir écrit le vôtre, jamais avant. Deux
semaines n'en proposent aucune, et la page vous dit alors pourquoi : parce qu'aucune
bibliothèque ne fait ce que la semaine demande, ce qui est une information en soi.

> [!WARNING]
 **Les carnets Colab ne sont pas encore publiés.** Vous verrez donc, au bas de chaque
 laboratoire, un badge **gris** portant la mention « Carnet à venir » : il n'est pas
 cliquable, et ce n'est pas une panne de votre navigateur. Rien ne vous empêche de
 travailler dès maintenant : l'énoncé, les fragments de code, les trous à combler et les
 points de contrôle sont complets dans la page, et un carnet Colab vierge suffit à les
 recevoir. Les carnets préremplis arriveront, et le badge deviendra alors un lien.

---

## Les deux pages à garder ouvertes

Deux annexes servent toute l'année, et elles font foi en cas de doute. La page
[Notation]({{< relref "/docs/annexes/notation" >}}) est la table unique des symboles : une
seule notation court de la semaine 1 à la semaine 15, et cette page dit aussi ce que
signifient les lettres qui portent deux sens. La page
[Glossaire]({{< relref "/docs/annexes/glossaire" >}}) fixe les équivalences français et
anglais retenues, avec les formes à éviter et la semaine où chaque terme est introduit.

[Commencer la semaine 1 →]({{< relref "/docs/ch1-fondations-outillage/week01" >}})

{{% comment %}}
Page enrichie en phase 4. Le squelette de phase 1 demandait trois ajouts : fil conducteur
entre les modules (diagramme Mermaid), charge de travail hebdomadaire, modalités des
laboratoires. L'en-tête, le tableau des modules et la ligne d'évaluation étaient déjà
corrects et ne sont pas touchés.

Tout ce qui est affirmé ici est vérifiable dans le dépôt :
- les étiquettes du diagramme reprennent les ouvertures des cinq pages d'accueil de module ;
- « de six à seize sections » est le décompte réel des fichiers section-*.md (minimum 6 en
  semaines 3, 9 et 10 ; maximum 16 en semaines 13 et 14) ;
- la structure introduction / sections / laboratoire / quiz, plus jalon en 3, 7, 10, 14 et
  livrables en 15, est celle des quinze dossiers de semaine ;
- niveaux en semaines 1 à 3 puis volets à partir de la semaine 4, volets évalués et volets
  facultatifs : titres réels des pages lab.md ;
- solution courte à partir de la semaine 9, absente en semaines 12 et 15, où la page dit
  pourquoi ;
- badge Colab gris : layouts/shortcodes/colab.html rend un badge désactivé portant « Carnet
  à venir » pour url="TODO", ce qui est le cas des 53 appels des laboratoires.

CHARGE DE TRAVAIL : aucune durée hebdomadaire n'est écrite nulle part dans le dépôt, ni dans
course.yaml ni dans les quinze semaines. Rien n'est donc inventé : la page explique ce que
contient une semaine et renvoie au budget de calcul que chaque laboratoire annonce, qui est
la seule durée réellement documentée.

Aucune référence bibliographique visible (D17/D18).
{{% /comment %}}
