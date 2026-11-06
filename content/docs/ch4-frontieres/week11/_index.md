---
title: "Semaine 11 : Exploration avancée"
weight: 11
bookCollapseSection: true
---

# Semaine 11 : Exploration avancée

Pendant dix semaines, nos agents ont exploré par accident : un \(\varepsilon\) qui décroît, du bruit sur une action, une prime d'entropie à côté d'une perte. Aucun de ces mécanismes ne décide **où aller**, et tant que la récompense est dense cela n'a pas d'importance. Cette semaine ouvre le module 4 sur la situation où cela en a une : sous une récompense parcimonieuse, un agent peut tourner pendant des heures et **ne jamais voir une seule récompense positive**, et le choix de la méthode d'apprentissage cesse alors d'avoir le moindre effet, parce que rien ne s'apprend d'un jeu de données où la chose à apprendre ne se produit jamais. Vous verrez pourquoi le défaut de la méthode \(\varepsilon\)-gloutonne n'est pas son hasard mais son **incohérence**, vous mesurerez cet échec sur une rivière à six états, vous rencontrerez les trois familles de méthodes qui y répondent, et vous finirez sur un renversement : sur une autre tâche, la méthode \(\varepsilon\)-gloutonne est la meilleure de toutes. La semaine ne porte aucun jalon.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** une exploration non dirigée retire sa décision à chaque pas, donc elle ne mène jamais une séquence à son terme ; les méthodes de cette semaine la remplacent par une pression cohérente vers la nouveauté, au prix de modifier le problème que l'agent résout.

---
## Description générale

La semaine commence par une démonstration d'impossibilité. Sous une récompense parcimonieuse, un agent peut n'avoir **jamais** rencontré la récompense positive, et dans ce régime la méthode d'apprentissage la plus efficace du domaine n'apprendra qu'une chose : qu'il n'existe aucun moyen d'obtenir une bonne récompense. L'exploration cesse d'être un réglage et devient une **condition de possibilité**. La semaine définit alors une exploration efficace par la négative, c'est-à-dire par le temps qu'elle ne perd pas dans des états déjà connus, et elle assume de ne pas pouvoir en donner la définition formelle.

Vient ensuite le procès de la méthode \(\varepsilon\)-gloutonne, et il comporte un acquittement. L'accusation selon laquelle ses actions aléatoires **biaisent** l'estimation des valeurs d'action est fausse pour la cible à un pas, et il suffit d'écrire cette cible pour le voir : l'action réellement jouée n'y apparaît pas, puisque le maximum porte sur les actions de l'état suivant. C'est exactement ce que signifie « hors politique », et c'est ce qui autorise un tampon de rejeu. La semaine concède la moitié honnête de l'accusation, parce que le biais **existe** dès que la cible est dépliée sur plusieurs pas, ce que la semaine 6 avait identifié et payé. Puis elle énonce le vrai reproche, qui organise tout le reste : avec du hasard injecté dans la trajectoire, la politique de collecte change à **chaque pas**, de sorte qu'aucune séquence d'actions coordonnées n'est jamais menée à son terme. Le défaut n'est pas le hasard, c'est l'**incohérence**.

Une rivière à six états mesure ce défaut. Un courant ramène le nageur vers sa rive de départ avec une probabilité de 1, tandis que chaque avancée contre le courant n'a qu'une chance sur trois de réussir : le progrès est improbable et incertain là où la régression est parfaitement fiable. Un agent purement aléatoire atteint la rive opposée **zéro** fois en cent pas, zéro fois en mille pas, et cinq fois en dix mille pas, soit cinq centièmes de pour cent des pas effectués. La semaine insiste sur l'unité de ces trois mesures, qui sont des pas et non des épisodes, et donne l'addition qui le vérifie.

Trois familles répondent au problème, et une image les sépare par leur **point d'attache**. La première place le bruit sur les **poids** du réseau : ce sont les réseaux bruités de la semaine 6, relus ici comme une exploration **dirigée**, puisque le bruit n'est retiré que de temps en temps et qu'une trajectoire entière est donc collectée par une politique unique prélevée dans un ensemble. La deuxième calcule une prime à partir d'un **comptage de visites**, décroissante comme l'inverse de la racine du compteur, et elle demande un hachage des états dès que l'observation est continue. La troisième calcule une prime à partir d'une **erreur de prédiction** : un réseau apprend à reproduire la sortie d'un autre réseau, aléatoire et figé, et son erreur mesure la nouveauté de l'observation sans aucun compteur. Les deux familles de prime sont indiscernables dans une perte et lisent deux quantités entièrement différentes, ce qui est la raison d'être de la figure.

