---
title: "10.5 SAC : payer en calcul plutôt qu'en échantillons"
weight: 6
---

## Une autre filiation : la semaine 9, et non la semaine 8

Quatrième et dernière méthode de la semaine, et la première chose à dire est qu'elle n'appartient pas à la famille des trois précédentes.

L'**acteur-critique doux** (*soft actor-critic*, SAC) est de 2018, et c'est aujourd'hui l'une des méthodes de référence pour le contrôle continu, très largement employée. Son idée centrale est beaucoup plus proche du DDPG de la semaine 9 que des gradients de politique de la semaine 8. Elle est **hors politique**, elle apprend depuis un tampon de rejeu, et elle hérite directement de deux correctifs de la section 9.6.

{{% comment %}}SOURCE: LAPAN ch.16 p.514{{% /comment %}}

La façon la plus exacte de la situer est celle-ci : elle optimise une politique **stochastique** d'une façon **hors politique**, ce qui fait d'elle un pont entre les deux moitiés du module 3. Elle n'est pas une descendante de TD3, les deux ayant été publiées à peu près en même temps, mais elle en reprend le **double Q écrêté** ; et parce que sa politique est intrinsèquement stochastique, elle bénéficie gratuitement de quelque chose qui ressemble au **lissage de la politique cible**. Trois objets de la semaine 9 dans une seule phrase, et le troisième est le tampon de rejeu.

{{% comment %}}SOURCE: SPINUP sac/background{{% /comment %}}

> [!NOTE]
 **Le double Q écrêté ne sera pas redérivé, et c'est volontaire.** Le minimum entre deux critiques jumeaux, la sous-estimation volontaire qu'il introduit, et la raison pour laquelle une erreur par défaut s'oublie là où une erreur par excès s'amplifie : tout cela est la section 9.6 du cours, et vous l'avez déjà. Je le réutilise ici comme un acquis, en une ligne de formule, parce que le redériver depuis une seconde source vous apprendrait qu'il s'agit de deux idées, alors qu'il s'agit de la même.

{{% comment %}}SOURCE: source-assets/raw-content/week-09.md §9.6{{% /comment %}}

Ce qui est nouveau est ailleurs, et cela change l'objectif lui-même.

---

## L'entropie entre dans l'objectif, et ce n'est pas la prime de la semaine 8

Rappelez-vous le problème de la semaine 9 : une politique déterministe n'explore rien, et il faut ajouter du bruit aux actions. Rappelez-vous aussi la réponse de la semaine 8 au même problème : ajouter à la perte un terme qui paie l'agent pour garder une politique large, la **prime d'entropie**.

SAC fait quelque chose de différent des deux, et la différence est de nature et non de degré. Il ne modifie ni la perte ni l'action : il modifie **l'objectif que la méthode cherche à maximiser**. L'agent ne cherche plus le rendement maximal, il cherche le meilleur compromis entre le rendement et l'entropie de sa propre politique, et il reçoit à chaque pas de temps une prime proportionnelle à l'entropie de sa politique dans l'état courant.

