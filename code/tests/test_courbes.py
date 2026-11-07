"""Moyenne et plage ombree sur plusieurs graines (regle 2 de la section 7.2).

Une courbe de comparaison se trace en moyenne avec une plage ombree, jamais comme une
execution unique. Le calcul de la bande est teste ici ; le dessin est teste ailleurs
parce qu'un test n'a jamais besoin d'un ecran.
"""
from __future__ import annotations

import numpy as np
import pytest

from sci1070.courbes import bande, lisser


class TestBande:
    def test_rend_trois_courbes_de_la_longueur_des_entrees(self):
        courbes = np.array([[1.0, 2.0, 3.0], [3.0, 4.0, 5.0]])
        moyenne, bas, haut = bande(courbes)
        assert moyenne.shape == bas.shape == haut.shape == (3,)

    def test_la_moyenne_est_la_moyenne_par_colonne(self):
        courbes = [[0.0, 10.0], [2.0, 20.0]]
        moyenne, _, _ = bande(courbes)
        assert moyenne == pytest.approx([1.0, 15.0])

    def test_les_bornes_encadrent_la_moyenne(self):
        rng = np.random.default_rng(0)
        courbes = rng.normal(size=(5, 20))
        moyenne, bas, haut = bande(courbes)
        assert np.all(bas <= moyenne) and np.all(moyenne <= haut)

    def test_des_courbes_identiques_donnent_une_bande_plate(self):
        courbes = np.tile(np.array([1.0, 2.0, 3.0]), (4, 1))
        moyenne, bas, haut = bande(courbes)
        assert bas == pytest.approx(moyenne) and haut == pytest.approx(moyenne)

    def test_une_seule_courbe_donne_une_bande_de_largeur_nulle(self):
        moyenne, bas, haut = bande([[1.0, 2.0, 3.0]])
        assert bas == pytest.approx(moyenne) and haut == pytest.approx(moyenne)

    def test_refuse_des_courbes_de_longueurs_differentes(self):
        # Le piege reel : une execution s'arrete plus tot et on agrege quand meme.
        with pytest.raises(ValueError):
            bande([[1.0, 2.0, 3.0], [1.0, 2.0]])

    def test_refuse_un_ensemble_vide(self):
        with pytest.raises(ValueError):
            bande([])


class TestLisser:
    def test_conserve_la_longueur(self):
        assert lisser([1.0, 2.0, 3.0, 4.0], alpha=0.98).shape == (4,)

    def test_commence_sur_la_premiere_valeur(self):
        # Demarrer a zero creerait une fausse montee au debut de chaque courbe.
        y = lisser([5.0, 5.0, 5.0], alpha=0.98)
        assert y[0] == pytest.approx(5.0)

    def test_une_serie_constante_reste_constante(self):
        y = lisser(np.full(50, 7.0), alpha=0.9)
        assert y == pytest.approx(np.full(50, 7.0))

    def test_alpha_eleve_lisse_davantage(self):
        rng = np.random.default_rng(1)
        bruit = rng.normal(size=400)
        doux = lisser(bruit, alpha=0.99)
        vif = lisser(bruit, alpha=0.5)
        assert doux.std() < vif.std()

    def test_alpha_nul_rend_la_serie_inchangee(self):
        x = np.array([1.0, 9.0, 2.0])
        assert lisser(x, alpha=0.0) == pytest.approx(x)

    def test_refuse_un_alpha_hors_de_zero_un(self):
        for mauvais in (-0.1, 1.0, 1.5):
            with pytest.raises(ValueError):
                lisser([1.0, 2.0], alpha=mauvais)
