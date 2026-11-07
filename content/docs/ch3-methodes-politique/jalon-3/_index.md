---
title: "Jalon 3 (25 %)"
weight: 11
---

# Jalon 3, 25 % de la note finale

Une méthode de politique qui apprend, une analyse de la variance de son gradient, et une
comparaison honnête avec le réseau Q profond du jalon 2, sur l'efficacité d'échantillon,
la stabilité et le temps d'horloge. L'exigence du jalon 2 est reprise sans modification :
plusieurs graines aléatoires et un intervalle autour de chaque moyenne.

---

## Ce que vous remettez

Un carnet Colab exécuté, un tableau de comparaison et une note de deux pages environ.
Vous choisissez d'abord l'une des deux routes, et ce choix figure dans votre annexe.

| Livrable | Forme | Points |
| --- | --- | --- |
| La méthode de politique, complète et correcte sur les quatre points de l'énoncé | Colab, sorties visibles | 4 |
| Elle **apprend** : au moins trois graines, intervalle, cible annoncée depuis un pilote | carnet, une courbe | 3 |
| Le diagnostic de la semaine : divergence par époque, fraction d'échantillons écrêtés | carnet, une figure | 2 |
| Variance du gradient entre au moins deux configurations, grandeur mesurée définie | une figure plus un paragraphe | 4 |
| Comparaison avec le DQN du jalon 2 sur les **trois** axes, mêmes graines, même évaluation | tableau | 5 |
| Exécutions n'ayant pas atteint la cible, comptées à part de la moyenne, par méthode | tableau ou note | 2 |
| Analyse critique, dont au moins une contradiction entre deux axes ou sa mention | note de 1 à 2 pages | 3 |
| Annexe de reproductibilité, **et la route choisie** | une demi-page | 2 |
| **Total** | | **25** |

**Ce qui n'est pas demandé** : battre un score, implémenter TRPO ou ACKTR, ou tourner sur
un banc d'essai de locomotion. Comptez deux à trois heures de calcul au total.

---

## L'énoncé complet

L'énoncé vit dans la semaine 10 : ce qui est évalué, les deux routes entre lesquelles vous
choisissez, le budget de calcul, les cinq étapes du livrable et les conseils de rédaction.

[Ouvrir l'énoncé du jalon 3 →]({{< relref "/docs/ch3-methodes-politique/week10/jalon-3" >}})

---

## Remise

{{< remise cle="jalon-3" >}}

{{% comment %}}
Cette page est un pointeur, pas une seconde copie. L'énoncé vit dans
content/docs/ch3-methodes-politique/week10/jalon-3.md, issu du bloc « Jalon 3 » de
source-assets/raw-content/week-10.md, de sorte qu'il n'existe qu'un seul texte à
corriger. Même forme que ch1-fondations-outillage/jalon-1 (vers week03/jalon-1.md) et
ch2-methodes-valeur/jalon-2 (vers week07/jalon-2.md).

Le 07/11, ajout du rappel des livrables et du bloc de remise, sur les cinq pages de
travail noté. Le tableau est une copie abrégée de celui de week10/jalon-3.md : même
ordre, mêmes points, même total, libellés raccourcis. L'échéance et le poids viennent de
[params.remises.jalon-3] dans hugo.toml, jamais du contenu.
{{% /comment %}}
