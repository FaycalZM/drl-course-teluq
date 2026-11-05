---
title: "Laboratoire"
weight: 8
---

Un seul carnet, trois niveaux, un fil unique : **écrire CEM de bout en bout sur CartPole, puis le pousser jusqu'à ce qu'il casse**. Le laboratoire est formatif, il n'est pas noté ; le travail évalué de la semaine est le jalon 1, qui vient juste après et qui suppose ce carnet terminé.

Quatre points de contrôle traversent le niveau 1, et chacun se vérifie en une ligne, par une assertion ou une valeur affichée. Budget de calcul : **quelques minutes au total sur processeur central**. Le processeur graphique n'apporte strictement rien ici : les réseaux sont minuscules et le temps passe dans la simulation, pas dans le calcul matriciel.

---

## Niveau 1 : Implémentation guidée

**Objectif.** Écrire les cinq étapes de la section 3.3 et résoudre CartPole. À la fin de ce niveau, votre agent affiche « Résolu ! » et vous savez dire à quelle itération.

**Exercice 3.A : le réseau et l'échantillonnage.** Deux trous à combler.

```python
class ReseauPolitique(nn.Module):
    def __init__(self, n_obs: int, n_actions: int, n_cache: int = 128):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            nn.ReLU(),
            ...,          # À COMPLÉTER : la couche de sortie. Combien de sorties, et rien après ?
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pipe(x)


def choisir_action(net, obs):
    obs_v = ...           # À COMPLÉTER : un tenseur float32, et la dimension de lot
    probs = softmax(net(obs_v)).data.numpy()[0]
    assert abs(probs.sum() - 1.0) < 1e-5, "ceci n'est pas une distribution"
    return int(np.random.choice(len(probs), p=probs))
```

**Exercice 3.B : le générateur de lots.** Écrivez `engendrer_lots`. Une seule contrainte, et c'est le point de contrôle 4 : l'observation enregistrée dans `EtapeEpisode` doit être **celle qui a servi à choisir l'action**. Ajoutez cette vérification, qui coûte une ligne et vous épargnera une soirée.

```python
# dans la boucle, juste après avoir construit l'étape :
assert etapes[-1].observation is obs, "on enregistre obs, jamais next_obs"
```

**Exercice 3.C : le filtre et la boucle.** Écrivez `filtrer_elites` puis la boucle d'entraînement. Deux points de contrôle supplémentaires s'y vérifient : le seuil est bien un **percentile des retours du lot** et non une constante écrite en dur, et la perte reçoit bien des **sorties brutes**.

```python
assert isinstance(objective, nn.CrossEntropyLoss)
assert not isinstance(net.pipe[-1], nn.Softmax), "la dernière couche est linéaire"
```

**Attentes.**

* Le retour moyen du premier lot est de l'ordre de quelques dizaines, ce qui doit vous rappeler la mesure de la semaine 1 : c'est la même politique aléatoire, obtenue cette fois par des poids tirés au hasard.
* Le seuil des élites **monte** itération après itération. Tracez-le : c'est la courbe la plus informative des trois, et c'est elle qui restera désespérément plate sur FrozenLake, au jalon.
* « Résolu ! » apparaît entre la trentième et la soixantième itération, donc entre 480 et 960 épisodes joués. Si vous êtes très au-delà, relisez d'abord le point de contrôle 4.
* La perte ne descend **pas** régulièrement, et c'est normal : le jeu d'entraînement change à chaque itération, et il devient plus difficile à mesure que les élites se ressemblent. Une perte qui remonte alors que le retour monte n'est pas un bogue.

{{< colab url="TODO" label="Niveau 1 : CEM sur CartPole, les quatre points de contrôle" >}}

---

## Niveau 2 : Hyperparamètres et sensibilité

**Objectif.** Vérifier sur vos propres courbes la robustesse annoncée de la méthode, et trouver les deux réglages qui la cassent. Chaque exécution est courte : prévoyez quatre à six exécutions comparées, et une phrase de conclusion pour chacune.

**Protocole.**

