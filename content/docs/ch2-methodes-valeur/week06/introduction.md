---
title: "Introduction"
weight: 1
---

## Cinq défauts nommés la semaine dernière, cinq réparations cette semaine

Bonjour à toutes et à tous ! La semaine 5 s'est terminée sur une liste, et je vous avais demandé de la garder. La voici, dans l'ordre exact où je l'avais écrite.

1. Le \(\max\) de la cible surestime les valeurs.
2. Le tirage dans le tampon de rejeu est uniforme.
3. Le réseau ne peut pas dire « cet état est mauvais quoi que je fasse ».
4. L'exploration est pilotée par un calendrier écrit à la main.
5. La cible est à un pas.

{{% comment %}}SOURCE: raw-content/week-05.md §5.9{{% /comment %}}

Cette semaine répare les cinq. Pas quatre, pas trois : les cinq, chacune par une méthode qui porte un nom, qui a été publiée, mesurée, et que vous allez implémenter. Et à la fin, nous les empilerons, parce qu'elles s'empilent : la combinaison des six améliorations les plus importantes du réseau Q profond a suffi, en 2017, à établir l'état de l'art sur Atari, sans qu'aucune idée nouvelle ne soit ajoutée. Elle porte un nom d'arc-en-ciel, Rainbow, et c'est le dernier mot de la semaine.

{{% comment %}}SOURCE: LAPAN ch.8 p.226{{% /comment %}}

Voici le tableau sur lequel toute la semaine est bâtie. Lisez-le maintenant, et revenez-y à chaque section : la colonne de gauche est la liste de la semaine 5, la colonne de droite est le programme de celle-ci.

| Défaut de la semaine 5 | La réparation | Ce qu'elle change dans le code |
| --- | --- | --- |
| nº1 le \(\max\) surestime | **double DQN** | trois lignes dans la perte |
| nº2 le tirage est uniforme | **tampon de rejeu priorisé** | le tampon, et la perte qui le nourrit |
| nº3 une seule tête de sortie | **architecture duale** | la classe du réseau, et rien d'autre |
| nº4 le calendrier \(\varepsilon\) à la main | **réseaux bruités** | deux couches échangées, et du code supprimé |
| nº5 la cible à un pas | **DQN à n étapes** | deux lignes, et la seconde est un piège |

{{% comment %}}SOURCE: LAPAN ch.8 p.241, p.246, p.250, p.257, p.264{{% /comment %}}

---

## Deux moitiés, et elles ne font pas le même métier

La semaine a une forme inhabituelle et je préfère vous l'annoncer, parce que vous allez la sentir au passage de la section 6.5 à la section 6.6.

La première moitié ne vous apprend aucune méthode. Elle pose une question d'ingénierie : après cinq semaines passées à réécrire la même boucle d'entraînement, **quels sont les bons objets** ? Pour y répondre, nous allons lire une bibliothèque spécialisée, PTAN, et la lire comme on lit un texte, pas comme on apprend une interface. C'est la seule semaine du cours où elle apparaîtra. Les laboratoires du cours, de la semaine 1 à la semaine 15, restent écrits en PyTorch et Gymnasium simples, et c'est un choix assumé dont je vous donnerai la raison en section 6.1.

La seconde moitié est un catalogue de réparations, et elle a besoin de la première. Une réparation qui tient en une ligne ne tient en une ligne que si les objets autour d'elle sont bien découpés : c'est parce que la source d'expérience de la section 6.3 livre déjà des transitions prêtes à l'emploi que le DQN à n étapes de la section 6.6 se réduit à deux paramètres. Et c'est parce qu'un socle de code unique existe que les quatre variantes du laboratoire sont **comparables** entre elles. Quatre scripts écrits séparément ne se comparent pas.

> [!IMPORTANT]
 **Je dois insister sur un réordonnancement, et je ne veux pas qu'il passe inaperçu.** Le tableau ci-dessus donne les défauts dans l'ordre de la semaine 5. Les sections, elles, ne suivent pas cet ordre : nous commençons par le défaut nº5, la cible à un pas, parce que sa réparation est la plus courte du lot et qu'elle repose directement sur la transition premier-dernier que vous aurez rencontrée en 6.3. Puis nº1, nº3, nº4 et nº2, dans un ordre qui va du plus simple au plus intrusif : une perte modifiée, puis une architecture, puis des couches, puis le tampon lui-même. Chaque section rappelle, dans son titre, le défaut auquel elle répond. Vous pouvez donc les lire dans l'ordre de la semaine 5 si vous préférez : rien n'y perd son sens.

---

## Objectifs de la semaine

À la fin de cette semaine, vous saurez :

