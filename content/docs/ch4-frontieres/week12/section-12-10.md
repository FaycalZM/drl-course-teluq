---
title: "12.10 Un monde concret : quarante tigres et deux cent quatre cerfs"
weight: 11
---

## Des environnements multi-agents, et pourquoi ils sont rares

Première difficulté pratique, et elle explique le choix de ce qui suit : les environnements multi-agents sont **rares**. L'écosystème d'environnements que ce cours emploie depuis la semaine 1 est conçu pour **un** agent, de bout en bout, jusque dans la signature de `step()`. Il existe des versions à deux joueurs de certains jeux d'arcade, mais elles sont non standard. Il existe des interfaces vers des jeux de stratégie complets, et elles sont beaucoup trop complexes pour un premier pas.

{{% comment %}}SOURCE: LAPAN ch.22 p.676{{% /comment %}}

L'environnement retenu ici s'appelle **MAgent**, et il est maintenu par la Farama Foundation sous le nom de **MAgent2**, installable en une ligne avec `pip install magent2==0.3.3`. Il existe par ailleurs une interface unifiée pour les environnements multi-agents, **PettingZoo**, que ce cours nomme sans l'employer.

{{% comment %}}SOURCE: LAPAN ch.22 p.676-677{{% /comment %}}

> [!WARNING]
 **Ce paquet n'est pas vérifié sur Colab, et le laboratoire de cette semaine n'en dépend donc pas.** `magent2` embarque un cœur compilé en C++, sa version est épinglée, et ce cours **n'a pas vérifié** qu'il s'installe dans une session Colab gratuite. Je ne vais donc rien vous promettre à son sujet : la partie multi-agent du laboratoire est un exercice de **lecture et d'analyse**, pas un exercice d'entraînement, et le laboratoire le dit explicitement. Si vous parvenez à l'installer et que l'expérience vous tente, faites-le par curiosité, pas parce qu'un travail en dépend.

---

## Le monde, et ses règles de survie

Le monde est une **grille**, avec des murs infranchissables, peuplée de **groupes** d'agents. Chaque groupe a ses propres caractéristiques, toutes réglables : la portée de sa perception, la distance de ses déplacements, la distance de ses attaques, sa santé initiale, et ce que lui coûte en santé un pas de temps. Le cœur du simulateur est écrit en C++ avec une interface Python, ce qui lui permet de faire vivre des **milliers** d'agents dans la même grille.

{{% comment %}}SOURCE: LAPAN ch.22 p.676-679{{% /comment %}}

L'exemple que nous suivrons est un monde **prédateur-proie** : une forêt de **64 sur 64** cases, avec des murs, **40 tigres** et **204 cerfs**. Les règles qui comptent sont celles de l'économie de la santé, et il faut les avoir en tête pour comprendre les mesures :

| Règle | Valeur |
| --- | --- |
| Santé initiale d'un tigre | **10** |
| Santé qu'un tigre dépense par pas de temps | **0,5** |
| Santé gagnée par un tigre qui mange un cerf | **8** |
| Récompense d'un tigre | **+1 par pas de temps**, tant qu'il est vivant |
| Récompense d'un cerf | **+1 par pas de temps**, tant qu'il est vivant |
| Santé d'un cerf | diminue seulement quand il est attaqué, et remonte à chaque pas |

