---
title: "8.5 Quatre problèmes, nommés"
weight: 6
---

## Le point de bascule de la semaine

Nous arrivons à la section la plus importante de la semaine sur le plan de la structure. Tout ce qui précède a construit un algorithme qui fonctionne sur CartPole ; tout ce qui suit répare les quatre choses qui l'empêchent de fonctionner ailleurs.

Je procède comme en semaine 6, où nous avions nommé les cinq défauts du réseau Q profond avant d'aller chercher leurs cinq réparations. Le bénéfice de cette façon de faire est double : vous saurez à tout instant **à quelle question** une technique répond, et vous saurez reconnaître, dans un article ou un dépôt que vous lirez plus tard, quel problème son auteur essayait de résoudre. Une technique sans son problème est une recette ; une technique avec son problème est une méthode.

Voici les quatre, dans l'ordre, avec la section qui y répond. **Lisez ce tableau maintenant et revenez-y à chaque section de la semaine.**

| nº | Le problème | Ce qui y répond | Où |
| --- | --- | --- | --- |
| 1 | **Les épisodes complets sont exigés** : rien ne peut être mis à jour avant la fin d'un épisode | le déroulement de l'équation de Bellman sur \(N\) pas, **ou** un \(\hat v(s,\mathbf{w})\) appris, c'est-à-dire le critique | 8.9, et les sections 8.7 et 8.8 pour le critique |
| 2 | **La variance du gradient est élevée** : l'échelle \(G_t\) dépend fortement de l'environnement | la **référence**, puis la référence dépendante de l'état \(\hat v\), c'est-à-dire l'avantage | 8.6, puis 8.7 |
| 3 | **L'exploration s'éteint** : la politique se verrouille sur un optimum local | la **prime d'entropie** | 8.9 |
| 4 | **Les échantillons sont corrélés** : une trajectoire n'est pas un échantillon indépendant | les environnements **parallèles ou vectorisés** | 8.9, puis 8.10 |

{{% comment %}}SOURCE: LAPAN ch.11 p.341-344{{% /comment %}}

Remarquez tout de suite une chose : le problème 1 a **deux** réponses, et la seconde, le critique, est aussi la réponse raffinée du problème 2. C'est ce chevauchement qui fait que la semaine converge vers un seul objet, A2C, au lieu de quatre correctifs indépendants.

---

## Problème 1 : les épisodes complets sont exigés

REINFORCE a besoin de \(G_t\), le retour complet depuis \(t\) jusqu'à la fin. Il faut donc **attendre la fin de l'épisode** avant de pouvoir mettre à jour quoi que ce soit. Et la situation est pire que cela : les deux méthodes que nous avons écrites jusqu'ici, REINFORCE comme la méthode d'entropie croisée, se comportent **mieux** quand on accumule plusieurs épisodes par mise à jour, parce que la moyenne sur plusieurs trajectoires réduit le bruit. L'incitation va donc dans le mauvais sens : plus la méthode est stable, plus elle attend.

{{% comment %}}SOURCE: LAPAN ch.11 p.341-342{{% /comment %}}

Sur CartPole, cela ne coûte rien, et c'est précisément ce qui rend le problème invisible aux débutants : les premiers épisodes durent à peine dix pas, puisque le pendule tombe immédiatement. Sur un jeu Atari, un épisode dure des centaines ou des milliers de trames, et il faut en accumuler plusieurs. Vous passez alors la quasi-totalité de votre temps à collecter des données avec une politique que vous savez déjà perfectible, sans avoir le droit de l'améliorer.

{{% comment %}}SOURCE: LAPAN ch.11 p.342{{% /comment %}}

