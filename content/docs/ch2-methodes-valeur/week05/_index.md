---
title: "Semaine 5 : Réseaux Q profonds (DQN)"
weight: 5
bookCollapseSection: true
---

# Semaine 5 : Réseaux Q profonds (DQN)

Cinquième semaine, et la dette ouverte par la semaine 4 est payée : la table devient une **fonction**, cette fonction est un réseau de neurones, et nous obtenons à la fin un agent qui apprend à jouer à un jeu vidéo en regardant les pixels de l'écran. Le prix de ce remplacement est annoncé dès l'introduction, parce que c'est lui qui fait l'intérêt de la semaine : trois choses qui étaient sûres en semaine 4 cessent de l'être en même temps. Les valeurs des états ne sont plus découplées, la mise à jour descend un gradient qui n'en est pas tout à fait un, et l'ensemble peut, de façon démontrable, **diverger**. Nous verrons la divergence se produire sur trois lignes d'arithmétique, puis les réparations d'ingénierie qui font tenir l'édifice en pratique, et nous finirons par le taux d'échec que cette méthode conserve même bien écrite.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** un réseau Q profond est le Q-learning de la semaine 4, dans lequel la table est devenue une fonction, la cible a été gelée, et les données ont été mises en réserve. Trois modifications, trois justifications, et aucune garantie de convergence au bout.

---
## Description générale

Les sections 5.1 à 5.3 posent le problème, puis l'objectif. La section 5.1 chiffre ce que l'apprentissage tabulaire suppose, et le diagnostic surprend presque tout le monde : ce n'est pas la mémoire qui lâche la première, ce sont les **échantillons**, parce qu'une table doit avoir visité un état pour lui donner une valeur, et l'avoir visité plusieurs fois pour la lui donner correctement. Un écran de jeu vidéo offre plus de \(10^{70\,802}\) combinaisons de pixels, et les quatre nombres réels de CartPole en offrent déjà \(3{,}4 \times 10^{38}\) : la table n'existe pas, et la discrétisation ne supprime pas le problème, elle le déplace vers le choix du découpage. La section 5.2 remplace donc le tableau de \(\lvert\mathcal{S}\rvert\) cases par une forme paramétrée \(\hat v(s,\mathbf{w})\) munie de \(d\) poids, et relit chaque mise à jour de la semaine 4 comme un exemple supervisé \(s \mapsto u\) dont la cible est **non stationnaire**. La section 5.3 écrit l'objectif \(\overline{VE}(\mathbf{w})\) et nomme ce que le cas tabulaire n'avait jamais eu à nommer, la pondération \(\mu(s)\), qui n'est ni un hyperparamètre ni une variable mais une propriété de la façon dont les données ont été produites.

Les sections 5.4 à 5.6 disent le prix, et c'est le cœur théorique de la semaine. La section 5.4 dérive la descente de gradient stochastique sur une valeur, puis montre exactement quel passage de la dérivation cesse d'être valide dès que la cible contient les poids : il manque un morceau du gradient, on l'assume, et ces méthodes s'appellent pour cette raison des **méthodes semi-gradient**. Une seule ligne de PyTorch réalise cette décision, et toute la semaine y renvoie. La section 5.5 refait le même geste pour les valeurs d'action, retrouve la règle de l'état terminal sous une troisième écriture, et justifie l'architecture à **une sortie par action** que la section 5.8 implémentera. La section 5.6 fait alors la démonstration promise : un système à deux états et un seul poids dont la valeur part à l'infini pour tout pas d'apprentissage positif, puis un processus de sept états où tout est favorable, la valeur vraie exactement représentable, et où les poids s'enfuient quand même. Elle nomme les trois ingrédients de la **triade fatale** et audite, ligne par ligne, l'agent que nous n'avons pas encore écrit : il les possède tous les trois.