Suit la section que la semaine prend à son compte. Une prime ajoutée dans une enveloppe est **additionnée** à la récompense de l'environnement, donc elle redéfinit la fonction de récompense, donc elle définit un autre processus de décision markovien : la politique optimale du problème modifié n'a aucune raison d'être celle du problème d'origine. Le dispositif habituel, qui consiste à entraîner deux têtes de valeur séparées, existe précisément pour éviter cela, et la raison qu'on donne de s'en passer, moins de modifications dans le code, est vraie sans être le prix complet. La prime reste tolérable ici à deux conditions accidentelles : elle décroît, et la sélection finale se fait sur la récompense de la tâche, mesurée sans enveloppe. D'où la règle de lecture qui gouverne toute la suite : seule la courbe d'évaluation est à l'échelle du problème d'origine.

La mesure se fait sur une voiture immobilisée au fond d'une vallée, dont le moteur est trop faible pour gravir la pente et qu'il faut faire osciller par des dizaines d'actions coordonnées. La récompense y vaut \(-1\) à chaque pas, sans exception, ce qui signifie que tant que le but n'est pas atteint **toutes les politiques se valent** : le jeu de données est plat, la perte diminue, les gradients sont propres, et rien n'est appris. La méthode de référence, un réseau Q profond \(\varepsilon\)-glouton, n'atteint le but **pas une seule fois**, ni en cent mille pas, ni en cinq heures d'agent purement aléatoire. Son échec est permanent plutôt que lent, puisque son \(\varepsilon\) a fini de décroître avant que quoi que ce soit ait été trouvé.

Six exécutions suivent, cinq correctifs et une seconde méthode de référence, et la semaine reconstruit leur tableau en séparant deux questions que l'on confond d'ordinaire : quand le but a-t-il été trouvé, et la tâche a-t-elle été résolue. Les réponses diffèrent, et c'est la meilleure observation de la semaine : la découverte la plus rapide de toutes, dix minutes, appartient à une exécution qui n'a **jamais** résolu la tâche, et les deux seules exécutions qui l'ont résolue ont mis presque quatre fois plus longtemps à trouver le but. **Deux exécutions sur sept ont résolu la tâche, toutes les deux avec une méthode de politique.** Le passage d'une méthode de valeur à une méthode de politique y reçoit une justification réutilisable : une récompense qui change en cours d'entraînement oblige une méthode de valeur à réapprendre ses valeurs, là où une méthode sur politique voit seulement un échantillon mieux payé.

La semaine se termine sur un renversement, et elle ne l'adoucit pas. Sur un jeu de sous-marin dont la seule compétence rare est de remonter respirer, la méthode \(\varepsilon\)-gloutonne est la **meilleure** de toutes celles qui ont été essayées, alors qu'elle était la plus mauvaise et de très loin sur la tâche précédente. Les deux mesures sont bonnes. Un classement de méthodes d'exploration ne se transfère donc pas d'un environnement à un autre, et la conclusion honnête d'une comparaison est parfois que la comparaison était locale. La semaine ferme sur l'inventaire de ses propres lacunes, théorie de l'exploration comprise, et sur une règle pratique qui tient en une question : votre agent rencontre-t-il jamais la récompense qui compte ?

---
## Mots-clés de la semaine

