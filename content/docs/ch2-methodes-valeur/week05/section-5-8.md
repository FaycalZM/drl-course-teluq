---
title: "5.8 L'implémentation : enveloppes, architecture, perte"
weight: 9
---

## Les enveloppes, ou pourquoi un DQN ne converge pas

Je commence par l'avertissement le plus utile de la semaine, et il ne porte ni sur les mathématiques ni sur l'architecture.

Quand un réseau Q profond ne converge pas, le problème n'est pas toujours dans le code de l'algorithme : il est très souvent dans l'**environnement mal enveloppé**. Le cas d'école, et il a coûté des journées de débogage à beaucoup de monde, est l'oubli de l'appui sur le bouton FIRE au début d'une partie : l'agent observe un écran immobile, n'obtient jamais de récompense, et tout le reste du code est pourtant parfaitement correct.

{{% comment %}}SOURCE: LAPAN ch.6 p.179{{% /comment %}}

C'est pour cela que cette sous-section existe. Les transformations qui suivent ne sont pas de la plomberie : elles définissent **ce que l'agent voit**, donc ce qu'il peut apprendre. En voici la liste complète, avec le rôle de chacune. Vous avez rencontré la notion d'**enveloppe** (*wrapper*) en semaine 1 ; c'est toujours le même mécanisme, appliqué huit fois de suite.

| Transformation | Ce qu'elle fait | Pourquoi |
| --- | --- | --- |
| une vie = un épisode | termine l'épisode à chaque vie perdue | épisodes plus courts, convergence plus rapide ; Pong s'y prête |
| jusqu'à 30 actions neutres au `reset()` | joue un nombre aléatoire d'actions sans effet au départ | saute les écrans d'introduction |
| **saut de trames** (*frame skipping*) | répète l'action choisie pendant \(K\) trames, avec \(K = 3\) ou 4 | traiter chaque trame avec un réseau est très coûteux, et l'écart entre deux trames consécutives est généralement minime |
| maximum pixel à pixel des deux dernières trames | combine les deux dernières images | les sprites d'Atari scintillent ; le scintillement est invisible à l'œil humain, mais il peut tromper un réseau de neurones |
| appui sur FIRE au `reset()` | lance la partie | sans cet appui l'environnement devient un PDM partiellement observable, puisque l'observation ne dit pas si FIRE a déjà été pressé |
| 210 × 160 en couleurs → 84 × 84 en **niveaux de gris** | réduit l'entrée du réseau | la couleur n'apporte rien ici ; l'implémentation originale prenait le canal de luminance, d'autres font un recadrage puis un redimensionnement |
| **empilement de trames** (*frame stacking*) | empile les 4 dernières observations | la propriété de Markov, section 5.7 |
| **écrêtage de la récompense** (*reward clipping*) à \(-1\), 0, 1 | ne garde que le signe de la récompense | Pong donne 1 par point, un autre jeu 100 par ennemi tué, et cet écart donne à la perte des échelles complètement différentes d'un jeu à l'autre |
| HWC → CHW | réordonne les axes de l'image | convention des tenseurs d'images de PyTorch |

{{% comment %}}SOURCE: LAPAN ch.6 p.178-179{{% /comment %}}

Deux détails d'implémentation méritent une phrase chacun, parce qu'ils causent des bogues silencieux.

Premièrement, l'enveloppe qui empile les trames doit renvoyer une **copie** de son tampon interne et non le tampon lui-même. La raison est que les observations vont être conservées dans le tampon de rejeu : sans copie, les pas suivants de l'environnement viendraient réécrire des observations déjà rangées. Toutes les entrées du tampon pointent alors vers le même tableau, réécrit en permanence, et le tampon finit par contenir des milliers d'exemplaires de l'observation la plus récente. Aucune exception n'est levée, et rien n'apprend.

Deuxièmement, cette enveloppe doit être la **dernière de la chaîne**, puisqu'elle empile ce que les autres ont déjà transformé.

{{% comment %}}SOURCE: LAPAN ch.6 p.181-182{{% /comment %}}

