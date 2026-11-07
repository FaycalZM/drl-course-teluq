---
title: "5.5 Le même geste, pour les valeurs d'action"
weight: 6
---

## De \(\hat v\) à \(\hat q\), et c'est presque gratuit

Tout ce que nous venons de construire porte sur des valeurs d'**état**. Or la semaine 4 nous a appris, et de façon décisive, que pour agir sans modèle il faut des valeurs d'**action** : avec \(Q\), l'amélioration de politique est une lecture de table ; avec \(V\), elle exige de savoir où mènent les actions.

Bonne nouvelle : l'extension des méthodes semi-gradient aux valeurs d'action est **directe**. Les exemples d'entraînement, qui étaient des paires \(S_t \mapsto U_t\), deviennent des paires \(S_t, A_t \mapsto U_t\), où \(U_t\) peut être n'importe quelle approximation de \(q_\pi(S_t,A_t)\). On apprend donc \(\hat q(s,a,\mathbf{w}) \approx q_\pi(s,a)\), et la mise à jour générique se recopie en changeant les lettres.

$$
\mathbf{w}_{t+1} \defeq \mathbf{w}_t + \alpha
\big[\, U_t - \hat q(S_t,A_t,\mathbf{w}_t) \,\big]\nabla\hat q(S_t,A_t,\mathbf{w}_t)
$$

{{% comment %}}SOURCE: SB ch.10 éq. 10.1 p.266{{% /comment %}}

Avec la cible à un pas de Sarsa, on obtient la méthode complète, qui s'appelle le **Sarsa semi-gradient à un pas épisodique** :

$$
\mathbf{w}_{t+1} \defeq \mathbf{w}_t + \alpha
\big[\, R_{t+1} + \gamma\,\hat q(S_{t+1},A_{t+1},\mathbf{w}_t) -
 \hat q(S_t,A_t,\mathbf{w}_t) \,\big]\nabla\hat q(S_t,A_t,\mathbf{w}_t)
$$

{{% comment %}}SOURCE: SB ch.10 éq. 10.2 p.266{{% /comment %}}

Comparez avec la mise à jour de Sarsa tabulaire de la semaine 4. Le crochet est **identique**, au chapeau près : c'est toujours récompense, plus valeur actualisée de la suite, moins valeur courante. Ce qui a changé est à l'extérieur du crochet : au lieu d'écrire le résultat dans une case, on s'en sert pour pondérer un gradient. C'est très exactement la ligne que je vous avais demandé de lire à voix haute à la fin de la semaine 4.

Pour faire du **contrôle** et non seulement de la prédiction, il faut maintenant une étape d'amélioration de politique, et voici la phrase qui va dicter l'architecture de notre réseau en section 5.8. Si l'ensemble des actions est **discret et pas trop grand**, alors pour chaque action \(a\) disponible dans l'état courant \(S_t\), on peut calculer \(\hat q(S_t,a,\mathbf{w})\) et chercher l'action gloutonne :

$$
A^*_t = \argmax_a \hat q(S_t,a,\mathbf{w}_t)
$$

L'amélioration de politique se fait alors en remplaçant la politique d'estimation par une approximation **souple** de cette politique gloutonne, et la méthode \(\varepsilon\)-gloutonne de la semaine 4 en est l'exemple le plus simple.

{{% comment %}}SOURCE: SB ch.10 p.266{{% /comment %}}

Notez bien la construction de cette phrase : *pour chaque action, calculer \(\hat q\)*. Elle suppose donc une boucle sur les actions. En section 5.8, l'implémentation fera mieux : le réseau émettra **toutes** les valeurs d'un coup, une sortie par action, et la boucle disparaîtra dans un seul passage avant. Le formalisme dit quoi calculer ; l'ingénierie dit comment le calculer une seule fois.

Le pseudocode de cette méthode traite explicitement le cas terminal, et je le fais figurer parce qu'il **boucle** avec la semaine 4. Lorsque \(S'\) est terminal, la mise à jour devient :

$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha
\big[\, R - \hat q(S,A,\mathbf{w}) \,\big]\nabla\hat q(S,A,\mathbf{w})
$$

{{% comment %}}SOURCE: SB ch.10 p.266{{% /comment %}}

Autrement dit, le terme de valeur future disparaît purement et simplement. Vous avez maintenant vu cette règle sous **quatre** écritures : « un état terminal a une valeur nulle » en semaine 4, \(\hat v(\text{terminal},\cdot) = 0\) dans le TD(0) semi-gradient de la section 5.4, le cas terminal ci-dessus, et, dans deux sections, une ligne de PyTorch qui s'écrit `valeurs_suivantes[termines] = 0.0`. Même règle, quatre vêtements. Si vous en oubliez un seul dans une implémentation, elle ne converge pas.

Voici le réseau, et c'est déjà, à peu de choses près, celui du DQN.