exploration efficace · exploration non dirigée · exploration dirigée · limites de la méthode epsilon-gloutonne · incohérence de la politique de collecte · récompense parcimonieuse · couverture de l'espace d'états · séquence d'actions coordonnées · River Swim · comptage de visites · absence de biais de la cible à un pas · biais de la cible dépliée · récompense intrinsèque · récompense extrinsèque · prime d'exploration · méthodes fondées sur le comptage · hachage des états · pseudo-comptage · modèle de densité · exploration par curiosité · méthodes fondées sur la prédiction · distillation de réseau aléatoire · réseau de référence figé · prédicteur à capacité limitée · réseaux bruités · fréquence d'échantillonnage du bruit · bruit de paramètres · têtes de valeur séparées · modification du processus de décision markovien · prime décroissante · critère d'arrêt extrinsèque · incomparabilité des courbes d'entraînement et d'évaluation · MountainCar · récompense constante avant le premier succès · entraînement sain qui n'apprend rien · position maximale comme instrument · sensibilité à une récompense modifiée en cours d'entraînement · découverte du but contre résolution de la tâche · comparaison des méthodes d'exploration · jeux à exploration difficile · non-transférabilité des résultats · comparaison locale

---
## En prévision de la semaine suivante

La semaine 12 garde la question de cette semaine et change complètement de réponse. Nos sept méthodes explorent toutes en **agissant** : elles perturbent une politique, elles paient une nouveauté, et elles découvrent le monde en s'y déplaçant réellement. La semaine 12 explore en **réfléchissant**. Avant de jouer un coup, l'agent construit un arbre de possibilités, y simule des suites, et décide à chaque nœud lequel mérite d'être approfondi : l'exploration devient une recherche dans un arbre plutôt qu'une perturbation d'une action, et la règle qui choisit la branche à approfondir est, elle, construite sur une borne de confiance, c'est-à-dire précisément l'objet que cette semaine a dû poser sans le démontrer. Vous verrez cette idée appliquée à des jeux à deux joueurs, où l'adversaire est l'agent lui-même, et vous verrez ce qui se passe lorsque le modèle utilisé pour simuler n'est pas donné mais **appris**. Gardez en tête la leçon de la section 11.7 : vous allez rencontrer une famille de méthodes dont les résultats sont spectaculaires sur une classe de tâches très précise, et la question à se poser en la lisant est, comme toujours, sur quoi elle a été mesurée.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 12{{% /comment %}}

{{% comment %}}
Pagination : indices PDF (D35). Imprimé = PDF moins 31 pour LAPAN, conformément à
MAP-lapan.md, comme dans le dossier et les notes de phase 1. Toutes les pages citées
ci-dessous sont des indices PDF.

SEMAINE À UNE SEULE SOURCE, ET C'EST UN FAIT SUR LA SEMAINE PLUTÔT QU'UN OUBLI. LAPAN ch. 18
est le seul matériel disponible sur ce sujet : les suppléments ne contiennent rien sur
l'exploration, ni le papier de la distillation de réseau aléatoire ni les papiers de
pseudo-comptage n'ont été déposés, sb/ch02 (bandits) n'est pas indexé, et lapan/ch17
(stratégies d'évolution, marqué optionnel pour cette semaine par COURSE-PLAN) n'a jamais été
indexé et n'a aucun chunk. La passe de lecture a donc lu le chapitre entier (13 823 tokens,
10 chunks et un résumé de chapitre), et la semaine dit explicitement où le domaine va plus loin
que le cours ne peut suivre : §11.3 pour la borne de confiance et le regret, §11.7 pour
l'inventaire complet des lacunes. Aucun chunk hors manifeste, aucun nouveau papier.

DOUZE PAGES RASTÉRISÉES PENDANT LA PASSE DE LECTURE, LES DOUZE OUVERTES (lapan 550, 551, 552,
554, 555, 559, 561, 562, 564, 565, 566, 568), parce que ce chapitre ne peut pas être cru ligne
à ligne. Tous les nombres de §11.5, §11.6 et §11.7 viennent des arbitrages de
index/notes/week-11.md, qui ont été rendus sur ces images, et NON du tableau de synthèse du
chapitre ni des chunks. La rédaction n'est jamais retournée à une page.

CINQ CORRECTIONS DE FOND, ET CHACUNE EST PORTÉE PAR LA PAGE SANS QUE L'ÉTUDIANT APPRENNE
QU'UNE SOURCE EXISTE.

