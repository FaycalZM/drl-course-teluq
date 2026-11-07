---
title: "Introduction"
weight: 1
---

## Onze semaines d'agents qui n'ont jamais regardé devant eux

Bonjour à toutes et à tous ! Je veux ouvrir cette semaine par une observation qui vaut pour les onze précédentes, et qu'aucune d'entre elles n'a formulée.

Faites l'inventaire avec moi. Depuis la semaine 4, nos agents agissent, observent ce qui arrive, et ajustent une table, des poids ou une politique. La semaine 5 a remplacé la table par un réseau, la semaine 8 a remplacé la valeur par une politique paramétrée, la semaine 9 a étendu tout cela aux actions continues, la semaine 10 a borné la taille d'un pas de mise à jour, la semaine 11 a payé la nouveauté. Onze semaines, six familles de méthodes, et une chose qu'aucune d'elles n'a jamais faite : **demander ce qui arriverait si**. Pour savoir qu'une action mène à une catastrophe, nos agents ont tous dû la jouer réellement, dans l'environnement réel, et encaisser la récompense réelle. C'est la définition même d'une **méthode sans modèle** (*model-free*), et la semaine 3 l'a nommée sans que nous en mesurions le prix.

Cette semaine donne à l'agent un modèle du monde et l'autorise à chercher dedans. Il pourra, avant de jouer, dérouler des suites de coups dans sa tête, comparer ce qu'elles donnent, et ne jouer que le coup qu'il a trouvé le meilleur. Puis la semaine posera la question difficile, celle qui fait tout l'intérêt du sujet : **et si le modèle lui-même devait être appris ?**

Il y a un second chantier, et je veux l'annoncer tout de suite parce qu'il remet en cause une hypothèse de la semaine 1. Nous allons mettre un deuxième agent dans le monde, puis quarante, puis deux cent quarante-quatre. Depuis la première semaine de ce cours, toutes nos démonstrations supposent que l'environnement **ne change pas pendant que l'agent apprend** : c'est la **stationnarité** (*stationarity*), elle est dans la définition d'un processus de décision markovien, et nous ne l'avons jamais discutée parce qu'elle était toujours vraie. Elle cesse de l'être dès qu'un autre agent apprend en même temps que le vôtre. Son comportement change, donc votre environnement change, donc la cible que vous poursuivez bouge toute seule.

> [!IMPORTANT]
 **Voici l'énoncé qui fait la charnière de la semaine, et il tient en deux cas.** Si les autres agents du monde sont **hors de votre contrôle** et n'apprennent pas, vous les absorbez dans l'environnement et **rien ne change** : vous faites de l'apprentissage par renforcement ordinaire, à un seul agent, exactement comme depuis onze semaines. L'auto-jeu de la première moitié de cette semaine est précisément ce cas, et c'est pourquoi il tient dans le cadre habituel. Le problème multi-agent commence à l'endroit exact où cette absorption cesse d'être adéquate, c'est-à-dire dès que l'autre agent **apprend aussi**.

{{% comment %}}SOURCE: LAPAN ch.22 p.675{{% /comment %}}

---

## Ce que vous allez lire, et les trois erreurs que je corrige en chemin

Voici la colonne vertébrale de la semaine, une phrase par section.

La section 12.1 dit ce qu'un modèle achète, et je vais être strict : il achète exactement **deux** choses, et je refuserai d'en nommer une troisième. La section 12.2 installe le jeu de plateau comme cas facile, avec sa part difficile, qui est l'adversaire. La section 12.3 construit la recherche arborescente : trois statistiques par arête, quatre phases, et un signe qui s'inverse à chaque niveau de la remontée. La section 12.4 isole la contrainte que cette recherche impose à un environnement, et c'est la contrainte la plus transposable de la semaine. La section 12.5 ferme la première méthode avec l'**auto-jeu** (*self-play*), et y rencontre un fait que je ne veux pas vous cacher : la perte ne mesure rien. La section 12.6 apprend le modèle aussi, en remplaçant un réseau par trois, et fait tourner la recherche dans un état caché qui n'est jamais comparé à une position réelle. La section 12.7 entraîne ce modèle qu'on ne peut pas vérifier. La section 12.8 rapporte le résultat obtenu, et ce résultat est un échec. Les sections 12.9 à 12.11 mettent plusieurs agents dans un monde : la notation que le cours doit inventer pour en parler, un monde concret de prédateurs et de proies, puis la collaboration et la non-stationnarité.

