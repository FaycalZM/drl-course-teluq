"""Les series de prix fournies pour le volet B de la semaine 7.

Le laboratoire dit « le jeu de donnees est fourni : vous n'avez aucune donnee de
marche a aller chercher ». C'est ce module. Il ne contient **pas** l'environnement
de negociation : l'ecrire est l'exercice, et ces tests ne doivent surtout pas en
tester un.

Ce qu'une serie doit garantir, c'est la coherence OHLC. Une barre dont le haut est
sous la cloture produit des rendements impossibles, et l'etudiant passerait sa
soiree a chercher le bogue dans sa recompense alors qu'il est dans les donnees.
"""
from __future__ import annotations

import numpy as np
import pytest

from sci1070.donnees import Prix, charger_prix, series_disponibles, series_synthetique


class TestInvariantsOHLC:
    @pytest.mark.parametrize("nom", series_disponibles())
    def test_chaque_serie_fournie_est_coherente(self, nom):
        p = charger_prix(nom)
        assert np.all(p.haut >= np.maximum(p.ouverture, p.cloture)), nom
        assert np.all(p.bas <= np.minimum(p.ouverture, p.cloture)), nom
        assert np.all(p.haut >= p.bas), nom
        assert np.all(p.ouverture > 0) and np.all(p.cloture > 0), nom
        assert np.all(p.volume > 0), nom

    @pytest.mark.parametrize("nom", series_disponibles())
    def test_les_cinq_tableaux_ont_la_meme_longueur(self, nom):
        p = charger_prix(nom)
        longueurs = {len(p.ouverture), len(p.haut), len(p.bas), len(p.cloture), len(p.volume)}
        assert len(longueurs) == 1, f"{nom} : longueurs {longueurs}"

    @pytest.mark.parametrize("nom", series_disponibles())
    def test_aucune_valeur_non_finie(self, nom):
        p = charger_prix(nom)
        for champ in ("ouverture", "haut", "bas", "cloture", "volume"):
            assert np.all(np.isfinite(getattr(p, champ))), f"{nom}.{champ}"

    @pytest.mark.parametrize("nom", series_disponibles())
    def test_assez_longue_pour_la_fenetre_par_defaut(self, nom):
        # Section 7.10 : b = 10 barres d'historique, plus une marge de 10b a la fin.
        p = charger_prix(nom)
        assert len(p.cloture) > 10 + 10 * 10, nom


class TestLoader:
    def test_il_existe_au_moins_une_serie(self):
        assert series_disponibles()

    def test_charger_rend_un_objet_prix(self):
        p = charger_prix(series_disponibles()[0])
        assert isinstance(p, Prix)

    def test_les_cinq_tableaux_sont_du_numpy_a_une_dimension(self):
        p = charger_prix(series_disponibles()[0])
        for champ in ("ouverture", "haut", "bas", "cloture", "volume"):
            a = getattr(p, champ)
            assert isinstance(a, np.ndarray) and a.ndim == 1, champ

    def test_charger_deux_fois_rend_les_memes_nombres(self):
        nom = series_disponibles()[0]
        assert np.array_equal(charger_prix(nom).cloture, charger_prix(nom).cloture)

    def test_une_serie_inconnue_leve_une_erreur_qui_nomme_les_series_connues(self):
        with pytest.raises(KeyError) as exc:
            charger_prix("pas-une-serie")
        assert series_disponibles()[0] in str(exc.value)


class TestSynthetique:
    def test_la_meme_graine_rend_la_meme_serie(self):
        a = series_synthetique(300, graine=7)
        b = series_synthetique(300, graine=7)
        assert np.array_equal(a.cloture, b.cloture)

    def test_deux_graines_rendent_deux_series(self):
        a = series_synthetique(300, graine=1)
        b = series_synthetique(300, graine=2)
        assert not np.array_equal(a.cloture, b.cloture)

    def test_respecte_la_longueur_demandee(self):
        assert len(series_synthetique(123, graine=0).cloture) == 123

    def test_respecte_les_invariants_ohlc(self):
        p = series_synthetique(500, graine=3)
        assert np.all(p.haut >= np.maximum(p.ouverture, p.cloture))
        assert np.all(p.bas <= np.minimum(p.ouverture, p.cloture))
        assert np.all(p.ouverture > 0)

    def test_refuse_une_longueur_trop_courte_pour_etre_utile(self):
        with pytest.raises(ValueError):
            series_synthetique(5, graine=0)


class TestSerieAPlat:
    """La serie « plate » : un cas de test, pas un marche.

    L'assertion 1 du volet B demande un achat puis une cloture SANS aucun mouvement
    de prix, qui doit rendre exactement -2*kappa. Fabriquer ce cas a la main est
    facile a rater (un centieme de variation suffit a fausser le nombre), donc la
    serie est fournie.
    """

    def test_tous_les_prix_sont_egaux(self):
        p = charger_prix("plate")
        assert len(np.unique(p.ouverture)) == 1
        assert np.array_equal(p.ouverture, p.cloture)
        assert np.array_equal(p.haut, p.bas)
        assert np.array_equal(p.haut, p.cloture)

    def test_le_rendement_d_un_aller_retour_est_nul_avant_commission(self):
        p = charger_prix("plate")
        assert float(p.cloture[-1] / p.cloture[0] - 1.0) == 0.0
