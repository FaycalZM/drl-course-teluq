---
title: "Semaine 7 : Accélérer l'apprentissage et étude de cas : le trading"
weight: 7
bookCollapseSection: true
---

# Semaine 7 : Accélérer l'apprentissage et étude de cas : le trading

La semaine 6 s'est terminée sur un agent qui fonctionne et qui coûte cher : des centaines de milliers de trames, des heures de calcul, et un débit qui baisse à mesure qu'on l'améliore. Cette semaine attaque les deux questions qui restent, et elles n'ont rien à voir l'une avec l'autre. D'abord : comment rendre une exécution bon marché, sans toucher à la méthode, et comment mesurer honnêtement si l'on a réussi. Ensuite : comment prendre un problème réel, où ni l'observation, ni les actions, ni la récompense ne sont données, et le transformer en processus de décision markovien. Le problème réel sera la négociation d'un titre sur un marché, et son résultat nous servira surtout à apprendre à ne pas croire un résultat trop vite.

> [!IMPORTANT]
 **Un chiffre n'est un résultat que si l'on sait ce qu'il aurait valu sans l'intervention, et combien il varie quand on ne change rien.**

---
## Description générale

La semaine se lit en deux moitiés qui ne partagent aucun sujet, et c'est assumé.

La première moitié, des sections 7.1 à 7.6, est de l'ingénierie de performance. Elle commence par montrer que la vitesse n'est pas un confort mais une variable de recherche, puisqu'elle décide du nombre d'expériences qui tiennent dans une semaine. Elle installe ensuite un protocole de mesure à **deux** indicateurs, le débit de trames et le temps d'horloge jusqu'à un seuil fixé d'avance, et elle explique pourquoi un seul des deux ne suffit jamais. Elle y ajoute l'exigence qui vaudra pour tout le reste du cours : plusieurs graines aléatoires et un intervalle de confiance, parce qu'une exécution unique ne permet de décider de rien. Puis viennent trois accélérations, par ordre croissant de perturbation du programme : la suppression du graphe de calcul là où il ne sert à rien, la vectorisation de l'environnement, et la séparation de la collecte et de l'entraînement en deux processus. La moitié se ferme sur un tableau qui met les six configurations côte à côte et montre que la configuration la plus rapide en trames par seconde est presque la plus lente à résoudre le jeu.

La seconde moitié, des sections 7.7 à 7.13, est de la modélisation. Elle prend un problème qui n'a pas été conçu pour l'apprentissage par renforcement et le formule entièrement : l'observation, les actions, la récompense, puis l'environnement écrit à la main derrière l'interface de Gymnasium. Trois moments y sont décisifs. Le protocole de validation d'une série temporelle, qui s'ajuste sur la période la plus ancienne et se valide sur la plus récente, et dont la généralisation vaut pour tout signal indexé par le temps. Les deux schémas de récompense, qui semblent équivalents et définissent en réalité deux problèmes différents, pour trois raisons distinctes. Et la lecture du résultat, où la commission de courtage fait passer le même agent, sur la même année, de \(+48\,\%\) à \(-60\,\%\).

La semaine **clôt le module 2** et porte le **jalon 2**, qui vaut 25 % de la note et qui demande les deux moitiés ensemble : une étude comparative avec plusieurs graines et des intervalles, et une accélération mesurée dans un tableau.

---

## Mots-clés de la semaine

vitesse d'itération expérimentale · correction avant vitesse · version de référence · protocole de mesure · trames par seconde · temps d'horloge · graine aléatoire · intervalle de confiance · désactivation des gradients · environnements vectorisés · séparation de la collecte et de l'entraînement · profilage · formulation d'un problème réel en processus de décision markovien · conception de la récompense · représentation relative des prix · barre de prix · partage chronologique entraînement-validation · validation hors échantillon · environnement sur mesure · commission de courtage · écart achat-vente · dérapage des prix · surapprentissage de l'agent · achat-conservation

## En prévision de la semaine suivante

La semaine 8 ouvre le module 3 et change de famille de méthodes. Au lieu d'apprendre une valeur et d'en déduire une politique par un \(\argmax\) sur les actions, elle apprend directement la **politique** comme un réseau qui produit une distribution de probabilité sur les actions. C'est ce qui lève le mur sur lequel le module 2 se termine : toutes les méthodes des semaines 4 à 7 exigent un espace d'actions discret et fini. Vous y verrez le théorème du gradient de politique, la méthode REINFORCE, et le problème de variance qui les accompagne.

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF − 31 pour LAPAN, conformément à MAP-lapan.md,
comme dans le dossier et les notes de phase 1. Toutes les pages citées ci-dessous sont des
indices PDF.

SEMAINE À DEUX CHAPITRES QUI NE PARTAGENT AUCUN SUJET, ET LE DOSSIER LE DIT AINSI. Le
ch. 9 est de l'ingénierie de performance et porte les sections 7.1 à 7.6 ; le ch. 10 est une
étude de cas de modélisation et porte les sections 7.7 à 7.13. Aucune source nouvelle cette
semaine : pas de nouveau papier, pas de nouveau chunk, et C4 (le dépôt de configurations de
référence) est une référence de configuration pour les tableaux d'hyperparamètres du jalon,
pas un texte lu. Les deux moitiés sont jointes par le jalon 2, qui demande les deux.

