---
title: "6.11 Elles se composent"
weight: 12
---

## Quatre réparations empilées, et ce que l'empilement coûte

Les cinq réparations sont sur la table. Posons maintenant la question que toute cette semaine préparait : que se passe-t-il si on les active **toutes en même temps** ?

La réponse est connue, elle est publiée, et elle est le résultat le plus cité de cette famille de méthodes. En 2017, une étude a combiné les six améliorations les plus importantes du réseau Q profond, sans en inventer aucune, et a mesuré ce que la combinaison donnait. Elle a atteint l'état de l'art sur la suite Atari. Le nom de l'agent obtenu est Rainbow, et je veux que vous reteniez précisément **ce qu'il est** : non pas un nouvel algorithme, mais un réseau Q profond auquel on a appliqué six corrections indépendantes.

{{% comment %}}SOURCE: LAPAN ch.8 p.226, p.279{{% /comment %}}

Voici comment elles s'empilent concrètement, et c'est l'enseignement de la section. Les chemins de l'architecture duale ne produisent plus des nombres mais des **distributions**, avec la soustraction de la moyenne des avantages appliquée dans chaque atome de la distribution. Les couches linéaires des deux chemins sont remplacées par des couches bruitées. Le tampon priorisé est placé dessous. Et l'équation de Bellman est dépliée sur \(n\) pas.

{{% comment %}}SOURCE: LAPAN ch.8 p.280{{% /comment %}}

Relisez cette énumération en regardant **où** chaque réparation intervient, parce que c'est la raison pour laquelle elles s'empilent au lieu de se gêner.

| La réparation | Ce qu'elle touche | Ce qu'elle laisse intact |
| --- | --- | --- |
| architecture duale | la **structure** du réseau | la perte, le tampon, la cible |
| réseaux bruités | les **couches** du réseau | la structure, la perte, le tampon |
| tampon priorisé | l'**échantillonnage** | le réseau et la forme de la cible |
| DQN à n étapes | la **cible** | le réseau et l'échantillonnage |
| double DQN | la **cible**, elle aussi | le réseau et l'échantillonnage |

Quatre points d'intervention distincts pour cinq réparations, et une seule collision : le double DQN et le dépliage modifient tous les deux la cible, et c'est d'ailleurs le couple dont on parle le moins. La composabilité n'est donc pas un miracle, c'est une conséquence du fait que ces méthodes réparent des défauts situés à des endroits différents du même programme. Retenez ce critère, il vous servira à lire bien d'autres combinaisons : deux améliorations qui touchent la même pièce ne se composent pas gratuitement.

Et maintenant l'honnêteté, parce que cette semaine en a besoin. La combinaison étudiée dans notre programme ne retient **que quatre** des réparations : le dépliage, l'architecture duale, les réseaux bruités et le tampon priorisé. Les deux autres, le double DQN et la version distributionnelle de la section 6.12, sont **écartées**, parce qu'elles n'apportaient pas grand-chose sur l'environnement d'essai utilisé. Nous avons donc passé une semaine à étudier cinq réparations, et le système combiné en embarque quatre.

{{% comment %}}SOURCE: LAPAN ch.8 p.280{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que c'est la leçon de méthode de la semaine entière.** Une réparation qui est correcte sur le plan théorique et mesurable sur un diagnostic peut n'apporter aucun gain sur un problème donné. Le double DQN réduit la surestimation, la Figure 6-3 le montre, et il n'accélère pas l'entraînement sur ce jeu-là. Ce n'est contradictoire qu'en apparence : la surestimation ne nuit au retour que si elle change l'**ordre** des valeurs d'action, et une surestimation à peu près uniforme ne change pas l'argument du maximum. Voilà ce que je veux que vous emportiez : on n'empile pas des améliorations parce qu'elles sont publiées, on les empile après avoir mesuré celles qui servent sur **son** problème. C'est le sens du laboratoire de cette semaine, et c'est le sens du jalon 2.

Les chiffres de la combinaison, pour finir, et ils sont spectaculaires. Après une centaine de parties seulement, l'agent combiné gagnait presque toutes les manches ; il a fallu une centaine de parties de plus pour que la moyenne lissée atteigne le seuil de 18. Après réglage des hyperparamètres, le score maximal est atteint juste après **40 parties**. Comparez avec les 400 parties de la référence.

{{% comment %}}SOURCE: LAPAN ch.8 p.281-282{{% /comment %}}

Et le prix, qui est maintenant un réflexe de lecture pour vous : le système combiné est **plus lent**. Il démarre à 170 trames par seconde et se dégrade jusqu'à 130, à cause de la complexité en \(O(N)\) du tampon priorisé. Troisième fois cette semaine qu'il faut demander « plus rapide en quoi ? », et troisième réponse différente.

{{% comment %}}SOURCE: LAPAN ch.8 p.281{{% /comment %}}

Une dernière réserve, et elle est importante pour la suite du cours. La liste des six améliorations est loin d'être complète, et elle est nettement orientée vers les travaux d'un seul laboratoire de recherche. Il ne faut donc pas la lire comme un inventaire des choses qu'on sait faire, mais comme un ensemble cohérent et bien mesuré de six idées qui ont fait leurs preuves ensemble. D'autres existent, et la semaine 11 en apportera une qui n'est pas dans cette liste.

{{% comment %}}SOURCE: LAPAN ch.8 p.283{{% /comment %}}

---
