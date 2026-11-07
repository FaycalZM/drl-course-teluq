---
title: "Laboratoire"
weight: 11
---

Un seul carnet, trois niveaux, et un fil unique : **construire le réseau des semaines 4 à 15, et le regarder apprendre**. Le réseau a la forme de \(Q(s,a)\), une entrée qui est un vecteur d'état, une sortie par action, scores bruts sans softmax. Les cibles, elles, sont **fournies, fixes, et parfaitement sages** : nous faisons de la régression. D'où viennent les vraies cibles d'un réseau de valeurs est la question des semaines 4 et 5, et je vous demande de la laisser de côté aujourd'hui.

Trois règles partout, et ce sont celles des sections précédentes : un seul `torch.device` construit au début du carnet, un `item()` sur toute valeur journalisée, un `zero_grad()` par lot. Budget de calcul : **quelques minutes au total**, processeur graphique facultatif.

---

## Niveau 1 : Implémentation guidée

**Objectif.** Écrire le réseau, la boucle, et l'instrumentation. À la fin de ce niveau, vous avez une courbe de perte qui descend dans TensorBoard.

**Exercice 2.A : le réseau de la forme de \(Q(s,a)\).** Trois trous à combler.

```python
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ReseauQ(nn.Module):
    def __init__(self, n_obs: int, n_actions: int, n_cache: int = 64):
        super().__init__()
        self.pipe = nn.Sequential(
            nn.Linear(n_obs, n_cache),
            ...,                      # À COMPLÉTER : sans ceci, les trois couches n'en font qu'une
            nn.Linear(n_cache, n_cache),
            nn.ReLU(),
            ...,                      # À COMPLÉTER : la couche de sortie, et pas de softmax
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return ...                    # À COMPLÉTER : un seul appel suffit


net = ReseauQ(n_obs=4, n_actions=2).to(device)
print(net)
print(net(torch.randn(8, 4, device=device)).shape)   # attendu : torch.Size([8, 2])
```

**Exercice 2.B : les données et la boucle.** Les cibles sont fabriquées par une fonction fixe que je vous donne, et qui n'a rigoureusement aucun sens physique : c'est volontaire, elle est là pour être non linéaire et reproductible.

```python
def fabriquer_donnees(n: int, graine: int = 0):
    """n états à 4 composantes, et 2 cibles par état. Rien d'autre qu'une régression."""
    g = torch.Generator().manual_seed(graine)
    x = torch.randn(n, 4, generator=g)
    y = torch.stack([
        torch.sin(x[:, 0]) + 0.5 * x[:, 2],
        torch.cos(x[:, 1]) - 0.5 * x[:, 3],
    ], dim=1)
    return x, y


x_train, y_train = fabriquer_donnees(4096, graine=0)
x_valid, y_valid = fabriquer_donnees(1024, graine=1)

loss_function = ...        # À COMPLÉTER : la perte de régression de la section 2.5
optimizer = ...            # À COMPLÉTER : Adam sur les paramètres du réseau, lr = 1e-3

for epoque in range(30):
    for debut in range(0, len(x_train), 64):
        batch_x_t = x_train[debut:debut + 64].to(device)
        batch_y_t = y_train[debut:debut + 64].to(device)

        out_t = net(batch_x_t)
        loss_t = loss_function(out_t, batch_y_t)
        ...                # À COMPLÉTER : les trois lignes qui manquent, dans le bon ordre
```

**Exercice 2.C : l'instrumentation.** Ajoutez un `SummaryWriter`, enregistrez `perte/entrainement` à chaque lot et `perte/validation` à chaque époque, puis ouvrez TensorBoard. Nommez l'exécution avec `comment=`.

**Attentes.**

* `print(net)` affiche bien cinq blocs : trois couches linéaires et deux activations. Si vous n'en voyez que trois, vous avez oublié l'activation de l'exercice 2.A, et la suite du laboratoire sera instructive pour une mauvaise raison.
* La sortie a la forme `[8, 2]` : **deux** valeurs par état, une par action, et la dimension 0 est celle du lot.
* La perte d'entraînement descend franchement sur les premières époques, puis ralentit. La perte de validation suit la perte d'entraînement, à un léger décalage près : vous venez de voir un écart de généralisation, mesuré et non raconté.
* Si la perte reste obstinément plate, vérifiez dans cet ordre : l'activation manquante, l'ordre des trois lignes de la boucle, le `zero_grad()`.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-02.ipynb" label="Niveau 1 : le réseau, la boucle, TensorBoard" >}}

---

## Niveau 2 : Hyperparamètres et sensibilité

**Objectif.** Reproduire, sur votre propre courbe, trois résultats que vous venez de lire. Quatre exécutions comparées dans TensorBoard, et une phrase de conclusion pour chacune.

**Protocole.**

