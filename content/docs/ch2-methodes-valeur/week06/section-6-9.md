---
title: "6.9 Défaut nº4, le calendrier à la main : les réseaux bruités"
weight: 10
---

## Faire apprendre l'exploration au lieu de la programmer

Quatrième défaut, et c'est celui dont la réparation est la plus élégante du lot.

Le calendrier de \(\varepsilon\) fonctionne. Il a fait converger votre agent la semaine dernière, il fonctionne bien sur les environnements simples à épisodes courts, et c'est pour cela qu'il est partout. Mais regardez-le avec un œil critique. C'est une fonction du **numéro de trame**, la même dans tous les états, écrite à la main avant l'entraînement par quelqu'un qui ne sait pas encore ce que l'agent va découvrir. Et même dans les cas simples, il demande un réglage : la valeur de départ, la valeur finale, la durée de la décroissance, trois nombres de plus à trouver.

{{% comment %}}SOURCE: LAPAN ch.8 p.250-251{{% /comment %}}

L'idée des **réseaux bruités** (*noisy networks*) est de supprimer ce calendrier et de faire **apprendre** les caractéristiques de l'exploration pendant l'entraînement. Le procédé est d'une simplicité désarmante : on ajoute du bruit aux **poids** des couches linéaires, et on laisse la rétropropagation régler les paramètres de ce bruit en même temps que le reste.

{{% comment %}}SOURCE: LAPAN ch.8 p.250, p.251{{% /comment %}}

Voici l'équation, pour un poids scalaire d'indices \(i,j\) :

$$
w_{i,j} \;=\; \mu_{i,j} + \sigma_{i,j}\cdot\epsilon_{i,j},
\qquad \epsilon_{i,j} \sim \mathcal{N}(0,1)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.251{{% /comment %}}

Lisez-la lentement, parce que la répartition des rôles est tout. \(\mu_{i,j}\) et \(\sigma_{i,j}\) sont des **paramètres entraînables** : ils reçoivent un gradient, ils sont dans `parameters()`, l'optimiseur les met à jour. \(\epsilon_{i,j}\) est un **tirage aléatoire**, retiré à intervalles réguliers, et il n'est jamais entraîné. Le réseau n'apprend donc pas le bruit, il apprend **l'amplitude** du bruit, couche par couche et poids par poids. Si une couche a besoin d'être précise, son \(\sigma\) descendra vers zéro ; si une couche gagne à rester floue, son \(\sigma\) restera grand.

Et c'est là que l'exploration apparaît, sans qu'on l'ait programmée. Un réseau dont les poids sont bruités produit des valeurs d'action bruitées, donc des argmax qui varient d'un passage à l'autre. L'agent reste purement glouton, au sens où il joue toujours l'argument du maximum de sa sortie, et il explore quand même, parce que sa sortie n'est pas déterministe.

> [!NOTE]
 **Notez bien ce que la méthode ne fait pas, parce que la confusion est fréquente et qu'elle survalorise beaucoup le procédé.** Un réseau bruité n'est **pas** un réseau qui décide où il a besoin d'explorer davantage. Il n'y a ici aucune notion de nouveauté, aucun compteur de visites, aucune curiosité. Ce qui est appris, c'est une amplitude de bruit par poids ; le **ciblage** de l'exploration, lui, n'est pas appris. La famille de méthodes qui s'attaque vraiment à cette question, par motivation intrinsèque ou par comptage d'états, est au programme de la semaine 11, et elle est d'un autre ordre de complexité.

{{% comment %}}SOURCE: LAPAN ch.8 p.251{{% /comment %}}

---

## Le bruit gaussien factorisé, ou comment payer moins de tirages

Il y a deux façons de tirer le bruit, et le choix a des conséquences pratiques.

La première est le bruit gaussien **indépendant** : une valeur aléatoire par poids. C'est la lecture littérale de l'équation, et c'est coûteux. Une couche de 3 136 entrées vers 512 sorties demande plus d'un million et demi de tirages, à refaire régulièrement.

La seconde est le **bruit gaussien factorisé** (*factorized Gaussian noise*), et c'est une astuce de calcul. On ne garde que **deux** vecteurs aléatoires, l'un de la taille de l'entrée, l'autre de la taille de la sortie, et on fabrique la matrice de bruit par leur **produit extérieur**. Dans l'exemple ci-dessus, cela ramène 1,6 million de tirages à 3 648.

{{% comment %}}SOURCE: LAPAN ch.8 p.251{{% /comment %}}

Les deux vecteurs ne sont pas utilisés bruts : on leur applique d'abord une transformation qui écrase les grandes valeurs. En écrivant \(f(x) = \operatorname{sgn}(x)\sqrt{\lvert x\rvert}\), le bruit d'un poids est

$$
\epsilon_{i,j} \;=\; f\big(\epsilon^{\text{in}}_{i}\big)\,
 f\big(\epsilon^{\text{out}}_{j}\big)
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.251, p.253{{% /comment %}}

