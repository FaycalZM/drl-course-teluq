---
title: "13.14 Le décalage de distribution, et l'erreur qui grandit"
weight: 15
---

## Deux décalages, et un seul qui tue

Nous arrivons au centre de la semaine. Si vous ne retenez qu'une section, que ce soit celle-ci.

Il y a **deux** décalages de distribution dans un problème hors ligne. Ils portent le même nom, ils ont des mécanismes différents, et un seul des deux est fatal. Les confondre, c'est se tromper sur ce qu'il faut réparer.

**Premier décalage, au moment du test, et il porte sur les états.** La politique apprise visite des états selon \(d^\pi(s)\), qui diffère systématiquement de \(d^{\mathcal{D}}(s)\). Déployée, elle se retrouve donc dans des états **hors distribution**, sur lesquels ni son acteur ni sa valeur d'action n'ont jamais été entraînés, et elle y produit des actions erronées. C'est vrai d'un acteur explicite comme de la politique gloutonne implicite d'une valeur d'action.

Ce décalage se **maîtrise**, au moins en principe. Contraindre la politique apprise à rester proche de la politique de comportement borne le décalage des distributions d'états :

$$
\KL(\pi \,\|\, \pi_\beta) \le \epsilon_{\text{c}}
\quad \Longrightarrow \quad
\KL\big(d^\pi \,\|\, d^{\mathcal{D}}\big) \;\le\; O\!\left(\frac{\epsilon_{\text{c}}}{(1-\gamma)^2}\right)
$$

{{% comment %}}SOURCE: OFFLINE p.18{{% /comment %}}

Deux remarques, et elles tempèrent sérieusement l'optimisme. D'abord, **cette borne est très lâche en pratique** : le facteur \(1/(1-\gamma)^2\) vaut dix mille pour \(\gamma = 0{,}99\), ce qui la rend inexploitable comme garantie numérique ; elle dit une **structure**, à savoir que contraindre la politique contrôle le décalage des états, et non une quantité. Ensuite, **rester près de \(\pi_\beta\) peut coûter très cher**, parce que \(\pi_\beta\) peut être bien plus mauvaise que ce que ses données permettraient : des données médiocres mais variées peuvent contenir de quoi faire excellent, et s'interdire de s'en écarter revient à jeter cette possibilité.

> [!NOTE]
 **Et une précision de lecture, parce que ce point se trouve écrit à l'envers dans des textes par ailleurs excellents.** Les états problématiques au moment du test sont ceux que visite la **politique apprise**, donc ceux tirés de \(d^\pi(s)\). Les états tirés de \(d^{\mathcal{D}}(s)\) sont, par définition, **dans** la distribution des données : c'est elle. Si vous lisez une phrase qui qualifie d'« hors distribution » des états tirés de la distribution des données, c'est un lapsus de notation, et il faut lire \(d^\pi\). Ce cours écrit la version correcte, et je la signale parce qu'un étudiant qui recopie la fausse perd le fil du mécanisme entier.

---

## Le second décalage, qui agit pendant l'entraînement et porte sur les actions

Et voici celui qui tue.

Commençons par une observation qui surprend : **le décalage des états n'a aucun effet pendant l'entraînement**. Regardez la boucle du code de la section 13.12. Ni la politique ni la valeur d'action n'y sont jamais évaluées en un état qui ne vienne pas de \(\mathcal{D}\) : tous les états du calcul sont tirés du jeu de données. Le décalage des états est donc un problème de **déploiement**, pas d'optimisation.

Mais regardez maintenant la cible de la remontée de Bellman, celle de l'équation de la section 13.12. Elle a besoin de

$$
Q^\pi(s_{t+1}, a_{t+1}) \qquad \text{avec} \qquad a_{t+1} \sim \pi(a_{t+1} \mid s_{t+1})
$$

L'état \(s_{t+1}\) vient bien du jeu de données : il est dans la transition qu'on a tirée. **Mais l'action \(a_{t+1}\) ne vient pas du jeu de données.** Elle vient de la politique qu'on est en train d'apprendre. C'est donc une valeur d'action évaluée en une action sur laquelle elle **n'a jamais été entraînée**, et ce calcul a lieu à **chaque pas de gradient**, dès le premier.

{{% comment %}}SOURCE: OFFLINE p.19{{% /comment %}}

C'est le **décalage des actions**, qui met en jeu ce que ce cours appellera désormais une **action hors distribution** (*out-of-distribution action*) : une action que la valeur n'a jamais vue à cet état. Il agit pendant l'entraînement, et il n'est pas évitable par un meilleur réglage : il est inscrit dans la forme de la cible.

> [!IMPORTANT]
 **Une conséquence structurelle qu'il faut retenir, parce qu'elle commande toute la section 13.15.** Puisque la valeur d'action est évaluée aux **mêmes états** que ceux sur lesquels elle a été entraînée, **seule son entrée d'action peut être hors distribution**. C'est une restriction énorme du problème, et c'est une bonne nouvelle : elle explique pourquoi il suffit de contraindre la **loi des actions** pour fermer la faille, et pourquoi personne n'essaie de contraindre la distribution des états pendant l'entraînement. Le problème est unidimensionnel, au sens où il n'y a qu'une seule entrée à surveiller.

