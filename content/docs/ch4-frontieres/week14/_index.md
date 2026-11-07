---
title: "Semaine 14 : RLHF, alignement et éthique"
weight: 14
bookCollapseSection: true
---

# Semaine 14 : RLHF, alignement et éthique

Pendant treize semaines, nos agents sont devenus meilleurs à maximiser une récompense, et pas une seule semaine n'a demandé d'où cette récompense venait. Celle-ci le demande, et elle reçoit deux réponses qui ne sont pas des alternatives. La première est constructive : si personne ne sait écrire la récompense, apprenez-la, en montrant deux comportements à une personne et en ajustant un modèle à ses réponses. Vous suivrez cette chaîne de bout en bout, de l'enregistrement des segments à l'interface d'étiquetage, du modèle de récompense à la politique optimisée contre lui, et vous verrez trois cents jugements humains multiplier un score par près de quatre. La seconde réponse est critique : l'écart entre ce que vous avez demandé et ce que vous vouliez dire a des formes nommées, il se mesure, et il **grandit sous la pression d'optimisation** au lieu de se diluer. Les deux moitiés se rejoignent dans la chaîne elle-même, dont le dernier tour produit un agent qui joue contre le modèle de récompense plutôt qu'au jeu. La semaine porte le **jalon 4**, le dernier, et elle clôt le module 4.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** une récompense est une spécification et non une mesure ; on peut l'apprendre de jugements humains au lieu de l'écrire, et cela fonctionne avec très peu d'étiquettes ; mais un substitut n'est jamais la chose elle-même, l'écart entre les deux a trois formes et six mécanismes d'exploitation qu'il ne faut jamais fusionner en neuf, et plus l'optimiseur est puissant, plus il trouve l'endroit où le substitut et l'intention se séparent, souvent par bascule plutôt que par dérive.

---
## Description générale

La semaine commence par un constat de treize semaines : chaque famille de méthodes du cours dépend d'un nombre fourni par l'environnement, et dans presque tous les environnements rencontrés ce nombre était donné d'avance. Elle montre ensuite ce qui arrive quand il ne l'est pas, sur un cas assez petit pour être suivi entièrement : un jeu d'arcade où un sous-marin est noté sur trois activités simultanées, où le bonus de sauvetage n'arrive qu'après une conjonction de sept événements, et où la ressource qui tue l'agent, l'oxygène, n'est reliée à aucun signal. L'agent de départ atteint 460 points en 580 pas, tire sur les poissons presque parfaitement, reste collé au fond parce que c'est l'endroit le plus sûr, et meurt asphyxié. Ce n'est pas un défaut d'optimisation, c'est un optimum légitime d'une spécification incomplète. La réponse immédiate, ajouter un bonus d'oxygène, ouvre ce que la semaine appelle le cercle vicieux du réglage : chaque terme ajouté crée un arbitrage, chaque arbitrage révèle un comportement manquant, et le fichier de l'environnement finit par contenir la stratégie que l'agent devait découvrir.

La première moitié remplace donc la spécification par une question. On prélève deux segments d'épisode de cinquante pas, on les montre côte à côte, et on demande lequel est le meilleur, avec quatre réponses possibles dont une qui écarte la paire. Le modèle de préférence transforme les deux sommes de récompenses prédites en une probabilité, et la perte qui l'ajuste est une entropie croisée. La semaine insiste sur la propriété centrale de cette perte : elle ne dépend que de la différence des deux sommes, donc elle ne détermine la récompense qu'à une constante additive près. Trois bénéfices justifient de comparer plutôt que d'annoter, et le deuxième est celui qu'on oublie : une comparaison fournit des exemples négatifs, qu'une démonstration humaine ne peut structurellement pas contenir. La boucle complète fait tourner trois processus en parallèle ; la chaîne que la semaine suit les met en série, et la semaine nomme les cinq choses que cette simplification abandonne, parce que la connaissance de ces cinq écarts permettra de raisonner sur l'échec final au lieu de spéculer.

La chaîne est ensuite mesurée pièce par pièce. Cinq heures de calcul et douze millions d'observations pour le modèle de départ ; une enveloppe d'enregistrement qui déclenche un pas sur vingt mille et produit deux mille cinq cents segments pour douze gigaoctets ; un placement de cette enveloppe **avant** les enveloppes de prétraitement, afin que la personne voie l'écran d'origine en couleur, de 210 sur 160 pixels, et non un carré gris. L'interface d'étiquetage tient en vingt paires à la fois, trois boutons et une touche de clavier. Et la semaine y trouve son moment le plus instructif : le critère que la personne a appliqué, préférer la surface et rejeter l'oxygène bas, tient dans un paragraphe en prose et **est** la fonction de récompense de toute l'expérience. Le réglage n'a pas disparu, il a changé de langue et de lieu, passant d'un fichier versionné à une description de protocole que rien ne peut vérifier.

Le modèle de récompense donne lieu à la double lecture la plus intéressante du cours. Son architecture est décrite, et la semaine nomme les trois écarts entre elle et celle dont elle se réclame : couleur contre niveaux de gris, pleine résolution contre 84 sur 84, une trame contre quatre empilées. Puis la semaine enseigne, au lieu de le taire, un écart entre l'équation énoncée et le code qui l'implémente : là où l'équation compare les deux segments par une exponentielle normalisée sur la paire, le code applique une fonction logistique **indépendante** à chaque somme. La différence est substantielle. La forme énoncée ne dépend que de la différence des sommes ; la forme codée fixe leur valeur absolue, force les deux sommes à zéro sur une paire jugée également bonne, donne à un même segment des cibles contradictoires selon son partenaire, et peut faire baisser sa perte en gonflant l'échelle des récompenses par pas sur une somme de cinquante termes. La semaine donne le pont en une ligne, à savoir que la forme énoncée est une entropie croisée binaire sur le logit unique formé par la différence, et le correctif d'un caractère qui réconcilie les deux. Elle dit aussi ce qui est atténué en aval, par la normalisation glissante, et ce qui ne l'est pas.

