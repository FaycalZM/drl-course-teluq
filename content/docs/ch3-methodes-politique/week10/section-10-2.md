---
title: "10.2 PPO : écrêter le rapport"
weight: 3
---

## La méthode que vous utiliserez, présentée d'abord

Nous y voilà. **L'optimisation proximale de politique** (*proximal policy optimization*, PPO) est une méthode de 2017, et c'est très probablement la méthode d'apprentissage par renforcement la plus utilisée au monde aujourd'hui : elle est le point de départ par défaut sur un problème continu, elle est au cœur de l'ajustement des grands modèles de langue par renforcement, et elle est la seule méthode de cette semaine que je vous demanderai d'écrire.

Elle se décrit en une phrase, et je vous la donne maintenant pour que vous sachiez où nous allons. Au lieu de dériver le logarithme de la probabilité de l'action jouée, PPO dérive le **rapport entre la nouvelle et l'ancienne politique**, multiplié par l'avantage, et il **écrête** ce rapport pour que la mise à jour cesse de rapporter au-delà d'une bande.

{{% comment %}}SOURCE: LAPAN ch.16 p.500{{% /comment %}}

Reprenons donc l'objectif de la semaine 8, celui que PPO remplace. Sous sa forme échantillonnée, le gradient de politique à avantage s'écrit :

$$
\nabla_\theta J(\theta) = \E_t\left[\, \nabla_\theta \ln \pi_\theta(a_t \mid s_t)\; \Adv_t \,\right]
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.500 (image){{% /comment %}}

Vous connaissez chaque symbole : \(\pi_\theta\) est la politique paramétrée, \(\Adv_t\) l'estimation de l'avantage de l'action jouée, et l'espérance porte sur les transitions du lot. Et vous connaissez aussi la contrainte invisible qui l'accompagne : ce gradient n'est valide que **sous la politique qui a collecté le lot**. Dès que \(\theta\) a bougé d'un pas, les transitions du lot ont été produites par une politique qui n'existe plus, et le lot est périmé. C'est la raison pour laquelle l'A2C de la semaine 8 jette chaque transition après un unique pas de gradient, et c'est l'origine de sa facture en échantillons.

---

## Du logarithme au rapport : l'échantillonnage préférentiel de la semaine 3 revient

Comment réutiliser un lot collecté sous une ancienne politique ? Vous connaissez déjà la réponse, et elle date de la semaine 3.

Lorsqu'on veut estimer une espérance sous une distribution \(p\) alors que les échantillons viennent d'une distribution \(q\), on pondère chaque échantillon par le rapport \(p/q\). C'est l'**échantillonnage préférentiel** (*importance sampling*), et le cours l'a rencontré pour la première fois en semaine 3, dans la méthode d'entropie croisée, où il servait déjà exactement à cela : récupérer des échantillons tirés sous une politique périmée.

{{% comment %}}SOURCE: LAPAN ch.16 p.500{{% /comment %}}

Appliqué ici, le rapport à former est celui des deux politiques, évaluées **sur l'action réellement jouée** :

$$
r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.500 (image){{% /comment %}}
{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

où \(\theta_{\text{old}}\) sont les paramètres **sous lesquels le lot a été collecté**, figés pendant toute l'exploitation de ce lot. Trois lectures de cette quantité, et elles sont toutes les trois utiles.

Si \(r_t(\theta) = 1\), la nouvelle politique donne à cette action exactement la même probabilité que l'ancienne : rien n'a changé pour elle. Si \(r_t(\theta) > 1\), la nouvelle politique rend cette action **plus** probable. Si \(r_t(\theta) < 1\), elle la rend **moins** probable. Le rapport est donc une mesure directe, action par action, de combien la politique a bougé, et c'est précisément la grandeur que l'introduction réclamait.

L'objectif devient alors le rapport pondéré par l'avantage :

$$
J(\theta) = \E_t\left[\, \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}\; \Adv_t \,\right]
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.500 (image){{% /comment %}}

**Le lien avec la semaine 8 est plus serré qu'il n'y paraît, et il vaut la vérification.** Dérivez l'objectif ci-dessus par rapport à \(\theta\) au point \(\theta = \theta_{\text{old}}\). Le dénominateur est une constante, le numérateur se dérive en \(\nabla_\theta \pi_\theta\), et comme \(\nabla_\theta \ln \pi_\theta = \nabla_\theta\pi_\theta / \pi_\theta\), les deux expressions coïncident exactement. Autrement dit, **au premier pas, PPO et la semaine 8 font la même chose.** Ce n'est qu'aux pas suivants, quand \(\theta\) s'est éloigné de \(\theta_{\text{old}}\) et que le rapport cesse de valoir 1, que les deux méthodes divergent. Le rapport n'est pas un nouveau gradient : c'est le gradient de la semaine 8 muni d'un **certificat de péremption** sur le lot qui l'a produit.

