"""Tracer une comparaison honnetement : moyenne et plage ombree, jamais une execution.

Le calcul (`bande`, `lisser`) est separe du dessin (`tracer_bande`) pour une raison
pratique : le calcul se teste sans ecran, et vous pouvez vouloir la bande sans vouloir
la figure.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .protocole import intervalle

__all__ = ["bande", "lisser", "tracer_bande"]


def bande(
    courbes: Sequence[Sequence[float]] | np.ndarray,
    niveau: float = 0.95,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Agrege plusieurs executions d'une meme configuration en (moyenne, bas, haut).

    `courbes` a une ligne par graine et une colonne par point de mesure. Les bornes
    sont celles de `protocole.intervalle`, point par point : la plage ombree est donc
    l'incertitude **sur la moyenne**, pas la dispersion des executions, et c'est bien
    ce qu'il faut pour decider si deux variantes se separent.
    """
    courbes = _en_matrice(courbes)
    rng = rng if rng is not None else np.random.default_rng(0)

    moyenne = courbes.mean(axis=0)
    bas = np.empty_like(moyenne)
    haut = np.empty_like(moyenne)
    for j in range(courbes.shape[1]):
        _, bas[j], haut[j] = intervalle(courbes[:, j], niveau=niveau, rng=rng)
    return moyenne, bas, haut


def lisser(x: Sequence[float] | np.ndarray, alpha: float = 0.98) -> np.ndarray:
    """Moyenne mobile exponentielle de la section 7.2.

        r_t = alpha * r_{t-1} + (1 - alpha) * x_t

    Elle demarre sur `x[0]` et non sur zero : demarrer a zero fabriquerait une montee
    au debut de chaque courbe, qu'on lirait ensuite comme un apprentissage.
    """
    if not 0.0 <= alpha < 1.0:
        raise ValueError(f"alpha doit etre dans [0, 1[, recu {alpha!r}")

    x = np.asarray(x, dtype=float).ravel()
    if x.size == 0:
        return x.copy()

    y = np.empty_like(x)
    y[0] = x[0]
    for t in range(1, x.size):
        y[t] = alpha * y[t - 1] + (1.0 - alpha) * x[t]
    return y


def tracer_bande(
    ax,
    abscisse: Sequence[float] | np.ndarray,
    courbes: Sequence[Sequence[float]] | np.ndarray,
    etiquette: str | None = None,
    niveau: float = 0.95,
    **kwargs,
):
    """Dessine la moyenne et sa plage ombree sur un axe Matplotlib existant.

    L'etiquette porte le nombre de graines, parce qu'une bande sans son n ne se lit
    pas : la meme largeur veut dire deux choses opposees a n = 3 et a n = 30.
    """
    courbes = _en_matrice(courbes)
    moyenne, bas, haut = bande(courbes, niveau=niveau)
    abscisse = np.asarray(abscisse, dtype=float).ravel()
    if abscisse.size != moyenne.size:
        raise ValueError(
            f"abscisse de taille {abscisse.size} pour des courbes de taille {moyenne.size}"
        )

    n = courbes.shape[0]
    titre = etiquette if etiquette is None else f"{etiquette} (n={n})"
    (ligne,) = ax.plot(abscisse, moyenne, label=titre, **kwargs)
    ax.fill_between(abscisse, bas, haut, alpha=0.2, color=ligne.get_color(), linewidth=0)
    return ligne


def _en_matrice(courbes) -> np.ndarray:
    if isinstance(courbes, np.ndarray):
        if courbes.ndim != 2:
            raise ValueError(f"attendu un tableau a deux dimensions, recu {courbes.ndim}")
        if courbes.size == 0:
            raise ValueError("aucune courbe a agreger")
        return courbes.astype(float)

    courbes = list(courbes)
    if not courbes:
        raise ValueError("aucune courbe a agreger")
    longueurs = {len(c) for c in courbes}
    if len(longueurs) != 1:
        raise ValueError(
            f"les executions n'ont pas la meme longueur ({sorted(longueurs)}). "
            "Tronquez-les explicitement a la plus courte plutot que d'agreger des "
            "points qui ne se correspondent pas."
        )
    return np.asarray(courbes, dtype=float)