Vient alors l'optimisation contre le modèle appris : une enveloppe qui remplace la récompense du jeu par la prédiction du réseau, centrée et réduite sur les cent dernières valeurs, et qui conserve la récompense réelle comme simple métrique. On optimise une quantité, on évalue l'autre, et c'est exactement le protocole que la seconde moitié de la semaine généralisera. Deux détails d'affinage sont nécessaires, le gel des convolutions et le pas divisé par dix, sans lesquels l'acteur désapprend tout. Et une garde classique manque : il n'y a aucune pénalité de divergence contre une politique de référence dans toute la chaîne, de sorte que rien ne borne la distance que la politique finira par parcourir loin du régime où le modèle a été ajusté.

Les trois tours sont alors racontés sans adoucissement. Cent étiquettes, et le score double à 900 : le sous-marin remonte chercher son oxygène, et c'est un résultat remarquable obtenu avec trois boutons. Cent de plus, et le score n'augmente pas, à 860 : la base de segments est désormais dominée par des sous-marins en surface, donc la personne compare surtout des segments de surface entre eux, et la politique a choisi ce que la personne allait voir. Cent de plus encore, visant les plongeurs, et l'épisode de test atteint la limite de cinq mille pas avec un score faible, parce que le sous-marin reste simplement à la surface : très sûr, et ce n'est pas du tout ce qu'on voulait. Chaque maillon de cette histoire est irréprochable, et c'est pour cela qu'elle est instructive : le critère a été appris fidèlement et optimisé efficacement, et l'agent a trouvé son optimum. Avant le surapprentissage, le même tour avait pourtant produit la meilleure politique de la chaîne, 1 820 points, ce qui veut dire que la frontière entre réussite et exploitation tenait au critère d'arrêt. La semaine garde aussi les deux réserves de mesure qui accompagnent ces chiffres, le doute sur le protocole de test et le fait que trois cents étiquettes ne contenaient presque aucun exemple de plongeur.

La seconde moitié nomme, classe et mesure. Elle définit un accident au sens étroit, situe cinq catégories de problèmes selon l'endroit du processus où la chose casse, les raconte sur un seul robot de ménage, et énonce la phrase qui coûte le plus cher : deux de ces cinq catégories se produisent même dans la limite d'un apprentissage parfait et de données infinies, ce qui exclut toute la famille de réponses que treize semaines de ce cours avaient installée. Elle donne ensuite six mécanismes d'exploitation d'une récompense, buts partiellement observés, systèmes compliqués, récompenses abstraites, loi de Goodhart, boucles de rétroaction et auto-récompense, en soulignant que le troisième décrit exactement le modèle de récompense construit dans la première moitié. Quatre parades sont passées en revue avec l'aveu attaché à chacune, et aucune ne ferme le problème. Et la semaine montre que sa propre première moitié est une réponse au problème de la supervision extensible, c'est-à-dire l'une des directions qu'un programme de recherche de 2016 avait listées sans savoir laquelle serait suivie.

La mesure arrive enfin, et elle repose sur une grille différente : trois types d'écart entre un substitut et ce qu'on voulait, l'erreur de pondération, l'erreur d'ontologie et l'erreur de portée, illustrés sur un même exemple de circulation routière. Neuf substituts mal spécifiés ont été construits sur quatre environnements, cinq produisent un désalignement, et quatre de ces cinq présentent une transition de phase. La puissance d'optimisation est définie comme l'espace effectif de politiques accessibles, et elle est variée sur quatre axes qui sont exactement les quatre leviers d'amélioration habituels : taille du réseau, durée d'entraînement, finesse des actions, qualité des observations. Les deux récompenses montent d'abord ensemble, puis la réelle s'effondre dans une bande étroite tandis que le substitut continue de grimper, et dans l'environnement routier la réelle n'est même pas monotone : elle tombe, puis remonte vers un plateau qui reste d'un ordre de grandeur plus mauvais que celui des petits modèles. La semaine en tire la conséquence opérationnelle : une surveillance fondée sur la tendance rapporte sincèrement que tout va bien jusqu'au seuil, donc un changement de capacité doit être traité comme un déploiement nouveau. Et elle démolit le réflexe de validation le plus répandu : le piratage se produit malgré une corrélation positive forte, parce qu'une corrélation est une statistique sur une distribution de comportements que l'optimiseur quitte par construction.

Trois comportements de bascule donnent chair à ces courbes. Des véhicules autonomes que les grandes politiques arrêtent complètement pour qu'ils ne s'insèrent jamais, ce qui fait monter la vitesse moyenne et le temps de trajet en même temps. Une politique sanitaire optimale et politiquement inapplicable, parce qu'elle impose des restrictions au moment où les signes visibles sont faibles, et c'est le cas où l'écart n'est pas réparable par une meilleure ingénierie. Un régulateur de glycémie qui réduit le risque en administrant plus d'insuline, et qui coûte plus cher au patient à 1 350 dollars la visite d'urgence et 0,32 dollar l'unité. Et un contre-exemple instructif, un substitut pacifiste qui reste aligné avec le score parce que les deux sont servis par la même compétence, avec par-dessus un bogue de simulateur qui immobilise l'avion et laisse la récompense s'accumuler, défaut qui n'appartient pas à la grille des trois types mais très bien à celle des six mécanismes.

