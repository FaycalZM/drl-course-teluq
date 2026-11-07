---
title: "6.7 Défaut nº1, le max surestime : le double DQN"
weight: 8
---

## Choisir l'action et évaluer l'action, avec deux estimations distinctes

Premier défaut de la liste, et c'est le plus profond des cinq, parce que c'est le seul qui porte sur une **erreur systématique** et non sur une inefficacité.

Voici l'affirmation de la semaine 5 : prendre le maximum d'un ensemble d'estimations bruitées ne donne pas une estimation du maximum, cela donne quelque chose de systématiquement trop grand. Autrement dit, notre agent souffre d'une **surestimation des valeurs d'action** (*value overestimation*), et le mot « surestimation » est à prendre au sens strict d'une erreur qui ne s'annule pas en moyenne. Cette affirmation, je l'avais énoncée sans la démontrer. Démontrons-la, parce que c'est à cette démonstration que tient toute la section, et parce qu'elle tient en trois phrases.

Imaginez un état où **toutes** les valeurs d'action vraies sont nulles. Nos estimations, elles, sont bruitées : certaines sont un peu positives, d'autres un peu négatives, et c'est le comportement normal d'un estimateur non biaisé. Le maximum des valeurs vraies vaut zéro. Le maximum des estimations, lui, est **positif**, parce que le maximum va chercher précisément celle des erreurs qui est la plus favorable. Nous utilisons donc un maximum d'estimations comme estimation d'un maximum, et cela produit un biais positif significatif. Ce phénomène porte un nom : le **biais de maximisation** (*maximization bias*).

{{% comment %}}SOURCE: SB ch.6 p.156{{% /comment %}}

Remarquez ce que cette démonstration n'a pas supposé. Ni réseau de neurones, ni approximation, ni amorçage : rien que du bruit d'estimation et un opérateur maximum. Le biais de maximisation n'est donc pas un défaut du DQN, c'est un défaut du \(\max\) de l'équation d'optimalité de Bellman, et il était déjà dans le Q-learning tabulaire de la semaine 4.

---

## Deux états, deux actions, et une erreur qui ne s'efface pas

L'exemple qui rend la chose palpable est minuscule et je vous demande de le suivre pas à pas, parce que son résultat est contre-intuitif.

Deux états, \(A\) et \(B\). Depuis \(A\), deux actions. L'action de droite termine immédiatement l'épisode avec une récompense de 0. L'action de gauche mène en \(B\), d'où de nombreuses actions sont disponibles, chacune terminant l'épisode avec une récompense tirée dans une loi normale de moyenne \(-0{,}1\) et de variance 1.

Faisons le calcul que l'agent devrait faire. Aller à droite rapporte 0. Aller à gauche rapporte en moyenne \(-0{,}1\). Aller à gauche est donc **toujours** une erreur, et la politique optimale ne joue jamais cette action, sauf quand l'exploration l'y force.

Or le Q-learning préfère la gauche, et il la préfère longtemps. Avec \(\varepsilon = 0{,}1\), un pas d'apprentissage \(\alpha = 0{,}1\) et \(\gamma = 1\), moyenné sur dix mille exécutions indépendantes, il commence par jouer la gauche dans la quasi-totalité des cas, et **même à l'asymptote il la joue environ 5 % de fois de trop**. La **Figure 6-2** montre les deux courbes, celle du Q-learning ordinaire et celle de la variante que nous allons construire, avec le petit processus de décision markovien dessiné en médaillon.

{{< bookfig src="06-02.png" week="06" >}}

{{% comment %}}SOURCE: SB ch.6 p.156-157{{% /comment %}}

Pourquoi la gauche ? Parce que les récompenses de \(B\) sont bruitées autour de \(-0{,}1\) avec une variance de 1 : certaines sont nettement positives. Le \(\max\) sur les actions de \(B\) attrape la plus favorable, et la valeur de \(B\) remonte en \(A\) comme si aller à gauche était prometteur. L'agent n'apprend pas une récompense, il apprend un maximum de bruit.

---

## Le diagnostic, et la séparation qui le répare

Voici la phrase sur laquelle construire toute la réparation, et elle est d'une précision qui mérite une lecture lente. Le problème vient de ce qu'on utilise **les mêmes échantillons** pour deux choses à la fois : déterminer quelle action maximise, et estimer la valeur de cette action.

{{% comment %}}SOURCE: SB ch.6 p.157{{% /comment %}}

