"""Convertir un point de controle Stable-Baselines3 vers le reseau de la section 5.8.

**Pourquoi ce module existe.** Le volet C de la semaine 5 n'entraine rien : il charge
des poids et demande d'ecrire la chaine d'enveloppes et la boucle d'evaluation. Reste
a produire les poids, et le laboratoire dit lui-meme qu'un entrainement complet sur
Pong demande une a trois heures de processeur graphique.

**Pourquoi ce depot ne livre aucun fichier de poids.** Les points de controle publics
qui conviendraient sont publies sans licence declaree. Les redistribuer depuis le
depot d'un cours universitaire est une decision qui appartient a l'equipe pedagogique
et non a ce module. Ce que ce module fournit, c'est la **conversion**, testee : elle
marche sur n'importe quel point de controle DQN a politique convolutive de SB3, y
compris un que vous aurez entraine vous-meme.

**Pourquoi une conversion suffit.** L'architecture de SB3 pour les images est celle du
reseau de la section 5.8, aux noms pres : trois convolutions (32 en 8x8 pas 4, 64 en
4x4 pas 2, 64 en 3x3 pas 1), puis une couche de 512, puis une sortie par action. Les
formes sont identiques, donc la conversion est un **pur renommage de cles**, sans
aucune reinterpretation des nombres.

Trois facons d'obtenir un point de controle :

1. en entrainer un vous-meme avec SB3 et le convertir ici ;
2. en telecharger un depuis un depot public, apres avoir verifie sa licence, et le
   convertir ici ;
3. ecrire votre propre entrainement, auquel cas ce module ne vous sert a rien.

    from stable_baselines3 import DQN as DQN_SB3
    from sci1070.poids import convertir_sb3
    import torch

    modele = DQN_SB3.load("dqn-PongNoFrameskip-v4.zip")
    torch.save(convertir_sb3(modele.policy.state_dict()), "pong_poids.dat")
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

__all__ = ["CORRESPONDANCE", "FORMES_ATTENDUES", "cles_attendues", "convertir_sb3"]

# De la couche SB3 vers la couche du reseau de la section 5.8.
# SB3 range la couche de 512 dans son extracteur de caracteristiques ; le cours la
# range dans sa tete. C'est le seul endroit ou le decoupage differe, et il ne change
# rien aux nombres.
CORRESPONDANCE: dict[str, str] = {
    "q_net.features_extractor.cnn.0": "convolutions.0",
    "q_net.features_extractor.cnn.2": "convolutions.2",
    "q_net.features_extractor.cnn.4": "convolutions.4",
    "q_net.features_extractor.linear.0": "tete.0",
    "q_net.q_net.0": "tete.2",
}

# Les formes qui ne dependent pas du nombre d'actions. La derniere couche en depend,
# donc elle n'est pas listee : sa premiere dimension est verifiee par le chargement.
FORMES_ATTENDUES: dict[str, tuple[int, ...]] = {
    "convolutions.0.weight": (32, 4, 8, 8),
    "convolutions.2.weight": (64, 32, 4, 4),
    "convolutions.4.weight": (64, 64, 3, 3),
    "tete.0.weight": (512, 3136),
}


def cles_attendues() -> list[str]:
    """Les dix cles que le reseau de la section 5.8 attend, dans un ordre stable."""
    return [f"{cible}.{suffixe}"
            for cible in CORRESPONDANCE.values()
            for suffixe in ("weight", "bias")]


def convertir_sb3(etat_sb3: Mapping[str, Any]) -> dict[str, Any]:
    """Renomme un `policy.state_dict()` de SB3 vers le reseau de la section 5.8.

    Le reseau cible de SB3 (`q_net_target.*`) est ignore : en evaluation on ne charge
    que le reseau entraine, et les deux sont de toute facon identiques a la fin d'un
    entrainement.

    Leve `KeyError` si une couche manque, et `ValueError` si une forme ne correspond
    pas -- un point de controle entraine sur trois trames empilees au lieu de quatre
    se chargerait sinon sans rien dire, et l'etudiant chercherait le bogue dans sa
    chaine d'enveloppes.
    """
    if not any(cle.startswith("q_net.") for cle in etat_sb3):
        raise KeyError(
            "cet etat ne ressemble pas a un point de controle SB3 : aucune cle ne "
            "commence par 'q_net.'. Attendu : le resultat de "
            "`modele.policy.state_dict()` d'un DQN a politique convolutive. "
            f"Recu, par exemple : {sorted(etat_sb3)[:3]}"
        )

    converti: dict[str, Any] = {}
    for source, cible in CORRESPONDANCE.items():
        for suffixe in ("weight", "bias"):
            cle_source = f"{source}.{suffixe}"
            if cle_source not in etat_sb3:
                raise KeyError(
                    f"couche absente du point de controle : {cle_source}. "
                    "S'agit-il bien d'un DQN a politique convolutive (CnnPolicy) ?"
                )
            converti[f"{cible}.{suffixe}"] = etat_sb3[cle_source]

    for cle, forme in FORMES_ATTENDUES.items():
        reelle = tuple(converti[cle].shape)
        if reelle != forme:
            raise ValueError(
                f"forme inattendue pour {cle} : {reelle}, attendu {forme}. "
                "Le point de controle a-t-il ete entraine sur une autre pile "
                "d'images que les quatre trames de la section 5.8 ?"
            )

    return converti
