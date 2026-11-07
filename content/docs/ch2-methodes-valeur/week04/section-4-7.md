---
title: "4.7 Contrôle : Sarsa, Q-learning et la méthode ε-gloutonne"
weight: 8
---

## Du v au q, parce qu'on veut agir et non seulement prédire

TD(0) évalue une politique. Nous voulons en trouver une bonne. Ce passage de la prédiction au **contrôle** suit exactement le schéma de la section 4.4 : on alterne évaluation et amélioration, c'est-à-dire l'itération généralisée de politique, et l'on met TD dans l'emplacement de l'évaluation.

Premier changement, et il est obligatoire : on estime désormais \(q_\pi\) plutôt que \(v_\pi\). La raison est celle de la section 4.3, et elle est maintenant doublement contraignante : sans modèle, on ne peut pas améliorer une politique à partir de \(V\), puisque comparer deux actions demanderait de savoir où elles mènent. Avec \(Q\), l'amélioration est une lecture de table.

{{% comment %}}SOURCE: SB ch.6 p.151{{% /comment %}}

Est-ce légitime du point de vue des garanties de convergence ? Oui, et l'argument est joli : une suite de **couples état-action** forme, elle aussi, une chaîne de Markov, avec son propre processus de récompense. Les théorèmes de convergence de TD(0) s'appliquent donc mot pour mot, en remplaçant simplement « état » par « couple état-action ». On ne refait aucune théorie, on change le nom des nœuds.

{{% comment %}}SOURCE: SB ch.6 p.151{{% /comment %}}

Second changement, et il est plus délicat : l'agent doit maintenant **explorer**. En section 4.5, l'exploration était fournie par cent pas aléatoires séparés de la décision. Ici, il n'y a plus de phase séparée : c'est la politique elle-même qui engendre les données. Il faut donc une politique qui exploite ce qu'elle sait **et** essaie de temps en temps autre chose. Et selon la façon dont on gère ce compromis, on obtient deux familles de méthodes : **sur politique** et **hors politique**, les deux axes de la semaine 3 qui reviennent ici en pleine lumière.

{{% comment %}}SOURCE: SB ch.6 p.151{{% /comment %}}

---

## La méthode ε-gloutonne, en deux lignes

Avant les deux algorithmes, il nous faut la politique d'exploration qu'ils utilisent tous les deux. Elle est si simple que je vous la donne entière, et je la définis ici parce que c'est l'endroit où le cours en a besoin.

La **méthode \(\varepsilon\)-gloutonne** (*epsilon-greedy*) consiste à jouer l'action gloutonne la plupart du temps, et à tirer une action au hasard le reste du temps. C'est tout.

$$
A_t =
\begin{cases}
\argmax_a Q(S_t, a) & \text{avec probabilité } 1 - \varepsilon, \\[4pt]
\text{une action tirée uniformément dans } \mathcal{A}(S_t)
  & \text{avec probabilité } \varepsilon.
\end{cases}
$$

Le paramètre \(\varepsilon\) est le taux d'exploration, et il vit dans \([0,1]\). À \(\varepsilon = 0\), la politique est purement gloutonne et n'explore jamais. À \(\varepsilon = 1\), elle est purement aléatoire et n'exploite jamais. En pratique, on prend une petite valeur, typiquement **0,1**, parfois décroissante au cours de l'entraînement.

