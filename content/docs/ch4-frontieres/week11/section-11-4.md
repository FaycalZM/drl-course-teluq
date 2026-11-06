---
title: "11.4 Ce que la prime fait au problème"
weight: 5
---

## Une récompense fabriquée est quand même une récompense

Cette section est courte, elle ne contient aucune méthode nouvelle, et c'est celle que je vous demande de lire deux fois. Elle pose une question que les trois familles de la section 11.3 ne posent pas, et la réponse est à moi : **je la signe et je l'assume**.

Voici d'abord ce que notre code fait, écrit sans détour. L'enveloppe de la section 11.3 renvoie, à chaque pas :

$$
R_t \;=\; R^e_t + R^i_t \;=\; R^e_t + \frac{c}{\sqrt{\tilde N(S_t)}}
$$

{{% comment %}}SOURCE: LAPAN ch.18 p.560{{% /comment %}}

Une note de lecture avant d'aller plus loin, parce que les deux écritures circulent et qu'elles se ressemblent dangereusement. Ce cours place le coefficient **dans** la récompense intrinsèque, d'où la somme simple ci-dessus. Vous rencontrerez aussi la forme \(R_t = R^e_t + c\,R^i_t\), où \(R^i_t\) désigne alors la prime **non pondérée**, c'est-à-dire \(1/\sqrt{\tilde N(S_t)}\) toute seule. Les deux disent exactement la même chose, à une condition et une seule : que \(c\) apparaisse **une fois**.

Le membre de gauche est ce que l'agent reçoit. Il n'y a pas deux récompenses dans la boucle, il y en a **une**, et c'est une somme. Rien, en aval de l'enveloppe, ne peut distinguer les deux termes : ni le tampon de rejeu, ni le calcul de l'avantage, ni le critique, ni la perte. La transition stockée porte un nombre, et ce nombre est le total.

Et maintenant la conséquence, qui est le contenu de cette section :

> [!IMPORTANT]
 **Ceci est une affirmation du cours, et je la prends à mon compte : en ajoutant la prime dans l'enveloppe, nous avons changé le problème.** Un processus de décision markovien est défini par ses états, ses actions, sa dynamique **et sa fonction de récompense**. Modifier la récompense, c'est définir un **autre** processus de décision markovien. Nos méthodes font donc exactement ce que nous leur demandons : elles cherchent la politique optimale, mais de ce nouveau problème. Or la politique optimale du problème modifié n'a **aucune raison** d'être la politique optimale du problème d'origine, et ce n'est pas une subtilité théorique : une prime assez grande rend préférable une visite éternelle d'états neufs à toute tentative de terminer la tâche. L'agent qui en résulte n'est pas défectueux, il est optimal pour la récompense que nous lui avons effectivement donnée.

Je formule la même chose en une phrase à retenir, parce qu'elle vous servira bien au-delà de cette semaine : **une récompense que l'agent fabrique est quand même une récompense.** Elle entre dans l'objectif au même titre que celle de l'environnement, et l'optimisation ne fait aucune différence entre les deux.

---

## Les deux têtes de valeur, et ce que leur abandon coûte vraiment

Il existe une façon de faire qui évite cela, et elle est connue : on n'additionne pas les deux récompenses. On garde **deux flux séparés**, et l'on entraîne **deux têtes de valeur**, l'une qui prédit la composante extrinsèque et l'autre la composante intrinsèque. La prime continue d'influencer le comportement, par la voie du gradient de politique, mais elle n'entre jamais dans l'estimation de la valeur **extrinsèque**, qui reste donc une estimation du problème réel.

La raison habituellement donnée pour s'en passer est qu'une simple enveloppe **minimise le nombre de modifications dans le code**. C'est vrai, c'est même un argument sérieux quand on veut mesurer cinq variantes d'exploration dans un temps fini, et je l'ai suivi dans tous les fragments de la section 11.3. Mais ce n'est pas le prix complet, et c'est le silence que cette section vient combler : ce qu'on abandonne avec les deux têtes, ce n'est pas de la propreté, c'est la **séparation entre le problème que l'on résout et l'incitation que l'on a ajoutée pour pouvoir le résoudre**.

{{% comment %}}SOURCE: LAPAN ch.18 p.565 (image){{% /comment %}}

Voici où se situe la bifurcation, en code. Une seule ligne change, et elle change le problème.

