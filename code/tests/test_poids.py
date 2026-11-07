"""Conversion d'un point de controle SB3 vers le reseau de la section 5.8.

Le volet C de la semaine 5 n'entraine rien : il charge des poids et ecrit la boucle
d'evaluation. Reste a produire les poids, et un entrainement complet sur Pong demande
une a trois heures, ce que le laboratoire dit lui-meme.

La conversion est un pur renommage de cles : l'architecture de SB3 (NatureCNN plus une
tete lineaire) a exactement les memes formes que le reseau de la section 5.8. Ces
tests le verifient sur des etats fabriques, sans rien telecharger.

Le reseau de reference ci-dessous reproduit celui de la section 5.8, qui est publie
en entier sur la page : le reecrire ici ne divulgue aucun exercice, et sans lui on ne
pourrait pas verifier que la conversion charge en mode strict.
"""
from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")
import torch.nn as nn  # noqa: E402

from sci1070.poids import CORRESPONDANCE, cles_attendues, convertir_sb3  # noqa: E402


class DQN(nn.Module):
    """Le reseau de la section 5.8, reproduit pour le test."""

    def __init__(self, forme_entree, n_actions: int):
        super().__init__()
        self.convolutions = nn.Sequential(
            nn.Conv2d(forme_entree[0], 32, kernel_size=8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1), nn.ReLU(),
            nn.Flatten(),
        )
        with torch.no_grad():
            taille = self.convolutions(torch.zeros(1, *forme_entree)).shape[1]
        self.tete = nn.Sequential(
            nn.Linear(taille, 512), nn.ReLU(),
            nn.Linear(512, n_actions),
        )

    def forward(self, obs):
        return self.tete(self.convolutions(obs.float() / 255.0))


FORME = (4, 84, 84)
N_ACTIONS = 6


def etat_sb3_fabrique(n_actions: int = N_ACTIONS) -> dict:
    """Un state_dict de la forme que SB3 produit, valeurs arbitraires mais distinctes."""
    formes = {
        "q_net.features_extractor.cnn.0.weight": (32, 4, 8, 8),
        "q_net.features_extractor.cnn.0.bias": (32,),
        "q_net.features_extractor.cnn.2.weight": (64, 32, 4, 4),
        "q_net.features_extractor.cnn.2.bias": (64,),
        "q_net.features_extractor.cnn.4.weight": (64, 64, 3, 3),
        "q_net.features_extractor.cnn.4.bias": (64,),
        "q_net.features_extractor.linear.0.weight": (512, 3136),
        "q_net.features_extractor.linear.0.bias": (512,),
        "q_net.q_net.0.weight": (n_actions, 512),
        "q_net.q_net.0.bias": (n_actions,),
    }
    g = torch.Generator().manual_seed(0)
    etat = {k: torch.randn(*f, generator=g) for k, f in formes.items()}
    # SB3 livre aussi le reseau cible : la conversion doit l'ignorer, pas s'en plaindre.
    etat.update({k.replace("q_net.", "q_net_target.", 1): v.clone()
                 for k, v in list(etat.items())})
    return etat


class TestCorrespondance:
    def test_elle_couvre_les_cinq_couches(self):
        assert len(CORRESPONDANCE) == 5

    def test_les_cibles_sont_celles_du_reseau_de_la_section_5_8(self):
        attendu = {"convolutions.0", "convolutions.2", "convolutions.4", "tete.0", "tete.2"}
        assert set(CORRESPONDANCE.values()) == attendu

    def test_cles_attendues_rend_poids_et_biais_de_chaque_couche(self):
        cles = cles_attendues()
        assert len(cles) == 10
        assert all(c.endswith((".weight", ".bias")) for c in cles)


