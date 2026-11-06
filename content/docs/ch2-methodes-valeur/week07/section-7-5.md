---
title: "7.5 Jouer et apprendre dans deux processus"
weight: 6
---

## Le point exact où la boucle se coupe

Les deux optimisations précédentes ne touchaient pas à l'architecture du programme. Celle-ci est la première modification **structurelle** de la semaine, et elle demande qu'on regarde la boucle d'entraînement comme un objet, et non comme une suite d'instructions.

Décomposons une itération en quatre étapes :

1. demander au réseau les actions, et les exécuter dans le tableau d'environnements ;
2. verser les observations obtenues dans le tampon de rejeu ;
3. échantillonner un lot dans le tampon ;
4. s'entraîner sur ce lot.

Les étapes 1 et 2 **remplissent** le tampon ; les étapes 3 et 4 **entraînent**.

{{% comment %}}SOURCE: LAPAN ch.9 p.295{{% /comment %}}

{{< bookfig src="07-01.png" week="07" >}}

Regardez la **Figure 7-1** et faites l'observation qui porte toute la section : les deux étapes du haut ne communiquent avec les deux étapes du bas que **par deux canaux**, le tampon de rejeu et le réseau. Aucun autre lien. Il n'y a pas de variable partagée, pas d'ordre imposé au-delà de ces deux canaux, pas de dépendance cachée. Et ce qui ne communique que par deux canaux explicites peut être séparé en deux processus parallèles.

{{% comment %}}SOURCE: LAPAN ch.9 p.295{{% /comment %}}

{{< bookfig src="07-02.png" week="07" >}}

La **Figure 7-2** est le même graphe, coupé. Le même vocabulaire, les mêmes boîtes, mais réparties en deux colonnes : un **processus d'entraînement** et un **processus de jeu**, reliés par une file d'attente. Le réseau, lui, reste à l'extérieur des deux et il est **partagé** : le processus de jeu le lit pour choisir ses actions, le processus d'entraînement le modifie. Dans les deux figures, les traits pleins sont des flux de données et les traits pointillés sont des **usages du réseau**, c'est-à-dire soit une inférence, soit un entraînement. Comparez les deux images un instant avant de continuer : tout l'argument de la section est dans leur différence, et nulle part ailleurs.

{{% comment %}}SOURCE: LAPAN ch.9 p.295-296, images{{% /comment %}}

---

## Quand cela paie vraiment, et quand cela ne paie presque pas

Je vais être directe sur le bénéfice attendu, parce que c'est le genre de modification qu'on entreprend pour les mauvaises raisons.

Sur Pong, la séparation **ne paie pas beaucoup**. L'environnement est rapide : avancer d'un pas dans un émulateur Atari coûte très peu, et le processus de jeu passe donc l'essentiel de son temps à attendre. Le cas où la séparation devient décisive est celui d'un environnement **lourd et lent**, où un seul pas prend des secondes de calcul. Les simulateurs neuromusculaires utilisés dans les concours de locomotion et de contrôle de prothèses sont exactement de cette nature : chaque pas résout un système mécanique, et la simulation domine totalement le coût de l'entraînement. Dans cette situation, on fait tourner **de nombreux** processus de jeu concurrents qui alimentent un seul processus d'entraînement central, et c'est la seule manière de garder le processeur graphique occupé.

{{% comment %}}SOURCE: LAPAN ch.9 p.296{{% /comment %}}

> [!TIP]
 **Le bon critère de décision, et il tient en une mesure.** Avant d'écrire une ligne de code parallèle, chronométrez séparément vos deux moitiés : le temps passé à collecter, et le temps passé à entraîner. Si la collecte représente 10 % du total, la séparation ne peut pas vous rapporter plus de 10 %, quelle que soit votre habileté. Si elle en représente 80 %, c'est la plus grosse optimisation disponible et vous devriez commencer par elle. C'est la loi la plus utile du profilage : **le gain maximal d'une optimisation est borné par la part du temps qu'elle touche.**

---

## Le mécanisme, et deux détails qui cassent en silence

Le module de multitraitement de PyTorch, `torch.multiprocessing`, remplace le module standard de Python sans changer d'interface : il suffit de changer la ligne d'importation. La raison de le préférer n'est pas l'interface, c'est ce qu'il fait des tenseurs. Il permet de **partager des tenseurs entre processus sans les copier** : mémoire partagée pour les tenseurs de processeur central, références aux zones mémoire du processeur graphique pour les tenseurs qui y résident. Ce partage supprime le goulot d'étranglement principal de la communication entre processus **à l'intérieur d'une même machine**. Attention toutefois : pour une communication véritablement distribuée, entre plusieurs machines, la sérialisation reste à votre charge.

{{% comment %}}SOURCE: LAPAN ch.9 p.296-297{{% /comment %}}

Le protocole entre les deux processus est une **file d'attente unique**, et elle transporte **deux sortes de messages**. D'abord les transitions d'expérience, qui sont la raison d'être du canal. Ensuite un message de fin d'épisode, qui porte la récompense totale, le nombre de pas et la valeur courante de \(\varepsilon\). Ce second message est un détail de conception que je trouve exemplaire : une fois la collecte déportée, le processus d'entraînement **ne voit plus les épisodes**, donc il ne peut plus calculer la récompense moyenne qui sert de critère d'arrêt. Le message de fin d'épisode lui restitue exactement cette information, et rien de plus.

