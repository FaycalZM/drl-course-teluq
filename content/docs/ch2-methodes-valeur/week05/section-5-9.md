---
title: "5.9 Ce que ça coûte, et quand ça ne converge pas"
weight: 10
---

## La boucle, et l'ordre de ses six gestes

Il nous reste à assembler. La boucle principale fait six choses, et leur **ordre** compte autant que leur contenu.

1. Mettre à jour \(\varepsilon\) selon le calendrier, en fonction du numéro de trame.
2. Faire **un** pas dans l'environnement, par l'intermédiaire de l'agent, et ranger la transition.
3. Si un épisode vient de se terminer, afficher les compteurs et sauvegarder le modèle si la moyenne établit un record.
4. **Ne rien apprendre** tant que le tampon ne contient pas `REPLAY_START_SIZE` transitions.
5. Synchroniser le réseau cible tous les `SYNC_TARGET_FRAMES` pas.
6. Puis seulement : remettre les gradients à zéro, tirer un lot, calculer la perte, rétropropager, faire un pas d'optimiseur.

{{% comment %}}SOURCE: LAPAN ch.6 p.194-195{{% /comment %}}

```python
optimiseur = torch.optim.Adam(reseau.parameters(), lr=1e-4)
tampon = TamponDeRejeu(REPLAY_SIZE)
retours, meilleur = [], None

for k in itertools.count():                      # k compte les TRAMES
    eps = epsilon(k)                             # 1. le calendrier
    retour_episode = agent.jouer_un_pas(reseau, tampon, eps)   # 2. UN pas

    if retour_episode is not None:               # 3. un épisode vient de finir
        retours.append(retour_episode)
        moyenne = float(np.mean(retours[-100:]))
        if meilleur is None or moyenne > meilleur:
            torch.save(reseau.state_dict(), "meilleur.dat")
            meilleur = moyenne
        if moyenne > MEAN_REWARD_BOUND:
            print(f"Résolu en {k} trames.")
            break

    if len(tampon) < REPLAY_START_SIZE:          # 4. on remplit, on n'apprend pas
        continue
    if k % SYNC_TARGET_FRAMES == 0:              # 5. theta- <- theta
        reseau_cible.load_state_dict(reseau.state_dict())

    optimiseur.zero_grad()                       # 6. le pas d'apprentissage
    perte = calculer_perte(tampon.echantillonner(BATCH_SIZE),
                           reseau, reseau_cible, GAMMA, peripherique)
    perte.backward()
    optimiseur.step()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(k\) | numéro de trame, l'horloge de tout l'algorithme | `k`, et **non** un numéro d'épisode |
| \(\varepsilon_k\) | taux d'exploration courant | `eps` |
| \(\mathcal{D}\) | le tampon | `tampon` |
| \(\theta^- \leftarrow \theta\) | la synchronisation | `load_state_dict(...)` |
| \(\nabla_\theta \mathcal{L}\) | le gradient du pas | `perte.backward()` |
| \(\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}\) | le pas d'optimiseur | `optimiseur.step()` |
| le critère d'arrêt | moyenne des 100 derniers épisodes | `moyenne > MEAN_REWARD_BOUND` |

Ce fragment est volontairement incomplet : c'est un plan de lecture, et le programme entier vit dans le carnet du laboratoire. Trois remarques, tout de même.

Le compteur est en **trames**, pas en épisodes. C'est la bonne unité : un épisode de Pong dure quelques milliers de trames et sa durée change au fil de l'apprentissage, de sorte qu'une courbe tracée en épisodes ne compare pas des quantités comparables. Tous les hyperparamètres de la section 5.8 sont libellés en trames pour la même raison.

Le critère d'arrêt est une moyenne du **retour**, pas une convergence numérique. On s'arrête quand la moyenne des cent derniers épisodes dépasse 19,0, c'est-à-dire quand l'agent gagne plus de 19 manches sur les 21 d'une partie. Et le modèle est sauvegardé chaque fois que cette moyenne établit un record, ce qui donne gratuitement le meilleur jeu de poids rencontré, et non le dernier.

{{% comment %}}SOURCE: LAPAN ch.6 p.194-195{{% /comment %}}

Enfin, un détail qui surprend et qui mérite son explication. Les deux réseaux, l'entraîné et la cible, partent de poids aléatoires **différents** : la copie profonde intervient avant toute synchronisation. Cela n'a guère d'importance, puisqu'ils sont synchronisés toutes les mille trames, ce qui correspond à peu près à un épisode de Pong : la désynchronisation initiale est effacée avant d'avoir pu nuire.

{{% comment %}}SOURCE: LAPAN ch.6 p.193{{% /comment %}}

---

## Le coût, en trames et en heures

Parlons chiffres, parce que c'est ce qui décide de la forme du laboratoire.

Il faut environ **400 000 trames** pour atteindre un retour moyen de 17, c'est-à-dire pour gagner plus de 80 % des manches. Et il en faut à peu près **autant encore** pour passer de 17 à 19. Donc, en moyenne, de l'ordre d'un **million de trames de jeu** pour un entraînement complet. L'exécution de référence, elle, s'arrête à 755 958 trames.

{{% comment %}}SOURCE: LAPAN ch.6 p.195, p.198{{% /comment %}}

Traduisons en temps. À 250 trames par seconde sur un processeur graphique de jeu haut de gamme de 2017, cela fait environ **une heure**. À 40 trames par seconde sur un processeur central de la même époque, environ **sept heures**. Et ce n'est que Pong : d'autres jeux demandent des centaines de millions de trames et un tampon de rejeu cent fois plus grand.

{{% comment %}}SOURCE: LAPAN ch.6 p.195{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister sur cette ligne, parce qu'elle commande tout le laboratoire de la semaine.** Une heure sur une bonne carte graphique, pour **le plus simple** des jeux Atari, avec un algorithme dont les hyperparamètres ont déjà été réglés pour lui. C'est l'ordre de grandeur réel de l'apprentissage par renforcement profond, et c'est pourquoi vous n'entraînerez pas Pong dans ce cours : une session Colab ne vous donnera pas une à trois heures de calcul fiable, et ce n'est de toute façon pas là que se trouve l'apprentissage. Vous entraînerez un DQN complet sur CartPole, en quelques minutes, et vous **évaluerez** un agent de Pong à partir de poids fournis. Le premier vous apprend à écrire la méthode, le second vous montre ce qu'elle produit. Ce découpage n'est pas une concession, c'est le bon usage du temps de calcul dont vous disposez.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

La chronologie d'une exécution mérite d'être connue, parce que ses deux premières phases ressemblent beaucoup à une panne.

Pendant que le tampon se remplit, la vitesse est d'environ **1 400 trames par seconde** : c'est normal, il n'y a aucun apprentissage, le réseau n'est pas sollicité pour autre chose que le choix des actions. Dès que l'entraînement démarre, elle tombe à environ **260 trames par seconde**. Ensuite, pendant les soixante-dix premières parties environ, le retour reste collé à \(-21\) ou \(-20\) : l'agent perd toutes les manches. Puis la récompense moyenne commence à croître, et cela se produit en général autour de \(\varepsilon = 0{,}5\). Et la partie 380 est la dernière.

{{% comment %}}SOURCE: LAPAN ch.6 p.196-198{{% /comment %}}

Un détail de vitesse que je signale parce qu'il paraît absurde la première fois : la cadence **diminue** encore à mesure que \(\varepsilon\) diminue. La raison est mécanique : quand \(\varepsilon\) est élevé, la plupart des actions sont tirées au hasard et ne coûtent rien ; à mesure que \(\varepsilon\) approche de zéro, il faut un passage avant dans le réseau à presque chaque pas pour obtenir les valeurs d'action et choisir la meilleure. Un agent qui explore est un agent qui ne calcule pas.

{{% comment %}}SOURCE: LAPAN ch.6 p.197{{% /comment %}}

---

## Une exécution sur dix ne converge pas, et c'est un résultat

Je garde pour la fin l'information la plus honnête de la semaine, et je vous demande de la lire comme un résultat et non comme un aveu.

Environ une exécution sur dix ne converge pas du tout. Le symptôme est reconnaissable : un flot ininterrompu de récompenses de \(-21\), c'est-à-dire des défaites complètes, qui se prolonge bien au-delà du moment où une exécution saine a commencé à progresser. D'où la consigne pratique, et elle est à retenir : si votre entraînement ne montre aucune dynamique positive pendant les 100 000 à 200 000 premières itérations, relancez-le au lieu de le laisser tourner.

{{% comment %}}SOURCE: LAPAN ch.6 p.198{{% /comment %}}

Une exécution sur dix. Même code, mêmes hyperparamètres, même environnement, et rien n'apprend. Posez maintenant cette observation à côté de la section 5.6, et regardez comme les deux moitiés s'emboîtent.

> [!IMPORTANT]
 **Je dois insister : ce taux d'échec est exactement le régime que la théorie prévoit, et c'est pour cela que la section 5.6 est dans cette semaine.** Notre agent possède les trois ingrédients de la triade fatale, nous l'avons audité ligne par ligne. Pour cette configuration, il n'existe **aucune preuve de convergence**, et il existe des contre-exemples de divergence pour Q-learning. La seule chose que l'on sache dire est qu'avec une politique de comportement \(\varepsilon\)-gloutonne, la divergence n'a jamais été observée, sans qu'aucune analyse théorique ne l'explique. Une exécution sur dix qui n'apprend rien n'est donc pas la trace d'un bogue dans votre code : c'est un algorithme sans garantie, employé dans le régime où il n'en a pas. Si vous passez trois jours à chercher la faute dans votre perte, vous chercherez quelque chose qui n'y est pas.

{{% comment %}}SOURCE: SB ch.11 p.285{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.6 p.198{{% /comment %}}

Le cours a déjà fait ce geste, en semaine 3, avec le plateau de la méthode d'entropie croisée sur FrozenLake : un résultat négatif, expliqué, vaut mieux qu'un succès réglé aux petits oignons. La différence, cette fois, est que nous disposons d'une **théorie** qui prédisait l'échec avant de l'observer. C'est rare et c'est précieux : gardez en mémoire que la section 5.6 a été écrite avant la section 5.9, et pas après.

---

## Ce qui ne va pas dans notre DQN, et qui est la semaine 6

Nous avons un agent qui fonctionne. Je veux refermer la semaine en listant, sans les résoudre, les défauts que l'on sait lui trouver. Chacun a été réparé, chaque réparation a un nom, et toutes sont au programme de la semaine prochaine. Nommer un problème n'est pas le résoudre : cette liste est un **état des lieux**, pas une solution.

1. **Le \(\max\) de la cible surestime les valeurs.** Prendre le maximum d'un ensemble d'estimations bruitées ne donne pas une estimation du maximum : cela donne quelque chose de systématiquement trop grand, parce que le maximum attrape le bruit positif. Notre cible fait exactement cela, à chaque transition de chaque lot.
2. **Le tirage dans le tampon est uniforme.** Une transition surprenante et une transition parfaitement banale ont la même chance d'être rejouée. Nous dépensons donc l'essentiel de nos pas d'apprentissage sur des données dont le réseau n'a plus rien à apprendre.
3. **Le réseau doit apprendre une valeur par couple état-action, séparément.** Rien, dans son architecture, ne lui permet de dire « cet état est mauvais quoi que je fasse » une fois pour toutes, puis de ne plus apprendre que les écarts entre actions.
4. **L'exploration est pilotée à la main.** Le calendrier de \(\varepsilon\) est le même dans tous les états, du premier au dernier pas, alors qu'un agent devrait explorer davantage là où il sait moins.
5. **La cible est à un pas.** Une récompense obtenue à la trame 1 000 ne remonte vers la trame 999 qu'à la mise à jour suivante, puis vers 998 à celle d'après : l'information se propage d'un pas par pas d'apprentissage.

Cinq défauts, cinq réparations, et la semaine 6 les empile l'une sur l'autre jusqu'à obtenir un agent qui porte un nom d'arc-en-ciel. Gardez cette liste : je vous demanderai de la relire, point par point, en ouverture de la semaine prochaine.

---