```python
def choisir_action_epsilon(q, etat, n_actions, epsilon):
    """Politique ε-gloutonne dérivée de la table Q."""
    if np.random.random() < epsilon:
        return int(np.random.randint(n_actions))      # exploration : tirage uniforme
    return int(np.argmax(q[etat]))                    # exploitation : la meilleure case
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\varepsilon\) | taux d'exploration | `epsilon` |
| \(\argmax_a Q(s,a)\) | l'action gloutonne, lue dans la table | `np.argmax(q[etat])` |
| tirage uniforme dans \(\mathcal{A}(s)\) | l'exploration | `np.random.randint(n_actions)` |

Deux remarques sur ce fragment de huit lignes, et la seconde explique pourquoi je l'ai mis en avant.

D'abord, l'exploration n'est pas gratuite, même quand elle ne sert plus à rien. Prenez un monde en grille appelé **grille ventée** (*windy gridworld*), où un courant ascendant pousse l'agent vers le haut dans certaines colonnes. Avec \(\varepsilon = 0{,}1\), \(\alpha = 0{,}5\) et une table initialisée à zéro, la politique gloutonne y est optimale depuis longtemps au bout de huit mille pas de temps. Et pourtant la longueur moyenne des épisodes se stabilise autour de **17 pas, alors que le minimum est de 15**. Les deux pas d'écart sont le prix permanent de \(\varepsilon\) : une fois sur dix, l'agent fait exprès n'importe quoi.

{{% comment %}}SOURCE: SB ch.6 p.152{{% /comment %}}

> [!WARNING]
 **Attention, \(\varepsilon\) est un impôt, et il se paie même sur une politique parfaite.** Beaucoup de courbes d'apprentissage décevantes s'expliquent par cette seule ligne : la politique **apprise** est excellente, et la politique **jouée** est celle qui explore encore. Quand vous évaluerez un agent dans ce cours, posez-vous toujours la question « est-ce que je mesure la politique gloutonne, ou la politique \(\varepsilon\)-gloutonne ? ». Ce ne sont pas les mêmes, et la section sur la falaise, en fin de semaine, en fait un cas d'école. Au passage, notez que la grille ventée est aussi un environnement où une méthode de Monte-Carlo ne peut même pas être employée : la terminaison n'y est pas garantie pour toutes les politiques, et une méthode qui attend la fin de l'épisode peut donc attendre pour toujours.

{{% comment %}}SOURCE: SB ch.6 p.152{{% /comment %}}

Ensuite, et je préfère vous le dire franchement : la théorie complète de ce compromis, avec ses variantes et ses bornes, appartient au cadre des bandits manchots, que ce cours ne traite pas. Nous prenons donc la méthode \(\varepsilon\)-gloutonne pour ce qu'elle est, l'outil d'exploration le plus simple qui fonctionne, et nous reviendrons sur ses **limites** en semaine 11, quand nous aurons des environnements qu'elle ne sait pas explorer.

---

## Sarsa : le quintuplet qui donne son nom à la méthode

Premier algorithme de contrôle. On applique TD(0) à la table \(Q\) au lieu de la table \(V\), et la règle de mise à jour s'écrit directement.

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t) +
  \alpha\big[\, R_{t+1} + \gamma\, Q(S_{t+1},A_{t+1}) - Q(S_t,A_t) \,\big]
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.7 p.151{{% /comment %}}

Et si \(S_{t+1}\) est terminal, on pose \(Q(S_{t+1}, A_{t+1}) \defeq 0\), comme toujours.

Regardez les symboles qui interviennent dans cette mise à jour : \(S_t\), \(A_t\), \(R_{t+1}\), \(S_{t+1}\), \(A_{t+1}\). Un quintuplet. C'est exactement de là que vient le nom **Sarsa**, qui n'est donc pas un acronyme savant mais la liste des cinq choses dont la formule a besoin.

Notez bien la cinquième, parce qu'elle contient toute la personnalité de la méthode : il faut \(A_{t+1}\), l'action que l'agent va **effectivement** jouer au pas suivant. On doit donc l'avoir déjà choisie, avec la politique \(\varepsilon\)-gloutonne, avant de pouvoir mettre à jour. La cible de Sarsa dépend de la politique de comportement : Sarsa est une méthode **sur politique**.

{{% comment %}}SOURCE: SB ch.6 p.151{{% /comment %}}

Sur la convergence, l'énoncé est le suivant : Sarsa converge avec probabilité 1 vers la politique optimale et vers la fonction de valeur d'action optimale, à deux conditions. Il faut que **tous les couples état-action soient visités une infinité de fois**, et il faut que la politique **converge vers la politique gloutonne**. La seconde condition se satisfait très simplement en faisant décroître \(\varepsilon\), par exemple en posant \(\varepsilon = 1/t\).

{{% comment %}}SOURCE: SB ch.6 p.151-152{{% /comment %}}

```
Sarsa (contrôle TD sur politique), pour estimer Q ≈ q_*

