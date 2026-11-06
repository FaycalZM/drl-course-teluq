---
title: "15.4 Une page rendue"
weight: 5
---

## Deux industries qui faisaient déjà ce travail, et une récompense que personne ne sait écrire

Troisième problème, et celui dont l'énoncé est le plus proche de ce qu'une entreprise appelle un besoin. La **navigation web** (*web navigation*), c'est le fait d'interagir avec un site : cliquer des liens, saisir du texte, et plus généralement enchaîner des actions vers un but.

Commençons par une remarque qui remet les choses en place. Ce travail est déjà **automatisé depuis longtemps**, et pas par de l'apprentissage par renforcement. Deux industries entières en vivent : le **test de site web** (*website testing*), où l'on rejoue des scénarios pour vérifier qu'une mise à jour n'a rien cassé, et l'**extraction de données web** (*web scraping*), où l'on récupère des informations publiées sur des pages. Les deux fonctionnent, les deux emploient des outils matures, et aucun de ces outils n'apprend quoi que ce soit.

{{% comment %}}SOURCE: LAPAN ch.14 p.429{{% /comment %}}

Posons alors les trois questions, et observons où la troisième bloque. Un agent émet des actions, observe un état : jusqu'ici tout va bien. Mais **la récompense n'est pas claire et doit être définie tâche par tâche** : remplir correctement un formulaire, atteindre la page qui porte l'information cherchée. Il n'existe pas de « score » qu'un navigateur fournirait, comme un jeu d'arcade fournit le sien. C'est le seul des quatre problèmes de la semaine où la récompense doit être **inventée de A à Z pour chaque tâche**, et c'est la raison pour laquelle l'automatisation du navigateur (*browser automation*) par apprentissage est restée un sujet de recherche alors que l'automatisation du navigateur par script est un métier.

{{% comment %}}SOURCE: LAPAN ch.14 p.429{{% /comment %}}

---

## Trois applications où l'apprentissage apporte quelque chose

Si des scripts suffisent, qu'est-ce que l'apprentissage ajoute ? Trois réponses, et elles sont précises.

**Le test qui généralise.** Un test scripté dit « déplace la souris de cinq pixels vers la gauche, puis clique ». Il casse au premier changement de mise en page. Un agent entraîné sur des **démonstrations humaines** (*human demonstrations*) apprend « ferme la boîte de dialogue », ce qui survit à un déplacement du bouton.

**L'exploration de vulnérabilités de sécurité.** Un agent essaie des actions bizarres, des séquences que personne n'a prévues, et il le fait **beaucoup plus vite** qu'une personne. C'est le cas où l'absence de bon sens de l'agent devient un avantage : c'est exactement ce qu'on lui demande.

**Le remplissage de formulaires à grande échelle.** Non pas un formulaire, mais des centaines de milliers de sites **hétérogènes**, où écrire un script par site est hors de question. C'est le cas où le coût du script dépasse le coût de l'apprentissage.

{{% comment %}}SOURCE: LAPAN ch.14 p.430{{% /comment %}}

---

## Le paragraphe le plus honnête de la semaine, et ce qu'il vous dit sur votre projet

Il y a dans ce problème un constat que je veux reprendre à mon compte, parce qu'il vaut pour n'importe quelle application réelle et parce qu'il explique l'existence des jeux de référence.

Construire un système d'extraction de données web à taille réelle demanderait **des mois de travail d'une équipe**, et la plus grande partie des difficultés rencontrées **n'auraient rien à voir avec l'apprentissage par renforcement** : rassembler les données, communiquer avec un moteur de navigateur, décider de la représentation des entrées et des sorties, maintenir tout cela en marche. L'algorithme serait une petite fraction du travail.

{{% comment %}}SOURCE: LAPAN ch.14 p.430{{% /comment %}}

> [!IMPORTANT]
 **Lisez cela comme une consigne pour votre livrable final, et non comme une anecdote.** La proportion d'un projet d'apprentissage par renforcement qui est de l'apprentissage par renforcement est faible, et elle est d'autant plus faible que le problème est réel. Ce qui reste, c'est de l'ingénierie d'environnement, de la représentation, de l'instrumentation et du protocole. Ce cours a passé quatorze semaines sur la petite fraction, parce que c'est ce qui ne s'apprend pas sur le terrain. Votre rapport, lui, sera jugé **aussi** sur l'autre part : la clarté de votre enveloppe, l'exactitude de votre journal, la reproductibilité de votre dépôt.

