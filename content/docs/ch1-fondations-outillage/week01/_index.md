---
title: "Semaine 1 : Rappels RL et API Gymnasium"
weight: 1
bookCollapseSection: true
---

# Semaine 1 : Rappels RL et API Gymnasium

Bienvenue dans la première semaine de ce cours. Vous arrivez avec le vocabulaire de l'apprentissage par renforcement classique ; nous allons le rendre **précis** (avec l'exactitude dont nous aurons besoin pendant quatorze semaines), puis le brancher sur l'outil qui nous accompagnera jusqu'au bout, l'interface Gymnasium. Deux moitiés, donc : le cadre mathématique d'abord, le code ensuite.

> [!IMPORTANT]
 **Si vous ne devez retenir qu'une ligne de cette semaine, retenez celle-ci :** l'amorçage se fonde sur `terminated`, jamais sur `truncated`. Nous n'avons pas encore écrit la perte qui le démontre : elle arrive.

---
## Description générale

Les sections 1.1 à 1.5 construisent le cadre. Nous situons d'abord l'apprentissage par renforcement face aux deux autres paradigmes et nommons les trois difficultés qui lui sont propres ; nous fixons ensuite les cinq entités (agent, environnement, action, récompense, observation) en insistant sur la distinction entre **état** et **observation**. Puis nous montons les trois étages du formalisme, un ingrédient à la fois : le **processus de Markov**, le **processus de Markov avec récompense** avec son retour et son facteur d'actualisation, enfin le **processus de décision markovien** et sa **politique**.

Les sections 1.6 à 1.10 branchent ce cadre sur du code. Nous écrivons la boucle d'interaction à la main, sans aucune bibliothèque, avant de la confier à l'API Gymnasium : les classes `Env` et `Space`, les deux espaces d'un environnement, le quintuplet de `step()` et la table de correspondance *symbole ↔ variable* qui relie le formalisme à ce que vous tapez réellement. Nous mesurons enfin un agent aléatoire sur CartPole, puis nous posons une **enveloppe** sur l'environnement pour le modifier sans le réécrire.

