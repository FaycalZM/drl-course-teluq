---
title: "5.7 Les quatre réparations"
weight: 8
---

## L'algorithme naïf, et les quatre raisons pour lesquelles il ne marche pas

Écrivons d'abord la version naïve, celle que l'on obtient en combinant mécaniquement la semaine 4 et les sections 5.2 à 5.5. Elle tient en cinq pas : initialiser les poids du réseau avec des valeurs quelconques ; interagir avec l'environnement et obtenir une transition ; calculer la perte, selon que l'épisode est terminé ou non ; faire un pas de descente de gradient stochastique ; recommencer.

Cet algorithme a l'air simple, et il ne fonctionnera pourtant pas très bien. Quatre problèmes s'y opposent, et je les prends dans l'ordre où ils apparaissent quand on essaie vraiment.

{{% comment %}}SOURCE: LAPAN ch.6 p.172-173{{% /comment %}}

---

## Réparation 1 : un calendrier pour \(\varepsilon\)

Le premier problème est l'interaction, et vous le connaissez : c'est le dilemme exploration-exploitation de la semaine 1, revu en semaine 4. Dans Pong, agir au hasard ne marque pratiquement jamais un point, donc une politique purement aléatoire n'engendre aucune donnée intéressante. Mais agir **gloutonnement** sur un réseau encore mauvais enferme l'agent : il reste coincé avec de mauvaises actions dans certains états, sans jamais essayer de se comporter autrement.

La méthode \(\varepsilon\)-gloutonne de la semaine 4 mélange les deux, et je ne la redéfinis pas : vous l'avez écrite. Ce qui est nouveau cette semaine, c'est qu'on la fait **décroître**. On part de \(\varepsilon = 1{,}0\), c'est-à-dire cent pour cent d'actions aléatoires, et on la diminue lentement jusqu'à une petite valeur.

{{% comment %}}SOURCE: LAPAN ch.6 p.173{{% /comment %}}

La décroissance est **linéaire** en nombre de trames vues, puis plate, et cela s'écrit en une ligne :

$$
\varepsilon_k = \max\!\big(\varepsilon_{\text{final}},\;
 \varepsilon_{\text{départ}} - k / N_{\text{décroissance}}\big)
$$

{{% comment %}}SOURCE: LAPAN ch.6 p.194{{% /comment %}}

```python
EPSILON_DEPART, EPSILON_FINAL, EPSILON_FIN_DECROISSANCE = 1.0, 0.01, 150_000

def epsilon(k: int) -> float:
    """Décroissance LINÉAIRE en nombre de trames, puis plateau."""
    return max(EPSILON_FINAL, EPSILON_DEPART - k / EPSILON_FIN_DECROISSANCE)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\varepsilon_k\) | taux d'exploration à la trame \(k\) | `epsilon(k)` |
| \(\varepsilon_{\text{départ}}\) | valeur initiale, cent pour cent d'aléatoire | `EPSILON_DEPART = 1.0` |
| \(\varepsilon_{\text{final}}\) | plancher, atteint puis conservé | `EPSILON_FINAL = 0.01` |
| \(N_{\text{décroissance}}\) | nombre de trames de la décroissance | `EPSILON_FIN_DECROISSANCE = 150_000` |
| \(k\) | compteur de trames, pas d'épisodes | l'indice de la boucle principale |

Le calendrier original de la méthode étalait la décroissance de \(1{,}0\) à \(0{,}1\) sur **un million** de trames. Celui que nous employons descend plus bas, jusqu'à \(0{,}01\), et beaucoup plus vite, en 150 000 trames. C'est un réglage fin, taillé pour un seul jeu, qui accélère considérablement la convergence sur Pong et qui peut casser la convergence sur d'autres jeux. Retenez-le : les hyperparamètres de la section 5.8 ne sont pas des constantes universelles, ce sont les réglages d'une expérience particulière.

{{% comment %}}SOURCE: LAPAN ch.6 p.185-186{{% /comment %}}

---

## Réparation 2 : le tampon de rejeu, qui résout un problème en créant un autre

Le deuxième problème est plus profond et il vient de l'optimisation, pas de l'apprentissage par renforcement. L'une des exigences fondamentales de la descente de gradient stochastique est que les données d'entraînement soient **indépendantes et identiquement distribuées**. C'est l'hypothèse sous laquelle un gradient calculé sur un petit lot est une estimation raisonnable du gradient sur l'ensemble des données.

Nos données la violent de **deux** façons, et il faut les distinguer parce que les réparations ne sont pas les mêmes.

D'abord, les transitions d'un même épisode sont toutes très proches les unes des autres : deux écrans de Pong séparés d'un trentième de seconde se ressemblent énormément, et la seconde transition n'apprend presque rien que la première n'ait déjà dit. Un lot composé de seize pas consécutifs ne contient donc pas seize informations, mais à peu près une, répétée seize fois.

Ensuite, la distribution des données n'est pas celle que l'on voudrait : elle est produite par la politique **courante**, ou aléatoire, ou \(\varepsilon\)-gloutonne, et non par la politique optimale dont nous cherchons les valeurs.

{{% comment %}}SOURCE: LAPAN ch.6 p.173-174{{% /comment %}}

La réparation est d'une simplicité désarmante : un grand tampon de l'expérience passée, dans lequel on **tire au hasard** au lieu d'utiliser la transition la plus récente. L'implémentation la plus simple est un tampon de taille fixe, les nouvelles transitions étant ajoutées à la fin de sorte qu'elles chassent les plus anciennes. On s'entraîne alors sur des données à peu près indépendantes, et pourtant assez fraîches pour provenir d'une politique récente.

Le compromis est entièrement dans la taille du tampon : trop petit, les transitions d'un lot restent corrélées ; trop grand, on s'entraîne sur le comportement d'un agent qui n'existe plus depuis longtemps.

{{% comment %}}SOURCE: LAPAN ch.6 p.174{{% /comment %}}

```python
import collections
import numpy as np

