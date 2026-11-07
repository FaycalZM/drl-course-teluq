---
title: "Laboratoire"
weight: 8
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté. Ce qui est noté cette semaine, c'est le jalon 3, qui vient juste après et qui réutilise votre code du volet A. Faites donc le laboratoire d'abord, sans exception : le jalon suppose que PPO tourne déjà chez vous.

Les trois volets partagent **un seul programme**. Le volet A écrit PPO et le fait converger. Le volet B règle ses trois boutons, avec graines et intervalles, ce qui est l'exercice que la fin du module exige. Le volet C ajoute une méthode hors politique sur la **même** tâche et mesure le compromis de la section 10.6 à l'échelle d'un carnet.

**La tâche est `Pendulum-v1`, nommée avec son identifiant exact, et c'est celle de la semaine 9.** Je redonne les trois raisons, parce que la tentation de prendre le banc d'essai de la section 10.1 est forte et qu'elle vous coûterait votre semaine. Un épisode y dure quelques secondes ; l'espace d'actions y a **une seule dimension**, un couple dans \([-2,2]\) ; et aucun moteur physique externe n'est à installer. Les chiffres du tableau 10-1, eux, portent sur des exécutions de huit à vingt heures chacune, et l'exécution hors politique de la section 10.6 demande dix heures pour cinq millions de transitions. Ce sont des **repères à décrire**, jamais des tâches à donner.