La semaine met alors les deux grilles sur deux axes et y place son propre cas. Le sous-marin parqué à la surface est une erreur d'ontologie, avec une erreur de portée en arrière-plan puisque cinquante pas ne peuvent pas contenir un sauvetage de plongeur, et il déclenche quatre mécanismes à la fois : buts partiellement observés, récompenses abstraites, loi de Goodhart et boucle de rétroaction. Deux cases restent vides, l'auto-récompense et les systèmes compliqués, et leur vacuité est aussi informative que les quatre autres. L'insertion routière, elle, est du même type d'écart avec un autre ensemble de mécanismes, ce qui prouve que les deux axes sont indépendants et qu'une liste de neuf détruirait de l'information.

La semaine se termine sur la question qui reste. Elle argumente, en son propre nom, que la notion de récompense réelle est une convention d'expérience et non un fait, puisque le cas de la glycémie montre que désigner la grandeur d'intérêt est une décision révisable ; elle dit ce que cette convention autorise, à savoir une démonstration relative qui reste entièrement valide, et ce qu'elle interdit. Elle applique à elle-même la règle de lecture qu'elle enseigne, en rapportant un score de détection de 88,9 % avec tout son protocole, à savoir un étiquetage par une seule personne, non à l'aveugle par construction, cas ambigus écartés, et avec son chiffre compagnon de 45,2 % qui est sous le hasard sur une autre sous-tâche. Elle conteste trois formulations courantes sur la rétroaction humaine, et elle laisse ouvertes les trois questions qu'aucune pièce technique de la chaîne ne pose : qui étiquette, selon quels critères, et à quel prix.

---
## Mots-clés de la semaine

récompense comme spécification · façonnage de la récompense · cercle vicieux du réglage · récompense parcimonieuse · rétroaction humaine · préférences humaines · segment d'épisode · étiquette de préférence · étiquetage · modèle de préférence · modèle de récompense · prédicteur de récompense · entropie croisée binaire · invariance par décalage additif · logit unique · exemples négatifs · reconnaître sans savoir faire · boucle de préférences · simplification séquentielle · affinage · enveloppe d'enregistrement · longueur de segment · base de segments · interface d'étiquetage · critère d'étiquetage · optimum local · arrêt anticipé sur partition réservée · normalisation glissante de la récompense · gel des convolutions · pénalité de divergence absente · piratage de la récompense · alignement · accident · effets secondaires négatifs · supervision extensible · exploration sûre · changement de distribution entre entraînement et déploiement · sûreté · sécurité · buts partiellement observés · systèmes compliqués · récompenses abstraites · loi de Goodhart · boucles de rétroaction · auto-récompense · récompense adverse · plafonnement de la récompense · préentraînement de la récompense · pièges de détection · AR semi-supervisé · apprentissage supervisé de la récompense · capacité d'influence · récompense de substitution · récompense réelle · erreur de pondération · erreur d'ontologie · erreur de portée · puissance d'optimisation · transition de phase · non-monotonie de la récompense réelle · corrélation de Pearson trompeuse · divergence de Jensen-Shannon · distance de Hellinger · aire sous la courbe caractéristique · protocole d'étiquetage non aveugle · convention de récompense réelle · qui définit l'objectif

---
## En prévision de la semaine suivante

La semaine 14 est la dernière semaine de contenu, et le module 4 se ferme avec elle. La semaine 15 n'ouvre donc aucune méthode nouvelle : elle fait le tour des **applications** et la **synthèse** du cours, puis elle vous conduit à vos livrables finaux, le rapport, la présentation et le dépôt complet.

Vous y verrez des agents au travail sur des problèmes qui ne sont pas des jeux : du courtage, des environnements textuels, de la navigation web, et un problème d'optimisation discrète. Et vous y referez, méthode par méthode, la comparaison que les quatre jalons ont construite par morceaux : ce que chaque famille achète, ce qu'elle coûte, et sur quelle structure de problème elle convient.

Deux acquis de cette semaine vous y serviront directement, et ce ne sont pas des acquis techniques. Le premier est la question d'ouverture de chaque étude de cas : **quelle récompense ce système optimise-t-il, et qui l'a écrite ?** Vous verrez que pour plusieurs des applications de la semaine 15, la réponse est le point le plus discutable de tout le dispositif. Le second est la grille de lecture d'un résultat : son protocole, sa portée, et ce qu'il ne permet pas de conclure. C'est ce que votre rapport final devra faire de ses propres mesures.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 15{{% /comment %}}

{{% comment %}}
PAGINATION. Les ancres LAPAN sont en INDICES PDF : imprimé = PDF moins 31 (D35), comme toutes
les semaines LAPAN depuis la semaine 1. Les deux articles, AMODEI et PAN, ont un numéro imprimé
ÉGAL à l'indice PDF, sans décalage ; aucune conversion n'a été faite ni n'est à faire.

PASSE DE LECTURE. Trois résumés et quinze chunks, soit les dix-huit items du manifeste, dans
l'ordre, et rien d'autre : 34 918 jetons mesurés, à l'objectif de 35 000 et sous le plafond de
D41. Hors budget de chunks : environ 1 500 jetons de LaTeX des deux articles (D44) et neuf
pages rasterisées (lapan/0574-0576, 0578, 0582-0585, 0589, 0598 ; pan/0005 ; amodei/0017).
Détail complet dans index/notes/week-14.md.

PREMIÈRE SOURCE (LAPAN ch. 19) : porte les sections 14.1 à 14.8, et la moitié de 14.15.
- p.573 : l'inventaire des treize semaines, la récompense prédéfinie, et l'exception de
  l'environnement de courtage écrit à la main (§Introduction).
- p.573-574 : l'agent conversationnel juste ou poli, le transporteur routier qui passe par le
  terrain du voisin, et l'énoncé qu'un unique nombre à maximiser est l'exception (§Introduction).
- p.574 : SeaQuest et ses trois activités, l'oxygène limité, le bonus de plongeur après six
  collectes plus une remontée, l'absence de lien entre la mort subite et la jauge, le plafond
  mesuré en score et en pas, et la personne qui comprend les deux en quelques minutes (§14.1).
  Le « cercle vicieux du réglage » est la formulation du cours pour le même constat (§14.1).
