---
title: "7.2 Mesurer d'abord : la version de référence"
weight: 3
---

## Deux indicateurs, jamais un seul

Nous allons accélérer un agent. Première question : accélérer par rapport à quoi ?

La **version de référence** est le réseau Q profond de la semaine 5, sur Pong, avec **exactement les mêmes hyperparamètres**. Rien n'est réglé à nouveau, et c'est ce qui rend toute la suite lisible : si je retouchais le pas d'apprentissage en même temps que la structure du programme, je ne saurais plus à qui attribuer l'écart. Une version de référence est donc d'abord une **promesse de ne pas toucher**.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

Deuxième question, et c'est la plus importante de la section : qu'est-ce qu'on mesure ?

**Premier indicateur, le débit de trames** (*frames per second*, FPS) : le nombre de trames consommées dans l'environnement par seconde. Il a l'avantage d'être immédiat, local, et de réagir à la moindre modification du programme. Il a aussi l'avantage de se convertir directement en durée. Les travaux publiés sur Atari rapportent typiquement des entraînements de **25 à 50 millions** de trames. Faisons le calcul pour 50 millions, à un débit de 200 trames par seconde :

$$
\frac{50 \cdot 10^{6}}{200 \cdot 60 \cdot 60 \cdot 24} \approx 2{,}89 \ \text{jours}
$$

Presque trois jours pour une seule exécution. Ce nombre est la raison d'être de toute la première moitié de la semaine.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

> [!WARNING]
 **Un piège d'unité, et il fait un facteur 4.** Les travaux publiés comptent des **trames brutes de l'environnement**. Mais presque toutes les piles Atari appliquent un saut de trames de 4, vu en semaine 5 : l'agent ne voit qu'une trame sur quatre et répète son action sur les trois autres. Le compteur que nous allons instrumenter compte les **communications entre l'agent et l'environnement**, c'est-à-dire les pas de l'agent, donc quatre fois moins. Le même entraînement, selon la convention retenue, s'annonce à 200 ou à 800 trames par seconde. Avant de comparer votre chiffre à un chiffre trouvé ailleurs, demandez-vous lequel des deux il compte.

$$
\text{FPS}_{\text{brut}} = k \cdot \text{FPS}_{\text{agent}}, \qquad k = 4
$$

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

**Second indicateur, le temps d'horloge** (*wall clock time*) jusqu'à la résolution. L'entraînement s'arrête quand la récompense lissée sur les **100 derniers épisodes** atteint **18**. Pong plafonne à 21, et le choix de 18 plutôt que 21 mérite une justification, parce qu'il a l'air arbitraire et ne l'est pas : au-delà de 18, l'agent gagne déjà systématiquement, et ce qu'on paierait en temps supplémentaire ne servirait qu'à polir. Fixer le seuil en dessous du maximum est donc un choix de protocole, pas un relâchement.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

Et maintenant la raison d'avoir **deux** indicateurs, que je veux formuler le plus nettement possible, parce que la section 7.6 va entièrement reposer dessus : en manipulant le code, on peut obtenir un débit de trames très élevé **et une convergence dégradée**. Les deux indicateurs ne mesurent pas la même chose. Le débit mesure l'efficacité de votre **programme**. Le temps à la résolution mesure l'efficacité de votre **agent**. Et c'est le second qui est l'objectif ; le premier n'est qu'un moyen.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

> [!NOTE]
 **Un point de comparabilité, pour éviter une erreur facile.** Ne comparez pas les durées de cette semaine à celles de la semaine 5. Le seuil de résolution y était fixé à 19, il est à 18 ici, et deux durées mesurées jusqu'à deux seuils différents ne sont pas commensurables. C'est le même piège que la différence entre trames brutes et pas de l'agent : la grandeur a l'air identique, la définition a changé.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

---

## Le lissage, et ce qu'il faut instrumenter

Une récompense d'épisode est bruyante au point d'être illisible brute. On en suit donc une moyenne mobile exponentielle, qui est la même formule que celle de la semaine 5 et qui reviendra chaque fois que vous tracerez une courbe :

$$
\bar r_t = \alpha \, \bar r_{t-1} + (1 - \alpha) \, r_t, \qquad \alpha = 0{,}98
$$

Avec \(\alpha = 0{,}98\), la moyenne garde une mémoire d'une cinquantaine d'épisodes. C'est beaucoup, et c'est voulu : une courbe trop réactive vous fera voir des tendances là où il n'y a que du bruit.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

Voici la liste des grandeurs à instrumenter, et je vous la donne comme une liste de contrôle à recopier dans votre carnet du volet A :

- `reward` : la récompense **brute et non actualisée** d'un épisode, en abscisse le numéro d'épisode ;
- `avg_reward` : la moyenne mobile ci-dessus ;
- `steps` : le nombre de pas de l'épisode ;
- `loss` : la perte, échantillonnée toutes les 100 itérations, et `avg_loss`, sa moyenne ;
- `epsilon` : le taux d'exploration courant ;
- `avg_fps` : le débit moyen.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