{{% comment %}}SOURCE: LAPAN ch.16 p.497, p.517{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

**Je ne vous donne aucun score à atteindre, et c'est la même décision qu'en semaine 9.** Tous les nombres de cette semaine portent sur deux corps simulés à huit ou vingt-six dimensions d'observation, sur des dizaines de millions de pas. Aucun ne s'applique à un pendule à une dimension d'action. Interpoler entre eux pour vous donner une cible rassurante serait inventer un chiffre. Ce que j'attends est donc une mesure **relative et reproductible** : commencez par une **exécution pilote** d'une seule graine, lisez le retour qu'elle atteint, annoncez-le dans votre rapport comme votre cible, et comparez toutes vos configurations à cette cible sur les mêmes graines. Souvenez-vous que les récompenses de cette tâche sont négatives : votre courbe monte vers zéro, et une valeur prédite positive est un bogue de signe et non un apprentissage optimiste.

> [!WARNING]
 **Quatre pièges de ce laboratoire, et chacun coûte une soirée.** Premier piège, **le détachement de l'ancienne log-probabilité** : si `anciennes_logprob` n'est pas détachée à la collecte, votre rapport a un gradient dans son dénominateur et vous n'optimisez pas ce que vous avez écrit. Deuxième piège, **le décalage d'un élément** : les avantages sont plus courts d'une transition que la trajectoire, et une erreur d'indexation ici ne lève aucune exception, elle décale juste tous vos avantages d'un pas. Troisième piège, **l'échelle de l'action** : `Pendulum-v1` attend un couple dans \([-2,2]\) et votre acteur sort une tangente hyperbolique dans \([-1,1]\) ; multipliez par la demi-étendue, une fois, au bon endroit. Quatrième piège, **l'évaluation avec tirage** : un score mesuré en tirant dans la politique n'est pas le score de votre politique, et pour PPO comme pour la méthode hors politique l'évaluation se fait sur la moyenne, sans échantillonnage.

---

## Volet A : PPO écrit de bout en bout sur `Pendulum-v1`

**Objectif.** Écrire la boucle en treize étapes de la section 10.2, et la faire converger.

**Étape 1.** Les deux réseaux, acteur et critique, repris des fragments de la section 10.1. Gardez deux réseaux **séparés** et deux optimiseurs : c'est ce qui vous permettra d'avoir deux pas d'apprentissage, et le jalon vous le demandera. Gardez aussi l'écart-type **global**, un simple `nn.Parameter`, pour le volet A : le volet C introduira la version fonction de l'état.

**Étape 2.** La collecte d'une trajectoire longue. Sur cette tâche, quelques centaines à deux mille transitions suffisent. **Mémorisez la log-densité de chaque action au moment où vous la jouez**, et détachez-la. C'est la seule donnée supplémentaire que PPO demande par rapport à la semaine 8, et tout en dépend.

**Étape 3.** L'avantage généralisé, en une passe arrière, avec le fragment de la section 10.2. Puis la normalisation, moyenne retirée et division par l'écart-type.

**Étape 4.** La boucle d'époques et de minilots, avec la perte écrêtée. Partez de \(\epsilon = 0{,}2\), \(\lambda = 0{,}95\) et dix époques : ce sont les réglages de référence, et le volet B les fera varier.

**Étape 5.** L'évaluation, **sans tirage**, sur dix épisodes, tous les quelques milliers de pas.

**Trois vérifications arithmétiques avant d'interpréter la moindre courbe.** Premièrement, au tout premier minilot de la première époque, le rapport `ratio` doit valoir **exactement 1** pour tous les échantillons, à la précision machine près, puisque la politique n'a pas encore bougé. Si ce n'est pas le cas, vous avez un bogue dans la mémorisation de l'ancienne log-densité, et vous le trouverez en trente secondes plutôt qu'en trois heures. Deuxièmement, la moyenne de vos avantages normalisés doit valoir zéro et leur écart-type un. Troisièmement, la longueur du tableau d'avantages doit valoir exactement la longueur de la trajectoire moins un.

**Le diagnostic de la semaine, et il est à produire ici.** Journalisez, pour chaque époque, deux quantités : la moyenne de \(\ln r_t(\theta)\) sur le minilot, qui estime la divergence entre la politique courante et celle de la collecte, et la **fraction des échantillons écrêtés**, c'est-à-dire ceux dont le rapport est sorti de la bande. Tracez les deux en fonction du numéro d'époque.

**Attendu.** La courbe d'évaluation sur au moins trois graines avec intervalle, votre cible annoncée à partir de l'exécution pilote, et la figure du diagnostic ci-dessus avec une phrase de lecture : à partir de quelle époque votre dixième époque ne sert-elle plus à rien ?

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-10.ipynb" label="Volet A : PPO écrit de bout en bout sur Pendulum-v1" >}}

---

## Volet B : régler les trois boutons, avec graines et intervalles

**Objectif.** Mesurer l'effet des trois hyperparamètres propres à PPO, dans un protocole qui autorise une conclusion.

**Étape 1, un seul programme et trois drapeaux.** Votre code accepte `--eps`, `--lambda` et `--epoques`, et **rien d'autre ne change** entre deux exécutions. C'est la discipline de l'étude à une variable des semaines 6 et 7, appliquée une troisième fois, et c'est la condition pour que vos écarts veuillent dire quelque chose.

**Étape 2, les configurations.** Au minimum sept exécutions, sur les **mêmes** graines :

| Configuration | \(\epsilon\) | \(\lambda\) | Époques |
| --- | --- | --- | --- |
| Référence | 0,2 | 0,95 | 10 |
| Bande étroite | 0,1 | 0,95 | 10 |
| Bande large | 0,4 | 0,95 | 10 |
| Avantage à un pas | 0,2 | 0 | 10 |
| Avantage de la semaine 8 | 0,2 | 1 | 10 |
| Une seule époque | 0,2 | 0,95 | 1 |
| Vingt époques | 0,2 | 0,95 | 20 |

**Étape 3, le protocole, et il n'est pas négociable.** Au moins **trois graines** par configuration, cinq de préférence, le même jeu de graines partout, évaluation sans tirage, et un intervalle autour de chaque moyenne. Si vos intervalles se recouvrent, votre conclusion est « je ne mesure pas de différence », et c'est une conclusion que je préfère de loin à un classement inventé sur une exécution.

**Étape 4, les quatre questions auxquelles votre rapport répond.** La bande étroite ralentit-elle l'apprentissage chez vous, et de combien ? La bande large provoque-t-elle une instabilité visible, et à quel moment ? Que se passe-t-il à \(\lambda = 1\), et le résultat est-il cohérent avec l'affirmation de la section 10.2 selon laquelle vous retrouvez alors l'avantage de la semaine 8 ? Et enfin, la plus intéressante : au-delà de combien d'époques votre score cesse-t-il de s'améliorer, et ce seuil correspond-il à ce que votre diagnostic du volet A annonçait ?

**Attendu.** Le tableau des sept configurations avec graines et intervalles, vos quatre réponses, et une phrase disant lequel des trois boutons a eu le plus d'effet sur votre tâche.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-10.ipynb" label="Volet B : régler epsilon, lambda et le nombre d'époques, avec graines et intervalles" >}}

---

## Volet C : une méthode hors politique sur la même tâche, et le compromis mesuré

**Objectif.** Reproduire, à l'échelle d'un carnet, la **forme** de l'argument de la section 10.6 : moins d'observations, plus de calcul.

**Étape 1.** Ajoutez à votre socle une méthode hors politique. Vous avez deux routes honnêtes, et je ne tranche pas pour vous. La route courte consiste à reprendre votre code de la semaine 9 et à y ajouter les deux changements de la section 10.5 : le terme d'entropie dans la cible et dans l'objectif de l'acteur, et un écart-type **fonction de l'état** avec la correction de jacobien de la tangente hyperbolique. La route encore plus courte consiste à prendre l'implémentation de la bibliothèque haut niveau, qui vous donne les deux méthodes en deux lignes, et à concentrer votre travail sur la mesure. La seconde est parfaitement acceptable pour ce volet, à une condition : dites-le.

**Étape 2, les deux mesures, et elles doivent être tracées dans deux figures différentes.** Première figure : le retour en fonction du **nombre d'observations consommées**, pour les deux méthodes, mêmes graines. Seconde figure : le retour en fonction du **temps d'horloge**, pour les deux méthodes, sur le même matériel. Ce sont les deux axes de la Figure 10-4, et vous allez voir qu'ils ne racontent pas la même histoire.

**Étape 3, la lecture.** Répondez à trois questions. Laquelle des deux méthodes atteint votre cible avec le moins d'observations ? Laquelle l'atteint en le moins de temps ? Et la question qui ferme le module : sur **votre** matériel et pour **votre** tâche, laquelle choisiriez-vous, et qu'est-ce qui est rare chez vous ?

**Étape 4, la vérification d'honnêteté.** Indiquez votre matériel, et indiquez combien de mises à jour de réseau chaque méthode effectue par observation collectée. Ce rapport est l'explication mécanique de tout ce que vos deux figures montrent, et il tient en un nombre.

```python
# La solution courte, pour verifier votre implementation et pour le volet C.
# A executer APRES avoir ecrit la votre, jamais avant.
import time

from stable_baselines3 import PPO, SAC

RESULTATS = {}

for nom, Classe, pas in [("sur politique", PPO, 60_000),
                         ("hors politique", SAC, 20_000)]:
    debut = time.perf_counter()
    modele = Classe("MlpPolicy", "Pendulum-v1", seed=0, verbose=0)
    modele.learn(total_timesteps=pas)
    RESULTATS[nom] = (pas, time.perf_counter() - debut)
    # Puis evaluer SANS tirage, sur plusieurs graines, et tracer les DEUX axes :
    # retour contre observations, et retour contre temps d'horloge.

for nom, (pas, duree) in RESULTATS.items():
    print(f"{nom:>16} : {pas} observations en {duree:.0f} s")
```

> [!NOTE]
 **Les deux budgets de pas ci-dessus ne sont pas des cibles, et le rapport entre eux n'est pas une prédiction.** Je les donne pour que le fragment tourne, et je m'attends à ce que vous les changiez. Le point du volet est précisément de **mesurer** combien d'observations chaque méthode demande chez vous, et non de vérifier un rapport que je vous aurais soufflé. Si vous trouvez qu'il faut autant d'observations aux deux, c'est un résultat : votre tâche est peut-être trop petite pour que l'efficacité d'échantillon se voie, et le dire est une meilleure conclusion qu'un chiffre arrangé.

**Attendu.** Les deux figures, sur au moins trois graines, vos trois réponses, votre matériel, et le nombre de mises à jour par observation pour chacune des deux méthodes.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-10.ipynb" label="Volet C : une méthode hors politique sur la même tâche, et le compromis en deux figures" >}}

> [!TIP]
 **Mon message pour ce laboratoire.** Faites les volets dans l'ordre, et résistez à la tentation de sauter au volet C, qui est le plus spectaculaire. La raison est celle de toute la semaine : la perte de PPO ne vous dit rien sur la santé de votre entraînement, puisqu'elle est l'opposé d'un objectif que l'écrêtage aplatit volontairement. Votre seul diagnostic honnête est le couple que le volet A vous demande de tracer, la divergence et la fraction d'échantillons écrêtés. Le volet B n'est interprétable qu'avec ce diagnostic sous les yeux, parce qu'il explique pourquoi une époque supplémentaire cesse d'apporter quoi que ce soit. Et le volet C n'est interprétable qu'après le volet B, parce qu'une comparaison entre deux méthodes dont l'une est mal réglée ne mesure que le réglage.

---
