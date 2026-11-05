---
title: "Semaine 2 : Apprentissage profond avec PyTorch"
weight: 2
bookCollapseSection: true
---

# Semaine 2 : Apprentissage profond avec PyTorch

Deuxième semaine, et un changement complet d'outil. Souvenez-vous de l'agent de la semaine 1 : sa ligne « décider » était un tirage au sort, et nous avons mesuré ce que cela donne. Cette semaine ne remplit pas cette ligne, elle **fabrique l'objet qui va la remplir**, un réseau de neurones construit et entraîné avec PyTorch. Il n'y a donc aucun apprentissage par renforcement dans ces neuf sections, et c'est entièrement assumé : nous ne pouvons pas brancher un outil que nous n'avons pas.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** sans fonction d'activation, empiler des couches n'achète **rien du tout**. Tout le reste, le graphe dynamique, les huit lignes de la boucle, Xavier, l'abandon de neurones, TensorBoard, est de l'outillage autour de cette vérité de deux lignes d'algèbre.

---
## Description générale

Les sections 2.1 à 2.5 montent l'outil dans l'ordre où l'on s'en sert. Le **tenseur** d'abord, seul objet que PyTorch manipule : ses types d'élément et le piège du flottant 64 bits, la différence entre opération en place et opération fonctionnelle, le périphérique de calcul et l'idiome d'un unique `torch.device`. La section 2.2 démontre ensuite, en deux lignes d'algèbre, pourquoi deux couches linéaires empilées **sans** fonction d'activation n'en valent qu'une, puis elle nomme les trois activations du cours et le chiffre qui reviendra deux sections plus loin, 0,25. La section 2.3 applique la **double lecture** à la rétropropagation : l'intuition d'un graphe parcouru dans les deux sens, la règle de dérivation en chaîne écrite couche par couche, puis l'unique appel `backward()` qui la réalise. Restent les briques de `torch.nn`, les deux gestes d'un module personnalisé, et la **boucle en huit lignes** que vous réécrirez jusqu'à la semaine 15.

Les sections 2.6 à 2.9 sont celles des ennuis et des remèdes. Nous nommons les deux pathologies du gradient, l'explosion et l'évanescence ; nous montrons la **brisure de symétrie**, que la descente de gradient stochastique par mini-lots ne répare pas ; et nous dérivons l'initialisation de Xavier en trois pas. Viennent ensuite les trois gestes de la généralisation, arrêt précoce, dégradation des poids et abandon de neurones, avec la mise en garde qui vaut pour les treize semaines suivantes : tout cela suppose une distribution de données **fixe**, ce que l'apprentissage par renforcement n'offre jamais. La section 2.8 explique pourquoi on n'aplatit pas une image et ce que coûte un biais inductif, et la section 2.9 installe TensorBoard, la fenêtre par laquelle vous regarderez tous les entraînements du cours.

Le laboratoire a un fil unique : **construire le réseau des semaines 4 à 15 et le regarder apprendre**. Une entrée qui est un vecteur d'état, une sortie par action, des scores bruts sans softmax, et des cibles fournies d'avance, fixes et parfaitement sages. Vous y reproduirez sur vos propres courbes trois résultats que la semaine énonce : la lenteur de la sigmoïde sur trois couches, une couche de 64 unités qui n'en utilise réellement qu'une, et une technique de régularisation qui **dégrade** les performances parce que les données ne la demandaient pas. Budget de calcul : quelques minutes au total, processeur graphique facultatif. Et la question qu'il laisse ouverte est exactement la bonne : d'où viennent ces cibles quand personne ne les fournit ?

---
## Mots-clés de la semaine

apprentissage profond · tenseur · type d'un tenseur · opération en place · tenseur scalaire · `item()` · périphérique de calcul · `to(device)` · perceptron multicouche · couche cachée · fonction d'activation \(\phi\) · unité linéaire rectifiée · fonction sigmoïde · tangente hyperbolique · approximateur universel · différentiation automatique · graphe de calcul · tenseur feuille · `requires_grad` · rétropropagation · propagation avant · règle de dérivation en chaîne · fonction objectif · module · couche linéaire · conteneur séquentiel · méthode forward · fonction de perte · optimiseur · boucle d'entraînement · lot · époque · accumulation des gradients · `zero_grad()` · stabilité numérique · gradient évanescent · gradient explosif · brisure de symétrie · initialisation des paramètres · initialisation de Xavier · généralisation · erreur de généralisation · écart de généralisation · surapprentissage · biais inductif · double descente · arrêt précoce · critère de patience · dégradation des poids · abandon de neurones · injection de bruit · invariance par translation · principe de localité · noyau de convolution · partage des poids · canal · carte de caractéristiques · remplissage · pas de la convolution · agrégation · aplatissement · détachement du graphe · `detach()` · suivi de l'entraînement · TensorBoard

---
## En prévision de la semaine suivante