```python
class ValeursActionApprochees(nn.Module):
    """hat q(s, ., w) : UNE SORTIE PAR ACTION, obtenues en un seul passage."""

    def __init__(self, taille_obs: int, n_actions: int, taille_cachee: int = 128):
        super().__init__()
        self.corps = nn.Sequential(
            nn.Linear(taille_obs, taille_cachee),
            nn.ReLU(),
            nn.Linear(taille_cachee, n_actions),   # pas de non-linéarité en sortie
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        return self.corps(obs)                     # forme (lot, n_actions)


def action_gloutonne(reseau, obs_unique: torch.Tensor) -> int:
    """A*_t = argmax_a hat q(S_t, a, w), en un passage avant et sans boucle."""
    with torch.no_grad():
        valeurs = reseau(obs_unique.unsqueeze(0))  # (1, n_actions)
    return int(valeurs.argmax(dim=1).item())
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\hat q(s,a,\mathbf{w})\) | valeur d'action approchée | une case de `reseau(obs)` |
| \(\hat q(s,\cdot,\mathbf{w})\) | **toutes** les valeurs d'action de \(s\) | la ligne entière `reseau(obs)` |
| \(A^*_t = \argmax_a \hat q(S_t,a,\mathbf{w}_t)\) | l'action gloutonne | `valeurs.argmax(dim=1)` |
| \(\mathcal{A}\) | l'ensemble des actions, discret et petit | `n_actions`, la dimension de sortie |
| cas terminal | le terme futur disparaît | `valeurs_suivantes[termines] = 0.0` |

Remarquez l'absence de non-linéarité sur la dernière couche. C'est volontaire et ce sera répété en 5.8 : une valeur d'action peut prendre **n'importe quelle valeur réelle**, positive ou négative, grande ou petite, et une sigmoïde ou une ReLU en sortie interdirait au réseau d'exprimer la moitié de ce qu'on lui demande.

---

## À quoi ressemble une valeur approchée sur un espace continu

Je veux maintenant vous montrer une image, parce que depuis la semaine 1 toutes nos fonctions de valeur ont été des **tableaux de nombres**, et qu'une fonction de valeur sur un espace continu n'a pas cette tête-là du tout.

L'environnement s'appelle Mountain Car, et sa règle est délicieuse. Une voiture est au fond d'une vallée, et son moteur est trop faible pour remonter la pente qui mène à l'objectif, même à plein régime. La seule solution est de **reculer**, de monter la pente opposée, et d'utiliser l'élan acquis. C'est l'exemple le plus simple que je connaisse d'une tâche de contrôle continu où les choses doivent d'abord empirer, en un certain sens, avant de pouvoir s'améliorer : il faut s'éloigner du but pour l'atteindre.

Les récompenses sont de \(-1\) à chaque pas jusqu'à ce que la voiture franchisse le sommet, ce qui met fin à l'épisode. Trois actions seulement : pousser vers l'avant, ne rien faire, pousser vers l'arrière. L'état est continu et bidimensionnel, position et vitesse.

{{% comment %}}SOURCE: SB ch.10 p.266-267{{% /comment %}}

La **Figure 5-1** montre cette tâche puis la surface de son **coût pour atteindre** (*cost-to-go*), défini comme \(-\max_a \hat q(s,a,\mathbf{w})\), à cinq moments d'un même apprentissage.

{{< bookfig src="05-01.png" week="05" >}}

{{% comment %}}SOURCE: SB ch.10 p.267{{% /comment %}}

Prenez le temps de la lire, parce qu'elle est deux choses à la fois. D'abord, c'est la première image du cours qui montre une valeur apprise sur un espace **continu** : une surface, et non une grille de nombres. Ensuite, c'est une image de l'**apprentissage lui-même**, puisque les panneaux successifs sont le même objet à des instants différents. Regardez la vallée se creuser : la surface, presque plate au départ, prend progressivement la forme du problème.

Un détail de cette figure est contre-intuitif et vaut une minute. Les valeurs d'action étaient toutes initialisées à **zéro**, ce qui, ici, est **optimiste** : toutes les valeurs vraies sont négatives, puisque chaque pas coûte \(-1\). Un agent qui croit que tout vaut zéro et qui découvre que tout coûte quelque chose explore spontanément, et c'est pourquoi l'exploration a eu lieu dans cette expérience **même avec \(\varepsilon = 0\)**. Au premier panneau, après 428 pas, aucun épisode n'était encore terminé : la voiture oscillait au fond de la vallée sans jamais atteindre le sommet.

{{% comment %}}SOURCE: SB ch.10 p.268{{% /comment %}}

> [!TIP]
 **Un conseil que vous utiliserez dès le laboratoire.** L'initialisation des valeurs n'est pas neutre, et sa neutralité apparente dépend du **signe des récompenses** de votre environnement. Des poids initialisés au hasard autour de zéro sont optimistes dans un environnement qui ne distribue que des pénalités, et pessimistes dans un environnement qui ne distribue que des gains. Cela ne remplace pas une stratégie d'exploration, mais cela explique bien des comportements du premier millier de pas, et cela vous évitera de chercher un bogue là où il n'y en a pas.

Une précision pour finir, parce que vous pourriez vouloir reproduire cette figure. La surface a été obtenue avec une approximation **linéaire sur des caractéristiques construites à la main**, c'est-à-dire par la route classique que ce cours ne prend pas. Ce que je vous demande de retenir de la Figure 5-1 est donc la **forme de la surface** et sa transformation au cours de l'apprentissage, et non la méthode qui l'a produite.

{{% comment %}}SOURCE: SB ch.10 p.268{{% /comment %}}

---
