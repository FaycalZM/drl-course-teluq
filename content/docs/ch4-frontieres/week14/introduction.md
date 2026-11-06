---
title: "Introduction"
weight: 1
---

## Treize semaines à maximiser un nombre que personne n'a choisi

Bonjour à toutes et à tous ! Je veux ouvrir cette dernière semaine de contenu par une question, et je vais la poser brutalement parce qu'elle mérite de l'être : **d'où vient la récompense ?**

Faites l'inventaire avec moi. La semaine 4 s'en est servie pour approcher une valeur d'action. La semaine 5 l'a écrêtée, mise dans un tampon et poussée à travers une cible de différence temporelle. La semaine 8 l'a transformée en avantage pour pondérer un gradient de politique. La semaine 10 a borné le pas de la mise à jour qui la maximise. La semaine 11 lui a ajouté une prime de nouveauté. La semaine 3 ne s'en servait que pour trier des candidats et garder les meilleurs. Six familles de méthodes, treize semaines de travail, et **la même hypothèse jamais discutée** : il existe un nombre, l'environnement le fournit, et ce nombre dit ce que nous voulons.

Dans presque tous les environnements que ce cours a touchés, ce nombre était en effet donné d'avance : le score d'un jeu vidéo, la case d'arrivée d'un monde en grille, la distance parcourue par un corps simulé. La seule exception fut l'environnement de courtage de la semaine 7, dont la récompense a été écrite à la main, et encore : le choix était assez évident pour que personne n'ait eu à en débattre.

{{% comment %}}SOURCE: LAPAN ch.19 p.573{{% /comment %}}

Cette semaine retire l'hypothèse. Elle part d'un constat que je vous demande de prendre au sérieux : **disposer d'un unique nombre à maximiser est l'exception, pas la norme.**

---

## Deux choses qu'on ne sait pas écrire, et un sous-marin

Deux exemples suffisent à ouvrir la brèche, et ils ne viennent pas de la théorie.

Prenez un agent conversationnel. Vous voulez des réponses correctes, et vous voulez des réponses polies. Écrivez maintenant le nombre qui arbitre entre une réponse juste et désagréable et une réponse aimable et fausse. Quel coefficient ? Quelle unité commune à la justesse et à la courtoisie ? Vous ne l'écrirez pas, et personne ne l'a écrit.

Prenez un transporteur routier dont la récompense est le profit. Il n'est pas difficile de prédire ce qu'un optimiseur compétent fera de cette spécification : il passera par le terrain du voisin, parce que c'est le chemin le plus court. Rien dans l'objectif n'interdit ce passage, et c'est précisément le problème. L'objectif n'est pas faux, il est **incomplet**, et un optimiseur ne distingue pas les deux.

{{% comment %}}SOURCE: LAPAN ch.19 p.573-574{{% /comment %}}

Et puis il y a le cas que toute la première moitié de la semaine va suivre, parce qu'il a l'avantage d'être petit, mesuré et honnêtement raconté : un sous-marin, dans un jeu d'arcade, noté sur trois activités à la fois.

---

## Deux réponses, et elles ne sont pas des alternatives

Face à cette question, cette semaine donne deux réponses. Elles ne sont pas en concurrence, elles se répondent, et c'est la raison pour laquelle elles tiennent dans la même semaine.

**La réponse constructive, et c'est la première moitié.** Si vous ne savez pas écrire la récompense, cessez d'essayer : **apprenez-la**. Montrez deux comportements à une personne, demandez-lui lequel est le meilleur, ajustez un réseau à ses réponses, et optimisez contre ce réseau. C'est l'apprentissage par renforcement à partir de **rétroaction humaine** (*human feedback*), c'est la famille de méthodes qui a rendu les grands modèles de langue utilisables, et ce cours va la suivre de bout en bout sur une chaîne complète, avec ses chiffres, son interface et ses échecs.

