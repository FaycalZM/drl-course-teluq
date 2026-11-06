---
title: "Notation"
weight: 1
---

# Notation du cours

Une seule notation, de la semaine 1 à la semaine 15, et elle prolonge celle de SCI1060 :
les symboles que vous avez appris en apprentissage par renforcement classique gardent ici
exactement le même sens, et le cours n'en change jamais en route. Cette page est la table
unique des symboles, et elle **fait foi**. Au moindre doute sur une lettre, c'est ici qu'il
faut revenir plutôt que de reconstituer le sens d'après le contexte.

Vous rencontrerez ailleurs, dans les implémentations comme dans les textes du domaine,
d'autres conventions pour les mêmes objets. Elles ne sont pas fautives, elles sont
différentes, et confondre deux conventions coûte en général une demi-journée. La dernière
section de cette page traduit les plus fréquentes.

> [!TIP]
 **Comment lire cette page.** Les symboles sont rangés par famille : les objets du
 processus de décision, puis les retours et les valeurs, puis les politiques, puis
 l'apprentissage, puis les quantités qui n'apparaissent que dans une ou deux semaines. Si
 vous cherchez une lettre précise, la fonction de recherche de votre navigateur est plus
 rapide que la lecture : toutes les familles sont sur cette seule page. Et si une lettre
 semble en porter deux sens, elle est très probablement dans l'avant-dernière section, qui
 ne contient que cela.

---

## Les conventions générales

Quatre règles valent partout, et les trois premières ont une conséquence immédiate à la
lecture d'une équation.

**Minuscule contre majuscule.** Les minuscules \(v_\pi\) et \(q_\pi\) désignent les valeurs
**vraies**, celles que l'on cherche sans jamais les connaître ; les majuscules \(V\) et
\(Q\) désignent des **estimations**, c'est-à-dire un tableau en mémoire ou la sortie d'un
réseau. La distinction porte tout le passage du tabulaire à l'approché, en semaine 5.

**Les vecteurs sont des colonnes.** Une matrice de poids multiplie donc à **gauche** :
pour une entrée \(\mathbf{x} \in \mathbb{R}^{d}\), une couche cachée de \(h\) unités et
\(q\) sorties, \(\mathbf{W}^{(1)} \in \mathbb{R}^{h \times d}\) et
\(\mathbf{W}^{(2)} \in \mathbb{R}^{q \times h}\). Vous croiserez ailleurs la convention
ligne, où les mêmes matrices sont transposées.

**Une récompense n'est pas un retour.** \(R_t\) est la récompense **d'un seul pas** ; le
total d'un épisode, actualisé ou non, s'écrit \(G\). L'inversion des deux est une source
d'erreurs tenace, parce qu'un retour qui vaut 475 ne ressemble en rien à une récompense qui
vaut 1.

**Le symbole \(\doteq\) signifie « défini comme »**, par opposition à une égalité que l'on
démontre. Et le logarithme naturel s'écrit \(\log\) jusqu'à la semaine 8, \(\ln\) à partir
de la semaine 9, où les densités gaussiennes rendent cette seconde forme plus lisible : les
deux désignent le même logarithme.

---

