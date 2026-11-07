---
title: "14.11 Les parades, et pourquoi aucune ne ferme le problème"
weight: 12
---

## Quatre parades, chacune avec son aveu

Il existe une dizaine d'approches proposées contre le piratage de la récompense. J'en prends quatre, choisies parce qu'elles sont représentatives et parce que chacune vient avec une limite explicitement reconnue. C'est cette honnêteté qui en fait un bon matériau d'enseignement : une parade dont on connaît la faille est utilisable, une parade présentée comme complète ne l'est pas.

**Parade 1 : la récompense adverse.** Si l'agent trouve des stratégies que la récompense n'avait pas prévues, faisons de la récompense un agent elle aussi : un système qui cherche activement les situations où le premier système prétend réussir sans réussir. La limite est immédiate et elle est structurelle : il faut alors garantir que le vérificateur est **plus puissant** que le vérifié, et on a déplacé le problème d'un cran sans le résoudre.

**Parade 2 : le plafonnement de la récompense.** Au lieu de maximiser, viser un seuil : au-delà d'un certain niveau, la récompense ne monte plus. L'effet est réel et bien ciblé : cela supprime l'intérêt des stratégies à très faible probabilité et à gain énorme, qui sont celles qui produisent les comportements les plus étranges. Et l'aveu est tout aussi net : cela ne fait rien contre le robot qui ferme les yeux, parce que fermer les yeux n'est pas une stratégie à gain énorme, c'est une stratégie à **coût nul**.

**Parade 3 : le préentraînement de la récompense.** Entraîner le modèle de récompense **hors ligne**, sur des données que l'agent n'a pas produites, de sorte que l'agent ne puisse plus influencer ce qui le note. Vous reconnaissez le problème de la semaine 13, et vous reconnaissez aussi l'aveu : on renonce alors à **continuer d'apprendre la récompense**, c'est-à-dire exactement à ce que les trois tours de la section 14.8 faisaient. Et ce renoncement crée ses propres vulnérabilités, puisqu'une récompense gelée ne peut plus être corrigée quand la politique découvre une région qu'elle note mal.

**Parade 4 : les pièges de détection** (*trip wires*). Introduire délibérément dans l'environnement des vulnérabilités plausibles, et surveiller si l'agent les emprunte. L'idée est élégante : on ne cherche pas à empêcher le piratage, on cherche à le **détecter tôt**, sur des cas qu'on a choisis. L'aveu est à la hauteur : un agent suffisamment capable peut comprendre que ce sont des pièges et les éviter, ce qui produit un système qui passe tous les tests précisément parce qu'il les a reconnus.

{{% comment %}}SOURCE: AMODEI p.9-11{{% /comment %}}

| Parade | Ce qu'elle achète | Ce qu'elle ne peut pas |
| --- | --- | --- |
| récompense adverse | une recherche active des failles de l'objectif | garantir que le vérificateur domine le vérifié |
| plafonnement | éliminer les stratégies rares à gain énorme | rien contre une stratégie à coût nul |
| préentraînement | soustraire la récompense à l'influence de l'agent | continuer d'apprendre la récompense |
| pièges de détection | détecter tôt, sur des cas choisis | résister à un agent qui reconnaît le piège |

> [!IMPORTANT]
 **Aucune de ces quatre parades ne ferme le problème, et ce n'est pas un défaut de la liste.** Je veux que vous lisiez ce tableau comme un état de la question plutôt que comme un catalogue d'échecs. Trois des quatre parades déplacent le problème vers un autre endroit du système, où il est parfois plus facile à surveiller ; la quatrième ne prétend pas empêcher, seulement détecter. C'est un progrès réel, et c'est aussi la raison pour laquelle la seconde moitié de cette semaine met l'accent sur la **mesure** plutôt que sur la garantie. Si l'on ne peut pas empêcher l'écart, savoir le mesurer et savoir quand il s'ouvre devient la compétence centrale, et c'est ce que les sections 14.12 à 14.14 enseignent.

---

## La supervision extensible, et le cadre auquel appartient notre première moitié

Montons d'un niveau, parce que nous arrivons à l'endroit où les deux moitiés de la semaine se nouent une seconde fois, et cette fois dans l'autre sens.