**La réponse critique, et c'est la seconde moitié.** L'écart entre ce que vous avez demandé et ce que vous vouliez dire n'est pas une fatalité vague : il a des **formes nommées**, il se **mesure**, et il **grandit sous la pression d'optimisation** au lieu de se diluer. Un agent plus capable obtient un meilleur score sur ce que vous avez écrit et un plus mauvais sur ce que vous vouliez. Et le passage de l'un à l'autre ressemble moins à une dérive qu'à une **bascule**.

> [!IMPORTANT]
 **Les deux moitiés de cette semaine se rejoignent, et c'est la chaîne de la première moitié qui les fait se rejoindre.** Je vous annonce la fin dès maintenant, parce que la lire sans l'avoir vue venir serait un gâchis. Nous allons construire un modèle de récompense à partir de jugements humains, nous allons l'améliorer en trois tours, nous allons mesurer un score multiplié par près de quatre, et au dernier tour **l'agent apprendra à jouer contre le modèle plutôt qu'à jouer au jeu**. Ce n'est pas une anecdote en marge de la chaîne. C'est la démonstration, faite par la chaîne elle-même, que la seconde moitié de la semaine parle de la première.

---

## Ce que vous allez lire

Voici la colonne vertébrale, une phrase par section.

La section 14.1 établit qu'une récompense est une **spécification** et non un fait, avec le sous-marin comme cas d'école. La section 14.2 remplace la spécification par une question posée à une personne, et donne l'unique morceau de mathématiques dont la première moitié a besoin. La section 14.3 explique pourquoi on compare deux comportements plutôt que d'annoter des actions, puis montre la boucle complète et la version simplifiée que nous suivrons. La section 14.4 mesure la chaîne : les heures, les gigaoctets, les segments, et le modèle de départ. La section 14.5 montre **où se tient l'humain**, et vous y trouverez le paragraphe qui est, littéralement, la fonction de récompense de toute l'expérience.

La section 14.6 est le cœur technique de la première moitié et la double lecture la plus intéressante du cours : l'équation du modèle de récompense, le code qui est censé l'implémenter, et **l'écart entre les deux**, que je vais enseigner au lieu de le taire. La section 14.7 branche le modèle appris à la place de la récompense réelle. La section 14.8 raconte les trois tours et la fin honnête.

La section 14.9 nomme ce que nous venons de voir : un **accident**, au sens étroit et utile du mot, et cinq catégories de problèmes dont deux survivent à un apprentissage parfait. La section 14.10 donne **six mécanismes** par lesquels un agent exploite une récompense mal spécifiée. La section 14.11 passe en revue les parades et dit pourquoi aucune ne ferme le problème.

La section 14.12 donne **trois types d'écart** entre un substitut et ce qu'on voulait, et ce n'est pas la même grille que les six mécanismes. La section 14.13 est le fait le plus dur de la semaine : l'écart grandit avec la pression d'optimisation, et la bascule est visible. La section 14.14 montre à quoi cela ressemble en comportement plutôt qu'en courbe. La section 14.15 met les deux grilles sur deux axes et y place notre sous-marin, ce qui est la seule façon de ne pas confondre trois et six. La section 14.16 pose la question qui reste : **qui définit l'objectif**, et à quel prix.

Puis viennent le laboratoire, le **jalon 4**, qui est le dernier et qui clôt le module 4, et le quiz.

---

## Les symboles de la semaine, et quatre renommages à accepter d'avance

Cette semaine fait entrer deux documents extérieurs dans un cours qui a déjà treize semaines de notation derrière lui, et quatre lettres entrent en collision. Deux de ces collisions tombent **à l'intérieur de l'équation centrale de la semaine**, ce qui ne laisse aucun choix : il faut trancher avant d'écrire, et non au milieu d'une démonstration. Les arbitrages ci-dessous sont inscrits dans la page « Notation » du cours.

