---
title: "7.8 Les trois décisions : observation, actions, récompense"
weight: 9
---

## Rien n'est donné, et c'est le sujet

Voici la phrase qui porte toute la seconde moitié de la semaine, et je vous demande de la lire deux fois.

Pour formuler un problème d'apprentissage par renforcement, il faut **trois** choses : une observation de l'environnement, un ensemble d'actions possibles, et un système de récompense. Dans toutes les semaines précédentes, les trois nous étaient **données**, et la mécanique interne de l'environnement nous était cachée. Nous ne sommes plus du tout dans cette situation.

{{% comment %}}SOURCE: LAPAN ch.10 p.305{{% /comment %}}

La récompense en particulier mérite d'être signalée, parce qu'elle choque un peu la première fois : elle **n'est pas donnée par un ensemble de règles strictes**. Elle est guidée par notre intuition et par notre connaissance du domaine. Ce n'est pas un relâchement de la rigueur, c'est la nature du travail : une récompense est une **définition de ce qu'on veut**, et il n'existe pas de procédure pour découvrir ce qu'on veut.

{{% comment %}}SOURCE: LAPAN ch.10 p.305{{% /comment %}}

Cette liberté est **simultanément une bonne et une mauvaise nouvelle**, et il faut tenir les deux. La bonne : vous pouvez donner à l'agent tout ce que vous jugez pertinent, y compris des données qui ne sont pas des prix, comme des statistiques économiques ou des dépêches d'actualité. La mauvaise : trouver un bon agent signifie désormais essayer **de nombreuses représentations de données**, et il n'est pas du tout évident, a priori, laquelle fonctionnera le mieux. La difficulté s'est déplacée de l'algorithme vers la représentation, et la représentation ne se démontre pas, elle s'éprouve.

{{% comment %}}SOURCE: LAPAN ch.10 p.305{{% /comment %}}

---

## Décision 1 : l'observation

Ce que l'agent voit, à chaque instant, est composé de trois blocs :

1. les **\(b\) dernières barres de prix**, chacune donnée par quatre nombres : ouverture, haut, bas, clôture ;
2. un **drapeau** indiquant qu'une action a été achetée il y a quelque temps, sachant qu'on n'en détient qu'une à la fois ;
3. le **profit ou la perte courante** sur cette position.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

Les deux derniers blocs ne sont pas des commodités : ils sont **indispensables**, et nous verrons en section 7.10 pourquoi. Sans eux, deux instants où les prix récents sont identiques mais où l'agent détient, ou non, une action, produiraient la même observation tout en exigeant des décisions différentes. La propriété de Markov serait perdue, et aucune des méthodes de ce cours ne s'appliquerait proprement.

---

## Décision 2 : les actions

Trois actions, et l'agent en choisit une par barre, c'est-à-dire une par minute :

- **ne rien faire** : attendre la barre suivante ;
- **acheter une action** : si une position est déjà ouverte, il ne se passe rien ; sinon la position est ouverte et la **commission de courtage** est payée ;
- **clôturer la position** : s'il n'y a pas de position, il ne se passe rien ; sinon la position est fermée et la commission est payée **une seconde fois**.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

Remarquez le traitement des actions **invalides** : elles ne sont pas interdites, elles ne lèvent pas d'erreur, elles ne sont pas pénalisées. Elles sont simplement **sans effet**. C'est un choix de conception très répandu et il mérite d'être nommé, parce qu'il a un coût : l'agent doit apprendre, par l'expérience, que l'action « acheter » ne sert à rien quand il détient déjà une action. Ce coût est faible ici, parce que l'information est dans l'état, et il serait prohibitif dans un espace d'actions plus riche.

---

## Décision 3 : la récompense, et deux schémas qui ne sont pas équivalents

Nous arrivons à la décision la plus délicate des trois, et à mon avis à l'endroit le plus instructif de la semaine.

Il y a deux manières naturelles de récompenser un gain de négociation.

**Schéma A, la récompense à la clôture.** On ne donne rien pendant la détention, et on verse **tout d'un coup** au moment où la position est fermée. Les commissions sont prélevées à l'achat et à la clôture.

