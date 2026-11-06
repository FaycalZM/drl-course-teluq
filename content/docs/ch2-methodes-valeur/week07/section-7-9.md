---
title: "7.9 Les données, et le protocole de validation du cours"
weight: 10
---

## Une barre, une minute, quatre prix

Avant d'écrire l'environnement, il faut savoir exactement ce qu'il va lire.

Les données sont des cotations à la minute, ce qu'on appelle des **barres M1**. Une ligne de fichier par minute, et pour chaque minute **quatre prix** qui résument tout le mouvement intervenu pendant l'intervalle :

- l'**ouverture** : le prix au début de l'intervalle ;
- le **haut** : le prix maximal atteint pendant l'intervalle ;
- le **bas** : le prix minimal ;
- la **clôture** : le dernier prix de l'intervalle.

L'intervalle lui-même s'appelle une **barre** (*bar*), et c'est l'unité de temps de notre environnement : un pas de l'agent est une barre.

{{% comment %}}SOURCE: LAPAN ch.10 p.307{{% /comment %}}

{{< bookfig src="07-04.png" week="07" >}}

La **Figure 7-4** montre une barre unique avec ses quatre prix repérés. Prenez trente secondes dessus si vous n'en avez jamais vu : toute la section 7.10 manipule ces quatre nombres, et les confondre rend le code incompréhensible. La convention usuelle d'affichage d'une série de barres s'appelle un **graphique en chandeliers** (*candlestick chart*), où chaque barre est dessinée par un rectangle entre l'ouverture et la clôture, prolongé par deux traits vers le haut et le bas.

{{% comment %}}SOURCE: LAPAN ch.10 p.307-308{{% /comment %}}

Le fichier porte un cinquième nombre, le **volume échangé** : le nombre d'ordres d'achat et de vente passés pendant la barre. Son interprétation exacte dépend du marché, mais il indique dans tous les cas à quel point le marché était **actif** pendant cet intervalle. Nous le laisserons **désactivé** par défaut dans l'observation, et la section 7.10 dira où se trouve l'interrupteur.

{{% comment %}}SOURCE: LAPAN ch.10 p.307{{% /comment %}}

Le format est un fichier à valeurs séparées par des virgules, avec un en-tête nommant les colonnes dans l'ordre date, heure, ouverture, haut, bas, clôture, volume. Une ligne ressemble à ceci :

```text
<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
20160104,100100,1148.90000,1148.90000,1148.90000,1148.90000,0
```

Regardez cette ligne, elle est instructive : les quatre prix sont **identiques** et le volume est nul. C'est une minute pendant laquelle rien ne s'est échangé, et il y en a beaucoup. Un fichier d'une année complète pour un seul titre fait environ **130 000 lignes**, ce qui paraît énorme et ne l'est pas du tout : nous y reviendrons en section 7.13, parce que c'est la limite la plus sérieuse de tout l'exercice.

{{% comment %}}SOURCE: LAPAN ch.10 p.307{{% /comment %}}

Le jeu de données fourni avec le carnet du laboratoire contient **deux années** de cotations, et c'est précisément ce qui rend la section suivante possible.

{{% comment %}}SOURCE: LAPAN ch.10 p.307-308{{% /comment %}}

---

## Le protocole du cours : on ajuste sur le passé, on valide sur la suite

Nous avons deux années. Laquelle sert à entraîner, laquelle sert à valider ? La question a l'air anodine. Elle ne l'est pas, et la réponse est l'enseignement le plus **transférable** de toute la semaine, bien au-delà de la finance.

**La règle du cours, et elle n'a pas d'exception.** Une série temporelle se partage dans l'**ordre chronologique**. Le modèle est ajusté sur la période **la plus ancienne** et validé sur la période **la plus récente**. Avec nos deux années, 2015 et 2016 : **on entraîne sur 2015, on valide sur 2016.** Rien d'autre.

Et voici pourquoi, en des termes que vous pourrez réutiliser dans n'importe quel projet. Valider sur une période qui **précède** la période d'entraînement revient à sélectionner un modèle sur le futur et à le tester sur le passé. Trois conséquences, et je les détaille parce que chacune est un piège distinct.

**Conséquence 1 : on répond à la mauvaise question.** Ce qu'un praticien a besoin de savoir, c'est si un modèle ajusté sur ce qui était connu à une date donnée **survit à ce qui est arrivé ensuite**. Avec l'ordre inversé, la question devient : est-ce qu'un modèle qui a déjà vu le futur parvient à expliquer le passé ? C'est une question que personne ne pourra jamais poser en production, et dont la réponse n'a donc aucune valeur prédictive.

**Conséquence 2 : la fuite passe par le régime, et elle passe par vous.** Toute décision prise en regardant la période la plus récente, le moment où l'on arrête l'entraînement, le nombre de barres d'observation, la taille du réseau, transporte de l'information depuis une période censée ne pas avoir été vue. Et cette fuite n'est pas dans les tenseurs : elle est dans l'**expérimentateur**. Aucune vérification de code ne la détectera, parce qu'il n'y a pas de bogue. C'est une fuite de **procédure**.

**Conséquence 3 : c'est indétectable dans les métriques.** Un partage pris à l'envers produit des courbes parfaitement ordinaires : une perte qui descend, une récompense qui monte, un écart entraînement-validation d'allure plausible. Rien dans les chiffres ne vous alertera. Seul le **protocole** vous dit que le résultat est nul et non avenu, et c'est précisément pour cela que le protocole doit être **écrit avant** l'exécution, et non reconstitué après.

