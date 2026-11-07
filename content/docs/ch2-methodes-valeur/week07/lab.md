---
title: "Laboratoire"
weight: 15
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté directement. Mais lisez ce paragraphe avant de commencer, parce qu'il change la façon de travailler. Le **volet A est la matière du jalon 2**, qui est remis à la fin de cette même semaine. Ce que vous mesurez ici, vous le rendrez dans quelques jours, mis en forme. Nommez donc vos fichiers, vos graines et vos exécutions comme si vous deviez les relire, parce que vous devrez les relire.

Les deux volets ne se ressemblent pas, exactement comme les deux moitiés de la semaine. Le volet A mesure et accélère ; le volet B écrit un environnement et le teste **sans rien entraîner**.

**Budget de calcul, et il est fixé explicitement.** Tout le volet A tourne sur `CartPole-v1`, et c'est la même décision qu'en semaine 6. Les durées que je vous ai données dans cette semaine, de 30 à 52 minutes par exécution, viennent de Pong sur une carte dédiée ; multipliées par le nombre de variantes et par le nombre de graines, elles donnent une dizaine d'heures de calcul, ce qui est hors de portée d'une semaine sur un processeur graphique partagé. Sur CartPole, une exécution se compte en minutes, et vous pourrez donc faire la seule chose qui compte pour ce laboratoire : **répéter**. Le volet B, lui, ne demande presque aucun calcul, et le jeu de données est **fourni** : vous n'avez aucune donnée de marché à aller chercher.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

> [!WARNING]
 **Un avertissement sur les chiffres, et il est le même que la semaine dernière.** Je ne vous donne, dans aucun volet, le débit ou la durée que vous devez obtenir. Ce n'est pas un oubli. Tous les nombres de cette semaine, les 229 trames par seconde, les 52 minutes, les +72,5 %, viennent d'une machine précise sur un jeu précis. Ils ne prédisent **rien** de ce que votre code fera sur CartPole dans un carnet partagé. Ce que j'attends de vous est donc **relatif** : des rapports, un classement, un signe, et un intervalle autour de chacun. Si vos nombres absolus ne ressemblent pas aux miens, c'est normal. Si vos **rapports** sont stables sur vos graines, vous avez un résultat.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

---

## Volet A : mesurer, puis changer une seule chose

**Objectif.** Produire un tableau d'accélération de la forme du Tableau 7-1, sur **votre** code et **votre** matériel, avec des intervalles.

**Étape 0, et elle précède toute exécution.** Écrivez dans votre carnet, avant de lancer quoi que ce soit, trois choses : le **critère d'arrêt** (par exemple, récompense moyenne sur les 100 derniers épisodes atteignant 475 sur `CartPole-v1`), les **deux indicateurs** que vous allez relever, et la **liste de vos graines**. Cet ordre n'est pas décoratif. Un critère d'arrêt choisi après avoir vu les courbes n'est plus un critère, c'est une justification.

**Étape 1, la version de référence.** Partez de votre socle de la semaine 6, sans le modifier. Mesurez-le sur \(k\) graines, avec \(k \ge 3\) et 5 de préférence. Rapportez pour chacun des deux indicateurs la moyenne **et** l'intervalle, avec le code de la section 7.2. Vérifiez en même temps que la version de référence **apprend** : c'est la règle « correction avant vitesse », et elle s'applique au livrable lui-même.

**Étape 2, une modification à la fois.** Appliquez **une seule** modification, remesurez sur **les mêmes graines**, inscrivez la ligne dans votre tableau, puis passez à la suivante. Trois modifications tiennent confortablement dans ce laboratoire :

1. **`torch.no_grad()` sur les deux usages sans gradient** du réseau, c'est-à-dire la cible et le choix de l'action. Si votre code de la semaine 6 les avait déjà, mesurez l'inverse : retirez-les, et voyez ce que vous obtenez.
2. **\(N\) environnements vectorisés**, avec la taille de lot mise à l'échelle et les deux constantes recalibrées (le calendrier de \(\varepsilon\) et la fenêtre du compteur de débit). Balayez \(N\) de 1 à 4 et tracez les deux indicateurs en fonction de \(N\) : c'est la plus belle courbe du laboratoire, parce qu'elle ne va pas dans le même sens pour les deux.
3. **La couche que personne ne profile.** Sur CartPole il n'y a pas de pile Atari à alléger, et c'est une bonne occasion d'apprendre à chercher soi-même : chronométrez séparément, sur mille pas, le temps passé dans l'environnement, dans la préparation des tenseurs, dans le passage avant, et dans l'optimiseur. Puis attaquez la plus grosse part. Dans la plupart des implémentations écrites en semaine 5, vous trouverez une conversion de tableau en tenseur refaite à chaque pas, ou un aller-retour inutile entre processeur central et processeur graphique.

