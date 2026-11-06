---
title: "8.3 REINFORCE"
weight: 4
---

## Le théorème devenu algorithme

Prenons la dernière ligne de la dérivation, retirons l'espérance, et appelons le résultat une mise à jour. C'est littéralement tout ce que fait REINFORCE.

$$
\theta_{t+1} \defeq \theta_t + \alpha G_t \dfrac{\nabla \pi(A_t \mid S_t, \theta_t)}{\pi(A_t \mid S_t, \theta_t)}
$$

{{% comment %}}SOURCE: SB éq. 13.8 p.349{{% /comment %}}

Cette formule a une lecture intuitive qui vaut d'être dite lentement, parce qu'elle explique à la fois le numérateur et le dénominateur.

L'incrément est un **retour multiplié par un vecteur**. Le vecteur \(\nabla \pi(A_t\mid S_t,\theta_t)\) est la direction, dans l'espace des paramètres, qui **augmente le plus la probabilité de rejouer \(A_t\) en \(S_t\)**. L'incrément est donc toujours un déplacement dans la direction qui rend l'action prise plus probable, pondéré par deux quantités.

Premièrement, il est **proportionnel au retour** \(G_t\), ce qui favorise les actions qui ont effectivement rapporté. Si l'épisode s'est bien terminé, on rend l'action plus probable ; s'il s'est mal terminé et que \(G_t\) est négatif, le signe s'inverse et on la rend moins probable. Deuxièmement, il est **inversement proportionnel à la probabilité de l'action**. Celle-ci demande une seconde de réflexion, et la raison est élégante : sans ce dénominateur, les actions fréquemment choisies gagneraient par simple répétition. Une action prise mille fois accumulerait mille petits déplacements favorables, même si une autre, prise dix fois, rapporte davantage à chaque fois. Diviser par \(\pi(A_t\mid S_t,\theta_t)\) compense exactement la fréquence de sélection, et laisse le retour seul décider.

{{% comment %}}SOURCE: SB ch.13 p.349{{% /comment %}}

Il existe une écriture équivalente et plus compacte, celle que vous rencontrerez partout et celle que le code implémente. Comme \(\nabla \ln x = \nabla x / x\), le quotient est un gradient de logarithme :

$$
\theta_{t+1} = \theta_t + \alpha G_t \nabla \ln \pi(A_t\mid S_t,\theta_t)
$$

{{% comment %}}SOURCE: SB ch.13 p.349{{% /comment %}}

Ce vecteur \(\nabla\ln\pi(A_t\mid S_t,\theta_t)\) porte un nom, **vecteur d'éligibilité** (*eligibility vector*), et il mérite une remarque d'architecture : c'est le **seul endroit de tout l'algorithme où la paramétrisation de la politique intervient**. Changez le réseau, changez le softmax, passez d'un perceptron à une convolution : rien d'autre dans REINFORCE ne bouge. Tout le reste de l'algorithme ne manipule que des retours et des pas d'apprentissage.

{{% comment %}}SOURCE: SB ch.13 p.349{{% /comment %}}

Deux conséquences, et elles délimitent ce que REINFORCE peut faire. Il utilise \(G_t\), le retour **complet** de \(t\) jusqu'à la fin de l'épisode : c'est donc une méthode de **Monte-Carlo**, définie uniquement dans le cas épisodique, et dont toutes les mises à jour sont faites **après coup**, une fois l'épisode terminé et les retours connus. Retenez ces deux mots, « complet » et « après coup » : ils sont la source du premier des quatre problèmes de la section 8.5.

{{% comment %}}SOURCE: SB ch.13 p.349{{% /comment %}}

Sur la convergence, enfin, il y a une bonne nouvelle et un avertissement. La bonne nouvelle est que, par construction, l'espérance de la mise à jour sur un épisode est dans la direction du gradient de la performance : la méthode améliore donc la performance pour un pas d'apprentissage suffisamment petit, et converge vers un optimum **local** sous les conditions usuelles d'approximation stochastique. L'avertissement est l'autre face de la même pièce : étant une méthode de Monte-Carlo, REINFORCE souffre d'une **forte variance**, et son apprentissage est lent. C'est exactement le deuxième des quatre problèmes.