(1) LA PREMIÈRE ACCUSATION CONTRE L'EPSILON-GLOUTON EST FAUSSE, ET §11.1 LE DÉMONTRE. La p.550
affirme, sans aucune réserve et en argumentant par le tampon de rejeu, que les actions
aléatoires biaisent l'estimation des valeurs d'action (« we will learn wrong Q-values »). Pour
la cible à un pas c'est faux : la cible prend le max sur les actions de l'état suivant, quelle
que soit l'action jouée, et c'est précisément ce qui définit le hors politique. §11.1 énonce
l'accusation comme une affirmation qui circule, SANS nommer personne et sans révéler qu'un
ouvrage existe, écrit la cible (11-E5, citée de la page de la semaine 6 et de notation.md),
montre que l'action jouée n'y figure pas, puis concède la moitié honnête : sous un dépliage à
n étapes (11-E6, semaine 6 §6.6) les récompenses intermédiaires SONT celles de la politique de
comportement et le biais est réel, ce que la semaine 6 avait déjà nommé et payé. La section
donne en plus un contrôle réutilisable : chercher l'action jouée dans la cible, à droite ou
seulement comme index à gauche. Le tableau symbole/variable porte une ligne dont la colonne
« variable du code » dit « aucune », ce qui est l'argument en une ligne.

(2) LES TROIS COMPTAGES DE RIVER SWIM SONT EN PAS, PAS EN ÉPISODES. La p.552 écrit deux fois
« episodes » là où les comptages somment exactement à 100, 1 000 et 10 000 et où la page
elle-même appelle les cinq visites « 0.05 % of all the steps ». À dix pas par épisode, les
trois exécutions valent 10, 100 et 1 000 épisodes. §11.2 écrit des PAS, donne l'équivalent en
épisodes entre parenthèses, et consacre un encadré [!WARNING] au contrôle par addition, qui
est plus utile qu'une correction silencieuse. Le dossier et le résumé de chapitre avaient tous
deux hérité de l'erreur de l'auteur ; les notes de phase 1 l'ont corrigée et la page suit les
notes.

(3) LE MÉLANGE s/x DE LA FACTORISATION DU PSEUDO-COMPTAGE EST IMPRIMÉ SUR LA PAGE. La p.554
imprime Ñ(s) = rho(x) n(x), mélangeant deux variables et écrivant le nombre TOTAL d'états
visités comme une fonction de l'état. Vérifié sur l'image : ce n'est pas un artefact
d'extraction. §11.3 écrit Ñ(s) ≈ rho(s) n en une seule variable (11-E3), dit en mots ce que
chaque facteur désigne, et LABELLE LA FORMULE COMME UNE ESQUISSE dans un encadré [!WARNING],
parce que la construction réelle du pseudo-comptage demande davantage et que ni l'un ni l'autre
des papiers concernés n'est disponible. La page ne la présente jamais comme une dérivation.

(4) LE TABLEAU DE COMPARAISON EST RECONSTRUIT, LIGNE PAR LIGNE, ET NON REPRODUIT. Six cases du
tableau 18.1 (p.568) contredisent le corps du chapitre, une ligne manque, et une phrase de la
même page contredit le tableau. Arbitrages suivis, tous rendus sur image dans
index/notes/week-11.md : DQN + réseaux bruités = 7 000 PAS D'ENTRAÎNEMENT et 20 min (le tableau
dit 8k ÉPISODES et 15 min ; l'unité elle-même est fausse, et la page le signale deux fois,
dans la sous-section et sous le tableau) ; DQN + comptage = LIGNE AJOUTÉE, but à 10 min,
jamais résolue, épisodes non rapportés (la ligne est absente du tableau d'origine alors que le
corps la rapporte, et c'est la découverte la plus rapide des sept : son omission cache la
meilleure observation de la semaine) ; PPO = 30k épisodes et 60 min (le tableau dit 40k) ;
PPO + réseaux bruités = 18k épisodes et 30 min (le tableau arrondit à 20k) ; PPO + comptage,
découverte = 23k épisodes, le temps de 36 min venant du tableau faute d'autre mesure ;
PPO + comptage, résolution = 61k épisodes et environ 1 h 37 (console elapsed=1:37:18, le
tableau arrondissant à 90 min) ; PPO + distillation = tableau tel qu'imprimé, la résolution
(33k, 84 min) étant confirmée à la minute par la console et la découverte (16k, 36 min) étant
MARQUÉE DANS LA CASE comme non recoupée, puisque ces deux valeurs n'existent nulle part
ailleurs. Et la phrase de la p.568 selon laquelle « both DQN and PPO with exploration
extensions are able to solve the MountainCar environment » est FAUSSE : aucune ligne DQN n'a de
résolution, et les p.559 et p.561 disent toutes deux que la barre de -130 n'a pas été franchie.
LA PAGE ÉCRIT : DEUX EXÉCUTIONS SUR SEPT ONT RÉSOLU MOUNTAINCAR, TOUTES LES DEUX AVEC PPO, et
elle le dit deux fois, dans §11.6 et dans la page d'accueil.

