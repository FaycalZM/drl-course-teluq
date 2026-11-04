---
title: "1.2 Les cinq entités : agent, environnement, action, récompense, observation"
weight: 3
---

## Deux boîtes, trois flèches, et un tuyau très étroit

Je vais être lente et précise ici : ces cinq mots reviendront chacune des quatorze semaines suivantes, et le dernier cache une subtilité que beaucoup d'étudiants ne remarquent qu'au moment où leur agent refuse d'apprendre.

Le schéma canonique de toute la discipline tient en deux boîtes et trois flèches, et c'est ce que montre la **Figure 1-1** : deux entités, l'**agent** (*agent*) et l'**environnement** (*environment*), et trois canaux de communication entre elles. Les actions descendent vers l'environnement, les récompenses et les observations remontent vers l'agent.

{{< bookfig src="01-01.png" week="01" >}}

{{% comment %}}SOURCE: LAPAN ch.1 p.38, fig.1.2{{% /comment %}}

Trois canaux, pas quatre : l'agent ne reçoit ni le plan du labyrinthe, ni les probabilités de transition, ni la fonction de récompense. Tout l'édifice du cours existe parce que ce tuyau est étroit.

---

## La récompense

La **récompense** (*reward*) est une valeur scalaire que l'environnement nous remet périodiquement : un seul nombre, pas un rapport détaillé. Le mot important est « périodiquement », car **la fréquence n'est pas imposée**, d'une récompense à chaque seconde à une seule récompense dans toute l'existence de l'agent. Ce second cas n'est pas théorique : dans un système à récompense terminale unique, toutes les récompenses sauf la dernière valent zéro, et c'est le régime normal des jeux de plateau. Le terme « renforcement » vient de là : la récompense **renforce** le comportement, positivement ou négativement. Mais elle est **locale**, car une grosse récompense maintenant n'interdit rien pour la suite : c'est un peu comme braquer une banque. Ce que l'agent maximise, c'est la récompense **accumulée**, à laquelle la section 1.4 donnera un nom et une formule.

{{% comment %}}SOURCE: LAPAN ch.1 p.39{{% /comment %}}

> [!WARNING]
 **Attention : erreur fréquente ici !** Dans un jeu d'arcade, le score affiché est **déjà** une quantité accumulée : donné tel quel, il annonce à l'agent « tu viens de gagner 4 000 points » alors qu'il a seulement survécu un pas de plus. La récompense correcte est la **dérivée** de ce score : +1 par ennemi détruit, −N à la mort du joueur, 0 le reste du temps.

{{% comment %}}SOURCE: LAPAN ch.1 p.39{{% /comment %}}

Gardez sous la main huit situations et, pour chacune, demandez-vous qui est l'agent, quelle est la récompense et ce que l'on voit exactement : courtage financier, échecs, système dopaminergique du cerveau, jeux vidéo, navigation web, recherche d'architecture de réseau, dressage d'un chien, notes scolaires.

{{% comment %}}SOURCE: LAPAN ch.1 p.39-40{{% /comment %}}

---

## L'agent, l'environnement, les actions

Un **agent** est quelqu'un ou quelque chose qui interagit avec l'environnement en exécutant des actions, en faisant des observations et en recevant d'éventuelles récompenses ; dans notre pratique, ce sera toujours « un morceau de code qui met en œuvre une politique ». L'**environnement** se définit par exclusion : **tout ce qui est extérieur à l'agent**. Pris au pied de la lettre cela désigne le reste de l'univers, ce qui est manifestement excessif ; en pratique nous découpons, et ce découpage est une décision de conception qui vous appartiendra au moment de définir votre projet.

Une **action** est ce que l'agent peut faire, et il n'existe que deux familles. Les actions **discrètes** forment un ensemble fini de possibilités mutuellement exclusives : gauche *ou* droite. Les actions **continues** portent une valeur attachée : un angle de braquage, une pression sur une pédale. L'argument qui les sépare suffit : « tourner le volant » ne dit rien du tout, il faut dire de combien de degrés et dans quel sens. Cette distinction structure le plan du cours : les semaines 4 à 8 traitent les espaces discrets, la semaine 9 est consacrée aux espaces continus.

{{% comment %}}SOURCE: LAPAN ch.1 p.40-41{{% /comment %}}

---

## État et observation : la distinction sur laquelle tout repose

L'**état** (*state*) de l'environnement est **interne** : il inclut potentiellement chaque atome de l'univers et, même borné raisonnablement, reste en général impossible à mesurer entièrement, les mesures disponibles étant de surcroît bruitées. L'**observation** (*observation*) est ce que l'environnement accepte de montrer. Les deux ne coïncident presque jamais, et ce n'est pas une faiblesse de notre cadre : l'apprentissage par renforcement a été conçu pour traiter ce cas **nativement**.

Trois exemples, en ordre croissant de brutalité. **Courtage financier** : l'état est le marché tout entier, chaque ordre, chaque dépêche, la politique, la météo ; votre observation, des prix et quelques nouvelles. **Échecs** : on croit que la position *est* l'état, mais l'état inclut le niveau réel de l'adversaire, son humeur, sa connaissance de vos habitudes, son plan tactique. **Jeu vidéo** : l'état est l'intégralité de la mémoire et du disque de la machine ; votre observation, l'écran et le son. Et le nombre d'images possibles en 1024 × 768, qui dépasse le nombre d'atomes de notre galaxie, reste malgré tout **plus petit** que le nombre d'états de la machine.

> [!IMPORTANT]
 **Je dois insister :** notre agent n'agit jamais sur la base de l'état, il agit sur la base de l'observation. Et toute la littérature, ce cours inclus, écrit souvent « état » là où il faudrait dire « observation ». En semaine 7, quand une seule image d'écran ne suffira plus et qu'il faudra en empiler quatre, vous verrez que la distinction est pratique et non philosophique.

Un dernier point à planter : une observation peut être pertinente ou non pour la récompense à venir, et elle peut contenir l'information utile sous une forme **dissimulée** : les points du score sont là, dans un jeu, mais sous forme de pixels qu'il faudra apprendre à lire.

{{% comment %}}SOURCE: LAPAN ch.1 p.42-43{{% /comment %}}