Deux repères de diagnostic qui valent leur poids en heures économisées. D'abord, la perte doit se tenir dans une bande d'environ \(2 \cdot 10^{-3}\) à \(1 \cdot 10^{-2}\), avec des pics occasionnels : un pic arrive quand l'agent découvre un comportement dont la récompense ne correspond pas à la valeur qu'il avait apprise, et c'est normal. Si votre perte sort de cette bande de plusieurs ordres de grandeur, inutile de profiler quoi que ce soit, il y a un bogue.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

Ensuite, la **longueur des épisodes** raconte une histoire que la courbe de récompense ne raconte pas. Au début, environ **1 000 pas** : l'agent perd vite. Puis **3 000 à 4 000** pas pendant qu'il progresse, parce que les échanges durent. Puis le retour vers **2 000** pas une fois le jeu maîtrisé, et cette redescente n'est pas une régression. Elle vient du facteur d'actualisation, qui récompense le fait de gagner **tôt** : une victoire dans 2 000 pas vaut plus qu'une victoire identique dans 4 000. Tracez donc toujours cette courbe à côté de la récompense ; elle est votre seule fenêtre sur le *style* de jeu de l'agent.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

> [!NOTE]
 **Une question que je laisse ouverte, et que nous reprendrons.** Cette redescente de la longueur des épisodes peut aussi se lire autrement : comme un indice que l'agent s'est **spécialisé** sur les régularités de cet environnement précis, ce qu'on appellerait du surapprentissage. Les deux lectures sont compatibles avec la courbe, et rien ici ne permet de trancher. Je préfère vous le dire plutôt que vous laisser croire qu'une courbe de longueur d'épisode s'interprète toute seule. Nous y reviendrons en seconde moitié de semaine, où le surapprentissage sera visible au lieu d'être supposé, et une dernière fois en semaine 15.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

Dernière convention, et elle coûte deux lignes de code pour un gain de lisibilité considérable : tracez vos courbes avec **deux axes des abscisses**. En bas, le temps d'horloge en heures ; en haut, le numéro de pas, d'épisode ou d'itération. Le même graphique répond alors aux deux questions qu'on se pose toujours devant une courbe d'entraînement, « combien de temps » et « combien d'expérience ».

{{% comment %}}SOURCE: LAPAN ch.9 p.289{{% /comment %}}

---

## Les graines ne suffisent pas, et c'est le point de départ du jalon

Nous arrivons au point le plus important de la section, et peut-être de la semaine. Je le place ici, dans le protocole de mesure, parce que c'est là qu'il appartient, et il reviendra tel quel dans les consignes du jalon 2.

Pour rendre une exécution reproductible, on fixe explicitement les graines aléatoires (*random seeds*) des trois sources de hasard du programme : celle de PyTorch, celle de l'environnement, celle de NumPy. C'est nécessaire. Ce n'est **pas suffisant**. Dès qu'il y a de la parallélisation, et toute la première moitié de la semaine en ajoute, l'ordre dans lequel les résultats arrivent dépend de l'ordonnancement du système d'exploitation, et il réinjecte du hasard qu'il est pratiquement impossible d'éliminer.

{{% comment %}}SOURCE: LAPAN ch.9 p.287{{% /comment %}}

La conséquence est inconfortable et elle est sans appel : **le résultat d'une exécution unique ne permet de décider de rien.** Pas « est fragile », pas « demande de la prudence » : ne permet de décider de rien. Il faut répéter l'exécution et agréger. Les mesures de référence que je vous donne dans cette semaine sont, chacune, la moyenne de **cinq exécutions** de la même expérience.

{{% comment %}}SOURCE: LAPAN ch.9 p.287-288{{% /comment %}}

Voici la preuve empirique, et je vous la donne maintenant parce qu'elle est plus convaincante que n'importe quel argument : dans cette semaine, la version de référence de Pong apparaîtra à **227**, à **228** et à **229** trames par seconde selon l'endroit où elle a été mesurée. Trois mesures du **même** programme sur la **même** machine. L'écart est petit, environ 1 %, et c'est exactement ce qui le rend dangereux : il est du même ordre que plusieurs des « gains » que nous allons mesurer en section 7.6. Une accélération annoncée à 2 % sur une exécution unique n'est pas une accélération, c'est une mesure du bruit.

{{% comment %}}SOURCE: LAPAN ch.9 p.294, p.299, p.302{{% /comment %}}

Alors, comment fait-on ? Aucune des méthodes rencontrées jusqu'ici ne répond à cette question, et je ne vais pas faire semblant qu'il existe une recette consacrée que vous pourriez aller copier. Je vous donne donc le protocole **du cours**, explicitement, et c'est celui que j'attends au jalon 2 et dans tous les jalons suivants.

**L'intuition.** Chaque exécution est un tirage dans une distribution de résultats que la méthode produit. Ce qui vous intéresse n'est pas le tirage, c'est la distribution : sa position, et sa largeur. Une variante n'est meilleure qu'une autre que si leurs distributions sont **séparées**, et pour le savoir il faut les avoir estimées toutes les deux.

