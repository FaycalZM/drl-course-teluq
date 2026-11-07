---
title: "Livrables finaux : rapport, présentation et dépôt"
weight: 14
---

## Ce qui est demandé, et ce sur quoi vous êtes évalué

Voici le dernier travail du cours, et il porte sur **l'ensemble de votre trajectoire** plutôt que sur une semaine. Trois pièces.

**Un rapport de huit à dix pages.** Il raconte votre projet d'un bout à l'autre : l'environnement choisi au jalon 1, la référence du jalon 1, le réseau Q profond et ses extensions du jalon 2, la méthode de politique du jalon 3, l'extension avancée du jalon 4, et ce que la comparaison des quatre a établi. Huit à dix pages, c'est court : vous allez devoir choisir, et le choix est une partie de l'évaluation.

**Une présentation de dix minutes.** Dix minutes, c'est environ huit diapositives et une démonstration. Elle n'est pas un résumé du rapport : elle répond à une question, celle de savoir ce que votre agent fait et pourquoi vous avez choisi cette route.

**Un dépôt complet.** Le code, les configurations, les journaux, et ce qu'il faut pour que quelqu'un d'autre reproduise au moins une de vos figures.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---

## Le critère unique, et cette semaine vient de le démontrer

Les quatre jalons ont chacun eu son critère propre : la qualité de l'analyse des limites, la performance relative et la stabilité, la convergence et l'efficacité d'échantillonnage, l'originalité et la profondeur. Le livrable final en ajoute un, et c'est celui sur lequel je serai le plus strict.

> [!IMPORTANT]
 **Le critère est : quelqu'un d'autre peut l'exécuter.** Pas « le code est propre », pas « les résultats sont bons » : quelqu'un d'autre, qui ne vous connaît pas, muni de votre dépôt et de votre rapport, obtient quelque chose de comparable à ce que vous rapportez, ou sait exactement pourquoi il ne l'obtient pas. C'est tout, et c'est beaucoup.

Et je veux que vous voyiez que ce critère n'est pas une préférence de ma part : **cette semaine vient de le démontrer deux fois**.

La section 15.7 a montré une méthode publiée dont la reproduction a échoué, et la première raison de l'échec n'était pas une difficulté scientifique : c'était **l'absence des hyperparamètres dans la publication**. Deux pages de configuration auraient changé l'issue. La même section a montré une expérience rapportée deux fois avec des chiffres incompatibles, parce que **le nombre n'avait pas été enregistré** au moment où il avait été obtenu. Dans les deux cas, le travail scientifique était sérieux et le défaut était gratuit.

C'est pour cela que la reproductibilité est le critère du dernier livrable. Non pas parce que c'est une vertu administrative, mais parce que c'est la seule propriété de votre travail qui décide si quelqu'un peut s'en servir.

---

## La liste de vérification, et je l'écris pour que vous puissiez la cocher

Voici concrètement ce que je vérifierai, point par point. Rien ici ne demande de travail supplémentaire si vous l'avez fait au fur et à mesure, et beaucoup si vous ne l'avez pas fait.

**Dans le dépôt.** Les versions épinglées de Python et des paquets, dans la première cellule de chaque carnet. Un fichier de configuration par expérience rapportée, et pas de valeur d'hyperparamètre écrite en dur dans le corps du code. Les **graines** employées, listées, et pas « plusieurs graines ». Les journaux d'exécution, bruts, non édités. Et une commande, une seule, qui reproduit une figure du rapport à partir de ces journaux.

**Dans le rapport.** Chaque nombre qui apparaît dans une phrase est traçable jusqu'à une ligne de journal. Chaque comparaison porte un **intervalle de confiance** et un nombre de graines. Chaque mesure est accompagnée de son **matériel** et de sa **durée**. Le **critère d'arrêt** est énoncé, et il a été fixé avant l'exécution. Et les unités de tout ce que vous comparez sont écrites explicitement, parce que la section 15.8 vient de montrer ce qu'il advient quand elles ne le sont pas.

**Et deux choses que je demande en plus, propres à cette semaine.** La première : une **cinquième colonne** de la Figure 15-1 pour votre propre problème, c'est-à-dire ce qu'est une observation, ce qu'est une action et quand arrive une récompense dans votre projet, sur une demi-page. La seconde : **trois numéros de semaine** et une phrase disant pourquoi les onze autres ne s'appliquent pas, comme la section 15.10 l'a fait sur son exemple.

**Un résultat négatif correctement établi vaut autant qu'un résultat positif.** Cette règle est en vigueur depuis le jalon 3 et elle s'applique une dernière fois ici, avec un argument de plus : six résultats négatifs de ce cours vous ont été présentés avec leur protocole, et ce sont eux dont vous vous souviendrez.

---

## Barème indicatif

| Critère | Points | Ce que je regarde |
| --- | --- | --- |
| **Reproductibilité** | 6 | la liste de vérification ci-dessus, point par point. C'est le poids le plus élevé, et il est délibéré |
| **Caractérisation du problème** | 4 | la cinquième colonne de la Figure 15-1, les trois numéros de semaine, et la justification des onze exclusions |
| **Comparaison des quatre jalons** | 4 | ce que chaque famille a acheté sur **votre** problème, avec vos propres chiffres et leurs intervalles |
| **Lecture critique de vos résultats** | 3 | ce que vos mesures établissent, ce qu'elles n'établissent pas, et ce qui reste inexpliqué |
| **Présentation orale** | 2 | dix minutes, une question, une démonstration qui fonctionne |
| **Qualité du rapport** | 1 | huit à dix pages, lisible, et les figures légendées |
| **Total** | **20** | |

---

## Remise

{{< remise cle="livrables-finaux" >}}

---

## La dernière page

Nous voici au bout, et je veux vous dire deux choses avant de refermer.

La première est un constat, et je le trouve plus encourageant qu'il n'en a l'air. Vous avez rencontré, en quinze semaines, une méthode qui ne converge pas, un classement qui s'inverse d'un environnement à l'autre, un agent qui désapprend quand on l'entraîne davantage, une récompense qui se laisse exploiter par l'agent qui l'optimise, une reproduction qui échoue, deux rapports d'une même expérience qui se contredisent, un jeu de référence dont la récompense dépend de la machine, et trois méthodes nommées autrement qu'elles ne sont. Ce n'est pas la chronique d'un domaine en désordre : c'est ce à quoi ressemble un domaine **jeune et actif** quand on le regarde d'assez près pour voir ses mesures. Un cours qui ne vous aurait montré que des courbes qui montent vous aurait moins bien préparé, et vous l'auriez découvert au premier projet réel.

La seconde est ce que je vous souhaite d'emporter. Les méthodes de ce cours se démoderont, certaines vite. Les trois questions de la section 15.1 ne se démoderont pas, parce qu'elles ne sont pas une technique : elles sont la façon de regarder un problème. Et la discipline de mesure ne se démodera pas non plus, parce qu'elle est ce qui distingue un résultat d'une impression. Si dans trois ans vous avez oublié la forme exacte d'un objectif écrêté mais que vous demandez encore, devant un système qu'on vous présente, **quelle récompense il optimise, qui l'a écrite, et dans quelles unités sont ses chiffres**, alors ce cours aura fait son travail.

Le module 5 se termine, et avec lui SCI1070. Il n'y a pas de semaine 16 : la suite, ce sont vos projets. Merci de m'avoir accompagnée pendant ces quinze semaines, bon courage pour vos livrables, et bonne route.

---