Maintenant, posons la bonne question : **à quoi sert l'épisode complet ?** À une seule chose, obtenir une estimation exacte de \(Q(s,a)\), c'est-à-dire du retour. Formulé ainsi, le problème se rapproche de quelque chose que nous savons faire. En semaine 5, le réseau Q profond a remplacé le retour exact par une estimation en un pas, \(Q(s,a) = r_a + \gamma V(s')\), l'équation de Bellman tronquée. Mais ici nous ne pouvons pas faire la même chose, pour une raison évidente et qu'il faut énoncer : dans un gradient de politique **nous n'avons ni \(V(s)\) ni \(Q(s,a)\)**. Nous avons éliminé la valeur, c'était tout le programme de la section 8.1.

Il y a donc deux sorties, et elles font le reste de la semaine. La première est de **demander au réseau d'estimer \(V(s)\)** : nous obtiendrons alors la valeur de la queue de trajectoire sans la jouer, et c'est la route acteur-critique des sections 8.7 et 8.8. La seconde est de **dérouler l'équation de Bellman sur \(N\) pas** : on joue \(N\) pas réels, on actualise, et on accepte de tronquer là.

{{% comment %}}SOURCE: LAPAN ch.11 p.342{{% /comment %}}

Pourquoi tronquer est-il acceptable ? Pour une raison arithmétique que je vous invite à vérifier de tête. Avec \(\gamma = 0{,}9\), le coefficient qui pèse la récompense du dixième pas vaut \(0{,}9^{10} \approx 0{,}35\), et celui du cinquantième \(0{,}9^{50} \approx 0{,}00515\). Autrement dit, au-delà de quelques dizaines de pas, la contribution d'une récompense au retour devient négligeable devant le bruit de l'estimation. Avec \(\gamma = 0{,}99\), la décroissance est plus lente et il faut davantage de pas, mais le principe tient : un horizon fini bien choisi approche le retour infini à une précision inférieure à celle que notre échantillonnage nous donne de toute façon.

{{% comment %}}SOURCE: LAPAN ch.11 p.342{{% /comment %}}

---

## Problème 2 : la variance du gradient est élevée

Le théorème nous a donné un gradient proportionnel à \(G_t\). Le problème est que \(G_t\) est une quantité dont l'échelle dépend entièrement de l'environnement, et sur laquelle nous n'avons aucun contrôle.

Prenez CartPole, où chaque pas rapporte 1. Tenir le pendule cinq pas donne un retour de l'ordre de 5 ; le tenir cent pas donne un retour de l'ordre de 100. Le gradient produit par un échantillon réussi est donc **vingt fois** plus grand que celui produit par un échantillon raté, et ce facteur n'a rien à voir avec la qualité de l'information que chaque échantillon porte : il reflète seulement l'unité dans laquelle l'environnement compte ses points. Conséquence directe : **un seul épisode chanceux peut dominer le gradient final** du lot, et la direction de mise à jour est alors décidée par un accident.

{{% comment %}}SOURCE: LAPAN ch.11 p.342{{% /comment %}}

Le remède est aussi simple que l'énoncé : **soustraire une référence** de \(G_t\), de façon que l'échelle du gradient mesure un écart et non un niveau. Trois candidats se présentent, par ordre croissant de raffinement, et nous les rencontrerons tous les trois dans cette semaine :

1. une **constante**, en général la moyenne des retours actualisés observés ;
2. une **moyenne glissante** de ces retours, qui suit la progression de l'agent ;
3. la **valeur de l'état**, \(V(s)\), qui est la seule des trois à distinguer les situations.

{{% comment %}}SOURCE: LAPAN ch.11 p.342-343{{% /comment %}}

La section 8.6 traite le cas général et démontre pourquoi l'opération est licite. La section 8.7 montre pourquoi le troisième candidat est le bon, et ce qu'il faut pour l'obtenir.

---

## Problème 3 : l'exploration s'éteint

Nous avons salué, en section 8.3, le fait qu'une politique stochastique explore d'elle-même. Il faut maintenant regarder le revers.

Rien ne garantit que cette exploration dure. La politique part d'une distribution presque uniforme, puis se resserre autour de ce qui a marché ; et comme la règle de mise à jour récompense l'exploitation de ce qui a déjà été trouvé, la politique devient **progressivement de moins en moins aléatoire** au fil de l'entraînement. Le degré de hasard restant dépend des conditions initiales et de la trajectoire de l'entraînement, c'est-à-dire d'éléments que vous ne contrôlez pas. Et l'issue défavorable est claire : la politique peut se verrouiller sur un **optimum local**, cesser d'explorer, et y rester indéfiniment, parfaitement satisfaite d'une solution médiocre.

{{% comment %}}SOURCE: SPINUP vpg/exploration-vs-exploitation{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.11 p.343{{% /comment %}}

Une politique \(\varepsilon\)-gloutonne par-dessus la politique apprise fonctionnerait, techniquement. Mais les méthodes de gradient de politique permettent quelque chose de nettement plus élégant, parce qu'elles ont accès à la distribution entière et non seulement à son mode : on peut **mesurer** le degré de hasard de la politique, et le faire figurer dans l'objectif. Cette mesure est l'**entropie**, et la technique est la **prime d'entropie** (*entropy bonus*) de la section 8.9.

$$
H(\pi) = -\sum_a \pi(a\mid s)\log\pi(a\mid s)
$$

Trois propriétés à retenir, et elles suffisent pour comprendre le signe du terme en section 8.9. L'entropie est toujours strictement positive pour une distribution non dégénérée. Elle est **maximale** pour la politique uniforme, celle qui n'a aucune préférence. Et elle tend vers **zéro** quand une action concentre toute la probabilité, c'est-à-dire quand la politique devient déterministe. Une entropie qui s'effondre tôt dans l'entraînement est donc le signal exact du problème que nous décrivons.

{{% comment %}}SOURCE: LAPAN ch.11 p.343{{% /comment %}}

---

## Problème 4 : les échantillons sont corrélés

Le dernier problème est celui que vous connaissez le mieux, parce que nous l'avons déjà résolu une fois, en semaine 5, et que la solution de la semaine 5 est cette fois **interdite**.

La descente de gradient stochastique suppose que les échantillons d'un lot sont indépendants et identiquement distribués. Or les transitions issues d'un même épisode ne le sont évidemment pas : elles se suivent, elles décrivent la même situation à quelques images d'intervalle, et elles partagent le même retour final. Un lot constitué d'un épisode contient donc une seule information répétée des centaines de fois. La conséquence est, une fois de plus, une **variance de gradient très élevée** : les exemples du lot poussent tous dans la même direction, et cette direction peut être globalement mauvaise si l'épisode était chanceux ou malchanceux.

{{% comment %}}SOURCE: LAPAN ch.11 p.343{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.12 p.373{{% /comment %}}

En semaine 5, nous avions réglé exactement ce problème avec un grand tampon de rejeu : en tirant au hasard dans un million de transitions provenant de milliers d'épisodes différents, on obtient un lot décorrélé. Cette solution n'est pas disponible ici. Les méthodes de gradient de politique sont **sur politique**, et s'entraîner sur d'anciennes transitions revient à calculer le gradient d'une **autre** politique que celle que l'on veut améliorer.

> [!WARNING]
 **La solution évidente est la mauvaise, et elle est tentante.** On se dit : gardons un tampon de rejeu, mais tout petit, de quelques milliers de transitions seulement, pour que son contenu reste proche de la politique courante. C'est faux dans les deux sens. Un tampon assez petit pour rester sur politique est trop petit pour décorréler, puisqu'il contient encore essentiellement les derniers épisodes. Et un tampon assez grand pour décorréler n'est plus sur politique. Il n'y a pas de réglage intermédiaire qui sauve l'affaire : le tampon de rejeu est le mauvais outil pour ce problème, et il faut en changer.

{{% comment %}}SOURCE: LAPAN ch.11 p.343-344{{% /comment %}}

La bonne réponse consiste à faire jouer **plusieurs environnements à la fois**, tous avec la politique courante. Le lot est alors constitué de transitions provenant de parties différentes, à des moments différents, ce qui casse la corrélation intra-épisode, et toutes ces transitions sont produites par la politique courante, ce qui préserve la contrainte sur politique. C'est la seule des quatre réponses de la semaine qui soit purement architecturale, et c'est aussi celle qui change le plus la forme du code. Les sections 8.9 et 8.10 lui sont consacrées.

{{% comment %}}SOURCE: LAPAN ch.12 p.373{{% /comment %}}

---
