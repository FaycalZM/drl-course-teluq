---
title: "15.2 Un marché"
weight: 3
---

## Trois actions, et un signal plus petit que ses frais

Commençons par le problème que vous connaissez déjà, parce que c'est le plus instructif des quatre pour une raison inattendue : c'est celui où l'agent fonctionne le moins bien, et où l'on sait exactement pourquoi.

La semaine 7 a construit cet agent. Je ne le reconstruis pas ici : je le relis avec les trois questions, et je vous invite à faire de même avec le vôtre.

**L'observation** est un vecteur. Les \(N\) dernières barres de prix, dix par défaut, un indicateur binaire disant si une position est détenue, et le profit relatif courant si elle l'est. Le détail qui compte, et qui est le seul morceau d'ingénierie de représentation de tout le problème : le haut, le bas et la clôture de chaque barre ne sont pas donnés en prix absolus mais en **pourcentages de l'ouverture** de cette même barre. Un prix absolu de 1 148,90 n'apprend rien à un réseau ; un écart de 0,3 % par rapport à l'ouverture apprend quelque chose, et surtout cette quantité est **comparable** d'une barre à l'autre et d'un titre à l'autre.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

**L'action** compte trois valeurs : ne rien faire, acheter, clôturer. C'est la plus petite des quatre colonnes de la semaine, et il faut voir ce qui a été retiré pour arriver là. Pas de vente à découvert, donc l'agent ne peut pas gagner sur une baisse. Pas de positions multiples, donc pas de dimensionnement : on est dedans ou dehors. Pas de taille d'ordre, donc pas de gestion du risque. Chacune de ces trois absences est une simplification volontaire, et chacune serait une extension sérieuse.

**La récompense** est le point intéressant, parce qu'il y en a **deux**, et que le choix entre les deux est un vrai choix de conception. Premier schéma : à chaque pas où une position est détenue, la récompense est le mouvement de la barre courante. Second schéma : rien du tout pendant la détention, puis l'intégralité du mouvement au moment de clôturer. Le premier schéma est dense et facile à apprendre ; le second est parcimonieux et correspond mieux à ce qu'un opérateur appelle un gain. Et dans les deux cas, l'unité est le **point de pourcentage**, avec une commission de 0,1 % prélevée à l'achat et à la clôture.

{{% comment %}}SOURCE: LAPAN ch.10 p.306, p.314{{% /comment %}}

---

## Le chiffre qui explique le résultat, et il tient en une soustraction

Mettez maintenant les deux derniers chiffres côte à côte, et vous aurez la difficulté de ce problème en une ligne.

Un aller-retour coûte **0,2 %**, puisque la commission se paie deux fois. Le mouvement typique d'une barre d'une minute sur un titre liquide est d'un ordre de grandeur comparable ou inférieur. Autrement dit : **le signal que l'agent doit extraire est plus petit que le prix d'y accéder.** Ce n'est pas une difficulté d'optimisation, c'est une propriété du problème, et aucune architecture ne la supprime.

Le résultat mesuré est à l'avenant, et je vous le donne tel quel parce qu'il est utile. Sur les données de validation, l'agent reste au-dessus de \(-0{,}2\) % pendant environ **quatre heures de marché**, puis décroche. Quatre heures, ce n'est pas rien et ce n'est pas une réussite : c'est la durée pendant laquelle un agent entraîné sur un régime de marché reste pertinent dans un autre.

{{% comment %}}SOURCE: LAPAN ch.10 p.322-323{{% /comment %}}

---

## La décision qui coûte le plus cher sur ce problème, et elle n'est pas dans le réseau

Il reste la décision la plus importante de cette application, et elle n'est ni dans l'observation, ni dans l'action, ni dans la récompense. Elle est dans le **protocole**.

La règle du cours a été posée en semaine 7 et elle n'a pas d'exception : une série indexée par le temps se partage dans l'**ordre chronologique**, on ajuste sur la période la plus ancienne et on valide sur la plus récente. Avec deux années de données, on entraîne sur la première et on valide sur la seconde. Rien d'autre.

{{% comment %}}SOURCE: source-assets/raw-content/week-07.md §7.6{{% /comment %}}

Je rappelle les trois conséquences d'un partage pris à l'envers, parce que cette semaine est celle où vous allez relire des résultats produits par d'autres et où vous devrez repérer ce défaut sans aide. **Un :** on répond à la mauvaise question, puisqu'on demande si un modèle qui a vu le futur explique le passé, ce qu'aucun praticien ne pourra jamais demander. **Deux :** la fuite d'information ne passe pas par les tenseurs mais par **vous**, par chaque décision prise en regardant la période réservée, et aucune relecture de code ne la détectera parce qu'il n'y a pas de bogue. **Trois :** c'est indétectable dans les métriques, puisqu'un partage inversé produit des courbes parfaitement ordinaires.

> [!WARNING]
 **Et voici pourquoi cette section ouvre la semaine plutôt que de la clore.** Les trois questions de la section 15.1 vous donnent la forme du problème. Elles ne vous donnent pas le **protocole**, et c'est le protocole qui décide si votre mesure veut dire quelque chose. Sur les quatre applications de cette semaine, trois ont un protocole de mesure discutable, et la section 15.7 en montrera deux où le défaut de protocole rend le résultat inutilisable. Posez les trois questions, puis posez la quatrième : **comment saurai-je que cela a fonctionné, et cette façon de le savoir est-elle écrite avant l'exécution ?**

---
