---
title: "7.10 L'environnement écrit à la main"
weight: 11
---

## Remplir l'API de Gymnasium soi-même

Nous avons les trois décisions et nous avons les données. Il reste à écrire l'environnement, et c'est l'exercice central du laboratoire de cette semaine.

L'environnement suit l'interface `Env` de Gym, et il délègue son état à des classes internes, ce qui est un bon découpage : la mécanique du marché d'un côté, l'habillage Gym de l'autre. Le bénéfice de cette conformité est immédiat et il mérite d'être souligné : un environnement conforme **se branche sans modification** sur toutes les classes que nous avons utilisées pour les jeux Atari. Le même agent, le même tampon de rejeu, la même boucle. C'est la raison pour laquelle on se donne la peine de respecter une interface plutôt que d'écrire une simulation à sa façon.

{{% comment %}}SOURCE: LAPAN ch.10 p.308, p.316{{% /comment %}}

Deux valeurs par défaut, au niveau du module, que vous retrouverez partout dans la suite : **10 barres** dans l'observation, et une **commission de 0,1 %**.

{{% comment %}}SOURCE: LAPAN ch.10 p.308-309{{% /comment %}}

Les trois actions sont une énumération, et je garde les noms anglais des identifiants de code comme le veut la règle du cours : `Skip = 0`, `Buy = 1`, `Close = 2`.

{{% comment %}}SOURCE: LAPAN ch.10 p.309{{% /comment %}}

> [!NOTE]
 **Un modèle de marché délibérément réduit, et il faut le dire à voix haute.** On ne peut acheter qu'**une seule** action. On ne peut pas renforcer une position déjà ouverte. Et on ne peut pas **vendre à découvert** (*short selling*), c'est-à-dire vendre une action qu'on ne possède pas en pariant sur une baisse, ce qui est une opération parfaitement courante sur les marchés réels. Ces trois restrictions ne sont pas des oublis : ce sont des décisions assumées pour garder l'exemple compréhensible. Elles ont pour conséquence directe que notre agent **ne peut gagner que dans les marchés qui montent**, ce qui limite sévèrement ce que son résultat peut démontrer.

{{% comment %}}SOURCE: LAPAN ch.10 p.309{{% /comment %}}

Pour la construction, deux chemins : soit on charge tous les fichiers d'un répertoire, soit on passe directement un dictionnaire de séries de prix déjà chargées. Une série de prix est simplement un objet portant **cinq tableaux NumPy à une dimension** : ouverture, haut, bas, clôture, volume.

{{% comment %}}SOURCE: LAPAN ch.10 p.309{{% /comment %}}

---

## Les sept paramètres, et pourquoi chacun est une décision de modélisation

Voici les sept paramètres de comportement de l'environnement. Je vous les donne sous forme de liste parce que c'est une énumération, mais lisez-les comme **sept décisions de conception**, pas comme sept options de configuration.

| Paramètre | Rôle | Défaut |
| --- | --- | --- |
| nombre de barres | taille de la fenêtre d'observation | 10 |
| commission | pourcentage du prix versé au courtier, **à l'achat et à la vente** | 0,1 % |
| fin d'épisode à la clôture | si vrai, l'épisode **se termine à la première clôture** de position | vrai |
| représentation 1-D | forme du tenseur d'observation, matrice ou vecteur plat | faux |
| offset aléatoire | point de départ tiré au hasard dans la série à chaque réinitialisation | vrai |
| récompense à la clôture | bascule entre le schéma A et le schéma B de la section 7.8 | faux |
| volumes | ajoute le volume échangé à l'observation | faux |

{{% comment %}}SOURCE: LAPAN ch.10 p.310-311{{% /comment %}}

Trois commentaires sur ce tableau, parce que trois de ces lignes ont des conséquences qu'on ne voit pas en les lisant.

