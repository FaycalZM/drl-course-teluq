"""Le protocole de mesure du cours (section 7.2).

On mesure une **configuration**, jamais une execution. Une execution unique ne permet
de decider de rien : il faut repeter sur plusieurs graines et rapporter la position
**et** la largeur de la distribution obtenue.

L'intervalle est calcule par reechantillonnage avec remise plutot que par la loi de
Student, parce que les resultats d'apprentissage par renforcement sont souvent
bimodaux (ca converge, ou ca ne converge pas) et que le reechantillonnage ne fait
aucune hypothese sur la forme de la distribution.

Ecart assume avec le fragment de la section 7.2 : `mesurer` y appelle une fonction
globale `une_execution`. Ici elle est passee en argument (`execution`), parce qu'une
bibliotheque ne peut pas deviner le nom d'une fonction qui vit dans votre carnet.
Tout le reste -- noms, ordre des arguments, valeurs rendues -- est celui de la page.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any

import numpy as np

__all__ = ["mesurer", "intervalle", "se_recouvrent"]


def mesurer(
    configuration: Any,
    graines: Iterable[int],
    seuil: float,
    execution: Callable[[Any, int, float], tuple[float, float]],
) -> tuple[np.ndarray, np.ndarray]:
    """Lance une configuration sur plusieurs graines et rend les deux indicateurs.

    `execution(configuration, graine, seuil)` rend le couple (debit, temps) d'une
    execution. Le **meme** jeu de graines doit servir a toutes les variantes que vous
    comparez : comparer la graine 1 d'une variante a la graine 7 d'une autre ajoute
    du bruit gratuitement.
    """
    graines = list(graines)
    if not graines:
        raise ValueError(
            "mesurer a recu zero graine. Une configuration se mesure sur au moins "
            "trois graines, cinq de preference (section 7.2)."
        )
    if len(set(graines)) != len(graines):
        raise ValueError(
            f"graines repetees : {graines}. Repeter une graine gonfle n sans ajouter "
            "d'information et retrecit l'intervalle a tort."
        )

    debits: list[float] = []
    temps: list[float] = []
    for graine in graines:
        d, t = execution(configuration, graine, seuil)
        debits.append(float(d))
        temps.append(float(t))
    return np.array(debits, dtype=float), np.array(temps, dtype=float)


def intervalle(
    x: Sequence[float] | np.ndarray,
    niveau: float = 0.95,
    tirages: int = 10_000,
    rng: np.random.Generator | None = None,
) -> tuple[float, float, float]:
    """Intervalle de la moyenne par reechantillonnage avec remise.

    Rend `(moyenne, bas, haut)`. La moyenne est celle de l'echantillon, pas celle des
    reechantillonnages : c'est la quantite que vous rapportez, et elle ne doit pas
    bouger d'un appel a l'autre.

    `rng` vaut par defaut un generateur de graine 0, donc deux appels sur les memes
    donnees rendent le meme intervalle. Un intervalle qui changerait a chaque lecture
    serait invitable a discuter.
    """
    if not 0.0 < niveau < 1.0:
        raise ValueError(f"niveau doit etre dans ]0, 1[, recu {niveau!r}")

    x = np.asarray(x, dtype=float).ravel()
    n = x.size
    if n == 0:
        raise ValueError("intervalle a recu un echantillon vide")

    rng = rng if rng is not None else np.random.default_rng(0)
    moyennes = x[rng.integers(0, n, size=(tirages, n))].mean(axis=1)
    bas = float(np.quantile(moyennes, (1 - niveau) / 2))
    haut = float(np.quantile(moyennes, 1 - (1 - niveau) / 2))
    return float(x.mean()), bas, haut


def se_recouvrent(
    a: Sequence[float] | np.ndarray,
    b: Sequence[float] | np.ndarray,
    niveau: float = 0.95,
) -> bool:
    """Deux intervalles qui se recouvrent ne separent pas deux variantes.

    C'est la regle d'interpretation de la section 7.2 : un ecart dont les intervalles
    se recouvrent n'est pas un resultat, et l'ecrire ainsi est une conclusion
    parfaitement honorable.
    """
    _, a_bas, a_haut = intervalle(a, niveau=niveau)
    _, b_bas, b_haut = intervalle(b, niveau=niveau)
    return not (a_haut < b_bas or b_haut < a_bas)