Nous avons construit l'instrument, il est temps d'en jouer. La semaine 3 rebranche la boucle de la semaine 1 et le réseau de la semaine 2, et vous verrez un agent apprendre à tenir le bâton de CartPole bien au-delà des quelques dizaines de pas que vous avez mesurées. La méthode employée, l'entropie croisée, est d'une simplicité presque insolente : elle se résume à garder les meilleurs épisodes et à les imiter. Elle franchira une grande partie de l'écart jusqu'à 195, puis nous lui trouverons des limites, et ces limites seront le point de départ du module 2. Gardez sous les yeux la boucle en huit lignes de la section 2.5 et la table de correspondance : nous allons y brancher un environnement.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (D35), imprimé = PDF − 31 pour LAPAN et PDF − 40 pour D2L,
conformément à MAP-lapan.md et MAP-d2l.md, comme dans le dossier et les notes de phase 1.

LAPAN ch. 3 « Deep Learning with PyTorch », p. 82-110 : cadrage du chapitre et apport de
l'apprentissage profond à l'apprentissage par renforcement (82) ; tenseurs, fig. 3.1 →
FIG 02-01, mise en garde sur l'algèbre tensorielle (83) ; treize types d'élément, trois classes
usuelles, trois modes de création, mémoire non garantie (84) ; opération en place contre
opération fonctionnelle (85) ; conversion NumPy, piège du float64, from_numpy déprécié (86) ;
tenseur scalaire et item(), deux emplacements des opérations (87) ; torch.cuda, moteurs
d'exécution CPU/CUDA/MPS, to(device) (87-88) ; idiome d'un seul torch.device (89) ;
différentiation automatique comme fonctionnalité décisive (89) ; graphe statique contre graphe
dynamique, fig. 3.2 → FIG 02-04, torch.compile et mode immédiat (90-91) ; grad, is_leaf,
requires_grad (91) ; session v1/v2/v_sum/v_res, contagion de requires_grad, fig. 3.3 →
FIG 02-06 (91-93) ; gradients stockés sur les feuilles, retain_grad, lecture de la valeur,
gradients d'entrée (93) ; briques nn, convention callable, services de nn.Module (94) ;
nn.Sequential, dim=1 parce que la dimension 0 est le lot, Dropout(p=0.3) (95) ; deux gestes du
module personnalisé, add_module, ResNet à 1001 couches (96-97) ; ne jamais appeler forward(),
__str__/__repr__, contrôle de flux par lot (97-98) ; fonction de perte, quatre pertes
nommées (98-99) ; optimiseur, quatre optimiseurs, construction depuis parameters() (99-100) ;
boucle en huit lignes, époque et lot, accumulation des gradients, zero_grad() (100-101) ; deux
optimiseurs sur deux modèles (101) ; le code ne marche jamais du premier coup, liste de ce
qu'on surveille (101) ; TensorBoard, port 6006, MLflow (102) ; torch.utils.tensorboard,
SummaryWriter, add_scalar, runs/, log_dir, comment (103) ; flush, tensorboard --logdir,
--bind_all, liste Runs, au-delà des scalaires (104) ; convention canaux-hauteur-largeur et
redimensionnement 64 × 64 (105-106) ; deux optimiseurs Adam betas=(0.5, 0.999) (108) ;
detach() et item() dans la boucle antagoniste (109) ; coût du montage antagoniste, 40-50k
itérations, ~30 min de GPU (110).

D2L ch. 5 « Multilayer Perceptrons », p. 207-239 : cadrage du chapitre (207) ; limites du
modèle linéaire, monotonie, trois contre-exemples (208) ; empilement de couches, fig. 5.1.1 →
FIG 02-02, formes, « deux couches » (209) ; effondrement affine → EQ 02-E1, 02-E2, activation
et EQ 02-E3, approximateur universel (210) ; profondeur contre largeur, ReLU → EQ 02-E4
(211) ; dérivée de ReLU, pReLU, sigmoïde → EQ 02-E5 (212) ; dérivée de la sigmoïde →
EQ 02-E6, maximum 0,25, tanh → EQ 02-E7 (213-214) ; propagation avant, z/h/o/L →
EQ 02-E8 (220) ; fonction objectif, fig. 5.3.1 → FIG 02-05, prod → EQ 02-E9 (221) ; chaîne
arrière 5.3.8-5.3.14 → EQ 02-E10, formes (222) ; interdépendance aller/retour, mémoire
proportionnelle à profondeur × taille de lot (223) ; composition de L couches et produit de
matrices → EQ 02-E11 (224) ; explosif et évanescent, zone utile de la sigmoïde, stabilité de
ReLU (225) ; cent matrices gaussiennes et 10^25, brisure de symétrie, SGD par mini-lots
n'y suffit pas (226) ; initialisation par défaut, dérivation de Xavier → EQ 02-E12 (227) ;
compromis de Xavier → EQ 02-E13, variante uniforme, réserve sur l'hypothèse linéaire, résumé
du chapitre (228) ; généralisation comme objectif réel, théorie non réglée (229-230) ; biais
inductif, erreur et écart de généralisation, surapprentissage, double descente (230-231) ;
bornes classiques insuffisantes (231) ; arrêt précoce, critère de patience, étiquettes propres
d'abord (232-233) ; dégradation des poids, ridge et lasso (233) ; abandon de neurones et bruit
en entrée (234) ; co-adaptation, fig. 5.6.1 → FIG 02-07, débiaisage → EQ 02-E14 (235) ;
désactivation au test, incertitude, masque, probabilité plus faible près de l'entrée (236) ;
if self.training, hyperparamètres 256/0,5/0,5/lr 0,1 (237) ; nn.Dropout après chaque couche
dense (238).