Le laboratoire ne contient **aucun réseau de neurones** : chaque exercice s'exécute en quelques secondes, ce qui vous autorise à répéter une mesure cent fois plutôt qu'à la commenter une fois. Vous y produirez vous-même le chiffre de départ du cours (la récompense d'une politique uniforme sur CartPole, à comparer à la frontière de 195), et vous instruirez par la mesure le choix de l'environnement de votre projet, attendu au premier jalon.

---
## Mots-clés de la semaine

apprentissage par renforcement · agent · environnement · observation · état · action discrète / continue · récompense · données non i.i.d. · dilemme exploration-exploitation · récompense différée · processus de Markov · propriété de Markov · espace d'états · matrice de transition · épisode · stationnarité · processus de Markov avec récompense · retour \(G_t\) · facteur d'actualisation \(\gamma\) · valeur d'état \(v(s)\), \(v_\pi(s)\) · processus de décision markovien · espace d'actions · politique \(\pi(a \mid s)\) · bandit manchot · Gymnasium · `Env` · `Space` · `Discrete` · `Box` · `reset()` · `step()` · terminaison · troncature · frontière de récompense · enveloppe · `ActionWrapper`

---
## En prévision de la semaine suivante

Nous avons soigneusement évité les réseaux de neurones, et vous avez peut-être remarqué que la ligne « décider » de notre agent est restée désespérément vide : un tirage au hasard. La semaine 2 va la remplir. Nous passerons à PyTorch : tenseurs, différentiation automatique, construction et entraînement d'un réseau. Rien d'apprentissage par renforcement là-dedans, et c'est assumé : il nous faut l'outil avant de l'utiliser. Préparez votre environnement Colab et gardez la table de correspondance de la section 1.8 sous les yeux : nous y brancherons un réseau dès la semaine 3.

{{% comment %}}
SOURCES COMPLÈTES (D17/D18, invisible aux étudiants)

Pagination : indices PDF (imprimé = PDF − 31), conformément à MAP-lapan.md, comme dans le
dossier et les notes de phase 1.

LAPAN ch. 1 « What Is Reinforcement Learning? », p. 35-56 : paradigmes et souris-robot
(35-37) ; trois difficultés (37-38) ; fig. 1.2 → FIG 01-01 (38) ; récompense, huit scénarios,
score d'arcade (39-40) ; agent, environnement, trois canaux (40-41) ; actions discrètes /
continues (41) ; état vs observation (42-43) ; six domaines (44) ; processus et propriété de
Markov, matrice beau/pluie, définition (S, T) → EQ 01-E1 (45-46) ; chaîne « employé de
bureau », fig. 1.5 → FIG 01-02 (47-48) ; matrice en pourcentages, fig. 1.6 → FIG 01-03 (48-49) ;
épisode, comptage, stationnarité (49) ; actualisation, retour, valeur d'état → EQ 01-E2,
01-E3 (50-51) ; récompenses du DRP et calcul γ = 0 (0,3 / 2,1 / 1,0 / 2,8), fig. 1.7 →
FIG 01-04 (51-52) ; divergence à γ = 1, bandit manchot, calcul différé (53) ; pavé
|S|×|S|×|A|, fig. 1.9 → FIG 01-05 (53-54) ; robot 3×3, 36 états, moteurs imparfaits, récompense
conditionnée (55-56) ; politique → EQ 01-E4 et « une politique fixée ramène un MDP à un MRP » (56).

LAPAN ch. 2 « OpenAI Gym API and Gymnasium », p. 57-80 : environnement et agent jouets, boucle
observer → décider → agir → encaisser, épisodes finis / infinis (59-62) ; Gym 2017 → Gymnasium
2021 (Farama), les quatre services, bornes continues, observations discrètes (64-65) ; classe
Space, Discrete, Box, écran Atari, fig. 2.1 → FIG 01-06 (66) ; Tuple et les deux membres Space
(67) ; reset() → (obs, info), step() → quintuplet, truncated distinct de done (67-69) ;
CartPole, session, bornes, sample() (71-73) ; agent aléatoire 12 pas, 12-15 pas, frontière 195,
« deux tiers de l'interface » (74-75) ; enveloppes, Wrapper, trois sous-classes, enveloppe
ε-aléatoire, fig. 2.4 → FIG 01-07 (75-77) ; HumanRendering, RecordVideo, render_mode (78-79) ;
reste du catalogue (80).

SUPPLÉMENT C3, Documentation Gymnasium (Farama), gymnasium.farama.org : catalogue officiel des
environnements, qui supersède le recensement du chapitre 2 (chunk 02-06, écarté du dossier) ;
liste des enveloppes ; cible du jalon 1. Confirme que le step() à cinq valeurs et le
reset() → (observation, info) sont inchangés depuis Gym v0.26, d'où l'absence de version
épinglée dans ce cours.

NON LU / VOLONTAIREMENT ÉCARTÉ (voir dossier week-01) : lapan/ch01/01-01 ; lapan/ch02/02-02
(nomme PTAN → D12, semaine 6) ; lapan/ch02/02-06. Bellman, itération sur les valeurs et
Q-learning tabulaire → semaine 4. Sutton & Barto non lu, donc aucune équation ne passe par un
placeholder (D11, D28).

ÉCARTS ASSUMÉS
- D11 : le V(s) de la source devient v(s) en section 1.4 (MRP, aucune politique) puis v_π(s)
 en section 1.5 dès que π existe ; le pont est la remarque de la source elle-même (p. 56).
- Terminologie : la source nomme `done` le troisième élément de step() ; le cours écrit
 `terminated` et le signale explicitement une fois (section 1.8).
- Trois erreurs d'auteur repérées en phase 1 et NON propagées : « extend our MDP » p. 53 (lire
 MRP) ; « Cofee » p. 51 ; `obs = env.reset()` et `obs, reward, done, _, _ = env.step(0)` p. 77.
- Justification de la troncature (amorçage sur `terminated` seul) : absente de la source,
 construite en phase 1 comme crochet vers les semaines 5, 8 et 10.
- **« 12 à 15 pas » (p. 74-75) n'est PAS repris comme fait du cours.** La source donne ce
 chiffre pour l'agent aléatoire, mais une politique uniforme sur `CartPole-v1` mesure
 couramment davantage, et aucune vérification n'était possible (gymnasium n'est pas, et ne
 doit pas être, installé dans le venv de rédaction). Le cours écrit donc « quelques dizaines
 de pas » / « un ordre de grandeur sous 195 » et confie le chiffre exact à la mesure du
 laboratoire. La frontière de 195, elle, est vérifiée sur l'image de page et reste exacte.
- D15 : tout le code est réécrit (noms, structure, annotations de type) ; rien n'est copié.

DÉCOMPTE : 10 sections · 7 placeholders FIG · 0 placeholder EQ
(les quatre équations 01-E1 à 01-E4 sont écrites directement en KaTeX, notation S&B.)
{{% /comment %}}