- Nommer les cinq défauts du réseau Q profond de la semaine 5 et, pour chacun, la méthode qui lui répond.
- Citer les cinq abstractions d'une bibliothèque d'apprentissage par renforcement et dire, pour chacune, ce qu'elle retire des mains de celui qui écrit le code.
- Dire ce que contient une **transition premier-dernier** et pourquoi elle rend le passage à \(n\) étapes immédiat.
- Distinguer une synchronisation par copie d'une **synchronisation douce**, et convertir son coefficient d'une convention à l'autre.
- Justifier qu'une étude d'ablation exige un socle de code unique, et dire ce qu'une comparaison perd sans lui.
- Écrire la cible à \(n\) étapes et désigner l'approximation exacte qui la sépare de la forme à un pas.
- Dire pourquoi \(n\) reste petit, et quelle réparation de la semaine 5 le dépliage de Bellman abîme.
- Montrer le **biais de maximisation** sur un exemple à deux états, et expliquer pourquoi deux estimations séparées le réduisent.
- Écrire la cible du **double DQN** en désignant le réseau qui fournit l'indice et celui qui fournit la valeur.
- Écrire la décomposition \(Q = V + A\) avec sa **contrainte de moyenne nulle**, et dire précisément ce qui se passe sans elle.
- Pointer, dans un fragment de PyTorch, la ligne qui réalise la moyenne sur les actions de cette contrainte.
- Expliquer ce qu'un **réseau bruité** apprend, et ce qu'il n'apprend pas.
- Dire ce que `.eval()` fait à un réseau bruité, et pourquoi cela change le sens d'une ligne de la semaine 5.
- Écrire la probabilité de tirage d'un **tampon de rejeu priorisé** avec son exposant \(\alpha_{\mathrm{PER}}\), et le poids de correction avec son exposant \(\beta\).
- Dire ce que \(\beta = 1\) restaure, et pourquoi on ne commence pas à cette valeur.
- Expliquer pourquoi la perte quadratique doit être écrite à la main dès qu'un tampon priorisé est en place.
- Énoncer quelles réparations la combinaison retient, lesquelles elle laisse de côté, et ce que l'empilement coûte en débit de trames.
- Énoncer l'équation de Bellman distributionnelle et dire ce que signifie une égalité **en distribution**.
- Mener une étude d'ablation sur CartPole à partir d'un socle commun, et mesurer la surestimation sur un ensemble d'états témoins.

---

## Prérequis et outils

De la semaine 5, tout : le réseau Q profond, le tampon de rejeu, le réseau cible, le masque terminal, `gather`, le détachement du graphe et la méthode semi-gradient. Cette semaine ne réexplique rien de cela, elle le modifie. De la semaine 4 : Q-learning, la méthode \(\varepsilon\)-gloutonne, l'amorçage, et surtout le \(\max\) de l'équation d'optimalité de Bellman, qui est l'accusé de la section 6.7. De la semaine 3 : l'axe sur politique contre hors politique, et l'**échantillonnage préférentiel** (*importance sampling*), que la semaine 5 avait délibérément laissé de côté et que la section 6.10 vient chercher. De la semaine 2 : `nn.Module`, `nn.Parameter`, les tampons enregistrés d'un module, la distinction entre mode entraînement et mode évaluation, et la perte quadratique.

| Outil | Usage dans la semaine |
| --- | --- |
| **Google Colab** | exécution des carnets ; l'accélérateur graphique aide mais n'est pas indispensable sur CartPole |
| **Gymnasium** | `CartPole-v1` pour tout le laboratoire |
| **PyTorch** | les quatre variantes, et une couche écrite de zéro en section 6.9 |
| **PTAN 0.8** | **objet d'étude de la première moitié**, installé une fois, jamais réutilisé ensuite |
| **NumPy** | le tampon priorisé et la mise en lot |
| **Matplotlib** | les courbes de l'ablation, et les deux diagnostics du volet D |
| **Page « Notation » du cours** | décisive cette semaine pour les trois sens de \(\alpha\) |
| **Page « Glossaire » du cours** | vingt et un termes nouveaux y entrent cette semaine |

{{% comment %}}SOURCE: LAPAN ch.7 p.203{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

Avant la première équation, un point de notation, et il est obligatoire cette semaine plus qu'aucune autre.

> [!IMPORTANT]
 **Je dois insister : la lettre \(\alpha\) va désigner trois choses différentes dans cette semaine, et le cours tranche une fois pour toutes.** Premièrement, \(\alpha\) tout court est le **pas d'apprentissage**, comme depuis la semaine 4, et il ne désignera jamais rien d'autre dans ce cours. Deuxièmement, l'exposant qui règle l'agressivité du tampon priorisé en section 6.10 s'écrit \(\alpha_{\mathrm{PER}}\), **toujours avec son indice**, parce que les deux apparaissent dans le même bloc d'hyperparamètres et qu'une confusion y est fatale. Troisièmement, le coefficient de mélange de la synchronisation douce en section 6.4 s'écrit \(\alpha_{\mathrm{sync}}\). Retenez la règle sous cette forme : **\(\alpha\) nu est le pas d'apprentissage ; tout autre \(\alpha\) porte un indice.**

{{% comment %}}SOURCE: notation.md §5{{% /comment %}}

> [!NOTE]
 **Notez bien ce point d'organisation.** La semaine 6 ne porte **aucun jalon** : le prochain est en semaine 7 et il clôt le module 2. Mais regardez ce qu'il demande, parce que cela change la façon de travailler cette semaine : un réseau Q profond **plus au moins deux extensions**, avec des courbes comparées. Le laboratoire de cette semaine produit exactement cela. Autrement dit, le volet évalué de la semaine 6 n'est pas un exercice qui s'arrête à sa remise : c'est la moitié du jalon 2. Faites-le proprement, nommez vos fichiers proprement, et gardez vos courbes.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---