**Étape 3, le tableau et sa lecture.** Rendez le tableau avec les colonnes du Tableau 7-1, augmentées d'une colonne « graines » et d'une colonne d'intervalle. Puis répondez par écrit à **une** question : avez-vous observé un cas où le classement en débit et le classement en temps se contredisent ? Si oui, lequel et pourquoi. Si non, dites-le explicitement : c'est aussi une réponse.

**Attendu.** Le tableau, les deux courbes en fonction de \(N\), vos intervalles, votre matériel, et un paragraphe de lecture.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-07.ipynb" label="Volet A : profiler et accélérer votre socle, avec graines et intervalles" >}}

---

## Volet B : écrire l'environnement, et le tester sans l'entraîner

**Objectif.** Écrire l'environnement de négociation de la section 7.10 **de zéro**, et le vérifier par des assertions. Aucun entraînement dans ce volet.

**Protocole.** Vous écrivez vous-même la classe d'état et l'habillage Gym, en vous appuyant sur les fragments de la section 7.10 et sur votre propre lecture des trois décisions de la section 7.8. Vous ne recopiez aucun code existant d'agent de négociation : l'écriture **est** l'exercice, et c'est aussi la règle de ce cours pour tout code de laboratoire.

**Les quatre assertions à écrire, et elles sont le cœur du volet.** Chacune tient en trois lignes et chacune attrape une classe d'erreur réelle.

1. **Le coût du voyage.** Un achat suivi d'une clôture, **sans aucun mouvement de prix**, rend exactement \(-2\kappa\). Si vous obtenez \(-\kappa\), vous avez oublié une jambe ; si vous obtenez 0, votre commission n'est pas branchée.
2. **Le rendement pur.** Avec \(\kappa = 0\), un achat au prix \(c_0\) et une clôture au prix \(c_1\) sous le schéma A rendent exactement \(100\,(c_1/c_0 - 1)\). Construisez une série de prix artificielle à la main : deux ou trois barres suffisent, et c'est bien plus facile à déboguer qu'un vrai fichier.
3. **Les deux schémas ne coïncident pas.** Appliquez les deux schémas à la **même** trajectoire et montrez qu'ils s'accordent au premier ordre et diffèrent au second. Le cas à deux barres à \(+10\,\%\) de la section 7.8, qui donne 20 points contre 21, est le test minimal ; faites-en une version paramétrée et tracez l'écart en fonction de la durée de détention. C'est la **preuve** que les deux schémas ne définissent pas le même objectif, et vous l'aurez produite vous-même.
4. **La forme de l'observation.** Elle a exactement \(3b + 2\) composantes, et sa **dernière** composante vaut 0 chaque fois qu'aucune position n'est détenue. Vérifiez les deux, et vérifiez-les sur plusieurs valeurs de \(b\).

{{% comment %}}SOURCE: LAPAN ch.10 p.313-315{{% /comment %}}

**Deux extensions facultatives, et je les recommande toutes les deux.**

L'**affichage**, qui n'est pas implémenté : tracez la série de prix de l'épisode et marquez dessus les achats et les clôtures. Dix lignes de Matplotlib, et vous obtiendrez la vue la plus informative de tout le volet.

La **stratégie d'achat-conservation**, qui est la comparaison manquante de la section 7.12 : achetez à la première barre, ne faites rien, vendez à la dernière, payez deux commissions, et rapportez le profit. Vous aurez alors le point de comparaison qu'un lecteur attend, et vous pourrez enfin dire si un agent qui finit à \(+10\,\%\) a créé ou détruit de la valeur.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-07.ipynb" label="Volet B : écrire l'environnement de négociation et vérifier sa récompense par des assertions" >}}

> [!TIP]
 **Mon message pour ce laboratoire.** Les deux volets vous enseignent le même geste par deux chemins opposés. Au volet A, vous mesurez avant de changer. Au volet B, vous testez avant d'entraîner. Dans les deux cas, vous refusez de lancer la grosse machine avant d'avoir établi un point de référence vérifiable. C'est la discipline la plus rentable de tout le métier, et c'est aussi la plus difficile à tenir quand on est impatient de voir une courbe monter. Je vous le dis sans détour : les étudiants qui prennent cette habitude cette semaine sont ceux qui termineront le cours avec des résultats défendables.

---
