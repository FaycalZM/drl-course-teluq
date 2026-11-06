---
title: "7.4 Plusieurs environnements : le lot n'est pas gratuit"
weight: 5
---

## Le réflexe supervisé, et pourquoi il ne se transporte pas

Si vous venez de l'apprentissage supervisé, vous avez un réflexe, et il est excellent dans son domaine d'origine : pour aller plus vite, augmentez la taille du lot jusqu'à remplir la mémoire du processeur graphique. Plus d'échantillons traités par unité de temps, donc moins de temps pour la même époque. C'est vrai, et c'est vérifiable.

{{% comment %}}SOURCE: LAPAN ch.9 p.292{{% /comment %}}

Ce réflexe **ne se transporte pas tel quel** en apprentissage par renforcement, et la raison est structurelle. Pendant un entraînement, deux choses se produisent en même temps : le réseau s'améliore sur les données dont il dispose, **et** l'agent explore, donc fabrique de nouvelles données. Les données d'entraînement sont produites par la chose même qu'on entraîne, et elles changent à mesure qu'elle change. Il n'y a pas de jeu de données fixe sur lequel accélérer une époque.

{{% comment %}}SOURCE: LAPAN ch.9 p.292{{% /comment %}}

L'image qui rend cela concret, et je vous la donne parce qu'elle est bonne. Imaginez un agent dans un jeu de tir, dont le tampon de rejeu ne contient que des morts rapides : partout où il va, il meurt. Qu'est-ce qu'un apprentissage parfaitement correct sur ces données va conclure ? Que mourir tôt minimise la souffrance, parce que c'est littéralement ce que les données disent. Et l'agent peut ne **jamais découvrir qu'il possède une arme**, parce que rien dans son tampon ne contient un tir suivi d'une récompense. L'entraînement a réussi, l'exploration a échoué, et la convergence en apprentissage par renforcement repose sur un équilibre fragile entre les deux.

{{% comment %}}SOURCE: LAPAN ch.9 p.292-293{{% /comment %}}

Augmenter la taille du lot sans augmenter la diversité de ce qu'il y a dedans ne fait donc qu'optimiser plus fort sur les mêmes informations. La bonne idée est ailleurs : augmenter la taille du lot **en augmentant le nombre de sources**.

---

## N copies, un seul passage avant

**L'intuition.** On instancie \(N\) copies du même environnement. À chaque itération d'entraînement, on avance d'un pas dans **chacune** des \(N\) copies, on verse les \(N\) transitions dans le tampon de rejeu, puis on échantillonne un lot **proportionnellement plus gros**. Les données sont \(N\) fois plus diverses pour un même nombre d'itérations, et la fragilité décrite plus haut diminue d'autant. Ces copies sont ce qu'on appelle des **environnements vectorisés** (*vectorized environments*).

Il y a un gain secondaire, et il est loin d'être négligeable : les \(N\) actions sont décidées en **un seul passage avant** du réseau, puisque les \(N\) observations forment naturellement un lot. C'est l'**inférence par lot** (*batched inference*), et c'est précisément le régime où un processeur graphique est efficace. Un passage avant sur une seule observation gaspille l'essentiel de la machine.

{{% comment %}}SOURCE: LAPAN ch.9 p.293{{% /comment %}}

```python
# Un seul environnement devient une liste. Tout le reste suit.
envs = [creer_env(nom_du_jeu) for _ in range(n_envs)]
etats = [env.reset()[0] for env in envs]

# Le lot grossit dans la MEME proportion : sinon on dilue l'apprentissage.
taille_lot = taille_lot_reference * n_envs

# ... et dans la boucle :
actions = choisir(reseau, torch.as_tensor(np.stack(etats)), epsilon, rng)  # 1 passage
for i, (env, a) in enumerate(zip(envs, actions)):
    obs, r, termine, tronque, _ = env.step(int(a))
    tampon.ajouter(etats[i], a, r, obs, termine)
    etats[i] = env.reset()[0] if (termine or tronque) else obs

# Deux constantes a RECALIBRER, et les oublier fausse la comparaison :
#   - le calendrier de decroissance de epsilon, compte en PAS DE L'AGENT ;
#   - la fenetre du compteur de debit, qui voit maintenant n_envs pas par iteration.
epsilon = calendrier(pas_agent=iteration * n_envs)
```

| Symbole | Signification | Variable du code |
| --- | --- | --- |
| \(N\) | nombre de copies de l'environnement | `n_envs` |
| \(S_t^{(i)}\) | observation courante de la copie \(i\) | `etats[i]` |
| \(A_t^{(i)}\) | action jouée dans la copie \(i\) | `actions[i]` |
| taille du lot | mise à l'échelle avec \(N\) | `taille_lot` |
| \(\varepsilon\) | taux d'exploration, compté en pas de l'agent | `epsilon` |
| \(\mathcal{D}\) | tampon de rejeu, alimenté par les \(N\) copies | `tampon` |

Le coût d'implémentation est réellement faible : une liste au lieu d'un objet, un facteur sur la taille du lot, et deux constantes à recalibrer. Mais ne sautez pas les deux constantes. Si votre calendrier de \(\varepsilon\) compte les itérations au lieu des pas de l'agent, vous explorez \(N\) fois moins longtemps qu'avant, et vous attribuerez à la vectorisation un effet qui vient du changement de calendrier.

{{% comment %}}SOURCE: LAPAN ch.9 p.293-294{{% /comment %}}

---

## Les mesures, et le point où le débit cesse de payer

Voici maintenant ce que la vectorisation rapporte, avec \(N\) balayé de 2 à 6, et c'est ici que la section devient intéressante.

Avec **deux** environnements : le débit passe de **227 à 335 trames par seconde**, soit **+47 %**, et le temps de résolution passe de **52 à 48 minutes**, soit environ **10 %**. Lisez les deux nombres côte à côte : près de la moitié de débit en plus, pour un dixième de temps en moins. Avec **trois** environnements : **398 trames par seconde** et **36 minutes**, ce qui est un bien meilleur compromis. Et au-delà de trois, le débit continue de monter, mais **la convergence se dégrade** : le temps de résolution remonte. La valeur retenue est donc \(N = 3\).

{{% comment %}}SOURCE: LAPAN ch.9 p.294{{% /comment %}}

C'est exactement la situation que la section 7.2 annonçait, et c'est pour cela que nous suivons deux indicateurs et pas un seul. Un ingénieur qui n'aurait regardé que le débit aurait choisi \(N = 6\) et aurait rendu son agent plus lent à apprendre.

{{% comment %}}SOURCE: LAPAN ch.9 p.294{{% /comment %}}

> [!IMPORTANT]
 **Une accélération n'est jamais gratuite : celle-ci ajoute un hyperparamètre.** \(N\) est à régler, comme le pas d'apprentissage ou la taille du tampon, et sa valeur optimale dépend du jeu, du réseau et de la machine. Retenez ce principe général pour toute la semaine : une optimisation qui introduit un réglage déplace une partie du coût du temps de calcul vers le temps humain. Ce peut être un excellent échange ; ce n'est pas un échange nul, et il faut le compter.

{{% comment %}}SOURCE: LAPAN ch.9 p.294{{% /comment %}}

---