> [!IMPORTANT]
 **Généralisez, parce que la règle n'est pas une règle de finance.** Elle vaut pour **toute** série indexée par le temps : relevés de capteurs, suivi clinique de patients, demande d'un produit, trafic d'un serveur, consommation électrique. Deux formulations à retenir mot pour mot. **On ne mélange jamais une série temporelle avant de la partager.** Et : **on ne partage jamais une série temporelle au hasard.** Un partage aléatoire place des barres de la même heure des deux côtés de la frontière ; le modèle n'a alors plus à **prévoir**, il lui suffit d'**interpoler** entre deux points qu'il connaît déjà, et il y réussira brillamment pour une raison qui n'a rien à voir avec sa capacité de prévision.

Deux raffinements, dans l'ordre où je vous conseille de les adopter.

**D'abord, trois blocs plutôt que deux**, et c'est la recommandation du cours pour le jalon 2. Un bloc d'**entraînement**, le plus ancien, sur lequel on ajuste. Un bloc de **validation**, qui sert à **choisir** : l'instant d'arrêt, l'architecture, les hyperparamètres. Et un bloc de **test**, le plus récent, qu'on ne touche **qu'une seule fois**, à la fin, pour rapporter un chiffre. La raison du troisième bloc apparaîtra crûment en section 7.12 : dès qu'on choisit un modèle d'après ses résultats de validation, on a **détruit l'idée même de validation**, et il ne reste plus rien pour mesurer honnêtement.

{{% comment %}}SOURCE: LAPAN ch.10 p.324{{% /comment %}}

**Ensuite, la validation glissante** (*walk-forward*), qui est la version honnête de tout ceci. Au lieu d'une seule coupure arbitraire, on fait **glisser** le couple (ajustement, validation) le long de la série : ajuster sur janvier à juin, valider sur juillet ; ajuster sur février à juillet, valider sur août ; et ainsi de suite. On rapporte alors une **distribution** de résultats au lieu d'un nombre unique. C'est plus cher en calcul, et c'est la seule manière de savoir si votre résultat dépend de l'endroit où vous avez coupé. Notez la parenté avec la section 7.2 : plusieurs coupures et un intervalle, c'est le même raisonnement que plusieurs graines et un intervalle.

```python
# partage.py : le protocole, et il ne coute AUCUNE ligne de code nouvelle.
# On passe le fichier le plus ANCIEN a --data et le plus RECENT a --val.
#
#   python entrainer.py --data cotations_2015.csv --val cotations_2016.csv -r essai1
#
# Trois blocs, pour le jalon 2 :
def partager_trois_blocs(barres, part_entrainement=0.6, part_validation=0.2):
    """Partage CHRONOLOGIQUE. Aucun melange, aucun tirage aleatoire."""
    n = len(barres)
    i = int(n * part_entrainement)
    j = int(n * (part_entrainement + part_validation))
    return barres[:i], barres[i:j], barres[j:]      # ajuster / choisir / rapporter

# Ce qu'il ne faut JAMAIS ecrire sur une serie temporelle :
#   rng.shuffle(barres)                      -> melange le futur et le passe
#   train_test_split(barres, shuffle=True)   -> meme faute, mieux habillee
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| bloc d'ajustement | période la plus ancienne | premier retour de `partager_trois_blocs` |
| bloc de validation | période intermédiaire, sert à **choisir** | deuxième retour |
| bloc de test | période la plus récente, touchée **une fois** | troisième retour |
| frontière chronologique | indices `i` et `j`, jamais un tirage | `i`, `j` |
| fichier d'entraînement | la plus ancienne des deux années | `--data` |
| fichier de validation | la plus récente des deux années | `--val` |

Je souligne un point pratique, pour que la consigne ne paraisse pas plus lourde qu'elle ne l'est : le script d'entraînement prend déjà deux arguments distincts pour les données d'ajustement et les données de validation. Appliquer le protocole du cours ne demande donc **aucune modification de code**, seulement de passer les deux fichiers dans le bon ordre. C'est une consigne de deux secondes dont l'effet sur la validité du résultat est total, et c'est une bonne illustration du fait qu'un protocole expérimental ne se mesure pas au nombre de lignes qu'il coûte.

{{% comment %}}SOURCE: LAPAN ch.10 p.318{{% /comment %}}

> [!WARNING]
 **Un piège de vocabulaire qui fait perdre des points à chaque session, et il n'est pas spécifique à la finance.** Évaluer l'agent sur les **données d'entraînement** avec l'exploration désactivée, \(\varepsilon = 0\), **n'est pas** une évaluation hors échantillon. C'est une évaluation de la politique gloutonne sur la distribution d'entraînement, ce qui est utile, mais tout à fait autre chose. Le piège est aggravé ici par la mécanique de l'environnement : chaque épisode démarre à un **offset aléatoire** dans la série, ce qui donne l'impression rassurante de données « nouvelles » alors qu'elles proviennent de la même année. Un seul critère vaut : **hors échantillon signifie une période que l'entraînement n'a jamais vue**, et dans notre montage c'est l'autre année, point final.

{{% comment %}}SOURCE: LAPAN ch.10 p.312, p.320{{% /comment %}}

---
