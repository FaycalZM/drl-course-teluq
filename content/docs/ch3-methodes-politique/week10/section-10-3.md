---
title: "10.3 TRPO : la théorie que PPO approche"
weight: 4
---

## Poser le problème pour de vrai, sous contrainte

**L'optimisation de politique à région de confiance** (*trust region policy optimization*, TRPO) est de 2015, et c'est la méthode qui a introduit dans ce domaine l'idée que l'introduction de la semaine a présentée. Elle est réputée difficile, et la réputation est fondée : l'article est dense en mathématiques et la méthode l'est aussi. Je ne vais donc pas vous la faire écrire. Je vais vous la faire **lire**, parce qu'il y a trois choses à en emporter et qu'elles sont toutes les trois utiles.

{{% comment %}}SOURCE: LAPAN ch.16 p.507{{% /comment %}}

La première chose à emporter est la **formulation du problème**, et elle est d'une clarté que PPO n'a pas. Voici ce que TRPO résout, exactement :

$$
\theta_{k+1} = \argmax_{\theta}\; \mathcal{L}(\theta_{\text{old}}, \theta)
\qquad \text{sous contrainte} \qquad
\bar{D}_{\mathrm{KL}}\!\left(\theta \,\|\, \theta_{\text{old}}\right) \le \delta
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Deux objets à définir, et nous les tenons tous les deux. Le premier, \(\mathcal{L}\), est l'**objectif de substitution** (*surrogate objective*), aussi appelé avantage de substitution :

$$
\mathcal{L}(\theta_{\text{old}}, \theta) = \E_{s,a \sim \pi_{\theta_{\text{old}}}}\left[\, \frac{\pi_\theta(a \mid s)}{\pi_{\theta_{\text{old}}}(a \mid s)}\; A^{\pi_{\theta_{\text{old}}}}(s,a) \,\right]
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Si vous avez l'impression de l'avoir déjà vu, c'est que vous l'avez déjà vu : **c'est, au symbole près, l'objectif non écrêté de la section 10.2.** Le rapport entre les deux politiques, pondéré par l'avantage estimé sous l'ancienne. PPO et TRPO maximisent donc la **même** quantité ; toute leur différence est dans la façon d'empêcher cette maximisation d'aller trop loin.

Le second objet est la contrainte, et c'est là que la méthode fait ce que PPO ne fait pas : elle borne explicitement l'écart entre les deux politiques, mesuré comme une **divergence moyenne** :

$$
\bar{D}_{\mathrm{KL}}\!\left(\theta \,\|\, \theta_{\text{old}}\right) = \E_{s \sim \pi_{\theta_{\text{old}}}}\left[\, \KL\!\left(\pi_\theta(\cdot \mid s)\;\middle\|\;\pi_{\theta_{\text{old}}}(\cdot \mid s)\right) \,\right]
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Lisez bien ce qu'il y a dans cette ligne, parce que chaque morceau porte quelque chose. À l'intérieur, pour un état donné, on compare deux distributions **sur les actions** : l'ancienne politique et la nouvelle, dans ce même état. À l'extérieur, on **moyenne** cette comparaison sur les états que l'ancienne politique visite réellement. La contrainte ne dit donc pas « que les deux politiques se ressemblent partout » : elle dit « qu'elles se ressemblent là où l'agent va ». C'est une contrainte sur la **politique**, et elle est mesurée là où les données existent.

> [!WARNING]
 **Un mot sur ce qualificatif, parce qu'il circule faux et que la différence est réelle.** La quantité ci-dessus est une divergence **moyenne** sur les états, et c'est ce que la barre au-dessus du \(D\) signifie. Vous lirez parfois que la contrainte de TRPO porte sur la divergence **maximale** entre les deux politiques. Ce sont deux contraintes distinctes : la version maximale demande que les deux politiques soient proches dans **tous** les états, y compris ceux qui ne sont presque jamais visités, et elle est beaucoup plus sévère. L'article de TRPO distingue d'ailleurs explicitement les deux et explique que la version moyenne est celle qui est mise en œuvre, parce que la version maximale est impraticable. Le cours écrit donc **moyenne**, et n'emploie pas le mot « maximale » dans ce contexte.

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Il reste à écrire la divergence elle-même, et je le fais avec un soin particulier.

