---
title: "6.2 Cinq objets, et ce que chacun cache"
weight: 3
---

## Le bon découpage, et ce que chaque objet vous retire des mains

Voici la liste, et c'est le cœur de la première moitié de la semaine.

| L'objet | Ce qu'il fait | Ce qu'il vous retire des mains | Son équivalent en semaine 5 |
| --- | --- | --- | --- |
| **sélecteur d'actions** | des sorties du réseau à des actions | le `if` du tirage aléatoire | votre `if random() < eps` |
| **agent** | d'un lot d'observations à un lot d'actions | la mise en lot et le transfert vers le périphérique de calcul | votre fonction `jouer_un_pas` |
| **source d'expérience** | de l'agent et des environnements à des transitions | la boucle de jeu entière, et sept gestes qu'elle cache | la moitié de votre boucle principale |
| **tampon de rejeu** | stocke et tire des transitions | la gestion de la capacité et du tirage | votre `TamponDeRejeu` |
| **réseau cible** | tient une copie figée à jour | la copie périodique des poids | votre `load_state_dict` tous les mille pas |

{{% comment %}}SOURCE: LAPAN ch.7 p.204{{% /comment %}}

Autour de ces cinq objets vivent des utilitaires : des aides pour la boucle d'entraînement et des enveloppes d'environnement. Ce sont de la plomberie, utile et sans enseignement, et nous ne nous y arrêterons pas.

{{% comment %}}SOURCE: LAPAN ch.7 p.204{{% /comment %}}

Regardez la dernière colonne. Vous avez écrit les cinq, la semaine dernière, sans leur donner de nom. C'est tout ce que fait cette section : donner un nom à cinq choses que vous connaissez déjà, pour pouvoir ensuite les remplacer une par une.

---

## Le **sélecteur d'actions** : quand un `if` devient un attribut

Commençons par le plus petit, et c'est celui qui enseigne le plus par unité de longueur.

Un **sélecteur d'actions** (*action selector*) est un petit morceau de logique qui sait transformer une sortie du réseau en action. Rien de plus. Il travaille en tandem avec l'agent : l'agent produit des nombres, le sélecteur décide ce qu'on en fait. Et il y a deux familles, parce qu'il y a deux sortes de sorties. Si le réseau produit des valeurs d'action, on prend l'argument du maximum ; s'il produit une distribution sur les actions, on y échantillonne.

{{% comment %}}SOURCE: LAPAN ch.7 p.205{{% /comment %}}

Trois sélecteurs suffisent à tout le cours. Un sélecteur glouton, qui prend l'argument du maximum sur le deuxième axe du tenseur, le premier axe étant celui du lot. Un sélecteur par échantillonnage, qui tire une action selon des probabilités. Et un sélecteur \(\varepsilon\)-glouton, qui est le plus intéressant des trois parce qu'il **enveloppe** l'un des deux autres : il tire une action au hasard avec probabilité \(\varepsilon\), et délègue au sélecteur enveloppé sinon.

{{% comment %}}SOURCE: LAPAN ch.7 p.205{{% /comment %}}

L'intuition d'abord, et c'est la politique de la semaine 4. Avec \(\lvert\mathcal{A}\rvert\) actions disponibles, une politique \(\varepsilon\)-gloutonne attribue à l'action gloutonne tout le reste de la masse de probabilité :

$$
\pi(a \mid s) =
\begin{cases}
1 - \varepsilon + \dfrac{\varepsilon}{\lvert\mathcal{A}\rvert}
  & \text{si } a = \argmax_{a'} Q_\theta(s,a'),\\[8pt]
\dfrac{\varepsilon}{\lvert\mathcal{A}\rvert} & \text{sinon.}
\end{cases}
$$

Et voici le code qui la réalise, en deux objets plutôt qu'en un `if` perdu au milieu d'une boucle.

