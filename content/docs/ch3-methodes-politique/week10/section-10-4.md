---
title: "10.4 ACKTR : la courbure, et un échec honnête"
weight: 5
---

## Le second ordre, en un paragraphe

La troisième méthode de la semaine part d'une idée que la section 10.3 vient de mettre sur la table sans la nommer. TRPO a introduit une matrice de courbure \(H\), et il s'en est servi pour corriger la direction du gradient. Pourquoi ne pas aller au bout de cette logique et construire une méthode d'**optimisation du second ordre** (*second-order optimization*) à part entière ?

**ACKTR** est cette méthode, publiée en 2017, et son nom développe en un programme : un acteur-critique à région de confiance utilisant une approximation de la courbure factorisée à la façon de Kronecker. Elle combine donc les deux idées, optimisation du second ordre et région de confiance.

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}

Le second ordre en un paragraphe, parce que c'est tout ce dont nous avons besoin. Une méthode du premier ordre, comme la descente de gradient, ne connaît que la **pente** de l'objectif au point courant : elle sait dans quelle direction descendre, pas de combien. Une méthode du second ordre connaît aussi la **courbure**, c'est-à-dire les dérivées secondes, ce qui lui permet d'estimer la longueur du pas et de converger en beaucoup moins d'itérations. Le prix est brutal : il faut construire et inverser une matrice hessienne dont le côté est le nombre de paramètres, et vous venez de voir en section 10.3 pourquoi c'est impossible à cette échelle. Toutes les méthodes du second ordre praticables sont donc des méthodes qui **approchent** cette matrice d'une façon ou d'une autre.

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}

Deux mots sur la matrice en question, parce que le vocabulaire vous poursuivra. La courbure qui compte ici n'est pas celle de l'objectif : c'est celle de la **divergence** entre les deux politiques, c'est-à-dire la matrice \(H\) de la section 10.3. Cette matrice porte un nom, elle s'appelle l'**information de Fisher** (*Fisher information*), et elle a une interprétation géométrique précise : elle définit la façon dont on mesure les distances dans l'espace des politiques, par opposition à l'espace des paramètres. Le gradient corrigé par son inverse, \(H^{-1}g\), est le **gradient naturel** : c'est la direction de plus forte pente lorsqu'on mesure les déplacements en divergence de politique au lieu de les mesurer en norme euclidienne des poids. Et c'est, mot pour mot, la reformulation que l'introduction de la semaine demandait.

$$
H = \nabla^2_\theta\, \bar{D}_{\mathrm{KL}}\!\left(\theta \,\|\, \theta_{\text{old}}\right)\Big\rvert_{\theta = \theta_{\text{old}}}
\qquad\qquad
\text{gradient naturel} \;=\; H^{-1} g
$$

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}
{{% comment %}}SOURCE: SPINUP trpo/key-equations{{% /comment %}}

---

## K-FAC, et une limite que j'assume

L'approximation sur laquelle ACKTR repose s'appelle **K-FAC**, pour approximation de la courbure par factorisation de Kronecker, et elle date de 2015. L'idée générale est de ne pas approcher la grande matrice d'un bloc, mais de la décomposer couche par couche en produits de deux matrices beaucoup plus petites, dont l'inverse se calcule séparément.

Et voici la limite, que je préfère énoncer plutôt que contourner : **une description détaillée de cette méthode est hors de portée de ce cours**, et je ne vais pas vous en donner une version diluée qui vous laisserait croire que vous l'avez comprise. Je ne peux pas vous en donner une présentation qui tienne la rigueur que les autres sections ont reçue, et je préfère vous le dire que faire semblant. Ce que vous devez en retenir tient en deux phrases : c'est une approximation structurée de l'information de Fisher, exploitant le fait qu'un réseau est fait de couches ; et elle rend le gradient naturel calculable à un coût raisonnable, là où TRPO le calcule par un gradient conjugué.

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}

> [!NOTE]
 **Pourquoi je m'arrête là plutôt que d'en dire plus.** Une des compétences que ce cours essaie de vous transmettre est de savoir où s'arrête ce que l'on sait. J'aurais pu écrire trois paragraphes plausibles sur les produits de Kronecker, et vous auriez eu le sentiment d'avoir appris quelque chose ; vous auriez surtout acquis une confiance non fondée. La section qui suit est, elle, entièrement vérifiable, et elle est bien plus utile.

---

## Ce qui a réellement tourné, et le verdict

Voici maintenant le contenu réel de cette section, et c'est un résultat négatif.

Ce qui a été mis en œuvre et mesuré sur le banc d'essai de la section 10.1, c'est l'acteur-critique de référence dont l'**optimiseur a été remplacé** par un optimiseur K-FAC repris d'un dépôt tiers et adapté, parce qu'il n'existe pas d'implémentation de K-FAC dans PyTorch lui-même. Le critique a été entraîné exactement comme dans la méthode de référence. Le remplacement de l'optimiseur a demandé en outre un **appel supplémentaire à `backward()`** à chaque pas, pour collecter l'information de Fisher. À part cela, le code est celui de la section 10.1.

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}

