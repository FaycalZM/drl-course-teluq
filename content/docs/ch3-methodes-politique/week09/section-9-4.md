---
title: "9.4 L'exploration remise à la main"
weight: 5
---

## Une politique déterministe n'explore rien

S'il ne devait rester qu'une phrase de cette semaine dans votre mémoire, je voudrais que ce soit celle-ci, et je l'écris sans précaution : **une politique déterministe n'explore rien**.

Pas « explore peu ». Pas « explore mal ». Rien. Un acteur déterministe est une fonction : pour un état donné, il renvoie une action, toujours la même. Si cette action est mauvaise, il la rejouera à chaque passage dans cet état, indéfiniment, et il ne découvrira jamais qu'une autre action valait mieux, parce qu'il ne l'essaiera jamais. Au début de l'entraînement, c'est encore plus net : un réseau initialisé au hasard renvoie des sorties quasi identiques pour des états différents, de sorte que l'agent, laissé à lui-même, jouerait à peu près la même action partout et remplirait son tampon de rejeu de transitions qui n'enseignent rien.

{{% comment %}}SOURCE: LAPAN ch.15 p.475 ; SPINUP ddpg/exploration{{% /comment %}}

C'est le prix de tout ce que la section 9.3 a gagné, et il faut le payer explicitement : il faut **ajouter du bruit** aux actions que l'acteur renvoie, avant de les transmettre à l'environnement.

> [!IMPORTANT]
 **Le bruit n'est pas un détail d'implémentation : il remplace \(\varepsilon\), et il change de lieu.** Depuis la semaine 4, l'exploration vivait dans le **choix** : avec probabilité \(\varepsilon\), on ignorait le classement et on prenait une action au hasard dans la liste. Cette mécanique suppose une liste, et elle suppose un choix. Ici, il n'y a ni liste ni choix : il n'y a qu'un vecteur de réels. Le seul endroit où l'on puisse mettre du hasard, c'est **dans l'action elle-même**. L'exploration déménage du choix vers l'espace d'actions, et c'est la raison pour laquelle cette section existe comme une section à part entière et non comme un paragraphe d'implémentation.

Ce déplacement a des conséquences que vous devez pouvoir énoncer. Avec \(\varepsilon\), l'exploration était **discrète et brutale** : soit on suit la politique, soit on tire complètement au hasard. Avec du bruit additif, elle est **continue et locale** : on joue toujours à proximité de ce que la politique propose, et le réglage de l'amplitude décide de la taille du voisinage visité. Le réglage d'une amplitude est d'ailleurs plus délicat que celui d'un \(\varepsilon\), parce qu'il est **dimensionné** : un bruit d'écart-type 0,1 est une grosse perturbation pour une commande bornée à \([-1,1]\) et une perturbation négligeable pour une commande bornée à \([-100,100]\). D'où un conseil de méthode : normalisez vos actions, ou exprimez toujours l'amplitude du bruit en fraction de l'étendue de l'espace d'actions.

---

## Le bruit le plus simple, et c'est le bon par défaut

La forme la plus simple s'écrit en une ligne : on ajoute à l'action proposée un bruit gaussien centré, mis à l'échelle par un coefficient \(\epsilon\).

$$
a = \mu_\theta(s) + \epsilon\,\mathcal{N}
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.475{{% /comment %}}

Ici \(\mathcal{N}\) désigne un tirage normal centré réduit, un par dimension d'action, et \(\epsilon\) est l'amplitude du bruit, qui est ce que vous réglez. Je souligne une collision de symbole, parce que celle-ci se paie cher : ce \(\epsilon\) **n'est pas** le \(\varepsilon\) de la semaine 5. Ce n'est pas une probabilité, cela ne vit pas dans \([0,1]\), et cela ne décroît pas forcément. C'est une échelle dans l'unité de l'action. Le cours écrit \(\varepsilon\) pour le taux d'exploration \(\varepsilon\)-glouton et \(\epsilon\) pour l'amplitude du bruit, et vous verrez ces deux lettres se côtoyer ailleurs sans que personne ne prenne la peine de les distinguer.

Trois lignes de code, et l'écrêtage de l'action à la fin :