Les sections 5.7 à 5.9 construisent cet agent et le mesurent. Quatre réparations, et chacune répond à une phrase précise des sections précédentes : un calendrier pour \(\varepsilon\), le **tampon de rejeu**, le **réseau cible**, et l'empilement de quatre trames, qui ne répare pas la triade mais la propriété de Markov. La deuxième de ces réparations est aussi, mot pour mot, le troisième ingrédient de la triade : nous renonçons sciemment à la seule condition connue qui garantisse la stabilité, parce qu'elle coûte trop cher en échantillons. La section 5.8 écrit le code qui compte, enveloppes comprises, parce qu'un agent qui n'apprend rien est plus souvent mal enveloppé que mal dérivé, et la section 5.9 donne les chiffres : de l'ordre d'un million de trames de jeu, une à trois heures de calcul, et **une exécution sur dix qui ne converge pas du tout**. Le laboratoire est **formatif**, la semaine 5 ne porte aucun jalon, mais il demande pour la première fois un **processeur graphique** : un réseau Q profond entier sur CartPole, l'**ablation évaluée** qui retire le réseau cible puis le tampon, une évaluation de Pong à partir de poids fournis, et un volet facultatif sur la perte de Huber.

---
## Mots-clés de la semaine

réseau Q profond · approximation de la fonction de valeur · vecteur de poids · généralisation · erreur quadratique moyenne sur les valeurs · distribution sur politique · agrégation d'états · méthode semi-gradient · détachement du graphe · coût pour atteindre · triade fatale · contre-exemple de Baird · moyenneurs · rejeu d'expérience · tampon de rejeu · réseau cible · empilement de trames · saut de trames · écrêtage de la récompense · niveaux de gris · PDM partiellement observable · enveloppe · perte de Huber · pas d'apprentissage

---
## En prévision de la semaine suivante

Nous repartons de la liste des cinq défauts de la section 5.9, et nous les réparons un par un. Le maximum de la cible surestime les valeurs, et il suffira de séparer le choix de l'action de son évaluation pour corriger ce biais. Le tirage dans le tampon est uniforme, et nous le rendrons proportionnel à ce que chaque transition a encore à nous apprendre. Le réseau apprend une valeur par couple état-action, et nous dédoublerons sa sortie pour qu'il apprenne séparément ce que vaut un état et ce que vaut chaque action dans cet état. L'exploration est pilotée par un calendrier écrit à la main, et nous la ferons produire par le réseau lui-même, en rendant ses poids bruités. La cible est à un pas, et nous la prendrons à plusieurs. Ces cinq réparations sont indépendantes, elles s'empilent, et la semaine 6 se termine en les empilant toutes. Vous y rencontrerez aussi, pour la seule fois du cours, une bibliothèque d'algorithmes spécialisée, non pas pour vous en servir mais pour **l'étudier** : savoir lire le code des autres fait partie du métier.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (D35). Imprimé = PDF − 31 pour LAPAN et PDF − 22 pour SB,
conformément à MAP-lapan.md et MAP-sb.md, comme dans le dossier et les notes de phase 1.
Toutes les pages citées ci-dessous sont des indices PDF.

SEMAINE À DEUX SOURCES, ET LE PARTAGE EST NET : le supplément donne l'ingénierie, le manuel
donne la raison pour laquelle elle est nécessaire. Sections 5.1, 5.7, 5.8, 5.9 reposent sur
LAPAN ch. 6 ; sections 5.2, 5.3, 5.4, 5.5, 5.6 reposent sur SB ch. 9, 10 et 11. La jonction est
écrite pour être invisible : aucune section n'est « la section du manuel » ou « la section du
supplément », et les deux voix sont retranscrites dans la notation unique de notation.md.
Les deux jonctions explicites du cours sont (a) detach() = semi-gradient, en 5.4, et
(b) le tampon de rejeu = troisième jambe de la triade, en 5.7.

