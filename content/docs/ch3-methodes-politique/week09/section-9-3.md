---
title: "9.3 La route déterministe : DDPG"
weight: 4
---

## Promouvoir le comportement de test au rang de comportement d'entraînement

Voici l'idée de la section, et elle tient en une phrase : prenons la politique d'évaluation de la section 9.2, celle qui renvoie la moyenne sans tirer, et faisons-en la politique d'entraînement.

Un **acteur** qui, à partir de l'état, fournit directement l'action à jouer. Pas une distribution sur les actions : l'action. Ce passage est **déterministe** par construction, puisqu'un réseau de neurones renvoie toujours la même sortie pour la même entrée. Nous l'écrirons \(\mu_\theta(s)\), avec le même symbole que la moyenne gaussienne de la section 9.2, et ce n'est pas une coïncidence de notation : c'est le même objet, auquel on a retiré l'échantillonnage.

{{% comment %}}SOURCE: LAPAN ch.15 p.474{{% /comment %}}

L'idée théorique qui autorise cela date de 2014, et sa version profonde, celle que nous allons écrire, de 2015. Elle porte le nom de **gradient de politique déterministe profond** (*deep deterministic policy gradient*, DDPG). La façon la plus juste de la présenter, je trouve, est celle-ci : DDPG est le Q-learning profond de la semaine 5 transporté dans un espace d'actions continu. Il apprend conjointement une fonction de valeur d'action et une politique ; il apprend la fonction de valeur hors politique, à partir de transitions stockées, par l'équation de Bellman ; et il se sert ensuite de cette fonction de valeur pour apprendre la politique. La maximisation sur les actions, qui est le seul endroit où le Q-learning profond cassait, est remplacée par un passage avant dans l'acteur.

{{% comment %}}SOURCE: SPINUP ddpg/background ; SPINUP ddpg/references ; LAPAN ch.15 p.473{{% /comment %}}

Et une limite à dire tout de suite, parce qu'elle est inhabituelle dans ce cours : cette méthode ne s'applique **qu'aux** espaces d'actions continus. Elle n'est pas une généralisation du réseau Q profond, elle en est la cousine de l'autre côté de la frontière. Sur un espace discret, elle ne s'écrit pas : il n'y a rien à dériver par rapport à une action qui est un entier.

{{% comment %}}SOURCE: SPINUP ddpg/quick-facts{{% /comment %}}

---

## Le critique change de forme, et c'est la leçon d'architecture de la semaine

Le critique, lui aussi, doit changer, et le changement est plus instructif que celui de l'acteur.

Depuis la semaine 5, nos réseaux de valeurs d'action prenaient l'**état** en entrée et sortaient **une valeur par action**, toutes d'un coup. C'était un choix d'efficacité, et un bon : un seul passage avant donnait les dix-huit nombres nécessaires au maximum. Ce choix n'est plus possible. On ne peut pas sortir une valeur par action quand les actions sont en nombre infini.

Le critique de cette semaine prend donc **deux** entrées, l'état **et** l'action, et renvoie **un seul** nombre, la valeur de ce couple. Nous l'écrirons \(q_{\mathbf{w}}(s,a)\). La **Figure 9-3** montre les deux réseaux côte à côte, et je vous demande de la regarder longuement : c'est le seul endroit de la semaine où la phrase « le critique note l'action de l'acteur » est visible comme un **câblage** et non comme une formule.

{{< bookfig src="09-03.png" week="09" >}}

{{% comment %}}SOURCE: LAPAN ch.15 p.474 ; p.476-477{{% /comment %}}

Lisez le câblage de la Figure 9-3 dimension par dimension. L'acteur est une pile droite : observation, couche de 400, ReLU, couche de 300, ReLU, couche de sortie à \(n\) neurones, tangente hyperbolique, action. Le critique est un **Y** : l'observation entre d'un côté et traverse une couche de 400 suivie d'une ReLU ; l'action entre de l'autre côté et est **concaténée** à ce résultat ; le vecteur ainsi formé, de taille \(400 + n\), traverse une couche de 300, une ReLU, puis une couche de sortie à un seul neurone sans activation.

