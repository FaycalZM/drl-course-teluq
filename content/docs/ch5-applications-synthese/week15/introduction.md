---
title: "Introduction"
weight: 1
---

## Quatorze semaines de méthodes, et personne pour vous donner la bonne

Bonjour à toutes et à tous ! Nous arrivons au bout, et je veux ouvrir cette dernière semaine en disant franchement ce qu'elle fait de différent, parce que c'est la seule du cours qui ne vous apprendra pas de méthode.

Regardez le chemin. La semaine 3 vous a donné une méthode de sélection d'élites. La semaine 5 un réseau Q profond. La semaine 8 un acteur-critique. La semaine 9 une politique gaussienne pour des actions continues. La semaine 10 une région de confiance. La semaine 11 une prime de nouveauté. La semaine 12 une recherche arborescente guidée par un réseau. La semaine 13 un modèle du monde et l'apprentissage hors ligne. La semaine 14 une récompense apprise de jugements humains. Chacune de ces semaines s'est terminée sur une phrase de la forme : **vous savez maintenant faire ceci**.

Aucune ne s'est terminée sur celle dont vous allez avoir besoin : **vous savez maintenant choisir**.

C'est pourtant la seule compétence que l'on vous demandera. Dans un cours, on vous remet une méthode et un problème taillé pour elle. Dans un emploi, dans un laboratoire, dans votre propre projet, on vous remet **un problème** et rien d'autre. Personne ne vous dira qu'il s'agit d'un problème à récompense parcimonieuse avec un espace d'actions discret et un modèle disponible. Personne ne vous dira que la semaine 11 est pertinente et que la semaine 9 ne l'est pas. Vous aurez à le décider, à estimer ce que cela coûtera, et à savoir d'avance comment vous saurez si cela a fonctionné.

Cette semaine est l'entraînement à cette décision, et elle est aussi la dernière chose que le cours vous demande, puisque vos livrables finaux en sont l'examen.

---

## Trois questions, et quatre problèmes qui n'ont rien en commun

La méthode que je vous propose tient en trois questions, et vous allez les voir appliquées quatre fois.

**Qu'est-ce qu'une observation ?** **Qu'est-ce qu'une action ?** **Quand arrive une récompense ?**

Ces trois questions ne sont pas une grille de lecture inventée pour l'occasion : elles sont la définition même d'un processus de décision markovien, celle de la semaine 1. La nouveauté de cette semaine est de les poser à des problèmes que personne n'a préparés pour elles.

Les quatre problèmes sont délibérément éloignés les uns des autres. **Un marché**, où une observation est une suite de prix et où l'action est d'acheter ou de ne rien faire. **Un paragraphe**, où l'observation *est* de la langue naturelle, et où l'action *est* une phrase. **Une page rendue dans un navigateur**, où l'observation est un dessin de 210 sur 160 pixels et l'action un clic dans un espace sans ordre naturel. Et **une permutation**, un cube de Rubik, où l'observation est l'état complet, où il y a douze actions, et où **aucune récompense n'arrive avant la toute fin**.

Quatre problèmes, trois questions, et un tableau qui tient sur une page. C'est l'objet central de la semaine, et tout le reste en découle.

---

## Ce que vous allez lire

Une phrase par section, pour que vous sachiez où vous allez.

La section 15.1 pose les trois questions et donne le tableau des quatre problèmes, qui est la colonne vertébrale de la semaine. Les sections 15.2 à 15.5 prennent les quatre problèmes un par un : le marché, le paragraphe, la page rendue, la permutation. Vous n'y apprendrez aucune méthode nouvelle, et c'est voulu : chaque fois, la méthode employée est une méthode que vous connaissez déjà, et l'intérêt est ailleurs, dans ce que le problème a fait à l'observation, à l'action et à la récompense.

La section 15.6 fait le compte de ce qui a transféré d'une semaine de cours à une application réelle, et de ce qui n'a pas transféré. Il y a trois choses dans la seconde colonne, et la troisième est la plus utile : **les chiffres publiés**.

La section 15.7 est la section de mesure de la semaine. Le cours a déjà montré quatre résultats négatifs, en semaines 10, 11, 12 et 13 ; en voici le cinquième et le sixième, et je les présente comme un **patron** et non comme une surprise. La section 15.8 réunit trois cas où un nom donné à une méthode ne correspond pas à ce que le code fait, et en tire une phrase que votre rapport final peut employer telle quelle. La section 15.9 reprend la tâche de la section 15.3 et la confie à un grand modèle de langue qui n'a reçu **aucun entraînement**, une semaine après la rétroaction humaine de la semaine 14 ; et je vous donne la lecture honnête de ce résultat, qui est plus intéressante que le résultat.

