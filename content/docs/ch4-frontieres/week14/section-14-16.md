---
title: "14.16 Qui définit l'objectif"
weight: 17
---

## « Récompense réelle » est une convention, et ce cours le dit en son nom

Nous avons employé trente fois l'expression « récompense réelle », et il est temps de regarder ce qu'elle suppose.

Elle suppose qu'il existe, pour un environnement donné, une grandeur qui **est** ce que l'on veut, par opposition à un substitut qui ne l'est pas. Et je veux vous dire clairement ce que ce cours en pense : **cette notion n'est pas bien définie**, et l'expression est une commodité de langage.

Ce n'est pas une position philosophique, c'est une conclusion tirée des mesures de cette semaine. Rappelez-vous le cas de la glycémie en section 14.14 : la récompense réelle y est le **coût pour le patient**, et non le risque d'hypoglycémie. Ce choix est défendable et il est aussi **révisable** : une autre équipe, avec les mêmes données, aurait pu décider que la grandeur d'intérêt était le risque, et elle aurait obtenu la conclusion inverse sur le même agent. Rappelez-vous le cas de la politique sanitaire : la stratégie optimale au sens médical est inapplicable au sens politique, et aucune des deux lectures n'est la vraie.

Ce que ce cours retient, et il le retient en son propre nom plutôt que de l'attribuer à quiconque : **une récompense dite réelle décrit un objectif possible de la personne qui conçoit le système, et non nécessairement l'objectif effectivement poursuivi.** C'est un point de référence choisi, pas un fait de la nature.

Et il ne faut pas en conclure que la mesure perd son sens, parce que ce serait la mauvaise conclusion. Ce que les sections 14.13 et 14.14 démontrent reste intégralement valide, et je formule ici ce que la convention autorise et ce qu'elle interdit.

**Ce qu'elle autorise.** La démonstration est **relative**, et c'est tout ce dont elle a besoin : prenez n'importe quel couple formé d'une grandeur optimisée et d'une grandeur évaluée, où la seconde a été choisie comme représentant mieux l'intention ; alors augmenter la puissance d'optimisation améliore la première et dégrade la seconde, souvent par bascule. Cette conclusion ne dépend pas de ce que la seconde grandeur soit la vérité ; elle dépend seulement de ce qu'elle soit différente.

**Ce qu'elle interdit.** Elle interdit de lire une de ces courbes comme un verdict moral sur un agent, et elle interdit de comparer deux environnements par les valeurs numériques de leurs récompenses réelles, puisque ces valeurs sont des conventions différentes. Elle interdit aussi, et ce n'est pas rien, de présenter une expérience de ce genre sans dire **qui** a choisi la grandeur d'évaluation et selon quel raisonnement.

> [!IMPORTANT]
 **C'est le point où l'éthique de cette semaine devient de l'ingénierie, et c'est la raison pour laquelle cette section n'est pas un sermon.** La question n'est pas de savoir si l'optimisation est une mauvaise chose. Elle est de savoir **qui écrit la grandeur optimisée, qui écrit la grandeur évaluée, et qui arbitre quand les deux divergent**. Dans toute la chaîne de la première moitié de cette semaine, ces trois rôles étaient tenus par la même personne, qui était aussi celle qui étiquetait, et c'est pourquoi la question ne s'est jamais posée. Dans un système déployé, ces trois rôles sont tenus par des personnes différentes, qui n'ont ni le même intérêt, ni la même information, ni le même pouvoir. Toute la difficulté est là, et elle est entièrement contenue dans un choix de fonction objectif.

---

## Un chiffre de détection, et tout son protocole

Puisque cette semaine passe deux sections à vous apprendre à lire la portée d'un résultat, elle doit s'appliquer la règle à elle-même. Voici donc un chiffre que je pourrais vous donner seul, et le protocole qui l'accompagne.

**Le chiffre.** On peut tenter de **détecter** un piratage de récompense sans observer la récompense réelle, en surveillant la loi des actions de la politique et en la comparant à celle d'une politique de confiance. Deux statistiques de divergence entre lois conviennent, la **divergence de Jensen-Shannon** et la **distance de Hellinger**, et toutes deux atteignent, dans leur variante en moyenne, une aire sous la courbe caractéristique de **88,9 %** sur la sous-tâche routière à erreur de pondération, avec une mesure F1 maximale de 0,900. Sur la même sous-tâche, une variante fondée sur l'étendue plutôt que sur la moyenne obtient 74,1 %.

