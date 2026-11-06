---
title: "Semaine 6 : Bibliothèques haut niveau et extensions de DQN"
weight: 6
bookCollapseSection: true
---

# Semaine 6 : Bibliothèques haut niveau et extensions de DQN

Sixième semaine, et c'est une semaine de réparations. La semaine 5 s'était terminée sur une liste de cinq défauts du réseau Q profond, et celle-ci les répare tous les cinq, chacun par une méthode qui porte un nom, qui a été publiée et mesurée, et que vous allez implémenter. La semaine a une forme inhabituelle, annoncée dès l'introduction : sa première moitié n'enseigne aucune méthode, elle pose une question d'ingénierie, celle des **bons objets**, et y répond en lisant une bibliothèque spécialisée pour la seule fois du cours. La seconde moitié a besoin de la première, parce qu'une réparation ne tient en une ligne que si la pièce qu'elle remplace était une pièce, et parce que quatre variantes ne deviennent comparables que si elles partagent un socle de code unique.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** les cinq réparations du réseau Q profond ne sont pas cinq nouveaux algorithmes, ce sont cinq corrections locales, chacune située à un endroit différent du même programme, et c'est pour cela qu'elles s'empilent.

---
## Description générale

Les sections 6.1 à 6.5 posent la question des objets, et elles la posent en ingénieur. La section 6.1 compte ce que cinq semaines de réécriture de la même boucle ont coûté, et nomme la raison pour laquelle cette répétition n'est pas un accident de style : la **généralité** des méthodes d'apprentissage par renforcement. La section 6.2 donne la liste à retenir, cinq objets et, pour chacun, une phrase disant ce qu'il retire des mains de celui qui écrit le code : un sélecteur d'actions, un agent, une source d'expérience, un tampon de rejeu, un réseau cible. La section 6.3 ouvre le plus important des cinq, la **source d'expérience**, et détaille les sept gestes qu'une seule itération cache, dont celui que presque tout le monde écrit mal la première fois, l'émission de la queue des sous-trajectoires en fin d'épisode ; elle isole surtout la **transition premier-dernier**, où la récompense est déjà accumulée et où le cas terminal est encodé par l'absence d'état final. La section 6.4 reprend le réseau cible de la semaine 5 et lui ajoute la **synchronisation douce**, avec la conversion entre les deux conventions de son coefficient, dette payée d'avance pour la semaine 11. La section 6.5 est la charnière de la semaine : un **socle commun**, hyperparamètres compris, sans lequel une étude d'ablation ne mesure rien du tout.

Les sections 6.6 à 6.10 sont le catalogue des réparations, et elles ne suivent pas l'ordre de la liste de la semaine 5 : elles vont de la moins intrusive à la plus intrusive, et chacune rappelle dans son titre le défaut auquel elle répond. La section 6.6 déplie l'équation de Bellman sur \(n\) pas, montre sur une chaîne de quatre états pourquoi l'information remonte plus vite, puis fait payer ce dépliage, qui rend la méthode à moitié sur politique et tire en sens contraire du tampon de rejeu ; son implémentation tient en deux paramètres, dont le second, \(\gamma^n\) au lieu de \(\gamma\), est le piège le plus coûteux de la semaine. La section 6.7 démontre le **biais de maximisation** sur un exemple à deux états, sépare le choix de l'action de son évaluation, écrit la cible du **double DQN** et, surtout, donne le protocole qui rend la surestimation visible : mille états témoins, et une moyenne tracée pendant l'entraînement. La section 6.8 décompose \(Q = V + A\) dans l'**architecture duale** et insiste sur ce qui fait réellement la méthode, la **contrainte de moyenne nulle** sans laquelle la décomposition n'est pas identifiable. La section 6.9 supprime le calendrier de \(\varepsilon\) en le remplaçant par des **réseaux bruités**, qui apprennent l'amplitude du bruit et non son ciblage, et dont le mode évaluation coupe l'exploration. La section 6.10 rend le tirage du tampon proportionnel à la surprise, paie le biais ainsi créé par des poids d'échantillonnage préférentiel, et oblige à écrire la perte quadratique à la main.

Les sections 6.11 et 6.12 referment la semaine. La section 6.11 empile les réparations, dit où chacune intervient et pourquoi elles se composent, puis donne l'honnêteté qui va avec : la combinaison de référence n'en retient que quatre, et le système obtenu est **plus lent** que l'agent ordinaire. La section 6.12 ouvre sur l'apprentissage par renforcement distributionnel avec deux trajets de même moyenne, et s'arrête à l'équation de Bellman écrite sur des distributions, sans en demander l'implémentation. Le laboratoire est **formatif**, puisque la semaine 6 ne porte aucun jalon, mais son volet évalué est la moitié du jalon 2 de la semaine prochaine : cinq volets sur un socle unique, une prédiction de trace sans entraînement, la référence sur CartPole, puis l'**ablation à quatre variantes sur trois graines** qui est l'exercice corrigé, deux protocoles de mesure pour rendre visibles la surestimation et la contrainte duale, et un volet facultatif sur les deux réparations les plus intrusives. Trois fois dans la semaine, une comparaison change de conclusion selon l'unité choisie : retenez la question, plus rapide en quoi ?

---
## Mots-clés de la semaine

sélecteur d'actions · source d'expérience · transition premier-dernier · synchronisation douce · socle commun · étude d'ablation · DQN à n étapes · déroulement de l'équation de Bellman · efficacité d'échantillon · sur politique et hors politique · double DQN · biais de maximisation · surestimation des valeurs d'action · architecture duale · avantage · contrainte de moyenne nulle de l'avantage · réseaux bruités · bruit gaussien factorisé · rapport signal sur bruit · tampon de rejeu priorisé · priorité d'un échantillon · poids de correction du biais · échantillonnage préférentiel · arbre de segments · apprentissage par renforcement distributionnel · équation de Bellman distributionnelle · Rainbow

---
## En prévision de la semaine suivante