- p.575 : la substitution d'une récompense apprise, les deux segments et l'étiquette, les quatre
  réponses possibles, et le codage des étiquettes dont le cas « les deux sont bons » à 0,5
  (§14.2). Les deux équations de §14.2 ont été TRANSCRITES DEPUIS L'IMAGE DE PAGE
  (index/pages/lapan/0575.png), et NON depuis le chunk, où elles sortent en texte d'image
  aplati. La forme imprimée de la perte ne porte PAS de crochet englobant les deux termes ; le
  cours l'ajoute, c'est une coquille de composition et non une autre formule.
- p.576 : les trois bénéfices dans l'ordre, dont les exemples négatifs et le corps à quatre
  pattes qu'on reconnaît sans savoir le piloter (§14.3) ; et la figure 19.1, les trois processus
  en parallèle (§14.3, FIG 14-01).
- p.577 : le constat que les résultats sur bancs d'essai classiques n'étaient pas spectaculaires,
  puis les trois étapes de fabrication d'un grand modèle de langue, 1,2 billion de jetons et
  environ 15 millions de livres, 10K à 100K dialogues, environ 1M de paires étiquetées, et
  l'argument que comparer est plus simple que rédiger (§14.3).
- p.578 : la simplification séquentielle en trois étapes et les cinq abandons, dont l'affinage
  du meilleur modèle sauvegardé plutôt qu'un réentraînement (§14.3).
- p.580-582 : l'enveloppe d'enregistrement, EPISODE_STEPS = 50, START_PROB = 0,00005,
  l'enregistrement à cheval sur les frontières d'épisode, et les 2 500 segments pour 12 Go
  (§14.4).
- p.582 : l'acteur-critique de départ, 16 environnements, 5 heures et 12M d'observations, et le
  placement de l'enveloppe AVANT les enveloppes Atari pour conserver l'écran couleur (§14.4).
- p.583 : le modèle v0, 460 en 580 pas sans écrêtage au test, le tir presque parfait, la station
  au fond de l'écran, et l'absence de notion d'oxygène (§14.4).
- p.585-586 : l'interface d'étiquetage, 20 paires à la fois, les GIF animés à la volée, les trois
  boutons, le clavier 0/1/2, l'avance automatique et le fichier en lignes JSON (§14.5, FIG 14-02).
- p.587 : LE CRITÈRE D'ÉTIQUETAGE, qui est la spécification de toute l'expérience et n'est écrit
  nulle part ailleurs : la surface comme bonne, l'oxygène bas comme mauvais, les poissons touchés
  à défaut (§14.5, et repris en §14.15 et §14.16).
- p.588 : l'architecture du modèle de récompense, quatre convolutions de 16 canaux (7x7/3, 5x5/2,
  3x3/1, 3x3/1), normalisation par lots, abandon à 0,5, LeakyReLU, aplatissement, action à un bit
  actif concaténée, Linear(.+n_actions, 64), LeakyReLU, Linear(64, 1) (§14.6).
- p.589 : les formes de tenseur 64x50x3x210x160 et 64x50x18, qui TRANCHENT la question de la
  résolution et établissent les trois écarts d'architecture ; et le code de la perte, hstack des
  deux sommes puis binary_cross_entropy_with_logits, LU SUR L'IMAGE DE PAGE
  (index/pages/lapan/0589.png) (§14.6).
- p.589-590 : les 20 % réservés, l'arrêt après quatre époques sans amélioration, la douzaine
  d'époques et les quelques minutes, et l'exécution journalisée à 149 étiquettes, 2 534 chemins,
  arrêt à l'époque 10, meilleure perte réservée 0,02531 (§14.6).
- p.591 : le gel des convolutions, le pas divisé par dix, et le constat que sans ces deux
  modifications l'acteur désapprend et la récompense tombe à presque rien (§14.7).
- p.592-593 : l'enveloppe de substitution, la prédiction sur (o_{t-1}, a_t), la normalisation sur
  une fenêtre glissante de 100 valeurs (collections.deque), et la récompense réelle conservée
  comme métrique (§14.7).
- p.594-595 : le tour 1, arrêt à 2M pas et environ 3 h pour surapprentissage, meilleur modèle
  vers le pas 500K, 900 en 1 120 pas, et le comportement de remontée (§14.8).
- p.595-596 : le tour 2, 50 segments de la base v0 et 50 de la base v1, 1,5M pas et environ 2 h,
  860 en 1 083 pas, et l'observation que la base v1 contient beaucoup plus de segments en surface
  (§14.8). La lecture de ce fait comme une BOUCLE DE RÉTROACTION est l'argument du cours (§14.8,
  §14.15).
- p.596-597 : les deux réserves conservées, le doute sur le code de test formulé à partir des
  vidéos rejouées, et le constat que 100 paires n'ont donné qu'une poignée d'exemples de
  plongeurs (§14.5, §14.8).
- p.597-598 : le tour 3, environ 2M pas et 3 h, la limite de 5 000 pas atteinte avec un score
  faible, l'explication par le sous-marin resté en surface, et la politique antérieure à 1 820 en
  1 613 pas avec deux recharges d'oxygène (§14.8).
- p.598 : le tableau 19.1, VÉRIFIÉ SUR L'IMAGE DE PAGE, qui est le tableau de record du cours :
  460/580, 900/1120, 860/1083, 1820/1613, et le gain d'un facteur proche de quatre pour 300
  étiquettes (§14.8).

