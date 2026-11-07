"""Gardes sur les carnets livres aux etudiants.

Un carnet casse ne se voit pas a la relecture : Colab n'ouvre pas un .ipynb invalide,
une coquille de syntaxe n'apparait qu'a l'execution de la cellule, et un `...` oublie
se lit comme du code correct. D'ou ces tests.

`test_chaque_semaine_a_son_carnet` est le pilote du chantier : il reste rouge tant que
les quinze carnets ne sont pas ecrits, et c'est exactement ce qu'on lui demande.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parent.parent.parent      # drl-course/
CARNETS = RACINE / "notebooks"
CONTENU = RACINE / "content" / "docs"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from build_notebooks import construire_carnet  # noqa: E402

BADGE = re.compile(r"\{\{<\s*colab")
MAGIE = re.compile(r"^\s*[!%]")


def semaines_avec_badge() -> list[int]:
    """Les semaines dont une page porte au moins un badge Colab."""
    vues: set[int] = set()
    for page in CONTENU.glob("*/week*/*.md"):
        if BADGE.search(page.read_text(encoding="utf-8")):
            vues.add(int(page.parent.name.removeprefix("week")))
    return sorted(vues)


def carnets_construits() -> list[Path]:
    return sorted(CARNETS.glob("semaine-*.ipynb"))


def code_executable(cellule: dict) -> str:
    """La source d'une cellule de code, magies de carnet retirees.

    `!pip install` et `%matplotlib` sont valides dans un carnet et invalides en
    Python. On les remplace par `pass` **a leur indentation**, et non par du vide :
    une magie seule dans un bloc `if` ou `except` laisserait sinon un bloc vide,
    donc une fausse erreur de syntaxe.
    """
    lignes = "".join(cellule["source"]).splitlines()
    sortie = []
    for ligne in lignes:
        if MAGIE.match(ligne):
            indentation = ligne[: len(ligne) - len(ligne.lstrip())]
            sortie.append(f"{indentation}pass")
        else:
            sortie.append(ligne)
    return "\n".join(sortie)


@pytest.fixture(scope="module")
def carnets() -> list[tuple[Path, dict]]:
    sortie = []
    for chemin in carnets_construits():
        sortie.append((chemin, json.loads(chemin.read_text(encoding="utf-8"))))
    return sortie


def test_il_existe_au_moins_un_carnet():
    assert carnets_construits(), "aucun carnet construit dans notebooks/"


def test_chaque_carnet_est_un_nbformat_4_valide(carnets):
    for chemin, nb in carnets:
        assert nb["nbformat"] == 4, chemin.name
        assert isinstance(nb["cells"], list) and nb["cells"], chemin.name


def test_chaque_cellule_de_code_est_du_python_valide(carnets):
    fautes = []
    for chemin, nb in carnets:
        for i, cellule in enumerate(nb["cells"]):
            if cellule["cell_type"] != "code":
                continue
            try:
                ast.parse(code_executable(cellule))
            except SyntaxError as exc:
                fautes.append(f"{chemin.name} cellule {i} : {exc}")
    assert not fautes, "\n".join(fautes)


def test_aucun_carnet_n_est_livre_avec_des_sorties(carnets):
    # Une sortie commise, c'est une figure que l'etudiant croit avoir produite.
    for chemin, nb in carnets:
        for i, cellule in enumerate(nb["cells"]):
            assert cellule.get("outputs", []) == [], f"{chemin.name} cellule {i}"


def test_chaque_trou_annonce_est_un_trou_reel(carnets):
    """« À COMPLÉTER » doit accompagner un `...`, jamais du code deja ecrit.

    Autrement le commentaire ment : l'etudiant croit avoir un exercice et la cellule
    s'execute sans rien lui demander.
    """
    fautes = []
    for chemin, nb in carnets:
        for i, cellule in enumerate(nb["cells"]):
            if cellule["cell_type"] != "code":
                continue
            for ligne in "".join(cellule["source"]).splitlines():
                if "À COMPLÉTER" in ligne and "..." not in ligne:
                    fautes.append(f"{chemin.name} cellule {i} : {ligne.strip()[:70]}")
    assert not fautes, "\n".join(fautes)


def test_chaque_carnet_correspond_a_sa_source(carnets):
    """Le .ipynb commis doit etre celui que la source produit.

    Sinon une correction faite dans src/ ne part jamais chez l'etudiant, et la
    source cesse d'etre la verite.
    """
    perimes = []
    for chemin, nb in carnets:
        source = CARNETS / "src" / f"{chemin.stem}.py"
        if not source.exists():
            perimes.append(f"{chemin.name} : aucune source dans src/")
            continue
        attendu = construire_carnet(source.read_text(encoding="utf-8"), titre=chemin.stem)
        if attendu != nb:
            perimes.append(f"{chemin.name} : perime, relancez tools/build_notebooks.py")
    assert not perimes, "\n".join(perimes)


def test_les_cellules_completes_s_executent(carnets):
    """Execute, carnet par carnet, les cellules declarees « smoke ».

    La plupart des cellules d'un carnet sont des exercices a trous et ne peuvent pas
    tourner : ce serait la solution. Celles qui sont completes -- les demonstrations
    reprises des sections, les cellules d'installation, les verifications fournies --
    sont marquees dans la source par « # %% [smoke] », et elles, elles doivent passer.
    """
    import matplotlib

    matplotlib.use("Agg")      # aucun ecran dans un test

    for chemin, nb in carnets:
        espace: dict = {"__name__": "__main__"}
        for i, cellule in enumerate(nb["cells"]):
            if not cellule.get("metadata", {}).get("sci1070", {}).get("smoke"):
                continue
            code = code_executable(cellule)
            try:
                exec(compile(code, f"{chemin.name}#{i}", "exec"), espace)
            except Exception as exc:        # noqa: BLE001 - on veut le contexte
                pytest.fail(
                    f"{chemin.name} cellule {i} ({type(exc).__name__}): {exc}\n"
                    f"--- code ---\n{code[:600]}"
                )


def test_chaque_semaine_a_son_carnet():
    """Pilote du chantier : rouge tant que les quinze carnets ne sont pas la."""
    attendues = semaines_avec_badge()
    presentes = {int(p.stem.removeprefix("semaine-")) for p in carnets_construits()}
    manquantes = [n for n in attendues if n not in presentes]
    assert not manquantes, (
        f"semaines sans carnet : {manquantes} "
        f"({len(presentes)}/{len(attendues)} faits)"
    )
