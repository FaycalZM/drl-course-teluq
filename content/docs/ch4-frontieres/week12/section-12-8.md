---
title: "12.8 Le résultat, et la largeur de la conclusion qu'il autorise"
weight: 9
---

## Quinze heures d'entraînement, et les meilleurs modèles sont les premiers

Je vais vous rapporter ce que cette seconde méthode obtient sur Puissance 4, et le rapport est bref parce que le résultat est bref.

**Quinze heures** d'entraînement, **3 400** épisodes. L'entraînement n'est pas rapide, et il faut le dire franchement : c'est bien plus lent, pour le même jeu, que la méthode de la section 12.5. Les courbes de perte de la politique et de la valeur n'ont, comme en auto-jeu, **aucune tendance claire**.

{{% comment %}}SOURCE: LAPAN ch.20 p.640{{% /comment %}}

Un tournoi est donc lancé entre les points de contrôle, comme en section 12.5, et c'est là que le résultat tombe. Près de deux cents points de contrôle ont été enregistrés. Les deux meilleurs sont les points de contrôle **numéro 10** et **numéro 15**, avec 339 victoires pour 41 défaites pour le premier, et 298 pour 82 pour le second. Le troisième du classement est le point de contrôle 155, loin derrière. Autrement dit : **les meilleurs modèles sont ceux du tout début de l'entraînement**, et les quatorze heures et demie suivantes ont produit des réseaux moins bons.

{{% comment %}}SOURCE: LAPAN ch.20 p.640{{% /comment %}}

C'est un échec de convergence, et il faut l'appeler ainsi. Une précision l'accompagne, et elle est décisive pour la suite de cette section : très peu de réglage d'hyperparamètres a été effectué sur cet entraînement.

{{% comment %}}SOURCE: LAPAN ch.20 p.640{{% /comment %}}

---

## Comment lire un résultat négatif, et c'est le deuxième en trois semaines

Vous avez déjà vu ce genre de rapport dans ce cours. La semaine 10 a rapporté une méthode d'optimisation du second ordre qui, dans sa mise en œuvre mesurée, ne battait pas ses concurrentes plus simples, et je vous avais demandé de ne pas en tirer de conclusion sur la méthode elle-même. Même exercice ici, et il vaut la peine d'être fait deux fois.

> [!IMPORTANT]
 **Voici la largeur exacte de ce que l'on peut conclure, et elle est étroite.** Ce qui est mesuré, c'est **une** mise en œuvre, sur **un** petit jeu, avec **un** jeu d'hyperparamètres non réglés, et qui ne converge pas. Voilà tout. La méthode, elle, détient l'état de l'art sur cinquante-sept jeux Atari et a dépassé les records de la méthode de la section 12.5 sur trois jeux de plateau classiques. Les deux énoncés sont vrais en même temps, et il n'y a aucune contradiction : ils ne portent pas sur le même objet. L'un porte sur une reproduction, l'autre sur une méthode. **L'écart entre les deux est la leçon de cette section**, et c'est une leçon dont vous aurez besoin chaque fois que vous lirez un résultat publié : une méthode qui fonctionne n'est pas une méthode qui fonctionnera chez vous, et une reproduction qui échoue ne réfute rien.

{{% comment %}}SOURCE: LAPAN ch.20 p.623 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.20 p.640{{% /comment %}}

Deux conséquences pratiques, que je vous donne parce qu'elles sont réutilisables.

**La première est un réflexe de lecture.** Quand vous rencontrez un résultat négatif sur une méthode connue, cherchez trois choses avant tout : la taille du problème, le temps de calcul dépensé, et ce qui est dit du réglage des hyperparamètres. Ici les trois sont donnés sans détour, ce qui rend ce résultat utilisable. Un résultat négatif qui cache ces trois informations n'est pas un résultat.

**La seconde est une leçon de conception.** Cette méthode a plus de pièces mobiles que la précédente : trois réseaux au lieu d'un, une récompense à prédire en plus, un déroulement à construire, une pondération à choisir. Chaque pièce mobile est une occasion de mal régler quelque chose. La généralité se paie en surface d'erreur, et c'est exactement ce que la section 12.1 annonçait en disant que le prix était connu d'avance.

---

## Ce qui reste vrai, et ce que cette semaine n'a pas pu vérifier

Une dernière précision, parce que je ne veux pas vous laisser avec une impression fausse dans un sens ou dans l'autre.

La généralisation que cette méthode promet est **réelle** : parce que la recherche se déroule dans un état caché, rien ne la limite aux jeux à deux joueurs ni aux plateaux. Un jeu à un joueur avec une récompense à chaque pas entre dans le même cadre, et c'est d'ailleurs la raison de la récompense prédite par la dynamique, qui ne servait à rien à Puissance 4.

Mais ce cours ne l'a pas vérifié, et je préfère le dire plutôt que de le suggérer : l'application de cette méthode à un jeu vidéo reste, ici, un exercice proposé et non une mesure. Le laboratoire de cette semaine ne vous la demandera pas, et la section 12.11 vous dira ce que vous pourriez en faire au jalon 4 si le sujet vous attire.

{{% comment %}}SOURCE: LAPAN ch.20 p.641{{% /comment %}}

---
