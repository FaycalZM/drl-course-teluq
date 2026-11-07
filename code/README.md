# `sci1070` — le code fourni du cours

Ce paquet contient **ce que le cours vous fournit**, et rien d'autre.

Il ne contient **aucune solution d'exercice**. Écrire le code des laboratoires *est*
l'exercice : si vous cherchez ici la réponse à un volet, vous ne la trouverez pas, et
c'est voulu. Ce que vous y trouverez, ce sont les pièces que l'énoncé ne vous demande
pas d'inventer — le protocole de mesure, les jeux de données, les environnements
fournis — plus les entrées de ligne de commande pour les entraînements trop longs
pour un carnet.

## Installation

Dans un carnet Colab, les carnets du cours s'en chargent eux-mêmes. En local :

```bash
git clone https://github.com/FaycalZM/drl-course-teluq.git
cd drl-course-teluq/code
python -m venv .venv && .venv/Scripts/activate      # Windows
pip install -e ".[torch,courbes]"
```

Les extras sont séparés exprès. Les semaines 1, 4 et le volet B de la semaine 7
n'ont besoin ni de réseaux ni d'écran, et doivent pouvoir tourner sans eux.

## Ce qu'il y a dedans

| Module | À partir de | Ce qu'il donne |
| --- | --- | --- |
| `sci1070.protocole` | section 7.2 | `mesurer`, `intervalle`, `se_recouvrent` — une configuration se mesure sur plusieurs graines, et une moyenne ne se rapporte jamais seule |
| `sci1070.graines` | section 7.2 | `fixer_graines` — les trois sources de hasard d'un coup |
| `sci1070.courbes` | section 7.2 | `bande`, `lisser`, `tracer_bande` — la moyenne et sa plage ombrée |

## Le protocole, en trois règles

Elles viennent de la section 7.2 et elles sont appliquées à la correction :

1. **Le même jeu de graines pour toutes les variantes.** Comparer la graine 1 d'une
   variante à la graine 7 d'une autre ajoute du bruit gratuitement.
2. **Une courbe de comparaison se trace en moyenne avec une plage ombrée**, jamais
   comme une exécution unique.
3. **Un écart dont les intervalles se recouvrent n'est pas un résultat.** Il faut
   l'écrire comme tel, et c'est une conclusion parfaitement honorable.

```python
from sci1070.protocole import mesurer, intervalle, se_recouvrent

debits, temps = mesurer("référence", graines=[0, 1, 2, 3, 4], seuil=475,
                        execution=mon_entrainement)
moyenne, bas, haut = intervalle(temps)
print(f"{moyenne:.0f} s  [{bas:.0f}, {haut:.0f}]")
```

## Développement

```bash
pip install -e ".[dev,torch,courbes]"
pytest                                        # la suite complète
python tools/build_notebooks.py ../notebooks  # reconstruire les carnets
python tools/build_notebooks.py ../notebooks --verifier   # garde : rien à reconstruire
```

Les carnets ne s'éditent **pas** en `.ipynb` : la source est
`../notebooks/src/semaine-NN.py`, au format « percent », parce qu'un JSON ne se
relit pas et qu'une diff de JSON ne se lit pas non plus. Le `.ipynb` en est fabriqué.
