---
title: "12.9 Plusieurs agents : quand le sol se met à bouger"
weight: 10
---

## La condition exacte qui fait basculer le problème

Changeons de sujet, et commençons par la distinction qui décide de tout. Elle est simple à énoncer et facile à manquer.

Mettez d'autres agents dans le monde de votre agent. Tant que ces autres agents sont **hors de votre contrôle et ne changent pas de comportement**, vous les absorbez dans l'environnement et vous n'avez **rien** à modifier : leur présence fait partie de la dynamique, votre agent apprend à y réagir, et vous faites de l'apprentissage par renforcement à un seul agent comme depuis onze semaines. Un adversaire scripté, un trafic simulé, une foule qui suit des règles fixes : tout cela est de l'environnement.

{{% comment %}}SOURCE: LAPAN ch.22 p.675{{% /comment %}}

L'auto-jeu des sections 12.3 à 12.5 est exactement ce cas, et c'est important de le voir. Pendant une partie d'auto-jeu, l'adversaire est un réseau **figé** : le meilleur réseau actuel, dont les poids ne bougent pas pendant toute la collecte. Il est donc, du point de vue de l'apprenti, une partie parfaitement stationnaire de l'environnement. Ce qui bouge, c'est la succession des phases : à chaque promotion, l'environnement change **d'un coup**, puis redevient fixe. C'est inconfortable, et nous avons vu en section 12.5 ce que cela fait à la courbe de perte, mais cela reste un problème à un seul agent.

L'**apprentissage par renforcement multi-agent** (*multi-agent reinforcement learning*, désormais MARL) commence là où cette absorption cesse d'être adéquate, c'est-à-dire précisément dès que **les autres agents apprennent aussi, en même temps que le vôtre**. Alors leur politique change à chaque instant, donc la dynamique que votre agent observe change à chaque instant, donc la cible de votre agent se déplace toute seule. Et ce déplacement n'est pas du bruit : c'est une dérive dirigée, puisque l'autre agent optimise, et il optimise souvent contre vous.

Les situations concrètes ne manquent pas. Un jeu de plateau à deux joueurs qui s'améliorent tous les deux. Une **simulation de marché**, où le prix que vous posez provoque la réaction des autres participants, qui change le prix que vous devriez poser. Les unités d'un jeu de stratégie en temps réel, qui coopèrent entre elles et s'affrontent par groupes. Et des applications réelles qui n'ont rien de ludique : les enchères, l'allocation de bande passante dans un réseau, les objets connectés qui se partagent un canal.

{{% comment %}}SOURCE: LAPAN ch.22 p.674-675{{% /comment %}}

---

## Compétitif, collaboratif, et les mélanges qui sont les cas intéressants

Deux régimes se distinguent, et je les donne surtout pour pouvoir dire aussitôt qu'ils sont rarement purs.

Un cadre est **compétitif** (*competitive*) quand un agent maximise son objectif en battant les autres : ce que l'un gagne, un autre le perd. Il est **collaboratif** (*collaborative*) quand plusieurs agents poursuivent un objectif commun et doivent accorder leurs actions pour l'atteindre. Les cas réellement intéressants sont des **mélanges** des deux : une équipe coopère à l'intérieur et affronte l'équipe adverse à l'extérieur, et c'est le cas des deux expériences des sections 12.10 et 12.11.

{{% comment %}}SOURCE: LAPAN ch.22 p.675{{% /comment %}}

Un mot sur ce que plusieurs agents simples peuvent produire, parce que c'est spectaculaire et que je veux poser le plafond avant de montrer le plancher. Dans un environnement de cache-cache devenu célèbre, des agents ont fini par construire une barrière avec les objets du décor pour s'enfermer à l'abri, puis l'équipe adverse a appris à se servir d'un trampoline pour passer par-dessus. C'est un **comportement émergent** (*emergent behaviour*) : rien dans la récompense ne décrivait une barrière ni un trampoline. Retenez cet exemple comme une borne supérieure de ce qu'on sait obtenir, et sachez que **ce n'est pas ce que cette semaine va vous montrer** : ce que vous verrez ici est beaucoup plus modeste, et une partie du travail de la section 12.11 consiste justement à ne pas confondre les deux.

{{% comment %}}SOURCE: LAPAN ch.22 p.675{{% /comment %}}

---

## Ce que cette semaine ne vous enseignera pas, et je préfère le nommer

Il existe une discipline entière consacrée à ce qui se passe quand plusieurs décideurs optimisent en même temps, avec ses équilibres, ses stratégies mixtes et ses théorèmes : la théorie des jeux. Minimax, que la section 12.2 a nommé, en est l'un des tout premiers résultats.

**Cette semaine ne l'enseigne pas**, et ce n'est pas un oubli : c'est un choix que je prends à mon compte, comme la semaine 11 l'avait fait pour les bornes de confiance. Je ne peux pas vous en donner, dans l'espace disponible, un exposé qui tienne la rigueur que les autres sections ont reçue, et je ne vais pas vous en servir une version diluée qui vous laisserait croire que vous la maîtrisez. Ce que je vous donne à la place est entièrement vérifiable : une notation, une expérience mesurée, et un phénomène nommé correctement.