{{% comment %}}SOURCE: LAPAN ch.22 p.678{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.688 (image){{% /comment %}}

Deux remarques de conception sur ce tableau, parce que ce sont des décisions et non des données de la nature.

**La récompense d'un cerf est un choix, et il était nécessaire.** Donner \(+1\) par pas à un cerf lui fournit la seule chose qui puisse l'intéresser : une raison de rester en vie. Sans cela, un cerf n'a aucun objectif, et la moitié du monde serait composée d'agents indifférents à leur propre survie.

**La pression sur les tigres ne vient pas de leur récompense mais de leur métabolisme.** Un tigre reçoit \(+1\) par pas, exactement comme un cerf, donc sa récompense ne lui dit rien sur la chasse. Ce qui l'oblige à chasser, c'est que chaque pas lui coûte \(0{,}5\) de santé : dix de santé initiale, c'est **vingt pas** de vie, et un cerf mangé rapporte huit de santé, c'est-à-dire **seize pas** de plus. Un tigre qui ne chasse pas meurt au vingtième pas. Retenez ces deux divisions, nous en aurons besoin dans deux pages.

---

## Une interface qui n'est pas celle des onze semaines précédentes

**L'intuition.** Jusqu'ici, un appel à `step()` rendait un état, une récompense, deux drapeaux et un dictionnaire d'informations. Avec \(n_t\) agents, il faut rendre tout cela \(n_t\) fois, et il faut pouvoir dire de quel agent chaque valeur provient. D'où une interface entièrement faite de **dictionnaires indexés par un identifiant d'agent**, du genre `tiger_3` ou `deer_12`.

Concrètement, deux différences changent tout votre code de boucle. `reset()` ne rend **qu'une seule** valeur, un dictionnaire d'observations, et non un couple. Et `step()` rend **cinq** dictionnaires. À la réinitialisation, `env.agents` contient **244** entrées, soit les 40 tigres et les 204 cerfs.

{{% comment %}}SOURCE: LAPAN ch.22 p.679-681 (image 681){{% /comment %}}

Conséquence immédiate et agaçante : aucune des enveloppes d'environnement que vous employez depuis la semaine 1 ne fonctionne ici, puisqu'elles supposent toutes la signature standard. L'enregistrement vidéo d'un épisode, en particulier, doit être fait à la main, image par image, au lieu d'être branché comme une enveloppe.

{{% comment %}}SOURCE: LAPAN ch.22 p.680-681 (image 681){{% /comment %}}

**Le code.** Voici une boucle d'épisode complète, écrite sans aucune bibliothèque d'agents, avec les deux pièges signalés à l'endroit où ils mordent.

```python
def groupe_de(identifiant: str) -> str:
    """"tiger_3" -> "tiger". Le groupe est le prefixe de l'identifiant."""
    return identifiant.split("_")[0]


def jouer_un_episode(env, politiques, tampons):
    """politiques[groupe] : UNE politique par groupe, partagee par ses agents.
    tampons[groupe]      : un tampon de rejeu par groupe.
    """
    observations = env.reset()          # UNE seule valeur, un dictionnaire

    while env.agents:                   # n_t > 0 : l'episode dure tant qu'il reste des agents
        # On FIGE la liste des agents vivants : elle va changer pendant le pas.
        vivants = list(env.agents)
        precedentes = observations

        # Une action par agent vivant : l'action jointe A_t.
        actions = {
            i: politiques[groupe_de(i)].choisir(precedentes[i])
            for i in vivants
        }

        observations, recompenses, termines, tronques, infos = env.step(actions)

        for i in vivants:
            # Au pas ou un agent meurt, il est encore la, avec termines[i] a True.
            # Au pas SUIVANT il a disparu de tous les dictionnaires et de
            # env.agents, et l'episode continue sans lui.
            tampons[groupe_de(i)].ajouter(
                precedentes[i], actions[i], recompenses[i],
                termines[i], observations.get(i),
            )
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(i\) | indice d'agent | `i`, une chaîne comme `"tiger_3"` |
| \(n_t\) | nombre d'agents vivants au pas \(t\) | `len(env.agents)`, figé dans `vivants` |
| \(O^i_t\) | observation de l'agent \(i\) | `precedentes[i]` |
| \(A^i_t\) | action de l'agent \(i\) | `actions[i]` |
| \(\mathbf{A}_t\) | action jointe | le dictionnaire `actions` entier |
| \(R^i_{t+1}\) | récompense de l'agent \(i\) | `recompenses[i]` |
| \(O^i_{t+1}\) | observation suivante, **ou rien si l'agent a disparu** | `observations.get(i)` |
| \(\pi_\theta(a \mid o^i)\) | politique partagée du groupe de \(i\) | `politiques[groupe_de(i)]` |

---

## Une population volatile, et ce que cela impose

Je veux insister sur la ligne `vivants = list(env.agents)`, parce qu'elle est la trace d'une propriété que ce cours n'a **jamais** rencontrée en onze semaines.

Quand un agent meurt, son drapeau de terminaison passe à vrai, puis il **disparaît de tous les dictionnaires et de la liste des agents**, et **l'épisode continue**. Ce n'est pas une fin d'épisode : c'est la fin d'un agent dans un épisode qui se poursuit. Quarante tigres entrent, trois survivent, l'épisode tourne encore.

{{% comment %}}SOURCE: LAPAN ch.22 p.681 (image){{% /comment %}}

Trois conséquences pratiques, toutes dans votre boucle :

1. **Vous ne pouvez pas itérer sur une liste qui change.** D'où la copie figée avant le pas.
2. **Vous ne pouvez pas supposer qu'une clé présente avant le pas l'est encore après.** D'où l'accès prudent à l'observation suivante, et le fait qu'un agent mort n'a pas d'état suivant à ranger dans le tampon.
3. **Votre épisode ne se termine pas sur un drapeau mais sur un compte.** La condition de boucle est « il reste des agents », pas « l'environnement a dit que c'était fini ».

C'est là, concrètement, que \(n_t\) gagne son indice de temps.

---

## Une observation égocentrée et relative au groupe, et c'est l'idée à retenir

**L'intuition.** Quarante tigres partagent un seul réseau. Comment un même réseau peut-il produire une action utile pour quarante agents situés à quarante endroits différents ? En ne leur montrant jamais la grille : en montrant à chacun **son voisinage, lui au centre**.

C'est une observation **égocentrée** (*egocentric*), et elle est en plus **relative au groupe** (*group-relative*), ce qui est la seconde moitié de l'idée. Voici les dimensions :

| | Tigre | Cerf |
| --- | --- | --- |
| Observation | \((9, 9, 5)\) | \((3, 3, 5)\) |
| Actions | 9 : quatre déplacements, ne rien faire, quatre attaques | 5 : quatre déplacements, ne rien faire |
| Position de l'agent | au centre de sa fenêtre | au centre de sa fenêtre |

Et les **cinq plans**, dans l'ordre : les murs ; les agents **de mon groupe** ; la santé des agents de mon groupe ; les agents du groupe **adverse** ; la santé des agents du groupe adverse.

{{% comment %}}SOURCE: LAPAN ch.22 p.680{{% /comment %}}

> [!IMPORTANT]
 **Regardez ce que « mon groupe » et « le groupe adverse » permettent : une seule politique peut servir deux groupes opposés.** Les plans ne disent pas « les tigres » et « les cerfs », ils disent « les miens » et « les autres ». Un tigre et un cerf reçoivent donc des observations de **même sémantique**, et un réseau entraîné sur l'un n'est pas désorienté par l'autre. C'est exactement le procédé des deux plans de la section 12.4, où le réseau voyait « mes jetons, ses jetons » plutôt que « rouge, jaune », et c'est le même bénéfice : la symétrie est traitée dans l'encodage de l'observation, une fois, au lieu d'être apprise par le réseau, mille fois. Quand vous concevrez un environnement multi-agent, c'est la première décision à prendre, et elle est gratuite.

Une limite de cette conception mérite d'être nommée, parce qu'elle est probablement la contrainte dominante de l'expérience. Un tigre voit **neuf cases sur neuf** autour de lui, et rien d'autre. Sur une grille de 64 sur 64, c'est une fenêtre minuscule : un tigre ne sait pas où sont les cerfs, il ne peut que découvrir ceux qui entrent dans sa fenêtre. Le simulateur offre une **mini-carte** optionnelle, désactivée ici, qui ajouterait à l'observation une vue d'ensemble de la position des deux groupes. L'hypothèse, et je vous la donne pour ce qu'elle est, c'est-à-dire une hypothèse non vérifiée, est que cette vue limitée est ce qui plafonne la qualité de la politique des tigres. L'activer est l'une des expériences les plus intéressantes que l'on puisse faire sur cet environnement.

{{% comment %}}SOURCE: LAPAN ch.22 p.680{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.688 (image){{% /comment %}}

---

## Ce que fait un épisode purement aléatoire, et c'est une excellente mesure de référence

Avant tout entraînement, faisons agir les deux groupes **au hasard**. Cette mesure de référence est beaucoup plus informative que d'ordinaire, et je vous recommande de la garder en tête comme modèle de ce qu'une bonne référence doit faire.

Avec les deux groupes aléatoires, les tigres **meurent de faim**. L'épisode se termine en trente à quarante pas. La plupart des tigres vivent **vingt et un pas**, ce qui est exactement ce que prévoit l'arithmétique de la santé : dix de santé, un demi-point par pas, vingt pas, plus l'arrondi du dernier. Et le décompte final est sans appel : de **204 cerfs contre 40 tigres** au départ, on arrive à **201 cerfs contre 1 tigre**. Trois cerfs mangés sur deux cent quatre.

{{% comment %}}SOURCE: LAPAN ch.22 p.681-683 (images 681, 683){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.682{{% /comment %}}

La **Figure 12-4** montre deux instants de cette forêt, le début et la fin d'un tel épisode, et les deux décomptes sont inscrits dans l'image : c'est la seule image de monde multi-agent de cette semaine, et elle rend tangible ce que « plusieurs centaines d'agents dans une grille » veut dire.

{{< bookfig src="12-04.png" week="12" >}}

Ce que cette référence a de bon, et que je vous demande d'imiter dans vos propres mesures : elle ne donne pas un score, elle donne un **mécanisme**. Elle ne dit pas « le hasard obtient 19 points », elle dit « le hasard laisse les tigres mourir de faim au vingt et unième pas, et trois cerfs sont mangés sur deux cent quatre ». Un score ne vous apprend rien sur ce qu'il faudra améliorer ; un mécanisme, oui.

---

## Ce que fait un groupe entraîné, et l'arithmétique des cent cinquante-cinq cerfs

Entraînons maintenant les tigres, et eux seuls : les cerfs continuent d'agir au hasard. La méthode est celle de la semaine 5, une politique partagée par les quarante tigres, et l'entraînement dure environ **une heure** de processeur graphique. Le score de test atteint **82,89**.

{{% comment %}}SOURCE: LAPAN ch.22 p.688 (image){{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.22 p.690 (image){{% /comment %}}

Ce nombre ne veut rien dire tel quel, et c'est l'occasion d'un petit exercice que je veux faire avec vous, parce qu'il transforme un score opaque en un fait sur le monde. Souvenez-vous que la récompense d'un tigre est de \(+1\) **par pas de temps vécu**. Un score moyen de 82 signifie donc qu'un tigre a vécu environ **82 pas**. Or :

- sa santé initiale lui paie \(10 / 0{,}5 = \mathbf{20}\) pas de vie, et pas un de plus ;
- chaque cerf mangé lui paie \(8 / 0{,}5 = \mathbf{16}\) pas supplémentaires.

Donc les 40 tigres ont vécu, au total, \(82 \cdot 40 = 3\,280\) pas, dont \(20 \cdot 40 = 800\) leur étaient acquis sans chasser. L'excédent est de \(3\,280 - 800 = 2\,480\) pas, et il a forcément été payé en cerfs :

$$
\frac{2\,480}{16} \;=\; 155 \text{ cerfs mangés}, \qquad \frac{155}{204} \;\approx\; 76\,\%
$$

{{% comment %}}SOURCE: LAPAN ch.22 p.688 (image){{% /comment %}}

**Trois cerfs sur deux cent quatre au hasard, cent cinquante-cinq après une heure d'entraînement.** Voilà un résultat, et il est obtenu par la méthode de la semaine 5 appliquée sans modification, à ceci près que l'environnement rend des dictionnaires et que l'observation est égocentrée.

> [!TIP]
 **Gardez cette méthode de lecture, elle vaut mieux qu'un score.** Nous sommes partis d'un nombre sans signification, 82,89, et nous en avons tiré une proportion interprétable en nous servant uniquement de la structure de la récompense et de deux divisions. C'est faisable chaque fois que la récompense a une unité connue, et cela devrait être un réflexe : **demandez-vous toujours en quelle unité votre score est libellé**, puis convertissez-le en quelque chose que vous pouvez raconter. « Soixante-seize pour cent des proies chassées » se discute ; « 82,89 » ne se discute pas, il s'affiche.

---
