---
title: "Semaine 15 : Applications industrielles, synthèse et soutenance"
weight: 15
bookCollapseSection: true
---

# Semaine 15 : Applications industrielles, synthèse et soutenance

Quatorze semaines se sont chacune terminées sur une phrase de la forme « vous savez maintenant faire ceci ». Aucune ne s'est terminée sur celle dont vous allez avoir besoin : « vous savez maintenant choisir ». Cette dernière semaine n'enseigne donc aucune méthode. Elle vous apprend à poser à un problème que personne n'a préparé trois questions qui décident de tout : qu'est-ce qu'une observation, qu'est-ce qu'une action, quand arrive une récompense. Et elle le fait sur quatre problèmes délibérément étrangers les uns aux autres, un marché, un paragraphe, une page rendue dans un navigateur et une permutation d'un cube de Rubik, dont elle montre qu'ils réemploient tous les quatre une méthode enseignée entre les semaines 5 et 12, sans en modifier une ligne. Vous y trouverez aussi les deux derniers résultats négatifs du cours, une reproduction qui a échoué et deux rapports contradictoires d'une même expérience, trois méthodes dont le nom ne dit pas ce que fait le code, et une carte de décision qui range les quatorze semaines par caractéristique de problème plutôt que par ordre chronologique. La semaine porte les **livrables finaux** et elle clôt le module 5, et le cours.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** des trois objets d'un problème de décision, l'observation et l'action sont des contraintes que vous subissez et la récompense est la seule décision que vous prenez ; choisir une méthode consiste à caractériser ces trois objets avant de regarder les algorithmes ; et la seule propriété de votre travail qui décide si quelqu'un peut s'en servir n'est ni l'élégance de votre code ni la hauteur de vos courbes, c'est le fait que quelqu'un d'autre puisse l'exécuter.

---
## Description générale

La semaine ouvre sur un constat de quatorze semaines : le cours a été organisé par méthode, ce qui est le bon ordre pour apprendre une méthode et le mauvais pour en choisir une. Dans la vie, personne ne vous remet une méthode : on vous remet un problème. La semaine propose donc une procédure en trois questions, qu'elle applique quatre fois, et un tableau de quatre colonnes qui en est l'objet central : qu'est-ce qu'une observation, qu'est-ce qu'une action, quand arrive une récompense, et ce qui rend chaque problème difficile. La thèse qu'elle en tire est que l'observation et l'action sont des contraintes du problème, tandis que la récompense est la seule des trois qui soit conçue, et que c'est pour cela que c'est la colonne où les quatre problèmes diffèrent le plus : deux des quatre ont dû modifier leur récompense pour devenir apprenables, un troisième l'a écrite à la main de deux façons incompatibles, et le quatrième en a une que personne n'a voulue dépendante de la machine.

Les quatre problèmes sont ensuite pris un par un. Le marché est le rappel de la semaine 7 : trois actions, des prix réécrits en pourcentages de l'ouverture, deux schémas de récompense possibles, et un signal plus petit que le coût d'un aller-retour, d'où un agent qui ne tient au-dessus du seuil de frais que pendant quatre heures de marché. La décision la plus lourde n'y est ni dans l'observation ni dans la récompense mais dans le protocole, et la semaine rappelle la règle du cours sur le partage chronologique d'une série temporelle et les trois conséquences d'un partage inversé, dont la plus désagréable est que la fuite d'information passe par l'expérimentateur et qu'aucune relecture de code ne la détectera.

Le paragraphe est une tâche de fiction interactive. L'observation y est du texte, jusqu'à deux cents jetons sur un vocabulaire de mille deux cent cinquante, et elle ne montre pas l'inventaire, ce qui en fait un processus de décision partiellement observable. L'action est une phrase que l'agent produit au lieu de la choisir, et la probabilité de tomber au hasard sur la bonne suite de quarante jetons est de un sur dix puissance cent vingt-trois. La semaine ajoute pour son compte une distinction que rien n'oblige à faire et qui est pourtant nécessaire : ce nombre est la taille de l'espace des solutions complètes, tandis que l'espace d'actions par pas est de mille deux cent cinquante puissance huit, et c'est le second que la liste des commandes admissibles ramène à une douzaine. Deux béquilles rendent la tâche apprenable, cette liste et une récompense rendue dense sur demande, et la semaine insiste sur le fait qu'aucune des deux n'améliore l'agent : les deux changent le problème en demandant à l'environnement de révéler ce qu'il sait. Elle s'arrête aussi sur une leçon d'ingénierie qu'elle juge la plus réutilisable de la section : cet environnement ne respecte pas la convention de Gymnasium, renvoie quatre valeurs au lieu de cinq et ne déclare aucun espace, donc aucune enveloppe du cours ne s'y applique et il faut écrire un adaptateur. Et elle note la conséquence d'architecture : comme la liste des commandes change d'un état à l'autre, la tête à une sortie par action de la semaine 5 ne tient plus, et le réseau prend en entrée un couple observation-commande pour produire une seule valeur.

La page rendue est une tâche de navigation web. La semaine commence par rappeler que deux industries entières automatisent déjà ce travail sans rien apprendre, et que l'apport de l'apprentissage se limite à trois cas précis : un test qui généralise au lieu de casser au premier changement de mise en page, l'exploration de vulnérabilités, et le remplissage de formulaires sur des centaines de milliers de sites hétérogènes. Elle reprend à son compte le constat qu'un système d'extraction à taille réelle demanderait des mois de travail d'une équipe et que la plus grande part des difficultés ne concernerait pas l'apprentissage par renforcement, ce qui explique l'existence des jeux de référence et les deux conditions contradictoires qu'un bon jeu de référence doit satisfaire. Puis elle détaille la réduction d'un espace de clic libre à deux cent cinquante-six actions discrètes, avec le calcul exact qui donne seize par seize, et elle note que le nombre dix y est la taille d'une cellule en pixels et non le nombre de cellules. Elle montre que l'agent est sans mémoire, de sorte qu'une tâche en deux étapes brise la propriété de Markov, ce qui est le même diagnostic que l'inventaire invisible de la section précédente. Et elle s'arrête sur le danger de mesure le plus instructif du cours, trouvé à l'intérieur du jeu de référence lui-même : la récompense fournie est la récompense de la tâche multipliée par une décroissance en temps d'horloge, si bien que le même clic correct vaut 0,7936 en deux secondes avec le navigateur dessiné et 0,9918 en neuf centièmes de seconde sans interface, pour une récompense brute identique. Tout score publié sur cette famille de tâches est donc dépendant de la machine et du mode de rendu. La section se termine sur les démonstrations humaines, une semaine après les préférences humaines, en soulignant la différence structurelle, à savoir qu'une démonstration ne contient aucun exemple négatif, et en montrant que l'injection de données hors politique dans une méthode sur politique se fait en traitant la tête de politique comme un classificateur, c'est-à-dire en réemployant l'objectif de la semaine 4.