Paramètres de l'algorithme : pas d'apprentissage α ∈ (0, 1], petit ε > 0
Initialiser Q(s,a), pour tout s ∈ S⁺ et tout a ∈ A(s), arbitrairement
    sauf Q(terminal, ·) = 0

Pour chaque épisode :
    Initialiser S
    Choisir A depuis S selon une politique dérivée de Q (par exemple ε-gloutonne)
    Pour chaque pas de l'épisode :
        Exécuter A, observer R et S'
        Choisir A' depuis S' selon une politique dérivée de Q (par exemple ε-gloutonne)
        Q(S,A) ← Q(S,A) + α [ R + γ Q(S',A') − Q(S,A) ]
        S ← S' ; A ← A'
    jusqu'à ce que S soit terminal
```

{{% comment %}}SOURCE: SB ch.6 p.152{{% /comment %}}

---

## Q-learning : un seul symbole change, et la méthode change de famille

Second algorithme, et c'est celui qui donne son nom à la moitié du cours.

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t) +
  \alpha\Big[\, R_{t+1} + \gamma \max_a Q(S_{t+1},a) - Q(S_t,A_t) \,\Big]
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.8 p.153{{% /comment %}}

Mettez cette ligne au-dessus de celle de Sarsa et cherchez la différence. Il y en a **une** : \(Q(S_{t+1}, A_{t+1})\) est devenu \(\max_a Q(S_{t+1}, a)\). L'action réellement jouée au pas suivant a été remplacée par la **meilleure** action du pas suivant, qu'elle soit jouée ou non.

C'est tout. Et cette substitution unique fait basculer la méthode d'une famille à l'autre.

> [!IMPORTANT]
 **Je dois insister, parce que c'est la définition de « hors politique » la plus concrète que ce cours puisse vous donner.** La cible de Sarsa contient l'action que l'agent va jouer ; elle évalue donc la politique que l'agent suit, exploration comprise. La cible de Q-learning contient le \(\max\) ; elle évalue donc la politique **gloutonne**, que l'agent ne suit pas. Conséquence, et elle est remarquable : le \(Q\) appris par Q-learning approche **directement \(q_*\)**, **indépendamment de la politique suivie**. La politique suivie ne décide plus de ce qui est appris : elle décide seulement **quels couples sont visités**. Vous pouvez explorer n'importe comment, ou apprendre des données d'un autre agent, et c'est toujours \(q_*\) que vous estimez. Voilà la liberté que la semaine 3 avait annoncée sans la montrer, et c'est exactement elle qui rendra possible le tampon de rejeu de la semaine 5.

{{% comment %}}SOURCE: SB ch.6 p.153{{% /comment %}}

La garantie de convergence s'énonce alors sans la seconde condition de Sarsa : Q-learning converge vers \(q_*\) avec probabilité 1, sous les conditions usuelles sur la suite des pas d'apprentissage, **à la seule condition que tous les couples état-action continuent d'être mis à jour**. On n'exige plus que la politique converge vers la gloutonne, puisque la cible ne dépend plus de la politique.

{{% comment %}}SOURCE: SB ch.6 p.153{{% /comment %}}

Voici les deux encadrés l'un sous l'autre. Je vous demande de les lire côte à côte avant de lire mon commentaire.

```
Q-learning (contrôle TD hors politique), pour estimer π ≈ π_*

Paramètres de l'algorithme : pas d'apprentissage α ∈ (0, 1], petit ε > 0
Initialiser Q(s,a), pour tout s ∈ S⁺ et tout a ∈ A(s), arbitrairement
    sauf Q(terminal, ·) = 0

