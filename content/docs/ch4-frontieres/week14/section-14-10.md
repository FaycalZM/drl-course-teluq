---
title: "14.10 Six mécanismes, et aucun n'est une faute d'inattention"
weight: 11
---

## Pourquoi une taxonomie des causes plutôt qu'une liste de maladresses

Avant les six mécanismes, un mot sur la raison d'être de la liste, parce que c'est elle qui lui donne sa valeur.

Devant chaque exemple de piratage de récompense, il est tentant de conclure que quelqu'un a mal fait son travail : la personne qui a écrit l'objectif aurait dû penser au vase, à la jauge d'oxygène, au fait qu'un robot peut fermer les yeux. Cette lecture est confortable et stérile, parce qu'elle ne permet de prédire aucun cas futur : elle dit seulement qu'il faudra être plus attentif, ce qui n'est pas une méthode.

L'approche de cette section est l'inverse, et c'est elle que ce cours adopte : traiter les objectifs mal spécifiés comme **émergeant de causes générales**, c'est-à-dire de propriétés structurelles de la situation plutôt que de défaillances individuelles. Si ces causes sont identifiables, elles sont vérifiables à l'avance, sur un cahier, avant d'avoir écrit la moindre ligne.

{{% comment %}}SOURCE: AMODEI p.9{{% /comment %}}

---

## Les six, un par un

**Mécanisme 1. Buts partiellement observés.** La tâche réelle porte sur un état du monde extérieur, mais l'agent ne confirme cet état qu'à travers une perception imparfaite. La récompense ne peut alors porter que sur la perception, et optimiser la perception n'est pas optimiser le monde. Le robot dont la récompense compte **les saletés qu'il voit** se pirate en fermant les yeux. Il existe une réponse formelle, qui consiste à reformuler le problème sur l'espace des croyances plutôt que sur celui des états, et cette réponse existe toujours en principe : elle est d'un coût prohibitif en pratique.

**Mécanisme 2. Systèmes compliqués.** La probabilité qu'une stratégie de piratage soit disponible croît avec la complexité de l'agent, comme la probabilité qu'un programme contienne un bogue croît avec sa taille. L'exemple canonique est frappant : il est possible, à partir de l'intérieur d'un vieux jeu de plateforme, d'exécuter du code arbitraire, simplement en exploitant les effets de bord de la machine qui fait tourner le jeu. Un agent suffisamment capable peut donc sortir du cadre que son concepteur croyait fermé.

**Mécanisme 3. Récompenses abstraites.** Dès que la récompense porte sur un concept qui ne se lit pas directement dans l'état, il faut l'**apprendre**, et une fonction apprise sur un espace de grande dimension hérite des faiblesses de toutes les fonctions apprises : elle peut avoir des valeurs anormalement élevées le long d'au moins une direction, et un optimiseur trouvera cette direction. C'est le mécanisme qui parle de notre propre modèle de récompense, et j'y reviens dans un instant.

**Mécanisme 4. La loi de Goodhart.** Une mesure corrélée à ce qui nous intéresse en conditions ordinaires **cesse de l'être quand on l'optimise fortement**. L'énoncé classique tient en une phrase : dès qu'une mesure devient une cible, elle cesse d'être une bonne mesure. L'exemple est celui du robot évalué sur la quantité d'eau de Javel consommée, parce que les bureaux propres en consomment : le robot la verse dans l'évier. Notez bien ce que ce mécanisme dit, car c'est la clé de la section 14.13 : la corrélation **était réelle**, et elle a été détruite par l'acte même de l'optimiser.

**Mécanisme 5. Boucles de rétroaction.** Un terme de l'objectif se renforce lui-même. L'exemple est une annonce affichée dans une police plus grande parce qu'elle est populaire, ce qui la rend plus populaire, ce qui augmente sa police. Rien dans ce circuit ne mesure ce qui nous intéressait au départ ; le circuit mesure sa propre sortie.

**Mécanisme 6. Ancrage de la récompense dans l'environnement, ou auto-récompense** (*wireheading*). La récompense n'est pas une abstraction : elle est **calculée quelque part**, par un programme, sur une machine. Un agent assez large pour agir sur cette machine peut agir sur le calcul lui-même, et obtenir sa récompense sans faire la tâche. Et le cas le plus préoccupant est celui où **une personne se trouve dans la boucle de récompense**, parce qu'une personne est aussi une partie de l'environnement.

{{% comment %}}SOURCE: AMODEI p.8-9{{% /comment %}}

> [!NOTE]
 **Un choix de traduction que ce cours assume, et je le signale parce qu'il n'est pas évident.** Le sixième mécanisme n'a pas de nom français attesté. Les descriptions qui en circulent sont des phrases plutôt que des termes, par exemple « manipulation par l'agent de sa propre récompense », et une phrase ne se met pas dans un tableau ni dans un index. Ce cours retient donc « **auto-récompense** », avec une glose à sa première occurrence, et place la phrase longue en explication plutôt qu'en terme. Si vous rencontrez le mot anglais ailleurs, c'est de ceci qu'il s'agit.

---

## Celui qui parle directement de notre propre modèle de récompense

Je veux revenir sur le mécanisme 3, parce qu'il décrit l'objet que nous avons construit en section 14.6, et qu'il le décrit avec une précision presque gênante.

Notre \(\hat r\) est une fonction **apprise**. Son espace d'entrée est une image de 210 sur 160 en trois canaux, plus une action : plus de cent mille dimensions. Elle a été ajustée sur trois cents comparaisons. Et nous l'avons ensuite placée sous un optimiseur dont le travail, pendant deux millions de pas, consiste à en chercher le maximum.

Le mécanisme 3 dit ceci : une récompense apprise sur un espace de grande dimension est vulnérable au piratage **s'il existe au moins une direction où elle prend des valeurs pathologiquement élevées**. Il ne dit pas qu'une telle direction existe nécessairement ; il dit que rien ne l'exclut, et que trois cents exemples ne suffisent certainement pas à l'exclure.

{{% comment %}}SOURCE: AMODEI p.8-9{{% /comment %}}

Et c'est bien ce que nous avons observé. La surface était une région où notre modèle prédisait des valeurs élevées, parce que la personne y avait mis toutes ses préférences positives, et rien dans les données n'indiquait que **rester** à la surface indéfiniment était différent d'**y remonter**. L'optimiseur a trouvé cette région et s'y est installé.

> [!TIP]
 **Le réflexe à emporter, et il se formule en une question.** Chaque fois que vous optimiserez contre une quantité apprise, posez-vous celle-ci : **sur quelle région de l'espace cette quantité a-t-elle été ajustée, et mon optimiseur est-il contraint de rester dans cette région ?** Si la réponse à la seconde partie est non, vous êtes dans la situation de la section 14.7 et de la semaine 13 : l'optimiseur va chercher les erreurs de l'estimateur, et il les trouvera, parce que c'est exactement son travail. La garde classique est une contrainte de divergence contre une politique de référence, et son absence dans la chaîne de la première moitié n'était pas un détail.

---
