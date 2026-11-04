---
title: "1.8 reset(), step() et la troncature"
weight: 9
---

## Deux boutons, cinq valeurs, et l'erreur la plus coûteuse du cours

Nous arrivons au point le plus délicat de la semaine, et je ne veux pas que vous le lisiez comme une page de documentation : c'est ici que le formalisme des sections 1.3 à 1.5 rencontre du code réel, et ici que se cache l'erreur la plus répandue de tout l'apprentissage par renforcement profond. Appliquons donc la **double lecture** du cours : l'intuition, l'équation, puis le code et la table qui relie les deux.

## 1. L'intuition

Imaginez un tourniquet de station de métro avec exactement deux boutons accessibles de l'extérieur. Le premier remet tout à zéro et vous donne votre position de départ : c'est `reset()`, et vous devez l'actionner avant toute chose, sinon l'environnement ne sait pas où vous êtes. Le second prend votre action, l'applique et vous rend un petit paquet d'informations : où vous êtes maintenant, combien vous venez de gagner, s'il faut s'arrêter. C'est `step()`, que vous actionnez en boucle. C'est tout : aussi complexe soit le monde simulé, l'interface d'un environnement Gymnasium, c'est deux boutons et deux descriptions d'espaces. Notez bien ce que ces boutons **ne donnent pas** : ni l'état interne, ni les probabilités de transition, ni la fonction de récompense. Le tourniquet reste une boîte noire.

{{% comment %}}SOURCE: LAPAN ch.2 p.67-68{{% /comment %}}

## 2. L'équation

Reprenons le processus de décision markovien de la section 1.5. Une **trajectoire** est la suite \(S_0, A_0, R_1, S_1, A_1, R_2, S_2, \ldots\), engendrée par les trois mécanismes que nous connaissons : un état initial tiré par l'environnement, une action tirée par la politique, puis un état suivant et une récompense tirés par la dynamique.

$$
A_t \sim \pi(\cdot \mid S_t), \qquad S_{t+1} \sim p(\cdot \mid S_t, A_t), \qquad R_{t+1} = r(S_t, A_t, S_{t+1})
$$

C'est là que le vocabulaire de la section 1.2 doit être réactivé : l'agent ne reçoit pas \(S_{t+1}\), il reçoit une **observation** de cet état, que nous noterons \(O_{t+1}\) lorsque la distinction importera. Sur CartPole, où l'observation est à peu près l'état, la différence est négligeable ; en semaine 7, sur des images d'écran, elle ne le sera plus.

Deux signaux supplémentaires, absents de toutes ces formules, complètent le tableau. La **terminaison** (*terminated*) : la trajectoire atteint un état terminal du processus (le bâton est tombé, la partie est perdue). C'est un fait **sur le modèle**, et il signifie que la valeur de la suite est nulle : il n'y a plus de suite. La **troncature** (*truncated*) : on arrête de regarder, l'horloge a sonné, un nombre maximal de pas est atteint, alors que le processus, lui, aurait très bien pu continuer. Les deux événements mettent fin à la boucle. **Ils ne signifient pas du tout la même chose.**

## 3. Le code

```python
import gymnasium as gym

env = gym.make("CartPole-v1")

# reset() renvoie un couple : l'observation initiale et un dictionnaire d'infos.
obs, info = env.reset(seed=42)

while True:
 action = env.action_space.sample() # la politique, ici uniforme
 obs, reward, terminated, truncated, info = env.step(action)
 if terminated or truncated: # fin de l'épisode, pour l'une OU l'autre raison
 break
```

**`reset()`** doit être appelé **après la création de l'environnement** et avant tout `step()`. Il renvoie un couple : l'observation initiale et un dictionnaire d'informations supplémentaires, vide pour la plupart des environnements standards, mais que des environnements plus riches remplissent de ce qui ne rentre pas dans l'observation. L'argument `seed=` fixe la graine aléatoire ; **prenez l'habitude de l'utiliser**, c'est la différence entre une expérience que vous pouvez refaire et une anecdote. **`step(action)`** renvoie un tuple Python de **cinq** éléments. Et je précise « tuple Python », pas la classe `Tuple` de la section 1.7, car les deux mots se ressemblent dangereusement.

| Position | Nom | Nature |
| --- | --- | --- |
| 1 | `obs` | l'observation suivante : un vecteur ou une matrice NumPy |
| 2 | `reward` | la récompense de la transition, un flottant |
| 3 | `terminated` | booléen : l'épisode est terminé « pour de vrai » et il faut appeler `reset()` |
| 4 | `truncated` | booléen : l'épisode a été coupé, le plus souvent par une limite de temps, et il faut également appeler `reset()` |
| 5 | `info` | dictionnaire propre à l'environnement ; l'usage courant est de l'ignorer dans les méthodes générales |

La boucle d'un agent tient alors en une phrase : appeler `step()` jusqu'à ce que `terminated` **ou** `truncated` passe à `True`, puis appeler `reset()` pour recommencer.

{{% comment %}}SOURCE: LAPAN ch.2 p.67-69{{% /comment %}}

## La table de correspondance symbole ↔ variable

