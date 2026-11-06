---
title: "9.2 La route facile : une politique gaussienne"
weight: 3
---

## Une seule chose change dans A2C

Commençons par la bonne nouvelle, et elle est plus grande qu'elle n'en a l'air : la méthode de la semaine 8 fonctionne déjà sur un espace continu, à **une** modification près.

Reprenez l'A2C que vous avez écrit. Le critique prédit un seul nombre, \(\hat v(s,\mathbf{w})\), et ce nombre ne dépend pas de la nature de l'espace d'actions : la tête de valeur est donc inchangée, strictement. Le calcul de l'avantage est inchangé. La cible à \(N\) pas est inchangée. Le tronc commun est inchangé. La seule chose qui soit touchée, c'est la **représentation de la politique**, c'est-à-dire la tête qui produisait une distribution sur un ensemble fini et qui doit maintenant produire une distribution sur \(\R^n\).

{{% comment %}}SOURCE: LAPAN ch.15 p.466{{% /comment %}}

Comment un réseau produit-il une distribution sur les réels ? Il y a une réponse naïve et une réponse utile. La réponse naïve : qu'il sorte directement l'action, un vecteur de \(n\) réels, et qu'on l'applique. C'est faisable, et c'est mauvais, pour une raison qui est presque entièrement une raison d'**exploration** : un réseau qui sort un seul point ne décrit aucune incertitude, et une politique qui ne décrit aucune incertitude ne tire pas au hasard, donc ne découvre rien. Nous reviendrons sur cette phrase en section 9.4, parce que la route déterministe de la section 9.3 est exactement ce choix naïf, assumé, avec la facture d'exploration payée séparément.

La réponse utile : que le réseau sorte les **paramètres** d'une loi de probabilité, et qu'on tire l'action dans cette loi. Pour \(n\) actions, la loi la plus simple est la loi normale, et le réseau produit donc deux vecteurs de taille \(n\) : un vecteur de moyennes \(\mu_\theta(s)\) et un vecteur de variances \(\sigma_\theta^2(s)\). L'action jouée est alors un vecteur de \(n\) variables normales **non corrélées**, chacune ayant sa propre moyenne et sa propre variance. C'est la **politique gaussienne** (*Gaussian policy*).

{{% comment %}}SOURCE: LAPAN ch.15 p.467{{% /comment %}}

> [!NOTE]
 **« Non corrélées » est une hypothèse, et il faut savoir ce qu'elle coûte.** Une loi normale multivariée générale porte une matrice de covariance complète, soit \(n(n+1)/2\) paramètres, et elle peut exprimer des énoncés du genre « quand je pousse le moteur avant gauche, je dois aussi pousser l'arrière droit ». En prenant les composantes indépendantes, nous réduisons cela à \(n\) variances et nous perdons la capacité d'exprimer une corrélation entre dimensions d'action. Pour huit moteurs d'un quadrupède, c'est une perte réelle. Elle est acceptée parce que \(n\) paramètres se prédisent et s'entraînent, alors qu'une matrice de covariance complète valide, c'est-à-dire définie positive, est autrement plus délicate à produire par un réseau. La coordination entre moteurs devra donc venir de la **moyenne**, qui est, elle, une fonction de l'état aussi riche qu'on veut.

---

## La loi normale comme politique, et ce qu'il faut en dériver

Voici la densité de la loi normale, sous la forme où nous l'utiliserons :

$$
f(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}}\; e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.467{{% /comment %}}

Mais ce n'est pas cette expression qui nous intéresse. La semaine 8 a montré que tout gradient de politique passe par \(\nabla_\theta \ln \pi_\theta(a \mid s)\), jamais par \(\pi_\theta\) elle-même. Il nous faut donc le **logarithme** de la densité, évalué en l'action jouée. Pour une dimension, en remplaçant la variable générique par l'action \(a\) et les paramètres par les sorties du réseau :

$$
\ln \pi_\theta(a \mid s) = -\frac{\left(a - \mu_\theta(s)\right)^2}{2\,\sigma_\theta^2(s)} \;-\; \ln\sqrt{2\pi\,\sigma_\theta^2(s)}
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.467 ; répété p.470{{% /comment %}}

Deux remarques, et elles ont chacune une conséquence de code. D'abord, le premier terme est un **écart quadratique normalisé** : il dit à quel point l'action jouée est loin de la moyenne prédite, en unités d'écart-type. Ensuite, le second terme ne dépend pas de l'action du tout : c'est le prix de normalisation de la loi, et il **pénalise** les grandes variances. C'est important pour comprendre le comportement de la méthode : à écart donné, le réseau peut augmenter la log-vraisemblance en réduisant \(\sigma_\theta\), ce qui resserre la politique, et c'est exactement par là que l'exploration s'éteint si rien ne la soutient.

