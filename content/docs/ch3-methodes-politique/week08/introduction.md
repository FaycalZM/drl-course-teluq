---
title: "Introduction"
weight: 1
---

## Sept semaines à apprendre un nombre, et une semaine pour apprendre la décision

Bonjour à toutes et à tous ! Le module 3 commence, et il commence par un changement d'objet. Je veux que vous mesuriez tout de suite l'ampleur de ce changement, parce que tout le reste de la semaine en découle.

Depuis la semaine 4, toutes nos méthodes ont fait la même chose. Elles ont appris un **nombre**, la valeur d'un état \(v_\pi(s)\) ou la valeur d'un couple état-action \(q_\pi(s,a)\), et elles en ont **déduit** un comportement. L'itération de valeur apprenait \(V\), puis la politique en tombait par \(\argmax_a\). Le Q-learning tabulaire apprenait une table, puis la politique en tombait par \(\argmax_a\). Le réseau Q profond a remplacé la table par un réseau, et la politique en tombait encore par \(\argmax_a\). Les cinq réparations de la semaine 6 ont amélioré la qualité de ce nombre, et la semaine 7 a rendu son calcul moins coûteux. Pendant sept semaines, la valeur a été le sujet et la politique a été une conséquence.

{{% comment %}}SOURCE: LAPAN ch.11 p.330-331{{% /comment %}}

Or regardez ce que nous voulons réellement. Un agent qui aperçoit un tigre dans les buissons a besoin d'une **décision**, pas d'une estimation précise de l'écart de valeur entre « courir » et « ne rien faire ». Peu lui importe que fuir vaille 12,7 et rester 3,2 : ce qui lui est utile, c'est de courir. La route par la valeur répond à la question de la politique de façon **indirecte**, et cette semaine nous allons y répondre directement.

{{% comment %}}SOURCE: LAPAN ch.11 p.331{{% /comment %}}

Le détour n'est pas seulement inélégant, il est parfois impraticable. Choisir une action par \(\argmax_a Q(s,a)\) suppose de savoir parcourir l'ensemble des actions à **chaque pas de temps**. Avec quatre actions de manette, c'est gratuit. Avec mille actions, cela commence à coûter. Et quand l'action est un couple de forces à appliquer à deux articulations, l'ensemble des actions n'est plus énumérable : l'\(\argmax\) devient un petit problème d'optimisation à résoudre à l'intérieur d'un réseau fortement non linéaire, à chaque pas, dans la boucle d'entraînement comme dans la boucle de jeu. C'est très exactement le mur sur lequel le module 2 s'est terminé. Une méthode qui n'a jamais besoin de la valeur n'a jamais besoin de cet \(\argmax\).

{{% comment %}}SOURCE: LAPAN ch.11 p.331{{% /comment %}}

Il y a un troisième argument, et il est plus subtil que les deux premiers. Une politique paramétrée produit une **distribution de probabilité** sur les actions, et une distribution convient mieux qu'une moyenne à un environnement stochastique. C'est le même esprit que l'ouverture distributionnelle de la semaine 6 : au lieu de résumer l'incertitude par un nombre, on la garde entière.

{{% comment %}}SOURCE: LAPAN ch.11 p.332{{% /comment %}}

Et une filiation, parce qu'elle va vous rassurer : vous avez déjà écrit une méthode de gradient de politique. La **méthode d'entropie croisée** de la semaine 3 en est une. Elle augmente la probabilité des actions issues des épisodes élites et ignore les autres, ce qui revient exactement à pondérer chaque transition par 1 si elle vient d'un épisode élite et par 0 sinon. REINFORCE, que nous écrirons en section 8.3, est cette même méthode avec un **vrai scalaire** à la place du 0/1. Vous n'abordez donc pas une famille inconnue : vous abordez la version bien faite de quelque chose que vous avez déjà fait fonctionner.

{{% comment %}}SOURCE: LAPAN ch.11 p.333-334{{% /comment %}}

