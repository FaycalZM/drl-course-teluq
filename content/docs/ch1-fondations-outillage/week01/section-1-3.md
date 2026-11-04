---
title: "1.3 Processus de Markov : la propriété, la matrice, l'épisode"
weight: 4
---

## Premier étage : un système qu'on ne peut que regarder tourner

Il nous manque le cadre mathématique. Nous allons le construire en trois temps, comme un jeu de poupées russes : le **processus de Markov**, où l'on observe seulement ; le **processus de Markov avec récompense** (*Markov reward process*), où l'on ajoute des récompenses ; le **processus de décision markovien**, où l'on ajoute des actions et où l'agent entre en scène. Chaque étage ajoute exactement un ingrédient et ne retire rien.

Un **processus de Markov** (*Markov process*), ou chaîne de Markov, est un système que vous pouvez **seulement observer** : aucun moyen de l'influencer. Les valeurs observées sont les **états** ; leur ensemble est l'**espace d'états** (*state space*), supposé fini (« mais il peut être extrêmement grand pour compenser »). La séquence observée s'appelle une **chaîne**, ou un historique.

{{% comment %}}SOURCE: LAPAN ch.1 p.45{{% /comment %}}

---

## La propriété de Markov

Il faut une hypothèse pour que ce cadre fonctionne, et c'est **la propriété de Markov** (*Markov property*) : la dynamique future du système, depuis n'importe quel état, ne doit dépendre **que de cet état**.

$$
\Pr\{S_{t+1} = s' \mid S_t = s\} \;=\; \Pr\{S_{t+1} = s' \mid S_t = s,\, S_{t-1}, \ldots, S_0\}
$$

Ce qui nous autorise à nommer cette quantité sans mentionner le passé :

$$
p(s' \mid s) \defeq \Pr\{S_{t+1} = s' \mid S_t = s\}
$$

L'objectif de cette propriété mérite d'être dit en clair, car c'est ce qui la rend opératoire : elle rend **chaque état observable autosuffisant** pour décrire le futur, ce qui exige en retour que les états soient distinguables et uniques. Prenons le plus petit exemple possible, le temps, avec deux états, *beau* et *pluie* : beau → beau 0,8, beau → pluie 0,2, pluie → beau 0,1, pluie → pluie 0,9. La météo est un bon exemple parce qu'elle est **presque** markovienne et qu'on voit où elle déraille : une pluie d'été et une pluie d'hiver n'ont pas la même suite probable. Avec deux états, le modèle est donc faux.

{{% comment %}}SOURCE: LAPAN ch.1 p.45-46{{% /comment %}}

> [!TIP]
 **Notez bien cette technique, vous la réutiliserez :** un modèle non markovien se répare en **agrandissant l'espace d'états** : ajoutez la saison, et les quatre états [beau+été, beau+hiver, pluie+été, pluie+hiver] rétablissent la propriété. Le prix est explicite, la taille de l'espace d'états : c'est l'arbitrage même qui justifiera l'empilement d'images en semaine 7.

---

## La matrice de transition, et un exemple à quatre états

On range ces probabilités dans une **matrice de transition** (*transition matrix*) : une matrice carrée \(N \times N\) dont la cellule \((i, j)\) donne la probabilité de passer de l'état \(i\) à l'état \(j\), chaque ligne sommant à 1. Un processus de Markov se définit donc entièrement par deux objets, un ensemble d'états \(\mathcal{S}\) et une matrice de transition \(T\). Rien de plus.

{{% comment %}}SOURCE: LAPAN ch.1 p.46{{% /comment %}}

Passons à un exemple assez riche pour être intéressant et assez petit pour tenir dans la tête : la journée d'un employé de bureau. Quatre états la décrivent, **Home** (pas encore au bureau), **Computer** (il travaille), **Coffee** (à la machine à café) et **Chat** (il bavarde). La **Figure 1-2** en donne le graphe ; observez deux particularités qui ne sont pas décoratives, la journée **commence toujours** à *Home* et passe **obligatoirement** par *Coffee* (aucune arête Home → Computer ni Home → Chat), et elle **se termine toujours** depuis *Computer*.

{{< bookfig src="01-02.png" week="01" >}}

{{% comment %}}SOURCE: LAPAN ch.1 p.47{{% /comment %}}

La **Figure 1-3** reprend le même graphe en portant les probabilités sur les arêtes ; voici la matrice correspondante, en pourcentages, la ligne étant l'état de départ.

{{< bookfig src="01-03.png" week="01" >}}

| depuis ↓ / vers → | Home | Coffee | Chat | Computer |
| --- | --- | --- | --- | --- |
| **Home** | 60 % | 40 % | 0 % | 0 % |
| **Coffee** | 0 % | 10 % | 70 % | 20 % |
| **Chat** | 0 % | 20 % | 50 % | 30 % |
| **Computer** | 20 % | 20 % | 10 % | 50 % |

{{% comment %}}SOURCE: LAPAN ch.1 p.48{{% /comment %}}

---

## L'épisode, la matrice inconnue, la stationnarité

Un **épisode** (*episode*) est une séquence d'états observée : Home → Coffee → Chat → Chat → Computer, par exemple. Et voici la remarque qui transforme un exercice de probabilités en problème d'apprentissage : **en pratique, la matrice de transition n'est pas donnée**. Nous ne disposons que d'épisodes. On estime alors la matrice en **comptant les transitions** observées depuis chaque état puis en normalisant chaque ligne à 1 ; plus on observe, plus l'estimation s'approche du modèle véritable. Il faut donc distinguer en permanence les transitions **observées** dans un épisode (un tirage aléatoire) de la distribution **sous-jacente** qui les a produites. Les confondre, c'est précisément ce que fait un agent qui surapprend sur trois parties chanceuses.

Dernier concept de l'étage, et c'est une conséquence et non une hypothèse de plus : la propriété de Markov **implique la stationnarité** (*stationarity*), c'est-à-dire que la distribution de transition d'un état ne change pas au cours du temps. Pourquoi automatiquement ? Parce qu'une non-stationnarité signifierait qu'un facteur extérieur aux observations influence la dynamique, ce qui contredit l'exigence que l'état seul suffise à décrire le futur.

{{% comment %}}SOURCE: LAPAN ch.1 p.49{{% /comment %}}
