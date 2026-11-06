---
title: "5.3 Ce que l'on minimise : l'erreur quadratique moyenne sur les valeurs"
weight: 4
---

## Le cas tabulaire n'avait pas d'objectif à choisir

Je commence par une question que la semaine 4 n'a jamais eu besoin de poser : **que cherche-t-on exactement à minimiser ?** Si elle vous paraît oiseuse, c'est bon signe, parce que c'est précisément la différence entre les deux semaines.

Dans le cas tabulaire, aucune mesure continue de la qualité des prédictions n'était nécessaire, et il y a deux raisons à cela. La première : la fonction de valeur apprise pouvait finir par égaler **exactement** la fonction de valeur vraie, donc il existait une solution parfaite et la seule question était de l'atteindre. La seconde, et c'est celle qu'il faut retenir : les valeurs apprises en chaque état étaient **découplées**. Une case juste, une case fausse, et elles ne se gênaient pas. Il n'y avait donc rien à arbitrer, et donc aucun objectif à choisir.

{{% comment %}}SOURCE: SB ch.9 p.221{{% /comment %}}

Avec une approximation véritable, c'est-à-dire avec beaucoup plus d'états que de poids, cette commodité disparaît. Rendre l'estimation d'un état plus exacte revient invariablement à rendre celle d'autres états moins exacte : les poids sont partagés, et il n'y en a pas assez pour satisfaire tout le monde. Nous sommes donc **obligés de dire quels états nous intéressent le plus**, et cette obligation n'a rien d'optionnel : sans elle, dire que l'on minimise l'erreur ne veut rien dire. Il faut donc fournir une distribution \(\mu(s) \ge 0\), avec \(\sum_s \mu(s) = 1\), qui dit quelle importance on attache à l'erreur commise en chaque état.

{{% comment %}}SOURCE: SB ch.9 p.221{{% /comment %}}

L'objectif naturel s'écrit alors, et il porte un nom : l'**erreur quadratique moyenne sur les valeurs** (*mean squared value error*), notée \(\overline{VE}\).

$$
\overline{VE}(\mathbf{w}) \defeq \sum_{s \in \mathcal{S}} \mu(s)
\big[\, v_\pi(s) - \hat v(s,\mathbf{w}) \,\big]^2
$$

{{% comment %}}SOURCE: SB ch.9 éq. 9.1 p.221{{% /comment %}}

Trois symboles, trois rôles. L'écart entre la valeur vraie et la valeur approchée est l'erreur. Le carré en fait une quantité positive que l'on peut minimiser. Et \(\mu(s)\) est la pondération, c'est-à-dire la réponse à la question posée au paragraphe précédent : quels états nous intéressent le plus.

Reste à savoir d'où vient \(\mu\). La réponse usuelle est aussi la plus simple : \(\mu(s)\) est la **fraction du temps passé dans \(s\)**. Sous un entraînement sur politique, cette fraction porte un nom, la **distribution sur politique** (*on-policy distribution*), et dans une tâche continue c'est la distribution stationnaire sous \(\pi\). Il existe une construction formelle de \(\mu\) dans le cas épisodique ; nous n'en avons pas besoin, et je me contente de vous dire qu'elle existe et qu'elle est bien définie.

{{% comment %}}SOURCE: SB ch.9 p.221{{% /comment %}}

Voici le fragment qui rend \(\mu\) concret, et c'est le fragment le plus important de la section, parce qu'il montre que vous avez déjà écrit \(\mu\) sans le savoir.