Nous avons passé la semaine à améliorer la **méthode**, et nous terminons avec un agent qui demande encore des centaines de milliers de trames et dont le débit a baissé. La semaine 7 attaque donc l'autre moitié du problème : améliorer les performances **sans toucher à la méthode**. Vous y verrez pourquoi un agent qui joue dans un seul environnement à la fois gaspille son processeur graphique, comment les environnements vectorisés de Gymnasium, déjà aperçus sous la source d'expérience de la section 6.3, suppriment ce gaspillage, et comment on **profile** une boucle d'entraînement pour savoir où le temps part réellement, ce qui n'est presque jamais là où l'on croit. Puis nous appliquerons tout le module à une étude de cas complète, un agent de négociation sur des données financières, où l'ingénierie de l'état et de la récompense compte davantage que le choix de l'algorithme. La semaine 7 clôt le module 2 et porte le **jalon 2**, dont le volet C de cette semaine est la moitié déjà faite.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (D35). Imprimé = PDF − 31 pour LAPAN et PDF − 22 pour SB,
conformément à MAP-lapan.md et MAP-sb.md, comme dans le dossier et les notes de phase 1.
Toutes les pages citées ci-dessous sont des indices PDF.

SEMAINE À DEUX CHAPITRES ET DEUX MÉTIERS. Le chapitre 7 est une bibliothèque, lue comme objet
d'étude et jamais adoptée (D12 : PTAN paraît cette semaine et plus jamais) ; il porte les
sections 6.1 à 6.4. Le chapitre 8 est un catalogue de réparations ; il porte les sections 6.5 à
6.12. Une seule source extérieure au supplément principal intervient, et sur une seule
section : SB ch. 6 §6.7 fournit la preuve du biais de maximisation que le chapitre 8 refuse
explicitement de donner, et sans elle la section 6.7 n'aurait pas de moitié formelle (D10).
La jonction avec la semaine 5 est la colonne vertébrale de la semaine : les cinq défauts de
§5.9 sont repris dans l'ordre de la semaine 5 en introduction, puis réordonnés pour
l'enseignement, et le réordonnancement est annoncé et non caché.

LAPAN ch. 7 « Higher-Level RL Libraries » : les ~200 lignes d'entraînement plus ~50 lignes
d'enveloppes du DQN du ch. 6, « utile pendant qu'on apprend » puis réécriture du même code,
répétition issue de la GÉNÉRALITÉ des méthodes (du code CartPole s'applique à Atari à peu de
retouches), code réutilisé mieux testé/lisible/documenté, et pip install ptan==0.8 (203) ;
les deux extrêmes, bibliothèque clé en main contre laquelle on se bat (OpenAI Baselines et
Stable-Baselines3 nommées, SEULE la seconde est reprise puisque le cours l'a déjà croisée en
semaines 3 et 5) et tout écrire soi-même, « error-prone, boring, and inefficient » (204) ;
la liste des entités, Agent / ActionSelector / ExperienceSource / ExperienceSourceBuffer /
utilitaires dont TargetNet, plus aides de boucle et enveloppes Gym (204) → TABLEAU des cinq
objets en 6.2, dont la dernière colonne (« son équivalent en semaine 5 ») est la lecture du
cours ; sélecteurs argmax pour les valeurs d'action et échantillonnage pour les politiques,
les trois classes, EpsilonGreedyActionSelector qui ENVELOPPE un autre sélecteur et porte
epsilon (205) ; selector.epsilon = 0.0 modifiable à l'exécution, « très commode quand on
recuit epsilon » (206, 209) → le « if random() < eps devenu un attribut » est la lecture du
cours, les deux moitiés ancrées ; le lot existe POUR LE GPU, « traiter plusieurs observations
en un passage est souvent bien plus rapide », et les trois variantes qui motivent la hiérarchie,
politique / état interne (POMDP nommé, non développé) / contrôle continu (207) ; DQNAgent rend
un COUPLE (actions, états internes), None pour un agent sans mémoire (209) ; PolicyAgent attend
des logits et apply_softmax=True pour la stabilité numérique, mentionné en une phrase comme
point de branchement de la semaine 8 (210) ; ce que la source d'expérience cache, plusieurs
environnements, prétraitement des trajectoires, environnements vectorisés de Gymnasium reportés
au ch. 17 donc SEMAINE 7, « a magic black box » (211) ; les trois classes, ExperienceSource avec
TOUS les pas intermédiaires, ExperienceSourceFirstLast « avec accumulation correcte de la
récompense entre les deux » et économie de mémoire en n étapes, et ExperienceSourceRollouts
pour A3C ch. 12 ; cette troisième classe est désignée sans être nommée, « rollout » étant déjà
fixé à « déploiement » depuis la semaine 1 et la collision inutile (211) ; l'environnement
jouet, observation 0→4, récompense = action, épisodes de 10 pas, DullAgent, toute sortie
prévisible (212) → VOLET A du laboratoire ; les SEPT gestes derrière une itération (213) ;
champs d'Experience dont done_trunc, un seul drapeau pour terminaison ou troncature, et tuples
PLUS COURTS que steps_count en fin d'épisode (214) ; plusieurs environnements servis à tour de
rôle et obligation d'INSTANCES INDÉPENDANTES, « sinon vos observations deviennent un désordre »
(215) ; la transition premier-dernier et sa motivation, « on veut des tuples (s,a,r,s') d'un
seul coup pour l'approximation de Bellman à un pas » et le repliement (premier état, action,
récompense totale sur n pas, état après n pas) (215) ; ses quatre champs, la récompense
PARTIELLE ACCUMULÉE et last_state = None si l'épisode est terminé (216) ; la trace avec
steps_count=2, récompense 2.0 la plupart du temps, puis 2.0 et 1.0 avec last_state=None en fin
d'épisode, la queue est payée, et « ces petits détails sont très faciles à implémenter de
travers » (217) → l'ENCADRÉ [!IMPORTANT] de 6.3, qui est la charnière encaissée en 6.6 ;
tampon de rejeu, échantillons corrélés « ce qui conduit à l'instabilité », hypothèse i.i.d. de
la SGD, trois implémentations derrière une interface (uniforme, priorisée naïve en O(n),
priorisée à arbres de segments « ce qui rend le code cryptique » en O(log n)) (217) ;
l'interface en trois choses, itération / populate(N) / sample(N), et la boucle DQN en cinq pas
« tout le reste se produit automatiquement » (218) → le FRAGMENT de cinq lignes de 6.2 ;
TargetNet « synchronise deux réseaux de même architecture », sync() copie et alpha_sync()
mélange, copie pour les actions discrètes « comme Atari et CartPole, comme au chapitre 6 »,
mélange pour le contrôle continu où « la transition entre les paramètres des deux réseaux doit
être lisse », et l'équation INLINE w_i = w_i·alpha + s_i(1−alpha) → EQ 06-E13, lue sur
index/pages/lapan/0219.png, page ABSENTE du dossier et rendue par la passe de lecture (219) ;
model (référence) et target_model (COPIE PROFONDE), tenseurs imprimés qui s'écartent après
net.ff.weight.data += 1.0 puis se réalignent après sync() (220) ; alpha_sync(0.1) sur cible
1,2039 et source 2,2039 donnant 2,1039, soit 0,1×1,2039 + 0,9×2,2039, DONC alpha pèse
l'ANCIENNE cible : vérifié arithmétiquement, et converti une fois dans l'encadré [!WARNING] de
6.4 en alpha_sync = 1 − tau, conformément à notation.md §6 et à concepts.yaml
(synchronisation-douce), pour que la semaine 11 n'hérite pas d'une contradiction silencieuse
(221). NON LUS et non enseignés : 07-08 (aides Ignite, plomberie de boucle autour d'une
bibliothèque que le cours n'adopte pas, 1 558 jetons) et 07-09 (panorama des autres
bibliothèques, 1 032 jetons) ; le solveur CartPole de PTAN (seuil 150, 2 000 à 3 000 itérations,
p.222-224) n'est connu qu'au niveau du résumé de chapitre et n'est PAS cité : il a servi à
dimensionner le laboratoire, pas à l'ancrer.

