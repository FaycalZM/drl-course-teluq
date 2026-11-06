---
title: "11.3 Trois familles, et où chacune injecte sa pression"
weight: 4
---

## Trois points d'attache, et une image qui les sépare

Nous savons maintenant ce qu'il faut réparer : il faut que l'agent puisse porter une intention sur plusieurs pas, et il faut que quelque chose, dans l'agent, le pousse vers ce qu'il n'a pas encore vu. Trois familles de méthodes répondent à cela, et je vous les donne d'emblée avec leur **point d'attache**, c'est-à-dire l'endroit de la boucle où chacune agit.

La première met du **hasard dans la politique**, mais pas dans l'action : le bruit est placé sur les **poids** du réseau. Ce sont les **réseaux bruités** de la semaine 6, et vous allez les relire autrement.

La deuxième calcule une **prime d'exploration** (*exploration bonus*) à partir d'un **comptage de visites** : les états peu vus valent plus que les états souvent vus. On parle de **méthodes fondées sur le comptage** (*count-based methods*).

La troisième calcule une prime à partir d'une **erreur de prédiction** : ce que l'agent ne sait pas prévoir est, par définition, ce qu'il n'a pas assez vu. On parle de **méthodes fondées sur la prédiction** (*prediction-based methods*).

{{% comment %}}SOURCE: LAPAN ch.18 p.553{{% /comment %}}

La **Figure 11-2** place les trois sur une même boucle agent-environnement, et je vous demande de l'étudier maintenant, parce qu'elle prévient la confusion la plus coûteuse de la semaine.

{{< bookfig src="11-02.png" week="11" >}}

La confusion en question est celle des deux familles de prime. Dans une perte, elles sont **indiscernables** : les deux ajoutent un nombre positif à la récompense, les deux font donc grimper la cible, et le code de la mise à jour est identique au caractère près. Elles diffèrent entièrement par la **quantité** qu'elles lisent. L'une consulte un compteur de ce que l'agent a déjà vu, c'est-à-dire une mémoire explicite du passé. L'autre consulte l'erreur d'un prédicteur sur l'observation **courante**, c'est-à-dire une mémoire implicite, logée dans les poids d'un réseau. C'est pour cette raison que la figure les sépare par leur point d'attache et non par leur effet.

> [!NOTE]
 **Ces trois familles ne sont pas la liste complète, et je ne vous la présente pas comme telle.** C'est un relevé du paysage : les trois idées sur lesquelles reposent la plupart des méthodes d'exploration dirigée que vous rencontrerez, et les trois que je peux vous enseigner avec du code à l'appui. L'exploration est un sujet beaucoup plus vaste, et de nombreuses méthodes intéressantes ne sont traitées ni cette semaine ni ailleurs dans ce cours. Je reviens là-dessus à la fin de la section 11.7, où je nomme précisément ce qui manque.

{{% comment %}}SOURCE: LAPAN ch.18 p.553, p.570{{% /comment %}}

---

## Les réseaux bruités, relus comme une exploration dirigée

Première famille, et vous la connaissez déjà : la semaine 6 lui a consacré sa section 6.9. Le bruit est placé sur les **poids** des couches linéaires, son amplitude est un **paramètre entraînable** que la rétropropagation règle en même temps que le reste, et le bruit lui-même est tiré par un procédé factorisé qui remplace un million et demi de tirages par quelques milliers. Je ne réécris ni la couche, ni l'équation du poids bruité, ni le bruit gaussien factorisé : tout cela est sur la page de la semaine 6, avec sa classe `CoucheBruitee`, et le relire là est un meilleur usage de votre temps que de me lire le répéter ici.

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.9{{% /comment %}}

Ce qui est **nouveau** cette semaine est une lecture, et elle tient en deux propriétés.

Première propriété : le bruit est sur les **poids**, donc il ne modifie pas une action, il modifie la **fonction** qui choisit les actions. Un réseau dont les poids sont perturbés est un autre réseau, c'est-à-dire une autre politique, cohérente avec elle-même sur tout l'espace d'états.

Seconde propriété, et c'est celle qui justifie que les réseaux bruités apparaissent dans une semaine consacrée à l'exploration : le bruit n'est **pas retiré à chaque pas**. Il est retiré de temps en temps. Entre deux tirages, l'agent joue donc une politique fixe, prélevée dans un **ensemble** de politiques voisines, et il la joue du début à la fin de la portion de trajectoire concernée. Nos échantillons d'entraînement ne sont donc pas produits par la politique courante, mais par cet ensemble.

