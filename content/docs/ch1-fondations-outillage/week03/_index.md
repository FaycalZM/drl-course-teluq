---
title: "Semaine 3 : Méthode d'entropie croisée (CEM)"
weight: 3
bookCollapseSection: true
---

# Semaine 3 : Méthode d'entropie croisée (CEM)

Troisième semaine, et le moment où les deux précédentes se branchent l'une sur l'autre : la boucle d'interaction de la semaine 1, le réseau de la semaine 2, et un agent qui apprend pour la première fois. La méthode tient en une phrase, jouer seize épisodes avec la politique courante, garder les meilleurs, apprendre au réseau à les imiter, recommencer, et son implémentation tient en moins de cent lignes. Elle résout CartPole en une quarantaine de lots. Puis nous reprenons ce même code, **sans y changer une ligne**, et nous le lançons sur un environnement où il n'apprendra rien du tout : c'est la seconde moitié de la semaine, et c'est elle que le jalon 1 évalue.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** les limites d'une méthode se lisent dans la **distribution de ses récompenses**, avant d'écrire la moindre ligne de code. Un histogramme de 200 épisodes aléatoires vous aurait prédit l'échec de FrozenLake en trente secondes, et il vous le prédira sur vos prochains environnements.

---
## Description générale

Les sections 3.1 à 3.3 installent la grille de lecture de tout le cours. Trois axes d'abord : avec ou sans modèle, fondée sur la politique ou sur la valeur, sur politique ou hors politique. Le troisième est celui que les textes emploient le plus souvent sans le définir, et nous le posons proprement : une méthode **sur politique** est le cas particulier d'une méthode hors politique où la politique cible et la politique de comportement coïncident. La section 3.2 rattache ensuite la méthode à la famille des méthodes de Monte-Carlo, critère par critère, et cette correspondance n'est pas décorative : les trois limites de la section 3.5 y sont déjà lisibles. La section 3.3 énonce enfin les **cinq étapes**, la politique vue comme un classifieur, l'échantillonnage de l'action comme unique mécanisme d'exploration, et le **seuil des élites** \(\psi_i\) défini comme un percentile des retours du lot.

Les sections 3.4 à 3.6 passent au code, puis à l'échec, puis à la théorie. La section 3.4 applique la **double lecture** à CEM sur CartPole, du réseau à la boucle, avec quatre points de contrôle dont un **bogue silencieux** : on enregistre l'observation qui a servi à **choisir** l'action, jamais celle qui en résulte, et se tromper ne lève aucune exception. La section 3.5 reprend ce code inchangé et le lance sur FrozenLake, où le seuil des élites reste plat à 0,0 du début à la fin ; la cause tient en quatre maillons, du 70ᵉ percentile d'un ensemble de 0 et de 1 jusqu'à la composition réelle de l'ensemble des élites, et les cinq correctifs qui suivent sont rangés par la limite que chacun attaque. La section 3.6 est **facultative** : elle part de l'échantillonnage préférentiel, passe par la divergence de Kullback-Leibler, et c'est le seul endroit où le nom de la méthode s'explique.

Le laboratoire est formatif et n'est pas noté : trois niveaux, un fil unique, **écrire CEM de bout en bout sur CartPole puis le pousser jusqu'à ce qu'il casse**. Budget de calcul, quelques minutes sur processeur central ; le processeur graphique n'apporte strictement rien ici, puisque le temps passe dans la simulation et non dans le calcul matriciel. Le travail évalué de la semaine est le **jalon 1**, qui vaut 25 % de la note et referme le module 1. Il ne demande pas de réimplémenter la méthode, mais de conduire une **analyse d'échec** : transférer l'agent, produire deux graphiques, expliquer l'effondrement avec vos propres chiffres, appliquer les correctifs et commenter le plateau. Il a sa propre page, juste après le laboratoire.

---
## Mots-clés de la semaine

méthode d'entropie croisée · taxonomie des méthodes d'apprentissage par renforcement · méthode sans modèle · méthode avec modèle · méthode fondée sur la politique · méthode fondée sur la valeur · sur politique · hors politique · politique cible · politique de comportement · couverture · méthode de Monte-Carlo · tâche épisodique · retour non actualisé \(G\) · politique représentée par un réseau de neurones · échantillonnage de l'action · sorties brutes · perte d'entropie croisée · seuil des élites \(\psi_i\) · percentile de sélection des épisodes · épisodes élites · frontière de récompense · codage one-hot · récompense parcimonieuse · limites de la méthode d'entropie croisée · score actualisé · échantillonnage préférentiel · divergence de Kullback-Leibler · log-vraisemblance négative · monde en grille · FrozenLake

---
## En prévision de la semaine suivante