La section 15.10 est la carte de décision : quatorze semaines rangées non pas par ordre chronologique mais par les **caractéristiques de problème** qui les sélectionnent. La section 15.11 dit les limites, celles du cours et celles du domaine, et rappelle le protocole de mesure que le cours exige depuis le jalon 2.

Puis viennent le laboratoire, qui dit exactement ce qui s'exécute et ce qui ne s'exécute pas, les **livrables finaux**, et le quiz.

---

## Les symboles de la semaine, et trois collisions à annoncer avant les équations

Cette semaine n'a presque pas de mathématiques, et c'est normal pour une synthèse. Elle en a quatre équations affichées, groupées dans les sections 15.5 et 15.7, plus une probabilité d'une ligne en section 15.3. Les quatre portent **trois collisions de notation** qu'il faut trancher avant de les écrire, et je les annonce ici plutôt qu'au milieu d'une démonstration.

**Première collision, et elle est la plus grave.** La méthode d'entraînement du cube a besoin d'une **fonction de transition** : l'état atteint depuis \(s\) en jouant \(a\). On la rencontre écrite \(A(s,a)\). Cette lettre est indisponible dans ce cours : \(A_t\) est l'action à l'instant \(t\) depuis la semaine 1, et \(A^\pi(s,a)\) est la fonction d'avantage depuis la semaine 8. Trois sens pour un \(A\), dont deux à l'intérieur de la même équation, serait intenable. Ce cours écrit donc la transition \(\mathcal{T}(s,a)\), en capitale calligraphique, et ne touche plus à \(A\).

**Deuxième collision, et elle est la plus sournoise, parce qu'elle ne ressemble pas à une collision.** On rencontre la valeur de l'état atteint écrite \(v_s(a)\), c'est-à-dire avec la forme d'une valeur d'action. Ce n'en est pas une. Ce n'est pas \(q(s,a)\), ce n'est pas une estimation du retour à partir de \(s\) en jouant \(a\) : c'est la valeur \(v\) évaluée en un **autre état**, celui où l'action nous dépose. Ce cours l'écrit donc \(v(\mathcal{T}(s,a))\), ce qui est plus long et rend la chose visible. Vous verrez à la section 15.7 que cette notation n'est pas un pédantisme : l'échec de reproduction de la semaine se diagnostique exactement là, dans ce que l'on additionne à quoi.

**Troisième collision, et elle est entre deux semaines de ce cours.** La semaine 12 a écrit \(U(s,a)\) pour l'**utilité de sélection complète**, c'est-à-dire la valeur observée plus la prime d'exploration. La règle de descente de la section 15.5 écrit \(U\) pour la **prime d'exploration seule**, et additionne séparément une seconde quantité. Même lettre, deux portées différentes, à trois semaines d'intervalle : je le dis avant l'équation, et l'équation le redira.

Et une quatrième chose, qui n'est pas une collision de lettre mais une **différence d'algorithme cachée sous une même lettre**. La semaine 12 écrivait \(W(s,a)\) pour la **somme** des valeurs remontées à travers une arête, divisée ensuite par le nombre de visites pour donner une moyenne. Le \(W(s,a)\) de la section 15.5 est le **maximum** sur tout le sous-arbre sous cette arête. Ce n'est pas une variante de présentation, c'est une remontée différente, et elle est défendable précisément là où elle est employée : sur un casse-tête **déterministe à un seul joueur**, où il n'y a ni adversaire ni hasard pour vous empêcher de rejouer le meilleur chemin trouvé. Je vous le signale parce que c'est le genre de détail qui se perd quand on lit deux descriptions d'une même méthode en pensant qu'elles parlent du même objet.

{{% comment %}}SOURCE: notation.md §3 quinquies{{% /comment %}}

---

## L'inventaire des symboles nouveaux

Comme à chaque semaine, rien ne vous est demandé de mémoire : chaque symbole est redéfini devant vous à sa première apparition.