Voici la colonne vertébrale de la semaine, en une phrase par étape, pour que vous sachiez à tout moment où vous êtes. Le **théorème du gradient de politique** (*policy gradient theorem*) établit que le gradient de la performance est calculable sans jamais dériver l'environnement, ce qui rend la chose légitime. **REINFORCE** est ce théorème transformé en algorithme, et il fonctionne. Puis **quatre choses se gâtent, et chacune a un nom**. Une **référence** répond à la deuxième. Un **critique** répond aux trois autres, et l'ensemble s'appelle **A2C**. Enfin, plusieurs environnements menés en parallèle rendent le tout utilisable. Cinq étapes, dans cet ordre, et la section 8.5 est le point de bascule.

Un dernier mot, et c'est une promesse de franchise. Cette semaine n'est pas une semaine de progrès net. Les méthodes de gradient de politique achètent deux choses précieuses, une politique authentiquement stochastique et la porte des actions continues, et elles les paient en **échantillons**. Je vous donnerai le chiffre en section 8.9, et je ne le maquillerai pas. Il n'y aura pas de classement à la fin de cette semaine, il y aura un arbitrage, et c'est l'arbitrage que la semaine 9 vous demandera d'avoir compris.

> [!IMPORTANT]
 **Le mot « référence » prend cette semaine son second sens, celui que j'ai séparé du premier en semaine 7.** Une **référence** (*baseline*) est désormais une quantité soustraite d'un retour pour réduire la variance d'un gradient : c'est un objet mathématique, et c'est le sujet de la section 8.6. Ce n'est pas la « version de référence » de la semaine 7, qui désignait la configuration non modifiée d'un banc d'essai, un objet de protocole expérimental. Dans cette semaine, j'écris « référence » tout court, et jamais « version de référence ».

{{% comment %}}SOURCE: source-assets/glossaire.md{{% /comment %}}

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Dire ce qu'une méthode fondée sur la politique (*policy-based*) apprend, ce qu'elle n'apprend pas, et nommer les trois situations où apprendre une valeur est un détour coûteux.
- Écrire la paramétrisation softmax d'une politique discrète à partir de préférences numériques, et dire pourquoi le réseau sort des **sorties brutes** (*logits*) et jamais des probabilités.
- Énoncer cinq avantages d'une politique paramétrée sur une politique \(\varepsilon\)-gloutonne, et expliquer celui qu'aucune méthode fondée sur la valeur ne peut obtenir : un optimum authentiquement stochastique.
- Calculer, sur l'exemple du couloir court, les valeurs atteintes par la meilleure politique déterministe et par la meilleure politique stochastique, et dire ce que l'écart démontre.
- Énoncer le **théorème du gradient de politique**, et dire précisément quelle quantité il ne contient pas, et pourquoi c'est tout son intérêt.
- Passer du théorème à sa forme échantillonnée en nommant les deux substitutions employées, et montrer qu'elles sont de la même nature.
- Expliquer pourquoi le théorème s'écrit avec un \(\propto\) et non un \(=\), et où passe la constante omise.
- Écrire la mise à jour de REINFORCE sous ses deux formes équivalentes, et dire pourquoi le gradient y est divisé par la probabilité de l'action.
- Expliquer pourquoi la quantité minimisée dans le code n'est pas une erreur, pourquoi sa valeur ne renseigne sur rien, et quelle autre quantité de la même perte est, elle, une véritable erreur.
- Nommer les trois objets des semaines 5 et 6 dont REINFORCE n'a aucun besoin, et dire pour chacun pourquoi.
- Nommer les quatre problèmes de REINFORCE, dans l'ordre, et associer à chacun la section qui y répond.
- Démontrer en trois égalités que soustraire une fonction de l'état seul laisse l'espérance du gradient inchangée.
- Expliquer, sur un exemple à trois actions, pourquoi un décalage constant des récompenses change le comportement d'une mise à jour sans changer les récompenses relatives.
- Dire quel ordre de grandeur sépare la variance du gradient avec et sans référence, et comment on mesure cette variance dans un carnet.
- Justifier que \(\hat v(s,\mathbf{w})\) est la référence naturelle, et écrire l'identité qui transforme l'échelle du gradient en **avantage**.
- Énoncer la frontière exacte entre une référence et un critique, et nommer l'opération qui la franchit.
- Écrire la chaîne de trois égalités qui réduit le pas acteur-critique à un pas à l'erreur de différence temporelle de la semaine 4.
- Distinguer les paramètres de l'acteur \(\theta\) des poids du critique \(\mathbf{w}\), y compris lorsqu'un tronc commun les fait se recouvrir physiquement.
- Écrire les trois termes de la perte d'A2C avec leurs signes, et dire ce que chacun pousse dans quel sens.
- Expliquer pourquoi l'appel à `detach()` sur la sortie du critique est une question de correction et non d'efficacité.
- Dire ce que le déroulement sur \(N\) pas achète, et pourquoi \(N\) peut descendre de dix à quatre dès qu'un critique existe.
- Écrire l'entropie d'une politique, dire sa valeur maximale pour deux actions, et expliquer le signe du terme d'entropie dans une perte minimisée.
- Chiffrer le coût en échantillons d'une méthode de gradient de politique face à un réseau Q profond, et énoncer la règle de choix entre les deux familles sans les classer.
- Distinguer environnements **vectorisés** et processus parallèles, et dire ce que chacun décorrèle réellement.
- Comparer le parallélisme de données et le parallélisme de gradients, et dire lequel survit sur une seule machine et pourquoi.

