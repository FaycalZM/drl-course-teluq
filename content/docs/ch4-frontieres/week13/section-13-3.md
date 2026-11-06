---
title: "13.3 Un espace latent, et deux chemins dont aucun ne suffit"
weight: 4
---

## Ce que l'agent voit, et ce qu'il ne voit pas

Posons le problème proprement, parce que la suite en dépend.

L'agent reçoit des images. Il ne reçoit pas l'état du système : il ne connaît ni la position angulaire exacte d'une articulation, ni sa vitesse, ni la masse du segment qu'elle porte. Il reçoit une grille de pixels, et une grille de pixels ne suffit même pas à déterminer un état, puisqu'une image ne contient aucune vitesse. C'est un **processus de décision markovien partiellement observable**, et ce cours en rencontre ici sa formulation complète. Quatre lois, dont trois appartiennent au monde et une à l'agent.

**L'intuition.** Un état caché du monde évolue selon ses propres lois ; il émet une observation et une récompense ; et l'agent, qui ne voit que les observations et se souvient de ses actions, doit en déduire quoi faire.

**L'équation.** Les quatre lois, dans l'ordre : transition, observation, récompense, politique.

$$
S_t \sim p(S_t \mid S_{t-1}, A_{t-1}), \qquad
O_t \sim p(O_t \mid S_t), \qquad
R_t \sim p(R_t \mid S_t), \qquad
A_t \sim p(A_t \mid O_{\le t}, A_{<t})
$$

{{% comment %}}SOURCE: PLANET éq. 1 p.2{{% /comment %}}

Les trois premières sont les lois du monde, et l'agent ne les connaît pas. La quatrième est ce qu'il cherche, et lisez bien son conditionnement : **la politique dépend de toutes les observations passées et de toutes les actions passées**, et non du seul \(O_t\). C'est la signature de l'observabilité partielle, et c'est ce qui va obliger le modèle à porter une mémoire. L'objectif reste celui de la semaine 1, l'espérance du retour :

$$
\max\ \E_p\!\left[\sum_{t=1}^{T} R_t\right]
$$

On suppose, sans perte de généralité, un état initial \(S_0\) fixé : il suffit d'absorber toute distribution initiale dans la première transition.

> [!IMPORTANT]
 **Une distinction typographique que je refuse de faire avec une police de caractères.** À partir d'ici, deux familles de lois cohabitent : les lois **vraies** du monde, que personne ne connaît, et les lois **apprises** du modèle, qui sont des réseaux de neurones. Il est d'usage de les distinguer par le style de la lettre, ce qui est illisible sur un écran et perdu dès qu'on recopie une équation à la main. Ce cours les distingue par l'**indice de paramètres** : \(p(\cdot)\) sans indice est la vraie loi, \(p_\theta(\cdot)\) avec indice est la loi apprise. Si vous voyez un \(\theta\), c'est un réseau ; s'il n'y en a pas, c'est le monde.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

---

## Mettre la dynamique dans un latent, et non dans les pixels

Voici la décision d'architecture, et elle est la bonne réponse à la deuxième difficulté de la section 13.2.

On pourrait apprendre un modèle qui, à partir d'une image et d'une action, prédit l'image suivante. On ne le fait pas, pour une raison de coût autant que de principe : un déroulement de douze pas demanderait alors de **générer douze images**, c'est-à-dire de faire douze passes dans un décodeur convolutif, pour chacune des mille suites d'actions que le planificateur veut évaluer. Douze mille images par décision. Et surtout, prédire une image, c'est dépenser de la capacité à prédire la texture du sol, qui n'a aucune importance pour le contrôle.

La décision est donc : **la dynamique vit dans un espace latent**, de dimension trente, et les images ne servent qu'à l'entraînement. Le modèle apprend trois composantes, auxquelles s'ajoute un encodeur.

**L'intuition.** Un état latent évolue selon sa propre loi apprise ; de cet état latent on sait prédire ce qu'on verrait, et ce qu'on gagnerait.

**L'équation.** Trois lois apprises, exactement parallèles aux trois premières lois du monde :

