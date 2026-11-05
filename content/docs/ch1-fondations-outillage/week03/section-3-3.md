---
title: "3.3 La méthode en cinq étapes"
weight: 4
---

## Une politique qui est un classifieur

L'explication de cette méthode se coupe naturellement en deux parties très inégales : une partie pratique, qui est intuitive et occupe les sections 3.3 à 3.5, et une partie théorique, sophistiquée, qui tient dans l'encadré facultatif de la section 3.6. Nous commençons par la pratique, et vous verrez qu'elle se suffit à elle-même.

{{% comment %}}SOURCE: LAPAN ch.4 p.120{{% /comment %}}

Remplaçons l'agent de la semaine 1 par une fonction non linéaire entraînable, qui transforme l'observation en une sortie. Comme la méthode est fondée sur la politique, cette sortie **est** la politique : pour chaque observation \(s\), le réseau produit \(\pi(a \mid s)\), une distribution de probabilité sur les actions. La **Figure 3-1** montre ce circuit, et c'est l'image qui fait tout comprendre d'un coup.

{{< bookfig src="03-01.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.120-121{{% /comment %}}

Regardez maintenant cette sortie avec les yeux de la semaine 2. Une distribution de probabilité sur un petit nombre d'actions, cela ressemble énormément à un **problème de classification**, le nombre de classes étant le nombre d'actions. CartPole a deux actions : c'est une classification binaire dont les classes s'appellent « pousser à gauche » et « pousser à droite ». Cette **politique représentée par un réseau de neurones** (*policy network*) est donc un classifieur, et c'est pour cela que la perte de la semaine 2 va s'appliquer telle quelle.

{{% comment %}}SOURCE: LAPAN ch.4 p.121{{% /comment %}}

---

## L'échantillonnage de l'action, et pourquoi il est votre seule exploration

Le cycle de l'agent devient : passer l'observation au réseau, obtenir une distribution, puis **tirer** l'action au hasard selon cette distribution. Ce tirage s'appelle l'**échantillonnage de l'action** (*action sampling*), et je veux que vous voyiez ce qu'il apporte. Il donne à l'agent son caractère aléatoire, ce qui est une bonne chose : au début de l'entraînement, quand les poids sont tirés au hasard, l'agent se comporte au hasard, et il explore donc son environnement de façon uniforme. À mesure que le réseau apprend, les distributions se resserrent, et l'exploration diminue d'elle-même sans qu'aucune ligne de code ne s'en occupe.

{{% comment %}}SOURCE: LAPAN ch.4 p.121{{% /comment %}}

> [!WARNING]
 **Attention, c'est le seul mécanisme d'exploration de toute la méthode.** Pas de \(\varepsilon\), pas de prime, pas de bruit ajouté : rien que ce tirage. C'est élégant, et c'est fragile. Si le réseau devient confiant trop vite, la distribution se concentre sur une action, le tirage ne produit plus de variété, et l'agent cesse d'explorer alors même qu'il n'a rien trouvé de bon. Retenez cette fragilité : elle explique une partie du plateau que nous mesurerons en section 3.5, et elle justifie à elle seule les mécanismes d'exploration des semaines 8 et 11.

---

## Le retour d'un épisode, et une lettre à fixer

Un épisode est une suite d'observations, d'actions et de récompenses. Plus l'agent joue bien, plus l'épisode est long et plus il accumule de récompenses. La **Figure 3-2** en montre quatre, de longueurs différentes, chacun accompagné de son total.

{{< bookfig src="03-02.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.121-122{{% /comment %}}

Ce total est le **retour** de l'épisode, et CEM le prend **non actualisé**, c'est-à-dire avec \(\gamma = 1\) : une simple somme des récompenses, du premier pas au dernier.

$$
G = \sum_{t=1}^{T} R_t
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.121-122{{% /comment %}}

Une convention de notation, et elle n'est pas un détail de confort. Dans ce cours, \(R_t\) est la récompense **d'un pas** et \(G\) le total **d'un épisode**. Vous croiserez ailleurs la lettre \(R\) employée pour ce total, et l'inversion des deux est une source d'erreurs tenace : un retour qui vaut 475 ne se confond pas avec une récompense qui vaut 1. La page « Notation » du cours fait foi, consultez-la au moindre doute.

---

## Les cinq étapes

La méthode complète, maintenant. Elle tient en cinq étapes, et vous allez les reconnaître une à une dans le code de la section 3.4.

1. Jouer \(N\) épisodes avec le modèle courant.
2. Calculer le retour total de chaque épisode et fixer un **seuil des élites**, en général un percentile de l'ensemble des retours, le 50ᵉ ou le 70ᵉ.
3. Écarter tous les épisodes situés sous ce seuil.
4. Entraîner le réseau sur les épisodes restants, les **épisodes élites** (*elite episodes*), en prenant les observations comme entrées et les actions effectivement jouées comme sorties désirées.
5. Reprendre à l'étape 1.

{{% comment %}}SOURCE: LAPAN ch.4 p.122{{% /comment %}}

Le cœur de la méthode est donc de **jeter les mauvais épisodes et de s'entraîner sur les meilleurs**. Formellement, le seuil de l'itération \(i\) est le percentile \(p\) des retours du lot :

$$
\psi_i = \mathrm{Perc}_{p}\left\{G^{(1)}, G^{(2)}, \ldots, G^{(N)}\right\}
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.122, p.127{{% /comment %}}

Avec \(p = 70\), le seuil garde les **30 % d'épisodes les mieux classés** du lot. Ce **percentile de sélection des épisodes** (*percentile filtering*) est l'unique mécanisme de sélection de la méthode, et c'est aussi, nous le verrons, son unique point de rupture.

{{% comment %}}SOURCE: LAPAN ch.4 p.123{{% /comment %}}

> [!WARNING]
 **Attention, un mot pour trois choses, et il faut trancher maintenant.** La semaine 1 a employé « frontière de récompense » pour le seuil qui déclare un environnement **résolu** : une moyenne sur 100 épisodes consécutifs, 475 pour la version de CartPole que nous utilisons ici. Ce sens reste celui du cours, et c'est celui du glossaire. Le seuil **mobile** que nous venons de définir, recalculé à chaque itération par un percentile, est une tout autre chose : il s'appellera dans ce cours le **seuil des élites**, et il se note \(\psi_i\). L'un est un critère d'arrêt fixé une fois pour toutes, l'autre est une quantité qui bouge à chaque lot. Les confondre rend la section 3.5 incompréhensible.

Le réseau apprend donc à répéter les actions qui ont mené à un retour plus élevé, ce qui **déplace le seuil vers le haut**, itération après itération. C'est un mécanisme qui se relance tout seul : de meilleurs épisodes donnent un seuil plus exigeant, un seuil plus exigeant donne de meilleurs élites, et ainsi de suite. Notez bien la condition cachée de cette mécanique, parce qu'elle sera notre point de rupture : il faut que le seuil **puisse** monter, donc que les retours du lot se distinguent les uns des autres.

{{% comment %}}SOURCE: LAPAN ch.4 p.122{{% /comment %}}