## Le processus de décision : états, actions, récompenses

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(S_t\) | état de l'environnement à l'instant \(t\) | |
| \(O_t\) | **observation** reçue par l'agent, éventuellement plus pauvre que l'état | `obs` |
| \(A_t\) | action jouée à l'instant \(t\) | `action` |
| \(R_t\) | récompense d'un pas | `reward` |
| \(t\), \(T\) | pas de temps courant ; pas terminal de l'épisode | |
| \(\mathcal{S}\) | ensemble des états | `observation_space` |
| \(\mathcal{A}(s)\) | actions disponibles dans l'état \(s\) | `action_space` |
| \(\mathcal{R}\) | ensemble des récompenses possibles | |
| \(p(s',r \mid s,a)\) | **dynamique** de l'environnement, à quatre arguments | |
| \(p(s' \mid s,a)\), \(r(s,a)\) | transition et récompense espérée, formes dérivées de la précédente | |

La dynamique \(p\) est l'objet que l'on possède en semaine 4 et que l'on perd dès la
semaine suivante : toutes les méthodes sans modèle du cours sont précisément celles qui ne
l'écrivent nulle part. Quand une loi porte un indice de paramètres, \(p_\theta\), c'est une
dynamique **apprise** et non la vraie : l'indice est toute la différence.

---

## Retours et valeurs

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(G_t\) | **retour** actualisé à partir de \(t\) | |
| \(G_{t:t+n}\) | retour tronqué à \(n\) pas | |
| \(\gamma\) | facteur d'actualisation | `gamma` |
| \(v_\pi(s)\), \(q_\pi(s,a)\) | valeurs **vraies** de l'état et du couple état-action sous \(\pi\) | |
| \(v_*(s)\), \(q_*(s,a)\), \(\pi_*\) | valeurs et politique **optimales** | |
| \(V(s)\), \(Q(s,a)\) | **estimations tabulaires** : un tableau en mémoire | `v_table`, `q_table` |
| \(\hat v(s,\mathbf{w})\), \(\hat q(s,a,\mathbf{w})\) | valeurs **approchées** par une fonction de poids \(\mathbf{w}\) | sortie du réseau |
| \(Q_\theta(s,a)\) | réseau de valeurs d'action | `net(states_v)` |
| \(Q_{\theta^-}\), \(Q_{\mathbf{w}^-}\) | **réseau cible**, la copie retardée | `tgt_net` |
| \(A^\pi(s,a)\) | fonction d'**avantage**, \(q_\pi(s,a) - v_\pi(s)\) | `advantage` |
| \(y\), \(U_t\) | cible d'une mise à jour, calculée côté cible | `cible` |

> [!IMPORTANT]
 **Les trois niveaux de valeur sont distincts et non interchangeables.** \(v_\pi\) est la
 valeur vraie, celle que l'on n'atteint jamais ; \(V\) est une estimation tabulaire, un
 nombre par état rangé en mémoire ; \(\hat v(s,\mathbf{w})\) est une estimation **calculée**
 par une fonction paramétrée, pour un état qui peut n'avoir jamais été visité. La semaine 4
 estime \(V\), la semaine 5 remplace \(V\) par \(\hat v\), et \(v_\pi\) reste ce que les
 deux cherchent. Une équation lue en confondant deux de ces trois niveaux dit presque
 toujours le contraire de ce qu'elle énonce.

---

## Politiques

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\pi(a \mid s)\) | politique stochastique | `policy` |
| \(\pi_\theta\), \(\pi(a \mid s,\theta)\) | politique **paramétrée**, et sa forme sous un gradient | |
| \(\mu_\theta(s)\) | acteur **déterministe**, ou moyenne d'une politique gaussienne | `acteur` |
| \(\sigma_\theta(s)\) | écart-type d'une politique gaussienne, fonction de l'état | |
| \(b(a \mid s)\) | politique de **comportement**, celle qui collecte en hors politique | |
| \(\pi_\beta(a \mid s)\) | politique qui a produit un jeu de données figé ; le \(b(a\mid s)\) de la semaine 4 | |
| \(\varepsilon\) | taux d'exploration d'une politique \(\varepsilon\)-gloutonne | `epsilon` |
| \(H\) | **entropie** d'une politique, et prime d'entropie dans une perte | `entropy_loss` |
| \(\rho_{t:T-1}\) | rapport d'échantillonnage préférentiel | |
| \(\pi \ge \pi'\) | ordre partiel sur les politiques | |

Un mot sur \(\mu\), parce que la lettre sert deux fois et que l'indice tranche : \(\mu(s)\)
**sans** indice de paramètres est la distribution sur politique des états, c'est-à-dire la
fréquence à laquelle la politique visite chaque état ; \(\mu_\theta(s)\) **avec** indice est
l'acteur de la semaine 9. Le cours n'écrit jamais un \(\mu(s)\) nu pour désigner un acteur,
même si c'est l'écriture la plus répandue ailleurs.

---

## Approximation, poids et apprentissage

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(\theta\) | paramètres d'un réseau, et en particulier de la **politique** | `net.parameters()` |
| \(\mathbf{w}\) | poids d'une fonction de **valeur** ; \(d\) est sa dimension | |
| \(\theta^-\), \(\mathbf{w}^-\) | paramètres des réseaux **cibles** | `tgt_net` |
| \(\alpha\) | **pas d'apprentissage** | `lr`, `learning_rate` |
| \(\delta_t\) | **résidu temporel**, l'erreur de différence temporelle | `td_error` |
| \(\nabla\) | gradient par rapport aux paramètres | `.backward()` |
| \(\mu(s)\) | distribution sur politique des états | |
| \(\overline{VE}(\mathbf{w})\) | erreur quadratique de valeur, l'objectif réellement approché | |
| \(\mathbf{x}(s)\), \(\mathbf{x}(s,a)\) | vecteurs de caractéristiques | |
| \(\mathcal{D}\) | **tampon de rejeu** ; en semaine 13, un jeu de données **figé** | `tampon` |
| \(\mathcal{B}\) | lot tiré dans \(\mathcal{D}\) | `batch` |
| \(D_{\mathrm{KL}}\) | divergence de Kullback-Leibler | `kl_divergence` |
| \(J(\theta)\) | mesure de performance que l'on **maximise** | `objective` |
| \(\vartheta\) | seuil de convergence d'un algorithme de programmation dynamique | `theta` |
| \(\mathbf{W}^{(\ell)}\), \(\mathbf{b}^{(\ell)}\) | poids et biais de la couche \(\ell\) | `layer.weight`, `layer.bias` |
| \(\mathbf{h}\), \(\mathbf{o}\) | vecteur caché et sortie d'un réseau | |
| \(\phi\) | fonction d'activation quelconque | |

Deux précisions qui évitent des heures de confusion. **\(\theta\) est toujours un
paramètre** dans ce cours, jamais un seuil : le seuil d'arrêt de la programmation dynamique,
que l'on écrit traditionnellement \(\theta\), s'écrit ici \(\vartheta\). Et **\(\theta\) et
\(\mathbf{w}\) ne sont pas synonymes** : dès que politique et valeur sont apprises
séparément, en semaine 8, les deux jeux de poids apparaissent dans la même équation et
chacun reçoit un gradient différent.

---

## Les symboles propres à une ou deux semaines

Les lettres ci-dessous ne servent que dans la ou les semaines indiquées, et elles y sont
définies devant vous à leur première apparition. Elles figurent ici pour que vous puissiez
relire une équation six semaines plus tard sans la remonter depuis son intuition.

### Actions continues et régions de confiance (semaines 9 et 10)

| Symbole | Signification |
| --- | --- |
| \(\tau\) | taux de **synchronisation douce** d'un réseau cible, petit (de l'ordre de 0,005) |
| \(d\) | délai de politique : une mise à jour d'acteur toutes les \(d\) mises à jour de critique |
| \(\epsilon\) | amplitude du bruit d'exploration, puis demi-largeur de la bande d'écrêtage |
| \(c\) | borne d'écrêtage du bruit ajouté à l'action cible |
| \(a_{\min}\), \(a_{\max}\) | bornes de l'espace d'actions, où l'action est écrêtée |
| \(r_t(\theta)\) | **rapport** entre la nouvelle et l'ancienne politique |
| \(\mathcal{L}(\theta_{\text{old}},\theta)\) | objectif de substitution, avant écrêtage |
| \(A^\pi_t\) | avantage **généralisé** au pas \(t\), accumulé à l'envers le long du lot |
| \(\lambda\) | pondération exponentielle de l'avantage généralisé (0,95 en pratique) |
| \(\delta\) | **budget de divergence**, sans indice, à ne pas confondre avec \(\delta_t\) |
| \(H\), \(Hx\) | hessienne de la divergence, et produit hessienne-vecteur |
| \(\alpha_{\text{ls}}\) | facteur de rebroussement de la recherche linéaire |

### Exploration dirigée (semaine 11)

| Symbole | Signification |
| --- | --- |
| \(R^e_t\), \(R^i_t\) | récompense **extrinsèque** de la tâche, et prime **intrinsèque** ajoutée par l'agent |
| \(c\) | poids de la prime d'exploration : ni un pas d'apprentissage, ni un coefficient d'entropie |
| \(\tilde N(s)\) | comptage de visites d'un état **haché** |
| \(h(s)\) | hachage d'une observation continue, arrondi avant comptage |
| \(\rho(s)\) | **modèle de densité** : la vraisemblance qu'il attribue à l'état \(s\) |
| \(f\), \(\hat f_\psi\) | réseau de référence aléatoire et figé, et le prédicteur entraîné à l'imiter |
| \(\psi\) | paramètres de ce prédicteur, distincts de \(\theta\) et de \(\mathbf{w}\) |
| \(\epsilon_{i,j}\) | bruit tiré dans une couche bruitée, jamais entraîné |

### Recherche arborescente et auto-jeu (semaine 12)

| Symbole | Signification |
| --- | --- |
| \(N(s,a)\) | comptage de visites d'une arête ; à la racine, ces comptages **deviennent** la politique |
| \(W(s,a)\) | **somme** des valeurs remontées à travers l'arête |
| \(Q(s,a) = W/N\) | leur moyenne, la statistique que lit l'utilité de sélection |
| \(P(s,a)\) | probabilité a priori de l'arête, fournie par la tête de politique |
| \(U(s,a)\) | **utilité de sélection** complète, valeur plus prime, qui décide quelle arête on descend |
| \(c_{\text{puct}}\) | constante d'exploration de cette utilité |
| \(\tau\) | **température** appliquée aux comptages de visites, dans \(N(s,a)^{1/\tau}\) |
| \(\alpha_{\mathrm{Dir}}\) | concentration de la loi de Dirichlet du bruit de racine |
| \(h_\theta\), \(g_\theta\), \(f_\theta\) | réseaux de représentation, de dynamique et de prédiction |
| \(s^k\) | **état caché** après \(k\) pas de dynamique apprise |
| \(r^k\), \(v^k\), \(\pi^k\) | récompense, valeur et politique prédites au pas \(k\) |
| \(z_k\), \(u_k\) | cibles de valeur et de récompense du pas \(k\) |
| \(K\) | longueur du déroulement déplié pendant l'entraînement |

### Plusieurs agents (semaine 12)

Cette famille est une **création du cours** : il n'existe pas de notation établie pour le
cas multi-agent, que l'on traite d'ordinaire sans une seule équation, en indexant tout par
des noms d'agents. Chaque symbole est donc défini devant vous avant de servir.

| Symbole | Signification |
| --- | --- |
| \(i\) | indice d'agent |
| \(n_t\) | **nombre d'agents vivants à l'instant \(t\)** |
| \(O^i_t\) | observation de l'agent \(i\), égocentrée donc relative à lui |
| \(A^i_t\), \(R^i_t\) | action et récompense de l'agent \(i\) |
| \(\mathbf{A}_t = (A^1_t, \dots, A^{n_t}_t)\) | **action jointe**, le \(n_t\)-uplet des actions |
| \(\pi_\theta(a \mid o^i)\) | **politique partagée** : un seul jeu de poids, servi à chaque agent avec sa propre observation |

> [!NOTE]
 **L'indice de temps de \(n_t\) n'est pas une coquetterie.** Le nombre d'agents **diminue
 en cours d'épisode** quand l'un d'eux disparaît alors que l'épisode continue. Un \(n\) fixe
 décrirait un autre problème que celui de la semaine 12.

### Modèle du monde et données figées (semaine 13)

| Symbole | Signification |
| --- | --- |
| \(Z_t\) | **état latent** appris, part stochastique de l'état du modèle |
| \(h_t\) | part **déterministe** et récurrente du même état |
| \(e_\theta(z \mid h, o)\) | **encodeur** : la loi qui produit le latent à partir de l'observation |
| \(p_\theta(z \mid h)\) | loi a priori, celle de l'imagination, sans observation |
| \(\pi_\phi(a \mid z)\) | l'**acteur** : une politique de l'état latent, jamais une valeur d'action |
| \(\hat v_\psi(z)\) | le **critique** : le \(\hat v(s,\mathbf{w})\) du cours, sur un latent |
| \(\theta\), \(\phi\), \(\psi\) | les trois jeux de paramètres : modèle du monde, acteur, critique |
| \(k\) | indice de temps **dans l'imagination**, pour ne pas surcharger \(t\) |
| \(H\) | **horizon** : de planification, puis d'imagination, puis de tâche |
| \(V_{\mathrm{R}}\), \(V_{\mathrm{N}}^{n}\), \(V_\lambda\) | les trois estimateurs de retour imaginé |
| \(\mu_{t:t+H}\), \(\sigma_{t:t+H}\) | loi sur les **suites d'actions** d'un planificateur |
| \(G^{(j)}\) | retour imaginé du candidat \(j\) |
| `action_repeat` | nombre de pas de simulation pendant lesquels une action est maintenue |
| \(d^\pi(s)\) | distribution des états visités par la politique apprise |
| \(d^{\mathcal{D}}(s)\) | distribution des états **couverts par le jeu de données** |
| \(\nu(a \mid s)\) | loi d'actions **adverse** d'une pénalité conservatrice |
| \(\alpha_{\text{cons}}\) | poids d'une contrainte ou d'une pénalité conservatrice |
| \(\beta_{\mathrm{KL}}\) | poids du terme de divergence dans une borne variationnelle |
| \(\epsilon_{\text{c}}\) | **budget** d'une contrainte de divergence |
| \(\epsilon_{\text{gen}}\) | **erreur de généralisation** d'un apprentissage supervisé |
| \(\mathcal{H}(\cdot)\) | entropie d'une loi, écrite ainsi parce que \(H\) désigne un horizon cette semaine |

> [!WARNING]
 **Même symbole, statut opposé, et l'identité du symbole est la leçon.** \(\mathcal{D}\)
 désigne depuis la semaine 5 un tampon de rejeu, alimenté en continu pendant
 l'entraînement. En semaine 13, pour la moitié hors ligne, \(\mathcal{D}\) est un jeu de
 données **figé avant même que l'agent existe**, et plus une seule transition n'y entrera.
 Le cours ne renomme pas, délibérément : c'est la même structure de données, et c'est le
 changement de régime qui fait toute la difficulté de la semaine.

### Récompense apprise et récompense mal spécifiée (semaine 14)

| Symbole | Signification |
| --- | --- |
| \(\zeta^1\), \(\zeta^2\) | les deux **segments d'épisode** comparés par une personne |
| \(L\) | longueur d'un segment, en pas de jeu |
| \(y_1\), \(y_2\) | l'**étiquette humaine** : \((1,0)\), \((0,1)\) ou \((0{,}5\,;0{,}5)\) |
| \(\hat r(o_t, a_t)\) | le **modèle de récompense** : un réseau qui note un couple observation-action |
| \(\tilde r_t\) | la récompense prédite **après** normalisation, celle que l'agent reçoit |
| \(\varsigma(\cdot)\) | la **fonction logistique**, écrite ainsi pour ne pas se confondre avec un écart-type |
| \(D\) | ensemble des paires **étiquetées** ; ce n'est pas le \(\mathcal{D}\) de la semaine 13 |
| \(P\) | récompense de **substitution**, celle que l'agent reçoit et maximise |
| \(T\) | récompense **réelle**, celle que l'on évalue et qui n'entre dans aucun gradient |
| \(\pi_\varnothing\) | la politique « ne rien faire », référence des effets secondaires |
| \(\varepsilon_{\text{res}}\) | **résolution** de l'espace d'actions, c'est-à-dire le pas d'arrondi appliqué à l'action |
| \(p_{\text{rec}}\) | probabilité de déclencher l'enregistrement d'un segment |

### Recherche sur un casse-tête déterministe (semaine 15)

| Symbole | Signification |
| --- | --- |
| \(\mathcal{T}(s,a)\) | **fonction de transition** : l'état atteint depuis \(s\) en jouant \(a\) |
| \(v(\mathcal{T}(s,a))\) | valeur de l'**état atteint**, et non une valeur d'action |
| \(U(s,a)\) | ici la **prime d'exploration seule**, et non l'utilité complète de la semaine 12 |
| \(W(s,a)\) | ici le **maximum** sur le sous-arbre, et non une somme à moyenner |
| \(R\) | **indicateur de but** : \(+1\) sur l'état résolu, \(-1\) partout ailleurs, et il ne s'actualise pas |

---

## Les lettres qui portent deux sens, et la règle du cours

Quelques lettres sont réclamées par deux objets différents, soit parce que l'usage du
domaine les leur a données toutes les deux, soit parce que deux semaines du cours en ont
besoin. Les règles ci-dessous sont **contraignantes** : c'est à elles que se tiennent les
quinze semaines, et chacune est rappelée sur place, à l'endroit où la collision mord.

| Symbole | Les deux sens, ou plus | La règle |
| --- | --- | --- |
| \(\theta\) | paramètres d'un réseau, partout, **et** seuil de convergence de la programmation dynamique | \(\theta\) est **toujours** un paramètre ; le seuil s'écrit \(\vartheta\) |
| \(\mu\) | distribution sur politique des états **et** moyenne d'une politique gaussienne | l'indice tranche : \(\mu(s)\) est la distribution, \(\mu_\theta(s)\) l'acteur |
| \(\sigma\) | fonction logistique **et** écart-type | \(\sigma(\cdot)\) **avec** argument est la logistique, \(\sigma\) seul est un écart-type ; en semaine 14, où les deux se croisent dans une même équation, la logistique s'écrit \(\varsigma(\cdot)\). Une activation quelconque s'écrit \(\phi\) |
| \(\alpha\) | pas d'apprentissage **et** exposant d'un tampon priorisé **et** concentration d'une loi de Dirichlet **et** facteur d'une recherche linéaire **et** coefficient d'entropie | \(\alpha\) nu est le pas d'apprentissage ; les autres s'écrivent \(\alpha_{\mathrm{PER}}\), \(\alpha_{\mathrm{Dir}}\), \(\alpha_{\text{ls}}\), \(\alpha_{\text{cons}}\), **à chaque occurrence**. Seul le coefficient d'entropie de la semaine 10 garde la lettre nue, parce qu'il la porte dans toutes les implémentations, et la section concernée le déclare avant sa première équation |
| \(\beta\) | exposant de correction du biais d'un tampon priorisé (semaine 6) **et** coefficient de la prime d'entropie (semaines 8 à 11) | la semaine 11 tranche en faveur du second : \(\beta\) nu est le coefficient d'entropie. L'exposant du tampon se reconnaît à ce qu'il se lit toujours par ses bornes, de 0,4 vers 1 ; une semaine qui aurait à les écrire côte à côte l'indicerait \(\beta_{\mathrm{PER}}\), par symétrie avec \(\alpha_{\mathrm{PER}}\) |
| \(\delta\) | résidu temporel **et** budget de divergence | le résidu porte toujours son indice, \(\delta_t\) ; le budget n'en porte jamais |
| \(\tau\) | taux de synchronisation douce **et** température sur des comptages de visites | aucune des deux semaines n'emploie l'autre sens ; la semaine 12 annonce la collision avant sa première équation |
| \(H\) | entropie **et** hessienne de la divergence **et** horizon | \(H\) est une entropie par défaut ; la semaine 10 l'emploie pour la courbure et la semaine 13 pour un horizon, chacune le déclarant avant usage, et la semaine 13 écrit alors l'entropie \(\mathcal{H}(\cdot)\) |
| \(\rho\) | rapport d'échantillonnage préférentiel **et** fréquence de visite actualisée **et** modèle de densité | \(\rho_{t:T-1}\), avec ses indices, est le rapport ; les deux autres sens sont nommés en français dans la prose et la lettre n'apparaît que dans l'équation qui en a besoin |
| \(r\) | récompense d'un pas **et** rapport de politiques | à partir de la semaine 10, \(r_t(\theta)\) est le rapport ; la récompense s'écrit \(R\) ou \(R_{t+1}\), ce qui est de toute façon la convention depuis la semaine 1 |
| \(\mathcal{D}\) | tampon de rejeu alimenté en continu **et** jeu de données figé | le symbole est volontairement le même, et le changement de statut est annoncé deux fois en semaine 13. L'ensemble des paires étiquetées de la semaine 14 s'écrit \(D\), sans calligraphie |
| \(U(s,a)\) | utilité de sélection complète, valeur plus prime (semaine 12) **et** prime d'exploration seule (semaine 15) | collision **entre deux semaines du cours** : la portée est annoncée avant la formule et rappelée sous la formule |
| \(W(s,a)\) | somme des valeurs remontées, que l'on divise par \(N\) (semaine 12) **et** maximum sur le sous-arbre (semaine 15) | même forme, autre algorithme : la remontée par maximum convient à un casse-tête déterministe à un seul joueur, où rien n'empêche de rejouer le meilleur chemin trouvé |
| \(\epsilon\) | taux d'exploration **et** amplitude d'un bruit **et** demi-largeur d'une bande d'écrêtage **et** budget de contrainte **et** erreur de généralisation **et** résolution d'un espace d'actions | \(\varepsilon\) nu est le taux d'exploration ; les autres sont indicés (\(\epsilon_{\text{c}}\), \(\epsilon_{\text{gen}}\), \(\varepsilon_{\text{res}}\)) ou nommés en français |
| \(V\), \(v\) | valeur d'état, partout | la lettre n'est jamais prêtée à autre chose, y compris là où un autre usage l'emploierait |
| \(s\) | état, partout **et** terme de régularisation dans certaines écritures de l'apprentissage profond | \(s\) est un état ; un régulariseur s'écrit \(\Omega\) |
| \(\gamma\) | facteur d'actualisation, partout **et** variance d'une entrée dans certaines écritures de l'initialisation | \(\gamma\) est le facteur d'actualisation ; la variance de l'entrée s'écrit \(\sigma_x^2\) |

---

## Les conventions que vous rencontrerez ailleurs

Une équation lue hors du cours peut dire exactement la même chose dans une autre notation.
Voici les six traductions qui reviennent le plus souvent, et dont l'ignorance coûte le plus
de temps.

**Les majuscules employées pour des valeurs vraies.** Beaucoup d'écritures emploient \(V\)
et \(Q\) là où ce cours écrit \(v_\pi\) et \(q_\pi\), et parfois un \(V\) qui désigne en
réalité \(v_*\). Ce n'est pas une faute, mais cela rend invisible la distinction entre une
cible et un tableau en mémoire, qui est le cœur de la semaine 5. Devant un symbole,
demandez-vous toujours s'il désigne une quantité à atteindre ou un objet calculé.

**\(R\) employé pour le total d'un épisode.** Vous le verrez, et la semaine 3 vous prévient
à l'endroit où cela arrive dans une dérivation, lettre comprise. Dans ce cours, le total
d'un épisode est \(G\), ou \(R(z)\) quand on veut insister sur la trajectoire \(z\) qui l'a
produit, et \(R_t\) reste la récompense d'un seul pas.

**\(\sigma_t\) employé pour le résidu temporel.** Le cours ne l'écrira jamais ainsi, parce
que \(\sigma\) est un écart-type dès la semaine 9 et que les deux objets se retrouvent sur
la même page en semaine 10. Le résidu temporel est \(\delta_t\), en semaine 4 comme en
semaine 10.

**Une égalité là où ce cours écrit une proportionnalité.** Dans le théorème du gradient de
politique, certaines écritures posent une égalité ; la constante omise est la longueur
moyenne d'un épisode, qui est absorbée dans le pas d'apprentissage. La conclusion pratique
est la même, mais la forme avec \(\propto\) dit la vérité.

**Trois conventions numériques pour la synchronisation douce, et elles sont inverses.** Ce
cours écrit \(\mathbf{w}^- \leftarrow \tau\, \mathbf{w} + (1-\tau)\, \mathbf{w}^-\) avec
\(\tau\) **petit** : \(\tau\) est la fraction du **nouveau** réseau qui entre dans la cible,
donc \(\tau = 0{,}005\) signifie « avance de un demi-pourcent ». Certaines écritures
emploient le complément \(1-\tau\), donc un nombre **proche de 1**, qui est la fraction de
l'**ancien** réseau conservée. Et une bibliothèque haut niveau expose ce complément sous le
nom `alpha`, d'où des appels de la forme `alpha_sync(alpha=1 - 1e-3)`, c'est-à-dire
\(\tau = 0{,}001\). Les trois disent la même chose : si vous lisez un nombre proche de 1 là
où vous attendiez 0,005, vous n'avez pas trouvé un réglage exotique, vous avez changé de
convention.

**La convention ligne pour les matrices de poids.** Là où ce cours écrit
\(\mathbf{W}^{(1)} \in \mathbb{R}^{h \times d}\) appliquée à un vecteur colonne, d'autres
écritures rangent les exemples en lignes et transposent toutes les matrices. Les dimensions
cessent alors de concorder avec les nôtres, et c'est la première chose à vérifier quand une
multiplication refuse de passer.

> [!TIP]
 **Une habitude qui vous servira au-delà de ce cours.** Devant une équation inconnue,
 identifiez d'abord trois choses, dans cet ordre : ce qui est une **vraie** valeur et ce qui
 est une estimation, ce qui porte un **indice de paramètres** et ce qui n'en porte pas, et
 ce qui est **détaché** du gradient. Ces trois lectures suffisent à comprendre la plupart
 des différences entre deux notations, et elles suffisent aussi à repérer la majorité des
 erreurs d'implémentation.

{{% comment %}}
Page rédigée en phase 4, à partir de source-assets/notation.md (référence de travail, non
modifiée) et des tableaux symbole ↔ variable réellement publiés dans content/docs.

D18, correction d'un manquement de phase 1 : le squelette publiait « Le cours suit la
notation de la 2ᵉ édition de *Reinforcement Learning: An Introduction* », seule référence
bibliographique visible du site livré. Elle est supprimée. La page dit désormais qu'une
seule notation court de la semaine 1 à la semaine 15 et qu'elle prolonge SCI1060, sans
nommer aucun ouvrage, auteur ni édition. Les divergences de source du §6 de la référence de
travail sont restituées en « vous rencontrerez ailleurs », sans attribution, ce qui est déjà
la formulation des semaines 3, 4, 9 et 10.

Promesses faites aux étudiants par les semaines, et honorées ici : table unique (sem. 1) ;
poids et pertes, convention colonne (sem. 2, section 2.2) ; la lettre H (sem. 3) ; v_pi, V,
v_chapeau et vartheta (sem. 4) ; w, theta, theta^- et mu(s) (sem. 5) ; les trois sens
d'alpha (sem. 6) ; S_t, A_t, R_t (sem. 7) ; theta et w séparés (sem. 8) ; mu contre mu_theta
et les trois conventions de synchronisation douce converties (sem. 9) ; les trois collisions
r, delta, alpha (sem. 10) ; le troisième sens de rho et la séparation de c (sem. 11) ; la
section multi-agent marquée comme création du cours (sem. 12) ; les arbitrages du modèle du
monde (sem. 13) ; zeta, y, varsigma, P et T (sem. 14) ; T(s,a), U et W (sem. 15).

Non repris de la référence de travail : les colonnes de concordance avec les sources, les
noms de sources du §6, la mention des huit agents d'indexation, et la liste des macros
KaTeX, qui est de l'outillage de rédaction et non du contenu étudiant.

Ajouts tirés des semaines publiées et absents de la référence de travail : les familles des
semaines 11 et 12 (recherche arborescente et exploration dirigée), que notation.md ne
couvrait pas, et trois collisions attestées dans le contenu publié, H (entropie, hessienne,
horizon), rho (trois sens) et D contre D calligraphique entre les semaines 13 et 14.
{{% /comment %}}
