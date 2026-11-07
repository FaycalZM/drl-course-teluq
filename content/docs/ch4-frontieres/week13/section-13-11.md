---
title: "13.11 Le gradient qui traverse la dynamique"
weight: 12
---

## Deux objectifs, et un arrêt de gradient

Nous avons un estimateur de retour imaginé. Les deux objectifs s'écrivent en deux lignes, et ils sont symétriques.

**L'intuition.** L'acteur veut que les états qu'il traverse valent cher : il maximise la somme des estimations de retour le long de la trajectoire imaginée. Le critique veut dire la vérité sur ces états : il minimise l'écart entre ce qu'il prédit et cette même estimation.

**L'équation.** L'acteur, qui monte :

$$
\max_\phi\; \E_{p_\theta,\, \pi_\phi}\!\left[\sum_{k=t}^{t+H} V_\lambda(Z_k)\right]
$$

{{% comment %}}SOURCE: DREAMER éq. 7 p.5{{% /comment %}}

Le critique, qui descend :

$$
\min_\psi\; \E_{p_\theta,\, \pi_\phi}\!\left[\sum_{k=t}^{t+H} \tfrac{1}{2}\,\big\lVert \hat v_\psi(Z_k) - V_\lambda(Z_k) \big\rVert^2\right]
$$

{{% comment %}}SOURCE: DREAMER éq. 8 p.5{{% /comment %}}

Et une précision qui n'est pas dans les symboles mais qui est indispensable : **le gradient est arrêté autour de la cible** du critique. Le \(V_\lambda(Z_k)\) du second objectif contient des appels à \(\hat v_\psi\), puisque c'est un retour amorcé ; si on laissait le gradient y passer, le critique optimiserait sa cible au lieu de la poursuivre. C'est la cible gelée de la semaine 5, sous une autre forme : là, un réseau cible séparé ; ici, un `detach` sur la cible. Le même principe, deux implémentations.

---

## La chaîne de dépendances, et l'endroit où ce gradient va

Voici la section la plus intéressante de la première moitié de la semaine. Nous allons suivre le gradient de l'acteur, lien par lien.

Que faut-il dériver ? \(\sum_k V_\lambda(Z_k)\) par rapport à \(\phi\). Déroulons la chaîne de dépendances :

- l'estimation \(V_\lambda\) dépend des **récompenses prédites** \(r_k\) et des **valeurs prédites** \(\hat v_\psi(Z_k)\) ;
- ces récompenses et ces valeurs dépendent des **états imaginés** \(Z_k\), puisque ce sont des fonctions de \(Z_k\) ;
- ces états imaginés dépendent des **actions imaginées** \(a_{k-1}\), par la transition apprise \(p_\theta\) ;
- et ces actions dépendent de \(\phi\), par l'acteur.

**Chaque lien de cette chaîne est un réseau de neurones**, donc chaque lien est dérivable. Le gradient \(\nabla_\phi\) se calcule donc **analytiquement**, par rétropropagation à travers tout l'enchaînement, en incluant les tirages grâce à la reparamétrisation de la section 13.9.

{{% comment %}}SOURCE: DREAMER p.5{{% /comment %}}

Mesurons ce que cela veut dire, en comparant aux trois familles que ce cours a déjà écrites.

| Famille | D'où vient le gradient de la politique | À travers quoi il passe |
| --- | --- | --- |
| semaines 8 et 10, A3C et PPO | estimateur de type Reinforce, log-vraisemblance fois avantage, avec une **référence** pour réduire la variance | aucune dynamique : le gradient ne traverse que le réseau de politique |
| semaines 9 et 11, DDPG et SAC | acteur reparamétré qui maximise une valeur d'action apprise | la valeur d'action **immédiate**, et rien de plus : la dynamique n'intervient pas |
| cette section | acteur reparamétré qui maximise un retour **imaginé sur \(H\) pas** | les \(H\) **transitions apprises**, le modèle de récompense et le critique |

La différence avec la ligne du milieu est celle qu'il faut retenir. Un acteur-critique continu des semaines 9 et 11 est déjà reparamétré, et son gradient passe déjà à travers un réseau de valeur. Mais il maximise une valeur d'action **au pas courant** : il ne tire aucun gradient des **transitions**, pour la raison simple qu'il n'a pas de modèle de transition. Ici, le gradient remonte quinze pas de dynamique apprise. Et c'est ce qui explique un détail qui pourrait sinon paraître une régression : le critique de cette méthode prédit une valeur **d'état** et non une valeur d'action, ce qui semble moins informatif. Cela suffit **précisément parce que** le gradient traverse la dynamique : l'information « quelle action est bonne » n'a pas besoin d'être stockée dans le critique, puisqu'elle est reconstruite en dérivant le modèle.