La permutation est un cube de Rubik, pris comme représentant de l'optimisation combinatoire. L'observation est l'état complet, l'action compte douze rotations en quarts de tour, et la récompense vaut plus un sur l'état résolu et moins un partout ailleurs : un bit, une seule fois, à la toute fin. La semaine donne quatre critères de choix d'une représentation d'état, qu'elle recommande de réemployer tels quels, et les applique : le codage naïf par autocollant est redondant de dix-sept ordres de grandeur, et la représentation retenue, un tenseur de vingt sur vingt-quatre en codage one-hot, l'est encore d'un facteur cent millions pour une raison précise, à savoir qu'un coin ne peut pas tourner seul. Elle explique pourquoi les six centres ne sont pas suivis, ce qui rend l'état invariant par rotation d'ensemble, et pourquoi deux représentations coexistent, un tenseur de 1 920 octets pour entrer dans le réseau et une permutation de 160 octets pour stocker les millions d'états de la recherche. Puis vient l'idée la plus astucieuse de la semaine, et c'est la seule double lecture complète qu'elle contienne : face à une récompense inaccessible au hasard, l'itération autodidacte ne cherche pas le but, elle en part. On brouille le cube résolu par un nombre tiré de rotations et on entraîne sur ce qui en sort, de sorte que chaque état d'entraînement a une distance au but connue et que le problème de la récompense parcimonieuse ne se présente jamais. La semaine énonce les deux conditions d'applicabilité de ce procédé, connaître l'état but et disposer d'une dynamique inversible, et recommande de se poser cette question avant de construire une prime de nouveauté. Les deux cibles d'entraînement sont écrites, avec le code qui les calcule et la table de correspondance. La recherche qui exploite ce réseau est celle de la semaine 12, citée et non redérivée, avec deux différences nommées : la lettre qui désignait une utilité complète désigne ici une prime seule, et la remontée prend un maximum sur le sous-arbre au lieu d'une moyenne, ce qui est défendable sur un casse-tête déterministe à un joueur et pas ailleurs.

La semaine fait ensuite le compte de ce qui a transféré. Les quatre applications réemploient quatre méthodes du cours sans en changer la substance, ce qui est le meilleur argument en faveur du programme suivi. Trois choses n'ont pas transféré : les enveloppes, qu'il faut réécrire chaque fois, la généralisation, un agent entraîné sur un jeu textuel ne résolvant aucun autre jeu et une variante à composant préentraîné apprenant plus vite tout en validant plus mal, et les chiffres publiés. Un tableau rassemble le coût en calcul de tout ce que le cours a décrit, d'une heure de processeur graphique pour le plus simple des jeux d'arcade à six jours pour une seule reproduction du solveur de cube, et vingt centimes pour l'évaluation sans entraînement de la section suivante.

Viennent alors les deux derniers résultats négatifs du cours, présentés comme un patron puisque les semaines 10, 11, 12 et 13 en avaient chacune montré un. Le cinquième est une reproduction qui a échoué, rapportée en entier : hyperparamètres absents de la publication, entraînement qui finit par diverger avec une perte de valeur passant de zéro à plus de quatre cents en quelques heures, et un diagnostic que la notation posée plus tôt rend lisible, à savoir que la valeur prédite est ajoutée à l'indicateur de but même sur l'état résolu, ce qui retire à la fonction de valeur son unique ancre. Le correctif tient en une ligne, forcer la cible à zéro sur le but, et il fait passer un cube réduit de cinquante-cinq à cent pour cent de résolution tout en divisant par trois à cinq le nombre de recherches nécessaires ; sur le cube complet il porte la portée de la profondeur neuf à la profondeur treize, là où le protocole publié évaluait sur des cubes brouillés par mille coups. La semaine délimite ce que cet échec démontre, à savoir qu'une méthode publiée sans ses hyperparamètres n'est pas reproductible, et ce qu'il ne démontre pas, à savoir quoi que ce soit sur la méthode. Le sixième est d'une autre nature : la même expérience a été rapportée deux fois à onze pages d'intervalle, et les deux rapports se contredisent sur cinq points, dont une journée contre douze heures et un problème déclaré résolu contre une récompense moyenne de 0,5 sur une échelle qui monte à un. La semaine ne retient aucun des deux chiffres et explique que ce n'est ni une fraude ni même une négligence, mais ce qui arrive quand une expérience est décrite deux fois sans qu'un nombre unique ait été enregistré. Le remède est celui du jalon 2 : le nombre vit dans le journal, pas dans la prose.

La semaine réunit ensuite trois cas où le nom d'une méthode ne dit pas ce que fait le code, et les corrige en son propre nom. Un agent de clic décrit comme asynchrone est un acteur-critique à avantage avec environnements vectorisés, c'est-à-dire la méthode de la semaine 8 : il y a un seul réseau, une seule mise à jour synchrone par lot, et le mot asynchrone qualifie les huit navigateurs, pas l'algorithme. Une règle de descente présentée comme une borne de confiance supérieure classique est la variante de la semaine 12, et deux signatures suffisent à le voir, l'absence de logarithme et la présence d'une probabilité a priori. Et le nombre de Dieu, qui vaut bien vingt, le vaut dans la métrique des demi-tours, alors que l'implémentation compte en quarts de tour, métrique dans laquelle la borne vaut vingt-six ; le cours énonce ce vingt-six en son propre nom. Il donne en outre une seconde raison, indépendante des métriques et plus instructive, qui est qu'une profondeur de brouillage n'est pas une longueur de solution optimale, puisque des rotations tirées au hasard s'annulent, de sorte qu'une saturation décrit la portée du solveur et non la borne. L'énoncé général est qu'une borne théorique ne contraint une mesure que si les deux sont dans les mêmes unités, et ici elles ne sont ni dans la même métrique ni dans la même quantité. La phrase à emporter est que le nom d'une méthode dans un texte n'est pas une preuve de ce que fait le code.