Et maintenant le danger, qui est entier. Rien, dans l'objectif ci-dessus, n'empêche de maximiser bêtement. Si une action a un avantage positif, l'objectif croît sans borne quand on augmente sa probabilité : le maximiseur poussera donc \(r_t(\theta)\) aussi haut qu'il peut, ce qui est très exactement le grand pas de la Figure 10-2. L'échantillonnage préférentiel nous a donné le droit de réutiliser le lot ; il ne nous a rien donné pour savoir quand nous nous sommes trop éloignés de lui.

{{% comment %}}SOURCE: LAPAN ch.16 p.500{{% /comment %}}

---

## L'objectif écrêté, et l'asymétrie qu'il faut voir

Voici la réponse de PPO, l'**objectif écrêté** (*clipped objective*), et c'est l'équation de la semaine :

$$
J^{\text{clip}}(\theta) = \E_t\left[\, \min\!\Big(\, r_t(\theta)\,\Adv_t,\;\; \operatorname{clip}\big(r_t(\theta),\, 1-\epsilon,\, 1+\epsilon\big)\,\Adv_t \,\Big) \,\right]
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.500, répétée p.505 (image){{% /comment %}}
{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

Le paramètre \(\epsilon\) est la demi-largeur de la **bande** dans laquelle le rapport est autorisé à vivre, et le choix usuel est \(\epsilon = 0{,}2\). La même expression, écrite échantillon par échantillon plutôt que sous l'espérance, donne la perte que vous coderez :

$$
L(s,a,\theta_{\text{old}},\theta) = \min\!\left(\frac{\pi_\theta(a\mid s)}{\pi_{\theta_{\text{old}}}(a\mid s)}\,A^{\pi_{\theta_{\text{old}}}}(s,a),\;\; \operatorname{clip}\!\left(\frac{\pi_\theta(a\mid s)}{\pi_{\theta_{\text{old}}}(a\mid s)},\, 1-\epsilon,\, 1+\epsilon\right)A^{\pi_{\theta_{\text{old}}}}(s,a)\right)
$$

$$
\theta_{k+1} = \argmax_{\theta}\; \E_{s,a \sim \pi_{\theta_{\text{old}}}}\left[\, L(s,a,\theta_{\text{old}},\theta) \,\right]
$$

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

Lue telle quelle, cette formule est opaque : un minimum entre un produit et le même produit avec un facteur écrêté, ce n'est pas une phrase qui s'interprète. Elle devient limpide dès qu'on la sépare selon le **signe de l'avantage**, et c'est ce que fait la **Figure 10-1**.

{{< bookfig src="10-01.png" week="10" >}}

Regardez les deux panneaux, et laissez l'asymétrie vous frapper.

**Panneau de gauche, avantage positif.** L'action jouée s'est révélée meilleure que ce que le critique attendait : nous voulons donc **augmenter** sa probabilité, c'est-à-dire pousser \(r\) vers la droite. L'objectif croît avec \(r\), comme il doit, jusqu'à \(1+\epsilon\). Puis il devient **plat**. Au-delà de la bande, augmenter encore la probabilité de cette action n'augmente plus l'objectif d'un iota : la mise à jour n'a plus rien à y gagner. Et remarquez l'autre côté : à gauche de la bande, la courbe n'est **pas** écrêtée, elle descend. Si le rapport avait dérivé vers le bas pour une action à avantage positif, l'objectif le punirait pleinement et le ramènerait.

**Panneau de droite, avantage négatif.** L'action s'est révélée moins bonne qu'attendu : nous voulons **réduire** sa probabilité, c'est-à-dire pousser \(r\) vers la gauche. Cette fois, c'est le côté gauche qui s'aplatit, à \(1-\epsilon\). Au-delà, continuer à réduire la probabilité de cette action ne rapporte plus rien. Et le côté droit n'est pas écrêté non plus : il continue de descendre, donc de pénaliser une politique qui augmenterait la probabilité d'une mauvaise action.

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

L'asymétrie est donc la même dans les deux cas, et elle se formule en une règle : **seul le côté vers lequel la mise à jour veut aller est aplati.** La bande ne construit pas une prison symétrique ; elle supprime la récompense de l'excès, dans la direction de l'excès, et laisse toute sa force au rappel dans l'autre sens.

La forme la plus commode pour écrire cela est la version par morceaux, où l'objectif s'exprime à l'aide d'une fonction de deux arguments :

$$
g(\epsilon, \Adv) = \begin{cases}
(1+\epsilon)\,\Adv & \text{si } \Adv \ge 0 \\[4pt]
(1-\epsilon)\,\Adv & \text{si } \Adv < 0
\end{cases}
\qquad\text{et}\qquad
L = \min\!\Big(r_t(\theta)\,\Adv,\; g(\epsilon, \Adv)\Big)
$$

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

C'est de cette forme que la Figure 10-1 est tracée, point par point, et c'est elle qu'il faut avoir en tête pour vérifier son propre code. Les deux branches se réécrivent d'ailleurs sans aucun minimum ni écrêtage, et je les donne parce qu'elles sont la preuve la plus courte de la lecture ci-dessus. Pour un avantage positif :

$$
L = \min\!\left(\frac{\pi_\theta(a\mid s)}{\pi_{\theta_{\text{old}}}(a\mid s)},\; 1+\epsilon\right)A^{\pi_{\theta_{\text{old}}}}(s,a)
$$

et pour un avantage négatif :

$$
L = \max\!\left(\frac{\pi_\theta(a\mid s)}{\pi_{\theta_{\text{old}}}(a\mid s)},\; 1-\epsilon\right)A^{\pi_{\theta_{\text{old}}}}(s,a)
$$

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

Dans la première, le rapport est plafonné à \(1+\epsilon\) et l'avantage est positif : le produit cesse de croître. Dans la seconde, le rapport est planché à \(1-\epsilon\) et l'avantage est négatif : le produit cesse de décroître, donc l'opposé, qui est ce que l'on minimise, cesse de croître. Le minimum et le maximum ne sont pas deux conventions arbitraires : ils sont le même geste, vu de part et d'autre de zéro.

> [!IMPORTANT]
 **Voici la formulation exacte de ce que l'écrêtage fait, et je vous demande de l'adopter telle quelle, parce que la formulation courante est fausse.** On lit souvent que l'écrêtage « limite la taille de la mise à jour ». Ce n'est pas ce qu'il fait. L'écrêtage **retire une incitation** : il agit comme un régularisateur en supprimant l'intérêt qu'aurait la politique à changer beaucoup, et le paramètre \(\epsilon\) dit jusqu'où la nouvelle politique peut s'écarter de l'ancienne **tout en y gagnant encore quelque chose**. Il n'impose aucune borne dure. Un gradient issu d'un autre terme de la perte, ou simplement un pas d'optimiseur un peu grand, peut parfaitement emmener le rapport au-delà de la bande : l'objectif ne l'encourage plus, il ne l'interdit pas. Un étudiant qui retient « l'écrêtage borne le pas » sera surpris la première fois qu'une exécution de PPO divergera, et il cherchera le bogue au mauvais endroit.

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

---

## GAE : un avantage entre un pas et tout l'épisode

Il reste à dire d'où vient \(\Adv_t\), et c'est le second apport de cette méthode. Il n'est pas accessoire : c'est la pièce qui fait fonctionner tout l'ensemble en pratique.

Partons de ce que la semaine 8 a établi. L'avantage peut s'estimer de plusieurs façons, et elles forment une famille indexée par l'horizon de déroulement. À un extrême, le résidu temporel à un pas : peu de variance, mais tout le poids du biais du critique. À l'autre extrême, le retour complet de l'épisode moins la valeur de l'état de départ : aucun biais venu du critique, mais toute la variance de la trajectoire. La semaine 8 a montré que le retour à \(N\) pas interpole entre les deux, et qu'un critique permet de descendre \(N\) de dix à quatre.

{{% comment %}}SOURCE: source-assets/raw-content/week-08.md §8.9{{% /comment %}}

Voici donc l'extrême à variance maximale, l'avantage calculé sur tout le reste de l'épisode :

$$
\Adv_t = -\,v_{\mathbf{w}}(s_t) + R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{\,T-t-1} R_{T} + \gamma^{\,T-t}\, v_{\mathbf{w}}(s_T)
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.500 (image){{% /comment %}}

L'**estimation généralisée de l'avantage** (*generalized advantage estimation*, GAE) remplace ce choix binaire par une moyenne pondérée de toute la famille, et le résultat est remarquablement simple : c'est une somme actualisée de résidus temporels, avec un facteur d'actualisation qui n'est plus \(\gamma\) mais le produit \(\gamma\lambda\).

$$
\Adv_t = \delta_t + (\gamma\lambda)\,\delta_{t+1} + (\gamma\lambda)^2\,\delta_{t+2} + \dots + (\gamma\lambda)^{\,T-t-1}\,\delta_{T-1}
$$

$$
\text{où}\qquad \delta_t = R_{t+1} + \gamma\, v_{\mathbf{w}}(s_{t+1}) - v_{\mathbf{w}}(s_t)
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.501 (image){{% /comment %}}

Le second objet, \(\delta_t\), est le **résidu temporel** (*TD residual*), et c'est une vieille connaissance : c'est l'erreur de différence temporelle de la semaine 4, telle quelle, sans une virgule de changement. Le premier objet est donc une somme de corrections locales, chacune pesée par \((\gamma\lambda)\) élevé à la distance temporelle.

> [!TIP]
 **Le paramètre \(\lambda\) est un curseur, et ses deux extrémités sont deux méthodes que vous connaissez déjà.** Posez \(\lambda = 0\) : tous les termes disparaissent sauf le premier, et l'avantage se réduit à \(\delta_t\), c'est-à-dire à l'avantage à un pas, biaisé par le critique et de faible variance. Posez maintenant \(\lambda = 1\) : les poids deviennent \(\gamma^k\), la somme des résidus se télescope, et vous retombez exactement sur l'avantage de la semaine 8, celui qui déroule la trajectoire. **La semaine 8 est donc le cas particulier \(\lambda = 1\) de ce que nous écrivons ici.** Le réglage usuel, \(\lambda = 0{,}95\), est un point entre les deux, très légèrement du côté de la variance. Et si cette lecture vous semble familière, c'est qu'elle est celle des traces d'éligibilité de SCI1060 : même curseur, même interpolation entre un pas et tout l'épisode.

{{% comment %}}SOURCE: LAPAN ch.16 p.501 (image){{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-08.md §8.9{{% /comment %}}

> [!WARNING]
 **Trois pièges de notation dans ces deux équations, et vous les rencontrerez ailleurs.** Premier piège, le résidu temporel est parfois écrit \(\sigma_t\). Ce cours l'écrit \(\delta_t\), comme en semaine 4, parce que \(\sigma\) est l'écart-type de la politique gaussienne depuis la semaine 9 et que les deux objets se croiseront en section 10.5. Deuxième piège, l'exposant du dernier terme : il vaut \(T-t-1\), et vous verrez parfois \(T-t+1\) imprimé à sa place. La vérification est immédiate et vous pouvez la refaire de tête, parce que c'est le genre de contrôle qui vous sauvera un jour : le terme d'indice \(t\) porte l'exposant 0, celui d'indice \(t+k\) porte l'exposant \(k\), donc celui d'indice \(T-1\) porte l'exposant \(T-1-t\). Troisième piège, le facteur d'actualisation de la somme est le **produit** \(\gamma\lambda\), et non \(\gamma\) élevé à la puissance \(\lambda\) : c'est un produit de deux nombres entre 0 et 1, et c'est ce que tout code correct calcule.

{{% comment %}}SOURCE: LAPAN ch.16 p.500, p.501, p.503 (images){{% /comment %}}

Reste à calculer cette somme sans faire exploser le coût. Écrite telle quelle, elle demande une somme par pas de temps, donc un coût quadratique en longueur de trajectoire. Mais la relation de récurrence saute aux yeux dès qu'on l'écrit à l'envers : l'avantage au pas \(t\) vaut le résidu du pas \(t\) plus \(\gamma\lambda\) fois l'avantage du pas \(t+1\). Une seule passe sur la trajectoire, parcourue de la fin vers le début, suffit donc.

{{% comment %}}SOURCE: LAPAN ch.16 p.502{{% /comment %}}

```python
import numpy as np


def avantages_gae(recompenses, valeurs, termines, gamma=0.99, lam=0.95):
    """GAE en UNE passe, de la fin vers le debut.

    recompenses[t] : R_{t+1}, la recompense de la transition t -> t+1
    valeurs[t]     : v_w(s_t), avec UN element de plus que recompenses
    termines[t]    : True si s_{t+1} est terminal
    """
    n = len(recompenses)
    avantages = np.zeros(n, dtype=np.float32)
    gae = 0.0

    for t in reversed(range(n)):
        if termines[t]:
            # Etat suivant terminal : c'est LA VALEUR DE L'ETAT SUIVANT qui
            # disparait, pas la recompense. R_{t+1} a bien ete recue.
            delta = recompenses[t] - valeurs[t]
            gae = delta                      # et la somme repart de zero
        else:
            delta = recompenses[t] + gamma * valeurs[t + 1] - valeurs[t]
            gae = delta + gamma * lam * gae

        avantages[t] = gae

    # La cible du critique est l'avantage plus la valeur predite.
    cibles_valeur = avantages + valeurs[:-1]
    return avantages, cibles_valeur
```

{{% comment %}}SOURCE: LAPAN ch.16 p.502{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\delta_t\) | résidu temporel du pas \(t\) | `delta` |
| \(\Adv_t\) | avantage généralisé, accumulé à l'envers | `gae`, `avantages[t]` |
| \(\gamma\) | facteur d'actualisation, 0,99 | `gamma` |
| \(\lambda\) | pondération exponentielle de GAE, 0,95 | `lam` |
| \(v_{\mathbf{w}}(s_t)\) | valeur prédite par le critique | `valeurs[t]` |
| \(R_{t+1}\) | récompense de la transition | `recompenses[t]` |
| \(\Adv_t + v_{\mathbf{w}}(s_t)\) | cible de régression du critique | `cibles_valeur` |

> [!NOTE]
 **Le traitement de l'état terminal, dit correctement, parce que la formulation courante est fautive.** À un pas terminal, ce qui disparaît de la formule du résidu est le terme \(\gamma\,v_{\mathbf{w}}(s_{t+1})\), c'est-à-dire **la valeur de l'état suivant**, et la raison est celle que le cours répète depuis la semaine 5 : un état terminal vaut zéro, il n'y a plus rien après. La récompense \(R_{t+1}\), elle, a bel et bien été reçue et reste dans le calcul ; c'est même souvent la récompense la plus informative de l'épisode. On lit parfois que c'est « la récompense » qui est écartée : ce serait une erreur de code grave, car vous supprimeriez le signal du pas le plus décisif de la trajectoire. Et la somme de GAE doit en outre **repartir de zéro** après un état terminal, puisqu'un épisode ne doit jamais propager son avantage dans l'épisode suivant.

{{% comment %}}SOURCE: LAPAN ch.16 p.502{{% /comment %}}

---

## Une longue trajectoire, plusieurs époques : le troisième changement

Le troisième apport de PPO n'est ni une équation ni une architecture : c'est un changement de **procédure**, et c'est celui qui transforme le rapport en gain réel.

La semaine 8 collectait un petit lot, faisait un pas de gradient, et jetait le lot. PPO collecte une **longue** séquence de transitions, calcule l'avantage généralisé sur toute la séquence en une passe arrière, puis effectue **plusieurs époques** d'entraînement sur cette même séquence, en la découpant en minilots. Les ordres de grandeur employés sur le banc d'essai de la section 10.1 sont une trajectoire de 2 049 transitions, dix époques, et des minilots de 64.

{{% comment %}}SOURCE: LAPAN ch.16 p.501 (image){{% /comment %}}

Voyez ce que cela coûte et ce que cela achète. Cela achète un facteur considérable en efficacité d'échantillon : chaque transition collectée sert à dix passes de gradient au lieu d'une. Et cela coûte exactement ce que l'écrêtage est là pour payer : dès la deuxième époque, la politique courante n'est plus celle qui a collecté les données, le rapport \(r_t(\theta)\) n'est plus égal à 1, et sans l'écrêtage la dixième époque optimiserait joyeusement un objectif sans aucun rapport avec la réalité. **L'écrêtage est ce qui rend les époques multiples sûres, et les époques multiples sont ce qui rend l'écrêtage utile.** Les deux idées ne se comprennent pas séparément.

Voici la boucle complète, et je l'écris en français comme je l'ai fait en semaines 8 et 9, parce qu'une boucle en dix lignes vaut mieux qu'un paragraphe :

```
 1. Initialiser l'acteur theta et le critique w
 2. Repeter :
 3.   Collecter une trajectoire longue (ici 2049 transitions) avec la politique
      courante, et MEMORISER, pour chaque transition, la log-probabilite de
      l'action sous cette politique : c'est ln pi_{theta_old}(a|s)
 4.   Calculer les valeurs v_w(s) sur toute la trajectoire
 5.   Calculer les avantages GAE en UNE passe arriere, et les cibles du critique
 6.   Normaliser les avantages : (A - moyenne) / ecart-type
 7.   Repeter PPO_EPOCHES fois :
 8.     Pour chaque minilot tire dans la trajectoire :
 9.       ratio  <- exp( ln pi_theta(a|s) - ln pi_{theta_old}(a|s) )
10.       perte_acteur    <- - moyenne( min( ratio * A , clip(ratio,1-eps,1+eps) * A ) )
11.       perte_critique  <- moyenne( ( v_w(s) - cible )^2 )
12.       Un pas sur theta avec son optimiseur, un pas sur w avec le sien
13. Jeter la trajectoire et revenir a l'etape 3
```

{{% comment %}}SOURCE: SPINUP ppo/pseudocode{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.501, p.504-505{{% /comment %}}

Le critique, à l'étape 11, fait exactement ce qu'il faisait en semaine 8 : une régression des moindres carrés sur une cible. Sous sa forme complète, moyennée sur les trajectoires d'un lot et sur les pas de chaque trajectoire, cette régression s'écrit :

$$
\mathbf{w}_{k+1} = \argmin_{\mathbf{w}}\; \frac{1}{\lvert \mathcal{D}_k \rvert\, T} \sum_{\tau \in \mathcal{D}_k} \sum_{t=0}^{T} \left(\, v_{\mathbf{w}}(s_t) - \hat{R}_t \,\right)^2
$$

{{% comment %}}SOURCE: SPINUP ppo/pseudocode{{% /comment %}}

où \(\hat{R}_t\) est la cible construite à l'étape 5, c'est-à-dire l'avantage plus la valeur prédite. Rien de nouveau : c'est la perte de critique de la semaine 8, et c'est pour cela que je ne m'y arrête pas.

Les réglages complets employés sur le banc d'essai, à titre d'ordre de grandeur et non de recette, sont les suivants : \(\gamma = 0{,}99\), \(\lambda = 0{,}95\), une trajectoire de 2 049 transitions, un pas d'apprentissage de \(10^{-5}\) pour l'acteur et de \(10^{-4}\) pour le critique, \(\epsilon = 0{,}2\), dix époques, des minilots de 64.

{{% comment %}}SOURCE: LAPAN ch.16 p.501 (image){{% /comment %}}

**Les deux pas d'apprentissage diffèrent d'un facteur dix, et ce n'est pas un hasard.** L'acteur apprend dix fois plus lentement que le critique. La raison est celle de toute la semaine : une erreur de critique se corrige, puisque le critique régresse sur des cibles que la prochaine trajectoire fournira à nouveau, alors qu'une erreur d'acteur choisit les données du pas suivant. On ralentit donc celui des deux dont les erreurs ne se rattrapent pas. Et comme les deux réseaux n'ont aucun poids commun, deux pas d'apprentissage distincts sont **possibles** : c'est le deuxième écart de la section 10.1 qui rend ce réglage disponible, et c'est un bon exemple de décision d'architecture qui ouvre une porte de réglage.

---

## Le pas PPO en code, et les trois lignes qui comptent

Voici le pas de mise à jour. Trois lignes y portent toute la méthode, et je les commente ensuite une par une.

```python
import torch
import torch.nn.functional as F

PPO_EPS = 0.2


def perte_ppo(acteur, critique, lot, eps=PPO_EPS):
    """Un minilot : perte de l'acteur ecretee, perte du critique."""
    etats, actions, anciennes_logprob, avantages, cibles = lot

    # 1. La log-densite de l'action JOUEE sous la politique COURANTE.
    mu = acteur(etats)
    sigma = torch.exp(acteur.logstd)
    loi = torch.distributions.Normal(mu, sigma)
    logprob = loi.log_prob(actions).sum(dim=-1)

    # 2. LE rapport. En logarithmes puis exponentielle : plus stable que le
    #    quotient de deux densites, et exact. anciennes_logprob est DETACHE.
    ratio = torch.exp(logprob - anciennes_logprob)

    # 3. L'ecretage, et le minimum des deux termes.
    objectif = ratio * avantages
    objectif_ecrete = torch.clamp(ratio, 1.0 - eps, 1.0 + eps) * avantages
    perte_acteur = -torch.min(objectif, objectif_ecrete).mean()

    perte_critique = F.mse_loss(critique(etats).squeeze(-1), cibles)
    return perte_acteur, perte_critique, ratio.detach()
```

{{% comment %}}SOURCE: LAPAN ch.16 p.504-505{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\ln \pi_\theta(a\mid s)\) | log-densité sous la politique courante | `logprob` |
| \(\ln \pi_{\theta_{\text{old}}}(a\mid s)\) | log-densité sous la politique de collecte, **détachée** | `anciennes_logprob` |
| \(r_t(\theta)\) | le rapport entre les deux politiques | `ratio` |
| \(\epsilon\) | demi-largeur de la bande, 0,2 | `eps` |
| \(\Adv_t\) | avantage généralisé, déjà normalisé | `avantages` |
| \(r_t(\theta)\,\Adv_t\) | le terme non écrêté | `objectif` |
| \(\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)\,\Adv_t\) | le terme écrêté | `objectif_ecrete` |
| \(-J^{\text{clip}}\) | ce que l'optimiseur minimise | `perte_acteur` |
| \(\left(v_{\mathbf{w}}(s)-\hat{R}\right)^2\) | perte du critique | `perte_critique` |

**Ligne 1, le rapport s'écrit comme une différence de logarithmes.** On ne divise pas deux densités : on soustrait deux log-densités et on exponentie. C'est mathématiquement la même chose et numériquement bien plus sûr, puisqu'une densité gaussienne peut valoir \(10^{-40}\) sans rien d'anormal, et qu'un quotient de deux nombres de cet ordre perd toute précision.

**Ligne 2, l'ancienne log-probabilité est détachée du graphe.** Elle a été calculée à la collecte, sous \(\theta_{\text{old}}\), et elle est une **constante** pour toute l'exploitation de la trajectoire. Si vous oubliez le détachement, le gradient remonte dans le dénominateur du rapport, et vous optimisez une quantité qui n'est pas celle que vous avez écrite. Vous reconnaissez la discipline de détachement de la semaine 5, dans un troisième contexte.

**Ligne 3, la perte est l'opposé du minimum.** PyTorch minimise, l'objectif se maximise : le signe négatif est tout ce qui sépare les deux. Si vous l'oubliez, votre agent apprend consciencieusement à jouer de pire en pire, et la courbe est parfaitement monotone, ce qui en fait un bogue étonnamment difficile à soupçonner.

Deux précisions d'implémentation, et chacune vaut une ligne de code.

**L'avantage est normalisé** avant usage : on lui retire sa moyenne et on le divise par son écart-type, sur l'ensemble de la trajectoire. Ce n'est pas exigé par les équations, c'est exigé par la pratique : cela stabilise l'entraînement en rendant l'échelle des gradients indépendante de l'échelle des récompenses de la tâche. Notez que cette normalisation change l'espérance de l'objectif et qu'elle est donc, formellement, un biais que l'on accepte en échange de la stabilité.

{{% comment %}}SOURCE: LAPAN ch.16 p.504{{% /comment %}}

**La trajectoire perd sa dernière transition.** L'avantage du pas \(t\) a besoin de la valeur de l'état \(t+1\) ; la dernière transition collectée n'a pas de successeur dans le lot, donc le tableau des avantages est plus court d'un élément que celui des transitions. Cette asymétrie est la source d'une erreur d'indexation silencieuse, et c'est la raison pour laquelle la taille de trajectoire ci-dessus est 2 049 et non 2 048 : un de plus qu'une puissance de deux, précisément pour qu'il reste un compte rond après la perte du dernier élément.

{{% comment %}}SOURCE: LAPAN ch.16 p.504{{% /comment %}}

---

## Ce que cela donne, et l'échec qu'il faut garder

Les résultats maintenant, avec le mauvais à côté du bon.

Sur le guépard sous PyBullet, PPO atteint environ **1 800 en entraînement et 2 500 en test, en 25 millions de pas et huit heures**. Mettez ce chiffre à côté de celui de la section 10.1 : la méthode de référence obtenait moins, en **110 millions de pas et vingt heures**. Quatre fois moins d'interactions, deux fois et demie moins de temps, et un meilleur score. Sur la fourmi, PPO dépasse la référence sur les deux moteurs physiques, et il y arrive presque deux fois plus vite.

{{% comment %}}SOURCE: LAPAN ch.16 p.505-507{{% /comment %}}

Et maintenant l'échec, qui est dans la même colonne du même tableau. Sur le guépard sous **MuJoCo**, la même méthode progresse beaucoup plus lentement, et l'exécution a été arrêtée à 50 millions de pas après douze heures, avec un score nettement inférieur à celui de la référence sur le même environnement. La raison est mécaniquement intéressante : l'agent a appris à **retourner le guépard sur le dos** et à avancer dans cette position, et il n'a jamais réussi à sortir de ce maximum local pendant toute la durée de l'entraînement.

{{% comment %}}SOURCE: LAPAN ch.16 p.505-507{{% /comment %}}

> [!IMPORTANT]
 **Un guépard qui avance sur le dos n'est pas un bogue, et c'est tout l'intérêt de l'exemple.** La récompense demandait d'avancer en dépensant peu d'énergie. Avancer sur le dos satisfait cette demande, moins bien qu'une course, mais suffisamment pour que tout petit changement de politique dans cette position dégrade le score plutôt que de l'améliorer. L'agent est donc dans un maximum local parfaitement légitime du point de vue de l'objectif qu'on lui a donné. Deux leçons, et la seconde est pour votre jalon. Première leçon : un maximum local de ce genre ne se signale par aucun symptôme numérique ; la perte est saine, le rapport reste dans sa bande, et seule une vidéo révèle ce qui se passe. Deuxième leçon : le même algorithme a obtenu un excellent résultat sur le même corps dans l'autre simulateur. Une seule exécution n'aurait donc permis de conclure ni que la méthode est bonne, ni qu'elle est mauvaise. C'est l'argument des graines multiples, et il revient en section 10.6 avec un tableau entier derrière lui.

---

## Ce que l'écrêtage ne garantit pas

Je dois fermer cette section sur une réserve, parce qu'elle fait partie de la méthode et qu'elle est systématiquement omise dans les présentations courtes.

L'écrêtage réduit fortement le risque d'une mise à jour déraisonnable. Il ne l'élimine pas. Rien n'interdit formellement d'aboutir à une nouvelle politique trop éloignée de l'ancienne, pour la raison exposée plus haut : l'objectif cesse de récompenser l'écart, il ne l'empêche pas. La parade employée par les implémentations sérieuses est d'une simplicité désarmante et s'appelle **arrêt précoce** : on mesure, à chaque époque, la divergence moyenne entre la nouvelle politique et celle de la collecte, et dès qu'elle dépasse un seuil, on arrête les pas de gradient sur cette trajectoire et on repart collecter.

{{% comment %}}SOURCE: SPINUP ppo/key-equations{{% /comment %}}

> [!TIP]
 **Le diagnostic propre à cette semaine, et il coûte deux lignes.** Journalisez, à chaque époque, la moyenne de \(\ln r_t(\theta)\) et la fraction des échantillons dont le rapport est sorti de la bande. La première quantité est une estimation de la divergence entre les deux politiques ; la seconde vous dit quelle part de votre minilot ne contribue plus au gradient, puisque les termes écrêtés ont un gradient nul. Si cette fraction atteint la moitié dès la troisième époque, vos sept époques suivantes ne font plus rien d'utile et vous payez du calcul pour rien : réduisez le nombre d'époques, ou raccourcissez la trajectoire. C'est la courbe que je vous demanderai au volet A du laboratoire, et c'est le genre de mesure qui remplace une opinion sur un hyperparamètre.

Un dernier mot sur la famille, pour que vous ne soyez pas perdus en lisant ailleurs. Il existe **deux** variantes de cette méthode. Celle que nous venons de voir écrête le rapport et ne comporte aucun terme de divergence dans son objectif, ni aucune contrainte explicite. L'autre, moins répandue, ne fait pas d'écrêtage et **pénalise** la divergence directement dans l'objectif, avec un coefficient qu'elle adapte automatiquement en cours d'entraînement. La première est la variante dominante en pratique, et c'est la seule que ce cours enseigne et que le laboratoire emploie. Je nomme la seconde une fois, ici, pour que son existence ne vous surprenne pas.

{{% comment %}}SOURCE: SPINUP ppo/background{{% /comment %}}

Deux faits à retenir pour la section 10.6, enfin. Cette méthode est **sur politique**, malgré ses époques multiples : la trajectoire est jetée à la fin, et la collecte suivante se fait sous la politique mise à jour. Et elle fonctionne sur des espaces d'actions **discrets comme continus**, ce qui n'était vrai d'aucune des méthodes de la semaine 9.

{{% comment %}}SOURCE: SPINUP ppo/quick-facts{{% /comment %}}

---