SUTTON & BARTO ch. 9 « On-policy Prediction with Approximation » : la valeur approchée comme
forme fonctionnelle paramétrée de vecteur de poids w ∈ R^d, hat v(s,w) ≈ v_π(s), linéaire ou
réseau multicouche ou arbre de décision ; d ≪ |S| et « changer un poids change la valeur
estimée de nombreux états », généralisation plus puissante mais plus difficile à gérer ;
applicabilité aux problèmes partiellement observables et impossibilité d'augmenter l'état avec
le souvenir des observations passées (219) ; relecture de chaque mise à jour comme exemple
supervisé s ↦ u, les trois cibles MC / TD(0) / n pas, « méthodes d'apprentissage supervisé »,
les deux exigences nouvelles, apprentissage en ligne et cible NON STATIONNAIRE (220) ; le cas
tabulaire n'avait pas besoin d'une mesure continue de qualité et ses valeurs étaient
découplées, obligation de dire quels états comptent, μ(s) ≥ 0 et Σμ(s) = 1, VE barre →
EQ 05-E1, μ comme fraction du temps passé dans s et distribution sur politique, éq. 9.2-9.3
hors sujet (221) ; VE barre n'est pas forcément le bon objectif puisque le but est une
meilleure politique, optimum global rare pour un réseau, optimum local « le mieux que l'on
puisse dire », et « certaines méthodes peuvent diverger, leur VE barre tendant vers l'infini »
(222) ; w vecteur colonne de d composantes et hat v différentiable, SGD « ajuster après chaque
exemple d'une petite quantité dans la direction qui réduirait le plus l'erreur », éq. 9.4-9.5 →
EQ 05-E2, définition du gradient éq. 9.6 → EQ 05-E3, pourquoi un petit pas et équilibre des
erreurs entre états, α décroissant (223) ; cible générique U_t éq. 9.7 → EQ 05-E4, condition
d'absence de biais et garantie de convergence vers un optimum local, Monte-Carlo par gradient →
EQ 05-E5, LE PARAGRAPHE DE LA SEMAINE sur les cibles amorcées, dépendance en w_t, biais,
invalidité du passage de 9.4 à 9.5, « tiennent compte de l'effet sur l'estimation mais ignorent
son effet sur la cible », nom « méthodes semi-gradient », apprentissage plus rapide, continu et
en ligne mais convergence moins robuste (224) ; encadré TD(0) semi-gradient → EQ 05-E6 avec
hat v(terminal, ·) = 0 (225) ; « semi-gradient » est un terme de la 2e édition, introduit sans
attribution comme vocabulaire du cours (259, lu dans index/summaries/sb/ch09.md) ; les garanties
de convergence de §9.4 tiennent PARCE QUE les mises à jour suivent la distribution sur
politique (230, cité d'après index/summaries/sb/ch09.md, chunk 09-04 non lu : énoncé en prose
sans ancre de page, planté en 5.3 et récolté en 5.6) ; toute la route linéaire, §§9.4 à 9.10
(bases polynomiale et de Fourier, codage grossier, pavage, fonctions à base radiale, LSTD,
méthodes à mémoire et à noyau) est VOLONTAIREMENT ÉCARTÉE, nommée en une incise en 5.2 et 5.3
et jamais enseignée.

