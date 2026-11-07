---
title: "Laboratoire"
weight: 18
---

Le laboratoire de cette semaine est **formatif** : rien n'y est noté. Ce qui est noté cette semaine, c'est le **jalon 4**, qui vient juste après et qui peut réutiliser le code des volets B et C si vous choisissez la cinquième route.

Et je commence par répéter ce que l'introduction annonçait, parce que c'est la condition d'honnêteté de la section. **La chaîne de la première moitié de la semaine n'est pas reproductible ici.** Treize heures de calcul sur processeur graphique, douze gigaoctets de segments en couleur à stocker, un serveur web à maintenir pendant l'étiquetage, et trois cents jugements humains : les trois premières contraintes excluent une session Colab gratuite, et la quatrième exclut toute machine, puisqu'elle demande une heure de votre attention par centaine d'étiquettes.

Le laboratoire fait donc le choix inverse, et je le crois plus instructif à ce stade du cours : il **isole quatre mécanismes** et les mesure séparément, chacun en quelques minutes. Pour chacun, je vous dis ce que la mesure établit et ce qu'elle n'établit pas.

> [!IMPORTANT]
 **Aucun des quatre volets n'a été exécuté par ce cours, et vous devez le savoir avant de commencer.** Les sections de la semaine établissent que chaque construction est correcte et soutenue par ce qu'elles décrivent ; elles n'établissent pas qu'une courbe précise sortira de votre session. Les volets sont donc écrits comme des **consignes**, jamais comme des résultats attendus, et là où je donne un ordre de grandeur, je dis d'où il vient. Si votre résultat diffère de ce que vous attendiez, la bonne réaction n'est pas de régler jusqu'à ce qu'il ressemble à une attente : c'est de dire ce que vous avez obtenu et d'expliquer ce que cela mesure. Après treize semaines, c'est devenu la compétence centrale de ce cours.

| Volet | Ce qu'il isole | Entraînement | Durée indicative |
| --- | --- | --- | --- |
| **A** | les deux formes de la perte de préférence, et ce qui les sépare | **aucun** | cinq minutes |
| **B** | une chaîne de préférences complète, de l'étiquette à la politique | une tâche de contrôle classique | dix à quinze minutes |
| **C** | la divergence entre substitut et récompense réelle sous la pression d'optimisation | deux ou trois tailles de réseau | dix à quinze minutes |
| **D** | le surapprentissage d'un modèle de récompense sur peu d'étiquettes | une régression logistique | cinq minutes |

---

## Volet A : les deux pertes, comme fonctions pures, et c'est le meilleur volet de la semaine

Je le mets en premier parce qu'il ne demande aucun entraînement, qu'il tient en vingt lignes, et qu'il enseigne le point le plus tranchant de la semaine.

**Ce que vous écrivez.** Deux fonctions, prenant toutes deux en entrée les deux sommes de segment \(R_1, R_2\) et l'étiquette \((y_1, y_2)\), et renvoyant un scalaire. La première implémente l'objectif énoncé de la section 14.2, dans sa forme réduite de la section 14.6, c'est-à-dire une entropie croisée binaire sur le **logit unique** \(R_1 - R_2\) contre la cible \(y_1\). La seconde implémente l'objectif réellement calculé de la section 14.6, c'est-à-dire une entropie croisée binaire sur le tenseur des deux sommes **empilées** contre l'étiquette complète.

N'entraînez rien. Évaluez.

**Étape 1, l'invariance par décalage.** Choisissez une paire de sommes, par exemple \(R_1 = 3\) et \(R_2 = 1\), avec \(y = (1, 0)\). Évaluez les deux pertes. Puis ajoutez une même constante aux deux sommes, par exemple cinquante, et réévaluez. **La première perte doit être identique au bit près, la seconde doit avoir changé.** C'est la mesure centrale du volet, et elle s'écrit en quatre lignes. Si votre première perte change, vous avez passé la mauvaise cible.

Pourquoi cinquante et non dix : parce qu'un segment compte \(L = 50\) pas, donc ajouter un à la récompense **par pas** ajoute cinquante à la somme. C'est l'échelle réaliste du décalage dont il est question.

**Étape 2, la paire « les deux sont bons ».** Reprenez \(y = (0{,}5\,;0{,}5)\) et cherchez, pour chacune des deux pertes, l'ensemble des couples \((R_1, R_2)\) qui la minimisent. Faites-le numériquement, par une grille sur \([-10, 10]^2\) et un tracé de la perte en carte de couleur : c'est plus parlant qu'une dérivation. Vous devez voir, pour la première perte, **une vallée le long de la diagonale** \(R_1 = R_2\) ; pour la seconde, **un unique minimum à l'origine**. Dites en une phrase ce que la seconde apprend au modèle sur deux segments que la personne trouvait tous les deux excellents.

