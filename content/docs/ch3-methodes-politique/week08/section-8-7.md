---
title: "8.7 De la référence à l'avantage, puis au critique"
weight: 8
---

## La valeur de l'état est la référence naturelle, et elle porte un nom

Reprenons la mise à jour avec référence et posons \(b(s) = V(s)\), la valeur de l'état. L'échelle du gradient devient \(Q(s,a) - V(s)\). Cette quantité, vous l'avez déjà rencontrée, et elle a un nom depuis la semaine 6 : c'est l'**avantage** (*advantage*).

$$
\Adv(s,a) = q_\pi(s,a) - v_\pi(s), \qquad\text{autrement dit}\qquad q_\pi(s,a) = v_\pi(s) + \Adv(s,a)
$$

{{% comment %}}SOURCE: LAPAN ch.12 p.359{{% /comment %}}

C'est exactement la décomposition sur laquelle reposait l'architecture duale de la semaine 6, et c'est le même objet avec le même sens : **de combien l'action prise est meilleure, ou pire, que la moyenne des actions dans cet état**. Un avantage positif veut dire « cette action valait mieux que ce que cet état promettait », un avantage négatif veut dire l'inverse, et un avantage nul veut dire que l'action ne change rien. C'est aussi une **attribution du mérite** (*credit assignment*) beaucoup plus fine que le retour brut : avec \(G_t\), toute une trajectoire réussie voyait chacune de ses actions créditée du même bon résultat, y compris les mauvaises ; avec l'avantage, chaque action est jugée relativement à ce que son état promettait. Voilà précisément l'unité dans laquelle nous voulions que l'échelle du gradient s'exprime : un écart, centré, indépendant du niveau général des récompenses.

Il reste un obstacle, et il est le même que d'habitude : nous ne connaissons pas \(V(s)\). La réponse est aussi la même que d'habitude depuis la semaine 5 : nous l'**approchons avec un réseau**, entraîné exactement comme nous l'avons fait pour les valeurs d'action, en prenant un pas de Bellman et en minimisant une erreur quadratique moyenne. Nous passons donc d'une politique paramétrée à une politique paramétrée **plus** une valeur paramétrée, et c'est la structure finale de la semaine.

{{% comment %}}SOURCE: LAPAN ch.12 p.359{{% /comment %}}

Une écriture intermédiaire mérite d'être affichée, parce qu'elle fait le pont entre la formule d'un seul pas de temps de la section 8.2 et la perte sur un lot entier que nous écrirons en section 8.8. Le gradient de la performance s'exprime comme une espérance sur les **trajectoires**, avec l'avantage déjà en place de l'échelle :

$$
\nabla_{\theta} J(\pi_{\theta}) = \E_{\tau \sim \pi_{\theta}}\!\left[\sum_{t=0}^{T} \nabla_{\theta} \log \pi_{\theta}(a_t\mid s_t)\, A^{\pi_{\theta}}(s_t,a_t)\right]
$$

{{% comment %}}SOURCE: SPINUP vpg/key-equations{{% /comment %}}

Comparez cette expression à la dernière ligne de la dérivation de la section 8.2. Trois choses ont changé, et aucune n'est un changement de méthode : l'espérance porte sur une trajectoire entière \(\tau\) au lieu d'un pas de temps, la somme sur les pas est explicite, et le retour \(G_t\) a été remplacé par l'avantage. C'est la même quantité, écrite dans la forme où un programme l'implémente.

---

## Un algorithme complet, avec référence apprise

Nous avons maintenant assez de pièces pour écrire un algorithme complet, et il vaut la peine d'être écrit **avant** A2C, parce qu'il isole une seule nouveauté : la référence est apprise.

