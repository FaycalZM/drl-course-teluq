"""Les journaux d'entrainement fournis pour le volet B de la semaine 15.

Le volet est une DEMONSTRATION : l'etudiant ne lance rien, il lit deux courbes et
les diagnostique. Il faut donc que les courbes portent reellement le phenomene que
la section 15.5 decrit, sinon le diagnostic demande est impossible a poser.

Ces journaux sont **reconstruits**, pas mesures : six jours de processeur graphique
separent ce cours d'un entrainement reel. Le dernier test de ce fichier verifie que
la description le dit, parce qu'une courbe reconstruite presentee comme une mesure
serait exactement la malhonnetete que le volet D apprend a reperer.
"""
from __future__ import annotations

import numpy as np
import pytest

from sci1070.donnees import Journal, charger_journal, journaux_disponibles


@pytest.mark.parametrize("nom", journaux_disponibles())
class TestFormeGenerale:
    def test_rend_un_journal(self, nom):
        assert isinstance(charger_journal(nom), Journal)

    def test_les_trois_series_ont_la_meme_longueur(self, nom):
        j = charger_journal(nom)
        assert len(j.pas) == len(j.perte_politique) == len(j.perte_valeur)

    def test_les_pas_sont_strictement_croissants(self, nom):
        j = charger_journal(nom)
        assert np.all(np.diff(j.pas) > 0)

    def test_les_pertes_sont_finies_et_positives(self, nom):
        j = charger_journal(nom)
        for serie in (j.perte_politique, j.perte_valeur):
            assert np.all(np.isfinite(serie)) and np.all(serie > 0)

    def test_assez_de_points_pour_etre_lisible(self, nom):
        assert len(charger_journal(nom).pas) >= 100

    def test_deux_chargements_rendent_les_memes_nombres(self, nom):
        assert np.array_equal(charger_journal(nom).perte_valeur,
                              charger_journal(nom).perte_valeur)

    def test_la_description_annonce_une_reconstruction(self, nom):
        # Le volet D de cette meme semaine apprend a reperer un rapport qui omet
        # ses reserves. Un journal reconstruit presente comme une mesure serait
        # precisement cela.
        texte = (charger_journal(nom).description + charger_journal(nom).titre).lower()
        assert "reconstruit" in texte


class TestLePhenomeneEstBienLa:
    """Sans ces proprietes, le diagnostic demande par l'etape 1 est impossible."""

    def test_la_perte_de_valeur_commence_par_un_plateau(self):
        j = charger_journal("cube-sans-ancre")
        debut = j.perte_valeur[: len(j.perte_valeur) // 4]
        assert debut.std() / debut.mean() < 0.15, "le plateau initial n'est pas plat"

    def test_la_perte_de_valeur_quitte_son_plateau_et_monte(self):
        j = charger_journal("cube-sans-ancre")
        plateau = j.perte_valeur[: len(j.perte_valeur) // 4].mean()
        fin = j.perte_valeur[-len(j.perte_valeur) // 10:].mean()
        assert fin > 10 * plateau, "la divergence de valeur ne se voit pas"

    def test_la_perte_de_politique_ne_previent_pas(self):
        """C'est le point du volet : une seule des deux courbes alerte.

        Si la perte de politique divergeait elle aussi, la troisieme question de
        l'etape 1 (« laquelle aurait declenche une alerte ») n'aurait pas de
        reponse, et le volet s'effondrerait.
        """
        j = charger_journal("cube-sans-ancre")
        debut = j.perte_politique[: len(j.perte_politique) // 4].mean()
        fin = j.perte_politique[-len(j.perte_politique) // 10:].mean()
        assert fin < debut, "la perte de politique doit descendre sagement"

    def test_le_journal_avec_ancre_ne_diverge_pas(self):
        j = charger_journal("cube-avec-ancre")
        plateau = j.perte_valeur[: len(j.perte_valeur) // 4].mean()
        fin = j.perte_valeur[-len(j.perte_valeur) // 10:].mean()
        assert fin < 3 * plateau, "le correctif devrait tenir l'echelle"

    def test_les_deux_journaux_partagent_le_meme_axe(self):
        # Sinon on ne peut pas les superposer, et la comparaison est impossible.
        a, b = charger_journal("cube-sans-ancre"), charger_journal("cube-avec-ancre")
        assert np.array_equal(a.pas, b.pas)


class TestLoader:
    def test_les_deux_journaux_attendus_sont_la(self):
        assert set(journaux_disponibles()) >= {"cube-sans-ancre", "cube-avec-ancre"}

    def test_un_journal_inconnu_nomme_les_journaux_connus(self):
        with pytest.raises(KeyError) as exc:
            charger_journal("pas-un-journal")
        assert "cube-sans-ancre" in str(exc.value)
