"""Les jeux de donnees fournis par le cours.

Semaine 7, volet B : « le jeu de donnees est fourni : vous n'avez aucune donnee de
marche a aller chercher ». Ce module tient cette promesse, et rien de plus. Il ne
contient pas l'environnement de negociation : l'ecrire est l'exercice.

**Pourquoi des series synthetiques plutot que des donnees de marche reelles.** Le
volet B ne teste pas une strategie, il teste une fonction de recompense, et ses
quatre assertions portent sur des identites exactes -- le cout du voyage vaut
-2*kappa, le rendement pur vaut 100*(c1/c0 - 1). Une serie deterministe rend ces
identites verifiables au centieme pres, alors qu'un fichier de marche ajouterait
une question de licence et de redistribution sans rien apprendre de plus. Les
series ci-dessous sont donc fabriquees, reproductibles, et coherentes au sens OHLC.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["Prix", "charger_prix", "series_disponibles", "series_synthetique"]


@dataclass(frozen=True)
class Prix:
    """Une serie de prix : cinq tableaux NumPy a une dimension (section 7.10).

    L'ordre des champs est celui de la page : ouverture, haut, bas, cloture, volume.
    """

    ouverture: np.ndarray
    haut: np.ndarray
    bas: np.ndarray
    cloture: np.ndarray
    volume: np.ndarray

    def __len__(self) -> int:
        return len(self.cloture)


def series_synthetique(n: int, graine: int = 0, depart: float = 100.0) -> Prix:
    """Une serie OHLCV deterministe de `n` barres.

    Marche aleatoire sur le logarithme du prix, avec une volatilite qui se groupe
    (les grosses variations appellent les grosses variations), parce qu'une serie a
    volatilite constante donne des graphiques qui ne ressemblent a rien de reel et
    rend le volet B moins credible qu'il ne doit l'etre.

    Les invariants OHLC sont imposes par construction et non esperes : le haut est
    pris au-dessus du maximum de l'ouverture et de la cloture, le bas en dessous de
    leur minimum.
    """
    if n < 20:
        raise ValueError(
            f"une serie de {n} barres est trop courte pour etre utile : la fenetre "
            "par defaut de la section 7.10 en demande 10, plus une marge de 10b."
        )

    rng = np.random.default_rng(graine)

    # Volatilite groupee : un processus autoregressif sur l'ecart-type.
    sigma = np.empty(n)
    sigma[0] = 0.012
    bruit_vol = rng.normal(0.0, 0.004, size=n)
    for t in range(1, n):
        sigma[t] = abs(0.92 * sigma[t - 1] + 0.08 * 0.012 + bruit_vol[t])

    rendements = rng.normal(0.0002, 1.0, size=n) * sigma
    cloture = depart * np.exp(np.cumsum(rendements))

    # L'ouverture d'une barre est la cloture de la precedente, decalee d'un souffle.
    ouverture = np.empty(n)
    ouverture[0] = depart
    ouverture[1:] = cloture[:-1] * (1.0 + rng.normal(0.0, 0.0008, size=n - 1))

    corps_haut = np.maximum(ouverture, cloture)
    corps_bas = np.minimum(ouverture, cloture)
    haut = corps_haut * (1.0 + np.abs(rng.normal(0.0, 0.004, size=n)))
    bas = corps_bas * (1.0 - np.abs(rng.normal(0.0, 0.004, size=n)))

    volume = np.round(1e5 * (1.0 + 3.0 * sigma / sigma.mean())
                      * (1.0 + np.abs(rng.normal(0.0, 0.3, size=n))))

    return Prix(ouverture=ouverture, haut=haut, bas=bas, cloture=cloture, volume=volume)


def _serie_plate(n: int = 400, prix: float = 100.0) -> Prix:
    """Une serie ou rien ne bouge. Un cas de test, pas un marche.

    L'assertion 1 du volet B veut un achat suivi d'une cloture sans aucun mouvement
    de prix, qui doit rendre exactement -2*kappa. Sur une serie fabriquee a la main
    un centieme de variation suffit a fausser le nombre et a envoyer l'etudiant
    chercher un bogue dans sa recompense.
    """
    plat = np.full(n, prix, dtype=float)
    return Prix(ouverture=plat.copy(), haut=plat.copy(), bas=plat.copy(),
                cloture=plat.copy(), volume=np.full(n, 1e5))


def _serie_en_escalier(n: int = 400, prix: float = 100.0, saut: float = 0.10) -> Prix:
    """Une serie qui monte de `saut` a chaque barre, sans aucun bruit.

    Pour l'assertion 3 : les deux schemas de recompense s'accordent au premier ordre
    et different au second. Le cas a deux barres a +10 % de la section 7.8 en est le
    test minimal, et cette serie en donne la version parametree.
    """
    cloture = prix * (1.0 + saut) ** np.arange(n)
    ouverture = np.concatenate([[prix], cloture[:-1]])
    return Prix(
        ouverture=ouverture,
        haut=np.maximum(ouverture, cloture),
        bas=np.minimum(ouverture, cloture),
        cloture=cloture,
        volume=np.full(n, 1e5),
    )


_SERIES = {
    "synthetique-a": lambda: series_synthetique(2000, graine=20240901),
    "synthetique-b": lambda: series_synthetique(2000, graine=20240902),
    "plate": _serie_plate,
    "escalier": _serie_en_escalier,
}


def series_disponibles() -> list[str]:
    """Les noms acceptes par `charger_prix`, dans un ordre stable."""
    return sorted(_SERIES)


def charger_prix(nom: str) -> Prix:
    """Rend la serie `nom`. Deux appels rendent les memes nombres."""
    try:
        fabrique = _SERIES[nom]
    except KeyError:
        raise KeyError(
            f"serie inconnue : {nom!r}. Series disponibles : "
            f"{', '.join(series_disponibles())}"
        ) from None
    return fabrique()
