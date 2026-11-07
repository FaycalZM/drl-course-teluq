---
title: "Laboratoire"
weight: 14
---

Le laboratoire de cette semaine est **formatif**, comme ceux des semaines 4 et 5 : la semaine 6 ne porte aucun jalon. Mais lisez le paragraphe suivant avant de commencer, parce qu'il change la manière de travailler.

L'**exercice évalué** est le **volet C**, l'ablation. Et le volet C est, littéralement, la moitié du jalon 2 de la semaine prochaine, qui demande un réseau Q profond plus au moins deux extensions, avec des courbes comparées. Ce que vous produisez cette semaine, vous le rendrez à nouveau, augmenté, dans huit jours. Nommez donc vos fichiers et vos exécutions comme si vous deviez les relire, parce que vous devrez les relire.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

Budget de calcul. Tout le laboratoire tourne sur **CartPole**, et c'est une décision qu'il faut comprendre. Les figures de cette semaine viennent d'exécutions sur un jeu Atari de six à sept cent mille trames, qui prennent de l'ordre d'une heure chacune sur un processeur graphique. Quatre variantes, avec trois graines chacune, cela fait douze heures de calcul : c'est hors de portée d'une session, et ce n'est de toute façon pas là qu'est l'apprentissage. Sur CartPole, une variante converge en quelques minutes, et vous pourrez donc faire ce qui compte vraiment, c'est-à-dire **répéter**.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.8 p.262{{% /comment %}}

> [!WARNING]
 **Attention, et c'est la mise en garde la plus importante du laboratoire.** Je ne vous donne, dans aucun volet, le nombre de trames que vous devez obtenir, et ce n'est pas un oubli. Tous les chiffres de cette semaine, les 400 parties, les 260, les 250, les 330, le 170 trames par seconde, viennent d'exécutions sur Atari avec des hyperparamètres réglés spécifiquement pour chaque variante, au prix d'une journée de processeur graphique de recherche d'hyperparamètres. Ils ne prédisent **rien** de ce que fait une variante sur CartPole en trois minutes. Les attentes des volets ci-dessous sont donc **qualitatives** : un ordre entre les courbes, un signe, une forme. Si vos nombres ne ressemblent pas à ceux de la page, c'est normal ; si l'**ordre** de vos courbes est stable sur trois graines, vous avez un résultat.

{{% comment %}}SOURCE: LAPAN ch.8 p.240{{% /comment %}}

---

## Volet A : lire la bibliothèque, et prédire sa sortie

**Objectif.** Vérifier que vous avez compris la transition premier-dernier, sans entraîner quoi que ce soit. Dix minutes, et c'est le meilleur rapport de tout le laboratoire entre ce que l'exercice apprend et ce qu'il coûte.

**Protocole.** On installe la bibliothèque en deux lignes, `pip install stable_baselines3` puis `pip install ptan==0.8 --no-deps` (la raison est donnée en section 6.1, et une installation ordinaire échoue), et on construit l'environnement jouet de la section 6.3 : une observation qui compte de 0 à 4, une récompense égale à l'action jouée, un épisode de dix pas exactement, et un agent qui joue toujours l'action 1.

**Ce que je vous demande, et dans cet ordre.** D'abord, **écrivez sur une feuille** les douze premières transitions que la source d'expérience va produire avec `steps_count=2`, avec leurs quatre champs. Ensuite seulement, exécutez. Puis comparez, et expliquez en une phrase chacun des écarts, s'il y en a.

**Trois questions à traiter en une ligne chacune.**

* Pourquoi la plupart des transitions portent-elles une récompense de 2 ?
* Que vaut le champ d'état final à la fin d'un épisode, et pourquoi ce choix de représentation plutôt qu'un drapeau ?
* Avec `steps_count=2`, deux transitions sortent coup sur coup en fin d'épisode avec des récompenses différentes. Laquelle est laquelle, et pourquoi la seconde est-elle plus petite ?

**Attendu.** Vos prédictions, la sortie réelle, et vos trois réponses. Pas de courbe, pas d'entraînement.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-06.ipynb" label="Volet A : prédire la sortie d'une source d'expérience avant de l'exécuter" >}}

---

## Volet B : le socle commun, et la référence sur CartPole

**Objectif.** Réorganiser votre code de la semaine 5 en un socle importable, et produire la courbe de référence contre laquelle les quatre variantes seront lues.

**Protocole.** Vous repartez de votre volet A de la semaine 5, et vous le découpez en deux fichiers. Un `commun.py` qui contient la structure d'hyperparamètres, le réseau, le tampon, le dépliage d'un lot, la perte de référence, le calendrier de \(\varepsilon\) et la boucle d'entraînement. Et un `executer.py` de trente lignes qui choisit une variante par un argument de ligne de commande et lance l'entraînement.