nous avons buté sur une chose précise, et il faut maintenant la nommer. Sur FrozenLake, notre agent ne peut juger un épisode qu'une fois celui-ci terminé, et le verdict est binaire : réussi, raté. Rien, dans toute la méthode, ne sait dire qu'une case est **meilleure** qu'une autre parce qu'elle est plus proche de l'objectif. C'est exactement ce qui manque, et c'est ce que la semaine 4 va construire : une quantité attachée à chaque état, qui mesure ce qu'il promet, et qui se propage de proche en proche sans attendre la fin de l'épisode. La question d'ouverture sera donc « à quoi servent les valeurs, au juste ? », et vous êtes parmi les rares à pouvoir y répondre par une expérience plutôt que par une définition. Gardez vos deux histogrammes sous les yeux : ce sont eux qui justifient tout le module 2.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (D35), imprimé = PDF − 31 pour LAPAN, conformément à MAP-lapan.md,
comme dans le dossier et les notes de phase 1. Les pages S&B sont citées dans l'indexation de
MAP-sb.md, sans conversion.

LAPAN ch. 4 « The Cross-Entropy Method », p. 118-141 : cadrage, moins de 100 lignes, convergence
dans les environnements simples à épisodes courts et récompenses fréquentes, méthode de
référence robuste aux hyperparamètres, fin de la partie 1 du livre (118, 122) ; les trois axes
annoncés puis définis, sans modèle / avec modèle, jeux de plateau et modèles difficiles,
fondée sur la politique / sur la valeur (119) ; hors politique comme apprentissage sur données
historiques, sur politique et données fraîches, troisième axe différé (120) ; partie pratique
et partie théorique, fonction entraînable, politique = classifieur, fig. 4.1 → FIG 03-01,
échantillonnage de l'action comme unique exploration (120-121) ; épisode, retour non actualisé
γ = 1, fig. 4.2 → FIG 03-02, les cinq étapes, percentile 50 ou 70, jeter les mauvais épisodes,
seuil qui monte (121-122) ; une couche cachée de 128 neurones « absolument arbitraire »,
HIDDEN_SIZE/BATCH_SIZE/PERCENTILE, 70ᵉ percentile = 30 % du haut, pas de softmax et argument de
stabilité numérique, exigence de sorties brutes (122-123) ; EpisodeStep et Episode, générateur,
nn.Softmax(dim=1) (124) ; unsqueeze(0), .data puis .numpy(), np.random.choice, quintuplet de
step(), observation qui a choisi l'action = bogue silencieux (125) ; fin d'épisode, yield,
collecte et entraînement dans le même fil, fraîcheur des données (126) ; np.percentile, moyenne
pour journalisation, filtre « < » qui conserve les égalités, FloatTensor/LongTensor (127) ;
gym.make, obs_size, n_actions, CrossEntropyLoss, Adam lr=0,01, corps de boucle, sens de la perte
(128) ; arrêt à 475, critère des 100 épisodes, plafond de 500 pas, itération 0 à 25,2 et
itération 43 à 475,5 (129) ; « pas plus de 50 lots », 30 à 60 lots (130, erreur d'auteur
corrigée) ; render_mode et RecordVideo (131) ; indépendance à l'environnement, exemple de
l'entrepôt, FrozenLake 4 × 4, trous, objectif à 1,0, glissement 0,33, fig. 4.6 → FIG 03-03 (132) ;
Discrete(16)/Discrete(4), reset(), rendu SFFF/FHFH/FFFH/HFFG, DiscreteOneHotWrapper, Box(0,1),
compatibilité à 100 % (133) ; aucune amélioration du score, fig. 4.8 → FIG 03-04 (seuil plat à
0,0), récompense par pas sur CartPole et distribution étalée (134) ; fig. 4.9 → FIG 03-05,
fig. 4.10 → FIG 03-06, deux sortes d'épisodes, échecs dominants, sélection « totalement fausse »,
trois limites (135) ; les cinq correctifs, reward_fun actualisée → EQ 03-E8, percentile sur les
scores, 5 000 itérations pour 50 % (136) ; filtre strict « > », full_batch, saut si vide,
borne à 500, BATCH_SIZE = 100, pas d'apprentissage divisé par 10, ~50 min pour 10 000 itérations,
plateau ~55 % (137) ; régularisation par entropie différée, is_slippery=False, effet
« dramatique », 120-140 itérations, cent fois plus rapide (138) ; « Résolu ! » à l'itération 143,
retour moyen 0,82 (139) ; §4.5 déclarée facultative, x = politique, p(x) = distribution sur les
politiques, H(x) = récompense → EQ 03-E1, approcher p(x)H(x) par q(x), KL → EQ 03-E2, entropie
sans effet sur la minimisation, entropie croisée et origine du nom, q_0 = p, indicatrice →
EQ 03-E3 (140) ; mise à jour de politique → EQ 03-E4, terme de normalisation omis, « minimiser
la log-vraisemblance négative des échantillons les plus réussis » (141, lu sur
index/pages/lapan/0141.png).