Mettez les deux ensemble et vous obtenez ce qui manquait à la section 11.1 : la **cohérence**. Là où l'\(\varepsilon\)-glouton retire sa décision à chaque pas, un réseau bruité collecte une trajectoire entière avec une politique unique, tirée au sort une fois. Le nageur choisit sa direction une fois et nage. C'est en ce sens précis que cette exploration est **dirigée**, et c'est la seule raison pour laquelle je reparle cette semaine d'une méthode déjà enseignée.

{{% comment %}}SOURCE: LAPAN ch.18 p.553-554 (image){{% /comment %}}

> [!WARNING]
 **Une mise en garde que la semaine 6 vous a déjà donnée et que je répète, parce que le mot « dirigée » peut la faire oublier.** Un réseau bruité ne **décide pas** où il a besoin d'explorer davantage. Il n'y a dans cette méthode aucune notion de nouveauté, aucun compteur de visites, aucune curiosité : ce qui est appris, c'est une **amplitude de bruit par poids**, pas une cible d'exploration. « Dirigée » veut ici dire **cohérente sur la durée**, et rien de plus. Les deux familles suivantes, elles, ciblent réellement la nouveauté, et c'est un autre ordre de complexité.

{{% comment %}}SOURCE: source-assets/raw-content/week-06.md §6.9{{% /comment %}}

Une dernière remarque, et c'est une direction que ce cours **ne suivra pas**. Il existe, à côté des réseaux bruités, une autre façon de placer du bruit sur les paramètres d'une politique, connue sous le nom de **bruit de paramètres** (*parameter noise*). Je la nomme pour que vous sachiez que cette famille ne se réduit pas aux réseaux bruités, et je m'arrête là : je ne vous donnerai pas une méthode que je ne peux pas vous faire écrire ligne à ligne, et celle-là n'est pas au programme de cette semaine. Une méthode nommée sans contenu est une case vide dans un plan de cours ; une méthode nommée **comme une lacune assumée** est au moins une information exacte.

---

## Compter les visites, et faire de la nouveauté une récompense

Deuxième famille, et son intuition se dit en une phrase : **visiter les états qui n'ont pas encore été explorés**. Tenons un compteur des états rencontrés, et préférons systématiquement ceux dont le compteur est bas.

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

Reste à transformer cette préférence en quelque chose que nos méthodes savent traiter. Nous n'avons qu'un seul levier qui fasse changer un comportement : la récompense. La nouveauté sera donc payée. L'agent reçoit une **récompense supplémentaire**, qui ne vient pas de l'environnement mais du **comptage de visites** de l'état où il se trouve, et c'est le couple de mots de l'introduction : la récompense de l'environnement est **extrinsèque**, celle que l'agent se fabrique est **intrinsèque**.

Voici la forme de cette prime :

$$
R^i_t \;=\; \frac{c}{\sqrt{\tilde N(S_t)}}
$$

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

Lisez-la lentement, parce que trois choses s'y décident. \(\tilde N(S_t)\) est le nombre de fois que l'agent a vu l'état \(S_t\), compté ou estimé. La **racine carrée** au dénominateur fait que la prime décroît quand le compteur monte, mais lentement : passer de une à quatre visites divise la prime par deux, pas par quatre. Et \(c\) fixe le poids de cette prime dans la récompense totale, c'est-à-dire le taux de change entre « être curieux » et « réussir la tâche ». Si \(c\) est trop petit, la prime ne change rien ; s'il est trop grand, l'agent devient un touriste qui visite sans jamais rien terminer.

> [!NOTE]
 **La forme de cette prime est posée, pas démontrée, et je vous dois la vérité sur ce point.** Le \(1/\sqrt{\tilde N}\) n'est pas un choix esthétique : cette forme vient de l'étude des **bandits manchots**, où l'on sait l'établir. **Ce cours ne l'établit pas.** Il n'a jamais enseigné les bornes de confiance, ni l'analyse du regret qui les accompagne, et je ne vais pas en improviser une version plausible : la formule est ici **posée**, avec son origine nommée, et vous devez la tenir pour une forme fonctionnelle commode plutôt que pour un résultat démontré dans ces pages. C'est la limite que j'avais annoncée dans l'introduction. La semaine 12 rencontrera une borne de confiance par un tout autre chemin, dans la règle de sélection d'un algorithme de planification, et vous pourrez alors rapprocher les deux.

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