{{% comment %}}SOURCE: SPINUP sac/background{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.514{{% /comment %}}

Écrivons-le. L'entropie d'une distribution, dans la forme la plus commode ici :

$$
H(P) = \E_{x \sim P}\left[\, -\ln P(x) \,\right]
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.514 (image){{% /comment %}}

Et le problème d'apprentissage par renforcement régularisé par l'entropie, c'est-à-dire la **régularisation par l'entropie** (*entropy regularization*), qui est le cœur de la méthode :

$$
\pi^* = \argmax_{\pi}\; \E_{\tau \sim \pi}\left[\, \sum_{t=0}^{\infty} \gamma^{\,t} \Big(\, R_{t+1} \;+\; \alpha\, H\big(\pi(\cdot \mid s_t)\big) \,\Big) \,\right]
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Regardez où le terme d'entropie est placé : **à l'intérieur de la somme actualisée**, au même rang que la récompense. Ce n'est pas un terme ajouté à une perte après coup, c'est un terme de la récompense elle-même. Le coefficient \(\alpha\) règle le change entre les deux monnaies, et il est strictement positif.

> [!WARNING]
 **La lettre \(\alpha\) change de sens dans cette section, et c'est la troisième de ses acceptions dans ce cours.** Ici, \(\alpha\) est le **coefficient d'entropie**, c'est-à-dire le prix auquel on achète de l'incertitude en unités de récompense. Ce n'est **pas** le pas d'apprentissage, qui porte cette lettre depuis la semaine 3 et dans toute la page « Notation ». Ce n'est pas non plus le facteur de rebroussement \(\alpha_{\text{ls}}\) de la section 10.3, ni le paramètre de synchronisation douce qu'une certaine bibliothèque appelle `alpha` et dont la semaine 9 a converti les trois conventions. Je garde malgré tout la lettre, contre ma propre habitude de renommer, et je vous dois la raison : \(\alpha\) apparaît dans les six équations de cette méthode et dans le nom de l'hyperparamètre de toutes ses implémentations, de sorte qu'un renommage vous rendrait la lecture de n'importe quel code plus difficile, pas plus facile. Dans cette section, et seulement dans cette section, \(\alpha\) est un coefficient d'entropie. Le pas d'apprentissage, lui, s'y écrit en français.

Maintenant la distinction que je veux absolument que vous fassiez, parce que les deux objets portent le même mot et ne font pas le même travail.

La **prime d'entropie** de la semaine 8 est un terme ajouté à une perte, avec un coefficient, pour empêcher la politique de se resserrer trop vite. Elle ne change ni la fonction de valeur, ni la cible, ni rien d'autre dans la méthode : c'est un régularisateur posé à côté. La **régularisation par l'entropie** de cette section change l'objectif, donc elle change ce que signifie « la valeur d'un état », donc elle change les fonctions de valeur et les cibles de Bellman. C'est pour cela que la section continue encore pendant trois équations : parce qu'il faut reconstruire les valeurs sur le nouvel objectif.

{{% comment %}}SOURCE: SPINUP sac/background{{% /comment %}}

Ce que l'on gagne en échange est double, et les deux moitiés comptent. Une politique plus large explore davantage, donc elle apprend plus vite ensuite. Et surtout, elle est **beaucoup moins susceptible de converger prématurément vers un mauvais optimum local**, ce qui est une réponse directe aux deux échecs que vous avez lus dans cette semaine : le guépard qui avance sur le dos en section 10.2, et la fourmi qui reste debout sans bouger en section 10.3. Les deux sont des optima locaux dans lesquels une politique trop étroite s'est enfermée.

{{% comment %}}SOURCE: SPINUP sac/background{{% /comment %}}

---

## Les fonctions de valeur suivent l'objectif

Puisque l'objectif a changé, les valeurs changent. La valeur d'un état inclut désormais la prime d'entropie de **tous** les pas de temps :

$$
v_\pi(s) = \E_{a \sim \pi}\left[\, q_\pi(s,a) \,\right] + \alpha\, H\big(\pi(\cdot \mid s)\big)
         = \E_{a \sim \pi}\left[\, q_\pi(s,a) - \alpha \ln \pi(a \mid s) \,\right]
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Les deux écritures sont la même, et le passage de l'une à l'autre est la définition de l'entropie : moins le logarithme de la probabilité, en espérance. C'est la deuxième écriture qui s'implémente, parce qu'un échantillon de \(-\ln\pi(a\mid s)\) est une estimation non biaisée de l'entropie et qu'on l'obtient gratuitement en tirant une action.

La valeur d'action, elle, inclut la prime de tous les pas **sauf le premier**, et la raison est simple : au premier pas, l'action est donnée, donc il n'y a aucune incertitude à payer. Cette asymétrie se voit directement dans la façon dont le terme d'entropie entre dans le report de Bellman :

$$
q_\pi(s,a) \approx R + \gamma\left(\, q_\pi(s', \tilde{a}') - \alpha \ln \pi(\tilde{a}' \mid s') \,\right),
\qquad \tilde{a}' \sim \pi(\cdot \mid s')
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Le terme d'entropie est **à l'intérieur** de l'actualisation, attaché à l'état suivant, et il porte l'action \(\tilde{a}'\) qui vient d'être tirée. Notez d'ailleurs, puisque la franchise est de mise, que le partage de la prime d'entropie entre \(v_\pi\) et \(q_\pi\) comporte une part d'arbitraire : on pourrait convenir de la compter autrement, et les formules changeraient d'aspect sans changer de contenu. La convention ci-dessus est celle qui rend les cibles les plus simples à écrire, et c'est la raison pour laquelle elle est adoptée.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

---

## La cible, et une politique écrasée par une tangente hyperbolique

Nous avons tout pour écrire la méthode. SAC apprend **une politique et deux fonctions de valeur d'action**, les deux critiques jumeaux de la semaine 9, chacun avec son réseau cible. Il n'y a pas de réseau de valeur d'état.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

