---
title: "8.1 Paramétrer la politique"
weight: 2
---

## Un réseau qui sort une distribution, et non un score par action

Reprenons le réseau de la semaine 5 et changeons une seule chose : ce que ses sorties **signifient**.

En semaine 5, le réseau avait une sortie par action et chaque sortie estimait \(Q(s,a)\), un nombre sans borne, comparable aux autres uniquement par son rang. Cette semaine, le réseau a encore une sortie par action, mais l'ensemble de ces sorties, après passage dans une fonction softmax, forme une **distribution de probabilité** : des nombres positifs qui somment à un, et dont chacun est la probabilité de choisir l'action correspondante. La **Figure 8-1** montre ce réseau et les probabilités qu'il produit. Regardez-la à côté de la figure équivalente de la semaine 5 : même boîte, mêmes entrées, même nombre de sorties, et une interprétation entièrement différente.

{{< bookfig src="08-01.png" week="08" >}}

{{% comment %}}SOURCE: LAPAN ch.11 p.332{{% /comment %}}

Formellement, nous demandons deux choses à cette politique. D'abord qu'elle soit **dérivable** par rapport à ses paramètres : \(\pi(a \mid s,\theta)\) doit admettre un gradient \(\nabla \pi(a\mid s,\theta)\) fini pour tout état, toute action et toute valeur des paramètres. Sans cela, rien de ce que fait cette semaine n'a de sens, puisque tout repose sur une montée de gradient dans \(\theta\). Ensuite, en pratique, nous exigeons qu'elle ne devienne **jamais** complètement déterministe, c'est-à-dire que \(\pi(a\mid s,\theta)\) reste strictement entre 0 et 1, parce que c'est l'échantillonnage dans cette distribution qui assure l'exploration. Une politique qui atteint exactement la probabilité 1 sur une action a cessé d'explorer, définitivement.

{{% comment %}}SOURCE: SB ch.13 p.344{{% /comment %}}

La paramétrisation standard pour un ensemble d'actions discret passe par des **préférences numériques** \(h(s,a,\theta)\), une par action, que l'on pousse dans un softmax :

$$
\pi(a \mid s, \theta) \defeq \frac{e^{h(s,a,\theta)}}{\sum_{b} e^{h(s,b,\theta)}}
$$

Les préférences elles-mêmes peuvent être n'importe quelle fonction dérivable. Elles peuvent être la sortie d'un réseau profond, \(\theta\) désignant alors l'ensemble de ses poids, ou simplement linéaires en des caractéristiques, \(h(s,a,\theta) = \theta^\top \mathbf{x}(s,a)\). Tout ce qui suit dans la semaine est indifférent à ce choix : le théorème de la section 8.2 ne regarde que \(\nabla \pi\).

{{% comment %}}SOURCE: SB ch.13 p.344{{% /comment %}}

Retenez le mot **préférence**, parce qu'il porte une distinction que nous allons exploiter dans un instant. Une préférence n'est pas une valeur. Elle ne cherche à estimer aucune quantité du monde. Elle n'a même pas d'échelle propre, puisque le softmax est insensible à l'ajout d'une constante à toutes les préférences d'un même état. Elle n'est qu'un **levier** sur la probabilité d'une action, et c'est précisément cela qui la rend plus libre qu'une valeur d'action.

---

## Cinq choses que la route par la valeur ne peut pas offrir

Je vais vous donner cinq avantages, du plus concret au plus théorique. Le deuxième est celui que je veux que vous reteniez, et je le démontrerai sur un exemple.

**Premier avantage : la politique approchée peut s'approcher du déterminisme.** Une politique \(\varepsilon\)-gloutonne garde toujours une probabilité \(\varepsilon\) sur une action tirée au hasard, par construction, et ne converge donc jamais vers une politique déterministe même quand c'est la bonne. On pourrait croire qu'un softmax sur les **valeurs d'action** réglerait le problème : il ne le règle pas, parce que les valeurs d'action convergent vers leurs valeurs vraies, qui diffèrent d'une quantité finie, ce qui laisse une probabilité finie aux actions sous-optimales. Les préférences, elles, ne convergent vers aucune valeur particulière : elles sont poussées sans limite vers la politique optimale, et elles peuvent donc produire un déterminisme arbitrairement proche.

{{% comment %}}SOURCE: SB ch.13 p.344{{% /comment %}}