Vient alors la section qui fait le pont avec la semaine 14 : la même tâche textuelle confiée à un grand modèle de langue qui n'a reçu aucun entraînement et à qui l'on ne fournit même pas la liste des commandes admissibles. Il résout la première partie en cinq pas, qui est l'optimum, et neuf parties sur vingt à l'échelle, pour quatre cent cinquante mille jetons et vingt centimes, face à un agent entraîné quatorze heures dont la récompense de validation est nulle. La semaine refuse d'en faire un tour d'honneur et fournit la lecture honnête que rien d'autre ne fournit : neuf sur vingt est un peu moins qu'une pièce lancée en l'air sur une quête de cinq coups ; l'absence d'entraînement sur cette tâche n'est pas une absence d'entraînement, le corpus contenant certainement de la fiction interactive ; rien ici ne compare du raisonnement à de l'apprentissage, les deux systèmes n'ayant pas reçu la même chose ; et la comparaison de coûts n'est pas à grandeurs égales, un agent entraîné tournant ensuite indéfiniment sans frais. Ce que le résultat montre suffit pourtant, et c'est la question d'ouverture remise à l'endroit : la première question devant un problème n'est pas quelle méthode, mais de quelle nature sont l'observation et l'action, et donc lesquels de vos problèmes sont des problèmes de langue.

La carte de décision range enfin les quatorze semaines par caractéristique de problème et non par ordre chronologique, sous forme de figure et de tableau interrogeable ligne par ligne, et la semaine montre la procédure complète sur un problème de maintenance industrielle inventé pour l'occasion, qui aboutit à trois semaines retenues et onze écartées, la décision la plus importante n'étant pas le choix de l'algorithme mais le fait de savoir si l'on dispose d'un simulateur ou seulement de journaux. La semaine se termine sur six limites établies par ses propres mesures, dont aucune ne se corrige par un meilleur algorithme, sur quatre choses que le cours n'a pas faites, et sur le protocole exigé depuis le jalon 2, plusieurs graines, des intervalles et un protocole écrit avant l'exécution, avec l'outil statistique du domaine simplement nommé. Le laboratoire dit en un tableau laquelle des quatre applications s'exécute et pourquoi les trois autres ne s'exécutent pas, et propose un volet noté sans aucun entraînement, un volet de démonstration sur des journaux fournis, un volet facultatif hors carnet et un exercice d'écriture. Les livrables finaux ferment le cours : un rapport de huit à dix pages, une présentation de dix minutes, un dépôt complet, et un critère unique que la semaine vient de démontrer deux fois, à savoir que quelqu'un d'autre puisse l'exécuter.

---
## Mots-clés de la semaine

caractérisation d'un problème · observation, action, récompense · récompense conçue et non observée · protocole avant exécution · partage chronologique · fiction interactive · commandes admissibles · récompense intermédiaire · espace d'actions par pas · action produite et non choisie · adaptateur d'interface · PDM partiellement observable · couple observation-commande · navigation web · automatisation du navigateur · test de site web · extraction de données web · arbre DOM · jeu de référence · grille de clics · sans interface · décroissance de la récompense avec le temps d'horloge · dépendance à la machine · démonstrations humaines · exemples négatifs absents · optimisation combinatoire · optimisation discrète · quatre critères de représentation · codage one-hot · invariant par rotation d'ensemble · cube élémentaire · deux représentations d'un état · itération autodidacte · profondeur de brouillage · données engendrées à reculons · dynamique inversible · cible de valeur ancrée · remontée par maximum · parcours en largeur · environnements vectorisés · mise à jour synchrone · probabilité a priori dans la prime d'exploration · perte virtuelle · nombre de Dieu · métrique des demi-tours · métrique des quarts de tour · unités d'une comparaison · échec de reproduction · résultats incompatibles · le nombre vit dans le journal · un nom n'est pas une preuve · résultat négatif correctement établi · grand modèle de langue sans entraînement · problème de langue · carte de décision · trois semaines pertinentes, onze écartées · reproductibilité · quelqu'un d'autre peut l'exécuter · livrables finaux

---
## Après la semaine 15

Il n'y a pas de semaine 16. Le module 5 se termine avec cette semaine, et SCI1070 avec lui.

Ce qui reste n'est donc pas un contenu à lire, c'est un travail à rendre : le rapport de huit à dix pages, la présentation de dix minutes et le dépôt complet, dont le brief est écrit à l'intérieur de cette semaine avec sa liste de vérification et son barème. Ils portent sur l'ensemble de votre trajectoire, des jalons 1 à 4, et ils sont évalués sur un critère que cette semaine démontre deux fois plutôt que de l'affirmer : **quelqu'un d'autre peut l'exécuter**.

Et pour la suite, qui ne sera plus organisée en semaines, trois choses de ce cours survivront à ses méthodes. Les trois questions de la section 15.1, qui s'appliquent à n'importe quel problème et ne se démodent pas. La carte de décision de la section 15.10, qui vous dit quoi ouvrir et surtout quoi laisser fermé. Et la discipline de mesure, qui est la seule partie de votre travail dont la valeur ne dépend pas de la méthode que vous aurez choisie.

{{% comment %}}
PAGINATION. Les ancres LAPAN sont en INDICES PDF : imprimé = PDF moins 31 (D35), comme toutes les
semaines LAPAN depuis la semaine 1. L'offset a été reconfirmé deux fois pendant la passe de
lecture, sur les quatre chapitres : l'indice 654 porte le folio 623, l'indice 445 porte le folio
414. Une affirmation d'un offset différent pour le chapitre textuel avait été vérifiée sur image
et corrigée : l'indice 390 porte le folio 359.

PASSE DE LECTURE. Quatre résumés de chapitre et onze chunks, soit les quinze items du manifeste,
dans l'ordre, et rien d'autre : 27 367 jetons mesurés, bien sous l'objectif de 35 000 de D41. Les
chunks de ces quatre chapitres totalisent 57 932 jetons, donc une lecture chunk par chunk était
exclue d'avance, ce que D41 anticipait nommément pour cette semaine. La marge est allée sur NEUF
PAGES RASTERISÉES (lapan/0393, 0394, 0437, 0441, 0445, 0654, 0656, 0657, 0667), aucune n'existant
avant cette passe, et sur quatre greps ciblés dans des chunks exclus (13-07, 13-08, 13-09, 21-07,
plus 14-04), environ 1 200 jetons de lignes appariées, à seule fin de vérifier des erreurs
d'auteur que les résumés affirment. AUCUN chunk exclu n'a été lu en entier et AUCUNE
implémentation n'a été lue. Détail complet dans index/notes/week-15.md.

QUATRE CHAPITRES, et ce que chacun porte.

PREMIER CHAPITRE (LAPAN ch. 10, le courtage) : lu AU NIVEAU DU RÉSUMÉ SEULEMENT, puisque la
semaine 7 l'a enseigné. Porte la section 15.2 et la colonne « marché » de §15.1.
- p.306 : les N dernières barres avec N = 10 par défaut, l'indicateur de position détenue, le
  profit relatif courant, la réécriture du haut, du bas et de la clôture en POURCENTAGES DE
  L'OUVERTURE, et les trois actions (§15.1, §15.2).