C'est de ce constat que découle le recours à un **jeu de référence** (*benchmark*), et les deux conditions qu'un bon jeu de référence doit satisfaire sont en tension : il doit être **assez simple pour qu'on puisse itérer vite**, et **assez difficile pour qu'il reste de la marge**. Un jeu de référence trop facile est résolu et n'apprend plus rien ; un jeu de référence trop lourd ne permet plus d'essayer dix idées dans une journée.

---

## MiniWoB, et l'histoire de son abandon

Le jeu de référence employé ici s'appelle **MiniWoB**, publié en décembre 2016 : **80 tâches** de navigateur, observées au niveau des pixels, accompagnées d'une description textuelle de la tâche, et pilotées à travers un protocole de bureau à distance. Il a été **abandonné presque aussitôt après sa publication**. Une université en a ensuite publié une continuation, **MiniWoB++**, aujourd'hui maintenue par la fondation qui maintient aussi Gymnasium.

{{% comment %}}SOURCE: LAPAN ch.14 p.431-432{{% /comment %}}

Je ne vous raconte pas cela pour le plaisir de l'anecdote : un jeu de référence abandonné puis repris par deux équipes successives est un objet dont les versions ne sont **pas interchangeables**, et c'est le genre de détail qui explique qu'un chiffre publié ne se retrouve pas.

L'étendue des tâches mérite d'être donnée, parce qu'elle est elle-même instructive sur ce qu'est une action. À un bout : « clique le bouton de fermeture de la boîte de dialogue », une action, zéro ambiguïté. À l'autre bout : « ouvre les groupes repliés et clique le lien qui porte tel texte », ou « choisis telle date dans le sélecteur de dates », la date étant **tirée au hasard à chaque épisode**. Et plus loin encore, des tâches qui demandent de la **reconnaissance de caractères**, du type « cochez les cases qui portent ce texte », le texte étant lui aussi engendré aléatoirement.

{{% comment %}}SOURCE: LAPAN ch.14 p.431{{% /comment %}}

Notez ce que la randomisation fait au problème. Une tâche où la cible change à chaque épisode interdit d'apprendre une position : il faut apprendre une **relation** entre l'énoncé et l'écran. C'est la différence entre un agent qui mémorise et un agent qui lit.

---

## Du clic libre à 256 actions, et le calcul exact

Voici la réduction d'espace d'actions la plus concrète de la semaine, et je la détaille parce que les chiffres sont vérifiables et parce que c'est la **Figure 15-3** qui les porte.

En principe, l'agent dispose du clavier entier, de la souris libre sur la page et de la molette. C'est un espace mixte, continu en position, et sans aucun ordre naturel : deux pixels voisins ne font pas deux actions voisines si l'un est sur un bouton et l'autre à côté.

La réduction retenue est la suivante. L'écran mesure **160 pixels de large sur 210 de haut**. Les **50 premiers pixels du haut** sont une bannière d'énoncé qui **ne contient aucun élément actif** : on les retire. Il reste donc une zone cliquable de **160 sur 160 pixels**, découpée en cellules de **10 pixels** de côté. Le compte :

$$
\frac{160}{10} = 16, \qquad \frac{210 - 50}{10} = 16, \qquad 16 \times 16 = 256
$$

**Une grille de 16 par 16, donc 256 clics discrets.** Le nombre 10 est la **taille d'une cellule en pixels**, et non le nombre de cellules d'un côté : l'énoncer dans l'autre sens donnerait une grille de 10 par 10, c'est-à-dire 100 actions, ce qui ne fait pas 256. Je le précise parce que les deux chiffres se confondent facilement et parce que la figure les sépare sans ambiguïté, en étiquetant les deux premières cellules de la grille.

{{% comment %}}SOURCE: LAPAN ch.14 p.437 (fig. 14.3, image){{% /comment %}}

{{< bookfig src="15-03.png" week="15" >}}

Deux conséquences chiffrées de cette réduction, et elles vont dans des directions opposées.

**La première est un coût.** 256 actions, c'est **128 fois** l'espace d'actions de CartPole. Vous avez passé les semaines 4 à 8 sur des espaces de deux à six actions ; en voici un de 256, avec la même méthode.