**La fin d'épisode à la première clôture** change complètement la nature de l'épisode. Avec cette option, un épisode est **une opération** : on entre, on attend, on sort, c'est fini. Sans elle, l'épisode court jusqu'au bout de la série, c'est-à-dire sur une année entière de données. Le choix a un effet direct sur la longueur des épisodes, donc sur l'actualisation, donc sur le comportement appris. Et il a un effet secondaire très pratique : avec cette option, **la longueur d'un épisode est exactement la durée de détention**, ce qui vous donne une statistique comportementale lisible gratuitement.

**La représentation 1-D** mérite une précision de vocabulaire. Elle choisit entre deux dispositions du même contenu. En position haute, l'observation est une **matrice** à une ligne par composante de prix, ce qui se prête à une convolution à une dimension : les lignes y jouent exactement le rôle que les plans de couleur jouaient dans les images Atari de la semaine 5. En position basse, l'observation est **un seul tableau plat** où les composantes de chaque barre sont placées à la suite, ce qui convient à un réseau entièrement connecté. Le contenu est identique, la disposition change, et **la disposition décide quelle architecture est possible**.

**Les volumes sont désactivés par défaut**, et je le mentionne parce que c'est contre-intuitif : on a une information de plus, et on choisit de ne pas la donner. C'est une décision défendable (le volume est bruyant et son interprétation varie selon le marché) et c'est exactement le genre de décision que le jalon 2 et la section 7.13 vous invitent à remettre en question par la mesure.

{{< bookfig src="07-05.png" week="07" >}}

La **Figure 7-5** met les deux dispositions côte à côte, et c'est la figure du vrai sujet de cette moitié de semaine : le choix de représentation, pas le choix d'algorithme. Deux remarques pour la lire sans se tromper. Le vecteur dessiné montre quatre composantes par barre, volume compris, alors que le volume est désactivé par défaut : avec les réglages par défaut, il y a **trois** composantes par barre. Et les deux dispositions sont dessinées sans la position ni le profit relatif, qui s'ajoutent à la fin dans les deux cas.

{{% comment %}}SOURCE: LAPAN ch.10 p.311, image{{% /comment %}}

Les deux espaces de Gym se déclarent alors directement : un espace d'actions discret à trois valeurs, et un espace d'observations continu dont la forme est celle du tenseur d'état. Notez que cet espace est déclaré **non borné**, de moins l'infini à plus l'infini : rien, au niveau de Gym, ne normalise l'observation. C'est à votre représentation de s'en charger, ce qu'elle fait, et c'est une bonne raison de plus de ne pas traiter la section 7.8 comme un détail.

{{% comment %}}SOURCE: LAPAN ch.10 p.311, image{{% /comment %}}

---

## L'état, et la seule chose qui rend ce problème markovien

Avant toute ligne de code, la question qu'il faut se poser : **qu'est-ce qui doit figurer dans l'état ?**

L'état contient évidemment les prix récents. Mais il contient aussi, et c'est le point décisif, **la position** : un booléen disant qu'une action est détenue, et le prix auquel elle a été achetée. Je veux que vous voyiez pourquoi cela n'est pas négociable.

Supposons que l'état ne contienne que les prix. Prenez deux instants \(t_1\) et \(t_2\) où les dix dernières barres sont numériquement identiques. Au premier, l'agent ne détient rien ; au second, il détient une action achetée 5 % plus bas. L'observation est la même, et la bonne action est différente : attendre une occasion d'acheter dans un cas, décider s'il faut encaisser dans l'autre. Deux états identiques exigeant deux décisions différentes : la **propriété de Markov** est violée, et toutes les méthodes de ce cours cessent d'être justifiées. **C'est la position dans l'état qui fait de ce problème un processus de décision markovien**, et rien d'autre.

{{% comment %}}SOURCE: LAPAN ch.10 p.313{{% /comment %}}

La taille de l'observation découle alors du compte :

$$
\dim(S_t) = 3b + \underbrace{1}_{\text{position}} + \underbrace{1}_{\text{profit relatif}} \qquad (\text{ou } 4b + 2 \text{ avec les volumes})
$$

