---
title: "13.13 Ce n'est pas de l'apprentissage supervisé, et voici un argument chiffré"
weight: 14
---

## Deux choses mises hors du sujet, délibérément

Avant l'argument, deux délimitations honnêtes.

**Première délimitation : l'exploration est hors sujet, et c'est assumé.** Si \(\mathcal{D}\) ne contient aucune transition à forte récompense, aucune méthode ne peut en découvrir. Pas « difficilement » : pas du tout. L'information n'est pas dans les données, et aucun algorithme ne l'y mettra. Tout ce domaine fait donc une **hypothèse de couverture** : le jeu contient quelque part de quoi faire mieux que la politique de comportement. Et il faut ajouter une précision désarmante : **formaliser cette hypothèse est un problème ouvert**. Il n'existe pas de condition suffisante non triviale, connue, sur \(\mathcal{D}\), qui garantisse qu'une bonne politique en soit extractible.

{{% comment %}}SOURCE: OFFLINE p.9{{% /comment %}}

**Seconde délimitation : si la politique apprise ne doit pas différer des données, l'exercice n'a pas d'objet.** Il existe une méthode triviale pour ne jamais sortir de la distribution des données : imiter la politique de comportement. On appelle cela le **clonage de comportement** (*behavioral cloning*), c'est de l'apprentissage supervisé pur, et cela donne au mieux \(\pi_\beta\). Tout l'intérêt de l'apprentissage hors ligne est de faire **mieux** que les données, donc de s'en écarter, donc d'affronter le problème de la section 13.14. On ne peut pas vouloir l'un sans l'autre.

---

## Le mot qui dit la vraie difficulté : contrefactuel

Voici la formulation que je trouve la plus éclairante de tout le domaine.

Un problème d'apprentissage supervisé pose des questions sur la **même** distribution que celle de ses données : étant donné une image tirée de la même loi que mes exemples, quelle est sa classe ? Un problème hors ligne pose des **requêtes contrefactuelles** (*counterfactual query*) : des questions en « et si », portant sur un cours d'action **différent** de celui que contiennent les données. Que se passerait-il si, dans cet état, on avait freiné au lieu d'accélérer ? Les données ne répondent pas, puisque personne n'a freiné.

Et c'est pour cela que les outils de l'apprentissage statistique, qui reposent tous sur une hypothèse d'indépendance et d'identité de distribution entre entraînement et test, sont mis à rude épreuve ici : la question posée **viole l'hypothèse par construction**.

{{% comment %}}SOURCE: OFFLINE p.9{{% /comment %}}

> [!TIP]
 **Un exemple pour fixer les idées, et il n'est pas théorique.** Vous disposez des dossiers de dix mille patients traités selon un protocole hospitalier existant, avec leurs issues. Vous voulez savoir si un autre protocole ferait mieux. Les données contiennent ce que le protocole existant a produit, et uniquement cela. Toute conclusion sur l'autre protocole est une inférence contrefactuelle, et le fait d'avoir cent mille dossiers au lieu de dix mille ne change **rien** à cette difficulté : cela réduit l'incertitude sur ce que fait le protocole existant, et pas sur ce que ferait l'autre. Retenez cette dernière phrase : la section 13.14 va la retrouver sous forme de courbe mesurée.

---

## L'argument chiffré, et son hypothèse hors de proportion

Voici maintenant un argument quantitatif. Il porte sur le cas le plus favorable imaginable, et c'est ce qui le rend fort.

**Posons l'hypothèse à voix haute** : supposons qu'on nous **donne l'action optimale** \(a^\star\) en chaque état de \(\mathcal{D}\). Pas une récompense, pas un retour : la bonne action, directement, gratuitement, à chaque état du jeu de données. C'est infiniment plus que ce dont dispose n'importe quel algorithme d'apprentissage par renforcement. Et on se contente d'apprendre, par minimisation du risque empirique, à les reproduire.

Mesurons l'erreur par le nombre d'actions fausses le long d'une trajectoire :

$$
\ell(\pi) \;=\; \E_{p_\pi}\!\left[\sum_{t=0}^{H} \mathbf{1}\big[A_t \ne a^\star_t\big]\right]
$$

Le premier résultat dit ceci. Si l'on minimise le risque empirique sur des états tirés de \(d^{\mathcal{D}}\), avec des étiquettes optimales et une **erreur de généralisation** (*generalization error*) \(\epsilon_{\text{gen}}\), alors la meilleure borne qu'on puisse établir est

$$
\ell(\pi) \;\le\; C + H^2\, \epsilon_{\text{gen}}
$$

{{% comment %}}SOURCE: OFFLINE thm 2.1 p.9{{% /comment %}}

Le second résultat change **une seule chose** au dispositif : les états sur lesquels on minimise le risque empirique sont tirés de \(d^\pi\), la distribution de la politique **apprise**, ce qui suppose évidemment de pouvoir la faire agir pour les obtenir. La borne devient

$$
\ell(\pi) \;\le\; C + H\, \epsilon_{\text{gen}}
$$

{{% comment %}}SOURCE: OFFLINE thm 2.2 p.10{{% /comment %}}

**Quadratique contre linéaire, avec des étiquettes parfaites.** Prenez la mesure de ce que cela dit. Même en vous offrant l'action optimale partout, le simple fait d'avoir appris sur la distribution de quelqu'un d'autre coûte un facteur \(H\) supplémentaire sur l'erreur. Sur un épisode de mille pas, c'est mille fois pire.

---

## Le mécanisme du carré, qui est la vraie leçon

La borne n'est pas intéressante ; son mécanisme l'est, et il se raconte en quatre temps.

**Un.** La politique apprise peut entrer dans des états très éloignés de sa distribution d'entraînement, puisque \(d^\pi\) peut différer énormément de \(d^{\mathcal{D}}\).

**Deux.** Dans un tel état, **la garantie de généralisation ne tient plus**. Une minimisation du risque empirique ne promet rien hors de la distribution sur laquelle le risque a été mesuré. C'est exact, c'est élémentaire, et c'est tout le problème.

**Trois.** Une fois dans un tel état, la politique **continue de se tromper**, et comme ses erreurs l'éloignent encore, elle peut rester hors distribution **pour tout le reste de l'essai**. Une entrée hors distribution coûte donc, en pire cas, \(O(H)\) erreurs et non une seule.

**Quatre.** Et il y a \(H\) instants auxquels elle peut y entrer. \(H\) occasions, \(O(H)\) erreurs chacune : \(O(H^2)\).

{{% comment %}}SOURCE: OFFLINE p.10{{% /comment %}}

> [!WARNING]
 **Et la réserve, qui est dans le texte même de l'argument et que je ne vais pas taire : cet exemple porte sur le clonage de comportement, pas sur l'apprentissage par renforcement hors ligne.** C'est un problème voisin, et assez orthogonal au sujet de cette moitié de semaine. Ce n'est donc **pas un théorème sur l'apprentissage hors ligne**, et il ne faut pas le présenter comme tel. Il a une valeur différente et, à mon avis, supérieure : il montre que le problème de la distribution **n'est pas un artefact de l'amorçage ni de la fonction de valeur**. Il est déjà là dans le cas le plus simple et le plus favorable qu'on puisse construire, avec des étiquettes parfaites et aucun apprentissage par renforcement. Ce qui vient ensuite est pire, et c'est maintenant.

---