```python
import gymnasium as gym

class EnveloppeEmpilementTrames(gym.ObservationWrapper):
    """Empile les k dernières observations. À PLACER EN DERNIER dans la chaîne."""

    def __init__(self, env, k: int = 4):
        super().__init__(env)
        self.k = k
        forme = env.observation_space.shape                 # (1, 84, 84)
        self.pile = np.zeros((k * forme[0], *forme[1:]), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=self.pile.shape, dtype=np.uint8)

    def reset(self, **kwargs):
        self.pile[:] = 0
        obs, info = self.env.reset(**kwargs)
        return self.observation(obs), info

    def observation(self, obs):
        self.pile[:-1] = self.pile[1:]                      # la plus vieille sort
        self.pile[-1] = obs
        return self.pile.copy()                             # UNE COPIE, obligatoire
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(k\) | nombre de trames empilées | `k = 4` |
| \(K\) | nombre de trames sautées par action | le paramètre de l'enveloppe de saut |
| l'observation \(s\) | la pile de \(k\) trames, pas une image | `self.pile.copy()` |
| le type de stockage | `uint8`, et non `float32` | `dtype=np.uint8` |

---

## L'architecture : une sortie par action

L'architecture est celle de la publication qui a fait école, et elle est modeste par les standards d'aujourd'hui : **trois couches de convolution**, puis **deux couches linéaires**, avec une unité linéaire rectifiée entre chacune d'elles, et **aucune non-linéarité sur la sortie**, puisqu'une valeur d'action peut prendre n'importe quelle valeur réelle.

{{% comment %}}SOURCE: LAPAN ch.6 p.182{{% /comment %}}

Les formes, parce que le laboratoire les redemande : entrée de \(4 \times 84 \times 84\) ; une convolution de 4 vers 32 canaux, noyau 8, pas 4 ; une de 32 vers 64, noyau 4, pas 2 ; une de 64 vers 64, noyau 3, pas 1 ; aplatissement vers **3136** valeurs ; une couche linéaire de 3136 vers 512 ; une couche linéaire de 512 vers le nombre d'actions, qui vaut 6 pour Pong.

{{% comment %}}SOURCE: LAPAN ch.6 p.183, p.196{{% /comment %}}

Le nombre 3136 n'est pas écrit en dur dans le code : on l'obtient à l'exécution en poussant un tenseur de zéros à travers la partie convolutive et en mesurant ce qui sort. C'est une petite discipline qui vous évitera de recalculer des dimensions à la main chaque fois que vous changez la taille d'entrée.

> [!IMPORTANT]
 **Je dois insister sur la seule décision d'architecture qui mérite un paragraphe : une sortie par action.** On pourrait prendre \(Q(s,a)\) au pied de la lettre et construire un réseau qui reçoit **l'état et l'action** et rend un seul nombre. C'est d'ailleurs la lecture naturelle de la notation. Ce n'est pas ce qu'on fait, et la raison est la vitesse : calculer toutes les valeurs d'action en un seul passage dans le réseau est significativement plus rapide. Comptez : avec six actions, choisir l'action gloutonne demanderait **six** passages avant au lieu d'un, et le calcul du \(\max_{a'}\) de la cible en demanderait six de plus par transition du lot. Souvenez-vous aussi de la section 5.5 : le formalisme demandait de calculer \(\hat q(S_t,a,\mathbf{w})\) *pour chaque action*. L'architecture à une sortie par action est l'exécution efficace de cette phrase, et c'est elle qui rend la semaine 6 possible, où la sortie se **dédoublera**.

{{% comment %}}SOURCE: LAPAN ch.6 p.183{{% /comment %}}

```python
class DQN(nn.Module):
    """Q_theta : de la pile de 4 trames vers une valeur par action."""

    def __init__(self, forme_entree, n_actions: int):
        super().__init__()
        self.convolutions = nn.Sequential(
            nn.Conv2d(forme_entree[0], 32, kernel_size=8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1), nn.ReLU(),
            nn.Flatten(),
        )
        # 3136 mesuré, jamais écrit en dur.
        with torch.no_grad():
            taille = self.convolutions(torch.zeros(1, *forme_entree)).shape[1]
        self.tete = nn.Sequential(
            nn.Linear(taille, 512), nn.ReLU(),
            nn.Linear(512, n_actions),          # AUCUNE non-linéarité ici
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        # Les observations arrivent en uint8 ; la division se fait ICI, sur le GPU.
        x = obs.float() / 255.0
        return self.tete(self.convolutions(x))
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta(s,\cdot)\) | les valeurs de toutes les actions de \(s\) | `reseau(obs)`, forme `(lot, n_actions)` |
| \(\theta\) | les poids du réseau | `reseau.parameters()` |
| \(\lvert\mathcal{A}\rvert\) | nombre d'actions, 6 pour Pong | `n_actions` |
| la pile d'entrée | \(4 \times 84 \times 84\) | `forme_entree` |
| aucune non-linéarité en sortie | une valeur Q peut être négative et grande | la dernière `nn.Linear` |

