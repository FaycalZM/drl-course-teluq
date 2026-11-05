---
title: "Jalon 1 : analyse de l'échec (25 %)"
weight: 9
---

## Ce qui est évalué, et pourquoi ce n'est pas une réimplémentation

Le jalon 1 clôt le module 1 et vaut **25 %** de la note du cours. Je ne vous demande pas de réécrire CEM : vous venez de le faire au laboratoire, et de toute façon une réimplémentation se recopie. Je vous demande de **conduire une analyse d'échec** et de la rendre lisible : prendre un agent qui fonctionne, le mettre en situation d'échouer, mesurer, expliquer la cause à partir de vos propres mesures, puis corriger et dire ce que la correction achète et ce qu'elle n'achète pas.

C'est la compétence la plus transférable de tout le cours. Dans les douze semaines qui suivent, vos agents échoueront régulièrement, et la question ne sera jamais « où est l'erreur de code ? » mais « qu'est-ce que la structure de ce problème empêche ma méthode de faire ? ».

---

## Les quatre étapes du livrable

**Étape 1 : le transfert.** Lancez l'agent de la section 3.4, **inchangé**, sur `FrozenLake-v1` derrière votre enveloppe one-hot. Inchangé veut dire inchangé : mêmes hyperparamètres, même filtre, même boucle. La seule ligne nouvelle du carnet est l'enveloppe. Laissez tourner une centaine d'itérations, ce qui prend quelques minutes, les épisodes étant très courts.

**Étape 2 : les deux graphiques.** Produisez, à partir de votre propre exécution :

* l'**histogramme des retours d'épisode**, sur un lot pris en début d'entraînement et sur un lot pris à la fin ;
* la courbe du **seuil des élites en fonction de l'itération**, superposée au retour moyen du lot.

Les deux graphiques doivent se suffire à eux-mêmes : axes nommés, unités, légende. Un correcteur doit pouvoir lire votre conclusion sur la figure avant de lire votre texte.

**Étape 3 : l'explication, et c'est le cœur de la note.** Expliquez l'effondrement **à partir de votre distribution**, pas à partir de cette page. Votre raisonnement doit contenir, avec vos propres chiffres : la proportion d'épisodes réussis dans vos lots, la valeur que prend le percentile sur cet ensemble de 0 et de 1, le comportement de votre filtre sur les épisodes **égaux** au seuil, et la conclusion sur la composition réelle de votre ensemble d'élites. Quatre maillons, une page.

**Étape 4 : les correctifs et le plateau.** Appliquez les cinq correctifs de la section 3.5. Votre exécution notée est la variante **non glissante** (`is_slippery=False`), qui converge en 120 à 140 itérations, donc en quelques minutes. Rapportez le nombre d'itérations et le retour moyen atteint, puis répondez à une question : lequel des cinq correctifs a été, sur **votre** exécution, le plus déterminant ? Justifiez par une mesure, par exemple en relançant sans ce correctif-là.

---

## Livrables, barème et contraintes

| Livrable | Forme | Points |
| --- | --- | --- |
| Carnet exécuté, de l'enveloppe à l'exécution corrigée | Colab, sorties visibles | 5 |
| Les deux graphiques de l'étape 2 | dans le carnet, axes nommés | 7 |
| L'explication de l'effondrement, chiffres à l'appui | note de 1 à 2 pages | 8 |
| Correctifs appliqués, mesure et commentaire du plateau | note, 1 page | 5 |

> [!IMPORTANT]
 **Je dois insister sur la contrainte de calcul, elle fait partie de la consigne.** L'exécution **notée** est celle du lac **non glissant** : environ 120 à 140 itérations, quelques minutes. Le lac glissant corrigé demande de l'ordre de **50 minutes** pour 10 000 itérations, et il n'est **pas** exigé. Si vous voulez le lancer, faites-le en extension facultative et commentez le plateau observé ; sinon, commentez les repères donnés en section 3.5, à savoir le passage à 50 % de réussites vers la 5 000ᵉ itération et l'arrêt des progrès autour de 55 %. Une analyse honnête de chiffres fournis vaut mieux qu'une exécution de 50 minutes mal interprétée.

**Ce qui n'est pas demandé**, et que je ne noterai pas : battre le plateau de 55 %, inventer un sixième correctif, ou atteindre un taux de réussite particulier sur le lac glissant. Le plateau est un résultat, pas un échec de votre part. Ce qui est noté est la **chaîne de raisonnement** qui va de la forme de votre distribution à la composition de vos élites.

> [!TIP]
 **Un conseil pour la rédaction.** Écrivez votre note comme si vous expliquiez à un collègue pourquoi son agent, qui fonctionne parfaitement ailleurs, ne donne rien sur son problème à lui. Pas de récit chronologique de vos essais : une mesure, une déduction, une conclusion. C'est le format de toute bonne analyse d'échec, et c'est celui que je vous demanderai encore au jalon 2.