{{% comment %}}SOURCE: SB ch.13 p.351{{% /comment %}}

---

## L'algorithme, en six étapes

Voici la recette complète, écrite comme on l'implémente et non comme on la démontre.

> **REINFORCE, le gradient de politique de Monte-Carlo**
>
> 1. Initialiser avec des poids aléatoires le réseau qui représente la politique \(\pi(a\mid s,\theta)\).
> 2. Jouer \(N\) épisodes **complets**, en échantillonnant l'action à chaque pas dans \(\pi(\cdot\mid s,\theta)\), et enregistrer les transitions \((s_t, a_t, r_t)\).
> 3. Pour chaque pas \(t\) de chaque épisode, calculer le retour actualisé \(G_t = \sum_{k \ge 0}\gamma^k r_{t+k}\), en remontant l'épisode à rebours.
> 4. Calculer la perte \(\mathcal{L}_\pi = -\sum_{t} G_t \log \pi(a_t \mid s_t,\theta)\).
> 5. Effectuer un pas de descente de gradient stochastique sur \(\mathcal{L}_\pi\), ce qui met \(\theta\) à jour.
> 6. Répéter à partir de l'étape 2 jusqu'à convergence.

{{% comment %}}SOURCE: LAPAN ch.11 p.334{{% /comment %}}

L'étape 3 mérite une ligne de code, parce que c'est l'endroit où l'on se trompe. On parcourt la liste des récompenses de l'épisode **à rebours**, en accumulant `somme = somme * GAMMA + r`. Le dernier pas reçoit alors exactement sa propre récompense, l'avant-dernier reçoit \(r_{T-1} + \gamma r_T\), et ainsi de suite jusqu'au premier. Écrit dans l'autre sens, ce calcul demanderait une boucle imbriquée et une puissance de \(\gamma\) recalculée à chaque fois ; à rebours, il est linéaire et il tient en quatre lignes.

{{% comment %}}SOURCE: LAPAN ch.11 p.335-336{{% /comment %}}