```python
def agir_avec_bruit(acteur, obs, amplitude: float, env, device):
    """Action deterministe + bruit gaussien non correle, puis ecretage de l'action."""
    obs_t = torch.as_tensor(np.asarray([obs]), dtype=torch.float32, device=device)
    with torch.no_grad():
        action = acteur(obs_t).cpu().numpy()[0]

    action = action + amplitude * np.random.normal(size=action.shape)
    return np.clip(action, env.action_space.low, env.action_space.high)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | action proposée par l'acteur | `acteur(obs_t)` |
| \(\epsilon\) | amplitude du bruit d'exploration | `amplitude` |
| \(\mathcal{N}\) | tirage normal centré réduit, un par dimension | `np.random.normal(size=...)` |
| \(\operatorname{clip}(\cdot, a_{\min}, a_{\max})\) | écrêtage de l'action aux bornes de l'environnement | `np.clip(..., low, high)` |

C'est ce que le cours appelle l'**exploration par bruit ajouté à l'action** (*exploration noise*), et c'est ce que le laboratoire emploiera. Mais la tradition de ce domaine en propose autre chose, et il faut savoir ce que c'est.

---

## Le processus d'Ornstein-Uhlenbeck, et ce qu'il coûte

L'implémentation historique de DDPG n'utilise pas un bruit indépendant d'un pas sur l'autre : elle utilise un bruit **corrélé en temps**, produit par un **processus d'Ornstein-Uhlenbeck** (*Ornstein-Uhlenbeck process*).

L'intuition physique est jolie, et elle explique pourquoi on y a pensé. Ce processus modélise la vitesse d'une particule brownienne massive soumise à un frottement : à chaque instant, la vitesse est rappelée vers une valeur moyenne par le frottement, et bousculée par un choc aléatoire. Il en résulte une trajectoire qui **dérive** : les valeurs successives se ressemblent, et le bruit pousse dans la même direction pendant plusieurs pas avant de changer d'avis. Transposé à un robot, l'argument est physiquement séduisant : un bruit indépendant à chaque pas se compense en moyenne et ne déplace donc le corps nulle part, alors qu'un bruit dérivant fait réellement explorer des **mouvements**, et non des tremblements.

{{% comment %}}SOURCE: LAPAN ch.15 p.475{{% /comment %}}

Voici le processus, dans sa forme continue, puis dans la forme discrète qu'on implémente :

$$
\partial x_t = \kappa\,(\bar x - x_t)\,\partial t + \sigma_{\mathrm{OU}}\,\partial W
$$

$$
x_{t+1} = x_t + \kappa\,(\bar x - x_t) + \sigma_{\mathrm{OU}}\,\mathcal{N}
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.475 ; code p.479{{% /comment %}}

**J'ai renommé les trois paramètres, et je vous dois la raison.** L'écriture usuelle de ce processus emploie \(\theta\) pour le taux de rappel, \(\mu\) pour la valeur moyenne et \(\sigma\) pour l'échelle du choc. Dans cette semaine, \(\theta\) désigne les paramètres de l'acteur, \(\mu_\theta\) l'acteur lui-même et \(\sigma_\theta\) l'écart-type d'une politique gaussienne : les trois lettres sont déjà prises, et les garder produirait des phrases où \(\theta\) apparaîtrait deux fois avec deux sens à trois lignes d'intervalle. J'écris donc \(\kappa\) pour le **taux de rappel vers la moyenne**, \(\bar x\) pour la **valeur moyenne** du processus et \(\sigma_{\mathrm{OU}}\) pour l'**échelle du choc**. Les trois réglages hérités de l'implémentation historique sont \(\bar x = 0\), \(\kappa = 0{,}15\) et \(\sigma_{\mathrm{OU}} = 0{,}2\), avec une amplitude globale \(\epsilon = 1{,}0\).

{{% comment %}}SOURCE: LAPAN ch.15 p.475, p.478{{% /comment %}}

Lisez la forme discrète comme une somme de deux forces. Le terme \(\kappa(\bar x - x_t)\) est un **rappel** : si le bruit a dérivé loin de zéro, il le ramène, d'autant plus fort qu'il est loin. Le terme \(\sigma_{\mathrm{OU}}\mathcal{N}\) est le **choc**, indépendant à chaque pas. Avec \(\kappa = 0{,}15\), le rappel est faible : il faut une dizaine de pas pour effacer la moitié d'un écart, et c'est très exactement cela, la corrélation temporelle.

```python
class BruitOU:
    """Bruit d'Ornstein-Uhlenbeck : il PORTE UN ETAT entre deux pas."""

    def __init__(self, forme, kappa=0.15, moyenne=0.0, sigma=0.2):
        self.forme, self.kappa, self.moyenne, self.sigma = forme, kappa, moyenne, sigma
        self.x = None
        self.reinitialiser()

    def reinitialiser(self) -> None:
        # A APPELER AU DEBUT DE CHAQUE EPISODE, sinon le bruit d'un episode
        # continue dans le suivant.
        self.x = np.zeros(self.forme, dtype=np.float32)

    def tirer(self) -> np.ndarray:
        choc = self.sigma * np.random.normal(size=self.forme)
        self.x = self.x + self.kappa * (self.moyenne - self.x) + choc
        return self.x
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(x_t\) | valeur courante du bruit, **conservée** entre les pas | `self.x` |
| \(\kappa\) | taux de rappel vers la moyenne | `self.kappa` |
| \(\bar x\) | valeur moyenne du processus, 0 ici | `self.moyenne` |
| \(\sigma_{\mathrm{OU}}\) | échelle du choc aléatoire | `self.sigma` |
| \(\mathcal{N}\) | tirage normal centré réduit | `np.random.normal` |
| \(\epsilon\) | amplitude globale appliquée à \(x_t\) | multipliée à l'appel |

