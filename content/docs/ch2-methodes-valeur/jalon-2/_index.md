---
title: "Jalon 2 (25 %)"
weight: 8
---

# Jalon 2, 25 % de la note finale

Un réseau Q profond, au moins deux extensions, une comparaison qui tient debout et une
accélération mesurée. À partir de ce jalon, toute comparaison repose sur plusieurs
graines aléatoires et un intervalle de confiance.

---

## Ce que vous remettez

Un carnet Colab exécuté, deux tableaux et une note de deux pages environ.

| Livrable | Forme | Points |
| --- | --- | --- |
| Socle de code unique, variantes activées par un drapeau, DQN plus deux extensions | Colab, sorties visibles | 3 |
| La version de référence, mesurée **et** montrée convergente avant toute accélération | carnet, une courbe | 3 |
| Courbes comparatives en moyenne avec intervalle, mêmes graines partout | une figure par comparaison | 5 |
| Tableau d'accélération : variante, FPS, ΔFPS, temps au seuil, ΔTemps, graines, intervalle, matériel | tableau | 4 |
| Le désaccord entre les deux indicateurs, ou la mention explicite qu'il n'y en a pas eu | un paragraphe | 2 |
| Exécutions non convergées, comptées à part de la moyenne, par variante | tableau ou note | 2 |
| Analyse critique : une mesure, une déduction, une conclusion | note de 1 à 2 pages | 4 |
| Annexe de reproductibilité : graines, hyperparamètres, seuil, matériel, durée | une demi-page | 2 |
| **Total** | | **25** |

**Ce qui n'est pas demandé** : battre un score, obtenir une accélération d'un facteur
donné, ou exécuter quoi que ce soit à l'échelle d'Atari. Comptez deux à trois heures de
calcul au total, pas davantage.

---

## L'énoncé complet

L'énoncé vit dans la semaine 7 : ce qui est évalué, le budget de calcul, les cinq étapes
du livrable, deux exemples travaillés de bonne lecture, et les contraintes.

[Ouvrir l'énoncé du jalon 2 →]({{< relref "/docs/ch2-methodes-valeur/week07/jalon-2" >}})

---

## Remise

{{< remise cle="jalon-2" >}}

{{% comment %}}
Cette page est un pointeur, pas une seconde copie. L'énoncé vit dans
content/docs/ch2-methodes-valeur/week07/jalon-2.md, issu du bloc « Jalon 2 » de
source-assets/raw-content/week-07.md, de sorte qu'il n'existe qu'un seul texte à
corriger. La duplication équivalente de la semaine 3 a été traitée depuis :
ch1-fondations-outillage/jalon-1 est devenue un pointeur vers week03/jalon-1.md le 06/11,
sur ce modèle. Les jalons 3 (semaine 10) et 4 (semaine 14) suivent la même forme.

Le 07/11, ajout du rappel des livrables et du bloc de remise, sur les cinq pages de
travail noté. Le tableau est une copie assumée de celui de week07/jalon-2.md, abrégée :
même ordre, mêmes points, même total. La ligne « Total » existe pour qu'une divergence
future se voie. L'échéance et le poids viennent de [params.remises.jalon-2] dans
hugo.toml, jamais du contenu.
{{% /comment %}}
