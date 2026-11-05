---
title: "2.8 Du perceptron multicouche au réseau convolutif"
weight: 9
---

## Quand l'ordre des entrées porte l'information

Cette section répond à une question que vous vous posez peut-être depuis la section 2.2 : pourquoi ne pas simplement **aplatir** une image en un grand vecteur et la donner à un perceptron multicouche ? La réponse est courte, et elle est décisive.

Un perceptron multicouche est **invariant à l'ordre de ses entrées**. Permutez les colonnes de votre matrice de données, de la même façon pour tous les exemples, et il apprendra exactement aussi bien : à ses yeux, l'entrée numéro 1 et l'entrée numéro 500 n'ont aucune relation de voisinage. Pour des caractéristiques tabulaires, c'est une propriété inoffensive. Pour une image, c'est un désastre : **aplatir, c'est jeter la structure spatiale**, c'est-à-dire précisément l'information qui dit que deux pixels voisins parlent probablement de la même chose.

{{% comment %}}SOURCE: D2L ch.7 p.273{{% /comment %}}

À quoi s'ajoute un argument de comptage sans appel. Une image d'un mégapixel reliée à mille unités cachées demande \(10^{9}\) paramètres, soit un milliard de nombres pour une seule couche. Écrite complètement, comme un tenseur de poids d'ordre quatre reliant chaque position d'entrée à chaque position de sortie, la même couche dense coûte \(10^{12}\) paramètres. Aucun matériel, aucun jeu de données ne rend cela raisonnable.

{{% comment %}}SOURCE: D2L ch.7 p.274, p.276{{% /comment %}}

---

## Deux principes, trois ordres de grandeur

La sortie de ce cul-de-sac tient en deux principes, qui sont deux hypothèses sur le monde, donc deux biais inductifs au sens de la section 2.7.

**L'invariance par translation** (*translation invariance*) : un détecteur de motif doit répondre de la même façon où que le motif se trouve dans l'image. Un chat dans le coin supérieur gauche est un chat. **Le principe de localité** (*locality*) : pour décider ce qui se passe à un endroit, il suffit de regarder un voisinage de cet endroit, pas l'image entière. S'y ajoute une troisième exigence, qui concerne la profondeur : les couches plus profondes doivent pouvoir voir **plus loin** que les premières, afin de composer des motifs locaux en motifs étendus.

{{% comment %}}SOURCE: D2L ch.7 p.275{{% /comment %}}

Le plus beau, c'est que ces principes ne sont pas des recettes ajoutées à la main : **ils se traduisent directement en contraintes sur les poids**, et la facture s'effondre en trois étapes. On part de la couche dense complète et de ses \(10^{12}\) paramètres. On impose ensuite que les poids **ne dépendent pas de la position** \((i,j)\) considérée, ce qui est exactement l'invariance par translation : il reste \(4 \times 10^{6}\) paramètres, et l'opération obtenue **est déjà une convolution**. On impose enfin la localité, en annulant tout poids au-delà d'une distance \(\Delta\) : il reste \(4\Delta^{2}\) paramètres, et \(\Delta\) dépasse rarement 10. D'un billion à quelques centaines.

{{% comment %}}SOURCE: D2L ch.7 p.276-277{{% /comment %}}

Le tableau de poids qui survit à ces deux contraintes porte un nom : c'est le **noyau de convolution** (*convolution kernel*), aussi appelé filtre, ou simplement « les poids ». Ses coefficients sont **partagés par toutes les positions** de l'image, et ce **partage des poids** (*weight sharing*) est la raison de l'effondrement du nombre de paramètres. La **Figure 2-8** montre le mécanisme : une fenêtre glisse sur l'entrée et, à chaque position, le noyau produit une valeur de la sortie.

{{< bookfig src="02-08.png" week="02" >}}

{{% comment %}}SOURCE: D2L ch.7 p.277, p.281{{% /comment %}}

> [!NOTE]
 **Notez bien ce que nous venons de payer, car rien n'est gratuit.** En imposant ces deux principes, nous avons rendu les caractéristiques apprises **invariantes par translation** et **strictement locales**. C'est merveilleux sur des images, où ces hypothèses sont vraies. Un bon biais inductif rend le modèle économe en données ; un mauvais biais inductif empêche le modèle d'ajuster même les données d'entraînement. En semaine 5, nous verrons un cas où une partie de cette invariance devient gênante, parce que la **position** d'un objet dans l'image est justement l'information qui compte.