class TestConversion:
    def test_rend_exactement_les_cles_du_reseau_du_cours(self):
        converti = convertir_sb3(etat_sb3_fabrique())
        assert set(converti) == set(cles_attendues())

    def test_charge_en_mode_strict_dans_le_reseau_de_la_section_5_8(self):
        # C'est le seul test qui compte vraiment : si celui-ci passe, l'etudiant
        # peut faire load_state_dict sans argument et sans surprise.
        reseau = DQN(FORME, N_ACTIONS)
        reseau.load_state_dict(convertir_sb3(etat_sb3_fabrique()), strict=True)

    def test_les_valeurs_sont_transportees_sans_modification(self):
        source = etat_sb3_fabrique()
        converti = convertir_sb3(source)
        assert torch.equal(converti["convolutions.0.weight"],
                           source["q_net.features_extractor.cnn.0.weight"])
        assert torch.equal(converti["tete.2.bias"], source["q_net.q_net.0.bias"])

    def test_le_reseau_cible_de_sb3_est_ignore(self):
        source = etat_sb3_fabrique()
        converti = convertir_sb3(source)
        assert not any("target" in c for c in converti)

    def test_accepte_un_nombre_d_actions_different(self):
        reseau = DQN(FORME, 4)
        reseau.load_state_dict(convertir_sb3(etat_sb3_fabrique(n_actions=4)), strict=True)

    def test_un_etat_incomplet_est_refuse_en_nommant_ce_qui_manque(self):
        source = etat_sb3_fabrique()
        del source["q_net.q_net.0.weight"]
        with pytest.raises(KeyError) as exc:
            convertir_sb3(source)
        assert "q_net.q_net.0.weight" in str(exc.value)

    def test_un_etat_qui_n_est_pas_du_sb3_est_refuse_clairement(self):
        with pytest.raises(KeyError) as exc:
            convertir_sb3({"convolutions.0.weight": torch.zeros(32, 4, 8, 8)})
        assert "SB3" in str(exc.value) or "sb3" in str(exc.value)

    def test_une_forme_inattendue_est_refusee(self):
        # Un point de controle entraine sur une autre pile d'images (trois trames au
        # lieu de quatre) chargerait silencieusement si on ne verifiait pas.
        source = etat_sb3_fabrique()
        source["q_net.features_extractor.cnn.0.weight"] = torch.zeros(32, 3, 8, 8)
        with pytest.raises(ValueError, match="forme"):
            convertir_sb3(source)

    def test_contre_un_vrai_modele_sb3_et_non_une_transcription(self):
        """Le seul test qui attrape un changement de disposition chez SB3.

        Les autres partent d'un state_dict fabrique d'apres ce que SB3 produit
        aujourd'hui. Celui-ci construit un vrai modele et convertit SA sortie : si
        une version future renomme ses couches, il echoue ici plutot que chez
        l'etudiant.
        """
        sb3 = pytest.importorskip("stable_baselines3")
        import warnings

        import numpy as np
        from gymnasium import spaces

        warnings.filterwarnings("ignore")
        import gymnasium as gym

        class FauxAtari(gym.Env):
            observation_space = spaces.Box(0, 255, FORME, dtype=np.uint8)
            action_space = spaces.Discrete(N_ACTIONS)

            def reset(self, seed=None, options=None):
                return self.observation_space.sample(), {}

            def step(self, action):
                return self.observation_space.sample(), 0.0, False, False, {}

        modele = sb3.DQN("CnnPolicy", FauxAtari(), buffer_size=10, learning_starts=10**6)
        converti = convertir_sb3(modele.policy.state_dict())

        reseau = DQN(FORME, N_ACTIONS)
        reseau.load_state_dict(converti, strict=True)

        # Et les deux reseaux doivent rendre la MEME chose sur la meme entree :
        # un renommage qui melangerait deux couches passerait load_state_dict sans
        # broncher, et seule une comparaison numerique l'attrape.
        #
        # L'entree est passee BRUTE aux deux. SB3 divise par 255 dans son
        # preprocessing, le reseau de la section 5.8 divise dans son forward : lui
        # donner une entree deja normalisee la diviserait deux fois, ce qui ecrase
        # tout vers zero et rend deux lots differents indistinguables.
        entree = torch.randint(0, 256, (2, *FORME), dtype=torch.uint8)
        reseau.eval()
        modele.policy.set_training_mode(False)
        with torch.no_grad():
            attendu = modele.policy.q_net(entree)
            obtenu = reseau(entree)
        assert torch.allclose(attendu, obtenu, atol=1e-5), (
            "la conversion ne reproduit pas la sortie de SB3 : une couche est "
            "mal appariee, ou le pretraitement differe"
        )

    def test_la_sortie_passe_une_vraie_passe_avant(self):
        reseau = DQN(FORME, N_ACTIONS)
        reseau.load_state_dict(convertir_sb3(etat_sb3_fabrique()))
        reseau.eval()
        with torch.no_grad():
            sortie = reseau(torch.zeros(2, *FORME, dtype=torch.uint8))
        assert sortie.shape == (2, N_ACTIONS)
        assert torch.all(torch.isfinite(sortie))
