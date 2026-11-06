---
title: "Introduction"
weight: 1
---

## Le pas dont on ne se relève pas

Bonjour à toutes et à tous ! Nous arrivons à la dernière semaine du module 3, et je veux l'ouvrir sur un fait que les semaines 8 et 9 ont contourné sans jamais le nommer.

Depuis la semaine 8, toutes nos méthodes font la même chose avec le gradient qu'elles ont calculé : elles le multiplient par un pas d'apprentissage, elles l'appliquent, et elles espèrent que le pas était assez petit. La semaine 9 a passé six sections à empêcher une mise à jour d'aller trop loin, et vous l'avez peut-être lue comme une collection de précautions sans parenté : un réseau cible pour ralentir la cible, un délai pour ralentir la politique, un minimum pour borner un optimisme, un bruit écrêté pour aplatir un pic. Ces quatre précautions répondent en réalité à **une seule** question, que personne n'avait encore posée de front : de combien une politique a-t-elle le droit de changer en un pas ?

Voici pourquoi la question est sérieuse, et pourquoi elle est propre à l'apprentissage par renforcement.

Une politique paramétrée par un réseau profond est un objet **fortement non linéaire** : un petit déplacement dans l'espace des paramètres peut produire un très grand déplacement dans l'espace des comportements. Un pas trop grand peut donc détruire en une mise à jour la politique que mille mises à jour avaient construite. Jusqu'ici, rien d'exceptionnel : un apprentissage supervisé souffre du même défaut. Mais regardez ce qui se passe **ensuite**, et c'est là que les deux situations divergent définitivement.

En apprentissage supervisé, un mauvais pas se corrige au pas suivant, parce que le pas suivant travaille sur les **mêmes** données. Le jeu d'entraînement ne sait pas que vos poids se sont dégradés ; il vous présente les mêmes exemples, avec les mêmes étiquettes, et le gradient vous ramène. Ici, le pas suivant travaille sur des données que la politique abîmée a elle-même collectées. Une politique dégradée joue mal, donc elle visite de mauvais états, donc elle produit un lot d'expérience qui n'enseigne rien de ce qu'il faudrait réapprendre. La mise à jour suivante part de ce lot. Puis la suivante.

> [!IMPORTANT]
 **Voici la phrase charnière de la semaine, et je vous demande de la retenir mot pour mot.** On ne se relève pas d'une mauvaise mise à jour de politique par les mises à jour suivantes, parce que c'est la mauvaise politique qui fournit les échantillons dont ces mises à jour se nourrissent. Le mauvais pas ne dégrade pas seulement la politique : il **choisit les données** du pas d'après. C'est la seule boucle de ce cours où une erreur se nourrit d'elle-même sans aucun mécanisme de rappel, et elle porte un nom mérité, l'effondrement de la performance.

{{% comment %}}SOURCE: LAPAN ch.16 p.492-493{{% /comment %}}
{{% comment %}}SOURCE: SPINUP trpo/background{{% /comment %}}

La **Figure 10-2** dit cela en une image, et je vous demande de la regarder avant de lire la suite, parce que les six sections de la semaine en sont des conséquences.

{{< bookfig src="10-02.png" week="10" >}}

Lisez-la en deux temps. En haut, deux courbes de rendement en fonction de la politique. L'une est le vrai rendement, celui que vous mesureriez en jouant. L'autre est ce que vos anciens échantillons prédisent, c'est-à-dire l'estimation construite à partir du lot que la politique actuelle a collecté. Les deux courbes se touchent à la politique actuelle, et elles y ont même la même pente : votre estimation est juste là où les données viennent, et juste au premier ordre, ce qui est exactement ce qu'un gradient utilise. Puis elles s'écartent. Un petit pas reste dans la zone où l'estimation vaut quelque chose. Un grand pas atterrit là où l'estimation promettait un gain et où le vrai rendement s'est effondré. En bas, la boucle : politique abîmée, échantillons abîmés, pas suivant, et retour à la politique abîmée.

Maintenant la fausse sortie, celle que tout le monde propose en premier et qu'il faut savoir refuser proprement. Si le danger vient de la taille du pas, réduisons le pas d'apprentissage et avançons à tout petits pas. C'est faisable, et ce n'est pas absurde : cela réduit effectivement le risque d'effondrement. Mais cela ralentit la convergence dans la même proportion, et sur des tâches qui demandent déjà des dizaines de millions d'interactions, ralentir sensiblement la convergence n'est pas une gêne, c'est un abandon. Vous achetez de la sécurité en payant en temps, au tarif fixé par le plus mauvais pas que vous craignez, pendant toute la durée de l'entraînement.