**Première collision, et elle est fatale si on la laisse passer.** Les deux morceaux de comportement que l'on montre à une personne s'écrivent habituellement avec la lettre sigma. Or cette semaine écrit une **fonction logistique** et un **écart-type** dans la même équation que ces deux morceaux. Trois sens pour une lettre, à trois lignes d'intervalle : c'est intenable. Les deux segments s'écrivent donc \(\zeta^1\) et \(\zeta^2\) dans tout ce cours.

**Deuxième collision, au même endroit.** L'étiquette fournie par la personne s'écrit habituellement avec la lettre mu, qui porte déjà dans ce cours une distribution d'états, une moyenne gaussienne, la moyenne d'une méthode d'entropie croisée et une loi adverse depuis la semaine 13. L'étiquette s'écrit donc \(y_1, y_2\), ce qui a un avantage supplémentaire : l'équation de la section 14.2 **se lit alors pour ce qu'elle est**, une entropie croisée binaire, avec la lettre que ce cours emploie pour une cible depuis la semaine 2.

**Troisième collision, et elle est de pure forme.** La fonction logistique apparaît dans la section 14.6 avec son argument, à côté d'un écart-type qui apparaît sans le sien. Pour que l'œil ne s'y trompe pas, la logistique s'écrit \(\varsigma(\cdot)\) cette semaine.

**Quatrième collision.** La seconde moitié de la semaine manipule deux récompenses à la fois, et les mesures dont elle se sert réemploient quelques pages plus loin l'une des deux lettres pour une loi d'actions. Ce cours écrit donc \(P\) pour la **récompense de substitution** et \(T\) pour la **récompense réelle**, et ne touche plus à ces lettres.

Et un refus, qui compte autant que les quatre renommages : **je n'introduirai pas la lettre rhô**. Elle porte déjà le rapport d'échantillonnage préférentiel de la semaine 3 et la semaine 13 lui a refusé un deuxième sens ; la corrélation de la section 14.13 sera donc nommée en toutes lettres, « la corrélation de Pearson », à chacune de ses apparitions.

{{% comment %}}SOURCE: notation.md §3 quater{{% /comment %}}

---

## L'inventaire des symboles nouveaux

Aucun de ces symboles ne vous est demandé de mémoire : chacun est redéfini devant vous à sa première apparition dans une section.

| Symbole | Ce qu'il désigne | Première section |
| --- | --- | --- |
| \(\zeta^1, \zeta^2\) | les deux **segments d'épisode** comparés, \(L\) pas de couples observation-action | 14.2 |
| \(y_1, y_2\) | l'**étiquette humaine** : \((1,0)\), \((0,1)\) ou \((0{,}5\,;0{,}5)\) | 14.2 |
| \(L\) | la longueur d'un segment, en pas de jeu | 14.2 |
| \(\hat r(O_t, A_t)\) | le **modèle de récompense**, un réseau qui note un couple observation-action | 14.2 |
| \(R_1, R_2\) | la somme des récompenses prédites sur chacun des deux segments | 14.2 |
| \(\hat P[\zeta^1 \succ \zeta^2]\) | la probabilité, selon le modèle, que le premier segment soit préféré | 14.2 |
| \(\varsigma(\cdot)\) | la **fonction logistique**, écrite ainsi pour ne pas se confondre avec un écart-type | 14.2 |
| \(D\) | l'ensemble des paires étiquetées ; ce n'est **pas** le \(\mathcal{D}\) de la semaine 13 | 14.2 |
| \(p_{\text{rec}}\) | la probabilité de déclencher l'enregistrement d'un segment | 14.4 |
| \(\hat\mu_{100}, \hat\sigma_{100}\) | moyenne et écart-type glissants des cent dernières prédictions du modèle | 14.7 |
| \(\tilde r_t\) | la récompense prédite **après** normalisation, celle que l'agent reçoit | 14.7 |
| \(\pi_\varnothing\) | la politique « ne rien faire », référence des effets secondaires | 14.9 |
| \(d(s_i, s_0)\) | une distance entre un état atteint et l'état de départ | 14.9 |
| \(P\) | la **récompense de substitution**, celle qu'on optimise | 14.12 |
| \(T\) | la **récompense réelle**, celle qu'on évalue et qu'on n'optimise jamais | 14.12 |

