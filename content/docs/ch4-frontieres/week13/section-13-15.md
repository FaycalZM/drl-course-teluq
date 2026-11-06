---
title: "13.15 Deux familles de réponses : contraindre la politique, ou pessimiser la valeur"
weight: 16
---

## Deux stratégies, et ce que chacune exige de savoir

Le problème est posé. Il y a deux grandes façons d'y répondre, et il vaut la peine de les opposer avant d'entrer dans les formules, parce qu'elles diffèrent par **ce qu'elles supposent connu**.

**Famille 1, contraindre la politique.** On empêche la politique apprise de s'écarter de la politique de comportement, de sorte que la valeur d'action ne soit **jamais interrogée sur une action hors distribution**. La faille de la section 13.14 est alors fermée à la source. Prix à payer : il faut savoir ce qu'est \(\pi_\beta\), ou l'estimer.

**Famille 2, pessimiser la valeur**, ce que l'on nomme aussi le **pessimisme** (*pessimism*). On laisse la politique faire ce qu'elle veut, et on modifie l'estimateur de valeur pour qu'il soit **systématiquement bas** là où il n'a pas de données. L'optimiseur cherche alors toujours les erreurs de son estimateur, comme en section 13.14, mais il n'y trouve plus de promesses : il trouve du pessimisme. Prix à payer : aucune connaissance de \(\pi_\beta\), ce qui est un avantage considérable, mais une tendance à être trop prudent.

Je traite les deux, dans cet ordre.

---

## Famille 1 : garder la politique près des données

Le principe est exactement celui du paragraphe précédent, et il s'appuie sur la remarque structurelle de la section 13.14 : seule l'entrée d'action peut être hors distribution. On s'assure donc que \(\pi(a' \mid s')\) reste proche de \(\pi_\beta(a' \mid s')\), et dans ce cas **les résultats de généralisation habituels de l'apprentissage supervisé devraient s'appliquer**, puisque la valeur d'action n'est plus interrogée que là où elle a appris.

{{% comment %}}SOURCE: OFFLINE p.19-20{{% /comment %}}

Deux questions de conception se posent alors, et elles sont indépendantes.

**Première question : où placer la contrainte ?** Deux possibilités. Une **contrainte de politique** (*policy constraint*) proprement dite, posée comme une contrainte d'optimisation sur la mise à jour de l'acteur. Ou une **pénalité de politique** (*policy penalty*), c'est-à-dire un terme soustrait de la récompense ou de la cible.

**Seconde question : quelle divergence employer ?** Une \(f\)-divergence sous forme explicite, une \(f\)-divergence sous forme implicite, ou une métrique de probabilité intégrale.

{{% comment %}}SOURCE: OFFLINE p.20{{% /comment %}}

**L'équation, première version : la paire contrainte.** C'est le schéma de toute la famille, et il vaut la peine de le lire comme un algorithme en deux lignes qui alternent.

$$
\hat Q^\pi_{k+1} \leftarrow \argmin_Q\; \E_{(s,a,s') \sim \mathcal{D}}\Big[\Big(Q(s,a) - \big(r(s,a) + \gamma\, \E_{a' \sim \pi_k}\big[\hat Q^\pi_k(s',a')\big]\big)\Big)^2\Big]
$$

$$
\pi_{k+1} \leftarrow \argmax_\pi\; \E_{s \sim \mathcal{D}}\Big[\E_{a \sim \pi}\big[\hat Q^\pi_{k+1}(s,a)\big]\Big]
\quad \text{sous la contrainte} \quad D(\pi, \pi_\beta) \le \epsilon_{\text{c}}
$$

{{% comment %}}SOURCE: OFFLINE p.20{{% /comment %}}