LAPAN ch. 9 « Ways to Speed up RL » : annonce d'une approche PUREMENT D'INGÉNIERIE, opposée
explicitement à l'approche algorithmique du chapitre précédent, même matériel, objectif
presque ×2 sur Pong (284) → §7.1 et la forme de la semaine en introduction ; l'installation
de 2005, 64 serveurs, trois armoires de 42 pouces, refroidissement et alimentation dédiés,
~1 M$, 922 GFLOPS, 4ᵉ des machines de l'ex-URSS, contre GTX 1080 Ti 12 ans plus tard à
11 340 GFLOPS (×12,3) pour 700 $, soit >17 500× par GFLOP et par dollar, et H100 à 134
téraflops FP32 (284-285) → §7.1 premier paragraphe, chiffres repris intégralement ;
l'argument d'échelle, un mois → 6 jours à ×5, 8 heures à ×100, 2-3 minutes à ×20 000 (285) ;
L'ARGUMENT RÉEL, qui est l'itération et non l'exécution unique, « presque impossible à
implémenter correctement du premier coup », nombreux essais avant de bons hyperparamètres
et avant la correction des bogues (286) → §7.1, reformulé en voix du cours ; l'anecdote
Hadoop, plusieurs semaines → quelques heures sur plusieurs téraoctets, ce qui change est la
DISPOSITION À LANCER des expériences et la qualité du produit final (286) → §7.1 encadré
[!TIP], ANECDOTE SUPPRIMÉE et FAIT CONSERVÉ (D45 : la première personne de l'auteur n'est
jamais celle de la professeure) ; second usage d'une accélération, la taille du problème
plutôt que l'attente (286) ; la raison propre à l'AR, méthodes très peu efficaces en
échantillons, millions d'interactions, semaines d'entraînement (286) → §7.1 seconde
sous-section ; le déplacement de la frontière, Atari considéré résolu y compris Montezuma's
Revenge, repliement des protéines et grands modèles de langue sur des milliers de GPU
(286-287) ; LA RÈGLE DE LA SEMAINE, « toute optimisation n'a de sens que si la méthode
fonctionne », « mieux vaut lent et correct que rapide et incorrect » (287) → §7.1 encadré
[!WARNING] et ordre du laboratoire.

§7.2 repose sur 287-289 : version de référence = le DQN du ch. 6 avec LES MÊMES
hyperparamètres, rien de réglé à nouveau (287) ; indicateur 1 = FPS, 25-50 M trames dans la
littérature, calcul 50·10⁶/(200·60·60·24) ≈ 2,89 jours (287, LU SUR L'IMAGE : la couche texte
aplatit la fraction) → EQ 07-E1, écrite directement en KaTeX ; le piège d'unité, trames brutes
contre pas de l'agent, saut de trames presque toujours 4, le compteur du texte compte les
COMMUNICATIONS agent-environnement (287, image) → EQ 07-E2 ; indicateur 2 = temps d'horloge
jusqu'à récompense lissée sur 100 épisodes = 18, maximum de Pong 21, au-delà « polir »
(287, image) ; la raison d'avoir DEUX indicateurs, « un FPS très élevé mais la convergence
peut souffrir » (287, image) → §7.2 et la lecture du tableau en §7.6 ; les graines PyTorch /
Gym / NumPy explicites et INSUFFISANTES, la parallélisation réinjecte un hasard « presque
impossible à éviter », donc répéter et moyenner, « le résultat d'une exécution unique ne
permet de prendre aucune décision » (287, image) → §7.2 troisième sous-section, et c'est le
crochet du jalon ; toutes les courbes du chapitre sont la moyenne de 5 exécutions (288) ;
matériel de mesure i5-7600K, GTX 1080 Ti, CUDA 12.3, pilote 545.29.06, donc SEULS LES
RAPPORTS se transportent sur un T4 (288) → §7.2 encadré [!WARNING] final ; la liste des
métriques instrumentées, reward / avg_reward (α = 0,98) / steps / loss toutes les 100
itérations / avg_loss / epsilon / avg_fps (288) → EQ 07-E3 et liste de contrôle du volet A ;
bande de perte attendue 2·10⁻³ à 1·10⁻², pics quand la récompense d'un comportement découvert
diffère de la valeur apprise (288) ; longueur d'épisode ~1 000 → 3 000-4 000 → ~2 000 pas, la
redescente expliquée par γ qui récompense une victoire précoce, et la remarque de l'auteur sur
un possible surapprentissage déclarée hors sujet (288) → §7.2 encadré [!NOTE], question laissée
OUVERTE et renvoyée en semaine 15 (le dossier demande de ne pas épuiser le matériel du ch. 10
dans une morale) ; convention des deux axes des abscisses, heures en bas, pas/épisodes en haut
(289) ; seuil de résolution passé de 19 (ch. 6) à 18 ici, donc durées NON COMMENSURABLES avec
la semaine 5 (287) → §7.2 encadré [!NOTE] de comparabilité.

§7.3 repose sur 289-292 et sur 302 : PyTorch construit le graphe de toute opération,
backward() sur la perte finale remplit les gradients (289) ; LES TROIS USAGES DU RÉSEAU dans un
DQN, valeurs de l'état courant pour la perte / réseau cible sur l'état suivant / agent qui
choisit, SEUL LE PREMIER a besoin de gradients (290) → le diagramme sans figure sur lequel la
section repose ; detach() = CORRECTION, « empêche les gradients de remonter dans le modèle par
une direction inattendue », sans quoi « le DQN peut ne pas converger du tout », et cas 3 déjà
protégé par la conversion en tableau NumPy (290) ; no_grad() = VITESSE, « le graphe est créé
même si on n'appelle pas backward() », coût en temps ET en mémoire (290) → l'encadré
[!WARNING] qui sépare les deux, exigé par le pitfall 2 du dossier ; décorateur ET gestionnaire
de contexte, effet BORNÉ à la région, multiplication hors zone par un tenseur qui demande des
gradients ⇒ un graphe repart (290-291) ; déjà appliqué dans l'agent et le calcul de perte de la
bibliothèque de la semaine 6, « très facile à oublier dans son propre code » (291) → le
paragraphe de crochet vers le volet B ; gain mesuré ~10 FPS sur ce réseau, 50 % observés sur des
réseaux récurrents plus complexes, donc la taille du gain est une propriété DU MODÈLE (292) ;
et la contradiction du tableau, sans no_grad() : −4,3 % FPS et −2,3 % de temps (302) → §7.3
encadré [!NOTE] et premier exemple travaillé du jalon.