$$
Z_t \sim p_\theta(Z_t \mid Z_{t-1}, A_{t-1}), \qquad
O_t \sim p_\theta(O_t \mid Z_t), \qquad
R_t \sim p_\theta(R_t \mid Z_t)
$$

{{% comment %}}SOURCE: PLANET éq. 2 p.3{{% /comment %}}

Et il manque une quatrième pièce, qui n'est pas dans la liste parce qu'elle n'appartient pas au modèle génératif : l'**encodeur** (*encoder*) \(e_\theta(z_t \mid o_{\le t}, a_{<t})\), qui est le chemin **inverse**, celui qui transforme une observation en latent. Les trois lois ci-dessus savent descendre du latent vers l'image ; l'encodeur sait remonter de l'image vers le latent.

> [!IMPORTANT]
 **Le modèle d'observation fournit le signal d'entraînement et ne sert jamais à planifier.** C'est la phrase sur laquelle toute l'architecture tient en équilibre, et elle mérite trente secondes. Pourquoi le garder, si le planificateur ne s'en sert pas ? Parce que c'est lui qui force le latent à contenir quelque chose. Sans contrainte de reconstruction, un latent de dimension trente entraîné à prédire une seule récompense scalaire apprendrait à ignorer l'image. Et pourquoi ne pas s'en servir au moment de planifier ? Parce que le planificateur n'a besoin que de récompenses, que la récompense est une fonction du **latent**, et que générer une image coûterait mille fois plus cher pour une information qu'on n'utiliserait pas.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

Notez enfin ce que cette architecture **n'a pas** : ni réseau de politique, ni réseau de valeur. Après douze semaines d'acteurs, de critiques et de têtes jumelles, c'est désorientant. **La politique, ici, c'est le planificateur** : interrogé dans un état, il cherche une suite d'actions dans le modèle et renvoie la première. Il n'y a rien à entraîner du côté du comportement, et c'est précisément ce que la section 13.8 va remettre en question.

{{% comment %}}SOURCE: PLANET p.3{{% /comment %}}

---

## Deux chemins, et aucun des deux ne suffit

Nous arrivons au raisonnement le plus élégant de la première moitié de la semaine. Il tient en deux refus et une réconciliation.

**Premier candidat : un chemin purement déterministe.** C'est un réseau récurrent ordinaire, de ceux que vous connaissez : un état caché \(h_t\), une transition qui calcule \(h_{t+1}\) à partir de \(h_t\) et de l'action, et des sorties qui prédisent l'observation et la récompense. La transition est une fonction, donc **entièrement déterministe** : même état, même action, même suite, toujours.

Cela a deux conséquences, et la seconde est désastreuse. D'abord, le modèle **ne peut pas représenter plusieurs futurs possibles** : il en affirme un. Ensuite, et c'est le point à retenir, **il devient facile pour le planificateur d'exploiter ses inexactitudes**. Souvenez-vous de l'avertissement de la section 13.2 : le planificateur cherche les endroits où le modèle promet. Un modèle déterministe promet sans réserve, et il promet en particulier dans les régions où il n'a rien appris. Le planificateur y trouve des suites d'actions magnifiques, qui ne valent rien dans le monde réel.

**Second candidat : un chemin purement stochastique.** C'est un modèle à espace d'états classique : à chaque pas on **tire** le nouvel état latent dans une loi apprise. Le modèle représente alors naturellement plusieurs futurs, puisqu'il en échantillonne un à chaque fois.

Mais il perd autre chose, et c'est fatal dans un environnement partiellement observable : **il devient difficile de retenir une information sur plusieurs pas de temps**. Chaque pas repasse l'état par un tirage aléatoire ; une information présente à l'instant \(t\) doit survivre à une dizaine de tirages successifs pour être encore disponible à l'instant \(t+10\). Or une tâche partiellement observable exige exactement cela : se souvenir de ce qu'on a vu, parce qu'on ne le voit plus.

