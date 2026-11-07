"""Le convertisseur source-percent -> .ipynb.

Les carnets sont ecrits a la main dans notebooks/src/semaine-NN.py, au format
« percent », parce qu'un .ipynb est du JSON et qu'on ne relit pas du JSON. Le
convertisseur ne decide de rien : il change le format, il n'ecrit pas de contenu.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from build_notebooks import construire_carnet  # noqa: E402


def cellules(source: str) -> list[dict]:
    return construire_carnet(source)["cells"]


class TestDecoupage:
    def test_une_cellule_de_code_simple(self):
        c = cellules("# %%\nprint('bonjour')\n")
        assert len(c) == 1
        assert c[0]["cell_type"] == "code"
        assert "".join(c[0]["source"]) == "print('bonjour')"

    def test_une_cellule_markdown_perd_son_prefixe_de_commentaire(self):
        c = cellules("# %% [markdown]\n# # Titre\n# Du texte.\n")
        assert c[0]["cell_type"] == "markdown"
        assert "".join(c[0]["source"]) == "# Titre\nDu texte."

    def test_alterne_markdown_et_code(self):
        src = "# %% [markdown]\n# Intro\n\n# %%\nx = 1\n\n# %% [markdown]\n# Fin\n"
        assert [x["cell_type"] for x in cellules(src)] == ["markdown", "code", "markdown"]

    def test_le_texte_avant_le_premier_marqueur_est_refuse(self):
        # Sinon il disparaitrait silencieusement du carnet produit.
        with pytest.raises(ValueError, match="avant le premier marqueur"):
            construire_carnet("import os\n\n# %%\nx = 1\n")

    def test_une_source_sans_aucun_marqueur_est_refusee(self):
        with pytest.raises(ValueError, match="aucun marqueur"):
            construire_carnet("print('rien')\n")

    def test_une_cellule_vide_est_ignoree(self):
        c = cellules("# %%\n\n# %%\nx = 1\n")
        assert len(c) == 1

    def test_une_ligne_de_commentaire_vide_en_markdown_devient_une_ligne_vide(self):
        c = cellules("# %% [markdown]\n# Un\n#\n# Deux\n")
        assert "".join(c[0]["source"]) == "Un\n\nDeux"

    def test_un_commentaire_ordinaire_survit_dans_une_cellule_de_code(self):
        c = cellules("# %%\n# un vrai commentaire\nx = 1\n")
        assert "".join(c[0]["source"]) == "# un vrai commentaire\nx = 1"

    def test_une_ligne_non_commentee_en_markdown_est_refusee(self):
        # Erreur d'edition classique : on oublie le # en ajoutant un paragraphe.
        with pytest.raises(ValueError, match="markdown"):
            construire_carnet("# %% [markdown]\n# Du texte\nx = 1\n")


class TestMarqueurSmoke:
    """« # %% [smoke] » declare une cellule complete, qui doit s'executer telle quelle.

    C'est la seule facon de tester un carnet dont la plupart des cellules sont des
    exercices a trous : on n'execute que celles qui n'en ont pas.
    """

    def test_une_cellule_smoke_est_une_cellule_de_code(self):
        c = cellules("# %% [smoke]\nx = 1\n")
        assert c[0]["cell_type"] == "code"

    def test_une_cellule_smoke_est_marquee_dans_ses_metadonnees(self):
        c = cellules("# %% [smoke]\nx = 1\n")
        assert c[0]["metadata"]["sci1070"]["smoke"] is True

    def test_une_cellule_de_code_ordinaire_n_est_pas_marquee(self):
        c = cellules("# %%\nx = 1\n")
        assert "sci1070" not in c[0]["metadata"]

    def test_le_marqueur_n_apparait_pas_dans_la_source_vue_par_l_etudiant(self):
        c = cellules("# %% [smoke]\nx = 1\n")
        assert "smoke" not in "".join(c[0]["source"])

    def test_une_cellule_smoke_ne_peut_pas_contenir_de_trou(self):
        # Contradiction dans les termes : une cellule declaree executable qui
        # contient un `...` echouera a l'execution, donc le garde serait faux.
        with pytest.raises(ValueError, match="smoke"):
            construire_carnet("# %% [smoke]\nx = ...  # À COMPLÉTER\n")


class TestFormat:
    def test_produit_un_nbformat_4_valide(self):
        nb = construire_carnet("# %%\nx = 1\n")
        assert nb["nbformat"] == 4
        assert nb["nbformat_minor"] >= 5
        assert nb["metadata"]["kernelspec"]["name"] == "python3"

    def test_chaque_cellule_de_code_a_les_champs_attendus_de_nbformat(self):
        cell = cellules("# %%\nx = 1\n")[0]
        assert cell["execution_count"] is None
        assert cell["outputs"] == []
        assert "id" in cell

    def test_les_identifiants_de_cellules_sont_uniques(self):
        src = "# %%\na = 1\n\n# %%\nb = 2\n\n# %%\nc = 3\n"
        ids = [x["id"] for x in cellules(src)]
        assert len(set(ids)) == len(ids)

    def test_les_carnets_sont_livres_sans_sortie(self):
        # Une sortie commise, c'est une figure que l'etudiant croit avoir produite.
        for cell in cellules("# %%\nprint(1)\n\n# %%\nprint(2)\n"):
            assert cell.get("outputs") == []

    def test_la_source_est_une_liste_de_lignes_terminees_sauf_la_derniere(self):
        src_cell = cellules("# %%\na = 1\nb = 2\n")[0]
        assert src_cell["source"] == ["a = 1\n", "b = 2"]

    def test_le_json_produit_est_serialisable(self):
        json.dumps(construire_carnet("# %% [markdown]\n# Accents : éèàç\n"))