SUTTON & BARTO ch. 10 « On-policy Control with Approximation » : « l'extension des méthodes
semi-gradient de prédiction aux valeurs d'action est directe », exemples S_t, A_t ↦ U_t (265) ;
éq. 10.1 → EQ 05-E7, éq. 10.2 Sarsa semi-gradient à un pas épisodique → EQ 05-E8, calcul de
hat q pour chaque action puis action gloutonne → EQ 05-E9 avec approximation souple
ε-gloutonne, branche terminale de l'encadré → EQ 05-E10, Mountain Car et l'obligation de
s'éloigner du but, « les choses doivent empirer avant de s'améliorer », récompense −1 par pas,
trois actions (266-267) ; fig. 10.1 → FIG 05-01, coût pour atteindre défini comme
−max_a hat q(s,a,w), panneaux pas 428 et épisodes 12, 104, 1000, 9000 (267) ; valeurs initiales
nulles donc OPTIMISTES puisque toutes les valeurs vraies sont négatives, exploration même à
ε = 0, aucun épisode terminé au pas 428 et voiture oscillant dans la vallée ; éq. 10.3 et les
paramètres de pavage sont HORS SUJET, la figure est demandée pour la forme de la surface et la
légende le dit (268). §§10.3 à 10.6 (récompense moyenne, valeurs différentielles, dépréciation
de l'actualisation) non lues, sur le programme d'aucune semaine.

SUTTON & BARTO ch. 11 « Off-policy Methods with Approximation » : seconde moitié du problème
hors politique, « la distribution des mises à jour ne correspond pas à la distribution sur
politique » ; exemple à deux états de valeurs w et 2w, caractéristiques 1 et 2, une action,
récompense nulle, trajectoire arithmétique 10 → 11 → 12,1 avec une erreur TD qui GRANDIT,
algèbre δ_t = (2γ−1)w_t et w_{t+1} = (1+α(2γ−1))w_t → EQ 05-E11, raison > 1 dès γ > 0,5, « la
stabilité ne dépend pas du pas d'apprentissage pourvu que α > 0 » (282) ; image de la facture
à payer sur politique contre la promesse oubliée hors politique, traduite et non calquée ;
contre-exemple de Baird, sept états, action en pointillés vers les six états du haut et action
pleine vers le septième, b(pointillés) = 6/7 et b(plein) = 1/7 donnant une distribution
uniforme des états suivants, π jouant toujours l'action pleine, récompenses nulles, γ = 0,99,
fig. 11.1 → FIG 05-02 (283) ; v_π = 0 exactement représentable par w = 0, huit poids pour sept
états, caractéristiques linéairement indépendantes, « les poids divergent vers l'infini » et
« l'instabilité se produit pour tout pas positif, aussi petit soit-il », divergence AUSSI sous
la mise à jour en espérance éq. 11.9 → EQ 05-E15 où il n'y a ni hasard ni asynchronie,
fig. 11.2 → FIG 05-03 avec α = 0,01 et w initial (1,1,1,1,1,1,10,1), et la réparation
indisponible : passer de la distribution uniforme à la distribution SUR POLITIQUE garantit la
convergence (284) ; contre-exemples de divergence pour Q-learning, convergence peut-être
garantie si la politique de comportement est assez proche de la cible, par exemple
ε-gloutonne, « à notre connaissance Q-learning n'a jamais été observé en train de diverger
dans ce cas, mais il n'existe aucune analyse théorique », éq. 11.10 de Tsitsiklis & Van Roy
NON reprise (285) ; stabilité garantie seulement pour les approximateurs qui n'extrapolent pas,
les MOYENNEURS, « mais pas les méthodes populaires comme le pavage et les réseaux de neurones
artificiels » ; la triade fatale en trois définitions, approximation / amorçage / hors
politique, « si deux éléments sont présents mais pas les trois, l'instabilité peut être
évitée », danger non dû au contrôle ni à l'itération généralisée de politique puisqu'il
apparaît en prédiction, non dû à l'apprentissage ni à l'incertitude puisqu'il apparaît en
programmation dynamique (286) ; lequel abandonner : jamais l'approximation, l'amorçage est
possible mais coûteux et « une capacité que nous aimerions beaucoup conserver », le hors
politique est possible, « on peut simplement utiliser Sarsa plutôt que Q-learning », au prix de
l'apprentissage parallèle de plusieurs prédictions sur un seul flux (286-287) ; §11.1 et son
éq. 11.5, qui dit qu'une mise à jour de valeur d'action à un pas n'a besoin d'AUCUN rapport
d'échantillonnage préférentiel, est citée d'après index/summaries/sb/ch11.md : le chunk 11-02
n'est PAS au dossier et n'a pas été lu, l'énoncé est donc écrit sans ancre de page (encadré
[!NOTE] en 5.7) et il est de toute façon lisible sur EQ 05-E12, où ni π ni b n'apparaissent.
§§11.4 à 11.9 (géométrie des fonctions de valeur, erreur de Bellman, apprenabilité,
Gradient-TD, TD emphatique) NON LUES : ce sont les réparations mathématiques de la triade, et
le cours gère le danger par l'ingénierie, notation.md §5 écartant déjà Gradient-TD du
programme.

