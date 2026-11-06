---
title: "14.6 Le modèle de récompense, et l'écart entre l'équation et le code"
weight: 7
---

## L'architecture, et trois écarts qu'il faut annoncer

Nous avons un jeu d'étiquettes et une équation. Il nous faut un réseau.

**Intuition.** Le modèle doit noter un couple observation-action. L'observation est une image en couleur ; l'action est un entier parmi dix-huit. On traite donc l'image par un tronc convolutif, on transforme l'action en vecteur à un bit actif, on **concatène** les deux représentations, et on fait passer le tout dans deux couches denses qui sortent un scalaire.

**L'architecture, pièce par pièce.** Quatre convolutions de seize canaux chacune : noyau 7 sur 7 au pas 3, puis 5 sur 5 au pas 2, puis 3 sur 3 au pas 1, puis 3 sur 3 au pas 1. Chacune est suivie de trois choses de la semaine 2 : une **normalisation par lots** (*batch normalization*), un **abandon de neurones** (*dropout*) à 0,5, et une activation linéaire rectifiée fuyante. Puis un aplatissement. Le vecteur d'action à un bit actif est alors concaténé, et la suite est dense : une couche linéaire vers soixante-quatre unités, une activation fuyante, et une couche linéaire vers un.

{{% comment %}}SOURCE: LAPAN ch.19 p.588{{% /comment %}}

**Le code.**

