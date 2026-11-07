---
title: "4.5 L'agent qui compte ses transitions"
weight: 6
---

## Un agent qui a le droit de regarder la dynamique

Passons à la pratique, et commençons par la phrase la plus importante de la semaine. Je la mets en encadré parce qu'elle n'est écrite nulle part ailleurs et qu'elle gouverne toute la suite du cours.

> [!IMPORTANT]
 **Je dois insister : l'agent de cette section a le droit de regarder la dynamique de son environnement, et il est le dernier du cours à l'avoir.** La programmation dynamique de la section 4.4 suppose \(p(s',r \mid s,a)\) **donné**. L'agent que nous allons écrire ne l'a pas : il va donc le **fabriquer**, en comptant ses transitions, et s'en servir à l'intérieur de la mise à jour de Bellman. C'est une différence de degré, pas de nature : avec un modèle donné ou avec un modèle estimé, cet agent prend ses décisions en consultant une représentation de la dynamique. Le DQN de la semaine 5 n'aura rien de tel, et ne pourra rien de tel. Quand vous aurez terminé le laboratoire, posez-vous cette question devant n'importe quel agent du cours : **où, dans ce code, la dynamique est-elle lue ?** Cette semaine, vous pourrez pointer la ligne. À partir de la semaine prochaine, la réponse sera « nulle part », et c'est très exactement ce que l'on entend par « sans modèle ».

{{% comment %}}SOURCE: SB ch.4 p.95 ; LAPAN ch.5 p.154{{% /comment %}}

---

## Pas de terminal où s'accrocher : la boucle à deux états

Avant le code, une objection qu'il faut lever, et un petit exemple la lève très bien.

Toute notre construction propage la valeur « de proche en proche ». D'où part-elle ? Dans un épisode qui se termine, on comprend : les états terminaux valent zéro, leurs voisins héritent de la récompense finale, et l'information remonte. Mais prenez maintenant un environnement de **deux états seulement**, chacun avec une action unique, qui vous renvoie dans l'autre. Les récompenses alternent, 1 puis 2 puis 1 puis 2, indéfiniment, avec \(\gamma = 0{,}9\). Il n'y a aucun état terminal. Le cycle rompt toute propagation à reculons : il n'existe aucun point d'ancrage.

Et pourtant les valeurs existent, et l'actualisation est ce qui les sauve. Le retour est une somme infinie, mais ses termes s'écrasent très vite : au bout de 10 pas, \(0{,}9^{10} \approx 0{,}349\) ; au bout de 100 pas, \(0{,}9^{100} \approx 0{,}0000266\). Cinquante termes suffisent largement à une précision bien meilleure que ce que l'on mesurera jamais, et l'on obtient, pour les deux états :

$$
V(s_1) = 14{,}736450674121663,
\qquad
V(s_2) = 15{,}262752483911719
$$

{{% comment %}}SOURCE: LAPAN ch.5 p.152-153{{% /comment %}}

Je donne ces chiffres avec toutes leurs décimales exprès : ils sortent d'un calcul exact, pas d'un entraînement. La morale est double. D'abord, \(\gamma < 1\) n'est pas un réglage de confort, c'est ce qui donne un sens à la valeur dans un environnement sans fin. Ensuite, la propagation à reculons depuis les terminaux est une **intuition**, pas un mécanisme : le mécanisme réel est le balayage répété, qui marche avec ou sans terminaux.

Ce qui nous donne la procédure, en trois lignes, telle qu'elle s'énonce sans aucune équation :

1. Initialiser toutes les valeurs \(V(s)\) à zéro.
2. Appliquer la mise à jour de Bellman à **chaque** état.
3. Répéter l'étape 2 jusqu'à ce que les changements deviennent petits.

{{% comment %}}SOURCE: LAPAN ch.5 p.153{{% /comment %}}

---

## Deux obstacles, et ils annoncent tous les deux la semaine 5

Entre cette procédure de trois lignes et un agent qui tourne, il y a deux obstacles. Je les nomme maintenant parce qu'ils sont, mot pour mot, le programme de la semaine prochaine.

**Premier obstacle : l'espace d'états doit être discret, et assez petit pour être balayé.** La procédure exige de visiter tous les états à chaque itération. FrozenLake en 4 × 4, seize états, ne pose aucun problème. FrozenLake en 8 × 8, soixante-quatre états, non plus. CartPole, lui, est hors de portée : ses observations sont quatre nombres réels, donc une infinité d'états. On peut bien sûr **discrétiser l'espace d'états** (*discretization*), c'est-à-dire découper chaque dimension en intervalles et traiter chaque case comme un état. Mais cela ouvre immédiatement deux questions sans bonne réponse : quelle largeur donner à un intervalle, et combien de données faudra-t-il pour remplir toutes les cases ainsi créées ? Trop fin, et chaque case est vide ; trop grossier, et deux situations très différentes partagent la même valeur.

**Second obstacle : les probabilités de transition ne sont pas données.** L'interface de Gymnasium vous laisse observer, agir et encaisser ; elle ne vous donne jamais \(p(s' \mid s,a)\). Il faut donc l'**estimer par comptage** (*transition counters*) : enregistrer les triplets (état de départ, action, état d'arrivée), compter, et normaliser.

