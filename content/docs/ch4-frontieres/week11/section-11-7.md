---
title: "11.7 L'inversion, et la fin de la semaine"
weight: 8
---

## Un sous-marin, de l'oxygène, et une raison de changer de tâche

Il reste une question, et c'est la seule qui compte vraiment quand on sort d'un tableau de comparaison : **ce classement vaut-il ailleurs ?**

Changeons donc complètement de tâche. Nous passons d'une voiture à deux observations continues à un jeu vidéo dont l'observation est une image : **Seaquest**, un jeu de sous-marin dans lequel le joueur descend chercher des plongeurs à secourir en évitant des poissons hostiles. Il appartient à ce que l'on appelle les **jeux à exploration difficile** (*hard-exploration games*), et sa difficulté est d'un genre très particulier, que je veux détailler parce qu'elle éclaire tout le reste.

Le sous-marin doit gérer son **oxygène**. S'il ne le fait pas, l'épisode se termine après **560 pas** avec une récompense maximale de **20** : l'oxygène s'épuise et le sous-marin meurt. S'il remonte à la surface pour se ravitailler, en revanche, la partie peut durer **presque indéfiniment** et rapporter un score de dix mille à cent mille.

Voilà donc une tâche à deux régimes, séparés par une **seule compétence** : remonter respirer. Et le fait remarquable, qui est la raison pour laquelle cette tâche appartient à notre semaine, est que les méthodes d'exploration traditionnelles **ont du mal à découvrir cela**. Un entraînement s'y bloque normalement à 560 pas, c'est-à-dire exactement au moment où l'oxygène s'épuise, et il y reste.

{{% comment %}}SOURCE: LAPAN ch.18 p.568 (image){{% /comment %}}

Un mot sur le coût de l'expérience, parce qu'il conditionne la lecture de ce qui suit. Chaque exécution de cette série demande **au moins une demi-journée** d'entraînement pour qu'on puisse en observer l'effet. Il y a donc **une seule exécution par méthode**, et aucune des configurations n'est finement réglée : ce sont des mesures d'un dispositif donné, pas des propriétés des méthodes. Je vous demande de les lire exactement dans ces termes.

{{% comment %}}SOURCE: LAPAN ch.18 p.569{{% /comment %}}

---

## Le classement s'inverse, et je ne vais pas l'adoucir

Voici les résultats.

| Méthode | Durée | Retour moyen | Détail |
| --- | --- | --- | --- |
| Réseau Q profond + **ε-glouton** | 13 h | **18** | maximum observé 25 ; quelques épisodes **trouvent l'oxygène** |
| Réseau Q profond + réseaux bruités | 6 h | 6 | nettement moins bon |
| PPO seul, PPO + réseaux bruités, PPO + distillation | non rapportée | 4 | **aucune progression** de la récompense, pour les trois variantes |

{{% comment %}}SOURCE: LAPAN ch.18 p.569-570{{% /comment %}}

Lisez la première ligne, puis relisez le Tableau 11-1. **Sur cette tâche, la méthode \(\varepsilon\)-gloutonne est la meilleure de toutes celles qui ont été essayées.** C'est la même méthode qui, sur MountainCar, n'a pas trouvé le but une seule fois en cinq heures et en cinq cent mille épisodes. Et c'est la seule, ici, dont quelques épisodes découvrent la remontée à la surface.

Les trois variantes de la méthode de politique, elles, n'enregistrent aucun progrès. Un détail s'ajoute à leur sujet, et je vous le donne avec sa réserve : ces trois exécutions sont **moins bonnes** qu'une version antérieure de la même expérience, conduite avec le même code. L'explication avancée pour cet écart est un possible défaut subtil du code ou de l'environnement d'entraînement employés, et cette explication **n'a pas été vérifiée**. Je vous la rapporte comme une hypothèse, non comme un diagnostic, et je ne la reprends pas à mon compte : rien dans ces mesures ne permet de la confirmer ni de l'écarter. Ce que j'en retiens de solide est plus modeste et plus utile : **sur cette tâche, dans ce dispositif, les trois variantes de PPO n'ont pas appris.**

{{% comment %}}SOURCE: LAPAN ch.18 p.570{{% /comment %}}