La cible des deux critiques s'écrit ainsi :

$$
y(R, s', d_{\text{term}}) = R + \gamma\left(1 - d_{\text{term}}\right)\left(\, \min_{j=1,2} q_{\mathbf{w}_j^-}(s', \tilde{a}') \;-\; \alpha \ln \pi_\theta(\tilde{a}' \mid s') \,\right),
\qquad \tilde{a}' \sim \pi_\theta(\cdot \mid s')
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Prenez le temps de lire cette ligne morceau par morceau, parce qu'elle contient toute la semaine 9 et une nouveauté.

Le facteur \((1 - d_{\text{term}})\) est l'écriture compacte de « un état terminal vaut zéro », celle que la semaine 9 a déjà présentée comme l'équivalent de la forme à deux cas ; \(d_{\text{term}}\) vaut 1 si \(s'\) est terminal et 0 sinon. Le minimum sur les deux critiques cibles est le **double Q écrêté** de la section 9.6, inchangé. Le terme \(-\alpha\ln\pi_\theta\) est la nouveauté, et c'est par là que l'entropie entre dans l'apprentissage de la valeur. Et le détail le plus important est le plus discret : l'action \(\tilde{a}'\) est **tirée fraîchement dans la politique courante**, et non lue dans le tampon de rejeu, et pas non plus produite par une politique cible.

> [!IMPORTANT]
 **Trois différences avec la méthode de la semaine 9, et elles sont exactement la passation entre les deux semaines.** Première différence : la cible porte un terme d'entropie, qui n'existait pas. Deuxième différence : l'action de l'état suivant vient de la **politique courante** et non d'une politique cible, de sorte qu'il n'y a pas de réseau cible pour l'acteur, seulement pour les deux critiques. Troisième différence : il n'y a **aucun lissage explicite de la politique cible**, le correctif 3 de la section 9.6, et il n'en a pas besoin, parce que la politique est stochastique et que le bruit de son propre échantillonnage produit un effet comparable. Autrement dit, cette méthode obtient gratuitement un correctif que la semaine 9 devait ajouter à la main, et elle l'obtient parce qu'elle a renoncé au déterminisme.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Reste la politique, et c'est là que deux choix changent tout par rapport aux trois méthodes précédentes de la semaine.

**Premier choix : l'écart-type est une sortie du réseau, donc une fonction de l'état.** Souvenez-vous du troisième écart de la section 10.1 : chez les trois méthodes sur politique, l'écart-type est un paramètre global, le même partout. Ici, il est prédit à partir de l'observation, comme la moyenne. Ce n'est pas un raffinement cosmétique : si l'écart-type ne dépend pas de l'état, l'entropie de la politique ne dépend pas de l'état non plus, et l'agent ne peut pas apprendre **où** il a besoin d'être incertain. La régularisation par l'entropie perd alors l'essentiel de son sens. Et la mesure confirme la théorie : une politique à écart-type indépendant de l'état, dans cette méthode, ne fonctionne pas.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

**Second choix : l'action est écrasée par une tangente hyperbolique, et la distribution cesse d'être gaussienne.** On tire d'abord une gaussienne, puis on applique \(\tanh\), ce qui borne l'action à \([-1,1]\) sans aucun écrêtage. Avant la tangente hyperbolique, la politique est une gaussienne à composantes indépendantes comme celle de la semaine 9 ; après, elle n'en est plus une. C'est la seconde route honnête que la section 9.2 avait annoncée pour se débarrasser du biais de l'écrêtage de l'action : choisir une loi dont le support est exactement l'intervalle autorisé, de sorte qu'il n'y ait rien à écrêter. La voici, et elle était bien dans cette semaine.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}
{{% comment %}}SOURCE: source-assets/raw-content/week-09.md §9.2{{% /comment %}}

L'écriture de cette politique est la suivante, et elle contient l'astuce qui rend tout dérivable :

$$
\tilde{a}_\theta(s, \xi) = \tanh\!\Big(\, \mu_\theta(s) + \sigma_\theta(s) \odot \xi \,\Big),
\qquad \xi \sim \mathcal{N}(0, I)
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

Le symbole \(\odot\) est le produit terme à terme, et \(\xi\) est un vecteur de bruit normal centré réduit, tiré indépendamment des paramètres. Cette écriture s'appelle la **reparamétrisation** (*reparameterization trick*), et son intérêt est entièrement technique et entièrement décisif : l'action est maintenant une **fonction déterministe** de l'état, des paramètres et d'un bruit extérieur. Le hasard a été sorti du chemin du gradient. Souvenez-vous de la raison pour laquelle, en semaine 8, le critique ne pouvait pas être dérivé vers l'acteur : un échantillonnage est une barrière pour la rétropropagation. La reparamétrisation déplace cette barrière à l'extérieur, dans le tirage de \(\xi\), et le gradient passe à travers le reste.

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

