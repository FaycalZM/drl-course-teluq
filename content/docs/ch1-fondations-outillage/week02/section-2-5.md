---
title: "2.5 Fonction de perte, optimiseur, boucle d'entraînement"
weight: 6
---

## Huit lignes que vous allez réécrire treize fois

Nous avons un réseau qui transforme des entrées en sorties et qui sait calculer ses gradients. Il manque deux pièces pour que cela apprenne : quelque chose qui **mesure** l'erreur, et quelque chose qui **agit** sur les poids. Appliquons encore la double lecture.

---

## 1. L'intuition, et les deux pièces manquantes

Une **fonction de perte** (*loss function*) est une fonction de deux arguments, la sortie du réseau et la sortie désirée, qui renvoie **un seul nombre** : la distance entre ce que le réseau a produit et ce qu'on voulait. Ce nombre s'appelle la valeur de perte, et plus il est petit, mieux c'est.

{{% comment %}}SOURCE: LAPAN ch.3 p.98{{% /comment %}}

Un **optimiseur** (*optimizer*) prend les gradients des paramètres et modifie ces paramètres de façon à faire baisser la perte. C'est tout son rôle, et il est entièrement séparé de celui du réseau : l'un sait dériver, l'autre sait avancer.

{{% comment %}}SOURCE: LAPAN ch.3 p.99{{% /comment %}}

Les fonctions de perte vivent dans `nn` et sont elles-mêmes des sous-classes de `nn.Module`, ce qui est cohérent : ce sont des objets qu'on appelle. PyTorch en livre une vingtaine ; quatre suffisent pour tout ce cours.

| Perte | Ce qu'elle attend | Usage |
| --- | --- | --- |
| `nn.MSELoss` | des valeurs réelles | l'erreur quadratique moyenne, la perte de régression par défaut. **C'est celle du laboratoire et celle de la semaine 5** |
| `nn.BCELoss`, `nn.BCEWithLogits` | une probabilité, ou un score brut | l'entropie croisée binaire ; la seconde variante applique la sigmoïde elle-même et est plus stable numériquement |
| `nn.CrossEntropyLoss` | des scores bruts | classification multiclasse ; applique un LogSoftmax en interne, donc **pas de softmax dans le réseau** |
| `nn.NLLLoss` | des log-probabilités | la même chose, quand le réseau fournit déjà les logarithmes |

{{% comment %}}SOURCE: LAPAN ch.3 p.99{{% /comment %}}

> [!TIP]
 **Notez la troisième ligne, elle vous attend à deux semaines d'ici.** `nn.CrossEntropyLoss` attend des **scores bruts** et applique la normalisation en interne. Mettre un `nn.Softmax` dans le réseau **et** utiliser cette perte revient à normaliser deux fois : l'entraînement n'échoue pas, il ralentit et plafonne, ce qui est beaucoup plus difficile à diagnostiquer qu'une erreur franche.

Côté optimiseurs, quatre noms à connaître : **SGD**, la descente de gradient stochastique, avec son option d'inertie ; **RMSprop** ; **Adagrad** ; et **Adam**, qui combine les deux précédents et qui est le choix par défaut de ce cours. Tous partagent la même interface et se construisent à partir d'un itérable de tenseurs à modifier, c'est-à-dire, en pratique, du résultat de l'appel aux paramètres du module de plus haut niveau.

{{% comment %}}SOURCE: LAPAN ch.3 p.99-100{{% /comment %}}

---

## 2. L'équation

La perte du laboratoire est l'erreur quadratique moyenne. Pour un lot de \(n\) exemples, elle s'écrit, en notation du cours :

$$
L = \frac{1}{n}\sum_{i=1}^{n}\left(o_i - y_i\right)^{2}
$$

Et le pas d'optimisation le plus simple, celui de la descente de gradient, s'écrit avec le **pas d'apprentissage** \(\alpha\) :

$$
\mathbf{w} \leftarrow \mathbf{w} - \alpha\,\nabla_{\mathbf{w}} J
$$

Lisez cette flèche comme une affectation, pas comme une égalité : les poids d'après valent les poids d'avant, moins une fraction du gradient. Le signe moins est tout l'algorithme, puisque le gradient pointe vers la **montée** de \(J\) et que nous voulons descendre. Les optimiseurs plus élaborés ne changent pas la structure de cette ligne, ils changent la façon de calculer le pas effectif : Adam, par exemple, entretient pour chaque paramètre une estimation de l'échelle de ses gradients passés et adapte son pas en conséquence. C'est pour cela qu'un même \(\alpha\) ne veut pas dire la même chose d'un optimiseur à l'autre.

---

## 3. Le code : la boucle en huit lignes

Voici l'artefact le plus réutilisé de la semaine. Huit lignes, et vous les retrouverez, à peine retouchées, dans chaque laboratoire jusqu'à la semaine 15.

```python
net = ReseauQ(n_obs=4, n_actions=2).to(device)
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)

for batch_x, batch_y in iterer_lots(donnees, taille_lot=32):        # 1
    batch_x_t = torch.tensor(batch_x, dtype=torch.float32).to(device)  # 2
    batch_y_t = torch.tensor(batch_y, dtype=torch.float32).to(device)  # 3

    out_t = net(batch_x_t)                                          # 4
    loss_t = loss_function(out_t, batch_y_t)                        # 5
    loss_t.backward()                                               # 6
    optimizer.step()                                                # 7
    optimizer.zero_grad()                                           # 8
```

