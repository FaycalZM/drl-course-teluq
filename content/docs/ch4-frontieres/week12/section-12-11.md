---
title: "12.11 Collaboration imposée, et la non-stationnarité enfin nommée"
weight: 12
---

## Un seul objet de configuration change, et les tigres doivent chasser à deux

Passons à la seconde expérience, et son dispositif est remarquablement économe : **la seule chose qui change est l'objet de configuration de l'environnement**. Aucune ligne de la boucle d'entraînement, aucune ligne du réseau, aucune ligne de la politique.

Le mode s'appelle `double_attack`, et sa règle est unique : un tigre ne peut blesser un cerf que si **deux tigres l'attaquent en même temps**. Une attaque solitaire n'a **aucun effet**, pas même partiel.

{{% comment %}}SOURCE: LAPAN ch.22 p.690 (image){{% /comment %}}

Les mesures d'entraînement, en prose parce qu'il n'y a rien à tracer d'intéressant : après deux heures, la récompense s'améliore encore, le nombre de pas par épisode ne dépasse jamais trois cents, ce qui peut être un plafond interne du simulateur comme la conséquence de l'inanition, et la **perte ne diminue pas**. L'interprétation qui en est donnée est un problème d'hyperparamètres, et je vous la transmets comme une hypothèse plutôt que comme une conclusion, parce que la section 12.5 nous a appris à nous méfier d'une perte dans ce genre de dispositif.

{{% comment %}}SOURCE: LAPAN ch.22 p.691{{% /comment %}}

---

## Des couples apparaissent, et ce que cela prouve exactement

Voici la partie de la semaine où je vais être le plus précis, parce que c'est la partie où l'on se raconte le plus volontiers des histoires.

**Premier énoncé, structurel, et il est certain.** Sous cette configuration, une attaque isolée n'a aucun effet sur un cerf. Donc un tigre seul **ne peut physiquement pas** se nourrir, quelle que soit sa politique, quelle que soit sa chance. Donc **toute** chasse réussie est, par définition de la règle, l'œuvre de deux tigres simultanés. Cette phrase ne demande aucune observation du comportement : elle se déduit de la configuration.

**Deuxième énoncé, comportemental.** Après entraînement, les tigres se déplacent effectivement par deux et attaquent ensemble. C'est rapporté, et je dois vous dire de quoi cette affirmation est tirée : d'un **enregistrement vidéo** d'un épisode. Pas d'une courbe, pas d'un compteur de couples, pas d'une statistique sur mille épisodes. C'est une observation visuelle d'une exécution, et elle n'est ni mesurée ni reproductible en l'état.