---

## Prérequis et outils

De la semaine 7 : les **environnements vectorisés** (*vectorized environments*), que nous retrouvons cette semaine comme réponse à un problème théorique et non comme optimisation, et le protocole de mesure à graines multiples, qui gouverne le volet A du laboratoire. De la semaine 6 : l'identité \(Q = V + A\) de l'architecture duale, qui est le pivot de la section 8.7, et la notion d'**efficacité d'échantillon** (*sample efficiency*), qui revient cette semaine avec une facture. De la semaine 5 : la **méthode semi-gradient** et l'erreur quadratique sur une cible amorcée, qui est exactement la façon dont le critique sera entraîné, et le détachement du graphe de calcul. De la semaine 4 : l'erreur de différence temporelle \(\delta_t\) et l'**amorçage** (*bootstrapping*), le mot qui séparera une référence d'un critique. De la semaine 3 : la méthode d'entropie croisée, les sorties brutes et l'**échantillonnage de l'action**. De la semaine 2 : le graphe de calcul de PyTorch et la rétropropagation, dont la section 8.8 fait un usage où une seule ligne manquante casse la correction.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les deux volets du laboratoire ; le volet A tient en quelques minutes sur processeur central, le volet B en quelques dizaines de minutes |
| **Gymnasium** | `CartPole-v1` pour les deux volets, et `gym.vector.SyncVectorEnv` pour les environnements vectorisés du volet B |
| **PyTorch** | `F.log_softmax`, l'échantillonnage d'une loi catégorielle, `detach()`, `clip_grad_norm_`, et le paramètre `eps` d'Adam, qui n'est pas un détail |
| **NumPy** | l'accumulation à rebours des retours, et le calcul de la variance des gradients |
| **Matplotlib** | la courbe de variance avec et sans référence, qui est la seule mesure que cette semaine produit elle-même |
| **TensorBoard** | les dix quantités à journaliser du volet B, qui forment aussi la liste de diagnostic de la semaine |
| **Page « Notation » du cours** | \(\theta\) et \(\mathbf{w}\) apparaissent pour la première fois sur la même page, et la page de notation les sépare depuis le début |
| **Page « Glossaire » du cours** | une quinzaine de termes nouveaux y entrent, dont acteur, critique, prime d'entropie et tronc commun |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

---