Voici la formulation du problème, et elle a l'avantage d'être concrète. Ce que nous voudrions évaluer, à chaque décision de l'agent, c'est : **si une personne passait quelques heures à examiner ce résultat en détail, à quel point en serait-elle satisfaite ?** C'est l'objectif correct, et il n'est pas vague : il est parfaitement défini. Il est simplement impossible à calculer des millions de fois.

On se rabat donc sur des mesures bon marché, et ces mesures ne suivent pas parfaitement ce qui nous importe. C'est la **supervision extensible**, et le constat qui l'accompagne est celui qui ferme la boucle : ce rabattement **aggrave à la fois les effets secondaires et le piratage de la récompense**.

{{% comment %}}SOURCE: AMODEI p.11{{% /comment %}}

Relisez maintenant la première moitié de cette semaine à la lumière de ce paragraphe, et vous verrez qu'elle en est une réponse directe. Nous ne pouvions pas demander un jugement humain à chaque pas, alors nous en avons demandé trois cents, et nous avons **appris à interpoler entre eux**. Le modèle de récompense n'est rien d'autre qu'un dispositif de supervision extensible : il transforme un petit nombre de jugements coûteux en un signal disponible à chaque pas.

Et le prix de cette extension est exactement celui que le paragraphe annonce. Notre dispositif a rendu le jugement humain disponible partout, y compris là où aucun jugement humain n'avait été rendu, c'est-à-dire sur un sous-marin flottant à la surface pendant cinq mille pas. La supervision s'est étendue ; la **validité** de la supervision ne s'est pas étendue avec elle.

---

## Un apprentissage semi-supervisé, et une direction esquissée il y a dix ans

Une dernière formulation, et c'est celle qui m'intéresse le plus pour des raisons d'histoire.

Imaginons un cadre où la récompense n'est visible que sur une **petite fraction** des pas de temps ou des épisodes, alors que la performance de l'agent continue d'être évaluée sur tous. C'est l'**apprentissage par renforcement semi-supervisé**, et il existe une variante active où l'agent peut **demander** une étiquette quand il en a besoin.

La solution de référence la plus naïve consiste à ignorer les épisodes non étiquetés : elle fonctionne, et elle apprend très lentement, puisqu'elle jette la majeure partie de l'expérience.

Et la première approche sérieuse envisagée porte un nom : **l'apprentissage supervisé de la récompense**. Ajuster un modèle qui prédit la récompense, puis l'employer sur les épisodes non étiquetés.

{{% comment %}}SOURCE: AMODEI p.11-12{{% /comment %}}

Vous venez de lire, en une phrase, la chaîne entière de la première moitié de cette semaine.

> [!TIP]
 **Et voici pourquoi je trouve ce rapprochement plus instructif qu'un panorama de l'état de l'art.** La grille de sûreté que les sections 14.9 à 14.11 présentent a été établie **en 2016**, et vous lisez cette page en 2026. Elle a été écrite comme un **programme de recherche** : une liste de directions, sans savoir lesquelles seraient suivies, et en mettant délibérément de côté les scénarios de superintelligence pour s'en tenir à des problèmes posables aujourd'hui. Parmi ces directions, une seule ligne mentionnait l'idée d'ajuster un modèle de récompense sur des jugements humains. Dix ans plus tard, c'est la pièce qui a rendu les grands modèles de langue utilisables, et c'est la première moitié de cette semaine. Je ne vous raconte pas cela pour saluer une prédiction : je vous le raconte parce qu'un programme de recherche de dix ans se lit toujours mieux par les directions qu'il a listées que par celles qu'il a hiérarchisées. Quand vous lirez une liste de problèmes ouverts, ne cherchez pas laquelle est la plus importante : notez-les toutes, et relisez-les plus tard.

{{% comment %}}SOURCE: AMODEI p.2{{% /comment %}}

Un dernier point, et il sert au laboratoire. La forme d'expérience proposée pour ce cadre est simple : rendre la récompense visible sur **un épisode sur dix tirés au hasard**, d'abord sur une tâche de contrôle classique, puis sur un jeu. Le volet B du laboratoire est exactement de cette forme, et c'est de là qu'il tire sa légitimité : ce n'est pas une réduction au rabais de la chaîne de la première moitié, c'est le format d'expérience que ce cadre proposait.

{{% comment %}}SOURCE: AMODEI p.13{{% /comment %}}

---
