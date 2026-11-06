---
title: "11.6 Six mesures, et ce que le tableau ne dit pas"
weight: 7
---

## Six exécutions, deux questions par exécution

Nous avons une tâche, une méthode de référence qui échoue complètement, et trois familles de correctifs. Mesurons.

Six exécutions suivent, et chacune répond à **deux questions distinctes** que je vous demande de ne jamais confondre :

1. **Quand l'état but a-t-il été trouvé pour la première fois ?** C'est la mesure de l'exploration proprement dite.
2. **La tâche a-t-elle été résolue**, c'est-à-dire le retour de test moyen a-t-il franchi \(-130\) ? C'est la mesure de l'apprentissage.

Ces deux questions ont des réponses **différentes**, et le fait qu'elles aient des réponses différentes est la meilleure observation de la semaine. Nous y reviendrons à la fin de la section, chiffres en main.

Deux correctifs d'abord sur une méthode de valeur, puis le même jeu sur une méthode de politique.

---

## Un réseau Q profond et des réseaux bruités : le but trouvé, la tâche non résolue

Premier correctif, et c'est la méthode de la semaine 6. Le réseau de la tâche est minuscule, et **une seule couche** devient bruitée : une couche linéaire de 2 vers 128, une unité rectifiée, puis une couche bruitée de 128 vers 3. Le calendrier de \(\varepsilon\) disparaît complètement, comme la semaine 6 l'avait promis.

Un seul écart avec la classe de la semaine 6, et c'est un écart de plomberie : le tirage du bruit devient une **méthode explicite**, appelée depuis la boucle d'entraînement, au lieu d'être déclenchée à l'intérieur de la couche. Sur une méthode hors politique, elle est appelée **à chaque itération d'entraînement**.

{{% comment %}}SOURCE: LAPAN ch.18 p.558-559 (image p.559){{% /comment %}}

