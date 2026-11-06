---
title: "8.4 Ça marche, sur un petit problème"
weight: 5
---

## CartPole, en moins de quatre cents épisodes

Avant de démonter l'algorithme, faisons-lui justice : il fonctionne, et il fonctionne avec très peu de réglage.

Les hyperparamètres tiennent en trois lignes. Un facteur d'actualisation \(\gamma = 0{,}99\). Un pas d'apprentissage de \(0{,}01\), ce qui est dix fois plus que ce que nous utilisions en semaine 5, et c'est révélateur : sans amorçage, la cible ne bouge pas sous nos pieds, et on peut avancer plus vite. Et quatre épisodes complets par mise à jour. Le réseau, lui, est le plus petit du cours depuis la semaine 2 : une couche cachée de 128 unités avec une activation ReLU, et une sortie par action.

{{% comment %}}SOURCE: LAPAN ch.11 p.335{{% /comment %}}

Le résultat, sur `CartPole-v1`, avec un critère d'arrêt placé à une récompense moyenne de 450 sur les cent derniers épisodes : **67 857 pas d'environnement et 384 épisodes**. Mettez ce nombre à côté de celui de la semaine 3. La méthode d'entropie croisée avait résolu le même problème en une quarantaine de lots de seize épisodes, soit environ **640 épisodes**. REINFORCE y arrive en moins de 400, et il y arrive avec la même structure de code, en remplaçant un filtre par percentile par un retour actualisé. C'est précisément le gain annoncé en introduction : remplacer un 0/1 par un vrai scalaire fait travailler toute l'information disponible au lieu d'un quart.

{{% comment %}}SOURCE: LAPAN ch.11 p.338{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.11 p.341{{% /comment %}}

La comparaison avec le réseau Q profond de la semaine 5 est plus intéressante encore, et elle est à double tranchant. Avec des hyperparamètres presque identiques sur le même problème, les deux méthodes convergent de façon **presque identique**, REINFORCE légèrement plus vite. Puis, une fois la récompense moyenne passée au-dessus de 400, le réseau Q profond rencontre des difficultés et perd une bonne partie de ce qu'il avait acquis, au point de devoir repartir presque de zéro, alors que REINFORCE termine proprement. Ce n'est pas une preuve de supériorité, c'est un épisode d'instabilité, et nous en avons vu les raisons en semaines 5 et 6 : une cible amorcée, un \(\max\) biaisé, un tampon qui mélange des politiques différentes. Mais c'est une illustration utile du fait qu'un algorithme plus simple n'est pas toujours le moins fiable.

{{% comment %}}SOURCE: LAPAN ch.11 p.340{{% /comment %}}

---

## Quatre différences entre les deux familles, et une franchise

Maintenant que vous avez les deux familles en main, voici leurs quatre différences structurelles. Je vous recommande de retenir ce tableau tel quel : il reviendra en section 8.9 avec des chiffres, et il reviendra en semaine 15 dans la comparaison méthodologique finale.

| | Méthodes fondées sur la politique | Méthodes fondées sur la valeur |
| --- | --- | --- |
| **Ce qui est optimisé** | le comportement, **directement** | le comportement, **indirectement**, via une valeur |
| **Origine des données** | **sur politique** : il faut des échantillons frais, produits par la politique courante | **hors politique** : on peut réutiliser d'anciennes transitions, des démonstrations humaines, des données d'une autre source |
| **Efficacité d'échantillon** | généralement **plus faible** : chaque transition sert une fois | généralement **plus élevée** : chaque transition est rejouée de nombreuses fois |
| **Coût de calcul par échantillon** | un seul passage dans le réseau, pour obtenir les probabilités d'action | **deux** lots d'états traités, l'état courant et le suivant, pour la cible de Bellman |

{{% comment %}}SOURCE: LAPAN ch.11 p.341{{% /comment %}}

Lisez attentivement les deux dernières lignes, parce qu'elles disent des choses contraires et que c'est voulu. L'**efficacité d'échantillon** n'est pas l'**efficacité de calcul**, et ces deux grandeurs pointent très souvent en sens inverse. Une méthode qui réutilise trente fois chaque transition consomme peu d'environnement et beaucoup de processeur graphique ; une méthode sur politique consomme beaucoup d'environnement et peu de calcul par échantillon. Vous avez déjà rencontré cette tension en semaine 7, quand la configuration la plus rapide en trames par seconde s'est révélée presque la plus lente à résoudre le jeu. La section 8.9 reprendra exactement ce raisonnement, avec les chiffres des deux colonnes.

{{% comment %}}SOURCE: LAPAN ch.11 p.341{{% /comment %}}

Et maintenant la franchise que je vous dois, parce qu'elle concerne la valeur pratique de ce que vous venez d'apprendre.

> [!NOTE]
 **Personne ne met REINFORCE en production, et ce n'est pas pour cela que nous l'écrivons.** Le gradient de politique nu, tel que nous venons de l'implémenter, n'est pratiquement plus utilisé : la méthode acteur-critique de la section 8.8, nettement plus stable, le remplace partout. Je vous le fais écrire quand même, et pour deux raisons précises. D'abord parce qu'il **établit les concepts** : le théorème, l'échelle du gradient, le vecteur d'éligibilité, la perte qui n'est pas une perte. Tout ce que nous ajouterons ensuite se greffe sur ce squelette, et rien ne s'y substitue. Ensuite parce qu'il **établit les instruments de mesure** : les quatre quantités que nous surveillerons à partir de la section 8.9 sont celles que REINFORCE rend lisibles, et les lire sur un algorithme simple avant de les lire sur un algorithme composite est la seule façon de savoir ce qu'elles valent.

{{% comment %}}SOURCE: LAPAN ch.11 p.344{{% /comment %}}

---