**L'équation.** Soit \(n\) exécutions indépendantes d'une même configuration, de résultats \(x_1, \dots, x_n\), de moyenne empirique \(\bar x\) et d'écart-type empirique \(s\). L'intervalle de confiance de la moyenne, au niveau \(1 - \alpha\), s'écrit :

$$
\bar x \pm t_{1-\alpha/2,\; n-1} \, \frac{s}{\sqrt{n}}
$$

où \(t_{1-\alpha/2,\,n-1}\) est le quantile de la loi de Student à \(n-1\) degrés de liberté. Avec \(n = 5\) et un niveau de 95 %, ce quantile vaut environ 2,78, ce qui vous dit tout de suite à quoi vous attendre : avec cinq graines, l'intervalle est **large**. C'est une information, pas un défaut de la méthode. Si vous préférez ne faire aucune hypothèse sur la forme de la distribution, ce qui est plus prudent ici parce que les résultats d'apprentissage par renforcement sont souvent bimodaux (ça converge, ou ça ne converge pas), utilisez un intervalle par **rééchantillonnage** : on retire \(n\) valeurs avec remise, un grand nombre de fois, et on lit les quantiles empiriques de la distribution des moyennes obtenues.

**Le code.** Une vingtaine de lignes, et elles valent une bonne part de la note du jalon 2.

```python
# protocole.py : on mesure une CONFIGURATION, pas une execution.
import numpy as np

def mesurer(configuration, graines, seuil):
    """Lance une configuration sur plusieurs graines et rend les deux indicateurs."""
    fps, temps = [], []
    for g in graines:                 # LE MEME jeu de graines pour toutes les variantes
        f, t = une_execution(configuration, graine=g, seuil=seuil)
        fps.append(f)
        temps.append(t)
    return np.array(fps, dtype=float), np.array(temps, dtype=float)

def intervalle(x, niveau=0.95, tirages=10_000, rng=None):
    """Intervalle de la moyenne par reechantillonnage avec remise."""
    rng = rng or np.random.default_rng(0)
    n = len(x)
    moyennes = x[rng.integers(0, n, size=(tirages, n))].mean(axis=1)
    bas = float(np.quantile(moyennes, (1 - niveau) / 2))
    haut = float(np.quantile(moyennes, 1 - (1 - niveau) / 2))
    return float(x.mean()), bas, haut

def se_recouvrent(a, b):
    """Deux intervalles qui se recouvrent ne separent pas deux variantes."""
    _, a_bas, a_haut = intervalle(a)
    _, b_bas, b_haut = intervalle(b)
    return not (a_haut < b_bas or b_haut < a_bas)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(n\) | nombre de graines par configuration | `len(graines)` |
| \(x_i\) | résultat de l'exécution \(i\) | une entrée de `fps` ou de `temps` |
| \(\bar x\) | moyenne empirique | `x.mean()` |
| \(s\) | écart-type empirique | `x.std(ddof=1)` |
| \(1-\alpha\) | niveau de confiance | `niveau` |
| bornes de l'intervalle | ce qui est rapporté, jamais la seule moyenne | `bas, haut` |
| \(T\) | temps d'horloge jusqu'au seuil | `temps` |
| seuil | critère d'arrêt **fixé d'avance** | `seuil` |

> [!IMPORTANT]
 **Trois règles découlent de ce protocole, et je les appliquerai à la correction.** Premièrement, **le même jeu de graines pour toutes les variantes** : comparer la graine 1 d'une variante à la graine 7 d'une autre ajoute du bruit gratuitement. Deuxièmement, une courbe de comparaison se trace en **moyenne avec une plage ombrée**, jamais comme une exécution unique. Troisièmement, et c'est la règle d'interprétation : **un écart dont les intervalles se recouvrent n'est pas un résultat.** Il faut l'écrire comme tel, et c'est une conclusion parfaitement honorable.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §10{{% /comment %}}
{{% comment %}}SOURCE: LAPAN ch.9 p.287-288{{% /comment %}}

> [!WARNING]
 **Les nombres absolus de cette semaine ne se transportent pas, et il vaut mieux le savoir avant d'être déçu.** Toutes les mesures que je vous donne, débits et durées, viennent d'une machine précise : un processeur Intel i5-7600K et une carte GTX 1080 Ti. Sur un processeur graphique partagé de Colab, vos nombres absolus seront différents, parfois de beaucoup, et cela ne voudra rien dire sur votre code. Ce qui se transporte, ce sont les **rapports** : un gain de 40 % reste un gain de 40 %, un classement entre deux variantes reste un classement. C'est pour cette raison que le tableau de la section 7.6 porte deux colonnes de pourcentages à côté de ses deux colonnes de valeurs, et que le jalon 2 vous demande d'indiquer votre matériel.

{{% comment %}}SOURCE: LAPAN ch.9 p.288{{% /comment %}}

---
