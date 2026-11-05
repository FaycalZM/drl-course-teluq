---
title: "4.4 De l'évaluation à l'itération sur la valeur"
weight: 5
---

## Quatre algorithmes, une seule équation, et une flèche

Nous entrons dans la section la plus importante de la semaine, et je veux d'abord vous dire comment je vais l'enseigner, parce que l'ordre choisi n'est pas l'ordre habituel.

La plupart des présentations donnent l'itération sur la valeur comme une recette : voici une boucle, voici un \(\max\), elle converge, suivant. Nous ne ferons pas cela. Nous allons construire quatre algorithmes dans l'ordre, chacun répondant à une insuffisance du précédent : évaluer une politique, puis l'améliorer, puis alterner les deux, puis constater qu'on peut tronquer l'évaluation à **un seul balayage** sans rien perdre, ce qui donne l'itération sur la valeur. À la fin, l'algorithme ne vous paraîtra pas tombé du ciel : il vous paraîtra inévitable.

Le cadre s'appelle la **programmation dynamique** (*dynamic programming*), et sa définition est exigeante : c'est l'ensemble des algorithmes qui calculent des politiques optimales **étant donné un modèle parfait de l'environnement** sous forme de processus de décision markovien fini. Modèle parfait : la dynamique \(p(s',r \mid s,a)\) est donnée, pas estimée. C'est l'hypothèse 1 de la section 4.3, prise au mot.

{{% comment %}}SOURCE: SB ch.4 p.95{{% /comment %}}

Autant le dire sans détour : avec cette hypothèse, l'utilité pratique directe est limitée. Alors pourquoi quatre sous-sections ?

> [!IMPORTANT]
 **Je dois insister, parce que cette phrase est la voûte des semaines 4 à 6.** Toutes les méthodes que nous verrons ensuite peuvent se lire comme des **tentatives d'obtenir le même effet que la programmation dynamique, avec moins de calcul et sans supposer un modèle parfait**. Lisez-la encore une fois. Elle veut dire que l'algorithme de cette section est l'**étalon** : il n'est pas une étape historique qu'on dépasse, c'est la cible que toutes les méthodes suivantes approchent par des chemins plus économes. Quand, en semaine 5, vous entraînerez un réseau sur des échantillons bruités, vous ferez une version pauvre et robuste de ce que nous faisons ici proprement. Savoir à quoi vous renoncez est la seule façon de savoir ce que vous payez.

{{% comment %}}SOURCE: SB ch.4 p.95{{% /comment %}}

Et voici la clé de lecture de toute la section, qui vous évitera d'apprendre quatre algorithmes au lieu d'un : **on obtient les algorithmes de programmation dynamique en transformant les équations de Bellman en affectations**, c'est-à-dire en règles de mise à jour. Chaque algorithme de cette semaine est une équation de Bellman dans laquelle on a mis une flèche. Le signe égal dit « ces deux quantités sont cohérentes » ; la flèche dit « rends-les cohérentes, maintenant, et écris le résultat dans la table ». C'est tout.

{{% comment %}}SOURCE: SB ch.4 p.96{{% /comment %}}

> [!NOTE]
 **Notez bien une lettre, parce qu'elle entre en collision dans ce cours.** Les algorithmes de cette section s'arrêtent lorsque les changements d'un balayage à l'autre deviennent plus petits qu'un petit seuil. Ce seuil se note traditionnellement \(\theta\). Dans ce cours, \(\theta\) est **toujours** un paramètre de réseau, dès la semaine 5 et jusqu'au bout. Le seuil de convergence s'écrira donc \(\vartheta\), y compris dans les encadrés de pseudocode que je vous donne, et y compris si vous le rencontrez autrement ailleurs. La page « Notation » du cours fait foi.

---

## Évaluation de politique : le problème de prédiction

Premier algorithme, et c'est le plus simple : étant donné une politique \(\pi\), calculer \(v_\pi\). Cette tâche s'appelle l'**évaluation de politique** (*policy evaluation*), et on la nomme aussi le **problème de prédiction** (*prediction problem*), parce qu'elle ne cherche pas à agir : elle cherche à prédire ce que la politique vaut.

L'existence et l'unicité de \(v_\pi\) sont garanties dès que l'une des deux conditions suivantes est satisfaite : \(\gamma < 1\), ou bien la terminaison de l'épisode est garantie depuis tous les états sous \(\pi\). Dans tout ce cours, l'une des deux est toujours vraie, et je ne la rappellerai plus.

{{% comment %}}SOURCE: SB ch.4 p.96{{% /comment %}}

Si la dynamique est connue, l'équation de Bellman de la section 4.2 est un système de \(|\mathcal{S}|\) équations linéaires à \(|\mathcal{S}|\) inconnues. On pourrait l'inverser, comme on l'a fait pour la grille de la Figure 4-2. Mais pour nos besoins, la résolution **itérative** est préférable, et la suite de la semaine va montrer pourquoi : elle se transporte, elle, dans un monde sans modèle.

On construit donc une suite de fonctions \(v_0, v_1, v_2, \ldots\), chacune obtenue de la précédente par la **mise à jour de Bellman** (*Bellman update*), c'est-à-dire par l'équation de Bellman munie d'une flèche.

$$
\begin{aligned}
v_{k+1}(s) &\defeq \E_\pi\big[R_{t+1} + \gamma\, v_k(S_{t+1}) \mid S_t = s\big] \\[2pt]
&= \sum_a \pi(a \mid s) \sum_{s',r} p(s',r \mid s,a)
   \big[\, r + \gamma\, v_k(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.4 éq. 4.5 p.96{{% /comment %}}

On part d'une initialisation arbitraire, à ceci près que les états terminaux reçoivent zéro, et l'on itère. La suite converge vers \(v_\pi\). C'est l'**évaluation itérative de politique**.

Maintenant, deux notions qui ont l'air techniques et qui sont en réalité le cœur de la comparaison avec la semaine 5. Regardez bien ce que fait la formule ci-dessus pour un état donné : elle somme sur **tous** les successeurs possibles, pondérés par leurs probabilités. Elle ne regarde pas un successeur tiré au sort : elle regarde la distribution complète.

> [!IMPORTANT]
 **Je dois insister sur ce point, parce que c'est précisément ce que la semaine 5 va vendre.** Chaque mise à jour de la programmation dynamique est une **mise à jour en espérance** (*expected update*) : elle est fondée sur une espérance sur **tous les états successeurs possibles**, et non sur un seul successeur observé. C'est ce qui la rend exacte, et c'est ce qui la rend impossible dès que la dynamique est inconnue ou l'espace trop grand. La section 4.6 lui opposera la **mise à jour par échantillon** (*sample update*), qui ne regarde qu'un seul successeur, celui que l'environnement a effectivement produit. Toute la différence entre « je sais » et « j'ai vu » est là, et c'est aussi toute la différence de prix.

{{% comment %}}SOURCE: SB ch.4 p.96-97{{% /comment %}}

Seconde notion, et elle a des conséquences immédiates dans le code. Un passage de la mise à jour sur l'ensemble des états s'appelle un **balayage de l'espace d'états** (*sweep*). Comment l'implémenter ? La lecture littérale de l'équation demande **deux tableaux** : on lit dans \(v_k\), on écrit dans \(v_{k+1}\), et on échange à la fin du balayage. Mais il existe une variante avec **un seul tableau**, écrasé au fur et à mesure : c'est la **mise à jour sur place** (*in-place update*). Elle converge aussi, et en général **plus vite**, parce qu'elle utilise les nouvelles valeurs dès qu'elles sont disponibles plutôt que d'attendre la fin du balayage. Le prix à payer est que **l'ordre des états dans le balayage se met à compter**, ce qui n'était pas le cas avec deux tableaux. C'est la version sur place qu'on a en tête, en pratique, quand on parle de programmation dynamique, et c'est celle que je vous donne.

{{% comment %}}SOURCE: SB ch.4 p.97{{% /comment %}}

Reste le critère d'arrêt. Après chaque balayage, on mesure le plus grand changement subi par une case, \(\max_s |v_{k+1}(s) - v_k(s)|\), et l'on s'arrête quand il descend sous \(\vartheta\). Voici l'algorithme complet.

```
Évaluation itérative de politique, pour estimer V ≈ v_π

Entrée : π, la politique à évaluer
Paramètre de l'algorithme : un petit seuil ϑ > 0 qui fixe la précision de l'estimation
Initialiser V(s), pour tout s ∈ S⁺, arbitrairement sauf V(terminal) = 0

Répéter :
    Δ ← 0
    Pour chaque s ∈ S :
        v ← V(s)
        V(s) ← Σ_a π(a|s) Σ_{s',r} p(s',r|s,a) [ r + γ V(s') ]
        Δ ← max(Δ, |v − V(s)|)
jusqu'à Δ < ϑ
```

{{% comment %}}SOURCE: SB ch.4 p.97{{% /comment %}}

Et voici la même chose en Python. Le dictionnaire des symboles suit immédiatement : prenez l'habitude de lire les deux ensemble, ligne par ligne.

```python
import numpy as np

GAMMA = 0.9
VARTHETA = 1e-6          # le seuil de convergence, noté ϑ dans les équations


def evaluer_politique(p, r, pi, n_etats, n_actions):
    """Évaluation itérative de politique, SUR PLACE : un seul tableau, écrasé.

    p[s, a, s2] : probabilité d'atteindre s2 depuis s par a.
    r[s, a, s2] : récompense de cette transition.
    pi[s, a]    : probabilité de jouer a dans s.
    """
    V = np.zeros(n_etats)
    while True:
        delta = 0.0
        for s in range(n_etats):                     # UN balayage
            v = V[s]
            V[s] = sum(
                pi[s, a] * sum(
                    p[s, a, s2] * (r[s, a, s2] + GAMMA * V[s2])
                    for s2 in range(n_etats)         # TOUS les successeurs
                )
                for a in range(n_actions)
            )
            delta = max(delta, abs(v - V[s]))
        if delta < VARTHETA:
            return V
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(V(s)\) | estimation tabulaire de la valeur d'état, pas \(v_\pi\) | `V[s]` |
| \(\pi(a \mid s)\) | la politique évaluée, donnée | `pi[s, a]` |
| \(p(s',r \mid s,a)\) | la dynamique, **connue** dans cette section | `p[s, a, s2]` et `r[s, a, s2]` |
| \(\gamma\) | facteur d'actualisation | `GAMMA` |
| \(\sum_{s'}\) | la mise à jour **en espérance** | la somme interne sur `s2` |
| un balayage | un passage sur tous les états | la boucle `for s in range(n_etats)` |
| \(\vartheta\) | seuil de convergence | `VARTHETA` |
| \(\max_s \lvert v_{k+1}(s) - v_k(s) \rvert\) | plus grand changement du balayage | `delta` |

Deux choses à remarquer dans ce fragment, et je vous demande de les noter parce qu'elles reviendront. La boucle intérieure sur `s2` parcourt **tous** les états successeurs : c'est la mise à jour en espérance, en une ligne de code. Et l'affectation `V[s] = ...` écrase la case **immédiatement**, ce qui fait de cette implémentation la version sur place.

---

## La figure qui justifie tout ce qui suit

Avant d'améliorer quoi que ce soit, je veux vous montrer une observation expérimentale, parce qu'elle va à elle seule dicter la suite de la section.

Prenons un monde en grille de quatre cases sur quatre, avec quatorze états non terminaux. Quatre actions déterministes ; une action qui sortirait de la grille laisse l'agent sur place ; **chaque** transition rapporte **−1** jusqu'à la terminaison, sans actualisation. Le dessin montre l'état terminal deux fois, dans deux coins opposés, mais il s'agit formellement d'un seul et même état.

Sous la politique aléatoire équiprobable, \(v_\pi(s)\) a une interprétation très parlante : c'est l'**opposé du nombre espéré de pas** avant la terminaison. Une case qui vaut −14 est une case dont on sort, en moyenne, en quatorze coups.

{{% comment %}}SOURCE: SB ch.4 p.98{{% /comment %}}

La **Figure 4-6** montre l'évaluation itérative à l'œuvre sur cette grille. Chaque ligne est un balayage : à gauche la table \(v_k\) pour la politique aléatoire, à droite la politique **gloutonne** par rapport à cette table \(v_k\).

{{< bookfig src="04-06.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.4 p.99{{% /comment %}}

Suivez la colonne de gauche, balayage par balayage. À \(k=0\), tout est à zéro. À \(k=1\), tout est à −1,0. À \(k=2\), les valeurs se différencient, −1,7 et −2,0. À \(k=3\), −2,4, −2,9, −3,0. À \(k=10\), −6,1, −7,7, −8,4, −9,0. Et la limite, \(k=\infty\), donne −14, −18, −20, −22.

Maintenant suivez la colonne de droite, et c'est là que tout se joue.

> [!IMPORTANT]
 **Je dois insister : regardez la politique gloutonne à \(k=3\), puis à \(k=\infty\). Elles sont identiques.** La politique gloutonne est **déjà optimale au troisième balayage**, alors que les valeurs de gauche en sont encore à −3,0 là où elles finiront à −22. Les valeurs sont fausses d'un facteur sept et la politique qu'elles désignent est déjà la bonne. Prenez une minute sur ce fait, parce qu'il est la motivation de tout le reste de la section : **on n'a pas besoin de valeurs exactes pour prendre les bonnes décisions.** Évaluer jusqu'à convergence est donc un gaspillage, et l'on peut tronquer. C'est précisément cette observation qui va produire l'itération sur la valeur, deux sous-sections plus bas.

{{% comment %}}SOURCE: SB ch.4 p.99{{% /comment %}}

---

## Amélioration de politique, et le théorème qui l'autorise

Nous savons évaluer. Que faire d'une évaluation ? L'utiliser pour faire mieux. C'est l'**amélioration de politique** (*policy improvement*), et le résultat qui la justifie est le plus élégant de la semaine.

Posons la question précisément. J'ai une politique \(\pi\) et j'ai calculé \(v_\pi\). Dans un état \(s\) donné, j'envisage de dévier : jouer une autre action \(a\), puis revenir à \(\pi\) ensuite. Comment savoir si cela vaut le coup ? Il suffit de comparer \(q_\pi(s,a)\) à \(v_\pi(s)\), et nous avons déjà l'outil pour calculer le premier à partir du second.

$$
\begin{aligned}
q_\pi(s,a) &\defeq \E\big[R_{t+1} + \gamma\, v_\pi(S_{t+1}) \mid S_t = s, A_t = a\big] \\[2pt]
&= \sum_{s',r} p(s',r \mid s,a)\big[\, r + \gamma\, v_\pi(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.4 éq. 4.6 p.100{{% /comment %}}

Voici maintenant le **théorème d'amélioration de politique** (*policy improvement theorem*). Il dit que si une déviation est bonne en chaque état, elle est bonne tout court.

$$
q_\pi\big(s, \pi'(s)\big) \ge v_\pi(s) \;\; \text{pour tout } s
\qquad \Longrightarrow \qquad
v_{\pi'}(s) \ge v_\pi(s) \;\; \text{pour tout } s
$$

{{% comment %}}SOURCE: SB ch.4 éq. 4.7-4.8 p.100{{% /comment %}}

Et si l'inégalité de gauche est **stricte** en un état, celle de droite est stricte en cet état aussi. L'amélioration locale se transmet globalement.

La démonstration tient en une idée : on déroule. Je vous en montre les deux premières lignes, parce que deux lignes suffisent à voir le mécanisme, et que les six suivantes sont la même ligne répétée.

$$
\begin{aligned}
v_\pi(s) &\le q_\pi\big(s, \pi'(s)\big)
  = \E\big[R_{t+1} + \gamma\, v_\pi(S_{t+1}) \mid S_t = s, A_t = \pi'(s)\big] \\[2pt]
&\le \E\big[R_{t+1} + \gamma\, q_\pi\big(S_{t+1}, \pi'(S_{t+1})\big) \mid S_t = s, A_t = \pi'(s)\big]
\end{aligned}
$$

On réapplique l'hypothèse à l'intérieur de l'espérance, ce qui fait apparaître une récompense de plus et repousse le \(v_\pi\) d'un pas ; on recommence ; à la limite, c'est \(v_{\pi'}(s)\) qui apparaît. Voilà. Retenez le geste, pas les huit lignes.

{{% comment %}}SOURCE: SB ch.4 p.100{{% /comment %}}

Reste à fabriquer une \(\pi'\) qui satisfait l'hypothèse. Il y a un choix évident, et c'est l'étape d'amélioration elle-même : prendre la politique **gloutonne** par rapport à \(v_\pi\).

$$
\begin{aligned}
\pi'(s) &\defeq \argmax_a q_\pi(s,a) \\[2pt]
&= \argmax_a \E\big[R_{t+1} + \gamma\, v_\pi(S_{t+1}) \mid S_t = s, A_t = a\big] \\[2pt]
&= \argmax_a \sum_{s',r} p(s',r \mid s,a)\big[\, r + \gamma\, v_\pi(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.4 éq. 4.9 p.101{{% /comment %}}

Les égalités se tranchent arbitrairement, et cette politique satisfait l'hypothèse du théorème **par construction** : elle choisit en chaque état l'action de plus grand \(q_\pi\), qui est donc au moins aussi bonne que celle que \(\pi\) choisissait. L'amélioration est donc gratuite et garantie.

{{% comment %}}SOURCE: SB ch.4 p.101{{% /comment %}}

Et que se passe-t-il si l'amélioration ne donne rien, si \(\pi'\) n'est pas meilleure que \(\pi\) ? Le raisonnement est joli : dans ce cas \(v_{\pi'} = v_\pi\), et en écrivant l'égalité, on constate que cette fonction satisfait l'équation d'**optimalité** de Bellman de la section 4.3. Par unicité, c'est donc \(v_*\), et les deux politiques étaient déjà optimales. Autrement dit : **l'amélioration produit une politique strictement meilleure, sauf lorsque la politique de départ était déjà optimale.** Il n'y a pas de plateau intermédiaire où l'on se bloquerait.

{{% comment %}}SOURCE: SB ch.4 p.101{{% /comment %}}

Un mot pour les politiques stochastiques, parce que la question se pose naturellement. Tout ce qui précède passe sans modification. En cas d'égalité entre plusieurs actions maximisantes, **n'importe quelle** répartition de probabilité entre elles est admissible, à la seule condition que les actions non maximisantes reçoivent une probabilité nulle.

{{% comment %}}SOURCE: SB ch.4 p.101{{% /comment %}}

> [!TIP]
 **Le pont avec la section 4.1, et il vaut la peine d'être explicité.** En 4.1, être glouton sur la **récompense immédiate** était un piège. En 4.3, être glouton sur \(v_*\) était optimal. Ici, être glouton sur \(v_\pi\) n'est ni l'un ni l'autre : ce n'est pas optimal, mais c'est **strictement meilleur**. Trois quantités, trois verdicts, et c'est l'échelle complète. Toute la programmation dynamique consiste à grimper cette échelle : glouton sur \(v_\pi\) donne une meilleure \(\pi\), dont le \(v_\pi\) est meilleur, sur lequel être glouton donne mieux encore. La boucle se referme dans la sous-section suivante.

---

## Itération sur la politique : évaluer, améliorer, recommencer

Nous avons deux mécanismes et ils s'emboîtent. L'évaluation produit \(v_\pi\) à partir de \(\pi\). L'amélioration produit une meilleure \(\pi\) à partir de \(v_\pi\). On alterne, et cela s'appelle l'**itération sur la politique** (*policy iteration*).

$$
\pi_0 \;\xrightarrow{\;E\;}\; v_{\pi_0} \;\xrightarrow{\;I\;}\; \pi_1
\;\xrightarrow{\;E\;}\; v_{\pi_1} \;\xrightarrow{\;I\;}\; \pi_2
\;\xrightarrow{\;E\;}\; \cdots \;\xrightarrow{\;I\;}\; \pi_* \;\xrightarrow{\;E\;}\; v_*
$$

Les \(E\) sont des évaluations complètes, les \(I\) des améliorations. Chaque politique de la chaîne est strictement meilleure que la précédente, sauf la dernière, qui est optimale.

Un argument de finitude clôt la question de la convergence, et il est imparable : un processus de décision markovien fini n'a qu'un **nombre fini** de politiques déterministes. Comme chaque itération produit une politique strictement meilleure, on ne peut pas tourner indéfiniment. L'itération sur la politique converge donc **en un nombre fini d'itérations**, et pas seulement « à la limite ».

{{% comment %}}SOURCE: SB ch.4 p.102{{% /comment %}}

Une remarque d'implémentation, qui change beaucoup le temps de calcul en pratique : chaque évaluation **repart de la fonction de valeur de l'itération précédente** au lieu de repartir de zéro. Comme les politiques successives se ressemblent, les valeurs aussi, et la nouvelle évaluation converge en bien moins de balayages que la première. C'est une optimisation d'une ligne pour un gain considérable.

{{% comment %}}SOURCE: SB ch.4 p.102{{% /comment %}}

Voici l'algorithme complet, en trois blocs numérotés : initialisation, évaluation, amélioration.

```
Itération sur la politique (avec évaluation itérative), pour estimer π ≈ π_*

1. Initialisation
   V(s) ∈ ℝ et π(s) ∈ A(s) arbitrairement, pour tout s ∈ S

2. Évaluation de la politique
   Répéter :
       Δ ← 0
       Pour chaque s ∈ S :
           v ← V(s)
           V(s) ← Σ_{s',r} p(s',r|s,π(s)) [ r + γ V(s') ]
           Δ ← max(Δ, |v − V(s)|)
   jusqu'à Δ < ϑ (un petit seuil positif qui fixe la précision de l'estimation)

3. Amélioration de la politique
   politique-stable ← vrai
   Pour chaque s ∈ S :
       ancienne-action ← π(s)
       π(s) ← argmax_a Σ_{s',r} p(s',r|s,a) [ r + γ V(s') ]
       Si ancienne-action ≠ π(s), alors politique-stable ← faux
   Si politique-stable, s'arrêter et renvoyer V ≈ v_* et π ≈ π_* ;
   sinon, retourner en 2
```

Deux détails de cet encadré méritent qu'on s'y arrête, parce qu'ils ne se devinent pas. Dans le bloc 2, la somme sur les actions a disparu : la politique évaluée ici est **déterministe**, donc \(\sum_a \pi(a \mid s)\) se réduit au seul terme \(\pi(s)\). Et le test d'arrêt du bloc 3 ne porte pas sur les valeurs mais sur les **actions** : on s'arrête quand plus aucun état ne change d'action, ce qui n'est pas le \(\Delta < \vartheta\) de la boucle d'évaluation située quatre lignes plus haut. Deux critères d'arrêt différents dans le même algorithme, et ils mesurent deux choses différentes.

{{% comment %}}SOURCE: SB ch.4 p.102{{% /comment %}}

En pratique, cette méthode converge remarquablement vite. Sur la grille de quatre cases sur quatre de la Figure 4-6, par exemple, elle trouverait l'optimum **après une seule itération**, puisque nous avons vu que la politique gloutonne est déjà optimale très tôt. Et c'est exactement ce constat qui va nous faire franchir le dernier pas.

{{% comment %}}SOURCE: SB ch.4 p.103-104{{% /comment %}}

> [!WARNING]
 **Attention au coût caché de cette méthode, parce que c'est lui qui motive la suite.** Chaque \(E\) de la chaîne ci-dessus est une **évaluation menée jusqu'à convergence**, donc une boucle de balayages, chacun parcourant tous les états. L'itération sur la politique est une boucle à l'intérieur d'une boucle. Et nous venons de constater, sur la Figure 4-6, que la précision obtenue par ces balayages est en grande partie **inutile** : la politique gloutonne se stabilise bien avant les valeurs. Nous payons donc très cher une exactitude qui ne change aucune décision.

---

## Itération sur la valeur : tronquer l'évaluation à un seul balayage

Le dernier pas, et il est court. Puisque l'évaluation complète est un gaspillage, tronquons-la. La bonne nouvelle est que la troncature **ne coûte pas la garantie de convergence** : on peut interrompre l'évaluation après un nombre fini de balayages et continuer d'alterner, l'ensemble converge toujours vers \(\pi_*\) et \(v_*\).

Et le cas particulier important est le plus brutal de tous : **arrêter l'évaluation après un seul balayage**. Un balayage d'évaluation, une amélioration, un balayage d'évaluation, une amélioration. Si l'on écrit ce qu'une telle alternance fait à la table, les deux étapes fusionnent en une seule formule, et cette formule est l'**itération sur la valeur** (*value iteration*).

{{% comment %}}SOURCE: SB ch.4 p.105{{% /comment %}}

Je vous la donne juste en dessous de la mise à jour d'évaluation, et je vous demande de les comparer symbole par symbole.

$$
\begin{aligned}
v_{k+1}(s) &\defeq \E_\pi\big[R_{t+1} + \gamma\, v_k(S_{t+1}) \mid S_t = s\big] \\[2pt]
&= \sum_a \pi(a \mid s) \sum_{s',r} p(s',r \mid s,a)
   \big[\, r + \gamma\, v_k(s') \,\big]
\end{aligned}
$$

$$
\begin{aligned}
v_{k+1}(s) &\defeq \max_a \E\big[R_{t+1} + \gamma\, v_k(S_{t+1}) \mid S_t = s, A_t = a\big] \\[2pt]
&= \max_a \sum_{s',r} p(s',r \mid s,a)
   \big[\, r + \gamma\, v_k(s') \,\big]
\end{aligned}
$$

{{% comment %}}SOURCE: SB ch.4 éq. 4.5 p.96, éq. 4.10 p.105{{% /comment %}}

Deux phrases, et la section est faite.

La première : la seconde formule est **identique à la première, au \(\max_a\) près**. La somme pondérée par la politique est remplacée par un maximum. C'est tout ce qui a changé, et c'est pour cela que l'amélioration a disparu en tant qu'étape séparée : le \(\max\) **est** l'amélioration, repliée dans le balayage.

La seconde : la formule de l'itération sur la valeur est l'**équation d'optimalité de Bellman transformée en règle de mise à jour**. Revenez à la section 4.3 et comparez : c'est, au signe de la flèche près, exactement l'équation que nous avions écrite pour caractériser \(v_*\). La clé de lecture de l'ouverture de cette section vient de payer pour la quatrième fois.

{{% comment %}}SOURCE: SB ch.4 p.105{{% /comment %}}

Un point de discipline, que ce cours tient et que beaucoup d'implémentations relâchent : la boucle produit \(V\), et c'est **une passe finale séparée**, un \(\argmax\) sur tous les états, qui produit la politique. Les deux ne sont pas mélangées. C'est plus clair à lire, et surtout cela rend visible ce que la boucle calcule réellement, à savoir une **table de valeurs** et non une politique.

{{% comment %}}SOURCE: SB ch.4 p.105{{% /comment %}}

```
Itération sur la valeur, pour estimer π ≈ π_*

Paramètre de l'algorithme : un petit seuil ϑ > 0 qui fixe la précision de l'estimation
Initialiser V(s), pour tout s ∈ S⁺, arbitrairement sauf V(terminal) = 0

Répéter :
    Δ ← 0
    Pour chaque s ∈ S :
        v ← V(s)
        V(s) ← max_a Σ_{s',r} p(s',r|s,a) [ r + γ V(s') ]
        Δ ← max(Δ, |v − V(s)|)
jusqu'à Δ < ϑ

Produire une politique déterministe π ≈ π_* telle que
    π(s) = argmax_a Σ_{s',r} p(s',r|s,a) [ r + γ V(s') ]
```

{{% comment %}}SOURCE: SB ch.4 p.105{{% /comment %}}

Et le code, à mettre côte à côte avec celui de l'évaluation de politique. Je vous laisse chercher la différence pendant dix secondes avant de lire la phrase qui suit le fragment.

```python
def iteration_valeur(p, r, n_etats, n_actions):
    """Itération sur la valeur : la boucle produit V, la passe finale produit pi."""

    def promesse(s, a, V):
        """La somme sur les successeurs, pour une action donnée."""
        return sum(p[s, a, s2] * (r[s, a, s2] + GAMMA * V[s2])
                   for s2 in range(n_etats))

    V = np.zeros(n_etats)
    while True:
        delta = 0.0
        for s in range(n_etats):
            v = V[s]
            V[s] = max(promesse(s, a, V) for a in range(n_actions))   # LE max
            delta = max(delta, abs(v - V[s]))
        if delta < VARTHETA:
            break

    pi = np.zeros(n_etats, dtype=int)        # passe finale, SÉPARÉE de la boucle
    for s in range(n_etats):
        pi[s] = int(np.argmax([promesse(s, a, V) for a in range(n_actions)]))
    return V, pi
```

La différence avec `evaluer_politique` tient en un appel de fonction : `sum(pi[s, a] * ...)` est devenu `max(...)`. Une somme pondérée est devenue un maximum. C'est, trait pour trait, la différence entre les deux équations ci-dessus, et c'est tout ce qui sépare « évaluer une politique donnée » de « trouver la meilleure ».

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(V(s)\) | estimation tabulaire, la seule chose que la boucle calcule | `V[s]` |
| \(\sum_{s',r} p(s',r \mid s,a)[r + \gamma V(s')]\) | la promesse de l'action \(a\) en \(s\) | `promesse(s, a, V)` |
| \(\max_a\) de l'itération sur la valeur | l'amélioration, repliée dans le balayage | `max(...)` |
| \(\argmax_a\) | la politique gloutonne extraite de \(V\) | `np.argmax([...])`, dans la passe finale |
| \(\vartheta\) | seuil de convergence | `VARTHETA` |
| \(\pi \approx \pi_*\) | la politique déterministe produite en sortie | `pi`, un tableau d'entiers |

Une dernière idée, en une phrase, parce qu'elle nomme ce que nous venons de faire quatre fois. Évaluation et amélioration peuvent interagir à **n'importe quelle granularité** : balayage complet contre balayage complet, un balayage contre un, ou même un seul état contre un seul état. Toutes ces variantes convergent, et elles ne se stabilisent toutes qu'à l'optimum, puisque c'est le seul point où l'amélioration ne change plus rien. On appelle ce schéma général l'**itération généralisée de politique** (*generalized policy iteration*, GPI), et vous allez le reconnaître dans toutes les méthodes du cours, jusqu'aux acteurs-critiques de la semaine 8.

{{% comment %}}SOURCE: SB ch.4 p.108{{% /comment %}}