Pour \(n\) dimensions indépendantes, les log-densités **s'additionnent**, parce que la densité conjointe est un produit :

$$
\ln \pi_\theta(a \mid s) = \sum_{i=1}^{n} \left[ -\frac{\left(a_i - \mu_{\theta,i}(s)\right)^2}{2\,\sigma_{\theta,i}^2(s)} - \ln\sqrt{2\pi\,\sigma_{\theta,i}^2(s)} \right]
$$

Ce qui soutient l'exploration, c'est la prime d'entropie de la semaine 8, et elle a ici une forme fermée. L'entropie différentielle d'une loi normale ne dépend que de sa variance :

$$
H = \ln\sqrt{2\pi e\,\sigma^2}
$$

{{% comment %}}SOURCE: LAPAN ch.15 p.467 ; code p.471{{% /comment %}}

Retenez la lecture : l'entropie d'une gaussienne **croît avec sa largeur**, et ne dépend ni de la moyenne, ni de l'état, ni de l'action. Ajouter une prime d'entropie à une politique gaussienne, c'est donc littéralement payer le réseau pour qu'il garde des variances non minuscules. Et comme en semaine 8 la perte est **minimisée**, le terme qui entre dans la perte est \(-\beta H\), avec un signe négatif : on minimise l'opposé de l'entropie, c'est-à-dire qu'on maximise l'entropie. En développant le logarithme, \(-H = -\tfrac12\left(\ln(2\pi\sigma^2) + 1\right)\), et c'est sous cette forme que le code l'écrit.

> [!WARNING]
 **Le signe de ce terme est la source d'erreur numéro un de la section.** Si vous l'écrivez \(+\beta H\) dans une perte minimisée, vous demandez au réseau de **réduire** son entropie, c'est-à-dire de resserrer ses variances aussi vite que possible. L'effet n'est pas une convergence un peu lente : c'est un effondrement de l'exploration en quelques milliers de pas, après quoi l'agent répète la même action pour toujours et la courbe de récompense devient parfaitement plate. Le diagnostic est immédiat si vous journalisez l'écart-type moyen prédit par le réseau, et c'est pour cela que je l'ai mis dans la liste des quantités à suivre.

---

## Trois têtes sur un tronc, et le code qui va avec

Le réseau tient en quelques lignes. Un tronc commun, puis trois têtes : la moyenne, la variance et la valeur. Chacune a une activation différente, et chacune pour une raison précise.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

TAILLE_CACHEE = 128


class ReseauGaussien(nn.Module):
    """Tronc commun, puis trois tetes : moyenne, variance, valeur."""

    def __init__(self, taille_obs: int, n_actions: int):
        super().__init__()
        self.tronc = nn.Sequential(
            nn.Linear(taille_obs, TAILLE_CACHEE),
            nn.ReLU(),
        )
        # Tanh borne la moyenne a [-1, 1] : les commandes y sont normalisees.
        self.mu = nn.Sequential(
            nn.Linear(TAILLE_CACHEE, n_actions),
            nn.Tanh(),
        )
        # Softplus, ln(1 + e^x), est > 0 partout : une variance ne peut pas
        # devenir negative, quoi que fasse l'optimiseur.
        self.var = nn.Sequential(
            nn.Linear(TAILLE_CACHEE, n_actions),
            nn.Softplus(),
        )
        # Aucune activation : une valeur d'etat n'est bornee ni en haut ni en bas.
        self.valeur = nn.Linear(TAILLE_CACHEE, 1)

    def forward(self, x):
        base = self.tronc(x)
        return self.mu(base), self.var(base), self.valeur(base)
```

{{% comment %}}SOURCE: LAPAN ch.15 p.468{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | vecteur des moyennes, borné à \([-1,1]\) | `self.mu(base)` |
| \(\sigma_\theta^2(s)\) | vecteur des variances, strictement positif | `self.var(base)` |
| \(\hat v(s,\mathbf{w})\) | valeur de l'état, non bornée | `self.valeur(base)` |
| \(\theta\), \(\mathbf{w}\) | paramètres de l'acteur et poids du critique, recouvrants dans le tronc | `self.parameters()` |
| \(n\) | nombre de dimensions d'action | `n_actions` |

Les trois activations méritent chacune une phrase. La **tangente hyperbolique** sur la moyenne la borne à \([-1,1]\), ce qui est le bon intervalle quand l'environnement normalise ses commandes ; si l'environnement attend \([-2,2]\), il faut multiplier la sortie par 2, et c'est une ligne qu'on oublie une fois dans sa vie. La fonction **softplus**, qui vaut \(\ln(1+e^x)\), est strictement positive partout : elle garantit qu'aucun pas d'optimisation ne pourra produire une variance négative, ce qui ferait une racine carrée de nombre négatif deux lignes plus loin. Et **aucune** activation sur la valeur, parce qu'une valeur d'état n'a pas de borne connue.

---

## Agir, puis évaluer, et la différence entre les deux

Agir est un tirage suivi d'un écrêtage de l'action :

```python
import numpy as np