§7.4 repose sur 292-295 : le réflexe supervisé, grossir le lot jusqu'à épuiser la mémoire
(292) ; pourquoi il ne se transporte pas, DEUX choses simultanées, le réseau s'améliore ET
l'agent explore, donc les données d'entraînement sont produites par la chose entraînée et
changent (292) ; l'image du jeu de tir, un tampon ne contenant que des morts rapides conduit à
conclure que mourir tôt minimise la souffrance et à NE JAMAIS DÉCOUVRIR L'ARME, « la convergence
repose sur un équilibre fragile entre entraînement et exploration » (292-293) → §7.4, image
conservée et reformulée ; le correctif, N copies, le tampon alimenté par les N et un lot
PROPORTIONNELLEMENT plus grand, plus le gain secondaire des N actions décidées en UN passage
avant (293) ; coût d'implémentation faible, liste d'environnements, agent déjà par lots,
batch_size *= n_envs, constantes de décroissance de ε et du compteur de FPS à recalibrer
(293-294) → le fragment de code et les deux lignes de commentaire sur les constantes ; mesures,
N balayé de 2 à 6 : deux environnements 227 → 335 FPS (+47 %) et 52 → 48 min (~10 %) ; trois
environnements 398 FPS et 36 min ; au-delà de trois le FPS monte et LA CONVERGENCE SE DÉGRADE,
donc N = 3 retenu (294) ; la conclusion de l'auteur, qui est celle du cours : on surveille non
pas la vitesse brute mais la rapidité à résoudre le jeu (294) ; N présenté comme un NOUVEL
HYPERPARAMÈTRE (294) → encadré [!IMPORTANT] de §7.4.

§7.5 repose sur 295-299 : la boucle en quatre étapes, 1-2 remplissent le tampon, 3-4
entraînent (295) ; L'ARGUMENT DE SÉPARATION en une phrase, « les deux étapes du haut ne
communiquent avec le bas que par le tampon de rejeu et le réseau » (295) ; fig. 9.6 p.295, LUE
SUR L'IMAGE : quatre boîtes rouges en boucle verticale (Observations → actions, Play steps,
Sample batch, Train net), Envs et Replay buffer en bleu à droite, NN dans une boîte GPU jaune,
traits pleins = flux de données, traits POINTILLÉS = usages du réseau → FIG 07-01, et la
convention plein/pointillé est DANS LA PROSE et dans la légende ; fig. 9.7 p.296, même
vocabulaire scindé en Train process / Play process joints par une Play queue, le NN hors des
deux sous GPU → FIG 07-02, PAIRE INDISSOCIABLE avec 07-01 (le dossier : « extraire les deux ou
aucune ») ; quand cela paie, PAS sur Pong, mais sur un environnement lourd où chaque pas prend
des secondes, simulateurs neuromusculaires de concours de locomotion et de prothèses, puis
plusieurs environnements concurrents vers un entraînement central (296) → §7.5, les NOMS DE
CONCOURS sont remplacés par leur description générique ; torch.multiprocessing en remplacement
direct du module standard et partage de tenseurs SANS COPIE, mémoire partagée pour le CPU,
références CUDA pour le GPU, « supprime le goulot principal au sein d'une même machine », mais
la communication réellement distribuée reste à sérialiser (296-297) ; le protocole à UNE file et
DEUX types de messages, les items d'expérience et une classe de fin d'épisode portant récompense,
pas et epsilon, pour que l'entraîneur puisse encore rapporter des statistiques qu'il n'observe
plus (296-297) → le fragment de code, et la justification explicite du second message ; côté
entraînement, le générateur vide la file, route les fins d'épisode vers une liste de statistiques
et le reste vers le tampon, attend `initial` items, puis livre un lot, en IMITANT l'interface de
la source d'expérience de la semaine 6 pour que le reste du code ne change pas (297-298) ; les
deux détails qui cassent en silence, set_start_method('spawn') « le plus flexible » et
Queue(maxsize=2) qui étrangle le collecteur (298-299) → §7.5, et l'interprétation de la petite
file comme MÉCANISME DE RÉGULATION (politique périmée) est la lecture du cours ; résultat 290 FPS
contre 228 (+27 %) et temps de résolution −41 %, donc MOINS de FPS que la version à trois
environnements (~400) mais MEILLEURE convergence (299) → deuxième désaccord FPS/temps.
LE DOSSIER INTERDIT D'ALLER PLUS LOIN : §7.5 s'arrête à un pas de A3C, aucune mention de
l'avantage, des acteurs-critiques ni du partage asynchrone de gradients, qui sont la semaine 8.