> [!WARNING]
 **Trois constantes et un ordre d'appel vous attendent au piège cette semaine, et je les corrige dans la page.** Les trois erreurs que cette semaine rencontre portent toutes sur du **code**, c'est-à-dire sur exactement ce qu'un étudiant recopie. La première retire à la recherche son terme d'exploration et la transforme silencieusement en descente gloutonne. La deuxième fixe un horizon de coups **en dessous du nombre minimal de coups qu'il faut pour gagner la partie qu'on joue**. La troisième applique un réseau de prédiction au mauvais état caché, et combine ensuite une récompense et une valeur qui ne viennent pas du même instant. Les trois sections concernées vous donnent la forme correcte, l'expliquent, et ne reproduisent jamais la forme fautive. Retenez surtout la méthode : une constante publiée se **redérive**, elle ne se recopie pas.

---

## Les symboles de la semaine, et trois collisions à trancher

Cette semaine porte neuf équations, dont une que le cours **invente** faute de toute notation existante. Avant d'entrer dans les sections, je dois trancher trois collisions de symboles, sans quoi la semaine se battrait contre sa propre notation pendant vingt pages.

**Première collision, et c'est la plus dangereuse : \(Q(s,a)\) ne désigne pas ici ce qu'il désigne depuis la semaine 4.** Dans toute la première moitié de la semaine, \(Q(s,a)\) est une **statistique de recherche** : la moyenne des valeurs remontées à travers l'arête \((s,a)\) de l'arbre, mise à jour à chaque passage. Ce n'est pas \(q_\pi(s,a)\), la valeur d'action vraie sous une politique fixée, et ce n'est pas non plus l'estimation \(Q_\theta(s,a)\) que la semaine 5 faisait sortir d'un réseau. C'est un compteur de moyenne, local à une recherche, et il est jeté quand la recherche se termine. Je l'écris \(Q(s,a)\) parce que c'est la lettre que tout le domaine emploie pour cet objet, et je vous demande de garder la distinction en tête.

**Deuxième collision : \(\tau\).** La semaine 9 a employé \(\tau\) pour le coefficient d'une mise à jour douce du réseau cible, autour de \(0{,}005\). Cette semaine, \(\tau\) est une **température** appliquée à des comptages de visites, et elle ne prend que les valeurs \(1\) et \(0\). Les deux objets n'ont aucun rapport, et aucune mise à jour douce n'apparaît dans cette semaine : il n'y a donc pas d'ambiguïté possible à l'intérieur d'une équation, mais je préfère le dire avant qu'après.

**Troisième collision : \(\alpha\), pour la quatrième fois dans ce cours.** \(\alpha\) est le pas d'apprentissage depuis la semaine 3, la semaine 6 a dû écrire \(\alpha_{\mathrm{PER}}\) pour l'exposant du tampon priorisé, et cette semaine introduit un troisième sens, la **concentration d'une loi de Dirichlet**. Je l'écris \(\alpha_{\mathrm{Dir}}\) partout, sans exception, et le \(\alpha\) nu reste le pas d'apprentissage.

Voici enfin les symboles nouveaux, dans l'ordre où ils apparaîtront.

