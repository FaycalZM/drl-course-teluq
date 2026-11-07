---
title: "Laboratoire"
weight: 13
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté. Ce qui est évalué, ce sont les **livrables finaux**, qui viennent juste après.

Et je commence par l'énoncé que l'introduction a annoncé et qui ne figure qu'ici, en entier, avec ses chiffres. Cette semaine a décrit quatre applications. **Une seule s'exécute dans un carnet**, et je vous dois les raisons des trois autres plutôt qu'un silence.

| Application | Statut dans ce cours | Pourquoi, exactement |
| --- | --- | --- |
| **Le marché** | **déjà fait**, en semaine 7 | Les données sont fournies, l'entraînement tient en quelques minutes sur Colab. Cette semaine le relit comme comparaison et ne le refait pas |
| **Le paragraphe** | **s'exécute**, avec trois réserves | **Réserve 1, la plateforme.** Le paquet s'installe dans un carnet **parce que Colab tourne sous Linux** ; il ne prend en charge que Linux et macOS, sur une machine Windows il demande un conteneur, et il dépend d'un moteur de fiction interactive externe. Il tourne donc dans le carnet et **pas forcément sur votre machine**. **Réserve 2, les versions.** Plusieurs paquets de la chaîne sont **épinglés à une version précise** et la compatibilité se casse d'une version à l'autre : si vous changez une version, vous changez d'expérience. **Réserve 3, le paiement.** La partie « modèle de langue » demande une **clé d'interface payante**, elle ne peut donc **pas** être exigée : la transcription est dans la page et rien ne vous est demandé |
| **La page rendue** | **facultative, non notée, hors du carnet** | Il faut un **navigateur piloté** : un pilote automatisé plus un binaire de pilotage dont la version doit correspondre à celle du navigateur installé. Cela ne tient pas dans une session Colab gratuite, et ce point a été tranché au début du cours : c'est un exercice facultatif hors environnement de carnet |
| **La permutation** | **démonstration seulement**, jamais un entraînement | Environ **six jours** de calcul sur un seul processeur graphique pour refaire l'entraînement d'origine ; environ **vingt heures** pour l'entraînement du cube trois par trois ; et **une à deux heures** même pour la version réduite au cube deux par deux. Vous examinerez un modèle et des journaux fournis |

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}} {{% comment %}}SOURCE: DECISIONS.md D14{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.13 p.390, p.420{{% /comment %}} {{% comment %}}SOURCE: LAPAN ch.21 p.668-669{{% /comment %}}

> [!IMPORTANT]
 **Pourquoi je mets ce tableau en tête du laboratoire et non en note de bas de page.** Pendant treize semaines, ce cours a distingué ce qui s'exécute de ce qui se raconte, et vous a dit chaque fois de quel côté vous étiez. Une dernière semaine qui annoncerait quatre laboratoires exécutables et n'en livrerait aucun annulerait ce travail d'un coup. Il y a **un** volet noté dans l'esprit des autres semaines, et il est court et il tourne. Il y a **un** volet de démonstration, où vous lisez des mesures fournies au lieu de les produire. Et il y a **deux** volets facultatifs, dont l'un ne tient pas dans un carnet et l'autre demande un paiement. C'est l'état réel des choses, et le savoir fait partie de ce que cette semaine enseigne.

---

## Volet A : mesurer ce qu'une liste de commandes admissibles fait à un problème

C'est le volet principal, c'est le seul qui tourne de bout en bout, et il est court. Il ne contient **aucun entraînement**, et c'est voulu : la semaine porte sur la caractérisation d'un problème, pas sur l'optimisation d'un agent.

**Étape 1, engendrer un jeu.** Demandez au générateur une quête de **longueur 5**, avec une graine fixée et notée. Fixez aussi le thème et le scénario, et écrivez dans votre carnet les cinq paramètres que vous avez choisis : c'est votre protocole, et sans lui votre mesure de l'étape 4 ne sera comparable à rien.

**Étape 2, écrire l'adaptateur, et c'est la pièce qui prend le plus de temps.** L'environnement renvoie **quatre** valeurs au lieu des cinq que Gymnasium attend, et ne déclare ni espace d'observations ni espace d'actions. Écrivez une classe qui enveloppe l'environnement, renvoie cinq valeurs, et **documente en commentaire la décision que vous avez prise** sur l'indicateur de troncature manquant : le mettez-vous toujours à faux, ou le déduisez-vous d'un compteur de pas que vous tenez vous-même ? Les deux choix sont défendables, et le non-choix n'en est pas un. Testez votre adaptateur sur un épisode complet joué au hasard, et vérifiez qu'il termine.

**Étape 3, inspecter ce que l'environnement accepte de montrer.** Demandez les champs d'information un par un et affichez-les pour trois états successifs : description de la pièce, inventaire, nom du lieu, faits du monde, dernière action, commandes admissibles, suite d'actions gagnante. Répondez à une question en une phrase : **lesquels de ces champs un environnement industriel vous donnerait-il ?**

**Étape 4, la mesure du volet.** Pour chacun des vingt premiers états que vous traversez, comptez la longueur de la liste de commandes admissibles. Puis calculez, et comparez, trois nombres : la taille de l'espace de production par pas, soit \(1250^8\) ; la médiane de vos longueurs de listes ; et le rapport des deux. Tracez l'histogramme des longueurs. Vous devez trouver une médiane de l'ordre d'une douzaine, et vous devez pouvoir écrire le rapport en ordre de grandeur.

**Étape 5, l'autre béquille.** Activez la récompense intermédiaire et rejouez le même épisode au hasard, en journalisant la récompense à chaque pas. Comparez le nombre de pas récompensés avec et sans. Dites en deux phrases lequel des deux réglages, la liste admissible ou la récompense intermédiaire, change la **classe** du problème, et lequel ne change que sa **difficulté**.

**Ce que ce volet établit** : que la réduction d'espace d'actions est mesurable, et de combien. **Ce qu'il n'établit pas** : quoi que ce soit sur la performance d'un agent, puisque vous n'en entraînez aucun. Dites-le dans votre conclusion.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-15.ipynb" label="Volet A : engendrer un jeu textuel, écrire l'adaptateur Gymnasium, et mesurer l'effet des commandes admissibles" >}}

---

## Volet B : lire une divergence, et poser l'ancre qui la répare

Volet de **démonstration**. Vous n'entraînez rien : vous recevez des journaux et un modèle, et vous les lisez. C'est le volet qui vous prépare le plus directement à la lecture critique que les livrables finaux demandent.

**Étape 1, le diagnostic.** Tracez les deux pertes fournies pour l'entraînement de la méthode d'origine, politique et valeur, sur le même axe de temps. Répondez à trois questions : à quel moment la perte de valeur quitte-t-elle son plateau, que fait la perte de politique à ce moment-là, et laquelle des deux courbes aurait déclenché une alerte si vous n'aviez surveillé qu'elle ?

**Étape 2, l'explication, et elle s'écrit sans code.** En trois ou quatre phrases, expliquez pourquoi la cible de valeur de la section 15.5 ne fixe aucune échelle, et pourquoi l'état résolu est le seul endroit de l'espace où une valeur est connue. Mentionnez la semaine 14 : c'est le même mécanisme sur un autre objet.

**Étape 3, le correctif, écrit comme une fonction pure.** Implémentez les deux variantes de la cible de valeur, celle de la section 15.5 et celle de la section 15.7, comme deux fonctions qui prennent les valeurs des enfants, les indicateurs de but et un booléen disant si l'état courant est résolu. **N'entraînez rien.** Évaluez les deux sur trois cas construits à la main : un état loin du but, un état à une rotation du but, et l'état résolu lui-même. Montrez numériquement que les deux fonctions coïncident sur les deux premiers et diffèrent sur le troisième.

**Étape 4, la lecture des mesures fournies.** Les deux tableaux de la section 15.7 vous donnent les résultats sur le cube deux par deux et sur le trois par trois. Écrivez trois phrases : ce que le correctif a amélioré, de combien, et pourquoi la profondeur 13 ne doit pas être comparée directement à la profondeur de brouillage de 1 000 du protocole publié. La troisième phrase est celle qui compte, et c'est la section 15.8 qui vous en donne les mots.

**Ce que ce volet établit** : que vous savez diagnostiquer une fonction de valeur sans ancre et écrire le correctif. **Ce qu'il n'établit pas** : que le correctif résout le problème, puisque la mesure fournie montre justement qu'il ne le résout pas sur le cube complet.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-15.ipynb" label="Volet B : lire une divergence de valeur sur des journaux fournis, et écrire les deux cibles comme fonctions pures" >}}

---

## Volet C : facultatif et non noté, et il demande un navigateur

Ce volet ne tourne pas dans un carnet, et il n'est pas noté. Je le propose parce qu'il contient la mesure la plus frappante de la semaine et qu'elle se refait en cinq minutes sur une machine de bureau.

**Prérequis, et ils sont réels.** Une installation locale, un navigateur, un binaire de pilotage dont la version correspond à celle du navigateur, et le paquet du jeu de référence. Si l'une des quatre conditions manque, passez ce volet : il n'enlève rien à votre évaluation.

**Étape 1.** Sur la tâche de clic élémentaire, émettez le **même** clic correct deux fois : une fois avec le navigateur dessiné à l'écran, une fois sans interface. Journalisez les trois valeurs renvoyées : la récompense fournie, la récompense brute, et le temps écoulé.

**Étape 2.** Répétez chaque condition dix fois et donnez la moyenne et l'écart des deux récompenses fournies. Vous devez obtenir deux populations qui ne se recouvrent pas, pour une récompense brute identique.

**Étape 3, et c'est la question du volet.** En deux phrases : qu'est-ce qu'un score publié sur ce jeu de référence mesure exactement, et que faudrait-il publier à côté pour qu'il soit comparable ?

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-15.ipynb" label="Volet C, facultatif et hors carnet : mesurer la décroissance de la récompense avec le temps d'horloge" >}}

---

## Volet D : la lecture, et elle ne demande ni machine ni paiement

Le dernier volet est une lecture, et il n'y a rien à exécuter. La transcription de la section 15.9 est dans la page : le dispositif, les cinq commandes de la partie résolue, le compte de neuf sur vingt, les quatre catégories d'échec et le coût.

**Ce que je vous demande**, et c'est un exercice d'écriture plutôt que de code : rédigez **un paragraphe de dix lignes** qui rapporte ce résultat honnêtement. Il doit contenir le chiffre, le protocole, les quatre réserves de la section 15.9, et la conclusion que le résultat autorise. Puis rédigez le même paragraphe **malhonnêtement**, c'est-à-dire en gardant tous les chiffres exacts mais en omettant ce qu'il faut pour que la conclusion paraisse plus large qu'elle n'est.

Mettez les deux côte à côte et gardez-les. C'est le meilleur entraînement que je connaisse à la relecture de son propre rapport, et c'est le dernier exercice que ce cours vous propose.

---

## Pas de solution courte cette semaine, et c'est délibéré

Les quatorze semaines précédentes se terminaient sur une solution courte de bibliothèque, pour que vous puissiez comparer votre code à une implémentation de référence. Cette semaine n'en a pas, et pour une raison qui est elle-même l'enseignement de la semaine : **aucune bibliothèque ne caractérise un problème à votre place**. Il n'existe pas de fonction qui vous dise de quelle nature est votre action, qui a écrit votre récompense, et laquelle des quatorze semaines s'applique. C'est le seul travail de ce cours qui ne s'automatise pas, et c'est pour cela qu'il est la dernière chose qu'il vous apprend.

---