def agir(reseau, obs, device, en_evaluation: bool = False):
    """Renvoie une action valide pour l'environnement."""
    obs_t = torch.as_tensor(np.asarray([obs]), dtype=torch.float32, device=device)
    with torch.no_grad():
        mu_t, var_t, _ = reseau(obs_t)

    mu = mu_t.cpu().numpy()[0]
    if en_evaluation:
        # AUCUN tirage : on joue la moyenne. C'est le pont vers la section 9.3.
        return np.clip(mu, -1.0, 1.0)

    sigma = np.sqrt(var_t.cpu().numpy()[0])
    actions = np.random.normal(mu, sigma)
    # Ecretage de l'action : les bornes de l'environnement sont dures.
    return np.clip(actions, -1.0, 1.0)
```

{{% comment %}}SOURCE: LAPAN ch.15 p.469{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\) | moyenne prédite | `mu` |
| \(\sigma_\theta(s)\) | écart-type, racine de la variance prédite | `sigma` |
| \(a \sim \mathcal{N}\!\left(\mu_\theta(s), \sigma_\theta^2(s)\right)\) | action tirée | `np.random.normal(mu, sigma)` |
| \(\operatorname{clip}(a, a_{\min}, a_{\max})\) | écrêtage de l'action | `np.clip(actions, -1.0, 1.0)` |

Et voici le détail que je veux que vous reteniez le plus de cette section, parce qu'il est le pont vers tout le reste de la semaine. **À l'évaluation, on ne tire pas.** On utilise directement la moyenne renvoyée par le réseau, sans aucun échantillonnage. C'est l'exact équivalent du \(\varepsilon = 0\) de la semaine 5 : le hasard sert à apprendre, pas à être jugé.

{{% comment %}}SOURCE: LAPAN ch.15 p.469{{% /comment %}}

Regardez maintenant ce que fait cette politique d'évaluation, en tant que fonction : elle prend un état et renvoie une action, toujours la même pour le même état. C'est une **politique déterministe**. La section 9.3 ne fera qu'une chose : promouvoir ce comportement de test au rang de comportement d'entraînement, et payer séparément la facture d'exploration qui en découle.

Du côté de la perte, les trois termes de la semaine 8 restent les trois termes de la semaine 8, et seule l'écriture du premier change puisque la log-densité est maintenant gaussienne. Deux gardes-fous valent une ligne de code chacun. Le premier : avant toute division, on force la variance à rester au-dessus d'un plancher, `var_t.clamp(min=1e-3)`, parce qu'une variance qui approche zéro fait exploser l'écart quadratique normalisé et produit un `inf` puis un `nan` en une seule mise à jour.

{{% comment %}}SOURCE: LAPAN ch.15 p.470{{% /comment %}}

Le second garde-fou, c'est le réglage lui-même. Les ordres de grandeur employés sur le robot de la Figure 9-2 sont un facteur d'actualisation de 0,99, un déroulement sur 2 pas, des lots de 32, un pas d'apprentissage de \(5\times 10^{-5}\), un coefficient d'entropie de \(10^{-4}\), et une évaluation tous les 1 000 pas d'entraînement. Deux de ces nombres détonnent par rapport à la semaine 8 : le pas d'apprentissage est très petit, et le coefficient d'entropie aussi. Ce n'est pas un hasard : une politique gaussienne a deux fois plus de paramètres de sortie à régler, et un pas trop grand sur la variance déstabilise la politique bien avant de déstabiliser la moyenne.

{{% comment %}}SOURCE: LAPAN ch.15 p.470{{% /comment %}}

---

## Ce que cela donne, et il faut le dire sans maquillage

Cette méthode, lancée sur le robot quadrupède, donne ceci : **neuf millions de trames, seize heures d'entraînement, et un meilleur score de test de 0,35**, pour une tâche dont le seuil de résolution est à 15. En rejouant le meilleur modèle enregistré, on obtient 0,312 et une vidéo de deux secondes : le robot ne tient pas debout.

{{% comment %}}SOURCE: LAPAN ch.15 p.471 ; p.473{{% /comment %}}

Je ne vous donne pas ce chiffre pour disqualifier la méthode, mais parce qu'il est la **mesure de référence** de la semaine : c'est le nombre contre lequel la section 9.3 se lira. Et parce que la raison de la faiblesse est instructive. Ce n'est pas la tête gaussienne qui échoue : elle fait exactement ce qu'on lui demande. Ce qui échoue, c'est le régime d'échantillonnage. Cette méthode est **sur politique**, elle collecte son expérience dans un seul environnement, et chaque transition est utilisée une fois puis jetée. Vous reconnaissez le problème 4 de la semaine 8 et sa facture en échantillons, et vous reconnaissez aussi pourquoi la semaine 8 insistait tant sur les environnements vectorisés.

{{% comment %}}SOURCE: LAPAN ch.15 p.471{{% /comment %}}

> [!TIP]
 **La question à se poser devant un mauvais résultat, et c'est une compétence de méthode.** Demandez-vous toujours **lequel des composants** a échoué. Ici, trois candidats : la représentation de la politique, le réglage, le régime d'échantillonnage. Le troisième est le coupable, et on le sait parce que la méthode de la section 9.3, qui garde une architecture comparable et change le régime d'échantillonnage en devenant hors politique, fait dix fois mieux avec moitié moins de trames. Une bonne lecture d'échec attribue la responsabilité à un composant nommé, pas à « la méthode ».

---

## Un mensonge discret : l'écrêtage de l'action contre la log-densité

Avant de quitter cette section, je dois nommer un défaut qui est dans tous les codes de ce type, qui ne provoque aucune erreur, qui n'apparaît dans aucun journal, et que presque personne ne mentionne.

Relisez les deux fragments. Dans `agir`, l'action est tirée dans une loi normale **puis écrêtée** aux bornes, et c'est l'action écrêtée qui est jouée, puis stockée dans le lot. Dans la perte, la log-densité est calculée sur cette action stockée, avec la formule de la loi normale **non tronquée**. Les deux ne parlent donc pas de la même loi.

Voyez ce qui se passe à une borne. Supposez que le réseau prédise une moyenne de 0,95 avec un écart-type de 0,3 : une part substantielle de la masse de probabilité tombe au-delà de 1. Toute cette masse est, par l'écrêtage de l'action, empilée exactement sur la valeur 1. La loi réelle de l'action jouée est donc une loi **tronquée avec des atomes aux bornes**, dont la probabilité de valoir exactement 1 est strictement positive, alors que la formule que nous dérivons est celle d'une densité continue pour laquelle cette probabilité est nulle. Nous dérivons donc le logarithme de la mauvaise loi, et l'erreur est d'autant plus grande que la politique est saturée.

{{% comment %}}SOURCE: LAPAN ch.15 p.469-470{{% /comment %}}

Et quand une politique est-elle saturée ? Quand la moyenne, qui sort d'une tangente hyperbolique, s'approche de ses bornes, c'est-à-dire **quand la politique devient bonne**. Le biais se renforce donc exactement là où l'on voudrait de la précision.

> [!WARNING]
 **Pourquoi je m'arrête sur un défaut qui ne casse rien.** Parce que c'est la première fois dans ce cours qu'une méthode se **ment à elle-même sur sa propre distribution**, et parce que toute la section 9.6 est consacrée à une autre forme du même genre de mensonge, celle d'un critique qui se rate dans une direction constante. Ce que je veux vous voir acquérir cette semaine, c'est le réflexe de demander, devant chaque méthode : « est-ce que la loi que je dérive est bien la loi dont je tire ? » Plusieurs des méthodes de cette semaine répondent non.

Deux façons honnêtes de s'en sortir, et je vous demande de savoir les nommer. La première, immédiate : stocker l'action **avant** l'écrêtage de l'action, l'utiliser pour la log-densité, et n'écrêter que ce qui part vers l'environnement. Le biais ne disparaît pas tout à fait, puisque l'environnement a bien reçu une autre action que celle dont on dérive la densité, mais la loi dérivée redevient la loi tirée. La seconde, plus profonde : choisir une loi dont le **support** est exactement l'intervalle autorisé, de sorte qu'il n'y ait rien à écrêter. Cette seconde route demande de transformer une variable normale par une fonction bornée et de corriger la densité en conséquence ; elle est la porte d'entrée d'une méthode de la semaine 10, et je m'arrête ici.

---