> **Le gradient de politique avec référence apprise**
>
> Pour chaque itération \(k\) :
>
> 1. Collecter un ensemble de trajectoires \(\mathcal{D}_k = \{\tau_i\}\) en jouant la politique \(\pi_{\theta_k}\).
> 2. Calculer les **retours restants** (*rewards-to-go*) \(\hat R_t\) de chaque pas de chaque trajectoire.
> 3. Calculer les estimations d'avantage \(\hat A_t\) à partir de la valeur courante \(\hat v(\cdot,\mathbf{w}_k)\).
> 4. Estimer le gradient de politique : \(\hat g_k = \dfrac{1}{|\mathcal D_k|}\sum_{\tau\in\mathcal D_k}\sum_{t=0}^{T}\nabla_\theta\log\pi_\theta(a_t\mid s_t)\big|_{\theta_k}\hat A_t\).
> 5. Mettre à jour la politique par **montée** de gradient, \(\theta_{k+1} = \theta_k + \alpha_k \hat g_k\), ou par un optimiseur comme Adam.
> 6. Ajuster la valeur par régression sur l'erreur quadratique :
>    \(\mathbf{w}_{k+1} = \argmin_{\mathbf{w}} \dfrac{1}{|\mathcal D_k|\,T}\sum_{\tau \in \mathcal{D}_k}\sum_{t=0}^{T}\big(\hat v(s_t,\mathbf{w}) - \hat R_t\big)^2\).
> 7. Recommencer.

{{% comment %}}SOURCE: SPINUP vpg/pseudocode{{% /comment %}}

Trois remarques, et la troisième est celle qui compte pour la suite de la semaine.

Premièrement, l'étape 5 est écrite en **montée**, avec un plus. C'est la forme mathématique honnête, et c'est la forme que votre code devra inverser, pour la raison exposée en section 8.3. Quand vous lirez un algorithme en montée et un code en descente, vous saurez où est passé le signe.

Deuxièmement, la valeur est ajustée à l'étape 6 par une **régression sur les retours restants observés** : la cible de cette régression est \(\hat R_t\), une quantité mesurée dans l'environnement, et non une prédiction du réseau. Il n'y a donc **aucun amorçage** dans cet algorithme, et retenez-le, parce que c'est exactement ce qui va changer dans deux paragraphes.

Troisièmement, cet algorithme n'a **pas** de terme d'entropie. Son exploration repose entièrement sur le caractère stochastique de la politique, avec la fragilité que la section 8.5 a décrite.

> [!IMPORTANT]
 **Les deux encadrés d'algorithme de cette semaine ne décrivent pas le même algorithme, et je préfère le dire ici plutôt que de vous laisser les confondre.** Celui que vous venez de lire ajuste sa valeur par régression sur des retours **observés**, et n'a pas de terme d'entropie. Celui de la section 8.8, A2C, ajuste sa valeur sur une cible **amorcée** à quatre pas, et ajoute un terme d'entropie. Ce sont deux points différents d'une même famille, et la différence entre les deux est le sujet des deux sous-sections qui suivent. Si l'on vous présente l'un comme le pseudocode de l'autre, c'est une imprécision.

---

## Une référence n'est pas un critique, et le mot qui les sépare est « amorçage »

Voici la distinction la plus nette de la semaine, et celle que les exposés rapides effacent le plus souvent.

L'algorithme ci-dessus apprend une politique **et** une fonction de valeur d'état. Il a donc tout l'air d'une méthode acteur-critique. Il n'en est pas une. La raison est précise : sa fonction de valeur sert **uniquement de référence**, jamais d'**amorçage**. Elle est soustraite de retours observés, et les retours observés, eux, ne la consultent pas. La valeur n'intervient jamais dans le calcul de la cible qui la définit.

{{% comment %}}SOURCE: SB ch.13 p.353{{% /comment %}}

Un critique, lui, est utilisé pour **estimer la cible elle-même**. Il remplace une partie du retour observé par sa propre prédiction. Et dès qu'on fait cela, on introduit deux choses que la référence n'introduisait pas : un **biais**, puisque la cible contient une estimation imparfaite, et une **dépendance asymptotique à la qualité de l'approximation**, puisque la limite de l'apprentissage dépend désormais de ce que le réseau de valeur est capable de représenter.

{{% comment %}}SOURCE: SB ch.13 p.353{{% /comment %}}

Alors pourquoi payer ce prix ? Parce qu'on achète en échange une réduction de variance et une accélération de l'apprentissage, et parce que les inconvénients de la pure méthode de Monte-Carlo sont réels. L'algorithme sans amorçage est **non biaisé** et converge asymptotiquement vers un minimum local ; mais comme toute méthode de Monte-Carlo, il apprend lentement, produit des estimations à forte variance, et se prête mal à un fonctionnement en ligne ou à un problème qui ne s'arrête jamais. Les méthodes de différence temporelle lèvent ces trois inconvénients, et c'est exactement l'arbitrage biais-variance de la semaine 7, reparu dans un autre vêtement.

{{% comment %}}SOURCE: SB ch.13 p.353{{% /comment %}}

