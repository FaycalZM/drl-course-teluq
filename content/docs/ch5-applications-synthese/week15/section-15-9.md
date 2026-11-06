---
title: "15.9 Une semaine après la rétroaction humaine"
weight: 10
---

## La même tâche, confiée à un système qui n'a rien appris d'elle

Nous revenons à la tâche de la section 15.3, le jeu textuel, et nous la confions à autre chose.

Le dispositif tient en trois phrases. On donne à un **grand modèle de langue** un énoncé qui contient l'objectif de la quête et la description de la pièce courante, et qui lui demande de répondre par **une commande en minuscules et rien d'autre**. À chaque tour, on lui transmet le résultat de sa commande précédente et la nouvelle description de pièce. Et c'est tout.

**Aucun entraînement d'aucune sorte.** Pas d'affinage, pas de modèle de récompense, pas de gradient : le modèle est employé tel quel. Et deux champs seulement sont demandés à l'environnement : la **description** et l'**objectif**. Pas les **commandes admissibles**.

{{% comment %}}SOURCE: LAPAN ch.13 p.421-424{{% /comment %}}

Relisez cette dernière phrase à la lumière de la section 15.3, parce qu'elle change l'évaluation du tout au tout. L'agent de la section 15.3 a reçu les deux béquilles : la liste d'une douzaine de commandes utiles, et une récompense dense. Celui-ci n'en reçoit **aucune**. Il doit **produire** sa commande dans un espace de \(1250^8\) suites possibles, et il n'a aucun signal de progression.

Un détail d'architecture, et il est le seul : **l'historique de la conversation est la seule mémoire**. L'objectif est montré une fois, au premier tour, et jamais répété. Sans cet historique, le système n'a pas assez d'information pour enchaîner les étapes requises. Autrement dit, la mémoire nécessaire au PDM partiellement observable de la section 15.3 est fournie ici par un mécanisme qui n'a pas été conçu pour cela.

---

## Les chiffres, et ils sont les chiffres d'une évaluation, pas d'un entraînement

**En mode interactif, sur la première graine de jeu.** La quête est résolue en **cinq pas**, par les commandes `go south`, `go east`, `go north`, `open type d locker`, `take keyboard`. Cinq pas pour une quête de longueur cinq : c'est une solution optimale.

{{% comment %}}SOURCE: LAPAN ch.13 p.422-423{{% /comment %}}

**À l'échelle, sur les vingt premières graines.** Vingt jeux, un plafond de vingt pas par jeu, et **neuf jeux résolus sur vingt**. Les échecs se répartissent en quatre catégories, et elles valent d'être nommées parce que trois sur quatre n'ont rien à voir avec du raisonnement : des **boucles**, le système rejouant indéfiniment la même séquence ; des commandes que l'analyseur syntaxique de l'environnement **refuse**, parce qu'elles sont bien formées en anglais mais pas dans la grammaire du jeu ; des culs-de-sac de navigation ; et **deux jeux perdus parce que le système a produit la commande `exit`**, qui termine l'environnement sur-le-champ.

Le coût total : **450 000 jetons** consommés, soit environ **0,20 dollar**.

{{% comment %}}SOURCE: LAPAN ch.13 p.425-426{{% /comment %}}

Mettez maintenant ces deux lignes à côté de celles de l'agent entraîné, que la section 15.6 a déjà données : quatorze heures d'entraînement, huit mille épisodes, et une récompense de validation nulle sur des jeux non vus.

---

## La lecture honnête, et c'est le cours qui doit la fournir

Voici le moment où cette section pourrait devenir un tour d'honneur, et où elle ne le sera pas. Je vous dois quatre réserves, et aucune des quatre n'annule le résultat.

> [!WARNING]
 **Quatre choses que ce résultat ne montre pas, et il faut les dire avant de dire ce qu'il montre.**
>
> **Un : neuf sur vingt n'est pas « résolu ».** C'est un peu moins qu'une pièce lancée en l'air, sur une quête de **cinq coups**. Un agent qui réussit une fois sur deux une tâche de cinq actions n'a pas démontré de compétence générale sur la tâche ; il a démontré qu'il la réussit parfois.
>
> **Deux : « aucun entraînement sur cette tâche » n'est pas « aucun entraînement ».** Le modèle n'a pas vu ces jeux, et il a été entraîné sur un corpus de texte dont il est hautement probable qu'il contienne de la fiction interactive : des parties, des solutions, des guides, des discussions. On ne mesure donc pas un raisonnement à partir de rien ; on mesure un transfert depuis un corpus dont on ne connaît pas le contenu. C'est une mesure utile, et ce n'est pas celle que le mot « aucun entraînement » suggère.
>
> **Trois : rien ici ne compare du raisonnement à de l'apprentissage.** Les deux systèmes n'ont pas reçu la même chose, n'ont pas eu accès aux mêmes champs de l'environnement, et n'ont pas été évalués sur le même protocole. Le seul énoncé solide est une comparaison de **métrique finale sur vingt jeux**, et il n'autorise aucune conclusion sur les mécanismes.
>
> **Quatre : la comparaison de coûts n'est pas à grandeurs égales.** Vingt centimes d'interface facturée contre des heures de processeur graphique, c'est vrai. Mais l'agent entraîné, une fois entraîné, **tourne hors ligne indéfiniment et gratuitement**, alors que chaque partie jouée par le modèle de langue se paie de nouveau. À dix mille parties, l'arithmétique s'inverse. Un coût unitaire et un coût d'investissement ne se comparent pas sans dire combien de fois on va s'en servir.

Et maintenant ce que ce résultat montre, qui est suffisant et qui est le vrai sujet de cette semaine.

Sur un problème dont **l'observation est une langue naturelle** et dont **l'action est une phrase de langue naturelle**, quatorze semaines d'apprentissage par renforcement ont été battues sur la métrique finale par un système qui ne fait aucun apprentissage par renforcement, sur une version **plus difficile** de la tâche, pour un coût de vingt centimes. Et la tâche est plus difficile en un sens précis et vérifiable : le système **produit** ses commandes au lieu de les choisir dans une liste d'une douzaine.

{{% comment %}}SOURCE: LAPAN ch.13 p.423{{% /comment %}}

> [!IMPORTANT]
 **La conclusion que j'en tire, et c'est la question de la section 15.1 remise à l'endroit.** Ce résultat ne dit pas que l'apprentissage par renforcement est dépassé ; il dit que **la première question à poser devant un problème n'est pas « quelle méthode », c'est « de quelle nature sont mon observation et mon action »**. Quand les deux sont de la langue naturelle, il existe depuis peu une famille de systèmes qui a déjà payé le coût de la représentation, et ne pas la considérer serait une faute professionnelle. Quand l'action est un couple de couples moteurs, quand l'observation est une image de caméra de profondeur, quand la récompense doit être optimisée sur dix millions de pas, cette famille n'offre rien et les quatorze semaines précédentes offrent tout. **La bonne question n'est donc pas « les modèles de langue remplacent-ils l'apprentissage par renforcement », c'est « lesquels de mes problèmes sont des problèmes de langue ».** Posez-la en premier, parce que la réponse décide du reste.

Et pour relier cette section à la précédente : la même idée est en train d'être essayée sur la navigation web, en demandant à un modèle de langue de **produire le script d'automatisation** correspondant à une tâche décrite en français plutôt que d'apprendre à cliquer. C'est le même déplacement : on ne change pas d'algorithme, on change la nature de l'objet que le système produit.

{{% comment %}}SOURCE: LAPAN ch.14 p.458{{% /comment %}}

---
