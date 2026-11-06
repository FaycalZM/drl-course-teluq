---
title: "10.6 Le compromis mesuré, et ce que le tableau ne dit pas"
weight: 7
---

## Cinq méthodes, quatre configurations, et aucun gagnant

Nous arrivons à la fin du module 3, et je veux le fermer sur une mesure plutôt que sur une préférence. Voici donc, dans un seul tableau, les quatre méthodes de cette semaine et la méthode de référence de la semaine 8, sur les quatre configurations de la section 10.1. Les nombres sont les meilleurs retours de test rapportés, et le gras marque le meilleur résultat de chaque colonne.

**Tableau 10-1.** Meilleur score obtenu par chaque méthode sur chacune des quatre configurations du banc d'essai. Lisez les deux notes sous le tableau avant d'en tirer quoi que ce soit.

| Méthode | Guépard, PyBullet | Guépard, MuJoCo | Fourmi, PyBullet | Fourmi, MuJoCo |
| --- | --- | --- | --- | --- |
| Acteur-critique à avantage (semaine 8) | 2 189 | 4 718 | 2 425 | **5 380** |
| PPO | **2 567** | 1 623 | **2 560** | 5 108 |
| TRPO | 2 419 | 5 753 | 834 | 993 |
| ACKTR | 250 | 3 100 | 1 820 | non rapporté (note 1) |
| Méthode hors politique mesurée (note 2) | 1 765 | **7 063** | 630 | non rapporté (note 1) |

{{% comment %}}SOURCE: LAPAN ch.16 p.520 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.499, p.507, p.511, p.519{{% /comment %}}

La première lecture est celle que les chiffres autorisent, et pas une ligne de plus : **il n'y a pas de méthode gagnante.** Certaines réussissent bien sur certains environnements et obtiennent de moins bons résultats sur d'autres. Les deux seules que l'on puisse qualifier de régulières sont la méthode de référence de la semaine 8 et PPO, qui obtiennent des résultats corrects partout, et la mauvaise colonne de PPO est précisément celle du guépard retourné sur le dos, c'est-à-dire d'un maximum local qu'une autre graine de départ aurait peut-être évité.

{{% comment %}}SOURCE: LAPAN ch.16 p.520 (image){{% /comment %}}

> [!IMPORTANT]
 **Relisez la phrase précédente, parce qu'elle contient un aveu méthodologique considérable.** Le plus mauvais chiffre de la famille sur politique, 1 623, est expliqué par une mauvaise graine de départ, dans la même phrase qui le rapporte comme une mesure. Les deux affirmations sont probablement vraies toutes les deux, et c'est bien le problème : si une exécution unique peut donner 1 623 là où une autre graine donnerait un bon score, alors **aucune** des vingt cases de ce tableau n'est une mesure de la méthode, et toutes sont des mesures du couple méthode plus graine. Ce tableau est le meilleur argument que je puisse vous donner pour l'exigence du jalon 2, reprise au jalon 3 : plusieurs graines, et un intervalle. Vous ne le lirez nulle part plus clairement qu'ici.

---

## Deux cases sans nombre, et ce qu'elles ne veulent pas dire

**Note 1.** Deux cases de ce tableau ne portent pas de nombre, et je veux être très précis sur ce qu'elles signifient, parce que la lecture naturelle est fausse.

Elles ne signifient **pas** que l'expérience n'a pas été faite. Les deux exécutions ont eu lieu. Dans le cas d'ACKTR sur la fourmi sous MuJoCo, l'entraînement a tourné et n'a produit aucune amélioration de récompense, et c'est précisément pour cela qu'aucun meilleur score n'a été rapporté : il n'y avait pas de progrès à rapporter. Dans le cas de la méthode hors politique sur la même configuration, l'entraînement a tourné aussi, et son résultat a été jugé bien plus mauvais que sur le guépard, avec une politique apprise qui parvient tout juste à tenir la fourmi debout.