**La seconde est plus grave et elle est structurelle.** L'agent est **sans mémoire** : il reçoit l'écran courant et rien d'autre. Or une tâche en deux étapes, du type « ouvre le menu, puis clique l'entrée », exige de savoir si le menu est déjà ouvert. Si cette information n'est pas lisible sur l'écran courant, la propriété de Markov est **brisée**, et aucun réglage d'hyperparamètres ne la rétablit. C'est le même diagnostic que l'inventaire invisible de la section 15.3, dans un autre habillage.

{{% comment %}}SOURCE: LAPAN ch.14 p.452{{% /comment %}}

---

## Ce qu'une observation donne vraiment ici, en une image

Un mot sur la ligne « observation » de ce problème, parce qu'elle est la plus riche des quatre et que cette richesse est elle-même un choix.

L'observation est un **dictionnaire** : un énoncé textuel, une capture d'écran en couleur de 160 pixels de large sur 210 de haut, et les éléments de l'**arbre DOM** (*DOM tree*) avec leurs attributs. Trois angles d'attaque donc, et ils ne demandent pas le même travail. Les pixels demandent un réseau convolutif et de la reconnaissance de formes. L'arbre DOM demande une représentation de graphe, et il rend la tâche beaucoup plus facile, au prix d'une hypothèse forte : que la page soit construite proprement. L'énoncé textuel ramène au problème de la section 15.3.

{{% comment %}}SOURCE: LAPAN ch.14 p.433, p.435{{% /comment %}}

La **Figure 15-4** montre trois instances de la même tâche, qui demande d'appuyer sur le bouton portant le nombre de côtés de la figure affichée. Regardez-la en vous demandant, pour chacun des trois angles d'attaque, ce qu'il faudrait pour réussir : en pixels, compter les côtés d'un polygone ; en DOM, lire un attribut qui peut-être n'existe pas ; en texte, comprendre un énoncé qui ne dit pas quelle est la figure. C'est le meilleur résumé en une image de ce que « choisir une représentation » veut dire.

{{< bookfig src="15-04.png" week="15" >}}

---

## La récompense qui décroît avec le temps d'horloge, et c'est un danger de mesure

Voici le point de cette section que je tiens pour le plus important de la semaine en matière de méthode, et il a été trouvé **à l'intérieur d'un jeu de référence**, c'est-à-dire à l'endroit où personne ne va regarder.

Prenez une tâche élémentaire : cliquer le bon élément. Le clic est correct, la tâche est réussie, et l'environnement renvoie **0,7936**, avec une récompense brute de **1** et un temps écoulé de **2,0666 secondes**. Rejouez exactement la même action, le navigateur n'étant plus dessiné à l'écran, c'est-à-dire **sans interface** (*headless*), et l'environnement renvoie **0,9918** en **0,09 seconde**, pour la même récompense brute de 1.

{{% comment %}}SOURCE: LAPAN ch.14 p.436{{% /comment %}}

La récompense fournie n'est donc pas la récompense de la tâche : c'est la récompense de la tâche **multipliée par une décroissance en temps d'horloge**. Plus votre machine est lente, plus votre agent est pénalisé, pour un comportement identique.

> [!WARNING]
 **Tirez-en la conséquence complète, parce qu'elle est plus large que ce jeu de référence.** Un score publié sur cette famille de tâches est **dépendant de la machine** et **dépendant du mode de rendu**. Deux équipes qui obtiennent la même politique, exactement la même, publieront deux nombres différents, et la différence peut valoir deux dixièmes sur une échelle qui va à un. Aucune des deux ne triche. Aucune des deux ne le sait forcément. Et surtout : **une comparaison de méthodes faite sur deux machines différentes mesure en partie les machines.** Le jalon 4 vous a demandé de traiter un changement de capacité comme un déploiement nouveau ; voici le même énoncé pour le matériel. Si vous rapportez un résultat sur une tâche chronométrée, **rapportez le matériel, le mode de rendu et le temps par pas**, sinon votre nombre n'est comparable à rien, pas même à lui-même d'une session à l'autre.

Et notez où ce défaut se trouve : pas dans un algorithme, pas dans un article, mais dans l'**instrument de mesure**, qui est précisément l'objet qu'on n'inspecte pas parce qu'on lui fait confiance. Le réflexe à emporter de cette semaine est simple : **avant de mesurer un agent, mesurez l'environnement**. Jouez une action dont vous connaissez la valeur attendue, deux fois, dans deux conditions, et regardez si vous obtenez le même nombre.