LAPAN ch. 6 « Deep Q-Networks » : le chapitre va des problèmes de l'itération sur la valeur au
Q-learning avec réseaux de neurones, « qui porte le nom de deep Q-network (DQN) », et
réimplémente la méthode des débuts (164) ; hypothèses de l'itération sur la valeur, la mémoire
n'est PAS l'obstacle (8,5 milliards de flottants dans 32 Go, balayage coûteux mais
parallélisable), les ÉCHANTILLONS le sont (un FrozenLake de 31 600 × 31 600 demanderait des
centaines de milliards de transitions uniformément réparties) (165) ; écran Atari 210 × 160 et
128 couleurs, 33 600 pixels, 128^33600 « un peu plus de 10^70802 », énumération « des milliards
de milliards d'années même pour le superordinateur le plus rapide » et 99,9 % de travail perdu
sur des écrans jamais affichés ; seconde limite, espaces d'actions discrets seulement, nommée
et reportée aux semaines 9-10 (165-166) ; CartPole, quatre float32, 2^128 ≈ 3,4·10^38, la
discrétisation « crée souvent plus de problèmes qu'elle n'en résout » parce qu'il faut décider
quelles plages comptent (171) ; fig. 6.2 → FIG 05-04, deux situations de Pong indiscernables sur une seule trame et
de sens opposés, et « problème de régression » comme nom du remplacement de la table (172) ;
algorithme naïf en cinq pas et « il ne fonctionnera pas très bien », problème 1 l'interaction,
aléatoire inutile dans Pong et glouton qui reste coincé, ε-gloutonne et pratique usuelle de
partir de 1,0 (173) ; problème 2 l'exigence i.i.d. de la SGD, deux violations (transitions d'un
même épisode très proches, distribution produite par la politique courante), tampon de rejeu de
taille fixe où les nouvelles données chassent les anciennes, « données plus ou moins
indépendantes mais assez fraîches », tampon priorisé explicitement reporté au ch. 8 du
supplément, donc semaine 6 (174) ; problème 3 la corrélation entre pas, s et s' séparés d'un
seul pas donc très semblables et difficiles à distinguer pour un réseau, « courir après sa
propre queue », réseau cible synchronisé tous les N pas avec N de l'ordre de 1k à 10k ;
problème 4 la propriété de Markov, une trame ne donne ni vitesse ni direction, PDM
partiellement observable, second exemple des jeux de cartes, empilement de k = 4 trames et
« bien sûr ce n'est qu'un bricolage », ε-gloutonne + tampon + réseau cible comme base ayant
permis 49 jeux (175) ; les dix pas de l'algorithme → EQ 05-E12, VÉRIFIÉS sur
index/pages/lapan/0176.png, et « plus de 1,5 million de paramètres » pour le modèle de 2015
(176) ; anecdote du bouton FIRE et des jours de débogage, réécrite en avertissement général
sans l'attribuer, plus les huit transformations d'enveloppe avec leur raison (178-179) ;
BufferWrapper renvoie une COPIE pour que le tampon de rejeu ne soit pas réécrit par les pas
suivants, et doit être la DERNIÈRE de la chaîne (181-182) ; architecture, trois convolutions,
deux couches linéaires, ReLU partout, aucune non-linéarité en sortie « puisque les valeurs Q
peuvent prendre n'importe quelle valeur » (182) ; UNE SORTIE PAR ACTION, « calculer toutes les
valeurs Q en un seul passage aide à augmenter la vitesse de façon significative », formes
4×84×84, (4,32,k8,s4), (32,64,k4,s2), (64,64,k3,s1), aplatissement 3136, 3136→512, 512→6 (183,
196) ; stockage uint8 et division par 255 DANS forward sur le GPU, « c'est rapide puisque le
tenseur d'octets est déjà dans la mémoire du GPU » (184) ; les neuf hyperparamètres, avec
l'avertissement que ce sont ceux d'une expérience et non du papier d'origine, tampon d'un
million de transitions et « environ 20 Go de RAM », décroissance de ε sur un million de trames,
« cette accélération implique un réglage fin pour un environnement particulier et peut casser
la convergence sur d'autres jeux » (185-186) ; np.asarray évite une copie, « sans cette
optimisation les performances chutent d'environ vingt fois », perte vectorisée « plus de deux
fois plus rapide » qu'une boucle explicite (189) ; gather prélève la valeur de l'action jouée,
dimension 1 = dimension des actions, « opération différentiable qui conservera tous les
gradients », fig. 6.3 → FIG 05-05 (190-191) ; masque terminal, « cela peut sembler mineur mais
c'est très important en pratique, sans cela l'entraînement ne convergera pas » (191) ;
detach() et sa justification, « empêcher les gradients de remonter dans le réseau utilisé pour
calculer l'approximation des états suivants », plus with torch.no_grad() autour du passage
avant de la cible en p.191 : LE GRADIENT EST BLOQUÉ DEUX FOIS, l'un ou l'autre suffirait, dit
en une phrase en 5.4 ; expected_state_action_values puis nn.MSELoss(), donc ERREUR QUADRATIQUE
ET NON HUBER → EQ 05-E12b (192) ; les deux réseaux partent de poids aléatoires différents,
« cela n'a pas beaucoup d'importance puisque nous les synchronisons toutes les 1k trames, ce
qui correspond à peu près à un épisode de Pong » (193) ; calendrier de ε en code → EQ 05-E13,
critère d'arrêt sur la moyenne des 100 derniers épisodes au-delà de 19,0 « soit gagner plus de
19 manches sur 21 », sauvegarde à chaque record, torch.save(net.state_dict(), ...) qui est ce
que le volet C du laboratoire charge (194) ; ordre des six gestes de la boucle, pas
d'apprentissage avant REPLAY_START_SIZE, synchronisation périodique, ~400k trames pour une
moyenne de 17 soit « plus de 80 % des manches » et autant encore pour aller de 17 à 19, « en
moyenne un million de trames de jeu », 250 tr/s sur un GPU haut de gamme ≈ une heure, 40 tr/s
sur CPU ≈ sept heures, autres jeux « des centaines de millions de trames et un tampon cent fois
plus grand » (194-195) ; journal d'exécution, ~1400 tr/s pendant le remplissage puis ~260 tr/s,
récompense collée à −21/−20 pendant les ~70 premières parties, « la récompense moyenne commence
à croître, ce qui arrive normalement autour de ε = 0,5 », résolu à la partie 380 (196-198) ;
la vitesse diminue quand ε diminue parce qu'il faut inférer pour choisir l'action (197) ;
« dans de rares cas, une exécution sur dix d'après mes expériences, l'entraînement ne converge
pas du tout », consigne de relancer si rien ne bouge en 100k-200k itérations, et « Solved in
755958 frames! » (198) ; fig. 6.4 p.196 (récompense moyenne sur 100 épisodes) DÉLIBÉRÉMENT NON
DEMANDÉE, le journal de console portant le même récit en texte avec de meilleurs chiffres.