Une remarque honnête sur cette dernière équation : elle décrit exactement ce que le code fait, et elle est de ma main. Le procédé est habituellement donné sous forme de code plutôt que sous forme de formule, et je préfère vous le donner sous les deux formes, puisque c'est la règle de ce cours. L'important est la conséquence : les bruits de deux poids d'une même ligne ne sont plus indépendants. On perd un peu de richesse dans le bruit et on gagne un facteur quatre cents sur le nombre de tirages.

Reste l'initialisation, qui n'est pas arbitraire. Les moyennes \(\mu\) sont tirées uniformément dans \([-1/\sqrt{n_{\text{in}}},\, +1/\sqrt{n_{\text{in}}}\,]\), ce qui est l'initialisation ordinaire d'une couche linéaire. Les écarts-types \(\sigma\) sont tous initialisés à \(0{,}1/\sqrt{n_{\text{in}}}\), c'est-à-dire à un dixième de l'échelle des poids eux-mêmes. L'exploration part donc modérée et le gradient décide de la suite.

{{% comment %}}SOURCE: LAPAN ch.8 p.253{{% /comment %}}

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class CoucheBruitee(nn.Module):
    """Une couche linéaire dont les poids portent un bruit factorisé appris."""

    def __init__(self, n_entrees: int, n_sorties: int, sigma_init: float = 0.1):
        super().__init__()
        self.n_entrees, self.n_sorties = n_entrees, n_sorties
        # ENTRAÎNABLES : moyennes et écarts-types.
        self.poids_mu = nn.Parameter(torch.empty(n_sorties, n_entrees))
        self.poids_sigma = nn.Parameter(torch.empty(n_sorties, n_entrees))
        self.biais_mu = nn.Parameter(torch.empty(n_sorties))
        self.biais_sigma = nn.Parameter(torch.empty(n_sorties))
        # NON ENTRAÎNABLES : le bruit tiré, enregistré comme tampon du module.
        self.register_buffer("poids_epsilon", torch.zeros(n_sorties, n_entrees))
        self.register_buffer("biais_epsilon", torch.zeros(n_sorties))

        borne = 1.0 / math.sqrt(n_entrees)
        nn.init.uniform_(self.poids_mu, -borne, borne)
        nn.init.uniform_(self.biais_mu, -borne, borne)
        nn.init.constant_(self.poids_sigma, sigma_init * borne)
        nn.init.constant_(self.biais_sigma, sigma_init * borne)
        self.tirer_bruit()

    @staticmethod
    def _echelle(taille: int) -> torch.Tensor:
        """f(x) = sgn(x) * sqrt(|x|), appliquée à un vecteur normal."""
        x = torch.randn(taille)
        return x.sign() * x.abs().sqrt()

    def tirer_bruit(self) -> None:
        """Deux vecteurs, un produit extérieur : le bruit factorisé."""
        eps_in = self._echelle(self.n_entrees)
        eps_out = self._echelle(self.n_sorties)
        self.poids_epsilon.copy_(eps_out.outer(eps_in))
        self.biais_epsilon.copy_(eps_out)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.training:
            poids = self.poids_mu + self.poids_sigma * self.poids_epsilon
            biais = self.biais_mu + self.biais_sigma * self.biais_epsilon
        else:
            poids, biais = self.poids_mu, self.biais_mu   # AUCUN bruit
        return F.linear(x, poids, biais)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mu_{i,j}\) | moyenne entraînable d'un poids | `poids_mu`, un `nn.Parameter` |
| \(\sigma_{i,j}\) | amplitude entraînable du bruit | `poids_sigma`, un `nn.Parameter` |
| \(\epsilon_{i,j}\) | le bruit tiré, jamais entraîné | `poids_epsilon`, un tampon du module |
| \(f(x) = \operatorname{sgn}(x)\sqrt{\lvert x\rvert}\) | la transformation des deux vecteurs | `_echelle` |
| \(\epsilon_{i,j} = f(\epsilon^{\text{in}}_i)f(\epsilon^{\text{out}}_j)\) | le produit extérieur | `eps_out.outer(eps_in)` |
| \(w_{i,j} = \mu_{i,j} + \sigma_{i,j}\epsilon_{i,j}\) | le poids effectif | la branche `if self.training` |
| \(1/\sqrt{n_{\text{in}}}\) | l'échelle d'initialisation | `borne` |

> [!WARNING]
 **Attention à deux pièges de ce fragment, et le second coûte des heures.** Premier piège : `register_buffer` et non `nn.Parameter` pour le bruit. Un tampon de module est déplacé vers le processeur graphique avec le reste et sauvegardé avec les poids, mais il ne reçoit **aucun** gradient, ce qui est précisément le statut de \(\epsilon\). Si vous l'écrivez comme un paramètre, l'optimiseur se met à entraîner le bruit, et la méthode n'a plus aucun sens. Second piège : le bruit doit être **retiré** régulièrement, et cela ne se produit pas tout seul. Les implémentations prêtes à l'emploi ne renouvellent pas toutes le tirage à chaque pas d'optimisation, et certaines exigent un appel explicite à une méthode de réinitialisation du bruit, parfois sans le documenter. Si votre réseau bruité explore de moins en moins vite que prévu, vérifiez d'abord que `tirer_bruit()` est appelée.

