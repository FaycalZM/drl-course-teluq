---
title: "Laboratoire"
weight: 11
---

Le laboratoire de cette semaine est **formatif** : la semaine 5 ne porte aucun jalon, le prochain est en semaine 7. L'**exercice évalué**, celui dont j'attends un rendu écrit et sur lequel porteront les questions du quiz, est le **volet B** : l'ablation. Le volet A est l'implémentation qui le rend possible, le volet C est la récompense de la semaine, et le volet D est facultatif.

Budget de calcul, et il faut le lire avant de commencer, parce qu'il explique la forme du laboratoire. Un DQN complet sur CartPole ou LunarLander tient en **moins de quinze minutes** sur un processeur graphique T4, celui que Colab accorde gratuitement : vous l'entraînerez donc pour de vrai, du premier pas à la convergence. Un DQN sur Pong demande **une à trois heures** : il est donc hors de portée d'une session, et le volet C **n'entraîne rien**. Il charge des poids fournis et évalue l'agent.

{{% comment %}}SOURCE: COURSE-PLAN-Lapan.md §9.2{{% /comment %}}

> [!TIP]
 **Un conseil avant de lancer quoi que ce soit.** Activez l'accélérateur graphique dans Colab **avant** d'exécuter la première cellule, et vérifiez-le par une ligne : `print(torch.cuda.is_available())`. Chaque session de ce laboratoire où un étudiant se plaint d'une lenteur commence par cette ligne, et elle affiche `False` neuf fois sur dix.

---

## Volet A : un DQN complet sur CartPole

**Objectif.** Écrire un réseau Q profond entier, des cinq pièces jusqu'à la boucle, et faire converger `CartPole-v1`. À la fin de ce volet, votre agent tient le bâton en équilibre pendant 500 pas, et vous savez dire au bout de combien de trames.

**Protocole.** CartPole n'a pas besoin de la machinerie Atari : pas d'enveloppes d'image, pas de convolutions, pas d'empilement de trames, puisque l'observation contient déjà la vitesse et la vitesse angulaire. Vous réutilisez donc le petit réseau de la section 5.5, avec deux couches cachées de 128 unités. Réglages de départ : `GAMMA = 0.99`, `BATCH_SIZE = 64`, `REPLAY_SIZE = 10_000`, `REPLAY_START_SIZE = 1_000`, `LEARNING_RATE = 1e-3`, `SYNC_TARGET_FRAMES = 500`, et une décroissance de \(\varepsilon\) de 1,0 à 0,02 sur 10 000 trames. Le critère d'arrêt est une moyenne de **475** sur les cent derniers épisodes.

**Les cinq pièces à écrire**, et je vous les donne dans l'ordre où je vous conseille de les tester.

```python
class TamponDeRejeu:
    def __init__(self, capacite):
        ...        # À COMPLÉTER : une seule ligne, et elle contient maxlen

    def echantillonner(self, taille_lot):
        ...        # À COMPLÉTER : tirage uniforme, puis cinq tableaux NumPy


def calculer_perte(lot, reseau, reseau_cible, gamma, peripherique):
    obs, actions, recompenses, termines, obs_suivantes = ...
    valeurs_action = ...      # À COMPLÉTER : gather sur la dimension des actions
    with torch.no_grad():
        valeurs_suivantes = ...   # À COMPLÉTER : le max, et sur QUEL réseau ?
        ...                       # À COMPLÉTER : le masque terminal
    cibles = ...
    return nn.MSELoss()(valeurs_action, cibles)
```

**Quatre points de contrôle, et chacun se vérifie en une assertion.** Je vous demande de les écrire dans votre carnet : ils attrapent quatre des cinq bogues classiques de cette semaine.

```python
# 1. gather prélève bien UNE valeur par ligne du lot.
assert valeurs_action.shape == (BATCH_SIZE,)

# 2. La cible ne porte AUCUN gradient. C'est le semi-gradient, vérifié.
assert not cibles.requires_grad

# 3. Les deux réseaux sont distincts en mémoire, et identiques après synchro.
assert reseau is not reseau_cible
reseau_cible.load_state_dict(reseau.state_dict())
assert torch.equal(next(reseau.parameters()), next(reseau_cible.parameters()))

# 4. Le masque terminal a bien mis des zéros, et pas des valeurs de table.
assert float(valeurs_suivantes[termines_t].abs().sum()) == 0.0
```