{{% comment %}}SOURCE: D2L ch.7 p.277{{% /comment %}}

---

## Canaux, cartes de caractéristiques, et un peu d'arithmétique

Une image en couleur n'est pas une matrice mais un tenseur d'ordre trois : hauteur, largeur, et un troisième axe, celui des **canaux** (*channels*). Un noyau de convolution a donc quatre dimensions, de forme \(c_o \times c_i \times k_h \times k_w\) : on **somme** sur les canaux d'entrée et on **empile** sur les canaux de sortie. Chaque grille de sortie ainsi produite s'appelle une **carte de caractéristiques** (*feature map*), et la pratique courante consiste à **échanger de la résolution spatiale contre de la profondeur de canaux** : à mesure qu'on avance dans le réseau, les cartes rétrécissent et se multiplient.

{{% comment %}}SOURCE: D2L ch.7 p.279, p.293-294{{% /comment %}}

Vient maintenant l'arithmétique dont vous aurez besoin au laboratoire, et je vous recommande de la faire au crayon avant de la coder. Pour une entrée de \(n_h \times n_w\) et un noyau de \(k_h \times k_w\) appliqué nûment, la sortie fait

$$
(n_h - k_h + 1) \times (n_w - k_w + 1)
$$

{{% comment %}}SOURCE: D2L ch.7 p.281{{% /comment %}}

Donc la sortie **rétrécit** à chaque convolution, ce qui limite la profondeur possible. Deux réglages permettent de piloter cela. Le **remplissage** (*padding*) ajoute des bordures de zéros autour de l'entrée, ce qui agrandit la sortie d'autant ; avec un noyau de taille impaire et un remplissage \(p = k - 1\) réparti de part et d'autre, la sortie conserve **exactement** la taille de l'entrée, et c'est le réglage le plus utilisé. Le **pas de la convolution** (*stride*) fait sauter la fenêtre de plusieurs cases à la fois, ce qui **divise** la taille de la sortie, avec une division **entière par défaut** puisqu'une fenêtre à cheval sur le bord est abandonnée. Un pas supérieur à 1 est donc un **sous-échantillonnage spatial** gratuit, intégré à la couche.

{{% comment %}}SOURCE: D2L éq. 7.3.1 p.289 (remplissage) et éq. 7.3.2 p.290 (pas, division entière){{% /comment %}}

$$
(n_h - k_h + p_h + 1) \times (n_w - k_w + p_w + 1)
$$

$$
\left\lfloor \frac{n_h - k_h + p_h + s_h}{s_h} \right\rfloor \times
\left\lfloor \frac{n_w - k_w + p_w + s_w}{s_w} \right\rfloor
$$

{{% comment %}}SOURCE: D2L ch.7 p.289-290{{% /comment %}}

Il existe un autre moyen de réduire la résolution, sans aucun paramètre à apprendre : l'**agrégation** (*pooling*) fait glisser une fenêtre et ne garde que le maximum, ou la moyenne, des valeurs qu'elle recouvre. Le maximum est le choix dominant, une fenêtre de 2 × 2 divise la résolution par quatre, et chaque canal est traité séparément. Nous ne l'utiliserons pas au laboratoire, qui réduit par le pas de la convolution ; j'en parle parce que la trace ci-dessous en contient, et parce que la semaine 5 expliquera pourquoi un réseau de valeurs peut avoir de bonnes raisons de s'en passer.

{{% comment %}}SOURCE: D2L ch.7 p.299-301{{% /comment %}}

Pour fixer tout cela, voici la trace de formes du réseau convolutif historique, celui qui lisait des chiffres manuscrits. C'est le modèle de calcul que je vous demande d'imiter au laboratoire.

| Étape | Forme du tenseur |
| --- | --- |
| image d'entrée, un seul canal | 28 × 28 |
| après une première convolution et sa réduction | 6 × 14 × 14 |
| après une seconde convolution et sa réduction | 16 × 5 × 5 |
| après **aplatissement** (*flattening*) | 400 |
| puis trois couches entièrement connectées | jusqu'au nombre de sorties voulu |

