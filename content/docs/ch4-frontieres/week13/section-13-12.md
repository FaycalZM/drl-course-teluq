---
title: "13.12 On retire l'environnement"
weight: 13
---

## Le même objectif, et plus aucun droit d'agir

Nous changeons de moitié de semaine. Respirez : tout ce qui précède, modèle du monde, latent, imagination, planificateur, est **mis de côté**. Pas contredit, mis de côté. La seconde moitié ne suppose aucun modèle, aucun latent, aucun encodeur. Elle suppose un jeu de données et une interdiction.

**L'énoncé.** L'objectif est celui de la semaine 1, inchangé : maximiser le retour espéré. Mais l'agent **ne peut plus interagir**. On lui donne un jeu de données **statique**

$$
\mathcal{D} = \big\{ (s^i_t,\; a^i_t,\; s^i_{t+1},\; r^i_t) \big\}_i
$$

et on lui demande la meilleure politique qu'il puisse en tirer. Les quatre conditions, et je les numérote parce que l'une d'elles s'oublie :

1. le jeu a été collecté par une **politique de comportement** \(\pi_\beta\), que l'on peut ne pas connaître ;
2. il est collecté **une seule fois** et **jamais modifié** ;
3. l'entraînement **n'interagit pas du tout** avec le processus de décision ;
4. la politique obtenue n'est déployée **qu'une fois complètement entraînée**.

{{% comment %}}SOURCE: OFFLINE p.7{{% /comment %}}

La quatrième est celle qui s'oublie, et elle est la plus lourde de conséquences pratiques. Il n'y a pas de phase de rodage, pas de déploiement progressif, pas de possibilité de corriger en observant les premiers pas. On entraîne, puis on branche, et ce qui se passe alors est ce qu'on obtient.

La loi des données se résume en deux lignes : les états suivent \(s \sim d^{\mathcal{D}}(s)\), c'est-à-dire la distribution des états que la politique de comportement a visités, et les actions suivent \(a \sim \pi_\beta(a \mid s)\). Rappel de l'introduction : \(\pi_\beta\) est **le \(b(a \mid s)\) de la semaine 4**, rebaptisé parce que cette moitié de semaine a besoin de l'écrire en indice d'une distribution d'états.

{{% comment %}}SOURCE: OFFLINE p.7-8{{% /comment %}}

---

## Un jeu d'entraînement pour une politique, et un jury qui n'est pas celui-là

Voici la façon la plus utile de se représenter la situation, et c'est l'analogie que je vous demande de garder tout en gardant aussi son démenti.

**\(\mathcal{D}\) est le jeu d'entraînement de la politique.** Exactement comme un jeu d'images est le jeu d'entraînement d'un classifieur. On a des données, on a un modèle à ajuster dessus, on a des lots et un optimiseur, et rien dans la boucle d'entraînement ne ressemble plus à ce que ce cours fait depuis douze semaines : il n'y a plus d'épisode, plus de collecte, plus d'alternance entre agir et apprendre. C'est de l'apprentissage sur un jeu fixe.

Et voici le démenti, qui est dans le même paragraphe et qui fait tout le problème : **la politique sera jugée sur le retour cumulé qu'elle obtient quand on l'emploie réellement à interagir avec le processus de décision**. On l'entraîne comme un apprentissage supervisé, et on la juge comme un apprentissage par renforcement.

{{% comment %}}SOURCE: OFFLINE p.7{{% /comment %}}

> [!IMPORTANT]
 **C'est le moment de reprendre le symbole \(\mathcal{D}\), et la page d'introduction vous avait prévenus.** Le \(\mathcal{D}\) de cette section est le même symbole que le tampon de rejeu de la semaine 5, et je le répète ici parce que c'est à cet endroit précis que la différence se met à mordre. En semaine 5, l'agent qui trouvait une estimation absurdement élevée pour une action allait l'essayer, observait qu'elle ne valait rien, rangeait cette transition dans son tampon, et corrigeait. **La boucle de correction passait par l'environnement.** Ici, cette boucle est coupée. L'agent peut croire n'importe quoi sur une action qui n'est pas dans \(\mathcal{D}\), et rien, jamais, ne viendra le démentir. Toute la section 13.14 est le développement de cette unique phrase.