Avec les réglages par défaut, \(b = 10\) barres et pas de volumes, cela fait \(3 \times 10 + 2 = \mathbf{32}\) nombres. Trente-deux. Après les 84 × 84 × 4 trames empilées des semaines 5 et 6, c'est un soulagement, et c'est aussi un avertissement : la petitesse de l'observation ne dit rien de la difficulté du problème.

En représentation 1-D, le même contenu devient une matrice de forme \((5, b)\), ou \((6, b)\) avec les volumes : trois lignes de prix, puis une ligne pour la position et une pour le profit relatif.

{{% comment %}}SOURCE: LAPAN ch.10 p.313, p.316{{% /comment %}}

Le profit relatif de la position ouverte, dernière composante de l'observation, s'écrit :

$$
\rho_t = \frac{c_t}{c_{\text{ouv}}} - 1, \qquad \text{et } \rho_t = 0 \text{ en l'absence de position}
$$

{{% comment %}}SOURCE: LAPAN ch.10 p.314, image{{% /comment %}}

Et le point de départ d'un épisode, quand l'offset aléatoire est actif, est tiré uniformément en laissant de la place devant et derrière :

$$
\text{offset} \sim \mathcal{U}\{0, \dots, L - 10b - 1\} + b
$$

où \(L\) est la longueur de la série. Le décalage de \(b\) garantit qu'il existe \(b\) barres d'historique à encoder dès le premier pas ; la marge de \(10b\) à la fin garantit qu'il reste de quoi jouer.

{{% comment %}}SOURCE: LAPAN ch.10 p.312{{% /comment %}}

---

## Le code de l'état, de bout en bout

Voici maintenant les deux méthodes qui portent toute la mécanique : le codage de l'observation, et le pas.

```python
# etat.py : la mecanique du marche. Aucun appel a Gym ici.
import numpy as np

class Etat:
    def __init__(self, nb_barres, commission, fin_a_la_cloture,
                 recompense_a_la_cloture, volumes=False):
        assert nb_barres > 0
        assert commission >= 0.0
        self.nb_barres = nb_barres
        self.commission = commission
        self.fin_a_la_cloture = fin_a_la_cloture
        self.recompense_a_la_cloture = recompense_a_la_cloture
        self.volumes = volumes

    def reinitialiser(self, prix, offset):
        self.prix = prix                 # hauts, bas, clotures : RELATIFS a l'ouverture
        self._offset = offset
        self.en_position = False         # <- la position fait partie de l'etat
        self.prix_entree = 0.0

    @property
    def forme(self):
        # [h, l, c] * barres + drapeau_position + profit_relatif
        return (3 * self.nb_barres + 1 + 1, )

    def _cloture_courante(self):
        """Reconstruit un prix ABSOLU : c = o * (1 + c_rel)."""
        o = self.prix.ouverture[self._offset]
        c_rel = self.prix.cloture[self._offset]
        return o * (1.0 + c_rel)

    def coder(self):
        """L'observation : b barres relatives, puis la position, puis le profit."""
        res = np.ndarray(self.forme, dtype=np.float32)
        decalage = 0
        for i in range(-self.nb_barres + 1, 1):
            res[decalage] = self.prix.haut[self._offset + i]
            res[decalage + 1] = self.prix.bas[self._offset + i]
            res[decalage + 2] = self.prix.cloture[self._offset + i]
            decalage += 3
        res[decalage] = float(self.en_position)
        decalage += 1
        if not self.en_position:
            res[decalage] = 0.0
        else:
            res[decalage] = self._cloture_courante() / self.prix_entree - 1.0
        return res

    def pas(self, action):
        """Rend (recompense, fin). La recompense est en POINTS DE POURCENTAGE."""
        recompense = 0.0
        fin = False
        cloture = self._cloture_courante()

        if action == Actions.Buy and not self.en_position:
            self.en_position = True
            self.prix_entree = cloture
            recompense -= self.commission                 # premiere jambe du cout

        elif action == Actions.Close and self.en_position:
            recompense -= self.commission                 # seconde jambe du cout
            fin |= self.fin_a_la_cloture
            if self.recompense_a_la_cloture:              # SCHEMA A
                recompense += 100.0 * (cloture / self.prix_entree - 1.0)
            self.en_position = False
            self.prix_entree = 0.0

        self._offset += 1
        cloture_precedente = cloture
        cloture = self._cloture_courante()
        fin |= self._offset >= self.prix.cloture.shape[0] - 1
        if self.en_position and not self.recompense_a_la_cloture:   # SCHEMA B
            recompense += 100.0 * (cloture / cloture_precedente - 1.0)

        return recompense, fin
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(S_t\) | observation complète | la valeur rendue par `coder()` |
| \(b\) | barres dans la fenêtre d'observation | `nb_barres` |
| \(o_t, h_t, l_t, c_t\) | ouverture, haut, bas, clôture de la barre | `prix.ouverture`, `prix.haut`, `prix.bas`, `prix.cloture` |
| \(h^{\text{rel}}, l^{\text{rel}}, c^{\text{rel}}\) | les mêmes, en proportion de l'ouverture | le contenu des tableaux chargés |
| \(c = o\,(1 + c^{\text{rel}})\) | retour au prix absolu | `_cloture_courante()` |
| \(c_{\text{ouv}}\) | prix d'entrée de la position | `prix_entree` |
| \(\rho_t\) | profit relatif de la position ouverte | dernière composante de `res` |
| \(\mathbf{1}[\text{position}]\) | indicateur de position, **dans l'état** | `en_position` |
| \(A_t \in \{\textsf{Skip}, \textsf{Buy}, \textsf{Close}\}\) | action | `action` |
| \(R_{t+1}\) | récompense, en points de pourcentage | `recompense` |
| \(\kappa\) | commission par opération | `commission` |
| schéma A ou B | bascule entre les deux récompenses | `recompense_a_la_cloture` |
| fin d'épisode | à la première clôture, ou en fin de série | `fin` |

{{% comment %}}SOURCE: LAPAN ch.10 p.313-315, image{{% /comment %}}

Trois choses à remarquer dans ce code, et ce sont les trois que je poserais à l'examen.

**Première chose, l'unité.** Le facteur 100 fixe l'unité de la récompense : un **point de pourcentage**. Conséquence immédiate et très utile, parce qu'elle donne un repère chiffré pour toute la section 7.12 : un aller-retour complet, achat puis clôture, sans aucun mouvement de prix, rapporte exactement

$$
-2\kappa = -0{,}2 \ \text{point}
$$

soit 0,1 à l'achat et 0,1 à la clôture. C'est le **coût du voyage**, et c'est le seuil que toute stratégie doit franchir avant de produire le moindre gain.

{{% comment %}}SOURCE: LAPAN ch.10 p.314-315, image ; p.322{{% /comment %}}

**Deuxième chose, l'ordre des opérations dans `pas()`.** Regardez bien la fin de la méthode. La position est remise à faux **avant** le bloc du schéma B. Ce n'est pas un détail d'implémentation, c'est ce qui garantit que les deux schémas couvrent le même trajet de prix sans double comptage : la barre de clôture est créditée par le schéma A dans sa branche, et par le schéma B lors du pas précédent. Si vous écrivez cet environnement vous-même, c'est **exactement** l'endroit où une erreur d'une ligne produit deux schémas qui ne mesurent plus la même chose. Le volet B du laboratoire vous fait vérifier ce point par un test, sans entraîner quoi que ce soit.

{{% comment %}}SOURCE: LAPAN ch.10 p.315, image{{% /comment %}}

**Troisième chose, l'approximation, et elle est nommée comme telle.** Nous supposons l'ordre **exécuté instantanément au prix de clôture de la barre courante**. C'est une simplification, et dans la réalité un ordre s'exécute à un prix différent de celui qu'on visait : ce décalage s'appelle le **dérapage des prix** (*price slippage*). Nous reviendrons sur ce qu'il coûte en section 7.13. Retenez surtout la méthode : une approximation **écrite dans le commentaire du code** est une approximation dont on pourra parler ; une approximation implicite est un piège tendu à son propre futur.

{{% comment %}}SOURCE: LAPAN ch.10 p.315{{% /comment %}}

---

## Les deux dernières méthodes, et une qui n'existe pas

La réinitialisation choisit l'instrument au hasard parmi les séries chargées, puis l'offset selon la formule vue plus haut, remet l'état à zéro et rend la première observation. Le pas est un **habillage mince** : l'objet d'état rend le couple récompense-fin, l'état se recode, et le dictionnaire d'information transporte l'instrument et l'offset courant, ce qui est précieux pour déboguer. Le tuple rendu est celui de Gymnasium : observation, récompense, terminaison, troncature, informations.

{{% comment %}}SOURCE: LAPAN ch.10 p.312{{% /comment %}}

```python
# environnement.py : l'habillage Gym, mince par construction.
import gymnasium as gym
import numpy as np

class EnvActions(gym.Env):
    def __init__(self, prix, nb_barres=10, commission=0.1, fin_a_la_cloture=True,
                 offset_aleatoire=True, recompense_a_la_cloture=False, volumes=False):
        self._prix = prix
        self._etat = Etat(nb_barres, commission, fin_a_la_cloture,
                          recompense_a_la_cloture, volumes)
        self._offset_aleatoire = offset_aleatoire
        self.action_space = gym.spaces.Discrete(n=len(Actions))
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=self._etat.forme, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._instrument = self.np_random.choice(list(self._prix.keys()))
        prix = self._prix[self._instrument]
        b = self._etat.nb_barres
        if self._offset_aleatoire:
            offset = self.np_random.choice(len(prix.haut) - b * 10) + b
        else:
            offset = b
        self._etat.reinitialiser(prix, offset)
        return self._etat.coder(), {}

    def step(self, action):
        recompense, fin = self._etat.pas(Actions(action))
        obs = self._etat.coder()
        info = {"instrument": self._instrument, "offset": self._etat._offset}
        return obs, recompense, fin, False, info
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{A}\) | espace d'actions, discret à trois valeurs | `action_space` |
| \(\mathcal{S}\) | espace d'observations, **non borné** | `observation_space` |
| \(L\) | longueur de la série de prix | `len(prix.haut)` |
| offset de départ | tiré uniformément, avec marge | `offset` |
| \(S_0\) | première observation de l'épisode | retour de `reset` |
| \((S_{t+1}, R_{t+1}, \text{fin})\) | résultat d'un pas | retour de `step` |