Et voici le coût, qui est un coût d'architecture et non de calcul. Ce bruit **porte un état**. La valeur \(x_t\) doit persister d'un pas au suivant, donc l'agent cesse d'être une fonction pure de l'observation : il devient un objet avec une mémoire, qu'il faut initialiser au début de chaque épisode, dimensionner à la taille de l'espace d'actions, et **dupliquer** si plusieurs environnements tournent en parallèle, puisque chacun a son propre bruit en cours. Une bibliothèque haut niveau comme celle de la semaine 6 prévoit exactement cela, avec une notion d'état initial d'agent, et c'est la même machinerie que réclame un environnement partiellement observable, où l'agent doit se souvenir de ce qu'il a vu. Au passage, une astuce d'implémentation élégante : renvoyer `None` comme état initial permet de ne dimensionner le vecteur de bruit qu'au premier appel, quand la taille de l'action est enfin connue.

{{% comment %}}SOURCE: LAPAN ch.15 p.478-479{{% /comment %}}

---

## Trois raisons de préférer le bruit non corrélé, et une règle de méthode

Maintenant la partie importante, et je vais être très direct : **le bruit corrélé est une tradition, pas une nécessité**, et le laboratoire de cette semaine emploiera le bruit gaussien simple. Trois constats indépendants soutiennent cette position.

**Premier constat.** La recommandation historique d'un bruit corrélé en temps a été remise en cause par des résultats plus récents : un bruit gaussien centré **non corrélé** fonctionne tout aussi bien en pratique. Comme il est plus simple, c'est lui que les implémentations actuelles de cette famille prennent par défaut.

{{% comment %}}SOURCE: SPINUP ddpg/exploration{{% /comment %}}

**Deuxième constat.** La campagne de mesure de 2018 qui a produit les trois correctifs de la section 9.6 s'est écartée de l'implémentation historique sur ce point précis : elle a employé un bruit non corrélé, après avoir constaté que le processus corrélé n'apportait **aucun gain de performance** mesurable. Son bruit d'exploration est une loi normale centrée d'écart-type 0,1, ajoutée à chaque dimension d'action.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.1{{% /comment %}}

**Troisième constat**, et c'est le plus parlant pédagogiquement. La variante distributionnelle évoquée à la fin de la section 9.3, celle qui atteint 17,9 sur le robot, a été lancée avec les deux bruits, corrélé et non corrélé, et **le résultat a été le même** ; l'approche la plus simple a donc été conservée, avec une amplitude de 0,3. Autrement dit, la même lignée de méthodes a donné lieu à une implémentation complète du processus corrélé, puis, pour sa variante suivante, à son abandon mesuré.

