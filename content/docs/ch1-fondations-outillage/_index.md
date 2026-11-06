---
title: "Module 1 : Fondations et outillage profond"
weight: 1
bookCollapseSection: true
---

# Module 1 : Fondations et outillage profond

Vous arrivez avec le vocabulaire de l'apprentissage par renforcement classique et, pour beaucoup d'entre vous, sans grande pratique de PyTorch. Ce module répond donc à une question très concrète : de quoi faut-il disposer, exactement, avant qu'un agent profond puisse exister ? De deux choses qui n'ont rien à voir l'une avec l'autre. Un cadre assez précis pour qu'une équation ne soit jamais ambiguë, et un outil assez familier pour qu'un réseau de neurones s'écrive sans hésitation. Nous construisons l'un, puis l'autre, et nous ne les mélangeons pas tant qu'ils ne tiennent pas debout séparément.

Ensuite nous les branchons l'un sur l'autre, et le premier agent de ce cours apprend. Sa méthode est d'une simplicité presque insolente : jouer seize épisodes avec la politique courante, garder les meilleurs, apprendre au réseau à les imiter, recommencer. Elle tient en moins de cent lignes, elle n'utilise **aucune fonction de valeur**, et elle résout CartPole en une quarantaine de lots. Puis nous la relançons, sans y changer une seule ligne, sur un environnement où elle n'apprendra rien du tout.

C'est cet échec qui fait l'intérêt du module, et c'est lui que le premier jalon évalue. Mesurer avant de conclure, nommer la limite d'une méthode plutôt que la contourner : voilà l'habitude que ces trois semaines installent, et dont les quatorze suivantes vivent. La méthode de la semaine 3 n'est d'ailleurs pas un cul-de-sac. Elle disparaît pendant dix semaines, et elle revient en semaine 13 comme planificateur à l'intérieur d'un modèle du monde.

> [!IMPORTANT]
 **Ce module ne vous apprend pas seulement une méthode, il vous apprend à la mesurer.** Résoudre CartPole est la partie facile. Nommer la raison pour laquelle la même méthode, au même code, n'apprend rien sur un autre environnement est la partie qui compte, et c'est elle qui est notée.

---
## Deux outils construits à part, puis un agent qui apprend

{{< mermaid >}}
graph TD
  W1["Semaine 1 : rappels RL et Gymnasium"] --> W2["Semaine 2 : apprentissage profond"]
  W1 -->|"la boucle d'interaction"| W3
  W2 -->|"la boucle d'entraînement"| W3["Semaine 3 : entropie croisée"]
  W3 -->|"son échec, analysé"| J1["Jalon 1"]
  J1 --> M2["Module 2 : une valeur par état"]
{{< /mermaid >}}

Les semaines 1 et 2 se suivent dans le calendrier sans dépendre l'une de l'autre par leur contenu : il n'y a pas une ligne d'apprentissage par renforcement dans la seconde, et c'est entièrement assumé, puisqu'on ne branche pas un outil que l'on ne possède pas. C'est la semaine 3 qui a besoin des deux à la fois, la boucle d'interaction de la première et la boucle d'entraînement de la seconde, et le jalon 1 referme le module sur ce qu'elles produisent ensemble.

---
## Ce que vous saurez faire en entrant dans le module 2

- écrire la boucle agent-environnement complète sur un environnement Gymnasium, sans aucune bibliothèque d'algorithmes, et dire pour chacune des cinq valeurs rendues par `step()` ce qu'elle représente dans le formalisme ;
- distinguer une terminaison d'une troncature, et dire laquelle des deux a le droit d'interrompre un amorçage ;
- poser une enveloppe (*wrapper*) sur un environnement pour en changer les observations, les actions ou la récompense sans toucher à son code ;
- construire un perceptron multicouche avec PyTorch, l'entraîner avec la boucle en huit lignes, et suivre ses courbes dans TensorBoard ;
- montrer sur vos propres mesures qu'un empilement de couches linéaires sans fonction d'activation ne vaut pas mieux qu'une couche unique ;
- écrire la méthode d'entropie croisée de bout en bout, en moins de cent lignes, et résoudre CartPole avec ;
- prédire l'échec d'une méthode sur un environnement donné à partir de l'histogramme des récompenses de deux cents épisodes aléatoires, avant d'avoir écrit une ligne de l'agent ;
- situer n'importe quelle méthode sur les trois axes du domaine : avec ou sans modèle, fondée sur la valeur ou sur la politique, sur politique ou hors politique.

---
## Le travail évalué de ce module

Le **jalon 1** referme le module et vaut 25 % de la note finale : l'environnement que vous avez choisi, la chaîne d'enveloppes qui l'adapte, une version de référence par entropie croisée, et l'analyse de ce qui la fait échouer. C'est l'analyse qui est notée, pas la réussite.

[Ouvrir le jalon 1 →]({{< relref "/docs/ch1-fondations-outillage/jalon-1" >}})

{{% comment %}}
Page de module rédigée en phase 4, à partir des trois pages d'accueil de semaine
(week01, week02, week03) et de course.yaml. Elle remplace le squelette de phase 1, qui
affichait « Contenu en préparation » et dupliquait la liste des semaines que la barre
latérale produit déjà.

Les trois pièces sont celles que le squelette demandait : accroche, fil conducteur en
Mermaid, et capacités vérifiables. Le renvoi au jalon pointe vers la page de jalon du
module, qui relaie elle-même vers l'énoncé unique dans week03/jalon-1.md.
{{% /comment %}}