Transition = collections.namedtuple(
    "Transition", ["obs", "action", "recompense", "termine", "obs_suivante"])


class TamponDeRejeu:
    """D : une file de capacité fixe, où la plus ancienne transition est chassée."""

    def __init__(self, capacite: int):
        self.memoire = collections.deque(maxlen=capacite)

    def __len__(self) -> int:
        return len(self.memoire)

    def ajouter(self, transition: Transition) -> None:
        self.memoire.append(transition)              # chasse la plus ancienne

    def echantillonner(self, taille_lot: int):
        """Tirage UNIFORME et SANS remise : toute transition a le même poids."""
        indices = np.random.choice(len(self.memoire), taille_lot, replace=False)
        lot = [self.memoire[i] for i in indices]
        return (
            np.asarray([t.obs for t in lot]),        # asarray : aucune copie
            np.asarray([t.action for t in lot]),
            np.asarray([t.recompense for t in lot], dtype=np.float32),
            np.asarray([t.termine for t in lot], dtype=bool),
            np.asarray([t.obs_suivante for t in lot]),
        )
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{D}\) | le tampon de rejeu | `TamponDeRejeu` |
| capacité de \(\mathcal{D}\) | nombre de transitions conservées | `collections.deque(maxlen=capacite)` |
| \((s,a,r,s')\) | une transition, plus le drapeau terminal | `Transition` |
| \(B\) | le lot tiré pour un pas d'apprentissage | la valeur de retour de `echantillonner` |
| \(\lvert B\rvert\) | taille du lot | `taille_lot` |
| \(\mu(s)\) | la distribution effective des mises à jour | ce que ce tirage **remplace** |

Un détail de performance, parce que vous le rencontrerez : le passage par `np.asarray` évite une copie des tableaux, et sans cette optimisation les performances chutent d'environ **vingt fois**. Dans une boucle qui tourne des centaines de fois par seconde, la mise en lot n'est pas un détail d'écriture, c'est la moitié du temps de calcul.

{{% comment %}}SOURCE: LAPAN ch.6 p.189{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que c'est la jonction entre les deux moitiés de cette semaine.** Le tampon de rejeu est présenté, et à juste titre, comme une réparation de l'hypothèse d'indépendance des données. Mais relisez la section 5.6 avec le code ci-dessus sous les yeux : tirer au hasard dans un stock de vieilles transitions, **c'est** s'entraîner sur une distribution autre que celle produite par la politique cible. C'est donc, mot pour mot, la définition du troisième ingrédient de la triade fatale. Le tampon de rejeu résout un problème **en créant un autre**, et il le fait sciemment : l'efficacité d'échantillon qu'il apporte vaut largement la garantie théorique qu'il détruit, puisque cette garantie, sans lui, s'appliquerait à un agent trop lent pour être entraîné. Si vous ne devez retenir qu'une chose de ces deux sections, retenez ce marché-là.

{{% comment %}}SOURCE: LAPAN ch.6 p.174{{% /comment %}}
{{% comment %}}SOURCE: SB ch.11 p.286{{% /comment %}}

Une remarque enfin sur le tirage, et c'est un hameçon pour la semaine prochaine. Ce tirage est **uniforme** : toute transition du tampon a exactement la même chance d'être rejouée, qu'elle soit informative ou parfaitement banale. Une transition où l'agent a encaissé son premier point après trois mille pas pèse autant qu'une transition où rien ne s'est passé. C'est manifestement perfectible, cela porte un nom, et c'est la semaine 6.

{{% comment %}}SOURCE: LAPAN ch.6 p.174{{% /comment %}}

---

## Réparation 3 : le réseau cible, pour arrêter de courir après sa propre queue

Le troisième problème est le plus subtil des quatre et c'est celui dont la section 5.2 vous a prévenus.

La cible contient la valeur de l'état suivant. Or l'équation de Bellman donne \(Q(s,a)\) à partir de \(Q(s',a')\), et ces deux états ne sont séparés que d'un seul pas : ils se ressemblent donc beaucoup, et il est très difficile pour un réseau de neurones de les distinguer. Conséquence directe du couplage de la section 5.2 : lorsque nous mettons à jour les poids pour rapprocher \(Q_\theta(s,a)\) de sa cible, nous modifions **aussi**, involontairement, la valeur que le réseau produit pour \(Q_\theta(s',a')\), c'est-à-dire la cible elle-même.

L'image à garder est celle du chien qui court après sa propre queue : nous poursuivons une cible que notre propre mouvement déplace.

{{% comment %}}SOURCE: LAPAN ch.6 p.174-175{{% /comment %}}

La réparation consiste à **figer** la cible. On garde une copie du réseau, et c'est elle, et elle seule, qui fournit la valeur \(Q(s',a')\) de l'équation de Bellman. Cette copie n'est synchronisée avec le réseau principal que périodiquement, une fois tous les \(N\) pas, et \(N\) est un hyperparamètre assez grand, de l'ordre de mille à dix mille itérations d'entraînement. Cette copie est le **réseau cible** (*target network*), et c'est elle que la notation \(Q_{\theta^-}\) désigne.

{{% comment %}}SOURCE: LAPAN ch.6 p.175{{% /comment %}}

```python
import copy

reseau = ValeursActionApprochees(taille_obs, n_actions)
reseau_cible = copy.deepcopy(reseau)        # Q_theta-moins : la copie figée

SYNC_RESEAU_CIBLE = 1_000                   # N, en trames

for k in range(n_trames):
    ...
    if k % SYNC_RESEAU_CIBLE == 0:
        reseau_cible.load_state_dict(reseau.state_dict())   # theta- <- theta
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta\) | le réseau que l'on entraîne | `reseau` |
| \(Q_{\theta^-}\) | la copie figée, qui construit les cibles | `reseau_cible` |
| \(\theta^- \leftarrow \theta\) | la synchronisation périodique | `load_state_dict(reseau.state_dict())` |
| \(N\) | période de synchronisation | `SYNC_RESEAU_CIBLE = 1_000` |

Prenez une minute pour relier cette réparation à la section 5.4, parce que les deux disent la même chose à deux échelles différentes. Le détachement du graphe empêche le gradient de remonter dans la cible **pendant un pas**. Le réseau cible empêche la cible de bouger **pendant mille pas**. Le premier rend la cible constante pour le calcul du gradient ; le second la rend constante dans le temps. L'un est une décision de différentiation, l'autre est une décision d'ingénierie, et elles poursuivent le même but : rendre le problème **supervisé** assez longtemps pour que la descente de gradient ait un sens.

> [!NOTE]
 **Notez bien ce qui n'apparaît nulle part dans ce dispositif : aucun rapport d'échantillonnage préférentiel.** Nous rejouons des transitions produites par de vieilles politiques, et nous ne corrigeons cette provenance par aucun poids correctif, alors que la semaine 3 nous avait appris qu'un changement de politique s'accompagne normalement d'un tel rapport. Ce n'est pas un oubli. Regardez la cible : elle contient \(r\), \(\gamma\) et un \(\max\) sur les actions. Ni \(\pi\) ni \(b\) n'y figurent. Une cible d'action à un pas, construite avec un maximum, n'a besoin d'aucun rapport, et **c'est exactement ce qui autorise le tampon de rejeu à exister**. Si la cible contenait l'action réellement jouée, comme celle de Sarsa, le rejeu de vieilles transitions serait illégitime. Le \(\max\) de Q-learning n'est pas seulement un choix de famille : c'est le permis de conduire du tampon.

{{% comment %}}SOURCE: SB ch.11 §11.1 (résumé de chapitre){{% /comment %}}

---

## Réparation 4 : empiler des trames, qui ne répare pas la triade mais Markov

La quatrième réparation est d'une autre nature que les trois précédentes, et c'est pour cela que je l'ai gardée pour la fin. Les trois premières traitent de l'optimisation. Celle-ci traite de la **propriété de Markov**, c'est-à-dire de la définition même de l'état.

Regardez la **Figure 5-4**. Elle montre deux situations de Pong qui appellent des actions **opposées** : dans l'une la balle vient vers la raquette de l'agent, dans l'autre elle s'en éloigne. Et pourtant un agent qui ne voit qu'une trame à la fois ne peut pas les distinguer, parce qu'une image fixe ne contient aucune information de direction : elle dit où est la balle, jamais où elle va.

{{< bookfig src="05-04.png" week="05" >}}

{{% comment %}}SOURCE: LAPAN ch.6 p.172{{% /comment %}}

Une observation réduite à une seule trame viole donc la propriété de Markov, et elle fait sortir Pong du cadre construit en semaine 1 pour le faire entrer dans celui des **PDM partiellement observables** (*POMDP*). Le second exemple canonique est le jeu de cartes, où les mains des adversaires sont cachées : l'observation ne porte pas tout l'état.

{{% comment %}}SOURCE: LAPAN ch.6 p.175{{% /comment %}}

Et voilà pourquoi j'avais gardé en réserve, depuis la section 5.2, cette phrase-ci : ce que l'approximation de la fonction de valeur ne sait **pas** faire, c'est augmenter la représentation de l'état avec le souvenir des observations passées. Aucune architecture, aucune profondeur, aucun réglage ne fera apparaître une vitesse dans une image fixe. L'information n'y est pas.

{{% comment %}}SOURCE: SB ch.9 p.219{{% /comment %}}

La réparation consiste donc à la **mettre dans l'observation** : on empile \(k\) trames consécutives et l'on donne la pile au réseau. C'est l'**empilement de trames** (*frame stacking*), et la valeur classique de \(k\) pour Atari est quatre. Autant le dire franchement : ce n'est qu'un bricolage, puisqu'il peut exister dans l'environnement des dépendances plus longues que quatre trames, mais pour la plupart des jeux ce bricolage fonctionne bien.

{{% comment %}}SOURCE: LAPAN ch.6 p.175{{% /comment %}}

Quatre trames suffisent pour une balle, qui a une position et une vitesse. Elles ne suffiraient pas pour un jeu où il faut se souvenir d'une porte ouverte il y a deux minutes. La vraie solution à ce second cas est un réseau à mémoire, et ce cours ne le traite pas : retenez simplement que l'empilement est une réponse **à la portée du problème**, et non une réponse générale à l'observabilité partielle.

---

## L'algorithme complet, en dix pas

Les trois premières réparations, prises ensemble, forment la base qui a permis d'entraîner un seul et même réseau Q profond sur quarante-neuf jeux Atari différents. Voici l'algorithme complet, et je le donne sous forme d'encadré parce que c'est à cet encadré que la section 5.8 va se référer, ligne par ligne.

{{% comment %}}SOURCE: LAPAN ch.6 p.175{{% /comment %}}

```
Réseau Q profond (DQN), les dix pas

 1. Initialiser les poids θ de Q_θ et θ⁻ de Q_θ⁻ avec des valeurs aléatoires,
    poser ε ← 1,0 et vider le tampon de rejeu D
 2. Avec probabilité ε, choisir une action aléatoire a ;
    sinon, poser a ← argmax_a Q_θ(s, a)
 3. Exécuter a, observer la récompense r et l'état suivant s'
 4. Ranger la transition (s, a, r, s') dans D
 5. Tirer dans D un lot B de transitions, UNIFORMÉMENT et au hasard
 6. Pour chaque transition du lot, calculer la cible :
        y = r                                  si l'épisode est terminé
        y = r + γ max_{a' ∈ A} Q_θ⁻(s', a')    sinon
 7. Calculer la perte L = (Q_θ(s, a) − y)²
 8. Mettre à jour θ par descente de gradient stochastique, en minimisant L
    par rapport à θ SEULEMENT (θ⁻ est tenu pour constant)
 9. Tous les N pas, recopier θ dans θ⁻
10. Revenir au pas 2
```

{{% comment %}}SOURCE: LAPAN ch.6 p.176{{% /comment %}}

Et la même chose en équations, sur une transition :

$$
y =
\begin{cases}
r & \text{si l'épisode est terminé},\\[4pt]
r + \gamma \max_{a' \in \mathcal{A}} Q_{\theta^-}(s',a') & \text{sinon,}
\end{cases}
\qquad
\mathcal{L} = \big(Q_\theta(s,a) - y\big)^2
$$

{{% comment %}}SOURCE: LAPAN ch.6 p.176{{% /comment %}}

Relisez le pas 8 et comparez-le à la section 5.4 : « par rapport à \(\theta\) seulement » est la traduction en français de `.detach()`. Et relisez le pas 6 : les deux cas sont le masque terminal, qui est la quatrième écriture de « un état terminal vaut zéro ». L'encadré ci-dessus ne contient donc, à proprement parler, aucune idée nouvelle depuis la section 5.5 : il contient quatre décisions d'ingénierie posées autour d'un Q-learning. Tout le reste de la semaine consiste à l'écrire correctement.

---
