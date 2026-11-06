---
title: "Glossaire"
weight: 2
---

# Glossaire français ⇄ anglais

La littérature de ce domaine est écrite en anglais, et vous la lirez : chaque terme est donc
donné dans les deux langues. Le terme français de la deuxième colonne est celui que le cours
emploie du début à la fin, et c'est aussi celui que j'attends dans vos rapports. L'anglais
figure en italique entre parenthèses à la première occurrence de chaque semaine, puis
disparaît.

La troisième colonne demande un mot d'explication, parce qu'elle est la plus utile des
quatre au moment de rédiger. Elle ne liste pas des fautes : elle liste des formes
**attestées** qu'il faut tout de même éviter ici, et les raisons sont de trois sortes. Un
anglicisme là où le français a un mot. Une traduction qui déplace le sens, comme
« stratégie » pour *policy*, qui suggère un plan alors qu'une politique est une règle de
décision instantanée. Et surtout, le cas le plus fréquent, un terme **déjà réservé** par une
autre semaine à un autre objet : la mention entre parenthèses dit alors laquelle. Quand la
case est vide, c'est qu'il n'y a rien à écarter.

La quatrième colonne donne la semaine où le terme est introduit. Elle sert à deux choses :
retrouver la section qui définit un mot, et juger de quel outillage une phrase a besoin.

> [!TIP]
 **Comment chercher ici.** Le glossaire est une seule table, rangée par ordre alphabétique
 du terme **anglais**, parce que c'est presque toujours l'anglais que vous avez sous les yeux
 quand vous cherchez. Pour aller d'un terme français à son entrée, utilisez la fonction de
 recherche de votre navigateur : la table complète est sur cette page, et elle inclut les
 formes à éviter, donc même une recherche sur un terme que le cours refuse vous amènera à la
 bonne ligne.

---

## Cinq distinctions qui coûtent cher dans un rapport

Cinq paires de termes reviennent si souvent, et se confondent si facilement, qu'elles
méritent plus qu'une case de tableau. Chacune a été tranchée une fois pour tout le cours.

**« Hors ligne » n'est pas « hors politique ».** Les deux ne sont pas synonymes, et ils ne
sont même pas de même nature : « hors politique » qualifie un **algorithme**, qui sait
apprendre d'une transition dont l'action vient d'une autre politique que la sienne ; « hors
ligne » décrit un **problème**, dans lequel aucune interaction n'aura lieu pendant
l'entraînement. Toute méthode hors ligne est hors politique ; presque aucune méthode hors
politique n'est hors ligne, puisqu'elles continuent presque toutes de collecter.

**« Sûreté » n'est pas « sécurité ».** L'anglais dispose de deux mots et les intervertit
parfois ; le français a une division nette et le cours la garde. La **sûreté** concerne ce
qui peut mal tourner sans que personne ne le veuille, et c'est tout le sujet de la fin de la
semaine 14. La **sécurité** concerne ce qui tourne mal parce que quelqu'un le veut, et le
cours la met explicitement hors de son champ.

**Le mot « écrêtage » seul appartient à la semaine 10.** Cinq opérations différentes
s'appellent *clipping* en anglais, et le cours les écrit **en entier** chaque fois :
écrêtage de la récompense, écrêtage du gradient, écrêtage de l'action, écrêtage du bruit.
Le mot nu désigne uniquement l'écrêtage du rapport de politiques, qui est l'objet central de
la semaine 10. Et une sixième opération n'est pas un écrêtage du tout : le **plafonnement**
de la récompense, en semaine 14, empêche la récompense de monter au-delà d'un seuil. L'un
remet un signal à l'échelle, l'autre change l'objectif, qui cesse de maximiser pour se
contenter d'un niveau suffisant.

**Trois problèmes de distribution, trois noms, et aucun raccourci.** La
**non-stationnarité** de la semaine 12 est un environnement qui bouge pendant que vous
apprenez, parce que l'adversaire apprend aussi. Le **décalage de distribution** de la
semaine 13 est une politique apprise qui quitte la région couverte par un jeu de données
figé, et c'est un problème interne à l'entraînement. Le **changement de distribution entre
entraînement et déploiement** de la semaine 14 est un troisième objet, écrit en entier et
jamais abrégé : un système ajusté sur une distribution et mis en service sur une autre, dont
la moitié la plus désagréable est qu'il peut continuer de se croire bon.

**« Erreur de généralisation », « écart de généralisation », « erreur
d'extrapolation ».** Les trois sont des quantités différentes, et la ressemblance des noms
est un piège. L'**erreur de généralisation** est l'erreur sur des données non vues, notion de
la semaine 2 ; l'**écart de généralisation** est la différence entre cette erreur et celle
mesurée sur les données d'entraînement ; l'**erreur d'extrapolation** de la semaine 13 est
tout autre chose, c'est l'erreur d'une valeur estimée pour une action que le jeu de données
ne contient pas, et elle grandit au lieu de se diluer. Un rapport qui emploie le premier
terme pour le troisième décrit un phénomène qui se corrige par plus de données, là où il
s'agit précisément de celui qui ne se corrige pas ainsi.

---

## Le glossaire

Quatre cent soixante-neuf entrées, par ordre alphabétique du terme anglais.

