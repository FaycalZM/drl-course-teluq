"""Fixer les trois sources de hasard d'une execution (section 7.2).

Necessaire, et **pas suffisant**. Des qu'il y a de la parallelisation, l'ordre dans
lequel les resultats arrivent depend de l'ordonnancement du systeme d'exploitation,
et il reinjecte du hasard qu'il est pratiquement impossible d'eliminer. C'est
precisement pour cela qu'on repete sur plusieurs graines au lieu de croire une
execution unique.

L'environnement est la quatrieme source et elle n'est pas fixee ici : Gymnasium la
prend par `env.reset(seed=...)`, appel par appel, et la masquer derriere une fonction
globale ferait oublier qu'une graine d'environnement se passe a chaque episode.
"""
from __future__ import annotations

import os
import random

import numpy as np

__all__ = ["fixer_graines"]


def fixer_graines(graine: int) -> np.random.Generator:
    """Fixe `random`, NumPy et, s'il est installe, PyTorch. Rend un generateur NumPy.

    Le generateur rendu est celui qu'il faut utiliser dans votre code : il est local
    et explicite, alors que `np.random.rand` tire dans un etat global que n'importe
    quelle bibliotheque peut deplacer sous vos pieds. Le hasard global est fixe
    quand meme, parce que beaucoup de code en depend sans le dire.
    """
    if isinstance(graine, bool) or not isinstance(graine, (int, np.integer)):
        raise TypeError(f"la graine doit etre un entier, recu {type(graine).__name__}")
    graine = int(graine)
    if graine < 0:
        raise ValueError(f"la graine doit etre positive ou nulle, recu {graine}")

    random.seed(graine)
    np.random.seed(graine)
    os.environ["PYTHONHASHSEED"] = str(graine)

    try:
        import torch
    except ImportError:
        pass
    else:
        torch.manual_seed(graine)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(graine)

    return np.random.default_rng(graine)