L'objectif de l'acteur s'écrit alors comme une maximisation sur les états du tampon et sur le bruit :

$$
\max_{\theta}\; \E_{s \sim \mathcal{D},\; \xi \sim \mathcal{N}}\left[\, \min_{j=1,2} q_{\mathbf{w}_j}\!\big(s, \tilde{a}_\theta(s,\xi)\big) \;-\; \alpha \ln \pi_\theta\!\big(\tilde{a}_\theta(s,\xi) \mid s\big) \,\right]
$$

{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

C'est l'objectif d'acteur de la semaine 9, avec deux modifications. L'acteur escalade le **minimum des deux critiques** et non le premier d'entre eux, ce qui est une différence réelle avec TD3 et non une variante d'écriture. Et il paie un terme d'entropie, qui le retient de devenir trop sûr de lui.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

LOGSTD_MIN, LOGSTD_MAX = -20.0, 2.0


class PolitiqueDouce(nn.Module):
    """Deux sorties : moyenne ET log ecart-type, toutes deux fonctions de l'etat."""

    def __init__(self, taille_obs: int, n_actions: int, cachee: int = 256):
        super().__init__()
        self.tronc = nn.Sequential(
            nn.Linear(taille_obs, cachee), nn.ReLU(),
            nn.Linear(cachee, cachee), nn.ReLU(),
        )
        self.mu = nn.Linear(cachee, n_actions)
        self.logstd = nn.Linear(cachee, n_actions)   # UNE COUCHE, pas un parametre

    def forward(self, obs):
        base = self.tronc(obs)
        # Le serrage evite un ecart-type nul ou gigantesque, qui ferait
        # exploser la log-densite des la premiere mise a jour.
        logstd = torch.clamp(self.logstd(base), LOGSTD_MIN, LOGSTD_MAX)
        return self.mu(base), logstd

    def echantillonner(self, obs):
        """Reparametrisation + tanh, et la log-densite CORRIGEE."""
        mu, logstd = self(obs)
        sigma = torch.exp(logstd)

        loi = torch.distributions.Normal(mu, sigma)
        u = loi.rsample()               # rsample() = reparametrisation : le
                                        # gradient traverse le tirage.
        action = torch.tanh(u)

        # La tanh deforme la densite : il faut retirer le logarithme du
        # jacobien, sans quoi la log-densite n'est pas celle de l'action jouee.
        logprob = loi.log_prob(u) - torch.log(1.0 - action.pow(2) + 1e-6)
        return action, logprob.sum(dim=-1)


def pas_sac(politique, q1, q2, q1_cible, q2_cible, lot, gamma, alpha):
    """Une mise a jour : les deux critiques, puis l'acteur."""
    etats, actions, recompenses, etats_suiv, termines = lot

    # --- Cible commune aux deux critiques.
    with torch.no_grad():
        act_suiv, logprob_suiv = politique.echantillonner(etats_suiv)
        q_min = torch.min(q1_cible(etats_suiv, act_suiv),
                          q2_cible(etats_suiv, act_suiv)).squeeze(-1)
        # Double Q ecrete (semaine 9) MOINS le terme d'entropie (nouveau).
        cible = recompenses + gamma * (1.0 - termines) * (q_min - alpha * logprob_suiv)

    perte_critiques = (F.mse_loss(q1(etats, actions).squeeze(-1), cible)
                       + F.mse_loss(q2(etats, actions).squeeze(-1), cible))

    # --- Acteur : il escalade le MINIMUM des deux critiques, pas le premier.
    act, logprob = politique.echantillonner(etats)
    q_acteur = torch.min(q1(etats, act), q2(etats, act)).squeeze(-1)
    perte_acteur = (alpha * logprob - q_acteur).mean()

    return perte_critiques, perte_acteur
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_\theta(s)\), \(\sigma_\theta(s)\) | moyenne et écart-type, **tous deux fonctions de l'état** | `self.mu(base)`, `torch.exp(logstd)` |
| \(\xi \sim \mathcal{N}(0,I)\) | bruit de reparamétrisation | tiré à l'intérieur de `rsample()` |
| \(\tilde{a}_\theta(s,\xi)\) | action écrasée par la tangente hyperbolique | `action` |
| \(\ln \pi_\theta(\tilde{a}\mid s)\) | log-densité **corrigée du jacobien** | `logprob` |
| \(\alpha\) | coefficient d'entropie | `alpha` |
| \(\min_{j=1,2} q_{\mathbf{w}_j^-}\) | double Q écrêté, côté cible | `torch.min(q1_cible, q2_cible)` |
| \(d_{\text{term}}\) | indicateur d'état terminal | `termines` |
| \(y\) | cible commune aux deux critiques | `cible` |
| \(\tilde{a}'\) | action de l'état suivant, **tirée dans la politique courante** | `act_suiv` |
| \(\mathcal{D}\) | tampon de rejeu | `lot`, tiré du tampon |

> [!WARNING]
 **La correction de jacobien est la ligne la plus facile à oublier de toute la semaine, et elle ne lève aucune erreur.** Quand on transforme une variable aléatoire par une fonction, sa densité se déforme, et le facteur de déformation est la dérivée de la transformation. La dérivée de \(\tanh\) étant \(1 - \tanh^2\), le logarithme de la densité de l'action vaut le logarithme de la densité gaussienne **moins** \(\ln(1 - a^2)\), terme par terme. Sans cette correction, vous calculez la log-densité de la variable d'avant la tangente hyperbolique et vous la faites passer pour celle de l'action : exactement le mensonge que la section 9.2 avait nommé, sous une autre forme. Le symptôme est discret et trompeur, un terme d'entropie systématiquement faux, donc un compromis entre rendement et entropie qui n'est pas celui que vous croyez régler. Et notez le \(10^{-6}\) ajouté dans le logarithme : quand l'action sature à \(\pm 1\), l'argument tend vers zéro et le logarithme vers l'infini.

---

## Ce que \(\alpha\) contrôle, et quatre faits à retenir

Le coefficient d'entropie \(\alpha\) contrôle explicitement le compromis entre exploration et exploitation, et c'est une des qualités de la méthode : là où la semaine 9 réglait une amplitude de bruit sans savoir ce qu'elle achetait, ce coefficient a une unité interprétable, puisqu'il convertit de l'entropie en récompense.

Deux variantes circulent. Dans la première, \(\alpha\) est un hyperparamètre fixé par vous. Dans la seconde, il est **ajusté automatiquement** en cours d'entraînement, de façon à maintenir l'entropie de la politique à un niveau cible. La seconde est généralement préférée en pratique, et c'est celle que les bibliothèques fournissent par défaut.

{{% comment %}}SOURCE: SPINUP sac/quick-facts{{% /comment %}}

Trois réglages de conduite, qui sont ceux de la semaine 9 et que je rappelle en une phrase chacun. À l'**évaluation**, on retire le hasard et on joue la moyenne de la politique, c'est-à-dire la tangente hyperbolique de \(\mu_\theta(s)\) : c'est le \(\varepsilon = 0\) de test de la semaine 5, pour la troisième fois. Au **démarrage**, on ignore la politique pendant les premiers milliers de pas et on tire les actions uniformément, pour remplir le tampon avec quelque chose de varié. Et le tampon, les réseaux cibles et la synchronisation douce sont ceux de la semaine 9, sans modification.

{{% comment %}}SOURCE: SPINUP sac/exploration{{% /comment %}}

Enfin, quatre faits de cadrage pour la section 10.6 et pour votre jalon.

Cette méthode est **hors politique** : elle apprend sur des transitions anciennes, donc elle réutilise chaque échantillon des dizaines de fois. C'est ce qui va faire tout l'argument de la section suivante. L'implémentation standard ne traite que les espaces d'actions **continus** ; une variante pour actions discrètes existe, avec une mise à jour de politique un peu différente, mais ce n'est pas celle que vous installerez. Elle ne se **parallélise pas** à la façon de la semaine 8 : il n'y a pas de version à seize environnements qui donne un facteur seize, parce que le goulot n'est pas la collecte. Et une version plus ancienne de la méthode apprenait **en plus** un réseau de valeur d'état, donc quatre réseaux au lieu de trois ; la formulation moderne, celle de cette section, s'en passe. Si vous lisez une présentation à quatre réseaux, vous lisez la version ancienne, et ce n'est pas une erreur, c'est une date.

{{% comment %}}SOURCE: SPINUP sac/quick-facts{{% /comment %}}
{{% comment %}}SOURCE: SPINUP sac/key-equations{{% /comment %}}

---