```python
# ESQUISSE, et elle n'est pas executable : il n'existe pas d'optimiseur K-FAC
# dans PyTorch, et celui employe ici viendrait d'un depot tiers.
#
# Tout le reste de la boucle est celle de la section 10.1 : meme acteur, meme
# critique, meme avantage. SEUL l'optimiseur de l'acteur change.

opt_acteur = KFACOptimizer(acteur, lr=1e-2)        # a la place d'Adam
opt_critique = torch.optim.Adam(critique.parameters(), lr=1e-3)

# --- Passe 1 : collecter l'information de Fisher.
# L'optimiseur a besoin de statistiques sur la distribution de la POLITIQUE,
# et non sur la perte : on retropropage donc une quantite construite a partir
# de la politique elle-meme, avec la collecte activee.
opt_acteur.acc_stats = True
loi = torch.distributions.Normal(acteur(etats), torch.exp(acteur.logstd))
echantillon = loi.sample()
perte_fisher = -loi.log_prob(echantillon).sum(dim=-1).mean()
opt_acteur.zero_grad()
perte_fisher.backward(retain_graph=True)           # LE backward() SUPPLEMENTAIRE
opt_acteur.acc_stats = False

# --- Passe 2 : le vrai gradient de politique, et le pas.
opt_acteur.zero_grad()
perte_acteur = -(logprob * avantages).mean()
perte_acteur.backward()
opt_acteur.step()                                  # pas de GRADIENT NATUREL
```

{{% comment %}}SOURCE: LAPAN ch.16 p.512{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(g\) | gradient de politique ordinaire | gradients après la passe 2 |
| \(H\) | information de Fisher, approchée par factorisation | statistiques internes de l'optimiseur |
| \(H^{-1}g\) | gradient naturel, appliqué par l'optimiseur | ce que fait `opt_acteur.step()` |
| passe de Fisher | la rétropropagation supplémentaire, sur la politique et non sur la perte | `perte_fisher.backward(...)` |
| \(\mathbf{w}\) | poids du critique, entraînés comme en section 10.1 | `opt_critique` |

Et le verdict, que je rapporte tel quel : **cette méthode a été très instable sur les deux environnements et sur les deux moteurs physiques.** La cause n'est pas établie. Deux explications restent ouvertes, et elles sont toutes les deux plausibles : un réglage insuffisant des hyperparamètres, ou des erreurs dans l'adaptation de l'optimiseur tiers.

{{% comment %}}SOURCE: LAPAN ch.16 p.513{{% /comment %}}

Les scores obtenus sont les suivants : **250** sur le guépard sous PyBullet, qui est le plus mauvais chiffre de tout le tableau de la section 10.6 ; **3 100** sur le guépard sous MuJoCo, c'est-à-dire en dessous de la méthode de référence ; **1 820** sur la fourmi sous PyBullet, également en dessous de la référence. Et sur la fourmi sous MuJoCo, l'exécution a bien eu lieu, mais elle n'a produit **aucune amélioration de récompense** mesurable, de sorte qu'aucun meilleur score n'en a été rapporté.

{{% comment %}}SOURCE: LAPAN ch.16 p.513-514{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.520 (image){{% /comment %}}

---

## Ce qu'un échec de reproduction enseigne, et ce qu'il n'enseigne pas

Je pourrais clore cette section en une ligne, et ce serait une erreur pédagogique. Je préfère vous dire pourquoi elle est ici.

ACKTR est une méthode publiée, évaluée par des pairs, et qui annonce des résultats supérieurs à ceux des méthodes du premier ordre. Un praticien attentif l'a mise en œuvre sur un banc d'essai standard, avec le reste de son code inchangé, et il n'a pas reproduit ces résultats. Il le rapporte, et il rapporte en plus qu'il ne sait pas pourquoi.

Voici ce que cela démontre, exactement. Cela démontre que cette méthode, **dans cette mise en œuvre et avec ce réglage**, s'est révélée instable sur ces quatre configurations. Cela démontre aussi quelque chose de plus large et de plus utile : qu'une méthode du second ordre apporte une dépendance supplémentaire, un optimiseur spécialisé que l'écosystème standard ne fournit pas, et que cette dépendance est un coût réel, qui se paie en instabilité quand elle est adaptée à la main.

Et voici ce que cela ne démontre pas. Cela ne démontre pas que la méthode ne fonctionne pas. Cela ne démontre pas que ses auteurs se sont trompés. Un échec de reproduction est une **mesure sur un dispositif complet**, et le dispositif comprend le code, le réglage, l'environnement et la personne. On ne peut pas en extraire un verdict sur la seule idée.

> [!IMPORTANT]
 **Pourquoi cette section est dans la semaine qui porte le jalon 3, et ce que j'attends de vous.** Le jalon 3 vous demande de comparer vos propres courbes à celles d'une autre méthode, et il est pratiquement certain qu'au moins une de vos exécutions ne donnera pas ce que la littérature annonce. Vous aurez alors deux routes. La première est de régler jusqu'à ce que le chiffre vous convienne, puis de ne rapporter que la dernière exécution : c'est ce que presque tout le monde fait, et c'est ce qui rend une bonne partie des comparaisons publiées inutilisables. La seconde est de rapporter ce que vous avez mesuré, avec votre réglage, votre environnement et votre incertitude sur la cause, exactement comme la section ci-dessus le fait. **C'est la seconde que je note.** Un résultat négatif correctement établi, avec son protocole et l'aveu de ce qui reste inexpliqué, vaut plus de points dans ce jalon qu'une courbe flatteuse sans intervalle. Et je ne veux pas lire « prometteur mais délicat » : si une méthode n'a pas fonctionné chez vous, écrivez qu'elle n'a pas fonctionné chez vous, et dites ce que vous avez essayé.

---