$$
\KL(P \,\|\, Q) = \sum_i p_i \,\ln \frac{p_i}{q_i}
$$

{{% comment %}}SOURCE: source-assets/notation.md §3{{% /comment %}}

C'est la **divergence de Kullback-Leibler** entre deux distributions discrètes, et le cours l'a introduite en semaine 3, où elle servait déjà à mesurer l'écart entre deux politiques. Elle vaut zéro si et seulement si les deux distributions coïncident, elle est positive partout ailleurs, et elle n'est pas symétrique : l'ordre des arguments compte.

> [!IMPORTANT]
 **Une mise en garde que je vous dois, et qui est utile bien au-delà de cette semaine.** Il circule, y compris dans des textes imprimés et sérieux, une autre formule présentée sous le nom de divergence de Kullback-Leibler : \(-\sum_i p_i \ln q_i\). Cette expression existe, elle est importante, et elle a un nom : c'est l'**entropie croisée** \(H(P,Q)\), celle que vous utilisez comme fonction de perte en classification depuis la semaine 2. Ce n'est pas la divergence KL. La différence est le terme \(-\sum_i p_i \ln p_i\), c'est-à-dire l'entropie de \(P\) elle-même : l'entropie croisée vaut la divergence KL **plus** l'entropie de \(P\). Les deux quantités ne sont donc égales que si \(P\) est déterministe, et elles ne jouent pas le même rôle : l'entropie croisée n'est pas nulle quand les deux distributions coïncident, elle vaut alors l'entropie de \(P\), de sorte qu'elle ne peut pas servir de budget dans une contrainte comme celle ci-dessus. Le test de reconnaissance est immédiat : **une divergence KL contient un quotient, une entropie croisée n'en contient pas.** Et pourquoi j'insiste : la formule correcte est le cœur de la contrainte que nous sommes en train de poser, et un étudiant qui coderait l'entropie croisée à sa place obtiendrait un budget qui ne vaut jamais zéro, donc une contrainte qui ne se relâche jamais, et une méthode qui n'avance plus.