---

## Pourquoi l'erreur grandit au lieu de se diluer, en trois temps

Et maintenant l'idée la plus importante de la semaine. Jusqu'ici, toutes les erreurs que ce cours a rencontrées se **diluaient** : une estimation bruitée est corrigée par la suivante, un biais s'amortit, une mauvaise cible est remplacée. Ici, l'erreur **grandit**, et voici pourquoi, en trois temps.

**Temps un : la cible est fausse.** Elle dépend de la valeur d'action en des actions hors distribution. Quand \(\pi\) diffère substantiellement de \(\pi_\beta\), ces valeurs peuvent être **très erronées**, parce qu'un réseau interrogé hors de son domaine d'entraînement renvoie ce que son extrapolation produit, c'est-à-dire n'importe quoi.

**Temps deux, et c'est le temps décisif : la politique est explicitement optimisée pour maximiser cette quantité.** Elle maximise \(\E_{a \sim \pi}[Q^\pi(s,a)]\). Donc si la valeur d'action est erronément **grande** quelque part hors distribution, la politique **apprend à aller exactement là**. Ce n'est pas un accident statistique : c'est le résultat du travail de l'optimiseur, qui fait précisément ce qu'on lui demande. Et cela vaut pour un acteur explicite comme pour la politique gloutonne implicite d'une valeur d'action : un \(\argmax\) sur les actions est la même recherche.

**Temps trois : en ligne, cela se corrige tout seul ; hors ligne, c'est impossible.** En ligne, l'agent va essayer la transition qu'il croit excellente, et il observe qu'elle ne l'est pas. La correction arrive, elle est automatique, et c'est la raison pour laquelle aucune des douze semaines précédentes n'a eu à s'en préoccuper. Hors ligne, **aucune correction n'est possible**, et les erreurs **s'accumulent à chaque itération de l'entraînement**, ce qui conduit à des résultats finaux arbitrairement mauvais.

{{% comment %}}SOURCE: OFFLINE p.19{{% /comment %}}

> [!IMPORTANT]
 **Voici la phrase que je veux que vous reteniez de la semaine entière : un optimiseur est une recherche des erreurs de son propre estimateur.** Ce n'est pas une métaphore. Maximiser \(Q\) sur les actions, c'est chercher l'action où \(Q\) est le plus grand ; or \(Q\) est le plus grand, en général, là où il se trompe le plus par excès, puisque c'est là qu'il n'est contraint par rien. Un optimiseur appliqué à un estimateur non contraint hors distribution **trouve ses erreurs et s'y installe**. En ligne, l'environnement joue le rôle d'un arbitre qui réfute. Hors ligne, il n'y a pas d'arbitre, et le même mécanisme qui faisait la force de la méthode devient ce qui la détruit. Et notez que vous avez déjà vu ce mécanisme cette semaine, en section 13.3 : le planificateur qui exploite les inexactitudes d'un modèle déterministe. **C'est rigoureusement le même phénomène**, appliqué à une valeur d'action au lieu d'une transition.

{{< bookfig src="13-03.png" week="13" >}}

La **Figure 13-3** est l'image la plus importante de cette semaine, et je vous demande d'y passer une vraie minute. Vous y verrez trois choses superposées : la **couverture** du jeu de données dans l'espace des couples état-action, la politique apprise qui **dérive hors de cette couverture**, et la valeur estimée qui **monte exactement là où il n'y a plus de données pour la démentir**. Et surtout la flèche de retour, celle qui part de l'\(\argmax\) de la valeur et pointe vers la région vide : c'est elle qui fait que l'erreur grandit, parce qu'elle montre que l'optimiseur **cherche** la région où l'estimation se trompe.

---

## Le code qui montre la faille en six lignes

**Le code.** La cible de la section 13.12, écrite de façon à rendre la faille **visible**. Il n'y a rien à corriger ici : ce code est correct au sens de la semaine 5, et c'est précisément ce qui est inquiétant.