```python
import torch.nn as nn
# CoucheBruitee est la classe de la semaine 6, section 6.9 : poids bruites,
# bruit gaussien factorise, amplitude apprise. Elle n'est PAS reecrite ici.
from semaine06 import CoucheBruitee


def reseau_bruite(taille_obs: int, n_actions: int, cachee: int = 128):
    """Une SEULE couche bruitee, en sortie. Plus aucun calendrier d'epsilon."""
    return nn.Sequential(
        nn.Linear(taille_obs, cachee), nn.ReLU(),
        CoucheBruitee(cachee, n_actions),
    )


def tirer_le_bruit(reseau) -> None:
    """Appelee A CHAQUE ITERATION D'ENTRAINEMENT en hors politique."""
    for module in reseau.modules():
        if isinstance(module, CoucheBruitee):
            module.tirer_bruit()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(w_{i,j} = \mu_{i,j} + \sigma_{i,j}\,\epsilon_{i,j}\) | poids bruité de la semaine 6 | interne à `CoucheBruitee` |
| \(\mu, \sigma\) | moyenne et amplitude, **apprises** | `poids_mu`, `poids_sigma` |
| \(\epsilon_{i,j}\) | bruit tiré, jamais entraîné | `poids_epsilon` |
| fréquence de tirage | une fois par itération d'entraînement | `tirer_le_bruit(reseau)` |
| \(\varepsilon\) | taux d'exploration | **supprimé : plus de calendrier** |

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.9{{% /comment %}}

Et voici le résultat, en deux temps. **Bonne nouvelle** : le but est trouvé, après seulement **7 000 pas d'entraînement**, soit **vingt minutes** de calcul. Rappelez-vous que la méthode de référence n'y est pas arrivée en cinq heures. **Moins bonne nouvelle** : le retour de test moyen de \(-130\) n'a **jamais** été atteint. Certains épisodes de test se terminent en moins de cent pas, ce qui est un excellent résultat, mais ils ne sont **pas assez fréquents** pour tirer la moyenne au-dessus du seuil.

{{% comment %}}SOURCE: LAPAN ch.18 p.559 (image){{% /comment %}}

> [!WARNING]
 **Les 7 000 de cette ligne sont des PAS D'ENTRAÎNEMENT, et non des épisodes, et c'est la seule ligne de tout le tableau qui soit dans cette unité.** Je le signale ici et je le re-signalerai sous le tableau, parce que l'erreur est facile à commettre et lourde de conséquences : 7 000 épisodes de cette tâche représenteraient plus d'un million de pas d'environnement, c'est-à-dire cent fois plus d'expérience que ce qui a réellement été consommé. Quand vous lisez une colonne de comparaison, vérifiez l'unité **ligne par ligne**, surtout si la colonne porte un titre unique.

---

## Un réseau Q profond et un comptage d'états : la découverte la plus rapide de la semaine

Deuxième correctif, et c'est l'enveloppe de la section 11.3, telle quelle : l'observation est hachée en arrondissant chacun de ses deux flottants à trois décimales, un compteur tient le nombre de visites de chaque clé, la prime vaut l'inverse de la racine du compteur, et la récompense renvoyée est la somme des deux.

Le résultat est le plus intéressant des six, et pour une raison qui n'est pas celle qu'on attend. **Il a fallu dix minutes pour découvrir l'état but.** C'est la découverte la plus rapide de toutes les exécutions de cette semaine, deux fois plus rapide que celle des réseaux bruités. Et pourtant : le retour de test moyen de \(-130\) n'a **pas** été atteint, même si l'on en est passé très près.

{{% comment %}}SOURCE: LAPAN ch.18 p.561 (image){{% /comment %}}

Lisez ces deux phrases ensemble, parce qu'elles contiennent l'observation que je veux que vous emportiez de cette section : **trouver le but vite et résoudre la tâche sont deux réussites différentes**, et la méthode qui gagne la première peut perdre la seconde. Si l'on dressait la liste des méthodes qui résolvent MountainCar, cette ligne disparaîtrait purement et simplement, et avec elle la seule mesure qui sépare les deux questions.

La raison de cet écart, elle, se devine et je ne vais pas la présenter comme mesurée. Un tampon de rejeu contient alors des centaines de milliers de transitions à \(-1\) et une poignée de transitions intéressantes ; chaque lot tiré au hasard contient donc l'information utile dans une proportion infime, et la fonction de valeur met très longtemps à s'en imprégner. Le but est **dans les données** et il n'arrive pas à en sortir. C'est exactement le premier des trois motifs de la sous-section suivante.

---

## Pourquoi je change de famille de méthode

Nous avons deux correctifs qui trouvent le but et aucun qui résolve la tâche. Avant d'en essayer d'autres, je change de méthode d'apprentissage, et je vous donne les trois raisons, parce que les deux premières sont **réutilisables bien au-delà de cette semaine**.

**Première raison : un tampon de rejeu absorbe lentement un échantillon rare.** Les bons échantillons sont ici une poignée parmi des centaines de milliers, et le tirage uniforme les dilue. On pourrait réparer cela dans la famille des méthodes de valeur, en agrandissant le tampon et en passant au tampon de rejeu priorisé de la semaine 6. On peut aussi changer de famille : une méthode **sur politique** ajuste la politique **immédiatement** en fonction de l'expérience obtenue, sans attendre qu'un échantillon ressorte d'un tirage.

**Deuxième raison, et c'est l'observation à retenir : une récompense qui change en cours d'entraînement est un problème pour une méthode de valeur, et presque pas pour une méthode de politique.** Une méthode de valeur a appris des valeurs numériques ; si la récompense change, il faut **réapprendre** ces valeurs, et le temps passé à les réapprendre est perdu. Or notre prime change la récompense à chaque visite, par construction. Une méthode sur politique, elle, ne stocke pas de valeur de référence pour les anciennes transitions : une récompense plus élevée met simplement **plus de poids** sur l'échantillon correspondant dans le gradient de politique, ce qui est le comportement souhaité et ne demande aucun réapprentissage.

**Troisième raison, honnête et méthodologique :** nous voulons mesurer les mêmes correctifs sur les deux familles, pour savoir si leur effet dépend de la méthode d'apprentissage ou non. C'est une raison de protocole, et elle vaut d'être dite.

{{% comment %}}SOURCE: LAPAN ch.18 p.561 (image), p.562{{% /comment %}}

> [!IMPORTANT]
 **Retenez cette compatibilité, parce qu'elle décide d'un choix d'architecture et qu'elle n'est écrite nulle part dans les semaines précédentes.** Dès que votre dispositif **modifie la récompense pendant l'entraînement** (une prime d'exploration, un façonnage de récompense, une normalisation adaptative, un modèle de récompense qui apprend), une méthode **sur politique** est structurellement plus à l'aise qu'une méthode de valeur à tampon de rejeu. La méthode de valeur doit réapprendre ses estimations à chaque changement d'échelle ; la méthode de politique voit seulement un échantillon mieux payé. Ce n'est pas un argument de performance, c'est un argument de **compatibilité entre deux mécanismes**, et c'est le genre d'argument qui vous fera gagner une semaine sur un projet.

La méthode employée pour la suite est **PPO**, celle de la section 10.2, et je ne la réexplique pas : même objectif écrêté, même avantage généralisé, mêmes époques multiples sur une même trajectoire. Les réseaux sont minuscules, à la mesure de la tâche : un acteur de 2 vers 64, une unité rectifiée, puis 3 sorties ; un critique de 2 vers 64, une unité rectifiée, puis une sortie. La prime d'entropie de la semaine 8 est présente, avec son coefficient \(\beta\).

{{% comment %}}SOURCE: LAPAN ch.18 p.562 (image){{% /comment %}}

---

## PPO seul : une heure pour trouver, trois heures pour rien

Commençons par la référence, c'est-à-dire PPO **sans aucun dispositif d'exploration**. Il faut être précis sur ce que cela veut dire : rien n'est fait spécifiquement pour explorer, et l'on compte uniquement sur l'**initialisation aléatoire des poids**, à laquelle s'ajoute le hasard d'une politique stochastique et la prime d'entropie qui l'empêche de se concentrer.

Résultat en deux parties, et elles ne disent pas la même chose. L'état but **a été trouvé**, après une heure de calcul et environ **30 000 épisodes**. Mais l'entraînement a ensuite été poursuivi **trois heures** sans aucune amélioration, puis arrêté. La tâche n'est pas résolue.

{{% comment %}}SOURCE: LAPAN ch.18 p.562 (image){{% /comment %}}

C'est une mesure utile et elle dit deux choses. D'abord qu'une politique stochastique explore mieux qu'une politique \(\varepsilon\)-gloutonne dont le \(\varepsilon\) a décru : elle trouve le but, là où la méthode de la section 11.5 ne le trouve jamais. Ensuite que cela ne suffit pas : trouver le but une fois toutes les quelques dizaines de milliers d'épisodes ne fournit pas assez d'exemples pour apprendre à le rejoindre délibérément.

---

## PPO et réseaux bruités : du bruit dans l'acteur seulement

Premier correctif sur la méthode de politique, et il demande une décision que la méthode de valeur n'avait pas à prendre : **où mettre le bruit** quand il y a deux réseaux ?

La réponse est : dans la couche de sortie de l'**acteur** uniquement. Le critique garde ses couches ordinaires. La raison est nette et vaut comme principe : on veut injecter du bruit dans la **politique**, pas dans l'**estimation de valeur**. Un critique bruité produirait des cibles bruitées, donc un avantage bruité, c'est-à-dire du bruit dans le signal d'apprentissage lui-même, ce qui n'a rien à voir avec de l'exploration.

{{% comment %}}SOURCE: LAPAN ch.18 p.563{{% /comment %}}

Et voici la deuxième décision, qui est le détail technique le plus réutilisable de la section. **La fréquence de tirage du bruit n'est pas la même selon la famille de méthode.**

| Famille | Quand le bruit est retiré | Pourquoi |
| --- | --- | --- |
| Hors politique (réseau Q profond) | à **chaque itération d'entraînement**, donc en pratique à chaque passe avant | les transitions sont réutilisées depuis un tampon : la cohérence d'une trajectoire n'est pas la grandeur qui compte |
| Sur politique (PPO) | une fois par **lot de 2 048 transitions** | un lot est **une** trajectoire collectée par **une** politique ; retirer le bruit en cours de collecte reviendrait à changer de politique au milieu du lot |

{{% comment %}}SOURCE: LAPAN ch.18 p.563{{% /comment %}}

Prenez la mesure de ce tableau, parce qu'il relie cette semaine à la semaine 10. Une méthode sur politique calcule un rapport entre la nouvelle et l'ancienne politique, et ce rapport n'a de sens que si **une** politique bien définie a collecté le lot. Retirer le bruit tous les dix pas rendrait l'« ancienne politique » du rapport indéfinissable. Le bruit doit donc être tiré **une fois par lot**, et c'est précisément ce qui fait de lui une exploration cohérente : 2 048 transitions entières collectées par une seule politique prélevée dans l'ensemble.

Résultat de cette configuration : le but est trouvé après **trente minutes** et environ **18 000 épisodes**, soit deux fois plus vite que PPO seul. Et comme pour la méthode de valeur, le seuil de \(-130\) n'est **pas** franchi.

{{% comment %}}SOURCE: LAPAN ch.18 p.564 (image){{% /comment %}}

---

## PPO et comptage d'états : la première des deux réussites

Deuxième correctif sur la méthode de politique, et c'est exactement l'enveloppe de la section 11.3, inchangée : le même hachage à trois décimales, le même compteur, la même prime.

Cette fois, la tâche est **résolue**.

Le but est découvert après environ **23 000 épisodes**, dans les **trente-six minutes** de calcul. Puis l'entraînement continue, et il franchit le seuil après environ **61 000 épisodes**, pour un temps total de calcul d'**une heure trente-sept**. Un détail de la fin d'exécution mérite d'être rapporté tel quel, parce qu'il dit quelque chose sur les seuils : l'épisode de test qui déclenche l'arrêt se termine en **91 pas** pour un retour de **\(-91\)**, et la moyenne mobile sur laquelle le critère porte vaut alors **\(-129{,}999\)**. La barre était à \(-130\). Elle a été franchie d'un millième.

{{% comment %}}SOURCE: LAPAN ch.18 p.564, p.565 (images){{% /comment %}}

> [!NOTE]
 **Ce millième n'est pas une anecdote, et je l'utilise comme une leçon sur les critères d'arrêt.** Une exécution déclarée « réussie » et une exécution déclarée « très proche du seuil » peuvent être séparées par un millième de point sur une moyenne mobile, c'est-à-dire par un unique épisode de test un peu meilleur, c'est-à-dire par une graine aléatoire. Le franchissement d'un seuil est une **variable binaire construite sur une grandeur continue bruitée**, et c'est pour cette raison que je vous demanderai, dans le laboratoire, de rapporter la **valeur atteinte** et pas seulement le verdict. Un tableau de « oui » et de « non » cache systématiquement les cas où la différence entre les deux est inférieure au bruit de mesure.

---

## PPO et distillation de réseau aléatoire : la deuxième réussite, et la moins chère

Troisième correctif sur la méthode de politique, et c'est la méthode de la section 11.3 que le cours n'avait jamais rencontrée avant cette semaine.

Les deux réseaux sont ceux du fragment de la section 11.3, avec leurs tailles exactes : la **référence** va de 2 à 128, de 128 à 128, puis de 128 à 1, et elle est figée dès l'initialisation ; le **prédicteur** est une **unique** couche linéaire de 2 vers 1. Ce déséquilibre est le résultat d'un réglage : les meilleurs résultats ont été obtenus avec une référence à trois couches et un prédicteur à une seule, ce qui limite le surapprentissage du prédicteur sur un espace d'observations aussi petit. La prime, dans cette mise en œuvre, est la **différence absolue** entre les deux sorties, détachée du graphe, tandis que le prédicteur est entraîné par une erreur quadratique moyenne contre la sortie de la référence.

{{% comment %}}SOURCE: LAPAN ch.18 p.565-566 (images){{% /comment %}}

La tâche est **résolue**, et c'est la plus économique des deux réussites : environ **33 000 épisodes**, pour **une heure vingt-quatre** de calcul, contre 61 000 épisodes et une heure trente-sept pour le comptage.

{{% comment %}}SOURCE: LAPAN ch.18 p.566 (image){{% /comment %}}

Pour la **découverte** du but par cette exécution, en revanche, je dois assortir le chiffre d'une réserve. Les deux nombres sont d'environ **16 000 épisodes** et **trente-six minutes**, et ils reposent sur une seule mesure là où les six autres lignes en ont deux, qui se confirment l'une l'autre. Je vous les donne donc avec cette réserve explicite, et je les signalerai de la même façon dans le tableau. C'est la règle de la semaine 10 appliquée à ma propre table : une case dont la provenance est plus faible que ses voisines doit le dire.

Reste la plus belle observation de la section, et elle vient d'une courbe que je ne peux pas vous montrer mais dont je peux vous donner la lecture. Si l'on trace la **perte du prédicteur** au cours de l'entraînement, elle reste basse et sans histoire pendant toute la période précédant la découverte : avant que l'agent trouve le but, tout est ennuyeux et prévisible. Puis, au moment où il comprend comment terminer un épisode en moins de 200 pas, cette perte **croît fortement**.

{{% comment %}}SOURCE: LAPAN ch.18 p.568 (image){{% /comment %}}

> [!TIP]
 **Lisez cette courbe à l'envers et vous comprendrez à quoi sert vraiment cette famille de méthodes.** La perte du prédicteur n'est pas un indicateur d'entraînement comme les autres : c'est une **mesure de nouveauté**, et elle monte exactement quand le comportement de l'agent change. Un agent qui tourne en rond produit des observations familières, donc une perte basse, donc une prime faible ; un agent qui vient de découvrir une région nouvelle produit une perte haute, donc une prime forte, donc une incitation à y retourner. La méthode ne récompense pas la nouveauté par un compteur, elle la récompense par **l'ignorance mesurée** de son propre prédicteur, et cette ignorance est journalisable. C'est, à mon avis, le meilleur rapport entre la simplicité du code et la qualité de l'information de toute la semaine.

---

## Le tableau, reconstruit, et les deux observations qu'il porte

Voici les sept exécutions dans un seul tableau : la référence de la section 11.5 et les six mesures de cette section. Je l'ai reconstruit **ligne par ligne**, et je vous dois trois précisions sur sa fabrication, que je place avant lui plutôt qu'après.

Premièrement, la colonne « but découvert » n'a **pas** la même unité partout, et chaque case porte donc son unité. Deuxièmement, les deux colonnes sont indépendantes : une exécution peut découvrir le but et ne jamais résoudre la tâche, et c'est le cas de **quatre** lignes sur sept. Troisièmement, **chaque case est une exécution unique**, sans intervalle.

**Tableau 11-1.** Les sept exécutions sur `MountainCar-v0`. « Résolue » signifie un retour de test moyen supérieur à \(-130\), mesuré sans prime.

| Méthode | But découvert | Tâche résolue |
| --- | --- | --- |
| Réseau Q profond + ε-glouton | **jamais** (ni en \(10^5\) pas, ni en 5 h à \(\varepsilon = 1\)) | non |
| Réseau Q profond + réseaux bruités | 7 000 **pas d'entraînement**, 20 min | non |
| Réseau Q profond + comptage d'états | **10 min** (épisodes non rapportés) | non, très près du seuil |
| PPO seul | 30 000 épisodes, 60 min | non (arrêté après 3 h) |
| PPO + réseaux bruités | 18 000 épisodes, 30 min | non |
| PPO + comptage d'états | 23 000 épisodes, 36 min | **oui** : 61 000 épisodes, ≈ 1 h 37 |
| PPO + distillation de réseau aléatoire | 16 000 épisodes, 36 min (chiffres non recoupés) | **oui** : 33 000 épisodes, ≈ 1 h 24 |

{{% comment %}}SOURCE: LAPAN ch.18 p.557, p.559, p.561, p.562, p.564, p.565, p.566, p.568 (images){{% /comment %}}

La **Figure 11-3** met la première colonne en image, parce que l'écart entre « jamais » et « dix minutes » se voit mieux qu'il ne se lit.

{{< bookfig src="11-03.png" week="11" >}}

Et maintenant les deux observations, que je formule aussi sèchement que possible.

**Première observation : deux exécutions sur sept ont résolu MountainCar, et toutes les deux appartiennent à la famille des méthodes de politique.** Aucune configuration de la méthode de valeur n'a franchi le seuil, même celle qui a trouvé le but le plus vite de toutes. Si vous lisez un jour que les deux familles résolvent cette tâche avec des extensions d'exploration, le tableau ci-dessus dit le contraire, ligne par ligne : les deux réussites sont **PPO + comptage** et **PPO + distillation**, et il n'y en a pas d'autre.

**Seconde observation : la vitesse de découverte ne prédit pas la réussite.** Classez les sept exécutions par temps de découverte et vous obtenez, en tête, le comptage sur la méthode de valeur, à dix minutes. Classez-les par réussite et cette même ligne est un échec. Les deux exécutions qui résolvent ont découvert le but en trente-six minutes, soit presque quatre fois plus lentement que la meilleure exploratrice. **Explorer et apprendre sont deux problèmes, et ils ont deux classements.**

> [!WARNING]
 **Trois mises en garde sur ce tableau, et la troisième est celle que vous appliquerez dans le laboratoire.** D'abord l'unité : la deuxième ligne est en **pas d'entraînement** et toutes les autres en **épisodes** ou en minutes ; une comparaison de nombres bruts entre ces lignes ne veut rien dire. Ensuite la provenance : la découverte de la dernière ligne repose sur des valeurs non recoupées, et je l'ai écrit dans la case plutôt que dans une note de bas de page. Enfin, et c'est le plus important : **chacune de ces quatorze cases est une exécution unique**, sans graine multiple et sans intervalle. Nous venons de voir un seuil franchi d'un millième de point ; nous savons donc qu'au moins une de ces cases pourrait basculer avec une autre graine. Ce tableau est utilisable pour **montrer des ordres de grandeur et séparer deux questions**, et il n'est pas utilisable pour **classer** les sept configurations. C'est exactement la leçon du tableau de la semaine 10, et c'est pourquoi le laboratoire de cette semaine vous demande plusieurs graines et un intervalle sur une tâche assez petite pour que cela tienne dans une soirée.

---
