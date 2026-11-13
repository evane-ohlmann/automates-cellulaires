"""
Automates cellulaires élémentaires (une dimension, deux états, rayon 1).

Chaque case d'une rangée vaut 0 (blanc) ou 1 (noir). À chaque étape, on calcule
une nouvelle rangée : la valeur d'une case dépend uniquement de sa voisine de
gauche, d'elle-même et de sa voisine de droite à l'étape précédente.
Les bords sont périodiques : la première et la dernière case sont voisines.

Les 256 règles possibles sont numérotées de 0 à 255 (classification de Wolfram).

Projet réalisé par Maud Sadrin et Evane Ohlmann.
"""

import numpy as np
import matplotlib.pyplot as plt


def regle_wolfram(numero):
    """Renvoie la règle de Wolfram de numéro donné (entre 0 et 255).

    Le voisinage (gauche, milieu, droite) est lu comme un nombre binaire entre 0 et 7.
    Le bit de même position dans l'écriture binaire du numéro donne le nouvel état.
    """
    if not 0 <= numero <= 255:
        raise ValueError("Le numéro d'une règle élémentaire est compris entre 0 et 255.")

    def regle(gauche, milieu, droite):
        return (numero >> (4 * gauche + 2 * milieu + droite)) & 1

    return regle


def automate(regle, n_etapes=100, n_cases=201, aleatoire=False, graine=42):
    """Fait évoluer un automate et renvoie la grille (une ligne par étape).

    - aleatoire=False : une seule case noire au centre au départ ;
    - aleatoire=True : première ligne tirée au hasard, avec une graine fixée
      pour que le résultat soit reproductible.
    """
    grille = np.zeros((n_etapes, n_cases), dtype=int)

    if aleatoire:
        rng = np.random.default_rng(graine)
        grille[0] = rng.integers(0, 2, n_cases)
    else:
        grille[0, n_cases // 2] = 1

    for t in range(1, n_etapes):
        precedente = grille[t - 1]
        gauche = np.roll(precedente, 1)    # voisine de gauche (bord périodique)
        droite = np.roll(precedente, -1)   # voisine de droite (bord périodique)
        grille[t] = regle(gauche, precedente, droite)

    return grille


def afficher(grille, titre, fichier=None):
    """Affiche la grille : les cases noires valent 1, les blanches 0."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(grille, cmap="binary", interpolation="nearest")
    ax.set_title(titre)
    ax.set_xlabel("Case")
    ax.set_ylabel("Étape")
    fig.tight_layout()
    if fichier:
        fig.savefig(fichier, dpi=150)
    return fig


# Les règles étudiées dans le projet
REGLES = {
    60: "Règle d'Étienne : noire si la case au-dessus à gauche et celle au-dessus diffèrent",
    90: "Règle 90 : noire si les cases au-dessus à gauche et à droite diffèrent",
    165: "Règle MCpL : noire si les cases au-dessus à gauche et à droite sont identiques",
    110: "Règle 110 : comportement complexe, capable en théorie de tout calcul",
}


if __name__ == "__main__":
    # Vérification : la règle 60 depuis une case reproduit le triangle de Pascal modulo 2
    test = automate(regle_wolfram(60), n_etapes=4, n_cases=9, aleatoire=False)
    assert test.tolist() == [
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0],
    ], "La règle 60 ne donne pas le résultat attendu"

    for numero, description in REGLES.items():
        print(f"Règle {numero} — {description}")
        for aleatoire in (False, True):
            depart = "aleatoire" if aleatoire else "une_case"
            grille = automate(regle_wolfram(numero), aleatoire=aleatoire)
            afficher(
                grille,
                f"Règle {numero}, départ {'aléatoire' if aleatoire else 'avec une case noire'}",
                fichier=f"images/regle_{numero}_{depart}.png",
            )
    plt.show()