LAPAN ch. 8 « DQN Extensions » : les six améliorations de Rainbow avec le problème que chacune
adresse, n étapes (vitesse de convergence par dépliage, « et pourquoi ce n'est pas une solution
ultime »), double DQN (surestimation), réseaux bruités (exploration), rejeu priorisé (« pourquoi
l'échantillonnage uniforme n'est pas la meilleure façon de s'entraîner »), duel (architecture
plus proche du problème), catégoriel (au-delà d'une espérance unique) ; Rainbow, octobre 2017,
état de l'art sur Atari PAR LA SEULE COMBINAISON ; la date et le résultat sont repris, les
auteurs NON, D18 interdisant la référence visible (226) ; la justification de l'usage d'une
bibliothèque dans un livre qui apprend à tout écrire soi-même, « le but n'est pas d'apprendre à
utiliser les bibliothèques existantes mais de développer l'intuition et, s'il le faut,
d'implémenter de zéro… les bibliothèques passent », REFORMULÉE à la première personne de la
professeure en 6.1 et jamais citée : c'est exactement la justification de D12 (227) ;
Hyperparams en dataclass et l'entrée Pong, replay_size=100 000, replay_initial=10 000,
target_net_sync=1 000, epsilon_frames=100 000, epsilon_final=0,02, learning_rate=0,0001,
batch_size=32, gamma=0,99, epsilon_start=1,0, stop_reward=18,0 → TABLEAU de 6.5, et la
comparaison avec les neuf nombres de la semaine 5 est la lecture du cours (228) ; unpack_batch
range l'ÉTAT INITIAL dans last_states pour une transition terminale, « le résultat sera masqué
de toute façon », et l'alternative (ne calculer que les non terminales) « rendrait la logique
de la perte un peu plus compliquée » (229) → la sous-section « une astuce qui mérite d'être
comprise » ; calc_loss_dqn « presque identique au chapitre 6 » plus torch.no_grad() autour du
réseau cible, puis bellman_vals = next_state_vals.detach()*gamma + rewards_v et
nn.MSELoss() (229-230) ; EpsilonTracker.frame() → EQ 06-E15, identique à 05-E13, redonnée ici
parce que 6.9 la supprime ; batch_generator, populate(initial) une fois puis populate(1) et
yield sample() indéfiniment (230) ; les trois aides de suivi, EndOfEpisodeHandler et la
définition opérationnelle de « résolu », EpisodeFPSHandler et le débit « métrique de
performance importante à suivre », PeriodicEvents toutes les 100 itérations « sinon les
fichiers deviennent énormes » (231-232) ; LA RÉFÉRENCE DE LA SEMAINE, « environ 700K trames et
environ 400 parties pour atteindre une récompense moyenne de 18 » (239) : la source se
contredit (360 en p.240, 350 en p.254) et le cours retient 400, le nombre attaché à
l'exécution de référence sous les paramètres communs, l'écrit UNE FOIS en 6.5 et le réutilise
tel quel en 6.6, 6.7 et 6.9, sans jamais mentionner le désaccord, selon le précédent de la
semaine 5 ; la recherche d'hyperparamètres par 30 essais Ray Tune coûtant une journée de GPU
(240), citée seulement comme justification de l'encadré [!WARNING] de 6.5 qui interdit de
prendre les chiffres Atari pour des attentes : le chunk 08-03 (Ray Tune, recherche aléatoire,
arrêt précoce, 3 013 jetons) est DÉLIBÉRÉMENT NON LU, le réglage comme sujet appartenant à la
semaine 7 et le cours n'utilisant pas Ray.

n ÉTAPES (241-246) : provenance, travaux de 1988 sur la prédiction par différences temporelles,
reprise comme fait daté SANS référence (241) ; les trois formes du dépliage lues sur
index/pages/lapan/0241.png, page ABSENTE du dossier (le dossier ouvrait à 242, une page trop
tard) et rendue par la passe de lecture → EQ 06-E1 (cible à un pas, p.247), EQ 06-E2 (un
dépliage, max encore à l'intérieur) et EQ 06-E3 (après suppression du max intermédiaire) ;
06-E2 → 06-E3 EST l'approximation de la section et le cours le dit explicitement ; la chaîne
s1→s2→s3→s4 à une seule action, « même à un pas il faut trois pas pour propager les bonnes
valeurs », et les six mises à jour → FIG 06-01 et EQ 06-E5, présentées en TABLEAU à deux
colonnes (242) ; pourquoi pas 100 pas, la suppression du max suppose un comportement optimal
alors qu'il est aléatoire au début, « plus on déplie, plus la mise à jour peut être fausse », et
le tampon « augmente la chance d'obtenir des transitions issues de l'ancienne mauvaise
politique » → l'encadré [!IMPORTANT] de 6.6 qui ADMET que la réparation nº5 abîme la réparation
de la semaine 5 ; hors politique « ne dépend pas de la fraîcheur des données » contre sur
politique qui « dépend fortement » de l'échantillonnage selon la politique courante, et l'image
de la voiture autonome, REPRISE COMME IMAGE et réécrite en prose simple, hors guillemets (243) ;
« ce n'est pas noir ou blanc » et « être modeste dans le choix de n », 2 ou 3
« marchent généralement bien » (243-244) ; l'implémentation en deux lignes dont la seconde est
le piège, steps_count=n_steps et gamma=params.gamma**n_steps, « cette modification est vraiment
facile à oublier, ce qui peut nuire à la convergence » → l'encadré [!WARNING] le plus appuyé de
la semaine (244) ; n=3 « converge significativement plus vite », 4 moins, 5 et 6 moins bons
(245) ; table 8.1 après réglage, n=2 293 parties, n=3 260, n=4 290, n=5 268, n=6 261, n=7 284 →
le TABLEAU en U de 6.6 (246). EQ 06-E4, la forme générale avec la somme des gamma^k r, est
ÉCRITE PAR LE COURS : la source ne montre que le cas à un pas, un dépliage et une liste à deux
pas, le gamma^n venant du code. Marquée comme généralisation du cours dans extraction/week-06.md
et ancrée p.241-242 et p.244.

DOUBLE DQN (246-250) : la méthode nommée d'après ses auteurs dans la source, repris SANS les
noms ; le DQN de base « tend à surestimer les valeurs de Q, ce qui peut nuire à l'entraînement
et parfois mener à des politiques sous-optimales » (246) ; « la cause racine est l'opération max
de l'équation de Bellman, mais la preuve stricte est un peu compliquée » : LE MANUEL DÉCLINE LA
PREUVE, d'où l'ajout de SB ch.6 §6.7 au dossier par la passe de lecture (247) ; la cible
imprimée Q(s_t,a_t) = r_t + gamma·MAX_a Q'(s_{t+1}, argmax_a Q(s_{t+1},a)) est une ERREUR
D'AUTEUR, confirmée sur index/pages/lapan/0247.png : l'argmax fixe déjà une action, le max ne
porte donc que sur une valeur et l'indice a est lié deux fois. Le cours écrit la FORME CORRIGÉE
→ EQ 06-E6, sans max, et NE REPRODUIT PAS la forme imprimée, pas même pour la critiquer,
exactement comme les semaines 4 et 5 ont traité leurs erreurs d'auteur. Est également trop
forte l'affirmation voisine selon laquelle « les auteurs ont prouvé que cette simple retouche
corrige complètement la surestimation » : le résultat de non-biais invoqué porte sur le cas
BANDIT à deux estimations (SB p.157) et la figure 8.9 de la source elle-même montre une
RÉDUCTION (p.250). Le cours écrit « réduit », explique pourquoi la forme forte n'est pas
disponible (un réseau cible n'est pas une estimation indépendante) et ne dit jamais qu'une
source affirme autre chose (D17/D18) ; les trois lignes de code, net(next_states_v).max(1)[1]
pour l'INDICE et tgt_net(...).gather(1, ...) pour la VALEUR (248) ; le protocole des 1 000 états
tirés au hasard et de la moyenne périodique de max_a Q, RÉUTILISÉ au volet D du laboratoire
(248-249) ; « le DQN de base surestime les valeurs, qui redescendent donc après un certain
niveau ; le double DQN croît plus régulièrement » → FIG 06-03, et l'effet sur le temps
d'entraînement est faible, 412 parties après réglage, donc PIRE que la référence de 400 (250).

DUEL (264-268) : la décomposition Q = V + A comme définition, l'avantage « n'est que l'écart,
disant combien de récompense supplémentaire telle action apporte », de signe et d'amplitude
quelconques ; la contribution est « une séparation EXPLICITE de la valeur et de l'avantage DANS
L'ARCHITECTURE », stabilité, convergence, résultats Atari (264) ; deux chemins depuis le même
corps convolutif, un nombre unique V(s) d'un côté, un vecteur de la taille de l'espace
d'actions de l'autre → FIG 06-04 ; LE PARAGRAPHE D'IDENTIFIABILITÉ, qui EST la section : rien
n'empêche V(s)=0 et A=[1,2,3,4], « ce qui est complètement faux puisque le V(s) prédit n'est
pas la valeur espérée de l'état », et la contrainte de moyenne nulle donne V(s)=2,5 et
A=[−1,5, −0,5, 0,5, 1,5] → EQ 06-E8 (265) ; contrainte imposée par la perte ou, comme le fait
la publication d'origine, en soustrayant la moyenne DANS le réseau, « ce qui tire effectivement
la moyenne de l'avantage vers zéro » (265) ; nombre de paramètres maintenu constant en passant
la largeur cachée de 512 à 256 dans les deux chemins, d'où la comparaison ÉQUITABLE PAR
CONSTRUCTION ; le 512 → 256 est cité comme la valeur de l'architecture Atari, et le fragment de
6.8, qui est à l'échelle de CartPole, applique le même PRINCIPE avec des têtes moitié moins
larges que le corps, ce que le volet B fait vérifier par une assertion sur le nombre de
paramètres (266) ; le code return val + (adv − adv.mean(dim=1,
keepdim=True)), et la partie subtile est la dimension, « la moyenne selon la seconde dimension
du tenseur, ce qui produit un vecteur de l'avantage moyen pour chaque échantillon du lot » :
LE dim=1 EST le (1/N)·somme_k de l'équation, et le cours le dit sous cette forme (267) ;
convergence plus rapide que la référence, réglage sans gain, avantage moyen collé à zéro
pendant que la valeur croît, « conforme à nos attentes » → FIG 06-05 (267-268).

RÉSEAUX BRUITÉS (250-256) : « apprendre les caractéristiques de l'exploration pendant
l'entraînement au lieu d'avoir un calendrier séparé » (250) ; le défaut nommé par la source, la
décroissance classique de epsilon « marche bien pour les environnements simples à épisodes
courts… mais même dans ces cas simples elle demande un réglage » (250-251) ; la méthode,
« ajouter du bruit aux poids des couches entièrement connectées et ajuster les paramètres de ce
bruit pendant l'entraînement par rétropropagation » → EQ 06-E9, mu et sigma entraînables,
epsilon retiré (251) ; les deux variantes, gaussienne indépendante (une valeur par poids) et
gaussienne FACTORISÉE, « en ne gardant que deux vecteurs aléatoires, un de la taille de
l'entrée et un de la taille de la sortie… la matrice de bruit est obtenue par produit
extérieur » (251) ; ce que la méthode N'EST PAS, « il ne faut pas la confondre avec l'idée que
le réseau décide où explorer davantage », famille plus complexe (motivation intrinsèque,
comptage) reportée au ch. 21 donc SEMAINE 11 → l'encadré [!NOTE] de 6.9 (251) ; initialisation
lue dans le code, mu_range = 1/sqrt(in_features) et uniforme dans [−mu_range, mu_range], sigma
rempli de std_init/sqrt(in_features) avec std_init=0,1, et le tirage factorisé par
x.sign().mul_(x.abs().sqrt_()) puis weight_epsilon.copy_(epsilon_out.outer(epsilon_in)) →
EQ 06-E9b, qui n'est AFFICHÉE NULLE PART dans la source : c'est le cours qui transcrit du code
en mathématiques, et la page le dit en une incise (253) ; weight est une PROPRIÉTÉ, mu + sigma·
epsilon en entraînement et mu SEUL en évaluation → le second sens de reseau.eval() de la
semaine 5, lecture du cours, les deux moitiés ancrées (254) ; le piège, « les valeurs d'epsilon
ne sont pas mises à jour après chaque pas d'optimisation (et ce n'est pas mentionné dans la
documentation) », une implémentation prête à l'emploi exigeant un appel explicite à
reset_noise(), reformulé sans nommer la bibliothèque tierce en cause, le fait important et non
le produit (254) ; recette de conversion, remplacer les deux nn.Linear par NoisyLinear et
« supprimer tout le code lié à la stratégie epsilon-gloutonne » (254) ; le diagnostic SNR →
EQ 06-E14, « le SNR dit combien de fois la composante stationnaire de la couche bruitée est
plus grande que le bruit injecté » (254) ; moyenne de 18 en 250 parties contre 350 pour la
référence dans la source, mais le cours écrit « 250 contre 400 », par cohérence avec la référence
unique retenue en 6.5 ; 194 trames/s contre 240, « donc en temps, la différence est moins
impressionnante », et 273 parties après réglage (254, 256) ; le comportement à raconter, rapport
de la couche 1 de 1/2 à presque 1/2,6 et de la couche 2 de 1/4 à 1/16, « mais après 450K trames
le niveau de bruit de la dernière couche a recommencé à AUGMENTER, poussant l'agent à explorer
davantage » → FIG 06-06, exprimé en SNR croissant (2 → 2,6 ; 4 → 16 puis retour vers 11) plutôt
qu'en fractions, et transcrit depuis index/pages/lapan/0255.png, la couche de texte ayant rendu
1/2,6 par « 2.61 » (255).

REJEU PRIORISÉ (256-264) : prioriser « selon la perte d'entraînement » (256) ; la prémisse
reprise, la SGD suppose l'i.i.d., d'où le tirage « au hasard et uniformément », et la politique
d'échantillonnage uniforme REMISE EN QUESTION : c'est exactement le défaut nº2 de la semaine 5
(257) ; le slogan et sa limite, s'entraîner davantage sur les données surprenantes mais « si on
se concentre sur un petit sous-ensemble du tampon, on perd la propriété i.i.d. et on surapprend
ce sous-ensemble » → EQ 06-E10, avec alpha_PER et NON alpha (D43, notation.md §5), les deux
bornes 0 (uniforme) et 1 (proportionnel) commentées et la valeur de départ 0,6 ; priorité
proportionnelle à la perte de la mise à jour de Bellman et PRIORITÉ MAXIMALE aux échantillons
neufs, max_prio = self.priorities.max(initial=1.0) (257, 259) ; le biais et sa réparation,
prioriser « introduit un biais dans la distribution des données… qu'il faut compenser pour que
la SGD fonctionne », par des poids multipliant la perte de chaque échantillon → EQ 06-E11, avec
N = len(self.buffer) ; beta = 1 compense entièrement, partir plus bas et monter vers 1 est
meilleur pour la convergence : c'est l'échantillonnage préférentiel de la semaine 3, DÉLIBÉRÉMENT
non dépensé en semaine 5 et récolté ici (257) ; le calendrier lu dans le code, BETA_START = 0,4,
BETA_FRAMES = 100 000 → EQ 06-E11b (258-259) ; weights /= weights.max(), donc le plus grand
poids vaut 1 et la correction ne peut que RÉDUIRE une contribution : non énoncé par la source,
visible dans la ligne, écrit comme lecture du cours (260) ; les deux changements de code, un
tampon qui suit les priorités et rend (samples, indices, weights), et une perte qui prend les
poids et rend les pertes PAR ÉCHANTILLON pour que update_priorities() soit appelable (258,
260-261) ; nn.MSELoss « ne gère pas les poids », d'où losses_v = batch_weights_v·(…)**2 rendu
comme losses_v.mean() plus (losses_v + 1e-5), le 1e-5 évitant une priorité nulle (261) ;
GLISSEMENT D'AUTEUR NON REPRODUIT : ce qui est réécrit comme priorités est losses_v + 1e-5,
c'est-à-dire les pertes PONDÉRÉES, et non les erreurs TD sur lesquelles la méthode priorise.
Le fragment du cours réécrit l'écart NON PONDÉRÉ, détaché, en valeur absolue, et la prose nomme
les deux usages distincts de la même quantité, sans jamais signaler l'alternative (261,
index/summaries/lapan/ch08.md) ; coût, « à peu près le même temps absolu pour résoudre
l'environnement… mais moins d'itérations d'entraînement et moins d'épisodes », l'écart étant
l'échantillonnage naïf en O(N) (262) ; 330 parties après réglage, meilleur alpha_PER = 0,6,
« comme dans la publication » (263) ; l'avertissement à garder, la perte baisse visiblement mais
« la valeur de la perte pendant l'entraînement n'est pas l'objectif premier à optimiser ; on
peut avoir une perte très faible et, faute d'exploration, une politique finale loin de
l'optimum » → l'encadré [!WARNING] de 6.10 (263).

COMBINAISON (277-283, chunk 08-12 AJOUTÉ au dossier par la passe de lecture) : « vous avez
maintenant vu toutes les améliorations du DQN mentionnées dans Rainbow… l'essentiel de cette
publication était de les combiner et de vérifier les résultats » (279) ; le système combiné
retient QUATRE améliorations et en écarte DEUX, le DQN catégoriel et le double DQN, « parce
qu'elles n'ont pas montré beaucoup d'amélioration sur notre environnement d'essai » : le test
d'honnêteté de la semaine, et il est écrit tel quel (280) ; comment elles s'empilent, chemins
duels sur des DISTRIBUTIONS avec soustraction de la moyenne de l'avantage dans chaque atome,
variantes bruitées de nn.Linear dans les deux chemins, tampon priorisé dessous, dépliage de
Bellman à n pas (280) → le TABLEAU « ce qu'elle touche / ce qu'elle laisse intact » de 6.11 est
la lecture du cours de ces quatre points, et le critère qu'il en tire (deux améliorations qui
touchent la même pièce ne se composent pas gratuitement) l'est aussi ; résultat, « après
seulement 100 parties il gagnait presque toutes les manches », puis 100 de plus pour que la
récompense lissée atteigne +18, et score maximal « juste après 40 parties » après réglage
(281-282) ; prix, « le système combiné est plus lent que la référence… démarre à 170 FPS et se
dégrade à 130 à cause de la complexité O(n) du tampon » (281) ; la réserve du chapitre, la liste
« est loin d'être complète » et « nettement orientée vers les publications de DeepMind »,
reformulée en « les travaux d'un seul laboratoire de recherche » (283) ; et la dernière ligne du
chapitre, « améliorer les performances du DQN sans toucher à la méthode sous-jacente », qui est
la semaine 7 en une phrase et qui est devenue le paragraphe « En prévision de la semaine
suivante » (283).

