---
title: "3.6 Pourquoi ça marche"
weight: 7
---

## Trois lettres à fixer avant la première équation

Cette section est **facultative**. Elle n'est utile qu'à qui veut savoir pourquoi la méthode fonctionne, et vous pouvez la sauter sans rien perdre du laboratoire ni du jalon. Je la maintiens pour une raison précise : c'est le seul endroit où le **nom** de la méthode s'explique. Je la présente comme un encadré, pas comme une dérivation à refaire.

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

Avant toute équation, trois symboles, et dans cet ordre, sans quoi toute la lecture s'inverse. Ici, \(x\) désigne une **politique**, et non une entrée du réseau. Donc \(p(x)\) est une **distribution sur les politiques**, et non sur des données. Et \(H(x)\) est la **récompense obtenue par la politique \(x\)**. Oui : dans cette dérivation, \(H\) est une récompense, pas une entropie, alors même que le mot « entropie » va apparaître deux paragraphes plus bas pour désigner tout autre chose.

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

> [!WARNING]
 **Attention, c'est le piège de notation le plus coûteux de la semaine.** Partout ailleurs dans ce cours, \(H\) est une **entropie**, et le total d'un épisode s'écrit \(G\), ou \(R(z)\) quand on veut insister sur la trajectoire \(z\) qui l'a produit. La page « Notation » tranche en ce sens. Si vous lisez les équations qui suivent en prenant \(H\) pour une entropie, vous comprendrez l'exact contraire de ce qu'elles disent : vous croirez qu'on maximise du désordre alors qu'on maximise une récompense. Relisez ce paragraphe avant de poursuivre.

---

## De l'échantillonnage préférentiel à l'entropie croisée

Le point de départ est l'**échantillonnage préférentiel** (*importance sampling*), un théorème très général : l'espérance d'une quantité sous une distribution peut se calculer à partir d'échantillons tirés d'une **autre** distribution, à condition de repondérer par le rapport des deux densités.

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

$$
\E_{x\sim p(x)}[H(x)] = \int_x p(x)H(x)\,dx
  = \int_x q(x)\frac{p(x)}{q(x)}H(x)\,dx
  = \E_{x\sim q(x)}\!\left[\frac{p(x)}{q(x)}H(x)\right]
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

L'intention est alors la suivante : nous ne voulons pas maximiser la récompense en parcourant **toutes** les politiques possibles, ce qui serait hors de portée. Nous voulons approcher \(p(x)H(x)\) par une distribution \(q(x)\), en réduisant itérativement la distance entre les deux. Reste à dire ce que « distance » veut dire, et c'est la **divergence de Kullback-Leibler** (*Kullback-Leibler divergence*) qui s'en charge.

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

$$
\KL\big(p_1(x)\,\|\,p_2(x)\big) = \E_{x\sim p_1(x)}\log\frac{p_1(x)}{p_2(x)}
  = \E_{x\sim p_1(x)}[\log p_1(x)] - \E_{x\sim p_1(x)}[\log p_2(x)]
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

Regardez les deux termes du membre de droite, parce que c'est ici que le nom de la méthode se décide. Le **premier** terme s'appelle l'entropie, et il ne dépend pas de \(p_2(x)\) : dans une minimisation par rapport à \(p_2\), il est une constante et on peut simplement l'oublier. Le **second** terme s'appelle l'**entropie croisée**, et c'est un objectif d'optimisation extrêmement courant en apprentissage profond ; c'est celui que vous avez utilisé toute la semaine 2, et celui que `nn.CrossEntropyLoss` calcule. Voilà d'où vient le nom de la méthode : elle minimise une entropie croisée.

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

En assemblant les deux, on obtient un algorithme itératif, qui part de \(q_0(x) = p(x)\) :

$$
q_{i+1}(x) = \argmin_{q_{i+1}(x)} -\,\E_{x\sim q_i(x)}
  \frac{p(x)}{q_i(x)}H(x)\log q_{i+1}(x)
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.140{{% /comment %}}

Un dernier pas, et c'est celui qui ramène tout dans notre code. Dans le cas de l'apprentissage par renforcement, on remplace \(H(x)\) par une **fonction indicatrice** : elle vaut 1 quand la récompense de l'épisode dépasse un seuil, et 0 sinon. En réécrivant l'ensemble en termes de politiques, avec \(z\) un épisode tiré sous la politique courante et \(\psi_i\) le seuil des élites de l'itération \(i\), on arrive à la forme qui nous intéresse vraiment.