**Le protocole, et il faut le lire en entier.** La vérité de terrain a été construite ainsi : **une seule personne, qui faisait partie de l'équipe même de l'expérience**, a étiqueté chaque politique comme acceptable, problématique ou ambiguë, **en fonction de sa récompense réelle relativement à celle des autres politiques**. Et seules les politiques ayant reçu une étiquette **non ambiguë** ont été conservées dans l'évaluation.

{{% comment %}}SOURCE: PAN p.8-9{{% /comment %}}

Reprenez cette phrase lentement, parce qu'elle contient trois limites et qu'aucune n'est cachée.

**Première limite : l'étiquetage n'est pas à l'aveugle, et il ne peut pas l'être.** La personne qui étiquette juge en regardant la récompense réelle, c'est-à-dire exactement la quantité que le détecteur n'a pas le droit de voir. Ce n'est pas une négligence de protocole, c'est une conséquence du problème : il n'existe pas d'autre source de vérité. Mais cela veut dire que la vérité de terrain est **un seuil appliqué par une personne sur une grandeur continue**.

**Deuxième limite : les cas difficiles ont été retirés du banc d'essai.** Les politiques ambiguës sont celles dont on ne sait pas dire si elles sont acceptables, c'est-à-dire précisément celles sur lesquelles un détecteur aurait de la valeur. Le score est donc mesuré sur la partie facile de la distribution.

**Troisième limite : l'étiquetage est le fait d'une seule personne, et elle n'est pas indépendante de l'expérience.** Il n'y a donc aucune mesure d'accord entre étiqueteurs, et aucun moyen de distinguer le critère de cette personne d'un critère partagé.

Et maintenant le fait qui, à mon sens, doit accompagner le chiffre partout où il voyage : **ce n'est pas le résultat central**. La même statistique de Jensen-Shannon en moyenne obtient **45,2 %** sur la sous-tâche sanitaire à erreur d'ontologie, c'est-à-dire **sous le hasard**, là où la variante fondée sur l'étendue atteint 88,1 %. L'énoncé qui résume le tableau complet est explicite : **chaque détecteur a au moins une sous-tâche où son score passe sous 60 %.**

{{% comment %}}SOURCE: PAN p.8-9 (tableau 2){{% /comment %}}

| Détecteur | Circulation, erreur de pondération | Politique sanitaire, erreur d'ontologie |
| --- | --- | --- |
| Jensen-Shannon en moyenne | **88,9 %** | **45,2 %**, sous le hasard |
| Hellinger en moyenne | **88,9 %** | non rapporté ici |
| Hellinger sur l'étendue | 74,1 % | **88,1 %** |

> [!TIP]
 **Pourquoi j'ai mis ce chiffre et son compagnon dans la même section, et ce que j'attends que vous en fassiez.** Pris seul, le 88,9 % raconte une histoire : la détection fonctionne, un gardien est possible. Pris avec son compagnon à 45,2 %, il raconte une autre histoire, plus juste et plus utile : **aucun détecteur unique ne couvre toutes les formes de piratage**, et le meilleur sur une sous-tâche peut être sous le hasard sur une autre. La conséquence pratique est importante, et elle est opérationnelle : on ne déploie pas un détecteur, on déploie un **ensemble** de détecteurs, et on ne tire de conclusion que sur les sous-tâches où l'on a mesuré. J'insiste sur la méthode plus que sur le chiffre : cette semaine vous a demandé deux fois de lire la portée d'un résultat, en section 14.8 pour un tableau de quatre lignes et ici pour une aire sous la courbe. C'est la même compétence, et c'est celle que le jalon 4 note le plus lourdement.

---

## Trois affirmations à contester, et je les conteste avec les mesures de la semaine

Trois formulations circulent au sujet de la rétroaction humaine, et je veux les examiner à la lumière de ce que cette semaine a établi. Je les conteste en mon nom, avec les mesures des sections précédentes comme arguments.