DISTRIBUTIONNEL (268-271, OUVERTURE SEULEMENT) : la publication de juin 2017 et un ouvrage de
2023 des mêmes auteurs, repris sans les noms ; la question, « est-il pratique de comprimer
toutes les récompenses futures possibles en un seul nombre ? dans les environnements compliqués
le futur peut être stochastique » (268) ; l'exemple des deux trajets avec ses nombres, voiture
≈ 30 minutes d'ordinaire et parfois trois fois plus, MOYENNE 35,43 ; train 40 minutes avec une
petite chance de +20, MOYENNE 40,54 ; sur les moyennes la voiture gagne, sur les distributions
le train gagne, « même dans le pire cas ce sera une heure contre une heure et demie », et le mot
est VARIANCE → FIG 06-07 et FIG 06-08, avec l'encadré [!WARNING] sur les deux axes horizontaux
qui ne couvrent pas la même plage (269-270) ; dans un PDM l'effet se compose, « travailler avec
des récompenses moyennes peut faire perdre beaucoup d'information sur la dynamique sous-jacente
de l'environnement » (270) ; la généralisation → EQ 06-E12, Z et R devenues des distributions et
le symbole d'égalité EN DISTRIBUTION, la source notant x l'état et notation.md gardant s ; seule
la perte change, divergence de Kullback-Leibler (entropie croisée) ou métrique de Wasserstein,
cette dernière justifiée théoriquement puis « a rencontré des limites » en pratique, « donc au
final la publication a utilisé la divergence KL » ; N_ATOMS=51 sur [−10, +10], d'où le nom C51
(271). Le chunk 08-11 (code de la PROJECTION, 2 876 jetons) est DÉLIBÉRÉMENT NON LU et la
section 6.12 le dit à sa façon, dans un encadré [!NOTE] qui borne explicitement ce qui est
exigible : la semaine enseigne l'IDÉE et pas l'implémentation (dossier, et pièges des notes).