§7.6 repose sur 299-303 : les enveloppes « faciles à négliger, écrites une fois ou empruntées,
appliquées puis laissées en place » (299) ; la pile DeepMind dans l'ordre avec le rôle de
chacune, NoopResetEnv (NOOP aléatoires au reset, supprime les observations initiales
atypiques), MaxAndSkipEnv (max sur N = 4, corrige le scintillement Atari), EpisodicLifeEnv (une
vie perdue termine l'épisode, raccourcit et accélère), FireResetEnv (certains jeux ne démarrent
pas sans FIRE), WarpFrame/ProcessFrame84 (niveaux de gris, 84×84), ClipRewardEnv (−1…1, unifie
le −21…21 de Pong et le 0…∞ de River Raid), FrameStack (N = 4, REQUISE pour la propriété de
Markov, une trame ne donne pas le sens du mouvement de la balle) (300) → la liste de §7.6, en
français et SANS les noms de classes de la pile, qui ne sont pas du vocabulaire du cours ;
enveloppes de Stable Baselines3 recommandées, fork d'OpenAI Baselines, « mais ne prenez pas ce
code pour une vérité définitive, votre environnement peut avoir d'autres exigences » (300) → la
mention de l'outil est permise (D18 ne couvre pas les outils) ; L'OBSERVATION CLÉ, les valeurs
par défaut ont été choisies pour entraîner sur les 50+ jeux de la suite Atari 2600, donc pour UN
jeu plusieurs sont du poids mort (300) ; les trois retouches, NoopResetEnv désactivée, saut de
quatre trames SANS max, deux trames empilées au lieu de quatre, appliquées PAR-DESSUS les deux
accélérations précédentes (301) ; l'optimisation périmée, pillow-simd contre OpenCV2 valait
~50 FPS avant 2020 et ne vaut plus rien, le redimensionnement d'OpenCV2 ayant été optimisé
(301) → encadré [!TIP] sur la péremption d'un résultat de profilage ; L'EXPÉRIENCE À UNE TRAME,
Pong encore résolu avec --stack 1 mais beaucoup plus long et instable, 3 exécutions sur 8 n'ont
PAS convergé, conclusion : Pong à une trame n'est probablement pas un PDM partiellement
observable mais l'efficacité souffre (302) → §7.6 sous-section propre, et SECOND EXEMPLE TRAVAILLÉ
du jalon (une moyenne sur 8 cache 37 % d'échecs) ; FireResetEnv justifiée dans la source par un
argument faux (impossible de converger) que p.302 contredit → §7.6 encadré [!NOTE] : on garde
l'enveloppe, on change la raison (pitfall 11 des notes) ; TABLEAU 9.1 transcrit intégralement
(302) → Tableau 7-1 en Markdown, avec les six lignes et les quatre colonnes, les tirets de
cellule vide remplacés par « aucun » (D37 : aucun tiret cadratin dans la page) ; EQ 07-E4 pour
les deux colonnes Δ, écrite directement, avec la convention de signe explicitée ; la lecture du
tableau, plus haut FPS (448, +95,6 %) = presque le pire gain de temps (−9,2 %), meilleur temps
(30,0 min, −42,5 %) à 325 FPS (302) ; FPS de référence cité 227 (294), 228 (299) et 229 (table),
LA TABLE FAIT FOI et l'écart est lui-même la preuve de l'exigence de graines.

FIG 07-03 est une FIGURE PRODUITE PAR LE COURS, pas une extraction : le nuage de points du
Tableau 7-1 dans le plan (FPS, temps à la résolution). Les notes de phase 1 la proposent en
gap 6 (« si la moitié accélération a besoin d'un second visuel »), et elle est retenue parce que
le ch. 9 n'a aucune illustration autre que la paire 9.6/9.7, toutes ses autres figures étant des
courbes de récompense ou de FPS exclues par la règle des semaines 2 et 3, et parce que le propos
de §7.6 est une lecture BIDIMENSIONNELLE d'un tableau : le nuage rend l'argument immédiat.
Provenance de la donnée : LAPAN table 9.1 p.302.

LAPAN ch. 10 « Stocks Trading Using RL » : objectif annoncé, appliquer le DQN du ch. 6 et les
extensions du ch. 8, IMPLÉMENTER UN ENVIRONNEMENT GYM PROPRE simulant le marché, entraîner un
agent à maximiser son profit (304) → §7.7 ; la modestie assumée de l'objectif, aucune promesse
d'enrichissement, but « beaucoup moins ambitieux : montrer comment aller au-delà des jeux
Atari » (304) → §7.7, reformulé en voix du cours, SANS guillemets ni attribution (D45) ; la
portée du mot trading, marchandises, actions, devises, jusqu'aux DÉRIVÉS CLIMATIQUES pour une
entreprise dont le revenu dépend de la météo, et les trois finalités, profit / couverture /
besoin (acheter de l'acier, échanger des USD contre des JPY) (304-305) ; le problème est ancien
et encombré, consultants, fonds, banques et particuliers (305) → §7.7, avec la conséquence
ajoutée par le cours (les bonnes méthodes ne sont pas publiées, une régularité exploitée
disparaît) ; le cadrage AR en une ligne, observer, décider acheter/vendre/attendre (305).

§7.8 repose sur 305-307 et 315 : LA PHRASE-THÈSE de la seconde moitié, « pour formuler un
problème d'AR il faut trois choses, observation, actions possibles, système de récompense ; dans
les chapitres précédents les trois nous étaient données et la mécanique interne était cachée ;
nous sommes maintenant dans une situation différente » (305) → §7.8 premier paragraphe,
reformulé sans aucune mention de la structure de la source (D17/D18 : le cours a des semaines) ;
la récompense « n'est pas donnée par un ensemble de règles strictes, elle est guidée par notre
ressenti et notre connaissance du domaine » (305) ; la flexibilité bonne ET mauvaise, on peut
ajouter nouvelles et statistiques, mais trouver un bon agent demande d'essayer de nombreuses
représentations « et il n'est pas toujours évident laquelle marchera mieux » (305) ;
OBSERVATION = N dernières barres (open, high, low, close), drapeau d'achat, profit/perte courant
(306) ; ACTIONS = ne rien faire / acheter (sans effet si déjà en position, sinon commission) /
clôturer (sans effet sans position, sinon commission) (306) → la remarque sur les actions
INVALIDES SILENCIEUSES et leur coût d'apprentissage est l'ajout du cours ; RÉCOMPENSE en deux
variantes, répartie sur la détention ou versée en bloc à la clôture (306) → EQ 07-E8 et 07-E9 ;
le commentaire de la source, « au premier regard les deux devraient donner le même résultat
final, peut-être avec des vitesses de convergence différentes ; en pratique la différence peut
être dramatique » (306) → §7.8, AFFÛTÉ et non recopié.

CORRECTION PORTÉE PAR LES NOTES ET APPLIQUÉE ICI. Le résumé de chapitre affirmait que le schéma
par barre « ne crédite jamais la barre de clôture ». C'EST FAUX, la passe de lecture a vérifié la
branche sur l'image de p.315 et le résumé a été corrigé en conséquence : le drapeau de position
est remis à faux AVANT le bloc par barre, et les deux schémas couvrent donc le MÊME intervalle de
prix. §7.8 écarte explicitement cette fausse piste, puis donne les TROIS vraies raisons, et §7.10
pointe l'ordre des opérations dans pas() comme l'endroit exact où une erreur d'une ligne casse
cette propriété. Les trois raisons : (1) ARITHMÉTIQUE, une somme de rendements simples n'est pas
le rendement composé, EQ 07-E10, exemple 20 points contre 21 sur deux barres à +10 % ;
(2) ACTUALISATION, γ^T sur une somme unique contre une actualisation terme par terme, donc des
G_t différents même à totaux non actualisés égaux, avec la conséquence comportementale (le
schéma A incite à clôturer tôt), qui est l'ajout du cours ; (3) ATTRIBUTION DU MÉRITE ET
VARIANCE, dense contre parcimonieux, avec le rappel de FrozenLake en semaine 3.

Représentation des prix (306) : le souhait d'un agent indépendant du niveau absolu, « l'action a
monté de 1 % pendant la dernière barre », la raison (des titres de prix différents aux motifs de
mouvement semblables), la discipline nommée ANALYSE TECHNIQUE, la décision de convertir chaque
barre en TROIS nombres, haut/bas/clôture en pourcentage de l'ouverture → EQ 07-E6, dont la forme
exacte est recouvrée du listing _cur_close() p.314 LU SUR L'IMAGE (c = o(1 + c_rel)), le
chargeur relatif n'étant jamais montré (gap 4 des notes : le cours définit la transformation) ;
LE COÛT de cette décision, énoncé par la source, la perte des NIVEAUX DE PRIX REMARQUABLES, les
marchés rebondissant sur les nombres ronds (exemple des 70 000 $ par bitcoin) et sur les points
de retournement passés (306) ; et la remarque que le réseau « pourrait l'apprendre seul, il
suffit de soustraire le prix moyen », la forme relative SIMPLIFIANT la tâche (306) → la
normalisation présentée comme un A PRIORI et rattachée au biais inductif de la semaine 2.

§7.9 repose sur 307-308 pour les données et sur 318 et 324 pour le protocole : marché russe
2015-2016, archive à décompresser (307) ; BARRES M1, une ligne CSV par minute, quatre prix,
Open (début), High (max), Low (min), Close (dernier), l'intervalle s'appelle une BARRE (307) ;
en-tête <DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL> et la ligne d'exemple 20160104,100100,
1148.90000 ×4, 0, fichier de référence de 130k lignes pour une année d'un titre (307) → le bloc
`text` de §7.9, et la LECTURE de cette ligne (quatre prix identiques, volume nul : une minute
sans échange) est l'ajout du cours ; VOLUME = nombre d'ordres d'achat et de vente pendant la
barre, interprétation dépendante du marché, indique l'activité (307) ; affichage usuel en
graphique en chandeliers, fig. 10.1 p.308 = un mois de cotations (307-308) → FIG 07-04, mais
PRODUITE ET NON RECADRÉE : la planche est petite, en niveaux de gris, et son axe des abscisses
est un index de barres non étiqueté ; un schéma annoté d'UNE barre OHLC enseigne davantage, et
les étiquettes y portent l'enseignement, ce qui est le seul cas où le projet produit une figure
(D19). Le recadrage de fig. 10.1 p.308 reste la solution de repli, consignée dans
extraction/week-07.md ; l'archive contient DEUX fichiers, 2016 et 2015 (308).

LE PROTOCOLE DE VALIDATION EST CELUI DU COURS, ET IL EST PRÉSENTÉ SANS AUCUNE MENTION D'UNE
SOURCE QUI FERAIT AUTREMENT (D17, D18, D45 ; pitfall 1 du dossier et des notes). Règle : partage
CHRONOLOGIQUE, ajustement sur la période la plus ancienne, validation sur la plus récente, donc
ici entraînement sur 2015 et validation sur 2016. Les trois conséquences d'un partage inversé
(mauvaise question, fuite par le régime et par l'EXPÉRIMENTATEUR, indétectabilité dans les
métriques), la généralisation hors finance (capteurs, suivi clinique, demande, trafic, jamais
mélanger ni partager au hasard une série temporelle), les trois blocs chronologiques avec un bloc
de test touché une seule fois, et la validation glissante comme version honnête, sont tous écrits
par le cours. Le seul ancrage de source est l'argument du troisième bloc, « choisir le modèle sur
les données de validation ruine l'idée de validation » (324), et la note opérationnelle que le
script prend déjà --data et --val, donc que le protocole ne coûte AUCUNE ligne de code (318). Le
piège de l'évaluation sur les données d'entraînement à ε = 0 avec offset aléatoire dans la MÊME
année est ancré sur 312 et 320 → §7.9 encadré [!WARNING] final.

§7.10 repose sur 308-316 : StocksEnv suit la classe Env de Gym et délègue son état à des
classes internes, le bénéfice étant de « se brancher sur les classes familières utilisées pour
Atari » (308, 316) ; défauts de module, 10 barres et 0,1 % de commission (308-309) ; actions en
énumération, Skip = 0, Buy = 1, Close = 2 (309) ; MODÈLE DE MARCHÉ DÉLIBÉRÉMENT RÉDUIT, une
seule action, pas d'extension de position, PAS DE VENTE À DÉCOUVERT, décision intentionnelle de
simplicité (309) → encadré [!NOTE], avec la conséquence ajoutée par le cours (l'agent ne peut
gagner qu'en marché haussier) ; deux chemins de construction, from_dir ou dictionnaire de Prices,
et un Prices = cinq tableaux NumPy 1-D (309) ; LES SEPT PARAMÈTRES DE COMPORTEMENT (310-311) →
le tableau de §7.10, avec trois commentaires développés (fin d'épisode à la clôture ⇒ la longueur
d'épisode EST la durée de détention, utilisé en §7.12 ; représentation 1-D ⇒ « le même sens que
les plans de couleur des images Atari » ; volumes désactivés par défaut) ; PIÈGE DE NOMMAGE
(pitfall 10) : la source documente conv_1d dans la prose et dans fig. 10.2 mais nomme state_1d
dans la signature, et les défauts de State (reward_on_close=True, volumes=True) sont l'INVERSE de
ceux de StocksEnv (False, False), qui les passe toujours explicitement ; le cours emploie UN SEUL
nom, « représentation 1-D », et énonce les défauts UNE FOIS, ceux de StocksEnv ; espaces
Discrete(len(Actions)) et Box(-inf, +inf, shape=state.shape, float32), BOÎTE NON BORNÉE, rien ne
normalise au niveau de Gym (311, image) ; fig. 10.2 p.311 → FIG 07-05, et la légende doit dire
que le vecteur dessiné inclut le volume alors que le défaut est de l'exclure ; reset() tire
l'instrument puis l'offset, np_random.choice(len(high) − bars·10) + bars (312) → EQ 07-E13 ;
step() en habillage mince, le 5-tuple de Gymnasium, info porte instrument et offset (312) ;
render() NON IMPLÉMENTÉE, la source note qu'un environnement de marché pourrait tracer les prix
pour déboguer (312) → extension facultative du volet B ; State garde ses arguments
(bars_count > 0, commission_perc >= 0) et tient la position en deux champs, have_position et
open_price (313) → §7.10 « la seule chose qui rend ce problème markovien », avec l'argument des
deux instants t1/t2 écrit par le cours ; taille d'observation 3·bars + 1 + 1, commentaire du
listing [h, l, c] * bars + position_flag + rel_profit, donc 32 nombres par défaut (313) →
EQ 07-E12 ; encode() parcourt bar_idx de −bars+1 à 0, puis drapeau, puis profit relatif, 0,0 sans
position et _cur_close()/open_price − 1,0 sinon (314, image) → EQ 07-E7 ; _cur_close() =
open·(1 + rel_close), seul endroit qui fixe ce que « relatif » veut dire (314, image) → EQ 07-E6 ;
step() branche par branche, Buy sans position (have_position = True, open_price = close,
reward −= commission), Close avec position (reward −= commission, done |= reset_on_close, et si
reward_on_close alors reward += 100·(close/open_price − 1), position effacée), puis toujours
_offset += 1, prev_close = close, close = _cur_close(), done |= _offset >= len − 1, et si une
position est ENCORE détenue et reward_on_close faux, reward += 100·(close/prev_close − 1)
(314-315, image) → le fragment de code de §7.10, réécrit en français (D15 : le code est réécrit,
jamais recopié) ; L'UNITÉ EST LE POINT DE POURCENTAGE à cause du facteur 100, et un aller-retour
sans mouvement rend exactement −0,2 (314-315 et 322) → EQ 07-E11, qui sert de seuil en §7.12 ;
L'APPROXIMATION NOMMÉE, « exécution instantanée au prix de clôture de la barre courante, qui est
une simplification de notre part ; normalement un ordre peut s'exécuter à un autre prix, ce qu'on
appelle le dérapage des prix » (315) ; State1D ne redéfinit QUE la représentation, forme (5, bars)
ou (6, bars), lignes hauts/bas/clôtures/volumes puis position et profit relatif, même
comportement et même récompense (316) → le dernier paragraphe de §7.10, qui est la formulation du
vrai sujet de la moitié.

§7.11 repose sur 316-319 : deux architectures, toutes deux DUALES, entraînées en DOUBLE DQN
avec dépliage de Bellman à DEUX étapes, « le reste du processus est celui d'un DQN classique »
(316) ; SimpleFFDQN, deux branches INDÉPENDANTES depuis l'observation plate, chacune
Linear(obs, 512) → ReLU → Linear(512, 512) → ReLU → Linear(512, ·), valeur à 1 sortie et avantage
à actions_n, recombinées par val + (adv − adv.mean(dim=1, keepdim=True)) (317) → EQ 07-E14 ;
DQNConv1D, extracteur partagé Conv1d(shape[0], 128, 5) → ReLU → Conv1d(128, 128, 5) → ReLU →
Flatten, taille aplatie obtenue par un passage avant à blanc, puis deux têtes
Linear(size, 512) → ReLU → Linear(512, 1 | actions_n) (317-318) ; réglages d'entraînement, ε
linéaire de 1,0 à 0,1 sur le premier million de pas, tampon 100k pré-rempli de 10k, valeur
moyenne d'un ensemble fixe d'états témoins toutes les 1 000 étapes, validation toutes les 100k
étapes sur 100 épisodes, sur les données d'entraînement ET sur des cotations inédites, en
journalisant profit moyen, nombre de barres et part du temps en position (318) ; deux scripts
d'entraînement aux mêmes options, --data, --val, -r (318-319) → la note de §7.9 sur le coût nul
du protocole. LE POINT D'ENSEIGNEMENT DE LA SECTION EST SA PROPRE PLATITUDE, et il est dit
explicitement, comme les notes le demandent.

§7.12 repose sur 319-325 : sur les données d'entraînement, la récompense moyenne croît
« lentement mais régulièrement », le rythme ralentit après 300k épisodes, courbes brutes et
lissées par une moyenne mobile simple sur 15 points (319) ; seconde paire de courbes sur les
MÊMES données d'entraînement sans actions aléatoires (ε = 0), même conclusion (320) ; LA LONGUEUR
DES ÉPISODES AUGMENTE après 100k épisodes, interprétée comme l'agent apprenant que garder
l'action peut être rentable (320) → §7.12, avec le rappel que la longueur EST la durée de
détention sous reset_on_close ; la valeur prédite sur l'ensemble fixe d'états ne cesse de monter,
« le réseau devient de plus en plus optimiste » (321) ; LE RETOURNEMENT, « tout cela a été obtenu
sur les données d'entraînement… mais est-ce que cela marchera sur des données jamais vues ? », la
récompense de validation SANS TENDANCE HAUSSIÈRE et sa version lissée qui DÉCROÎT après la
première heure, au moment même où la longueur d'épisode d'entraînement avait sauté (321) → la
coïncidence temporelle est présentée comme LE diagnostic ; surapprentissage daté, à partir de
1 M d'itérations, et pendant les 4 PREMIÈRES HEURES la récompense de validation reste au-dessus
de −0,2 %, qui est exactement la commission d'un aller-retour, d'où « mieux qu'un singe qui
achète et vend au hasard » (322) → §7.12, et LE COURS DIT QUE CE REPÈRE NE VAUT PRESQUE RIEN
(pitfall 7) ; sauvegarde des modèles sur DEUX critères, record de Q moyen sur les états témoins
OU record de récompense de validation, le second rendant l'aveu final nécessaire (322) ;
run_model.py rejoue un modèle sur un fichier de cotations et trace le profit cumulé en pourcent,
options -d, -m, -b (doit correspondre à l'entraînement, défaut 10), -n, --commission (défaut
0,1 %), et C'EST --commission QUI REND L'EXPÉRIENCE DE COÛT POSSIBLE (322).

LA PAIRE DE COMMISSION, QUI EST LE CŒUR DE §7.12 ET UNE EXIGENCE DU DOSSIER (pitfall 5). Fig.
10.8 p.322, LUE SUR L'IMAGE : panneau gauche, année d'entraînement, profit cumulé presque
monotone jusqu'à ≈ +150 % sur ~31 000 barres ; panneau droit, année tenue à l'écart, chute
jusqu'à un creux ≈ −80 % vers la barre 17 000 et fin ≈ −60 % → FIG 07-06, et les trois nombres
sont DANS LA PROSE, la prose de la source ne donnant que « bien pire ». Fig. 10.9 p.323, LUE SUR
L'IMAGE : même modèle, même année tenue à l'écart, --commission 0.0, oscillation entre ≈ −10 % et
+15 % sur les 20 000 premières barres puis fin ≈ +48 % → FIG 07-07, AJOUTÉE par la passe de
lecture et extraite EN PAIRE avec 07-06 : montrer l'une sans l'autre enseigne le contraire de ce
qu'il faut. La lecture de la source est conservée dans ses DEUX moitiés, « sans commission notre
agent peut être rentable » ET « bien sûr, la commission n'est pas le seul problème, notre
simulation d'ordres est très primitive et ignore l'écart de prix et le dérapage » (323).
L'ARITHMÉTIQUE QUI REND LA PAIRE ENSEIGNABLE est l'ajout du cours : 0,1 % par jambe, 0,2 % par
aller-retour, l'écart entre ≈ +48 % et ≈ −60 % sur la même année avec les mêmes poids est le COÛT
CUMULÉ DE SA PROPRE FRÉQUENCE, la stratégie échouant non pas parce qu'elle prédit mal mais parce
qu'elle n'est pas assez rentable PAR OPÉRATION ; et la généralisation, un terme de coût peut
INVERSER LE SIGNE d'un résultat sans changer la politique, d'où l'encadré [!WARNING] et ses
exemples hors finance.

Fig. 10.10 p.323 a été LUE SUR L'IMAGE et VOLONTAIREMENT NON EXTRAITE : ses nombres sont portés
en prose dans §7.12 (modèle choisi sur la meilleure récompense de validation, commission active,
entraînement terminant ≈ +33 % après un pic ≈ +55 %, validation terminant ≈ −10 % après un creux
≈ −38 %), une troisième paire de courbes de profit quasi identiques diluerait la paire 07-06 /
07-07. L'AVEU, « prendre le meilleur modèle d'après les données de validation est tricher ; en
utilisant les résultats de validation pour la sélection, nous ruinons l'idée de validation ; ces
courbes montrent seulement qu'il EXISTE des modèles qui marchent à peu près sur des données
inédites » (324) → §7.12 troisième sous-section, reformulé, et la règle propre (sélectionner sur
validation, rapporter sur un test jamais utilisé pour sélectionner) est la formulation du cours,
annoncée dès §7.9. Le modèle à convolution, fenêtre de contexte élargie sans forte croissance du
réseau, défaut 50 barres au lieu de 10, dynamique « presque identique », récompense de validation
LÉGÈREMENT supérieure, surapprentissage PLUS TARDIF (324) → la « bonne taille de conclusion »
donnée en modèle aux étudiants.

§7.13 repose sur 325-326 : le cadrage, « utiliser l'AR pour créer une stratégie complète et
rentable est un grand projet qui peut demander plusieurs mois de travail dédié » (325) ; la
représentation « assurément imparfaite », ni niveaux de support et de résistance, ni valeurs
rondes, ni autre information de marché (325) ; PLUSIEURS ÉCHELLES DE TEMPS, les barres d'une
minute sont bruyantes, « comme regarder le marché au microscope », les barres horaires ou
journalières montrent les tendances longues, un agent pourrait regarder plusieurs échelles à la
fois (transformeurs, attention, longues fenêtres de contexte) (325) ; DAVANTAGE DE DONNÉES, le
plus fort des cinq, une année d'un titre = 130k barres « peut-être insuffisant pour capturer
toutes les situations de marché », un agent réel voudrait des centaines de titres sur dix ans ou
plus (325) → §7.13, où le cours RELIE explicitement ce chantier au surapprentissage de §7.12 ;
architecture ouverte, nombre de couches, taille de noyau, connexions résiduelles, attention (325)
→ et la remarque du cours que c'est le chantier le moins prometteur quand la limite est la
quantité de données ; l'analogie avec le traitement du langage, deux domaines de séquences de
longueur variable produites par des humains, des barres tokenisables (« monté de 1 % » → jeton A)
et des plongements applicables (325) ; clôture de la partie 2, la partie 3 ouvre sur les gradients
de politique, REINFORCE et A3C (326) → la transition vers la semaine 8, QUI N'EST PAS DÉPENSÉE
ICI. Les trois coûts absents (écart achat-vente, dérapage, impact de marché) sont rassemblés et
définis par le cours à partir de 315, 323 et 325 ; l'écart achat-vente et l'impact de marché ne
sont que NOMMÉS dans la source, leur définition est écrite par le cours.

LABORATOIRE (COURSE-PLAN §9.2, plus les ancrages ci-dessus). Volet A : protocole en quatre
étapes, seuil et indicateurs fixés AVANT, référence sur k graines, UNE modification à la fois,
tableau de la forme du Tableau 7-1. Les trois modifications sont celles des notes (no_grad sur
les deux usages sans gradient, N environnements vectorisés, la couche que personne ne profile),
la troisième étant ADAPTÉE à CartPole, qui n'a pas de pile Atari à alléger : chronométrage par
couche puis attaque de la plus grosse part. Volet B : écrire l'environnement et le TESTER SANS
RIEN ENTRAÎNER, les quatre assertions des notes reprises telles quelles (aller-retour à −2κ,
rendement pur à 100(c1/c0 − 1) sous κ = 0, les deux schémas qui diffèrent au second ordre,
3b + 2 composantes dont la dernière nulle hors position). Deux extensions facultatives :
render(), qui n'existe pas dans la source, et l'ACHAT-CONSERVATION, qui n'existe nulle part dans
le corpus (gap 3) et dont la définition et le protocole sont écrits par le cours. Colab : le volet
A tourne comme écrit PARCE QUE le T4 est contraint ; le volet B reçoit le JEU DE DONNÉES FOURNI,
et l'étudiant n'a aucune donnée de marché à aller chercher.

JALON 2 (25 %), dont le contenu de cette page est destiné à week07/jalon-2.md. Livrables et
critères : COURSE-PLAN §10 et la page squelette du module. Les huit éléments du barème
reprennent les huit points de matière des notes, ramenés à des lignes évaluables et totalisant
25 points. LA MÉTHODE DE COMPARAISON N'EXISTE NULLE PART DANS LE CORPUS (gap 1) : les deux
chapitres motivent parfaitement l'exigence (287-288, 302) mais ne donnent AUCUNE procédure, pas
de formule d'intervalle, pas de nombre de graines. EQ 07-E5 et le protocole de §7.2 sont donc
écrits par le cours, sans attribution, et c'est assumé. LE CONFLIT DE BUDGET (gap 2) EST TRANCHÉ
EXPLICITEMENT DANS LES CONSIGNES, comme la semaine 6 l'avait fait : l'étude comparative tourne
sur CartPole, plusieurs graines par variante, et l'accélération se mesure sur ce que l'étudiant
profile lui-même ; une exécution à l'échelle d'Atari ne rapporte aucun point. Sans cette
décision écrite, l'exigence de graines serait silencieusement ignorée. Les deux exemples
travaillés offerts à l'étudiant sont ceux des notes : la ligne sans no_grad (deux indicateurs qui
se contredisent sur un écart plus petit que la dispersion) et les 3 échecs sur 8 à une trame
empilée (une moyenne qui cache 37 % d'échecs). La continuité de ton avec le jalon 1 est tenue :
une mesure, une déduction, une conclusion, pas de récit chronologique.

CE QUE LA SEMAINE N'A PAS UTILISÉ, et pourquoi. Les figures 9.1 à 9.5, 9.8 à 9.10, 10.3 à 10.7,
10.11 et 10.12 sont exclues par la règle des semaines 2 et 3 (courbes de récompense ou de FPS
que le laboratoire fait produire à l'étudiant). Fig. 10.10 est exclue avec ses nombres conservés
en prose. Le chunk ch.08-03 sur le réglage d'hyperparamètres par recherche automatique est hors
sujet (le dossier : ce n'est pas du profilage) et n'a pas été lu. Les détails de nommage de la
bibliothèque de la semaine 6 (classes PTAN) ne reparaissent pas : D12 réserve PTAN à la semaine 6
comme objet d'étude. Et la section 7.5 s'arrête volontairement avant A3C.

DÉCOMPTE : 13 sections numérotées · 7 placeholders FIG (dont 2 figures produites par le cours)
· 0 placeholder EQ (14 équations, toutes écrites directement en KaTeX, 5 transcrites d'une image
de page vérifiée)
{{% /comment %}}
