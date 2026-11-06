---
title: "Laboratoire"
weight: 12
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté. Il n'y a pas de jalon cette semaine, le prochain est en semaine 10, et je vous recommande d'utiliser cette respiration pour écrire du code soigné plutôt que du code pressé.

Les deux volets suivent la structure de la semaine. Le **volet A** prend REINFORCE, le fait tourner avec et sans référence, et **mesure** la différence de variance. Le **volet B** écrit A2C vectorisé, avec son tronc commun et ses trois termes de perte. Le volet A est court et contient la seule mesure quantitative de la semaine ; le volet B est l'implémentation de référence que vous réutiliserez en semaines 9 et 10.

**Ce que le laboratoire n'implémente pas, et pourquoi.** A3C, c'est-à-dire la version à processus multiples de la section 8.10, n'est pas au programme du laboratoire : les processus multiples sont limités dans un carnet partagé, et une implémentation à quatre processus n'y est pas exécutable de façon fiable. Le volet B utilise donc des **environnements vectorisés synchrones**, qui règlent le problème 4 de la section 8.5 sans réclamer un seul processus supplémentaire. La section 8.10 se lit, se discute et ne s'exécute pas, et c'est une décision assumée.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

> [!WARNING]
 **Je ne vous donne aucun chiffre à atteindre pour A2C sur CartPole, et c'est volontaire.** Les nombres que cette semaine a cités sont ancrés : 384 épisodes pour REINFORCE sur CartPole, huit millions de trames pour A2C sur un jeu Atari. Aucun ne s'applique à ce que vous allez exécuter, qui est A2C sur CartPole, et je ne vais pas interpoler entre les deux pour vous donner une cible rassurante et fausse. Ce que j'attends de vous est donc une mesure **relative** et **reproductible** : votre propre nombre de pas à la résolution, obtenu sur au moins trois graines, avec son intervalle, et comparé à votre propre REINFORCE du volet A sur les mêmes graines. C'est exactement la discipline de la semaine 7, et c'est aussi la seule honnête quand aucune référence extérieure n'existe.

---

## Volet A : REINFORCE avec et sans référence, et la variance mesurée

**Objectif.** Produire **une** figure : la variance du gradient de politique au cours de l'entraînement, deux courbes, avec et sans référence, sur les mêmes graines.

**Étape 1.** Écrivez REINFORCE sur `CartPole-v1`, en reprenant les fragments des sections 8.1 et 8.3. Votre code doit comporter un indicateur `--reference` qui active ou désactive la soustraction d'une référence, et rien d'autre ne doit changer entre les deux modes. C'est une étude d'ablation à une variable, comme en semaine 6.

**Étape 2.** Utilisez comme référence la **moyenne glissante** des retours actualisés observés depuis le début de l'exécution. Deux lignes suffisent : un compteur de pas et une somme cumulée.

**Étape 3, le cœur du volet.** Isolez le gradient du terme de politique avec la manœuvre de la section 8.6, en rétropropageant ce terme seul avec `retain_graph=True`, en lisant les gradients avant de rétropropager l'entropie, puis en laissant l'optimiseur avancer sur la somme. Journalisez à chaque mise à jour la variance, la norme \(L_2\) et le maximum absolu de ce gradient.

**Étape 4.** Tracez les deux courbes de variance sur le même graphique, en échelle logarithmique en ordonnée, parce que l'écart attendu est de deux à trois ordres de grandeur et qu'une échelle linéaire l'écraserait. Puis répondez par écrit à deux questions : l'écart que vous mesurez est-il du même ordre que celui annoncé en section 8.6 ? Et la version avec référence résout-elle le problème en moins de pas, sur vos graines ?

**Deux vérifications arithmétiques avant de conclure.** Si vous utilisez un horizon de déroulement de 10 pas avec \(\gamma = 0{,}99\), votre référence doit converger vers \(1 + 0{,}99 + \dots + 0{,}99^9 \approx 9{,}56\), et vos échelles \(G_t - b\) doivent osciller autour de zéro. Si l'un des deux n'est pas vérifié, corrigez le bogue avant d'interpréter la moindre courbe.