| Symbole | Ce qu'il désigne | Première section |
| --- | --- | --- |
| \(\mathcal{T}(s,a)\) | la **transition** : l'état atteint depuis \(s\) en jouant \(a\) | 15.5 |
| \(v(\mathcal{T}(s,a))\) | la valeur de l'état **atteint**, et non une valeur d'action | 15.5 |
| \(R(s)\) | un **indicateur de but** : \(+1\) sur l'état résolu, \(-1\) partout ailleurs | 15.5 |
| \(y_v\), \(y_p\) | les deux **cibles d'entraînement** de l'itération autodidacte, valeur et politique | 15.5 |
| \(N\) | la **profondeur de brouillage** appliquée à l'état résolu | 15.5 |
| \(N(s,a)\), \(P(s,a)\) | nombre de visites et probabilité a priori, les symboles de la semaine 12 | 15.5 |
| \(W(s,a)\) | ici le **maximum** des valeurs du sous-arbre, et non la somme de la semaine 12 | 15.5 |
| \(U(s,a)\) | ici la **prime d'exploration seule**, et non l'utilité complète de la semaine 12 | 15.5 |
| \(c\) | la constante d'exploration, le \(c_{\text{puct}}\) de la semaine 12 | 15.5 |
| \(p_{\text{demo}}\) | la probabilité qu'un lot soit un lot de démonstrations | 15.4 |

> [!NOTE]
 **Une remarque sur \(R\), parce que cette lettre a beaucoup servi dans ce cours.** Le \(R(s)\) de la section 15.5 n'est pas un retour, n'est pas une récompense de pas au sens de la semaine 1, et ne s'actualise pas. C'est un **indicateur** : il vaut \(+1\) si l'état est l'état résolu et \(-1\) sinon, point final. Il n'apparaît que dans les deux cibles d'entraînement du cube, et nulle part ailleurs de la semaine. Si vous le lisez comme une récompense ordinaire, l'équation 15-E1 vous paraîtra dire que l'on additionne une valeur et une récompense immédiate, ce qui est exactement l'erreur que la section 15.7 va diagnostiquer.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Poser à un problème non préparé les **trois questions** de la section 15.1, et dire laquelle des trois colonnes est **conçue** plutôt qu'observée.
- Décrire, pour chacun des quatre problèmes de la semaine, ce qu'est une observation, ce qu'est une action et quand arrive une récompense, sans confondre les quatre.
- Dire pourquoi la colonne « récompense » est celle où les quatre problèmes diffèrent le plus, et nommer les deux des quatre qui ont dû la **modifier** pour devenir apprenables.
- Énoncer la règle de partage d'une série temporelle que le cours applique depuis la semaine 7, et dire les trois conséquences d'un partage inversé.
- Dire pourquoi un espace d'actions formé de **phrases** ne se traite pas comme un espace d'actions discret ordinaire, et calculer l'ordre de grandeur qui le rend intraitable.
- Distinguer l'espace des **solutions complètes** de l'espace d'actions **par pas**, et dire lequel des deux la liste de commandes admissibles réduit.
- Nommer les **deux béquilles** qui rendent la tâche textuelle apprenable, et dire en quoi chacune est une intervention sur l'environnement et non sur l'agent.
- Expliquer pourquoi une interface qui ne respecte pas la convention de Gymnasium interdit l'emploi des enveloppes du cours, et dire quelle pièce il faut écrire à la place.
- Dire pourquoi un agent qui choisit parmi une liste de commandes variable ne peut pas employer la tête à une sortie par action de la semaine 5, et quelle architecture le remplace.
- Décrire la réduction d'un espace de clics continu à **256 actions discrètes**, et donner le calcul exact qui donne 16 par 16.
- Expliquer ce qu'une récompense qui **décroît avec le temps d'horloge** fait à la comparabilité d'un score publié, et donner les deux mesures qui l'établissent.
- Dire pourquoi des **démonstrations humaines** ne s'injectent pas directement dans une méthode sur politique, et nommer l'objectif de la semaine 4 qui sert de pont.
- Distinguer **démonstrations humaines** et **préférences humaines**, et dire ce qu'une démonstration ne contient structurellement pas.
- Énoncer les **quatre critères** de choix d'une représentation d'état, et les appliquer à un codage naïf pour montrer qu'il est redondant.
- Expliquer comment l'itération autodidacte supprime le problème de la récompense parcimonieuse **sans méthode d'exploration**, et dire à quelle classe de problèmes ce procédé se généralise.
- Écrire les deux cibles d'entraînement de l'itération autodidacte, et dire ce que chacune apprend à laquelle des deux têtes.
- Reconnaître la règle de sélection de la semaine 12 sous un autre nom, et nommer les **deux différences** entre la version de la semaine 12 et celle-ci.
- Dire pourquoi une remontée par **maximum** est défendable sur un casse-tête déterministe à un joueur et pas sur un jeu à deux joueurs.
- Faire le compte de ce qui a transféré d'une méthode de cours à une application, et nommer les **trois choses** qui n'ont pas transféré.
- Lire un **échec de reproduction** : dire ce qu'il démontre, ce qu'il ne démontre pas, et quelles trois informations le rendent utilisable.
- Diagnostiquer, sur une courbe de perte, une fonction de valeur **sans ancrage**, et écrire le correctif d'une ligne qui l'ancre.
- Dire ce que deux rapports incompatibles d'une même expérience permettent de conclure, et pourquoi ce n'est ni une fraude ni même une négligence.
- Énoncer la phrase que les trois cas de la section 15.8 établissent : **le nom d'une méthode dans un texte n'est pas une preuve de ce que fait le code.**
- Distinguer la **métrique des demi-tours** de la **métrique des quarts de tour**, donner la borne connue dans chacune, et dire laquelle s'applique à une implémentation à douze actions.
- Expliquer pourquoi une **profondeur de brouillage** n'est pas une **longueur de solution optimale**, et ce que cette différence fait à une prédiction de saturation.
- Énoncer la règle générale dont les deux points précédents sont des cas : une borne théorique ne contraint une mesure que si les deux sont dans les mêmes unités.
- Lire le résultat de la section 15.9 : dire ce qu'il montre, ce qu'il ne montre pas, et pourquoi la comparaison de coûts n'est pas à grandeurs égales.
- Classer un problème nouveau sur la carte de décision de la section 15.10, et nommer les **trois semaines** pertinentes et les onze qui ne le sont pas.
- Énoncer le protocole de mesure que le cours exige depuis le jalon 2, et dire ce qu'il change à la lecture d'une comparaison de méthodes.
- Rédiger un rapport, une présentation et un dépôt qui satisfont le seul critère que cette semaine impose : **quelqu'un d'autre peut l'exécuter.**