Maintenant la question pratique, qui décide si la méthode est utilisable : **comment compte-t-on ?** Un compteur par état fonctionne quand les états sont peu nombreux et discrets, comme les six états de River Swim. Dès que l'observation est un vecteur de flottants, ou une image, chaque état n'est vu qu'une seule fois et tous les compteurs valent 1 : le comptage ne dit plus rien. Il faut alors **transformer l'état** avant de le compter, par une fonction de hachage ou par un plongement, de façon que des états voisins tombent dans la même case.

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

La version la plus simple de cette transformation, et celle que la section 11.6 mesurera, consiste à **arrondir** chaque composante de l'observation à trois décimales, puis à utiliser le tuple obtenu comme clé d'un dictionnaire. C'est le **hachage des états** (*state hashing*) dans sa forme la plus brutale, et il suffit à faire fonctionner la méthode sur une tâche à deux observations continues.

```python
import gymnasium as gym
import numpy as np
from collections import Counter


class PrimeDeComptage(gym.Wrapper):
    """Ajoute c / sqrt(N(h(s))) a la recompense de l'environnement.

    ATTENTION : cette enveloppe modifie le PROBLEME, et non seulement
    l'exploration. La section 11.4 dit ce que cela implique.
    """

    def __init__(self, env, c: float = 1.0, decimales: int = 3):
        super().__init__(env)
        self.c = c
        self.decimales = decimales
        self.compteur = Counter()

    def _hacher(self, obs) -> tuple:
        """h(s) : chaque flottant arrondi, puis un tuple utilisable comme cle."""
        plat = np.asarray(obs, dtype=np.float64).ravel()
        return tuple(round(float(v), self.decimales) for v in plat)

    def step(self, action):
        obs, recompense, termine, tronque, info = self.env.step(action)
        h = self._hacher(obs)
        self.compteur[h] += 1
        # C'est exactement R^i_t, coefficient c COMPRIS. Il n'apparait qu'ici.
        prime = self.c / np.sqrt(self.compteur[h])
        info["recompense_extrinseque"] = recompense      # on garde la trace
        info["prime"] = prime
        return obs, recompense + prime, termine, tronque, info
```

