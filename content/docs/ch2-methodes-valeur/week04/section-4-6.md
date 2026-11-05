---
title: "4.6 Apprendre sans modèle : TD(0)"
weight: 7
---

## L'idée la plus centrale et la plus nouvelle de tout le domaine

C'est une idée qui fait consensus, et je la formule aussi nettement que je peux : s'il fallait désigner une seule idée comme centrale et nouvelle dans l'apprentissage par renforcement, ce serait sans aucun doute l'**apprentissage par différences temporelles** (*temporal-difference learning*). Pas la descente de gradient, pas les réseaux profonds : celle-ci. Prenons donc le temps de comprendre pourquoi.

{{% comment %}}SOURCE: SB ch.6 p.141{{% /comment %}}

Nous avons, à ce stade, deux familles, et chacune a exactement une qualité qui manque à l'autre.

Les méthodes de Monte-Carlo de la semaine 3 n'ont besoin **d'aucun modèle** : elles jouent, elles observent, elles moyennent. En revanche elles doivent attendre la **fin de l'épisode**, puisque leur signal est le retour complet.

La programmation dynamique de la section 4.4 n'attend rien : elle met à jour la valeur d'un état à partir des valeurs de ses voisins, immédiatement. En revanche elle exige un **modèle parfait**.

L'apprentissage par différences temporelles prend la qualité de chacune : il **échantillonne** comme Monte-Carlo, donc il n'a pas besoin de modèle, et il **estime à partir d'une autre estimation** comme la programmation dynamique, donc il n'attend pas la fin de l'épisode. Ce second mécanisme porte un nom que j'ai promis en semaine 3 et que je vous donne maintenant : l'**amorçage** (*bootstrapping*). Amorcer, c'est utiliser une estimation existante comme si c'était une vérité, pour en produire une meilleure. C'est circulaire, c'est inconfortable à la première lecture, et cela converge.

{{% comment %}}SOURCE: SB ch.6 p.141{{% /comment %}}

---

## La cible change, et c'est tout ce qui change

Partons de la forme la plus simple de Monte-Carlo incrémental, celle qui ajuste une table d'un petit pas à chaque retour observé. On l'appelle Monte-Carlo à \(\alpha\) constant.

$$
V(S_t) \leftarrow V(S_t) + \alpha\big[\, G_t - V(S_t) \,\big]
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.1 p.141{{% /comment %}}

Lisez cette règle comme une phrase : « déplace ta valeur d'une fraction \(\alpha\) de l'écart entre ce que tu as observé et ce que tu croyais ». La quantité entre crochets est une **erreur**, et \(\alpha\) est le **pas d'apprentissage** (*step size*, parfois appelé *learning rate*), avec \(\alpha \in (0,1]\).

Le problème est entièrement dans le symbole \(G_t\). C'est la **cible** de la mise à jour, et le retour complet n'est connu qu'à la fin de l'épisode. Toute la méthode est bloquée par ce seul symbole.

L'idée de TD est de remplacer la cible. Plutôt que d'attendre le retour complet, on utilise ce que l'on peut observer dès l'instant \(t+1\) : la récompense réellement reçue, plus l'estimation courante de la valeur de l'état où l'on vient d'arriver.

$$
V(S_t) \leftarrow V(S_t) + \alpha\big[\, R_{t+1} + \gamma\, V(S_{t+1}) - V(S_t) \,\big]
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.2 p.142{{% /comment %}}

Voilà. C'est **TD(0)**, aussi appelé TD à un pas (*one-step TD*), et c'est la seule différence avec la ligne précédente : \(G_t\) est devenu \(R_{t+1} + \gamma V(S_{t+1})\). Comparez maintenant cette règle à l'équation de Bellman de la section 4.2 : \(R_{t+1} + \gamma V(S_{t+1})\) est, à l'espérance près, exactement le membre de droite de Bellman. TD(0) est donc l'équation de Bellman avec une flèche, comme tous les algorithmes de cette semaine, mais une flèche appliquée sur **un seul échantillon** plutôt que sur l'espérance complète.

{{% comment %}}SOURCE: SB ch.6 p.142{{% /comment %}}

Il y a maintenant un point qui mérite un paragraphe à lui seul, parce qu'il place proprement les trois familles les unes par rapport aux autres. Les deux cibles, \(G_t\) et \(R_{t+1} + \gamma V(S_{t+1})\), sont toutes les deux des **estimations**. Mais elles le sont pour des raisons **différentes**, et il y en a trois en tout.

| Famille | Pourquoi sa cible est une estimation |
| --- | --- |
| **Monte-Carlo** | l'espérance du retour est inconnue, et un retour **échantillonné** la remplace |
| **Programmation dynamique** | \(v_\pi(S_{t+1})\) est inconnue, et l'estimation courante \(V(S_{t+1})\) la remplace |
| **TD** | **les deux raisons à la fois** : la transition est échantillonnée **et** la valeur suivante est une estimation |

