---
title: "2.9 Suivi de l'entraînement avec TensorBoard"
weight: 10
---

## Regarder un entraînement plutôt que l'attendre

Je termine par un outil, et je le fais exprès en dernier, pour que vous arriviez à cette section avec une boucle d'entraînement en tête et une question : **comment je sais si ça marche ?**

Commençons par la phrase la plus honnête de la semaine, et elle vaut pour moi comme pour vous : même avec des outils modernes, votre code ne fonctionne presque jamais du premier coup, et c'est une chose à laquelle il faut vous habituer. Un entraînement d'apprentissage profond n'est pas un programme qui réussit ou qui échoue : c'est un processus qui dérive, plafonne, oscille ou s'effondre, et dont il faut **observer** le comportement.

{{% comment %}}SOURCE: LAPAN ch.3 p.101{{% /comment %}}

Que regarde-t-on ? La pratique est assez stable, et voici la liste que je vous recommande de suivre dès cette semaine. La **valeur de perte**, et pas seulement son total : ses composantes séparément, la perte de base d'un côté, les termes de régularisation de l'autre. Les résultats de **validation**, sur le jeu d'entraînement **et** sur le jeu de test, puisque c'est leur écart qui dit le surapprentissage. Des **statistiques sur les gradients et les poids**, c'est-à-dire exactement les quantités dont la section 2.6 vous a appris à redouter l'explosion ou l'extinction. Les **valeurs produites par le réseau** : en classification, l'entropie des probabilités prédites ; en régression, les prédictions brutes. Les **hyperparamètres** qui évoluent au cours du temps, pas d'apprentissage en tête. Et la **durée d'une époque**, qui est la donnée qui vous dira si votre expérience tient dans une soirée.

{{% comment %}}SOURCE: LAPAN ch.3 p.101{{% /comment %}}

---

## Trois lignes pour instrumenter un entraînement

TensorBoard est un petit service web écrit en Python. Vous lui indiquez un répertoire, il le surveille, et vous ouvrez un navigateur sur le **port 6006** pour voir les valeurs s'actualiser **en temps réel** pendant que le programme tourne. C'est particulièrement commode quand l'entraînement se déroule sur une machine distante, ce qui est exactement notre situation avec Colab. D'autres outils occupent la même niche, MLflow par exemple ; nous nous en tiendrons à celui-ci.

{{% comment %}}SOURCE: LAPAN ch.3 p.102{{% /comment %}}

Bonne nouvelle, il n'y a rien à installer : PyTorch écrit nativement le format de données attendu, et aucun paquet tiers n'est plus nécessaire. Tout tient dans `torch.utils.tensorboard`.

{{% comment %}}SOURCE: LAPAN ch.3 p.103{{% /comment %}}

```python
from torch.utils.tensorboard.writer import SummaryWriter

writer = SummaryWriter(comment="relu-lr1e-3")      # dossier unique sous runs/

for pas, (batch_x, batch_y) in enumerate(iterer_lots(donnees, taille_lot=32)):
    ...
    loss_t = loss_function(out_t, batch_y_t)
    loss_t.backward()
    optimizer.step()
    optimizer.zero_grad()

    writer.add_scalar("perte/entrainement", loss_t.item(), pas)   # nom, valeur, itération

writer.close()
```

{{% comment %}}SOURCE: LAPAN ch.3 p.103{{% /comment %}}

Toute l'interface utile est là, et elle tient en trois appels. `SummaryWriter()` crée un dossier unique sous `runs/` à chaque lancement, nommé avec la date, l'heure et le nom de la machine ; l'argument `log_dir` permet d'imposer le chemin, et l'argument `comment` d'ajouter un suffixe lisible, du genre `dropout=0.3` ou `forte-regularisation`. `add_scalar()` prend trois arguments, dans cet ordre : un nom, une valeur, et un numéro d'itération qui doit être un **entier**. Et `close()` termine proprement.

{{% comment %}}SOURCE: LAPAN ch.3 p.103{{% /comment %}}

| Ce que l'on veut | Appel | Remarque |
| --- | --- | --- |
| ouvrir un journal | `SummaryWriter(comment="...")` | un dossier par exécution, sous `runs/` |
| enregistrer un nombre | `add_scalar(nom, valeur, iteration)` | le troisième argument est un entier |
| sortir un scalaire du graphe | `loss_t.item()` | **jamais** le tenseur lui-même, voir section 2.1 |
| forcer l'écriture sur disque | `flush()` | l'écriture est périodique, toutes les deux minutes par défaut |
| fermer le journal | `close()` | à la fin du programme |

{{% comment %}}SOURCE: LAPAN ch.3 p.103-104{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur la troisième ligne de cette table.** Écrivez `loss_t.item()`, jamais `loss_t`. Un tenseur passé à `add_scalar` traîne derrière lui tout son graphe de calcul, que PyTorch doit alors conserver en mémoire. Dans une boucle de cent mille itérations, c'est une fuite de mémoire garantie, et le programme finit par être tué sans explication. C'est le même raisonnement qu'en section 2.1, et c'est pour cela que je vous ai demandé d'apprendre `item()` délibérément.

Pour lire les journaux, une commande et une adresse :

```text
tensorboard --logdir runs
```

Puis `http://localhost:6006` dans le navigateur. Sur un serveur distant, ajoutez `--bind_all` pour que le service accepte les connexions extérieures. La **Figure 2-9** montre ce que vous verrez pendant le laboratoire.

{{FIG:02-09 | nouvelle figure : capture de TensorBoard sur l'exécution du laboratoire}}

{{% comment %}}SOURCE: LAPAN ch.3 p.104{{% /comment %}}

> [!TIP]
 **La fonctionnalité qui va changer votre façon de travailler.** Comme chaque lancement crée son propre dossier, toutes vos exécutions apparaissent dans la liste **Runs**, à gauche, et vous pouvez les afficher ou les masquer pour **superposer leurs courbes**. C'est ainsi qu'on compare deux réglages : non pas en relisant deux fois des nombres dans la console, mais en regardant deux courbes sur le même graphique. Nommez donc vos exécutions avec `comment=`, sinon vous aurez huit courbes et aucune idée de laquelle est laquelle.

{{% comment %}}SOURCE: LAPAN ch.3 p.104{{% /comment %}}

TensorBoard ne se limite pas aux scalaires : il accepte des images, du son, du texte, des représentations vectorielles, et sait même afficher la structure du réseau. L'appel pour une image suit la même forme que pour un scalaire, en prenant soin de fabriquer une grille normalisée des échantillons à montrer.

```python
writer.add_image("echantillons", vutils.make_grid(images, normalize=True), pas)
```

{{% comment %}}SOURCE: LAPAN ch.3 p.104, p.110{{% /comment %}}

Nous n'en aurons pas besoin cette semaine, mais retenez que cette porte existe : en semaine 5, voir ce que le réseau reçoit vraiment en entrée vaut souvent mieux qu'une heure de relecture de code.