**Deuxième avantage : des probabilités arbitraires, donc un optimum stochastique accessible.** Dans un jeu à information imparfaite, il arrive que la meilleure façon de jouer soit de faire deux choses avec des probabilités précises. Au poker, bluffer à une certaine fréquence est optimal : jouer toujours la même action rend l'adversaire capable de vous lire. Une méthode fondée sur la valeur n'a aucun moyen naturel de représenter un tel optimum, parce qu'elle choisit par un \(\argmax\) et qu'un \(\argmax\) est déterministe. Une politique paramétrée, elle, représente « 59 % à droite, 41 % à gauche » aussi naturellement que n'importe quoi d'autre.

{{% comment %}}SOURCE: SB ch.13 p.345{{% /comment %}}

Et voici l'exemple qui le prouve, en cinq lignes, parce qu'une démonstration vaut mieux qu'une affirmation. Imaginez un couloir de trois états non terminaux, en file. À chaque pas, la récompense est \(-1\), ce qui veut dire qu'il faut sortir vite. Deux actions, « droite » et « gauche ». Et un piège : dans le **deuxième** état, les deux actions sont **inversées**, « droite » déplaçant vers la gauche et réciproquement. Si l'agent ne dispose que des caractéristiques \(\mathbf{x}(s,\text{droite}) = [1,0]^\top\) et \(\mathbf{x}(s,\text{gauche}) = [0,1]^\top\), les trois états lui paraissent **identiques** : il ne peut pas reconnaître celui où les actions sont inversées, et doit donc appliquer la même distribution partout.

Que peut-il faire ? Avec \(\varepsilon = 0{,}1\), une politique \(\varepsilon\)-gloutonne qui préfère « droite » obtient une valeur de l'état de départ pire que \(-44\), et celle qui préfère « gauche » pire que \(-82\). Les deux sont mauvaises, et elles sont les deux seules options d'une méthode qui choisit par \(\argmax\). La meilleure politique **stochastique**, elle, prend « droite » avec une probabilité d'environ \(0{,}59\) et atteint environ \(-11{,}6\), soit près de quatre fois mieux que la meilleure des deux politiques déterministes. Aucun réglage de \(\varepsilon\), aucune amélioration de l'estimation des valeurs, aucune profondeur de réseau ne permet à une méthode fondée sur la valeur d'atteindre ce chiffre. Il faut pouvoir représenter \(0{,}59\), et pour cela il faut paramétrer la politique.

{{% comment %}}SOURCE: SB ch.13 p.345{{% /comment %}}

> [!IMPORTANT]
 **C'est l'argument central de la semaine, et il ne porte pas sur la vitesse.** Les quatre autres avantages sont des arguments de commodité ou d'efficacité, et on pourrait les discuter. Celui-ci est un argument d'**expressivité**. Il existe des problèmes dont la solution optimale est une distribution, et une méthode qui sélectionne par \(\argmax\) ne peut pas l'écrire, quelle que soit la qualité de son estimation. Quand on vous demandera pourquoi apprendre la politique directement, c'est cette phrase qu'il faut donner avant toutes les autres.

**Troisième avantage : la politique est parfois la fonction la plus simple à approcher.** Selon le problème, la politique optimale peut être beaucoup plus simple à représenter que la fonction de valeur. Au Tetris, par exemple, décider où poser la pièce courante est plus facile que chiffrer la valeur d'une configuration de plateau. Quand c'est le cas, apprendre la politique demande moins de capacité et moins de données que d'apprendre la valeur pour en déduire la politique.

**Quatrième avantage : la paramétrisation est un endroit où injecter ce qu'on sait déjà.** Choisir la forme de \(\pi(a\mid s,\theta)\) permet d'y encoder des connaissances préalables sur le problème : des symétries, des contraintes, une structure. C'est souvent la raison la plus déterminante en pratique, parce qu'elle décide de ce que le réseau n'a **pas** besoin d'apprendre.

{{% comment %}}SOURCE: SB ch.13 p.345-346{{% /comment %}}

**Cinquième avantage, théorique : les probabilités varient continûment avec les paramètres.** C'est une propriété de régularité, et elle a des conséquences sur les garanties de convergence. Sous une politique \(\varepsilon\)-gloutonne, un changement arbitrairement petit des valeurs d'action estimées peut faire basculer l'\(\argmax\) et changer **brutalement** les probabilités d'action : une action passe de \(\varepsilon/|\mathcal{A}|\) à presque 1 parce qu'un nombre a bougé au troisième chiffre. Avec une paramétrisation continue de la politique, un petit déplacement de \(\theta\) ne produit qu'un petit déplacement de la distribution. Les garanties de convergence les plus fortes connues pour les méthodes de gradient de politique reposent sur cette continuité.

{{% comment %}}SOURCE: SB ch.13 p.346{{% /comment %}}