{{% comment %}}SOURCE: LAPAN ch.5 p.153-154{{% /comment %}}

Notez bien l'asymétrie entre les deux obstacles. Le second se contourne, et c'est ce que nous allons faire dans deux paragraphes. Le premier ne se contourne pas : il se résout en changeant de représentation, c'est-à-dire en remplaçant la table par une fonction. C'est la semaine 5, et elle commence ici.

---

## Trois tables, et une probabilité estimée par comptage

Notre agent va tenir trois structures de données, et elles méritent d'être nommées une par une parce que le laboratoire les redemande.

| Table | Clé | Contenu |
| --- | --- | --- |
| **table des récompenses** | (état, action, état cible) | la récompense observée sur cette transition |
| **table des transitions** | (état, action) | un compteur, par état cible, du nombre de fois qu'on y a atterri |
| **table des valeurs** | état | l'estimation \(V(s)\), ou \((\text{état}, \text{action})\) et \(Q(s,a)\) dans la variante de la fin de section |

{{% comment %}}SOURCE: LAPAN ch.5 p.154{{% /comment %}}

Un exemple rend la deuxième ligne concrète. Si l'agent a exécuté dix fois l'action 1 depuis l'état 0, et qu'il a atterri trois fois dans l'état 4 et sept fois dans l'état 5, le compteur associé à la clé (0, 1) vaut `{4: 3, 5: 7}`. Le total est 10, et les probabilités estimées sont donc 0,3 et 0,7.

{{% comment %}}SOURCE: LAPAN ch.5 p.154{{% /comment %}}

Voilà l'estimation. La **Figure 4-7** montre ce que cela donne quand on l'injecte dans la mise à jour de Bellman : chaque probabilité est remplacée par une fréquence observée, le compte d'une issue divisé par le total des exécutions.

{{< bookfig src="04-07.png" week="04" >}}

{{% comment %}}SOURCE: LAPAN ch.5 p.156-157{{% /comment %}}

$$
Q(s,a) = \sum_i \frac{c_i}{\text{total}}
  \Big(\, r(s,a,s_i) + \gamma\, V(s_i) \,\Big)
$$

{{% comment %}}SOURCE: LAPAN ch.5 p.156-157{{% /comment %}}

Comparez cette formule à l'itération sur la valeur de la section 4.4. Le \(p(s' \mid s,a)\) exact est devenu \(c_i / \text{total}\). Rien d'autre n'a changé. Et le balayage, lui, s'écrit alors exactement comme l'équation :

$$
V(s) \leftarrow \max_a \sum_{s'} p(s' \mid s,a)
  \Big(\, r(s,a,s') + \gamma\, V(s') \,\Big)
$$

{{% comment %}}SOURCE: LAPAN ch.5 p.153{{% /comment %}}

Passons au code. Je le découpe en trois fragments : la collecte, le calcul de valeur, le balayage.