{{% comment %}}SOURCE: LAPAN ch.16 p.513{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.518-519{{% /comment %}}

> [!TIP]
 **La règle de lecture, et elle vaut pour tous les tableaux que vous lirez après ce cours.** Une case vide dans un tableau de comparaison est une **décision de rapport**, pas une absence de donnée. Trois situations très différentes produisent la même case vide : l'expérience n'a pas été tentée, elle a été tentée et a échoué, ou elle a été tentée et son résultat a été jugé non rapportable. Les trois ont des conséquences opposées sur la conclusion que vous pouvez tirer, et le tableau seul ne vous dit jamais laquelle s'applique : il faut aller lire le texte autour. Quand ce sera vous qui écrirez le tableau, dans le jalon 3, je vous demande de ne jamais laisser une case vide sans une note qui dit laquelle des trois situations elle décrit. C'est une demi-ligne, et c'est ce qui sépare un tableau lisible d'un tableau qui donne une fausse impression de complétude.

---

## Une colonne qui doit être attribuée à ce qui a réellement tourné

**Note 2.** La dernière ligne du tableau ne porte pas de nom de méthode, et c'est une décision que je vous dois en entier, parce qu'elle concerne le meilleur chiffre de tout le tableau.

Cette ligne devrait, si l'on s'en tenait à l'étiquette sous laquelle ses nombres ont été publiés, porter le nom de la méthode de la section 10.5. Mais le code qui a produit ces quatre chiffres n'implémente pas cette méthode, et le texte qui l'accompagne le dit explicitement, à deux endroits. Premier aveu : la variance de la politique n'y est pas paramétrée par l'état, ce qui est le troisième écart de la section 10.1, et l'idée centrale de la régularisation par l'entropie **ne peut pas être mise en œuvre sans une variance paramétrée**. Second aveu, plus direct encore : le code du pas d'acteur ne contient **pas** le terme d'entropie, et il correspond donc à un entraînement de type DDPG. La lecture du code confirme les deux : le terme d'entropie est absent de l'objectif de l'acteur, et celui-ci escalade le **premier** critique au lieu du minimum des deux.

{{% comment %}}SOURCE: LAPAN ch.16 p.515, p.517 (images){{% /comment %}}

Ce qui a donc tourné pour produire ces quatre nombres, c'est un **DDPG hors politique à double Q écrêté dans sa cible, sans aucun terme d'entropie**. C'est une méthode parfaitement respectable, c'est même à peu près la méthode de la section 9.6 privée de deux de ses trois correctifs, mais ce n'est pas la méthode de la section 10.5.

> [!WARNING]
 **La conséquence est simple et elle est sans appel : le chiffre 7 063 n'est pas le résultat de SAC, et ce cours ne vous le présentera jamais comme tel.** Je pourrais faire autrement. Je pourrais recopier le tableau avec son étiquette d'origine, et vous auriez un joli record à retenir. Vous retiendriez un chiffre faux, attribué à la mauvaise méthode, avec ma voix derrière, et vous le citeriez un jour. Les deux seules routes honnêtes sont d'attribuer chaque nombre à **ce qui a réellement tourné**, ou de ne pas le citer du tout. J'ai pris la première, parce que ces quatre nombres gardent une valeur réelle : ils mesurent bien ce qu'une méthode **hors politique à tampon de rejeu** obtient sur ce banc d'essai, et c'est exactement la grandeur dont la fin de cette section a besoin. Si vous cherchez un résultat publié pour la méthode de la section 10.5 elle-même, il en existe ; ce cours ne vous en citera aucun qu'il ne puisse pas attribuer à ce qui a réellement tourné, et il ne va certainement pas l'inventer.

Une précision pour que la leçon porte au-delà du cas. Ce qui rend cette situation instructive n'est pas qu'une erreur ait été commise : c'est qu'elle ait été **signalée par celui-là même qui la commettait**, dans le paragraphe qui précède la section de résultats, et qu'elle ait quand même traversé jusque dans l'étiquette d'un tableau de synthèse. Un aveu placé deux pages avant un tableau ne protège personne. Quand vous rapporterez une mesure obtenue avec une implémentation incomplète, écrivez-le **dans la légende du tableau**, pas dans le corps du texte.

---

## Le compromis qui ferme le module 3

Et maintenant la conclusion du module, qui est une mesure et non une opinion.

Deux chiffres sur l'efficacité en échantillons, d'abord. Sur le guépard, la méthode hors politique de la note 2 atteint un retour de **900 après seulement un demi-million d'observations**. PPO a eu besoin de **plus d'un million** d'observations pour atteindre la même politique. Facteur deux, en faveur du hors politique.

{{% comment %}}SOURCE: LAPAN ch.16 p.517 (image){{% /comment %}}

Deux chiffres sur le coût en calcul, ensuite, et ils vont dans l'autre sens. Parce qu'elle est hors politique, cette méthode fait beaucoup plus de calcul par observation : sur le guépard, **cinq millions de transitions ont demandé dix heures**. Dans le même temps, la méthode de référence de la semaine 8 en traite **cinquante millions**. Facteur dix, en faveur du sur politique. Les exécutions complètes de la méthode hors politique ont pris entre neuf et treize heures pour cinq millions d'observations.

{{% comment %}}SOURCE: LAPAN ch.16 p.517 (image){{% /comment %}}

La **Figure 10-4** met ces quatre nombres côte à côte, parce que le compromis se voit mieux qu'il ne se raconte.

{{< bookfig src="10-04.png" week="10" >}}

> [!IMPORTANT]
 **La règle qui ferme le module 3, et je voudrais que vous la gardiez comme une question à vous poser avant de choisir une méthode.** Si votre environnement est rapide et que les observations sont bon marché, une méthode **sur politique** comme PPO est probablement le meilleur choix : vous avez les échantillons, autant les dépenser plutôt que de payer du calcul pour les économiser. Si vos observations sont difficiles à obtenir, par exemple parce qu'un pas de simulation est lourd, parce qu'un robot réel est au bout de la boucle, ou parce qu'une évaluation humaine est nécessaire, alors une méthode **hors politique** fera un meilleur travail, mais il faudra payer en calcul. La question à se poser n'est donc pas « quelle méthode est la meilleure », elle est **« qu'est-ce qui est rare chez moi, le temps de calcul ou les observations »**. C'est une question d'ingénierie, elle a une réponse différente selon le projet, et c'est tout ce que le module 3 avait à dire de plus fort.

{{% comment %}}SOURCE: LAPAN ch.16 p.517 (image){{% /comment %}}

Une remarque, enfin, sur la raison pour laquelle le compromis survit à la note 2. Le code qui a produit ces mesures n'est pas celui de la section 10.5, mais la **forme** du compromis ne dépend pas de ce détail : moins d'observations et plus de calcul est une propriété de l'apprentissage hors politique avec tampon de rejeu, c'est-à-dire d'une famille entière, et c'est bien ce qui a tourné. Les quatre chiffres sont donc utilisables pour l'argument que je viens de faire, et inutilisables pour attribuer un record à une méthode nommée. Savoir pour quel usage un chiffre vaut quelque chose est, à ce stade du cours, une compétence que je vous demande d'avoir.

---

## Ce que ce tableau démontre sur les graines, en trois lignes

Je ferme la section sur l'exigence du jalon, et le Tableau 10-1 me dispense de l'argumenter.

TRPO obtient 5 753 sur le guépard sous MuJoCo, le meilleur résultat de la famille sur politique, et 993 sur la fourmi sous MuJoCo, un sixième de ce que la méthode de référence obtient. PPO obtient le meilleur score de deux colonnes et le deuxième plus mauvais d'une troisième. ACKTR obtient 250 sur une configuration et 3 100 sur la même tâche dans l'autre simulateur. Et le plus mauvais chiffre de la famille sur politique est, dans le texte même qui le rapporte, attribué à une graine de départ malheureuse.

Voilà vingt cases, cinq méthodes, et pas une seule qui soit accompagnée d'un intervalle. Chacune est une exécution. Je ne reproche rien à personne : chaque exécution de ce tableau coûte entre huit et vingt heures de calcul, et dix graines par case représenteraient plusieurs mois de machine. C'est un arbitrage défendable, et il est explicite. Mais la conséquence est que ce tableau ne permet pas de classer les cinq méthodes, et c'est exactement pourquoi votre jalon 3 mesurera sur une tâche assez petite pour que dix graines tiennent dans une soirée. Le choix de la tâche n'est pas une facilité, c'est **ce qui rend votre conclusion possible**.

---