**Attentes.**

* L'environnement est résolu en **quelques dizaines de milliers de trames**, en moins de quinze minutes, et le plus souvent en beaucoup moins.
* Tracez le retour par épisode, **sans lissage** d'abord, puis lissé sur dix épisodes. Les deux courbes sont instructives : la première montre à quel point un DQN est bruité, la seconde montre qu'il apprend quand même.
* Attendez-vous à voir le retour **redescendre** après un premier succès, parfois brutalement. Ce n'est pas un bogue, c'est le régime de la section 5.9, et vous le commenterez en une phrase.
* **Comptez les trames, pas les épisodes.** Si votre axe horizontal est en épisodes, votre courbe compare des épisodes de 20 pas avec des épisodes de 500 pas.

{{< colab url="TODO" label="Volet A : un DQN complet sur CartPole, des cinq pièces à la convergence" >}}

---

## Volet B, évalué : l'ablation, ou ce que chaque réparation répare vraiment

**Objectif.** Mesurer, et non croire. La section 5.7 affirme que le réseau cible et le tampon de rejeu sont nécessaires. Vous allez les **retirer**, un par un, et regarder ce qui se passe. C'est l'exercice le plus instructif de la semaine et il ne coûte que trois exécutions de votre code du volet A.

**Protocole.** Trois configurations, **le même code**, **la même graine aléatoire**, le même nombre de trames, et trois courbes sur un seul graphique.

| Configuration | La seule chose qui change | Ce que vous retirez |
| --- | --- | --- |
| **(1) complète** | rien | la référence du volet A |
| **(2) sans réseau cible** | `reseau_cible` remplacé par `reseau` dans la perte | la cible cesse d'être figée |
| **(3) sans tampon** | le lot est fait des 64 **dernières** transitions, dans l'ordre | l'indépendance des données |

```python
# Configuration (2) : une seule ligne change dans tout le programme.
valeurs_suivantes = reseau(obs_suiv_t).max(1)[0]      # au lieu de reseau_cible

# Configuration (3) : le tampon devient une fenêtre glissante, sans tirage.
def dernieres_transitions(memoire, taille_lot):
    """AUCUN tirage : les transitions les plus récentes, dans l'ordre."""
    return list(memoire)[-taille_lot:]
```

**Attentes, et c'est ce que je corrigerai.**

* Les trois courbes sur un même graphique, axes nommés, légende, axe horizontal en **trames**, lissage identique pour les trois. Sans cette dernière précaution, la comparaison ne veut rien dire.
* **Une demi-page écrite**, et c'est le cœur de l'exercice. Pour chacune des deux ablations, dites : quelle hypothèse de la section 5.2 ou 5.7 vous venez de violer, ce que vous observez dans la courbe, et pourquoi la seconde découle de la première. Les mots que j'attends dans ce texte sont « non stationnaire », « corrélées » et « distribution ».
* **Un tableau à trois lignes** donnant, pour chaque configuration, le nombre de trames nécessaires pour atteindre une moyenne de 200, ou la mention « jamais atteint ».
* **Et une mise en garde que je vous demande d'écrire vous-même**, en une phrase : pourquoi une seule exécution par configuration ne suffit-elle pas à conclure ? Vous avez la réponse dans la section 5.9, et elle vaut un chiffre.
* **Facultatif, et instructif** : une quatrième configuration où vous retirez `.detach()` et `torch.no_grad()` de la cible. Prédisez le résultat **avant** de lancer, écrivez votre prédiction, puis comparez. C'est la façon la plus rapide de vérifier que la section 5.4 est comprise.

{{< colab url="TODO" label="Volet B, évalué : trois ablations, trois courbes, une demi-page" >}}

---

## Volet C : jouer à Pong, à partir de poids fournis

**Objectif.** Voir ce que la méthode produit, et écrire la boucle d'évaluation qui le montre. **Rien n'est entraîné dans ce volet** : les poids vous sont fournis, parce qu'un entraînement complet demanderait une à trois heures.