> [!NOTE]
 **Une mise en garde sur le symbole \(D\), qui arrive une semaine après un symbole très proche.** La semaine 13 a écrit \(\mathcal{D}\) pour un **jeu de données figé de transitions**, et la leçon de cette semaine-là était justement que ce symbole porte le même contenu qu'un tampon de rejeu. Le \(D\) de cette semaine-ci est un autre objet : un ensemble de **paires étiquetées**, c'est-à-dire de triplets formés de deux segments et d'un jugement. Il n'y a pas de transition dedans, il n'y a pas de récompense dedans, et il n'alimente aucune cible de Bellman. Il alimente une régression logistique. Je l'écris sans la ronde de la semaine 13 pour cette raison, et je ne m'en servirai que dans la section 14.2.

---

## Un mot que la semaine 13 détient déjà, et qu'il ne faut pas lui prendre

Une dernière précaution de vocabulaire, et elle vaut trois paragraphes plutôt qu'une section.

La semaine 13 a installé « **décalage de distribution** » dans un sens précis : une politique apprise qui quitte la région de l'espace couverte par un jeu de données figé. C'est un problème interne à l'entraînement, et c'est celui qui faisait grandir l'erreur.

Il existe un autre problème, voisin par le nom et différent par la nature : un modèle entraîné sur une distribution et **déployé sur une autre**, par exemple un robot réglé dans un bureau et mis en service dans un atelier. L'enjeu y est double, et la seconde partie est la plus désagréable : non seulement la performance baisse, mais le système peut **croire à tort qu'il fonctionne bien**.

{{% comment %}}SOURCE: AMODEI §7 p.16-17{{% /comment %}}

Ce cours ne donnera pas le même nom aux deux. « Décalage de distribution » garde le sens de la semaine 13. Le second s'écrit en toutes lettres, **« changement de distribution entre entraînement et déploiement »**, et ne sera jamais abrégé. Vous le rencontrerez deux fois cette semaine, pas davantage : ce n'est pas le sujet de la semaine, c'est une voisine à ne pas confondre.