{{% comment %}}SOURCE: LAPAN ch.18 p.559-560{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(R^e_t\) | récompense extrinsèque, celle de l'environnement | `recompense` |
| \(R^i_t\) | récompense intrinsèque, coefficient compris | `prime` |
| \(c\) | poids de la prime, **ni \(\alpha\) ni \(\beta\)** | `self.c` |
| \(\tilde N(s)\) | comptage de visites de l'état haché | `self.compteur[h]` |
| \(h(s)\) | hachage de l'observation, arrondi à trois décimales | `self._hacher(obs)` |
| \(R^e_t + R^i_t\) | ce que l'agent reçoit réellement | deuxième valeur renvoyée par `step` |

Deux remarques sur ce fragment, et la seconde est importante.

Premièrement, le coefficient \(c\) n'apparaît **qu'une fois**, et c'est une discipline à tenir. Ce cours l'écrit **à l'intérieur** de la prime, comme dans l'équation ci-dessus et comme dans le code. Vous verrez ailleurs la prime écrite sans son coefficient, celui-ci étant alors appliqué au moment de la somme : les deux conventions décrivent la même quantité, et la seule erreur possible est d'appliquer \(c\) **deux fois**, ce qui arrive en pratique quand une enveloppe pondère déjà et qu'un hyperparamètre de la boucle pondère encore.

Deuxièmement, remarquez les deux lignes qui écrivent dans `info`. Elles ne changent rien au comportement de l'agent, et elles vous sauveront une soirée : elles conservent séparément la récompense de l'environnement et la prime, ce qui est la seule façon de tracer une courbe d'entraînement lisible. La section 11.4 explique pourquoi ce n'est pas un luxe.

---

## Le pseudo-comptage, que je vous donne comme une esquisse

Le hachage répare le comptage dans les cas faciles. Il ne le répare pas dans les cas difficiles : sur des images, deux observations voisines n'ont aucune raison de tomber dans la même case, et l'on retombe sur des compteurs qui valent tous 1.

L'idée du **pseudo-comptage** (*pseudo-count*) est de remplacer le compteur par une estimation issue d'un **modèle de densité**. Si l'on dispose d'un modèle qui attribue à chaque état une vraisemblance, alors un état très vraisemblable est un état que l'agent a beaucoup vu, et un état très improbable est un état nouveau, **même si son compteur exact vaut zéro**. Le comptage devient alors :

$$
\tilde N(s) \;\approx\; \rho(s)\,n
$$

où \(\rho(s)\) est la vraisemblance que le modèle de densité, en pratique un réseau de neurones, attribue à l'état \(s\), et où \(n\) est le nombre total d'états vus jusqu'ici.

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

> [!WARNING]
 **Je vous présente cette formule comme une esquisse, et je veux que vous la reteniez comme telle.** L'idée est juste et elle est utile : une densité apprise permet de compter là où aucun compteur ne fonctionne. Mais ce que je viens d'écrire n'est pas la construction complète du pseudo-comptage, qui demande davantage que la vraisemblance d'un état et un nombre total de visites. **Cette construction est hors de portée de cette semaine**, et je préfère vous le dire que de maquiller une intuition en dérivation. Retenez donc : le comptage exact ne passe pas à l'échelle, un modèle de densité permet de l'estimer, et le détail de cette estimation est hors de portée de cette semaine. Rien dans le laboratoire n'en dépend.

Une variante extrême de cette famille mérite d'être nommée, parce qu'elle est l'aboutissement logique de l'idée de prime. Dans l'**exploration par curiosité** (*curiosity-driven exploration*), la récompense de l'environnement est **ignorée entièrement** : l'entraînement et l'exploration sont dirigés à cent pour cent par la nouveauté de l'expérience de l'agent. Cela paraît absurde, et ce ne l'est pas : une telle méthode peut être efficace non seulement pour découvrir des états, mais aussi pour apprendre de bonnes politiques. Je la nomme ici et je n'y entre pas, parce que la construire demande un objet que le cours n'a pas encore, un **modèle de la dynamique** de l'environnement. C'est le sujet de la semaine 13.

{{% comment %}}SOURCE: LAPAN ch.18 p.554 (image){{% /comment %}}

---

## Prédire pour mesurer la surprise : la distillation de réseau aléatoire

Troisième famille, et son intuition est la plus élégante de la semaine.

Si l'agent sait **prédire** correctement ce qui va se passer, c'est qu'il a déjà vécu cette situation un nombre suffisant de fois, et elle ne mérite pas qu'on l'explore davantage. Si au contraire quelque chose d'inhabituel se produit et que sa prédiction se révèle très fausse, c'est peut-être qu'il faut porter attention à l'état où il se trouve. L'erreur de prédiction devient donc la mesure de la nouveauté, et elle se calcule sans aucun compteur et sans aucune mémoire explicite du passé.

{{% comment %}}SOURCE: LAPAN ch.18 p.555 (image){{% /comment %}}

Reste une difficulté, et sa solution est le tour de force de la méthode. Prédire **quoi** ? Prédire l'état suivant demande un modèle de la dynamique, qui est coûteux et que nous n'avons pas. La **distillation de réseau aléatoire** (*random network distillation*) répond ainsi : faisons prédire la sortie d'un **autre réseau de neurones**, initialisé au hasard et jamais entraîné. On envoie la même observation dans les deux réseaux, l'un figé et l'autre entraîné à reproduire la sortie du premier, et l'erreur entre les deux sorties mesure la nouveauté de l'observation.

{{% comment %}}SOURCE: LAPAN ch.18 p.555 (image){{% /comment %}}

Prenez le temps de voir pourquoi cela fonctionne. Le réseau figé calcule une fonction arbitraire mais **fixe** et **déterministe** de l'observation. Le réseau entraîné apprend cette fonction par descente de gradient, donc il l'apprend **là où on lui montre des exemples**, c'est-à-dire là où l'agent est déjà passé. Sur une observation familière, les deux sorties coïncident presque. Sur une observation que l'agent n'a jamais visitée, le réseau entraîné n'a rien appris et son erreur est grande. Aucune des deux fonctions n'a le moindre sens en soi ; c'est leur **écart** qui porte l'information, et cet écart est une mesure de couverture de l'espace d'observations.

Voici l'équation, dans la notation du cours :

$$
R^i_t \;=\; \big\lVert\, \hat f_\psi(S_t) - f(S_t) \,\big\rVert^2
$$

{{% comment %}}SOURCE: LAPAN ch.18 p.555 (image){{% /comment %}}

\(f\) est le réseau de **référence**, figé, aux poids tirés au hasard à l'initialisation et jamais modifiés. \(\hat f_\psi\) est le **prédicteur**, de paramètres \(\psi\), entraîné à reproduire \(f\) sur les observations rencontrées. J'écris \(\psi\) et non \(\theta\) ni \(\mathbf{w}\) : ce prédicteur n'est ni une politique ni un critique, c'est un troisième réseau avec sa propre perte, et le mélanger avec les deux autres est une erreur de lecture coûteuse.

> [!TIP]
 **Un point de rigueur sur lequel je dois être explicite, parce que les deux formes circulent.** Ce cours écrit la prime comme une **erreur quadratique**, c'est la forme de l'équation ci-dessus, et c'est elle que j'emploierai partout dans cette semaine et dans le laboratoire. Vous rencontrerez aussi la **différence absolue** entre les deux sorties : c'est ce que font plusieurs mises en œuvre, y compris celle dont la section 11.6 rapporte les mesures, qui calcule la prime en valeur absolue tout en entraînant le prédicteur avec une erreur quadratique moyenne. Les deux choix sont défendables et ils ne sont pas équivalents : la différence absolue écrase les grandes surprises et change donc l'échelle utile de \(c\). Si vous changez de forme, **réglez \(c\) à nouveau**, et dites dans votre rapport laquelle vous utilisez.

{{% comment %}}SOURCE: LAPAN ch.18 p.555, p.565, p.566 (images){{% /comment %}}

Le code tient en une quinzaine de lignes, et deux détails y font tout le travail.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


def reseau_reference(taille_obs: int, cachee: int = 128) -> nn.Module:
    """f : TROIS couches, poids aleatoires, FIGE pour toujours."""
    net = nn.Sequential(
        nn.Linear(taille_obs, cachee), nn.ReLU(),
        nn.Linear(cachee, cachee), nn.ReLU(),
        nn.Linear(cachee, 1),
    )
    net.train(False)                 # pas de mode entrainement
    net.requires_grad_(False)        # DETAIL 1 : aucun gradient, jamais
    return net


def reseau_predicteur(taille_obs: int) -> nn.Module:
    """f_psi : UNE seule couche, volontairement plus faible que la reference."""
    return nn.Linear(taille_obs, 1)  # DETAIL 2 : capacite limitee


def prime_et_perte(obs_t, ref_net, pred_net):
    """Renvoie la prime intrinseque (detachee) et la perte du predicteur."""
    with torch.no_grad():
        cible = ref_net(obs_t)                       # f(S_t)
    predit = pred_net(obs_t)                         # f_psi(S_t)
    prime = (predit - cible).pow(2).detach()         # R^i_t : erreur quadratique
    perte = F.mse_loss(predit, cible)                # la perte du predicteur
    return prime, perte
```

{{% comment %}}SOURCE: LAPAN ch.18 p.565-566 (images){{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(f\) | réseau de référence, aléatoire et figé | `ref_net`, `requires_grad_(False)` |
| \(\hat f_\psi\) | prédicteur entraîné | `pred_net` |
| \(\psi\) | paramètres du prédicteur, distincts de \(\theta\) et de \(\mathbf{w}\) | `pred_net.parameters()` |
| \(S_t\) | observation courante, envoyée dans les **deux** réseaux | `obs_t` |
| \(R^i_t\) | prime intrinsèque, **détachée** du graphe | `prime` |
| perte de \(\psi\) | erreur quadratique moyenne entre les deux sorties | `perte` |

Les deux détails commentés dans le code valent une explication, parce qu'ils ne sont pas des précautions de style.

**Le réseau de référence ne reçoit jamais de gradient.** S'il en recevait, il apprendrait à être prévisible, les deux réseaux convergeraient l'un vers l'autre et la prime s'effondrerait vers zéro partout, y compris dans les états jamais visités. Le `requires_grad_(False)` n'est pas une optimisation, c'est la condition de fonctionnement de la méthode.

**Le prédicteur est volontairement plus faible que la référence.** Trois couches d'un côté, **une seule** de l'autre : ce déséquilibre est un choix mesuré, et il évite le surapprentissage du prédicteur quand l'espace d'observations est petit. Un prédicteur trop puissant apprend la fonction aléatoire **partout**, y compris par interpolation dans des régions qu'il n'a jamais visitées, et la prime cesse de distinguer le connu de l'inconnu. Retenez le principe : la capacité du prédicteur est un bouton d'exploration déguisé.

{{% comment %}}SOURCE: LAPAN ch.18 p.565-566 (images){{% /comment %}}

---
