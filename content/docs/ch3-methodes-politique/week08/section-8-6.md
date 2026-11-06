---
title: "8.6 Réponse au problème 2 : la référence"
weight: 7
---

## Soustraire sans toucher à l'espérance

Nous voulons retirer quelque chose de \(G_t\) pour que l'échelle du gradient mesure un écart plutôt qu'un niveau. La question est : a-t-on le droit ? Et la réponse, remarquablement, est : oui, et pour une raison qui tient en trois égalités.

Le théorème du gradient de politique se généralise immédiatement pour accueillir une **référence** \(b(s)\) :

$$
\nabla J(\theta) \propto \sum_s \mu(s)\sum_a \big(q_\pi(s,a) - b(s)\big)\nabla\pi(a\mid s,\theta)
$$

{{% comment %}}SOURCE: SB éq. 13.10 p.351{{% /comment %}}

La référence peut être **n'importe quelle fonction**, y compris une variable aléatoire, à une seule condition : qu'elle ne varie **pas avec \(a\)**. Voici pourquoi, et je vous demande de suivre les trois égalités une par une, parce que c'est la seule démonstration de la semaine que je vous demande de savoir refaire au tableau.

$$
\sum_a b(s)\nabla\pi(a\mid s,\theta) = b(s)\nabla\sum_a \pi(a\mid s,\theta) = b(s)\nabla 1 = 0
$$

{{% comment %}}SOURCE: SB p.351, égalité non numérotée{{% /comment %}}

Première égalité : \(b(s)\) ne dépend pas de \(a\), donc elle sort de la somme sur les actions, et le gradient, qui est linéaire, passe à travers la somme. Deuxième égalité : la somme des probabilités d'une distribution vaut 1, par définition. Troisième égalité : le gradient d'une constante est nul. Le terme soustrait est donc **exactement zéro**, pas approximativement, pas en espérance : zéro. L'expression ci-dessus et le théorème de la section 8.2 sont la **même** quantité.

La mise à jour correspondante s'écrit alors :

$$
\theta_{t+1} \defeq \theta_t + \alpha\big(G_t - b(S_t)\big)\dfrac{\nabla\pi(A_t\mid S_t,\theta_t)}{\pi(A_t\mid S_t,\theta_t)}
$$

{{% comment %}}SOURCE: SB éq. 13.11 p.351{{% /comment %}}

C'est une **généralisation stricte** de REINFORCE : posez \(b \equiv 0\) et vous retrouvez la mise à jour de la section 8.3, au caractère près. Et voici la phrase qui résume la section, celle qui explique pourquoi on se donne cette peine : soustraire une référence laisse la **valeur espérée** de la mise à jour inchangée, et peut avoir un effet considérable sur sa **variance**.

{{% comment %}}SOURCE: SB ch.13 p.351{{% /comment %}}

> [!IMPORTANT]
 **C'est un repas gratuit, et ils sont rares.** Nous modifions une quantité estimée sans modifier ce qu'elle estime. Aucune approximation n'est introduite, aucun biais, aucun hyperparamètre de compromis : l'estimateur reste non biaisé et sa dispersion diminue. Gardez ce schéma en tête, parce que vous le reverrez : beaucoup de progrès en apprentissage par renforcement consistent à trouver une quantité de moyenne nulle qu'on peut retirer d'un estimateur bruité. La contrainte, en revanche, est absolue : dès que \(b\) dépend de \(a\), la première des trois égalités tombe, le terme soustrait n'est plus nul, et vous optimisez autre chose que ce que vous croyez.

---

## Pourquoi une constante ne suffit pas, et pourquoi il y a maintenant deux pas d'apprentissage

Puisque toute fonction de l'état est admissible, laquelle choisir ? Commençons par éliminer le candidat le plus simple.

Une **constante** unique, par exemple la moyenne de tous les retours observés, fonctionne et améliore les choses. Mais elle ne peut pas faire ce qu'il faudrait, et la raison est facile à voir. Dans certains états, toutes les actions ont une valeur élevée, et il faut une référence élevée pour distinguer la très bonne action de la simplement bonne. Dans d'autres états, toutes les actions ont une valeur faible, et une référence élevée les rendrait toutes négatives, c'est-à-dire également indésirables. Une seule valeur ne peut pas séparer les deux situations. Pour un problème de bandit, où il n'y a qu'un état, une constante est exactement ce qu'il faut ; pour un processus de décision markovien, la référence doit **varier avec l'état**.