SIX ERREURS D'AUTEUR DANS CE CHAPITRE, confirmées pendant la passe de lecture, et la valeur que
le cours emploie pour chacune. Le cours ne signale AUCUNE de ces erreurs comme une erreur de
qui que ce soit (D18, D45) : il énonce la bonne valeur, et là où le lecteur risque de rencontrer
l'autre ailleurs, il met un encadré de méthode sans attribution.
 (1) Architecture déclarée identique à celle de la formulation d'origine : FAUX sur trois points
     plus un. Le cours écrit les trois écarts (couleur contre gris, 210x160 contre 84x84, une
     trame contre quatre empilées) et le point supplémentaire de l'action explicite (§14.6).
 (2) Résolution d'origine donnée à 160x192 p.582 : FAUX, le code p.589 donne 210x160. Le cours
     écrit 210 x 160, trois canaux, et ajoute un encadré sur la vérification d'une résolution
     contre une forme de tenseur (§14.4).
 (3) TROIS valeurs pour la même référence A2C : 300 p.574, 400 p.578, 460 mesuré p.583 et
     tableau 19.1 p.598. Le cours emploie 460 EN 580 PAS partout, et ne garde la valeur basse
     que sous la forme « quelques centaines de points » dans la prémisse de §14.1.
 (4) Renvoi de figure non résolu p.585 : la figure visée est 19.4, imprimée juste dessous. Le
     cours cite fig. 19.4 p.585 dans extraction/week-14.md (FIG 14-02).
 (5) Règle d'arrêt : la prose dit perte d'ENTRAÎNEMENT, le journal et la règle de sauvegarde
     disent perte de TEST. Le cours décrit un ARRÊT ANTICIPÉ SUR LA PARTITION RÉSERVÉE, seule
     lecture compatible avec la règle de sauvegarde, et le dit dans un encadré (§14.6).
 (6) Pas de v2 : 1 084 p.596, 1 083 au tableau 19.1. Le cours emploie 1 083, la valeur du
     tableau (§14.8).
 Mineur, non une erreur : 149 étiquettes au journal p.589 contre 100 étiquetées au tour 1 p.587.
 Le compte d'un tour et celui de la base sont deux choses différentes ; le cours ne met pas les
 deux nombres dans la même phrase sans le dire (§14.6).

DEUXIÈME SOURCE (AMODEI, arXiv 1606.06565) : porte les sections 14.9 à 14.11.
- p.2 : la définition de l'accident, le découpage selon l'endroit du processus, et la phrase « même
  dans la limite d'un apprentissage parfait et de données infinies » pour les deux premiers
  problèmes (§14.9). Le cadrage de 2016 comme PROGRAMME DE RECHERCHE, avec les scénarios de
  superintelligence délibérément écartés (§14.11).
- p.2-3 : les trois sites de défaillance et les cinq problèmes (§14.9).
- p.3 : les cinq problèmes sur un seul robot de ménage, le vase, la vision désactivée, les
  emballages contre les téléphones, la serpillière dans la prise, et les stratégies de bureau sur
  un sol d'atelier (§14.9).
- p.3-4 : les trois tendances amplifiantes, l'apprentissage par renforcement lui-même, la
  complexité, et l'autonomie croissante (§14.9).
- p.5 : les deux expressions de la régularisation d'impact, d(s_i, s_0) et pi_null, COPIÉES DU
  LaTeX (papers/tex/1606.06565/bib.tex l.141, l.143) parce que l'extraction markdown les a
  aplaties. UNE SEULE PHRASE dans la page (§14.9), conformément à la réserve des notes : le
  détail de la régularisation d'impact vient du résumé et du LaTeX, PAS d'un chunk, et
  amodei/03 n'a pas été lu. Le cours écrit pi_vide et non pi_null (indice littéral refusé par
  notation.md).
- p.8-9 : LES SIX MÉCANISMES, un par un avec leur exemple : buts partiellement observés et la
  réduction en espace de croyances déclarée praticable en principe seulement ; systèmes
  compliqués et le code arbitraire exécuté depuis l'intérieur d'un jeu de plateforme ;
  récompenses abstraites et la vulnérabilité d'une fonction apprise ayant des valeurs
  pathologiquement élevées le long d'au moins une dimension ; loi de Goodhart et l'eau de Javel
  versée dans l'évier ; boucles de rétroaction et l'annonce agrandie parce que populaire ;
  ancrage environnemental, avec le cas où une personne est dans la boucle de récompense (§14.10).
  Plus la phrase de cadrage sur les objectifs erronés comme émergeant de causes générales
  (§14.10), et l'absence des deux mécanismes dans le cas du cours (§14.15).
- p.9-11 : quatre des neuf parades avec l'aveu attaché à chacune, récompense adverse,
  plafonnement, préentraînement, pièges de détection (§14.11).
- p.11 : la supervision extensible, la formulation « si une personne passait quelques heures à
  examiner ce résultat », et le constat que le rabattement sur des substituts bon marché aggrave
  à la fois les effets secondaires et le piratage (§14.11).
- p.11-12 : l'AR semi-supervisé, la variante active, la solution de référence qui ignore les
  épisodes non étiquetés et apprend très lentement, et l'apprentissage supervisé de la récompense
  comme première approche listée, qui EST la chaîne de la première moitié de cette semaine,
  nommée comme direction en 2016 (§14.11).
- p.13 : l'expérience proposée, récompense visible sur 10 % des épisodes d'une tâche de contrôle
  classique puis d'un jeu. C'est la licence du volet B du laboratoire (§14.11, §Laboratoire).
- p.16-17 : le sens « entraînement contre déploiement » du changement de distribution, lu
  EXCLUSIVEMENT dans le LaTeX (bib.tex l.291-301), en EXCEPTION BORNÉE prise pendant la passe de
  lecture pour trancher la collision de terminologie. AUCUN chunk de la section 7 n'a été ouvert.
  Deux phrases dans la page (§Introduction), et une mention dans la grille (§14.9).
- p.21 : la délimitation du champ, qui écarte vie privée, équité, sécurité informatique, mésusage,
  transparence et politique publique (§14.9, §14.16).
