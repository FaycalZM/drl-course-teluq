---
title: "7.13 Ce qu'il faudrait pour que ce soit sérieux"
weight: 14
---

## Cinq chantiers, et trois coûts que la simulation ignore

Fermons cette moitié de semaine honnêtement, en disant ce qui manque. Et commençons par le cadrage, parce qu'il remet les proportions en place : construire une stratégie de négociation complète et rentable par apprentissage par renforcement est un **grand projet**, qui peut demander plusieurs mois de travail à temps plein. Ce que nous avons fait en une semaine est une maquette qui montre les mécanismes, et c'était l'objectif.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

**Chantier 1, la représentation.** Elle n'est **pas satisfaisante**, et nous savons déjà pourquoi grâce à la section 7.8 : elle ne porte ni les niveaux de support et de résistance, ni les valeurs rondes, ni aucune information de marché autre que le prix et le volume de l'instrument lui-même.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

**Chantier 2, plusieurs échelles de temps.** Des barres d'une minute sont **bruyantes**, et l'image est juste : c'est regarder le marché au microscope. On voit chaque fluctuation et aucune tendance. Des barres horaires ou journalières montrent les mouvements longs. Un agent peut en principe regarder **plusieurs échelles à la fois**, et c'est une direction naturelle avec les architectures à attention et à longue fenêtre de contexte.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

**Chantier 3, davantage de données, et c'est le plus sérieux des cinq.** Une année d'un seul titre, c'est 130 000 barres. Cela ressemble à beaucoup. Ce n'est rien du tout : ces 130 000 barres décrivent **un seul régime de marché**, celui de cette année-là, pour **une seule entreprise**. Toutes les situations de marché qui ne se sont pas produites en 2015 sont absentes de l'entraînement. Un agent sérieux voudrait des **centaines de titres sur dix ans ou plus**. Et remarquez que ce chantier explique entièrement la section 7.12 : le surapprentissage observé n'est pas la faute de l'architecture, c'est le comportement normal d'un réseau de plusieurs centaines de milliers de paramètres entraîné sur un unique régime.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

**Chantier 4, l'architecture.** Tout est ouvert : le nombre de couches, la taille des noyaux, les connexions résiduelles, l'attention. Et c'est le chantier le moins prometteur des cinq, ce qui est en soi une information : quand la limite est la quantité de données, changer d'architecture ne la déplace pas.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

**Chantier 5, une analogie à garder en tête.** Une série de barres et une phrase ont une parenté réelle : ce sont deux séquences de longueur variable produites par des humains. On peut donc envisager de **découper les barres en jetons**, en associant par exemple un symbole à « a monté d'environ 1 % », puis d'appliquer les outils de la modélisation de séquences, plongements et architectures à attention. C'est une piste, pas un résultat, et je la mentionne parce qu'elle montre comment des domaines distants s'empruntent des représentations.

{{% comment %}}SOURCE: LAPAN ch.10 p.325{{% /comment %}}

---

## Les trois coûts absents, et pourquoi ils ne sont pas des détails

Il reste à nommer précisément les trois choses que notre simulation **ne modélise pas du tout**, parce qu'après la leçon de la section 7.12 vous savez maintenant ce qu'un coût absent peut faire à un résultat.

**L'écart achat-vente** (*spread*). À tout instant, sur un marché réel, il y a deux prix et non un : celui auquel on peut vendre immédiatement, et celui, plus élevé, auquel on peut acheter immédiatement. L'écart entre les deux est payé à chaque passage, en plus de la commission. Notre simulation utilise un seul prix de clôture pour l'achat et pour la vente, donc elle **ignore entièrement** ce coût.

**Le dérapage des prix** (*price slippage*). Nous supposons l'exécution instantanée au prix de clôture de la barre. En réalité, entre la décision et l'exécution, le prix a bougé, et il a statistiquement tendance à bouger **contre** vous, puisque vous achetez quand les autres achètent.

**L'impact de marché.** Vos propres ordres déplacent le prix. Pour une action, l'effet est négligeable ; pour un volume significatif, il ne l'est pas, et il a cette propriété désagréable qu'il **croît** avec la taille de la position : une stratégie rentable à petite échelle peut cesser de l'être précisément parce qu'elle a réussi.

{{% comment %}}SOURCE: LAPAN ch.10 p.315, p.323, p.325{{% /comment %}}

Les trois ont le même signe : ils coûtent. Aucun des trois n'est dans notre récompense. Et la section 7.12 nous a déjà montré ce qu'un **seul** coût de 0,1 % par opération fait au résultat.

> [!IMPORTANT]
 **La phrase que je veux que vous reteniez de toute cette moitié de semaine.** Une simulation historique n'est pas une promesse. C'est l'évaluation d'une politique sur **un** chemin du passé, sous **les hypothèses de votre simulateur**, et rien de plus. Quand vous lisez un résultat de ce type, le vôtre ou celui d'un autre, posez les mêmes cinq questions : combien d'instruments, combien de périodes, quels coûts modélisés, quelle sélection de modèle, et par rapport à quelle stratégie passive ? Si l'une des cinq réponses manque, le résultat n'est pas interprétable. Il n'est pas faux : il est **non interprétable**, ce qui est une situation différente et plus fréquente.

---