Si c'est le cumul de ces deux rôles qui crée le biais, alors il suffit de les séparer. Entretenons **deux** estimations indépendantes, \(Q_1\) et \(Q_2\). L'une sert à choisir :

$$
A^* = \argmax_{a} Q_1(a)
$$

et l'autre sert à évaluer ce choix. Le résultat clé est que \(Q_2(A^*)\) est alors **non biaisée** :

$$
\E\big[\,Q_2(A^*)\,\big] = q(A^*)
$$

{{% comment %}}SOURCE: SB ch.6 p.157{{% /comment %}}

L'indice et la valeur ne viennent plus du même bruit. La mise à jour complète, écrite pour la première des deux estimations, est celle du **double Q-learning** :

$$
Q_1(S_t,A_t) \;\leftarrow\; Q_1(S_t,A_t) + \alpha\Big[\,
 R_{t+1} + \gamma\,Q_2\big(S_{t+1},\, \argmax_{a} Q_1(S_{t+1},a)\big) -
 Q_1(S_t,A_t) \,\Big]
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.10 p.158{{% /comment %}}

Regardez l'intérieur du crochet, parce que c'est là que tout se joue : \(Q_1\) fournit l'**indice** de l'action, \(Q_2\) fournit la **valeur** à cet indice. À chaque pas, on tire à pile ou face laquelle des deux estimations est mise à jour, l'autre fournissant la valeur.

Le coût de ce procédé, dans le cas tabulaire, est connu et il est honnête : il **double la mémoire**, puisqu'il faut deux tables, mais il n'augmente pas la quantité de calcul par pas, puisqu'une seule des deux estimations est mise à jour à la fois.

{{% comment %}}SOURCE: SB ch.6 p.157{{% /comment %}}

> [!TIP]
 **Et voici pourquoi cette réparation est, de loin, la moins chère des cinq.** Un réseau Q profond possède déjà deux réseaux : l'entraîné et la cible. Le double DQN ne paie donc **ni** le doublement de la mémoire, **ni** le calcul supplémentaire : les deux estimations sont déjà là, et la seule chose qui manquait était de les faire jouer deux rôles différents. Trois lignes dans la perte, pas un paramètre de plus, pas un octet de plus. C'est l'exemple le plus net que je connaisse d'une réparation théorique qui ne coûte rien parce que l'ingénierie l'avait anticipée sans le savoir.

