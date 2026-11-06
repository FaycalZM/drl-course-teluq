---
title: "13.8 Charnière : cesser de replanifier, et deux objections qui valent d'être pesées"
weight: 9
---

## Le même modèle, une question différente

Nous changeons de question sans changer d'objet. **Le modèle du monde reste exactement celui des sections 13.3 à 13.6** : même scission déterministe-stochastique, même borne variationnelle, même terme de divergence, même boucle de collecte, même répétition d'action, même latent de dimension trente. Je ne le reconstruirai pas, et si vous vous surprenez à relire la section 13.3 en pensant qu'il s'agit d'autre chose, c'est le signe qu'il faut revenir ici.

Ce qui change est ce qu'on **fait** du modèle. Jusqu'ici : on cherche dedans, à chaque pas, une suite d'actions, et on en joue la première. Désormais : on y **entraîne une politique**, une fois pour toutes, et au moment d'agir on lui demande son avis en une seule passe avant.

Deux objections motivent ce changement, et elles sont de natures très différentes.

**Première objection : un horizon fini rend l'agent myope.** Maximiser les récompenses imaginées sur un horizon \(H\) revient à ignorer tout ce qui se passe après \(H\). Un agent qui planifie sur douze pas ne verra jamais qu'une action lui coûte cher au quinzième. C'est l'objection que la section 13.7 vient d'annoncer, et la réponse est une **fonction de valeur** : un nombre, attaché à l'état où le plan s'arrête, qui résume ce que vaut la suite. Vous avez écrit cela en semaine 7 et vous l'avez employé à chaque semaine depuis : c'est exactement la raison d'être de l'amorçage.

**Seconde objection : planifier en ligne est cher au moment de décider, et jette un gradient qu'on vous offre.** Reprenez le coût de la section 13.5 : mille candidats, dix itérations, douze pas, à **chaque pas d'environnement**. Cent vingt mille passes de transition par décision. Un acteur entraîné, lui, décide en une passe. Et la seconde partie de l'objection est la plus intéressante : cette recherche est **sans dérivée**, alors que la dynamique dans laquelle elle cherche est un **réseau de neurones**, c'est-à-dire un objet dérivable de part en part. On choisit habituellement une recherche sans dérivée par prudence, parce qu'un gradient calculé à travers un modèle imparfait peut mener n'importe où. L'objection consiste à dire que cette prudence coûte très cher : on paie cent vingt mille passes avant pour obtenir ce qu'un gradient donnerait d'un coup.

{{% comment %}}SOURCE: DREAMER p.1{{% /comment %}}

{{< bookfig src="13-02.png" week="13" >}}

La **Figure 13-2** met les deux régimes côte à côte. À gauche, la recherche de la section 13.5 : un éventail de suites d'actions, relancé à chaque pas, et un mur à l'horizon \(H\) au-delà duquel rien n'est évalué. À droite, un acteur entraîné dans l'imagination : une seule flèche au moment de décider, et au bout du déroulement imaginé un **critique** qui chiffre ce qui reste. Les deux étiquettes de coût au bas des panneaux sont la moitié de l'argument de la section ; la différence entre le mur et le critique en est l'autre moitié.

---

## Trois composantes, et une convention que je pose maintenant

Un agent de ce type se décrit en trois composantes, et je pose le découpage ici parce que les trois sections suivantes en traitent une chacune.

**Apprentissage de la dynamique.** Entraîner le modèle du monde sur les données déjà collectées. C'est la section 13.4, inchangée.

**Apprentissage du comportement.** Entraîner un acteur et un critique **sur des trajectoires imaginées** par le modèle. C'est nouveau, et ce sont les sections 13.9 à 13.11.

**Interaction avec l'environnement.** Collecter de nouveaux épisodes avec l'acteur, pour alimenter la dynamique. C'est la section 13.6, dont seule la ligne de collecte change : le planificateur est remplacé par l'acteur.

Les trois tournent **en alternance ou en parallèle**, et l'ordre exact n'est pas ce qui fait le résultat.

{{% comment %}}SOURCE: DREAMER p.2{{% /comment %}}

> [!IMPORTANT]
 **Une observation de vocabulaire qui va vous épargner une confusion, et je la pose avant la section 13.9.** À partir d'ici, deux mondes coexistent dans chaque phrase : le monde **réel**, où l'agent collecte, et le monde **imaginé**, où il apprend à se comporter. Ce cours les distingue par trois conventions tenues sans exception. Le temps réel s'indice \(t\), le temps imaginé s'indice \(k\). Une récompense **reçue** s'écrit \(R_t\), une récompense **prédite** par le modèle s'écrit \(r_k\) : la seconde n'a jamais été perçue par personne. Et une loi apprise porte toujours un indice de paramètres, \(\theta\) pour le modèle, \(\phi\) pour l'acteur, \(\psi\) pour le critique. Si une phrase vous semble ambiguë, regardez l'indice de temps : il dit dans quel monde vous êtes.

---