D2L ch. 7 « Convolutional Neural Networks », LU AU SEUL NIVEAU DU RÉSUMÉ (D41) : invariance à
l'ordre des entrées (273) ; comptage du mégapixel, 10^9 (274) ; trois exigences (275) ; trois
ordres de grandeur, 10^12 → 4·10^6 → 4Δ² (276-277) ; noyau, partage des poids, prix du biais
inductif (277) ; carte de caractéristiques (279) ; forme de sortie nue, fig. 7.2.1 → FIG 02-08
(281) ; remplissage → EQ 02-E15, noyau impair p = k − 1 (289) ; pas et division entière →
EQ 02-E15 (290) ; compromis résolution contre canaux (293) ; noyau c_o × c_i × k_h × k_w
(294) ; agrégation sans paramètres, maximum, 2 × 2 (299-301) ; trace de formes LeNet-5
(303-305).

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossier week-02) : lapan/ch03/03-08 (PyTorch Ignite, et
il nomme PTAN → D12, semaine 6) ; d2l/ch05/05-03 (implémentation concise, D15) ; 05-08
(non paramétrique, k-NN, noyau tangent neuronal) ; 05-11 (tutoriel Kaggle) ; les 20 chunks de
d2l/ch07, lus par leur résumé. Bellman, amorçage, réseau cible, origine des cibles de Q →
semaines 4 et 5. Sutton & Barto non lu cette semaine.

ÉCARTS ASSUMÉS
- Convention : les équations de la semaine sont écrites en **convention colonne** de S&B
  (notation.md §6), là où la source écrit XW en convention ligne. L'effondrement devient donc
  W = W(2)W(1) et b = W(2)b(1) + b(2), facteurs inversés par rapport à la source.
- Activation notée φ et non σ (notation.md §5) ; σ(·) reste la sigmoïde.
- Terme de régularisation noté Ω et non s, qui est l'état dans ce cours. À inscrire dans
  notation.md.
- Variance des entrées notée σ_x² et non γ², qui est le facteur d'actualisation dans ce cours.
  Collision non signalée par les notes de phase 1. À inscrire dans notation.md.
- Quatre erreurs d'auteur repérées en phase 1 et NON propagées : zero_grads() (l'API est
  zero_grad(), et la section 2.4 le signale sans jamais écrire la forme fautive) ; « quatre
  types flottants » suivi de trois (le cours écrit quatre, et dit pourquoi : deux variantes de
  16 bits) ; point parasite en fin de la cinquième ligne du squelette de boucle ; numéros de
  version flottants entre deux valeurs selon les pages, d'où l'absence de toute version citée.
- Aucun numéro de version de PyTorch n'est donné, conformément à la règle posée en semaine 1.
- Les formules de forme de sortie avec remplissage et avec pas (EQ 02-E15) ne sont PAS écrites :
  les notes de phase 1 les donnent par leur numéro seulement, le chapitre 7 ayant été lu au
  niveau du résumé. Placeholder, et le laboratoire les contourne en faisant calculer la forme
  par une passe avant factice.
- Le montage antagoniste n'est pas le laboratoire (coût, ressources d'images) ; il n'apparaît
  que comme contexte de detach(), lequel est enseigné délibérément, sans dire à quoi la
  semaine 5 l'emploie.
- « agrégation » est introduite malgré la réserve des notes, parce que la trace de formes de
  LeNet-5 (28 → 14 → 5) est incompréhensible sans elle. « corrélation croisée », « champ
  réceptif » et « convolution 1 par 1 » restent pour la semaine 5.
- D15 : tout le code est réécrit (noms français, annotations de type, structure différente) ;
  rien n'est copié d'un dépôt.
- FIG 02-08 (fig. 7.2.1 p.281) est ajoutée délibérément hors du dossier, comme l'autorise la
  note de phase 1 (« gaps », point 3). FIG 02-03 et FIG 02-09 sont produites par le cours.

DÉCOMPTE : 9 sections · 9 placeholders FIG · 5 placeholders EQ
(02-E1 à 02-E9 et 02-E12 sont écrites directement en KaTeX ; 02-E10, 02-E11, 02-E13, 02-E14 et
02-E15 passent par un placeholder, voir extraction/week-02.md.)
{{% /comment %}}
