"""Convertit les sources « percent » des carnets en .ipynb.

Outil de maintenance du cours, pas du code etudiant : il n'entre pas dans la roue
(hatch n'empaquette que src/sci1070).

Pourquoi ce detour plutot que d'ecrire du .ipynb a la main : un carnet est du JSON,
une relecture de JSON ne detecte rien, et une diff de JSON encore moins. Les carnets
sont donc ecrits dans notebooks/src/semaine-NN.py, qui se lit et se compare, et ce
script en fabrique le .ipynb. Il ne decide d'aucun contenu -- il change le format.

    python tools/build_notebooks.py ../notebooks
    python tools/build_notebooks.py ../notebooks --verifier

`--verifier` ne reecrit rien et sort en code 1 si un .ipynb ne correspond plus a sa
source : c'est la forme utilisable dans un garde.

Format accepte :

    # %% [markdown]
    # Du texte, chaque ligne prefixee par « # ».

    # %%
    code = "tel quel"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MARQUEUR = re.compile(r"^#\s*%%(.*)$")
NBFORMAT_MINOR = 5


def _identifiant(graine: str) -> str:
    """Identifiant de cellule stable : la meme source rend le meme .ipynb.

    nbformat veut un id unique par cellule. Un uuid aleatoire ferait changer le
    fichier a chaque construction, donc une diff bruyante et un `--verifier`
    inutilisable. Celui-ci est derive du contenu.
    """
    return hashlib.sha1(graine.encode("utf-8")).hexdigest()[:16]


def _en_lignes(texte: str) -> list[str]:
    """nbformat veut une liste de lignes terminees par \\n, sauf la derniere."""
    if not texte:
        return []
    lignes = texte.split("\n")
    return [ligne + "\n" for ligne in lignes[:-1]] + [lignes[-1]]


def construire_carnet(source: str, titre: str = "") -> dict:
    """Rend le dictionnaire nbformat correspondant a une source percent."""
    lignes = source.splitlines()

    # Teste avant le balayage : sans ce garde, un fichier entierement depourvu de
    # marqueurs est signale comme « du contenu avant le premier marqueur », ce qui
    # est vrai mais envoie chercher une erreur d'edition la ou il manque tout.
    if not any(MARQUEUR.match(ligne) for ligne in lignes):
        raise ValueError("aucun marqueur « # %% » dans la source")

    blocs: list[tuple[str, list[str]]] = []
    courant: list[str] | None = None
    genre = "code"

    for numero, ligne in enumerate(lignes, start=1):
        m = MARQUEUR.match(ligne)
        if m:
            if courant is not None:
                blocs.append((genre, courant))
            options = m.group(1)
            if "[markdown]" in options:
                genre = "markdown"
            elif "[smoke]" in options:
                genre = "smoke"
            else:
                genre = "code"
            courant = []
            continue
        if courant is None:
            if ligne.strip():
                raise ValueError(
                    f"ligne {numero} : du contenu avant le premier marqueur « # %% ». "
                    "Il serait perdu silencieusement dans le carnet produit."
                )
            continue
        courant.append(ligne)

    if courant is None:
        raise ValueError("aucun marqueur « # %% » dans la source")
    blocs.append((genre, courant))

    cellules: list[dict] = []
    for genre, corps in blocs:
        texte = _nettoyer(genre, corps)
        if not texte.strip():
            continue
        cid = _identifiant(f"{titre}:{len(cellules)}:{texte}")
        if genre == "markdown":
            cellules.append(
                {"cell_type": "markdown", "id": cid, "metadata": {},
                 "source": _en_lignes(texte)}
            )
            continue

        metadonnees: dict = {}
        if genre == "smoke":
            if "..." in texte:
                raise ValueError(
                    "cellule « smoke » contenant un trou (`...`) : une cellule "
                    "declaree executable ne peut pas etre un exercice, sinon le "
                    "garde d'execution echoue a chaque fois.\n"
                    f"  {texte.strip()[:70]}"
                )
            metadonnees = {"sci1070": {"smoke": True}}
        cellules.append(
            {"cell_type": "code", "id": cid, "metadata": metadonnees,
             "execution_count": None, "outputs": [], "source": _en_lignes(texte)}
        )

    return {
        "cells": cellules,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        },
        "nbformat": 4,
        "nbformat_minor": NBFORMAT_MINOR,
    }


def _nettoyer(genre: str, corps: list[str]) -> str:
    if genre in ("code", "smoke"):
        return "\n".join(corps).strip("\n")

    sorties: list[str] = []
    for ligne in corps:
        nue = ligne.rstrip()
        if not nue:
            sorties.append("")
        elif nue == "#":
            sorties.append("")
        elif nue.startswith("# "):
            sorties.append(nue[2:])
        elif nue.startswith("#"):
            sorties.append(nue[1:])
        else:
            raise ValueError(
                f"cellule markdown : la ligne {nue[:50]!r} n'est pas commentee. "
                "Prefixez-la par « # », ou ouvrez une cellule de code."
            )
    return "\n".join(sorties).strip("\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("racine", type=Path, help="dossier notebooks/ (contenant src/)")
    p.add_argument("--verifier", action="store_true",
                   help="ne rien ecrire ; sortir en 1 si un carnet est perime")
    args = p.parse_args(argv)

    sources = sorted((args.racine / "src").glob("semaine-*.py"))
    if not sources:
        print(f"aucune source dans {args.racine / 'src'}", file=sys.stderr)
        return 1

    perimes: list[str] = []
    for src in sources:
        cible = args.racine / f"{src.stem}.ipynb"
        carnet = construire_carnet(src.read_text(encoding="utf-8"), titre=src.stem)
        rendu = json.dumps(carnet, ensure_ascii=False, indent=1) + "\n"
        if args.verifier:
            actuel = cible.read_text(encoding="utf-8") if cible.exists() else ""
            if actuel != rendu:
                perimes.append(cible.name)
            continue
        cible.write_text(rendu, encoding="utf-8")
        n = len(carnet["cells"])
        print(f"  {cible.name:24s} {n:3d} cellules")

    if args.verifier:
        if perimes:
            print("carnets perimes : " + ", ".join(perimes), file=sys.stderr)
            print("relancez : python tools/build_notebooks.py ../notebooks", file=sys.stderr)
            return 1
        print(f"{len(sources)} carnet(s) a jour")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
