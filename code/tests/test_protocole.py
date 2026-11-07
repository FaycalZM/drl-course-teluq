"""Le protocole de mesure de la section 7.2.

Ces tests sont ecrits avant l'implementation. Ils fixent ce que le cours promet aux
etudiants : une moyenne n'est jamais rapportee seule, l'intervalle vient du
reechantillonnage, et deux intervalles qui se recouvrent ne separent rien.
"""
from __future__ import annotations

import numpy as np
import pytest

from sci1070.protocole import intervalle, mesurer, se_recouvrent


class TestIntervalle:
    def test_rend_moyenne_puis_bornes_dans_l_ordre(self):
        x = np.array([10.0, 12.0, 11.0, 13.0, 9.0])
        moyenne, bas, haut = intervalle(x)
        assert bas <= moyenne <= haut
        assert moyenne == pytest.approx(x.mean())

    def test_est_deterministe_a_graine_fixee(self):
        x = np.array([1.0, 5.0, 2.0, 8.0, 3.0])
        assert intervalle(x) == intervalle(x)

    def test_echantillon_constant_donne_un_intervalle_de_largeur_nulle(self):
        # Aucun bruit a estimer : les deux bornes tombent sur la constante.
        x = np.full(7, 42.0)
        moyenne, bas, haut = intervalle(x)
        assert (moyenne, bas, haut) == pytest.approx((42.0, 42.0, 42.0))

    def test_plus_l_echantillon_est_disperse_plus_l_intervalle_est_large(self):
        serre = np.array([10.0, 10.1, 9.9, 10.05, 9.95])
        large = np.array([2.0, 18.0, 5.0, 15.0, 10.0])
        _, b1, h1 = intervalle(serre)
        _, b2, h2 = intervalle(large)
        assert (h2 - b2) > (h1 - b1)

    def test_un_niveau_plus_eleve_donne_un_intervalle_plus_large(self):
        x = np.array([3.0, 7.0, 5.0, 9.0, 4.0, 6.0])
        _, b90, h90 = intervalle(x, niveau=0.90)
        _, b99, h99 = intervalle(x, niveau=0.99)
        assert (h99 - b99) >= (h90 - b90)

    def test_accepte_une_liste_python(self):
        # Les etudiants accumulent dans une liste ; refuser l'entree serait une
        # friction gratuite au moment ou ils rapportent leur mesure.
        moyenne, bas, haut = intervalle([4.0, 6.0, 5.0])
        assert bas <= moyenne <= haut

    def test_une_seule_graine_rend_un_intervalle_degenere(self):
        # Pas une erreur, mais rien n'est estime : c'est exactement le cas que la
        # section 7.2 refuse d'appeler un resultat.
        moyenne, bas, haut = intervalle([12.0])
        assert (moyenne, bas, haut) == pytest.approx((12.0, 12.0, 12.0))

    def test_refuse_un_echantillon_vide(self):
        with pytest.raises(ValueError):
            intervalle([])

    def test_refuse_un_niveau_hors_de_zero_un(self):
        for mauvais in (0.0, 1.0, -0.1, 1.5):
            with pytest.raises(ValueError):
                intervalle([1.0, 2.0, 3.0], niveau=mauvais)


class TestSeRecouvrent:
    def test_deux_echantillons_identiques_se_recouvrent(self):
        x = [10.0, 11.0, 9.0, 10.5, 9.5]
        assert se_recouvrent(x, list(x)) is True

    def test_deux_echantillons_bien_separes_ne_se_recouvrent_pas(self):
        bas = [1.0, 1.2, 0.8, 1.1, 0.9]
        haut = [50.0, 51.0, 49.0, 50.5, 49.5]
        assert se_recouvrent(bas, haut) is False

    def test_la_relation_est_symetrique(self):
        a = [1.0, 2.0, 3.0, 4.0, 5.0]
        b = [4.0, 5.0, 6.0, 7.0, 8.0]
        assert se_recouvrent(a, b) == se_recouvrent(b, a)


class TestMesurer:
    def test_appelle_l_execution_une_fois_par_graine_avec_la_graine_et_le_seuil(self):
        vus = []

        def execution(configuration, graine, seuil):
            vus.append((configuration, graine, seuil))
            return float(graine), float(graine) * 2.0

        fps, temps = mesurer("reference", [1, 2, 3], seuil=18, execution=execution)

        assert vus == [("reference", 1, 18), ("reference", 2, 18), ("reference", 3, 18)]
        assert fps == pytest.approx([1.0, 2.0, 3.0])
        assert temps == pytest.approx([2.0, 4.0, 6.0])

    def test_rend_des_tableaux_numpy_de_flottants(self):
        fps, temps = mesurer("c", [0, 1], seuil=1, execution=lambda c, graine, seuil: (1, 2))
        assert isinstance(fps, np.ndarray) and fps.dtype == np.float64
        assert isinstance(temps, np.ndarray) and temps.dtype == np.float64

    def test_refuse_une_liste_de_graines_vide(self):
        # Mesurer zero graine rendrait un tableau vide et un intervalle impossible ;
        # mieux vaut echouer ici que deux fonctions plus loin.
        with pytest.raises(ValueError):
            mesurer("c", [], seuil=1, execution=lambda c, graine, seuil: (1, 2))

    def test_refuse_des_graines_repetees(self):
        # Repeter une graine gonfle artificiellement n et retrecit l'intervalle.
        with pytest.raises(ValueError):
            mesurer("c", [3, 3], seuil=1, execution=lambda c, graine, seuil: (1, 2))