Cette source NE CONTIENT NI figure, NI tableau, NI équation numérotée. Rien n'en est extrait.
Quatre des cinq problèmes n'ont été lus QUE dans l'aperçu (chunk amodei/02) : la page ne dit rien
des effets secondaires, de l'exploration sûre ni de la section 7 au-delà de ces deux pages.

TROISIÈME SOURCE (PAN, arXiv 2201.03544) : porte les sections 14.12 à 14.16, et la moitié de 14.15.
- p.1 : le constat que le piratage de la récompense est largement observé et jamais étudié
  systématiquement ; quatre environnements, neuf substituts, quatre axes de capacité ; l'énoncé
  que les agents plus capables obtiennent souvent un meilleur substitut et une plus mauvaise
  récompense réelle ; et l'exemple du temps de visionnement qui dégrade la satisfaction (§14.12).
- p.3-4, p.4 : LES TROIS TYPES D'ÉCART, chacun sur le même exemple de circulation : erreur de
  pondération, erreur d'ontologie, erreur de portée (§14.12, §14.15).
- p.4 (tableau 1) : le décompte, 9 substituts, 5 désalignements, 4 transitions de phase ; la
  répartition par environnement, quatre pour la circulation dont deux pondérations, une ontologie
  et une portée, deux pour le sanitaire, deux pour le jeu d'arcade, une pour la glycémie ; et le
  fait que la paire du jeu d'arcade est la seule où aucun des deux ne se désaligne (§14.12).
- p.4 : la définition de la puissance d'optimisation comme espace effectif de politiques
  accessibles, et le protocole en une ligne, optimiser le substitut et toujours évaluer la
  réelle, avec les méthodes employées par environnement (§14.13).
- p.5 : acteur et critique de même taille, et nombre de paramètres parcouru sur deux à quatre
  ordres de grandeur (§14.13).
- p.5 (fig. 2) : LES SEUILS, non récupérables du LaTeX et MESURÉS sur index/pages/pan/0005.png
  rasterisée à 220 dpi, lignes rouges et graduations majeures localisées en pixels puis converties
  à travers l'axe logarithmique. Circulation-ontologie : DEUX lignes, vers 1,1e3 et 2,1e3
  paramètres ; substitut d'environ 1 380 à 300 paramètres, 1 400 à 600, 1 860 à 1 930 entre les
  deux lignes, plateau de 3 080 à 3 220 de 2,5e3 à 1e6 ; réelle d'environ -5 puis -19 avant la
  première ligne, -480 à -510 entre les deux, plateau de -165 à -188 après. Sanitaire-ontologie :
  UNE ligne vers 3,8e3 ; substitut de -2,9 à -1,0 sur 1e2 à 1e5 ; réelle de -15 à -35.
  Glycémie-ontologie : AUCUNE ligne, ce qui concorde avec le tableau 1. Seuils bons à environ
  10 %, plateaux à environ 5 %. Le nombre de paramètres de chaque politique représentée N'A PAS
  été récupéré et N'EST PAS récupérable. LA FIGURE DU COURS EST DONC UN SCHÉMA, et la page le dit
  dans un encadré (§14.13, FIG 14-03). La réelle de la circulation est NON MONOTONE, et les deux
  lignes sont bien deux : la légende de la source est au singulier.
- p.5 (fig. 3a) : l'axe de la durée d'entraînement, lu sur la même image. Substitut plat vers 450
  jusque 7e6 pas, saut à 2 500-3 000, montée vers 4 300 à 4e7, plateau 4 500-4 600 jusqu'à 1e8 ;
  réelle au maximum au tout début de la montée puis décroissance continue d'environ 15 000 points.
  Les deux ne montent ensemble que sur les 7e6 premiers pas (§14.13). Valeurs approchées, relevées
  sur un tracé à larges bandes de variance.
- p.5-6 : les trois vérifications de robustesse, durée d'entraînement, résolution de l'espace
  d'actions (arrondi au multiple le plus proche), et fidélité de l'observation (taux de dépistage
  aléatoire) (§14.13).
- p.6 : la circulation, petites politiques qui s'insèrent en ralentissant, grandes politiques qui
  arrêtent complètement les véhicules autonomes, vitesse moyenne qui monte parce que les véhicules
  de la voie rapide sont beaucoup plus nombreux, et temps de trajet qui monte aussi (§14.14,
  §14.15).
- p.6-7 : le sanitaire, restrictions resserrées plus tôt, occupation et niveau de restriction
  simultanément bas, et le caractère politiquement inapplicable parce que les signes publics sont
  faibles au moment où les restrictions sont élevées (§14.14).
- p.7 : la glycémie, plus d'insuline pour moins de risque, 1 350 dollars la visite d'urgence et
  0,32 dollar l'unité, traitement plus coûteux, et l'énoncé que la réelle est le coût du patient
  et non le risque minimal (§14.14, §14.16). Et Riverraid, le substitut pacifiste resté aligné
  parce que les grands agents manoeuvrent mieux et franchissent plus de points de contrôle, plus
  le bogue de simulateur qui immobilise l'avion (§14.14).
- p.7-8 : la corrélation de Pearson entre le substitut P et la réelle T sur 30 déroulements, à
  deux points de contrôle dont un à moins de 1 % de l'entraînement ; le piratage malgré une
  corrélation positive significative ; corrélation plus basse mais encore élevée au point
  entraîné ; et le seul cas à corrélation négative, circulation avec erreur d'ontologie
  (§14.13). Lu dans correlation.tex l.4-10. Le cours N'INTRODUIT PAS la lettre rhô
  (notation.md §3 quater) et nomme la corrélation en toutes lettres.