| Symbole | Ce qu'il désigne | Première section |
| --- | --- | --- |
| \(P(s,a)\) | probabilité a priori portée par une arête, fournie par la tête de politique du réseau | 12.3 |
| \(N(s,a)\) | comptage de visites de l'arête ; à la racine, ces comptages **deviennent** la politique | 12.3 |
| \(W(s,a)\), \(Q(s,a)\) | somme des valeurs remontées, et sa moyenne | 12.3 |
| \(U(s,a)\) | utilité de sélection, celle qui décide quelle arête on descend | 12.3 |
| \(c_{\text{puct}}\) | constante d'exploration de cette utilité | 12.3 |
| \(\alpha_{\mathrm{Dir}}\) | concentration de la loi de Dirichlet du bruit de racine | 12.3 |
| \(\tau\) | température sur les comptages de visites | 12.5 |
| \(h_\theta\), \(g_\theta\), \(f_\theta\) | réseaux de représentation, de dynamique et de prédiction | 12.6 |
| \(s^k\) | état caché après \(k\) pas de dynamique | 12.6 |
| \(r^k\), \(v^k\), \(\pi^k\) | récompense immédiate, valeur et politique prédites au pas \(k\) | 12.6 |
| \(K\) | longueur du déroulement | 12.7 |
| \(z_k\), \(u_k\) | cible de valeur et cible de récompense du pas \(k\) | 12.7 |
| \(i\), \(n_t\) | indice d'un agent, et **nombre d'agents vivants à l'instant \(t\)** | 12.9 |
| \(O^i_t\), \(A^i_t\), \(R^i_t\) | observation, action et récompense de l'agent \(i\) | 12.9 |
| \(\mathbf{A}_t\) | action jointe, c'est-à-dire le \(n_t\)-uplet des actions | 12.9 |
| \(\pi_\theta(a \mid o^i)\) | politique partagée par tout un groupe d'agents | 12.9 |

> [!NOTE]
 **Les six dernières lignes de ce tableau sont une création de ce cours, et vous avez le droit de le savoir.** Il n'existe pas de notation établie pour le cas multi-agent : le cas se traite d'ordinaire sans une seule équation, tout y est indexé par des noms d'agents sous forme de dictionnaires, et la notation de référence de ce cours ne le couvre pas. La page « Notation » a donc gagné une section cette semaine, marquée comme une création, et la section 12.9 définit chacun de ces symboles devant vous avant de s'en servir. Un détail de cette notation n'est pas cosmétique : \(n_t\) porte un indice de temps, parce que le nombre d'agents **diminue en cours d'épisode** pendant que l'épisode continue.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Énoncer les **deux** motivations d'une méthode avec modèle, et dire pourquoi ce cours refuse d'en ajouter une troisième.
- Expliquer pourquoi la frontière entre « un environnement » et « un modèle de l'environnement » est plus mince que le vocabulaire ne le laisse croire, avec trois exemples déjà rencontrés dans ce cours.
- Dire ce qu'un jeu de plateau rend facile, ce qu'il rend difficile, et pourquoi l'analyse d'une position exige un modèle du jeu.
- Décrire minimax en une phrase, définir le facteur de branchement, et dire ce que l'élagage de l'arbre remplace.
- Citer trois ordres de grandeur qui ferment la porte à l'énumération complète d'un jeu, et dire lequel des trois jeux reste résoluble entièrement.
- Nommer les **trois statistiques** portées par une arête de l'arbre de recherche, et dire laquelle devient la politique à la racine.
- Écrire l'utilité de sélection avec ses deux termes, dire ce que fait la racine carrée de son numérateur, et décrire **précisément** ce qui arrive à la recherche si on l'oublie.
- Dire pourquoi \(Q(s,a)\) ne désigne pas, dans cette semaine, la valeur d'action des semaines 4 à 10.
- Décrire les **quatre phases** d'une recherche arborescente et dire, dans la phase de remontée, pourquoi le signe de la valeur s'inverse à chaque niveau.
- Expliquer ce que le bruit de Dirichlet fait à la racine, pourquoi il n'est appliqué **qu'**à la racine, et ce qu'une concentration trop faible produit sur sept colonnes.
- Énoncer la contrainte qu'une recherche arborescente impose à un environnement, et dire pourquoi l'interface standard d'un environnement d'apprentissage par renforcement ne la satisfait pas.
- Expliquer ce qu'un encodage compact d'une position achète, et pourquoi la mémoire est la ressource contraignante d'une recherche.
- Décrire un réseau à deux têtes, dire ce que chaque tête renvoie, et expliquer pourquoi deux plans d'entrée suffisent à rendre le réseau indépendant du joueur.
- Transformer des comptages de visites en politique, et dire ce que font les deux valeurs de la température.
- Décrire la porte d'évaluation qui autorise un apprenti à remplacer le meilleur réseau, avec ses deux nombres.
- Expliquer **pourquoi la perte d'un entraînement par auto-jeu ne contient aucune information**, pourquoi le taux de victoire contre le meilleur réseau reste autour d'un demi, et par quelle mesure on constate alors un progrès.
- Nommer les trois fonctions qui remplacent un simulateur exact, et dire ce que chacune prend en entrée et ce qu'elle renvoie.
- Expliquer pourquoi rien n'oblige un état caché à ressembler à une position de jeu, et quelle conséquence pratique cela a sur la structure de l'arbre.
- Écrire les trois cibles d'un déroulement sur cinq pas, et dire quelle est la seule chose contre laquelle le modèle appris est effectivement entraîné.
- Dire pourquoi une pondération constante appliquée à des pertes n'est pas équivalente à une mise à l'échelle du gradient dans une récurrence.
- Rapporter un résultat d'entraînement **négatif** avec la largeur de conclusion qu'il autorise, et distinguer ce qui est mis en cause d'une méthode et de sa reproduction.
- Dire à quelle condition exacte la présence d'autres agents ne change rien, et à quelle condition elle change tout.
- Définir l'action jointe et la politique partagée, et dire pourquoi le nombre d'agents porte un indice de temps.
- Décrire une observation **égocentrée et relative au groupe**, et expliquer comment une seule politique peut servir deux groupes opposés.
- Dire ce qui, dans une interface multi-agent, interdit de réutiliser les outils des onze semaines précédentes, et ce qu'une population volatile impose à une boucle d'entraînement.
- Reconstruire, à partir de quatre nombres, la proportion de proies chassées dans un épisode entraîné.
- Expliquer pourquoi une chasse en couple n'est pas la preuve d'un algorithme collaboratif, et dire ce qu'elle prouve réellement.
- **Nommer la non-stationnarité**, la reconnaître sur une courbe sans tendance, et dire en quoi son mécanisme diffère de celui de la triade fatale de la semaine 5 tout en produisant la même signature.
- Nommer trois routes que cette semaine ouvre vers le jalon 4.