{{% comment %}}SOURCE: notation.md §3 quater{{% /comment %}}

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Expliquer pourquoi une récompense est une **spécification** et non une mesure, et donner deux objectifs qu'on ne sait pas réduire à un nombre unique.
- Décrire le cas du sous-marin : les trois activités notées, le délai du bonus de sauvetage, et pourquoi la ressource qui tue l'agent n'est liée à aucun signal.
- Dire ce qu'est le **cercle vicieux du réglage** d'un environnement, et pourquoi ce cours le présente comme un aveu d'échec plutôt que comme une solution.
- Définir un **segment d'épisode** et une **étiquette de préférence**, et donner les trois valeurs possibles de l'étiquette.
- Écrire le **modèle de préférence** à partir des deux sommes de récompenses prédites, et dire ce qu'il suppose sur le lien entre une préférence et une somme.
- Écrire la **perte d'entropie croisée** de ce modèle, et dire à quelle transformation de \(\hat r\) elle est **invariante**.
- Donner les **trois bénéfices** de la comparaison sur l'annotation, et dire lequel des trois est structurellement impossible à obtenir d'une démonstration humaine.
- Décrire la boucle complète à trois processus, puis la simplification séquentielle, et nommer **cinq choses** que cette simplification abandonne.
- Expliquer, sans rien construire, à quoi sert la rétroaction humaine dans la fabrication d'un grand modèle de langue, et dans quel ordre les trois étapes s'enchaînent.
- Donner le coût mesuré de la chaîne : heures de calcul, pas d'environnement, nombre de segments, et volume de stockage.
- Dire pourquoi l'enveloppe d'enregistrement se place **avant** les enveloppes de prétraitement, et ce que la personne verrait autrement.
- Décrire le modèle de départ et son **optimum local**, et dire ce que cet optimum démontre sur la récompense d'origine.
- Décrire l'interface d'étiquetage, et dire combien de décisions une personne prend réellement par paire.
- Identifier, dans la description d'une expérience de ce type, **la phrase qui tient lieu de fonction de récompense**, et expliquer pourquoi elle n'est écrite nulle part ailleurs.
- Décrire l'architecture du modèle de récompense, et nommer les **trois écarts** entre cette architecture et celle dont elle se réclame.
- Décrire la règle d'arrêt anticipé employée, et dire sur quelle partition elle est évaluée.
- Écrire l'objectif **réellement calculé** par le code de référence, et dire en quoi il diffère de l'objectif énoncé.
- Démontrer en deux lignes que l'objectif énoncé est une entropie croisée binaire sur un seul logit, et nommer le correctif d'un caractère qui réconcilie les deux formes.
- Énoncer **trois conséquences pratiques** de la différence, dont le sort d'une paire étiquetée « les deux sont bons » et la dérive de l'échelle sur une somme de cinquante pas.
- Dire ce que la normalisation glissante de la section 14.7 corrige, et ce qu'elle ne corrige pas.
- Écrire la normalisation de la récompense prédite, et dire pourquoi une fenêtre glissante plutôt qu'une statistique globale.
- Dire ce que le gel des convolutions remplace, et nommer la garde classique qui est absente de toute la chaîne.
- Lire le tableau des trois tours, et dire pourquoi la phrase qui résume le gain ne doit pas être lue seule.
- Expliquer ce que démontre le tour 3, et en quoi il est la rencontre des deux moitiés de la semaine.
- Définir un **accident** au sens étroit, et situer cinq catégories de problèmes selon l'endroit du processus où la chose casse.
- Nommer les **deux catégories** qui survivent à un apprentissage parfait et à des données infinies, et dire pourquoi c'est la phrase la plus coûteuse de la semaine.
- Nommer les trois tendances qui amplifient le problème, et dire laquelle concerne directement ce cours.
- Énoncer les **six mécanismes** d'exploitation d'une récompense, avec un exemple pour chacun, et dire lequel s'applique directement à un modèle de récompense appris.
- Énoncer la **loi de Goodhart** et dire ce qui, dans son énoncé, rend une corrélation observée inutile comme garantie.
- Décrire quatre parades et, pour chacune, l'aveu qui l'accompagne.
- Définir la **supervision extensible**, et expliquer pourquoi la première moitié de cette semaine en est une réponse.
- Définir l'**apprentissage par renforcement semi-supervisé**, et reconnaître la chaîne de la première moitié dans une direction esquissée dix ans plus tôt.
- Distinguer les **trois types d'écart** entre un substitut et ce qu'on voulait, chacun sur le même exemple de circulation routière.
- Définir la **puissance d'optimisation**, et nommer les quatre axes par lesquels on la fait varier.
- Expliquer le protocole qui rend l'écart mesurable, et dire laquelle des deux récompenses n'est jamais optimisée.
- Lire une courbe de substitut contre récompense réelle, repérer une **transition de phase**, et dire pourquoi une baisse non monotone n'est pas une anomalie de mesure.
- Dire ce que change une transition de phase pour la **surveillance** d'un système déployé.
- Expliquer pourquoi une forte corrélation positive entre substitut et récompense réelle ne protège de rien.
- Raconter trois comportements de bascule, dont un où l'optimum du substitut est politiquement inapplicable et un où moins de risque coûte plus cher.
- Expliquer pourquoi un contre-exemple où le substitut reste aligné est instructif, et ce qu'un bogue de simulateur y ajoute.
- Placer un même cas sur les **deux axes** de la semaine : un type d'écart, plusieurs mécanismes, et des cases vides.
- Expliquer pourquoi une liste de neuf éléments serait une erreur de lecture, et non un simple raccourci.
- Argumenter que la notion de **récompense réelle** est une convention d'expérience, et dire ce que cette convention autorise et interdit.
- Lire un chiffre de détection avec son protocole : ce que l'étiquetage a mesuré, ce qu'il a écarté, et le chiffre compagnon sous le hasard.
- Poser les trois questions que la chaîne de la première moitié ne pose pas : qui étiquette, selon quels critères, et à quel prix.