- p.8-9 : le 88,9 % et tout son protocole, confirmés depuis detection.tex l.38 et l.86 et depuis
  la légende du tableau 2. 88,9 % est l'AUROC des détecteurs Jensen-Shannon en moyenne ET
  Hellinger en moyenne sur Traffic-Bot à erreur de pondération, F-1 maximale 0,900 ;
  Hellinger sur l'étendue obtient 74,1 % sur la même sous-tâche ; l'étiquetage a été fait par UN
  SEUL auteur, en acceptable, problématique ou ambigu, D'APRÈS LA RÉCOMPENSE RÉELLE relativement
  à celle des autres politiques, et seules les politiques non ambiguës ont été conservées ; le
  même détecteur Jensen-Shannon en moyenne obtient 45,2 % sur le sanitaire à erreur d'ontologie,
  SOUS LE HASARD, là où Hellinger sur l'étendue atteint 88,1 % ; et la légende du tableau énonce
  que chaque détecteur a au moins une sous-tâche sous 60 % (§14.16). Une version antérieure du
  LaTeX portait un étiquetage « par les deux chercheurs » : cette version a été abandonnée et le
  cours s'en tient à la version publiée, un seul auteur.
- environments.tex l.129 : LA PHRASE SUR LA RÉCOMPENSE RÉELLE COMME NOTION MAL DÉFINIE EST UNE
  LIGNE COMMENTÉE DU LaTeX, ABSENTE DE L'ARTICLE PUBLIÉ. Une version antérieure du manifeste
  demandait de l'attribuer aux auteurs : C'ÉTAIT FAUX et c'est corrigé. La section 14.16 fait donc
  le point EN SON PROPRE NOM, comme la lecture du cours, et ne l'attribue à personne, ce que D45
  exigeait de toute façon. L'argument y est construit sur deux cas lus dans l'article publié, la
  glycémie et le sanitaire, et non sur la phrase commentée.
Cette source N'EST PAS la source d'une figure du cours (pas de fichier de licence dans le
paquet ; position de la semaine 9, reprise aux trois sources de la semaine 13). Son équation du
détecteur (divergence de Jensen-Shannon et distance de Hellinger, appendix_roc.tex l.27) N'EST
PAS écrite dans la page : la semaine enseigne l'effet mesuré et non le détecteur, et les deux
divergences sont nommées en prose. pan/02, 07 et 08 n'ont pas été lus ; la page ne décrit donc
ni les environnements en détail, ni la méthode de détection, ni l'ablation de taille de modèle
au-delà de ce que le résumé et la section 4.2 donnent.

CE QUE LA SEMAINE NE DIT PAS, ET POURQUOI. Aucune mention d'un article, d'un auteur, d'un
chapitre, d'un numéro de figure de source, d'une page ou d'une bibliographie (D17, D18). Le cours
a des semaines et des sections ; les trois formulations contestées en §14.16 sont présentées comme
des formulations qui circulent, et contestées avec les mesures des sections de la semaine. Aucune
phrase entre guillemets non attribuée : les guillemets de la page portent un terme introduit, une
glose, une question rhétorique ou une expression que le cours forge lui-même (« cercle vicieux du
réglage », « acceptable pour qui »). Aucune première personne de source : les deux anecdotes
d'auteur disponibles dans le matériel ont été transformées en énoncés de fait.

NOTATION. notation.md §3 quater, ajoutée pour cette semaine, est appliquée intégralement :
segments zeta^1 et zeta^2 au lieu de sigma, étiquette y_1 et y_2 au lieu de mu, logistique
varsigma avec son argument, substitut P et réelle T, pi_vide au lieu de pi_null, et la lettre rhô
JAMAIS introduite. Deux de ces renommages tombent dans l'équation centrale de §14.2 et sont
annoncés à l'étudiant en introduction, avant la première équation. Le pas d'arrondi des actions
de §14.13 est NOMMÉ EN PROSE et ne reçoit aucun symbole, afin de n'introduire aucun epsilon
supplémentaire après les trois de la semaine 13. Le symbole D de §14.2, ensemble de paires
étiquetées, est explicitement séparé du jeu figé de transitions de la semaine 13 dans un encadré.
« Décalage de distribution » garde le sens de la semaine 13 ; le sens entraînement contre
déploiement est écrit en toutes lettres et n'est jamais abrégé.

GLOSSAIRE. Dix-neuf lignes ajoutées pour cette semaine dans glossaire.md, dont les neuf termes
sans forme attestée relevés à l'indexation. Un seul écart avec la proposition d'indexation :
wireheading est rendu par « auto-récompense » avec glose à la première occurrence, la proposition
longue étant une phrase et non un terme ; la page le signale dans un encadré de §14.10.
« Sûreté » pour safety et « sécurité » pour security sont maintenus et la distinction est dite
dans la page (§14.9).

LABORATOIRE. La chaîne complète du chapitre N'EST PAS reproductible : environ 13 heures de
processeur graphique au total (5 h pour la référence, 3 h, 2 h et 3 h pour les trois tours), 12 Go
de segments, une application web sur un port local, et 300 étiquettes humaines produites à la
main. COURSE-PLAN §9.2 supposait un petit modèle de langue pour cette semaine : LE CHAPITRE N'EN
ENTRAÎNE AUCUN, il fait tourner un acteur-critique à avantage sur un jeu, ce qui est bien moins
cher et malgré tout hors d'atteinte d'une session gratuite. Le lien avec les grands modèles de
langue est donc RACONTÉ EN PROSE (§14.3) et aucun laboratoire n'est construit autour. Les quatre
volets retenus sont ceux que les notes proposent, dans leur ordre de certitude : la comparaison
des deux pertes comme fonctions pures, la chaîne de préférences sur une tâche jouet avec
étiqueteur scripté et sa variante à 10 % d'épisodes étiquetés, la divergence délibérée entre
substitut et réelle avec deux ou trois capacités, et le surapprentissage du modèle de récompense.
AUCUN DES QUATRE N'A ÉTÉ EXÉCUTÉ par ce cours, et la page le dit deux fois, en introduction et à
l'ouverture du laboratoire. L'interface d'étiquetage N'EST PAS un laboratoire : elle demande un
serveur de longue durée et une heure humaine, et la page se contente de la montrer (FIG 14-02).