```python
from collections import Counter, defaultdict

GAMMA = 0.9
TEST_EPISODES = 20


class AgentTabulaire:
    """Itération sur la valeur avec un modèle ESTIMÉ par comptage."""

    def __init__(self, env):
        self.env = env
        self.etat, _ = env.reset()
        self.recompenses: dict[tuple[int, int, int], float] = defaultdict(float)
        self.transitions: dict[tuple[int, int], Counter] = defaultdict(Counter)
        self.valeurs: dict[int, float] = defaultdict(float)

    def enregistrer(self, etat, action, cible, recompense):
        """Les deux seules lignes qui construisent le modèle de l'environnement."""
        self.recompenses[(etat, action, cible)] = float(recompense)
        self.transitions[(etat, action)][cible] += 1

    def jouer_pas_aleatoires(self, n: int) -> None:
        for _ in range(n):
            action = self.env.action_space.sample()
            cible, recompense, terminated, truncated, _ = self.env.step(action)
            self.enregistrer(self.etat, action, cible, recompense)
            if terminated or truncated:
                self.etat, _ = self.env.reset()
            else:
                self.etat = cible
```

{{% comment %}}SOURCE: LAPAN ch.5 p.154-156{{% /comment %}}

```python
    def valeur_action(self, etat: int, action: int) -> float:
        """La mise à jour de Bellman, avec c_i / total au lieu de p(s'|s,a)."""
        compteurs = self.transitions[(etat, action)]
        total = sum(compteurs.values())
        if total == 0:
            return 0.0                      # action jamais essayée dans cet état
        q = 0.0
        for cible, compte in compteurs.items():
            proba = compte / total          # p(s' | s, a), ESTIMÉ
            r = self.recompenses[(etat, action, cible)]
            q += proba * (r + GAMMA * self.valeurs[cible])
        return q

    def choisir_action(self, etat: int) -> int:
        """Pur argmax : AUCUNE exploration ici, et c'est délibéré."""
        return max(range(self.env.action_space.n),
                   key=lambda a: self.valeur_action(etat, a))

    def balayage(self) -> None:
        """UN balayage d'itération sur la valeur, sur place."""
        for etat in range(self.env.observation_space.n):
            self.valeurs[etat] = max(self.valeur_action(etat, a)
                                     for a in range(self.env.action_space.n))
```

