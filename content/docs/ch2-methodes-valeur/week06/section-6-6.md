---
title: "6.6 Défaut nº5, la cible à un pas : le DQN à n étapes"
weight: 7
---

## Déplier Bellman, et payer le dépliage

Reprenons le cinquième défaut de la semaine 5, dans les termes où je l'avais posé. Une récompense obtenue à la trame 1 000 ne remonte vers la trame 999 qu'à la mise à jour suivante, puis vers la trame 998 à celle d'après. L'information se propage d'**un pas par pas d'apprentissage**, et c'est lent.

L'idée qui répare cela est ancienne : elle date des premiers travaux sur la prédiction par différences temporelles, à la fin des années 1980, et elle consiste en un **déroulement de l'équation de Bellman** (*Bellman unrolling*), que j'appellerai aussi son dépliage, au lieu d'une seule application. La méthode qui en résulte s'appelle le **DQN à n étapes** (*n-step DQN*).

{{% comment %}}SOURCE: LAPAN ch.8 p.241{{% /comment %}}

Partons de la cible que vous connaissez, celle de la semaine 5, où \(Q_{\theta^-}\) est le réseau cible :

$$
Q_\theta(s_t,a_t) \;=\; r_t + \gamma \max_{a} Q_{\theta^-}(s_{t+1},a)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.247{{% /comment %}}

Maintenant, remarquez une chose : le terme \(Q_{\theta^-}(s_{t+1},a)\) est lui-même une valeur d'action, donc il obéit à la même équation. Substituons-la :

$$
Q_\theta(s_t,a_t) \;=\; r_t + \gamma \max_{a}\Big[\,
 r_{a,t+1} + \gamma \max_{a'} Q_{\theta^-}(s_{t+2},a') \,\Big]
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.241{{% /comment %}}

Ici \(r_{a,t+1}\) est la récompense immédiate obtenue en jouant l'action \(a\) depuis \(s_{t+1}\). Cette équation est **exacte** et elle est inutilisable : le maximum extérieur exige de connaître la récompense de chaque action possible au pas \(t+1\), ce que notre tampon de rejeu ne contient pas. Il ne contient qu'une chose, l'action que l'agent a **effectivement** jouée.

Alors on fait l'approximation, et il faut la regarder en face parce qu'elle est tout le contenu de la section. On suppose que l'action jouée au pas \(t+1\) était la bonne, c'est-à-dire que le maximum extérieur est atteint par l'action du tampon. Le \(\max_a\) intermédiaire disparaît :

$$
Q_\theta(s_t,a_t) \;=\; r_t + \gamma\,r_{t+1} +
 \gamma^2 \max_{a'} Q_{\theta^-}(s_{t+2},a')
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.241{{% /comment %}}

Et en répétant l'opération \(n\) fois, on obtient la cible à \(n\) étapes, qui est celle que le code calculera :

$$
y_i \;=\; \sum_{k=0}^{n-1}\gamma^k\,r_{t+k}
 \;+\; \gamma^{n} \max_{a'} Q_{\theta^-}(s_{t+n},a')
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.241-242, p.244{{% /comment %}}

Trois équations, et je vous demande de retenir laquelle est l'approximation. Ce n'est pas la dernière : la dernière n'est que la deuxième répétée. C'est le passage de la deuxième à la troisième, le moment où un \(\max\) a été remplacé par ce que l'agent avait sous la main. Nous allons payer ce passage dans deux paragraphes.

---

## Pourquoi c'est plus rapide : une chaîne de quatre états

Voici l'argument, et il tient sur un exemple de quatre états. Une chaîne \(s_1 \to s_2 \to s_3 \to s_4\), une seule action possible dans chaque état, les récompenses \(r_1\), \(r_2\), \(r_3\) sur les transitions, et \(s_4\) terminal. La **Figure 6-1** la montre telle quelle.