{{% comment %}}SOURCE: LAPAN ch.22 p.690-691{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.693{{% /comment %}}

> [!WARNING]
 **La chasse en couple n'est pas la preuve d'un algorithme collaboratif, et c'est la confusion la plus répandue sur ce genre d'expérience.** Ce qui a produit les couples, c'est la **structure de la récompense** : un environnement où manger seul est impossible n'a pas d'autre solution que le couple, et n'importe quelle méthode qui apprend à manger apprendra donc à se mettre en couple. La méthode d'apprentissage, elle, est restée **exactement** celle de la semaine 5 : aucune communication entre agents, aucun terme de coordination dans la perte, aucune valeur jointe, pas même la conscience qu'un autre agent existe autrement que comme une case de plus dans l'observation. Dire « les agents ont appris à collaborer » est donc une phrase à deux lectures : ils ont appris le comportement que l'environnement rendait obligatoire, et ils n'ont rien appris sur la collaboration. Quand vous lirez une annonce de comportement collaboratif émergent, la question à poser est toujours la même : **un agent seul pouvait-il réussir ?** Si la réponse est non, le comportement est dans la conception du problème, pas dans l'algorithme.

---

## Les deux groupes apprennent en même temps, et les courbes perdent leur tendance

Dernière expérience de la semaine, et c'est celle pour laquelle tout ce qui précède a été construit. Jusqu'ici, un seul groupe apprenait : les tigres s'améliorent, les cerfs agissent au hasard, et l'environnement des tigres est donc **stationnaire**. Entraînons maintenant **les deux groupes à la fois**.

Le dispositif : deux agents de valeur, donc deux réseaux, un par groupe, plus aucun filtrage par groupe dans la collecte, et un seul tampon de rejeu dont le lot est séparé en deux au moment de l'entraînement. Du point de vue du code, c'est une petite modification.

{{% comment %}}SOURCE: LAPAN ch.22 p.692{{% /comment %}}

Du point de vue du problème, ce n'est pas une petite modification du tout. Les tigres progressent d'abord, puis **cessent de progresser**. Et les courbes de récompense de test des deux groupes n'ont, l'une comme l'autre, **aucune tendance** : elles montent, elles descendent, elles ne vont nulle part. Les deux groupes sont en compétition et chacun essaie de battre l'autre.

{{% comment %}}SOURCE: LAPAN ch.22 p.692-693{{% /comment %}}

Et au final, ce sont les **cerfs** qui gagnent, pour une raison purement mécanique qui mérite d'être savourée : les deux groupes se déplacent à la **même vitesse**. Un cerf n'a donc pas besoin d'être malin, il a besoin de ne jamais s'arrêter. Il fuit, le tigre suit sans jamais rattraper, et le tigre meurt de faim. La stratégie optimale du cerf, dans ce monde, est de courir et d'attendre.

{{% comment %}}SOURCE: LAPAN ch.22 p.693{{% /comment %}}

Un détail honnête sur ce résultat, parce qu'il en dit long sur la profondeur des comportements obtenus : dans l'enregistrement de cet épisode, les cerfs se contentent tous de **se déplacer vers la gauche**. Pas de dispersion, pas d'esquive, pas de regroupement : la gauche. Une politique de tigre un peu mieux entraînée exploiterait probablement cette régularité sans difficulté. Je vous rapporte cette observation avec la même réserve que la précédente, puisqu'elle vient aussi d'un enregistrement, et elle suffit à calibrer l'enthousiasme : le comportement émergent de cette expérience est **peu profond**.

{{% comment %}}SOURCE: LAPAN ch.22 p.693{{% /comment %}}

---

## La non-stationnarité, nommée

Le phénomène que vous venez de voir deux fois a un nom, et je vais le donner parce que c'est l'apport principal de cette semaine au vocabulaire du cours.

La **non-stationnarité** (*non-stationarity*) est le fait qu'un agent optimise contre un environnement qui change **parce qu'un autre agent y apprend**. Formellement, la dynamique que l'agent \(i\) perçoit dépend de \(\mathbf{A}_t\), donc des politiques des autres agents ; si celles-ci sont mises à jour, la dynamique perçue par \(i\) change, et le problème que \(i\) résout au pas \(t+1\) n'est **pas** celui qu'il résolvait au pas \(t\). La stationnarité de la semaine 1, que la définition d'un processus de décision markovien exige, est violée. Il n'y a pas d'optimum fixe vers lequel converger : il y a deux politiques qui se poursuivent.

La signature est une **courbe sans tendance**, exactement celle que nous avons vue.

> [!IMPORTANT]
 **Deux mécanismes différents, une même signature, et il ne faut pas les confondre : voici le rapprochement avec la semaine 5.** La triade fatale de la semaine 5 produisait aussi des courbes sans tendance, et parfois une divergence franche, parce que la cible d'amorçage se déplaçait : nous estimions \(Q_\theta\) à l'aide d'une cible calculée avec \(Q_\theta\) lui-même, donc chaque mise à jour des poids déplaçait la cible, et le réseau cible de la semaine 5 existe précisément pour **figer** cette cible pendant quelques milliers de pas. Ici, le mécanisme est entièrement différent : la cible se déplace parce qu'un **autre agent**, avec ses propres poids et son propre optimiseur, apprend en même temps. Aucun réseau cible ne peut figer cela, puisque ce qui bouge n'est pas dans vos poids. Les deux phénomènes se ressemblent sur un graphique et se soignent de façons incomparables : l'un par un gel local de la cible, l'autre par rien de ce que cette semaine vous a donné. Retenez les deux noms, et retenez surtout que **la même courbe plate peut avoir deux causes dont une seule est de votre ressort**.

---

## Ce que cette semaine ne couvre pas, et pourquoi je le nomme

Je termine, comme la semaine 11, par un inventaire de ce que cette semaine laisse de côté, parce qu'un cours honnête nomme ses lacunes au lieu de les contourner.

**La théorie des jeux**, nommée en section 12.9, et dont minimax est le seul fragment que vous aurez vu.

**Les algorithmes réellement multi-agents.** Il existe des méthodes conçues pour le cas multi-agent, avec critique centralisé, exécution décentralisée, valeurs jointes ou factorisées. Cette semaine ne vous en a montré aucune : elle vous a montré une méthode à un agent appliquée \(n_t\) fois, et elle vous l'a dit chaque fois.

**L'observabilité partielle traitée pour elle-même.** L'observation égocentrée de la section 12.10 est partielle, massivement, et nous l'avons traitée comme si elle était complète. Le cadre qui traite correctement cela, le processus de décision markovien **partiellement observable**, est hors du programme de ce cours.

**La mémoire dans un agent.** Un tigre qui a aperçu un cerf au pas 40 l'a oublié au pas 41, parce que sa politique est une fonction de son observation courante et de rien d'autre.

**L'efficacité en échantillons comme sujet à part entière**, alors même que c'est la première motivation que la section 12.1 a donnée aux méthodes avec modèle.

---

## Trois routes vers le jalon 4

Cette semaine ne porte aucun jalon, et le jalon 4 vous attend en semaine 14. Il pourra s'appuyer sur ce que vous venez d'apprendre, et je veux nommer les trois routes que cette semaine lui ouvre, pour que vous sachiez dès maintenant laquelle vous attire.

**L'auto-jeu**, première route : prendre un jeu à deux joueurs, écrire son modèle, et laisser le système se nourrir lui-même. C'est la route la plus sûre, parce que le laboratoire de cette semaine en fait déjà la moitié, et la plus exigeante sur la mesure, puisque vous savez maintenant que la courbe de perte ne vous dira rien et qu'il faudra organiser un tournoi.

**La planification avec un modèle appris**, deuxième route : trois réseaux, une recherche dans un espace caché, et la discipline de ne jamais chercher à interpréter cet espace. C'est la route la plus ambitieuse, et la section 12.8 vous a dit franchement ce qu'elle coûte et ce qu'elle risque.

**Le multi-agent**, troisième route : un monde avec plusieurs agents, une politique partagée par groupe, et un phénomène, la non-stationnarité, que vous pouvez maintenant diagnostiquer au lieu de le combattre. C'est la route la plus exploratoire, et la plus incertaine sur le plan de l'outillage, puisque rien de ce qui est multi-agent n'a été vérifié ici sur une session gratuite.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §2 wk 12{{% /comment %}}
{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}

---
