---
title: "Conclusion du cours"
weight: 6
---

# Conclusion du cours

Cette page se lit deux fois.

**La première fois, maintenant**, avant la semaine 1, parce qu'elle vous dit où vous
allez, comment les quatre jalons s'emboîtent et quels pièges coûtent le plus de temps.
Rien de ce qui suit ne demande de connaître une méthode.

**La seconde fois, à la fin**, quand les quinze semaines seront derrière vous. Les mêmes
phrases ne diront plus la même chose, et c'est le signe que le cours a fonctionné.

---

## Les quatre jalons ne sont pas quatre travaux

C'est la chose que je voudrais que vous compreniez avant de commencer. Les quatre jalons
pèsent 25 % chacun, mais ils ne sont pas interchangeables et ils ne se préparent pas
séparément : **chacun garde les exigences du précédent et en ajoute une**. Votre jalon 2
sera comparé à votre jalon 3, votre jalon 3 à votre jalon 4, et les livrables finaux
porteront sur les quatre ensemble.

{{< mermaid >}}
graph TD
  J1["Jalon 1 : analyser un échec"] -->|"ajoute plusieurs graines et un intervalle"| J2["Jalon 2 : accélérer et comparer"]
  J2 -->|"ajoute trois axes qui peuvent se contredire"| J3["Jalon 3 : politique contre valeur"]
  J3 -->|"ajoute le choix de la méthode, à justifier"| J4["Jalon 4 : une extension avancée"]
  J4 -->|"ajoute l'exécution par quelqu'un d'autre"| LF["Livrables finaux"]
{{< /mermaid >}}

Deux conséquences pratiques, et elles valent de l'argent en temps de calcul.

**Choisissez votre environnement une fois, au jalon 1, et gardez-le.** Les trois jalons
suivants comparent votre nouvel agent à l'ancien sur la même tâche. Changer
d'environnement en route vous obligerait à remesurer l'agent précédent, c'est-à-dire à
refaire un travail déjà noté.

**Gardez tout.** Vos graines, vos hyperparamètres, vos courbes, vos journaux, et le code
qui les a produits. Le jalon 3 vous demandera des chiffres du jalon 2, et les livrables
finaux des chiffres des quatre. Une mesure que vous ne retrouvez pas est une mesure à
refaire.

---

## Six règles qui survivent aux méthodes

Les méthodes de ce cours se démoderont, certaines vite. Les six règles qui suivent ne se
démoderont pas, parce qu'elles ne sont pas des techniques. Elles s'installent une par une
entre les semaines 3 et 15, et à partir du jalon 2 elles sont notées.

1. **Une exécution unique ne permet de décider de rien.** Trois graines au minimum, cinq
   de préférence, le même jeu de graines pour toutes les variantes que vous comparez.
2. **Un écart dont les intervalles se recouvrent n'est pas un résultat.** Écrivez-le
   ainsi, sans excuse. C'est la phrase la plus difficile à écrire du domaine, et celle
   que je cherche dans vos notes.
3. **Les exécutions qui n'ont pas convergé se comptent à part de la moyenne.** Une
   moyenne sur huit exécutions, présentée seule, peut cacher trois échecs sur huit.
4. **Le critère d'arrêt se fixe avant de mesurer, jamais après.** Un seuil choisi en
   regardant la courbe transforme n'importe quelle variante en gagnante.
5. **Un chiffre sans son protocole n'est pas une mesure.** Les graines, les
   hyperparamètres, le matériel, la durée, les versions. La semaine 15 vous montrera un
   travail sérieux rendu inutilisable par l'absence de deux pages de configuration.
6. **Demandez toujours quelle récompense est optimisée, et qui l'a écrite.** Des trois
   objets d'un problème de décision, c'est le seul que vous concevez, donc le seul dont
   vous êtes responsable.

> [!TIP]
 **Le format d'une note qui se lit.** Une mesure, une déduction, une conclusion. Pas de
 récit chronologique de vos essais, pas de « prometteur mais délicat ». Si quelque chose
 n'a pas fonctionné chez vous, écrivez-le, et dites que vous ne savez pas pourquoi si
 vous ne le savez pas. C'est le format des quatre jalons, et je le demande dès le
 premier.

---

## Les pièges qui coûtent le plus de temps

Ceux-ci ne sont pas des erreurs de débutant. Ce sont les pannes qui ne lèvent aucune
exception, et c'est précisément ce qui les rend chères. Le cours les rencontre une par
une ; les voici rassemblés, pour que vous les reconnaissiez avant de perdre une soirée.

**Le bogue qui n'arrête rien.** La semaine 3 vous fera écrire un agent qui apprend
l'inverse de ce qu'il devrait, sans lever une erreur et sans ralentir. Un bogue qui
empêche tout est facile à trouver ; celui qui dégrade, ou qui inverse, vous rendra une
courbe parfaitement lisible. **Premier réflexe : comparez à un agent aléatoire.** Si
votre agent fait moins bien que le hasard, il apprend, et il apprend le mauvais signe.

**Le critère de réussite qui mesure la chance.** La semaine 4 vous fera franchir un seuil
qui porte sur vingt épisodes de test, et le nombre de tours nécessaires variera d'un
facteur sept selon la graine. Avant de conclure que votre code est lent, demandez-vous
sur combien d'épisodes votre critère est calculé.

**L'accélération qui casse l'apprentissage.** Mesurez votre version de référence et
montrez qu'elle converge **avant** d'accélérer quoi que ce soit. Après coup, une
accélération qui a cassé l'apprentissage ressemble exactement à une accélération qui
marche.

**Les deux indicateurs qui se contredisent.** Le débit en trames par seconde et le temps
pour atteindre le seuil peuvent pointer en sens opposé sur la même variante. Savoir
lequel croire demande d'avoir répété ; aucun raisonnement ne remplace la répétition.