---

## Prérequis et outils

De la **semaine 3**, la taxonomie des méthodes et la distinction entre méthode avec modèle et méthode sans modèle : cette semaine est la première à se placer du côté « avec modèle ». De la **semaine 5**, le réseau de valeurs d'action, sa cible à un pas et son réseau cible, parce que la seconde moitié de la semaine les applique **sans y changer une ligne**. De la **semaine 8**, le réseau à deux têtes de l'acteur-critique : la première méthode de la semaine emploie exactement cette architecture, et je ne la réexpliquerai pas. De la **semaine 11**, le comptage de visites, qui revient ici dans un rôle complètement différent, et l'idée d'une exploration **dirigée**, dont la recherche arborescente est la forme la plus aboutie que ce cours rencontrera. De la **semaine 1**, enfin, la stationnarité, qui est l'hypothèse que la fin de la semaine casse.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les trois volets du laboratoire ; aucun ne demande de processeur graphique, et le plus long tient dans une heure |
| **PyTorch** | le réseau à deux têtes, ses blocs de convolution résiduels, et les trois réseaux de la seconde moitié |
| **NumPy** | l'encodage des positions, le masquage des coups illégaux, et le tirage de Dirichlet |
| **Python standard** | `dataclasses` pour les hyperparamètres, et un dictionnaire pour les statistiques de l'arbre |
| **Matplotlib** | les courbes du laboratoire, et surtout le tableau du tournoi entre points de contrôle |
| **TensorBoard** | la perte, le taux de victoire contre le meilleur réseau, et le compteur de promotions |
| **Gymnasium** | **absent de la première moitié de la semaine, et c'est le sujet de la section 12.4** : son interface ne permet pas ce qu'une recherche exige |
| **Page « Notation » du cours** | la section multi-agent, nouvelle cette semaine, et les trois collisions tranchées ci-dessus |
| **Page « Glossaire » du cours** | une trentaine de termes nouveaux, dont « remontée », qui ne doit pas être confondu avec « sauvegarde » |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 12{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

> [!NOTE]
 **Cette semaine ne porte aucun jalon, et son laboratoire est formatif.** Le jalon 4 vous attend en semaine 14, et il pourra s'appuyer sur ce que vous écrivez ici : la section 12.11 nomme, en terminant, trois routes que cette semaine ouvre vers lui. Profitez du caractère formatif du laboratoire pour faire la chose que cette semaine demande et qu'une semaine notée rend inconfortable : **regarder une perte qui ne descend pas, sans la corriger**, parce qu'ici elle n'a rien à descendre.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---