{{% comment %}}SOURCE: LAPAN ch.4 p.140-141{{% /comment %}}

$$
\pi_{i+1}(a \mid s) = \argmin_{\pi_{i+1}}
  -\,\E_{z \sim \pi_i(a \mid s)}\!\left[R(z) \ge \psi_i\right]
  \log \pi_{i+1}(a \mid s)
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.141{{% /comment %}}

Lisez cette équation à côté de la perte de la section 3.4 : ce sont les mêmes. Le crochet est l'indicateur qui sélectionne les épisodes au-dessus du seuil, donc exactement notre `if`. Le logarithme de la politique sur les paires retenues, pris en négatif, est exactement la **log-vraisemblance négative** (*negative log likelihood*) de nos élites, c'est-à-dire `nn.CrossEntropyLoss` appliquée aux sorties brutes. À une réserve près, honnête et sans conséquence pratique : cette formule omet le terme de normalisation, et elle fonctionne tout de même. La méthode se résume donc à ceci : on échantillonne des épisodes avec la politique courante, et on minimise la log-vraisemblance négative des plus réussis d'entre eux.

{{% comment %}}SOURCE: LAPAN ch.4 p.141{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(x\), \(p(x)\) | une politique ; une distribution sur les politiques | aucune : objets de la dérivation seulement |
| \(H(x)\) | la récompense obtenue par la politique \(x\) | `Episode.retour`, pour une politique donnée |
| \(z\) | un épisode tiré sous \(\pi_i\) | un élément du `lot` |
| \(\psi_i\) | seuil des élites à l'itération \(i\) | `seuil` |
| \(\left[R(z) \ge \psi_i\right]\) | indicatrice de sélection | le `if` de `filtrer_elites` |
| \(\argmin\) de l'espérance | la minimisation | `loss_v.backward()` puis `optimizer.step()` |

---

## Le même théorème, énoncé proprement

Une précision pour qui veut un énoncé rigoureux de l'échantillonnage préférentiel, parce que la version compacte ci-dessus a un coût. C'est une technique générale d'estimation d'espérances sous une distribution à partir d'échantillons tirés d'une autre. Appliquée au cas hors politique, elle pondère les retours par la probabilité relative de leur trajectoire sous la politique cible et sous la politique de comportement : ce poids s'appelle le rapport d'échantillonnage préférentiel.

{{% comment %}}SOURCE: SB éq. 5.3 p.126{{% /comment %}}

$$
\rho_{t:T-1} \defeq
\frac{\prod_{k=t}^{T-1} \pi(A_k \mid S_k)\, p(S_{k+1} \mid S_k, A_k)}
     {\prod_{k=t}^{T-1} b(A_k \mid S_k)\, p(S_{k+1} \mid S_k, A_k)}
= \prod_{k=t}^{T-1} \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)}
$$

{{% comment %}}SOURCE: SB ch.5 §5.5 p.125-126{{% /comment %}}

La propriété remarquable de ce rapport tient en une phrase, et elle se comprend sans calcul. Les probabilités de transition de l'environnement apparaissent **à l'identique au numérateur et au dénominateur**, et elles **se simplifient**. Le rapport ne dépend donc que des deux politiques et de la suite des états et des actions observés, **pas de la dynamique de l'environnement**. C'est ce qui rend la technique utilisable alors même que nous ne connaissons pas cette dynamique, et c'est aussi ce qui en fera, en semaine 10, l'ingrédient central des méthodes à région de confiance.

{{% comment %}}SOURCE: SB ch.5 §5.5 p.126{{% /comment %}}

> [!NOTE]
 **Une honnêteté intellectuelle, et une réserve pour plus tard.** L'estimateur dit ordinaire est sans biais, mais sa variance peut être **non bornée** ; la version pondérée est légèrement biaisée, d'un biais qui tend vers zéro, et sa variance est en pratique spectaculairement plus faible, ce qui la fait préférer presque toujours. Il existe même un exemple d'école, à un seul état, où l'estimateur ordinaire **ne converge pas** vers la bonne valeur après des millions d'épisodes. Cette semaine, l'échantillonnage préférentiel ne sert qu'à **justifier** la forme de notre perte : nous n'estimons rien avec. Quand nous nous en servirons pour de bon, la variance redeviendra un vrai sujet.

{{% comment %}}SOURCE: SB ch.5 §5.5 p.127, p.128-130{{% /comment %}}