SUTTON & BARTO ch. 5 « Monte Carlo Methods » : expérience seule, aucune connaissance de la
dynamique, transitions échantillonnées plutôt que distributions complètes, moyenne de retours
échantillonnés, tâches épisodiques, mise à jour à l'achèvement de l'épisode, retours complets
(113) ; définition sur politique / hors politique (§5.4, 122) ; politique cible et politique de
comportement, hors politique plus général et plus variable, sur politique comme cas particulier,
hypothèse de couverture, apprentissage depuis un contrôleur ou un expert (§5.5, 125) ;
échantillonnage préférentiel et rapport ρ → EQ 03-E9 (placeholder), simplification des
probabilités de transition (§5.5, 125-126) ; ordinaire sans biais mais variance non bornée,
pondéré biaisé et préféré en pratique (§5.5, 127) ; exemple de variance infinie à un seul état
(128-130).

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossier week-03) : sb/ch05/05-02 à 05-04 et 05-08 à 05-13
(≈ 11 300 jetons), tous matière de la semaine 4 ou au-delà de ce que CEM demande ; lapan/ch05 et
au-delà. Aucune fonction de valeur n'apparaît dans cette semaine : ni v_π, ni q_π, ni V(s), ni
équation de Bellman, ni itération sur les valeurs, ni Q-learning tabulaire. S&B éq. 5.4 est
écartée pour cette raison précise : son énoncé passe par v_π.

ÉCARTS ASSUMÉS
- D11 : le total d'un épisode, noté R dans la source, devient G (notation.md §6). La lettre R
  reparaît en section 3.6 uniquement dans R(z), parce que EQ 03-E4 est recopiée telle quelle.
- D11 : H(x) est une récompense dans §4.5 alors que H est une entropie partout ailleurs dans le
  cours (notation.md §5). Le sens est fixé AVANT la première équation de la section 3.6, comme
  la règle l'exige.
- Terminologie tranchée cette semaine : « frontière de récompense » reste le seuil de résolution
  (475 ici, 195 en semaine 1), conformément au glossaire ; le seuil mobile calculé par percentile
  s'appelle « seuil des élites » et se note ψ_i. La source emploie « reward boundary » pour les
  deux ; le cours sépare.
- Erreur d'auteur NON propagée : « 30 à 60 épisodes » (p. 130) se lit « 30 à 60 **lots** », comme
  la parenthèse de la même phrase le confirme (16 épisodes par lot).
- Chiffres du plateau : une seule exécution, deux repères (≈ 5 000 itérations pour 50 %, puis
  plateau ≈ 55 % à 10 000 itérations en ≈ 50 min). La paire 50 min / 55 % est le chiffre de tête.
- Synthèse propre au cours, signalée comme telle dans l'encadré de la section 3.5 : le 70ᵉ
  percentile d'un ensemble de 0 et de 1 vaut exactement 0,0 tant que moins de 30 % des épisodes
  réussissent (p. 135), et le filtre naïf conserve les égalités (p. 127). Les deux faits sont
  dans la source ; leur rapprochement ne l'est pas. C'est la dérivation que le jalon demande de
  reproduire.
- « Méthode de Monte-Carlo » est employée SANS italiques de première occurrence : concepts.yaml
  date ce terme de la semaine 4 et rien ne doit le contredire. La ligne a été ajoutée au
  glossaire avec la semaine 4 en colonne.
- « Amorçage » n'est ni employé ni mis en italiques (ligne 39 du glossaire, semaine 4) : la
  section 3.2 décrit le mécanisme en mots et renvoie explicitement à la semaine 4.
- D15 : tout le code est réécrit (noms français, structures de données en dataclass, annotations
  de type, assertions ajoutées). Rien n'est copié du dépôt de la source.
- D12 : PyTorch nu et Gymnasium uniquement. Aucune bibliothèque d'algorithmes n'est proposée en
  solution courte cette semaine : CEM s'écrit en moins de cent lignes, et c'est l'argument.

DÉCOMPTE : 6 sections · 6 placeholders FIG · 1 placeholder EQ
(les équations 03-E1 à 03-E4 sont recopiées depuis index/equations/lapan-ch04.md, vérifiées sur
les images de page 0140 et 0141 ; 03-E5 à 03-E8 sont écrites directement en KaTeX, notation S&B ;
seule 03-E9, le rapport d'échantillonnage préférentiel, passe par un placeholder.)
{{% /comment %}}