Deux remarques sur ce fragment, et la seconde est une astuce que vous réutiliserez partout.

La division par 255 est faite **à l'intérieur** de `forward`, et non au moment du stockage. Les observations sont donc conservées en `uint8` dans le tampon de rejeu, ce qui divise par quatre la mémoire occupée et la bande passante vers le processeur graphique, et la conversion en flottants se fait sur le processeur graphique, où elle est rapide puisque le tenseur d'octets d'entrée y est déjà. Avec un tampon de dix mille piles de quatre trames de 84 sur 84, la différence est de l'ordre de deux gigaoctets contre huit.

{{% comment %}}SOURCE: LAPAN ch.6 p.184{{% /comment %}}

Et une mesure, pour calibrer vos attentes : ce modèle de 2015, qui est minuscule par les standards d'aujourd'hui, compte déjà plus de 1,5 million de paramètres. Comparez avec les 769 poids du petit réseau de la section 5.2, et avec les seize cases de la table de la semaine 4. Trois ordres de grandeur séparent chacun de ces objets du suivant, et ils calculent tous la même chose.

{{% comment %}}SOURCE: LAPAN ch.6 p.176{{% /comment %}}

---

## La perte, ligne par ligne

Nous arrivons au cœur du code, et c'est ici que la double lecture de cette semaine se referme. Trois lignes, trois idées, et chacune des trois a déjà été démontrée dans une section précédente.

La **Figure 5-5** suit les formes des tenseurs à travers ce calcul : la sortie du réseau, les actions réellement jouées, les valeurs Q sélectionnées, et le résultat du prélèvement ligne par ligne. Gardez-la sous les yeux pendant la lecture du fragment, parce que presque toutes les erreurs de ce calcul sont des erreurs de forme.

{{< bookfig src="05-05.png" week="05" >}}

{{% comment %}}SOURCE: LAPAN ch.6 p.190-191{{% /comment %}}

```python
def calculer_perte(lot, reseau, reseau_cible, gamma: float,
                   peripherique) -> torch.Tensor:
    """La perte d'un DQN sur un lot. Trois décisions, trois lignes commentées."""
    obs, actions, recompenses, termines, obs_suivantes = lot

    obs_t = torch.as_tensor(obs).to(peripherique)
    obs_suiv_t = torch.as_tensor(obs_suivantes).to(peripherique)
    actions_t = torch.as_tensor(actions).to(peripherique)
    recompenses_t = torch.as_tensor(recompenses).to(peripherique)
    termines_t = torch.as_tensor(termines).to(peripherique)

    # 1. Dans chaque ligne du lot, prélever le Q de l'action RÉELLEMENT jouée.
    #    gather est différentiable : les gradients passent par ce prélèvement.
    valeurs_action = reseau(obs_t).gather(
        1, actions_t.unsqueeze(-1)).squeeze(-1)

    with torch.no_grad():
        # Le MAX est pris sur le réseau CIBLE, jamais sur le réseau entraîné.
        valeurs_suivantes = reseau_cible(obs_suiv_t).max(1)[0]
        # 2. Le masque terminal : quatrième écriture de « un terminal vaut zéro ».
        valeurs_suivantes[termines_t] = 0.0
        # 3. Le semi-gradient : la cible est tenue pour une constante.
        valeurs_suivantes = valeurs_suivantes.detach()

    cibles = recompenses_t + gamma * valeurs_suivantes
    return nn.MSELoss()(valeurs_action, cibles)      # erreur quadratique moyenne
```

Et la perte que ce fragment calcule, écrite proprement :