L'équation que toute cette moitié de semaine attaque est, elle aussi, une vieille connaissance. C'est l'équation de Bellman pour une politique :

$$
Q^\pi(s_t, a_t) \;=\; r(s_t, a_t) \;+\; \gamma\, \E_{s_{t+1} \sim T,\; a_{t+1} \sim \pi}\big[ Q^\pi(s_{t+1}, a_{t+1}) \big]
$$

{{% comment %}}SOURCE: OFFLINE éq. 3 p.5{{% /comment %}}

Regardez où est le problème, et il est dans un seul endroit : **l'espérance de droite tire \(a_{t+1}\) dans \(\pi\)**, la politique qu'on apprend. Pas dans \(\pi_\beta\), la politique qui a produit les données. On a donc besoin de la valeur de \(Q^\pi\) à des actions que \(\pi\) choisirait, et dont rien ne garantit qu'elles figurent dans \(\mathcal{D}\). Gardez cette ligne à l'œil : c'est la seule faille, et toutes les réponses de la section 13.15 la bouchent de deux façons différentes.

---

## La recette qui semble suffire, et qui ne suffit pas

Il y a une façon évidente de faire de l'apprentissage hors ligne, et elle tient en deux modifications d'un code que vous avez déjà.

Prenez votre agent de la semaine 5. **Préremplissez son tampon de rejeu avec \(\mathcal{D}\), et mettez à zéro le nombre de transitions collectées par itération.** C'est tout. La boucle d'entraînement est inchangée : tirer un lot, calculer une cible, descendre un gradient. Vous venez d'écrire un algorithme hors ligne.

{{% comment %}}SOURCE: OFFLINE p.8{{% /comment %}}

**Le code.** La différence, dans son intégralité.

```python
def entrainer_hors_ligne(donnees_figees, q_reseau, q_cible, optimiseur,
                         n_pas=1000, taille_lot=256, gamma=0.99):
    """Un apprentissage hors ligne, obtenu depuis la boucle de la semaine 5
    par DEUX modifications et rien d'autre.

    1. Le tampon est prerempli avec le jeu de donnees figé.
    2. Aucune transition n'est collectee : la ligne de collecte a disparu.
    """
    tampon = donnees_figees                 # modification 1 : D, prerempli

    for pas in range(n_pas):
        lot = echantillonner(tampon, taille_lot)
        perte = perte_q(lot, q_reseau, q_cible, gamma)
        optimiseur.zero_grad()
        perte.backward()
        optimiseur.step()

        # modification 2 : il n'y a RIEN ici. Pas de env.step(),
        # pas de tampon.ajouter(), pas d'episode. La boucle est fermee
        # sur elle-meme, et c'est tout le probleme de la section 13.14.
    return q_reseau
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\mathcal{D}\) | le jeu de données **figé** | `donnees_figees`, puis `tampon` |
| \(\mathcal{B}\) | un lot tiré dans \(\mathcal{D}\) | `lot` |
| \(Q_{\mathbf{w}}(s,a)\) | la valeur d'action apprise | `q_reseau` |
| \(Q_{\mathbf{w}^-}\) | le réseau cible de la semaine 5, inchangé | `q_cible` |
| transitions collectées par itération | **zéro**, et c'est la définition du problème | l'absence de code |

> [!WARNING]
 **Et maintenant la phrase qui justifie les quatre sections suivantes : toutes les méthodes obtenues de cette façon ne sont pas efficaces en régime hors ligne.** Le code ci-dessus tourne. Il ne plante pas, la perte descend, les courbes ont l'air normales. Et la politique qu'il produit peut être **arbitrairement mauvaise**, y compris très en dessous de la politique de comportement qui a produit les données, y compris après avoir été meilleure en cours de route. Tout ce qui suit explique pourquoi, et cela n'a rien à voir avec un réglage d'hyperparamètre.

{{% comment %}}SOURCE: OFFLINE p.8{{% /comment %}}

---