```python
    def step(self, action):
        obs, recompense, termine, tronque, info = self.env.step(action)
        prime = self.c / np.sqrt(self.compteur[self._hacher(obs)])

        # ROUTE 1 (sections 11.3 et 11.6) : on additionne. Une recompense,
        # un MDP modifie, et aucun moyen de revenir en arriere en aval.
        # return obs, recompense + prime, termine, tronque, info

        # ROUTE 2 : on NE touche pas a la recompense de la tache. Les deux
        # flux restent separes, et c'est a la boucle d'apprentissage de les
        # traiter : deux tetes de valeur, deux cibles, un seul gradient de
        # politique. Ce cours ne met PAS cette boucle en oeuvre.
        info["prime"] = prime
        return obs, recompense, termine, tronque, info
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(R^e_t\) | récompense de la tâche, intacte sur la route 2 | `recompense` |
| \(R^i_t\) | prime, transportée hors de la récompense | `info["prime"]` |
| \(R_t = R^e_t + R^i_t\) | la somme, qui définit le problème modifié | route 1 seulement |
| deux têtes de valeur | deux estimations séparées, extrinsèque et intrinsèque | non implémentées dans ce cours |

Je suis explicite sur ce que ce fragment est et n'est pas. Il montre **où** la séparation se fait, c'est-à-dire dans l'enveloppe, et il s'arrête là : la boucle d'apprentissage à deux têtes n'est pas écrite dans ce cours, et je ne vais pas vous donner dix lignes plausibles qui vous laisseraient croire le contraire. Ce que je vous demande de savoir, c'est que la route 1 est un **choix**, que ce choix a un coût, et que ce coût n'est pas le volume de code.

---

## Pourquoi la prime reste tolérable ici, et pourquoi c'est un accident

Si la route 1 change le problème, pourquoi les mesures de la section 11.6 sont-elles quand même utilisables ? Parce que deux propriétés du dispositif la sauvent, et je veux que vous les voyiez comme des **accidents de ce montage** et non comme des garanties.

**Premier accident : la prime décroît toute seule.** La forme \(1/\sqrt{\tilde N}\) est décroissante en le nombre de visites. Un état fraîchement découvert paie bien ; le même état, visité mille fois, ne paie presque plus. Le problème modifié se rapproche donc du problème d'origine à mesure que l'agent couvre l'espace d'états, et le détour cesse d'être rentable pour l'agent au moment précis où il devient inutile. Remarquez que cela vaut pour le comptage et pour la distillation, dont l'erreur de prédiction décroît aussi là où le prédicteur a appris, mais **pas** pour une prime constante : une prime qui ne décroît pas déforme le problème jusqu'au dernier pas de l'entraînement.

**Second accident : le critère d'arrêt est extrinsèque.** Toutes les exécutions de la section 11.6 sont arrêtées sur un **retour de test moyen**, mesuré sur l'environnement **sans enveloppe**, donc sur la récompense de la tâche seule. Si nous arrêtions l'entraînement sur la récompense totale, nous sélectionnerions la politique qui visite le mieux, et nous appellerions cela un succès.

Retenez la règle qui sort de ces deux points, parce qu'elle est directement applicable : **une prime ajoutée à la récompense est acceptable à deux conditions, qu'elle décroisse et que la sélection finale se fasse sur la récompense de la tâche.** Si l'une des deux manque, vous optimisez autre chose que ce que vous croyez.

---

## La conséquence mesurable : deux courbes qui ne se comparent pas

Cette déformation du problème n'est pas seulement un argument : elle est **visible** dans vos journaux, et elle produit une illusion que je veux vous apprendre à reconnaître.

Lorsque l'environnement d'entraînement est enveloppé par la prime et que l'environnement de test ne l'est pas, les valeurs observées pendant l'entraînement sont **plus hautes** que celles observées en test. Ce n'est pas un problème de généralisation, ce n'est pas du surapprentissage, et ce n'est pas un bogue : les deux courbes mesurent deux grandeurs différentes, dont l'une contient la prime et l'autre non.

{{% comment %}}SOURCE: LAPAN ch.18 p.561 (image){{% /comment %}}

> [!WARNING]
 **La règle de lecture de la semaine, et je l'appliquerai sans exception dans la section 11.6 : seule la courbe d'évaluation est à l'échelle du problème d'origine.** Une courbe d'entraînement obtenue sous enveloppe ne se compare ni à une courbe de test, ni à une courbe d'entraînement d'une autre configuration dont le \(c\) diffère, ni à une courbe de la méthode de référence, qui n'a pas de prime du tout. Dans vos rapports, à partir de cette semaine, je veux que les courbes sous enveloppe soient **étiquetées comme telles**, et que toute comparaison entre méthodes se fasse sur l'évaluation. C'est le prolongement direct de la règle de la semaine 10 sur les chiffres de banc d'essai : un nombre dont on ne sait pas sur quelle récompense il a été mesuré n'est pas une mesure.

Un dernier point, pour éviter une confusion de causes. Il existe un **autre** argument, différent de celui de cette section, contre la modification des récompenses en cours d'entraînement : une méthode de valeur doit **réapprendre** ses valeurs quand la récompense change, ce qui coûte du temps et de la stabilité. Cet argument ne parle pas de l'optimum du problème, il parle du coût d'apprentissage, et il sera le premier des trois motifs du changement de méthode en section 11.6. Les deux reproches sont réels et indépendants : l'un dit que la cible bouge, l'autre dit que la cible n'est pas la bonne.

{{% comment %}}SOURCE: LAPAN ch.18 p.559 (image){{% /comment %}}

---