> [!NOTE]
 **Et voici la réserve honnête sur cet argument, celle qu'il faut enseigner avec lui.** Rien n'interdit **en principe** à un modèle purement stochastique de résoudre le problème : il suffirait qu'il apprenne à mettre certaines de ses variances à zéro, ce qui rendrait les composantes correspondantes déterministes et donc capables de porter une mémoire. La loi est dans la famille de modèles ; elle est représentable. Seulement **l'optimisation ne la trouve pas**. C'est une distinction que ce cours a déjà faite en semaine 7, à propos de l'approximation de fonction : « représentable » et « trouvable par descente de gradient » sont deux propriétés différentes, et c'est la seconde qui décide de ce qui marche.

{{% comment %}}SOURCE: PLANET p.4{{% /comment %}}

**La réconciliation : les deux chemins, côte à côte.** On ne choisit pas. L'état du modèle est **scindé** en deux parts qui avancent ensemble : une part déterministe \(h_t\), portée par une cellule récurrente, et une part stochastique \(Z_t\), tirée à chaque pas dans une loi qui dépend de \(h_t\). La première assure la mémoire longue ; la seconde assure la multiplicité des futurs. Et c'est tout l'argument.

**L'équation.** La transition devient quatre lignes, la première étant une fonction et les trois autres des lois :

$$
h_t = f_\theta(h_{t-1}, Z_{t-1}, A_{t-1}), \qquad
Z_t \sim p_\theta(Z_t \mid h_t)
$$

$$
O_t \sim p_\theta(O_t \mid h_t, Z_t), \qquad
R_t \sim p_\theta(R_t \mid h_t, Z_t)
$$

{{% comment %}}SOURCE: PLANET éq. 4 p.4 (vérifié sur image de page){{% /comment %}}

Cette architecture scindée porte un nom, qu'il vaut la peine de connaître parce qu'il dit exactement ce qu'elle est : un **modèle à espace d'états récurrent** (*recurrent state-space model*), c'est-à-dire un modèle à espace d'états auquel on a ajouté une part récurrente.

Lisez la première ligne lentement. La cellule \(f_\theta\) reçoit **trois** entrées : son propre état précédent, le **latent tiré** au pas précédent, et l'action. C'est ce qui couple les deux chemins : la part stochastique nourrit la part déterministe, et la part déterministe conditionne la loi de la part stochastique. Et notez que \(h_t\) est la seule chose qui traverse le temps sans être rééchantillonnée : la chaîne déterministe existe pour que le modèle puisse accéder non seulement au dernier état mais à **tous les états précédents**, de façon déterministe.

{{% comment %}}SOURCE: PLANET p.4{{% /comment %}}

{{< bookfig src="13-01.png" week="13" >}}

La **Figure 13-1** dessine les trois graphes côte à côte, avec la convention habituelle : un **carré** pour une variable déterministe, un **cercle** pour une variable tirée, un trait **plein** pour une dépendance du modèle génératif et un trait **pointillé** pour une dépendance d'inférence, c'est-à-dire pour le chemin de l'encodeur. Les deux premiers panneaux sont les deux refus, le troisième est la réconciliation, et vous y verrez les deux rangées superposées : les carrés en haut, les cercles en bas, et les flèches qui passent de l'une à l'autre dans les deux sens.

---

## Le code de la transition, et l'ablation qui ferme le débat

**Le code.** Un pas du modèle, dans ses deux régimes. Regardez bien qu'il y a **deux** lois sur le latent : la loi **a priori**, qui ne connaît que \(h_t\), et c'est celle qu'on utilise pour imaginer ; et la loi **a posteriori**, qui voit en plus l'observation, et c'est l'encodeur. Pendant l'entraînement on dispose des deux ; pendant la planification, seule la première est disponible, puisqu'il n'y a pas d'observation future.