{{% comment %}}SOURCE: D2L ch.7 p.303-305{{% /comment %}}

Vérifiez le 400 : \(16 \times 5 \times 5 = 400\). Ce nombre est le point de contact entre la partie convolutive et la partie dense, et c'est **le** calcul que les étudiants ratent. Mon conseil : calculez-le à la main, puis vérifiez-le en faisant passer un tenseur factice dans la partie convolutive seule et en lisant sa forme. Deux lignes de code contre une heure de messages d'erreur sur des dimensions incompatibles.

---

## La convention des canaux, et le geste `detach()`

Deux faits pratiques pour terminer, et tous les deux vous serviront en semaine 5.

Le premier est une **convention de disposition**. Les couches de convolution de PyTorch attendent un tenseur dont les axes sont, dans cet ordre, les **canaux**, la **hauteur**, la **largeur**. Or les images arrivent presque toujours avec le plan de couleur en **dernier** : une image d'arcade de 210 × 160 pixels en couleur se présente comme un tableau de forme (210, 160, 3). Il faut donc, avant toute chose, redimensionner l'image à la taille voulue, **déplacer l'axe des canaux de la dernière à la première position**, et convertir en flottants. C'est le travail d'une enveloppe, exactement au sens de la semaine 1, et c'est le seul fait dont le laboratoire a besoin.

{{% comment %}}SOURCE: LAPAN ch.3 p.105-106{{% /comment %}}

Le second est un geste, et je le présente délibérément parce que vous allez le réutiliser. Il arrive qu'on veuille utiliser le résultat d'un réseau dans le calcul de la perte d'un **autre** réseau, sans que les gradients ne remontent dans le premier. La méthode `detach()` fait exactement cela : elle renvoie une copie du tenseur **sans aucun lien avec le graphe de son parent**.

```python
sortie_a = reseau_a(x)
perte_b = critere(reseau_b(sortie_a.detach()), cible)   # gèle sortie_a en constante
perte_b.backward()                                      # aucun gradient ne va dans reseau_a
```

{{% comment %}}SOURCE: LAPAN ch.3 p.109{{% /comment %}}

> [!TIP]
 **La seule formule à retenir sur `detach()` : « geler une valeur en constante ».** Du point de vue de la rétropropagation, un tenseur détaché n'est plus un résultat de calcul, c'est un nombre tombé du ciel. Rien à dériver, donc rien à remonter. Notez-le bien : **la semaine 5 utilise exactement ce geste**, au cœur de son algorithme, et je m'arrête là volontairement. Quand vous le reverrez, vous saurez déjà ce qu'il fait ; il vous restera à comprendre pourquoi on le veut.

{{% comment %}}SOURCE: LAPAN ch.3 p.109{{% /comment %}}

Le cadre classique où l'on rencontre `detach()` est celui des **réseaux antagonistes génératifs** (*generative adversarial networks*), que la semaine 1 avait mentionnés en passant comme exemple d'**apprentissage non supervisé**. Deux réseaux y travaillent en sens contraire : le **générateur** fabrique des contrefaçons, le **discriminateur** tente de les démasquer, chacun avec son optimiseur et sa perte, sur les mêmes données. C'est le schéma à deux optimiseurs annoncé en section 2.5, et le `detach()` y sert à entraîner le discriminateur sans corriger le générateur du même coup.

```python
opt_gen = torch.optim.Adam(gen.parameters(), lr=1e-4, betas=(0.5, 0.999))
opt_dis = torch.optim.Adam(dis.parameters(), lr=1e-4, betas=(0.5, 0.999))
```

{{% comment %}}SOURCE: LAPAN ch.3 p.108-109{{% /comment %}}

Je ne ferai pas de ce montage le laboratoire de la semaine, et je préfère vous dire pourquoi plutôt que de vous laisser le découvrir : ce genre d'entraînement demande entre 40 000 et 50 000 itérations avant de produire quelque chose de regardable, soit environ une demi-heure de processeur graphique, et il suppose des ressources d'images que notre installation ne contient pas. Le laboratoire de cette semaine se mesure en minutes. Gardons le processeur graphique pour la semaine 5, où il servira à apprendre quelque chose.

{{% comment %}}SOURCE: LAPAN ch.3 p.110{{% /comment %}}