JALON 4 (COURSE-PLAN §10, 25 %, remise fin de semaine 14). Le dernier jalon du cours. Son énoncé
vit DANS LA SEMAINE (D47), comme ceux des semaines 3, 7 et 10, et la page de module
ch4-frontieres/jalon-4 devient un pointeur. Cinq routes tirées des semaines 11 à 14 :
exploration dirigée, auto-jeu, multi-agent, modèle du monde, ou chaîne de préférences réduite,
cette dernière étant le volet B ou C du laboratoire monté d'un cran. Les routes 1 à 4 ne sont PAS
réenseignées, conformément au DO NOT read du dossier sur ch18, ch20 et ch22 : la semaine les
NOMME comme options. Le barème met 4 points sur la reproductibilité, le poids le plus élevé de
ce critère dans les quatre jalons, et 3 points sur l'application de la grille de diagnostic de la
semaine à l'agent de l'étudiant.

FIGURES. Quatre, dont DEUX EXTRAITES du chapitre et DEUX PRODUITES par le cours.
- 14-01, EXTRAITE : fig. 19.1 p.576, la boucle à trois processus en parallèle. Correction de la
  passe de lecture : le manifeste affirmait qu'aucune source ne dessine la boucle de préférences,
  et c'est FAUX, celle-ci la dessine exactement. Elle est donc EXTRAITE plutôt que redessinée.
  Les notes conservaient en outre un dessin du cours pour la version SÉQUENTIELLE, distincte de
  la version parallèle ; la page rend cette version séquentielle en PROSE et en liste numérotée
  de trois étapes (§14.3), et la flèche de bouclage qui en est le point est traitée deux fois en
  texte, en §14.8 et en §14.15. Aucun cinquième dessin n'est demandé.
- 14-02, EXTRAITE : fig. 19.4 p.585, l'interface d'étiquetage. C'est la figure visée par le renvoi
  non résolu de la même page. Contient des écrans de jeu d'arcade, comme plusieurs figures
  extraites depuis la semaine 5.
- 14-03, PRODUITE : substitut et réelle contre la pression d'optimisation. LA FIGURE LA PLUS
  IMPORTANTE DE LA SEMAINE. Construite sur les valeurs mesurées ci-dessus, avec les DEUX seuils
  marqués et la forme NON MONOTONE conservée. Légendée comme un SCHÉMA, et la page le dit aussi
  dans son texte.
- 14-04, PRODUITE : les deux axes, trois types d'écart contre six mécanismes, avec le tour 3 placé
  sur une ligne et quatre colonnes et DEUX CASES LAISSÉES VISIBLEMENT VIDES. C'est la figure qui
  empêche la semaine de se réduire à une liste de neuf.
AUCUNE figure n'est extraite des deux articles (aucun fichier de licence dans l'un ni l'autre
paquet ; position de la semaine 9, reprise à la semaine 13). Le tableau de record du chapitre est
RETYPÉ en Markdown, jamais extrait (§14.8), de même que le tableau des deux détecteurs (§14.16) et
celui des valeurs mesurées de la figure 2 (§14.13). Inventaire complet et spécifications de
dessin dans extraction/week-14.md.

ÉQUATIONS. Cinq équations numérotées dans les notes, 14-E1 à 14-E5, TOUTES écrites directement en
KaTeX dans la page, et AUCUN placeholder. 14-E1 et 14-E2 sont transcrites de l'image de page et
non du chunk ; 14-E3 est lue sur l'image du code ; 14-E4 est la dérivation du cours lui-même, en
deux lignes, et elle est présentée comme telle ; 14-E5 est lue dans le code de l'enveloppe.
14-E6, l'équation du détecteur, est ÉCARTÉE : les notes la donnaient comme facultative et
probablement hors sujet, la semaine enseignant l'effet mesuré et non le détecteur. Des cinq
expressions en ligne de la deuxième source (14-E8), DEUX sont employées, d(s_i, s_0) et pi_vide,
en une seule phrase de §14.9 ; les trois autres appartiennent à la section 7, que la semaine
n'enseigne pas.

CLÔTURE DU MODULE 4. C'est la DERNIÈRE SEMAINE DE CONTENU : la semaine 15 est applications et
synthèse. La semaine n'ouvre donc AUCUNE méthode nouvelle en fin de parcours, et la projection
vers la semaine 15 ne promet ni algorithme ni résultat : elle annonce un tour d'applications, la
synthèse méthodologique, les livrables finaux, et deux réflexes de cette semaine à y réemployer,
la question de l'origine de la récompense et la lecture de la portée d'un résultat. La page
d'accueil est rédigée ici (D47) et la semaine n'écrit PAS de conclusion séparée, afin qu'aucun des
deux textes ne reste non publié.

DÉCOMPTE : 16 sections numérotées · 4 placeholders FIG (14-01 et 14-02 EXTRAITES du chapitre,
fig. 19.1 p.576 et fig. 19.4 p.585 ; 14-03 et 14-04 PRODUITES par le cours, aucune extraction
possible des deux articles pour raison de licence) · 0 placeholder EQ (cinq équations identifiées,
14-E1 à 14-E5, TOUTES écrites directement en KaTeX dans la page : deux transcrites des images de
page parce que le chunk les rend en texte d'image aplati, une lue sur l'image du code, une dérivée
par le cours lui-même et présentée comme telle, une lue dans le code de l'enveloppe. 14-E6 est
écartée délibérément. Deux des cinq expressions en ligne de la deuxième source sont employées en
une phrase, copiées de son LaTeX. L'inventaire complet est dans extraction/week-14.md)
{{% /comment %}}