**Ce que vous écrivez.** Toute la chaîne d'enveloppes de la section 5.8, le réseau de la section 5.8, le chargement des poids, et la boucle d'évaluation. Cette boucle est courte et elle contient **deux** décisions qui ne vont pas de soi.

```python
reseau = DQN(env.observation_space.shape, env.action_space.n).to(peripherique)
reseau.load_state_dict(torch.load("pong_poids.dat", map_location=peripherique))
reseau.eval()                       # décision 1 : mode évaluation

retours = []
for _ in range(N_EPISODES):
    obs, _ = env.reset()
    retour, termine, tronque = 0.0, False, False
    while not (termine or tronque):
        obs_t = torch.as_tensor(obs).unsqueeze(0).to(peripherique)
        with torch.no_grad():                        # décision 2 : aucun gradient
            action = int(reseau(obs_t).argmax(dim=1).item())   # PUREMENT glouton
        obs, recompense, termine, tronque, _ = env.step(action)
        retour += float(recompense)
    retours.append(retour)

print(f"retour moyen sur {N_EPISODES} épisodes : {np.mean(retours):.1f}")
```

**Attentes.**

* Un retour moyen **positif** sur une dizaine d'épisodes, et proche de la borne du jeu si les poids correspondent à un entraînement mené à son terme.
* **La question que je veux voir traitée en trois lignes** : pourquoi l'évaluation se fait-elle avec \(\varepsilon = 0\), alors que l'entraînement gardait \(\varepsilon = 0{,}01\) ? La semaine 4 vous a donné la réponse, sur la falaise, et je veux la retrouver ici avec les mots « politique apprise » et « politique jouée ».
* **Une vérification qui attrape le bogue classique de ce volet** : si votre agent obtient \(-21\) à tous les épisodes avec des poids réputés bons, le problème est dans la **chaîne d'enveloppes**, pas dans les poids. Vérifiez dans l'ordre : la forme de l'observation, l'ordre des axes, l'appui sur FIRE, puis la position de l'enveloppe d'empilement, qui doit être la dernière.
* **Facultatif** : enregistrez une vidéo d'un épisode avec l'enveloppe d'enregistrement de Gymnasium et regardez jouer votre agent. Cela prend trois lignes, et c'est le moment le plus satisfaisant de la semaine.

{{< colab url="TODO" label="Volet C : évaluer un agent de Pong à partir de poids fournis" >}}

---

## Volet D, facultatif : LunarLander, et la perte de Huber

**Objectif ouvert.** Reprendre le DQN du volet A sur un environnement plus difficile, puis mesurer l'effet du changement de perte annoncé en section 5.8.

**Piste de départ.** `LunarLander-v3` a huit nombres en observation et quatre actions, et il reste dans le budget des quinze minutes sur un T4. Il est plus intéressant que CartPole pour une raison précise : ses récompenses ont une **large amplitude**, avec de gros bonus à l'atterrissage et de grosses pénalités au crash, ce qui est exactement la situation où une erreur quadratique laisse une transition dominer un lot.

**Critères de réussite.**

* Le même code que le volet A, trois constantes changées, et l'environnement résolu ou presque.
* Deux exécutions, identiques à une ligne près : `nn.MSELoss()` d'un côté, `nn.SmoothL1Loss()` de l'autre. Deux courbes superposées.
* **Trois phrases de conclusion.** Laquelle apprend le plus vite ? Laquelle est la plus régulière d'une exécution à l'autre ? Et, compte tenu de la section 5.9, qu'est-ce que deux exécutions vous autorisent réellement à conclure ?

> [!TIP]
 **Mon message pour ce laboratoire.** Le volet A vous apprend à écrire un réseau Q profond, et dans six mois vous l'écrirez de mémoire en vingt minutes. Ce n'est pas le plus important. Le plus important est le volet B, parce qu'il vous apprend à **mesurer une hypothèse** : vous aurez lu dans cette page que le réseau cible est nécessaire, et vous saurez par vous-même ce qui se passe sans lui, sur votre propre courbe. Toute la suite du cours, jusqu'aux méthodes de la semaine 13, est une succession d'affirmations de ce genre, et chacune se retire en une ligne de code. Prenez l'habitude de les retirer.

---