La version pratique du même point mérite d'être dite dans le vocabulaire d'un praticien, parce que c'est sous cette forme que vous la rencontrerez : la sortie d'une distribution de probabilité donne une **représentation lisse**. Une petite modification des poids donne une petite modification de la distribution, là où une sortie discrète peut sauter d'une action à une autre. Et comme une descente de gradient ne fait, par définition, que de petits déplacements des poids, une représentation lisse est exactement ce qu'il lui faut.

{{% comment %}}SOURCE: LAPAN ch.11 p.332{{% /comment %}}

---

## Échantillonner au lieu de choisir

Il reste un changement d'habitude, et c'est celui que les étudiants oublient le plus souvent en écrivant leur première boucle.

Avec un réseau Q profond, deux sorties valant \(0{,}4\) et \(0{,}5\) signifiaient que l'agent prenait la seconde action **cent pour cent du temps**, à l'exploration \(\varepsilon\) près. L'écart entre les deux nombres n'avait aucune importance : seul leur ordre comptait. Avec une politique, deux probabilités valant \(0{,}4\) et \(0{,}5\) signifient que l'agent prend la première action **quarante pour cent du temps**. L'écart est devenu le sujet, et le choix de l'action est un **échantillonnage de l'action** (*action sampling*), non une comparaison.

{{% comment %}}SOURCE: LAPAN ch.11 p.336{{% /comment %}}

Deuxième changement d'habitude, purement technique mais lourd de conséquences numériques. Le réseau ne renvoie **pas** de probabilités : il renvoie des **sorties brutes**, et le softmax n'est jamais appliqué dans la passe avant. La raison est que presque tout ce dont nous avons besoin est le **logarithme** d'une probabilité, et que calculer un softmax puis en prendre le logarithme est numériquement mauvais : l'exponentielle peut déborder vers le haut, et une probabilité très petite devient zéro, dont le logarithme est moins l'infini. La fonction `F.log_softmax` calcule \(\log \pi\) en une seule étape stable, en soustrayant le maximum avant d'exponentier. Gardez donc la règle suivante : **les sorties brutes circulent, le softmax ne s'applique qu'au moment de l'échantillonnage, et le logarithme ne s'obtient jamais en composant les deux.**

{{% comment %}}SOURCE: LAPAN ch.11 p.335{{% /comment %}}

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class ReseauPolitique(nn.Module):
    """Deux couches, une sortie par action, et ces sorties sont des LOGITS."""

    def __init__(self, taille_obs: int, n_actions: int, largeur: int = 128):
        super().__init__()
        self.corps = nn.Sequential(
            nn.Linear(taille_obs, largeur), nn.ReLU(),
            nn.Linear(largeur, n_actions),
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        # Aucun softmax ici : la sortie n'est pas normalisee, et c'est voulu.
        return self.corps(obs)


def choisir_action(reseau: ReseauPolitique, obs: torch.Tensor) -> int:
    """On ECHANTILLONNE dans la distribution, on ne prend pas son argmax."""
    with torch.no_grad():
        logits = reseau(obs.unsqueeze(0))
        probs = F.softmax(logits, dim=1)
    return int(torch.multinomial(probs, num_samples=1).item())
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(h(s,a,\theta)\) | préférence numérique de l'action \(a\) | la sortie de `self.corps`, c'est-à-dire `logits` |
| \(\pi(a \mid s,\theta)\) | politique paramétrée | `probs`, de forme `(1, n_actions)` |
| \(\theta\) | paramètres de la politique | `reseau.parameters()` |
| \(A_t \sim \pi(\cdot \mid S_t,\theta)\) | action échantillonnée | la valeur de retour de `choisir_action` |
| \(\log \pi(a\mid s,\theta)\) | logarithme de la probabilité | `F.log_softmax(logits, dim=1)`, jamais `probs.log()` |

Notez le `torch.no_grad()` au moment du choix de l'action : c'est la leçon de la semaine 7 appliquée sans réfléchir, parce qu'elle s'applique ici exactement comme là-bas. Le réseau servira trois fois dans la semaine, et une seule de ces trois utilisations a besoin de gradients.

> [!TIP]
 **Un réflexe à prendre dès maintenant.** Quand une politique paramétrée se comporte mal, la première chose à regarder n'est pas la perte, c'est la distribution elle-même. Affichez \(\pi(\cdot\mid s)\) sur quelques états, au début et après quelques milliers de pas. Si elle est presque uniforme au début, le réseau est correctement initialisé. Si une action est déjà à 0,99 après mille pas, votre pas d'apprentissage est trop grand et la politique a déjà cessé d'explorer. Vous venez de diagnostiquer, en dix secondes, le problème numéro 3 de la section 8.5.

---