SUTTON & BARTO ch. 6 §6.7 « Maximization Bias and Double Learning » (156-158, chunk AJOUTÉ au
dossier par la passe de lecture : le dossier de la semaine 4 l'avait reporté PAR ÉCRIT à la
semaine 6 et le dossier de la semaine 6 ne l'avait pas repris) : le mécanisme en deux phrases,
« un maximum de valeurs estimées est utilisé implicitement comme estimation du maximum des
valeurs, ce qui peut conduire à un biais positif significatif », et l'exemple où les valeurs
vraies sont toutes nulles et les estimations réparties de part et d'autre, « le maximum des
valeurs vraies est nul, celui des estimations est positif » ; le nom, BIAIS DE MAXIMISATION
(156) ; LE DIAGNOSTIC SUR LEQUEL LA SECTION 6.7 EST BÂTIE, le problème est dû à « l'usage des
MÊMES ÉCHANTILLONS à la fois pour déterminer l'action maximisante et pour estimer sa valeur » ;
la séparation, A* = argmax_a Q1(a) et Q2(A*) non biaisée, E[Q2(A*)] = q(A*) (157) ; le coût du
double apprentissage, « double les besoins en mémoire mais n'augmente pas la quantité de calcul
par pas », une seule estimation mise à jour par coup (157) → la remarque du cours selon laquelle
le double DQN ne paie NI l'un NI l'autre, les deux réseaux existant déjà, les deux moitiés
ancrées (SB p.157 et LAPAN p.219) ; l'exemple 6.7, le PDM A/B, « right » terminant avec 0 et
« left » menant en B d'où de nombreuses actions terminent avec une récompense N(−0,1, 1), donc
« left » toujours fautive, et pourtant « même à l'asymptote, le Q-learning prend l'action gauche
environ 5 % de fois de plus que l'optimum », avec epsilon = 0,1, alpha = 0,1, gamma = 1 et
10 000 exécutions → FIG 06-02 et EQ 06-E7 (156-158, fig. 6.5 p.157, éq. 6.10 p.158, toutes deux
lues sur index/pages/sb/0157.png et 0158.png). NON LU et volontairement laissé fermé :
sb/ch06/06-06 (Expected Sarsa, reporté à la semaine 9 où le cours le rencontre dans la
publication TD3) et TOUT S&B ch. 7 sur les retours à n pas : le « n étapes » de cette semaine
est le dépliage de Bellman du supplément, pas la théorie des retours à n pas, et la semaine 4
avait délibérément gardé le crochet intact.

COURSE-PLAN §2, §9.2, §9.3 et §10 : semaine 6 en module 2, chapitres 7-8, AUCUN JALON (le
prochain est en semaine 7, qui clôt le module) ; laboratoire = ablation DQN contre double contre
duel contre n étapes avec courbes comparées ; faisabilité Colab, « comparer sur CartPole, PAS
sur Atari » (§9.2), ce qui commande toute la forme du laboratoire et l'encadré [!WARNING] qui
interdit de prendre les chiffres Atari pour des attentes ; option B retenue (D12) : PTAN
enseignée UNE SEMAINE comme concept, laboratoires en PyTorch et Gymnasium simples, d'où la
double insistance de 6.1 ; exigence méthodologique de §10, « à partir du jalon 2, toute
comparaison repose sur PLUSIEURS GRAINES ALÉATOIRES avec intervalles de confiance, ce que le
manuel n'exige pas et que le cours exige » → les trois graines des volets B, C et D, et la
phrase sur la dispersion dans les attendus du volet C ; jalon 2 en semaine 7, « DQN + au moins
deux extensions + courbes comparatives », dont le volet C de cette semaine est la moitié.

GAPS ASSUMÉS, repris des notes de phase 1 :
1. AUCUNE DONNÉE CARTPOLE dans le corpus. Tout le chapitre 8 est sur Pong ; le seul ancrage
   CartPole est une ligne de résumé issue d'un chunk non lu. Les attentes du laboratoire sont
   donc QUALITATIVES, exactement comme le volet tabulaire de la semaine 4, et l'encadré
   [!WARNING] d'ouverture du laboratoire le dit à l'étudiant sous forme de consigne de lecture
   plutôt que d'aveu.
2. AUCUN ARBRE DE SEGMENTS nulle part dans le corpus : nommé trois fois, jamais montré. La
   section 6.2 nomme le passage de O(N) à O(log N), dit ce que la structure maintient, et
   s'arrête là ; le tampon du laboratoire est le tampon naïf.
3. EQ 06-E4 est l'écriture du cours (voir ci-dessus).
4. EQ 06-E9b n'existe que sous forme de code dans la source (voir ci-dessus).
5. Deux figures sont DEMANDÉES EN REDESSIN et non en recadrage, FIG 06-01 et FIG 06-04 : la
   première parce que trois cercles et trois flèches se redessinent mieux qu'ils ne se
   recadrent, la seconde parce que la source la donne comme venant de la publication duelle et
   parce qu'un recadrage ne montre PAS la soustraction de la moyenne au point de jonction, qui
   est tout l'argument de 6.8. Détail dans extraction/week-06.md.
6. Budget de lecture de la phase 1 : 35 297 jetons lus contre 31 689 prévus, 18 chunks et
   2 résumés de chapitre, après ajout de sb/ch06/06-07 et de lapan/ch08/08-12. Rien n'a été
   tronqué.

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossiers/week-06.md, section « DO NOT read ») :
lapan/ch08/08-03 (réglage d'hyperparamètres avec Ray Tune, recherche aléatoire, arrêt précoce,
3 013 jetons : hors programme de la semaine, le réglage comme sujet appartient à la semaine 7 et
le cours n'utilise pas Ray) ; lapan/ch08/08-11 (le code de la projection de C51, 2 876 jetons :
la semaine enseigne l'idée, pas l'implémentation) ; les deux premières pages de
lapan/ch08/08-12 (résultats de C51 et figures 8.23 à 8.25) ; lapan/ch07/07-08 (aides Ignite,
1 558 jetons) et lapan/ch07/07-09 (panorama des autres bibliothèques, 1 032 jetons) ; TOUT
lapan/ch09 et ch10, qui sont la semaine 7, et ch09 est le plus tentant de la liste puisque le
socle commun est l'endroit où un travail de vitesse commencerait, la vitesse n'étant PAS le
sujet de cette semaine ; sb/ch06/06-06 (Expected Sarsa) et TOUT S&B ch. 7 (retours à n pas).