{{% comment %}}SOURCE: SB ch.13 p.351{{% /comment %}}

Le choix naturel est donc une estimation de la valeur de l'état, \(\hat v(S_t,\mathbf{w})\), avec \(\mathbf{w} \in \R^m\) un vecteur de poids appris. Et nous savons déjà comment l'apprendre : c'est exactement l'objet de la semaine 5, l'approximation d'une fonction de valeur par une méthode semi-gradient.

{{% comment %}}SOURCE: SB ch.13 p.351{{% /comment %}}

Mais remarquez ce qui vient d'arriver à notre algorithme : il a maintenant **deux** jeux de paramètres, donc **deux** pas d'apprentissage, \(\alpha^\theta\) pour la politique et \(\alpha^{\mathbf{w}}\) pour la valeur. Et ces deux pas ne sont pas également faciles à régler, ce qui est une information pratique de première importance.

Régler \(\alpha^{\mathbf{w}}\) est **relativement facile** : la valeur est une régression ordinaire, sa cible a une échelle connue, et il existe des règles empiriques utilisables, notamment dans le cas linéaire. Régler \(\alpha^\theta\) est **beaucoup moins clair**. Sa bonne valeur dépend de l'amplitude de variation des récompenses, qui est une propriété de l'environnement, et de la paramétrisation retenue, qui est une propriété de votre réseau. Il n'existe pas de règle générale, et c'est pourquoi ce pas d'apprentissage est, dans toute cette semaine, l'hyperparamètre qu'il faut balayer en premier quand quelque chose ne va pas.

{{% comment %}}SOURCE: SB ch.13 p.352{{% /comment %}}

---

## La variance, rendue visible puis mesurée

Je vous ai dit que la variance baisse. Je vais maintenant vous montrer **pourquoi**, par une expérience de pensée qui coûte un paragraphe et qui est, à mon avis, l'intuition la plus utile de toute la semaine. Puis je vous donnerai la mesure.

Imaginez trois actions dans un même état, avec des échelles de gradient \(Q_1\) et \(Q_2\) petites et positives, et \(Q_3\) grande et **négative**. Que fait la mise à jour ? Elle pousse la politique **fortement loin** de l'action 3, et légèrement vers les actions 1 et 2. C'est exactement ce qu'on veut : l'action 3 est désastreuse, il faut arrêter de la prendre.

Maintenant ajoutons une constante à toutes les récompenses de l'environnement, assez grande pour que tout devienne positif. Les récompenses **relatives** n'ont pas changé d'un iota : l'action 3 reste la pire des trois, exactement du même écart. Mais nos trois échelles valent désormais \(Q_1\) et \(Q_2\) grandes et positives, \(Q_3\) petite et positive. Que fait la mise à jour ? Elle pousse fortement vers les actions 1 et 2, et **légèrement vers l'action 3**. Nous ne fuyons plus l'action 3 : nous nous en approchons, lentement. Le problème n'a pas changé et le comportement de l'algorithme, lui, a changé de nature.

{{% comment %}}SOURCE: LAPAN ch.12 p.356{{% /comment %}}

Ce décalage finit par s'effacer, parce que la moyenne de nombreux échantillons le compense. Mais il faut **beaucoup** plus d'échantillons pour l'effacer, et il y a pire : comme le retour actualisé total augmente à mesure que l'agent s'améliore, le décalage lui-même **dérive pendant l'entraînement**. La variance n'est donc pas une constante gênante, c'est une cible mouvante.

L'exemple concret est frappant. Au jeu Pong, un agent qui débute obtient un retour moyen autour de \(-21\) ou \(-20\), parce qu'il perd tous les échanges : toutes les actions paraissent également catastrophiques, et le gradient ne distingue presque rien. Soustrayez une référence de \(-21\) et un retour de \(-20\) devient \(+1\), c'est-à-dire **une victoire relative** : l'algorithme voit soudain une différence là où il n'en voyait aucune. C'est le même état du monde, décrit dans une unité utile.

{{% comment %}}SOURCE: LAPAN ch.12 p.356{{% /comment %}}

Rappelons au passage la définition, parce que nous allons la calculer :

$$
\mathrm{Var}[x] = \E\big[(x - \E[x])^2\big]
$$

{{% comment %}}SOURCE: LAPAN ch.12 p.355{{% /comment %}}

