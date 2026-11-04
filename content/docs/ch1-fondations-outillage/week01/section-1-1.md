---
title: "1.1 L'apprentissage par renforcement, troisième paradigme"
weight: 2
---

## Trois façons d'apprendre, et une seule qui agit

Replaçons d'abord notre discipline sur la carte. L'**apprentissage supervisé** dispose d'étiquettes : une image marquée « chat », une transaction marquée « frauduleuse », et il généralise la correspondance. L'**apprentissage non supervisé** n'en a aucune ; son objectif est de faire émerger une structure cachée, par partitionnement en grappes ou, de façon plus spectaculaire, avec deux réseaux qui s'affrontent : l'un produit des contrefaçons, l'autre tente de les démasquer. L'**apprentissage par renforcement** (*reinforcement learning*) est le troisième camp et se situe entre les deux : ni supervision complète, ni absence totale de signal. Personne ne dit à notre agent quelle action était la bonne, mais l'environnement lui renvoie de temps à autre un nombre. Ce nombre n'est pas une étiquette (il ne désigne pas la bonne réponse) et il n'est pas rien non plus.

{{% comment %}}SOURCE: LAPAN ch.1 p.35-36{{% /comment %}}

> [!NOTE]
 **Notez bien cette intuition :** notre discipline emprunte à l'apprentissage supervisé l'essentiel de sa machinerie (réseaux profonds, descente de gradient stochastique, rétropropagation), mais elle en fait un **usage** radicalement différent. Voilà pourquoi la semaine 2, consacrée à PyTorch, n'est pas un détour.

## Les trois difficultés propres à l'apprentissage par renforcement

Trois difficultés lui sont spécifiques, et je veux que vous les connaissiez **maintenant** : chacune reviendra plus loin sous la forme d'un algorithme précis.

**Les observations ne sont pas i.i.d.** La plupart des méthodes supervisées exigent des données indépendantes et identiquement distribuées ; c'est une hypothèse de travail, pas un détail. Or les observations de notre agent dépendent de son propre comportement : un agent entêté ne récolte que ce que sa routine produit, et ces observations lui donnent la fausse impression qu'il n'existe aucun moyen d'obtenir une récompense plus grande. La boucle se referme sur elle-même, et c'est exactement ce que le rejeu d'expérience viendra casser en semaine 5.

**Le dilemme exploration-exploitation.** Faut-il retourner au restaurant que vous aimez ou essayer celui qui vient d'ouvrir ? Rester dans votre poste ou accepter l'offre qu'on vous fait ? Ces analogies *sont* le problème. Trop d'exploitation, et l'agent reste enfermé dans une stratégie médiocre ; trop d'exploration, et la récompense s'effondre, l'agent pouvant même **oublier** ce qu'il avait appris. C'est l'une des questions fondamentales encore ouvertes du domaine ; nous y reviendrons en semaine 4, puis en semaine 11 avec de l'artillerie lourde.

**La récompense est différée.** Aux échecs, un seul coup fort au milieu de la partie peut faire basculer l'équilibre, et la récompense n'arrive qu'à la fin. L'agent doit **découvrir** cette causalité, qui n'est écrite nulle part. Ce problème porte un nom, l'attribution du mérite, et c'est le cœur de la semaine 8.

{{% comment %}}SOURCE: LAPAN ch.1 p.37-38{{% /comment %}}

Si la terminologie du domaine vous paraît hétérogène, c'est qu'elle l'est : l'apprentissage par renforcement se tient à l'intersection de six traditions qui ont travaillé les mêmes objets sous d'autres noms. Ce sont l'apprentissage automatique, l'ingénierie et la commande optimale, les neurosciences, la psychologie, l'économie, les mathématiques et la recherche opérationnelle. Quand vous lirez « *cost-to-go* » dans un article de commande optimale, demandez-vous s'il ne s'agit pas de notre valeur d'état.

{{% comment %}}SOURCE: LAPAN ch.1 p.44{{% /comment %}}