{{% comment %}}SOURCE: LAPAN ch.15 p.476-477{{% /comment %}}

```python
class Acteur(nn.Module):
    """Etat -> action. Deterministe : meme entree, meme sortie."""

    def __init__(self, taille_obs: int, n_actions: int):
        super().__init__()
        self.pile = nn.Sequential(
            nn.Linear(taille_obs, 400), nn.ReLU(),
            nn.Linear(400, 300), nn.ReLU(),
            nn.Linear(300, n_actions), nn.Tanh(),   # action bornee a [-1, 1]
        )

    def forward(self, etats):
        return self.pile(etats)


class Critique(nn.Module):
    """(etat, action) -> UN scalaire. L'action entre au deuxieme etage."""

    def __init__(self, taille_obs: int, n_actions: int):
        super().__init__()
        self.voie_obs = nn.Sequential(
            nn.Linear(taille_obs, 400), nn.ReLU(),
        )
        self.voie_jointe = nn.Sequential(
            nn.Linear(400 + n_actions, 300), nn.ReLU(),
            nn.Linear(300, 1),                      # aucune activation
        )

    def forward(self, etats, actions):
        base = self.voie_obs(etats)
        return self.voie_jointe(torch.cat([base, actions], dim=1))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | acteur déterministe | `acteur(etats)` |
| \(\theta\) | paramètres de l'acteur | `acteur.parameters()` |
| \(q_{\mathbf{w}}(s,a)\) | critique, l'action **en entrée**, un scalaire en sortie | `critique(etats, actions)` |
| \(\mathbf{w}\) | poids du critique | `critique.parameters()` |
| concaténation \((\,\cdot\,,a)\) | l'action rejoint la voie de l'observation | `torch.cat([base, actions], dim=1)` |

Et voilà le point qui rend la suite possible. Les deux réseaux sont des **fonctions dérivables**, donc ils se composent : substituez l'acteur dans le critique et vous obtenez une seule fonction de l'état, \(q_{\mathbf{w}}(s, \mu_\theta(s))\), dérivable de bout en bout par rapport à \(\theta\). Il n'y a rien de mystérieux là-dedans ; un réseau de neurones est une fonction, et composer deux fonctions dérivables donne une fonction dérivable.

{{% comment %}}SOURCE: LAPAN ch.15 p.474{{% /comment %}}

---

## Le gradient de politique déterministe

Nous avons donc, pour chaque état, une quantité qui mesure la qualité de ce que l'acteur propose, et qui dépend de \(\theta\). La performance à maximiser est sa moyenne sur les états visités, et son gradient s'écrit ainsi :

$$
\nabla_\theta J(\theta) = \E_{s \sim \mu}\left[\, \nabla_a\, q_\pi(s,a)\big\rvert_{a = \mu_\theta(s)} \;\; \nabla_\theta\, \mu_\theta(s) \,\right]
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §3 (tex éq. 1){{% /comment %}}

C'est le **gradient de politique déterministe** (*deterministic policy gradient*), et je veux que vous y lisiez trois choses.

Premièrement, sa structure : c'est une **règle de dérivation en chaîne**, et rien d'autre. Le premier facteur, \(\nabla_a q_\pi\), est le gradient du critique **par rapport à l'action**, évalué à l'action que l'acteur propose : il dit dans quelle direction, dans l'espace des actions, la valeur augmente. Le second facteur, \(\nabla_\theta \mu_\theta\), est le gradient de l'acteur par rapport à ses propres paramètres : il dit comment modifier \(\theta\) pour déplacer l'action dans une direction donnée. Mis bout à bout : le critique indique où aller dans l'espace des actions, l'acteur traduit cette indication en modification de poids.

Deuxièmement, ce qui n'y figure pas. Il n'y a **aucune** log-probabilité. Toute la semaine 8 reposait sur \(\nabla_\theta \ln \pi_\theta(a\mid s)\), et ce facteur a disparu, parce qu'il n'y a plus de probabilité : il n'y a qu'une action, et un gradient qui la pousse. C'est une simplification considérable, et c'est aussi ce qui fait que cette méthode est **beaucoup plus avare en échantillons** que celle de la section 9.2.

Troisièmement, un résultat théorique qu'il faut connaître sans le démontrer : le gradient de politique stochastique de la semaine 8 et ce gradient déterministe sont **équivalents**, le second étant la limite du premier quand la variance de la politique tend vers zéro. Autrement dit, nous ne changeons pas de théorie en changeant de route ; nous prenons un cas limite de la théorie de la semaine 8.

{{% comment %}}SOURCE: LAPAN ch.15 p.474{{% /comment %}}

> [!NOTE]
 **Deux \(\mu\) sur la même ligne, et c'est voulu.** Dans l'équation ci-dessus, \(\mu\) sans indice sous le signe d'espérance est la distribution sur politique des états, celle de la semaine 8 : on moyenne sur les états que la politique visite réellement. Et \(\mu_\theta(s)\) avec indice est l'acteur. L'indice tranche, comme la page « Notation » du cours l'a fixé dès le départ, et je n'écrirai **jamais** un \(\mu(s)\) nu pour désigner l'acteur, même si c'est l'écriture la plus répandue ailleurs.

---

## L'objectif de l'acteur, et un critique qui n'est plus optionnel

Dans la pratique, on n'implémente pas le gradient : on écrit l'objectif et on laisse l'autodifférenciation faire la chaîne. L'objectif de l'acteur est une maximisation :

$$
\max_\theta\; \E_{s \sim \mathcal{D}}\left[\, q_{\mathbf{w}}\!\left(s, \mu_\theta(s)\right) \,\right]
$$

{{% comment %}}SOURCE: SPINUP ddpg/key-equations{{% /comment %}}

L'espérance est prise sur les états du **tampon de rejeu** \(\mathcal{D}\), et les poids \(\mathbf{w}\) du critique sont traités comme des **constantes** dans cette maximisation. Comme PyTorch minimise, la quantité effectivement écrite dans le code est l'opposé, moyennée sur un lot \(B\) :

$$
\mathcal{L}_\mu = -\frac{1}{|B|}\sum_{s \in B} q_{\mathbf{w}}\!\left(s, \mu_\theta(s)\right)
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.481{{% /comment %}}

```python
# Pas de l'acteur : une ligne de perte, et un piege dans la ligne suivante.
perte_acteur = -critique(etats_t, acteur(etats_t)).mean()