Réglages de départ, qui sont ceux de votre laboratoire de la semaine 5 et qui ne changeront **pour aucune variante** : `GAMMA = 0.99`, `TAILLE_LOT = 64`, `TAILLE_TAMPON = 10_000`, `TAMPON_INITIAL = 1_000`, `PAS_APPRENTISSAGE = 1e-3`, `SYNCHRO_CIBLE = 500`, une décroissance de \(\varepsilon\) de 1,0 à 0,02 sur 10 000 trames, et un critère d'arrêt à une moyenne de 475 sur les cent derniers épisodes.

```python
# executer.py : une variante est un triplet (perte, classe de réseau, n).
VARIANTES = {
    "reference": (commun.perte_reference, commun.Reseau,     1),
    "n-etapes":  (commun.perte_reference, commun.Reseau,     3),  # seul n change
    "double":    (commun.perte_double,    commun.Reseau,     1),  # seule la perte
    "duel":      (commun.perte_reference, commun.ReseauDuel, 1),  # seul le réseau
}
```

**Trois points de contrôle à écrire comme des assertions**, parce qu'ils attrapent les trois bogues de structure de ce volet.

```python
# 1. Le socle est importé, pas recopié : une seule source de vérité.
assert commun.HYPERPARAMETRES["gamma"] == 0.99

# 2. Toutes les variantes partagent la MÊME graine, passée explicitement.
assert graine is not None

# 3. Le réseau duel a un nombre de paramètres COMPARABLE à la référence.
n_ref = sum(p.numel() for p in reseau_reference.parameters())
n_duel = sum(p.numel() for p in reseau_duel.parameters())
assert 0.8 < n_duel / n_ref < 1.25        # sinon la comparaison est truquée
```

**Attentes.**

* La référence résout CartPole, et vous notez combien de trames il lui faut, en moyenne sur **trois graines**.
* Une courbe de retour par épisode, lissée sur dix épisodes, avec l'axe horizontal en **trames** et non en épisodes.
* La troisième assertion ci-dessus doit passer. Si elle échoue, réduisez la largeur des couches cachées du réseau duel, comme la section 6.8 l'explique.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-06.ipynb" label="Volet B : un socle commun et la courbe de référence sur CartPole" >}}

---

## Volet C, évalué : l'ablation à quatre variantes

**Objectif.** Mesurer ce que chaque réparation apporte **sur votre problème**, et non sur celui des figures de cette page.

**Protocole.** Quatre configurations, le même socle, les mêmes hyperparamètres, les **mêmes trois graines**, le même nombre maximal de trames, le même lissage.

| Configuration | La seule chose qui change | Le défaut visé |
| --- | --- | --- |
| **(1) référence** | rien | la ligne de base |
| **(2) n étapes**, \(n = 3\) | `steps_count=3` et `gamma ** 3` dans la perte | nº5, la cible à un pas |
| **(3) double** | trois lignes dans la perte | nº1, le \(\max\) qui surestime |
| **(4) duel** | la classe du réseau, et rien d'autre | nº3, une seule tête |

**Attentes, et c'est ce que je corrigerai.**

* **Les quatre courbes sur un seul graphique**, axes nommés, légende, axe horizontal en trames, lissage identique. Et, puisque vous avez trois graines, tracez la **médiane** par configuration avec l'intervalle entre les exécutions extrêmes en bande claire. Une courbe par graine superposée fait un plat de spaghettis illisible.
* **Un tableau à quatre lignes** donnant, pour chaque configuration, le nombre de trames nécessaire pour atteindre une moyenne de 400, ou la mention « jamais atteint », et l'écart entre la meilleure et la pire des trois graines.
* **Une page écrite, et c'est le cœur de l'exercice.** Pour chacune des trois variantes : quel défaut nommé en section 5.9 elle répare, par quel mécanisme, ce que vous observez, et si l'écart que vous mesurez est plus grand ou plus petit que la dispersion entre vos graines. Les mots que j'attends dans ce texte sont « surestimation », « identifiable », « dépliage » et « dispersion ».
* **Une phrase que je veux lire textuellement**, et qui est la compétence de la semaine : dites ce qui, dans votre protocole, garantit que vous mesurez la variante et non autre chose.
* **Un piège à vérifier explicitement**, et il vaut des points : montrez par un test ou par une capture que la configuration (2) utilise bien \(\gamma^3\) dans sa perte et non \(\gamma\). C'est l'erreur qui invalide le plus souvent cette expérience, et elle ne lève aucune exception.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-06.ipynb" label="Volet C, évalué : quatre variantes, trois graines, une page d'analyse" >}}