(5) LA PRIME DE LA DISTILLATION EST INCOHÉRENTE DANS LA SOURCE, ET LA PAGE TRANCHE. La p.555
dit que la prime est proportionnelle à l'erreur quadratique moyenne ; la p.565 et le code de la
p.566 emploient la DIFFÉRENCE ABSOLUE pour la prime et une erreur quadratique moyenne pour la
perte du prédicteur. §11.3 enseigne l'ERREUR QUADRATIQUE (11-E4), le dit explicitement dans un
encadré [!TIP], signale que la différence absolue circule aussi et qu'elle est ce que fait la
mise en œuvre dont §11.6 rapporte les mesures, et ajoute la conséquence pratique : changer de
forme oblige à régler c de nouveau. Le laboratoire emploie l'erreur quadratique, et la consigne
demande à l'étudiant de dire laquelle il utilise.

DEUX AUTRES ERREURS DE LA SOURCE, NI REPRISES NI COMMENTÉES. La p.566 écrit que 33k épisodes
représentent « presque deux fois moins que Noisy Networks », alors que les réseaux bruités
n'ont jamais résolu MountainCar et que le terme de comparaison est PPO + comptage (61k) : la
page compare 33k à 61k en nommant la bonne méthode et ne mentionne pas la confusion. Et le
chapitre appelle deux fois la distillation de réseau aléatoire « policy distillation » (p.553 et
p.561), qui est une méthode entièrement différente : la page écrit TOUJOURS « distillation de
réseau aléatoire », le glossaire porte la mise en garde, et « distillation de politique »
n'apparaît nulle part.

