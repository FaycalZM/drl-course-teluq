---
title: "Introduction"
weight: 1
---

## Deux moitiés qui ne font pas le même métier, et un jalon qui les joint

Bonjour à toutes et à tous ! La semaine 6 s'est terminée sur un constat que j'avais laissé exprès en suspens : après cinq réparations du réseau Q profond, notre agent reste **lent**. Quelques centaines de milliers de trames pour un jeu simple, des heures de calcul, et un débit qui a baissé à mesure que nous l'améliorions. Cette semaine attaque l'autre moitié du problème, celle dont on parle rarement dans un cours et tout le temps dans un laboratoire : comment rendre une exécution **bon marché**, sans toucher à la méthode.

Puis, à la section 7.7, la semaine change complètement de sujet. Nous quittons les jeux pour un problème réel, où plus rien n'est donné : ni l'observation, ni les actions, ni la récompense. Il faut les inventer, et c'est là que se trouve la difficulté, pas dans le choix de l'algorithme.

Je vous annonce donc franchement la forme de la semaine, parce que vous allez la sentir au passage de 7.6 à 7.7 : **les deux moitiés ne partagent aucun sujet**. La première est de l'ingénierie de performance, la seconde est de la modélisation. Ce qui les joint n'est pas une transition rhétorique, c'est le **jalon 2**, qui vaut 25 % de la note finale et qui demande exactement les deux : une accélération **mesurée**, et une comparaison qui **tient debout**. L'une vous apprend à produire des chiffres rapidement, l'autre à ne pas les croire trop vite.

{{% comment %}}SOURCE: LAPAN ch.9 p.284{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.10 p.304{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

Et une phrase à garder sous les yeux pendant les sept jours, parce qu'elle gouverne tout le reste, y compris l'ordre dans lequel le laboratoire est écrit : **mieux vaut un programme lent et juste qu'un programme rapide et faux.** Toute optimisation n'a de sens que si la méthode fonctionne déjà.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Dire ce qu'une accélération achète réellement dans un projet d'apprentissage par renforcement, et pourquoi la bonne unité est le **nombre d'expériences** et non la durée d'une exécution.
- Calculer la durée d'un entraînement à partir d'un débit en trames par seconde et d'un budget de trames, et convertir un débit « trames brutes » en débit « pas de l'agent ».
- Énoncer les **deux** indicateurs d'un banc d'essai d'apprentissage par renforcement, et dire ce qu'une mesure d'un seul des deux rend invisible.
- Fixer un critère d'arrêt **avant** de lancer une exécution, et dire pourquoi l'ordre importe.
- Justifier qu'une comparaison repose sur plusieurs **graines aléatoires** avec un **intervalle de confiance**, et écrire cet intervalle.
- Distinguer `detach()` de `torch.no_grad()` : lequel est une question de **correction**, lequel est une question de **vitesse**, et ce qui casse si on les échange.
- Nommer les trois usages du réseau dans une boucle de réseau Q profond et dire, pour chacun, s'il a besoin de gradients.
- Expliquer pourquoi le réflexe supervisé « augmenter la taille du lot » ne se transporte pas tel quel en apprentissage par renforcement.
- Mettre en place \(N\) **environnements vectorisés**, dire ce que \(N\) ajoute comme hyperparamètre, et reconnaître le point où davantage de débit achète moins de convergence.
- Dire **où exactement** la boucle d'entraînement peut se couper en deux processus, et pourquoi c'est précisément à cet endroit.
- Nommer les enveloppes de la pile Atari classique, dire à quoi chacune sert, et justifier le retrait de celles qui ne servent pas à un jeu donné.
- Lire un tableau d'accélérations à **deux colonnes de résultats** et expliquer un cas où le classement en débit et le classement en temps se contredisent.
- Formuler un problème réel en processus de décision markovien, en justifiant séparément le choix de l'observation, celui des actions et celui de la récompense.
- Écrire les **deux** schémas de récompense d'un agent de négociation, et démontrer qu'ils ne définissent pas le même objectif, pour trois raisons distinctes.
- Écrire la **représentation relative** des prix, dire quelle information elle détruit, et pourquoi on l'adopte malgré cela.
- Énoncer le protocole de validation d'une série temporelle, et les trois conséquences d'un partage pris à l'envers.
- Remplir l'API `Env` de Gymnasium à la main : espace d'observation, espace d'actions, `reset`, `step`, et la position comme composante de l'état.
- Dire pourquoi un agent de négociation sans la position dans son état ne résout pas un processus de décision markovien.
- Calculer le coût d'un aller-retour en points de récompense, et montrer qu'un terme de coût peut **inverser le signe** d'un résultat sans changer la politique.
- Énoncer les conditions exactes sous lesquelles un résultat de simulation historique a été obtenu, et dire ce qu'il ne permet pas de conclure.
- Nommer la comparaison manquante d'une étude de rendement, et la définir assez précisément pour la calculer.
- Produire un tableau d'accélération complet, avec graines, intervalles et matériel, et en tirer une conclusion défendable.

---

## Prérequis et outils

De la semaine 6, tout le socle : le réseau Q profond avec ses extensions, le socle de code unique du volet C, l'étude d'ablation, l'architecture duale, le double DQN et la cible à \(n\) étapes. La seconde moitié de la semaine les réutilise **sans les modifier**, et c'est tout l'intérêt. De la semaine 5 : le tampon de rejeu, le réseau cible, le détachement du graphe, la pile d'enveloppes d'environnement, l'empilement de trames et le saut de trames. De la semaine 2 : le graphe de calcul de PyTorch, les tenseurs feuilles, la rétropropagation, la convolution, et le surapprentissage, dont la seconde moitié de la semaine donne l'exemple le plus net de tout le cours.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les deux volets du laboratoire ; au volet A, la contrainte du processeur graphique partagé est un atout pédagogique et non un obstacle |
| **Gymnasium** | `CartPole-v1` au volet A ; au volet B, l'API `Env` est remplie **à la main** |
| **PyTorch** | `torch.no_grad()`, `detach()`, `torch.multiprocessing`, et les deux architectures de la section 7.11 |
| **NumPy** | les séries de prix, le codage de l'état, le tirage de l'offset de départ |
| **Matplotlib** | les courbes à moyenne et intervalle, et la courbe de profit cumulé |
| **Jeu de données fourni** | deux années de cotations à la minute, livrées avec le carnet du volet B : vous n'avez **aucune** donnée de marché à aller chercher |
| **Page « Notation » du cours** | la convention \(S_t, A_t, R_t\) appliquée à un problème qui n'est pas un jeu |
| **Page « Glossaire » du cours** | une trentaine de termes nouveaux y entrent cette semaine, dont une quinzaine de vocabulaire financier |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

Avant d'entrer dans le vif, un point de vocabulaire, et il va servir deux fois.

> [!IMPORTANT]
 **Le mot « référence » va désigner deux choses dans ce cours, et je les sépare maintenant.** Cette semaine, une **version de référence** (*baseline version*) est la configuration non modifiée d'un banc d'essai, celle contre laquelle on mesure toutes les autres : c'est un objet de protocole expérimental. En semaine 8, vous rencontrerez une **référence** (*baseline*) au sens des méthodes de gradient de politique, qui est une quantité soustraite d'un retour pour réduire sa variance : c'est un objet mathématique. Les deux sens n'ont rien à voir l'un avec l'autre. Dans cette semaine, j'écrirai toujours « version de référence » en entier, et jamais « référence » tout court.

{{% comment %}}SOURCE: source-assets/glossaire.md{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

---
