---
title: "7.6 Les enveloppes, et le tableau qui départage"
weight: 7
---

## La couche que personne ne profile

Il reste une couche dont nous n'avons pas parlé, et c'est celle que personne ne regarde jamais. Les enveloppes (*wrappers*) d'environnement sont faciles à oublier, pour une raison sociologique plus que technique : on les écrit une fois, ou bien on les reprend d'un code existant, on les applique à l'environnement, et ensuite on les laisse là. Elles deviennent une partie du décor. Or elles s'exécutent à **chaque pas**, elles manipulent des images, et elles sont donc candidates naturelles à un profilage.

{{% comment %}}SOURCE: LAPAN ch.9 p.299{{% /comment %}}

Reprenons la pile Atari classique de la semaine 5, dans l'ordre, et disons pour chacune ce qu'elle fait **et pourquoi** :

- **actions nulles au démarrage** : joue un nombre aléatoire d'actions neutres après chaque réinitialisation, ce qui supprime les observations initiales atypiques et diversifie les points de départ ;
- **saut de trames avec maximum** : saute \(N = 4\) trames et rend le **maximum** par pixel sur les trames sautées, ce qui corrige le scintillement de certains jeux Atari où un objet n'est dessiné qu'une trame sur deux ;
- **une vie perdue termine l'épisode** : raccourcit les épisodes, ce qui accélère la convergence en rendant le signal de mort immédiat ;
- **appui sur le bouton de tir au démarrage** : certains jeux ne démarrent pas sans cet appui, et la partie resterait figée ;
- **conversion en niveaux de gris et redimensionnement en 84 × 84** : réduit l'observation à ce dont le réseau a besoin ;
- **écrêtage de la récompense dans l'intervalle \([-1, 1]\)** : met sur une même échelle des jeux dont les récompenses natives vont de \(-21\) à \(21\) pour l'un et de 0 à l'infini pour un autre, ce qui permet d'utiliser les mêmes hyperparamètres partout ;
- **empilement de trames** : empile \(N = 4\) observations consécutives, et celle-ci n'est pas une commodité. Elle est **nécessaire à la propriété de Markov** : d'une seule image, vous ne pouvez pas savoir dans quel sens la balle se déplace.

{{% comment %}}SOURCE: LAPAN ch.9 p.300{{% /comment %}}

> [!NOTE]
 **Une précision sur l'appui au démarrage, parce que la justification qu'on en donne souvent est fausse.** On lit parfois que sans cet appui l'apprentissage serait impossible, par analogie avec l'observabilité partielle. Ce n'est pas de cela qu'il s'agit : si la partie ne démarre pas, il n'y a simplement **aucune donnée**, et aucune méthode ne peut apprendre de rien. C'est une question de protocole du jeu, pas de représentation de l'état. Gardez l'enveloppe, changez-en la raison.

{{% comment %}}SOURCE: LAPAN ch.9 p.300, p.302{{% /comment %}}

Pour l'implémentation, les enveloppes fournies par Stable Baselines3 sont le choix raisonnable : elles sont éprouvées et largement utilisées. Mais elles ne constituent pas une vérité définitive, et votre environnement concret peut avoir d'autres exigences. Ce qui m'amène à l'observation qui ouvre la section suivante.

{{% comment %}}SOURCE: LAPAN ch.9 p.300{{% /comment %}}

---

## Des réglages choisis pour cinquante jeux, appliqués à un seul

Voilà l'observation, et elle est d'une simplicité désarmante : **les valeurs par défaut de cette pile ont été choisies pour entraîner un même agent sur l'ensemble des 50 jeux et plus de la suite Atari 2600.** Elles sont un compromis. Pour **un** jeu donné, plusieurs d'entre elles sont du poids mort.

{{% comment %}}SOURCE: LAPAN ch.9 p.300{{% /comment %}}

Trois retouches suivent de cette observation, et elles sont appliquées **par-dessus** les deux accélérations précédentes :

1. **désactiver les actions nulles au démarrage** : Pong n'a pas d'observation initiale atypique à corriger ;
2. **remplacer le saut de trames avec maximum par un saut sans maximum** : le maximum par pixel sur quatre images existe pour le scintillement, et Pong ne scintille pas. On garde le saut, on jette le calcul de maximum ;
3. **empiler deux trames au lieu de quatre** : deux trames suffisent pour lire une direction, qui est la seule information dynamique dont Pong a besoin.

