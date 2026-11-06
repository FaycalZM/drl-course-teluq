---
title: "8.9 Réponses aux problèmes 1, 3 et 4, puis le prix"
weight: 10
---

## Problème 1, réglé : le critique paie la queue de la trajectoire

Reprenons le tableau de la section 8.5 et cochons la première ligne, parce qu'elle est déjà réglée et que vous l'avez peut-être laissée passer.

Le problème était qu'il fallait attendre la fin d'un épisode pour connaître \(G_t\). Avec un critique, on n'attend plus : on joue \(N\) pas, on additionne les \(N\) récompenses réellement reçues, et on demande au critique ce que vaut la suite. Le retour complet a été remplacé par \(G^{(N)}_t\), et la mise à jour peut avoir lieu toutes les \(N\) interactions au lieu d'une fois par épisode. Sur un jeu dont un épisode dure mille trames, le passage est de une mise à jour par mille pas à une mise à jour tous les quatre pas.

C'est la combinaison des deux réponses envisagées en section 8.5, et non l'une ou l'autre : on **déroule** l'équation de Bellman sur \(N\) pas, **et** on confie le reste à un \(\hat v\) appris. La troncature n'est plus une approximation qu'on accepte, c'est une frontière où une estimation prend le relais.

> [!NOTE]
 **Et l'honnêteté sur ce que ce réglage coûte.** La valeur estimée \(\hat v(s_{t+N},\mathbf{w})\) est fausse au début de l'entraînement, parce que le critique n'a encore rien appris. Les premières mises à jour de l'acteur sont donc pondérées par des avantages calculés à partir de prédictions arbitraires. L'entraînement commence ainsi par une phase où les deux réseaux s'améliorent mutuellement à partir de rien, et c'est précisément pourquoi un A2C est plus sensible au pas d'apprentissage qu'un REINFORCE : il n'y a plus de quantité mesurée pour ancrer les premiers pas. Si votre courbe de récompense reste plate pendant longtemps puis décolle brusquement, c'est le plus souvent cela que vous observez, et non un bogue.

---

## Problème 3, réglé : la prime d'entropie

Le terme a déjà été écrit en section 8.8, et son signe a été établi. Il reste à dire comment on le surveille, et à être franche sur ce qu'on ne sait pas régler.

**Ce qu'il faut regarder.** L'entropie de la politique est une quantité à journaliser à chaque mise à jour, et sa courbe est l'un des meilleurs diagnostics de la semaine. Sur `CartPole-v1`, qui a deux actions, l'entropie maximale vaut

$$
H_{\max} = -\left(\tfrac{1}{2}\log\tfrac{1}{2} + \tfrac{1}{2}\log\tfrac{1}{2}\right) = \log 2 \approx 0{,}69
$$

et c'est bien la valeur qu'affiche un réseau fraîchement initialisé, puisque ses sorties sont presque égales. Au cours d'un entraînement qui se passe bien, cette entropie **descend**, par exemple de \(0{,}69\) à environ \(0{,}52\) : la politique quitte l'uniformité et se forme une opinion. Ce qu'il ne faut pas voir, c'est une entropie qui s'effondre vers zéro en quelques centaines de pas, ce qui signifie que la politique s'est verrouillée avant d'avoir rien exploré, ni une entropie qui reste collée à son maximum, ce qui signifie que le terme d'entropie écrase les deux autres et que l'agent n'apprend rien.

{{% comment %}}SOURCE: LAPAN ch.11 p.348{{% /comment %}}