ÉCARTS ASSUMÉS
- TROIS SENS DE α DANS UNE SEULE SEMAINE. notation.md §5 ne tranchait que la collision
  pas d'apprentissage / exposant du tampon priorisé (D43). La synchronisation douce de la
  section 6.4 en apporte un troisième. La règle est énoncée UNE fois, dans un encadré
  [!IMPORTANT] de l'introduction, AVANT la première équation et SANS attribution : α nu est le
  pas d'apprentissage, tout autre α porte un indice. D'où α_PER (6.10) et α_sync (6.4), le
  second étant un ajout du cours à notation.md et non une forme de la source. ALIGNEMENT DE
  notation.md SIGNALÉ, PAS EFFECTUÉ : éditer notation.md n'est pas une opération de rédaction.
- SYNCHRONISATION DOUCE ÉCRITE À L'ENVERS DE LA SEMAINE 11, et la dette est payée ici.
  alpha_sync(0,1) garde 10 % de l'ancienne cible, vérifié arithmétiquement sur les tenseurs
  imprimés ; la convention τ de la semaine 11 est la complémentaire. La conversion
  α_sync = 1 − τ est donnée une fois, dans un encadré [!WARNING], avec la valeur usuelle
  τ = 0,005 pour que la comparaison soit concrète.
