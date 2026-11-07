---
title: "14.5 Où se tient l'humain, et ce qu'on lui demande vraiment"
weight: 6
---

## Vingt paires à la fois, trois boutons, et un fichier qui s'allonge

Nous arrivons à la pièce de la chaîne dont on parle le moins et qui détermine le plus : l'interface par laquelle le jugement humain entre dans le système.

C'est une page web, servie localement. Elle tire **vingt paires de segments au hasard** dans la base et les affiche l'une après l'autre. Pour chaque paire, les deux segments sont rendus côte à côte sous forme d'**images animées fabriquées à la volée** à partir des trames enregistrées, de sorte que la personne voit deux petits films de trois secondes plutôt que deux listes de nombres.

Sous les deux films, trois boutons : le premier est meilleur, **les deux sont bons**, le second est meilleur. Les touches 1, 0 et 2 du clavier font la même chose, l'affichage passe automatiquement à la paire suivante, et chaque jugement est ajouté à un fichier texte à raison d'une ligne par étiquette.

{{% comment %}}SOURCE: LAPAN ch.19 p.585-586{{% /comment %}}

La **Figure 14-2** montre cette page en fonctionnement : les deux clips avec leurs scores respectifs, la jauge d'oxygène visible dans chacun, la liste des paires restantes, les trois boutons et le rappel des touches.

{{< bookfig src="14-02.png" week="14" >}}

Trois choses à remarquer sur cette interface, et aucune des trois n'est cosmétique.

**Elle est conçue pour le clavier.** Pas de glisser, pas de curseur à régler, pas de champ de texte. Une touche par paire. C'est ce qui rend trois cents jugements faisables en une session plutôt qu'en une journée.

**Elle ne demande aucune justification.** La personne appuie et passe. Le système n'apprendra donc jamais **pourquoi** un segment a été préféré : il n'apprendra que **qu'il** l'a été. Toute la richesse du jugement est comprimée dans un trit.

**Et elle tire les paires au hasard dans la base.** Pas de sélection des paires informatives, pas de recherche active des cas où le modèle est incertain. Un tirage uniforme. C'est simple, c'est honnête, et c'est l'une des raisons pour lesquelles les trois cents étiquettes de cette chaîne portent moins loin qu'elles pourraient.

---

## Le paragraphe qui est, littéralement, la fonction de récompense

Et maintenant le point de cette section, celui pour lequel je l'ai écrite.

La personne qui a produit les trois cents étiquettes de cette chaîne a suivi un critère, et ce critère est le suivant : accorder le plus d'attention aux cas rares où **le sous-marin est à la surface**, et les marquer comme bons ; accorder de l'attention aux situations plus fréquentes où **l'oxygène est bas**, et les marquer comme mauvais ; et à défaut, préférer les segments où des poissons sont touchés.

{{% comment %}}SOURCE: LAPAN ch.19 p.587{{% /comment %}}

Relisez ce critère et comparez-le à ce que nous cherchions en section 14.1. Nous voulions trois choses : tirer, gérer l'oxygène, et **sauver des plongeurs**. Le critère d'étiquetage en contient deux. Le sauvetage de plongeurs, l'activité la plus rémunératrice du jeu et celle que l'agent de départ ignorait complètement, n'y figure pas.

> [!IMPORTANT]
 **Ce critère EST la fonction de récompense de toute l'expérience, et c'est là que la spécification a lieu.** Je veux que vous mesuriez le déplacement. Nous avons commencé par refuser d'écrire une récompense à la main, en section 14.1, parce que régler des coefficients revenait à écrire la solution dans l'environnement. Et nous venons de la réécrire, non pas en Python mais en français, dans un paragraphe de méthode. Le réglage n'a pas disparu : il a changé de langue et de lieu. Il est passé du fichier de l'environnement, où il était versionné, testable et visible, à une description de protocole. Et à la différence d'un coefficient, un critère d'étiquetage n'est pas vérifiable automatiquement : rien dans le système ne peut détecter qu'il a été appliqué de travers, ni qu'il a changé au milieu de la session.

C'est la première fois dans ce cours qu'une fonction de récompense est écrite en prose, et c'est un fait sur lequel la section 14.16 reviendra pour poser les trois questions qui en découlent : qui étiquette, selon quels critères, et à quel prix.

---

## Trois cents étiquettes, et ce qu'elles ne contiennent pas

Un dernier chiffre pour fermer la section, et c'est un chiffre sur une absence.

Sur les cent paires du premier tour, le nombre de segments contenant un sauvetage de plongeur se compte sur les doigts d'une main. Ce n'est pas étonnant : les segments sont tirés au hasard dans la production d'une politique qui ne sauve jamais de plongeur, et ils durent cinquante pas, ce qui ne suffit pas pour en collecter six et remonter. **Le comportement que nous voudrions le plus enseigner est celui dont les données contiennent le moins d'exemples**, et la raison en est circulaire : il faudrait que l'agent le fasse déjà un peu pour qu'on puisse le lui montrer.

{{% comment %}}SOURCE: LAPAN ch.19 p.596-597{{% /comment %}}

Gardez cette circularité en tête. C'est une version de l'exploration, et c'est aussi la raison pour laquelle le tour 3 de la section 14.8 échouera sur le point précis où il visait les plongeurs.

---