> [!IMPORTANT]
 **Voici la conclusion de la semaine, et je l'énonce sans précaution oratoire, parce que l'adoucir serait vous mentir.** Un classement de méthodes d'exploration **ne se transfère pas d'un environnement à un autre**. La hiérarchie que la section 11.6 a établie, où la méthode \(\varepsilon\)-gloutonne arrive dernière et de très loin, est vraie sur MountainCar et fausse sur ce jeu. Les deux mesures sont bonnes toutes les deux. Après quatre semaines pendant lesquelles chaque méthode battait la précédente, vous avez besoin de ce constat : la conclusion honnête d'une comparaison est parfois que **la comparaison était locale**. Ce n'est pas un échec de la mesure, c'est une information sur le domaine, et c'est même ainsi que certaines directions de recherche s'ouvrent : un résultat qui contredit l'attente est un endroit où quelque chose reste à comprendre.

{{% comment %}}SOURCE: LAPAN ch.18 p.569{{% /comment %}}

Je veux maintenant expliquer pourquoi ce renversement n'est pas absurde, et je le fais prudemment, en distinguant ce que je sais de ce que je conjecture.

Ce que je sais : les deux tâches n'ont pas la même structure d'exploration. Sur MountainCar, il faut une **longue séquence coordonnée**, des dizaines d'actions dans le bon ordre, et le hasard pas-à-pas ne la produit jamais. Sur le jeu de sous-marin, il y a beaucoup de choses à faire qui rapportent un peu, des plongeurs à récupérer, des poissons à éviter, et une seule compétence rare à découvrir. Une récompense dense et abondante accompagne donc l'exploration d'un bout à l'autre de l'entraînement.

Ce que je conjecture, et je le signale comme tel : c'est probablement cette abondance qui fait la différence. Là où la récompense extrinsèque suffit à guider l'apprentissage, une prime de nouveauté ajoute surtout du bruit à un signal qui fonctionnait, et un bruit cohérent sur les poids ne vaut pas mieux qu'un bruit incohérent sur les actions. Je n'ai pas de mesure qui établisse cette explication, et je ne vous la donne donc pas comme un résultat.

> [!TIP]
 **La règle pratique que je tire de ces deux sections, et c'est celle que j'appliquerais sur un nouveau projet.** Avant de choisir une méthode d'exploration sophistiquée, **mesurez une seule chose** : votre agent rencontre-t-il jamais la récompense qui compte ? Cela se journalise en trois lignes, comme la section 11.5 l'a montré. Si la réponse est oui, même rarement, commencez par la méthode la plus simple et dépensez votre temps ailleurs, parce que vous êtes dans le régime du jeu de sous-marin. Si la réponse est non, aucun raffinement de l'algorithme d'apprentissage ne vous sauvera et c'est **là** qu'il faut investir, parce que vous êtes dans le régime de MountainCar. Cette question coûte dix minutes d'instrumentation et elle décide de l'ordre dans lequel vous devez travailler.

---

## Ce que cette semaine ne couvre pas, et pourquoi je le nomme

Je ferme le contenu de la semaine par un inventaire de ses lacunes, parce que savoir où s'arrête ce que l'on sait fait partie de ce que ce cours essaie de vous transmettre.

**La théorie manque, et elle manque entièrement.** La définition formelle d'une exploration efficace, les bornes de confiance qui justifient la forme de la prime de la section 11.3, l'analyse du regret qui les accompagne : rien de cela n'est dans cette semaine, et je ne l'ai remplacé par aucune formule décorative. La prime est posée, son origine est nommée, et c'est tout ce que je peux honnêtement en dire.

**La construction complète du pseudo-comptage manque aussi**, et la section 11.3 l'a signalée comme une esquisse. **Le bruit de paramètres** est nommé et non traité. **La boucle à deux têtes de valeur** de la section 11.4 est décrite dans son principe et n'est pas écrite.

Et deux sujets voisins sont **délibérément reportés**, parce qu'ils demandent des outils que le cours n'a pas encore. L'**exploration par curiosité**, nommée en section 11.3, demande un modèle de la dynamique de l'environnement : c'est la semaine 13. Et une tout autre façon de diriger une exploration, par la **planification** plutôt que par une prime, arrive la semaine prochaine : explorer un arbre de possibilités en décidant à chaque nœud lequel mérite d'être approfondi est une exploration dirigée, et la règle de sélection qui gouverne ce choix est, elle, construite sur une borne de confiance. Vous y retrouverez donc, par un autre chemin, l'idée que cette semaine a dû poser sans la démontrer.

Enfin, un dernier mot sur l'ampleur du sujet lui-même : l'exploration est un domaine beaucoup plus vaste que ces sept sections, et de nombreuses méthodes intéressantes restent en dehors de ce cours. Le but de cette semaine n'était pas de les couvrir, il était de vous rendre capables de reconnaître le problème, de le mesurer, et de choisir entre trois familles en sachant ce que chacune fait au problème que vous résolvez.

{{% comment %}}SOURCE: LAPAN ch.18 p.570{{% /comment %}}

---