{{% comment %}}SOURCE: SB ch.6 p.157{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.7 p.219{{% /comment %}}

---

## La cible du double DQN, et les trois lignes qui la réalisent

Passons au réseau Q profond. L'idée s'énonce en une phrase : **choisir** l'action du prochain état avec le réseau entraîné, et **lire** la valeur de cette action sur le réseau cible.

{{% comment %}}SOURCE: LAPAN ch.8 p.247{{% /comment %}}

$$
y \;=\; r_t + \gamma\, Q_{\theta^-}\!\big(s_{t+1},\,
 \argmax_{a'} Q_{\theta}(s_{t+1},a')\big)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.247{{% /comment %}}

Comparez avec la cible de la semaine 5. Il n'y a plus de \(\max\) dans cette expression, et c'est normal : l'\(\argmax\) a déjà désigné **une** action, il n'y a donc plus rien sur quoi maximiser. Toute la différence entre les deux cibles tient à ceci : la semaine 5 demandait au réseau cible à la fois quelle action choisir et combien elle valait, alors que celle-ci confie la question à l'un et la réponse à l'autre.

Trois lignes de PyTorch, et je les commente parce que c'est la modification que le laboratoire vous demandera d'activer par un drapeau.

```python
def calculer_perte_double(lot, reseau, reseau_cible, gamma, peripherique,
                          double: bool = True):
    """Le socle de 6.5, avec les trois lignes du double DQN."""
    etats, actions, recompenses, termines, etats_finaux = deplier_lot(lot)
    # ... mise en tenseurs identique à la section 6.5 ...

    valeurs_action = reseau(etats_t).gather(
        1, actions_t.unsqueeze(-1)).squeeze(-1)

    with torch.no_grad():
        if double:
            # 1. L'INDICE vient du réseau ENTRAÎNÉ.
            indices = reseau(etats_f_t).max(1)[1]
            # 2. La VALEUR vient du réseau CIBLE, à cet indice.
            valeurs_finales = reseau_cible(etats_f_t).gather(
                1, indices.unsqueeze(-1)).squeeze(-1)
        else:
            # 3. La version de la semaine 5 : le même réseau fait les deux.
            valeurs_finales = reseau_cible(etats_f_t).max(1)[0]
        valeurs_finales[termines_t] = 0.0

    cibles = recompenses_t + gamma * valeurs_finales
    return nn.MSELoss()(valeurs_action, cibles)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\argmax_{a'} Q_\theta(s',a')\) | l'action choisie par le réseau **entraîné** | `reseau(etats_f_t).max(1)[1]` |
| \(Q_{\theta^-}(s',\cdot)\) | les valeurs lues sur le réseau **cible** | `reseau_cible(etats_f_t)` |
| \(Q_{\theta^-}(s', \argmax \ldots)\) | la valeur à l'indice choisi | `.gather(1, indices...)` |
| \(\max_{a'} Q_{\theta^-}(s',a')\) | la cible de la semaine 5, pour comparaison | `.max(1)[0]` |
| \(y\) | la cible du double DQN | `cibles` |

Notez que `max(1)` rend un couple et que les deux variantes en prennent des moitiés différentes : `[1]` est l'indice de l'action, `[0]` est sa valeur. Dans la version de la semaine 5, l'indice et la valeur sortent du **même** appel, donc du même réseau. Dans la version double, l'indice sort d'un réseau et la valeur de l'autre. Deux caractères de différence, et c'est toute la méthode.

{{% comment %}}SOURCE: LAPAN ch.8 p.248{{% /comment %}}

---

## Mesurer la surestimation, puisqu'elle est invisible dans une courbe de récompense

Il reste un problème de méthode, et sa solution est si bonne que le laboratoire la réutilisera : comment **voir** une surestimation ? La récompense n'en dit rien, puisqu'un agent qui surestime toutes ses valeurs de la même quantité joue exactement la même politique.

Le protocole est le suivant. Avant l'entraînement, on met de côté **mille états tirés au hasard**. Ce sont des états témoins : ils ne servent jamais à l'apprentissage. Puis, périodiquement pendant l'entraînement, on calcule la moyenne de \(\max_a Q_\theta(s,a)\) sur ces mille états, et on la trace. Comme l'ensemble ne change pas, la courbe mesure l'évolution de ce que le réseau **croit** valoir, indépendamment de ce qu'il gagne.

{{% comment %}}SOURCE: LAPAN ch.8 p.248-249{{% /comment %}}

La **Figure 6-3** donne les deux courbes obtenues ainsi.

{{< bookfig src="06-03.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.250{{% /comment %}}

Et elle montre très exactement ce que la théorie annonçait. Les valeurs du réseau Q profond ordinaire montent, dépassent un certain niveau, puis **redescendent** : le réseau a cru à des valeurs qu'il a ensuite dû démentir, ce qui est la trace d'une surestimation corrigée tardivement. Les valeurs de la version double, elles, croissent de façon plus régulière.

{{% comment %}}SOURCE: LAPAN ch.8 p.250{{% /comment %}}

> [!WARNING]
 **Attention à la force de la conclusion, et je vais être précis parce que c'est le point où ce genre de section dérape habituellement.** Le résultat de non-biais énoncé plus haut, \(\E[Q_2(A^*)] = q(A^*)\), porte sur le cas de **deux estimations indépendantes dans un problème à un seul état**. Un réseau cible n'est pas indépendant du réseau entraîné : c'en est une copie récente. La séparation **réduit** donc la surestimation, et la Figure 6-3 montre une réduction ; elle ne la supprime pas et rien dans ce cours ne vous autorisera à dire qu'elle la supprime. Écrivez « réduit », pas « élimine ». Vous retrouverez ce même biais, non résolu, en semaine 11, dans le contrôle continu, où il faudra deux critiques entiers pour le contenir.

{{% comment %}}SOURCE: SB ch.6 p.157{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.8 p.250{{% /comment %}}

Et pour finir, le résultat le plus instructif de la section, parce qu'il est décevant. Sur le jeu de référence, l'effet du double DQN sur le temps d'entraînement est **faible**, et après réglage des hyperparamètres il a fallu 412 parties, c'est-à-dire un peu **plus** que les 400 de la référence. Le défaut est réel, la mesure le montre, et le gain de vitesse n'est pas garanti. Les deux affirmations sont vraies en même temps, et c'est exactement le genre de résultat qu'un cours doit transmettre : une réparation correcte n'est pas forcément une réparation rentable sur un problème donné.

{{% comment %}}SOURCE: LAPAN ch.8 p.250{{% /comment %}}

---