opt_acteur.zero_grad()
perte_acteur.backward()
opt_acteur.step()          # SEUL l'optimiseur de l'acteur avance.
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | action proposée par l'acteur, **dans le graphe** | `acteur(etats_t)` |
| \(q_{\mathbf{w}}(s,\mu_\theta(s))\) | note donnée par le critique à cette action | `critique(etats_t, acteur(etats_t))` |
| \(\mathcal{L}_\mu\) | opposé de la note moyenne | `perte_acteur` |
| \(\nabla_\theta \mathcal{L}_\mu\) | gradient, obtenu par la chaîne du critique vers l'acteur | `perte_acteur.backward()` |

> [!WARNING]
 **Le piège de ces quatre lignes, et il est silencieux.** La rétropropagation traverse le critique pour atteindre l'acteur : c'est précisément ce qu'on veut. Mais en traversant, elle **dépose des gradients dans les poids du critique**, qui n'ont rien à voir avec l'entraînement du critique. Si vous appelez l'optimiseur du critique après cet appel sans avoir remis ses gradients à zéro, vous entraînez votre critique à maximiser sa propre sortie, ce qui est une divergence garantie en quelques centaines de pas. La discipline est donc : **deux optimiseurs distincts**, et une remise à zéro explicite avant chaque usage. Garder deux optimiseurs n'est pas une élégance, c'est ce qui rend la gestion des gradients lisible.

{{% comment %}}SOURCE: LAPAN ch.15 p.479-481{{% /comment %}}

Il y a maintenant un point théorique que je veux souligner, parce qu'il distingue cette semaine de la précédente de la façon la plus nette. **En semaine 8, le critique était optionnel.** Il servait de référence pour réduire la variance ; retirez-le et vous retombez sur REINFORCE, qui fonctionne. La raison de cette optionnalité, c'est que la politique stochastique **tire** son action, et qu'un tirage au hasard est une barrière pour la rétropropagation : le gradient ne traverse pas un échantillonnage, donc le critique ne pouvait pas être dérivé vers l'acteur, donc il ne pouvait être qu'un facteur d'échelle.

