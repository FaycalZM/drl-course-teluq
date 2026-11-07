---
title: "15.10 La carte de décision"
weight: 11
---

## Quatorze semaines, rangées autrement

Nous arrivons à l'objet pour lequel cette semaine existe, et je l'appelle une **carte de décision** (*decision map*). Je vais vous donner les quatorze semaines du cours rangées **non pas par ordre chronologique** mais par les **caractéristiques du problème** qui les sélectionnent.

Pourquoi cette réorganisation est nécessaire, et pourquoi elle n'est pas un simple exercice de présentation : vous avez appris ces méthodes dans l'ordre où elles se construisent les unes sur les autres, ce qui est le bon ordre pour les **apprendre**. Ce n'est pas du tout le bon ordre pour les **choisir**. Devant un problème, vous ne vous demandez pas « quelle est la méthode qui vient après celle de la semaine dernière » : vous vous demandez « mes actions sont-elles continues », et la réponse à cette seule question élimine la moitié du programme.

La **Figure 15-2** est cette carte, et elle est volontairement dessinée comme une carte et non comme une frise. Vous devez pouvoir y entrer par n'importe quelle caractéristique, sans avoir lu les semaines dans l'ordre. Elle retient les **cinq questions** qui séparent le plus vite : vos actions sont-elles discrètes ou continues, votre récompense est-elle dense, parcimonieuse ou à apprendre, la collecte est-elle bon marché ou coûteuse, y a-t-il un agent ou plusieurs, et disposez-vous d'un modèle du monde. Deux marques y cohabitent : une pleine pour « c'est là que l'on commence », une creuse pour « cela s'applique, sans être le premier réflexe ». Les semaines 1 et 2 y occupent une bande sans aucune marque, et c'est volontaire : ce sont de l'outillage, elles ne se choisissent pas, elles se traversent.

{{< bookfig src="15-02.png" week="15" >}}

---

## La carte, en tableau

Le tableau ci-dessous est la version longue de la même carte, celle que vous pouvez interroger ligne par ligne, et il porte des caractéristiques que les cinq questions de la figure ne couvrent pas : la nature des observations, le cas d'un adversaire, et deux entrées qui ne sont pas des méthodes du tout. Lisez la figure pour décider vite et le tableau pour les cas particuliers. Chaque ligne est une **caractéristique du problème** ; la colonne de droite dit où aller.

| Caractéristique de votre problème | Où aller |
| --- | --- |
| Je veux une référence en une soirée, sans théorie | semaine 3, la méthode de sélection d'élites. Elle est simple, elle marche souvent, et son échec est informatif |
| Actions discrètes, peu nombreuses, modèle de la dynamique **disponible** | semaine 4, itération de la valeur : ne construisez pas de réseau si une table suffit |
| Actions discrètes, peu nombreuses, modèle **indisponible**, observations riches | semaine 5, réseau Q profond, puis semaine 6 pour les extensions qui le stabilisent |
| Actions discrètes **très** nombreuses, ou qui **changent d'un état à l'autre** | semaine 5 avec l'architecture de la section 15.3 : entrée en couple observation-action, une seule sortie |
| Actions **produites** plutôt que choisies, et de la langue naturelle | section 15.9 avant tout le reste : demandez-vous si c'est un problème de langue |
| Actions **continues** | semaine 9 pour la politique gaussienne et les méthodes déterministes, semaine 10 pour la stabilité |
| Entraînement instable, pas de mise à jour impossible à régler | semaine 10, régions de confiance et objectif écrêté |
| Variance du gradient trop forte | semaine 8 : référence, avantage, et prime d'entropie |
| Récompense **dense**, beaucoup d'interactions disponibles | semaines 5, 8 et 10, dans cet ordre de complexité croissante |
| Récompense **parcimonieuse**, état but **inconnu** | semaine 11, exploration dirigée : comptage, nouveauté, distillation de réseau aléatoire |
| Récompense **parcimonieuse**, état but **connu** et dynamique **inversible** | section 15.5 : n'explorez pas, **engendrez vos données à reculons** depuis le but |
| Récompense **inexistante** ou impossible à spécifier | semaine 14 : apprenez-la de jugements humains, et lisez la seconde moitié de cette semaine-là avant de le faire |
| Interactions **coûteuses** mais possibles | semaine 13, première moitié : apprenez un modèle du monde et entraînez dedans. Et semaine 7 pour que ce que vous avez aille plus vite |
| **Aucune** interaction possible, un jeu de données figé | semaine 13, seconde moitié : apprentissage hors ligne, contraintes et pessimisme |
| Un modèle de la dynamique disponible **et** un budget de calcul par décision | semaine 12 : planifiez, et guidez la planification par un réseau |
| Un adversaire, ou une symétrie à exploiter | semaine 12, auto-jeu |
| **Plusieurs agents** qui apprennent en même temps | semaine 12, seconde moitié : attendez-vous à de la non-stationnarité |
| L'entraînement est correct mais trop lent | semaine 7 : profilez d'abord, vectorisez ensuite, et ne faites jamais l'inverse |
| Les observations sont des **images** | semaine 2 pour l'architecture, semaine 5 pour les enveloppes de prétraitement |
| Les observations sont du **texte** | section 15.3 pour la représentation, section 15.9 pour la question préalable |
| Le système est **déjà déployé** et on me demande s'il va bien | semaine 14, seconde moitié : la pression d'optimisation, la transition de phase, et pourquoi une corrélation ne protège de rien |