L'IDÉE QUE NUL NE DIT ET QUE LE COURS SIGNE (§11.4). Ajouter la prime dans une enveloppe change
le processus de décision markovien : une récompense fabriquée est quand même une récompense,
donc la politique optimale du problème modifié n'a aucune raison d'être celle du problème
d'origine. La source ne dit nulle part cela : la p.565 abandonne les deux têtes de valeur du
papier d'origine en nommant un seul coût, « this minimizes the number of modifications in the
code », et la p.559 énonce un argument DIFFÉRENT, sur le réapprentissage des valeurs en hors
politique, que la page place en §11.6 comme premier motif du changement de famille. §11.4
énonce la conséquence dans un encadré [!IMPORTANT] explicitement attribué au cours (« Ceci est
une affirmation du cours, et je la prends à mon compte »), ajoute les deux conditions
accidentelles qui la rendent tolérable ici (la prime décroît en 1/racine(Ñ) ; l'arrêt se fait
sur un retour de test EXTRINSÈQUE), et en tire la règle de lecture des courbes, appuyée sur la
conséquence mesurable de la p.561 (les valeurs d'entraînement sont plus hautes que celles de
test parce que l'environnement d'entraînement porte l'enveloppe).

« PARAMETER NOISE » : NOMMÉ COMME UNE DIRECTION NON SUIVIE. COURSE-PLAN §2 wk 11 le liste pour
cette semaine ; ni le chapitre ni aucun élément disponible ne le traite. Décision prise à la
rédaction, enregistrée aussi dans extraction/week-11.md : la page le NOMME en une phrase à la
fin de la sous-section sur les réseaux bruités (§11.3), sans aucune description de mécanisme,
et dit que le cours ne le suit pas. Aucun traitement n'est improvisé, et §11.7 le reprend dans
l'inventaire des lacunes.

NOTATION. Trois objets sont déclarés dans l'introduction et redéclarés là où ils mordent :
c (poids de la prime, NI alpha le pas d'apprentissage depuis la semaine 3, NI beta le
coefficient d'entropie depuis la semaine 8, les trois apparaissant dans §11.6) ; rho(s), qui
prend son TROISIÈME sens dans le cours (rapport d'échantillonnage préférentiel dans
notation.md, fréquence de visite actualisée en semaine 10, modèle de densité ici), nommé en
français partout sauf dans 11-E3 ; et psi, les paramètres du prédicteur de la distillation,
distincts de theta (politique) et de w (valeur), déclaré à l'endroit où il apparaît. La
source écrit r_i pour la prime (indice i sur r) : le cours écrit R^i_t, exposant i pour
« intrinsèque », conformément à S&B qui réserve l'indice au temps.

INTRODUCTION. Le régime où l'exploration décide de la possibilité d'apprendre, et non seulement
de la vitesse (p.548-549) ; LA PHRASE CHARNIÈRE, sans bons échantillons la méthode la plus
efficace n'apprendra que l'absence de récompense (p.549) -> encadré [!IMPORTANT], reformulé en
voix propre ; les trois arguments dans leur ordre, dont le gain sous récompense dense par
diversité de l'échantillon (p.549) ; la définition par la négative de l'exploration efficace
(p.549) ; et l'absence de définition formelle, assumée dans un encadré [!NOTE] sur le modèle de
la limite K-FAC de la semaine 10. Le décompte des cinq mécanismes d'exploration des semaines 4
à 10 vient des pages du cours lui-même, pas d'une source. Le couple dirigé / non dirigé est
coiné ici, d'après p.553.

§11.1. Les deux formes de hasard, epsilon-glouton et prime d'entropie, et le réglage que la
seconde exige (p.549-550, image) ; la phrase qui les résume, « pour explorer, nous introduisons
du hasard dans nos actions » (p.550, image), rendue en voix propre ; L'ACCUSATION DE BIAIS
(p.550, image) et sa réfutation par 11-E5, qui vient de la page de la semaine 6 §6.6 et de
notation.md, PAS de LAPAN ; la concession par 11-E6 (semaine 6 §6.6, plus la semaine 8 pour le
dépliage) ; LE VRAI REPROCHE, la politique qui change à chaque pas et la mauvaise couverture
quand plusieurs pas sont nécessaires (p.550, image) ; et le jugement de clôture, l'agent
n'essaie pas d'explorer, il espère (p.553) -> encadré [!TIP] qui coine « non dirigée ». Fragment
de code et tableau symbole/variable écrits pour le cours.

§11.2. Structure complète transcrite des images des figures 18.1 et 18.2 (p.550-551) : six
états, une seule action aux deux rives, 0,6 / 0,4 depuis l'état 1, 0,35 / 0,60 / 0,05 pour
l'action droite depuis 2-5, p = 1 pour l'action gauche, retour de 6 vers 5. Récompense de
1 000 à l'entrée en 6 et petite récompense de 1 entre 1 et 5 (p.551, image), la petite restant
volontairement sans emphase comme la lacune 5 des notes le demande. Dix pas par épisode et
agent à epsilon = 1 (p.551, p.553). Les trois comptages (p.552, image) et la correction d'unité
ci-dessus. La généralisation à 20 ou 50 états et aux centaines de décisions d'un jeu (p.552,
image). L'argument d'asymétrie (progrès improbable et incertain contre régression fiable) est
une lecture du cours sur la structure transcrite, et la page REFUSE explicitement de donner une
probabilité de premier passage, faute de calcul disponible. Fragment de simulation écrit pour
le cours, d'après la structure : rien n'est recopié d'un dépôt (D15).

§11.3. Les trois familles nommées et présentées comme un relevé de paysage, non comme une liste
exhaustive (p.553). Réseaux bruités : la lecture « dirigée », bruit sur les poids, tirage
intermittent, ensemble de politiques (p.553-554, image), la couche elle-même étant CITÉE de la
page de la semaine 6 §6.9 et jamais redérivée, mise en garde de la semaine 6 comprise (pas de
notion de nouveauté). Comptage : visiter ce qui n'a pas été vu, prime non issue de
l'environnement, vocabulaire intrinsèque/extrinsèque, 11-E1 transcrite de l'image de la p.554
et renommée en notation S&B ; passage à l'échelle par hachage ou plongement (p.554, image) ;
hachage à trois décimales et enveloppe (p.559-560). Lacune de la borne de confiance et du
regret nommée dans un [!NOTE], avec l'origine (étude des bandits) et le renvoi à la semaine 12 ;
sb/ch02 n'est pas indexé et le cours n'a jamais enseigné UCB. Pseudo-comptage : 11-E3 et
l'esquisse assumée (p.554, image). Curiosité nommée et non construite, renvoyée à la semaine 13
(p.554, image). Distillation : l'intuition de la prédiction (p.555, image), le mécanisme des
deux réseaux (p.555, image), 11-E4 écrite directement, et les tailles 2-128-128-1 contre
Linear(2,1) avec la raison du déséquilibre (p.565-566, images). Les deux détails commentés dans
le fragment (gradient interdit sur la référence, capacité limitée du prédicteur) sont la lecture
du cours sur ces deux faits.

§11.4. Ce que l'enveloppe renvoie, 11-E2, écrite d'après le code de la p.560 ; l'abandon des
deux têtes de valeur et le seul coût nommé par la source, le volume de code (p.565, image) ;
l'argument DIFFÉRENT de la p.559 sur le réapprentissage des valeurs, signalé comme distinct et
renvoyé à §11.6 ; la conséquence mesurable sur les deux courbes (p.561, image). LE RESTE EST DU
COURS : la modification du MDP, les deux conditions accidentelles, la règle de lecture des
courbes, et le fragment à deux routes qui montre OÙ la séparation se fait tout en disant que la
boucle à deux têtes n'est pas écrite dans ce cours.

§11.5. La tâche et sa ressemblance trompeuse avec le pendule (p.555, image) ; la difficulté et
le pont avec River Swim (p.556) ; l'interface complète, observation, actions, récompense,
troncature, et le retour d'environ -80 de la meilleure politique (p.556, p.557) ; le critère de
résolution à -130 (p.559, p.564, images) ; DQN + epsilon-glouton, calendrier sur 10^5 pas, deux
à trois minutes, environ 500 épisodes, but jamais atteint, et le caractère PERMANENT de l'échec
puisque epsilon a fini de décroître (p.556-557) ; la variante à epsilon = 1 maintenu, cinq
heures et 500k épisodes sans un seul exemple du but (p.558) ; et la phrase qui justifie la
semaine, sans exploration appropriée on peut simplement échouer à entraîner (p.557) -> encadré
[!WARNING]. La figure 18.3 de la source (capture pygame avec barre de titre) n'est PAS extraite,
décision enregistrée dans extraction/week-11.md ; la vallée est décrite en prose. Les deux
instruments (compteur d'atteintes du but, position maximale) sont une conception du cours.

§11.6. DQN + réseaux bruités, architecture et tirage à chaque itération (p.558-559, image
p.559), résultat 7 000 pas / 20 min et jamais -130, certains épisodes de test sous 100 pas mais
pas assez fréquents (p.559, image). DQN + comptage, hachage à trois décimales, Counter, prime
racine, somme dans l'enveloppe (p.559-561), but en 10 min et seuil non franchi de peu (p.561,
image). Les trois motifs du passage à une méthode de politique (p.561 image, p.562), dont la
deuxième est l'observation réutilisable -> encadré [!IMPORTANT]. PPO de référence, architectures
2-64-3 et 2-64-1, prime d'entropie, aucune exploration dédiée, but trouvé en 60 min et 30k
épisodes, trois heures sans amélioration puis arrêt (p.562, image). PPO + réseaux bruités,
acteur SEUL bruité et la raison (ne pas bruiter l'estimation de valeur), tirage une fois par
lot de 2 048 transitions contre chaque passe avant en hors politique (p.563), but en 30 min et
18k épisodes (p.564, image). PPO + comptage, résolution à 61k épisodes et 1 h 37, épisode de
test à 91 pas pour -91 et moyenne à -129,999 (p.564, p.565, images) ; la console n'est pas
recopiée, ses nombres sont rapportés en prose (D45). PPO + distillation, tailles des réseaux et
raison du déséquilibre, prime en différence absolue dans cette mise en œuvre et perte en erreur
quadratique moyenne, résolution à 33k épisodes et 1 h 24 (p.565-566, images) ; et la lecture de
la perte de distillation, basse avant la découverte puis en forte croissance (p.568, image) ->
encadré [!TIP]. Le Tableau 11-1 est une table Markdown écrite par le cours (D19 : une table
n'est jamais une image), avec l'unité portée DANS chaque case et la provenance faible marquée
DANS la case. La ligne sur l'absorption lente d'un échantillon rare par un tampon est présentée
comme une conjecture et non comme une mesure.

§11.7. Seaquest et la gestion de l'oxygène, 560 pas et récompense maximale de 20 sans elle,
partie presque infinie et 10k-100k avec elle, et la difficulté des méthodes traditionnelles à
le découvrir (p.568, image) ; le coût d'une demi-journée par expérience et l'absence de réglage
fin (p.569) ; DQN + epsilon-glouton MEILLEUR, 13 h, moyenne 18, maximum 25, quelques épisodes
trouvant l'oxygène (p.569) ; DQN + réseaux bruités à 6 après 6 h (p.570) ; les trois variantes
de PPO sans progression, moyenne 4, moins bonnes qu'une version antérieure du même code, avec
l'hypothèse d'un défaut subtil rapportée COMME UNE HYPOTHÈSE NON VÉRIFIÉE et non reprise par le
cours (p.570) ; et l'admission de clôture, le sujet de l'exploration est beaucoup plus vaste
(p.570), qui alimente l'inventaire des lacunes. L'explication structurelle du renversement
(longue séquence coordonnée contre récompense dense et abondante) est signalée dans la page
comme une CONJECTURE du cours, séparée de ce qui est mesuré.

LABORATOIRE. COURSE-PLAN §2 wk 11 pour les trois méthodes comparées et §9.2 pour la
faisabilité sur Colab, marquée sans réserve ; la tâche et ses chiffres viennent de §11.5 ; le
protocole à graines multiples avec intervalle est celui du jalon 2 (semaine 7) et s'applique
depuis. L'échauffement River Swim, les deux instruments, les quatre pièges et l'exigence de
rapporter la VALEUR atteinte plutôt que le verdict sont une conception du cours. Aucun score
cible n'est donné, pour la raison écrite dans le [!NOTE] : tous les chiffres de la semaine
portent sur un autre code et d'autres hyperparamètres. Les deux budgets de pas du fragment
Stable-Baselines3 sont déclarés non prédictifs.

PAS DE JALON CETTE SEMAINE, et le module 4 s'ouvre : le jalon 3 s'est fermé en semaine 10 et le
jalon 4 est en semaine 14 (COURSE-PLAN §10). La page d'accueil est rédigée ici (D47) et la
semaine n'écrit PAS de conclusion séparée, afin qu'aucun des deux textes ne reste non publié.
La projection vers la semaine 12 (auto-jeu, planification, multi-agent) vient de COURSE-PLAN
§2 wk 12 et ne dépense pas le contenu de cette semaine-là : elle annonce l'exploration par
recherche dans un arbre et la borne de confiance de sa règle de sélection, sans décrire aucune
méthode.

DÉCOMPTE : 7 sections numérotées · 3 placeholders FIG (les trois sont des dessins du cours,
aucune figure du chapitre n'étant extractible : 11-01 River Swim et 11-02 les trois points
d'attache sont DÉJÀ PRODUITS sur disque par scripts/make_figures_week11.py, et 11-03, le temps
jusqu'au but, reste à produire ; voir extraction/week-11.md) · 0 placeholder EQ
(6 équations identifiées, 11-E1 à 11-E6, toutes écrites directement en KaTeX dans la page :
11-E1 et 11-E3 TRANSCRITES de l'image vérifiée de la p.554, la seconde avec la correction de
variable et le label « esquisse » ; 11-E2 ÉCRITE d'après le code de la p.560 ; 11-E4 ÉCRITE
directement dans la notation du cours ; 11-E5 et 11-E6 CITÉES de la page de la semaine 6 §6.6
et de notation.md, jamais de LAPAN. La couche bruitée et son bruit gaussien factorisé ne
portent pas d'identifiant : la semaine 6 §6.9 les a dérivés et cette semaine ne les réécrit
pas. L'inventaire complet est dans extraction/week-11.md)
{{% /comment %}}