{{% comment %}}SOURCE: LAPAN ch.15 p.484, p.486{{% /comment %}}

> [!IMPORTANT]
 **La règle de méthode, et elle vaut bien au-delà de cette semaine : la complexité se paie par une mesure.** Un processus d'Ornstein-Uhlenbeck, ce sont trois hyperparamètres de plus, un agent qui porte un état, une réinitialisation à ne pas oublier au début de chaque épisode, et une duplication par environnement parallèle. Tout cela est acceptable **si** cela achète quelque chose de mesurable. Les trois constats ci-dessus disent qu'ici, cela n'achète rien. Un étudiant qui implémente malgré tout le processus corrélé n'apprend pas une technique avancée : il apprend à ajouter de la complexité sans mesure, et c'est exactement l'habitude que ce cours cherche à défaire. Dans le laboratoire, le bruit par défaut est donc gaussien non corrélé, et la comparaison des deux bruits est proposée comme une **expérience** à une ligne, avec la réponse « aucune différence mesurable » pleinement admise comme résultat.

---

## Trois réglages qui ne sont pas des détails

Le bruit ne suffit pas tout à fait. Trois réglages l'accompagnent, et chacun répond à un problème précis.

**Premier réglage : une phase de démarrage purement aléatoire.** Pendant les premiers pas, on ignore complètement l'acteur et on tire les actions **uniformément** dans l'espace d'actions valide, puis on passe au régime normal, acteur plus bruit. La durée varie selon la tâche, et elle se règle : les implémentations en font un paramètre à part entière, et la campagne de mesure de 2018 a employé une politique purement exploratoire pendant les 1 000 premiers pas sur la plupart de ses tâches, et pendant les 10 000 premiers sur ses deux tâches à épisodes longs. La raison est celle du premier paragraphe de cette section : un acteur non entraîné propose presque la même action partout, et un tampon rempli de cette action unique ne contient aucune information sur la forme de la fonction de valeur. On commence donc par remplir le tampon avec quelque chose de varié, et seulement ensuite on commence à suivre l'acteur.

{{% comment %}}SOURCE: SPINUP ddpg/exploration ; arXiv:1802.09477 §6.1{{% /comment %}}

**Deuxième réglage : aucun bruit à l'évaluation.** C'est le pendant exact du \(\varepsilon = 0\) de test de la semaine 5, et il n'y a aucune exception à cette règle. Un score mesuré avec le bruit activé n'est pas le score de votre politique, c'est le score de votre politique perturbée, et il est systématiquement plus mauvais, d'une quantité qui dépend de votre réglage de bruit. Comparer deux configurations mesurées l'une avec bruit et l'autre sans est une erreur de protocole qui peut inverser une conclusion.

{{% comment %}}SOURCE: SPINUP ddpg/exploration ; LAPAN ch.15 p.469{{% /comment %}}

**Troisième réglage : l'amplitude peut décroître, ou pas.** On peut faire décroître l'amplitude du bruit au cours de l'entraînement, comme on faisait décroître \(\varepsilon\) en semaine 5. C'est intuitivement séduisant : beaucoup d'exploration au début, de la précision à la fin. Mais ce n'est pas obligatoire, et plusieurs implémentations très utilisées gardent l'amplitude **constante** du début à la fin. Je ne vous donne donc pas de recommandation, je vous donne une consigne de rigueur : décidez, écrivez votre décision dans votre rapport, et ne comparez jamais deux exécutions dont l'une décroît et l'autre pas.

{{% comment %}}SOURCE: SPINUP ddpg/exploration{{% /comment %}}

> [!TIP]
 **Le diagnostic d'exploration en une courbe.** Journalisez, à chaque pas, l'écart quadratique moyen entre l'action envoyée à l'environnement et l'action proposée par l'acteur. C'est l'amplitude **effective** de votre exploration, après écrêtage de l'action, et elle n'est pas égale à votre réglage : dès que l'acteur sature vers ses bornes, l'écrêtage de l'action rogne la moitié du bruit, et votre exploration réelle s'effondre silencieusement alors que votre paramètre est resté le même. Cette courbe vaut une après-midi de débogage, et elle coûte deux lignes.

---