COURSE-PLAN §2 et §9.2 : aucun jalon en semaine 5, le prochain est en semaine 7, laboratoire
formatif ; DQN sur CartPole ou LunarLander sous quinze minutes sur T4, donc entraînement réel ;
DQN sur Pong de une à trois heures, donc poids fournis et ÉVALUATION SEULEMENT. Le découpage du
laboratoire en quatre volets est écrit autour de cette contrainte depuis la première ligne.
La perte de Huber est promise par §9.2 du plan pour cette semaine.

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossiers/week-05.md, section « DO NOT read ») :
lapan/ch06/06-02 (Q-learning tabulaire : la semaine 4 l'a enseigné depuis la source qui le
définit, et son laboratoire l'a implémenté) ; lapan/ch06/06-10 et 06-11 (jouer un modèle
sauvegardé, et résumé de chapitre) ; sb/ch11/11-02 (§11.1 et les conversions semi-gradient,
éq. 11.1 à 11.8, qui mettraient ρ_{t:T−1} et quatre variantes à n pas sur la page, toutes deux
de la semaine 6) ; sb/ch09/09-04 à 09-09 et 09-11 à 09-13 (toute la route linéaire) ;
sb/ch09/09-10 (panorama des réseaux de neurones, que la semaine 2 a traité avec du code) ;
sb/ch10/10-03 à 10-06 ; sb/ch11/11-05 à 11-12 (les réparations de la triade) ; et tout
lapan/ch07 et ch08, qui sont la semaine 6.