1. **Le percentile.** Faites varier `PERCENTILE` sur 30, 50, 70, 90 en gardant tout le reste. Relevez le nombre d'itérations jusqu'à résolution, et la taille du jeu d'entraînement à l'itération 10. Expliquez le compromis : un percentile élevé donne des exemples meilleurs, mais combien ?
2. **La taille du lot.** Faites varier `BATCH_SIZE` sur 4, 16, 64. Comptez cette fois en **épisodes joués**, pas en itérations, sinon la comparaison est trompeuse.
3. **La capacité du réseau.** Passez `HIDDEN_SIZE` de 128 à 8, puis à 512. La méthode est annoncée robuste aux hyperparamètres : dites si vos mesures le confirment, et où se situe la limite.
4. **Le bogue silencieux, délibérément.** Enregistrez `next_obs` au lieu de `obs`, relancez à l'identique, et comparez les deux courbes de retour moyen. Décrivez ce que vous voyez en une phrase qui n'emploie pas le mot « bogue », mais qui dit ce que le réseau a appris.

**Attentes.**

* À `PERCENTILE = 90`, chaque itération ne retient qu'un ou deux épisodes sur seize : la mise à jour devient bruyante et l'entraînement, souvent, plus lent plutôt que plus rapide. À 30, les exemples sont médiocres et le seuil monte paresseusement. L'intervalle utile est large, et c'est précisément ce qu'on entend par « robuste aux hyperparamètres ».
* À `BATCH_SIZE = 4`, le percentile porte sur quatre nombres : le seuil devient très instable d'une itération à l'autre. Vous venez de rencontrer, sur un cas facile, le mécanisme exact qui fera échouer FrozenLake.
* Avec huit neurones cachés, l'agent progresse puis plafonne : la capacité du réseau finit par limiter la politique. Avec 512, le temps par itération augmente sans gain notable.
* Avec `next_obs`, l'entraînement **fonctionne encore**, plus lentement et moins loin. C'est le point important de tout le niveau : un bogue qui empêche tout est facile ; un bogue qui dégrade est ce qui vous coûtera du temps dans la vraie vie.

{{< colab url="TODO" label="Niveau 2 : percentile, taille de lot, capacité, bogue silencieux" >}}

---

## Niveau 3 : Extension créative, prédire avant de lancer

**Objectif ouvert.** Reprenez l'environnement que vous avez choisi et instrumenté au niveau 3 de la semaine 1. Avant d'y lancer quoi que ce soit, **prédisez par écrit** si CEM va y fonctionner, en vous appuyant sur les trois limites de la section 3.5. Puis vérifiez.

**Critères de réussite.**

* Une page de prédiction, écrite **avant** la première exécution et horodatée dans le carnet. Elle répond à trois questions : les épisodes sont-ils finis et courts ? la récompense arrive-t-elle en cours d'épisode ou seulement à la fin ? deux épisodes de qualité différente obtiennent-ils des retours différents ?
* Une mesure qui tranche, et elle ne demande aucun entraînement : jouez 200 épisodes avec une politique aléatoire et **tracez l'histogramme des retours**. Un histogramme étalé annonce que la méthode a une chance ; deux barres annoncent l'effondrement de la section 3.5.
* L'agent lancé tel quel, sans rien adapter d'autre que l'enveloppe d'observation si l'espace est discret. Vous notez l'écart entre votre prédiction et le résultat, et vous l'expliquez.
* Si votre environnement a un espace d'actions **continu**, dites pourquoi la méthode telle que nous l'avons écrite ne s'y applique pas, en une phrase qui parle du nombre de classes du classifieur.

**Piste de départ.** L'histogramme des retours d'une politique aléatoire est, dans tout ce cours, le premier diagnostic à poser sur un environnement inconnu. Il coûte trente secondes et il vous dit à quelle famille de méthodes vous avez affaire.

> [!TIP]
 **Mon message pour ce laboratoire.** Vous venez d'écrire, en moins de cent lignes, un agent qui apprend réellement. Savourez-le : c'est la première fois du cours, et la méthode est assez simple pour que vous en teniez chaque ligne dans votre tête. Mais ne confondez pas « ça marche » avec « j'ai compris ». La compréhension, cette semaine, se mesure à votre capacité d'annoncer **à l'avance** sur quel environnement ce même code va échouer. C'est très exactement ce que le jalon vous demande.
