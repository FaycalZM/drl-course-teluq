---
title: "9.6 Trois correctifs, trois changements indépendants"
weight: 7
---

## Trois interventions sur la même boucle, et pas une méthode en bloc

Nous arrivons au cœur de la semaine, et je commence par une insistance qui va se répéter.

Ce que la section 9.5 a établi, c'est que la boucle de la section 9.3 a un défaut de direction : son critique se trompe par excès, et son acteur va chercher ces excès. Une campagne de mesure de 2018 a proposé **trois** réponses à ce défaut, et elles portent ensemble le nom de TD3 (*twin delayed deep deterministic policy gradient*), que l'on peut rendre en français par **gradient de politique déterministe profond jumelé et retardé**. Les trois réponses sont :

1. le **double Q écrêté** (*clipped double-Q*) : deux critiques, et la cible prend le plus petit des deux ;
2. la **mise à jour retardée de la politique** (*delayed policy updates*) : l'acteur et les réseaux cibles avancent moins souvent que les critiques ;
3. le **lissage de la politique cible** (*target policy smoothing*) : du bruit est ajouté à l'action cible avant de l'évaluer.

{{% comment %}}SOURCE: SPINUP td3/background{{% /comment %}}

La **Figure 9-4** place les trois interventions sur la boucle de la section 9.3, et je vous demande de la regarder avant de lire la suite : elle montre que les trois touchent **trois endroits différents** et qu'aucune ne dépend des deux autres.

{{< bookfig src="09-04.png" week="09" >}}

> [!IMPORTANT]
 **Ne lisez jamais ces trois correctifs comme une méthode indivisible, et je vais le répéter en fin de section.** Chacun des trois est un changement **indépendant** : on peut les activer séparément, dans n'importe quelle combinaison, et c'est exactement ce que l'ablation de la fin de cette section a mesuré, avec dix graines par configuration. Les résultats de cette ablation sont la moitié la plus intéressante du sujet, ils réservent deux surprises, et ils sont ce qui rend le laboratoire de cette semaine possible. Un étudiant qui retient « TD3 = DDPG + trois trucs » a retenu un nom ; un étudiant qui sait lequel des trois sert à quoi, et sur quelle tâche, a retenu la semaine.

Pourquoi la boucle de la section 9.3 a-t-elle besoin de tout cela ? Parce qu'elle est **fragile**, au sens précis suivant : son résultat dépend beaucoup des hyperparamètres et du réglage, et son mode de défaillance le plus courant est celui que la section 9.5 a décrit, un critique dont les valeurs s'emballent vers le haut, suivi d'une politique qui se casse parce qu'elle **exploite** les erreurs de ce critique. Le mot est bien choisi : l'acteur ne subit pas les erreurs du critique, il les cherche, puisque son métier est de trouver les actions les mieux notées.

{{% comment %}}SOURCE: SPINUP td3/background{{% /comment %}}

---

## Correctif 1 : le double Q écrêté

**L'intuition.** Entraînez **deux** critiques au lieu d'un, indépendamment initialisés, et pour calculer la cible, prenez la **plus petite** de leurs deux estimations. Deux estimateurs se trompent rarement par excès au même endroit : en prenant le minimum, on refuse de croire à un optimisme qui n'est pas confirmé par le second avis.

Avant d'écrire la formule, il faut comprendre pourquoi les deux réparations de la semaine 6 ne suffisent pas ici, parce que c'est ce qui justifie une troisième idée.

**Pourquoi le double DQN transplanté échoue.** Le principe du double DQN est de séparer le choix de l'action et son évaluation : le réseau en ligne choisit, le réseau cible évalue. Cela marche en discret parce que les deux réseaux diffèrent assez pour que leurs erreurs soient à peu près indépendantes. Dans un cadre acteur-critique, la politique change **lentement**, parce qu'elle avance par petits pas de gradient et parce qu'elle est elle-même suivie par un réseau cible en synchronisation douce. Le réseau courant et le réseau cible sont donc trop **semblables** pour fournir deux estimations indépendantes, et la séparation n'achète presque rien.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2{{% /comment %}}