---

## Des démonstrations humaines, une semaine après des préférences humaines

Il reste un morceau de ce problème, et il tombe exactement une semaine après la semaine 14. Je le traite donc en soulignant la **différence**, parce que les deux objets se ressemblent par le nom et pas par la nature.

La semaine 14 demandait à une personne de **comparer** deux comportements. Ici, on demande à une personne de **faire** la tâche, et on enregistre ce qu'elle fait : ce sont des **démonstrations humaines**. La différence structurelle est la suivante, et elle est la raison pour laquelle les deux ne sont pas interchangeables : **une démonstration ne contient aucun exemple négatif.** Elle vous montre un chemin qui marche ; elle ne vous dit rien de ce qui ne marche pas, ni pourquoi. La comparaison de la semaine 14, elle, produisait des exemples négatifs par construction, puisque l'un des deux segments était jugé moins bon.

{{% comment %}}SOURCE: LAPAN ch.14 p.452{{% /comment %}}

Et il y a un second obstacle, purement technique celui-là, et c'est un bel exercice de révision. Des démonstrations sont des données **hors politique** : elles ont été produites par une personne, pas par la politique courante. Or la méthode employée ici est **sur politique**. On ne peut donc pas les verser dans le gradient de politique : la dérivation de la semaine 8 suppose que les trajectoires viennent de la politique qu'on dérive.

La solution est élégante et elle ne demande aucune méthode nouvelle. On traite la **tête de politique comme un classificateur** et on lui applique une **entropie croisée** vers l'action démontrée. Autrement dit : on réemploie l'objectif de vraisemblance logarithmique de la semaine 4. Il n'est pas question de remplacer l'apprentissage par renforcement par de l'apprentissage supervisé ; il est question de réemployer une technique supervisée **au service** d'une méthode d'apprentissage par renforcement, sur un lot de données qu'elle ne saurait pas digérer autrement.

{{% comment %}}SOURCE: LAPAN ch.14 p.454{{% /comment %}}

La mécanique tient en trois lignes de consigne, et je vous la donne parce qu'elle est réutilisable telle quelle : avec une probabilité \(p_{\text{demo}} = 0{,}5\), le lot courant est tiré dans l'ensemble des démonstrations plutôt que dans l'expérience collectée ; on calcule alors une entropie croisée entre la sortie de la tête de politique et l'action démontrée ; et la **tête de valeur n'est pas touchée**, puisqu'une démonstration ne porte aucune information de valeur.

{{% comment %}}SOURCE: LAPAN ch.14 p.455{{% /comment %}}

---

## Et l'outil qui existait, mais pas pour cet usage

Un dernier détail, court, et je le garde parce qu'il illustre une phrase que je veux que vous retiriez de ce cours.

L'enregistrement des démonstrations avait un outil officiel, livré avec le jeu de référence. Il enregistre l'**arbre DOM** et **pas les pixels**. Comme l'agent dont il est question travaille sur les pixels, ses démonstrations sont **inutilisables** telles quelles, et un second enregistreur a dû être écrit pour capturer les captures d'écran en même temps que les actions.

{{% comment %}}SOURCE: LAPAN ch.14 p.453{{% /comment %}}

**« L'outil existe » ne veut pas dire « l'outil convient ».** C'est une ligne de budget, pas une ligne de documentation, et elle apparaît dans tous les projets.

Et pour finir sur un résultat mesuré, qui donne l'ordre de grandeur de ce que tout cela achète : sur une tâche nettement plus difficile, un tic-tac-toe joué dans le navigateur, **deux heures** d'entraînement avec démonstrations donnent une récompense moyenne de **0,05**. L'agent gagne quelques parties ; il en perd d'autres, et en termine d'autres encore sur un match nul.

{{% comment %}}SOURCE: LAPAN ch.14 p.456-457{{% /comment %}}

Et une note pour la section 15.9, parce que la suite logique de ce problème y est : il existe des travaux qui ne cherchent plus à faire apprendre un agent à cliquer, mais à demander à un **grand modèle de langue** de **produire le script d'automatisation** correspondant à une tâche décrite en français. Nous y venons dans trois sections.

{{% comment %}}SOURCE: LAPAN ch.14 p.458{{% /comment %}}

---
