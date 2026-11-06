---
title: "5.1 La table n'a pas de ligne pour CartPole"
weight: 2
---

## Ce n'est pas la mémoire qui manque, ce sont les échantillons

Reprenons l'itération sur la valeur de la semaine 4 et regardons ce qu'elle suppose, non pas en théorie, mais en pratique. Elle suppose trois choses : que l'on connaisse **tous** les états à l'avance, que l'on puisse **itérer** sur eux, et que l'on puisse **ranger** une valeur pour chacun. Sur FrozenLake, les trois sont gratuites. Posons donc la question qui tue : à partir de quelle taille d'environnement laquelle des trois lâche en premier ?

{{% comment %}}SOURCE: LAPAN ch.6 p.165{{% /comment %}}

La réponse surprend presque tout le monde, et c'est pour cela que je la mets en premier. **Ce n'est pas la mémoire.** Un ordinateur très ordinaire garde plusieurs milliards de nombres flottants en mémoire vive : trente-deux gigaoctets en contiennent environ huit milliards et demi en simple précision. Et itérer sur des milliards de valeurs, c'est coûteux en temps de calcul, mais c'est faisable, surtout en parallélisant. La mémoire et le temps de calcul encaissent donc l'augmentation beaucoup plus longtemps qu'on ne le croit.

Ce qui lâche, c'est l'**échantillonnage**. Imaginez un FrozenLake d'un milliard d'états, c'est-à-dire une grille de 31 600 cases sur 31 600. Pour approcher correctement la dynamique de cet environnement, il faudrait des **centaines de milliards de transitions**, et il faudrait en plus qu'elles soient réparties à peu près uniformément sur tous les états. Ce n'est pas une question de matériel. C'est une question d'expérience disponible.

{{% comment %}}SOURCE: LAPAN ch.6 p.165{{% /comment %}}

> [!IMPORTANT]
 **Je dois insister, parce que ce diagnostic commande tout le reste du cours.** L'obstacle de l'apprentissage tabulaire n'est **pas** la place qu'occupe la table, c'est le **nombre d'interactions** nécessaires pour la remplir. Une table a besoin d'avoir visité un état pour lui donner une valeur, et elle a besoin de l'avoir visité plusieurs fois pour la lui donner correctement. Retenez cette phrase sous cette forme : le problème n'est pas de ranger un milliard de nombres, c'est de les **mériter** un par un. Toute la semaine consiste à construire une représentation qui n'a pas à les mériter un par un.

---

## Compter les écrans d'Atari, une fois, pour ne plus y revenir

Prenons l'environnement qui va nous occuper jusqu'à la fin de la semaine : un jeu Atari, dont l'observation est l'écran. Cet écran fait 210 pixels sur 160, avec 128 couleurs possibles par pixel. Cela fait 33 600 pixels, et donc

$$
128^{33\,600} \;>\; 10^{70\,802}
$$

écrans distincts. Je vous laisse mesurer ce nombre : l'univers observable contient de l'ordre de \(10^{80}\) atomes. Énumérer ces écrans une seule fois demanderait des milliards de milliards d'années, même au plus rapide des superordinateurs existants. Et le pire n'est pas là : **99,9 % de ce travail serait du pur gaspillage**, parce que l'immense majorité de ces combinaisons de pixels ne s'affiche jamais dans aucune partie réelle.

{{% comment %}}SOURCE: LAPAN ch.6 p.165-166{{% /comment %}}

Cette dernière remarque est la plus importante des deux, et elle oriente la solution. Les états qu'un agent rencontre réellement vivent sur une toute petite partie de l'espace des observations possibles. Nous n'avons donc aucun besoin d'une structure qui prévoit une case pour chaque écran concevable. Nous avons besoin d'une structure qui, à partir des écrans effectivement vus, sache répondre quelque chose de sensé sur un écran voisin jamais vu. Ce verbe, « voisin », n'a aucun sens dans une table.

---

## CartPole suffit à faire le même point

Vous pourriez penser que ce raisonnement ne concerne que les images. Non, et c'est pourquoi je prends maintenant l'environnement le plus modeste du cours, celui que vous connaissez depuis la semaine 1. L'observation de CartPole est un vecteur de **quatre nombres** en simple précision. Quatre nombres de trente-deux bits, cela fait

$$
2^{4 \times 32} \approx 3{,}4 \times 10^{38}
$$

combinaisons. Un environnement que vous avez pris pour un jouet a déjà un espace d'états dix mille milliards de milliards de fois plus grand que le nombre de secondes écoulées depuis le début de l'univers.

{{% comment %}}SOURCE: LAPAN ch.6 p.171{{% /comment %}}

L'objection naturelle est la discrétisation, et la semaine 4 l'a déjà nommée : découper chaque dimension en intervalles, et traiter chaque case ainsi obtenue comme un état. Cela marche parfois, et cela crée souvent plus de problèmes que cela n'en résout. La difficulté n'est pas technique, elle est méthodologique : il faut décider **quelles plages de valeurs comptent** et avec quelle finesse, et cette décision demande de regarder à l'intérieur de l'environnement. Autrement dit, il faut déjà savoir quelque chose du problème pour pouvoir commencer à l'apprendre.

{{% comment %}}SOURCE: LAPAN ch.6 p.171{{% /comment %}}

Voici un fragment qui rend la chose palpable. Il ne fait rien d'autre que compter les cases d'une table discrétisée, et il n'y a pas d'astuce : le nombre de cases est le produit des découpages.

```python
import math

# CartPole : 4 dimensions continues. On découpe chaque dimension en b intervalles.
for b in (5, 10, 20, 50):
    cases = b ** 4
    print(f"{b:3d} intervalles par dimension -> {cases:>10,d} cases")

# Et pour un bras robotisé à 12 articulations, même découpage :
for b in (5, 10):
    print(f"{b:3d} intervalles, 12 dimensions -> {b ** 12:.2e} cases")
```

Avec vingt intervalles par dimension, CartPole demande déjà cent soixante mille cases, dont la plupart ne seront jamais visitées, et les autres le seront trop peu pour qu'une moyenne y signifie quoi que ce soit. Avec douze articulations, la table a plus de cases qu'un disque ne peut en tenir. La discrétisation ne supprime pas le problème : elle le déplace vers le choix du découpage.

Une seconde limite de l'itération sur la valeur mérite d'être nommée ici, pour qu'elle ne vous surprenne pas plus tard : elle ne traite que des **espaces d'actions discrets**. Tout ce que nous construisons cette semaine hérite de cette limite, parce que le \(\max_{a}\) de Q-learning exige d'énumérer les actions. Les espaces d'actions continus, et donc tout le contrôle de robots, attendront les semaines 9 et 10.

{{% comment %}}SOURCE: LAPAN ch.6 p.166{{% /comment %}}

Il nous faut donc remplacer la table par autre chose, et ce quelque chose doit faire une opération que la table ne sait pas faire : **répondre sur un état qu'il n'a jamais vu**. En vocabulaire d'apprentissage automatique, nous cherchons une représentation non linéaire qui envoie l'état, ou le couple état-action, vers une valeur. Cela porte un nom, et vous l'avez rencontré en semaine 2 : c'est un **problème de régression**.

{{% comment %}}SOURCE: LAPAN ch.6 p.172{{% /comment %}}

---
