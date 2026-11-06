---
title: "6.5 Un socle commun, sans quoi il n'y a pas d'ablation"
weight: 6
---

## Quatre scripts qui ne diffèrent que d'une ligne

Nous arrivons à la charnière de la semaine, et c'est une section d'ingénierie qui porte une exigence de méthode.

Nous allons étudier cinq variantes du réseau Q profond et le laboratoire vous en fera comparer quatre. Posons la question à l'envers : qu'est-ce qui rend une telle comparaison **valide** ? Pas la qualité de chaque implémentation prise à part. Ce qui la rend valide est que les quatre programmes soient **identiques partout sauf à l'endroit étudié**. Même tampon, même optimiseur, même pas d'apprentissage, même calendrier d'exploration, même critère d'arrêt, même mise en lot. Si deux variantes diffèrent par deux choses, la comparaison ne mesure rien, et c'est l'erreur de méthode la plus répandue dans tout ce domaine.

D'où un **socle commun** : un seul fichier, importé par toutes les variantes, qui contient les hyperparamètres, le dépliage d'un lot, la perte de référence, et le calendrier d'exploration. Une variante est alors un script de trente lignes qui importe le socle et change une chose.

{{% comment %}}SOURCE: LAPAN ch.8 p.227-232{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que c'est la compétence évaluée de cette semaine et qu'elle n'est pas une compétence de codage.** Une étude d'ablation (*ablation study*) n'est pas une collection de résultats : c'est une expérience contrôlée. Elle exige un socle de code unique, des hyperparamètres identiques, les mêmes graines aléatoires, le même nombre de pas, et des courbes lissées de la même façon. Quatre scripts écrits séparément, même tous corrects, produisent quatre nombres **incomparables**. Retenez la formule : dans une ablation, ce qui est commun est aussi important que ce qui diffère.

Commençons par les hyperparamètres. Les voici, rassemblés dans une seule structure, avec les valeurs du jeu de référence.

| Hyperparamètre | Valeur | Rôle |
| --- | --- | --- |
| `gamma` | 0,99 | le facteur d'actualisation \(\gamma\) |
| `batch_size` | 32 | la taille du lot \(\lvert B\rvert\) |
| `replay_size` | 100 000 | la capacité du tampon \(\mathcal{D}\) |
| `replay_initial` | 10 000 | transitions accumulées avant le premier pas d'apprentissage |
| `learning_rate` | \(10^{-4}\) | le pas d'apprentissage \(\alpha\) |
| `target_net_sync` | 1 000 | la période \(N\) de recopie de \(\theta\) dans \(\theta^-\) |
| `epsilon_start` / `epsilon_final` | 1,0 / 0,02 | les bornes du calendrier de \(\varepsilon\) |
| `epsilon_frames` | 100 000 | la durée de la décroissance linéaire |
| `stop_reward` | 18,0 | le seuil de résolution sur la moyenne des derniers épisodes |

{{% comment %}}SOURCE: LAPAN ch.8 p.228{{% /comment %}}

Comparez avec les neuf nombres de la section 5.8 et vous verrez qu'ils ne sont pas les mêmes : le tampon est dix fois plus grand, la décroissance de \(\varepsilon\) est plus courte, le seuil de résolution est à 18 et non à 19. C'est normal, et c'est l'illustration la plus économique de l'avertissement de la semaine dernière : ces nombres sont les réglages d'une expérience, pas des constantes de la méthode. Ce qui compte ici n'est aucune de ces valeurs, c'est qu'elles soient **les mêmes pour les cinq variantes**.

---

## Le dépliage d'un lot, et une astuce qui mérite d'être comprise

Le socle contient une fonction qui prend une liste de transitions premier-dernier et rend cinq tableaux : les états, les actions, les récompenses, le masque terminal, et les états finaux. Rien de surprenant, sauf une ligne, et cette ligne est un bon exercice de lecture.

Que met-on dans le tableau des états finaux quand l'épisode s'est terminé, c'est-à-dire quand la transition porte `None` ? La réponse qui vient à l'esprit est : rien, on écarte ces transitions. La réponse employée en pratique est plus astucieuse : on y met l'**état initial de la même transition**, qui est forcément disponible. C'est une valeur arbitraire, et c'est sans conséquence, parce que le masque terminal va de toute façon annuler cette colonne dans le calcul de la cible. Le bénéfice est que tous les tableaux ont la même longueur et qu'un seul passage avant suffit pour tout le lot, sans partition ni réassemblage.

{{% comment %}}SOURCE: LAPAN ch.8 p.229{{% /comment %}}

C'est le `valeurs_suivantes[termines] = 0.0` de la semaine 5, descendu d'un étage et enfin justifié. La semaine dernière, cette ligne était une correction ; ici, elle est la condition qui autorise l'astuce.

```python
import numpy as np
import torch
import torch.nn as nn

def deplier_lot(lot):
    """Cinq tableaux de même longueur, masque terminal compris."""
    etats, actions, recompenses, termines, etats_finaux = [], [], [], [], []
    for transition in lot:
        etats.append(transition.etat)
        actions.append(transition.action)
        recompenses.append(transition.recompense)
        termines.append(transition.etat_final is None)
        # Pour une transition terminale, on range l'état INITIAL : la valeur
        # est arbitraire, le masque l'annulera de toute façon.
        etats_finaux.append(transition.etat
                            if transition.etat_final is None
                            else transition.etat_final)
    return (np.asarray(etats, dtype=np.float32),
            np.asarray(actions),
            np.asarray(recompenses, dtype=np.float32),
            np.asarray(termines, dtype=bool),
            np.asarray(etats_finaux, dtype=np.float32))


def calculer_perte(lot, reseau, reseau_cible, gamma: float, peripherique):
    """La perte de référence. Identique à la semaine 5, à un détail près."""
    etats, actions, recompenses, termines, etats_finaux = deplier_lot(lot)

    etats_t = torch.as_tensor(etats).to(peripherique)
    etats_f_t = torch.as_tensor(etats_finaux).to(peripherique)
    actions_t = torch.as_tensor(actions).to(peripherique)
    recompenses_t = torch.as_tensor(recompenses).to(peripherique)
    termines_t = torch.as_tensor(termines).to(peripherique)

    valeurs_action = reseau(etats_t).gather(
        1, actions_t.unsqueeze(-1)).squeeze(-1)

    with torch.no_grad():                       # LE détail de cette semaine
        valeurs_finales = reseau_cible(etats_f_t).max(1)[0]
        valeurs_finales[termines_t] = 0.0       # le masque terminal

    cibles = recompenses_t + gamma * valeurs_finales.detach()
    return nn.MSELoss()(valeurs_action, cibles)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta(s_i,a_i)\) | valeur de l'action réellement jouée | `valeurs_action`, via `gather` |
| \(\max_{a'} Q_{\theta^-}(s'_i,a')\) | la meilleure valeur suivante, poids figés | `valeurs_finales` |
| \(\hat q(\text{terminal},\cdot) = 0\) | le masque terminal | `valeurs_finales[termines_t] = 0.0` |
| \(y_i = r_i + \gamma\max_{a'}Q_{\theta^-}(s'_i,a')\) | la cible | `cibles` |
| \(\gamma\) | facteur d'actualisation | `gamma`, et il **changera** en 6.6 |
| « cible tenue pour constante » | le semi de semi-gradient | `torch.no_grad()` et `.detach()` |

Le seul changement par rapport à la semaine 5 est le `torch.no_grad()` qui entoure explicitement le passage avant du réseau cible. Vous l'aviez déjà, et je le signale pour une raison de méthode : dans un fichier que quatre variantes vont importer et modifier, une protection redondante n'est pas du luxe. La prochaine personne qui éditera cette fonction, et ce sera vous en section 6.10, doit pouvoir le faire sans se demander par où un gradient pourrait remonter.

{{% comment %}}SOURCE: LAPAN ch.8 p.229-230{{% /comment %}}

---

## Le calendrier d'exploration, et le suivi de l'entraînement

Le socle contient aussi le calendrier de \(\varepsilon\), devenu un objet. Sa règle est celle de la semaine 5, et je la redonne parce que c'est précisément cette formule que la section 6.9 va supprimer :

$$
\varepsilon_k = \max\!\big(\varepsilon_{\text{final}},\;
 \varepsilon_{\text{départ}} - k / N_{\text{trames}}\big)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.230{{% /comment %}}

Une décroissance linéaire, bornée par le bas, pilotée par le numéro de trame. L'objet qui la porte expose une méthode à appeler une fois par trame, et c'est cette méthode qui écrit dans l'attribut `epsilon` du sélecteur de la section 6.2. Trois objets, une seule décision d'exploration, et pas une ligne de calendrier dans la boucle principale.

Le socle contient enfin un générateur de lots, dont la logique tient en trois lignes : remplir une fois le tampon jusqu'à `replay_initial`, puis, indéfiniment, ajouter une transition et rendre un lot tiré au hasard. Et trois utilitaires de suivi que je mentionne parce que leur rôle est moins décoratif qu'il n'y paraît. Un premier détecte la fin d'un épisode et déclare l'environnement « résolu » quand la récompense moyenne franchit le seuil, ce qui est la définition opérationnelle de la convergence dans toute cette semaine. Un deuxième mesure le débit en trames par seconde, et vous verrez en 6.9 et en 6.11 que cette mesure change la conclusion de deux comparaisons sur cinq. Un troisième n'écrit les métriques que toutes les cent itérations, sans quoi les fichiers de suivi deviennent énormes.

{{% comment %}}SOURCE: LAPAN ch.8 p.230, p.231-232{{% /comment %}}

Reste à établir la **référence**, puisqu'une ablation se lit toujours contre quelque chose. Avec les hyperparamètres du tableau ci-dessus et sur le jeu de référence, un réseau Q profond ordinaire atteint une récompense moyenne de 18 en environ **700 000 trames** et environ **400 parties**. Ces deux nombres sont la ligne de base de toute la seconde moitié de la semaine, et je les écrirai sous cette forme chaque fois que j'en aurai besoin.

{{% comment %}}SOURCE: LAPAN ch.8 p.239{{% /comment %}}

> [!WARNING]
 **Attention, et cet avertissement vaut pour les six sections qui suivent.** Les 700 000 trames et les 400 parties ci-dessus, comme tous les chiffres de comparaison que je vais citer, viennent de runs sur un jeu Atari, avec des hyperparamètres réglés pour lui, sur un processeur graphique, pendant des heures. Votre laboratoire tourne sur CartPole, en quelques minutes. Ces chiffres sont des **ordres de grandeur sur Atari** et rien d'autre : ils vous disent si une réparation vaut dix pour cent ou un facteur trois, et ils ne vous disent **rien** de ce que vous allez observer vendredi. Ne les prenez jamais pour des attentes. Les attentes du laboratoire sont écrites dans le laboratoire, et elles sont qualitatives.

{{% comment %}}SOURCE: LAPAN ch.8 p.240, p.262{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

---