- RÉFÉRENCE UNIQUE POUR TOUTE LA SECONDE MOITIÉ : 700 000 trames et 400 parties, écrites en
  6.5, réutilisées telles quelles en 6.6, 6.7 et 6.9. Conséquence assumée : la comparaison des
  réseaux bruités se lit « 250 contre 400 » et non « 250 contre 350 » comme la source l'écrit
  en p.254. Les deux nombres restent ceux de la source ; seul l'appariement est du cours, et il
  est imposé par le choix d'une référence unique. Aucune mention du désaccord.
- TROIS ERREURS DE SOURCE ÉCRITES CORRECTEMENT ET EN SILENCE : le max surnuméraire de la cible
  du double DQN (EQ 06-E6), l'affirmation que la retouche corrige « complètement » la
  surestimation, et les priorités réécrites depuis les pertes pondérées plutôt que depuis les
  erreurs TD. Détail et formulation retenue dans extraction/week-06.md. Dans les trois cas la
  page écrit la version juste, sans réserve, sans note de bas de page et sans rien qui indique
  à l'étudiant qu'une source existe (D17, D18). Même traitement qu'en semaines 4 et 5.
- SYNTHÈSE PROPRE AU COURS, SIGNALÉE COMME TELLE, cinq fois : (a) le tableau défaut ↔ réparation
  de l'introduction, dont l'appariement est du cours et dont chaque moitié est ancrée ; (b) le
  tableau des cinq objets de 6.2 et sa colonne « son équivalent en semaine 5 » ; (c) la remarque
  que le double DQN ne paie ni la mémoire ni le calcul du double apprentissage, qui tient
  SB p.157 et LAPAN p.219 dans une phrase ; (d) le second sens de reseau.eval() sur un réseau
  bruité, qui tient LAPAN p.254 et le volet C de la semaine 5 ; (e) le tableau « ce qu'elle
  touche / ce qu'elle laisse intact » de 6.11 et le critère qu'il en tire. Chacune est livrée
  dans un encadré ou un tableau, et chacune cite ses moitiés en commentaire.
