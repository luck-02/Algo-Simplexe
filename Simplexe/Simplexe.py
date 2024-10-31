from typing import List, Optional


# Fonction pour résoudre un problème d'optimisation linéaire Simplexe
# coef: Coefficients de la fonction objectif
# matrice_sous_contrainte: Matrice des contraintes
# vecteur: Côtés droits des inégalités
# type_inegalites: Type des inégalités
# maximisation: Maximiser ou minimiser (Sachant qu'on ne vas pas implémenter la minimisation)
def simplexe(
    coef: List[float],
    matrice_sous_contrainte: List[List[float]],
    vecteurs_Q,
    type_inegalite,
    maximisation=True,
):
    Z = 0

    # Création de la matrice des coefficients du bloc des contraintes
    matrice_coef_bloc_contrainte = matrice_sous_contrainte.copy()

    # Ajout des colonnes pour les variables d'écart
    for row in matrice_coef_bloc_contrainte:
        for _ in range(len(matrice_sous_contrainte)):
            row.append(0)

    # Remplissage des colonnes des variables d'écart
    for row_index in range(len(matrice_sous_contrainte)):
        if type_inegalite[row_index] == "<=":
            # On ajoute 1 pour les variables d'écart si c'est une inégalité <=
            matrice_coef_bloc_contrainte[row_index][
                row_index + len(matrice_sous_contrainte)
            ] = 1
        else:
            # On ajoute -1 pour les variables d'écart si c'est une inégalité >=
            matrice_coef_bloc_contrainte[row_index][
                row_index + len(matrice_sous_contrainte)
            ] = -1

    # Ajout des colonnes pour les variables d'écart
    for _ in range(len(matrice_sous_contrainte)):
        coef.append(0)

    # Création du vecteur Zj
    Zj = [0 for _ in range(len(coef))]

    # Création du vecteur Cj - Zj
    difference_Cj_Zj = [0 for _ in range(len(coef))]

    # Création du vecteur des coefficients pivot
    coef_pivot = [0 for _ in range(len(matrice_sous_contrainte))]

    for i in range(len(coef)):
        difference_Cj_Zj[i] = coef[i] - Zj[i]

    valeur_entrante = max(difference_Cj_Zj)
    colonne_valeur_entrante = difference_Cj_Zj.index(valeur_entrante)

    # Calcul de la valeur sortante
    min_value = vecteurs_Q[0] / matrice_coef_bloc_contrainte[0][colonne_valeur_entrante]
    index_min_value = 0

    for i in range(1, len(matrice_coef_bloc_contrainte)):
        if (
            vecteurs_Q[i] / matrice_coef_bloc_contrainte[i][colonne_valeur_entrante]
            < min_value
        ):
            min_value = (
                vecteurs_Q[i] / matrice_coef_bloc_contrainte[i][colonne_valeur_entrante]
            )
            index_min_value = i

    coef_pivot[index_min_value] = min_value

    ligne_pivot = matrice_coef_bloc_contrainte[index_min_value]

    pivot = matrice_coef_bloc_contrainte[index_min_value][colonne_valeur_entrante]

    Z = 0
    for i in range(len(coef_pivot)):
        Z = Z + coef_pivot[i] * vecteurs_Q[i]

    # ============== Affichage du tableau Simplexe =================
    VDB = [0 for _ in range(len(coef_pivot))]
    display_tab(
        coef,
        matrice_coef_bloc_contrainte,
        vecteurs_Q,
        coef_pivot,
        Z,
        Zj,
        difference_Cj_Zj,
        VDB,
    )
    # ===================== Fin de l'affichage =====================

    print("Pivot: ", pivot)
    print(
        "Position pivot: row:",
        index_min_value + 1,
        "column: x",
        colonne_valeur_entrante + 1,
    )


# Fonction pour afficher le tableau Simplexe
def display_tab(
    coef: List[float],
    matrice_sous_contrainte: List[List[float]],
    vecteurs_Q,
    coef_pivot,
    Z,
    Zj,
    difference_Cj_Zj,
    VDB,
):
    print("=================================================")
    print("Tableau Simplexe")
    print("Cj              |", coef, "| Ratio")
    print("-------------------------------------------------")
    if len(coef_pivot) == 2:
        print("CP   | VDB | Q  | x1 x2 x3 x4  |")
    else:
        print("CP   | VDB | Q  | x1 x2 x3 x4 x5 x6  |")
    print("-------------------------------------------------")
    for column in range(len(coef_pivot)):
        print(
            f"{coef_pivot[column]:.2f} | {VDB[column]}   | {vecteurs_Q[column]} | {matrice_sous_contrainte[column]} | todo"
        )
    print("Z =", Z, "  | Zj |", Zj)
    print("Cj - Zj         |", difference_Cj_Zj)


# =================== Testing ===================
# Coefficients de la fonction objectif
c = [4, 5, 6]

# Matrice des contraintes
A = [[2, 3, 1], [1, 4, 2], [3, 1, 2]]

# Côtés droits des inégalités
b = [10, 12, 14]

type_inegalite = ["<=", "<=", "<="]

# Appel de la fonction pour maximiser
print("3 Variables")
simplexe(c, A, b, type_inegalite, maximisation=True)

# Exemple avec 2 variables
c = [2, 3]
# Matrice des contraintes
A = [[1, 2], [2, 1]]

# Côtés droits des inégalités
b = [8, 10]

type_inegalite = ["<=", "<="]

# Appel de la fonction pour maximiser
# print("2 Variables")
# simplexe(c, A, b, type_inegalite, maximisation=True)