**Pourquoi le double Q-learning complet ne suffit pas non plus.** On peut aller plus loin et entretenir deux acteurs et deux critiques, chaque critique servant à former la cible de l'autre. C'est mieux. Mais les deux critiques ne sont pas indépendants pour autant : ils apprennent sur le **même** tampon de rejeu, et chacun apparaît dans la cible de l'autre. Il en résulte que, pour certains états, le second critique note l'action du premier acteur **plus haut** que le premier critique ne le fait, et dans ce cas la construction croisée **aggrave** la surestimation au lieu de la corriger.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2{{% /comment %}}

**D'où le correctif.** Puisque le danger est qu'un critique moins biaisé serve de cible alors que l'autre est plus optimiste, il suffit de **borner par le haut** la valeur retenue par la plus pessimiste des deux. Borner par le haut avec le plus petit des deux nombres, c'est prendre le minimum :

$$
y_1 = r + \gamma \min_{i=1,2} q_{\mathbf{w}^-_i}\!\left(s', \mu_{\theta_1}(s')\right)
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2 (tex éq. 10){{% /comment %}}

Trois lectures de cette ligne, et la première est celle qu'on rate.

**Lecture 1 : la sous-estimation est volontaire.** Le minimum ne peut pas introduire plus de surestimation que la cible ordinaire, par construction. En revanche, il peut introduire une **sous-estimation**. Ce n'est pas un dégât collatéral, c'est un arbitrage explicite, et il est asymétrique pour une raison précise : la valeur d'une action **sous-estimée** n'est pas propagée par la mise à jour de la politique, puisque l'acteur s'en détourne et ne la rejoue plus, alors que la valeur d'une action **surestimée** est explicitement renforcée, puisque l'acteur y va. Une erreur par défaut s'oublie, une erreur par excès s'amplifie. On préfère donc, délibérément, se tromper vers le bas.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2{{% /comment %}}

**Lecture 2 : un effet secondaire bienvenu sur la variance.** L'espérance du minimum d'un ensemble de variables aléatoires **diminue** quand leur variance augmente. Prendre le minimum revient donc à préférer les états dont l'estimation de valeur est **peu dispersée**, ce qui donne des cibles plus stables et des mises à jour de politique plus prudentes. Le correctif 1 traite donc la surestimation **et** la variance, ce qui explique une partie de son poids dans l'ablation.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2{{% /comment %}}

**Lecture 3 : l'économie d'implémentation.** Dans l'équation ci-dessus, l'action vient de \(\mu_{\theta_1}\), c'est-à-dire d'un premier acteur, ce qui laisse croire qu'il en faut deux. Il n'en faut qu'**un**. L'algorithme final garde un seul acteur, optimisé contre le **premier** critique uniquement, et emploie la **même** cible pour les deux critiques. L'argument est direct : si le second critique annonce une valeur supérieure au premier, le minimum retient le premier et la mise à jour est identique à celle d'un critique unique, donc n'ajoute aucun biais ; et dans le cas contraire, la cible est bornée par le pessimiste, ce qui est l'effet voulu.

{{% comment %}}SOURCE: arXiv:1802.09477 §4.2 ; SPINUP td3/key-equations{{% /comment %}}