```python
import torch
import torch.nn as nn


class ModeleDeRecompense(nn.Module):
    """Note un couple (observation, action) par un scalaire.

    L'action entre explicitement, sous forme de vecteur a un bit actif.
    """

    def __init__(self, forme_obs, n_actions):
        super().__init__()
        self.n_actions = n_actions

        def bloc(e, s, noyau, pas):
            return [
                nn.Conv2d(e, s, kernel_size=noyau, stride=pas),
                nn.BatchNorm2d(s),
                nn.Dropout(0.5),
                nn.LeakyReLU(),
            ]

        self.tronc = nn.Sequential(
            *bloc(forme_obs[0], 16, 7, 3),
            *bloc(16, 16, 5, 2),
            *bloc(16, 16, 3, 1),
            *bloc(16, 16, 3, 1),
            nn.Flatten(),
        )
        taille = self.tronc(torch.zeros(1, *forme_obs)).shape[1]
        self.tete = nn.Sequential(
            nn.Linear(taille + n_actions, 64),
            nn.LeakyReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, obs, actions):
        # obs : (N, 3, 210, 160) ; actions : (N,) entiers
        traits = self.tronc(obs)
        chaud = nn.functional.one_hot(actions, self.n_actions).float()
        return self.tete(torch.cat([traits, chaud], dim=1)).squeeze(-1)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(o_t\) | observation, image couleur 210 sur 160 | `obs` |
| \(a_t\) | action, un entier parmi dix-huit | `actions` |
| le vecteur à un bit actif de \(a_t\) | encodage de l'action, concaténé aux traits | `chaud` |
| \(\hat r(o_t, a_t)\) | la récompense prédite pour ce couple | la sortie de `forward` |

**Et les formes de tenseur, qui règlent une question.** Pour un lot de soixante-quatre paires de segments de cinquante pas, les observations forment un tenseur \(64 \times 50 \times 3 \times 210 \times 160\) et les actions un tenseur \(64 \times 50 \times 18\).

{{% comment %}}SOURCE: LAPAN ch.19 p.589{{% /comment %}}

> [!WARNING]
 **Cette architecture est souvent présentée comme identique à celle de la formulation d'origine, et elle en diffère sur trois points plus un.** Les formes de tenseur ci-dessus le démontrent sans discussion possible. **Premier écart : la couleur.** Ici trois canaux, là des niveaux de gris. **Deuxième écart : la résolution.** Ici 210 sur 160, là 84 sur 84. **Troisième écart : l'empilement temporel.** Ici une seule trame par pas, là quatre trames empilées, ce qui est loin d'être neutre, puisque c'est l'empilement qui donne au réseau l'accès à la vitesse. **Et le point supplémentaire** : ici l'action est fournie explicitement au modèle, ce que la formulation d'origine ne précise pas. Comparez les deux architectures si vous voulez, mais ne les comparez pas ligne à ligne : elles ne voient pas la même chose.

---

## Entraîner sur deux cents étiquettes, et s'arrêter à temps

Ajuster un réseau convolutif sur quelques centaines d'exemples est une invitation au surapprentissage, et la chaîne s'en protège par le moyen le plus simple : une partition et un arrêt.

**Vingt pour cent des paires sont mises de côté** et ne servent jamais à la descente de gradient. L'entraînement s'arrête quand la perte évaluée sur cette partition réservée **ne s'améliore plus pendant quatre époques consécutives**, et le modèle conservé est celui qui a obtenu la meilleure perte sur cette même partition.

{{% comment %}}SOURCE: LAPAN ch.19 p.589-590{{% /comment %}}

> [!NOTE]
 **Une mise au point sur la règle d'arrêt, parce que deux versions en circulent.** On lit parfois que l'arrêt est déclenché par une **montée de la perte d'entraînement**. Ce n'est pas ce que fait le code : ce qui est surveillé, et ce qui déclenche l'arrêt comme la sauvegarde, c'est la perte sur les vingt pour cent **réservés**. Ce cours décrit donc la règle comme un **arrêt anticipé sur la partition réservée**, ce qui est la seule lecture compatible avec la règle de sauvegarde. La différence n'est pas académique : un arrêt sur la perte d'entraînement d'un réseau avec abandon de neurones à 0,5 se déclencherait pour du bruit.

Le coût de cette étape est dérisoire par rapport au reste : **une douzaine d'époques et quelques minutes** pour deux cents étiquettes. Sur une exécution journalisée, le chargement porte sur **cent quarante-neuf étiquettes et deux mille cinq cent trente-quatre chemins de segments**, et l'entraînement s'arrête à l'époque dix avec une meilleure perte de **0,02531** sur la partition réservée.

{{% comment %}}SOURCE: LAPAN ch.19 p.589-590{{% /comment %}}

Un mot sur ces cent quarante-neuf étiquettes, pour éviter un contresens : ce n'est pas en contradiction avec les cent étiquettes du premier tour. Le compte d'un tour et le compte total de la base sont deux choses différentes, et la base contient ce que les sessions précédentes y ont déposé. Ne mettez pas les deux nombres dans la même phrase sans dire lequel est lequel.

---

## Le code de la perte, et il ne calcule pas l'équation de la section 14.2

Nous arrivons à la double lecture la plus intéressante de ce cours, et je vais la conduire lentement.

Rappelons l'objectif énoncé, celui de la section 14.2 : une exponentielle normalisée **sur la paire**, puis une entropie croisée contre l'étiquette. Rappelons sa propriété : il ne dépend que de \(R_1 - R_2\).

Voici maintenant ce que fait le code. Il calcule les deux sommes \(R_1\) et \(R_2\), il les **empile côte à côte** dans un tenseur à deux colonnes, et il appelle l'entropie croisée binaire avec logits sur ce tenseur contre l'étiquette.

```python
import torch
import torch.nn.functional as F


def perte_implementee(r1, r2, y):
    """Ce que le code de reference calcule reellement.

    r1, r2 : (N, L) recompenses predites, pas a pas, pour chaque segment
    y      : (N, 2) etiquette humaine, (1,0) / (0,1) / (0.5,0.5)
    """
    R1 = torch.sum(r1, dim=1)            # (N,)  somme sur les L pas
    R2 = torch.sum(r2, dim=1)            # (N,)

    R = torch.hstack((R1.unsqueeze(-1), R2.unsqueeze(-1)))   # (N, 2)
    return F.binary_cross_entropy_with_logits(R, y)