**En semaine 9, le critique est l'objectif.** Il n'y a plus d'échantillonnage entre l'acteur et le critique, donc le gradient traverse, donc le critique n'est plus un correcteur de variance : il **est** la fonction que l'acteur escalade. Retirez-le et il ne reste rien à optimiser. C'est la même paire de mots, acteur et critique, pour un rapport de forces complètement différent.

{{% comment %}}SOURCE: LAPAN ch.15 p.475{{% /comment %}}

---

## Le critique, sa cible, et le retour du hors politique

Reste à entraîner le critique, et là, vous êtes en terrain connu depuis la semaine 5 : une cible de Bellman à un pas, une erreur quadratique, un réseau cible.

La cible, dans la forme à deux cas que le cours emploie depuis la semaine 5 :

$$
y = \begin{cases}
r & \text{si } s' \text{ est terminal} \\[4pt]
r + \gamma\, q_{\mathbf{w}^-}\!\left(s', \mu_{\theta^-}(s')\right) & \text{sinon}
\end{cases}
$$

{{% comment %}}SOURCE: SPINUP ddpg/pseudocode ; LAPAN ch.15 p.480{{% /comment %}}

Et la perte, une erreur quadratique moyenne de Bellman sur un lot tiré du tampon :

$$
L(\mathbf{w}) = \E_{(s,a,r,s') \sim \mathcal{D}}\left[\left( q_{\mathbf{w}}(s,a) - y \right)^2\right]
$$

{{% comment %}}SOURCE: SPINUP ddpg/key-equations{{% /comment %}}

Trois détails dans la cible, et chacun compte.

**Premier détail : quel réseau fournit l'action \(\mu_{\theta^-}(s')\).** C'est l'**acteur cible**, et son résultat est noté par le **critique cible**. Il y a donc deux réseaux cibles, un par réseau entraîné, et la cible est calculée entièrement du côté cible. L'acteur cible est ce qui remplace la maximisation : il fournit l'action qui maximise approximativement le critique cible, et cette approximation coûte un passage avant au lieu d'une optimisation.

{{% comment %}}SOURCE: SPINUP ddpg/key-equations ; LAPAN ch.15 p.480{{% /comment %}}

**Deuxième détail : l'écriture compacte, et une collision de symbole à connaître.** Les implémentations écrivent souvent la cible en une ligne, avec un facteur \((1-d)\) où \(d\) vaut 1 si l'état suivant est terminal et 0 sinon : \(y = r + \gamma(1-d)\,q_{\mathbf{w}^-}(s',\mu_{\theta^-}(s'))\). C'est exactement la forme à deux cas, et c'est la quatrième écriture de « un état terminal vaut zéro » que ce cours vous présente. Attention toutefois : en section 9.6, la lettre \(d\) désignera un tout autre objet, un **délai** de mise à jour. Pour éviter la confusion, le cours garde la forme à deux cas et réserve \(d\) au délai.

**Troisième détail : pourquoi nous avons le droit d'apprendre sur des transitions anciennes.** L'équation de Bellman ne s'intéresse pas à la provenance des transitions. Elle relie la valeur d'un couple état-action à la valeur de l'état suivant, et cette relation est vraie quelle que soit la politique qui a choisi l'action, et quel que soit l'âge de la transition. Toute transition jamais vécue est donc utilisable. C'est l'argument qui autorise le tampon de rejeu, c'est le même qu'en semaine 5, et c'est ce qui fait de DDPG une méthode **hors politique**.

{{% comment %}}SOURCE: SPINUP ddpg/key-equations{{% /comment %}}

Conséquence, et elle est grande : les deux objets de la semaine 5 reviennent. Le **tampon de rejeu**, avec son arbitrage familier, trop petit on surapprend sur un échantillon étroit, trop grand on ralentit l'apprentissage en gardant des transitions produites par une politique périmée, et un réglage à trouver entre les deux ; sur le robot de la Figure 9-2, il contenait 100 000 transitions. Et le **réseau cible**, avec une différence de régime sur laquelle il faut s'arrêter.