Voici le livrable de cette section, et la table à laquelle revenir chaque fois qu'un symbole du cours vous paraîtra abstrait. À gauche le formalisme des sections 1.3 à 1.5 ; à droite ce que vous tapez réellement.

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(S_t\) | état de l'environnement à l'instant \(t\), **interne, généralement inaccessible** | aucune variable : jamais exposé par l'interface |
| \(O_t\) | l'observation réellement reçue | `obs`, second élément de `reset()`, premier de `step()` |
| \(A_t\) | l'action prise à l'instant \(t\) | `action`, argument de `env.step(action)` ; tirée dans `env.action_space` |
| \(R_{t+1}\) | la récompense de la transition partant de \(t\) | `reward`, second élément de `step()` (flottant) |
| \(G_t\) | le retour actualisé à partir de \(t\) | `total_reward` accumulé dans la boucle, **sans actualisation** |
| \(\gamma\) | le facteur d'actualisation | aucune variable d'interface : il appartient à l'algorithme, pas à l'environnement |
| \(\pi(a \mid s)\) | la politique | ici `env.action_space.sample()` : la politique uniforme |
| \(\mathcal{S}\) | l'espace d'états | `env.observation_space`, par exemple `Box` de forme `(4,)` |
| \(\mathcal{A}\) | l'espace d'actions | `env.action_space`, par exemple `Discrete(2)` |
| \(p(s' \mid s, a)\) | la dynamique de transition | **aucune variable** : elle est cachée dans l'environnement |
| état terminal atteint | la trajectoire s'achève dans le modèle | `terminated` |
| arrêt artificiel | limite de temps, **extérieure au modèle** | `truncated` |
| *(aucun)* | information de diagnostic, hors formalisme | dictionnaire `info` |

{{% comment %}}SOURCE: LAPAN ch.1 p.42, p.46, p.50 ; ch.2 p.68-69, p.72, p.74{{% /comment %}}

> [!IMPORTANT]
 **Deux lignes méritent qu'on s'arrête.** Celle de \(p(s' \mid s, a)\) : **il n'y a pas de variable**. Tout notre cours existe parce que la dynamique n'est pas accessible : si elle l'était, nous ferions de la programmation dynamique et nous aurions fini en trois semaines. Et celle de \(G_t\) : `total_reward` additionne les récompenses **sans les actualiser**. L'écart n'est pas une négligence mais une convention de mesure : on rapporte la récompense brute d'un épisode, et c'est l'algorithme qui, à l'intérieur, travaille avec \(\gamma\).

## Un mot de vocabulaire, à dire une fois pour toutes

Vous rencontrerez, dans du code et des documents plus anciens (ils sont nombreux, car la convention a changé en cours de route), une version de `step()` qui ne renvoie que **quatre** valeurs, dont un troisième élément nommé `done`. Ce `done` est l'ancêtre de notre `terminated`, mais il mélangeait souvent les deux situations. Dans ce cours les noms sont fixés : en prose nous parlons de **terminaison** et de **troncature** ; dans le code nous écrivons `terminated` et `truncated`, jamais `done`. Les identifiants de l'interface (`terminated`, `truncated`, `obs`, `info`, `action_space`) restent en anglais dans les listings : ce sont des noms de variables, pas des mots de la langue.

> [!NOTE]
 **La question des versions est réglée.** Le `step()` à cinq valeurs et le `reset()` qui renvoie `(observation, info)` n'ont pas changé depuis plusieurs années : l'interface décrite ici est l'interface courante, et vous pouvez installer `gymnasium` sans épingler de version. Si un bout de code trouvé en ligne échoue sur une erreur de dépaquetage, vous savez maintenant pourquoi, et comment le corriger.

## Pourquoi nous insistons dès maintenant sur la troncature

On pourrait présenter `truncated` comme une bizarrerie de l'interface, un drapeau de plus dont on se débarrasse en écrivant `if terminated or truncated: break`. Beaucoup de code fait exactement cela ; voici l'enjeu réel, que je ne peux pas encore vous montrer en équations.

Pour la plupart des environnements, la troncature vient d'une enveloppe de limite de temps : au bout d'un certain nombre de pas, l'épisode est coupé. Sans drapeau séparé, impossible de distinguer deux situations radicalement différentes : *l'agent a atteint la fin de l'épisode* et *l'agent a atteint la limite de temps de l'environnement*. Pourquoi radicalement ? Parce qu'à partir de la semaine 4, tous nos algorithmes estimeront la valeur d'un état en s'appuyant sur celle de l'état suivant : c'est l'amorçage. Dans un **vrai** état terminal, la valeur de la suite est **nulle** : il n'y a plus rien après, par définition du modèle. Mais dans un état simplement **tronqué**, la suite existe parfaitement ; c'est nous qui avons détourné le regard. Lui attribuer une valeur nulle revient à enseigner à l'agent que le monde s'arrête au bout de 500 pas.

{{% comment %}}SOURCE: LAPAN ch.2 p.69{{% /comment %}}

> [!WARNING]
 **Attention, c'est l'erreur la plus coûteuse du cours, et elle est silencieuse.** L'amorçage doit se fonder sur `terminated` **seul**. Un code qui construit son masque de cible avec `terminated or truncated` n'a pas un petit biais : il **optimise la mauvaise fonction de perte**. Rien ne plante, rien n'avertit, et l'agent apprend sagement quelque chose de faux : il devient pessimiste sur tout ce qui ressemble à la fin de l'horloge. Vous rencontrerez ce masque en semaine 5 avec DQN, puis en semaines 8 et 10 avec A2C et PPO ; vous saurez alors déjà pourquoi la ligne est écrite comme elle l'est.

C'est pour cette raison, et non par souci documentaire, que notre code écrira systématiquement les cinq valeurs de `step()` et nommera les deux drapeaux séparément, dès le premier laboratoire.