```

{{% comment %}}SOURCE: LAPAN ch.19 p.589{{% /comment %}}

Prenez une minute sur la dernière ligne, parce que tout est là. `binary_cross_entropy_with_logits` applique une **fonction logistique indépendante à chaque élément** du tenseur qu'on lui passe, puis compare chaque résultat à l'élément correspondant de la cible. Sur un tenseur à deux colonnes, cela fait **deux classifications binaires séparées**, et non une comparaison entre les deux colonnes.

**L'équation réellement optimisée** est donc celle-ci, avec \(\varsigma\) la fonction logistique :

$$
\mathcal{L} = -\frac{1}{2} \sum_{i \in \{1, 2\}} \Big[\, y_i \log \varsigma(R_i) + (1 - y_i) \log\big(1 - \varsigma(R_i)\big) \Big], \qquad R_i = \sum_{t=1}^{L} \hat r\big(o^i_t, a^i_t\big)
$$

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\hat r(o^i_t, a^i_t)\) | récompense prédite, pas à pas, pour le segment \(i\) | `r1`, `r2` |
| \(R_i\) | somme prédite sur le segment \(i\) | `R1`, `R2` |
| \(y_i\) | étiquette humaine pour le segment \(i\) | `y[:, 0]`, `y[:, 1]` |
| \(\varsigma(\cdot)\) | la fonction logistique | implicite dans le suffixe `_with_logits` |
| les deux colonnes empilées | la cible à deux entrées indépendantes | `R` |
| \(\mathcal{L}\) | la perte moyenne sur le lot et sur les deux colonnes | la valeur retournée |

**Comparez les deux objectifs sur un seul point et la différence saute aux yeux.** L'objectif énoncé ne voit que \(R_1 - R_2\). L'objectif calculé voit \(R_1\) **et** \(R_2\), séparément, chacun comparé à sa propre étiquette. Il pousse la somme du segment préféré vers le haut et celle de l'autre vers le bas, **dans l'absolu**. L'échelle et le décalage de la récompense ne sont plus libres : ils sont fixés par la perte elle-même.

---

## Trois conséquences pratiques, et elles ne sont pas de même gravité

Je ne veux pas que vous reteniez « ce sont deux formules différentes ». Je veux que vous sachiez ce que la différence fait, et cela se dit en trois points.

**Première conséquence : une paire étiquetée « les deux sont bons » reçoit deux consignes différentes.** Sous l'objectif énoncé, \(y = (0{,}5\,;0{,}5)\) est satisfaite dès que \(R_1 = R_2\), **quelle que soit leur valeur commune**. Sous l'objectif calculé, la même étiquette exige que \(\varsigma(R_1) = \varsigma(R_2) = 0{,}5\), c'est-à-dire que **les deux sommes soient nulles**. Deux segments que la personne trouvait tous les deux excellents se voient donc assigner une récompense totale de zéro. Ce n'est pas ce que la personne a dit.

**Deuxième conséquence : un segment reçoit des cibles absolues contradictoires selon son partenaire.** Imaginez un segment moyen, apparié une première fois avec un mauvais segment, où il gagne, et une seconde fois avec un bon segment, où il perd. Sous l'objectif énoncé, les deux paires sont parfaitement compatibles : la première dit « au-dessus de celui-là », la seconde dit « en dessous de celui-ci », et un même nombre satisfait les deux. Sous l'objectif calculé, la première paire pousse sa somme vers le haut dans l'absolu et la seconde la pousse vers le bas dans l'absolu. Le modèle reçoit deux ordres contraires sur la même quantité, et il les moyenne.

**Troisième conséquence, et c'est la plus sournoise : la perte peut baisser en gonflant l'échelle.** L'entropie croisée binaire sur un logit décroît indéfiniment quand le logit part vers l'infini du bon côté. Or ce logit est une **somme sur cinquante pas**. Multiplier toutes les prédictions par dix multiplie le logit par dix, améliore la perte, et ne change rien à l'ordre des segments. Le modèle est donc incité à produire des récompenses par pas de plus en plus grandes, et l'échelle obtenue dépend de \(L\) plutôt que de quoi que ce soit d'intéressant.

---

## Le pont en une ligne, et le correctif d'un caractère

Pourquoi ces deux formes se ressemblent-elles assez pour qu'on les confonde ? Parce que l'objectif énoncé **est** une entropie croisée binaire. Simplement, elle porte sur un seul logit, et ce logit est une différence.

Faites la réduction vous-même, c'est deux lignes. Divisez le numérateur et le dénominateur de l'équation de la section 14.2 par \(\exp(R_2)\) :

$$
\hat P\big[\zeta^1 \succ \zeta^2\big] = \frac{e^{R_1}}{e^{R_1} + e^{R_2}} = \frac{1}{1 + e^{-(R_1 - R_2)}} = \varsigma(R_1 - R_2)
$$

Et reportez dans la perte de la section 14.2, en utilisant \(y_2 = 1 - y_1\) :

$$
\mathrm{perte}(\hat r) = - \sum_{D} \Big[\, y_1 \log \varsigma(R_1 - R_2) + (1 - y_1) \log\big(1 - \varsigma(R_1 - R_2)\big) \Big]
$$

C'est mot pour mot une entropie croisée binaire, **sur le logit unique \(R_1 - R_2\)** et contre la cible unique \(y_1\).

> [!IMPORTANT]
 **Le correctif tient en un caractère, et c'est pour cela qu'il faut savoir le voir.** Là où le code passe le tenseur empilé `R` et l'étiquette complète `y`, il suffit de passer **`R1 - R2`** et **`y[:, 0]`** pour que la fonction calcule exactement l'objectif énoncé. Même appel, même fonction de la bibliothèque, un signe moins et un indice de colonne. Je vous montre cela pour une raison qui dépasse la semaine : un écart d'une ligne entre une équation et son code ne se détecte pas en lisant la perte afficher des valeurs qui descendent. Elle descend dans les deux cas. Le seul moyen de le voir est de **raisonner sur ce dont la perte dépend**, et c'est exactement ce que le volet A du laboratoire vous fera faire, en vingt lignes et sans entraîner quoi que ce soit.

---

## Un fait atténuant, et deux qui ne s'atténuent pas

Je ne veux pas être alarmiste, parce que la chaîne **fonctionne** et que la section 14.8 va le montrer en chiffres. Faisons donc le bilan honnête de cet écart.

**Ce qui est atténué.** La récompense prédite ne part pas directement dans l'agent : elle est **normalisée** sur une fenêtre glissante avant d'y arriver, et nous écrirons cette normalisation dans un instant. Un décalage additif constant est donc largement lavé au moment de l'usage, et c'est la conséquence la moins grave des trois.

**Ce qui n'est pas atténué.** La dérive d'échelle, d'abord : une normalisation par la moyenne et l'écart-type recentre et remet à l'échelle, mais elle n'empêche pas le modèle d'avoir appris une géométrie déformée pendant l'entraînement, où les écarts entre segments sont écrasés par rapport à leur niveau absolu. Et la distorsion de l'étiquette « les deux sont bons », ensuite, qui est une erreur sur le **contenu** de l'information humaine et qu'aucune normalisation en aval ne peut défaire : deux excellents segments ont été enseignés comme valant zéro.

{{% comment %}}SOURCE: LAPAN ch.19 p.592-593{{% /comment %}}

> [!TIP]
 **La leçon de méthode, et c'est pour elle que cette section existe.** Vous lirez beaucoup de code dans votre vie professionnelle, et vous y trouverez des écarts de ce genre. La bonne réaction n'est ni de les taire, ni de conclure que tout est faux. Elle tient en trois gestes : **écrire les deux objectifs**, **dire de quoi chacun dépend**, et **chercher ce qui, en aval, compense ou non**. Ici le troisième geste sauve un tiers du problème et laisse les deux autres tiers debout. C'est une conclusion plus utile qu'un verdict, et c'est aussi ce que le jalon 4 attend de vous quand votre résultat ne ressemble pas à celui que vous attendiez.

---