Pour chaque épisode :
    Initialiser S
    Pour chaque pas de l'épisode :
        Choisir A depuis S selon une politique dérivée de Q (par exemple ε-gloutonne)
        Exécuter A, observer R et S'
        Q(S,A) ← Q(S,A) + α [ R + γ max_a Q(S',a) − Q(S,A) ]
        S ← S'
    jusqu'à ce que S soit terminal
```

{{% comment %}}SOURCE: SB ch.6 p.153{{% /comment %}}

Deux différences, et deux seulement.

La première est la **position du choix d'action**. Chez Sarsa, le choix de la première action se fait **avant** la boucle interne, et le choix de l'action suivante se fait **à l'intérieur**, parce que la mise à jour en a besoin. Chez Q-learning, le choix se fait au début de chaque pas, et il n'y a plus de « action suivante » à transporter d'un pas à l'autre. Le code de Q-learning est donc structurellement plus simple : une variable de moins à faire survivre.

La seconde est le \(\max_a\) qui remplace \(Q(S',A')\). C'est la seule différence de contenu.

Passons au code, les deux fonctions côte à côte.

```python
def q_learning(env, n_episodes, alpha=0.5, gamma=1.0, epsilon=0.1):
    """HORS politique : la cible prend le max, quelle que soit l'action jouée."""
    n_a = env.action_space.n
    q = np.zeros((env.observation_space.n, n_a))

    for _ in range(n_episodes):
        etat, _ = env.reset()
        while True:
            action = choisir_action_epsilon(q, etat, n_a, epsilon)
            suivant, recompense, terminated, truncated, _ = env.step(action)

            cible_future = 0.0 if terminated else q[suivant].max()      # LE max
            erreur_td = recompense + gamma * cible_future - q[etat, action]
            q[etat, action] += alpha * erreur_td

            etat = suivant
            if terminated or truncated:
                break
    return q


def sarsa(env, n_episodes, alpha=0.5, gamma=1.0, epsilon=0.1):
    """SUR politique : la cible prend l'action qui sera réellement jouée."""
    n_a = env.action_space.n
    q = np.zeros((env.observation_space.n, n_a))

    for _ in range(n_episodes):
        etat, _ = env.reset()
        action = choisir_action_epsilon(q, etat, n_a, epsilon)      # A, avant la boucle
        while True:
            suivant, recompense, terminated, truncated, _ = env.step(action)
            suivante = choisir_action_epsilon(q, suivant, n_a, epsilon)   # A', dedans

            cible_future = 0.0 if terminated else q[suivant, suivante]    # PAS de max
            erreur_td = recompense + gamma * cible_future - q[etat, action]
            q[etat, action] += alpha * erreur_td

            etat, action = suivant, suivante
            if terminated or truncated:
                break
    return q
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q(S,A)\) | la table, indexée par état et action | `q[etat, action]`, un tableau de forme `(n_etats, n_actions)` |
| \(\alpha\) | pas d'apprentissage, \(\alpha \in (0,1]\) | `alpha` |
| \(\gamma\) | facteur d'actualisation | `gamma` |
| \(R\) | récompense de la transition unique | `recompense`, renvoyée par `env.step()` |
| \(S'\) | état suivant | `suivant` |
| \(\max_a Q(S',a)\) | la cible **hors politique** : la meilleure action suivante, jouée ou non | `q[suivant].max()` |
| \(Q(S',A')\) | la cible **sur politique** : l'action effectivement choisie ensuite | `q[suivant, suivante]` |
| \(\delta\) | erreur TD, le crochet | `erreur_td` |
| \(\varepsilon\) | taux d'exploration de la politique \(\varepsilon\)-gloutonne | `epsilon` |
| \(\leftarrow\) | affectation **sur place**, et **non** un pas de gradient | `q[etat, action] += alpha * erreur_td` |

Je veux que vous lisiez la dernière ligne de ce tableau à voix haute, parce qu'elle mesure très exactement la distance qui nous sépare de la semaine prochaine. Cette semaine, la mise à jour **écrit dans une case**. Une case, une valeur, aucun effet sur les autres cases. La semaine prochaine, la mise à jour **descendra un gradient** : elle modifiera des poids partagés, et chaque modification déplacera donc, un peu, **toutes** les valeurs à la fois. C'est toute la différence entre \(V\) et \(\hat v(s,\mathbf{w})\), et c'est de là que viendront à la fois la puissance de la semaine 5 et ses instabilités.

---

## La falaise, où la meilleure politique obtient le pire score

Nous terminons sur l'expérience que je trouve la plus instructive de toute la semaine, et c'est la pièce centrale du laboratoire.

L'environnement s'appelle la **marche au bord de la falaise** (*cliff walking*). C'est un monde en grille épisodique et non actualisé. Le départ et l'objectif sont tous deux sur la **rangée du bas**, et entre eux, sur cette même rangée, s'étend « la falaise ». Chaque transition rapporte **−1**. Entrer dans la falaise rapporte **−100** et renvoie immédiatement l'agent à la case de départ, sans terminer l'épisode. La **Figure 4-8** montre la grille et les deux chemins dont nous allons parler.

{{< bookfig src="04-08.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}

Entraînons les deux méthodes sur cet environnement, toutes deux avec une sélection \(\varepsilon\)-gloutonne à \(\varepsilon = 0{,}1\). Et voici ce qu'elles apprennent.

**Q-learning apprend les valeurs de la politique optimale**, qui consiste à longer le bord de la falaise, au plus court. C'est bien la meilleure politique : le chemin le plus court coûte le moins de −1. Et comme l'agent joue, lui, la politique \(\varepsilon\)-gloutonne, une fois sur dix il fait un pas au hasard, et comme il marche au bord du gouffre, ce pas au hasard le fait régulièrement **tomber**. Chaque chute coûte 100.

**Sarsa apprend le chemin plus long, par les rangées du haut.** Et la raison est précisément celle de la section précédente : la cible de Sarsa contient l'action **réellement jouée**, donc Sarsa **tient compte de la règle de sélection**. Il apprend que « longer la falaise **quand on dévie une fois sur dix** » est une mauvaise idée, et il contourne. La politique qu'il apprend est sous-optimale, et c'est la bonne réponse au problème qu'on lui a réellement posé.

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}

La **Figure 4-9** montre le résultat en une courbe : la somme des récompenses par épisode sur 500 épisodes. Sarsa se stabilise autour de **−25**, Q-learning autour de **−50**.

{{< bookfig src="04-09.png" week="04" >}}

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, c'est la phrase à retenir de la semaine 4 si vous n'en retenez qu'une.** **La performance en ligne de Q-learning est pire que celle de Sarsa, alors que Q-learning a appris la meilleure politique.** Les deux moitiés de cette phrase sont vraies en même temps, et c'est tout l'intérêt de l'expérience. Il y a deux objets distincts, la politique **apprise** et la politique **jouée**, et la falaise est l'environnement qui les sépare le plus brutalement possible. Une méthode hors politique apprend l'optimum et le paie en ligne ; une méthode sur politique apprend un compromis et le joue bien. Aucune des deux n'a tort : elles répondent à deux questions différentes, et c'est à vous de savoir laquelle vous posez.

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}

Et si l'on faisait décroître \(\varepsilon\) progressivement ? Les deux méthodes convergeraient alors vers la politique optimale, puisque la politique jouée finirait par coïncider avec la politique gloutonne et que l'écart entre « apprise » et « jouée » se refermerait. C'est le correctif, et il est important de voir que le problème n'était pas dans les algorithmes mais dans le réglage de l'exploration.

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}

> [!TIP]
 **Une question à vous poser avant le quiz, et je ne vous donne pas la réponse.** Si la sélection d'action était purement **gloutonne**, c'est-à-dire \(\varepsilon = 0\), Q-learning et Sarsa seraient-ils exactement le même algorithme ? Écrivez les deux mises à jour côte à côte, remplacez \(A'\) par ce que la sélection gloutonne choisirait, et voyez. Puis demandez-vous si les deux **suites de tables** produites seraient identiques, et pas seulement les deux formules. La réponse tient en deux lignes, et elle vaut mieux qu'un paragraphe de ma part.

{{% comment %}}SOURCE: SB ch.6 p.154{{% /comment %}}