{{% comment %}}SOURCE: LAPAN ch.16 p.493{{% /comment %}}

> [!TIP]
 **La reformulation qui débloque tout, et c'est le programme de la semaine en une ligne.** Le problème n'est pas que le pas soit grand dans l'espace des **paramètres** : c'est qu'il soit grand dans l'espace des **politiques**. Deux jeux de poids très proches peuvent décrire deux comportements très différents, et c'est précisément pourquoi un pas d'apprentissage, qui borne un déplacement de poids, ne borne rien de ce qui compte. Il faut donc arrêter de **réduire** le pas et commencer à le **contraindre** : mesurer directement l'écart entre la politique d'avant et la politique d'après, et refuser tout pas qui dépasse un budget fixé d'avance. Cet écart se mesure par une divergence entre deux distributions, la zone de l'espace des paramètres où il reste sous le budget s'appelle une **région de confiance** (*trust region*), et la famille de méthodes qui s'y tient porte ce nom.

{{% comment %}}SOURCE: SPINUP trpo/background{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.16 p.493{{% /comment %}}

La question à laquelle les quatre méthodes de la semaine répondent se formule alors exactement, et je la poserai une fois, ici, pour que vous la gardiez en tête à chaque section : comment prendre le plus grand pas d'amélioration possible avec les données dont on dispose, sans aller si loin que l'on provoque un effondrement de la performance ?

{{% comment %}}SOURCE: SPINUP ppo/background{{% /comment %}}

---

## Ce que vous allez lire, et dans quel ordre, parce que l'ordre est inversé

Voici la colonne vertébrale, une phrase par section, et une franchise au milieu.

La section 10.1 installe le banc d'essai : deux corps simulés, deux moteurs physiques, et trois écarts avec l'A2C de la semaine 8 qui comptent pour le laboratoire. Elle contient surtout deux pièges de mesure, et je les place en début de semaine parce que le jalon 3 vous demandera de comparer vos propres courbes à celles d'autrui. La section 10.2 présente **PPO** : le rapport entre la nouvelle et l'ancienne politique remplace la log-probabilité, et l'écrêtage de ce rapport fait que, au-delà d'une bande, la mise à jour **cesse de rapporter**. Trois équations, une image, et c'est la méthode que vous utiliserez. La section 10.3 présente **TRPO**, c'est-à-dire la théorie que PPO approche : un objectif de substitution sous contrainte de divergence, une expansion de Taylor, un gradient naturel, un gradient conjugué et une recherche linéaire. La section 10.4 présente **ACKTR**, qui promettait la courbure et a livré de l'instabilité. La section 10.5 présente **SAC**, qui n'appartient pas du tout à cette famille : hors politique, descendant du DDPG de la semaine 9, et qui achète son exploration en la plaçant dans l'objectif lui-même. Et la section 10.6 ferme le module 3 sur le compromis mesuré qui organise tout : des observations bon marché favorisent une méthode sur politique, des observations coûteuses justifient de payer en calcul pour une méthode hors politique.

> [!WARNING]
 **L'ordre de lecture est inversé par rapport aux dates, et je préfère vous le dire que de vous laisser le découvrir.** TRPO est de 2015, PPO de 2017 : la méthode que je vous présente en premier est la plus récente des deux, et elle est historiquement une **simplification** de la seconde. Je prends cet ordre pour deux raisons. La première est que PPO s'écrit en trois équations et que TRPO en demande une dizaine, de sorte que lire TRPO d'abord ferait passer une semaine difficile pour une semaine impossible. La seconde est plus intéressante : une fois PPO compris, TRPO se résume en une phrase, et cette phrase est la meilleure définition de PPO que je connaisse. Vous la lirez en section 10.3. Si l'ordre inversé vous gêne, lisez 10.3 avant 10.2 : rien ne s'y oppose, et vous y trouverez les dates et les filiations exactes.

{{% comment %}}SOURCE: LAPAN ch.16 p.500, p.509{{% /comment %}}

---

## Trois notations à surveiller, et le mot que je vous dois depuis la semaine 5

Cette semaine est la plus dense en symboles de tout le cours, et trois lettres y portent deux sens chacune. Je les déclare toutes les trois ici, et je les redéclarerai à l'endroit exact où chacune mord.

**La lettre \(r\) est prise.** À partir de la section 10.2, \(r_t(\theta)\) désigne le **rapport entre la nouvelle et l'ancienne politique** (*policy ratio*), qui est l'objet central de la semaine. La récompense d'une transition ne peut donc plus s'écrire \(r\) : je l'écris \(R\) dans une cible portant sur une seule transition, et \(R_{t+1}\) dans une somme indexée par le temps, ce qui est de toute façon la convention de la page « Notation » du cours depuis la semaine 1.

**La lettre \(\delta\) porte deux objets, et l'indice les sépare.** \(\delta_t\) est le **résidu temporel** de la semaine 4, la vieille erreur de différence temporelle, et c'est lui qui construira l'avantage en section 10.2. \(\delta\) sans indice, en section 10.3, est le **budget de divergence**, c'est-à-dire le nombre que la contrainte de TRPO ne doit pas dépasser. Rien ne les apparente. J'écris toujours le résidu avec son indice, et toujours le budget sans.

**La lettre \(\alpha\) porte trois objets dans ce cours, et deux d'entre eux arrivent cette semaine.** \(\alpha\) est, depuis la semaine 3, le **pas d'apprentissage**. En section 10.3, le coefficient de la recherche linéaire de TRPO s'écrit traditionnellement \(\alpha\) aussi : je l'écris \(\alpha_{\text{ls}}\) et je le nomme en français. En section 10.5, \(\alpha\) est le **coefficient d'entropie** de SAC, et là je garde la lettre, parce qu'elle apparaît dans toutes les équations de la méthode et qu'un renommage rendrait votre lecture de n'importe quelle implémentation plus difficile, pas plus facile. Dans la section 10.5, et seulement là, \(\alpha\) n'est pas un pas d'apprentissage.

Et une quatrième, qui n'est pas une collision mais une traduction : vous verrez ailleurs le résidu temporel écrit \(\sigma_t\). Le cours ne l'écrira jamais ainsi, parce que \(\sigma\) est, depuis la semaine 9, l'écart-type d'une politique gaussienne, et que les deux objets apparaîtront sur la même page en section 10.5. Le résidu temporel est \(\delta_t\), ici comme en semaine 4.

> [!NOTE]
 **Le mot « écrêtage » tout court devient disponible cette semaine, et c'était prévu depuis la semaine 5.** Le cours a employé jusqu'ici cinq écrêtages, et il les a tous écrits en entier, à chaque fois : l'**écrêtage de la récompense** en semaine 5, l'**écrêtage du gradient** en semaine 8, l'**écrêtage de l'action** et l'**écrêtage du bruit** en semaine 9, et le **double Q écrêté**, également en semaine 9. Cette discipline un peu lourde avait un but unique : réserver le mot seul pour aujourd'hui. À partir de la section 10.2, l'**écrêtage** (*clipping*), sans complément, désigne l'écrêtage du rapport entre les deux politiques, et rien d'autre. Si vous lisez « l'écrêtage » dans cette semaine, c'est de cela qu'il s'agit ; les cinq autres gardent leur nom complet.

{{% comment %}}SOURCE: source-assets/glossaire.md{{% /comment %}}

Je garde enfin l'écriture \(\ln\) pour le logarithme naturel, comme la semaine 9, et pour la même raison : les densités gaussiennes reviennent en section 10.5.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Expliquer pourquoi un mauvais pas de politique est **irrécupérable** en apprentissage par renforcement alors qu'il est récupérable en apprentissage supervisé, et nommer la boucle qui fait la différence.
- Dire pourquoi réduire le pas d'apprentissage est une réponse valide mais inacceptable au problème, et formuler la reformulation qui la remplace.
- Distinguer un déplacement dans l'espace des paramètres d'un déplacement dans l'espace des politiques, et dire laquelle des deux grandeurs la contrainte d'une région de confiance borne.
- Décrire le banc d'essai de la semaine, nommer ses deux corps simulés, et énoncer les deux raisons pour lesquelles des courbes obtenues sur deux moteurs physiques différents ne se comparent pas.
- Énoncer les trois écarts entre l'acteur-critique de cette semaine et celui de la semaine 8, et dire ce que chacun change dans le code.
- Expliquer ce qu'une variance de politique **globale**, indépendante de l'observation, permet et interdit.
- Écrire le rapport entre la nouvelle et l'ancienne politique, et dire de quel résultat de la semaine 3 il provient.
- Écrire l'objectif écrêté, et expliquer, pour un avantage positif puis pour un avantage négatif, **de quel côté** la courbe s'aplatit et pourquoi l'asymétrie est voulue.
- Énoncer ce que l'écrêtage retire exactement, en une formule et en une phrase, et dire pourquoi « l'écrêtage borne la taille du pas » est une lecture fausse.
- Dire ce qui peut encore se produire malgré l'écrêtage, et nommer la précaution d'implémentation que les mises en œuvre sérieuses ajoutent pour cela.
- Écrire l'estimation généralisée de l'avantage, identifier le paramètre qui l'interpole, et dire quelle valeur de ce paramètre redonne l'avantage de la semaine 8.
- Écrire le résidu temporel, et calculer l'avantage généralisé en **une seule** passe sur une trajectoire, parcourue à l'envers.
- Expliquer pourquoi le rapport entre les politiques autorise plusieurs époques d'entraînement sur une même trajectoire, alors que la semaine 8 jetait chaque transition après un pas.
- Énoncer le problème que TRPO résout, sous la forme d'une maximisation sous contrainte, et écrire la contrainte avec le bon qualificatif.
- Écrire la divergence de Kullback-Leibler correctement, et reconnaître l'entropie croisée quand on vous la présente sous un autre nom.
- Décrire les quatre mouvements qui transforment le problème de TRPO en un pas calculable, et dire ce que chacun approche.
- Expliquer pourquoi TRPO n'inverse jamais la matrice de courbure, et dire ce dont le gradient conjugué a besoin à la place.
- Résumer en une phrase le rapport exact entre PPO et TRPO.
- Énoncer ce qu'une méthode du second ordre cherche et ce qu'elle coûte, et nommer l'approximation sur laquelle ACKTR repose.
- Lire un résultat négatif : dire ce qu'un praticien attentif qui ne reproduit pas une méthode publiée démontre, et ce qu'il ne démontre pas.
- Expliquer pourquoi la régularisation par l'entropie de SAC change l'**objectif** et pas seulement l'exploration, et la distinguer de la prime d'entropie de la semaine 8.
- Écrire la cible de SAC et y montrer les trois objets qui viennent de la semaine 9 et le quatrième qui n'en vient pas.
- Expliquer ce que la reparamétrisation rend possible, et ce que la tangente hyperbolique finale change à la distribution de la politique.
- Lire un tableau de comparaison de méthodes : dire ce qu'une case sans nombre signifie, pourquoi une colonne peut devoir être attribuée à autre chose que son titre, et pourquoi aucune des cinq lignes ne gagne partout.
- Énoncer le compromis qui ferme le module 3, et le justifier par deux mesures et non par une préférence.
- Dire pourquoi ce tableau, à lui seul, impose plusieurs graines avec intervalles pour toute comparaison que vous publierez.

---

## Prérequis et outils

De la semaine 8, l'essentiel du vocabulaire : l'acteur et le critique, l'avantage, la prime d'entropie, le retour à \(N\) pas et le déroulement de l'équation de Bellman, la facture en échantillons d'une méthode sur politique, les environnements vectorisés, et le partage \(\theta\) pour l'acteur et \(\mathbf{w}\) pour le critique. La section 10.2 s'appuie directement sur le déroulement à \(N\) pas de la semaine 8 : l'estimation généralisée de l'avantage en est une moyenne pondérée, et c'est **la page de la semaine 8** qui fournit l'argument, non une source extérieure. De la semaine 9, trois objets reviennent intacts en section 10.5 : la politique gaussienne et sa log-densité, le tampon de rejeu avec ses réseaux cibles et la synchronisation douce, et le **double Q écrêté**, que le cours a dérivé en section 9.6 et qu'il ne redérivera pas. De la semaine 3, l'échantillonnage préférentiel et la divergence de Kullback-Leibler, qui sont littéralement l'objet de la section 10.2. De la semaine 7, le protocole de mesure à graines multiples avec intervalle, obligatoire depuis le jalon 2 et donc obligatoire ici sans que je le redemande.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les trois volets du laboratoire ; aucun ne dépasse une vingtaine de minutes sur un processeur graphique partagé |
| **Gymnasium** | `Pendulum-v1` pour toutes les mesures du laboratoire et du jalon, comme en semaine 9 |
| **PyTorch** | `torch.distributions.Normal`, `torch.exp` pour le rapport, `detach()` sur la log-probabilité ancienne, deux optimiseurs distincts, et un second appel à `backward()` si vous explorez la section 10.4 |
| **NumPy** | la passe arrière de l'avantage généralisé, qui s'écrit plus clairement en NumPy qu'en PyTorch |
| **Matplotlib** | les courbes du laboratoire, et la figure de variance du gradient exigée par le jalon 3 |
| **TensorBoard** | la divergence moyenne entre l'ancienne et la nouvelle politique à chaque époque, qui est le diagnostic propre à cette semaine |
| **Stable-Baselines3** | la solution courte du laboratoire, et le moyen le moins coûteux d'obtenir une référence sur politique et une référence hors politique sur la même tâche |
| **Page « Notation » du cours** | les trois collisions de la semaine y sont tranchées, et le résidu temporel y porte son nom depuis la semaine 4 |
| **Page « Glossaire » du cours** | vingt-cinq termes nouveaux, dont le mot « écrêtage » enfin libéré de son complément |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 10{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

---