- p.306, p.314 : les DEUX schémas de récompense, le mouvement par barre pendant la détention et le
  mouvement entier à la clôture, en points de pourcentage, commission de 0,1 % à l'aller et au
  retour (§15.1, §15.2).
- p.322-323 : l'agent au-dessus de -0,2 % pendant environ quatre heures de marché, et le constat
  que le signal est plus petit que le coût d'un aller-retour (§15.1, §15.2).
- La RÈGLE DE PARTAGE CHRONOLOGIQUE de §15.2 et ses trois conséquences sont CELLES DU COURS, écrites
  en semaine 7 et citées ici depuis la page de la semaine 7 (raw-content/week-07.md §7.6). Aucune
  source extérieure n'est invoquée pour elles, conformément à D45.

DEUXIÈME CHAPITRE (LAPAN ch. 13, la fiction interactive) : porte la section 15.3, la moitié de
§15.6 et toute la section 15.9.
- p.390-391 : l'outil, juin 2018, interface de style Gym, générateur de quêtes paramétrable, accès
  à l'état interne ; les paramètres de génération et la longueur de quête 5 ; et la prise en charge
  LINUX ET MACOS SEULEMENT, plus la dépendance à un moteur de fiction interactive (§15.3, labo).
- p.393 : l'observation textuelle jusqu'à 200 jetons sur 1 250 mots ; l'inventaire non montré, donc
  PDM partiellement observable ; et L'INTERFACE QUI N'EST PAS CELLE DE GYMNASIUM, à savoir la
  fonction de création propre au paquet, l'absence de spécification d'espaces, les QUATRE valeurs
  de retour sans indicateur de troncature, et l'impossibilité d'appliquer les enveloppes du cours
  (§15.3, §15.6, labo volet A).
- p.393 (image) : la probabilité 1/1250^40 ~ 1/10^123, TRANSCRITE DE L'IMAGE DE PAGE
  (index/pages/lapan/0393.png) et NON du chunk, où elle sort en « 12501⁴⁰ ≈ 101¹²³ » (§15.3,
  équation 15-E5).
- p.394 (image) : la réduction de l'espace d'actions à « une douzaine » par la liste des commandes
  admissibles. LA DISTINCTION ENTRE L'ESPACE DES SOLUTIONS COMPLÈTES (1250^40) ET L'ESPACE
  D'ACTIONS PAR PAS (1250^8 ~ 6.10^24) EST UNE PRÉCISION DU COURS, ajoutée en son nom parce que la
  réduction qui rend un réseau Q applicable porte sur le second (§15.3).
- p.394-395 : les sept champs d'état interne plus le réglage de récompense intermédiaire, et le
  constat que sans ces deux béquilles rien n'apprend (§15.3, labo volet A).
- p.401 : la conséquence d'architecture, un réseau qui prend un COUPLE observation-commande et
  renvoie UNE valeur, parce que la liste des commandes change d'un état à l'autre (§15.3, §15.6).
- p.412-420 (résumé) : les chiffres de l'agent entraîné, 3 min et 120 épisodes pour UN jeu avec une
  récompense de validation NULLE, deux heures sur 20 jeux et validation plafonnée à 2 sur 6, la
  meilleure variante à 2 h 30 puis DÉGRADÉE, et l'encodeur de phrases préentraîné qui apprend plus
  vite et valide moins bien (§15.6, §15.9).
- p.414 : 14 heures et 8 000 épisodes, retenu comme LE chiffre de l'entraînement. Une mention de
  13 heures p.416 est une référence arrière parenthétique ; le cours emploie 14 (§15.6, tableau de
  coût).
- p.420 : les paquets ÉPINGLÉS dont la compatibilité se casse d'une version à l'autre, et la CLÉ
  D'INTERFACE PAYANTE de la partie « modèle de langue » (labo).
- p.421-424 : le dispositif du modèle de langue, l'énoncé en trois phrases, l'historique de
  conversation comme SEULE mémoire, l'objectif montré une seule fois, et les DEUX champs demandés,
  description et objectif, SANS les commandes admissibles (§15.9).
- p.422-423 : la graine 1 résolue en CINQ pas, avec les cinq commandes (§15.9).
- p.423 : la tâche est PLUS DIFFICILE que celle de l'agent entraîné, puisque le modèle PRODUIT ses
  commandes au lieu de les choisir dans une liste (§15.9).
- p.425-426 : 20 jeux, plafond de 20 pas, NEUF résolus sur vingt ; les quatre catégories d'échec
  dont deux parties perdues par la production de la commande « exit » ; 450 000 jetons, 0,20 $
  (§15.9, tableau de coût).