{{% comment %}}SOURCE: SPINUP ddpg/key-equations ; LAPAN ch.15 p.479-480{{% /comment %}}

En semaine 5, le réseau cible était recopié intégralement tous les \(N\) pas. Sur les problèmes à actions continues, cette copie brutale fonctionne moins bien, et on la remplace par la **synchronisation douce** (*soft target update*) rencontrée en semaine 6 : à chaque mise à jour, le réseau cible avance d'une petite fraction vers le réseau entraîné :

$$
\mathbf{w}^- \leftarrow \tau\, \mathbf{w} + (1-\tau)\, \mathbf{w}^- \qquad\text{et}\qquad \theta^- \leftarrow \tau\, \theta + (1-\tau)\, \theta^-
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.481 ; SPINUP ddpg/key-equations ; arXiv:1802.09477 §3{{% /comment %}}

avec \(\tau\) petit : 0,005 dans les travaux de la section 9.6, 0,001 dans l'implémentation du robot. Le résultat est un réseau cible qui ne saute jamais, mais qui suit toujours.

> [!WARNING]
 **Trois conventions numériques pour le même paramètre, et elles sont inverses l'une de l'autre.** La convention de ce cours, celle que j'écris ci-dessus, est \(\tau\) **petit** : \(\tau\) est la fraction du **nouveau** réseau qui entre dans la cible, donc \(\tau = 0{,}005\) signifie « avance de un demi-pourcent ». Certaines écritures emploient un paramètre \(\rho = 1-\tau\), donc **proche de 1**, qui est la fraction de l'**ancien** réseau conservée. Et la bibliothèque haut niveau de la semaine 6 expose un paramètre `alpha` qui suit cette seconde convention, d'où des appels de la forme `alpha_sync(alpha=1 - 1e-3)`, c'est-à-dire \(\tau = 0{,}001\). Les trois disent la même chose. Si vous lisez un nombre proche de 1 là où vous attendiez 0,005, vous n'avez pas trouvé un réglage exotique, vous avez changé de convention. Convertissez une fois, notez-le dans votre code, et n'y revenez plus.

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\tau\) | taux de synchronisation douce, petit | `tau = 0.005` |
| \(1-\tau\) | la même chose dans l'autre convention, proche de 1 | `alpha_sync(alpha=1 - 1e-3)` |
| \(\mathbf{w}^-\), \(\theta^-\) | critique cible, acteur cible | `critique_cible`, `acteur_cible` |
| \(y\) | cible de Bellman, calculée entièrement côté cible | `cible` |
| \(\mathcal{D}\) | tampon de rejeu | `tampon` |

```python
def synchroniser_doucement(reseau, reseau_cible, tau: float) -> None:
    """w_cible <- tau * w + (1 - tau) * w_cible, parametre par parametre."""
    with torch.no_grad():
        for p, p_cible in zip(reseau.parameters(), reseau_cible.parameters()):
            p_cible.mul_(1.0 - tau).add_(tau * p)
```

---

## La boucle complète, en neuf étapes

Voici l'algorithme entier. Je l'écris en français, en neuf étapes, et je vous conseille de le garder sous les yeux pendant le volet A du laboratoire.

```
 1. Initialiser l'acteur mu_theta et le critique q_w au hasard
 2. Recopier leurs poids dans l'acteur cible et le critique cible
 3. Jouer un pas : a = ecretage( mu_theta(s) + bruit ),  observer r, s'
    (le bruit est le sujet de la section 9.4 ; sans lui, rien n'explore)
 4. Ranger la transition (s, a, r, s', terminal) dans le tampon D
 5. Tirer un lot B dans D, uniformement, et calculer la cible
        y = r                                      si s' est terminal
        y = r + gamma * q_{w-}( s', mu_{theta-}(s') )   sinon
 6. Pas du critique : minimiser ( q_w(s,a) - y )^2 par rapport a w SEULEMENT
 7. Pas de l'acteur : minimiser  - q_w( s, mu_theta(s) )  par rapport a theta SEULEMENT
 8. Synchronisation douce des deux reseaux cibles, avec tau
 9. Revenir a l'etape 3
```