Des travaux intermédiaires existent, qui étendent la cible de valeur d'action à plusieurs pas sans pour autant dériver à travers les transitions. Ils occupent la place entre la deuxième et la troisième ligne du tableau, et ce cours n'y entre pas.

> [!IMPORTANT]
 **Et une phrase d'une ligne, facile à manquer, qui rend tout cela calculable : le modèle du monde est gelé pendant qu'on apprend le comportement.** Les paramètres \(\theta\) ne reçoivent aucun gradient de l'objectif de l'acteur. Imaginez l'inverse un instant : l'acteur, qui maximise un retour prédit par le modèle, pourrait obtenir un retour énorme en **modifiant le modèle** pour qu'il promette davantage. Ce serait l'optimisation la plus facile du monde et la plus vide de sens. Le gel du modèle est donc ce qui empêche l'acteur de tricher, et c'est la même précaution structurelle qu'un réseau cible en semaine 5 : on sépare ce qui bouge de ce contre quoi on mesure.

{{% comment %}}SOURCE: DREAMER p.5{{% /comment %}}

---

## Le code des deux mises à jour

**Le code.** Les deux objectifs, avec le gel du modèle et l'arrêt de gradient à l'endroit exact.

```python
import torch


def pas_de_comportement(modele, acteur, critique, opt_acteur, opt_critique,
                        h0, z0, gamma=0.99, lam=0.95, horizon=15):
    """Un pas d'apprentissage du comportement, dans l'imagination.

    Le modele est GELE : aucun de ses parametres ne recoit de gradient ici.
    """
    for p in modele.parameters():
        p.requires_grad_(False)

    etats, recompenses = imaginer(modele, acteur, h0, z0, horizon)
    valeurs = critique(etats)

    # --- Acteur : il MONTE la somme des retours lambda. Le gradient remonte
    # les H transitions apprises, grace aux rsample de imaginer().
    cibles = retour_lambda(recompenses, valeurs, gamma, lam)
    perte_acteur = -cibles.sum(0).mean()
    opt_acteur.zero_grad()
    perte_acteur.backward(retain_graph=True)
    opt_acteur.step()

    # --- Critique : il DESCEND vers la meme cible, qui est detachee.
    # Sans ce detach, le critique optimiserait sa propre cible.
    with torch.no_grad():
        cibles_gelees = retour_lambda(recompenses.detach(), valeurs.detach(),
                                      gamma, lam)
    pred = critique(etats.detach())
    perte_critique = 0.5 * (pred - cibles_gelees).pow(2).sum(0).mean()
    opt_critique.zero_grad()
    perte_critique.backward()
    opt_critique.step()

    for p in modele.parameters():
        p.requires_grad_(True)
    return perte_acteur.item(), perte_critique.item()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\max_\phi \sum_k V_\lambda(Z_k)\) | objectif de l'acteur, signe inversé pour descendre | `perte_acteur = -cibles.sum(0).mean()` |
| \(\min_\psi \tfrac12\lVert \hat v_\psi - V_\lambda\rVert^2\) | objectif du critique | `perte_critique` |
| gradient arrêté autour de la cible | la cible du critique ne se dérive pas | `cibles_gelees`, `etats.detach()` |
| modèle gelé | \(\theta\) ne reçoit aucun gradient ici | `p.requires_grad_(False)` |
| \(H\) | horizon d'imagination, quinze | `horizon` |
| \(\gamma, \lambda\) | actualisation et pondération du retour | `gamma`, `lam` |

---

## L'ablation qui établit le résultat, et ce n'est pas celle qu'on attendrait

Il faut maintenant dire **quelle mesure démontre quoi**, parce que c'est là qu'une lecture rapide se trompe.

On pourrait croire que l'argument de cette section se démontre par une courbe d'efficacité en échantillons : « avec le critique, l'agent apprend plus vite ». Ce n'est pas la bonne mesure, et ce n'est pas celle qui est faite. **L'ablation qui porte l'argument est un balayage de l'horizon d'imagination.**

Voici le protocole. Trois agents : celui de cette section, avec acteur et critique ; un acteur **sans critique**, c'est-à-dire entraîné sur l'estimateur \(V_{\mathrm{R}}\) de la section 13.10 ; et la planification en ligne de la section 13.5. On trace la performance finale de chacun **en fonction de l'horizon d'imagination**, de dix à quarante, sur quatre tâches : le pendule sur chariot, la course du guépard, la marche du quadrupède et la marche du bipède.

Et le résultat est le suivant. Apprendre une valeur d'état pour estimer les récompenses au-delà de l'horizon rend l'agent **robuste à la longueur de l'horizon**, et lui permet de bien se comporter **même à horizon court**. Les deux autres, non : leur performance dépend fortement de l'horizon qu'on leur donne, parce qu'ils ne voient rien derrière.

{{% comment %}}SOURCE: DREAMER p.4{{% /comment %}}
{{% comment %}}SOURCE: DREAMER p.9{{% /comment %}}

> [!TIP]
 **Pourquoi cette ablation est la bonne, et pas une courbe d'apprentissage.** La thèse à établir n'est pas « le critique accélère l'apprentissage » : c'est « le critique **achète l'horizon** », c'est-à-dire qu'il dispense de regarder loin. Une courbe d'efficacité en échantillons mesurerait la vitesse à horizon fixé, ce qui confond deux effets. Un balayage de l'horizon mesure exactement la quantité en cause : la **dépendance** de la performance à la profondeur du déroulement. Un agent dont la courbe est plate sur l'intervalle de dix à quarante a démontré que la profondeur ne lui importe plus. Retenez la méthode au-delà du résultat : **quand vous voulez montrer qu'un mécanisme rend une quantité inutile, faites varier cette quantité**, ne mesurez pas la vitesse à sa valeur par défaut.

Une mesure complémentaire dit la même chose par l'autre bout. Sans critique, un agent qui n'optimise que les récompenses imaginées à l'intérieur de l'horizon, que ce soit par un acteur ou par une planification en ligne, produit des comportements **à courte vue** qui ne réussissent que sur les tâches **réactives**, comme la marche du bipède, où la bonne action se décide localement. C'est sur les tâches à attribution du mérite longue, comme redresser un pendule à deux segments ou faire sauter un corps, que le défaut devient visible.

{{% comment %}}SOURCE: DREAMER p.7{{% /comment %}}

---

## Deux extensions en une ligne chacune, et un résultat chiffré

Trois compléments, pour fermer la première moitié de la semaine sans l'allonger.

**Actions discrètes.** Toute la construction suppose une action continue, puisqu'elle dérive à travers l'action. Pour une action discrète, la méthode emploie un **gradient traversant** (*straight-through gradient*) : on échantillonne discrètement vers l'avant, et on fait passer vers l'arrière le gradient de la loi continue sous-jacente. C'est une ligne de code et un compromis assumé, et ce cours n'y entre pas davantage.

**Terminaison anticipée.** Dans un environnement où un épisode peut s'arrêter, le modèle du monde prédit aussi, depuis chaque latent, le **facteur d'actualisation** à appliquer ; les termes des deux objectifs sont alors pondérés par le produit cumulé des facteurs prédits. Un épisode imaginé qui a probablement pris fin cesse ainsi de compter, progressivement et sans discontinuité.

{{% comment %}}SOURCE: DREAMER p.5{{% /comment %}}

**Et une question que cette semaine ne traite pas, mais dont je dois nommer l'existence.** On peut se demander si la reconstruction d'images de la section 13.4 est bien le meilleur objectif pour apprendre une représentation : il existe des alternatives, notamment des objectifs **contrastifs**, qui apprennent à distinguer les vraies transitions de fausses plutôt qu'à reconstruire, et des objectifs purement fondés sur la **prédiction de récompense**. La comparaison a été faite, et le verdict tient en une phrase : la reconstruction gagne à peu près partout, l'objectif contrastif résout environ la moitié des tâches, et la prédiction de récompense seule ne suffit pas. Nous en restons là, et nous gardons la reconstruction.

{{% comment %}}SOURCE: DREAMER p.5-7{{% /comment %}}

Le résultat chiffré, enfin, puisqu'il faut bien un chiffre. **Sous le nom de Dreamer**, cette méthode a été mesurée sur vingt tâches de contrôle continu, images de 64 sur 64, dimensions d'action de 1 à 12, récompenses dans \([0,1]\), épisodes de mille pas, répétition d'action fixée à 2, **le même jeu d'hyperparamètres sur toutes les tâches continues**, cinq graines. Score moyen de **823 après cinq millions de pas**, contre 332 pour la planification en ligne de la section 13.5 au même budget, et 786 pour D4PG après **cent millions** de pas. Le coût : environ **trois heures par million de pas** sur un processeur graphique de centre de données et dix cœurs de calcul, contre onze heures pour la planification en ligne et vingt-quatre pour D4PG.

{{% comment %}}SOURCE: DREAMER p.8-9{{% /comment %}}

> [!WARNING]
 **Et la limite honnête, qui est dans la page parce qu'elle est dans les résultats.** Sur des jeux vidéo à actions discrètes et sur des environnements en trois dimensions à la première personne, cette méthode **apprend, mais n'est pas compétitive**. C'est la seule affirmation que ce cours tient pour sûre sur ce point, et je ne la décore pas. Vous venez de lire six sections sur une architecture qui domine un banc d'essai de contrôle continu ; elle ne domine pas tout, et le périmètre d'un résultat fait partie du résultat. La semaine 12 vous a entraînés à cette lecture, et c'est la troisième fois en quatre semaines que ce cours s'en sert.

{{% comment %}}SOURCE: DREAMER p.16{{% /comment %}}

---