{{% comment %}}SOURCE: LAPAN ch.8 p.254{{% /comment %}}

Et un point que je veux souligner parce qu'il donne un second sens à une ligne de la semaine 5. Regardez la branche `else` du passage avant : en mode évaluation, la couche n'utilise que les moyennes, sans aucun bruit. Donc, sur un réseau bruité, `reseau.eval()` ne change pas seulement le comportement de l'abandon de neurones et de la normalisation par lots : **il coupe l'exploration**. La ligne du volet C de la semaine dernière, celle que vous aviez écrite avant la boucle d'évaluation, est devenue le remplaçant exact de \(\varepsilon = 0\).

{{% comment %}}SOURCE: LAPAN ch.8 p.254{{% /comment %}}

---

## Ce que l'on supprime, et ce que l'on observe

La conversion d'un réseau Q profond ordinaire en réseau bruité est brutalement simple : on remplace les deux couches linéaires de la tête par des couches bruitées, et **on supprime tout le code lié à la stratégie \(\varepsilon\)-gloutonne**. Le sélecteur de la section 6.2, le calendrier de la section 6.5, les trois hyperparamètres qui le règlent : tout cela disparaît. C'est la seule réparation de la semaine qui retire plus de code qu'elle n'en ajoute.

{{% comment %}}SOURCE: LAPAN ch.8 p.254{{% /comment %}}

Comment savoir, alors, ce que l'agent explore ? En instrumentant les couches. On calcule, pour chaque couche bruitée, le **rapport signal sur bruit** (*signal-to-noise ratio*) :

$$
\mathrm{SNR} \;=\; \frac{\mathrm{RMS}(\mu)}{\mathrm{RMS}(\sigma)}
$$

{{% comment %}}SOURCE: LAPAN ch.8 p.254{{% /comment %}}

où \(\mathrm{RMS}\) est la moyenne quadratique des coefficients de la couche. Ce rapport dit combien de fois la composante stationnaire de la couche est plus grande que le bruit injecté. Un rapport qui monte signifie que la couche devient déterministe ; un rapport qui descend signifie qu'elle redevient exploratoire.

La **Figure 6-6** donne ces deux courbes sur un entraînement complet, et je vous demande de regarder attentivement la seconde moitié de celle qui suit la dernière couche.

{{< bookfig src="06-06.png" week="06" >}}

{{% comment %}}SOURCE: LAPAN ch.8 p.255{{% /comment %}}

Voici ce qu'on y lit. Le rapport de la première couche reste bas et monte lentement, de 2 à environ 2,6 : cette couche garde du bruit pendant tout l'entraînement. Celui de la seconde part de 4 et grimpe jusqu'à 16 : elle devient nettement plus déterministe, ce qui est raisonnable puisque c'est elle qui produit les valeurs d'action. Et puis, après environ 450 000 trames, ce rapport **redescend**, vers 11. Le niveau de bruit de la dernière couche a recommencé à augmenter, ce qui pousse l'agent à explorer davantage.

{{% comment %}}SOURCE: LAPAN ch.8 p.255{{% /comment %}}

Arrêtons-nous une seconde sur cette dernière phrase, parce que c'est l'argument décisif de la section. **Aucun calendrier écrit à la main ne fait cela.** Un calendrier de \(\varepsilon\) décroît et ne remonte jamais ; un agent qui a fini de descendre son calendrier n'explorera plus, même s'il arrive dans une région du jeu qu'il n'a jamais vue. Ici, le gradient a décidé, à la moitié de l'entraînement, qu'il fallait réexplorer. On peut trouver le gain modeste ; le mécanisme, lui, est d'une nature différente.

Les chiffres, avec le même avertissement que d'habitude. Sur le jeu de référence, la version bruitée atteint une moyenne de 18 en environ **250 parties**, contre 400 pour la référence : c'est le meilleur gain par partie de toutes les réparations prises isolément. Mais elle tourne à **194 trames par seconde** contre 240, parce que le tirage du bruit et le calcul des poids effectifs coûtent à chaque passage avant. En temps de calcul, la différence est donc beaucoup moins impressionnante qu'en nombre de parties. Après réglage, 273 parties.

{{% comment %}}SOURCE: LAPAN ch.8 p.254, p.256{{% /comment %}}

C'est la deuxième fois de la semaine qu'une comparaison change de conclusion selon l'unité choisie, et ce ne sera pas la dernière. Prenez l'habitude de demander, devant toute affirmation de ce domaine : plus rapide **en quoi** ?

---