---

## Comment on s'en sert, sur un problème que personne n'a préparé

Je vous montre la procédure une fois, sur un problème inventé pour l'occasion, parce que c'est exactement ce que vos livrables finaux demandent.

**Le problème.** Un parc de deux cents machines industrielles. Chaque jour, on décide pour chaque machine : ne rien faire, inspecter, ou remplacer une pièce. On observe des relevés de capteurs, un historique de pannes, et le temps écoulé depuis la dernière intervention. Une panne coûte cher, une intervention coûte un peu, et une machine arrêtée ne produit pas. On nous demande un agent.

**Première question, l'observation.** Un vecteur de relevés par machine, plus de l'historique. Ce n'est ni une image ni du texte : les semaines 2 et 5 ne sont pas le cœur du sujet, et la section 15.9 ne s'applique pas. En revanche l'historique pose une question de mémoire : deux cents machines dans des états différents, est-ce **une** décision sur deux cents dimensions ou **deux cents** décisions couplées ? La ligne « plusieurs agents » de la carte s'allume, et il faut y réfléchir avant d'écrire une ligne de code.

**Deuxième question, l'action.** Trois actions discrètes par machine. Discret et peu nombreux : les semaines 9 et 10 ne sont pas nécessaires. La semaine 5 l'est.

**Troisième question, la récompense.** Et c'est ici que le problème se décide. Qui écrit la récompense ? Il faut arbitrer entre le coût d'une panne, le coût d'une intervention et le coût d'un arrêt de production. Ces trois coûts n'ont pas d'unité commune évidente, et le choix du coefficient **est** la politique de maintenance de l'entreprise. La semaine 14 s'allume, et plutôt dans sa seconde moitié : vous n'avez pas un problème d'optimisation, vous avez un problème de **spécification**.

**Quatrième question, celle de la section 15.2.** Combien d'interactions pouvez-vous obtenir ? Vous ne pouvez pas casser deux cents machines pour entraîner un agent. Donc : soit vous avez un **simulateur**, et vous êtes dans la semaine 12 ou la première moitié de la semaine 13 ; soit vous n'avez que les **journaux historiques** du parc, et vous êtes dans la seconde moitié de la semaine 13, avec tout ce qu'elle a dit du décalage de distribution.

**Le verdict.** Trois semaines sont pertinentes : la **semaine 13** pour le régime d'apprentissage, la **semaine 14** pour la spécification de la récompense, et la **semaine 5** pour la méthode de base. Onze ne le sont pas. Et la décision la plus importante n'est pas le choix de l'algorithme : c'est de savoir si vous avez un simulateur ou des journaux, parce que cette seule réponse déplace le problème d'un module du cours à un autre.

> [!TIP]
 **Le test que je vous propose pour savoir si vous avez acquis quelque chose cette semaine.** Prenez un problème qui vous intéresse, et écrivez **trois numéros de semaine** et **une phrase** expliquant pourquoi les onze autres ne s'appliquent pas. Si vous écrivez huit numéros, vous n'avez pas encore décidé. Si vous écrivez zéro, le problème n'est peut-être pas un problème d'apprentissage par renforcement, et c'est une conclusion parfaitement respectable : c'en est même souvent la bonne. Et regardez la carte à l'envers une fois : une ligne qui ne s'allume jamais sur aucun de vos problèmes est une méthode que vous n'avez pas besoin de maîtriser cette année.

---