{{% comment %}}SOURCE: LAPAN ch.11 p.347{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.12 p.357-359{{% /comment %}}

**Attendu.** La figure, les deux nombres de pas à la résolution avec leur intervalle sur vos graines, et un paragraphe de lecture.

{{< colab url="TODO" label="Volet A : REINFORCE avec et sans référence, et la variance du gradient mesurée" >}}

---

## Volet B : A2C vectorisé sur CartPole

**Objectif.** Écrire A2C de bout en bout, avec tronc commun, cible à \(N\) pas et perte à trois termes, sur un ensemble d'environnements vectorisés.

**Étape 1, les environnements.** Gymnasium fournit l'emballage qu'il faut. Un ensemble vectorisé synchrone enveloppe une liste de fabriques d'environnements et se présente comme **un** environnement qui accepte un vecteur d'actions et renvoie des lots d'observations et de récompenses. Attention aux deux attributs qui vous serviront à dimensionner le réseau : les espaces d'un ensemble vectorisé sont eux-mêmes des espaces de lots, et ce sont `single_observation_space` et `single_action_space` qui décrivent **un** environnement.

```python
import gymnasium as gym

N_ENVS = 16

envs = gym.vector.SyncVectorEnv(
    [lambda: gym.make("CartPole-v1") for _ in range(N_ENVS)]
)
taille_obs = envs.single_observation_space.shape[0]   # 4, et non (16, 4)
n_actions = int(envs.single_action_space.n)           # 2, et non (16,)
```

{{% comment %}}SOURCE: LAPAN ch.12 p.365-366{{% /comment %}}

**Étape 2, la cible à \(N\) pas, et c'est la fonction la plus délicate du volet.** Pour chaque transition du lot, la cible vaut la somme actualisée des \(N\) récompenses réellement reçues, à laquelle on ajoute \(\gamma^N \hat v(s_{t+N},\mathbf{w})\) **uniquement si l'épisode n'est pas terminé**. Le piège est la gestion des transitions terminales : si vous ajoutez la valeur estimée d'un état terminal, vous promettez à l'agent une récompense future qui n'existe pas. La façon propre de traiter cela est de collecter les indices des transitions non terminales, de n'évaluer le critique que sur celles-là, et d'ajouter le terme à ces indices seulement.

```python
import numpy as np
import torch


def preparer_lot(lot, reseau, gamma: float, n_pas: int, device):
    """(etats, actions, cibles) a partir d'un lot de transitions premier-dernier.

    Chaque transition porte deja la somme actualisee de ses n_pas recompenses ;
    il ne reste qu'a ajouter la queue estimee, et SEULEMENT si elle existe.
    """
    etats, actions, cibles = [], [], []
    derniers_etats, idx_non_terminaux = [], []

    for i, exp in enumerate(lot):
        etats.append(exp.etat)
        actions.append(exp.action)
        cibles.append(exp.recompense_actualisee)
        if exp.dernier_etat is not None:        # l'episode continue
            idx_non_terminaux.append(i)
            derniers_etats.append(exp.dernier_etat)

    etats_t = torch.as_tensor(np.asarray(etats), dtype=torch.float32, device=device)
    actions_t = torch.as_tensor(actions, dtype=torch.int64, device=device)
    cibles = np.asarray(cibles, dtype=np.float32)

    if derniers_etats:
        derniers_t = torch.as_tensor(np.asarray(derniers_etats),
                                     dtype=torch.float32, device=device)
        with torch.no_grad():                   # le critique est INTERROGE, pas entraine ici
            v_derniers = reseau(derniers_t)[1].squeeze(-1).cpu().numpy()
        cibles[idx_non_terminaux] += (gamma ** n_pas) * v_derniers

    return etats_t, actions_t, torch.as_tensor(cibles, device=device)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\sum_{i=0}^{N-1}\gamma^i r_{t+i}\) | somme actualisée des récompenses observées | `exp.recompense_actualisee` |
| \(s_{t+N}\) | état atteint après \(N\) pas, ou absent si l'épisode s'est terminé | `exp.dernier_etat` |
| \(\hat v(s_{t+N},\mathbf{w})\) | valeur estimée de la queue | `v_derniers` |
| \(\gamma^N\) | actualisation de la queue | `gamma ** n_pas` |
| \(G^{(N)}_t\) | la cible complète | la troisième valeur de retour |

**Étape 3, la boucle.** Assemblez la perte à trois termes de la section 8.8, additionnez les trois, rétropropagez une seule fois, écrêtez la norme du gradient, et avancez. N'oubliez ni le `detach()` ni le `eps` d'Adam : ce sont les deux lignes qui décident si ce volet fonctionne.

**Étape 4, les dix quantités à journaliser.** Cette liste est à la fois le tableau de bord du volet et la liste de diagnostic de la semaine. Journalisez : l'**avantage** moyen, la **valeur** moyenne prédite par le critique, la **récompense** moyenne par épisode, les **trois termes de perte** séparément, la **perte totale**, et les **trois statistiques de gradient** (norme \(L_2\), maximum absolu, variance). Ajoutez l'**entropie** de la politique, qui n'est pas dans la perte sous cette forme et qui est votre meilleur indicateur du problème 3.

{{% comment %}}SOURCE: LAPAN ch.12 p.369{{% /comment %}}

**Étape 5, l'ablation, et elle est rapide.** Relancez trois fois en retirant **un** élément à la fois : sans le terme d'entropie, sans l'écrêtage du gradient, et avec un seul environnement au lieu de \(N\). Pour chacun, dites ce qui change dans les courbes et à quel problème de la section 8.5 ce changement correspond. C'est l'exercice qui transforme le tableau de la section 8.5 en savoir pratique.

**Attendu.** La courbe de récompense sur au moins trois graines avec intervalle, les dix quantités journalisées, le tableau de vos trois ablations, et la comparaison avec votre REINFORCE du volet A sur les mêmes graines.

{{< colab url="TODO" label="Volet B : A2C vectorisé sur CartPole, trois termes de perte et dix quantités journalisées" >}}

**Diagnostic facultatif, et je vous le recommande vivement si vous avez du temps.** Mesurez la **divergence de Kullback-Leibler** \(\KL\) entre la politique avant et après chaque pas d'optimisation. C'est trois lignes : gardez les probabilités avant le pas, recalculez les log-probabilités après, et formez \(\sum_a \pi_{\text{avant}}\,(\log\pi_{\text{avant}} - \log\pi_{\text{après}})\). Une exécution saine reste en dessous de \(10^{-3}\). Des pics élevés sont un mauvais signe : ils veulent dire que le pas a déplacé la politique **trop loin**, et un réseau très non linéaire en grande dimension réagit mal à cela. Retenez cette quantité : elle est le sujet de la semaine 10.

{{% comment %}}SOURCE: LAPAN ch.11 p.346 ; ch.11 p.349{{% /comment %}}

> [!TIP]
 **Mon message pour ce laboratoire.** Le volet A mesure une variance et le volet B construit un algorithme, et c'est dans cet ordre que je vous demande de les faire, même si le volet B est le plus intéressant. La raison est celle de toute la semaine : vous n'avez, dans A2C, **aucune** perte dont la valeur vous dise si les choses se passent bien. Le seul moyen de savoir ce qui se passe est de savoir à quoi ressemble une variance normale, une entropie normale, une norme de gradient normale. Le volet A vous donne ces repères sur un algorithme simple. Sans eux, le volet B est une boîte noire qui monte ou ne monte pas.

---