{{% comment %}}SOURCE: LAPAN ch.22 p.675-676{{% /comment %}}

---

## La notation que ce cours doit inventer

**L'intuition.** Nous avons besoin d'écrire des choses comme « l'observation de l'agent numéro 3 au pas 12 » et « ce que tous les agents font ensemble à cet instant ». Aucune notation standard n'existe pour cela : le domaine traite habituellement ces objets par des dictionnaires indexés par un nom d'agent, et la notation de référence de ce cours, conçue pour un agent unique, ne couvre pas le cas. Ce cours écrit donc la sienne, et je la définis devant vous.

**L'équation.** Six symboles, et une seule subtilité :

$$
i \in \{1, \dots, n_t\}, \qquad O^i_t,\; A^i_t,\; R^i_t, \qquad \mathbf{A}_t = (A^1_t, \dots, A^{n_t}_t), \qquad \pi_\theta(a \mid o^i)
$$

{{% comment %}}SOURCE: LAPAN ch.22 résumé{{% /comment %}}
{{% comment %}}SOURCE: source-assets/notation.md{{% /comment %}}

- \(i\) est l'**indice d'agent**. Il remplace une clé de dictionnaire, rien de plus.
- \(O^i_t\), \(A^i_t\) et \(R^i_t\) sont l'**observation**, l'**action** et la **récompense** de l'agent \(i\) au pas \(t\). L'exposant est l'agent, l'indice est le temps : c'est la seule convention à retenir, et elle est tenue partout dans cette page.
- \(\mathbf{A}_t\) est l'**action jointe** (*joint action*), c'est-à-dire le \(n_t\)-uplet de toutes les actions du pas \(t\). C'est elle que l'environnement reçoit, et non une action individuelle : c'est le point où la définition de la semaine 1 se fissure, car un processus de décision markovien reçoit **une** action.
- \(\pi_\theta(a \mid o^i)\) est une **politique partagée** (*shared policy*) : **un seul** jeu de poids \(\theta\), appliqué successivement à l'observation de chaque agent du groupe. Quarante tigres, un réseau.

Et la subtilité, qui n'est pas cosmétique : **\(n_t\) porte un indice de temps**. Le nombre d'agents n'est pas une constante du problème, il **diminue en cours d'épisode** quand un agent meurt, alors que l'épisode continue sans lui. Écrire \(n\) au lieu de \(n_t\) décrirait un autre problème que celui que nous étudions, et le code de la section 12.10 vous montrera que cette variation est la première chose qui casse une boucle d'entraînement ordinaire.

> [!NOTE]
 **Une politique partagée est une simplification, et il faut savoir ce qu'elle coûte.** Si tous les agents d'un groupe partagent leurs poids, ils ne peuvent pas se spécialiser : il n'y aura pas un tigre rabatteur et un tigre embusqué, parce que les deux sont littéralement le même réseau. En échange, on entraîne un réseau au lieu de quarante, les données des quarante agents alimentent un seul apprentissage, et **la méthode d'apprentissage ne change pas d'une ligne**. C'est l'hypothèse qui rend la suite de cette semaine réalisable, et elle vaut la peine d'être énoncée comme une hypothèse plutôt que subie comme un détail.

{{% comment %}}SOURCE: LAPAN ch.22 p.674{{% /comment %}}

---

## Et la méthode d'apprentissage ? Celle de la semaine 5, sans y changer une ligne

C'est le moment de la révélation la plus désarmante de la semaine, et je préfère qu'elle vienne de moi plutôt que de votre déception en arrivant au code.

**Il n'y a pas d'algorithme multi-agent dans cette semaine.** La méthode employée dans les sections 12.10 et 12.11 est le réseau de valeurs d'action de la semaine 5, avec son tampon de rejeu, son réseau cible et sa politique \(\varepsilon\)-gloutonne. La cible est celle de la semaine 5 :

$$
Y_t \;=\; R^i_{t+1} + \gamma \max_{a'} Q_{\theta^-}\!\left(O^i_{t+1}, a'\right)
$$

{{% comment %}}SOURCE: source-assets/raw-content/week-05.md{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.674{{% /comment %}}

appliquée à chaque agent séparément, avec sa propre observation, sa propre action et sa propre récompense, et la perte est la même erreur quadratique. Je ne la redérive pas : la semaine 5 l'a fait, et la relire est l'affaire de cinq minutes.

Ce qui devient multi-agent, c'est l'**environnement**, et lui seul : la façon de lui parler, la façon de ranger ce qu'il renvoie, et la façon de construire l'observation d'un agent. C'est simultanément la leçon de ces deux sections et leur plafond, et je vous demande de tenir les deux. La leçon : un problème multi-agent peut souvent être ramené à un problème d'ingénierie d'environnement, et c'est une très bonne nouvelle quand on veut commencer. Le plafond : rien de ce que vous verrez ici ne fait coopérer des agents **par construction**, et nous verrons en section 12.11 ce que cela implique sur la lecture des résultats.

---