**Étape 3, les cibles absolues contradictoires.** Construisez trois segments fictifs, un mauvais, un moyen et un bon, représentés par trois valeurs de somme. Formez deux paires : moyen contre mauvais, étiquetée en faveur du moyen, et moyen contre bon, étiquetée en faveur du bon. Pour chacune des deux pertes, calculez le gradient par rapport à la somme du segment **moyen** dans les deux paires, et dites s'ils pointent dans le même sens ou en sens contraires. C'est la deuxième conséquence de la section 14.6, vérifiée en six lignes.

**Étape 4, la dérive d'échelle.** Fixez \(y = (1,0)\) et une paire telle que \(R_1 > R_2\). Multipliez les deux sommes par deux, puis par cinq, puis par dix, et tracez chaque perte en fonction du facteur. La seconde doit **décroître continûment** sans que l'ordre des segments change, ce qui est la troisième conséquence de la section 14.6.

**Ce que ce volet établit** : que les deux objectifs ne dépendent pas des mêmes quantités, et exactement en quoi. **Ce qu'il n'établit pas** : que l'un des deux produit un meilleur agent. Pour cela il faudrait entraîner, et nous n'avons pas de machine pour cela cette semaine. Dites-le dans votre conclusion.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-14.ipynb" label="Volet A : les deux formes de la perte de préférence, et quatre mesures sans entraînement" >}}

---

## Volet B : une chaîne de préférences complète, à un millième du coût

**L'idée.** Reconstruire les quatre pièces de la première moitié de la semaine sur une tâche assez petite pour tenir dans une session : enregistrer des segments, les étiqueter, ajuster un modèle de récompense, optimiser contre lui. Une seule pièce est remplacée, et c'est la bonne : **la personne est remplacée par une règle que vous écrivez vous-même**.

**Étape 1, l'environnement et l'enregistreur.** Prenez une tâche de contrôle classique de Gymnasium, un pendule ou un chariot, ou bien un petit monde en grille. Écrivez l'enveloppe d'enregistrement de la section 14.4, avec une longueur de segment de l'ordre de la vingtaine ou de la trentaine de pas et une probabilité de déclenchement réglée pour obtenir quelques centaines de segments en quelques minutes. Gardez le compteur : vous devez savoir combien de segments vous avez.

**Étape 2, l'étiqueteur scripté, et c'est la pièce qui demande de la réflexion.** Écrivez une fonction qui reçoit deux segments et renvoie une étiquette, en appliquant un critère que **vous** décidez. Deux contraintes, et elles sont pédagogiques : votre critère ne doit **pas** être la récompense de l'environnement, sinon vous n'apprenez rien de nouveau ; et il doit être exprimable en une phrase de français, comme celui de la section 14.5. Par exemple, pour un chariot : préférer le segment où le chariot reste le plus près du centre, sans tenir compte de l'angle. Écrivez votre phrase en commentaire au-dessus de la fonction, et prévoyez le cas « les deux sont bons » quand les deux segments se ressemblent à une tolérance près.

**Étape 3, le modèle de récompense.** Un réseau dense à deux couches suffit, vous n'avez pas d'images. Entraînez-le avec la perte de l'étape 1 du volet A, c'est-à-dire la **forme énoncée**, et gardez vingt pour cent des paires de côté.

**Étape 4, la politique contre le modèle.** Écrivez l'enveloppe de substitution de la section 14.7, avec la normalisation glissante sur cent valeurs, et entraînez un acteur-critique ou une méthode de région de confiance dessus. **Journalisez les deux récompenses**, celle du modèle et celle de l'environnement, sur deux courbes.

**Étape 5, la variante semi-supervisée.** Reprenez l'étape 4 en rendant la récompense de l'environnement visible sur **un épisode sur dix tirés au hasard** et en employant le modèle sur les neuf autres. Comparez à deux solutions de référence : la politique entraînée sur la récompense complète, et celle entraînée en ignorant purement et simplement les épisodes non étiquetés. La seconde doit apprendre nettement plus lentement, et dire pourquoi est la question de l'étape.

**Ce que ce volet établit** : que les quatre pièces se branchent, et que votre critère écrit en une phrase produit un comportement identifiable. **Ce qu'il n'établit pas** : quoi que ce soit sur l'efficacité de la rétroaction humaine, puisque votre étiqueteur est déterministe, sans bruit, sans fatigue et sans contradiction, c'est-à-dire exactement ce qu'une personne n'est pas.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-14.ipynb" label="Volet B : la chaîne de préférences complète, avec un étiqueteur scripté et sa variante semi-supervisée" >}}

---

## Volet C : faire divergier le substitut et la récompense réelle, délibérément

C'est le volet qui produit, à votre échelle, la forme de la Figure 14-3. Il est aussi celui dont le code sert le plus directement au jalon 4.

**Étape 1, les deux récompenses.** Choisissez une tâche et écrivez-en **deux** fonctions de récompense, en vous servant de l'enveloppe de la section 14.13. La récompense réelle est celle que vous considérez comme l'intention ; le substitut en diffère par une **erreur de portée**, c'est-à-dire qu'il mesure le même désidérata sur une partie seulement de l'espace d'états ou de la durée de l'épisode. Deux exemples qui fonctionnent : sur un chariot, ne compter la stabilité que lorsque le chariot est dans la moitié droite du rail ; sur un monde en grille, ne compter la progression que dans la moitié supérieure de la grille.

