---
title: "6.12 Au-delà de la moyenne : une ouverture"
weight: 13
---

## Deux trajets de même moyenne, et pourquoi la moyenne ne suffit pas

Il reste la sixième amélioration, et je la garde pour la fin parce qu'elle n'est pas de la même nature que les cinq autres. Les cinq réparations précédentes amélioraient l'estimation d'une valeur. Celle-ci remet en question **ce qu'est** une valeur.

Posons la question telle qu'elle mérite de l'être. Depuis la semaine 1, la valeur d'un couple état-action est l'**espérance** du retour. Un seul nombre, qui résume tous les futurs possibles. Est-il raisonnable de comprimer tous les retours futurs possibles en un nombre unique ? Dans un environnement compliqué, le futur est stochastique, et une moyenne est une description très pauvre d'une distribution.

{{% comment %}}SOURCE: LAPAN ch.8 p.268{{% /comment %}}

L'exemple qui emporte l'affaire est quotidien. Vous allez au travail, et vous avez deux options.

En voiture, le trajet prend environ 30 minutes la plupart du temps. Mais de temps en temps, un accident ou un embouteillage le fait tripler, et vous mettez une heure et demie. La **Figure 6-7** donne la distribution complète de ce temps de trajet.

{{< bookfig src="06-07.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.269{{% /comment %}}

En train, le trajet prend 40 minutes, presque toujours. Il arrive qu'un incident ajoute une vingtaine de minutes, mais cela reste borné. La **Figure 6-8** donne cette seconde distribution.

{{< bookfig src="06-08.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.270{{% /comment %}}

Faisons le calcul que fait un agent qui ne connaît que des moyennes. La voiture : 35,43 minutes en moyenne. Le train : 40,54 minutes. La voiture gagne, et un agent fondé sur l'espérance choisira la voiture, systématiquement, sans hésitation.

Faisons maintenant le calcul que vous feriez, vous. Le train a une moyenne un peu moins bonne, et son **pire cas** est une heure, contre une heure et demie pour la voiture. Si vous avez une réunion importante, vous prenez le train, et vous avez raison. Le mot qui nomme ce que la moyenne a jeté est **variance**, et un agent qui ne manipule que des espérances est structurellement incapable de ce raisonnement.

{{% comment %}}SOURCE: LAPAN ch.8 p.269-270{{% /comment %}}

> [!WARNING]
 **Attention en lisant les deux figures côte à côte, parce que l'œil se fait piéger.** Les deux axes horizontaux ne couvrent pas la même plage : celui de la voiture va de 20 à 100 minutes, celui du train de 33 à 62 seulement. Au premier regard, la distribution du train paraît donc la plus large des deux, ce qui est exactement l'inverse de la conclusion. Lisez les chiffres, pas la forme : une bosse à 90 minutes d'un côté, une bosse à 60 de l'autre.

Et dans un processus de décision markovien, cet effet **se compose**. Chaque pas ajoute son aléa, et travailler avec des récompenses moyennes revient à perdre, pas après pas, une grande quantité d'information sur la dynamique réelle de l'environnement.

{{% comment %}}SOURCE: LAPAN ch.8 p.270{{% /comment %}}

---

## L'équation de Bellman, écrite sur des distributions

La famille de méthodes qui prend cette critique au sérieux s'appelle l'**apprentissage par renforcement distributionnel** (*distributional reinforcement learning*), et sa généralisation est d'une élégance qui vaut le détour : elle tient en une ligne. On reprend l'équation de Bellman et on remplace chaque nombre par la **distribution** correspondante. \(Z(s,a)\) est la distribution du retour obtenu en jouant \(a\) dans \(s\), et \(R(s,a)\) est la distribution de la récompense immédiate :

$$
Z(s,a) \;\stackrel{D}{=}\; R(s,a) + \gamma\,Z(s',a')
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.271{{% /comment %}}

Cette **équation de Bellman distributionnelle** mérite une lecture attentive, parce qu'un seul symbole y est nouveau. Le symbole \(\stackrel{D}{=}\) n'est pas une égalité de nombres : c'est une égalité **en distribution**. Il dit que la variable aléatoire de gauche et celle de droite ont la même loi, et non qu'elles prennent la même valeur. Les deux opérations qui apparaissent à droite ont donc un sens nouveau : multiplier une distribution par \(\gamma\) est une contraction de son support vers zéro, et y ajouter la distribution des récompenses est une convolution. L'équation de Bellman ordinaire est le cas particulier obtenu en prenant l'espérance des deux côtés.

Ce qui change dans l'implémentation est, en principe, minime : la sortie du réseau devient une distribution par action au lieu d'un nombre par action, et la perte quadratique est remplacée par une mesure d'écart entre distributions. Deux candidates se présentent. La divergence de Kullback-Leibler, c'est-à-dire l'entropie croisée que vous connaissez depuis la semaine 3, et la métrique de Wasserstein. Le travail d'origine justifiait théoriquement la seconde, a rencontré des difficultés pratiques en l'employant, et a finalement utilisé la première.

{{% comment %}}SOURCE: LAPAN ch.8 p.271{{% /comment %}}

La version concrète de cette idée s'appelle C51, parce qu'elle représente chaque distribution par **51 atomes** répartis sur l'intervalle \([-10, +10]\).

{{% comment %}}SOURCE: LAPAN ch.8 p.271{{% /comment %}}

> [!NOTE]
 **Notez bien les limites de ce que cette section vous demande, parce qu'elles sont volontaires et que je les assume.** Vous devez savoir énoncer l'équation ci-dessus, dire ce que signifie l'égalité en distribution, expliquer avec l'exemple des deux trajets pourquoi une moyenne jette de l'information, et nommer la perte employée. Vous n'avez **pas** à savoir implémenter cette méthode, et ce cours ne vous le demandera pas. La raison est précise : passer d'une distribution continue à 51 atomes fixes demande une opération de projection dont le code est, de toute cette semaine, le plus délicat, et il ne vous apprendrait rien de plus sur l'apprentissage par renforcement. La semaine 9 vous donnera une autre occasion de travailler avec des distributions, et ce sera dans un cadre où elles paient immédiatement.

---