GAP DOCUMENTÉ, ET IL TOUCHE LE LABORATOIRE : le chunk 06-10 contient la seule recette
« charger un state_dict et jouer » du chapitre, et il est exclu du dossier. La boucle
d'évaluation du volet C est donc ÉCRITE par le cours plutôt qu'adaptée, ce que D15 exige de
toute façon. Les deux décisions qu'elle contient (reseau.eval() et torch.no_grad()) sont des
conséquences de la semaine 2, et le choix de ε = 0 à l'évaluation est une conséquence de la
falaise de la semaine 4 : le volet demande à l'étudiant de l'écrire lui-même.

ÉCARTS ASSUMÉS
- D43 et notation.md l.33-34 : deux notations pour un seul réseau. Le formalisme garde w, les
  sections DQN gardent θ et θ⁻, la règle est énoncée UNE fois, dans un encadré [!IMPORTANT] de
  l'introduction, AVANT la première équation, et SANS attribution : aucun auteur, aucun
  ouvrage, aucun chapitre. Même geste que la semaine 4 pour l'échelle v_π / V / hat v.
- notation.md §6 appliqué silencieusement : le Q(s,a) de la source devient Q_θ(s,a), son hat Q
  devient Q_{θ⁻}, son ε s'écrit varepsilon. Traduction faite AUSSI à l'intérieur de l'encadré
  de pseudocode des dix pas, pour qu'un étudiant qui le recopie dans un carnet n'importe pas
  une seconde notation du réseau cible.
- notation.md §4 contre les notes : VE barre y est glosée « erreur quadratique de valeur »,
  tandis que les notes et index/summaries/sb/ch09.md écrivent « erreur quadratique moyenne sur
  les valeurs ». La seconde forme est retenue, la première est enregistrée comme synonyme
  accepté dans glossaire.md. Même traitement que « pas d'apprentissage » contre « taux
  d'apprentissage » en semaine 4. Alignement du registre signalé, pas effectué.
- ε-GLOUTONNE NON RÉENSEIGNÉE : la semaine 4 l'a définie, la source la remotive de zéro en
  p.173. La semaine 5 ne garde que ce qui est nouveau, le CALENDRIER de décroissance
  (EQ 05-E13) et ses nombres.
- TROIS VALEURS FINALES DE ε DANS LA MÊME SOURCE (5 % ou 2 % en p.173, 1,0 → 0,1 sur un million
  de trames en p.185, EPSILON_FINAL = 0,01 sur 150 000 trames en p.186). Le cours écrit les
  nombres DU CODE comme hyperparamètres de l'implémentation et le calendrier D'ORIGINE comme
  calendrier d'origine ; la prose n'est pas citée. Aucune mention du désaccord : rien dans la
  page ne dit qu'il existe une source.
- TROIS COÛTS DE CONVERGENCE (≈ 50 minutes en p.185, ≈ une heure et ≈ un million de trames en
  p.195, « Solved in 755958 frames! » en p.198). Le cours écrit 755 958 trames, « environ une
  heure » sur le même matériel et « environ sept heures » sur processeur central, plus les
  400 000 trames pour atteindre 17 et autant encore pour 19. La valeur de 50 minutes n'est pas
  citée. Même silence.