> [!NOTE]
 **Le même arbitrage, trois fois dans ce cours.** En semaine 4, entre Monte-Carlo et TD(0) pour estimer une valeur : TD(0) amorce, donc biaise, et apprend plus vite. En semaine 6, avec la cible à \(n\) étapes : plus \(n\) est grand, moins on amorce, plus on est non biaisé, plus la variance monte. Et cette semaine, entre une référence et un critique. Ce n'est pas une coïncidence : c'est la même question posée à trois endroits, et c'est pourquoi je vous demande de retenir la frontière plutôt que la liste des méthodes. **Amorce-t-on ?** Si oui, biais et variance faible. Si non, pas de biais et variance élevée.

---

## Le pas acteur-critique à un pas, et une vieille connaissance au bout

Franchissons la frontière. Remplaçons le retour complet \(G_t\) par le retour à **un pas** \(G_{t:t+1}\), qui n'attend pas la fin de l'épisode mais consulte la valeur estimée de l'état suivant. C'est l'analogue exact, pour une politique, de ce que TD(0), Sarsa(0) et le Q-learning faisaient en semaine 4 pour une valeur : entièrement en ligne, entièrement incrémental, sans la machinerie des traces d'éligibilité.

{{% comment %}}SOURCE: SB ch.13 p.353{{% /comment %}}

Voici la chaîne de trois égalités, et je vous demande de regarder la troisième ligne avant de lire le commentaire.

$$
\begin{aligned}
\theta_{t+1} &\defeq \theta_t + \alpha\big(G_{t:t+1} - \hat v(S_t,\mathbf{w})\big)\dfrac{\nabla\pi(A_t\mid S_t,\theta_t)}{\pi(A_t\mid S_t,\theta_t)} \\[6pt]
&= \theta_t + \alpha\big(R_{t+1} + \gamma\hat v(S_{t+1},\mathbf{w}) - \hat v(S_t,\mathbf{w})\big)\dfrac{\nabla\pi(A_t\mid S_t,\theta_t)}{\pi(A_t\mid S_t,\theta_t)} \\[6pt]
&= \theta_t + \alpha\,\delta_t\,\dfrac{\nabla\pi(A_t\mid S_t,\theta_t)}{\pi(A_t\mid S_t,\theta_t)}
\end{aligned}
$$

{{% comment %}}SOURCE: SB éq. 13.12, 13.13, 13.14 p.353{{% /comment %}}

La première ligne est la mise à jour avec référence, où le retour complet a été remplacé par le retour à un pas. La deuxième développe \(G_{t:t+1} = R_{t+1} + \gamma \hat v(S_{t+1},\mathbf{w})\), c'est-à-dire la récompense réellement reçue plus la valeur estimée de la suite. Et la troisième est la chute : la parenthèse entière, \(R_{t+1} + \gamma\hat v(S_{t+1},\mathbf{w}) - \hat v(S_t,\mathbf{w})\), **est** l'erreur de différence temporelle \(\delta_t\) de la semaine 4, au caractère près, sans la moindre modification.

Prenez un instant pour mesurer ce que cela veut dire. Le pas acteur-critique à un pas est : **l'erreur de différence temporelle, multipliée par le vecteur d'éligibilité de la politique.** Rien de plus. L'objet que vous avez calculé des milliers de fois en semaine 4 pour corriger une table de valeurs sert ici, sans aucune adaptation, à pondérer un gradient de politique. C'est l'une des plus belles économies de tout le cours, et c'est aussi ce qui rend A2C implémentable en quelques dizaines de lignes.

Deux précisions pour terminer la section. Le partenaire naturel de cet acteur est le critique **semi-gradient TD(0)** de la semaine 5 : même cible amorcée, même erreur quadratique, même raison de ne pas dériver la cible. Et l'ensemble fonctionne **entièrement en ligne** : états, actions et récompenses sont traités à mesure qu'ils arrivent, et **jamais revisités**. Il existe bien sûr des généralisations, un retour à \(n\) pas au lieu d'un seul, un retour \(\lambda\), des traces d'éligibilité séparées pour l'acteur et le critique ; elles sont directes et nous n'en aurons pas besoin, à une exception près que la section 8.9 utilisera : le passage de un pas à \(N\) pas.

{{% comment %}}SOURCE: SB ch.13 p.353-354{{% /comment %}}

---
