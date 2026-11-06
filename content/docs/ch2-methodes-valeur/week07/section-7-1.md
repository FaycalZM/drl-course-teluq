---
title: "7.1 La vitesse est une variable de recherche"
weight: 2
---

## Ce qu'une accélération achète réellement

Commençons par une comparaison de matériel, parce qu'elle est spectaculaire et qu'elle conduit tout droit à une conclusion qui ne l'est pas.

En 2005, une installation de calcul destinée à la mécanique des fluides numérique occupait **soixante-quatre serveurs**, répartis dans **trois armoires de 42 pouces**, avec son refroidissement et son alimentation électrique dédiés. Environ **un million de dollars** de matériel, pour **922 gigaflops** théoriques, ce qui la classait quatrième des machines de l'ex-URSS. Douze ans plus tard, une seule carte graphique grand public, la GTX 1080 Ti, annonçait **11 340 gigaflops**, soit **12,3 fois** plus, pour **700 dollars**. Rapporté au dollar, le prix du gigaflop avait été divisé par **plus de 17 500**. Et une carte de centre de données d'aujourd'hui est donnée pour **134 téraflops** en simple précision.

{{% comment %}}SOURCE: LAPAN ch.9 p.284-285{{% /comment %}}

Voilà pour les chiffres. Maintenant, pourquoi est-ce que je vous les donne ? Pas pour vous impressionner, et surtout pas pour vous laisser croire qu'il suffit d'attendre la prochaine carte. Je vous les donne parce qu'ils rendent visible un effet d'échelle qu'on sous-estime toujours. Prenez un calcul qui dure **un mois**. Multipliez la vitesse par 5 : il dure **six jours**, et vous pouvez le relancer le lendemain d'une erreur. Par 100 : **huit heures**, vous le lancez le soir et vous lisez le résultat au réveil. Par 20 000 : **deux à trois minutes**, et le calcul devient interactif, c'est-à-dire qu'il change de nature.

{{% comment %}}SOURCE: LAPAN ch.9 p.285{{% /comment %}}

Ce changement de nature est le vrai sujet de la section. Ce n'est pas la durée d'**une** exécution qui compte, c'est le **nombre d'exécutions** que vous pouvez vous permettre. Et en apprentissage automatique, le nombre d'exécutions n'est pas un confort : c'est la méthode de travail. Même un problème simple est presque impossible à implémenter correctement du premier coup. Il faut de nombreux essais avant de trouver des hyperparamètres convenables et avant d'avoir corrigé tous les bogues. Une accélération vaut donc exactement ce qu'elle achète en essais.

{{% comment %}}SOURCE: LAPAN ch.9 p.286{{% /comment %}}

> [!TIP]
 **Un effet secondaire que presque personne n'anticipe.** Quand le délai d'une expérience passe de plusieurs semaines à quelques heures, ce qui change n'est pas le résultat d'une expérience donnée : c'est la **disposition à en lancer**. Une question à laquelle on ne répondait pas, parce qu'elle coûtait trois semaines, devient une question qu'on tranche avant le déjeuner. Et la qualité de ce qui sort à la fin monte, non pas parce que chaque expérience est meilleure, mais parce qu'il y en a eu dix au lieu d'une. C'est un effet d'organisation du travail, et c'est le plus sous-estimé des bénéfices d'un profilage.

{{% comment %}}SOURCE: LAPAN ch.9 p.286{{% /comment %}}

Il y a un second usage possible d'une accélération, et il faut savoir qu'il existe pour pouvoir le choisir : au lieu de dépenser le gain en **attente évitée**, on peut le dépenser en **taille de problème**. Moins de simplifications, plus de données, plus de précision. Le même facteur 10 peut donc servir à aller dix fois plus vite ou à traiter un problème dix fois plus gros, et c'est une décision de projet, pas une conséquence technique.

{{% comment %}}SOURCE: LAPAN ch.9 p.286{{% /comment %}}

---

## Pourquoi cette question est plus aiguë en apprentissage par renforcement qu'ailleurs

Il y a une raison précise pour laquelle ce cours consacre une semaine entière à la performance, alors qu'un cours d'apprentissage supervisé ne le ferait pas.

Les méthodes de l'état de l'art en apprentissage par renforcement sont **très peu efficaces en échantillons**. Vous avez déjà rencontré le terme en semaine 6 : il désigne le nombre d'interactions avec l'environnement nécessaires pour atteindre un niveau donné. Pour un jeu Atari, il se compte en **millions** d'interactions, ce qui peut représenter des semaines d'entraînement. Autrement dit, le coût de calcul n'est pas une nuisance périphérique de la discipline : il est au centre, et il décide de ce que vous avez le droit d'essayer.

{{% comment %}}SOURCE: LAPAN ch.9 p.286{{% /comment %}}

Un mot sur la frontière de la recherche, pour situer ce que nous faisons. Les jeux Atari sont aujourd'hui considérés comme résolus, y compris ceux qui demandent une exploration difficile, comme *Montezuma's Revenge*, dont vous entendrez encore parler en semaine 11. L'effort s'est déplacé vers des problèmes comme le repliement des protéines et les grands modèles de langue, qui s'entraînent sur des **milliers** de processeurs graphiques en parallèle. Nous travaillons donc, cette semaine, sur un problème dont la difficulté a été largement absorbée par le matériel, et c'est exactement ce qui le rend bon pour apprendre : les ordres de grandeur sont tenables, et les mécanismes sont les mêmes.

{{% comment %}}SOURCE: LAPAN ch.9 p.286-287{{% /comment %}}

> [!WARNING]
 **La règle de la semaine, et je la place ici pour qu'elle précède tout le reste.** Toute optimisation de performance n'a de sens que si la **méthode** fonctionne déjà correctement. Un programme lent et juste vaut beaucoup mieux qu'un programme rapide et faux, pour une raison très concrète : le programme lent vous donne une réponse tardive, le programme faux vous donne une réponse fausse, et vous la croyez. L'ordre imposé par cette règle n'est pas négociable, et c'est l'ordre du laboratoire : on fait marcher, **puis** on mesure, **puis** on accélère, **puis** on remesure.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

---