$$
R_t = -\kappa \quad \text{à l'action \textsf{Acheter}}, \qquad
R_T = -\kappa + 100\left(\frac{c_T}{c_{\text{ouv}}} - 1\right) \quad \text{à l'action \textsf{Clôturer}}
$$

**Schéma B, la récompense par barre.** On verse à chaque pas, pendant toute la détention, le mouvement de prix de **cette** barre.

$$
R_{t+1} = 100\left(\frac{c_{t+1}}{c_t} - 1\right) \quad \text{tant que la position est détenue}
$$

Dans les deux expressions, \(c_t\) est le prix de clôture de la barre \(t\), \(c_{\text{ouv}}\) le prix d'entrée de la position, \(c_T\) le prix de clôture au moment de la fermeture, et \(\kappa\) la commission en pourcentage, par opération. Le facteur 100 fixe l'unité : les récompenses sont en **points de pourcentage**.

{{% comment %}}SOURCE: LAPAN ch.10 p.306, p.315{{% /comment %}}

Au premier regard, les deux schémas devraient donner le même résultat final, avec seulement des vitesses de convergence différentes. En pratique, **la différence peut être considérable**, et je veux que vous sachiez pourquoi, parce que c'est un raisonnement entièrement transférable à n'importe quelle conception de récompense.

Commençons par écarter une fausse piste, parce qu'elle est tentante. Les deux schémas couvrent **exactement le même intervalle de prix** : le schéma B commence à créditer à partir de la barre qui suit l'achat et s'arrête à la barre de clôture incluse, et le schéma A couvre le même trajet de \(c_{\text{ouv}}\) à \(c_T\). Il n'y a pas de barre manquante d'un côté ni de l'autre, et les commissions sont identiques dans les deux cas. La différence est ailleurs, et elle est triple.

{{% comment %}}SOURCE: LAPAN ch.10 p.315, image{{% /comment %}}

**Raison 1, l'arithmétique.** Une somme de rendements simples n'est pas le rendement composé. Formellement :

$$
\sum_{k=0}^{T-1}\left(\frac{c_{k+1}}{c_k} - 1\right) \ \neq \ \frac{c_T}{c_0} - 1
$$

et la raison en est élémentaire : les **produits** se télescopent, les **sommes** non. Prenons un exemple numérique pour que ce soit palpable. Deux barres consécutives à \(+10\,\%\) chacune. Le schéma B verse \(10 + 10 = \mathbf{20}\) points. Le schéma A verse \(100\,(1{,}1 \times 1{,}1 - 1) = \mathbf{21}\) points. Un point d'écart sur deux barres, et l'écart croît avec la durée de détention et avec l'amplitude des mouvements. **Les deux schémas ne définissent donc pas la même fonction objectif**, et un agent optimal pour l'un n'est pas optimal pour l'autre.

**Raison 2, l'actualisation.** Celle-ci est spécifique à l'apprentissage par renforcement, et c'est la plus facile à oublier. Le retour vu par l'agent n'est pas la somme des récompenses, c'est la somme **actualisée** :

$$
G_t = \sum_{k=0}^{\infty} \gamma^{k} R_{t+k+1}
$$

Avec \(\gamma < 1\), une somme unique versée au pas \(T\) est multipliée par \(\gamma^{T}\), tandis que le même mouvement étalé sur la durée de détention est actualisé terme par terme, chaque terme avec son propre exposant. Les deux retours diffèrent donc **même dans le cas où les totaux non actualisés coïncideraient**. Et l'effet n'est pas symétrique : plus la détention est longue, plus le schéma A est pénalisé par l'actualisation, donc plus l'agent entraîné sous A est incité à **clôturer tôt**. Le choix du schéma de récompense modifie le comportement souhaité, pas seulement la vitesse d'apprentissage.

**Raison 3, l'attribution du mérite et la variance.** Le schéma B produit une récompense **dense**, une à chaque pas ; le schéma A une récompense **parcimonieuse**, une à la fin d'une détention qui peut durer des centaines de barres. Vous connaissez déjà cette opposition : elle est la raison pour laquelle FrozenLake a résisté à la méthode d'entropie croisée en semaine 3. Une récompense dense facilite énormément l'attribution du mérite, parce que chaque décision reçoit un signal immédiat ; une récompense parcimonieuse exige que l'information remonte par amorçage à travers tout l'épisode, ce qui est plus lent et plus bruité.

{{% comment %}}SOURCE: LAPAN ch.10 p.306, p.315{{% /comment %}}

```python
# recompense.py : les DEUX schemas, dans une fonction pure et testable.
# C'est exactement ce que le volet B du laboratoire vous demande de verifier,
# sans entrainer quoi que ce soit.
KAPPA = 0.1          # commission, en pourcentage du prix, PAR OPERATION

def recompense_a_la_cloture(closes, kappa=KAPPA):
    """Schema A : tout verse au moment de la cloture."""
    c_ouv, c_fin = closes[0], closes[-1]
    return -kappa + (-kappa + 100.0 * (c_fin / c_ouv - 1.0))

def recompense_par_barre(closes, kappa=KAPPA):
    """Schema B : une recompense par barre pendant la detention."""
    total = -kappa                                  # commission a l'achat
    for precedent, courant in zip(closes[:-1], closes[1:]):
        total += 100.0 * (courant / precedent - 1.0)
    return total - kappa                            # commission a la cloture

# Deux barres a +10 % : 21 points d'un cote, 20 de l'autre, commissions mises a part.
serie = [100.0, 110.0, 121.0]
# recompense_a_la_cloture(serie) - (-2 * KAPPA)  ->  21.0
# recompense_par_barre(serie)    - (-2 * KAPPA)  ->  20.0
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(c_t\) | prix de clôture de la barre \(t\) | une entrée de `closes` |
| \(c_{\text{ouv}}\) | prix d'entrée de la position | `c_ouv` |
| \(c_T\) | prix de clôture à la fermeture | `c_fin` |
| \(\kappa\) | commission par opération, en pourcentage | `KAPPA` |
| \(R_t\) | récompense d'un pas, en points de pourcentage | les termes ajoutés à `total` |
| \(\gamma\) | facteur d'actualisation, qui sépare les deux schémas | hors de cette fonction, dans la perte |

> [!IMPORTANT]
 **La leçon à emporter, et elle ne concerne pas la finance.** Deux schémas de récompense qui décrivent le même objectif en français peuvent définir deux problèmes différents. Avant de choisir, posez-vous les trois questions de cette section : est-ce que mon agrégation est la bonne opération arithmétique ? est-ce que l'actualisation traite mes deux schémas de la même manière ? et est-ce que mon signal est dense ou parcimonieux ? Les trois questions se posent à chaque fois que vous concevez une récompense, dans n'importe quel domaine.

---

## La représentation des prix, et l'information qu'on accepte de détruire

Dernière décision de conception, et elle porte sur la forme des nombres plutôt que sur leur nature.

**Le souhait.** On veut un agent **indépendant du niveau absolu des prix**, un agent qui raisonne en termes de « l'action a monté de 1 % pendant la dernière barre » plutôt que de « l'action valait 1 148,90 ». La raison est simple et solide : des titres différents ont des prix très différents et des **motifs de mouvement** semblables. La discipline qui étudie ces motifs porte un nom, l'**analyse technique** (*technical analysis*), et l'hypothèse de travail de notre représentation est exactement la sienne : ce qui se répète, c'est la forme du mouvement, pas le niveau du prix.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

**La décision.** Chaque barre, qui arrive avec quatre nombres (ouverture, haut, bas, clôture), est convertie en **trois** nombres : le haut, le bas et la clôture exprimés en proportion de l'ouverture.

$$
h^{\text{rel}} = \frac{h}{o} - 1, \qquad l^{\text{rel}} = \frac{l}{o} - 1, \qquad c^{\text{rel}} = \frac{c}{o} - 1
$$

L'ouverture disparaît de l'observation, puisqu'elle est devenue le point de référence et vaut donc zéro par construction : quatre nombres deviennent trois, et l'échelle absolue a disparu. La transformation est inversible dès qu'on connaît l'ouverture, ce qui servira en section 7.10 :

$$
c = o\,(1 + c^{\text{rel}})
$$

{{% comment %}}SOURCE: LAPAN ch.10 p.314, image{{% /comment %}}

**Le coût de cette décision, et il faut le nommer.** La représentation relative **détruit** une information : les **niveaux de prix remarquables**. Les marchés ont tendance à réagir au voisinage de nombres ronds, et le seuil de 70 000 dollars pour un bitcoin en est un exemple typique, ainsi qu'au voisinage des points de retournement passés. Un agent qui ne voit que des pourcentages de variation ne peut pas savoir qu'il se trouve juste sous un tel niveau. Cette information est réellement perdue, pas simplement masquée.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

Alors pourquoi la détruire ? Parce que la normalisation est ici un **a priori**, pas une nécessité. Le réseau pourrait très bien apprendre seul cette transformation : il lui suffirait de soustraire un prix moyen, ce qu'une couche linéaire fait sans difficulté. En la lui fournissant toute faite, on ne lui donne aucune capacité nouvelle, on lui **simplifie la tâche** : il n'a plus à dépenser de capacité et d'échantillons pour redécouvrir une invariance que nous connaissons déjà. C'est exactement le rôle d'un biais inductif, vu en semaine 2, et c'est le même raisonnement qui justifie la convolution sur une image.

{{% comment %}}SOURCE: LAPAN ch.10 p.306{{% /comment %}}

> [!TIP]
 **Un bon réflexe pour toutes vos conceptions d'observation.** Chaque fois que vous normalisez, demandez-vous ce que la normalisation **efface**, et notez-le. Souvent la réponse est « rien d'utile », et c'est parfait. Parfois, comme ici, la réponse est une information réelle dont vous acceptez la perte en échange d'un apprentissage plus facile. Un échange assumé est une décision d'ingénierie ; un échange inaperçu est un bogue qui ne se manifestera que sur les données de validation.

---
