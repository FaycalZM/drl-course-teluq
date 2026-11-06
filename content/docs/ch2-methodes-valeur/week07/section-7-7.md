---
title: "7.7 Un vrai problème, et une promesse qu'on ne fait pas"
weight: 8
---

## Pourquoi un marché est un bon exercice et une mauvaise promesse

Changement de sujet. Jusqu'ici, dans ce cours, on vous a toujours donné l'environnement. Une grille, un pendule, un émulateur Atari : dans chaque cas, quelqu'un d'autre avait décidé ce que l'agent observe, ce qu'il peut faire et ce qu'il reçoit. Nous allons maintenant prendre un problème où **personne** n'a pris ces décisions, et les prendre nous-mêmes.

Le problème choisi est la négociation d'un titre financier. L'objectif est triple : réutiliser le réseau Q profond et ses extensions des semaines 5 et 6 sans les modifier, **écrire un environnement Gym de bout en bout**, et entraîner un agent à acheter et vendre pour maximiser son profit.

{{% comment %}}SOURCE: LAPAN ch.10 p.304{{% /comment %}}

Et maintenant, l'avertissement, que je place **avant** le contenu et non après, parce que la modestie de l'objectif fait partie de la leçon. Je ne vous promets pas que ce code vous enrichira sur un marché d'actions ou de devises, et je vous demande de ne pas l'espérer. L'objectif de cette seconde moitié est beaucoup plus limité, et beaucoup plus utile : **montrer comment on sort des jeux Atari**, c'est-à-dire comment on transforme un problème qui n'a pas été conçu pour l'apprentissage par renforcement en processus de décision markovien. Ce qui est enseigné ici, ce sont les décisions de modélisation. Le résultat financier, nous le lirons avec le scepticisme qu'il mérite, et la section 7.12 est en grande partie consacrée à ce scepticisme.

{{% comment %}}SOURCE: LAPAN ch.10 p.304{{% /comment %}}

> [!WARNING]
 **Les conditions exactes de l'expérience, données une fois pour toutes, et je vous demande de les relire avant de conclure quoi que ce soit.** L'agent de cette semaine est entraîné sur **un seul instrument financier**, sur **une seule année** de données, en **barres d'une minute**. Il ne détient **qu'une action à la fois**, il ne peut pas renforcer une position existante, et il ne peut pas **vendre à découvert**. Les ordres sont supposés exécutés **instantanément au prix de clôture de la barre courante**. La simulation ne modélise **ni l'écart achat-vente, ni le dérapage des prix, ni l'impact de ses propres ordres sur le marché**. Et le chiffre de profit le plus spectaculaire de la section 7.12 est obtenu **sur les données d'entraînement elles-mêmes**. Chacune de ces neuf conditions est une raison suffisante pour que le résultat ne soit pas une preuve de quoi que ce soit de négociable. C'est un exercice de modélisation, et il est présenté comme tel.

{{% comment %}}SOURCE: LAPAN ch.10 p.309, p.315, p.323, p.325{{% /comment %}}

---

## Ce qu'on négocie, et pour quelles raisons

Un mot de contexte, parce que le mot « trading » évoque souvent une seule image et que le domaine est plus large.

On négocie des **marchandises** (le blé, l'acier, le pétrole), des **actions**, des **devises**, et des instruments plus inattendus comme les **dérivés climatiques** : une entreprise dont le chiffre d'affaires dépend de la météo peut acheter un instrument dont la valeur augmente quand la météo lui est défavorable, et compenser ainsi une partie de son risque.

{{% comment %}}SOURCE: LAPAN ch.10 p.304-305{{% /comment %}}

Et on négocie pour trois raisons distinctes, qu'il est utile de séparer. Le **profit**, qui est l'investissement au sens courant. La **protection**, qu'on appelle la couverture : on accepte de perdre un peu en moyenne pour réduire une exposition. Et le **besoin** : une usine qui achète de l'acier et une entreprise qui change des dollars en yens font des opérations de marché sans aucune intention spéculative.

{{% comment %}}SOURCE: LAPAN ch.10 p.304-305{{% /comment %}}

Il faut aussi dire que le problème est **ancien et extrêmement encombré**. Un très grand nombre de consultants financiers, de fonds d'investissement, de banques et de particuliers essaient de prédire les marchés, avec des moyens considérables. Une méthode qui fonctionne a une valeur économique immédiate, ce qui a deux conséquences : les bonnes méthodes ne sont pas publiées, et toute régularité exploitable tend à disparaître dès qu'elle est exploitée. Gardez cela en tête quand vous lirez que notre agent gagne 150 % en un an.

{{% comment %}}SOURCE: LAPAN ch.10 p.305{{% /comment %}}

La formulation en apprentissage par renforcement, maintenant, en une phrase : l'agent **observe** le marché, et **décide** d'acheter, de vendre ou d'attendre. S'il achète avant une hausse, son profit est positif ; sinon la récompense est négative. C'est tout, et c'est trompeusement simple, parce que les trois mots « observe », « décide » et « profit » cachent chacun une décision de conception.

{{% comment %}}SOURCE: LAPAN ch.10 p.305{{% /comment %}}

---