LA LECTURE HONNÊTE DE §15.9 EST ÉCRITE PAR LE COURS, et la source ne la fournit pas : les quatre
réserves (9/20 est sous une pièce lancée en l'air sur une quête de cinq coups ; « sans entraînement
sur cette tâche » n'est pas « sans entraînement », le corpus contenant certainement de la fiction
interactive ; rien ne compare raisonnement et apprentissage, les deux systèmes n'ayant pas reçu les
mêmes champs ; et un coût unitaire ne se compare pas à un coût d'investissement) sont des énoncés
du cours, de même que la conclusion « lesquels de mes problèmes sont des problèmes de langue ».
TROIS ERREURS D'AUTEUR DE CE CHAPITRE SONT ÉCARTÉES SANS ÊTRE DISCUTÉES, parce que la page n'a
besoin d'aucune d'elles : le drapeau « -s medium » (p.413), qui est le mauvais drapeau ET le mauvais
type, la forme correcte étant « --params medium » ; le compte « 21 jeux » (p.390) contre « 20 jeux
plus un jeu de validation » (p.411), réconciliable en 20 jeux d'entraînement plus un de validation ;
et deux chemins différents pour un même script de génération (p.390 contre p.411), non
réconciliables. LA PAGE N'IMPRIME NI LIGNE DE COMMANDE NI CHEMIN DE FICHIER, ce qui rend les trois
sans objet.

TROISIÈME CHAPITRE (LAPAN ch. 14, la navigation web) : porte la section 15.4, la moitié de §15.6,
le premier cas de §15.8 et le sixième résultat négatif de §15.7.
- p.429 : la définition de la navigation web, les deux industries préexistantes (test de site web,
  extraction de données web), et l'aveu que la récompense N'EST PAS CLAIRE et doit être propre à la
  tâche (§15.4).
- p.430 : les trois applications, dont l'exploration de vulnérabilités de sécurité ; et LE
  PARAGRAPHE LE PLUS TRANSFÉRABLE DU CHAPITRE, à savoir qu'un système à taille réelle demanderait
  des mois de travail d'une équipe et que la plupart des difficultés ne concerneraient pas
  l'apprentissage par renforcement, d'où les jeux de référence et leurs deux conditions
  contradictoires (§15.4).
- p.431-432 : MiniWoB, décembre 2016, 80 tâches, pixels plus énoncé, pilotage par bureau à distance,
  ABANDONNÉ presque aussitôt ; puis MiniWoB++ et sa maintenance actuelle (§15.4).
- p.431 : l'étendue des tâches, de la fermeture d'une boîte de dialogue au sélecteur de dates avec
  date tirée à chaque épisode, et les tâches demandant de la reconnaissance de caractères (§15.4).
- p.436 : LA DÉCROISSANCE DE LA RÉCOMPENSE AVEC LE TEMPS D'HORLOGE : 0,7936 en 2,0666 s avec le
  navigateur dessiné, 0,9918 en 0,09 s sans interface, pour une récompense brute de 1 dans les deux
  cas (§15.1, §15.4, §15.11, labo volet C). C'est le point que les notes signalent comme NON
  ANTICIPÉ par le manifeste, et la page lui consacre un passage et un encadré.
- p.437 (image, fig. 14.3) : la grille d'actions. 50 px de bannière d'énoncé SANS ÉLÉMENT ACTIF,
  160 px de hauteur cliquable, cellules de 10 px, donc 16 x 16 = 256. UNE SEULE IMAGE TRANCHE à la
  fois le 256 et l'arithmétique de p.452 (§15.4, FIG 15-03).
- p.433, p.435 : l'observation en dictionnaire, énoncé textuel, capture couleur et arbre DOM avec
  attributs, soit trois angles d'attaque (§15.1, §15.4).
- p.441 (image) : LE CODE DU MODÈLE, lu sur l'image de page. UNE classe de réseau, deux couches
  convolutives, UNE couche linéaire de politique, UNE couche linéaire de valeur ; et le script
  d'entraînement « exactement le même que celui du chapitre 12 », avec AsyncVectorEnv et huit
  environnements parallèles. Plus le résultat de 0,9 en environ 8 minutes sur la tâche élémentaire
  (§15.6, §15.8, tableau de coût).
- p.445 (image, fig. 14.7) : les trois panneaux de la tâche de comptage de côtés (§15.4, FIG 15-04).
- p.445 (image) et p.456 : LES DEUX RAPPORTS INCOMPATIBLES de la même expérience, transcrits tous
  les deux. Le cours NE RETIENT NI L'UN NI L'AUTRE comme LE chiffre et nomme les cinq désaccords
  (§15.7).
- p.452 : les 256 actions valant 128 fois CartPole, et l'agent SANS MÉMOIRE dont une tâche en deux
  étapes brise la propriété de Markov. La formule « 256 actions correspondant à des grilles de
  10 x 10 » de la même page est arithmétiquement impossible et la figure la réfute : 10 est la
  TAILLE D'UNE CELLULE EN PIXELS. §15.4 énonce 16 x 16 et le calcul, EN SON PROPRE NOM, sans
  mentionner l'autre forme (§15.4).
- p.452, p.454 : les démonstrations comme données HORS POLITIQUE face à une méthode SUR POLITIQUE,
  et le pont par l'entropie croisée sur la tête de politique, c'est-à-dire l'objectif de la
  semaine 4 réemployé. La phrase « nous ne remplaçons pas l'AR par de l'apprentissage supervisé »
  est RESTITUÉE DANS LA VOIX DU COURS, sans guillemets ni attribution (D45) (§15.4, 15-E7).
- p.455 : DEMO_PROB = 0,5 par lot, l'entropie croisée vers l'action démontrée, et la tête de valeur
  non touchée (§15.4).
- p.453 : l'enregistreur officiel qui capte l'arbre DOM ET PAS LES PIXELS, donc des démonstrations
  inutilisables pour un agent à pixels, et un second enregistreur écrit pour l'occasion (§15.4).
- p.456-457 : le tic-tac-toe, deux heures d'entraînement avec démonstrations, récompense moyenne de
  0,05 (§15.4, tableau de coût).
- p.458 : les travaux qui demandent à un modèle de langue de PRODUIRE le script d'automatisation,
  mentionnés en UNE phrase en fin de §15.4 et rappelés en fin de §15.9, sans être poursuivis.

QUATRIÈME CHAPITRE (LAPAN ch. 21, le cube) : porte la section 15.5, le cinquième résultat négatif
de §15.7 et les deuxième et troisième cas de §15.8.
- p.645-646 : le cube comme optimisation combinatoire, en compagnie du voyageur de commerce, du
  repliement de protéines et de l'allocation de ressources ; 4,33.10^19 états atteignables et
  5,19.10^20 si l'on démonte, les états supplémentaires étant insolubles sans démontage (§15.5).
- p.646 : les douze rotations et LA PHRASE QUI DÉCIDE DE LA MÉTRIQUE, à savoir que les demi-tours
  ne sont pas des transformations distinctes et coûtent deux actions. La même phrase contient
  « 6 arêtes » là où un cube a 6 FACES et 12 arêtes : §15.5 écrit « six faces, deux sens, douze
  rotations » EN SON PROPRE NOM, sans signaler l'autre forme (§15.5, §15.8).
- p.647 : les deux familles préexistantes, théorie des groupes et recherche heuristique, toutes
  deux exigeant beaucoup de connaissance du domaine ; et le fait que la troisième approche n'a
  besoin QUE DU CUBE LUI-MÊME. Et l'énoncé du nombre de Dieu à 20 SANS SA MÉTRIQUE, qui est toute
  l'erreur (§15.5, §15.8).
- p.648 : la convention majuscule horaire, minuscule antihoraire (§15.1, §15.5).
- p.649-651 : LES QUATRE CRITÈRES DE REPRÉSENTATION (éviter la redondance, efficacité en mémoire,
  performance des transformations, compatibilité avec un réseau) ; le codage naïf 6^48 ~ 2,25.10^37 ;
  le tenseur 20 x 24 donnant 24^20 ~ 4,02.10^27, encore 10^8 de trop, parce qu'on ne peut pas faire
  tourner un seul coin en place ; les six centres non suivis et l'invariance par rotation
  d'ensemble ; 8 coins x 3 orientations = 24 et 12 bords x 2 = 24 ; et les vingt autocollants
  suivis (§15.5, 15-E6).
- p.651 : LES DEUX REPRÉSENTATIONS, tenseur de 1 920 octets pour le réseau et permutation de
  160 octets pour le stockage (§15.1, §15.5).
- p.653-654 (image) : l'architecture, corps dense 4 096 puis 2 048 avec ELU, tête de politique
  2048-512-512-12, tête de valeur 2048-512-512-1, et le drapeau qui permet d'évaluer la tête de
  valeur seule (§15.5).
- p.654 (image) : L'ITÉRATION AUTODIDACTE, et les deux cibles 15-E1 et 15-E2, TRANSCRITES DE
  L'IMAGE DE PAGE. Plus la récompense +1 sur le but et -1 ailleurs (§15.1, §15.5).
- p.656 (image) : l'échec du suivi glouton de la politique, le réseau donnant des directions et non
  des actions optimales, et les 0,0000005 % de l'espace d'états vus après un mois (§15.5). C'est
  AUSSI la page du NOMMAGE « Upper Confidence Bound 1 », une page AVANT la formule : correction de
  passe de lecture, le manifeste et le résumé ch21 disaient « même page », LES DEUX PAGES SONT
  CITÉES (§15.8).
- p.657 (image) : la règle de descente 15-E3, TRANSCRITE DE L'IMAGE DE PAGE et IDENTIQUE DE FORME à
  12-E1 de la semaine 12, avec W = MAXIMUM sur le sous-arbre au lieu de la moyenne courante. Plus
  les deux extractions de solution, naïve et par parcours en largeur. Et l'énoncé selon lequel « une
  perte supplémentaire pourrait être retranchée de A_t », impossible puisque A_t est un indice
  d'action : §15.8 écrit que la perte virtuelle se retranche de W(s,a) (§15.5, §15.8).
- p.657-658 : les chiffres publiés, 44 h sur trois processeurs graphiques, 8 milliards d'états,
  environ 50 000 cubes/s ; 640 cubes brouillés par 1 000 coups, limite d'une heure, les deux
  solveurs résolvant tout ; médiane d'une seconde contre environ dix minutes ; et 55 % des cas où la
  LONGUEUR DE SOLUTION égale ou améliore celle du solveur classique (§15.5).
- p.666 : la tentative de reproduction, l'ABSENCE DANS LA PUBLICATION des hyperparamètres, de la
  profondeur de brouillage d'entraînement et de la convergence obtenue, et la recherche
  d'hyperparamètres qui s'ensuit (§15.7).
- p.666-667 (image) : les résultats TRÈS DIFFÉRENTS, la convergence TRÈS INSTABLE, la divergence
  avec perte de valeur croissant exponentiellement, et la figure 21.6 (perte de politique de 0,08 à
  0,04 en 1 h 30 puis au-dessus de 0,10 ; perte de valeur à zéro pendant deux heures puis
  verticalement au-delà de 400) (§15.7, FIG 15-05).
- p.667 (image) : LE DIAGNOSTIC, à savoir que la valeur prédite est TOUJOURS ajoutée à la récompense
  réelle, MÊME SUR L'ÉTAT BUT, de sorte que les valeurs renvoyées peuvent valoir n'importe quoi ; et
  le correctif d'une ligne, 15-E4, dont les accolades sont INTACTES SUR L'IMAGE et DISLOQUÉES dans
  le chunk. La formulation « la fonction de valeur n'a pas d'ancre » est celle du cours, de même que
  le parallèle avec l'invariance par décalage additif de la semaine 14 (§15.7).
- p.669 : ce que le correctif achète sur le cube 2 x 2, lots de 10 000, profondeur de brouillage
  200, 20 cubes de test à chacune des profondeurs 1 à 50 soit 1 000 cubes, 30 000 pas de recherche
  par cube : perte finale 0,032572 contre 0,012226, 55 % contre 100 % de cubes résolus, 3 à 5 fois
  moins de recherches (§15.7).
- p.670 : ce qu'il n'achète pas sur le cube 3 x 3 : environ 20 h, portée jusqu'à la profondeur
  « 12 … 15 » dans une phrase et 13 dans une autre, la méthode d'origine à la profondeur 9 et la
  version modifiée à 13. LE COURS EMPLOIE 13, parce que c'est le chiffre attaché à la méthode
  modifiée et celui que p.671 répète. Plus la recherche plafonnée à 100 000 pas et CINQ brouillages
  par profondeur seulement (§15.7).
- p.668-669 : 50 000 cubes/s sur trois Titan Xp contre 15 000 sur une GTX 1080 Ti, donc PRESQUE SIX
  JOURS sur un seul processeur graphique pour refaire l'entraînement, ce qui est la raison d'être de
  l'environnement réduit au cube 2 x 2 (§15.7, labo, tableau de coût).
- p.671 : la prédiction de saturation « après une profondeur de 20, cela devrait saturer », et la
  répétition du chiffre 13 (§15.8).

LE 26 EST UNE AFFIRMATION DU COURS. La source ne le donne nulle part. §15.8 énonce que le nombre de
Dieu vaut 20 dans la MÉTRIQUE DES DEMI-TOURS (résultat de 2010) et 26 dans la MÉTRIQUE DES QUARTS DE
TOUR (résultat de 2014), et que l'implémentation compte en quarts de tour puisqu'elle facture un
demi-tour deux actions. Le 26 n'est attribué à personne et n'est présenté comme la correction de
personne. §15.8 donne en outre la SECONDE RAISON, INDÉPENDANTE, qui enseigne davantage : une
PROFONDEUR DE BROUILLAGE n'est pas une LONGUEUR DE SOLUTION OPTIMALE, puisque des rotations tirées
au hasard s'annulent, de sorte qu'une saturation décrit la PORTÉE DU SOLVEUR et non la borne.
L'énoncé général, « une borne théorique ne contraint une mesure que si les deux sont dans les mêmes
unités », est du cours.

LES DEUX 55 % SONT SÉPARÉS PAR CONSTRUCTION. Celui de p.658 (proportion de cas où la longueur de
solution égale ou améliore celle du solveur classique, cube 3 x 3) est en fin de §15.5 ; celui de
p.669 (taux de résolution des 1 000 cubes de test du 2 x 2 par la méthode d'origine) est dans le
tableau de §15.7, et un encadré de §15.7 dit explicitement que les deux nombres sont égaux et sans
rapport. Ils n'apparaissent jamais dans la même phrase.

DEUX ERREURS SIGNALÉES PAR LES RÉSUMÉS ET NON VÉRIFIÉES INDÉPENDAMMENT (chunk 21-08, exclu) : un nom
de fonction au pluriel dans le texte contre le singulier dans le code, et un état résolu enregistré
à la profondeur 1. Elles sont marquées « source résumé » dans les notes et LA SEMAINE N'EN A BESOIN
D'AUCUNE : rien de la page ne s'appuie sur elles.

TROIS CORRECTIONS DE MANIFESTE FAITES PENDANT LA PASSE DE LECTURE, et la page en dépend.
(1) La page du nommage « Upper Confidence Bound 1 » est 656 et non 657 ; les deux pages sont citées.
(2) Le manifeste affirmait que les chapitres ne fournissent « presque rien » en figures : vrai de
l'EXTRACTION MARKDOWN, faux du PDF. Trois figures ont été vues intactes sur image et sont des
figures DU LIVRE et non de l'article : fig. 14.3 p.437, fig. 14.7 p.445, fig. 21.6 p.667. Les trois
sont extraites, et c'est ce qui fait passer la semaine de deux figures produites à deux produites
plus trois extraites. Les figures 21.1 à 21.4 restent inutilisables : elles viennent de l'article.
(3) Le résumé ch14 affirmait que « hors-politique » n'existe pas au glossaire : la ligne 40 porte
« sur politique / hors politique » depuis la semaine 3. Aucun terme à ouvrir de ce côté.

CE QUE LA SEMAINE N'ENSEIGNE PAS, ET C'EST L'INSTRUCTION LA PLUS FORTE DU MANIFESTE. Aucune
cinquième méthode. L'itération autodidacte est la SEULE double lecture complète de la semaine
(15-E1, 15-E2, 15-E4, avec code et table de correspondance), et elle y est parce que l'échec de
reproduction de §15.7 NE PEUT PAS être enseigné sans la cible qui le cause. La règle de descente
(15-E3) est CITÉE de la semaine 12 et non redérivée ; l'objectif de démonstration (15-E7) est CITÉ
des semaines 4 et 8 et ne reçoit aucune équation, le chapitre n'en donnant d'ailleurs aucune ; le
réseau à deux têtes est cité de la semaine 12 ; le réseau Q profond de la semaine 5 ; l'acteur-
critique de la semaine 8. Les implémentations des quatre chapitres n'ont pas été lues (DO NOT read
du manifeste) et la semaine n'en construit aucune.

NOTATION. notation.md §3 quinquies est ajouté par cette semaine et contient QUATRE lignes : la
transition renommée T(s,a) parce que A_t est l'action et A^pi l'avantage ; la valeur de l'état
atteint écrite v(T(s,a)) et non v_s(a), qui a la forme d'une valeur d'action sans en être une ;
U(s,a) qui est ici la PRIME SEULE alors que 12-E1 en fait l'utilité complète ; et W(s,a) qui est ici
un MAXIMUM sur le sous-arbre alors que la semaine 12 en fait une somme divisée par le compte. Les
trois premières collisions tombent à l'intérieur des équations de §15.5 et §15.7, et les quatre sont
annoncées dans l'introduction AVANT la première équation. Aucune autre section de notation.md n'a
été touchée.

GLOSSAIRE. Vingt-trois lignes ajoutées en semaine 15, dont DEUX qui sont toute l'erreur de §15.8 et
doivent coexister : « métrique des demi-tours » et « métrique des quarts de tour ». Et une ligne
tenue à l'écart de deux voisines : « démonstrations humaines » n'est ni « préférences humaines »
(semaine 14), puisqu'une démonstration ne contient aucun exemple négatif, ni « clonage de
comportement » (semaine 13), qui est une méthode et non une donnée. DEUX des dix-neuf lignes que les
notes demandaient EXISTAIENT DÉJÀ et n'ont pas été dupliquées : « codage one-hot » est la ligne 137,
semaine 3, et les notes proposaient « codage un parmi n », forme ÉCARTÉE au profit de la ligne
existante ; « environnements vectorisés » est la ligne 224, semaine 7. Trois lignes nouvelles que les
notes ne demandaient pas : « cube élémentaire », parce que « arête » est pris par la semaine 12 au
sens d'arête d'arbre et qu'un cube a des arêtes d'un autre genre ; « carte de décision », qui est
l'objet de §15.10 ; et « plongement de phrase », employé une fois en §15.6.

FIGURES. Cinq, dont DEUX PRODUITES par le cours et TROIS EXTRAITES du livre. Les deux dessins
EXISTENT DÉJÀ sur disque et sont produits par scripts/make_figures_week15.py ; une seule
étiquette a été corrigée après le premier rendu, « donc POMDP » devenant « donc partiellement
observable », parce que la ligne 191 du glossaire donne POMDP comme forme à éviter depuis la
semaine 5. Restent les TROIS EXTRACTIONS.
- 15-01, PRODUITE : les quatre problèmes en trois lignes. C'EST L'IMAGE ORGANISATRICE DE LA SEMAINE,
  construite cellule par cellule sur le tableau de §15.1, dont chaque case est ancrée. Les livrables
  finaux demandent à l'étudiant d'en produire une CINQUIÈME COLONNE pour son propre problème, et la
  figure doit donc laisser la place visible pour celle-ci.
- 15-02, PRODUITE : la carte de décision. Quatorze semaines contre les caractéristiques de problème
  qui sélectionnent une méthode. CE N'EST PAS UNE FRISE : aucune flèche chronologique, aucune
  numérotation ordonnée comme axe. §15.10 en donne le contenu complet en TABLEAU, de sorte que la
  page tient sans la figure.
- 15-03, EXTRAITE : fig. 14.3 p.437, la grille d'actions. Une seule image tranche le 256 et
  l'arithmétique fautive de p.452.
- 15-04, EXTRAITE : fig. 14.7 p.445, les trois panneaux de la tâche de comptage de côtés. C'est la
  tâche dont §15.7 rapporte les deux résultats incompatibles, ce qui est une raison de plus de la
  montrer.
- 15-05, EXTRAITE : fig. 21.6 p.667, les deux pertes de la méthode d'origine. C'EST LE PORTRAIT
  D'UNE FONCTION DE VALEUR SANS ANCRE, et la figure du cinquième résultat négatif.
UNE SIXIÈME FIGURE A ÉTÉ PROPOSÉE PAR LES NOTES ET N'EST PAS DEMANDÉE : la comparaison
d'efficacité d'échantillonnage et de temps d'horloge accumulée au fil du cours. Le manifeste la
donnait comme possiblement meilleure en tableau, et c'est la décision prise : §15.6 porte un TABLEAU
DE COÛT de quinze lignes, chiffré, dont chaque ligne est ancrée soit sur une page du cours soit sur
une page de cette semaine. Un dessin aurait perdu les chiffres, qui sont tout l'intérêt. Les
identifiants ne sont jamais renumérotés (D22) : si un auteur ultérieur veut ce dessin, il prend
15-06. AUCUNE figure du chapitre 10 n'est candidate, la semaine 7 ayant pris ce qu'il lui fallait.
AUCUNE figure ne rend de crédit (D39) : les trois extractions sont LAPAN, dont la licence ne fait
pas de l'attribution une condition de réutilisation, et les deux dessins portent « Création du
cours ». Inventaire et spécifications de dessin dans extraction/week-15.md.

ÉQUATIONS. Sept identifiées dans les notes, 15-E1 à 15-E7, et AUCUN PLACEHOLDER.
- 15-E1 et 15-E2, les deux cibles de l'itération autodidacte, ÉCRITES DIRECTEMENT en KaTeX,
  TRANSCRITES DE index/pages/lapan/0654.png et non du chunk, avec les deux renommages de notation.
- 15-E3, la règle de descente, ÉCRITE DIRECTEMENT mais PRÉSENTÉE COMME CITÉE de la semaine 12 : elle
  est affichée parce que la comparaison terme à terme AVEC la borne de confiance supérieure
  classique est l'enseignement de §15.8, et non pour être dérivée. Transcrite de 0657.png.
- 15-E4, la cible ancrée, ÉCRITE DIRECTEMENT, transcrite de 0667.png où les accolades sont intactes.
  NE JAMAIS la reprendre du chunk, qui les disloque.
- 15-E5, la probabilité 1/1250^40, ÉCRITE DIRECTEMENT en une ligne, transcrite de 0393.png. Le chunk
  l'aplatit en « 12501⁴⁰ ≈ 101¹²³ » : INUTILISABLE, et à ne pas réparer au jugé.
- 15-E6, les tailles d'espace d'états : EN PROSE et en affichages courts dans §15.5, exposants
  intacts.
- 15-E7, l'objectif de démonstration : EN PROSE, cité des semaines 4 et 8. Le chapitre n'en donne
  aucune équation, seulement du code.
Le calcul 160/10 = 16, (210-50)/10 = 16, 16 x 16 = 256 de §15.4 est un AFFICHAGE DU COURS, lu sur la
figure 14.3 ; il n'a pas d'identifiant parce qu'il n'est pas une équation de source. Le chapitre de
la navigation web n'a AUCUNE équation (le drapeau has_equations du chunk 14-05 est faux : vérifié,
il n'y a que de la notation de coordonnées), et celui du courtage non plus.

VOIX DU COURS (D45). Aucune citation visible nulle part. Les trois cas de §15.8 sont écrits sur le
patron que la semaine 12 avait installé, « vous rencontrerez ... et cette forme est fausse », sans
sujet nommé, sans « l'auteur » et sans « le livre ». Les deux rapports incompatibles de §15.7 sont
introduits au passif, « la même expérience a été rapportée deux fois », et le cours NE RETIENT NI
L'UN NI L'AUTRE. L'échec de reproduction est rapporté au passif, et la première personne de la
source (« mes résultats », « je n'ai pas pu ») n'est JAMAIS reprise : les faits sont écrits, les
anecdotes sont supprimées. Les deux phrases que les notes rapportaient entre guillemets, sur le
remplacement de l'AR par de l'apprentissage supervisé et sur le fait que les réseaux « ne sont au
moins pas pires », sont RESTITUÉES dans la voix du cours. Aucune occurrence de guillemets de plus de
quatre-vingts caractères ne subsiste dans la page.

RUNNABILITÉ (D14, COURSE-PLAN §9.2). Énoncée UNE SEULE FOIS, en tête du laboratoire, en tableau, avec
ses chiffres. UN volet noté et il tourne (fiction interactive, aucun entraînement) ; UN volet de
démonstration sur journaux fournis (le cube) ; UN volet FACULTATIF ET NON NOTÉ HORS CARNET
(navigation web, décidé le 25/10 par D14 et NON RÉOUVERT) ; UN exercice de lecture et d'écriture (le
modèle de langue, clé payante, donc rien n'est exigé). L'introduction annonce en une phrase que le
laboratoire porte cet énoncé et ne le duplique pas.

`rliable` (C5) EST NOMMÉ ET RIEN DE PLUS, en §15.11. Il est cité dans SOURCES.md et n'a jamais été
déposé : la page nomme l'outil, renvoie au PROTOCOLE DU COURS (plusieurs graines, intervalles,
exigés depuis le jalon 2, issus des consignes de jalon du cours), et dit explicitement de ne pas
chercher de référence dans ce cours. Personne n'est envoyé vers une source absente.

LIVRABLES FINAUX (D47, COURSE-PLAN §10). Le brief est ÉCRIT DANS LA SEMAINE : rapport de 8 à 10
pages, présentation de 10 minutes, dépôt complet, évalués sur l'ensemble de la trajectoire. Le
critère unique, « quelqu'un d'autre peut l'exécuter », est RELIÉ EXPLICITEMENT aux deux résultats
négatifs de §15.7 : hyperparamètres absents d'une publication, et nombre non enregistré au moment où
il a été obtenu. Deux exigences propres à la semaine s'ajoutent au barème : la cinquième colonne de
la figure 15-01 pour le problème de l'étudiant, et trois numéros de semaine avec la justification
des onze exclusions.

CLÔTURE. IL N'Y A PAS DE SEMAINE 16. Le module 5 se termine et le cours avec lui. La page d'accueil
est rédigée ici (D47) et la semaine n'écrit PAS de conclusion de semaine séparée, afin qu'aucun des
deux textes ne reste non publié ; le dernier bloc de la page d'accueil, « Après la semaine 15 », clôt
le cours et ne pointe vers rien. Le dernier texte de corps est la sous-section « La dernière page »
de la section des livrables, qui est le dernier paragraphe que l'étudiant lit dans SCI1070. Elle est
écrite à la première personne dans la voix des ouvertures (D31) et NON SIGNÉE D'UN NOM, parce
qu'aucune des quatorze semaines précédentes ne signe d'un nom et qu'une signature nominale
apparaissant pour la première fois à la dernière page serait une rupture de registre.

DÉCOMPTE : 11 sections numérotées · 5 placeholders FIG (15-01 et 15-02 PRODUITES par le cours,
15-03, 15-04 et 15-05 EXTRAITES du livre, fig. 14.3 p.437, fig. 14.7 p.445 et fig. 21.6 p.667, vues
intactes sur image pendant la passe de lecture ; la sixième figure proposée par les notes est
REMPLACÉE par le tableau de coût de §15.6, décision prise à l'écriture) · 0 placeholder EQ (sept
équations identifiées, 15-E1 à 15-E7, aucune par placeholder : quatre écrites directement en KaTeX
dont trois transcrites d'images de page et une citée de la semaine 12, deux en prose, une citée des
semaines 4 et 8 sans affichage. L'inventaire complet est dans extraction/week-15.md)
{{% /comment %}}