{{% comment %}}SOURCE: LAPAN ch.9 p.301{{% /comment %}}

```python
# Pile allegee pour UN jeu. Chaque ligne retiree est une hypothese a tester.
def creer_env(nom_du_jeu, graine=None):
    env = gym.make(nom_du_jeu)
    # 1. Actions nulles au demarrage : RETIREES (inutiles sur ce jeu).
    env = SautDeTrames(env, saut=4, maximum=False)   # 2. saut garde, maximum jete
    env = FinSurVie(env)
    env = TirAuDemarrage(env)
    env = NiveauxDeGris(env, taille=84)
    env = EcretageRecompense(env)
    env = EmpilementTrames(env, n=2)                 # 3. deux trames au lieu de quatre
    if graine is not None:
        env.reset(seed=graine)
    return env
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(k\) | facteur de saut de trames | `saut=4` |
| \(n\) | trames empilées dans l'observation | `EmpilementTrames(env, n=2)` |
| \(S_t\) | observation après toute la pile | la sortie de `creer_env` |
| \(R_{t+1}\) | récompense après écrêtage | `EcretageRecompense` |
| graine | fixée au niveau de l'environnement | `env.reset(seed=graine)` |

> [!TIP]
 **Un résultat de profilage a une date de péremption, et voici la preuve.** Avant 2020, remplacer la bibliothèque de traitement d'images utilisée pour redimensionner les trames par une variante optimisée rapportait une cinquantaine de trames par seconde, ce qui était l'une des meilleures optimisations disponibles. Aujourd'hui, le code de redimensionnement d'origine a été optimisé et l'échange **ne change plus rien**. Tirez-en la seule conclusion qui vaille : un conseil d'optimisation trouvé en ligne et daté de plus de deux ans doit être **remesuré**, jamais appliqué de confiance. Et votre propre tableau de mesures a une date, qu'il faut écrire dessus.

{{% comment %}}SOURCE: LAPAN ch.9 p.301{{% /comment %}}

---

## Une trame suffit-elle ? Trois exécutions sur huit répondent non

Une expérience mérite d'être isolée, parce qu'elle est le meilleur résultat empirique de toute la première moitié de la semaine, et parce qu'elle sert deux fois.

Poussons la troisième retouche à son terme : **une seule** trame dans l'observation, au lieu de deux ou de quatre. L'agent ne peut alors plus voir la direction de la balle. Il devrait donc échouer, et le mot savant serait que Pong devient un processus de décision markovien partiellement observable.

Ce qu'on observe est plus nuancé, et plus instructif. Pong est **encore résolu** avec une seule trame. Mais l'entraînement est beaucoup plus long, beaucoup plus instable, et surtout : sur **huit exécutions, trois n'ont pas convergé du tout**.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

Deux conclusions, et elles n'ont pas le même statut. La première porte sur le jeu : avec une seule trame, Pong n'est probablement pas réellement partiellement observable, parce qu'une position de raquette et une position de balle contiennent plus d'information qu'on ne le croit ; mais l'efficacité de l'apprentissage, elle, souffre énormément.

La seconde porte sur la **manière de rapporter** un résultat, et c'est celle que je veux que vous reteniez. Trois échecs sur huit, c'est un **taux d'échec de 37 %**. Une moyenne sur huit exécutions, présentée seule, le dissimule entièrement : elle sera simplement un peu plus basse, et on l'attribuera à une convergence plus lente. Le nombre d'exécutions qui n'ont pas convergé est une information **irremplaçable**, et il n'apparaît dans aucune moyenne. C'est pour cela que le jalon 2 le demande explicitement.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

---

## Le tableau qui départage, et comment on le lit

Rassemblons tout. Voici le **Tableau 7-1**, qui met côte à côte la version de référence et les cinq variantes de la semaine. Les pourcentages sont relatifs à la version de référence, et chaque ligne est une moyenne sur cinq exécutions.

| Variante | Débit, FPS (trames/s) | ΔFPS | Temps (min) | ΔTemps |
| --- | --- | --- | --- | --- |
| Version de référence | 229 | aucun | 52,2 | aucun |
| Sans `torch.no_grad()` | 219 | −4,3 % | 51,0 | −2,3 % |
| 3 environnements | 395 | +72,5 % | 36,0 | −31,0 % |
| Collecte et entraînement séparés | 290 | +26,6 % | 31,2 | −40,2 % |
| Enveloppes allégées + 3 environnements | 448 | **+95,6 %** | 47,4 | −9,2 % |
| Enveloppes allégées + processus séparés | 325 | +41,9 % | **30,0** | **−42,5 %** |

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

Les deux colonnes de pourcentages se calculent ainsi, et je les écris parce que le jalon 2 vous demande de les produire :

$$
\Delta_{\text{FPS}} = \frac{\text{FPS}_v - \text{FPS}_b}{\text{FPS}_b}, \qquad \Delta_T = \frac{T_v - T_b}{T_b}
$$

où l'indice \(v\) désigne la variante et l'indice \(b\) la version de référence. Notez la convention de signe, qui est la seule cohérente : un \(\Delta_T\) **négatif** est un gain, puisque le temps diminue ; un \(\Delta_{\text{FPS}}\) **positif** est un gain, puisque le débit augmente. Les deux colonnes ne se lisent donc pas dans le même sens, et c'est une source d'erreurs de lecture qu'il faut neutraliser en nommant les colonnes correctement.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

Et maintenant, la lecture du tableau, qui est **tout le propos de la section**. Regardez la ligne au plus haut débit : les enveloppes allégées avec trois environnements, à 448 trames par seconde, **presque le double** de la version de référence. C'est la ligne la plus spectaculaire du tableau. C'est aussi, à l'exception de la ligne de bruit, celle qui apporte **le plus faible gain de temps** : 9,2 %. Et le meilleur temps, 30 minutes et 42,5 % de gain, est obtenu par une ligne à 325 trames par seconde, c'est-à-dire **un quart de débit en moins** que la championne.

{{< bookfig src="07-03.png" week="07" >}}

La **Figure 7-3** place les six variantes dans le plan débit-temps et rend l'argument immédiat : si le débit et le temps mesuraient la même chose, les six points s'aligneraient sur une droite décroissante. Ils ne s'alignent pas. **Le débit et la convergence sont deux biens différents**, et ce tableau en est la démonstration.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

> [!IMPORTANT]
 **La règle à retenir de toute la première moitié de la semaine.** Ne rapportez jamais un débit seul. Choisissez l'indicateur qui correspond à votre objectif, et votre objectif n'est pas un processeur graphique occupé : c'est un environnement résolu. Le débit est un indicateur de **diagnostic**, utile pour savoir où part le temps ; le temps à un seuil fixé d'avance est l'indicateur de **résultat**. Les confondre est l'erreur la plus commune du profilage d'un apprentissage par renforcement, et elle conduit à optimiser consciencieusement dans la mauvaise direction.

{{% comment %}}SOURCE: LAPAN ch.9 p.302{{% /comment %}}

Un dernier mot sur ce tableau, pour fermer la boucle avec la section 7.2. La première ligne de variante, celle sans `torch.no_grad()`, annonce **−4,3 % de débit et −2,3 % de temps**. Les deux indicateurs se contredisent, sur une modification qui ne change aucun calcul. Et la version de référence elle-même a été mesurée, selon l'endroit, à 227, 228 ou 229 trames par seconde. Conclusion : cette ligne ne dit rien du tout, et il faut savoir le lire. **Lorsqu'une mesure est du même ordre que la dispersion de votre version de référence, la seule conclusion honnête est qu'il n'y a pas de différence mesurable.** C'est aussi ce qui justifie les cinq exécutions par ligne : sans elles, on aurait écrit que retirer `no_grad()` accélère la résolution de 2,3 %, ce qui est une absurdité physique.

{{% comment %}}SOURCE: LAPAN ch.9 p.294, p.299, p.302{{% /comment %}}

Voilà pour la première moitié de la semaine. Nous avons gagné un facteur de l'ordre de 1,7 sur le temps de résolution, à méthode strictement inchangée, et surtout nous avons un protocole. La seconde moitié n'a plus rien à voir.

---