{{% comment %}}SOURCE: SB ch.6 p.142{{% /comment %}}

C'est ce tableau qu'il faut retenir de la section, plus que les formules. TD cumule les deux approximations, ce qui devrait l'affaiblir et ce qui, en pratique, le rend applicable partout.

Voici l'algorithme complet.

```
TD(0) tabulaire, pour estimer v_π

Entrée : la politique π à évaluer
Paramètre de l'algorithme : pas d'apprentissage α ∈ (0, 1]
Initialiser V(s), pour tout s ∈ S⁺, arbitrairement sauf V(terminal) = 0

Pour chaque épisode :
    Initialiser S
    Pour chaque pas de l'épisode :
        A ← action donnée par π pour S
        Exécuter A, observer R et S'
        V(S) ← V(S) + α [ R + γ V(S') − V(S) ]
        S ← S'
    jusqu'à ce que S soit terminal
```

{{% comment %}}SOURCE: SB ch.6 p.142{{% /comment %}}

Et le code. Il est beaucoup plus court que celui de la section 4.5, et cette brièveté est elle-même l'argument : il n'y a plus de table des transitions, plus de table des récompenses, plus de comptage. Trois lignes ont disparu, et avec elles tout le modèle de l'environnement.

```python
def td_zero(env, politique, alpha=0.1, gamma=0.9, n_episodes=500):
    """TD(0) tabulaire : AUCUN modèle, aucune probabilité de transition."""
    V = np.zeros(env.observation_space.n)

    for _ in range(n_episodes):
        etat, _ = env.reset()
        while True:
            action = politique(etat)
            cible, recompense, terminated, truncated, _ = env.step(action)

            # V(terminal) = 0 : une condition EXPLICITE, jamais la case de la table
            futur = 0.0 if terminated else V[cible]
            delta = recompense + gamma * futur - V[etat]    # l'erreur TD
            V[etat] += alpha * delta                        # on ÉCRIT dans une case

            etat = cible
            if terminated or truncated:
                break
    return V
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(V(S_t)\) | estimation tabulaire de la valeur de l'état courant | `V[etat]` |
| \(R_{t+1}\) | récompense de la transition, **un seul échantillon** | `recompense` |
| \(V(S_{t+1})\) | estimation de la valeur de l'état suivant, ou 0 s'il est terminal | `futur` |
| \(R_{t+1} + \gamma V(S_{t+1})\) | la **cible** TD | `recompense + gamma * futur` |
| \(\delta_t\) | l'erreur TD, le crochet | `delta` |
| \(\alpha\) | pas d'apprentissage | `alpha` |
| \(\leftarrow\) | affectation **sur place**, et non un pas de gradient | `V[etat] += alpha * delta` |

> [!WARNING]
 **Attention à la ligne du `futur`, c'est l'erreur la plus fréquente de tout l'apprentissage tabulaire.** Quand l'épisode se termine, la valeur de l'état suivant doit être **zéro**, et non `V[cible]`. Notez aussi la distinction entre `terminated` et `truncated` : un épisode **tronqué** par une limite de temps n'a pas atteint un état terminal, et sa valeur future n'est donc **pas** nulle. Confondre les deux introduit un biais systématique qui ne lève aucune exception et que vous ne verrez que dans les courbes, trop tard. C'est la semaine 1 qui payait d'avance pour cette ligne.

---

## Mise à jour par échantillon contre mise à jour en espérance

Nous pouvons maintenant nommer proprement l'opposition qui traverse toute la semaine, et c'est le contraste le plus net que je peux vous offrir avant la semaine 5.

TD et Monte-Carlo regardent en avant vers **un seul état successeur échantillonné**, celui que l'environnement a effectivement produit, et utilisent sa valeur pour corriger. C'est une **mise à jour par échantillon**. La programmation dynamique, elle, utilise la **distribution complète** des successeurs, tous pesés par leurs probabilités. C'est une mise à jour en espérance.

{{% comment %}}SOURCE: SB ch.6 p.143{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que ce choix est celui que la semaine 5 pousse à l'extrême.** La mise à jour en espérance est **exacte** et demande un modèle. La mise à jour par échantillon est **bruitée** et ne demande rien. Tout le reste du cours travaille avec des mises à jour par échantillon, et presque toutes les difficultés que nous rencontrerons, de la variance du gradient de politique en semaine 8 jusqu'aux divergences de la semaine 6, sont le prix de ce choix. Vous venez de voir la version exacte fonctionner en moins d'une seconde sur FrozenLake, en section 4.5. Gardez-la en mémoire comme point de comparaison : elle est le plafond que les méthodes suivantes essaient d'atteindre à l'aveugle.

---

## L'erreur TD, et son décalage d'un pas

La quantité entre crochets revient tellement souvent qu'elle porte un nom et un symbole : c'est l'**erreur TD** (*TD error*), notée \(\delta_t\).

$$
\delta_t \defeq R_{t+1} + \gamma\, V(S_{t+1}) - V(S_t)
$$

{{% comment %}}SOURCE: SB ch.6 éq. 6.5 p.143{{% /comment %}}

Lisez-la comme un signal de surprise : positive si l'état a mieux tourné que vous ne le pensiez, négative sinon, nulle si vos estimations étaient cohérentes entre elles. Nous la retrouverons sous ce nom et sous ce symbole jusqu'à la fin du cours, et en semaine 8 elle servira même directement de mesure d'avantage.

Un détail de chronologie mérite d'être relevé, parce qu'il surprend toujours. \(\delta_t\) est l'erreur commise sur \(V(S_t)\), donc une erreur attachée à l'instant \(t\). Mais elle n'est **pas disponible** à l'instant \(t\) : elle fait intervenir \(R_{t+1}\) et \(S_{t+1}\), qui n'existent qu'un pas plus tard. L'erreur de l'instant \(t\) ne se connaît qu'à l'instant \(t+1\). C'est pourquoi, dans le code, la mise à jour s'écrit **après** l'appel à `step()`.

{{% comment %}}SOURCE: SB ch.6 p.143{{% /comment %}}

Je signale, sans la dériver, une identité qui existe et à laquelle nous reviendrons : l'erreur de Monte-Carlo sur un épisode peut s'écrire comme une **somme actualisée des erreurs TD** de cet épisode. Elle n'est exacte que si \(V\) reste figée pendant tout l'épisode, ce qui n'est pas le cas dans nos implémentations, mais elle éclaire la parenté des deux familles. Elle resservira plus loin dans le cours, et je préfère ne pas en dire davantage maintenant.

{{% comment %}}SOURCE: SB ch.6 p.143{{% /comment %}}

---

## Rentrer chez soi, et corriger en route

Je garde pour la fin l'intuition la plus convaincante de la section, et elle ne contient aucune équation.

Vous quittez le bureau à 18 heures et vous estimez qu'il vous faut 30 minutes pour rentrer. En arrivant à la voiture, il pleut, et vous révisez : plutôt 40 minutes au total. Vous sortez de l'autoroute mieux que prévu et vous révisez encore : 35 minutes. Puis vous vous retrouvez derrière un camion sur une départementale : 40. Vous entrez dans votre rue : 43. Vous arrivez : 43, et c'est le chiffre définitif.

| Situation | Temps écoulé | Temps restant prédit | **Temps total prédit** |
| --- | --- | --- | --- |
| quitter le bureau | 0 | 30 | **30** |
| rejoindre la voiture, il pleut | 5 | 35 | **40** |
| sortir de l'autoroute | 20 | 15 | **35** |
| derrière un camion | 30 | 10 | **40** |
| entrer dans la rue | 40 | 3 | **43** |
| arriver | 43 | 0 | **43** |

{{% comment %}}SOURCE: SB ch.6 p.144-145{{% /comment %}}

Posons maintenant la question qui sépare les deux familles : à quel moment corrigez-vous votre première estimation, celle de 30 minutes ?

Une méthode de Monte-Carlo vous répond : **à l'arrivée**. On attend le chiffre final, 43, et on corrige toutes les prédictions de l'épisode en une fois, vers cette valeur observée.

TD vous répond : **immédiatement, et à chaque pas**. Chaque estimation est déplacée vers celle qui la **suit**. Les 30 minutes sont corrigées vers 40 dès qu'il se met à pleuvoir, sans attendre de savoir si l'on arrivera à 43 ou à 55.

Et voici la variante qui tranche la question. Supposez qu'après 25 minutes de route, vous vous retrouviez immobilisé dans un embouteillage manifestement durable. Vous savez **déjà**, avec certitude, que votre estimation initiale de 30 minutes était trop optimiste. Faut-il attendre d'être rentré pour l'écrire ? Monte-Carlo vous y oblige. TD, non. L'information était disponible, et attendre la fin de l'épisode pour l'utiliser n'est pas de la prudence, c'est du gaspillage.

{{% comment %}}SOURCE: SB ch.6 p.144-145{{% /comment %}}

Trois avantages pratiques, pour conclure, et je m'arrête à trois.

1. **Aucun modèle n'est requis** : ni les probabilités de transition, ni la fonction de récompense.
2. La méthode est **entièrement incrémentale et en ligne** : une transition arrive, une case bouge.
3. Elle est **insensible aux épisodes longs ou inexistants**. Un épisode de dix mille pas ne pose pas plus de problème qu'un épisode de trois, et une tâche qui ne se termine jamais ne pose pas de problème du tout.

{{% comment %}}SOURCE: SB ch.6 p.146{{% /comment %}}