- D45 : AUCUNE PHRASE DE SOURCE N'EST CITÉE. Les guillemets de la page couvrent uniquement un
  terme en cours d'introduction, une glose française, une question rhétorique, le mot « résolu »
  comme critère, et deux phrases que ce cours a lui-même forgées (« cet état est mauvais quoi
  que je fasse », reprise de la semaine 5, et « s'entraîner plus sur ce qui surprend »). Aucune
  première personne autre que celle de la professeure n'apparaît sur la page : la justification
  de l'auteur sur l'emploi d'une bibliothèque (p.227) est reformulée comme la position du cours,
  et l'image de la voiture autonome (p.243) est reprise comme image, en prose, hors guillemets.
- HAMEÇONS POSÉS, AUCUN DÉPENSÉ : semaine 7 (vectorisation, parallélisme, profilage, étude de
  cas) annoncée par 6.3 et par la transition ; semaine 8 (méthodes sur politique, agent de
  politique attendant des logits) annoncée en 6.2 et en 6.6 ; semaine 9 (distributions dans un
  cadre où elles paient) en 6.12 ; semaine 11 (synchronisation douce, exploration dirigée,
  surestimation en contrôle continu) en 6.4, 6.7 et 6.9. Aucun nom de méthode de ces semaines
  n'est donné.
- D12 : PTAN est LUE, jamais adoptée. Elle est nommée deux fois dans la page, dans le tableau
  des outils et dans la commande d'installation, et le volet A du laboratoire est le seul qui
  l'exécute. Tout le reste du laboratoire, et tous les fragments des sections 6.4 à 6.10, sont
  en PyTorch nu et Gymnasium.
- D15 : tout le code est réécrit (identifiants français, annotations de type, sélecteurs comme
  objets appelables, transition premier-dernier en dataclass, réseau cible avec sa copie
  profonde explicite, couche bruitée écrite de zéro avec register_buffer, tampon priorisé naïf
  écrit autour d'un tableau NumPy de priorités, perte pondérée rendant deux valeurs, assertions
  et points de contrôle ajoutés). Rien n'est copié d'un dépôt de source, et la correction de la
  priorité non pondérée est une réécriture, pas une transcription.
- RIEN QUE L'ÉTUDIANT DOIVE EXÉCUTER N'EST DANS LA PAGE : les onze fragments Python des
  sections servent la double lecture (D10), plus trois extraits de consigne dans le
  laboratoire, et les cinq volets passent par {{< colab >}}. Les
  fragments de 6.7 et 6.10 portent explicitement la mention que la mise en tenseurs est celle de
  6.5, pour qu'aucun ne se présente comme un programme complet.

DÉCOMPTE : 12 sections · 8 placeholders FIG · 0 placeholder EQ
(les dix-sept équations 06-E1 à 06-E15 plus 06-E9b et 06-E11b sont écrites directement :
treize sont RECOPIÉES depuis index/notes/week-06.md, elles-mêmes lues lettre à lettre sur les
pages rasterisées sous index/pages/lapan/ et index/pages/sb/, 06-E14 comprise, qui avait survécu
à l'extraction et a été confirmée en contexte ; quatre viennent d'un LISTAGE DE CODE, à savoir
06-E4 dont le gamma^n est le gamma**n_steps du code, 06-E9b, 06-E11b et 06-E15 ;
06-E4 et 06-E9b appartiennent au cours et la page le dit pour la seconde. Aucune ne passe par un
placeholder, ce qui est le régime prévu par D22 pour une formule vérifiée sur sa page. Quatre
formules affichées de plus ne portent pas d'identifiant 06-E parce qu'elles sont standard ou
déjà du vocabulaire du cours : la politique ε-gloutonne de 6.2, les deux lignes A* et
E[Q2(A*)] = q(A*) de 6.7, et la définition Q = V + A de 6.8 ; elles sont enregistrées dans
extraction/week-06.md.)
{{% /comment %}}