```python
import torch
import torch.nn as nn


class ModeleScinde(nn.Module):
    """Un pas de transition a deux chemins : h deterministe, z stochastique."""

    def __init__(self, dim_z=30, dim_h=200, dim_a=1, dim_enc=1024):
        super().__init__()
        self.cellule = nn.GRUCell(dim_z + dim_a, dim_h)          # f_theta
        self.tete_prior = nn.Sequential(                          # p_theta(z | h)
            nn.Linear(dim_h, 200), nn.ReLU(), nn.Linear(200, 2 * dim_z))
        self.tete_post = nn.Sequential(                           # e_theta(z | h, o)
            nn.Linear(dim_h + dim_enc, 200), nn.ReLU(), nn.Linear(200, 2 * dim_z))
        self.dim_z = dim_z

    @staticmethod
    def _loi(sortie):
        moyenne, brut = sortie.chunk(2, dim=-1)
        ecart = torch.nn.functional.softplus(brut) + 0.1         # variance bornee en bas
        return torch.distributions.Normal(moyenne, ecart)

    def avancer(self, h, z, a, enc_obs=None):
        """h, z : etat du modele au pas precedent. a : action jouee.
        enc_obs : observation encodee, ou None si l'on imagine.
        Rend le nouvel h, la loi a priori, et la loi a posteriori si possible.
        """
        h = self.cellule(torch.cat([z, a], dim=-1), h)           # part deterministe
        prior = self._loi(self.tete_prior(h))
        if enc_obs is None:
            return h, prior, None                                # regime imagination
        post = self._loi(self.tete_post(torch.cat([h, enc_obs], dim=-1)))
        return h, prior, post                                    # regime entrainement
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(h_t\) | part déterministe, mémoire longue | `h` |
| \(Z_t\) | part stochastique, échantillonnée | `z`, puis `post.rsample()` |
| \(f_\theta(h_{t-1}, Z_{t-1}, A_{t-1})\) | la cellule récurrente, 200 unités | `self.cellule` |
| \(p_\theta(Z_t \mid h_t)\) | loi a priori, celle de l'imagination | `prior` |
| \(e_\theta(Z_t \mid h_t, O_t)\) | encodeur, loi a posteriori | `post` |
| \(O_t\) encodé | l'image passée dans un tronc convolutif | `enc_obs` |
| dimension du latent | trente, loi gaussienne diagonale | `dim_z=30` |

Le `enc_obs=None` du code n'est pas un détail d'ingénierie : c'est la **frontière entre entraînement et planification**, écrite en une ligne. Pendant l'entraînement, l'observation est là et l'encodeur corrige le latent. Pendant la planification, l'observation future n'existe pas, et le modèle doit se contenter de sa loi a priori. Tout ce que la section 13.4 va construire sert à faire en sorte que ces deux lois se ressemblent.

---

## Et l'ablation, qui tranche dans le sens inattendu

L'argument des deux chemins est joli. Est-il vrai ? La mesure existe, sur les six tâches de contrôle, et elle donne trois choses.

**Les deux parts comptent, sur les six tâches.** Aucune des deux n'est décorative.

**La part déterministe achète la mémoire sur plusieurs pas**, ce qui est exactement ce que l'argument annonçait.

**Et la part stochastique est encore plus importante : sans elle, l'agent n'apprend pas du tout.** Pas « moins bien » : pas du tout. C'est le résultat que je trouve le plus intéressant de la section, parce qu'il n'est pas celui qu'on attendrait d'un raisonnement sur la mémoire. Deux explications sont proposées, et toutes deux sont des hypothèses, non des démonstrations : d'une part les tâches sont **stochastiques du point de vue de l'agent**, puisque les états initiaux ne sont que partiellement observés, de sorte qu'un modèle incapable de représenter une incertitude est faux dès le premier pas ; d'autre part le bruit du tirage ajoute peut-être une **marge de sécurité** qui rend les suites d'actions retenues plus robustes, c'est-à-dire qui pénalise les plans qui ne marchent que si tout se passe exactement comme prévu.

{{% comment %}}SOURCE: PLANET p.7{{% /comment %}}

> [!TIP]
 **Retenez la seconde explication : c'est une idée transposable.** Un planificateur qui évalue ses candidats dans un modèle **bruité** préfère les plans qui survivent au bruit. Le bruit du modèle joue le rôle d'un régularisateur sur le plan, et il attaque directement la faiblesse du chemin déterministe, celle du planificateur qui exploite les inexactitudes. C'est la même intuition que le lissage de la cible de la semaine 9 : on ne demande pas à l'estimation d'être bonne en un point, on lui demande d'être bonne dans un voisinage.

---