**Deux réparations qui se gênent.** À la semaine 6, une correction installée la semaine
précédente sera abîmée par une autre. Les correctifs ne s'empilent pas toujours
proprement, et le dire est plus utile que de choisir le plus récent.

**Le classement qui ne se transfère pas.** À la semaine 11, une hiérarchie de méthodes
établie sur une tâche sera fausse sur une autre, les deux mesures étant bonnes. La
conclusion honnête d'une comparaison est parfois que la comparaison était locale.

**La perte d'information qu'on ne voit jamais autrement.** Si vous encodez un état en
entier, écrivez le test de l'aller-retour. Deux positions différentes qui produisent le
même entier ne se signalent par aucune erreur, et leurs effets ressemblent à un mauvais
réglage.

**Le gradient qui disparaît au lieu de diminuer.** À la semaine 13, un chemin
d'optimisation mal construit ne rendra pas un petit gradient : il n'en rendra aucun, et
la bibliothèque lèvera. Un message d'erreur est ici une bonne nouvelle.

---

## Travailler dans le budget

Le cours est conçu pour tourner sur un processeur graphique partagé, dans un carnet.
Cette contrainte n'est pas un pis-aller, elle est écrite dans les énoncés : **aucun jalon
ne demande plus de deux à quatre heures de calcul au total**, et dépasser ce budget ne
rapporte aucun point.

Trois conseils qui en découlent.

**Le temps économisé sur le calcul est à dépenser dans l'analyse**, qui est la partie
notée. Un résultat modeste accompagné de son protocole vaut plus de points qu'un résultat
impressionnant dont personne ne peut dire d'où il vient. Et un résultat négatif
correctement établi vaut autant qu'un résultat positif.

**Lancez une exécution pilote avant d'annoncer une cible.** Une seule, courte, pour voir
l'ordre de grandeur. Annoncer une cible atteignable et l'atteindre sur trois graines vaut
mieux qu'annoncer une cible ambitieuse et rendre trois exécutions non convergées.

**Servez-vous du code fourni.** Le paquet `sci1070` du dépôt du cours contient le
protocole de mesure, les jeux de données et les environnements que les énoncés ne vous
demandent pas d'inventer. Il ne contient aucune solution d'exercice, et c'est voulu :
écrire le code des laboratoires *est* l'exercice. Mais `mesurer`, `intervalle`,
`se_recouvrent` et `tracer_bande` existent pour que les règles 1 à 3 ci-dessus ne vous
coûtent pas une demi-journée de code à chaque jalon.

---

## Ce qui ne figure dans aucun barème

Deux remarques pour terminer, et ce sont les deux choses que je n'ai pas trouvé le moyen
de noter.

La première est que **vous allez rencontrer beaucoup de méthodes qui ne fonctionnent
pas**. Une qui ne converge pas, un classement qui s'inverse, un agent qui désapprend
quand on l'entraîne davantage, une récompense qui se laisse exploiter, une reproduction
qui échoue. Ce n'est pas la chronique d'un domaine en désordre : c'est ce à quoi
ressemble un domaine jeune quand on le regarde d'assez près pour voir ses mesures. Un
cours qui ne vous aurait montré que des courbes qui montent vous aurait moins bien
préparé.

La seconde est que **la discipline de mesure se transfère plus loin que
l'apprentissage par renforcement**. Si dans trois ans vous avez oublié la forme exacte
d'un objectif écrêté mais que vous demandez encore, devant un système qu'on vous
présente, quelle récompense il optimise, qui l'a écrite et dans quelles unités sont ses
chiffres, alors ce cours aura fait son travail.

Les mots de la fin sont à la dernière page de la semaine 15, et c'est là qu'ils doivent
être lus, pas ici.

[Ouvrir la dernière page →]({{< relref "/docs/ch5-applications-synthese/week15/livrables-finaux" >}})

{{% comment %}}
Page ajoutée le 07/11, à la demande de l'équipe pédagogique : une conclusion de cours
portant des conseils, et non un second adieu.

Elle ne duplique PAS la sous-section « La dernière page » de
week15/livrables-finaux.md, qui garde les mots de la fin et vers laquelle cette page
renvoie. Le partage est celui-ci : là-bas le constat et l'adieu, ici le mode d'emploi.
Les deux paragraphes de « Ce qui ne figure dans aucun barème » sont volontairement
proches du ton de la dernière page, parce qu'ils répondent à la même question, mais ils
disent autre chose : là-bas « voilà ce que vous avez vu », ici « voilà ce que ça vous
coûtera si vous l'ignorez ».

Pas de source raw-content : comme les cinq pages de remise, cette page n'appartient à
aucune semaine. Le jour où elle doit être reprise, elle se corrige ici, et ici
seulement.

Aucune référence externe nommée (D17, D18) : la section « Et après » qu'on attendrait
d'une conclusion n'existe donc pas, et c'est voulu. Une liste de lectures serait une
référence visible. Ce qui la remplace, c'est la section du budget et celle des six
règles, qui parlent de pratique et non de bibliographie.

Les huit pièges sont tous tirés de semaines écrites, dans l'ordre : 3 (bogue silencieux
next_obs), 4 (critère sur vingt épisodes), 7 (l'ordre référence puis accélération, et
les deux indicateurs), 6 (§6.6, dépliage contre tampon de rejeu), 11 (§11.7, le
classement local), 12 (le test de l'aller-retour de l'encodage), 13 (le gradient qui
disparaît sans reparamétrisation). Aucun n'est inventé pour la page.

Le poids 6 place la page entre le module 5 (5) et les annexes, qui passent de 6 à 7.
{{% /comment %}}
