---
title: "3.5 L'échec sur FrozenLake"
weight: 6
---

## Le même code, sur un autre environnement

Voici le moment de la semaine que je préfère enseigner. Notre implémentation ne dépend d'**aucun détail propre à l'environnement** : elle reçoit un vecteur d'observations, elle renvoie un indice d'action, elle note les épisodes par leur retour. On pourrait la brancher sur un modèle d'entrepôt dont les observations seraient des quantités de produits et la récompense l'argent gagné, sans toucher une ligne. Cette généralité est la grande promesse de la méthode, et c'est ce qui va rendre son échec instructif : quand il surviendra, il n'y aura **rien de faux dans le code**.

{{% comment %}}SOURCE: LAPAN ch.4 p.132{{% /comment %}}

Prenons donc un autre environnement, FrozenLake, un **monde en grille** (*grid world*) de 4 × 4 cases. L'agent démarre en haut à gauche et doit atteindre l'objectif en bas à droite. Quatre actions : haut, bas, gauche, droite. Certaines cases sont des trous : y tomber termine l'épisode avec une récompense de 0. Atteindre l'objectif donne une récompense de **1,0** et termine également l'épisode. La **Figure 3-3** montre la grille telle que l'environnement la dessine.

{{< bookfig src="03-03.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.132{{% /comment %}}

Le lac est glissant, et c'est là tout son sel. L'action demandée n'est exécutée telle quelle qu'avec une probabilité d'environ 0,33 ; sinon, l'agent part dans l'une des deux directions perpendiculaires, chacune avec la même probabilité. Dit autrement, votre action est remplacée une fois sur trois par sa version tournée de 90 degrés. Vouloir aller à droite ne veut donc pas dire aller à droite.

{{% comment %}}SOURCE: LAPAN ch.4 p.132, p.138{{% /comment %}}

Côté interface, l'espace d'observations est `Discrete(16)` et l'espace d'actions `Discrete(4)` ; `reset()` renvoie l'indice 0, celui de la case de départ. Un seul obstacle technique nous sépare donc de notre agent : notre réseau attend un **vecteur** de flottants, et l'environnement lui tend un **entier**. La réponse est une enveloppe d'observation, exactement de la famille écrite en semaine 1, qui convertit l'entier en **codage one-hot** (*one-hot encoding*) : seize flottants, tous nuls sauf celui de la case courante.

{{% comment %}}SOURCE: LAPAN ch.4 p.133{{% /comment %}}

```python
class EnveloppeOneHot(gym.ObservationWrapper):
    """Discrete(n) -> Box(0.0, 1.0, (n,)) : un vecteur nul sauf en la case courante."""

    def __init__(self, env):
        super().__init__(env)
        n = env.observation_space.n
        self.observation_space = gym.spaces.Box(0.0, 1.0, (n,), dtype=np.float32)

    def observation(self, observation: int) -> np.ndarray:
        v = np.zeros(self.observation_space.shape, dtype=np.float32)
        v[observation] = 1.0
        return v
```

{{% comment %}}SOURCE: LAPAN ch.4 p.133{{% /comment %}}

Après cette enveloppe, l'espace d'observations et l'espace d'actions sont **compatibles à 100 %** avec notre solution de CartPole. On change l'identifiant de l'environnement, on ajoute l'enveloppe, et on relance la boucle de la section 3.4, inchangée.

{{% comment %}}SOURCE: LAPAN ch.4 p.133{{% /comment %}}

---

## Ce que montrent les courbes

Le résultat est sans appel : **le score ne s'améliore pas avec le temps**. La perte descend, puisqu'un réseau finit toujours par ajuster ce qu'on lui donne, mais le retour moyen reste au ras du sol. Et une courbe parle plus fort que les autres : le seuil des élites, celui qui devait monter régulièrement itération après itération, reste à 0,0 du début à la fin. La **Figure 3-4** montre cette ligne plate, qui est le symptôme et presque le diagnostic.

{{< bookfig src="03-04.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.133-134{{% /comment %}}

---

## La dérivation, et c'est le cœur de la semaine

Comparons les deux environnements par ce qui compte vraiment : la **forme de la distribution des retours**.

Sur CartPole, l'agent reçoit une récompense de 1,0 à **chaque pas** tant que le bâton tient. Plus il tient longtemps, plus il accumule. Comme son comportement comporte une part d'aléa, les épisodes ont des longueurs différentes, et les retours se répartissent selon une distribution approximativement normale, avec une moyenne et une dispersion. La **Figure 3-5** la montre.

{{< bookfig src="03-05.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.134{{% /comment %}}

C'est **cette dispersion** qui rend le seuil utile. Choisir un percentile dans une distribution étalée sépare réellement les épisodes moins bons des meilleurs, et apprendre à répéter les seconds a un sens. Le seuil peut monter parce qu'il y a toujours, dans le lot, des épisodes au-dessus et des épisodes en dessous.

{{% comment %}}SOURCE: LAPAN ch.4 p.134{{% /comment %}}

Sur FrozenLake, la récompense de 1,0 n'arrive qu'à l'objectif, et elle ne dit **rien** de la qualité de l'épisode. L'agent a-t-il filé droit au but, ou a-t-il tourné quatre fois sur le lac avant de poser par hasard le pied sur la case finale ? Le retour vaut 1,0 dans les deux cas. C'est l'exemple même d'une **récompense parcimonieuse** (*sparse reward*). Il n'existe donc que **deux sortes d'épisodes** : ceux qui valent 0 et ceux qui valent 1. Et au début de l'entraînement, quand l'agent agit au hasard, les échecs dominent massivement. La **Figure 3-6** montre cette distribution à deux pics, à comparer avec la précédente.

{{< bookfig src="03-06.png" week="03" >}}

{{% comment %}}SOURCE: LAPAN ch.4 p.135{{% /comment %}}

Maintenant, je fais un pas que l'on vous fera rarement : je rapproche deux faits que l'on rencontre presque toujours séparés, l'un dans l'analyse, l'autre dans le code. Suivez la chaîne, elle a quatre maillons et aucun n'est difficile.

> [!IMPORTANT]
 **Je dois insister : cette dérivation est le contenu évalué du jalon 1.**
 **Premier maillon.** Tant que moins de 30 % des épisodes réussissent, le 70ᵉ percentile d'un ensemble de 0 et de 1 vaut exactement **0,0** : le seuil n'est pas « proche de zéro », il **est** zéro.
 **Deuxième maillon.** Notre filtre écarte les épisodes **strictement inférieurs** au seuil, donc il conserve les égalités. Or tous les échecs valent exactement 0,0, soit exactement le seuil.
 **Troisième maillon.** L'ensemble des élites est donc le **lot entier**, échecs compris : l'agent s'entraîne à reproduire ses propres échecs, c'est-à-dire des exemples qui ne contiennent aucune information sur ce qu'il fallait faire.
 **Quatrième maillon.** La ligne plate à 0,0 de la Figure 3-4 n'est pas une bizarrerie d'affichage : c'est l'enregistrement, itération après itération, du fait que le seuil ne peut pas monter. La sélection par percentile est devenue totalement inopérante, et c'est là toute la raison de l'échec.

{{% comment %}}SOURCE: LAPAN ch.4 p.127, p.134-135{{% /comment %}}

Prenez une minute pour apprécier ce que cela signifie. Le code est juste. Le réseau est bon. L'optimiseur fonctionne. La perte descend. Et pourtant, aucun apprentissage n'a lieu, parce que le **signal** que la méthode utilise pour trier ses exemples a disparu. En apprentissage par renforcement, l'erreur la plus coûteuse n'est presque jamais dans le code : elle est dans l'inadéquation entre la méthode et la structure de la récompense.

---

## Trois limites, qui sont celles de la famille entière

L'échec se généralise en trois limites, et vous reconnaîtrez dans les deux premières ce que la section 3.2 avait déjà annoncé.

1. **Les épisodes doivent être finis**, et de préférence courts. Une méthode qui ne juge qu'après coup ne peut rien faire d'un épisode qui ne finit pas.
2. **Le retour total doit avoir assez de variabilité** pour séparer les bons épisodes des mauvais. C'est exactement ce qui manque sur FrozenLake.
3. **Les récompenses intermédiaires valent mieux qu'une unique récompense terminale.** Un signal qui n'arrive qu'à la fin ne dit rien de ce qui s'est passé au milieu.

{{% comment %}}SOURCE: LAPAN ch.4 p.135-136{{% /comment %}}

Ces trois limites ne condamnent pas CEM : elles délimitent son domaine, et elles définissent en creux le programme des douze semaines qui suivent. Chacune des méthodes que nous rencontrerons attaque l'une d'elles, en commençant dès la semaine prochaine par la troisième, qui est la plus profonde.

{{% comment %}}SOURCE: LAPAN ch.4 p.136{{% /comment %}}

---

## Cinq correctifs, et à quelle limite chacun s'attaque

Peut-on sauver la méthode sur FrozenLake sans changer de famille ? En partie, oui, et l'exercice est très instructif parce que chaque correctif vise une limite identifiée.

| # | Correctif | Pourquoi il aide | Limite visée |
| --- | --- | --- | --- |
| 1 | Des lots beaucoup plus grands, au moins 100 épisodes au lieu de 16 | simplement pour qu'il y ait **quelques** épisodes réussis dans le lot | 2 |
| 2 | Un retour **actualisé**, avec \(\gamma = 0{,}9\) ou \(0{,}95\) | le score dépend alors de la longueur de l'épisode, donc les réussites courtes passent devant les longues : la distribution retrouve de la variabilité | 1 et 2 |
| 3 | Conserver les épisodes élites sur plusieurs itérations | un épisode réussi est une bête rare : le jeter après une seule mise à jour est un gâchis | 2 |
| 4 | Diminuer le pas d'apprentissage | laisser au réseau le temps de moyenner davantage d'exemples, et réduire l'effet de chaque nouveau lot | stabilité |
| 5 | Entraîner beaucoup plus longtemps | la rareté des réussites se paie en itérations, des milliers plutôt que des dizaines | 3 |

{{% comment %}}SOURCE: LAPAN ch.4 p.136{{% /comment %}}

Le correctif 2 demande une formule. Le score servant au classement devient le retour multiplié par l'actualisation de la longueur de l'épisode :

$$
\tilde{G} = \gamma^{T} \, G
\qquad \text{avec } T \text{ la longueur de l'épisode}
$$

{{% comment %}}SOURCE: LAPAN ch.4 p.136{{% /comment %}}

> [!NOTE]
 **Notez bien ce que cette quantité est, et ce qu'elle n'est pas.** \(\tilde{G}\) est un **score de classement**, pas le retour actualisé \(G_t\) de la page « Notation ». Le retour actualisé pondère chaque récompense selon l'instant où elle arrive ; ici, la récompense est unique et terminale, et on se contente de pénaliser la longueur. Deux épisodes réussis, l'un en 6 pas et l'autre en 30, obtiennent \(0{,}9^{6} \approx 0{,}53\) et \(0{,}9^{30} \approx 0{,}04\). La distribution des scores, qui n'avait que deux valeurs, en a maintenant autant que de longueurs possibles : la variabilité est revenue, et le percentile redevient capable de trancher.

Voici les deux changements de code. Ils sont courts, et l'un d'eux tient en un caractère.

```python
GAMMA = 0.9
BATCH_SIZE = 100            # correctif 1
LR = 0.001                  # correctif 4 : le pas d'apprentissage divisé par dix
MEMOIRE_MAX = 500           # correctif 3 : on borne tout de même la mémoire


def filtrer_elites_actualise(lot: list[Episode], percentile: float):
    scores = [ep.retour * (GAMMA ** len(ep.etapes)) for ep in lot]
    seuil = float(np.percentile(scores, percentile))

    elites = [ep for ep, s in zip(lot, scores) if s > seuil]   # STRICTEMENT supérieur
    obs_elites = [e.observation for ep in elites for e in ep.etapes]
    act_elites = [e.action for ep in elites for e in ep.etapes]
    return elites, obs_elites, act_elites, seuil


memoire: list[Episode] = []
for iteration, lot in enumerate(engendrer_lots(env, net, BATCH_SIZE)):
    memoire, obs_elites, act_elites, seuil = filtrer_elites_actualise(
        memoire + lot, PERCENTILE)                             # correctif 3
    if not memoire:
        continue                                               # aucun élite : on passe
    memoire = memoire[-MEMOIRE_MAX:]

    obs_v = torch.tensor(np.vstack(obs_elites), dtype=torch.float32)
    act_v = torch.tensor(act_elites, dtype=torch.long)
    optimizer.zero_grad()
    loss_v = objective(net(obs_v), act_v)
    loss_v.backward()
    optimizer.step()
```

{{% comment %}}SOURCE: LAPAN ch.4 p.136-137{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\gamma\) | facteur d'actualisation, correctif 2 seulement | `GAMMA = 0.9` |
| \(T\) | longueur de l'épisode | `len(ep.etapes)` |
| \(\tilde{G}\) | score de classement de l'épisode | `scores` |
| \(\psi_i\) | seuil des élites, sur les scores actualisés | `seuil` |
| \(\mathcal{E}\) | élites, cumulées sur plusieurs itérations | `memoire`, bornée à 500 |
| \(\alpha\) | pas d'apprentissage | `LR = 0.001` |

> [!WARNING]
 **Attention au caractère qui change tout.** Le filtre de la section 3.4 écartait les épisodes **strictement inférieurs** au seuil, donc gardait les égalités ; celui-ci garde les épisodes **strictement supérieurs**, donc écarte les égalités. Avec un seuil coincé à 0,0, ce seul caractère fait la différence entre « tous les échecs sont élites » et « aucun échec n'est élite ». C'est le genre de détail qu'on ne voit jamais en lisant un algorithme, et qui décide pourtant si l'entraînement fonctionne ou non. Quand vous reprendrez du code existant, lisez les comparaisons.

{{% comment %}}SOURCE: LAPAN ch.4 p.127, p.136{{% /comment %}}

Le résultat, maintenant, et il demande d'être lu avec soin. Sur le lac glissant, l'entraînement corrigé demande environ **50 minutes pour 10 000 itérations**, atteint 50 % d'épisodes réussis vers la 5 000ᵉ itération, puis **cesse de progresser autour de 55 %**. Une seule exécution, deux repères sur la même courbe : un point de passage à mi-parcours, puis un plateau. Et c'est le plateau qui est le résultat intéressant, parce qu'il dit que le calcul supplémentaire n'achète plus rien. Doubler le temps de calcul ne double pas la performance ; au-delà d'un certain point, il ne l'améliore même plus.

{{% comment %}}SOURCE: LAPAN ch.4 p.136-137{{% /comment %}}

Ce plateau a des remèdes, dont la régularisation par une perte d'entropie, qui empêche la politique de devenir trop confiante trop tôt. Je le nomme et je m'arrête là : c'est le sujet des semaines 8 et 11, et nous n'avons pas encore les outils pour en parler honnêtement.

{{% comment %}}SOURCE: LAPAN ch.4 p.138{{% /comment %}}

---

## La variante non glissante, et ce qu'elle démontre

Une dernière expérience, qui tient en un argument de la fonction de création de l'environnement : `gym.make("FrozenLake-v1", is_slippery=False)`. L'agent va alors exactement où il demande à aller. L'effet est spectaculaire : le problème est résolu en **120 à 140 lots**, soit environ cent fois plus vite que dans la version bruitée ; une exécution de référence affiche « Résolu ! » à l'itération 143, avec un retour moyen de 0,82.

{{% comment %}}SOURCE: LAPAN ch.4 p.138-139{{% /comment %}}

Tirez-en la bonne conclusion, parce qu'elle est contre-intuitive. Ce n'est pas la taille de l'espace d'états qui faisait la difficulté : la grille a seize cases dans les deux cas. Ce n'est pas non plus la parcimonie de la récompense à elle seule, car elle est identique dans les deux cas. C'est le **bruit** : quand l'action demandée n'est exécutée qu'une fois sur trois, le lien entre ce que l'agent a fait et ce qu'il a obtenu devient très ténu, et une méthode qui juge des épisodes entiers a besoin d'énormément d'échantillons pour le retrouver. Vous venez d'isoler une variable et de mesurer son effet : c'est exactement le geste que le jalon 1 vous demande de reproduire.