{{% comment %}}SOURCE: SPINUP ddpg/pseudocode ; LAPAN ch.15 p.479-481{{% /comment %}}

Comparez cette boucle à celle de la semaine 5, étape par étape. Les étapes 1 à 6 et 9 sont le Q-learning profond, à deux mots près : à l'étape 3 le choix de l'action vient d'un réseau au lieu d'un \(\argmax\), et à l'étape 5 le maximum a été remplacé par un passage avant dans l'acteur cible. L'étape 7 est nouvelle, et c'est l'acteur. L'étape 8 remplace la copie périodique. Autrement dit, DDPG n'est pas une nouvelle famille : c'est le Q-learning profond avec l'\(\argmax\) remplacé par un réseau, exactement comme l'introduction l'annonçait.

Deux précisions d'implémentation, et ce sont deux lignes qui décident si la boucle fonctionne. La cible doit être **détachée** du graphe avant le calcul de l'erreur quadratique, faute de quoi le gradient remonterait aussi dans le réseau cible, et vous reconnaissez là le `detach()` de la semaine 5. Et le déroulement de l'expérience se fait sur **un seul pas** : il n'y a pas de cible à \(N\) pas ici, parce que la méthode est hors politique et qu'un retour à \(N\) pas collecté sous une ancienne politique est un biais, pas une amélioration.

{{% comment %}}SOURCE: LAPAN ch.15 p.480{{% /comment %}}

---

## Ce que cela donne, et où va cette famille

Sur le robot quadrupède, cette méthode donne : **cinq millions d'observations, une vingtaine d'heures, et une récompense moyenne de 4,5** sur dix épisodes de test. En rejouant le meilleur modèle, on obtient 3,03, et la vidéo dure onze secondes avant que le robot ne tombe vers l'avant.

{{% comment %}}SOURCE: LAPAN ch.15 p.481-484{{% /comment %}}

Mettons les deux mesures côte à côte, parce que la comparaison est la vraie conclusion de la section :

| Méthode | Trames consommées | Durée | Meilleur score de test |
| --- | --- | --- | --- |
| Politique gaussienne sur politique (section 9.2) | 9 millions | 16 h | 0,35 |
| Politique déterministe hors politique (section 9.3) | 5 millions | 20 h | 4,5 |

Un facteur treize sur le score, avec **moitié moins** de trames. Le gain ne vient pas de l'architecture, qui est comparable, mais du régime : chaque transition est réutilisée des dizaines de fois au lieu d'une seule. Et pour que la lecture reste honnête, deux réserves : la durée est plus longue malgré les trames en moins, parce que chaque pas d'environnement entraîne maintenant deux réseaux ; et un processeur graphique n'apporte ici qu'environ 30 % de gain, parce que les réseaux sont petits et que le temps part dans la simulation physique, qui tourne sur le processeur central. Le seuil de résolution de la tâche, lui, est à 15 : aucune des deux méthodes ne l'atteint.

{{% comment %}}SOURCE: LAPAN ch.15 p.481-484{{% /comment %}}

Un mot, enfin, sur la direction dans laquelle cette famille s'est développée, parce que vous allez la croiser et que je ne veux pas qu'elle vous paraisse étrangère. Gardez l'acteur de cette section, et remplacez le critique par un critique **distributionnel** de la semaine 6, qui prédit non pas un nombre mais une distribution sur 51 atomes répartis entre \(-10\) et 10 ; ajoutez des retours à plusieurs pas. Sur le même robot, cette variante atteint **17,9** après 3,5 millions d'observations et une vingtaine d'heures, soit au-dessus du seuil de résolution de 15. Je ne vous demande pas de l'implémenter, et elle n'est pas au programme du laboratoire ; je vous demande de retenir ce qu'elle démontre : l'essentiel de la marge restante, sur cette tâche, était dans la **représentation de la valeur**, pas dans la représentation de la politique. Et nous retrouverons cette même famille en section 9.4, où son choix de bruit d'exploration servira d'argument.

{{% comment %}}SOURCE: LAPAN ch.15 p.484-488{{% /comment %}}

---
