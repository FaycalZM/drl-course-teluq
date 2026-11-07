---
title: "12.1 Ce qu'un modèle achète, et ce qu'il ne faut pas lui prêter"
weight: 2
---

## Le mot « modèle », et pourquoi onze semaines s'en sont passées

La semaine 3 a posé la taxonomie que ce cours suit depuis : une méthode est fondée sur la valeur ou sur la politique, elle est sur politique ou hors politique, et elle est **avec modèle** (*model-based*) ou **sans modèle**. Nous avons exploré les deux premières oppositions dans tous les sens pendant huit semaines. La troisième, nous l'avons laissée intacte : toutes les méthodes de ce cours, sans une seule exception, sont du côté sans modèle.

{{% comment %}}SOURCE: LAPAN ch.20 p.601{{% /comment %}}

Mettons-nous d'accord sur le mot, parce qu'il est employé pour deux choses différentes et que la confusion est facile. Ici, « modèle » ne désigne pas le réseau de neurones. Il désigne un **modèle de l'environnement** : un objet qui, à partir d'un état et d'une action, vous rend un nouvel état et une récompense, sans que l'environnement réel ait besoin d'être touché. Une méthode sans modèle ne fait **aucun effort** pour prédire, comprendre ou simuler son environnement : elle le subit, elle y agit, et elle apprend de ce qu'il lui renvoie.

{{% comment %}}SOURCE: LAPAN ch.20 p.601{{% /comment %}}

---

## Deux motivations, et pas une troisième

Pourquoi se donner ce travail supplémentaire ? Il y a exactement deux réponses, et je vais vous demander de les tenir toutes les deux, sans en inventer une troisième.

**Première motivation : l'efficacité en échantillons.** Un modèle réduit la dépendance à l'environnement réel, et cette réduction n'exige pas que le modèle soit bon. Même un modèle imparfait diminue le nombre d'échantillons réels nécessaires, parce qu'une grande partie du travail d'essai et d'erreur peut se faire dedans. L'argument historique est celui de la robotique, et il est très concret : un robot coûte cher, il s'use, il casse, le nombre d'échantillons qu'on peut en tirer est borné par la physique et non par la patience, et un robot à nombreux degrés de liberté n'est de toute façon pas à la portée de la plupart des équipes. Quand l'échantillon est la ressource rare, un modèle est le seul moyen d'en fabriquer.

{{% comment %}}SOURCE: LAPAN ch.20 p.602{{% /comment %}}

**Deuxième motivation : la transférabilité entre objectifs.** Un bon modèle d'un bras manipulateur sert à beaucoup d'objectifs différents, sans qu'il faille réapprendre quoi que ce soit depuis le début. C'est une propriété que nos onze semaines n'ont jamais eue : une politique entraînée à poser un objet sur une étagère ne sait rien faire d'autre, et un changement d'objectif demande un nouvel entraînement complet. Un modèle, lui, décrit la **dynamique** du système, et la dynamique ne dépend pas de ce que vous voulez obtenir.

{{% comment %}}SOURCE: LAPAN ch.20 p.602{{% /comment %}}

> [!TIP]
 **Deux motivations, et je vous demande de refuser la troisième.** Vous lirez souvent qu'un modèle rend l'apprentissage « plus intelligent », « plus proche du raisonnement humain » ou « plus interprétable ». Aucune de ces trois affirmations n'est mesurable, et la section 12.6 vous donnera un contre-exemple cinglant à la dernière : nous construirons un modèle dont l'état interne est un vecteur de soixante-quatre nombres que **personne**, ni vous ni la personne qui l'a entraîné, ne peut interpréter comme une position de jeu. Un modèle achète des échantillons et du transfert. Tenez-vous-en là, et vous lirez la suite de la semaine sans vous faire d'illusions.

---

## La frontière entre un environnement et un modèle est plus mince qu'elle n'en a l'air

Voici une remarque qui déplace un peu le sujet, et qui m'importe parce qu'elle évite de traiter le modèle comme un objet exotique.

Depuis la semaine 1, nous travaillons avec des simulateurs physiques, des émulateurs de console, un simulateur de conduite, un pendule inversé sur un chariot. Toutes ces choses **sont déjà des modèles du monde**. Le pendule de la semaine 1 n'est pas un pendule : c'est une équation différentielle intégrée à pas fixe. Un émulateur de console n'est pas une console. Un simulateur physique n'est pas la physique. Nous avons appelé tout cela « l'environnement » pendant onze semaines, et nous avions raison du point de vue de l'agent, puisque c'était bien ce avec quoi il interagissait. Mais du point de vue du monde, c'étaient des modèles.

{{% comment %}}SOURCE: LAPAN ch.20 p.601-602{{% /comment %}}

La leçon pratique est que la question « ai-je un modèle ? » est mal posée. La bonne question est : **puis-je l'interroger comme je veux ?** C'est précisément la contrainte de la section 12.4, et c'est elle qui sépare un simulateur utilisable par une recherche d'un simulateur qui ne l'est pas.

---

## Le prix, annoncé avant la facture

Une dernière chose avant d'entrer dans la méthode, et elle concerne la structure de la semaine.

La première méthode de la semaine suppose un modèle du jeu **donné**, écrit à la main, exact. La seconde l'apprend. La seconde est donc plus générale : elle s'applique là où personne ne peut écrire les règles, et c'est une avancée considérable. Elle se paie, et le prix est connu d'avance : plus de réseaux à entraîner, un entraînement plus long, et des résultats possiblement **moins bons**. La section 12.8 vous montrera ce prix sur une mesure réelle, et il n'y aura rien à embellir.

{{% comment %}}SOURCE: LAPAN ch.20 p.600{{% /comment %}}

---