{{% comment %}}SOURCE: LAPAN ch.9 p.296-297{{% /comment %}}

Du côté de l'entraînement, un générateur vide la file, range les messages de fin d'épisode dans une liste de statistiques et tout le reste dans le tampon de rejeu, attend que le tampon contienne le nombre minimal de transitions prévu, puis se met à livrer des lots échantillonnés. Et il **imite délibérément l'interface de la source d'expérience de la semaine 6**, y compris sa méthode de relevé des récompenses, de sorte que la boucle d'entraînement elle-même n'ait pas une ligne à changer. C'est la bonne manière de faire entrer une modification structurelle dans un programme qui marche : on remplace un objet par un autre objet de même forme.

{{% comment %}}SOURCE: LAPAN ch.9 p.297-298{{% /comment %}}

```python
# collecte.py : le processus de jeu. Il ne connait que la file et le reseau partage.
import torch.multiprocessing as mp
from dataclasses import dataclass

@dataclass
class FinEpisode:          # le second type de message : des STATISTIQUES, pas du vecu
    recompense: float
    pas: int
    epsilon: float

def jouer(reseau_partage, file, nom_du_jeu, graine):
    env = creer_env(nom_du_jeu, graine=graine)
    etat, _ = env.reset()
    total, pas = 0.0, 0
    while True:
        a = choisir(reseau_partage, preparer(etat), epsilon_courant(), rng)
        obs, r, termine, tronque, _ = env.step(int(a))
        file.put(Transition(etat, a, r, obs, termine))     # message de type 1
        total += r
        pas += 1
        etat = obs
        if termine or tronque:
            file.put(FinEpisode(total, pas, epsilon_courant()))   # message de type 2
            etat, _ = env.reset()
            total, pas = 0.0, 0

# entrainement.py : le processus d'entrainement.
def lots(file, tampon, initial, taille_lot):
    """Vide la file, trie les deux types de messages, puis livre des lots."""
    statistiques = []
    while True:
        while not file.empty():
            message = file.get()
            if isinstance(message, FinEpisode):
                statistiques.append(message)      # ni dans le tampon, ni appris
            else:
                tampon.ajouter(message)
        if len(tampon) < initial:
            continue
        yield tampon.echantillonner(taille_lot), statistiques
        statistiques = []

if __name__ == "__main__":
    mp.set_start_method("spawn")        # OBLIGATOIRE, et le plus souple des modes
    reseau.share_memory()               # les poids sont partages, pas recopies
    file = mp.Queue(maxsize=2)          # VOLONTAIREMENT minuscule : voir ci-dessous
    processus = mp.Process(target=jouer, args=(reseau, file, nom_du_jeu, 0))
    processus.start()
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(S_t, A_t, R_{t+1}, S_{t+1}\) | la transition transportée | `Transition(...)` |
| \(\mathcal{D}\) | tampon de rejeu, côté entraînement | `tampon` |
| \(\theta\) | poids du réseau, **partagés** entre les deux processus | `reseau.share_memory()` |
| \(\varepsilon\) | taux d'exploration, remonté avec la statistique | `FinEpisode.epsilon` |
| canal unique | file d'attente à deux types de messages | `mp.Queue(maxsize=2)` |
| taille minimale du tampon | avant le premier lot livré | `initial` |

Deux détails opérationnels, et je les signale parce qu'ils cassent **en silence**, c'est-à-dire sans message d'erreur.

Le premier : la méthode de démarrage des processus doit être fixée explicitement, et le mode à retenir est celui qui recrée un interpréteur neuf, le plus souple des trois. Sans cette ligne, selon le système d'exploitation, vous héritez d'un mode qui duplique l'état du processus parent, ce qui se passe très mal avec un contexte de processeur graphique déjà initialisé.

Le second, plus subtil et plus intéressant : la file est délibérément **minuscule**, de taille 2. L'intuition dit « une grande file, pour ne jamais bloquer le collecteur ». C'est exactement le contraire qu'il faut faire. Une grande file laisse le collecteur courir loin devant l'entraîneur, et le tampon se remplit alors de transitions produites par une politique **périmée**, puisque les poids ont changé depuis. Une file de taille 2 **étrangle** volontairement le collecteur et le force à rester au pas de l'entraîneur. La petitesse de la file est donc un mécanisme de régulation, pas une économie de mémoire.

{{% comment %}}SOURCE: LAPAN ch.9 p.298-299{{% /comment %}}

**Le résultat mesuré** : **290 trames par seconde contre 228**, soit **+27 %**, et un temps de résolution en baisse de **41 %**. Comparez maintenant avec la section précédente : la version à trois environnements atteignait près de 400 trames par seconde, donc **bien davantage**, mais résolvait le jeu en 36 minutes contre 31 ici. Moins de débit, meilleure convergence. C'est la **deuxième fois** dans cette semaine que le classement en débit et le classement en temps se contredisent, et la section suivante en donne une troisième.

{{% comment %}}SOURCE: LAPAN ch.9 p.299{{% /comment %}}

---