{{% comment %}}SOURCE: LAPAN ch.3 p.100{{% /comment %}}

Reprenons les huit étapes une par une, parce que chacune a sa raison d'être. **(1)** On itère sur les lots de données. **(2) et (3)** On convertit les tableaux du lot en tenseurs, du bon type, sur le bon périphérique : c'est la section 2.1 au travail. **(4)** On passe les entrées dans le réseau en appelant l'instance : propagation avant. **(5)** On calcule la perte entre la sortie et la cible. **(6)** `backward()` déroule le graphe et calcule les gradients de **toutes** les feuilles qui ont `requires_grad=True`, c'est-à-dire tous les paramètres du réseau. **(7)** L'optimiseur prend ces gradients et met les poids à jour. **(8)** On remet les gradients à zéro.

{{% comment %}}SOURCE: LAPAN ch.3 p.100{{% /comment %}}

Deux définitions au passage, parce que ce sont celles que tout le monde utilise sans les préciser. Une **époque** (*epoch*) est **une** itération sur la totalité du jeu de données. Quand les données ne tiennent pas en mémoire, ou simplement quand on veut mettre à jour les poids plus souvent, on les découpe en **lots** (*batches*) de taille égale, chacun portant des échantillons et les étiquettes correspondantes, les deux sous forme de tenseurs.

{{% comment %}}SOURCE: LAPAN ch.3 p.100{{% /comment %}}

---

## Pourquoi la ligne 8 n'est pas optionnelle

Il reste à expliquer la huitième ligne, et c'est la plus instructive des huit. Quand PyTorch calcule un gradient, il ne l'**écrit pas** dans `tensor.grad` : il l'y **ajoute**. On appelle cela l'**accumulation des gradients** (*gradient accumulation*), et ce n'est pas un défaut, c'est un choix de conception parfaitement justifié : si un même tenseur intervient plusieurs fois dans un calcul, par exemple une cellule récurrente appliquée à plusieurs entrées successives, les contributions doivent bien être **sommées**, puisque c'est ce que dit la règle de dérivation en chaîne.

{{% comment %}}SOURCE: LAPAN ch.3 p.100{{% /comment %}}

> [!WARNING]
 **Attention, c'est l'erreur silencieuse la plus classique de PyTorch.** Oubliez la ligne 8 et rien ne plante : les gradients du lot 2 s'ajoutent simplement à ceux du lot 1, ceux du lot 3 aux deux précédents, et votre réseau avance à grands pas dans une direction qui mélange tout l'historique. La perte se met à osciller ou à exploser, et vous chercherez un bogue d'apprentissage là où il y a un gradient non remis à zéro.

On peut appeler `zero_grad()` indifféremment sur le réseau ou sur l'optimiseur : l'effet est le même, puisque l'optimiseur agit sur les paramètres du réseau. Et la placer en début de boucle plutôt qu'en fin ne change rien d'important, du moment qu'elle est appelée **une fois par lot**. Je l'écris en fin de boucle dans ce cours, pour que l'ordre de lecture suive l'ordre causal : on mesure, on dérive, on avance, on efface l'ardoise.

{{% comment %}}SOURCE: LAPAN ch.3 p.100-101{{% /comment %}}

Un dernier mot sur la souplesse de ce schéma, parce qu'elle sera utile plus tard. Rien n'oblige à n'avoir qu'un réseau et qu'un optimiseur : on peut parfaitement faire travailler **deux** optimiseurs sur **deux** modèles à partir des mêmes données, chacun avec sa propre perte. Nous en verrons un exemple en section 2.8, et le schéma reviendra dès que deux réseaux devront être entraînés ensemble.

{{% comment %}}SOURCE: LAPAN ch.3 p.101{{% /comment %}}

---

## La table de correspondance de la semaine

Voilà la table à laquelle revenir chaque fois qu'un symbole du cours vous paraîtra abstrait. À gauche la notation du cours, à droite ce que vous tapez réellement.

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathbf{x}\) | l'entrée, ou le lot d'entrées | `batch_x_t` |
| \(y\) | la cible, fournie d'avance cette semaine | `batch_y_t` |
| \(\mathbf{o}\) | la sortie du réseau, une valeur par action | `out_t = net(batch_x_t)` |
| \(L\) | la valeur de perte sur le lot | `loss_t` |
| \(\mathbf{w}\) | tous les paramètres du réseau | `net.parameters()` |
| \(\nabla_{\mathbf{w}} J\) | les gradients de tous les paramètres | remplis par `loss_t.backward()`, lisibles dans `p.grad` |
| \(\alpha\) | le pas d'apprentissage | `lr=` du constructeur de l'optimiseur |
| \(\mathbf{w} \leftarrow \mathbf{w} - \alpha \nabla_{\mathbf{w}} J\) | un pas d'optimisation | `optimizer.step()` |
| \(\lambda\) | la force de la pénalité sur les poids | `weight_decay=` de l'optimiseur |
| *(aucun)* | effacer les gradients avant le lot suivant | `optimizer.zero_grad()` |

{{< colab url="TODO" label="Faire tourner la boucle en huit lignes dans Colab" >}}