```python
def calculer_retours(recompenses: list[float], gamma: float) -> list[float]:
    """G_t pour tous les t d'un episode, en UNE passe, de la fin vers le debut."""
    retours, somme = [], 0.0
    for r in reversed(recompenses):
        somme = somme * gamma + r      # G_t = r_t + gamma * G_{t+1}
        retours.append(somme)
    retours.reverse()                  # on avait construit la liste a l'envers
    return retours
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(r_t\) | récompense du pas \(t\) | un élément de `recompenses` |
| \(\gamma\) | facteur d'actualisation | `gamma` |
| \(G_t = r_t + \gamma G_{t+1}\) | retour, sous sa forme récursive | la ligne `somme = somme * gamma + r` |
| \(G_t\) | retour du pas \(t\) | `retours[t]`, après le `reverse()` |

---

## La perte qui n'est pas une perte

Nous arrivons au point que je considère comme le plus important de la semaine sur le plan pédagogique, et je le place **avant** le code plutôt qu'après, parce qu'une fois le code lu il est trop tard.

Reprenons l'étape 4. Le théorème nous donne un gradient à faire **monter** : nous voulons augmenter \(J(\theta)\). En notation d'ascension, le pas s'écrit très simplement \(\theta_{k+1} = \theta_k + \alpha \nabla_{\theta} J(\pi_{\theta_k})\), et c'est bien une somme, un plus, une montée.

{{% comment %}}SOURCE: SPINUP vpg/key-equations{{% /comment %}}

Mais les optimiseurs de PyTorch **minimisent**. Leur contrat est : donnez-moi un scalaire, j'en calcule le gradient et je déplace les poids dans la direction opposée. Pour leur faire exécuter une montée, il n'existe qu'un geste : leur donner l'**opposé** de la quantité à maximiser. D'où le signe moins de l'étape 4, et d'où la forme sous laquelle on écrit systématiquement les méthodes de gradient de politique :

$$
\mathcal{L}_\pi = -\,G_t \log \pi(a \mid s,\theta)
$$

{{% comment %}}SOURCE: LAPAN ch.11 p.333{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.11 p.338{{% /comment %}}

Ce signe moins n'est donc ni une convention esthétique ni une subtilité mathématique : c'est un adaptateur entre une formule qui monte et une bibliothèque qui descend. Et maintenant, la conséquence que je veux que vous teniez pour acquise avant de regarder une seule courbe.

> [!WARNING]
 **Cette quantité porte le nom de « perte » et n'en est pas une.** Depuis la semaine 2, vous avez vu des pertes : une entropie croisée, une erreur quadratique, une perte de Huber. Toutes avaient trois propriétés communes. Elles mesuraient un **écart** à une cible. Elles avaient un **plancher**, le plus souvent zéro. Et leur **valeur** vous renseignait : une perte qui descend vers son plancher voulait dire que l'apprentissage marche. La quantité de l'étape 4 n'a aucune de ces trois propriétés. Il n'y a pas de cible : rien, nulle part, ne dit ce que \(-G_t \log\pi\) devrait valoir. Il n'y a pas de plancher : en faisant croître les retours et les log-probabilités, on peut la rendre arbitrairement négative. Et sa valeur ne renseigne sur **rien**. Une perte de politique qui devient de plus en plus négative n'est pas en train de converger, et une perte de politique qui remonte n'est pas en train de diverger. Le seul contenu informatif de ce nombre est son **gradient**, qui est une direction. Ce qu'une courbe de perte de politique affiche n'est pas une erreur en train de diminuer, c'est l'ampleur et le sens moyens du déplacement que le lot courant demande.

Je vous donne tout de suite le contraste, parce qu'il est ce qui rend la distinction utilisable. Dans la section 8.8, la perte d'A2C aura **trois** termes. Le terme de politique sera celui que je viens de décrire : sans cible, sans plancher, illisible en valeur. Le terme de **valeur**, lui, sera une honnête erreur quadratique moyenne entre la sortie du critique et une cible, exactement comme en semaine 5. Celui-là, vous aurez le droit de le lire comme vous lisiez vos pertes de la semaine 2 : s'il ne descend pas, le critique n'apprend pas. Deux termes dans la même somme, deux régimes de lecture différents, et savoir lequel est lequel vous évitera plusieurs journées perdues.

> [!TIP]
 **La question à vous poser devant n'importe quelle courbe de perte, à partir de cette semaine.** « Cette quantité mesure-t-elle un écart à quelque chose ? » Si oui, sa valeur est un diagnostic. Si non, seule sa variation brutale est un signal, et il faut regarder ailleurs pour savoir si l'apprentissage fonctionne : la récompense par épisode, l'entropie de la politique, la norme des gradients. Je vous donnerai la liste complète des quantités à surveiller en section 8.9 et au laboratoire.

Voici maintenant le code, et il tient en six lignes qui méritent chacune un regard.

```python
def perte_politique(reseau, etats_t, actions_t, echelles_t):
    """La quantite minimisee : l'OPPOSE de ce que le theoreme fait monter.

    etats_t    : (B, taille_obs)
    actions_t  : (B,) entiers, l'action REELLEMENT prise
    echelles_t : (B,) le facteur G_t (plus tard : G_t - b, puis l'avantage)
    """
    logits_t = reseau(etats_t)                              # (B, n_actions)
    log_prob_t = F.log_softmax(logits_t, dim=1)             # (B, n_actions)
    lot = range(len(actions_t))
    # On ne garde que la log-probabilite de l'action prise : une par ligne.
    log_prob_action_t = log_prob_t[lot, actions_t]           # (B,)
    # Moyenne sur le lot, puis NEGATION : l'optimiseur descend, nous montons.
    return -(echelles_t * log_prob_action_t).mean()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(h(s,a,\theta)\) | préférences, sorties brutes du réseau | `logits_t` |
