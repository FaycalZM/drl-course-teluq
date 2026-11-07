"""Les journaux d'entrainement du volet B de la semaine 15.

**Ces courbes sont reconstruites, pas mesurees.** Refaire l'entrainement d'origine
demande environ six jours de processeur graphique, et ce cours ne les a pas. Les
journaux ci-dessous reproduisent le phenomene que la section 15.5 decrit, a partir
de ce que la section en dit, pour que le volet B puisse etre fait : son objet est de
**diagnostiquer** une divergence de valeur, pas de la produire.

La distinction est dite dans le champ `description`, qui s'affiche dans le carnet, et
elle est verifiee par un test. Le volet D de cette meme semaine demande a l'etudiant
d'ecrire un rapport honnete puis le meme rapport malhonnete, en gardant les chiffres
exacts et en omettant les reserves ; livrer une courbe reconstruite sans le dire
serait exactement l'exercice malhonnete, en tete du volet qui l'enseigne.

Ce que les courbes portent, et pourquoi chaque trait est la :

- la perte de **valeur** tient un plateau, puis le quitte et monte sans borne. La
  cible de la section 15.5 ne fixe aucune echelle : rien n'empeche les valeurs de
  deriver ensemble, et elles derivent ;
- la perte de **politique**, elle, descend sagement du debut a la fin. C'est le point
  du volet : une seule des deux courbes alerte, et un entrainement surveille par la
  mauvaise des deux ne previent de rien ;
- le journal « avec ancre » tient l'echelle, parce que l'etat resolu y est le point
  ou une valeur est connue.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["Journal", "charger_journal", "journaux_disponibles"]

_N_POINTS = 400
_PAS_PAR_POINT = 250


@dataclass(frozen=True)
class Journal:
    """Deux pertes le long d'un entrainement, sur un axe commun."""

    titre: str
    description: str
    pas: np.ndarray
    perte_politique: np.ndarray
    perte_valeur: np.ndarray

    def __len__(self) -> int:
        return len(self.pas)


_AVERTISSEMENT = (
    "Courbes RECONSTRUITES a partir de ce que la section 15.5 decrit, et non "
    "mesurees : l'entrainement d'origine demande environ six jours de processeur "
    "graphique. Elles servent a poser le diagnostic du volet B, qui est l'objet de "
    "l'exercice ; elles ne sont pas une mesure et ne doivent pas etre citees comme "
    "telle."
)


def _axe() -> np.ndarray:
    return np.arange(1, _N_POINTS + 1, dtype=int) * _PAS_PAR_POINT


def _perte_politique(rng: np.random.Generator) -> np.ndarray:
    """Une descente ordinaire, bruitee. Elle ne previent de rien, et c'est le point."""
    t = np.linspace(0.0, 1.0, _N_POINTS)
    fond = 0.35 + 1.75 * np.exp(-4.5 * t)
    return fond * np.exp(rng.normal(0.0, 0.045, size=_N_POINTS))


def _perte_valeur_sans_ancre(rng: np.random.Generator) -> np.ndarray:
    """Plateau, puis derive : aucune echelle n'est fixee, donc rien ne la retient."""
    t = np.linspace(0.0, 1.0, _N_POINTS)
    depart = 0.30
    # Le plateau tient sur le premier tiers, puis la croissance prend le dessus.
    derive = np.where(t < 0.33, 0.0, (t - 0.33) ** 2 * 38.0)
    fond = depart * (1.0 + derive * 40.0)
    return fond * np.exp(rng.normal(0.0, 0.05, size=_N_POINTS))


def _perte_valeur_avec_ancre(rng: np.random.Generator) -> np.ndarray:
    """L'etat resolu ancre l'echelle : la perte descend, puis se stabilise."""
    t = np.linspace(0.0, 1.0, _N_POINTS)
    fond = 0.12 + 0.20 * np.exp(-5.0 * t)
    return fond * np.exp(rng.normal(0.0, 0.05, size=_N_POINTS))


def _sans_ancre() -> Journal:
    rng = np.random.default_rng(1505)
    return Journal(
        titre="Cube : cible de valeur sans ancre (courbes reconstruites)",
        description=_AVERTISSEMENT,
        pas=_axe(),
        perte_politique=_perte_politique(rng),
        perte_valeur=_perte_valeur_sans_ancre(rng),
    )


def _avec_ancre() -> Journal:
    rng = np.random.default_rng(1507)
    return Journal(
        titre="Cube : cible de valeur ancree sur l'etat resolu (courbes reconstruites)",
        description=_AVERTISSEMENT,
        pas=_axe(),
        perte_politique=_perte_politique(rng),
        perte_valeur=_perte_valeur_avec_ancre(rng),
    )


_JOURNAUX = {
    "cube-sans-ancre": _sans_ancre,
    "cube-avec-ancre": _avec_ancre,
}


def journaux_disponibles() -> list[str]:
    """Les noms acceptes par `charger_journal`, dans un ordre stable."""
    return sorted(_JOURNAUX)


def charger_journal(nom: str) -> Journal:
    """Rend le journal `nom`. Deux appels rendent les memes nombres."""
    try:
        fabrique = _JOURNAUX[nom]
    except KeyError:
        raise KeyError(
            f"journal inconnu : {nom!r}. Journaux disponibles : "
            f"{', '.join(journaux_disponibles())}"
        ) from None
    return fabrique()
