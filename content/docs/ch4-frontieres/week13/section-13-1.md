---
title: "13.1 L'interaction est la ressource rare, et trois régimes qui ne se valent pas"
weight: 2
---

## Compter les épisodes plutôt que les pas, et ce que le compte révèle

Prenons un instant pour regarder le prix de ce que nous faisons depuis douze semaines, non pas en heures de calcul mais en **interactions avec le monde**.

Un agent de la semaine 5 sur un jeu vidéo demande des dizaines de millions de pas. Un acteur-critique continu des semaines 8 et 9, sur une tâche de contrôle continu, demande couramment cent mille épisodes. Cent mille épisodes, pour apprendre à faire courir un guépard simulé. Tant que l'environnement est un simulateur qui tourne mille fois plus vite que le temps réel, cela se paie en électricité et personne ne s'en plaint. Dès que l'environnement est un bras robotisé, un patient, un réseau électrique ou un portefeuille, le compte change de nature : chaque épisode coûte du temps réel, de l'usure, de l'argent, ou pire.

C'est la raison d'être de toute cette semaine. **L'interaction est la ressource rare**, et les deux moitiés de la semaine sont deux façons d'en consommer moins : la première remplace l'interaction par du calcul dans un modèle appris, et fait passer un même résultat de cent mille épisodes à quelques centaines ; la seconde remplace l'interaction par un jeu de données que quelqu'un a déjà payé, et la fait passer à zéro.

---

## Trois régimes, et la seule question qui les sépare

Mettons les trois cas côte à côte. La question qui les sépare est unique, et elle tient en deux mots : **qui collecte, et quand ?**

**Régime sur politique.** La politique \(\pi_k\) agit, produit un flot de transitions, s'améliore avec, et jette ses données. À l'itération suivante, c'est \(\pi_{k+1}\) qui collecte, pour elle-même. C'est la semaine 8 et c'est la semaine 10 : chaque gradient est calculé sur des données produites par la politique qu'il modifie, et une donnée vieille d'une itération est déjà inutilisable.

**Régime hors politique à tampon vivant.** Les transitions sont conservées dans un tampon \(\mathcal{D}\) qui contient, à l'itération \(k\), des échantillons produits par \(\pi_0, \pi_1, \dots, \pi_k\). Chaque nouvelle politique **ajoute** au tampon au lieu de le remplacer. C'est la semaine 5, c'est la semaine 6, ce sont les semaines 9 et 11. Le tampon est hétérogène, les données sont vieilles, et c'est acceptable parce que l'agent continue d'en produire de nouvelles qui corrigent ce qu'il croit.

**Régime hors ligne.** Le jeu de données \(\mathcal{D}\) a été collecté par une **politique de comportement** (*behavior policy*) \(\pi_\beta\), que l'on peut très bien ne pas connaître : un opérateur humain, un contrôleur industriel existant, un agent entraîné autrement, ou un mélange de tout cela. Il est collecté **une fois**, il n'est **jamais modifié**, l'entraînement n'interagit **pas du tout** avec le processus de décision, et la politique obtenue n'est déployée qu'une fois complètement entraînée.

{{% comment %}}SOURCE: OFFLINE p.2{{% /comment %}}
{{% comment %}}SOURCE: OFFLINE p.7-8{{% /comment %}}

{{< bookfig src="13-04.png" week="13" >}}

La **Figure 13-4** met les trois régimes côte à côte, et je vous conseille d'y revenir chaque fois qu'un doute de vocabulaire vous arrête dans la seconde moitié de la semaine. Regardez en particulier la flèche de retour, celle qui part de la politique et revient aux données : elle existe dans les deux premiers panneaux et elle est **absente** du troisième. C'est tout, et c'est toute la semaine.

---

## Pourquoi le vocabulaire a dérapé, et comment ce cours le fixe

Il faut dire un mot de l'histoire de ce vocabulaire, parce qu'elle explique la confusion que l'introduction a dû désamorcer.

« Hors politique » est un terme **parapluie**. Il couvre le Q-learning, les acteurs-critiques à valeur d'action, et la plupart des méthodes avec modèle : tous savent, en principe, apprendre sur des données produites par une autre politique. Mais tous, en pratique, **continuent de collecter en ligne**. Le terme ne dit donc rien sur la présence ou l'absence de collecte, et il a fallu lui ajouter un qualificatif, du genre « entièrement hors politique », pour désigner le cas où elle s'arrête.

Un autre nom a circulé pour ce cas, qui parlait de **lots** de données, et il a été abandonné pour une raison que vous apprécierez : le mot « lot » désigne déjà, dans tout l'apprentissage profond, le petit paquet d'exemples sur lequel on calcule un gradient. Appeler « apprentissage par lots » un apprentissage sur un jeu figé obligeait ensuite à préciser à chaque phrase de quel lot on parlait, et à inventer des adjectifs pour distinguer un jeu réellement figé d'un jeu qui grossit. Le terme retenu est donc **hors ligne**, qui dit la bonne chose : non pas « par paquets », mais « sans connexion au monde ».

{{% comment %}}SOURCE: OFFLINE p.8{{% /comment %}}

> [!TIP]
 **Un test en une question, à vous poser chaque fois que vous lisez une description de méthode.** Pendant que cette méthode s'entraîne, est-ce que **de nouvelles transitions entrent** dans ses données ? Si oui, elle est en ligne, qu'elle soit sur politique ou hors politique. Si non, elle est hors ligne, et tout ce que raconte la seconde moitié de cette semaine s'applique à elle. Le test ne porte ni sur l'algorithme, ni sur la perte, ni sur l'architecture : il porte sur une flèche dans un schéma.

---