---

## Volet D : rendre visibles deux effets invisibles

**Objectif.** Reproduire, sur CartPole, les deux protocoles de mesure des sections 6.7 et 6.8. C'est le volet qui vous apprendra le plus sur la manière dont on démontre quelque chose dans ce domaine.

**Protocole 1, la surestimation.** Avant l'entraînement, collectez **mille états témoins** en jouant une politique aléatoire, et mettez-les de côté. Pendant l'entraînement, toutes les mille trames, calculez la moyenne de \(\max_a Q_\theta(s,a)\) sur ces mille états et enregistrez-la. Faites-le pour la configuration (1) et pour la configuration (3), et tracez les deux courbes ensemble.

```python
# Les états témoins ne servent JAMAIS à l'apprentissage.
etats_temoins = torch.as_tensor(collecter_aleatoirement(env, 1000)).to(peripherique)

@torch.no_grad()
def valeur_moyenne_temoins(reseau) -> float:
    return float(reseau(etats_temoins).max(dim=1)[0].mean())
```

**Protocole 2, la contrainte duale.** Sur un ensemble d'états fixé, suivez pendant l'entraînement la moyenne des avantages produits par votre réseau duel, et la moyenne de sa tête de valeur. Tracez les deux.

**Attentes.**

* Deux graphiques, et **trois phrases** sur chacun.
* Sur le premier : la version ordinaire s'attribue-t-elle, à un moment, des valeurs qu'elle finit par démentir ? Et, question plus importante : pouvez-vous le conclure sur une seule graine ?
* Sur le second : la moyenne des avantages doit rester proche de zéro. Donnez son amplitude. Si elle dérive franchement, votre soustraction est mal branchée, et ce volet vient de vous faire gagner une soirée.
* **Une remarque sur la méthode, en deux phrases** : pourquoi ces deux mesures sont-elles indispensables, alors que la courbe de retour ne montre ni l'une ni l'autre ?

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-06.ipynb" label="Volet D : mille états témoins, et la contrainte de moyenne nulle mesurée" >}}

---

## Volet E, facultatif : les deux réparations les plus intrusives

**Objectif ouvert.** Ajouter au socle les deux réparations que le volet C n'a pas testées, et qui touchent les couches et le tampon.

**Piste 1, les réseaux bruités.** Écrivez la couche bruitée de la section 6.9, remplacez les deux couches linéaires de la tête de votre réseau, et **supprimez** tout le code de la stratégie \(\varepsilon\)-gloutonne : le sélecteur, le calendrier, les trois hyperparamètres. Vérifiez que `reseau.eval()` rend bien l'agent déterministe, et tracez le rapport signal sur bruit de vos deux couches pendant l'entraînement.

**Piste 2, le tampon priorisé.** Écrivez le tampon naïf de la section 6.10 et la perte pondérée qui va avec. Puis faites le seul réglage qui compte : comparez \(\alpha_{\mathrm{PER}} = 0\) et \(\alpha_{\mathrm{PER}} = 0{,}6\), et vérifiez que la première valeur reproduit **exactement** la courbe de la configuration (1), aux fluctuations de tirage près. Si elle ne la reproduit pas, votre tampon priorisé a un bogue, et ce test est le plus rapide pour le trouver.

**Critères de réussite.**

* Pour la piste 1 : la courbe de retour, la courbe du rapport signal sur bruit, et une phrase sur la question qui compte, à savoir si votre rapport remonte quelque part.
* Pour la piste 2 : la vérification \(\alpha_{\mathrm{PER}} = 0\), et une mesure en **deux** unités, le nombre de pas d'apprentissage et le temps écoulé. Si vos deux unités donnent deux conclusions opposées, vous venez de reproduire le résultat de la section 6.10 et je veux le lire.

> [!TIP]
 **Mon message pour ce laboratoire.** La semaine dernière, le volet évalué vous demandait de retirer une pièce pour voir ce qu'elle faisait. Cette semaine, il vous demande d'en ajouter quatre et de dire laquelle sert. C'est le même geste, dans l'autre sens, et c'est le geste central de tout ce domaine. Vous allez trouver, je le crois, que sur CartPole les écarts entre variantes sont du même ordre que l'écart entre deux graines de la même variante. Ce serait un excellent résultat, et il ne faut surtout pas le cacher : il signifie que vous avez mesuré votre dispersion avant de conclure, ce que beaucoup de publications de ce domaine ont longtemps omis de faire. Un résultat nul correctement établi vaut mieux qu'un écart impressionnant obtenu sur une seule exécution.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-06.ipynb" label="Volet E, facultatif : couches bruitées et tampon priorisé" >}}

---