```python
# Deux critiques, un acteur. Les deux critiques partagent la MEME cible.
critique_1 = Critique(taille_obs, n_actions).to(device)
critique_2 = Critique(taille_obs, n_actions).to(device)

with torch.no_grad():
    q1_cible = critique_1_cible(etats_suiv_t, actions_cibles_t)
    q2_cible = critique_2_cible(etats_suiv_t, actions_cibles_t)
    q_min = torch.min(q1_cible, q2_cible)          # LE correctif, en un appel
    q_min[termines_t] = 0.0                        # un etat terminal vaut zero
    cible = recompenses_t + gamma * q_min

perte_critiques = F.mse_loss(critique_1(etats_t, actions_t), cible) \
                + F.mse_loss(critique_2(etats_t, actions_t), cible)

# L'acteur, lui, n'escalade QUE le premier critique.
perte_acteur = -critique_1(etats_t, acteur(etats_t)).mean()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(q_{\mathbf{w}_1}\), \(q_{\mathbf{w}_2}\) | les deux **critiques jumeaux** (*twin critics*) | `critique_1`, `critique_2` |
| \(\mathbf{w}^-_1\), \(\mathbf{w}^-_2\) | leurs deux réseaux cibles | `critique_1_cible`, `critique_2_cible` |
| \(\min_{i=1,2}\) | le double Q écrêté | `torch.min(q1_cible, q2_cible)` |
| \(y\) | la cible, **commune aux deux critiques** | `cible` |
| \(\mu_\theta\) | l'acteur unique, entraîné contre \(q_{\mathbf{w}_1}\) | `acteur` |

---

## Correctif 2 : la mise à jour retardée de la politique

**L'intuition**, et elle découle directement de l'expérience sur les réseaux cibles de la fin de la section 9.5. Si un réseau cible sert à réduire l'erreur sur plusieurs mises à jour, et si une mise à jour de politique effectuée sur des états à forte erreur conduit à la divergence, alors la politique doit avancer **moins souvent** que la fonction de valeur : il faut d'abord réduire l'erreur, et seulement ensuite bouger la politique.

La réalisation est d'une simplicité presque décevante : on ne met à jour l'acteur et les réseaux cibles qu'**une fois sur \(d\)** mises à jour du critique. Le choix retenu est \(d = 2\).

{{% comment %}}SOURCE: arXiv:1802.09477 §5.2{{% /comment %}}

```python
# A l'interieur de la boucle de mise a jour, apres le pas des critiques :
compteur += 1
if compteur % d == 0:                  # d = 2
    perte_acteur = -critique_1(etats_t, acteur(etats_t)).mean()
    opt_acteur.zero_grad()
    perte_acteur.backward()
    opt_acteur.step()

    # LES RESEAUX CIBLES AVANCENT DANS CETTE BRANCHE AUSSI, pas en dehors.
    synchroniser_doucement(acteur, acteur_cible, tau)
    synchroniser_doucement(critique_1, critique_1_cible, tau)
    synchroniser_doucement(critique_2, critique_2_cible, tau)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(d\) | délai de politique, \(d=2\) | `d`, `policy_delay` |
| compteur de mises à jour | ce que l'on compte modulo \(d\) | `compteur` |
| \(\tau\) | taux de synchronisation douce, 0,005 | `tau` |

Deux remarques qui valent chacune un point d'examen. **Première remarque :** les réseaux cibles avancent **à l'intérieur** de la branche retardée, et non en dehors. Ce n'est pas un détail d'écriture : cibler plus souvent que l'on ne met à jour la politique reviendrait à annuler une partie de l'effet recherché, puisque la cible se remettrait à suivre un critique dont l'erreur n'a pas encore été réduite. **Seconde remarque :** c'est un algorithme à **deux échelles de temps**, une structure que la théorie de la convergence réclame fréquemment dans le cadre linéaire. Vous avez donc ici un cas rare et agréable : un correctif purement pratique qui se trouve avoir un pedigree théorique.

{{% comment %}}SOURCE: arXiv:1802.09477 §5.2{{% /comment %}}

Et un résultat contre-intuitif à retenir : ce correctif **améliore généralement** la performance **tout en réduisant** le temps d'entraînement, alors même que l'acteur s'entraîne deux fois moins souvent. Moins de travail, et un meilleur résultat : c'est la signature d'un problème où l'on allait trop vite.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.2{{% /comment %}}

---

## Correctif 3 : le lissage de la politique cible

**L'intuition**, et c'est ma favorite des trois. Une politique déterministe a un défaut structurel : elle peut **surapprendre un pic étroit** de l'estimation de valeur. Si votre critique porte, par accident d'approximation, une petite bosse à une action particulière, l'acteur y marchera tout droit, et rien ne l'en empêchera, puisque son unique métier est de monter. Le pic est un artefact, mais l'acteur n'a aucun moyen de le savoir.

{{% comment %}}SOURCE: arXiv:1802.09477 §5.3{{% /comment %}}

La réponse est de **flouter la cible** : au lieu d'évaluer la valeur de l'action cible exacte, on évalue la valeur **moyenne d'un petit voisinage** autour d'elle. Un pic d'une largeur d'un centième d'unité survit mal à une moyenne prise sur un voisinage dix fois plus large, alors qu'un véritable maximum, large et régulier, y survit très bien. C'est un **régularisateur**, et il impose au critique une contrainte parfaitement explicite : des actions semblables doivent avoir des valeurs semblables.