```python
import numpy as np

class SelecteurGlouton:
    """De valeurs d'action vers des actions : argmax sur l'axe des actions."""

    def __call__(self, valeurs: np.ndarray) -> np.ndarray:
        # valeurs : (lot, n_actions) ; l'axe 0 est le lot, l'axe 1 les actions.
        return valeurs.argmax(axis=1)


class SelecteurEpsilonGlouton:
    """Enveloppe un autre sélecteur. epsilon est un ATTRIBUT, pas une constante."""

    def __init__(self, epsilon: float, selecteur=None):
        self.epsilon = epsilon
        self.selecteur = selecteur or SelecteurGlouton()

    def __call__(self, valeurs: np.ndarray) -> np.ndarray:
        actions = self.selecteur(valeurs)
        lot, n_actions = valeurs.shape
        au_hasard = np.random.random(size=lot) < self.epsilon
        actions[au_hasard] = np.random.choice(n_actions, sum(au_hasard))
        return actions
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta(s,\cdot)\) | les valeurs d'action du lot | `valeurs`, forme `(lot, n_actions)` |
| \(\argmax_{a} Q_\theta(s,a)\) | l'action gloutonne | `valeurs.argmax(axis=1)` |
| \(\varepsilon\) | taux d'exploration | `self.epsilon`, **un attribut modifiable** |
| \(\varepsilon / \lvert\mathcal{A}\rvert\) | la part tirée au hasard | `np.random.choice(n_actions, ...)` |
| \(\lvert\mathcal{A}\rvert\) | nombre d'actions | `n_actions`, la deuxième dimension |

Une seule ligne de ce fragment porte tout l'enseignement, et c'est `self.epsilon`. Parce que \(\varepsilon\) est un attribut, il se change **pendant** l'exécution : écrire `selecteur.epsilon = 0.0` suffit à rendre l'agent purement glouton, et un calendrier de décroissance se réduit à une affectation par trame. Comparez avec la semaine 5, où le taux d'exploration était un argument passé de main en main depuis la boucle principale jusqu'au cœur de la fonction qui jouait un pas.

{{% comment %}}SOURCE: LAPAN ch.7 p.206, p.209{{% /comment %}}

> [!TIP]
 **Un conseil de lecture, et il vaut pour les quatre objets suivants.** Devant chaque abstraction de cette section, posez-vous une question unique : *qu'est-ce que j'écrivais à la main la semaine dernière, et qu'est-ce que je n'écris plus ?* Si la réponse est « rien », l'abstraction ne sert à rien. Si la réponse est « quelque chose que je me trompais régulièrement à écrire », elle est utile. Et si la réponse est « quelque chose que je ne savais même pas qu'il fallait écrire », elle est précieuse, et c'est le cas de la section 6.3.

---

## L'**agent** : un lot d'observations, un lot d'actions

Un agent, ici, est un objet dont le contrat tient en une ligne : il transforme un **lot** d'observations en un **lot** d'actions.

{{% comment %}}SOURCE: LAPAN ch.7 p.204{{% /comment %}}

Le pluriel n'est pas une coquetterie, c'est une décision de performance, et c'est la même que celle de la section 5.8 pour la sortie par action. Traiter plusieurs observations en un seul passage dans le réseau est très souvent beaucoup plus rapide que de les traiter une par une, parce qu'un processeur graphique est fait pour cela. Le lot est donc dans le contrat de l'objet, pas dans son implémentation.

{{% comment %}}SOURCE: LAPAN ch.7 p.207{{% /comment %}}

Trois situations expliquent pourquoi l'agent est un objet et non une fonction. Premièrement, un agent peut être fondé sur une politique plutôt que sur une valeur : son réseau produit alors des probabilités d'action et non des valeurs d'action, et c'est la semaine 8. Deuxièmement, un agent peut porter un **état interne**, par exemple une mémoire récurrente pour un problème partiellement observable, et cet état doit être transporté d'un pas au suivant. Troisièmement, un agent peut travailler sur des actions continues, et c'est la semaine 9.

{{% comment %}}SOURCE: LAPAN ch.7 p.207{{% /comment %}}

D'où un détail d'interface qui surprend à la première lecture et qui est le bon choix : l'agent ne renvoie pas des actions, il renvoie un **couple**, les actions et la liste des états internes. Pour un agent sans mémoire, cette seconde valeur est une liste de `None`. Le prix est une valeur de retour un peu encombrante ; le bénéfice est qu'un agent récurrent se branche à la même place, sans toucher à la boucle.

{{% comment %}}SOURCE: LAPAN ch.7 p.209{{% /comment %}}

Un dernier point que je signale sans le développer, parce qu'il est au programme de la semaine 8 : un agent fondé sur la politique attend des **sorties brutes** (*logits*) et non des probabilités, et applique la fonction softmax lui-même si on le lui demande. La raison est la stabilité numérique, exactement comme en semaine 3. Vous avez donc déjà, dans cette interface, la place où la semaine 8 viendra se brancher.

{{% comment %}}SOURCE: LAPAN ch.7 p.210{{% /comment %}}

---

## Le **tampon de rejeu** : trois implémentations derrière une interface

Le tampon de rejeu, vous l'avez écrit. Reprenons tout de même la justification, parce que la section 6.10 va venir la contredire à moitié.

Les échantillons issus de pas consécutifs sont corrélés, et cette corrélation conduit à l'instabilité ; or la descente de gradient stochastique suppose des données indépendantes et identiquement distribuées. D'où un tampon de taille bornée, dans lequel les nouvelles transitions chassent les anciennes, et un tirage au hasard à chaque pas d'apprentissage.

{{% comment %}}SOURCE: LAPAN ch.7 p.217{{% /comment %}}

Ce qui compte, pour cette semaine, est qu'il existe **trois** tampons derrière la même interface. Un tampon uniforme, celui de la semaine 5. Un tampon priorisé naïf, dont le tirage coûte \(O(N)\) opérations pour un tampon de \(N\) transitions. Et un tampon priorisé à **arbre de segments** (*segment tree*), qui ramène ce coût à \(O(\log N)\) au prix d'un code sensiblement plus difficile à lire.

{{% comment %}}SOURCE: LAPAN ch.7 p.217{{% /comment %}}

Je m'arrête une phrase sur l'arbre de segments et je n'y reviendrai pas, parce que c'est exactement le genre de détail qui mange une semaine sans rien enseigner sur l'apprentissage par renforcement. Un arbre de segments est une structure de données qui maintient des sommes partielles sur un tableau, de sorte qu'un tirage proportionnel à des poids se fasse en descendant un arbre au lieu de parcourir tout le tableau. Retenez le passage de \(O(N)\) à \(O(\log N)\), retenez que la différence devient visible quand le tampon dépasse quelques dizaines de milliers de transitions, et sachez que le tampon du laboratoire sera le tampon naïf, qui est largement suffisant sur CartPole.

{{% comment %}}SOURCE: LAPAN ch.7 p.217, ch.8 p.258{{% /comment %}}

L'interface, maintenant, parce que c'est elle qui rend la substitution possible. Elle tient en trois choses : on peut itérer sur le tampon, on peut lui demander de se **remplir** de \(N\) transitions, et on peut lui **tirer** un lot de \(N\) transitions.

{{% comment %}}SOURCE: LAPAN ch.7 p.218{{% /comment %}}

Et voici la boucle d'entraînement d'un réseau Q profond, écrite sur cette interface. Comparez-la avec les six gestes de la section 5.9 : c'est la même, moins la plomberie.

```python
tampon.remplir(TRANSITIONS_INITIALES)      # on remplit AVANT d'apprendre