1. **Remplacer ReLU par la sigmoïde**, partout, sans rien changer d'autre. Relevez le nombre d'époques nécessaires pour atteindre la perte que ReLU atteint en dix époques. Rapprochez votre observation du chiffre **0,25** de la section 2.2 : avec trois couches, le gradient qui arrive à la première est multiplié par trois facteurs inférieurs à 0,25.
2. **Briser la brisure de symétrie.** Initialisez **tous** les poids d'une couche cachée à la même constante, par exemple 0,1, et entraînez. Puis affichez, après entraînement, les poids de cette couche. Que constatez-vous, et combien d'unités distinctes votre couche de 64 unités contient-elle réellement ?
3. **Xavier contre l'initialisation par défaut.** Appliquez le fragment de la section 2.6, relancez, superposez les deux courbes. Attendez-vous à une différence modeste, et sachez dire pourquoi : le réseau est petit et peu profond.
4. **Abandon de neurones.** Ajoutez `nn.Dropout(p=0.3)` après chaque activation et comparez les deux courbes, entraînement et validation. Faites ensuite l'erreur **exprès** : évaluez la validation **sans** appeler `net.eval()`, et regardez ce que devient la courbe.

**Attentes.**

* Avec la sigmoïde, la convergence est nettement plus lente, et la différence s'accentue si vous ajoutez une quatrième couche. C'est le gradient évanescent, sur un réseau de trois couches et un ordinateur portable.
* Avec l'initialisation constante, les 64 unités de la couche restent **égales entre elles** du début à la fin : la couche travaille comme si elle avait une seule unité, et la perte plafonne très haut. Vous venez de reproduire la brisure de symétrie manquée.
* Sur ce problème, l'abandon de neurones **dégrade** la perte d'entraînement et n'améliore pas la validation : les données sont propres, abondantes et sans bruit d'étiquetage. C'est le résultat attendu, et c'est le meilleur antidote à l'idée qu'une technique de régularisation serait bonne en soi.
* Sans `net.eval()`, la courbe de validation devient bruitée et systématiquement pessimiste. Notez l'écart : c'est le coût d'une ligne oubliée.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-02.ipynb" label="Niveau 2 : sigmoïde, symétrie, Xavier, abandon" >}}

---

## Niveau 3 : Extension créative, le même réseau en convolutif

**Objectif ouvert.** Refaire le niveau 1 avec des **images** en entrée, et un corps convolutif. Les cibles restent fournies et la perte reste l'erreur quadratique moyenne : rien ne change au protocole, tout change à la forme des données.

**Les données, à fabriquer vous-même.** Des images d'un seul canal, 28 × 28, noires, avec un carré blanc de 4 × 4 posé à une position tirée au hasard. La cible est le couple de coordonnées du centre du carré, normalisé dans \([-1, 1]\). C'est un problème que la structure spatiale résout et que l'aplatissement maltraite, donc exactement le banc d'essai de la section 2.8. Respectez la convention des canaux : vos tenseurs ont la forme `(N, 1, 28, 28)`.

**Critères de réussite.**

* Vous **calculez au crayon** la forme de sortie de chaque couche convolutive, puis vous la vérifiez en faisant passer `torch.zeros(1, 1, 28, 28)` dans le corps convolutif seul et en lisant la forme obtenue. Les deux doivent coïncider avant que vous n'écriviez la première couche dense.
* La réduction de résolution se fait par le **pas de la convolution**, pas par agrégation. Deux couches convolutives suffisent, et vous donnez la taille du vecteur aplati comme un nombre, pas comme une constante magique trouvée par essais.
* Vous entraînez ensuite un perceptron multicouche sur les **mêmes images aplaties**, avec un nombre de paramètres comparable, et vous comparez les deux courbes dans TensorBoard. Comptez les paramètres des deux modèles, c'est la moitié de la démonstration.
* Un paragraphe de conclusion qui répond à une question précise : lequel des deux modèles généralise mieux sur des positions de carré **jamais vues à l'entraînement**, et quel principe de la section 2.8 l'explique.

**Piste de départ.** `sum(p.numel() for p in net.parameters())` compte les paramètres d'un modèle. La comparaison la plus parlante n'est pas « le convolutif gagne », c'est « le convolutif gagne **avec dix fois moins de paramètres** ».

> [!TIP]
 **Mon message pour ce laboratoire :** vous n'entraînez pas un agent, et c'est normal. Vous fabriquez l'instrument, vous apprenez à le régler, et vous installez les réflexes qui vous éviteront, les treize semaines suivantes, de confondre un bogue de PyTorch avec un échec d'apprentissage par renforcement. Quand votre agent de la semaine 5 refusera d'apprendre, la première question sera : « est-ce que le réseau, lui, apprend ? » Cette semaine vous donne les moyens d'y répondre en cinq minutes.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-02.ipynb" label="Niveau 3 : corps convolutif, carré blanc, comparaison" >}}