Dites explicitement, en commentaire, lequel des trois types de la section 14.12 vous avez construit. Si vous préférez construire une erreur de pondération ou une erreur d'ontologie, c'est également accepté, mais dites-le : la portée est la plus facile à faire basculer sur une petite tâche.

**Étape 2, deux ou trois tailles.** Entraînez le même algorithme sur le **substitut seul**, avec deux ou trois tailles de réseau séparées par un ordre de grandeur en nombre de paramètres. Gardez tout le reste identique : mêmes graines, même nombre de pas, même pas d'apprentissage. La seule variable est la capacité.

**Étape 3, les deux courbes.** Tracez, pour chaque taille, le substitut et la récompense réelle. Vous cherchez la forme de la section 14.13 : une montée commune, puis une séparation. Et je vous préviens tout de suite, parce que c'est le point où l'honnêteté du volet se joue : **il est très possible que vous n'obteniez aucune séparation**. Les transitions mesurées en section 14.13 apparaissent sur des plages de capacité de deux à quatre ordres de grandeur, et vous en couvrez un. Si vous ne voyez rien, ce n'est pas un échec du volet : c'est un résultat, et il se rapporte ainsi, avec l'écart d'échelle comme explication candidate.

**Étape 4, la corrélation, et c'est l'étape que je préfère.** Calculez la corrélation de Pearson entre le substitut et la récompense réelle sur une trentaine de déroulements, à deux points de contrôle : un très précoce et celui du meilleur substitut. Vous devriez trouver une corrélation **positive aux deux points**, même si votre plus grand modèle s'est dégradé. C'est la mesure de la section 14.13 refaite chez vous, et c'est la plus utile des quatre, parce qu'elle vous apprend à ne pas faire confiance à une corrélation.

**Ce que ce volet établit** : le protocole, et la forme des courbes si vous la voyez. **Ce qu'il n'établit pas** : un seuil, ni une valeur. Les seuils de la section 14.13 sont des mesures relevées sur des figures et ne sont pas des références.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-14.ipynb" label="Volet C : substitut contre récompense réelle, deux ou trois capacités, et la corrélation aux deux points de contrôle" >}}

---

## Volet D : le surapprentissage d'un modèle de récompense, si le temps le permet

Le plus court des quatre, et le plus directement utile si vous choisissez la cinquième route du jalon.

**Étape 1.** Reprenez le modèle de récompense du volet B et les étiquettes de votre étiqueteur scripté. Faites varier le nombre d'étiquettes : cinquante, deux cents, mille.

**Étape 2.** Pour chaque taille, gardez **vingt pour cent** de côté, entraînez avec un **arrêt anticipé sur cette partition réservée** après quatre époques sans amélioration, et journalisez les deux pertes, entraînement et réservée, à chaque époque.

**Étape 3.** Tracez les six courbes et répondez à deux questions. À partir de combien d'étiquettes l'écart entre les deux pertes cesse-t-il de croître ? Et à quelle époque votre arrêt se déclenche-t-il, comparé à l'ordre de grandeur d'une douzaine d'époques mentionné en section 14.6 ?

**Étape 4, facultative et instructive.** Ajoutez du bruit dans votre étiqueteur : avec une probabilité de dix pour cent, il se trompe. Refaites la mesure. C'est le seul volet du laboratoire qui approche de la condition réelle d'un étiquetage humain.

**Ce que ce volet établit** : l'ordre de grandeur du régime de données dans lequel un modèle de récompense cesse de surapprendre, **sur votre tâche**. **Ce qu'il n'établit pas** : rien de transférable à une tâche visuelle, où le modèle de la section 14.6 avait plus de cent mille dimensions d'entrée et trois cents exemples.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-14.ipynb" label="Volet D : trois tailles d'étiquetage, arrêt anticipé sur la partition réservée, et un étiqueteur bruité" >}}

---

## La solution courte, et pourquoi elle ne dispense pas du volet A

Comme à chaque semaine, une référence pour comparer votre code, et elle vaut surtout pour les volets B et C : une implémentation de bibliothèque d'une méthode de région de confiance, branchée sur l'enveloppe de substitution que vous aurez écrite. L'enveloppe reste votre travail, puisque c'est elle qui porte toute la semaine ; l'algorithme peut venir d'ailleurs.

En revanche, le volet A n'a **aucune** solution courte, et c'est délibéré : aucune bibliothèque ne vous dira de quoi une perte dépend. Il faut l'évaluer soi-même, et cela prend cinq minutes.

{{< colab url="https://colab.research.google.com/github/FaycalZM/drl-course-teluq/blob/main/notebooks/semaine-14.ipynb" label="Référence : une méthode de région de confiance de bibliothèque sur l'enveloppe de substitution des volets B et C" >}}

---