Et la méthode qui n'existe pas : l'affichage. Elle est **facultative** dans l'interface de Gym, et elle n'est pas implémentée ici. C'est pourtant l'un des meilleurs exercices optionnels de la semaine, parce qu'un environnement de marché a un affichage naturel et très utile pour le débogage : tracer la série de prix, et marquer dessus les instants d'achat et de clôture de l'agent. Vous verriez alors, en un seul coup d'œil, ce qu'aucune courbe de récompense ne vous dira : **quand** l'agent décide d'agir.

{{% comment %}}SOURCE: LAPAN ch.10 p.312{{% /comment %}}

Un dernier mot sur la variante 1-D. Elle **hérite** de la classe d'état et ne redéfinit que la représentation : la forme devient \((5, b)\), le codage remplit la ligne 0 avec les hauts, la ligne 1 avec les bas, la ligne 2 avec les clôtures, la ligne 3 avec les volumes s'ils sont activés, puis place la position et le profit relatif dans les deux lignes suivantes. **Même comportement, même récompense, même dynamique, un tenseur différent.** Je vous invite à lire les deux classes l'une après l'autre, parce que leur rapprochement est la plus nette illustration du vrai sujet de cette moitié de semaine : deux agents sur le **même** processus de décision markovien, qui ne diffèrent que par la disposition de l'observation, et cette disposition décide quelle architecture vous pouvez employer.

{{% comment %}}SOURCE: LAPAN ch.10 p.316{{% /comment %}}

---