La forme idéale est une espérance sur le bruit :

$$
y = r + \E_{\tilde\epsilon}\left[\, q_{\mathbf{w}^-}\!\left(s', \mu_{\theta^-}(s') + \tilde\epsilon\right) \,\right]
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §5.3 (tex éq. 13){{% /comment %}}

Cette espérance n'est pas calculable, et on l'approche par **un seul tirage**, avec un écrêtage du bruit pour garantir que le voisinage reste petit :

$$
y = r + \gamma\, q_{\mathbf{w}^-}\!\left(s', \mu_{\theta^-}(s') + \tilde\epsilon\right), \qquad \tilde\epsilon \sim \operatorname{clip}\!\left(\mathcal{N}(0,\sigma),\, -c,\, c\right)
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §5.3 (tex éq. 14){{% /comment %}}

Trois précisions, chacune utile.

**Première précision : l'écrêtage du bruit n'est pas optionnel.** Sans la borne \(\pm c\), un tirage normal peut produire occasionnellement une action cible très éloignée, voire hors de l'espace d'actions, et la cible évaluerait alors la valeur d'une action que l'acteur ne jouerait jamais. L'écrêtage du bruit maintient le voisinage à sa taille voulue, et c'est le deuxième des trois écrêtages de la semaine. Les réglages employés sont \(\sigma = 0{,}2\) et \(c = 0{,}5\) : pour des actions normalisées dans \([-1,1]\), le voisinage ne dépasse donc jamais le quart de l'étendue totale.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.1{{% /comment %}}

**Deuxième précision : ce bruit n'est pas le bruit d'exploration.** Le bruit \(\tilde\epsilon\) de cette formule est ajouté à l'action **cible**, à l'intérieur du calcul de la cible, pendant la mise à jour, et il n'est jamais envoyé à l'environnement. Le bruit \(\epsilon\) de la section 9.4 est ajouté à l'action **jouée** et ne touche jamais la cible. Les deux sont tirés indépendamment, et leurs amplitudes sont réglées indépendamment : 0,1 pour l'exploration, 0,2 pour le lissage. Deux bruits, deux métiers, et c'est pour éviter la confusion que j'écris le second \(\tilde\epsilon\) et non \(\epsilon\).

{{% comment %}}SOURCE: arXiv:1802.09477 §5.3, §6.1{{% /comment %}}

**Troisième précision : la parenté avec les méthodes tabulaires de SCI1060.** Évaluer la cible en une action légèrement perturbée, c'est faire ce que fait une mise à jour SARSA, qui évalue l'action réellement jouée au lieu de la meilleure ; et moyenner sur le voisinage, c'est l'esprit de SARSA espéré, qui moyenne sur la distribution des actions. La différence, et elle est jolie, est que ce lissage s'obtient ici **hors politique**, par un bruit ajouté dans le calcul de la cible, sans jamais changer la façon dont les transitions ont été collectées.

{{% comment %}}SOURCE: arXiv:1802.09477 §5.3{{% /comment %}}

---

## La cible complète, et quatre endroits où les écritures divergent

Combinez les correctifs 1 et 3, et vous obtenez la cible complète de la méthode :

$$
y = r + \gamma \min_{i=1,2} q_{\mathbf{w}^-_i}\!\left(s', \mu_{\theta^-}(s') + \tilde\epsilon\right), \qquad \tilde\epsilon \sim \operatorname{clip}\!\left(\mathcal{N}(0,\sigma),\, -c,\, c\right)
$$

{{% comment %}}SOURCE: arXiv:1802.09477 §6 (tex éq. 15){{% /comment %}}

Le correctif 2, lui, n'apparaît pas dans la cible : il vit dans la boucle, comme un compteur.

Maintenant, un point de méthode qui compte au moins autant que les équations. Vous allez trouver, dans les implémentations publiques, des formes qui ne coïncident pas tout à fait avec celles que je viens d'écrire, et je préfère vous les montrer plutôt que de vous laisser croire à une erreur. Les implémentations calculent d'abord l'action cible, en **écrêtant le résultat** aux bornes de l'espace d'actions :