- « TRIADE FATALE » et non « triade mortelle » : l'index se contredit (summaries/sb/ch11.md
  écrit fatale, summaries/sb/ch09.md écrit mortelle) et le chapitre 11 est celui qui définit la
  notion. La ligne de glossaire ajoutée cette semaine liste « triade mortelle » comme forme à
  éviter.
- PERTE DE HUBER (EQ 05-E14) : DÉFINIE PAR LE COURS, sans attribution. Le plan la promet pour
  cette semaine et AUCUNE source du corpus ne la contient ; l'implémentation étudiée appelle
  nn.MSELoss(). Le cours la définit en deux lignes dans un encadré [!TIP] en fin de 5.8, dit
  explicitement que l'implémentation de la page minimise l'erreur quadratique, et renvoie la
  mesure au volet D du laboratoire. Rien n'est affirmé sur son effet mesuré, et elle n'est
  attribuée à personne. Même traitement que la méthode ε-gloutonne de la semaine 4.
- SYNTHÈSE PROPRE AU COURS, SIGNALÉE COMME TELLE, trois fois : (a) l'audit en trois lignes qui
  montre que notre DQN possède les trois ingrédients de la triade, assemblé depuis SB p.286 et
  le code de LAPAN ; (b) le rapprochement « detach() = le semi de semi-gradient », qui tient
  deux anchors (SB p.224 et LAPAN p.191-192) dans une seule phrase ; (c) la lecture du tampon
  de rejeu comme solution d'un problème et création d'un autre, qui tient LAPAN p.174 et SB
  p.286 ensemble. Aucune source ne formule ces trois rapprochements ; chacun est livré dans un
  encadré et chacun cite ses deux moitiés en commentaire.
- HAMEÇONS DE LA SEMAINE 6 NOMMÉS, AUCUN DÉPENSÉ : surestimation par le max, uniformité du
  tirage dans le tampon, séparation valeur/avantage, bruit de paramètres à la place de ε, cible
  à un pas. Les cinq sont listés en fin de 5.9 comme DÉFAUTS CONNUS, aucun n'est corrigé, et
  aucun nom de méthode de la semaine 6 n'est donné. 08-06_double-dqn n'a pas été ouvert.
- D15 : tout le code est réécrit (noms français, annotations de type, TamponDeRejeu construit
  autour d'un deque et d'une namedtuple, enveloppe d'empilement réécrite en ObservationWrapper,
  calcul de 3136 par un passage de zéros, assertions et points de contrôle ajoutés). Rien n'est
  copié d'un dépôt de source.
- D12 : PyTorch nu, Gymnasium, NumPy, Matplotlib. Aucune bibliothèque d'algorithmes cette
  semaine ; PTAN est annoncé pour la semaine 6, comme OBJET D'ÉTUDE, dans la dernière phrase de
  la transition.
- RIEN QUE L'ÉTUDIANT DOIVE EXÉCUTER N'EST DANS LA PAGE : les treize fragments Python des sections sont
  là pour la double lecture (D10), les programmes complets et les quatre volets passent par
  {{< colab >}}. La boucle de 5.9 est explicitement présentée comme un plan de lecture
  incomplet.

DÉCOMPTE : 9 sections · 5 placeholders FIG · 0 placeholder EQ
(les seize équations 05-E1 à 05-E15 plus 05-E12b sont écrites directement : quatorze sont
RECOPIÉES depuis index/notes/week-05.md, elles-mêmes transcrites depuis quatorze pages
rasterisées sous index/pages/sb/ et deux pages sous index/pages/lapan/, et confirmées une par
une sur l'image ; 05-E13 est écrite depuis le code ; 05-E14, la perte de Huber, est écrite
directement et appartient au cours. Aucune ne passe par un placeholder, ce qui est le régime
prévu par D22 pour une formule vérifiée sur sa page.)
{{% /comment %}}