```python
import torch


def cible_hors_ligne(lot, q_cible, acteur, gamma=0.99):
    """La cible de Bellman, avec la faille annotee.

    Toutes les entrees d'ETAT viennent du jeu de donnees.
    UNE SEULE entree ne vient pas des donnees, et c'est l'action.
    """
    etats, actions, recompenses, etats_suivants = lot

    with torch.no_grad():
        # s' vient de D : il est DANS la distribution. Aucun probleme ici.
        # a' vient de la politique APPRISE : il peut etre n'importe ou.
        actions_suivantes = acteur(etats_suivants)

        # Et c'est ici, et seulement ici, que l'erreur entre :
        # q_cible est interrogee en une action sur laquelle elle
        # n'a jamais ete entrainee, et personne ne peut la dementir.
        q_suivant = q_cible(etats_suivants, actions_suivantes)

        cible = recompenses + gamma * q_suivant

    return cible
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s_{t+1}\) | état suivant, **tiré de \(\mathcal{D}\)**, donc dans la distribution | `etats_suivants` |
| \(a_{t+1} \sim \pi\) | action suivante, **produite par la politique apprise** | `actions_suivantes` |
| \(Q^\pi(s_{t+1}, a_{t+1})\) | la seule quantité hors distribution du calcul | `q_suivant` |
| \(r + \gamma Q^\pi(s',a')\) | la cible, fausse dès que la ligne précédente l'est | `cible` |
| \(\E_{a\sim\pi}[Q^\pi(s,a)]\) | ce que l'acteur maximise, donc ce qu'il cherche | dans la perte de l'acteur |

Comparez ligne à ligne avec le code de la semaine 9 : **c'est le même**. Rien n'a changé dans le calcul de la cible. La seule chose qui a changé est qu'aucune transition nouvelle n'entrera jamais dans `lot`.

---

## La courbe de désapprentissage, et le fait qui devrait vous inquiéter

Il reste à montrer que tout cela se produit réellement, et la mesure existe. Elle porte un nom, le **désapprentissage** (*unlearning*), et elle est, de mon point de vue, la plus troublante de ce cours.

Le dispositif : un acteur-critique à entropie maximale, de ceux de la semaine 9, entraîné **hors ligne** sur un jeu de données du guépard simulé. En abscisse, le nombre de **pas de gradient appliqués à la valeur d'action**, de zéro à mille. En ordonnée, le **retour réellement obtenu** par la politique gloutonne, mesuré en la déployant.

Et voici la courbe. Le retour **monte d'abord**, ce qui est normal et encourageant : l'agent apprend quelque chose. Puis il **s'effondre**, nettement, et il ne remonte pas. Pendant ce temps, le panneau voisin trace le logarithme de la valeur d'action estimée, et celui-là **monte** sans cesse. L'agent est donc de plus en plus convaincu de sa qualité pendant qu'il devient de plus en plus mauvais.

{{% comment %}}SOURCE: OFFLINE p.19{{% /comment %}}

Cela ressemble à du surapprentissage, et toute votre expérience d'apprentissage profond vous souffle le remède habituel : plus de données.

> [!WARNING]
 **Et voici le fait qui doit vous empêcher de dormir : cet effet persiste quand on augmente la taille du jeu de données.** Les courbes sont tracées pour mille, dix mille, cent mille et un **million** de transitions, soit un facteur mille entre la première et la dernière, et le phénomène est toujours là. Ce n'est donc **pas** du surapprentissage statistique : un surapprentissage s'atténue avec les données, par définition. Ce qui se passe ici est d'une autre nature. Le problème n'est pas qu'il manque des exemples dans les régions couvertes ; le problème est que la politique apprise va chercher des régions que **aucune quantité de données issues de \(\pi_\beta\) ne couvrira jamais**, parce que \(\pi_\beta\) n'y va pas. Mille fois plus de données de la même politique, ce sont mille fois plus de données **au même endroit**. Relisez l'exemple des dossiers de patients, en section 13.13 : c'est le même énoncé, et le voilà mesuré.

---

## Trois façons de nommer le même obstacle, et un lien que ce cours tire lui-même

Le même phénomène se décrit de trois façons, et chacune suggère un remède différent. Elles valent d'être mises côte à côte, parce que c'est le plan de la section 13.15.

**Première formulation : erreur d'extrapolation** (*extrapolation error*). Le problème est qu'on évalue la valeur d'action en des actions absentes du jeu. Remède suggéré : restreindre l'évaluation aux actions **présentes dans les données**.

**Deuxième formulation : décalage de distribution.** Le problème est que la loi des actions a changé. Remède suggéré, et il est **moins restrictif** que le précédent : limiter l'**ampleur** du décalage, sans confiner la politique aux seules actions déjà vues.

**Troisième formulation : une famille de contraintes.** Diverses contraintes, de formes variées, fonctionnent, ce qui indique que ce qui compte est le fait de contraindre plus que la forme précise de la contrainte.

{{% comment %}}SOURCE: OFFLINE p.19{{% /comment %}}

> [!TIP]
 **Et un lien que ce cours tire de lui-même, parce que personne ne l'a tiré pour nous : c'est la triade fatale de la semaine 5, poussée au bout.** Souvenez-vous des trois jambes : approximation de fonction, amorçage, et apprentissage hors politique. Les trois sont présentes ici. L'approximation de fonction, c'est le réseau. L'amorçage, c'est la cible de Bellman qui s'appuie sur sa propre estimation. Et le hors politique est poussé à sa **limite logique** : non seulement les données viennent d'une autre politique, mais la politique apprise peut s'en écarter **sans aucune contrainte et sans aucun retour**. La semaine 5 vous a montré la divergence sous sa forme la plus douce, celle qu'un réseau cible et un tampon suffisent à contenir. Cette section vous la montre sans aucun garde-fou possible. Je précise que ce rapprochement est le mien : il n'est pas de l'ordre de la définition, et vous pouvez le contester. Mais il tient, et il explique pourquoi le remède de la semaine 5, geler la cible, ne suffit pas ici : une cible gelée reste fausse si elle est évaluée là où rien ne l'a jamais entraînée.

---