Et voici comment on mesure la variance **du gradient de politique seul**, ce qui demande une petite manœuvre sur le graphe de calcul. Le problème est que la perte totale contient plusieurs termes, et qu'une seule rétropropagation mélange leurs gradients de façon irrécupérable. La solution consiste à rétropropager le terme de politique **d'abord**, à lire les gradients accumulés dans les paramètres, puis à rétropropager les autres termes, et seulement ensuite à faire avancer l'optimiseur sur la somme.

```python
import numpy as np

optimiseur.zero_grad()

# 1. On retropropage LE SEUL terme de politique. retain_graph=True parce que
#    le graphe servira encore pour les autres termes.
perte_politique_t.backward(retain_graph=True)

# 2. On lit les gradients MAINTENANT : ils ne contiennent que la politique.
grads = np.concatenate([
    p.grad.detach().cpu().numpy().ravel()
    for p in reseau.parameters() if p.grad is not None
])
grad_var = float(np.var(grads))      # la quantite a tracer
grad_l2 = float(np.sqrt(np.mean(np.square(grads))))
grad_max = float(np.abs(grads).max())

# 3. On retropropage le reste ; les gradients s'ACCUMULENT sur les precedents.
perte_entropie_t.backward()

# 4. Un seul pas d'optimiseur, sur la somme des gradients.
optimiseur.step()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{L}_\pi\) | terme de politique de la perte | `perte_politique_t` |
| \(\nabla_\theta \mathcal{L}_\pi\) | son gradient, et lui seul | `p.grad` après l'étape 1 |
| \(\mathrm{Var}[\nabla_\theta \mathcal{L}_\pi]\) | la quantité que cette section veut comparer | `grad_var` |
| \(\lVert \nabla_\theta \mathcal{L}_\pi \rVert_2\) | norme du gradient, en moyenne quadratique | `grad_l2` |
| \(\mathcal{L}_H\) | terme d'entropie de la perte | `perte_entropie_t` |

{{% comment %}}SOURCE: LAPAN ch.12 p.357-358{{% /comment %}}

**Le résultat de cette mesure, et c'est le chiffre de la section.** Sur CartPole, en faisant tourner le même gradient de politique avec et sans référence, la variance du gradient de la version avec référence est de **deux à trois ordres de grandeur** plus basse que celle de la version sans. Pas de quelques pour cent : d'un facteur cent à mille. Et c'est ce qui fait converger le système plus vite, puisqu'un gradient moins dispersé permet un pas d'apprentissage plus grand à risque égal.

{{% comment %}}SOURCE: LAPAN ch.12 p.359{{% /comment %}}

La **Figure 8-2** donne la même conclusion sous une autre forme, sur le problème du couloir court de la section 8.1, et je vous la commente parce qu'elle contient un détail honnête qu'il faut voir. La version avec référence, réglée à \(\alpha^\theta = 2^{-9}\) et \(\alpha^{\mathbf{w}} = 2^{-6}\), atteint la valeur optimale de l'état de départ en une centaine d'épisodes. La version sans référence, à son **meilleur** pas d'apprentissage \(\alpha = 2^{-13}\), monte encore au quatre-centième épisode sans y être parvenue. Le détail honnête est le mot « meilleur » : la comparaison n'oppose pas une version réglée à une version négligée, elle oppose deux versions réglées chacune au mieux. Et notez que la référence employée y est un **unique scalaire**, \(\hat v(s,\mathbf{w}) = w\) : sur ce problème, où tous les états se ressemblent, une référence constante suffit à produire cet écart.

{{< bookfig src="08-02.png" week="08" >}}

{{% comment %}}SOURCE: SB ch.13 p.352-353{{% /comment %}}

> [!TIP]
 **Une vérification arithmétique à garder sous la main, et elle vous servira au laboratoire.** Si votre référence est la moyenne des retours actualisés sur un horizon de 10 pas avec \(\gamma = 0{,}99\), et que l'environnement donne 1 par pas, alors la référence doit converger vers \(1 + 0{,}99 + \dots + 0{,}99^9 \approx 9{,}56\). Et une fois qu'elle y est, les échelles du lot, \(G_t - b\), doivent **osciller autour de zéro**. Si votre référence se stabilise ailleurs, ou si vos échelles restent toutes du même signe, vous avez un bogue et non un problème d'apprentissage. Deux nombres, trente secondes, et un diagnostic.

{{% comment %}}SOURCE: LAPAN ch.11 p.347{{% /comment %}}

---