| Anglais | Terme retenu en français | Formes à éviter | Semaine |
| --- | --- | --- | --- |
| ablation study | étude d'ablation | étude par retrait | 6 |
| abstract rewards | récompenses abstraites | récompenses implicites, récompenses de haut niveau | 14 |
| accident | accident | incident (trop faible), bogue (c'est exactement ce que ce n'est pas), défaillance | 14 |
| ACKTR | ACKTR, acteur-critique à région de confiance factorisée de Kronecker | ACKTR en prose sans l'avoir développé | 10 |
| action clipping | écrêtage de l'action | troncature de l'action, écrêtage (seul : réservé à la semaine 10) | 9 |
| action repeat | répétition d'action | saut d'image (sens différent, semaine 5), maintien d'action | 13 |
| action sampling | échantillonnage de l'action | sampling d'action | 3 |
| action selector | sélecteur d'actions | sélecteur d'action | 6 |
| action space | espace d'actions |  | 1 |
| action value, Q-value | valeur d'une action | Q-valeur, valeur-Q | 4 |
| activation function | fonction d'activation | fonction de transfert | 2 |
| actor | acteur | agent de politique | 8 |
| actor-critic | acteur-critique | acteur-évaluateur, actor-critic | 8 |
| admissible commands | commandes admissibles | commandes valides, commandes autorisées, actions légales (réservé au sens du plateau de jeu, semaine 12) | 15 |
| advantage | avantage |  | 6 |
| advantage actor-critic, A2C | acteur-critique à avantage | A2C en prose sans l'avoir développé | 8 |
| advantage normalisation | normalisation de l'avantage | centrage de l'avantage (incomplet : on divise aussi) | 10 |
| adversarial reward function | récompense adverse | récompense antagoniste, récompense contradictoire | 14 |
| agent | agent |  | 1 |
| agent index | indice d'agent | numéro d'agent, identifiant d'agent (c'est la clé du code, pas le symbole) | 12 |
| alignment | alignement |  | 14 |
| all-actions method | méthode toutes actions | méthode sur toutes les actions | 8 |
| AlphaGo Zero | AlphaGo Zero | alphago zero, AlphaGo (méthode différente et antérieure) | 12 |
| analytic gradient | gradient analytique | gradient exact (vague), gradient fermé | 13 |
| anchoring | ancrage | fixation, contrainte seule | 13 |
| asynchronous advantage actor-critic, A3C | acteur-critique à avantage asynchrone | A3C en prose sans l'avoir développé | 8 |
| AUROC | aire sous la courbe caractéristique | aire sous la courbe (ambigu), AUROC en prose sans l'avoir développée | 14 |
| autodidactic iteration, ADI | itération autodidacte (ADI) | ADI en prose sans l'avoir développé, auto-apprentissage (vague), itération autodidactique | 15 |
| automatic differentiation | différentiation automatique | dérivation automatique | 2 |
| averagers | moyenneurs (*averagers*) | moyenneurs seul en prose | 5 |
| backpropagation | rétropropagation | backprop | 2 |
| backtest | simulation historique (*backtest*) | rétro-test, backtest seul en prose | 7 |
| backtracking line search | recherche linéaire par rebroussement | recherche par retour arrière, backtracking | 10 |
| backup diagram | diagramme de sauvegarde | diagramme de retour | 4 |
| backup of value | remontée de la valeur | sauvegarde (réservée au diagramme de la semaine 4 et à l'enregistrement d'un point de contrôle), rétropropagation (réservée au sens de la semaine 2) | 12 |
| Baird's counterexample | contre-exemple de Baird | exemple de Baird | 5 |
| baseline | référence (*baseline*) | base, version de référence (réservée au sens de la semaine 7) | 8 |
| baseline version, reference run | version de référence | référence (réservée au sens de la semaine 8) | 7 |
| batch, minibatch | lot | batch, paquet | 2 |
| batched inference | inférence par lot | inférence groupée | 7 |
| behavior policy | politique de comportement | politique de collecte (acceptée en glose), politique source | 13 |
| behavioral cloning | clonage de comportement | imitation seule, apprentissage par imitation (famille plus large) | 13 |
| Bellman equation | équation de Bellman |  | 4 |
| Bellman optimality equation | équation d'optimalité de Bellman | équation de Bellman optimale | 4 |
| Bellman unrolling | déroulement de l'équation de Bellman | déroulage, expansion de Bellman | 6 |
| Bellman update | mise à jour de Bellman | approximation de Bellman | 4 |
| benchmark (suite of tasks) | jeu de référence | banc d'essai (réservé au sens de la semaine 7), référentiel, benchmark | 15 |
| bid-ask spread | écart achat-vente (*spread*) | écart, spread | 7 |
| bootstrapping | amorçage |  | 4 |
| branching factor | facteur de branchement | facteur d'embranchement, degré de ramification | 12 |
| brokerage commission | commission de courtage | frais, commission seule | 7 |
| browser automation | automatisation du navigateur | automatisation web (ambigu avec l'extraction de données), pilotage de navigateur (accepté en glose) | 15 |
| buy-and-hold | achat-conservation (*buy-and-hold*) | acheter et garder, buy-and-hold | 7 |
| candlestick chart | graphique en chandeliers | graphique en bougies | 7 |
| ceiling row | ligne plafond | borne supérieure (vague), oracle | 13 |
| chain rule | règle de dérivation en chaîne | règle de la chaîne | 2 |
| channel | canal | plan, couche de couleur | 2 |
| checkpoint | point de contrôle | sauvegarde (voir la note sur « remontée »), snapshot | 3 |
| checkpoint tournament | tournoi entre points de contrôle | classement des modèles (vague) | 12 |
| cliff walking | marche au bord de la falaise | cliff walking | 4 |
| clipped double-Q | double Q écrêté | double Q borné, Q écrêté | 9 |
| clipped objective | objectif écrêté | objectif tronqué, objectif borné | 10 |
| clipping | écrêtage | rognage, clipping | 10 |
| collaborative setting | cadre collaboratif | cadre coopératif (accepté en glose, non retenu comme terme) | 12 |
| combinatorial optimization | optimisation combinatoire | optimisation discrète (terme voisin, voir l'entrée *discrete optimization*), optimisation ensembliste | 15 |
| comparison of continuous-control methods | comparaison des méthodes de contrôle continu | banc d'essai (réservé au sens de la semaine 7) | 10 |
| comparison of exploration methods | comparaison des méthodes d'exploration | banc d'essai (réservé au sens de la semaine 7) | 11 |
| competitive setting | cadre compétitif | cadre concurrentiel | 12 |
| complexity term | terme de complexité | terme de régularisation (vague), terme KL seul | 13 |
| computation graph | graphe de calcul | graphe computationnel | 2 |
| confidence interval | intervalle de confiance | barre d'erreur (sens différent) | 7 |
| conjugate gradient and line search | méthode du gradient conjugué et recherche linéaire | gradient conjugué seul quand la recherche linéaire est aussi en jeu | 10 |
| Connect 4 | Puissance 4 | Connect 4, quatre à la suite | 12 |
| conservative penalty | pénalité conservatrice | pénalité conservative (anglicisme), pénalité prudente | 13 |
| continuous action space | espace d'actions continu | espace d'action continue, espace continu | 9 |
| convolution kernel, filter | noyau de convolution | filtre, kernel | 2 |
| convolution layer | couche de convolution | couche convolutive | 2 |
| coordinated actions | séquence d'actions coordonnées | suite d'actions, enchaînement | 11 |
| cost-to-go | coût pour atteindre | coût restant | 5 |
| count-based methods | méthodes fondées sur le comptage | méthodes par comptage, comptage seul | 11 |
| counterfactual query | requête contrefactuelle | question hypothétique (trop faible), simulation | 13 |
| credit assignment | attribution du mérite | affectation du crédit | 8 |
| critic | critique | évaluateur | 8 |
| cross-entropy loss | perte d'entropie croisée | perte CE | 3 |
| cross-entropy method, CEM | méthode d'entropie croisée | entropie croisée (seule), CEM en prose | 3 |
| cubelet | cube élémentaire | arête (réservée à l'arête d'un arbre de recherche, semaine 12), cubie, petit cube | 15 |
| cumulative profit curve | courbe de profit cumulé | courbe de gain | 7 |
| curiosity-driven exploration | exploration par curiosité | curiosité seule, motivation intrinsèque | 11 |
| custom environment | environnement sur mesure | environnement personnalisé | 7 |
| data coverage | couverture des données | support des données (réservé à « contrainte de support »), étendue | 13 |
| data leakage | fuite d'information | fuite de données | 7 |
| data parallelism | parallélisme de données | parallélisation des données | 8 |
| deadly triad | triade fatale | triade mortelle | 5 |
| decision map | carte de décision | arbre de décision (objet différent en apprentissage supervisé), organigramme, carte mentale | 15 |
| deep deterministic policy gradient, DDPG | gradient de politique déterministe profond (DDPG) | DDPG en prose sans l'avoir développé | 9 |
| deep learning | apprentissage profond | apprentissage en profondeur | 2 |
| deep Q-network, DQN | réseau Q profond | réseau-Q, DQN profond | 5 |
| delayed policy updates | mise à jour retardée de la politique | politique retardée | 9 |
| density model | modèle de densité | modèle de probabilité (vague), densité seule | 11 |
| detaching from the graph | détachement du graphe | détachement | 2 |
| deterministic policy gradient | gradient de politique déterministe | gradient déterministe | 9 |
| device | périphérique de calcul | appareil, dispositif | 2 |
| directed exploration | exploration dirigée | exploration guidée, exploration ciblée | 11 |
| Dirichlet concentration | concentration de Dirichlet | paramètre alpha seul (quatrième sens d'alpha : voir `notation.md`) | 12 |
| Dirichlet noise at the root | bruit de Dirichlet à la racine | bruit de racine seul, bruit d'exploration (réservé au sens de la semaine 9) | 12 |
| discount factor | facteur d'actualisation | taux d'escompte | 1 |
| discounted visitation frequency | fréquence de visite actualisée des états | fréquence d'occupation, distribution d'états (réservée au sens de la semaine 8) | 10 |
| discrete optimization | optimisation discrète | optimisation combinatoire (terme voisin, voir l'entrée *combinatorial optimization*), optimisation entière (sous-cas) | 15 |
| discretization, binning | discrétisation de l'espace d'états | binning, mise en classes | 4 |
| distributional Bellman equation | équation de Bellman distributionnelle | Bellman distributionnel | 6 |
| distributional change (training to deployment) | changement de distribution entre entraînement et déploiement | décalage de distribution (réservé au sens de la semaine 13), dérive de distribution (réservée au sens de la semaine 12), et **toute abréviation** | 14 |
| distributional RL | apprentissage par renforcement distributionnel | RL distributionnel | 6 |
| distributional shift | décalage de distribution | glissement de distribution, dérive de distribution (réservée au sens de la semaine 12) | 13 |
| DOM tree | arbre DOM | arbre du document, DOM employé seul comme nom, arborescence de la page | 15 |
| double descent | double descente |  | 2 |
| double DQN | double DQN | DQN double, DDQN en prose | 6 |
| drawbacks of epsilon-greedy | limites de la méthode epsilon-gloutonne | défauts de l'exploration (trop vague) | 11 |
| drawdown | repli maximal (*drawdown*) | perte maximale, drawdown | 7 |
| dropout | abandon de neurones (*dropout*) | décrochage, dropout | 2 |
| dueling architecture | architecture duale | réseau duel, architecture duelle | 6 |
| dynamic programming | programmation dynamique |  | 4 |
| dynamics network | réseau de dynamique | modèle de transition (vague), réseau dynamique (adjectif : contresens) | 12 |
| early stopping | arrêt précoce | arrêt anticipé | 2 |
| early termination on a healthiness check | terminaison précoce par contrôle de santé | arrêt sanitaire, troncature (réservé au sens Gymnasium de la semaine 1) | 10 |
| edge | arête | arc, branche | 12 |
| effective exploration | exploration efficace | bonne exploration, exploration suffisante | 11 |
| egocentric observation | observation égocentrée | observation égocentrique, observation centrée sur l'agent (acceptée en glose) | 12 |
| eligibility vector | vecteur d'éligibilité | vecteur d'admissibilité | 8 |
| elite episodes | épisodes élites | meilleurs épisodes | 3 |
| elite threshold | seuil des élites | frontière de récompense (réservée au seuil de résolution) | 3 |
| emergent behaviour | comportement émergent | émergence seule, auto-organisation | 12 |
| empowerment | capacité d'influence | autonomisation, empouvoirement, pouvoir d'agir | 14 |
| encoder | encodeur | réseau de représentation (réservé au sens de la semaine 12), codeur | 13 |
| entropy bonus | prime d'entropie | bonus d'entropie, régularisation d'entropie | 8 |
| entropy coefficient | coefficient d'entropie | poids de l'entropie | 8 |
| entropy regularization | régularisation par l'entropie | prime d'entropie (réservée au sens de la semaine 8) | 10 |
| environment | environnement | milieu | 1 |
| episode | épisode | partie, essai | 1 |
| episode segment | segment d'épisode | tronçon d'épisode (« tronçon » est réservé au sens de la semaine 13), extrait, clip | 14 |
| epoch | époque | cycle | 2 |
| epsilon-greedy | méthode epsilon-gloutonne | epsilon-greedy, politique ε-avide | 4 |
| evaluation gate | porte d'évaluation | seuil de promotion (accepté en glose, non retenu comme terme) | 12 |
| evaluation (search phase) | évaluation | estimation (réservée au sens statistique) | 12 |
| expected update | mise à jour en espérance | mise à jour espérée | 4 |
| experience replay | rejeu d'expérience | mémoire de relecture | 5 |
| experience source | source d'expérience | générateur d'expérience | 6 |
| exploding gradient | gradient explosif | gradient qui explose | 2 |
| exploration bonus | prime d'exploration | bonus | 11 |
| exploration constant | constante d'exploration | constante PUCT sans l'avoir développée | 12 |
| exploration/exploitation | dilemme exploration-exploitation |  | 1 |
| exploration noise | exploration par bruit ajouté à l'action | bruit d'exploration seul (ambigu avec le bruit de lissage) | 9 |
| extrapolation error | erreur d'extrapolation | erreur de généralisation (sens différent, voir l'entrée *generalization error*) | 13 |
| extrinsic reward | récompense extrinsèque | récompense externe, récompense de l'environnement (acceptée en glose, pas comme terme) | 11 |
| f-divergence | f-divergence | divergence généralisée, divergence f (ordre inversé) | 13 |
| factorized Gaussian noise | bruit gaussien factorisé | bruit gaussien factorisable | 6 |
| failed reproduction | échec de reproduction | non-reproductibilité (c'est la propriété, pas l'événement), résultat non reproduit, échec de réplication | 15 |
| feature map | carte de caractéristiques | carte d'activation | 2 |
| feedback loop | boucle de rétroaction | boucle de retour, cercle vicieux (expression du cours, pas le terme) | 14 |
| filtering distribution | loi de filtrage | loi de lissage (c'est l'objet que la semaine 13 refuse), postérieure seule | 13 |
| financial instrument | instrument financier | titre, valeur | 7 |
| fine-tuning | affinage | affinement, ajustement fin, réglage fin | 14 |
| first-last transition | transition premier-dernier | transition début-fin | 6 |
| Fisher information | information de Fisher | matrice de Fisher seule quand c'est la métrique qui est en jeu | 10 |
| flattening | aplatissement | mise à plat | 2 |
| forward method | méthode forward | méthode avant | 2 |
| forward propagation | propagation avant | passe avant | 2 |
| frame skipping | saut de trames | saut d'images, frame skip | 5 |
| frame stacking | empilement de trames | empilement d'images | 5 |
| frames per second, FPS | trames par seconde (*FPS*) | images par seconde, FPS seul en prose | 7 |
| free nats | nats libres | nats gratuits, bits libres (l'unité n'est pas la même) | 13 |
| frozen random target network | réseau de référence figé | réseau cible (réservé au sens de la semaine 5), réseau gelé | 11 |
| Gaussian policy | politique gaussienne | politique normale | 9 |
| generalization | généralisation |  | 2 |
| generalization error | erreur de généralisation | erreur de test, écart de généralisation | 2 et 13 |
| generalization gap | écart de généralisation | fossé de généralisation | 2 |
| generalized advantage estimation, GAE | estimation généralisée de l'avantage (GAE) | GAE en prose sans l'avoir développé, avantage généralisé seul | 10 |
| generalized policy iteration, GPI | itération généralisée de politique | GPI en prose | 4 |
| generative adversarial network | réseau antagoniste génératif | réseau génératif adversaire | 2 |
| generator and discriminator | générateur et discriminateur |  | 2 |
| global policy variance | variance globale de la politique | variance fixe (elle est apprise, pas fixée) | 10 |
| goal discovery vs task solving | découverte du but contre résolution de la tâche | réussite seule | 11 |
| God's number | nombre de Dieu | nombre divin, borne de Dieu, et surtout **le terme employé sans sa métrique** (voir les entrées *half-turn metric* et *quarter-turn metric*) | 15 |
| Goodhart's law | loi de Goodhart | effet Goodhart, principe de Goodhart | 14 |
| gradient | gradient |  | 2 |
| gradient accumulation | accumulation des gradients | cumul des gradients | 2 |
| gradient clipping | écrêtage du gradient | rognage du gradient, écrêtage (seul : réservé à la semaine 10) | 8 |
| gradient parallelism | parallélisme de gradients | parallélisation des gradients | 8 |
| grayscale | niveaux de gris | échelle de gris, grayscale | 5 |
| greedy | glouton | avide | 4 |
| greedy policy | politique gloutonne | politique avide, politique gourmande | 4 |
| grid world | monde en grille | grille, gridworld | 3 |
| group-relative | relatif au groupe | relatif à l'équipe, relatif au camp | 12 |
| half-turn metric | métrique des demi-tours | métrique des faces, métrique des tours de face (acceptée en glose), « métrique » employée seule | 15 |
| hard-exploration games | jeux à exploration difficile | jeux difficiles (vague) | 11 |
| headless (browser) | sans interface | sans tête, headless, en mode invisible | 15 |
| Hellinger distance | distance de Hellinger | divergence de Hellinger (c'est bien une distance), métrique de Hellinger | 14 |
| hidden layer | couche cachée | couche intermédiaire | 2 |
| hidden state | état caché | couche cachée (objet différent, semaine 2), état latent (objet différent, semaine 13), état interne | 12 |
| Huber loss | perte de Huber | perte Huber, Huber loss | 5 |
| human demonstrations | démonstrations humaines | préférences humaines (objet différent, semaine 14 : une démonstration ne contient aucun exemple négatif), clonage de comportement (c'est la méthode, pas la donnée, semaine 13), exemples humains | 15 |
| human feedback | rétroaction humaine | retour humain, feedback humain | 14 |
| human preferences | préférences humaines | choix humains, goûts humains | 14 |
| hyperbolic tangent, tanh | tangente hyperbolique |  | 2 |
| imagination horizon | horizon d'imagination | horizon de déroulement, horizon seul | 13 |
| imagined reward | récompense prédite | récompense imaginée (acceptée en glose), récompense reçue (contresens) | 13 |
| imagined trajectory | trajectoire imaginée | trajectoire simulée (vague), déploiement imaginé (« déploiement » est réservé au sens de la semaine 1) | 13 |
| importance sampling | échantillonnage préférentiel | échantillonnage d'importance | 3 |
| importance-sampling weights | poids de correction du biais | poids d'importance | 6 |
| in-place operation | opération en place | opération sur place | 2 |
| in-place update | mise à jour sur place | mise à jour en place (réservée aux tenseurs, semaine 2) | 4 |
| in-sample / out-of-sample | dans l'échantillon / hors échantillon | en échantillon, out-of-sample | 7 |
| incoherent collecting policy | incohérence de la politique de collecte | instabilité de la politique (réservée au sens de la semaine 10) | 11 |
| inductive bias | biais inductif |  | 2 |
| integral probability metric | métrique de probabilité intégrale | distance intégrale, IPM en prose sans l'avoir développée | 13 |
| interactive fiction | fiction interactive | jeu d'aventure textuel (accepté en glose), jeu de rôle textuel, fiction | 15 |
| intermediate reward | récompense intermédiaire | récompense partielle, récompense de progression (acceptée en glose), façonnage de la récompense (opération différente, semaine 14) | 15 |
| interpolating the training data | interpolation des données d'entraînement |  | 2 |
| intrinsic reward | récompense intrinsèque | récompense interne, récompense auxiliaire | 11 |
| Jensen-Shannon divergence | divergence de Jensen-Shannon | distance de Jensen-Shannon (ce n'en est pas une), JSD en prose sans l'avoir développée | 14 |
| joint action | action jointe | action conjointe, action collective | 12 |
| K-FAC | approximation de la courbure par factorisation de Kronecker (K-FAC) | K-FAC en prose sans l'avoir développé | 10 |
| KL constraint | contrainte sur la divergence KL | contrainte de divergence maximale (c'est une moyenne) | 10 |
| Kullback-Leibler divergence | divergence de Kullback-Leibler | distance KL | 3 |
| labelling | étiquetage | annotation (ce mot désigne la méthode par action que la semaine 14 refuse), labellisation | 14 |
| latent dynamics | dynamique latente | dynamique cachée, dynamique interne | 13 |
| latent state | état latent | état caché (objet différent, semaine 12), état interne, état compressé | 13 |
| leaf | feuille | nœud terminal (ambigu avec « état terminal »), tenseur feuille (autre sens, semaine 2) | 12 |
| leaf tensor | tenseur feuille | tenseur terminal | 2 |
| limitations of the cross-entropy method | limites de la méthode d'entropie croisée |  | 3 |
| linear layer, fully connected layer | couche linéaire | couche dense | 2 |
| locality | principe de localité | localité | 2 |
| locomotion environments | environnements de locomotion | environnements de marche, environnements robotiques (réservé à la semaine 9) | 10 |
| logits | sorties brutes (*logits*) | logits seul en prose | 3 |
| loss function | fonction de perte | fonction d'erreur | 2 |
| market impact | impact de marché | effet de marché | 7 |
| Markov decision process | processus de décision markovien | PDM, MDP | 1 |
| Markov process | processus de Markov | chaîne de Markov | 1 |
| Markov property | propriété de Markov | hypothèse de Markov | 1 |
| Markov reward process | processus de Markov avec récompense |  | 1 |
| maximization bias | biais de maximisation | biais du maximum | 6 |
| mean squared value error | erreur quadratique moyenne sur les valeurs |  | 5 |
| minimax | minimax | min-max, minmax, méthode du minimum-maximum | 12 |
| misweighting | erreur de pondération | mauvaise pondération (acceptée en glose), déséquilibre | 14 |
| model-based | méthode avec modèle | basée sur un modèle, model-based | 3 |
| model exploitation | exploitation du modèle | détournement du modèle, piratage du modèle (réservé au sens de la semaine 14) | 13 |
| model-free | méthode sans modèle | sans-modèle, model-free | 3 |
| model-predictive control | commande prédictive | contrôle prédictif, MPC en prose sans l'avoir développé | 13 |
| module | module | bloc | 2 |
| Monte Carlo method | méthode de Monte-Carlo | Monte-Carlo seul, MC | 3 |
| Monte Carlo tree search, MCTS | recherche arborescente de Monte-Carlo (MCTS) | MCTS en prose sans l'avoir développé, arbre de Monte-Carlo, recherche de Monte-Carlo (seule : elle désigne aussi l'estimation par échantillonnage) | 12 |
| MountainCar | MountainCar | la voiture dans la vallée (en prose seulement, jamais comme nom de tâche) | 11 |
| multi-agent reinforcement learning, MARL | apprentissage par renforcement multi-agent (MARL) | MARL en prose sans l'avoir développé, apprentissage multi-agents (avec un s) | 12 |
| multi-armed bandit | bandit manchot | bandit à plusieurs bras | 1 |
| multilayer perceptron | perceptron multicouche | MLP | 2 |
| multiple epochs over one trajectory | époques multiples sur une même trajectoire | passes multiples, itérations sur le lot | 10 |
| multiprocessing | multitraitement | multiprocessus, multiprocessing | 7 |
| MuZero | MuZero | Muzero, MuZéro | 12 |
| n-step DQN | DQN à n étapes | DQN n-step, DQN à n pas | 6 |
| natural policy gradient | gradient naturel de politique | gradient naturel seul (ambigu hors du contexte des politiques) | 10 |
| negative log likelihood | log-vraisemblance négative | NLL | 3 |
| negative side effects | effets secondaires négatifs | dommages collatéraux, effets de bord (anglicisme informatique) | 14 |
| neural network | réseau de neurones | réseau neuronal | 2 |
| node | nœud | sommet | 12 |
| node expansion | expansion d'un nœud | développement d'un nœud, extension | 12 |
| noise clipping | écrêtage du bruit | bornage du bruit, écrêtage (seul : réservé à la semaine 10) | 9 |
| noise injection | injection de bruit | ajout de bruit | 2 |
| noise sampling frequency | fréquence d'échantillonnage du bruit | fréquence de bruit, rafraîchissement du bruit | 11 |
| noisy networks | réseaux bruités | réseaux bruyants, noisy nets | 6 |
| non-stationarity | non-stationnarité | instabilité (réservée au sens de la semaine 10), dérive de l'environnement | 12 |
| numerical preference | préférence numérique | score, poids d'action | 8 |
| numerical stability | stabilité numérique |  | 2 |
| objective function | fonction objectif | fonction de coût | 2 |
| observation | observation | perception | 1 |
| observation model | modèle d'observation | décodeur (accepté en glose pour sa partie générative seule) | 13 |
| observation space | espace d'observations |  | 1 |
| offline RL | apprentissage par renforcement hors ligne | RL batch, apprentissage par lots, en/hors ligne pour sur/hors politique | 13 |
| on-policy distribution | distribution sur politique | distribution de la politique | 5 |
| on-policy / off-policy | sur politique / hors politique | en/hors ligne | 3 |
| one-hot encoding | codage one-hot | codage à chaud, encodage one-hot | 3 |
| ontological misspecification | erreur d'ontologie | erreur ontologique, mauvaise définition (vague) | 14 |
| open, high, low, close | ouverture, haut, bas, clôture | OHLC en prose | 7 |
| optimal policy | politique optimale |  | 4 |
| optimization power | puissance d'optimisation | capacité d'optimisation (« capacité » est prise par la capacité du modèle, qui est un des quatre axes), force d'optimisation | 14 |
| optimizer | optimiseur | optimisateur | 2 |
| Ornstein-Uhlenbeck process | processus d'Ornstein-Uhlenbeck | bruit OU, processus OU | 9 |
| out-of-distribution action | action hors distribution | action inconnue, action non vue (vague) | 13 |
| overfitting | surapprentissage | surajustement | 2 |
| overparameterization | surparamétrisation |  | 2 |
| padding | remplissage | bourrage, padding | 2 |
| parameter initialization | initialisation des paramètres |  | 2 |
| parameter noise | bruit de paramètres | bruit sur les poids (réservé aux réseaux bruités de la semaine 6) | 11 |
| partially observable MDP, POMDP | PDM partiellement observable | MDP partiellement observable, POMDP | 5 |
| partially observed goals | buts partiellement observés | objectifs cachés, buts partiels | 14 |
| patience criterion | critère de patience |  | 2 |
| percentage point | point de pourcentage | point de base (sens différent) | 7 |
| percentile filtering | percentile de sélection des épisodes | centile, filtrage percentile | 3 |
| performance collapse | effondrement de la performance | écroulement, crash de la politique | 10 |
| pessimism | pessimisme | prudence (trop faible), aversion au risque (notion différente) | 13 |
| phase transition | transition de phase | bascule (acceptée en prose), saut, point de rupture | 14 |
| physics simulator comparison | comparaison des simulateurs physiques | comparaison des moteurs (ambigu) | 10 |
| planning horizon | horizon de planification | profondeur de planification, horizon seul | 13 |
| policy | politique | stratégie | 1 |
| policy-based | méthode fondée sur la politique | basée sur la politique | 3 |
| policy constraint | contrainte de politique | contrainte sur la divergence KL (c'est un cas particulier, semaine 10) | 13 |
| policy evaluation | évaluation de politique |  | 4 |
| policy gradient theorem | théorème du gradient de politique | théorème du gradient | 8 |
| policy head | tête de politique | sortie de politique, branche de politique | 8 |
| policy improvement | amélioration de politique |  | 4 |
| policy improvement theorem | théorème d'amélioration de politique |  | 4 |
| policy iteration | itération sur la politique | itération de politique | 4 |
| policy network | politique représentée par un réseau de neurones | réseau de politique | 3 |
| policy penalty | pénalité de politique | pénalité seule, régularisation de politique | 13 |
| policy ratio | rapport entre la nouvelle et l'ancienne politique | ratio de politiques, rapport de vraisemblance | 10 |
| policy update instability | instabilité de la mise à jour de politique | instabilité de l'apprentissage (trop vague) | 10 |
| pooling | agrégation | mise en commun, pooling | 2 |
| position | position | avoir, portefeuille | 7 |
| predator-prey | prédateur-proie | proie-prédateur, chasseur-gibier | 12 |
| prediction-based methods | méthodes fondées sur la prédiction | méthodes par erreur de prédiction, méthodes de surprise | 11 |
| prediction network | réseau de prédiction | prédicteur (réservé au sens de la semaine 11) | 12 |
| prediction problem | problème de prédiction |  | 4 |
| preference label | étiquette de préférence | annotation de préférence (« annotation » désigne la méthode par action que la semaine refuse), note | 14 |
| preference model | modèle de préférence | modèle de choix, modèle comparatif | 14 |
| price bar, OHLC bar | barre de prix (*bar*) | chandelier (réservé au graphique), bougie | 7 |
| price slippage | dérapage des prix (*slippage*) | glissement, slippage | 7 |
| prior probability | probabilité a priori | a priori employé seul comme nom, prior | 12 |
| prioritized replay buffer | tampon de rejeu priorisé | tampon priorisé seul en première occurrence | 6 |
| profiling | profilage | profiling | 7 |
| proximal policy optimization, PPO | optimisation proximale de politique (PPO) | PPO en prose sans l'avoir développé | 10 |
| proxy reward | récompense de substitution | récompense substitut, récompense de remplacement, objectif de substitution (c'est un *objectif*, semaine 10) | 14 |
| pseudo-count | pseudo-comptage | comptage approché, comptage estimé | 11 |
| Q-iteration | itération sur Q | Q-itération | 4 |
| Q-learning | Q-learning | apprentissage Q | 4 |
| Q-learning update | mise à jour de Q-learning |  | 4 |
| quarter-turn metric | métrique des quarts de tour | métrique des quarts, métrique à douze actions (décrit l'implémentation et non la métrique) | 15 |
| random network distillation, RND | distillation de réseau aléatoire (RND) | **distillation de politique** (méthode différente), RND en prose sans l'avoir développé | 11 |
| random seed | graine aléatoire | germe, graine seule | 7 |
| reconstruction term | terme de reconstruction | terme de vraisemblance (vague) | 13 |
| rectified linear unit, ReLU | unité linéaire rectifiée | ReLU, redresseur | 2 |
| recurrent state-space model | modèle à espace d'états récurrent | modèle récurrent seul (vague), RSSM en prose sans l'avoir développé | 13 |
| reinforcement learning | apprentissage par renforcement |  | 1 |
| relative price representation | représentation relative des prix | prix normalisés | 7 |
| reparameterization trick | reparamétrisation | astuce de reparamétrage | 10 |
| replay buffer | tampon de rejeu | mémoire tampon | 5 |
| representation network | réseau de représentation | encodeur (réservé aux architectures des semaines 2 et 13) | 12 |
| results do not transfer | non-transférabilité des résultats | généralisation (réservée au sens de l'apprentissage supervisé) | 11 |
| return | retour | rendement, récompense cumulée | 1 |
| reward | récompense | gain | 1 |
| reward boundary | frontière de récompense | seuil de résolution | 1 |
| reward capping | plafonnement de la récompense | écrêtage de la récompense (opération différente, semaine 5), bornage | 14 |
| reward clipping | écrêtage de la récompense | rognage de la récompense | 5 |
| reward hacking | piratage de la récompense | détournement | 14 |
| reward model, reward predictor | modèle de récompense, prédicteur de récompense | réseau de récompense (vague), critique (objet différent, semaine 8) | 14 |
| reward modification during training | sensibilité à une récompense modifiée en cours d'entraînement | récompense variable, récompense non stationnaire | 11 |
| reward pretraining | préentraînement de la récompense | pré-apprentissage, récompense gelée (décrit l'effet et non l'opération) | 14 |
| reward shaping | façonnage de la récompense | modelage | 14 |
| rewards-to-go | retours restants | récompenses à venir, rewards-to-go | 8 |
| ridge and lasso regularization | régularisation ridge et lasso |  | 2 |
| River Swim | River Swim | « la rivière » seule, traversée de rivière | 11 |
| rollout | déploiement | déroulé, rollout | 1 |
| rotation-invariant (whole-cube) | invariant par rotation d'ensemble | invariant par rotation (ambigu : une rotation est aussi une action), invariance globale | 15 |
| round trip | aller-retour | cycle achat-vente, round trip | 7 |
| safe exploration | exploration sûre | exploration prudente, exploration sécurisée (« sécurité » est réservée) | 14 |
| safety | sûreté | sécurité (réservée au sens de *security*) | 14 |
| sample efficiency | efficacité d'échantillon | efficience des données | 6 |
| sample priority | priorité d'un échantillon | poids d'un échantillon (réservé à la correction du biais) | 6 |
| sample update | mise à jour par échantillon | mise à jour échantillonnée | 4 |
| Sarsa | Sarsa | SARSA en capitales | 4 |
| scalable oversight | supervision extensible | supervision à grande échelle (décrit l'échelle et non la propriété), surveillance (sens différent, voir §14.13) | 14 |
| scalar tensor | tenseur scalaire | tenseur 0-D | 2 |
| scope misspecification | erreur de portée | erreur de périmètre (acceptée en glose), portée insuffisante | 14 |
| scramble, scramble depth | brouillage, profondeur de brouillage | mélange (réservé au mélange d'un jeu de données), désordre, nombre de coups de mélange | 15 |
| search statistic | statistique de recherche | valeur d'action (réservée au sens des semaines 4 à 10) | 12 |
| second-order optimization | optimisation du second ordre | méthode de Newton (cas particulier) | 10 |
| security | sécurité | sûreté (réservée au sens de *safety*) | 14 |
| segment tree | arbre de segments | arbre segmenté | 6 |
| selection (search phase) | sélection | descente (c'est le mouvement, pas la phase) | 12 |
| self-play | auto-jeu | jeu contre soi | 12 |
| semi-gradient method | méthode semi-gradient | méthode demi-gradient | 5 |
| semi-supervised RL | apprentissage par renforcement semi-supervisé | AR partiellement supervisé, semi-supervision | 14 |
| sentence embedding | plongement de phrase | encodage de phrase (accepté en glose), vectorisation de phrase, embedding | 15 |
| separate actor and critic networks | réseaux séparés pour l'acteur et le critique | réseaux indépendants (ils partagent les données, pas les poids) | 10 |
| separate value heads | têtes de valeur séparées | double critique (réservé au sens de la semaine 9), deux critiques | 11 |
| sequential container | conteneur séquentiel |  | 2 |
| shared body | tronc commun | corps partagé, base commune | 8 |
| shared policy | politique partagée | politique commune, politique unique | 12 |
| short selling | vente à découvert | vente courte, short | 7 |
| sigmoid | fonction sigmoïde | sigmoïde logistique | 2 |
| signal-to-noise ratio | rapport signal sur bruit | rapport signal-bruit, SNR en prose | 6 |
| soft actor-critic, SAC | acteur-critique doux (SAC) | SAC en prose sans l'avoir développé, acteur-critique souple | 10 |
| soft synchronization, soft update | synchronisation douce | mise à jour Polyak, synchronisation souple | 6 |
| sparse reward | récompense parcimonieuse | récompense rare, récompense creuse | 3 |
| spatial downsampling | sous-échantillonnage spatial | décimation | 2 |
| starvation | inanition | famine (mauvais registre) ; « mourir de faim » est accepté en prose | 12 |
| state | état |  | 1 |
| state aggregation | agrégation d'états | regroupement d'états | 5 |
| state hashing | hachage des états | discrétisation de l'espace d'états (réservée au sens de la semaine 4) | 11 |
| state space | espace d'états |  | 1 |
| state space coverage | couverture de l'espace d'états | exploration de l'espace (vague) | 11 |
| state value | valeur d'état | valeur de l'état | 1 |
| static dataset, frozen dataset | jeu de données figé | jeu de données statique (accepté en glose), tampon figé | 13 |
| stationarity | stationnarité |  | 1 |
| step size, learning rate | pas d'apprentissage |  | 4 |
| straight-through gradient | gradient traversant | gradient direct, straight-through en prose | 13 |
| stride | pas de la convolution | foulée, stride | 2 |
| supervised reward learning | apprentissage supervisé de la récompense | apprentissage de récompense (vague), régression de récompense | 14 |
| support constraint | contrainte de support | contrainte de densité (c'est exactement ce qu'elle n'est pas) | 13 |
| surrogate objective | objectif de substitution | objectif substitut, objectif de remplacement | 10 |
| sweep | balayage de l'espace d'états | passage, itération | 4 |
| symmetry breaking | brisure de symétrie | rupture de symétrie | 2 |
| tabular learning | apprentissage tabulaire | apprentissage par tables | 4 |
| tabular Q-learning | Q-learning tabulaire |  | 4 |
| target network | réseau cible | réseau de référence | 5 |
| target policy smoothing | lissage de la politique cible | lissage de la cible seul (ambigu avec le réseau cible) | 9 |
| taxonomy of RL methods | taxonomie des méthodes d'apprentissage par renforcement | classification des méthodes | 3 |
| TD(0), one-step TD | TD(0) | TD zéro | 4 |
| TD error | erreur TD |  | 4 |
| TD residual | résidu temporel | sigma_t (notation de source), delta seul | 10 |
| technical analysis | analyse technique | analyse graphique | 7 |
| temporal-difference learning | apprentissage par différences temporelles | apprentissage TD en prose | 4 |
| tensor | tenseur |  | 2 |
| tensor type, dtype | type d'un tenseur | type de données | 2 |
| terminal state | état terminal | état final | 4 |
| terminated | terminaison (*terminated*) | fini, « done » | 1 |
| timeframe | échelle de temps | horizon seul (voir la note de la semaine 13), unité de temps | 7 |
| train/validation split | partage entraînement-validation | découpage train/test | 7 |
| training loop | boucle d'entraînement | boucle d'apprentissage | 2 |
| training monitoring | suivi de l'entraînement | surveillance | 2 |
| trajectory stitching | recomposition de trajectoires | assemblage de trajectoires (accepté en glose), couture | 13 |
| transition counters | estimation des probabilités de transition | compteurs de transition | 4 |
| transition matrix | matrice de transition |  | 1 |
| translation invariance | invariance par translation | invariance translationnelle | 2 |
| tree pruning | élagage de l'arbre | taille de l'arbre (ambigu avec sa dimension), pruning | 12 |
| trip wires | pièges de détection | fils-pièges, détecteurs (vague), garde-fous | 14 |
| true reward | récompense réelle | vraie récompense, récompense véritable (les deux suggèrent un fait là où c'est une convention, voir §14.16) | 14 |
| truncated | troncature (*truncated*) | interrompu, coupé | 1 |
| trust region | région de confiance | zone de confiance | 10 |
| trust region policy optimization, TRPO | optimisation de politique à région de confiance (TRPO) | TRPO en prose sans l'avoir développé | 10 |
| twin critics | critiques jumeaux | double critique, critiques jumelés | 9 |
| twin delayed deep deterministic policy gradient, TD3 | TD3, gradient de politique déterministe profond jumelé et retardé | TD3 en prose sans l'avoir développé | 9 |
| two-headed network | réseau à deux têtes | réseau bicéphale, réseau à double sortie | 12 |
| undirected exploration | exploration non dirigée | exploration aléatoire (c'est le moyen, pas la propriété) | 11 |
| universal approximator | approximateur universel |  | 2 |
| unlearning | désapprentissage | oubli (réservé au sens de l'oubli catastrophique), régression | 13 |
| unsupervised learning | apprentissage non supervisé | apprentissage sans supervision | 1 |
| value-based | méthode fondée sur la valeur | basée sur la valeur | 3 |
| (value-)function approximation | approximation de la fonction de valeur | approximation fonctionnelle | 5 |
| value head | tête de valeur | sortie de valeur, branche de valeur | 8 |
| value iteration | itération sur la valeur | itération de valeur, value iteration | 4 |
| value overestimation | surestimation des valeurs d'action | survalorisation | 6 |
| vanishing gradient | gradient évanescent | gradient qui disparaît | 2 |
| variational bound | borne variationnelle | borne inférieure variationnelle (acceptée en glose), ELBO en prose | 13 |
| vectorized environments | environnements vectorisés | environnements parallèles | 7 |
| visit count | comptage de visites | compteur d'états, fréquence de visite (réservée au sens de la semaine 10) | 11 |
| volatile population | population volatile | population variable, effectif changeant | 12 |
| volume | volume échangé | volume seul | 7 |
| walk-forward validation | validation glissante (*walk-forward*) | validation avançante | 7 |
| wall clock time | temps d'horloge | temps réel, temps écoulé | 7 |
| web navigation | navigation web | navigation sur le web, surf, navigation internet | 15 |
| web scraping | extraction de données web | moissonnage, grattage, scraping | 15 |
| website testing | test de site web | test web, recette (jargon de projet), validation (sens différent, semaines 7 et 13) | 15 |
| weight decay | dégradation des poids | décroissance des poids | 2 |
| weight sharing | partage des poids | poids partagés | 2 |
| weight vector | vecteur de poids | vecteur de paramètres | 5 |
| windy gridworld | grille ventée | monde venté | 4 |
| wireheading | auto-récompense | manipulation par l'agent de sa propre récompense (glose acceptée, trop longue pour un terme), auto-stimulation | 14 |
| world model | modèle du monde | modèle de l'environnement | 13 |
| wrapper | enveloppe (*wrapper*) | emballeur | 1 |
| Xavier initialization | initialisation de Xavier | initialisation de Glorot | 2 |
| zero-mean advantage constraint | contrainte de moyenne nulle de l'avantage | normalisation de l'avantage | 6 |

{{% comment %}}
Page rédigée en phase 4 à partir de source-assets/glossaire.md (référence de travail, non
modifiée). Trois décisions de publication, plus une quatrième venue de la fusion.

1. COLONNES. Les quatre colonnes de la référence sont publiées. La colonne « À éviter » est
conservée parce qu'elle est la plus utile à qui rédige : elle ne liste pas des fautes mais
des formes attestées réservées ailleurs dans le cours, et sans elle les réservations entre
semaines deviennent invisibles. La colonne de semaine est de la structure de cours, pas une
source : elle est publiable telle quelle et sert de renvoi vers la section qui définit le
terme. Le tiret cadratin que la référence employait pour « rien à éviter » est remplacé par
une case vide (D37), ce qui est annoncé dans l'introduction de la page.

2. ORDRE. Alphabétique sur l'anglais, et non groupé par module : la page est un outil de
consultation, c'est l'anglais que l'étudiant a sous les yeux quand il cherche, et le
groupement par module raconterait une histoire que les pages de module racontent déjà mieux.
Une seule table, donc une seule recherche de navigateur pour tout atteindre, y compris par
une forme à éviter.

3. CE QUI NE VOYAGE PAS. Les notes de fin de la référence de travail sont rédigées en
anglais : c'est de l'outillage de rédaction, et la règle de langue interdit de publier quoi
que ce soit d'anglais que l'étudiant doive lire. Aucune n'est reprise telle quelle. Cinq
portaient une distinction dont l'étudiant profite, et elles sont réécrites en français comme
phrases du cours, en section « Cinq distinctions » : hors ligne contre hors politique, sûreté
contre sécurité, la famille des écrêtages, les trois problèmes de distribution, et les trois
erreurs de généralisation. Les référentiels terminologiques nommés en tête de la référence ne
sont pas publiés (D18).

4. FUSION. Les deux lignes « generalization error » de la référence (semaines 2 et 13) sont
fusionnées en une entrée unique portant « 2 et 13 » et l'union des formes à éviter. Leur
voisinage, qui était l'argument de la seconde ligne dans la référence, n'existe plus après
tri alphabétique : la distinction qu'elles portaient est donc reprise, explicitement, dans
la cinquième des distinctions ci-dessus. D'où 469 entrées publiées pour 470 lignes de
référence.

Sept lignes de la référence renvoyaient à « la ligne précédente » ou « la ligne suivante »,
renvois qui ne survivent pas au tri : ils sont réécrits en nommant l'entrée visée
(extrapolation error, annotation, safety, security, combinatorial / discrete optimization,
God's number et ses deux métriques).
{{% /comment %}}