**Ce qu'on ne sait pas régler, et je ne vais pas l'inventer.** Il n'existe, dans aucun des outils de ce cours, de règle principielle pour choisir le coefficient \(\beta\). La valeur \(0{,}01\) est un point de départ qui fonctionne sur les problèmes de cette semaine. Le seul conseil opérationnel disponible est comparatif, et il est utile : **vérifiez l'ordre de grandeur relatif du terme d'entropie et du terme de politique**, et assurez-vous que le premier ne domine pas le second. C'est précisément pour cela que le code de la section 8.8 renvoie les trois termes séparément. Quant au calendrier de \(\beta\), l'usage est de le garder constant, ou de le faire décroître linéairement au cours de l'entraînement, de façon à explorer tôt et exploiter tard. Je vous donne ces deux pratiques comme des pratiques, pas comme des théorèmes : si quelqu'un vous présente une formule pour \(\beta\), demandez-lui d'où elle sort.

{{% comment %}}SOURCE: LAPAN ch.11 p.349{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.12 p.361{{% /comment %}}

Une nuance de vocabulaire, enfin, pour que vos lectures ne vous troublent pas. Le terme ajouté à la perte s'écrit \(\mathcal{L}_H = -\beta\,H(\pi)\) et il n'est pas l'entropie : il est son opposé, mis à l'échelle. L'entropie \(H(\pi)\) est ce que l'on **trace** et que l'on veut haut ; \(\mathcal{L}_H\) est ce que l'on **minimise**. Les deux portent la même lettre dans leur nom et vont dans des sens opposés, alors nommez-les distinctement dans votre code, comme le fait le fragment de la section 8.8 avec `perte_entropie_t` d'un côté et l'entropie journalisée de l'autre.

---

## Problème 4, réglé : plusieurs environnements, et ce qu'ils sont vraiment

Le quatrième problème était la corrélation des échantillons, et la réponse est de faire jouer plusieurs environnements à la fois. La **Figure 8-5** montre le dispositif : un seul agent, un seul réseau, et plusieurs environnements qui lui fournissent chacun un flux de transitions, le tout alimentant une unique boucle d'entraînement.

{{< bookfig src="08-05.png" week="08" >}}

{{% comment %}}SOURCE: LAPAN ch.12 p.373-374{{% /comment %}}

Maintenant, ce que ces environnements sont **réellement**, parce que c'est une source de malentendu constante et que le laboratoire de cette semaine en dépend.

Quand on passe un tableau de \(k\) environnements à une source d'expérience, celle-ci passe en mode **tourniquet** : chaque demande de transition s'adresse à l'environnement suivant du tableau, chacun conservant son propre état entre deux visites. Le flux de transitions qui arrive dans le lot provient donc alternativement de \(k\) parties différentes, à des moments différents de leur déroulement. C'est **équivalent** à une communication parallèle avec les environnements du point de vue du contenu du lot, avec une seule différence : la communication n'est pas parallèle au sens strict, elle est **séquentielle**. Un seul processus, un seul fil d'exécution, \(k\) environnements interrogés à tour de rôle.

{{% comment %}}SOURCE: LAPAN ch.12 p.374{{% /comment %}}

> [!IMPORTANT]
 **Environnements vectorisés et processus parallèles ne sont pas la même chose, et seule la première des deux propriétés nous intéresse ici.** La **décorrélation** des échantillons est obtenue par le tourniquet, c'est-à-dire par le simple fait de mélanger les sources : elle ne demande aucun processus supplémentaire et aucune mémoire partagée. L'**accélération**, elle, demande de vrais processus, parce que c'est elle qui recouvre le temps d'attente de l'environnement avec le temps de calcul du réseau. Le laboratoire de cette semaine s'intéresse à la première et laisse la seconde de côté, ce qui est aussi un choix de faisabilité : les processus multiples sont limités dans un carnet partagé. Autrement dit, la réponse au problème 4 est acquise **sans** parallélisme réel, et la section 8.10 parle d'autre chose : de vitesse, pas de corrélation.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

Un bénéfice secondaire, et il n'est pas négligeable : avec \(k\) environnements, le réseau reçoit un lot de \(k\) observations à traiter en un seul passage avant, au lieu de \(k\) passages d'une observation. C'est l'argument d'inférence par lot de la semaine 7, et il s'applique tel quel.

---

## Le prix, en échantillons, et il faut le dire en entier

Nous avons quatre problèmes réglés et un algorithme qui fonctionne. Il reste à payer, et je veux que cette sous-section soit celle que vous reteniez de la semaine sur le plan du jugement professionnel.

**Combien de fois une méthode utilise-t-elle chaque transition ?** Posons la question à nos deux familles, et faisons le calcul.

Un réseau Q profond avec un tampon de rejeu d'un million de transitions, qui tire un lot de 32 pour chaque nouvelle trame collectée, utilise chaque transition environ **trente-deux fois** avant qu'elle ne soit évincée du tampon. Avec un tampon priorisé, les transitions les plus informatives sont tirées davantage, et le compte monte. Une méthode de gradient de politique utilise chaque transition **une seule fois**, parce qu'elle ne peut pas faire autrement : la contrainte sur politique l'interdit. L'écart d'efficacité d'échantillon entre les deux familles peut donc atteindre **un ordre de grandeur**.

{{% comment %}}SOURCE: LAPAN ch.12 p.373-374{{% /comment %}}

Voilà le passif. Maintenant l'actif, et il faut le donner avec la même précision, sans quoi la comparaison devient un slogan.

**Premier contrepoids, le chiffre réel.** Sur le même jeu Atari, A2C a convergé en **huit millions** de trames, contre environ **un million** pour un réseau Q profond de base. Huit fois plus, donc, et non cent fois plus. L'écart théorique d'un ordre de grandeur se retrouve bien dans la mesure, mais il ne s'aggrave pas : les méthodes de gradient de politique ne sont pas inutilisables, elles sont **différentes**.

{{% comment %}}SOURCE: LAPAN ch.12 p.374{{% /comment %}}

**Deuxième contrepoids, celui que la section 8.4 avait déjà installé.** L'efficacité d'échantillon n'est pas l'efficacité de calcul. A2C touche le réseau **une fois** par échantillon d'entraînement ; un réseau Q profond le touche **deux** fois, puisqu'il lui faut l'état courant et l'état suivant pour former la cible de Bellman. Et les huit millions de trames d'A2C sont collectées par cinquante environnements en parallèle, ce qui change radicalement le temps d'horloge que ce nombre représente.

{{% comment %}}SOURCE: LAPAN ch.11 p.341{{% /comment %}}

**La règle de choix, et je la donne comme une règle de décision, pas comme un classement.** Elle tient à une seule question : **votre environnement est-il bon marché ?** Si l'environnement est rapide, léger en mémoire et parallélisable, par exemple un jeu simple ou une simulation vectorisable, alors les échantillons ne coûtent presque rien et une méthode de gradient de politique peut être le meilleur choix, parce qu'elle convertit ces échantillons bon marché en progrès stable. Si l'environnement est cher, par exemple un simulateur physique lent, un système réel, ou une interaction qui engage un utilisateur, alors chaque transition est précieuse et une méthode hors politique capable de la rejouer trente fois est le choix intelligent.

{{% comment %}}SOURCE: LAPAN ch.12 p.374{{% /comment %}}

> [!WARNING]
 **Ne quittez pas cette semaine avec un classement, quittez-la avec un arbitrage.** Les méthodes de gradient de politique n'améliorent pas les méthodes fondées sur la valeur, et ne les remplacent pas. Elles achètent **deux** choses, et il est important de savoir que la liste s'arrête là. D'abord une politique authentiquement **stochastique**, utilisable là où l'optimum lui-même est stochastique, comme le couloir court de la section 8.1 ou un jeu à information imparfaite. Ensuite la porte des **actions continues**, puisque rien dans cette semaine n'a jamais eu besoin d'énumérer les actions. Elles paient ces deux choses en échantillons, et le prix est d'un facteur de l'ordre de dix. La semaine 9 vous demandera de tenir cet arbitrage en tête, parce qu'elle ouvrira la seconde de ces deux portes.

---