for pas in itertools.count():
    tampon.remplir(1)                      # 1. un pas d'environnement
    lot = tampon.echantillonner(TAILLE_LOT)  # 2. un lot tiré du tampon

    optimiseur.zero_grad()
    perte = calculer_perte(lot, reseau, reseau_cible, GAMMA)  # 3.
    perte.backward()                       # 4.
    optimiseur.step()                      # 5. et on recommence
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{D}\) | le tampon de rejeu | `tampon` |
| un pas dans l'environnement | l'agent joue, la transition est rangée | `tampon.remplir(1)` |
| \(B \sim \mathcal{D}\) | le lot tiré | `tampon.echantillonner(TAILLE_LOT)` |
| \(\mathcal{L}(\theta)\) | la perte sur le lot | `perte` |
| \(\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}\) | le pas d'optimiseur | `optimiseur.step()` |

Cinq lignes utiles. Tout le reste, le jeu dans l'environnement, la gestion des épisodes, l'accumulation des récompenses, la rotation du tampon, se produit à l'intérieur de `remplir`. C'est commode, et c'est aussi exactement ce qui doit vous inquiéter : nous venons de mettre sous le tapis la partie du programme où se cachent les erreurs les plus silencieuses. La section 6.3 soulève le tapis.

{{% comment %}}SOURCE: LAPAN ch.7 p.218{{% /comment %}}

---