{{< bookfig src="06-01.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.242{{% /comment %}}

Avec une seule action par état, il n'y a aucun choix à faire : la valeur de chaque état est entièrement déterminée par les récompenses qui suivent. L'agent n'a donc rien à apprendre sur la politique, seulement à propager des nombres. Regardons combien de balayages il lui faut.

| À un pas | À deux pas |
| --- | --- |
| \(Q(s_1,a) \leftarrow r_1 + \gamma\,Q(s_2,a)\) | \(Q(s_1,a) \leftarrow r_1 + \gamma\,r_2 + \gamma^2 Q(s_3,a)\) |
| \(Q(s_2,a) \leftarrow r_2 + \gamma\,Q(s_3,a)\) | \(Q(s_2,a) \leftarrow r_2 + \gamma\,r_3\) |
| \(Q(s_3,a) \leftarrow r_3\) | \(Q(s_3,a) \leftarrow r_3\) |

{{% comment %}}SOURCE: LAPAN ch.8 p.242{{% /comment %}}

Lisez la colonne de gauche de bas en haut. Au premier balayage, seule la troisième ligne est utile : \(Q(s_3,a)\) devient correct, parce que \(r_3\) est la récompense finale et qu'il n'y a rien après. Les deux premières lignes, elles, ont amorcé sur des valeurs encore fausses. Il faut un deuxième balayage pour que \(Q(s_2,a)\) devienne correct, et un troisième pour \(Q(s_1,a)\). **Trois balayages pour propager l'information dans une chaîne de trois transitions**, et c'est le meilleur cas possible : une seule action, aucun bruit, aucune exploration.

{{% comment %}}SOURCE: LAPAN ch.8 p.242{{% /comment %}}

Maintenant la colonne de droite. Dès le premier balayage, \(Q(s_2,a)\) et \(Q(s_3,a)\) sont corrects, puisque leurs cibles ne contiennent que des récompenses réelles. Il ne reste que \(Q(s_1,a)\), qui devient correct au deuxième. **Deux balayages au lieu de trois**, et sur une chaîne plus longue l'écart se creuse proportionnellement à \(n\).

C'est tout le bénéfice, et il est réel : moins de pas d'apprentissage pour le même résultat, c'est-à-dire une meilleure **efficacité d'échantillon** (*sample efficiency*).

---

## Et maintenant le prix, qui est de devenir à moitié sur politique

Si déplier sur deux pas accélère, pourquoi ne pas déplier sur cent ?

Revenons à l'approximation. Pour supprimer le \(\max\) intermédiaire, nous avons supposé que l'action jouée au pas suivant était l'action optimale. Au début de l'entraînement, la politique de comportement est quasi aléatoire : cette supposition est fausse presque partout. Et chaque pas de dépliage supplémentaire ajoute une supposition de ce genre. Autrement dit, plus on déplie l'équation de Bellman, plus la mise à jour peut être fausse.

{{% comment %}}SOURCE: LAPAN ch.8 p.243{{% /comment %}}

Le tampon de rejeu aggrave la chose, et c'est le point que je veux que vous reteniez de cette section. Un tampon contient des transitions produites par des politiques **anciennes**, donc moins bonnes. Plus le tampon est grand, plus la probabilité de tirer une sous-trajectoire jouée par une mauvaise politique est élevée, et plus l'approximation du dépliage est violée.

{{% comment %}}SOURCE: LAPAN ch.8 p.243{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que c'est la seule interaction négative entre deux réparations de cette semaine, et qu'elle contredit en partie ce que je vous ai annoncé en introduction.** La réparation du défaut nº5 abîme la réparation que la semaine 5 avait installée pour la corrélation des données. Le dépliage veut des données **fraîches**, le tampon de rejeu existe pour en garder des **anciennes**, et les deux tirent en sens contraire. Les cinq réparations de cette semaine s'empilent, c'est vrai, et celle-ci est la nuance : elle s'empile en se contredisant un peu. Nous y reviendrons en section 6.11.

Il vaut la peine de nommer proprement ce qui vient de se passer, parce que cet axe va structurer tout le module 3. Une méthode **hors politique** (*off-policy*) ne dépend pas de la fraîcheur des données : c'est exactement ce qui autorise un grand tampon de rejeu, et c'est pour cela que le Q-learning en tolère un. Une méthode **sur politique** (*on-policy*), à l'inverse, exige que les données soient échantillonnées selon la politique courante, et son coût est connu : il faut jeter les données après usage, donc interagir beaucoup. L'image qui fixe l'idée est celle d'une voiture autonome : avec une méthode purement sur politique, il faut beaucoup de voitures accidentées avant que le système apprenne que les murs et les arbres sont des choses à éviter.

{{% comment %}}SOURCE: LAPAN ch.8 p.243{{% /comment %}}

Le dépliage de Bellman rend donc notre DQN **partiellement** sur politique. En pratique les choses ne sont pas noires ou blanches : un peu de dépliage est presque toujours rentable, beaucoup ne l'est jamais. La consigne pratique est d'être modeste dans le choix de \(n\), et les valeurs 2 ou 3 fonctionnent généralement bien.

{{% comment %}}SOURCE: LAPAN ch.8 p.243-244{{% /comment %}}

---

## L'implémentation, en deux paramètres et un piège

Voici le moment où la section 6.3 est encaissée. Le DQN à \(n\) étapes demande deux changements, et aucun n'est une ligne de logique.

```python
# 1. La source d'expérience replie n pas en une transition premier-dernier.
source = SourcePremierDernier(env, agent, gamma=GAMMA, steps_count=N_PAS)

# 2. LE PIÈGE : la perte doit actualiser l'état final par gamma PUISSANCE n.
perte = calculer_perte(lot, reseau, reseau_cible,
                       gamma=GAMMA ** N_PAS,      # et NON gamma
                       peripherique=peripherique)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(n\) | profondeur de dépliage | `steps_count=N_PAS` |
| \(\sum_{k=0}^{n-1}\gamma^k r_{t+k}\) | récompense accumulée et actualisée | `transition.recompense`, calculée par la source |
| \(s_{t+n}\) | état après \(n\) pas | `transition.etat_final` |
| \(\gamma^n\) | actualisation de l'état final | `GAMMA ** N_PAS` |
| \(\gamma\) | le facteur du cas à un pas | `GAMMA`, qui reste dans la source |

> [!WARNING]
 **Attention, ce piège est le plus coûteux de la semaine et il ne lève aucune exception.** La source d'expérience actualise les récompenses intermédiaires avec \(\gamma\), c'est son travail. Mais le terme d'amorçage de la perte porte sur un état situé \(n\) pas plus loin : il doit donc être actualisé par \(\gamma^n\). Si vous laissez \(\gamma\) dans la perte, tout tourne, rien ne plante, les courbes montent un peu, et votre agent apprend une fonction de valeur qui n'est celle d'aucun problème. Avec \(\gamma = 0{,}99\) et \(n = 3\), l'écart entre 0,99 et 0,970 est assez petit pour passer inaperçu sur CartPole et assez grand pour abîmer la convergence sur un problème à long horizon. Écrivez-le une fois pour toutes dans votre socle commun, et faites de \(n\) le seul paramètre que la variante expose.

{{% comment %}}SOURCE: LAPAN ch.8 p.244{{% /comment %}}

Et les chiffres de référence, avec l'avertissement de la section 6.5 toujours valable. Sur le jeu de référence, \(n = 3\) converge nettement plus vite que la version à un pas ; \(n = 4\) apporte moins ; \(n = 5\) et \(n = 6\) sont **moins bons** que la référence. Après réglage des hyperparamètres pour chaque valeur de \(n\), le nombre de parties nécessaires dessine la même courbe en U.

| \(n\) | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- |
| parties | 293 | **260** | 290 | 268 | 261 | 284 |

{{% comment %}}SOURCE: LAPAN ch.8 p.245, p.246{{% /comment %}}

Contre 400 parties pour la référence, le gain est net et il est loin d'être proportionnel à \(n\). Regardez surtout la forme de la ligne : elle ne décroît pas, elle a un creux. C'est la signature du marché que nous venons de décrire, de la vitesse de propagation d'un côté et de la fausseté croissante de l'approximation de l'autre.

---