---

## Prérequis et outils

De la **semaine 1**, la définition même d'une récompense et l'hypothèse que cette semaine met en cause. De la **semaine 2**, trois choses qui servent directement : le réseau convolutif, l'**entropie croisée binaire** comme perte de classification, et le couple normalisation par lots et abandon de neurones, que la section 14.6 retrouve tel quel. De la **semaine 3**, la divergence de Kullback-Leibler, nommée en section 14.7 pour constater son **absence**. De la **semaine 5**, les enveloppes de prétraitement Atari, l'écrêtage de la récompense et le passage en niveaux de gris : la section 14.4 va délibérément se placer **avant** elles. De la **semaine 8**, l'acteur-critique à avantage et les environnements vectorisés, qui sont l'algorithme de toute la chaîne. De la **semaine 10**, l'objectif de substitution sous contrainte, et surtout la discipline de mesure installée au jalon 3 : plusieurs graines, un intervalle, et un protocole écrit. De la **semaine 13**, enfin, un mécanisme dont vous allez voir la copie exacte sous un autre nom : un optimiseur branché sur un estimateur que rien ne vient contredire **cherche les erreurs de cet estimateur**. Remplacez « estimateur de valeur » par « modèle de la préférence humaine », et vous tenez la section 14.8 avant de l'ouvrir.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | les quatre volets du laboratoire ; aucun ne demande de processeur graphique, et le plus long tient en une quinzaine de minutes |
| **PyTorch** | le modèle de récompense, les deux formes de la perte de préférence, et l'acteur-critique réduit du volet B |
| **Gymnasium** | l'environnement jouet des volets B et C, et l'enveloppe qui substitue une récompense à une autre |
| **NumPy** | la fenêtre glissante de normalisation, et la génération des étiquettes par une règle écrite par vous |
| **Matplotlib** | les deux courbes du volet C, qui sont la figure centrale de la semaine refaite à votre échelle |
| **Python standard** | `collections.deque` pour la fenêtre glissante, `json` pour le fichier d'étiquettes |
| **Page « Notation » du cours** | la section ajoutée cette semaine, avec les quatre renommages ci-dessus |
| **Page « Glossaire » du cours** | une vingtaine de termes nouveaux, dont neuf qui n'avaient pas de forme française attestée |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 14{{% /comment %}}

> [!WARNING]
 **La chaîne que cette semaine décrit n'est pas reproductible dans une session gratuite, et je le dis avant de commencer plutôt qu'en note de bas de page.** Comptez environ treize heures de calcul sur processeur graphique pour l'ensemble des quatre entraînements, douze gigaoctets de segments enregistrés sur disque, un serveur web à maintenir en vie pendant l'étiquetage, et trois cents jugements humains produits à la main. Aucune de ces quatre contraintes ne tient dans un carnet Colab, et la quatrième ne tient dans aucune machine. Le laboratoire fait donc autre chose, et il le fait ouvertement : il isole **quatre mécanismes** que l'on peut écrire, exécuter et mesurer en quelques minutes chacun. **Aucun des quatre volets n'a été exécuté par ce cours**, et les consignes le disent à nouveau à l'endroit où cela compte.

---
