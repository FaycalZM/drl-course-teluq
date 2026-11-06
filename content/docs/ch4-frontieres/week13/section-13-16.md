---
title: "13.16 Le pont que cette semaine ne franchit pas"
weight: 17
---

## Les deux moitiés de la semaine se rejoignent, et c'est délicat

Cette semaine a deux moitiés, et vous avez sans doute déjà formé la question évidente : **que se passe-t-il si on apprend un modèle du monde à partir d'un jeu de données figé ?** La première moitié économise l'interaction, la seconde la supprime ; la combinaison semble tentante, et elle est effectivement un domaine de recherche à elle seule. Cette semaine ne la traite pas, parce qu'elle a déjà deux cœurs et qu'un troisième aplatirait les deux. Mais je veux nommer la difficulté, parce qu'elle est le plus beau résumé de la semaine.

Reprenez le mécanisme de la section 13.14, et remplacez « valeur d'action » par « transition ». Le phénomène porte alors un autre nom, l'**exploitation du modèle** (*model exploitation*), et c'est le même. La politique est optimisée pour obtenir le retour le plus élevé **sous le modèle courant**. L'optimisation peut donc la pousser à produire des états et des actions hors distribution, là où le modèle **prédit à tort des états successeurs qui mènent à des retours plus élevés que les vrais états successeurs**.

{{% comment %}}SOURCE: OFFLINE p.26-27{{% /comment %}}

C'est **exactement** le mécanisme de la section 13.14, déplacé de \(Q\) vers \(T\). Et c'est **exactement** la faiblesse du chemin déterministe de la section 13.3, celle que le planificateur exploitait. Trois fois le même phénomène dans une seule semaine, sous trois noms différents : exploitation d'un modèle par un planificateur, croissance de l'erreur sur une valeur d'action hors ligne, et exploitation du modèle en régime hors ligne. Si vous ne reteniez qu'une structure de cette semaine, retenez celle-ci : **un optimiseur branché sur un estimateur non contraint hors distribution trouve les erreurs de cet estimateur**, et la seule chose qui l'en empêche d'ordinaire est la possibilité de vérifier.

---

## La borne qui dit où va le coût

Il existe une borne pour ce cas, et son intérêt est moins sa valeur numérique que la **lecture** qu'on en fait.

$$
J(\pi) \;\ge\; J_\theta(\pi) - \left[ \frac{2\gamma\, r_{\max}\,(\epsilon_m + 2\epsilon_\pi)}{(1-\gamma)^2} \;+\; \frac{4\, r_{\max}\, \epsilon_\pi}{1-\gamma} \right]
$$

où \(J(\pi)\) est le retour réel de la politique, \(J_\theta(\pi)\) son retour **sous le modèle appris**, \(\epsilon_m = \max_t \E_{d^\pi_t}\big[D_{\mathrm{TV}}(T_\theta \,\|\, T)\big]\) l'erreur du modèle mesurée en distance en variation totale, et \(\epsilon_\pi\) l'écart entre la politique apprise et la politique de comportement sur les états échantillonnés.

{{% comment %}}SOURCE: OFFLINE p.27{{% /comment %}}

La lecture est la suivante. Le **second** terme est l'erreur accumulée par le décalage de **politique** : il ne dépend que de \(\epsilon_\pi\), et il croît en \(1/(1-\gamma)\). Le **premier** est l'erreur accumulée par le décalage de **modèle** : il croît en \(1/(1-\gamma)^2\), donc beaucoup plus vite. Et le détail qui mérite l'attention : **le premier terme dépend aussi de \(\epsilon_\pi\)**. Ce n'est pas une maladresse d'écriture, c'est le cœur du problème : une politique qui s'écarte davantage de la politique de comportement conduit à des états plus éloignés de la distribution des données, **ce qui rend les erreurs du modèle plus probables**. Les deux décalages ne s'additionnent pas, ils se **multiplient**.

---

## Et la conséquence pratique, qui tient en un mot : court

De cette borne découle une recommandation, et elle est la raison pour laquelle je tenais à mettre cette section dans la semaine. Si appliquer le modèle de façon récursive fait croître l'erreur, alors **des déroulements plus courts doivent en accumuler beaucoup moins**.

{{% comment %}}SOURCE: OFFLINE p.27{{% /comment %}}

D'où la recette : **des déroulements courts, branchés sur des états que les données contiennent**. On ne part jamais de rien, on part d'un état réel, on imagine quelques pas, et on arrête. Vous avez déjà rencontré exactement cela deux fois cette semaine : la section 13.9 branche chaque trajectoire imaginée sur un état réel encodé depuis les données, et la section 13.5 ne joue jamais plus que le premier pas de son plan. Dans les trois cas, le principe est le même, et il est la seule défense générale contre l'accumulation : **ne jamais s'éloigner longtemps de ce qu'on a vu**.

> [!TIP]
 **Une dernière idée, qui répond à une objection que vous vous êtes peut-être faite depuis la section 13.12 : comment une politique peut-elle être meilleure que les données qui l'ont entraînée ?** Si le jeu de données ne contient que des trajectoires médiocres, d'où pourrait sortir une bonne politique ? La réponse s'appelle la **recomposition de trajectoires** (*trajectory stitching*), et elle est simple et belle. Supposez que le jeu contienne une trajectoire qui va du point 1 au point 2, et une autre, produite dans un tout autre contexte, qui va du point 2 au point 3. Aucune des deux ne va de 1 à 3. Mais une méthode qui apprend une **valeur** et non une imitation peut **assembler** les deux morceaux, parce que la remontée de Bellman passe par l'état intermédiaire sans se préoccuper de savoir quelle trajectoire l'a produit. C'est la réponse honnête à la question, et c'est aussi ce qui explique qu'un clonage de comportement ne puisse jamais dépasser les données alors qu'une méthode fondée sur la valeur, elle, le peut. Les bancs d'essai du domaine, dont le plus employé s'appelle D4RL, mesurent explicitement cette capacité en construisant des jeux de données faits de morceaux.

{{% comment %}}SOURCE: OFFLINE p.29{{% /comment %}}

---

## Le lien avec le jalon 4, et il est direct

Je termine par la raison pour laquelle cette moitié de semaine arrive juste avant le jalon 4.

**Les données que votre projet a déjà collectées constituent un jeu de données figé.** Ce ne sont pas des données d'entraînement en ligne : ce sont des transitions produites par une politique donnée, à un moment donné, et qui ne bougeront plus. Toute question que vous leur posez sur une **autre** politique est une question contrefactuelle, au sens exact de la section 13.13. Et en particulier : **évaluer une politique sur un jeu de données qu'elle n'a pas produit est un problème hors ligne**, avec toutes les difficultés de la section 13.14 et aucune de ses solutions, puisqu'une évaluation n'a même pas la ressource de contraindre la politique.

Gardez donc deux réflexes de cette semaine pour la suivante. Le premier : **demandez toujours qui a produit les données sur lesquelles un chiffre a été calculé**. Le second : si la réponse est « une autre politique que celle qu'on évalue », alors le chiffre porte une incertitude qui n'est pas dans sa barre d'erreur, et cette incertitude ne diminue pas quand on ajoute des données de la même provenance.

---
