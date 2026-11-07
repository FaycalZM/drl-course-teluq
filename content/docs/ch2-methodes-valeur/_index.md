---
title: "Module 2 : Méthodes à base de valeur"
weight: 2
bookCollapseSection: true
---

# Module 2 : Méthodes à base de valeur

Le module 1 s'est terminé sur un agent qui ne sait juger qu'une seule chose : un épisode entier, une fois qu'il est fini, réussi ou raté. Rien, dans cette méthode, ne permet de dire qu'une case est meilleure qu'une autre parce qu'elle est plus proche du but. Ce module construit exactement ce qui manquait : un nombre attaché à chaque état, ou à chaque couple état-action, qui dit ce que cet état promet sans qu'il faille attendre la fin de la partie.

La question est donc : jusqu'où va-t-on en n'apprenant qu'une valeur ? Très loin, et par un seul objet, l'**équation de Bellman**, que nous écrivons quatre fois sans jamais changer sa substance. Avec la distribution exacte des successeurs, ce qui donne une table de seize nombres et un FrozenLake glissant résolu en moins d'une seconde. Avec un seul successeur observé, ce qui retire le modèle de l'environnement. Avec une fonction paramétrée à la place de la table, ce qui donne un agent qui apprend à jouer à un jeu vidéo en regardant les pixels de l'écran. Et avec cinq corrections locales, chacune réparant un défaut nommé de la version précédente.

Le remplacement de la table par un réseau est le moment central de ce cours, et il se paie comptant. Nous voyons la divergence se produire sur trois lignes d'arithmétique, puis nous écrivons les réparations d'ingénierie qui font tenir l'édifice, et nous finissons par le chiffre que cette méthode conserve même bien écrite : une exécution sur dix qui ne converge pas du tout. Le module se referme alors sur un problème que personne n'a préparé pour nous, une série de prix, où ni l'observation, ni les actions, ni la récompense ne sont données. La difficulté n'y est plus l'algorithme : le signal utile y est plus petit que le coût d'un aller-retour, et la seule commission de courtage fait passer le même agent, sur la même année, de \(+48\,\%\) à \(-60\,\%\).

> [!WARNING]
 **Trois certitudes tombent en même temps quand la table devient un réseau.** Les valeurs des états cessent d'être découplées, la mise à jour descend un gradient qui n'en est pas tout à fait un, et l'ensemble peut, de façon démontrable, diverger. Les quatre réparations qui suivent sont de l'ingénierie : elles font tenir l'édifice en pratique, elles ne rendent aucune garantie.

---
## La même équation, quatre fois, de seize nombres aux pixels

{{< mermaid >}}
graph TD
  M1["Module 1 : juger un épisode, ou rien"] -->|"il manque une valeur par état"| W4["Semaine 4 : équation de Bellman"]
  W4 -->|"une table ne généralise pas"| W5["Semaine 5 : réseaux Q profonds"]
  W5 -->|"cinq défauts nommés"| W6["Semaine 6 : les cinq réparations"]
  W6 -->|"un agent qui coûte cher"| W7["Semaine 7 : accélérer, puis un vrai problème"]
  W7 --> J2["Jalon 2"]
  J2 --> M3["Module 3 : apprendre la politique"]
{{< /mermaid >}}

Chaque flèche porte l'insuffisance que la semaine suivante corrige, et c'est ce qui donne à ce module sa forme : il avance par réparations successives d'un même programme, non par empilement de méthodes nouvelles. La dernière semaine fait exception, et délibérément. Elle ne répare plus la méthode, elle change de question : comment rendre une exécution bon marché sans toucher à l'algorithme, et comment transformer un problème réel en processus de décision markovien.

---
## Ce que vous saurez faire en entrant dans le module 3

- dériver l'équation de Bellman depuis la seule récurrence du retour, et dire où se place le \(\max\) dans chacune des deux équations d'optimalité ;
- écrire, depuis une page blanche, l'itération sur la valeur, Sarsa et le Q-learning tabulaire, et expliquer ce qui sépare les deux derniers en un symbole ;
- écrire, depuis une page blanche, un réseau Q profond (*deep Q-network*) qui apprend sur CartPole : tampon de rejeu, réseau cible, calendrier d'\(\varepsilon\), et la ligne qui détache la cible du graphe de calcul ;
- auditer un agent donné et y nommer les trois ingrédients de la triade fatale, en disant lequel a été accepté sciemment et pourquoi ;
- implanter au moins deux des cinq extensions sur un socle de code commun, et dire à quel endroit du programme chacune intervient ;
- conduire une étude d'ablation sur plusieurs graines aléatoires, avec un intervalle autour de chaque moyenne, et refuser de conclure d'une exécution unique ;
- mesurer une accélération avec deux indicateurs, le débit de trames et le temps d'horloge jusqu'à un seuil fixé d'avance, et expliquer pourquoi la configuration la plus rapide en trames par seconde peut être la plus lente à résoudre le jeu ;
- formuler en processus de décision markovien un problème qui n'a pas été conçu pour cela, et partager une série temporelle dans le sens qui ne fuit pas.

---
## Le travail évalué de ce module

Le **jalon 2** referme le module et vaut 25 % de la note finale : un réseau Q profond, au moins deux extensions, une comparaison qui tient debout et une accélération mesurée. C'est à partir de ce jalon que toute comparaison, dans ce cours, repose sur plusieurs graines aléatoires et un intervalle de confiance.

[Ouvrir le jalon 2 →]({{< relref "/docs/ch2-methodes-valeur/jalon-2" >}})

{{% comment %}}
Page de module rédigée en phase 4, à partir des quatre pages d'accueil de semaine
(week04 à week07) et de course.yaml. Elle remplace le squelette de phase 1, qui affichait
« Contenu en préparation » et dupliquait la liste des semaines que la barre latérale
produit déjà.

Le chiffre de la commission de courtage et l'exécution sur dix qui ne converge pas sont
repris des pages d'accueil des semaines 7 et 5, sans nouvelle dérivation. Le renvoi au
jalon pointe vers la page de jalon du module, qui relaie vers l'énoncé unique dans
week07/jalon-2.md.
{{% /comment %}}