$$
a'(s') = \operatorname{clip}\!\left( \mu_{\theta^-}(s') + \operatorname{clip}(\tilde\epsilon, -c, c),\; a_{\min},\, a_{\max} \right), \qquad \tilde\epsilon \sim \mathcal{N}(0,\sigma)
$$

$$
y = r + \gamma\,(1-d_{\text{term}}) \min_{i=1,2} q_{\mathbf{w}^-_i}\!\left(s', a'(s')\right)
$$

{{% comment %}}SOURCE: SPINUP td3/key-equations{{% /comment %}}

Comparez ligne à ligne avec les équations précédentes, et vous verrez deux ajouts : un **écrêtage de l'action** cible aux bornes de l'environnement, et un facteur terminal. Voici les quatre divergences recensées, avec la position du cours sur chacune :

| Objet | Ce que les équations écrivent | Ce que les implémentations ajoutent | Position du cours |
| --- | --- | --- | --- |
| Action cible | bruit écrêté à \(\pm c\), **l'action résultante n'est pas écrêtée** | un écrêtage de l'action supplémentaire aux bornes \([a_{\min}, a_{\max}]\) | enseigner la forme des équations, et **ajouter** l'écrêtage de l'action en pratique : une action cible hors bornes est une action que le critique n'a jamais vue en entraînement |
| État terminal | rien : les équations s'écrivent \(y = r + \gamma\min_i q\) | un facteur \((1-d_{\text{term}})\) dans toutes les cibles | le facteur est **nécessaire** et les équations abrègent ; le cours garde la forme à deux cas de la semaine 5, qui dit la même chose sans introduire une lettre de plus |
| Ce que compte le délai | le **pas d'environnement**, avec une mise à jour de critique par pas | l'**indice de mise à jour** à l'intérieur d'un bloc de mises à jour | les deux expriment la même intention ; il faut **choisir et le dire** : le laboratoire compte les mises à jour du critique |
| Sens du paramètre de synchronisation douce | \(\tau\) petit, fraction du nouveau réseau | un paramètre complémentaire proche de 1 selon les bibliothèques | convertir une fois, dans le tableau de symboles, et ne plus y revenir |

> [!NOTE]
 **La règle que j'applique, et que je vous demande d'appliquer.** Quand deux écritures d'une même méthode diffèrent, l'écriture **mathématique** est l'autorité et l'écriture **algorithmique** est un commentaire, parce que la seconde a été produite pour être exécutable et porte donc des précautions d'ingénierie que la première passe sous silence. Mais un commentaire peut être juste là où l'autorité abrège : le facteur terminal en est l'exemple parfait, puisqu'il est indispensable et absent des équations. La discipline n'est donc pas de choisir un camp, c'est de **dire laquelle des deux on montre** et de ne jamais les fondre silencieusement en une troisième écriture qui ne serait ni l'une ni l'autre.

Une dernière précision d'architecture, et elle est facile à rater : dans la configuration mesurée ci-dessous, le critique reçoit l'état **et** l'action **dès la première couche**, alors que l'implémentation historique de la section 9.3 fait entrer l'action au deuxième étage, comme la Figure 9-3 le montre. C'est l'un des éléments du réglage qui, vous allez le voir dans l'ablation, pèse étonnamment lourd.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.1{{% /comment %}}

---

## L'algorithme complet

Voici la boucle entière, les trois correctifs en place. Je l'écris en français, dans la continuité des neuf étapes de la section 9.3, pour que vous puissiez mesurer **exactement** ce qui a changé.

```
 1. Initialiser l'acteur mu_theta et les DEUX critiques q_w1, q_w2
 2. Recopier leurs poids dans l'acteur cible et les deux critiques cibles
 3. Jouer un pas : a = ecretage( mu_theta(s) + bruit d'exploration )
    (pendant les premiers pas : action uniforme dans l'espace d'actions)
 4. Ranger (s, a, r, s', terminal) dans le tampon D
 5. Tirer un lot B dans D, uniformement
 6. Action cible, AVEC lissage :
        bruit  <- ecretage( N(0, sigma), -c, +c )          <- correctif 3
        a'     <- ecretage( mu_{theta-}(s') + bruit, a_min, a_max )
 7. Cible COMMUNE aux deux critiques :
        y = r                                              si s' est terminal
        y = r + gamma * min( q_{w1-}(s',a'), q_{w2-}(s',a') )   sinon
                                                           <- correctif 1
 8. Pas des deux critiques : minimiser  ( q_w1(s,a) - y )^2 + ( q_w2(s,a) - y )^2
 9. UNE FOIS SUR d SEULEMENT :                             <- correctif 2
      9a. Pas de l'acteur : minimiser  - q_w1( s, mu_theta(s) )
      9b. Synchronisation douce des TROIS reseaux cibles, avec tau
10. Revenir a l'etape 3
```

{{% comment %}}SOURCE: arXiv:1802.09477 Algorithm 1 p.5 ; SPINUP td3/pseudocode{{% /comment %}}

Mettez cette boucle à côté de celle de la section 9.3 et comptez les différences : il y en a trois, aux étapes 6, 7 et 9, et elles correspondent une pour une aux trois correctifs. Tout le reste, y compris le tampon de rejeu, le bruit d'exploration, le détachement de la cible et la synchronisation douce, est inchangé. C'est précisément ce que signifie « trois changements indépendants ».

```python
def un_pas_de_mise_a_jour(lot, reseaux, opts, hp, compteur):
    """Un pas complet : critiques toujours, acteur et cibles une fois sur d."""
    etats, actions, recompenses, etats_suiv, termines = lot

    # --- Correctifs 3 puis 1 : l'action cible est lissee, la cible est le min.
    with torch.no_grad():
        bruit = (torch.randn_like(actions) * hp.sigma).clamp(-hp.c, hp.c)
        actions_cibles = (reseaux.acteur_cible(etats_suiv) + bruit).clamp(
            hp.a_min, hp.a_max
        )
        q_min = torch.min(
            reseaux.critique_1_cible(etats_suiv, actions_cibles),
            reseaux.critique_2_cible(etats_suiv, actions_cibles),
        ).squeeze(-1)
        q_min[termines] = 0.0
        cible = (recompenses + hp.gamma * q_min).unsqueeze(-1)

    perte_critiques = (
        F.mse_loss(reseaux.critique_1(etats, actions), cible)
        + F.mse_loss(reseaux.critique_2(etats, actions), cible)
    )
    opts.critiques.zero_grad()
    perte_critiques.backward()
    opts.critiques.step()

    # --- Correctif 2 : l'acteur et les cibles n'avancent qu'une fois sur d.
    perte_acteur = None
    if compteur % hp.d == 0:
        perte_acteur = -reseaux.critique_1(etats, reseaux.acteur(etats)).mean()
        opts.acteur.zero_grad()
        perte_acteur.backward()
        opts.acteur.step()

        for reseau, cible_reseau in reseaux.paires_cibles():
            synchroniser_doucement(reseau, cible_reseau, hp.tau)

    return perte_critiques.item(), perte_acteur
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\tilde\epsilon \sim \operatorname{clip}(\mathcal{N}(0,\sigma),-c,c)\) | bruit de lissage, écrêtage du bruit inclus | `bruit` |
| \(a'(s')\) | action cible lissée puis soumise à l'écrêtage de l'action | `actions_cibles` |
| \(\min_{i=1,2} q_{\mathbf{w}^-_i}\) | double Q écrêté | `torch.min(...)` |
| \(y\) | cible commune aux deux critiques | `cible` |
| \(d\) | délai de politique | `hp.d` |
| \(\tau\) | synchronisation douce des trois réseaux cibles | `hp.tau` |
| \(\sigma\), \(c\) | échelle du bruit de lissage et sa borne d'écrêtage | `hp.sigma`, `hp.c` |

Les réglages complets, pour mémoire, parce qu'ils forment un ensemble cohérent qu'il vaut mieux reprendre en bloc que bricoler : bruit de lissage \(\mathcal{N}(0; 0{,}2)\) écrêté à \((-0{,}5; 0{,}5)\) ; délai \(d = 2\) ; \(\tau = 0{,}005\) pour tous les réseaux cibles ; bruit d'exploration \(\mathcal{N}(0; 0{,}1)\) ; optimiseur Adam au pas \(10^{-3}\) ; lots de 100 transitions tirés uniformément dans un tampon qui conserve **tout** l'historique de l'agent ; réseaux à deux couches cachées de 400 et 300 unités avec ReLU, et tangente hyperbolique en sortie de l'acteur.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.1{{% /comment %}}

---

## L'étude d'ablation, et les trois lectures à ne pas manquer

Nous arrivons à ce que je considère comme la partie la plus instructive de la semaine, et elle est expérimentale.

**Le protocole d'abord**, parce qu'il est exemplaire et qu'il vous est familier : un million de pas de temps par tâche ; une évaluation tous les 5 000 pas ; chaque évaluation est la moyenne de dix épisodes joués **sans bruit d'exploration** ; et chaque configuration est rejouée sur **dix graines aléatoires**, du simulateur comme de l'initialisation des réseaux. Vous reconnaissez le protocole que la semaine 7 vous a imposé, et je voudrais que vous notiez ceci : ce n'est pas une exigence inventée par ce cours pour vous faire travailler, c'est le standard d'un travail publié sérieux.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.1{{% /comment %}}

Premier tableau, la comparaison d'ensemble sur quatre tâches de locomotion simulée. Les colonnes sont, dans l'ordre : la méthode complète aux trois correctifs, la version publiée de la méthode de la section 9.3, et cette même méthode **re-réglée** avec l'architecture, les hyperparamètres et le bruit d'exploration de la configuration mesurée, mais **sans aucun** des trois correctifs.

**Tableau 9-1.** Meilleur retour moyen sur dix exécutions d'un million de pas ; l'intervalle est un écart-type entre exécutions. En gras, le meilleur résultat de chaque ligne.

| Tâche | Trois correctifs | Section 9.3, version publiée | Section 9.3, re-réglée |
| --- | --- | --- | --- |
| HalfCheetah | **9 636,95** ± 859,07 | 3 305,60 | 8 577,29 |
| Hopper | **3 564,07** ± 114,74 | 2 020,46 | 1 860,02 |
| Walker2d | **4 682,82** ± 539,64 | 1 843,85 | 3 098,11 |
| Ant | **4 372,44** ± 1 000,33 | 1 005,30 | 888,77 |

{{% comment %}}SOURCE: arXiv:1802.09477 Table 1 p.7{{% /comment %}}

Second tableau, l'ablation proprement dite : la moyenne des dix dernières évaluations, dix exécutions, un million de pas. La ligne « réglage seul » désigne la configuration re-réglée sans aucun correctif ; les lignes « + » ajoutent un seul correctif à celle-ci ; les lignes « moins » retirent un seul correctif de la méthode complète.

**Tableau 9-2.** Étude d'ablation des trois correctifs. En gras, le meilleur résultat de chaque colonne.

| Configuration | HalfCheetah | Hopper | Walker2d | Ant |
| --- | --- | --- | --- | --- |
| Les trois correctifs | 9 532,99 | **3 304,75** | 4 565,24 | **4 185,06** |
| Section 9.3, version publiée | 3 162,50 | 1 731,94 | 1 520,90 | 816,35 |
| Réglage seul, aucun correctif | 8 401,02 | 1 061,77 | 2 362,13 | 564,07 |
| Réglage + mise à jour retardée | 7 588,64 | 1 465,11 | 2 459,53 | 896,13 |
| Réglage + lissage de la cible | 9 023,40 | 907,56 | 2 961,36 | 872,17 |
| Réglage + double Q écrêté | 6 470,20 | 1 134,14 | 3 979,21 | 3 818,71 |
| Les trois, moins la mise à jour retardée | 9 590,65 | 2 407,42 | **4 695,50** | 3 754,26 |
| Les trois, moins le lissage de la cible | 8 987,69 | 2 392,59 | 4 033,67 | 4 155,24 |
| Les trois, moins le double Q écrêté | 9 792,80 | 1 837,32 | 2 579,39 | 849,75 |
| Variante à double Q complet | 9 433,87 | 1 773,71 | 3 100,45 | 2 445,97 |
| Variante à double DQN transplanté | **10 306,90** | 2 155,75 | 3 116,81 | 1 092,18 |

{{% comment %}}SOURCE: arXiv:1802.09477 Table 2 p.8{{% /comment %}}

Commençons par la lecture prudente, celle que ces chiffres autorisent et pas une ligne de plus : l'importance de chaque composant **varie d'une tâche à l'autre** ; l'ajout d'un seul composant ne produit, dans la plupart des cas, qu'une amélioration peu significative ; ce sont les **combinaisons** qui produisent un saut net ; et la méthode complète dépasse toutes les autres combinaisons sur la plupart des tâches. Pas sur toutes : sur la plupart.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.2{{% /comment %}}

Maintenant les trois lectures que je veux enseigner explicitement, parce qu'elles sont dans le tableau et qu'on les saute.

**Première lecture : retirer un correctif améliore parfois le résultat.** Regardez la ligne « les trois, moins le double Q écrêté ». Sur Ant, elle fait tomber le score de 4 185 à 850, soit une perte de presque tout ; sur Walker2d, de 4 565 à 2 579, soit une perte de la moitié ; et sur HalfCheetah, elle **monte**, de 9 533 à 9 793. Ce n'est pas du bruit de mesure déguisé, c'est le comportement attendu d'un correctif qui échange de la surestimation contre de la sous-estimation : là où la surestimation ne nuit pas, payer une sous-estimation est une perte sèche. Notez d'ailleurs que, sur Ant, **toutes** les configurations qui réduisent la surestimation font un bond, ce qui identifie cette tâche comme celle où le défaut de la section 9.5 mord le plus fort. Vous avez déjà vu ce raisonnement en semaine 6, avec un double DQN qui réduisait la surestimation sans accélérer l'apprentissage sur un jeu donné : une réparation correcte n'est pas une réparation utile partout.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.2 ; Table 2 p.8{{% /comment %}}

**Deuxième lecture, et c'est la plus dérangeante : sur une tâche, le simple réglage bat n'importe quel correctif isolé.** Sur HalfCheetah, la configuration « réglage seul », qui ne contient **aucun** des trois correctifs et ne diffère de la version publiée que par l'architecture, les hyperparamètres et le bruit d'exploration, obtient 8 401 contre 3 163. L'écart gagné par le réglage seul est donc de plus de 5 200 points, quand l'ajout du meilleur des trois correctifs à cette configuration en ajoute au mieux 600. Conclusion honnête, et je l'assume : une bonne part de la réputation de fragilité de la méthode de la section 9.3 est une affaire de **réglage**, et les trois correctifs comptent là où la surestimation nuit réellement, ce qui n'est pas partout.

{{% comment %}}SOURCE: arXiv:1802.09477 Table 2 p.8{{% /comment %}}

**Troisième lecture : les deux transplantations de la semaine 6 ne sont pas ridicules.** Les deux dernières lignes du tableau sont les variantes mesurées en section 9.5 : le double Q-learning complet et le double DQN transplanté. Elles ne sont ni absurdes ni dominantes ; sur HalfCheetah, la seconde donne même le meilleur score de tout le tableau. Mais regardez leur colonne Ant, 2 446 et 1 092 contre 4 185 : elles n'offrent qu'une amélioration peu significative par rapport au retrait du double Q écrêté, ce qui est l'écho expérimental exact de la mesure de surestimation de la section 9.5. Les deux moitiés du raisonnement, le mécanisme et la mesure, se recoupent, et c'est cela qui rend l'argument solide.

{{% comment %}}SOURCE: arXiv:1802.09477 §6.2{{% /comment %}}

> [!IMPORTANT]
 **Et voici la raison expérimentale de choisir `Pendulum-v1` pour le laboratoire, promise en section 9.1.** La même campagne de mesure a porté sur d'autres tâches que les quatre ci-dessus, et l'une d'elles est un pendule inversé simulé sous MuJoCo. Sur cette tâche-là, la méthode complète, la méthode de la section 9.3, sa version re-réglée, et trois autres familles de méthodes obtiennent **toutes exactement 1 000,00**, c'est-à-dire le maximum atteignable. La tâche **sature**. Une étude d'ablation menée sur un banc d'essai saturé ne mesure strictement rien : toutes vos configurations donneront le même nombre, et vous concluerez, à tort, que les trois correctifs ne servent à rien. Choisir sa tâche de mesure est une décision expérimentale à part entière, et le critère est qu'elle doit **séparer** les configurations que l'on compare. Voilà pourquoi le laboratoire mesure sur `Pendulum-v1`, et pourquoi il ne mesure pas sur `InvertedPendulum-v5`.

{{% comment %}}SOURCE: arXiv:1802.09477 Table 1 p.7{{% /comment %}}

---
