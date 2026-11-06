---
title: "9.5 Le critique surestime, et on le mesure"
weight: 6
---

## Le biais de maximisation, revu du côté continu

La semaine 6 vous a présenté la surestimation des valeurs d'action, et vous l'avez réparée du côté discret avec le double DQN. Je vais reprendre l'argument depuis le début, parce que cette semaine en pousse les conséquences beaucoup plus loin, et parce qu'il est au cœur de tout ce qui suit.

L'argument est d'une simplicité désarmante. Supposez que votre estimation de valeur d'action soit entachée d'une erreur \(\eta\), et supposez cette erreur **centrée** : en moyenne, vous ne vous trompez ni vers le haut ni vers le bas. Prenez maintenant le maximum sur les actions de l'estimation bruitée, et regardez son espérance :

$$
\E_\eta\!\left[\max_{a'}\left( q(s',a') + \eta \right)\right] \;\ge\; \max_{a'} q(s',a')
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §4{{% /comment %}}

L'inégalité est toujours vraie, dans un seul sens. La raison intuitive est que le maximum **sélectionne** : parmi plusieurs actions, il retient celle dont l'estimation est la plus grande, et une estimation est d'autant plus grande que son erreur était positive. Le maximum fait donc remonter les erreurs favorables et écarte les défavorables. Une erreur de moyenne nulle produit, après maximisation, une **surestimation systématique**.

Et cette surestimation ne reste pas où elle est née : elle entre dans la cible de Bellman, qui sert à mettre à jour l'estimation, dont le maximum sera repris au pas suivant. Elle se **propage**, et elle s'accumule. Notez enfin que l'on ne peut pas se débarrasser de \(\eta\) : une erreur d'approximation est inévitable dès qu'un réseau de taille finie représente une fonction sur un espace d'états trop grand pour être énuméré, ce qui est la condition de toutes nos méthodes depuis la semaine 5.

{{% comment %}}SOURCE: arXiv:1802.09477 §4{{% /comment %}}

> [!NOTE]
 **J'ai écrit \(\eta\) pour l'erreur d'approximation, et c'est un choix du cours.** L'écriture habituelle de cette inégalité emploie \(\epsilon\), lettre que la section 9.4 vient de réserver à l'amplitude du bruit d'exploration et que la section 9.6 réemploierait pour le bruit ajouté à l'action cible. Trois objets, une lettre : le cours en renomme un. L'erreur d'approximation du critique s'écrit donc \(\eta\) dans cette section, et nulle part ailleurs.

---

## En acteur-critique, le maximum se cache dans un pas de gradient

Vous pourriez objecter, et l'objection est bonne : il n'y a **aucun** \(\max\) dans la boucle de la section 9.3. L'acteur ne maximise pas, il avance d'un petit pas de gradient. L'argument précédent devrait donc tomber.

Il ne tombe pas, et c'est tout l'intérêt. Le maximum n'a pas disparu, il a changé de forme : l'acteur est entraîné à monter le long de \(q_{\mathbf{w}}\), donc il se déplace **vers** les actions que le critique note le plus haut, donc il trouve, pas après pas, les endroits où le critique se trompe par excès. Il n'exécute pas une maximisation en un coup, il en réalise une au ralenti, et le biais prend le même chemin.

On peut l'établir proprement, et c'est fait : pour un pas d'apprentissage suffisamment petit, la politique obtenue en suivant le gradient du critique **approché** est notée, par ce même critique, au moins aussi haut que sa vraie valeur :

$$
\E\!\left[\, q_{\mathbf{w}}\!\left(s, \mu_{\text{approx}}(s)\right) \,\right] \;\ge\; \E\!\left[\, q_\pi\!\left(s, \mu_{\text{approx}}(s)\right) \,\right]
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §4.1 (tex éq. 7){{% /comment %}}

où \(\mu_{\text{approx}}\) désigne l'acteur mis à jour avec le gradient du critique approché. Le critique est donc, de façon démontrable, trop optimiste sur la politique qu'il a lui-même produite.

Et maintenant la phrase que je veux que vous reteniez de cette section, parce qu'elle décrit un **mécanisme** et non une anomalie. Une estimation de valeur inexacte produit une mise à jour de politique médiocre. Cette politique médiocre est ensuite évaluée par le même critique médiocre, qui la note haut, ce qui **renforce** l'action médiocre à la mise à jour suivante. Une boucle de rétroaction s'installe, et les deux objets se dégradent ensemble : les estimations de valeur divergent par surestimation quand la politique est mauvaise, et la politique devient mauvaise quand l'estimation est inexacte.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.1 ; §5.2{{% /comment %}}

> [!WARNING]
 **Ce que cela signifie pour vos propres courbes, et c'est un diagnostic utilisable dès ce soir.** Une valeur prédite qui monte régulièrement, sans plateau, est souvent interprétée comme un bon signe. Elle ne l'est pas. Si la valeur moyenne prédite par votre critique monte alors que la récompense par épisode stagne ou descend, ce n'est pas un apprentissage en cours : c'est une divergence par surestimation en train de se mettre en place. Journalisez **toujours** les deux quantités sur le même graphique, la valeur prédite et le retour réellement obtenu. L'écart entre les deux courbes est le sujet de cette section, et c'est aussi la mesure que le volet B du laboratoire vous demandera de produire.

---

## Comment on mesure une surestimation

Dire qu'un critique surestime est facile ; le montrer demande un protocole, et le protocole est instructif en lui-même parce qu'il faut trouver un substitut à une quantité inconnue.

Le protocole est celui-ci. On fixe un ensemble de **10 000 états**, et on y calcule la **valeur moyenne estimée** par le critique : c'est la quantité dont on soupçonne qu'elle est trop grande. Il faut ensuite la comparer à la valeur vraie, qui est inconnue, et c'est là qu'intervient le substitut : on prend comme estimation de la valeur vraie le **retour actualisé moyen sur 1 000 épisodes** joués en suivant la politique courante, depuis des états tirés dans le tampon de rejeu. Deux courbes, l'estimation et le retour, et l'écart entre les deux est la surestimation. L'expérience a été menée sur deux tâches de locomotion simulée, sur un million de pas de temps.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.1{{% /comment %}}

Le verdict est net : un biais de surestimation très clair apparaît, et il est produit **par la procédure d'apprentissage elle-même**. La même mesure, refaite avec le premier des trois correctifs de la section 9.6, montre une surestimation fortement réduite.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.1{{% /comment %}}

Deux mesures complémentaires, sous le même protocole, méritent une phrase chacune parce qu'elles expliquent pourquoi la section 9.6 ne se contente pas de transplanter les recettes de la semaine 6. La transplantation directe du double DQN dans un cadre acteur-critique **surestime à peu près autant** que la méthode de base. La transplantation du double Q-learning complet, avec deux acteurs et deux critiques, fait mieux, mais **n'élimine pas** la surestimation.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2{{% /comment %}}

Le code de la mesure tient en quelques lignes, et je vous le donne parce que c'est exactement ce que le volet B du laboratoire demande :

```python
def mesurer_surestimation(critique, acteur, env, etats_fixes, gamma, n_episodes, device):
    """Compare la valeur estimee par le critique au retour reellement obtenu."""
    # 1. Ce que le critique PREDIT, sur un ensemble d'etats fige une fois pour toutes.
    etats_t = torch.as_tensor(etats_fixes, dtype=torch.float32, device=device)
    with torch.no_grad():
        valeur_estimee = critique(etats_t, acteur(etats_t)).mean().item()

    # 2. Ce que la politique OBTIENT reellement, sans aucun bruit d'exploration.
    retours = []
    for _ in range(n_episodes):
        obs, _ = env.reset()
        retour, actualisation, termine, tronque = 0.0, 1.0, False, False
        while not (termine or tronque):
            obs_t = torch.as_tensor(np.asarray([obs]), dtype=torch.float32, device=device)
            with torch.no_grad():
                action = acteur(obs_t).cpu().numpy()[0]
            obs, r, termine, tronque, _ = env.step(action)
            retour += actualisation * r
            actualisation *= gamma
        retours.append(retour)

    return valeur_estimee, float(np.mean(retours))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\frac{1}{\lvert S\rvert}\sum_{s \in S} q_{\mathbf{w}}(s,\mu_\theta(s))\) | valeur moyenne estimée sur l'ensemble figé | `valeur_estimee` |
| \(S\) | ensemble d'états tirés du tampon, **fixé une fois** | `etats_fixes` |
| \(G_t = \sum_i \gamma^i r_i\) | retour actualisé réellement collecté | `retour` |
| \(\E[G_t]\) | substitut de la valeur vraie, moyenne sur les épisodes | `np.mean(retours)` |
| écart | la surestimation, ce que l'on trace | la différence des deux sorties |

> [!TIP]
 **Pourquoi l'ensemble d'états doit être figé.** Si vous retirez de nouveaux états du tampon à chaque mesure, vous mesurez deux choses à la fois : l'évolution du critique et l'évolution de la distribution des états visités. Les deux bougent, et vous ne pourrez attribuer l'écart à aucune des deux. Tirez vos états une fois, au début, gardez-les sur le disque, et mesurez toujours sur les mêmes. C'est la même discipline que la version de référence de la semaine 7.

---

## Le nombre que je ne vous donnerai pas

Je dois maintenant être franc sur une limite, parce que vous allez chercher ce nombre et qu'il est préférable que vous sachiez pourquoi il n'est pas là.

Vous venez de voir le mécanisme, le protocole et le verdict. Ce que je ne vous donne pas, c'est l'**ampleur** : de combien le critique surestime, en pourcentage ou en unités de récompense. La raison est simple et je la préfère à une approximation rassurante : cette ampleur existe sous forme de **courbes**, que ce cours ne peut pas vous montrer, et lire un ordre de grandeur sur l'axe d'une figure pour le réciter comme une mesure serait malhonnête. Un nombre inventé, même plausible, vaut moins que l'absence de nombre.

{{% comment %}}SOURCE: index/notes/week-09.md gap 2{{% /comment %}}

Il y a deux routes honnêtes, et je prends la seconde. La première consiste à attendre une mesure que je puisse vous montrer. La seconde consiste à **la produire vous-même**, sur une tâche assez petite pour tenir dans un carnet, et c'est le volet B du laboratoire : vous avez le protocole, vous avez les quinze lignes de code, et vous avez une tâche à une dimension d'action sur laquelle mille épisodes coûtent quelques minutes. Vous obtiendrez un nombre qui sera **le vôtre**, mesuré sur votre tâche, avec un intervalle sur plusieurs graines. C'est une meilleure situation que de réciter le nombre de quelqu'un d'autre, et c'est en réalité le genre d'exercice qui distingue un praticien d'un lecteur.

Ce que la section 9.6 vous donnera en revanche, ce sont les **conséquences** mesurées : les scores obtenus avec et sans chacun des trois correctifs, sur quatre tâches, avec dix graines. Ce sont des nombres exacts, et ils disent indirectement ce que la surestimation coûte.

---

## Pourquoi la variance n'est pas un problème secondaire

Il y a un second mécanisme, moins célèbre que la surestimation et étroitement lié à elle, et il faut le connaître pour comprendre le deuxième des trois correctifs.

Chaque mise à jour du critique réduit l'erreur de différence temporelle, mais ne l'annule pas : il reste un résidu. Appelons \(\delta(s,a)\) ce résidu, et écrivons que l'estimation satisfait l'équation de Bellman **à ce résidu près** :

$$
q_{\mathbf{w}}(s,a) = r + \gamma\,\E\left[q_{\mathbf{w}}(s',a')\right] - \delta(s,a)
$$

Déroulez cette relation sur toute la trajectoire, comme la semaine 6 l'a fait pour le dépliage de Bellman, et vous obtenez une lecture frappante :

$$
q_{\mathbf{w}}(s_t,a_t) = \E\left[\sum_{i=t}^{T} \gamma^{\,i-t}\left( r_i - \delta_i \right)\right]
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §5.1 (tex éq. 11-12){{% /comment %}}

Autrement dit, votre critique n'approche pas le retour : il approche le retour **moins la somme actualisée de toutes les erreurs de différence temporelle futures**. Deux conséquences, et elles sont toutes les deux pratiques. Primo, avec un facteur d'actualisation élevé, cette somme contient beaucoup de termes, et sa variance peut croître rapidement à chaque mise à jour si l'erreur de chaque mise à jour n'est pas maîtrisée. Secundo, chaque pas de gradient ne réduit l'erreur que sur un **petit lot** : il n'offre aucune garantie sur la taille des erreurs dans les estimations hors de ce lot, et ces erreurs-là sont précisément celles que l'acteur ira chercher.

{{% comment %}}SOURCE: arXiv:1802.09477 §5.1{{% /comment %}}

Une estimation à forte variance fait donc un gradient d'acteur bruyant, et un gradient d'acteur bruyant conduit la politique vers les creux et les bosses parasites du critique. Surestimation et variance ne sont pas deux problèmes séparés : ce sont les deux faces du même, et les trois correctifs de la section suivante s'attaquent, pour deux d'entre eux, à la variance.

---

## Le réseau cible, et ce que \(\tau\) décide vraiment

Un dernier résultat avant les correctifs, parce qu'il explique l'un d'eux, et parce qu'il change le statut du réseau cible dans votre esprit.

L'expérience est la suivante. Sur une tâche de locomotion, on suit la valeur estimée d'un état choisi au hasard, sous trois régimes de réseau cible : \(\tau = 1\), c'est-à-dire **sans** réseau cible du tout puisque la cible devient une copie instantanée, puis \(\tau = 0{,}1\) et \(\tau = 0{,}01\). Et on refait l'expérience deux fois : une fois avec une politique **figée**, une fois avec une politique **apprise** en même temps.

Avec une politique figée, les trois régimes convergent de façon comparable : le réseau cible n'apporte presque rien. Avec une politique apprise, les réseaux cibles à mise à jour rapide produisent un comportement **fortement divergent**.

{{% comment %}}SOURCE: arXiv:1802.09477 §5.2{{% /comment %}}

Lisez bien ce que cela dit, parce que ce n'est pas ce qu'on raconte habituellement sur les réseaux cibles. Un réseau cible n'est pas, en soi, un stabilisateur de régression : contre une politique fixe, il est presque superflu. Son rôle est de **découpler deux apprentissages qui se nourrissent l'un de l'autre**. Il empêche l'erreur du critique d'être immédiatement amplifiée par une politique qui, elle aussi, bouge. Et une fois cela compris, un correctif se dessine tout seul, celui qui demande : et si, au lieu de seulement ralentir la cible, on ralentissait aussi la **politique** ? C'est le deuxième des trois correctifs de la section suivante.

---