Deux conventions de lecture, avant d'aller plus loin. D'abord, \(k\) compte ici les **itérations de la paire**, et non un pas imaginé : il n'y a plus d'imagination dans cette moitié de semaine. Ensuite, le chapeau de \(\hat Q^\pi_k\) distingue l'**estimation** obtenue à l'itération \(k\) de la vraie valeur \(Q^\pi\) de la section 13.12, que personne ne connaît : c'est la même distinction que celle du \(\hat v(s,\mathbf{w})\) de la semaine 7, et toute la section 13.14 porte sur l'écart entre les deux. Et remarquez que **sans la contrainte finale, ces deux lignes sont exactement un acteur-critique hors politique ordinaire**, c'est-à-dire la méthode de la semaine 9 appliquée à un jeu figé, c'est-à-dire le code de la section 13.12. Toute la famille 1 se résume donc à : la même chose, plus une contrainte.

**L'équation, seconde version : la paire à pénalité.** On déplace le terme de divergence de la contrainte vers les objectifs eux-mêmes. Dans la cible :

$$
\hat Q^\pi_{k+1} \leftarrow \argmin_Q\; \E_{\mathcal{D}}\Big[\Big(Q(s,a) - \big(r(s,a) + \gamma\, \E_{a' \sim \pi_k}\big[\hat Q^\pi_k(s',a')\big] - \alpha_{\text{cons}}\, \gamma\, D\big(\pi_k(\cdot \mid s'), \pi_\beta(\cdot \mid s')\big)\big)\Big)^2\Big]
$$

et dans l'objectif de l'acteur :

$$
\pi_{k+1} \leftarrow \argmax_\pi\; \E_{s \sim \mathcal{D}}\Big[\E_{a \sim \pi}\big[\hat Q^\pi_{k+1}(s,a)\big] - \alpha_{\text{cons}}\, D\big(\pi(\cdot \mid s), \pi_\beta(\cdot \mid s)\big)\Big]
$$

{{% comment %}}SOURCE: OFFLINE p.20{{% /comment %}}

> [!TIP]
 **Pourquoi la pénalité entre aussi dans la cible, avec son facteur \(\gamma\) : c'est le détail élégant de cette paire.** La pénalité de l'objectif de l'acteur suffit à décourager un écart **au présent**. Mais on veut davantage : on veut décourager les actions qui **conduisent** à des états où la politique devra s'écarter davantage dans le futur. Or le mécanisme qui propage une conséquence future dans une décision présente, c'est exactement la remontée de Bellman. En plaçant le terme de divergence **dans la cible**, avec son facteur \(\gamma\), on le fait propager comme une récompense négative : s'écarter demain coûte aujourd'hui, actualisé. C'est une idée que vous pouvez réemployer ailleurs : **toute quantité qu'on veut rendre prévoyante se met dans la récompense, pas dans l'objectif**.

---

## Quelle divergence, et pourquoi la plus évidente est la mauvaise

Il reste à choisir \(D\). C'est ici que se trouve, selon moi, la meilleure idée de la section.

La forme générale d'une \(f\)-divergence s'écrit comme une espérance d'une fonction du rapport des deux densités :

$$
D_f\big(\pi(\cdot \mid s), \pi_\beta(\cdot \mid s)\big) \;=\; \E_{a \sim \pi(\cdot \mid s)}\!\left[ f\!\left( \frac{\pi(a \mid s)}{\pi_\beta(a \mid s)} \right) \right]
$$

{{% comment %}}SOURCE: OFFLINE éq. 19 p.20{{% /comment %}}

Avec \(f(x) = \log x\), on retrouve la divergence de Kullback-Leibler, que ce cours emploie depuis la semaine 10. Et elle a une faiblesse pratique immédiate : pour calculer \(\log \pi_\beta(a \mid s)\), il faut **un modèle explicite de la politique de comportement**, qu'on obtient en général par un clonage de comportement. On ajoute donc un apprentissage supervisé, avec ses propres erreurs, à l'intérieur de l'objectif.

Il existe une **forme implicite** qui évite cela, et elle est jolie. On écrit la politique idéale de l'étape comme la politique de comportement **repondérée** par l'exponentielle de la valeur, \(\bar\pi_{k+1} \propto \pi_\beta \exp(Q/\alpha_{\text{cons}})\), puis on y projette la politique paramétrée par une divergence de Kullback-Leibler. En pratique, cela se réduit à quelque chose que vous savez faire en une ligne : **pondérer les échantillons déjà présents dans \(\mathcal{D}\) par \(\exp(Q/\alpha_{\text{cons}})\), et faire une régression supervisée pondérée**. Aucun modèle de la politique de comportement n'est nécessaire, parce qu'elle est présente **en nature** dans les données : les échantillons de \(\mathcal{D}\) *sont* des tirages de \(\pi_\beta\). Le coefficient \(\alpha_{\text{cons}}\) y joue le rôle d'un multiplicateur de Lagrange.

{{% comment %}}SOURCE: OFFLINE p.21{{% /comment %}}

> [!IMPORTANT]
 **Et voici l'idée que je trouve la plus profonde de la section 13.15 : la divergence de Kullback-Leibler est le mauvais outil pour ce travail, et le contre-exemple est limpide.** Supposez que la politique de comportement soit **uniforme** sur les actions. Le jeu de données couvre alors tout, il n'existe **aucune action hors distribution**, et l'apprentissage hors ligne devrait être facile : effectivement, un acteur-critique sans aucune contrainte s'en sort très bien dans ce cas. Or que ferait une contrainte de divergence de Kullback-Leibler ? Elle interdirait à la politique apprise de s'éloigner d'une loi uniforme, c'est-à-dire **l'obligerait à rester très stochastique**, donc très mauvaise. La contrainte détruirait un problème qui n'avait aucune difficulté. Le diagnostic est donc précis : ce qu'on veut interdire, c'est de **sortir** de l'ensemble des actions probables ; ce qu'on ne veut surtout pas interdire, c'est de **se concentrer sur un sous-ensemble** de ces actions. Une divergence de Kullback-Leibler ne distingue pas les deux : elle pénalise toute différence de forme, dans les deux sens.

{{% comment %}}SOURCE: OFFLINE p.22{{% /comment %}}

---

## La réponse : une contrainte de support

La bonne notion est donc le **support**, et non la densité, et la réponse de cette famille s'appelle une **contrainte de support** (*support constraint*).

Si l'on contraint seulement le **support** de la politique apprise à rester dans le support de la politique de comportement, alors la politique apprise peut être **déterministe et optimale**. C'est exactement ce que le contre-exemple ci-dessus demandait : sous une politique de comportement uniforme, tout le domaine est dans le support, et la contrainte n'interdit rien, de sorte que la politique peut se concentrer autant qu'elle veut. Et quand la politique de comportement n'a **pas** un support complet, la contrainte de support empêche toujours les actions hors distribution, qui est le seul service qu'on lui demande.

{{% comment %}}SOURCE: OFFLINE p.22-23{{% /comment %}}

**L'équation.** Pour un espace d'actions discret, cela prend une forme très simple : on pénalise la **masse de probabilité** que la politique apprise met sur les actions dont la probabilité sous la politique de comportement est sous un seuil.

$$
D_{\text{support},\, \varepsilon_{\text{s}}}\big(\pi(\cdot \mid s), \pi_\beta(\cdot \mid s)\big) \;=\; \sum_{a \in \mathcal{A},\; \pi_\beta(a \mid s) \le \varepsilon_{\text{s}}} \pi(a \mid s)
$$

{{% comment %}}SOURCE: OFFLINE éq. 23 p.23{{% /comment %}}

Lisez la condition de la somme : elle ne regarde **que** si une action est rare sous la politique de comportement, sans comparer les deux densités. Une action fréquente dans les données ne contribue rien à cette divergence, quelle que soit la probabilité que la politique apprise lui donne. C'est précisément la propriété que la divergence de Kullback-Leibler n'a pas.

Et cela explique, au passage, un fait structurel : **les \(f\)-divergences comparent des densités, elles sont donc inadaptées à une comparaison de supports en échantillon fini**. Estimer un rapport de densités demande de connaître les deux densités ; décider si une action est dans un support demande seulement de compter. Le second problème est strictement plus facile, et c'est pour cela qu'il se résout mieux.

{{% comment %}}SOURCE: OFFLINE p.22-23{{% /comment %}}

Il existe une troisième voie, que je mentionne en une phrase sans la développer : les **métriques de probabilité intégrales** (*integral probability metric*), dont deux instances connues sont l'écart moyen maximal et la distance de Wasserstein d'ordre un. Elles comparent des lois par leur action sur une famille de fonctions test plutôt que par un rapport de densités, ce qui les rend plus tolérantes au support. Ce cours en reste au constat.

{{% comment %}}SOURCE: OFFLINE p.21{{% /comment %}}

---

## Famille 2 : pessimiser la valeur, et un ancrage très astucieux

Changeons d'angle. Et l'attrait de cette seconde famille se dit en deux arguments, dans cet ordre.

**Premier argument : elle s'applique à tout.** Un acteur-critique, bien sûr, mais aussi un Q-learning pur, même quand **aucune politique n'est représentée explicitement**. Puisque l'intervention porte sur la valeur et non sur la politique, elle ne suppose pas qu'il y ait une politique à contraindre.

**Second argument, et c'est le plus fort : elle évite de modéliser la politique de comportement.** Toute la famille 1 en dépend, soit explicitement, soit par le détour de la repondération. Celle-ci n'en a aucun besoin.

{{% comment %}}SOURCE: OFFLINE p.23{{% /comment %}}

**L'intuition.** On ajoute à l'objectif habituel de la valeur d'action un terme qui **pousse les valeurs vers le bas**. Pas partout : sur les états du jeu de données, et sous une loi d'actions qu'on choisit **adverse**, c'est-à-dire concentrée exactement là où la valeur est la plus grande. L'optimiseur de la politique continue de chercher le maximum ; il trouve une estimation qu'on a déjà rabaissée.

**L'équation.** L'objectif modifié est une somme de deux termes, et le second est l'erreur de Bellman ordinaire.

$$
\tilde{\mathcal{E}}(\mathcal{B}, \mathbf{w}) \;=\; \alpha_{\text{cons}}\, \mathcal{C}(\mathcal{B}, \mathbf{w}) \;+\; \mathcal{E}(\mathcal{B}, \mathbf{w})
$$

avec, pour cette **pénalité conservatrice** (*conservative penalty*) dans sa forme la plus simple,

$$
\mathcal{C}_{\mathrm{CQL}_0}(\mathcal{B}, \mathbf{w}) \;=\; \E_{s \sim \mathcal{B},\; a \sim \nu(a \mid s)}\big[ Q_{\mathbf{w}}(s,a) \big]
$$

{{% comment %}}SOURCE: OFFLINE p.23-24{{% /comment %}}

Ici \(\mathcal{B}\) est le lot tiré dans \(\mathcal{D}\), \(\mathbf{w}\) sont les paramètres de la valeur d'action (le vecteur de poids de la semaine 7), et \(\nu(a \mid s)\) est la **loi d'actions adverse**, celle que l'on choisit pour maximiser le terme qu'on va ensuite minimiser.

> [!IMPORTANT]
 **Et voici l'ancrage, qui est toute l'intuition de cette famille et qui mérite d'être lu deux fois.** Le second terme de l'objectif, l'erreur de Bellman, **continue de forcer les valeurs à obéir à la remontée pour les actions présentes dans les données**. Ces valeurs-là sont donc tenues : on ne peut pas les abaisser sans augmenter l'erreur de Bellman. Avec un \(\alpha_{\text{cons}}\) bien choisi, la pénalité ne peut donc faire baisser que ce qui n'est tenu par rien, c'est-à-dire **les valeurs des actions hors distribution, celles qui sont potentiellement et erronément hautes**. Les actions présentes dans les données sont, selon le mot juste, **ancrées** par l'erreur de Bellman. Le résultat est une **borne inférieure démontrable** sur la vraie valeur d'action de la politique courante : on ne surestime plus, par construction.

{{% comment %}}SOURCE: OFFLINE p.24{{% /comment %}}

---

## La forme fermée, et la variante qu'il faut réellement employer

Reste à choisir la loi adverse \(\nu\). Si on la laisse libre, elle se concentre sur le maximum et le terme devient un simple maximum, ce qui est brutal. On la régularise donc par son entropie :

$$
\nu \;=\; \argmax_\nu\; \E_{s \sim \mathcal{D}}\Big[ \E_{a \sim \nu(a \mid s)}\big[Q_{\mathbf{w}}(s,a)\big] + \mathcal{H}\big(\nu(\cdot \mid s)\big) \Big]
$$

Ce problème a une solution explicite, et c'est la loi de Boltzmann des valeurs : \(\nu(a \mid s) \propto \exp Q_{\mathbf{w}}(s,a)\). En la substituant, la pénalité se réduit à une expression que vous pouvez coder en une ligne :

$$
\mathcal{C}_{\mathrm{CQL}_0}(\mathcal{B}, \mathbf{w}) \;=\; \E_{s \sim \mathcal{B}}\Big[ \log \sum_a \exp Q_{\mathbf{w}}(s,a) \Big]
$$

{{% comment %}}SOURCE: OFFLINE p.24{{% /comment %}}

Et la lecture de cette expression est la partie instructive : **la log-somme-exponentielle est dominée par l'action de plus grande valeur**. Minimiser ce terme revient donc à **rabaisser, en chaque état, la valeur la plus élevée**, quelle qu'elle soit. C'est exactement ce qu'on veut, puisque la section 13.14 a établi que la valeur la plus élevée est aussi, hors distribution, la plus suspecte. Pour un espace d'actions grand ou continu, où la somme n'est pas calculable, on l'estime en échantillonnant des actions dans l'acteur courant et en les repondérant.

**L'équation, et c'est celle à retenir.** La pénalité précédente a un défaut : elle rabaisse **tout**, y compris les valeurs des actions présentes dans les données, ce qui produit une sous-estimation excessive. La correction consiste à **remonter** ce qui est dans le lot, par un second terme :

$$
\mathcal{C}_{\mathrm{CQL}_1}(\mathcal{B}, \mathbf{w}) \;=\; \E_{s \sim \mathcal{B},\; a \sim \nu(a \mid s)}\big[Q_{\mathbf{w}}(s,a)\big] \;-\; \E_{(s,a) \sim \mathcal{B}}\big[Q_{\mathbf{w}}(s,a)\big]
$$

{{% comment %}}SOURCE: OFFLINE p.24{{% /comment %}}

Lisez la différence des deux espérances. La première tire l'action dans la loi **adverse** ; la seconde tire le **couple état-action du lot lui-même**, c'est-à-dire des actions réellement présentes dans les données. On abaisse donc ce que l'adversaire désigne et on relève ce que les données contiennent : c'est un contraste, et il a trois propriétés qu'il faut énoncer ensemble.

**Un.** Ce n'est **plus** une borne inférieure ponctuelle de la vraie valeur d'action. On a perdu cette garantie en ajoutant le second terme.

**Deux.** Cela reste une borne inférieure **en espérance sous la politique courante**, ce qui est la garantie utile, puisque c'est sous cette politique qu'on va agir.

**Trois.** Cela réduit la sous-estimation excessive, et **produit les meilleures performances en pratique**.

Et un cas particulier qui éclaire la forme : **quand la loi adverse coïncide avec la politique de comportement, la pénalité est nulle en moyenne**, puisque les deux espérances portent alors sur la même loi. La pénalité ne mesure donc rien d'autre que l'**écart** entre ce que l'adversaire propose et ce que les données contiennent, ce qui est exactement la quantité pertinente.

---

## Le code de la pénalité conservatrice, et ses deux limites

**Le code.** La pénalité à deux termes, ajoutée à l'erreur de Bellman de la section 13.12. Six lignes.

```python
import torch


def penalite_conservatrice(q_reseau, lot, acteur, n_actions_tirees=10):
    """La penalite a deux termes : on abaisse ce que l'adversaire propose,
    on releve ce que les donnees contiennent.

    Espace d'actions continu : la somme sur les actions est estimee
    en tirant des actions dans l'acteur courant.
    """
    etats, actions_du_lot = lot[0], lot[1]
    n = etats.shape[0]

    # Terme adverse : des actions proposees par la politique courante,
    # qui est, par construction, concentree ou Q est grand.
    etats_rep = etats.repeat_interleave(n_actions_tirees, dim=0)
    actions_adv = acteur(etats_rep)
    q_adv = q_reseau(etats_rep, actions_adv).view(n, n_actions_tirees)
    terme_adverse = torch.logsumexp(q_adv, dim=1).mean()

    # Terme d'ancrage : les actions REELLEMENT presentes dans le lot.
    terme_donnees = q_reseau(etats, actions_du_lot).mean()

    return terme_adverse - terme_donnees


def perte_conservatrice(q_reseau, q_cible, lot, acteur, alpha_cons=5.0, gamma=0.99):
    """L'objectif modifie : alpha * penalite + erreur de Bellman."""
    cible = cible_hors_ligne(lot, q_cible, acteur, gamma)
    pred = q_reseau(lot[0], lot[1])
    erreur_bellman = (pred - cible).pow(2).mean()
    penalite = penalite_conservatrice(q_reseau, lot, acteur)
    return alpha_cons * penalite + erreur_bellman
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\tilde{\mathcal{E}}(\mathcal{B}, \mathbf{w})\) | l'objectif modifié | la valeur rendue par `perte_conservatrice` |
| \(\mathcal{E}(\mathcal{B}, \mathbf{w})\) | l'erreur de Bellman ordinaire, celle qui **ancre** | `erreur_bellman` |
| \(\mathcal{C}_{\mathrm{CQL}_1}\) | la pénalité à deux termes | `penalite_conservatrice` |
| \(\nu(a \mid s)\) | la loi d'actions adverse | `actions_adv`, tirées dans l'acteur |
| \(\log \sum_a \exp Q_{\mathbf{w}}(s,a)\) | la forme fermée, dominée par la plus grande valeur | `torch.logsumexp(q_adv, dim=1)` |
| \(\E_{(s,a) \sim \mathcal{B}}[Q_{\mathbf{w}}]\) | le terme d'ancrage, sur les actions du lot | `terme_donnees` |
| \(\alpha_{\text{cons}}\) | poids de la pénalité | `alpha_cons` |
| \(\mathcal{B}\) | le lot tiré dans \(\mathcal{D}\) | `lot` |

> [!WARNING]
 **Les deux limites de cette famille, et je les donne sans les adoucir.** Première limite : **une pessimisation est trop prudente sur un petit jeu de données**. C'est logique et c'est embêtant. Moins de données signifie moins de régions ancrées par l'erreur de Bellman, donc une pénalité qui rabaisse presque tout, donc une politique qui n'ose plus rien et se rabat sur ce que les données contiennent déjà. La pessimisation est d'autant plus coûteuse qu'elle est nécessaire. Seconde limite, et elle est structurelle : l'accumulation d'erreur reste en \(1/(1-\gamma)^2\), c'est-à-dire de l'ordre de \(H^2\), **et c'est inévitable dans le pire cas**. Vous venez de rencontrer ce carré deux fois dans cette semaine : dans la borne du clonage de comportement en section 13.13, et ici. Ce n'est pas une coïncidence : les deux comptent la même chose, à savoir \(H\) occasions d'entrer hors distribution, chacune coûtant \(O(H)\).

{{% comment %}}SOURCE: OFFLINE p.24-26{{% /comment %}}

> [!TIP]
 **Et une lecture d'ensemble des deux familles, qui est à mon avis la bonne façon de retenir cette section.** Les deux font la même chose par deux bouts différents. La famille 1 **empêche la politique de poser la question** à laquelle la valeur ne peut pas répondre. La famille 2 **fait répondre « je ne sais pas, donc c'est mauvais »** à cette même question. Dans les deux cas, ce qui est réparé est le même objet : l'absence de contradiction. Et dans les deux cas le prix est le même, payé différemment : on renonce à une partie de ce que les données auraient permis. Il n'y a pas de repas gratuit ici, et il n'en existe pas : l'information qui manque manque réellement.

---
