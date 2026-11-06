---
title: "14.4 La chaîne, mesurée, et son prix annoncé d'avance"
weight: 5
---

## Le point de départ, et ce qu'il coûte

Avant toute rétroaction humaine, il faut un agent qui joue. La chaîne part donc d'un **acteur-critique à avantage** (*advantage actor-critic*) tout à fait ordinaire, celui de la semaine 8 : seize environnements en parallèle, les enveloppes Atari habituelles de la semaine 5, et des hyperparamètres repris de la formulation d'origine.

Le coût mesuré de cette étape : **cinq heures de calcul et douze millions d'observations**.

{{% comment %}}SOURCE: LAPAN ch.19 p.582{{% /comment %}}

Je donne ce chiffre tout de suite parce qu'il fixe l'échelle de tout ce qui suit. Douze millions de pas pour le modèle de départ, et nous verrons que les trois tours d'affinage coûtent ensemble environ huit heures de plus. L'ordre de grandeur total est de **treize heures de processeur graphique**, et c'est avant de compter le temps humain.

---

## L'enveloppe d'enregistrement, et deux constantes qui décident de tout

Pendant que l'agent joue, il faut constituer la base de segments. Cela se fait par une **enveloppe** (*wrapper*), au sens de la semaine 1 : un objet qui s'interpose entre l'agent et l'environnement et qui, ici, ne modifie rien mais observe.

**Intuition.** On ne veut pas enregistrer en continu, ce serait des téraoctets. On veut des échantillons représentatifs du comportement courant, prélevés rarement et au hasard. L'enveloppe tire donc, à chaque pas, une pièce très biaisée : avec une probabilité \(p_{\text{rec}}\) elle déclenche l'enregistrement des \(L\) pas qui suivent, puis elle écrit le segment sur disque et redevient inactive.

**Les deux constantes**, et elles sont petites toutes les deux :

$$
L = 50, \qquad p_{\text{rec}} = 5 \times 10^{-5}
$$

Autrement dit, un pas sur vingt mille déclenche un enregistrement de cinquante pas.

{{% comment %}}SOURCE: LAPAN ch.19 p.580-582{{% /comment %}}

**Le code.** Voici la mécanique, réécrite, sans la partie qui sérialise les images.