| \(\log \pi(\cdot \mid s,\theta)\) | log-probabilités de toutes les actions | `log_prob_t` |
| \(\log \pi(A_t \mid S_t,\theta)\) | log-probabilité de l'action prise | `log_prob_action_t` |
| \(G_t\) | l'échelle du gradient, ici le retour | `echelles_t` |
| \(\mathcal{L}_\pi = -\overline{G_t \log\pi(A_t\mid S_t,\theta)}\) | la quantité minimisée | la valeur de retour |
| \(\nabla \ln\pi(A_t\mid S_t,\theta_t)\) | vecteur d'éligibilité | jamais écrit : il est produit par `.backward()` |

Deux remarques sur ce fragment. L'indexation `log_prob_t[lot, actions_t]` est le geste que vous avez déjà fait en semaine 5 pour extraire \(Q(s,a)\) de la sortie du réseau Q : une ligne du lot, une colonne donnée par l'action. Et la **moyenne** sur le lot, plutôt que la somme, n'est qu'une mise à l'échelle du pas d'apprentissage par la taille du lot ; elle rend \(\alpha\) indépendant de cette taille, ce qui est commode quand on fait varier le nombre d'épisodes par mise à jour.

{{% comment %}}SOURCE: LAPAN ch.11 p.338{{% /comment %}}

Une phrase enfin sur le vocabulaire de l'étape 2, parce qu'elle vient d'une tradition que vous croiserez : pousser vers le haut les probabilités des actions qui mènent à un retour élevé, vers le bas celles qui mènent à un retour faible, et recommencer. C'est une description honnête de ce que fait l'algorithme, et elle ne contient aucune mathématique. Gardez-la comme résumé mnémonique.

{{% comment %}}SOURCE: SPINUP vpg/background{{% /comment %}}

---

## Trois objets des semaines 5 et 6 qui disparaissent

Regardez ce qui n'est pas dans l'algorithme, parce que les absences enseignent autant que les présences. Trois pièces centrales du réseau Q profond ont disparu, et chacune pour une raison différente.

**Pas d'exploration explicite.** Il n'y a ni \(\varepsilon\), ni calendrier de décroissance, ni couche bruitée. Le réseau démarre avec des poids aléatoires, ce qui produit une distribution de sortie presque uniforme, c'est-à-dire un comportement presque aléatoire ; et l'échantillonnage dans cette distribution **est** l'exploration. À mesure que la politique s'affine, la distribution se resserre et l'exploration diminue d'elle-même. Cela paraît élégant, et nous verrons en section 8.5 que c'est aussi un problème.

**Pas de tampon de rejeu.** Les méthodes de gradient de politique sont **sur politique** (*on-policy*) : le théorème calcule une espérance sous \(\pi\), la politique **courante**. Des transitions produites par une politique d'il y a dix mille pas ne sont pas des échantillons de la politique courante, et les réutiliser donne le gradient de la mauvaise politique. Cette contrainte a un bon côté, la convergence est généralement plus rapide par mise à jour, et un mauvais, il faut beaucoup plus d'interactions avec l'environnement. C'est de là que vient la facture de la section 8.9.

**Pas de réseau cible.** Le réseau cible existait pour stabiliser une cible qui s'amorçait sur elle-même ; or REINFORCE n'amorce rien, puisque son échelle \(G_t\) est un retour observé, mesuré, qui ne dépend d'aucune prédiction du réseau. Notez cependant que cette absence n'est pas définitive : dès la section 8.7, le critique **amorcera**, et la question de la stabilité de la cible reviendra avec lui.

{{% comment %}}SOURCE: LAPAN ch.11 p.334{{% /comment %}}

---
