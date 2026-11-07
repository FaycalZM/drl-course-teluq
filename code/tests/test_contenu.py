"""Gardes sur ce que les pages du cours promettent au sujet de l'outillage.

Une page peut vieillir sans que rien ne casse : le site se construit, les tests du
paquet passent, et c'est l'etudiant qui decouvre que l'identifiant cite n'existe
plus. Gymnasium retire ses anciennes versions a chaque generation, donc le cours
doit etre relu contre le registre, pas contre la memoire.

Trouve a l'ecriture des carnets : la semaine 4 annoncait `CliffWalking-v0`, retire
depuis Gymnasium 1.x, et la semaine 9 nommait `InvertedPendulum-v1`, qui n'a jamais
existe -- dans la meme page qui demande de « nommer l'environnement exactement ».
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import pytest

warnings.filterwarnings("ignore", category=DeprecationWarning)

import gymnasium as gym  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent.parent     # drl-course/
CONTENU = RACINE / "content"

IDENTIFIANT = re.compile(r"\b([A-Za-z][A-Za-z0-9]*(?:NoFrameskip)?-v[0-9]+)\b")

# Familles dont une dependance lourde n'est pas installee pour les tests : leur
# absence du registre ne prouve rien. MuJoCo et Atari s'installent a part.
SANS_DEPENDANCE_ICI = {"HalfCheetah", "Ant", "Hopper", "Walker2d", "Humanoid",
                       "InvertedPendulum", "InvertedDoublePendulum", "Swimmer",
                       "Reacher", "Pusher", "Pong", "Breakout"}


def identifiants_cites() -> dict[str, set[str]]:
    trouves: dict[str, set[str]] = {}
    for page in CONTENU.rglob("*.md"):
        for ident in IDENTIFIANT.findall(page.read_text(encoding="utf-8")):
            trouves.setdefault(ident, set()).add(str(page.relative_to(CONTENU)))
    return trouves


def test_le_cours_cite_au_moins_un_environnement():
    assert identifiants_cites(), "aucun identifiant trouve : le motif a-t-il change ?"


def test_aucun_identifiant_d_environnement_n_est_perime():
    """Un id absent du registre alors que sa famille y est : la version a ete retiree.

    C'est le cas grave, et le seul que ce test traite comme une erreur. Un id dont
    la famille entiere manque veut simplement dire que la dependance n'est pas
    installee pour les tests.
    """
    registre = set(gym.registry)
    familles = {x.rsplit("-v", 1)[0] for x in registre}

    perimes = []
    for ident, pages in sorted(identifiants_cites().items()):
        if ident in registre:
            continue
        famille = ident.rsplit("-v", 1)[0]
        if famille in SANS_DEPENDANCE_ICI and famille not in familles:
            continue
        if famille in familles:
            dispo = sorted(x for x in registre if x.rsplit("-v", 1)[0] == famille)
            perimes.append(
                f"{ident} cite dans {', '.join(sorted(pages))} "
                f"-> disponibles : {', '.join(dispo)}"
            )

    assert not perimes, "identifiant(s) perime(s) :\n  " + "\n  ".join(perimes)


@pytest.mark.parametrize("ident", ["CartPole-v1", "FrozenLake-v1", "Pendulum-v1"])
def test_les_environnements_du_tronc_commun_se_construisent(ident):
    """Les trois environnements sur lesquels reposent les laboratoires non MuJoCo."""
    env = gym.make(ident)
    obs, info = env.reset(seed=0)
    env.step(env.action_space.sample())
    env.close()