```python
import random


class EnregistreurDeSegments:
    """Enveloppe qui preleve des segments de longueur fixe, au hasard.

    Elle ne modifie NI l'observation NI la recompense : elle observe.
    """

    LONGUEUR = 50          # L : nombre de pas d'un segment
    PROBA = 0.00005        # p_rec : probabilite de declencher

    def __init__(self, env, base):
        self.env = env
        self.base = base
        self.tampon = None     # None = inactif ; une liste = enregistrement en cours

    def step(self, action):
        obs, recompense, termine, tronque, info = self.env.step(action)

        if self.tampon is None:
            if random.random() < self.PROBA:
                self.tampon = []        # on demarre un segment
        if self.tampon is not None:
            self.tampon.append((obs, action))
            if len(self.tampon) == self.LONGUEUR:
                self.base.ecrire(self.tampon)   # segment complet
                self.tampon = None

        return obs, recompense, termine, tronque, info
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(L\) | longueur d'un segment, en pas de jeu | `LONGUEUR` |
| \(p_{\text{rec}}\) | probabilité de déclencher un enregistrement | `PROBA` |
| \((o_t, a_t)\) | le couple enregistré à chaque pas | `(obs, action)` |
| \(\zeta\) | le segment complet, écrit en base | `self.tampon` au moment de l'écriture |

> [!WARNING]
 **Un détail de ce code mérite une mise en garde, parce qu'il a une conséquence que la plupart des lecteurs ne voient pas.** L'enregistrement **ignore les frontières d'épisode**. Si le déclenchement tombe quarante pas avant une mort, le segment contient la fin de l'épisode, la réinitialisation, et les dix premiers pas de l'épisode suivant. La personne qui jugera ce segment verra donc un sous-marin mourir puis réapparaître intact, ce qui est visuellement déroutant et difficile à noter. Ce n'est pas un bogue, c'est une simplification assumée : enregistrer à cheval sur un épisode évite de maintenir un état de synchronisation avec l'environnement. Mais c'est une source de bruit dans les étiquettes, et quand nous compterons les explications possibles de l'échec final, celle-ci figurera dans la liste.

{{% comment %}}SOURCE: LAPAN ch.19 p.580{{% /comment %}}

Et le volume, mesuré : **après douze millions de pas, la base contient environ deux mille cinq cents segments, qui occupent douze gigaoctets**.

{{% comment %}}SOURCE: LAPAN ch.19 p.582{{% /comment %}}

Faites la division : douze gigaoctets pour cent vingt-cinq mille images, cela fait de l'ordre de cent kilooctets par image. Ce n'est pas une erreur de calcul, c'est la conséquence du choix que je décris maintenant.

---

## Pourquoi l'enveloppe se place avant les autres, et non après

Voici une décision d'architecture qui a l'air technique et qui est en réalité une décision sur l'**interface humaine**.

Les enveloppes Atari de la semaine 5 font quatre choses : elles réduisent l'image, la passent en niveaux de gris, en empilent plusieurs, et sautent des trames. C'est exactement ce qu'il faut pour un réseau convolutif, et c'est exactement ce qu'il ne faut pas pour un œil humain. Un carré gris de quatre-vingt-quatre pixels de côté empilé par quatre est illisible.

L'enveloppe d'enregistrement se place donc **avant** elles, au contact de l'environnement brut. Elle voit et conserve l'écran d'origine : **210 pixels de haut sur 160 de large, en trois canaux de couleur**. La jauge d'oxygène y est visible, les plongeurs y sont reconnaissables, les couleurs distinguent les ennemis. C'est le prix des douze gigaoctets, et c'est un prix qu'il faut payer : sans lui, la personne ne pourrait pas juger.

{{% comment %}}SOURCE: LAPAN ch.19 p.582, p.589{{% /comment %}}

> [!NOTE]
 **Deux résolutions circulent pour cette chaîne et une seule est la bonne, alors fixons-la ici une fois pour toutes.** La trame native de cet émulateur de jeux d'arcade est de **210 sur 160** en hauteur sur largeur, trois canaux. C'est cette valeur que ce cours emploie, et elle est confirmée par la forme des tenseurs que la section 14.6 va écrire. Si vous rencontrez ailleurs la mention d'une autre résolution d'origine pour le même système, c'est une inversion ou une coquille, et vos tenseurs ne se brancheront pas. Vérifiez toujours une résolution annoncée contre une forme de tenseur dans le code : la forme de tenseur ne ment pas.

---

## Le modèle de départ, et l'optimum local qui est toute la semaine en une phrase

Cinq heures plus tard, nous avons un agent. Voici ce qu'il vaut, mesuré sans écrêtage de la récompense au moment du test, ce qui importe car l'écrêtage de la semaine 5 falsifierait le score rapporté :

**une récompense de 460 en 580 pas de jeu.**

{{% comment %}}SOURCE: LAPAN ch.19 p.583, p.598{{% /comment %}}

Et voici ce qu'il fait, décrit en trois traits. Il **tire sur les poissons presque parfaitement**, ce qui est l'activité dont le signal était dense. Il **reste au fond de l'écran**, parce que c'est l'endroit le plus sûr, les sous-marins ennemis n'y descendant pas. Et il n'a **aucune notion de l'oxygène** : il meurt asphyxié, épisode après épisode.

Lisez maintenant ces trois traits ensemble, parce qu'ils forment la phrase la plus importante de la première moitié de la semaine. L'agent a trouvé un **optimum local parfaitement légitime du point de vue de l'objectif qu'on lui a donné**. Rester au fond et tirer maximise la récompense sur l'horizon de cinq cents pas qu'il connaît. Remonter coûte du temps de tir et ne rapporte, dans sa récompense, rien du tout. Il n'y a pas de bogue à corriger, il n'y a pas d'exploration à améliorer : il y a une **spécification qui ne contient pas l'oxygène**.

> [!IMPORTANT]
 **Ce que nous allons demander à la personne, et je vous le dis maintenant pour que vous voyiez la fin venir.** La chaîne va servir à apprendre une récompense qui, elle, contient l'oxygène. Pour cela, la personne qui étiquette va préférer les segments où le sous-marin remonte à la surface et rejeter ceux où la jauge est basse. Autrement dit, nous allons **demander à l'agent de remonter**. Souvenez-vous de cette phrase à la section 14.8 : l'agent va nous donner exactement ce que nous avons demandé, et rien d'autre, et c'est ce « rien d'autre » qui est la leçon de la semaine.

---