---

## Prérequis et outils

De la **semaine 1**, les trois objets d'un processus de décision markovien, qui sont les trois questions de cette semaine. De la **semaine 4**, l'objectif de vraisemblance logarithmique de la méthode d'entropie croisée, que la section 15.4 retrouve sous une autre application. De la **semaine 5**, le réseau Q profond, qui est la méthode de la tâche textuelle, et la notion de processus de décision **partiellement observable**, qui est exactement ce que cette tâche est. De la **semaine 7**, l'étude de cas du courtage, dont la section 15.2 est le rappel et non la reprise, et la règle de partage chronologique d'une série temporelle. De la **semaine 8**, l'acteur-critique à avantage et les **environnements vectorisés**, et la section 15.8 vous expliquera pourquoi ces deux acquis suffisent à identifier une méthode mal nommée. De la **semaine 11**, le constat qu'un classement de méthodes ne se transfère pas d'un environnement à l'autre. De la **semaine 12**, la recherche arborescente de Monte-Carlo, sa règle de descente et le réseau à deux têtes, que la section 15.5 réemploie intégralement. De la **semaine 13**, la lecture d'un résultat accompagné de son coût. De la **semaine 14**, enfin, la question à poser à tout système d'apprentissage par renforcement avant de regarder ses courbes : **quelle récompense optimise-t-il, et qui l'a écrite ?**

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | la pièce notée du laboratoire, qui n'a besoin d'aucun processeur graphique et tient en quelques minutes |
| **Gymnasium** | la convention d'interface que la section 15.3 va voir enfreindre, et l'adaptateur que le laboratoire vous fait écrire |
| **TextWorld** | le générateur de jeux textuels de la section 15.3 ; il s'installe dans le carnet et pas forcément sur votre machine, le laboratoire dit pourquoi |
| **PyTorch** | lecture de l'architecture à deux têtes de la section 15.5 ; aucun entraînement n'est demandé cette semaine |
| **Matplotlib** | la lecture des courbes de perte fournies avec la démonstration du cube |
| **Selenium et un pilote de navigateur** | uniquement pour la pièce **facultative et non notée** de la section 15.4 |
| **Page « Notation » du cours** | la section ajoutée cette semaine, avec les trois collisions ci-dessus |
| **Page « Glossaire » du cours** | une vingtaine de termes nouveaux, dont deux qui ne diffèrent que par un mot et qui sont toute l'erreur de la section 15.8 |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 15{{% /comment %}}

> [!IMPORTANT]
 **Une seule des quatre applications de cette semaine s'exécute dans un carnet, et je ne vais pas vous laisser le découvrir à la fin.** Le laboratoire dit exactement laquelle, où, et pourquoi les trois autres ne s'exécutent pas : un entraînement de six jours sur un processeur graphique pour l'une, un navigateur piloté qui ne tient pas dans une session gratuite pour l'autre, une clé d'interface payante pour la troisième. Après treize semaines passées à distinguer ce qui tourne de ce qui se raconte, une dernière semaine qui promettrait quatre laboratoires exécutables et n'en livrerait aucun serait la pire des sorties. L'énoncé complet est au laboratoire, une seule fois, avec ses chiffres.

---