```python
def erreur_quadratique_sur_valeurs(reseau, etats_visites, valeurs_vraies):
    """VE barre, estimée sur les états que l'agent a RÉELLEMENT visités.

    La moyenne sur un lot d'expérience EST la pondération par mu(s) :
    un état deux fois plus fréquent apparaît deux fois plus souvent dans le lot,
    donc son erreur pèse deux fois plus dans la somme. Personne n'écrit mu(s)
    dans le code ; c'est la provenance des données qui l'écrit.
    """
    estimations = reseau(etats_visites)
    return ((valeurs_vraies - estimations) ** 2).mean()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\hat v(s,\mathbf{w})\) | les valeurs approchées du lot | `estimations` |
| \(v_\pi(s)\) | les valeurs vraies, connues seulement sur un problème jouet | `valeurs_vraies` |
| \(\mu(s)\) | la distribution sur politique | la **fréquence des états dans le lot**, jamais écrite |
| \(\sum_s \mu(s)\,[\cdot]^2\) | l'objectif \(\overline{VE}(\mathbf{w})\) | `((...) ** 2).mean()` |

Je veux que vous reteniez la troisième ligne de ce tableau. \(\mu(s)\) n'est pas un hyperparamètre, ce n'est pas une variable, ce n'est même pas une ligne de code : c'est une propriété de **la façon dont vos données ont été produites**. Changer la politique qui collecte, changer la façon d'échantillonner dans un tampon, rejouer de vieilles transitions : chacune de ces décisions change \(\mu\), donc change l'objectif que votre optimiseur minimise réellement, et elle le change silencieusement. Vous ne verrez jamais cette modification dans votre code. Vous la verrez dans vos courbes.

---

## Deux honnêtetés qu'il faut garder en tête

Je ne vais pas vous vendre cet objectif plus qu'il ne vaut, parce que ses deux limites sont des informations utiles et que la seconde est le sujet de la section 5.6.

Première honnêteté : il n'est pas complètement clair que \(\overline{VE}\) soit le bon objectif pour l'apprentissage par renforcement. Notre but final est de trouver une **meilleure politique**, pas une meilleure estimation, et la meilleure fonction de valeur pour ce but n'est pas nécessairement celle qui minimise \(\overline{VE}\). C'est une réserve de fond, elle est reconnue comme telle, et elle reviendra en semaine 8 quand nous optimiserons directement la politique.

{{% comment %}}SOURCE: SB ch.9 p.222{{% /comment %}}

Seconde honnêteté, et elle est plus immédiatement pratique. Pour des approximateurs simples, on peut espérer atteindre un **optimum global** de \(\overline{VE}\). Pour des approximateurs complexes comme les réseaux de neurones, c'est rare, et le mieux que l'on puisse en général affirmer est la convergence vers un **optimum local**. Et ce n'est pas tout : certaines méthodes peuvent purement et simplement **diverger**, leur \(\overline{VE}\) tendant vers l'infini à la limite.

{{% comment %}}SOURCE: SB ch.9 p.222{{% /comment %}}

> [!WARNING]
 **Attention à cette dernière proposition : elle n'est pas une précaution de style, elle est un énoncé technique, et nous la vérifierons.** « Tendre vers l'infini » ne veut pas dire « converger lentement » ni « osciller autour de la solution ». Cela veut dire que les poids grandissent sans borne, pour **tout** pas d'apprentissage positif, aussi petit qu'on le choisisse. En section 5.6 vous ferez tourner cette divergence à la main, en douze lignes de Python et sans aucun réseau. Je préfère vous l'annoncer maintenant : la méthode que nous construisons cette semaine n'a pas de garantie de convergence, et ce n'est pas une lacune de ce cours, c'est l'état de la question.

Un dernier point, que je **plante** ici pour le récolter en 5.6. Les garanties de convergence dont nous disposons pour les méthodes d'approximation reposent sur une hypothèse précise : que les mises à jour suivent la **distribution sur politique**, celle que l'on vient de noter \(\mu\). Gardez cette condition en mémoire pendant quatre sections. Le tampon de rejeu de la section 5.7, qui est l'outil le plus utile de la semaine, est très exactement ce qui la viole.

{{% comment %}}SOURCE: SB ch.9 §9.4 (résumé de chapitre){{% /comment %}}

---