$$
y_i =
\begin{cases}
r_i & \text{si } s'_i \text{ est terminal},\\[4pt]
r_i + \gamma \max_{a'} Q_{\theta^-}(s'_i,a') & \text{sinon,}
\end{cases}
\qquad
\mathcal{L}(\theta) = \frac{1}{\lvert B\rvert}
 \sum_{i \in B} \big(Q_\theta(s_i,a_i) - y_i\big)^2
$$

{{% comment %}}SOURCE: LAPAN ch.6 p.176, p.192{{% /comment %}}

Voici le tableau de correspondance complet de la semaine. C'est celui que je vous demande de savoir reconstituer, et c'est à lui que renverront les questions du quiz.

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(Q_\theta(s,a)\) | valeur d'action estimée par le réseau entraîné | `reseau(obs_t)` |
| \(Q_\theta(s_i,a_i)\) | valeur de l'action **réellement jouée** | `valeurs_action`, via `gather` |
| \(Q_{\theta^-}(s',a')\) | valeurs produites par le réseau cible | `reseau_cible(obs_suiv_t)` |
| \(\max_{a'} Q_{\theta^-}(s',a')\) | meilleure valeur suivante sous les poids figés | `.max(1)[0]` |
| \(\hat v(\text{terminal},\cdot) = 0\) | un état terminal vaut zéro | `valeurs_suivantes[termines_t] = 0.0` |
| « cible tenue pour constante » | le **semi** de semi-gradient | `torch.no_grad()` **et** `.detach()` |
| \(y_i\), \(U_t\) | la cible de la mise à jour | `cibles` |
| \(\mathcal{L}(\theta)\) | la perte, moyenne sur le lot | `nn.MSELoss()(...)` |
| \(\delta_t\) | l'erreur TD | implicite dans `MSELoss` |
| \(\theta\), \(\mathbf{w}\) | les poids appris | `reseau.parameters()` |
| \(\theta^-\) | la copie figée | `reseau_cible.state_dict()` |
| \(\alpha\) | pas d'apprentissage | `LEARNING_RATE = 1e-4`, dans Adam |
| \(\gamma\) | facteur d'actualisation | `gamma = 0.99` |
| \(\lvert B\rvert\) | taille du lot | `BATCH_SIZE = 32` |
| \(\mathcal{D}\) | tampon de rejeu | `TamponDeRejeu`, `REPLAY_SIZE = 10_000` |
| \(N\) | période de synchronisation de \(\theta^-\) | `SYNC_RESEAU_CIBLE = 1_000` |
| \(\varepsilon\) | taux d'exploration | `epsilon(k)` |
| \(k\) | trames empilées | `EnveloppeEmpilementTrames(env, k=4)` |
| \(K\) | trames sautées | l'enveloppe de saut de trames |
| \(\mu(s)\) | distribution sur politique | **absente** : c'est ce que le tirage dans \(\mathcal{D}\) détruit |
| \(\rho_t\) | rapport d'échantillonnage préférentiel | **absent**, et délibérément |

Reprenons les trois lignes commentées, parce que chacune cache un piège.

**Le prélèvement.** Le réseau produit une valeur par action, soit un tenseur de forme `(lot, n_actions)`. Or la perte ne concerne qu'une seule action par transition : celle que l'agent a réellement jouée. `gather` fait exactement ce prélèvement, ligne par ligne, selon la dimension 1 qui est la dimension des actions. Le `unsqueeze(-1)` puis le `squeeze(-1)` ne sont là que pour accorder les formes. Et le point qui compte : `gather` est une opération **différentiable**, qui conserve tous les gradients par rapport à la valeur finale de la perte. Le prélèvement n'est donc pas une sortie du graphe de calcul, c'est une opération du graphe.

{{% comment %}}SOURCE: LAPAN ch.6 p.190-191{{% /comment %}}

**Le masque terminal.** Si la transition du lot provient du dernier pas d'un épisode, la valeur de l'action ne comporte aucune récompense actualisée pour l'état suivant, puisqu'il n'y a pas d'état suivant. Cela peut sembler mineur et cela ne l'est pas du tout : sans cette ligne, l'entraînement ne converge pas. C'est la même règle que la semaine 4 énonçait en une phrase, que la section 5.4 écrivait \(\hat v(\text{terminal},\cdot) = 0\) et que la section 5.5 isolait dans un cas terminal. Quatre écritures, un seul fait, et une ligne de code qui ne lève aucune exception quand elle manque.

{{% comment %}}SOURCE: LAPAN ch.6 p.191{{% /comment %}}

**Le détachement.** Rien de nouveau depuis la section 5.4, et c'est précisément pour cela que je l'y avais placé : au moment d'écrire le code, cette ligne devait être une évidence et non une surprise. Notez tout de même une différence par rapport au fragment de la section 5.4 : ici le passage avant est fait par le **réseau cible**, qui n'est de toute façon pas optimisé. Le détachement reste nécessaire, parce que rien dans PyTorch n'empêche un gradient de remonter dans les poids d'un réseau au prétexte qu'il s'appelle « cible ».

{{% comment %}}SOURCE: LAPAN ch.6 p.192{{% /comment %}}

Une dernière mesure, parce qu'elle justifie l'écriture vectorielle de ce fragment : la perte calculée sur un lot entier, comme ci-dessus, est plus de deux fois plus rapide que la même perte calculée par une boucle explicite sur les transitions. Écrire des boucles Python dans une fonction appelée des centaines de fois par seconde est le moyen le plus simple de rendre un entraînement correct inutilisable.

{{% comment %}}SOURCE: LAPAN ch.6 p.189{{% /comment %}}

---

## Les hyperparamètres, et l'avertissement qui va avec

| Hyperparamètre | Valeur | Rôle |
| --- | --- | --- |
| `GAMMA` | 0,99 | le facteur d'actualisation \(\gamma\) |
| `BATCH_SIZE` | 32 | la taille du lot \(\lvert B\rvert\) |
| `REPLAY_SIZE` | 10 000 | la capacité du tampon \(\mathcal{D}\) |
| `REPLAY_START_SIZE` | 10 000 | transitions à accumuler **avant le premier pas d'apprentissage** |
| `LEARNING_RATE` | \(10^{-4}\) | le pas d'apprentissage \(\alpha\), avec Adam |
| `SYNC_TARGET_FRAMES` | 1 000 | la période \(N\) de recopie de \(\theta\) dans \(\theta^-\) |
| `EPSILON_START` / `EPSILON_FINAL` | 1,0 / 0,01 | les bornes du calendrier de \(\varepsilon\) |
| `EPSILON_DECAY_LAST_FRAME` | 150 000 | la durée de la décroissance linéaire |
| `MEAN_REWARD_BOUND` | 19 | le seuil d'arrêt sur la moyenne des 100 derniers épisodes |

{{% comment %}}SOURCE: LAPAN ch.6 p.185-186{{% /comment %}}

> [!WARNING]
 **Attention, ces neuf nombres ne sont pas des constantes de la méthode, ce sont les réglages d'une expérience.** Les valeurs d'origine étaient tout autres sur deux points au moins : un tampon de rejeu d'**un million** de transitions, soit environ 20 Go de mémoire vive, et une décroissance de \(\varepsilon\) étalée sur un million de trames. Les valeurs du tableau ci-dessus sont cent fois plus modestes, et c'est ce qui rend l'expérience reproductible sur une machine ordinaire. Le prix est connu et il faut l'accepter : cette accélération suppose un réglage fin pour un environnement particulier, et elle peut casser la convergence sur d'autres jeux. Quand vous changerez d'environnement au laboratoire, attendez-vous à devoir rejouer ces neuf nombres, et commencez par la taille du tampon et par la période de synchronisation.

{{% comment %}}SOURCE: LAPAN ch.6 p.185-186{{% /comment %}}

> [!TIP]
 **Une variante de la perte, qui tient en une ligne et qu'il faut connaître : la perte de Huber.** Regardez la dernière ligne du fragment ci-dessus : l'implémentation que nous venons d'écrire minimise l'**erreur quadratique**. Cela a une conséquence qu'il faut voir. Une erreur quadratique pèse une grande erreur TD **quadratiquement** : une transition dont l'erreur vaut 10 contribue cent fois plus qu'une transition dont l'erreur vaut 1, et une seule transition aberrante peut donc dominer tout un lot de trente-deux. La **perte de Huber** corrige cela en restant quadratique près de zéro et en devenant **linéaire** au-delà d'un seuil \(\delta\), ce qui borne l'amplitude du gradient qu'une transition peut produire.
>
> $$L_\delta(x) = \begin{cases} \tfrac12 x^2 & \text{si } \lvert x \rvert \le \delta, \\[4pt] \delta\big(\lvert x \rvert - \tfrac12\delta\big) & \text{sinon.} \end{cases}$$
>
> C'est une pratique courante dans les implémentations de réseaux Q profonds, et le changement coûte exactement une ligne : `nn.MSELoss()` devient `nn.SmoothL1Loss()`. Je vous demande deux choses. Que vous sachiez dire **pourquoi** on le fait, c'est-à-dire la phrase sur l'amplitude du gradient. Et que vous le **mesuriez** plutôt que de me croire : c'est le volet D du laboratoire.

{{% comment %}}SOURCE: LAPAN ch.6 p.192{{% /comment %}}

---
