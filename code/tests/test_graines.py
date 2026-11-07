"""Fixer les graines des trois sources de hasard (section 7.2).

La section est explicite : fixer les graines est **necessaire et pas suffisant**.
Ces tests verifient le necessaire, et le dernier verifie que la fonction ne pretend
pas fournir le suffisant.
"""
from __future__ import annotations

import random

import numpy as np
import pytest

from sci1070.graines import fixer_graines

torch = pytest.importorskip("torch", reason="le volet graines de torch n'est pas teste sans torch")


def test_rend_un_generateur_numpy():
    rng = fixer_graines(0)
    assert isinstance(rng, np.random.Generator)


def test_deux_appels_a_la_meme_graine_donnent_la_meme_suite_numpy():
    a = fixer_graines(7).random(5)
    b = fixer_graines(7).random(5)
    assert a == pytest.approx(b)


def test_deux_graines_differentes_donnent_des_suites_differentes():
    a = fixer_graines(1).random(5)
    b = fixer_graines(2).random(5)
    assert not np.allclose(a, b)


def test_fixe_le_module_random_de_la_bibliotheque_standard():
    fixer_graines(3)
    a = [random.random() for _ in range(4)]
    fixer_graines(3)
    b = [random.random() for _ in range(4)]
    assert a == pytest.approx(b)


def test_fixe_le_hasard_global_de_numpy():
    # Beaucoup de code etudiant utilise np.random.rand plutot qu'un Generator ;
    # laisser cette source libre rendrait la reproductibilite partielle et
    # d'autant plus difficile a diagnostiquer.
    fixer_graines(4)
    a = np.random.rand(4)
    fixer_graines(4)
    b = np.random.rand(4)
    assert a == pytest.approx(b)


def test_fixe_torch():
    fixer_graines(5)
    a = torch.randn(4)
    fixer_graines(5)
    b = torch.randn(4)
    assert torch.allclose(a, b)


def test_un_reseau_initialise_apres_la_meme_graine_a_les_memes_poids():
    # C'est l'usage reel : on veut que deux executions partent du meme reseau.
    fixer_graines(11)
    a = torch.nn.Linear(6, 3).weight.detach().clone()
    fixer_graines(11)
    b = torch.nn.Linear(6, 3).weight.detach().clone()
    assert torch.allclose(a, b)


def test_refuse_une_graine_non_entiere():
    with pytest.raises(TypeError):
        fixer_graines(1.5)


def test_refuse_une_graine_negative():
    with pytest.raises(ValueError):
        fixer_graines(-1)