{{% comment %}}SOURCE: source-assets/notation.md §3{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-03.md{{% /comment %}}

Et une dernière remarque, qui rend la formulation naturelle plutôt que technique. Au point \(\theta = \theta_{\text{old}}\), l'objectif **et** la contrainte valent tous les deux zéro, et le gradient de la contrainte y est nul lui aussi. La contrainte est donc inactive au départ et ne devient contraignante qu'à mesure qu'on s'éloigne : c'est exactement le comportement qu'on attend d'un budget de déplacement.

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

---

## D'où vient l'objectif de substitution, et pourquoi il porte ce nom

Un détour de deux paragraphes, parce qu'il explique le mot « substitution » et parce qu'il introduit un objet que vous rencontrerez partout dans cette littérature.

La performance d'une politique est son rendement actualisé espéré, que l'on note ici \(\eta\) :

$$
\eta(\pi) = \E\left[\, \sum_{t=0}^{\infty} \gamma^{\,t} R_{t+1} \,\right]
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.508 (image){{% /comment %}}

Ce que l'on voudrait maximiser, c'est \(\eta\) de la nouvelle politique. Le problème est qu'on ne peut pas le mesurer sans jouer avec la nouvelle politique, ce qui est précisément ce qu'on essaie d'éviter. On construit donc une quantité qui s'évalue avec les **anciens** échantillons et qui approche la vraie performance. Il faut pour cela une façon de dire à quelle fréquence chaque état est visité, et c'est la **fréquence de visite actualisée des états** (*discounted visitation frequency*) :

$$
\rho_\pi(s) = P(s_0 = s) + \gamma\, P(s_1 = s) + \gamma^2\, P(s_2 = s) + \dots
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.507 (image){{% /comment %}}

Chaque terme est la probabilité de rencontrer l'état \(s\) à une position donnée d'une trajectoire, et l'actualisation pèse les positions tardives moins que les précoces. C'est la distribution sur politique des états de la semaine 8, munie d'une actualisation explicite.

Avec ces deux objets, l'objectif de substitution s'écrit sous sa forme originale : la performance de l'ancienne politique, **plus** l'avantage que la nouvelle politique récolte sur la distribution d'états de l'ancienne.

$$
L_\pi(\tilde\pi) = \eta(\pi) + \sum_s \rho_\pi(s) \sum_a \tilde\pi(a \mid s)\, \Adv(s,a)
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.508 (image){{% /comment %}}

Ici \(\pi\) est l'ancienne politique et \(\tilde\pi\) la candidate. Lisez la somme intérieure : pour chaque état, on demande à la nouvelle politique quelles actions elle choisirait, et on les note avec l'avantage **de l'ancienne**. C'est tout ce que l'on peut faire avec les données disponibles, et c'est en cela que cette quantité est une substitution : elle remplace ce qu'on veut mesurer par ce qu'on peut mesurer, et elle est fidèle **aussi longtemps que les deux politiques visitent à peu près les mêmes états**. D'où la contrainte. Les deux formes, celle-ci et le rapport de la section 10.2, décrivent le même objet ; la seconde est celle sous laquelle on optimise, parce qu'elle s'estime directement par une moyenne sur un lot de transitions.

---

## Quatre mouvements pour rendre le problème calculable

Nous avons un problème d'optimisation sous contrainte dans un espace à plusieurs millions de dimensions. Voici comment TRPO le rend calculable, en quatre mouvements et pas un de plus.

**Mouvement 1 : développer les deux fonctions au voisinage de \(\theta_{\text{old}}\).** L'objectif est développé au premier ordre, la contrainte au second. Ce choix n'est pas arbitraire : la contrainte et son gradient étant nuls au point de départ, son premier terme non nul est justement le terme quadratique.

$$
\mathcal{L}(\theta_{\text{old}}, \theta) \approx g^{\mathsf{T}}\left(\theta - \theta_{\text{old}}\right)
\qquad\qquad
\bar{D}_{\mathrm{KL}}\!\left(\theta \,\|\, \theta_{\text{old}}\right) \approx \tfrac{1}{2}\left(\theta - \theta_{\text{old}}\right)^{\mathsf{T}} H \left(\theta - \theta_{\text{old}}\right)
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Le vecteur \(g\) est le gradient de l'objectif de substitution en \(\theta_{\text{old}}\), et voici un cadeau pour l'économie de ce cours : **ce gradient est exactement le gradient de politique de la semaine 8.** Pas un parent, pas une variante : le même objet, celui que vous avez déjà codé. La matrice \(H\) est la hessienne de la divergence moyenne, c'est-à-dire sa courbure au point de départ.

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

**Mouvement 2 : résoudre le problème quadratique.** Maximiser une forme linéaire sous une contrainte quadratique est un problème classique, qui se résout analytiquement par la dualité lagrangienne. La solution est :

$$
\theta_{k+1} = \theta_{\text{old}} + \sqrt{\frac{2\delta}{g^{\mathsf{T}} H^{-1} g}}\; H^{-1} g
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Arrêtons-nous une seconde sur cette ligne, parce qu'elle a un nom et une importance qui dépassent TRPO. La direction du pas n'est pas \(g\), c'est \(H^{-1}g\), c'est-à-dire le gradient **corrigé par l'inverse de la courbure de la divergence**. Cette direction s'appelle le **gradient naturel de politique**, et la racine carrée devant elle est simplement le facteur d'échelle qui place le pas exactement sur le bord du budget \(\delta\). Si l'on s'arrêtait là, on aurait un algorithme complet, et c'est d'ailleurs un algorithme qui existe sous ce nom.

**Mouvement 3 : ne pas s'arrêter là, parce que les deux développements mentent un peu.** Le pas ci-dessus est optimal pour le problème **approché**, pas pour le vrai. À cause des erreurs d'approximation introduites par les développements de Taylor, il peut violer la contrainte de divergence, ou même ne pas améliorer l'objectif de substitution. TRPO ajoute donc une **recherche linéaire par rebroussement** : on essaie le pas complet, on vérifie les deux conditions, et si elles ne sont pas satisfaites on réduit le pas d'un facteur constant et on réessaie.

$$
\theta_{k+1} = \theta_{\text{old}} + \alpha_{\text{ls}}^{\,j}\; \sqrt{\frac{2\delta}{g^{\mathsf{T}} H^{-1} g}}\; H^{-1} g
\qquad\qquad \alpha_{\text{ls}} \in (0,1)
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

L'exposant \(j\) est le nombre de rebroussements, c'est-à-dire le plus petit entier pour lequel le pas réduit satisfait la contrainte et améliore l'objectif. Le coefficient \(\alpha_{\text{ls}}\) est le facteur de réduction, typiquement un peu moins que 1.

> [!NOTE]
 **Deux lettres déclarées ici, comme annoncé en introduction.** Le coefficient de rebroussement s'écrit traditionnellement \(\alpha\), lettre que ce cours a réservée au pas d'apprentissage depuis la semaine 3 : je l'écris donc \(\alpha_{\text{ls}}\), et je l'appelle en français le **facteur de rebroussement**. Et le budget de la contrainte s'écrit \(\delta\), sans indice, qui n'a rien à voir avec le résidu temporel \(\delta_t\) de la section 10.2. L'indice tranche, comme pour \(\mu\) en semaine 9 : avec indice c'est un résidu, sans indice c'est un budget.

**Mouvement 4 : ne jamais former \(H^{-1}\).** Et c'est le mouvement le plus instructif des quatre, parce que c'est une pure décision d'ingénierie et qu'elle décide de la faisabilité de tout le reste.

---

## Pourquoi un gradient conjugué, et jamais une inversion

Regardez la taille de \(H\). C'est une matrice carrée dont le côté est le nombre de paramètres de la politique. Pour un réseau modeste de cent mille paramètres, cela fait dix milliards de coefficients, soit quarante gigaoctets en simple précision, et l'inverser coûterait de l'ordre de \(10^{15}\) opérations. Pour un réseau d'un million de paramètres, les deux chiffres sont à multiplier par cent et par mille. Calculer et stocker \(H^{-1}\) est donc, très concrètement, hors de question dès qu'on parle de réseaux de neurones.

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

TRPO contourne l'obstacle en remarquant qu'il n'a pas besoin de \(H^{-1}\) : il a besoin du **vecteur** \(x = H^{-1}g\), ce qui est tout autre chose. Ce vecteur est la solution du système linéaire \(Hx = g\), et il existe une méthode classique pour résoudre un tel système sans jamais former la matrice, la **méthode du gradient conjugué** (*conjugate gradient*). Cette méthode est itérative, et son unique besoin est une fonction qui, à un vecteur \(x\) donné, sait rendre le produit \(Hx\).

Et ce produit s'obtient sans la matrice, par une double dérivation :

$$
Hx = \nabla_\theta \left(\, \left(\nabla_\theta \bar{D}_{\mathrm{KL}}\!\left(\theta \,\|\, \theta_{\text{old}}\right)\right)^{\mathsf{T}} x \,\right)
$$

{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

Lisez la mécanique : on dérive la divergence une première fois, ce qui donne un vecteur ; on fait le produit scalaire de ce vecteur avec \(x\), ce qui donne un scalaire ; et on dérive ce scalaire une seconde fois, ce qui donne \(Hx\). Deux passes de rétropropagation, aucune matrice. C'est exactement le genre d'opération que l'autodifférenciation de PyTorch sait faire, et c'est pour cela que la méthode est implémentable du tout.

Voici les deux morceaux de code qui portent la méthode. Je les donne en PyTorch, écrits pour être lus et non exécutés, parce que l'essentiel de TRPO est une plomberie de gradients et que je ne vous demanderai pas de l'écrire.

```python
import torch


def perte_substitution(acteur, etats, actions, anciennes_logprob, avantages):
    """L'objectif de substitution : le rapport PPO, SANS ecretage."""
    mu = acteur(etats)
    sigma = torch.exp(acteur.logstd)
    loi = torch.distributions.Normal(mu, sigma)
    logprob = loi.log_prob(actions).sum(dim=-1)
    ratio = torch.exp(logprob - anciennes_logprob)
    # Aucun clamp, aucun minimum : c'est la contrainte qui s'en charge.
    return (ratio * avantages).mean()


def kl_moyenne_gaussiennes(acteur, etats, mu_old, logstd_old):
    """KL moyenne entre deux gaussiennes diagonales, forme analytique.

    Pour chaque dimension d'action :
        KL = ln(s1/s0) + (s0^2 + (m0 - m1)^2) / (2 s1^2) - 1/2
    avec l'indice 0 pour l'ANCIENNE politique et 1 pour la nouvelle.
    """
    mu_new = acteur(etats)
    logstd_new = acteur.logstd.expand_as(mu_new)
    var_old = torch.exp(2.0 * logstd_old)
    var_new = torch.exp(2.0 * logstd_new)

    kl = (logstd_new - logstd_old
          + (var_old + (mu_old - mu_new).pow(2)) / (2.0 * var_new)
          - 0.5)
    return kl.sum(dim=-1).mean()          # somme sur les actions, moyenne sur les etats


def produit_hessien_vecteur(acteur, etats, mu_old, logstd_old, x, amorti=0.1):
    """Hx, sans jamais former H. Deux retropropagations."""
    kl = kl_moyenne_gaussiennes(acteur, etats, mu_old, logstd_old)
    params = list(acteur.parameters())

    # 1re derivation : le graphe est CONSERVE pour pouvoir deriver a nouveau.
    grads = torch.autograd.grad(kl, params, create_graph=True)
    grad_plat = torch.cat([g.reshape(-1) for g in grads])

    # 2e derivation, du produit scalaire avec x.
    produit = (grad_plat * x).sum()
    hx = torch.autograd.grad(produit, params)
    hx_plat = torch.cat([h.reshape(-1) for h in hx])

    # Amortissement : H peut etre mal conditionnee, on ajoute un petit multiple
    # de l'identite pour que le gradient conjugue converge.
    return hx_plat + amorti * x
```

{{% comment %}}SOURCE: LAPAN ch.16 p.508-509{{% /comment %}}
{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{L}(\theta_{\text{old}},\theta)\) | objectif de substitution, sans écrêtage | `perte_substitution(...)` |
| \(g\) | son gradient, **le gradient de politique de la semaine 8** | `torch.autograd.grad` sur la ligne précédente |
| \(\bar{D}_{\mathrm{KL}}\) | divergence moyenne entre les deux politiques | `kl_moyenne_gaussiennes(...)` |
| \(H\) | hessienne de la divergence, la métrique de courbure | jamais formée |
| \(Hx\) | produit hessienne-vecteur, par double dérivation | `produit_hessien_vecteur(...)` |
| \(x = H^{-1}g\) | le gradient naturel, solution de \(Hx=g\) | sortie du gradient conjugué |
| \(\delta\) | budget de divergence | un argument de ligne de commande |
| \(\alpha_{\text{ls}}^{\,j}\) | facteur de rebroussement à la \(j\)-ième tentative | la boucle de recherche linéaire |

> [!NOTE]
 **Une franchise sur ce code, et elle est de méthode.** Deux détails de ce fragment ne viennent d'aucune équation de cette section : le terme d'amortissement ajouté à \(Hx\), et la forme analytique de la divergence entre deux gaussiennes. Le premier est une précaution numérique indispensable, parce que la hessienne d'une divergence estimée sur un lot fini est souvent mal conditionnée. Le second est un gain de précision et de vitesse : on **pourrait** estimer la divergence par échantillonnage, mais entre deux gaussiennes diagonales elle a une expression fermée, et une expression fermée vaut toujours mieux qu'une estimation bruitée dans une contrainte. Je les signale parce que c'est la règle de la semaine 9 que j'applique encore : quand une équation et un code diffèrent, on dit lequel des deux on montre, et on n'en fond jamais silencieusement un troisième.

---

## PPO, dit en une phrase

Et voici la phrase pour laquelle j'ai inversé l'ordre de la semaine. Elle vaut mieux qu'un résumé, parce qu'elle définit les deux méthodes l'une par l'autre :

**PPO est TRPO dans lequel le gradient conjugué et la recherche linéaire ont été remplacés par un simple écrêtage du rapport entre les politiques.**

{{% comment %}}SOURCE: LAPAN ch.16 p.509{{% /comment %}}

Reprenez les deux sections avec cette phrase en main, et comptez ce qui est commun. L'objectif maximisé est le même, au symbole près. La grandeur contrôlée est la même, l'écart entre l'ancienne et la nouvelle politique. Ce qui diffère est uniquement le **mécanisme de contrôle** : TRPO pose une contrainte explicite et paie pour la respecter, en courbure, en double dérivation, en gradient conjugué et en recherche linéaire ; PPO renonce à la contrainte et supprime seulement l'**incitation** à la violer, ce qui coûte une ligne de `clamp`. Deux ingénieries très différentes au service d'une seule idée, et c'est précisément pourquoi la section 10.2 devait venir d'abord : vous avez appris l'idée sous sa forme la moins chère, et vous voyez maintenant ce que coûte sa forme exacte.

Une précision d'honnêteté, enfin, sur ce qui tourne réellement quand on lance TRPO. Il n'existe pas, pour cette méthode, d'implémentation de référence courte et autonome : les mises en œuvre disponibles reprennent toutes, d'un dépôt à l'autre, les mêmes fonctions de gradient conjugué et de recherche linéaire, qui descendent du code original des auteurs. Les deux morceaux que j'ai montrés ci-dessus sont les seuls qui soient vraiment spécifiques à la méthode ; tout le reste est une plomberie d'optimisation numérique partagée. C'est une raison supplémentaire pour que le laboratoire ne vous demande pas de l'écrire, et c'en est une bonne pour que PPO ait gagné.

{{% comment %}}SOURCE: LAPAN ch.16 p.508-509{{% /comment %}}

---

## Ce que cela donne : excellent sur un corps, presque nul sur l'autre

Les résultats, et ils sont les plus contrastés de la semaine.

Sur le guépard sous PyBullet, TRPO obtient **2 419**, dans la moyenne des autres méthodes. Sur le guépard sous MuJoCo, il obtient **5 753**, qui est le meilleur résultat de toute la famille sur politique sur cet environnement, nettement au-dessus de la référence et de PPO. Un très bon guépard, donc.

Et sur la fourmi, **834** sous PyBullet et **993** sous MuJoCo, c'est-à-dire entre un cinquième et un sixième de ce que la méthode de référence obtient sur le même corps. La raison est connue et observable : l'entraînement s'est enfermé dans un minimum local où l'agent **reste debout sans bouger**. La politique apprise tient la fourmi en équilibre, ce qui lui évite les pénalités d'énergie et de chute, et n'avance nulle part.

{{% comment %}}SOURCE: LAPAN ch.16 p.510-511{{% /comment %}}

> [!IMPORTANT]
 **Une méthode, deux corps, et un facteur six d'écart : voilà l'argument des graines multiples, servi sur un plateau.** Si vous n'aviez lu que la colonne du guépard sous MuJoCo, vous auriez conclu que TRPO est la meilleure méthode sur politique de la semaine. Si vous n'aviez lu que la colonne de la fourmi, vous auriez conclu qu'elle ne fonctionne pas. Les deux conclusions reposent sur une exécution, et les deux sont fausses parce qu'elles sont trop générales. La conclusion que les chiffres autorisent est plus modeste et plus utile : sur ce banc d'essai, dans cette configuration, cette méthode a excellé sur un corps et s'est enfermée dans un minimum local sur l'autre. Et la bonne question suivante n'est pas « quelle méthode est la meilleure », c'est « combien de fois ce minimum local se produit-il sur dix graines », une question à laquelle une exécution unique ne peut pas répondre. Le jalon 3 vous demandera cette discipline, et la section 10.6 va vous montrer qu'elle n'est pas une exigence de pédagogue.

---