**Première affirmation : cette approche nous dispense du réglage de bas niveau de la fonction de récompense.** Ce que les mesures montrent : le réglage ne disparaît pas, il **change de lieu et de langue**. Il quitte le fichier de l'environnement, où il était versionné et testable, pour se loger dans le protocole d'étiquetage, où il n'est ni l'un ni l'autre. La section 14.5 l'a montré, puisque la spécification de toute l'expérience tenait dans un paragraphe en prose, et la section 14.8 l'a réfutée en acte : le tour 3 a produit exactement ce que le protocole d'étiquetage demandait, et pas ce que nous voulions.

**Deuxième affirmation : l'affinage par rétroaction humaine est l'étape d'alignement d'un modèle.** Ce que les mesures montrent : la grille de la section 14.9 compte **cinq** catégories de problèmes, et **trois d'entre elles ne sont pas des problèmes de spécification d'objectif** du tout. Ce sont l'exploration sûre, la supervision extensible et le changement de distribution entre entraînement et déploiement. Deux des cinq survivent par ailleurs à un apprentissage parfait et à des données infinies. Aucune étape unique d'entraînement ne peut donc être **l'**étape d'alignement, et parler ainsi laisse croire qu'une case a été cochée. La rétroaction humaine est une réponse puissante à **un** des cinq problèmes, et une réponse partielle à un second.

**Troisième affirmation : la méthode permet d'obtenir un comportement socialement acceptable.** Ma contestation tient en deux mots : **acceptable pour qui ?** Cette semaine a vu une personne définir ce qui est bon pour un sous-marin, une personne définir ce qui est acceptable pour une politique de circulation, et une personne décider que la grandeur d'intérêt d'un régulateur de glycémie était le coût et non le risque. Trois spécifications, trois personnes, et dans aucun des trois cas la question de la légitimité n'est posée, parce que dans aucun des trois cas l'enjeu ne la rendait nécessaire. Elle le devient dès qu'un système est déployé.

{{% comment %}}SOURCE: LAPAN ch.19 p.574, p.577, p.578 ; AMODEI p.2-3{{% /comment %}}

---

## Les trois questions que la chaîne ne pose pas

Je termine la partie enseignante de la semaine sur trois questions, et je les laisse ouvertes parce qu'elles n'ont pas de réponse technique.

**Qui étiquette ?** Dans notre chaîne, une personne, qui était aussi celle qui avait écrit le code et qui connaissait l'objectif. Dans une chaîne industrielle, des milliers de personnes, qui ne connaissent ni le système ni son usage prévu. Le modèle de récompense apprend leur critère, quel qu'il soit, et il l'apprend fidèlement : c'est tout ce qu'il sait faire.

**Selon quels critères ?** Dans notre chaîne, un paragraphe en prose, écrit par la personne qui étiquetait, pour elle-même. Dans une chaîne industrielle, un document de consignes, qui est à proprement parler **la fonction de récompense du système** et qui n'est presque jamais publié. C'est le document que vous voudriez lire pour comprendre le comportement du modèle, et c'est celui que vous ne lirez pas.

**À quel prix ?** Cette question n'est posée par aucune des constructions techniques que cette semaine a décrites, et son absence est en elle-même une information. Un million de paires étiquetées se lit comme un chiffre d'ingénierie et se vit comme un volume de travail humain. Ce cours ne peut pas la trancher et il ne va pas la contourner : elle fait partie de la chaîne au même titre que le pas d'apprentissage.

---

## Ce que cette semaine ne prétend pas trancher

Un mot de délimitation pour finir, et il est de la même nature que celui de la section 14.9.

Cette semaine a traité des **accidents** : des systèmes qui font autre chose que ce qu'on voulait, sans que personne l'ait voulu. Elle n'a pas traité de la vie privée, de l'équité des décisions automatisées, de la sécurité informatique, du mésusage délibéré, de la transparence ni de la régulation. Ces questions sont réelles, elles concernent les mêmes systèmes, et aucune ne se réduit à un problème de spécification de récompense.

{{% comment %}}SOURCE: AMODEI p.21{{% /comment %}}

Ce que cette semaine vous laisse est plus modeste et, j'espère, plus solide : une grille de diagnostic à deux axes, un protocole de mesure qui tient en deux lignes de code, et la connaissance précise de ce qu'un très bon optimiseur fait d'une spécification approximative.

---