{{% comment %}}SOURCE: LAPAN ch.5 p.156-157{{% /comment %}}

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(s\), \(a\), \(s'\) | état courant, action, état cible | `etat`, `action`, `cible` |
| \(V(s)\) | **estimation tabulaire** de la valeur d'état, ni \(v_\pi\) ni \(v_*\) | `self.valeurs[etat]` |
| \(Q(s,a)\) | estimation tabulaire de la valeur d'action | la valeur renvoyée par `valeur_action` |
| \(r(s,a,s')\) | récompense observée sur cette transition | `self.recompenses[(etat, action, cible)]` |
| \(c_i\) | nombre de transitions \((s,a) \to s_i\) | `compte`, dans `compteurs.items()` |
| \(\sum_i c_i\) | nombre total d'exécutions de \(a\) dans \(s\) | `total = sum(compteurs.values())` |
| \(p(s' \mid s,a)\) | probabilité de transition **estimée** | `compte / total` |
| \(\gamma\) | facteur d'actualisation | `GAMMA = 0.9` |
| \(\max_a\) de l'itération sur la valeur | l'amélioration repliée dans le balayage | `max(...)` dans `balayage()` |
| \(\argmax_a\) | la politique gloutonne extraite de \(V\) | `choisir_action()` |
| \(\vartheta\) | seuil de convergence de la programmation dynamique | **absent de cet agent**, qui s'arrête sur le retour de test |

La dernière ligne du tableau mérite un commentaire. L'algorithme de la section 4.4 s'arrête quand la table cesse de bouger ; cet agent s'arrête quand il **gagne**, c'est-à-dire quand son retour moyen de test dépasse un seuil. Ce n'est pas le même critère, et ce n'est pas le même esprit : l'un mesure la convergence numérique, l'autre mesure la performance. Les deux sont légitimes, mais ne les confondez pas dans vos propres implémentations.

---

## La boucle d'entraînement, et une absence remarquable

L'entraînement alterne trois choses : jouer 100 pas aléatoires pour rafraîchir les tables, faire **un** balayage d'itération sur la valeur, puis jouer 20 épisodes de test. On s'arrête lorsque le retour moyen de ces 20 épisodes dépasse **0,80**.

{{% comment %}}SOURCE: LAPAN ch.5 p.154, p.158-159{{% /comment %}}

```python
import gymnasium as gym

# FrozenLake : observations Discrete(16), actions Discrete(4). Deux espaces DISCRETS,
# ce qui est exactement ce que l'apprentissage tabulaire exige.
env = gym.make("FrozenLake-v1")
env_test = gym.make("FrozenLake-v1")
agent = AgentTabulaire(env)

tour = 0
while True:
    tour += 1
    agent.jouer_pas_aleatoires(100)      # rafraîchir les trois tables
    agent.balayage()                     # UN balayage, et un seul

    retour = 0.0
    for _ in range(TEST_EPISODES):
        etat, _ = env_test.reset()
        while True:
            action = agent.choisir_action(etat)
            cible, r, terminated, truncated, _ = env_test.step(action)
            agent.enregistrer(etat, action, cible, r)   # le test NOURRIT les tables
            retour += float(r)
            etat = cible
            if terminated or truncated:
                break
    retour /= TEST_EPISODES

    print(f"tour {tour:3d} : retour moyen de test = {retour:.3f}")
    if retour > 0.80:
        print(f"Résolu en {tour} tours.")
        break
```

{{% comment %}}SOURCE: LAPAN ch.5 p.158-159{{% /comment %}}

Trois remarques sur cette boucle, et la troisième est celle que je veux que vous reteniez.

La première : les épisodes de test **nourrissent les tables** eux aussi. Ce n'est pas une faute, c'est une gratuité qu'il serait absurde de refuser : ces transitions sont des données comme les autres, et il n'y a ici aucun jeu de validation à protéger.

La deuxième : il y a **un seul** balayage par tour, pas une convergence. C'est l'itération sur la valeur de la section 4.4, dans sa forme tronquée, et la justification est exactement celle de la Figure 4-6.

La troisième, et c'est l'absence remarquable. Regardez `choisir_action` : c'est un \(\argmax\) pur. **Aucune exploration.** Dans un agent sans modèle, c'est très exactement l'endroit où l'on insérerait une méthode \(\varepsilon\)-gloutonne, et son absence ici n'est pas un oubli : les 100 pas aléatoires du début de chaque tour fournissent déjà toute l'exploration nécessaire. L'exploration et la décision sont séparées, dans deux morceaux de code distincts. En section 4.7, elles ne le seront plus, et il faudra remettre de l'aléa **dans** la décision.

{{% comment %}}SOURCE: LAPAN ch.5 p.157{{% /comment %}}

---

## Résultats, et pourquoi c'est aussi rapide

Lançons. Une exécution de référence résout FrozenLake en **11 tours**, et l'ensemble prend **moins d'une seconde**. Mais ne retenez pas ce nombre comme une attente, et je préfère vous le dire ici plutôt que de vous laisser croire que votre code est lent. Les exécutions varient beaucoup, parce que les pas aléatoires varient et surtout parce que le critère d'arrêt ne porte que sur vingt épisodes de test : sur dix graines, le seuil est franchi entre le tour **37** et le tour **282**. Le laboratoire revient sur ce que cette dispersion enseigne.

{{% comment %}}SOURCE: LAPAN ch.5 p.159{{% /comment %}}

Mettez ce chiffre à côté de celui de la semaine 3. Le même environnement, le même objectif, et d'un côté cinquante minutes de calcul pour 55 % de réussites, de l'autre moins d'une seconde pour dépasser 80 %. Il faut comprendre d'où vient un écart de cet ordre, parce que ce n'est pas une question de puissance de calcul.

Deux raisons, et elles sont toutes les deux structurelles.

**La première : l'incertitude est traitée au lieu d'être subie.** L'itération sur la valeur estime les probabilités des issues et prend l'**espérance** sur ces issues. La méthode de la semaine 3 ne faisait qu'encaisser des retours bruités et espérer qu'en moyenne, sur assez d'épisodes, le bruit s'annule. Ici, le bruit est **modélisé**, et modéliser le bruit coûte infiniment moins d'échantillons que l'attendre. C'est ce que l'on appelle, dans ce cours, l'efficacité d'échantillon.

**La seconde : il n'y a plus besoin d'épisodes complets.** Une méthode de Monte-Carlo ne peut rien apprendre avant la fin d'un épisode, puisque son signal est le retour total. L'itération sur la valeur se met à jour **à partir de transitions individuelles**. Dans un cas extrême, on peut commencer à corriger ses valeurs à partir d'**un seul exemple**. Gardez cette phrase : c'est l'annonce exacte de la section 4.6.

{{% comment %}}SOURCE: LAPAN ch.5 p.159{{% /comment %}}

> [!WARNING]
 **Attention tout de même, parce que la rapidité a une condition.** FrozenLake ne paie **qu'à l'objectif** : tant que l'agent n'a pas atteint la case finale **au moins une fois**, toutes les récompenses observées valent zéro, toutes les valeurs estimées valent zéro, et le \(\argmax\) choisit arbitrairement. Il n'y a rigoureusement rien à apprendre avant la première réussite, même fortuite. C'est pourquoi le 4 × 4 va vite, où la marche aléatoire finit par tomber sur l'objectif, et pourquoi le **8 × 8 demande de 150 à 1 000 tours**, dont l'essentiel n'est que de l'attente. Retenez la nature du problème : ce n'est pas un problème d'apprentissage, c'est un problème d'**exploration**, et c'est le sujet de la semaine 11.

{{% comment %}}SOURCE: LAPAN ch.5 p.160{{% /comment %}}

---

## Itération sur Q, et ce qu'elle achète

Une dernière variante, et elle prépare directement la semaine prochaine. Remplaçons la table de \(V\) par une table de \(Q\) : c'est l'**itération sur Q** (*Q-iteration*). Trois choses changent dans le code, et elles valent la peine d'être énumérées parce que le laboratoire demande de les écrire.

1. La table des valeurs est désormais indexée par un **couple** (état, action) et non par un état.
2. La fonction `valeur_action` **disparaît** : il n'y a plus rien à calculer, la valeur est dans la table.
3. La mise à jour de Bellman **déménage** dans le balayage, qui a maintenant besoin de la valeur de l'état cible et l'obtient en appelant la sélection d'action sur cet état cible. Et `choisir_action` devient une simple lecture de table.

{{% comment %}}SOURCE: LAPAN ch.5 p.161-162{{% /comment %}}

Le bilan est instructif. La vitesse de convergence est la même, l'occupation mémoire est **quatre fois plus grande** (quatre actions par état), et une exécution de référence résout l'environnement en **18 tours**. On paie donc de la mémoire et on n'achète aucune vitesse. Alors pourquoi le faire ?

Pour la raison annoncée en section 4.3, et elle est décisive : avec \(Q\), **la décision n'a plus besoin des probabilités**. L'agent lit sa table et agit. La dynamique estimée reste nécessaire pendant l'**apprentissage**, mais plus du tout pour **agir**. C'est le premier pas hors du modèle, et la section 4.6 fera le second en supprimant aussi le modèle de l'apprentissage.

{{% comment %}}SOURCE: LAPAN ch.5 p.162-163{{% /comment %}}

> [!NOTE]
 **Notez bien que \(V\) ne devient pas inutile pour autant.** Ce cours va privilégier \(Q\) pendant quatre semaines, et vous pourriez en conclure que la valeur d'état est une étape dépassée. Ce serait une erreur : la valeur d'état est **essentielle** aux méthodes acteur-critique, où un réseau apprend la politique et un second apprend \(V\) pour juger ce que la politique fait. C'est la semaine 8, et vous y retrouverez tout ce que nous venons de construire, du côté du critique.

{{% comment %}}SOURCE: LAPAN ch.5 p.163{{% /comment %}}
