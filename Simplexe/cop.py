# from typing import List, Optional

# #! Ne pas oublié de parler de la complexité de cette algorithme Simplexe

# # Fonction pour résoudre un problème d'optimisation linéaire Simplexe
# # coef: Coefficients de la fonction objectif
# # matrice_sous_contrainte: Matrice des contraintes
# # vecteur: Côtés droits des inégalités
# # type_inegalites: Type des inégalités
# # maximisation: Maximiser ou minimiser (Sachant qu'on ne vas pas implémenter la minimisation)
# def simplexe(
#     coef: List[float],
#     matrice_sous_contrainte: List[List[float]],
#     vecteurs_Q,
#     type_inegalite,
#     maximisation=True,
# ):
#     Z = 0

#     # Création de la matrice des coefficients du bloc des contraintes
#     matrice_coef_bloc_contrainte = matrice_sous_contrainte.copy()

#     # Ajout des colonnes pour les variables d'écart
#     for row in matrice_coef_bloc_contrainte:
#         for _ in range(len(matrice_sous_contrainte)):
#             row.append(0)

#     # Remplissage des colonnes des variables d'écart
#     for row_index in range(len(matrice_sous_contrainte)):
#         if type_inegalite[row_index] == "<=":
#             # On ajoute 1 pour les variables d'écart si c'est une inégalité <=
#             matrice_coef_bloc_contrainte[row_index][
#                 row_index + len(matrice_sous_contrainte)
#             ] = 1
#         else:
#             # On ajoute -1 pour les variables d'écart si c'est une inégalité >=
#             matrice_coef_bloc_contrainte[row_index][
#                 row_index + len(matrice_sous_contrainte)
#             ] = -1

#     # Ajout des colonnes pour les variables d'écart
#     for _ in range(len(matrice_sous_contrainte)):
#         coef.append(0)

#     # Création du vecteur Zj
#     Zj = [0 for _ in range(len(coef))]

#     # Création du vecteur Cj - Zj
#     difference_Cj_Zj = [0 for _ in range(len(coef))]

#     # Création du vecteur des coefficients pivot
#     coef_pivot = [0 for _ in range(len(matrice_sous_contrainte))]

#     for i in range(len(coef)):
#         difference_Cj_Zj[i] = coef[i] - Zj[i]

#     valeur_entrante = max(difference_Cj_Zj)
#     colonne_valeur_entrante = difference_Cj_Zj.index(valeur_entrante)

#     # Initialisation des variables dans base
#     vdb = ["" for _ in range(len(coef_pivot))]
#     for i in range(len(vdb)):
#         vdb[i] = "x" + str(i + len(coef_pivot) + 1)

#     # Initialisation des ratios
#     ratio = [0 for _ in range(len(matrice_coef_bloc_contrainte))]

#     # ============== Affichage du tableau Simplexe Initialisation =================
#     display_tab(
#         coef,
#         matrice_coef_bloc_contrainte,
#         vecteurs_Q,
#         coef_pivot,
#         Z,
#         Zj,
#         difference_Cj_Zj,
#         vdb,
#         ratio,
#     )
#     # ===================== Fin de l'affichage =====================

#     # Calcul de la valeur sortante
#     min_value = vecteurs_Q[0] / matrice_coef_bloc_contrainte[0][colonne_valeur_entrante]
#     index_min_value = 0

#     ratio[0] = vecteurs_Q[0] / matrice_coef_bloc_contrainte[0][colonne_valeur_entrante]

#     for i in range(1, len(matrice_coef_bloc_contrainte)):
#         if (
#             vecteurs_Q[i] / matrice_coef_bloc_contrainte[i][colonne_valeur_entrante]
#             < min_value
#         ):
#             min_value = (
#                 vecteurs_Q[i] / matrice_coef_bloc_contrainte[i][colonne_valeur_entrante]
#             )
#             index_min_value = i

#         ratio[i] = (
#             vecteurs_Q[i] / matrice_coef_bloc_contrainte[i][colonne_valeur_entrante]
#         )

#     coef_pivot[index_min_value] = min_value
#     pivot = matrice_coef_bloc_contrainte[index_min_value][colonne_valeur_entrante]
#     ligne_pivot = [x / pivot for x in matrice_coef_bloc_contrainte[index_min_value]]

#     vecteurs_Q[index_min_value] = vecteurs_Q[index_min_value] / pivot

#     matrice_coef_bloc_contrainte[index_min_value] = ligne_pivot

#     # Calcul des lignes par rapport à la ligne pivot
#     for row in range(len(matrice_coef_bloc_contrainte)):
#         if row != index_min_value:
#             coef_colonne_pivot = matrice_coef_bloc_contrainte[row][colonne_valeur_entrante]
#             print("coef_colonne_pivot", coef_colonne_pivot)
#             print("row de matrice_coef_bloc_contrainte", matrice_coef_bloc_contrainte[row])
#             matrice_coef_bloc_contrainte[row] = [
#                 x - coef_colonne_pivot * pivot for x in matrice_coef_bloc_contrainte[row]
#             ]
#             vecteurs_Q[row] = vecteurs_Q[row] - (coef_colonne_pivot * pivot)

#     print("ligne pivot", ligne_pivot)
#     print("vecteurs_Q", vecteurs_Q)

#     # division par le pivot pour la ligne pivot

#     # Calcul de Z
#     Z = 0
#     for i in range(len(coef_pivot)):
#         Z = Z + coef_pivot[i] * vecteurs_Q[i]

#     # Calcul pour trouver le nouveau Valeur Dans la Base
#     max_difference_Cj_Zj = max(difference_Cj_Zj)
#     print("Max difference Cj - Zj: ", max_difference_Cj_Zj)
#     index_max_difference_Cj_Zj = difference_Cj_Zj.index(max_difference_Cj_Zj)
#     print("Index max difference Cj - Zj: ", index_max_difference_Cj_Zj)

#     vdb[index_min_value] = "x" + str(index_max_difference_Cj_Zj + 1)

#     # ============== Affichage du tableau Simplexe =================
#     display_tab(
#         coef,
#         matrice_coef_bloc_contrainte,
#         vecteurs_Q,
#         coef_pivot,
#         Z,
#         Zj,
#         difference_Cj_Zj,
#         vdb,
#         ratio,
#     )
#     # ===================== Fin de l'affichage =====================

#     print("Pivot: ", pivot)
#     print(
#         "Position pivot: row:",
#         index_min_value + 1,
#         "column: x",
#         colonne_valeur_entrante + 1,
#     )


# # Fonction pour afficher le tableau Simplexe
# def display_tab(
#     coef: List[float],
#     matrice_sous_contrainte: List[List[float]],
#     vecteurs_Q,
#     coef_pivot,
#     Z,
#     Zj,
#     difference_Cj_Zj,
#     vdb,
#     ratio,
# ):
#     print("=================================================")
#     print("Tableau Simplexe")
#     print("Cj                                     |", coef, "   |  Ratio")
#     print("-------------------------------------------------")
#     if len(coef_pivot) == 2:
#         print("     CP      |    vdb    |      Q      | x1 x2 x3 x4  |")
#     else:
#         print("     CP      |    vdb    |      Q      | x1 x2 x3 x4 x5 x6                    |")
#     print("-------------------------------------------------")
#     for column in range(len(coef_pivot)):
#         print(
#             f"{coef_pivot[column]:.2f}         | {vdb[column]}        | {vecteurs_Q[column]:.1f}        | {matrice_sous_contrainte[column]}   | {ratio[column]:.2f}"
#         )
#     print("Z =", Z,"       |     Zj    |", Zj)
#     print("Cj - Zj          |", difference_Cj_Zj)


# # =================== Testing ===================
# # Coefficients de la fonction objectif
# c = [4, 5, 6]

# # Matrice des contraintes
# A = [[2, 3, 1], [1, 4, 2], [3, 1, 2]]

# # Côtés droits des inégalités
# b = [10, 12, 14]

# type_inegalite = ["<=", "<=", "<="]

# # Appel de la fonction pour maximiser
# print("3 Variables")
# simplexe(c, A, b, type_inegalite, maximisation=True)

# # Exemple avec 2 variables
# c = [2, 3]
# # Matrice des contraintes
# A = [[1, 2], [2, 1]]

# # Côtés droits des inégalités
# b = [8, 10]

# type_inegalite = ["<=", "<="]

# # Appel de la fonction pour maximiser
# # print("2 Variables")
# # simplexe(c, A, b, type_inegalite, maximisation=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
# Luc
#  A faire tant que les coefficients de la fonction objectif sont strictement positif

# Coeff fonction objectif :
objectif = [4, 5, 6]
# Coeff contraintes :
contraintes = [[2, 3, 1],
 [1, 4, 2],
 [3, 1, 2]]
# Quantité :
quantite = [10, 12, 14]

# # Coeff fonction objectif :
# objectif = [30, 50]
# # Coeff contraintes :
# contraintes = [[3, 2],
#  [1, 0],
#  [0, 1]]
# # Quantité :
# quantite = [1800, 400, 600]

size_contraintes = np.shape(contraintes)

# Comparaison :
inegalites = ["<=", "<=", "<="]

# Etape 1 : Ecrire le système sous forme standard

def forme_standard(contraintes, inegalites) :
    contraintes_standard = contraintes.copy()
    nb_colonnes_init = np.shape(contraintes)[1] #Sert a avoir le bon nombre de colonnes car la fonction copy n'empeche pas la modification de la liste originale

    # Ajout des colonnes pour les variables d'écart
    for lignes in contraintes_standard:
        for _ in range(len(contraintes_standard)):
            lignes.append(0)

    for lignes in range(len(contraintes_standard)):
        if inegalites[lignes] == "<=":
            # On ajoute 1 pour les variables d'écart si c'est une inégalité <=
            contraintes_standard[lignes][lignes + nb_colonnes_init] = 1
        else:
            # On ajoute -1 pour les variables d'écart si c'est une inégalité >=
            contraintes_standard[lignes][lignes + nb_colonnes_init] = -1
    return contraintes_standard

# tab = forme_standard(contraintes, inegalites)

# Etape 2 : Initialisation des paramètres

def initParam(tab, size_contraintes, objectif):
    nom_coeff = [f"X{i}" for i in range(1, np.shape(tab)[1] + 1)]
    cp = [0] * np.shape(tab)[0]
    vdb = nom_coeff[size_contraintes[1] - np.shape(tab)[1]:] #Le nombre de colonne final moins le nombre de colonnes initiales pour avoir les valeurs d'écarts ici VDB au départ
    ratio = [0] * np.shape(tab)[0]
    select_tab_vdb = (np.shape(tab)[1] - size_contraintes[1])
    objectif.extend([0] * select_tab_vdb) #Initialise Cj en lui rajoutant les zeros
    z = 0
    zj = [0] * np.shape(tab)[1]
    Cj_Zj = np.subtract(objectif, zj).tolist()
    max_Cj_Zj = max(Cj_Zj)
    return nom_coeff, cp, vdb, ratio, z, zj, Cj_Zj, max_Cj_Zj

# nom_coeff, cp, vdb, ratio, select_tab_vdb, z, zj, Cj_Zj, max_Cj_Zj = initParam(tab, size_contraintes, objectif)


def built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio):
    df_param = pd.DataFrame({"Cp": cp,"VDB": vdb,"Q": quantite,}) #Tables de gauche
    df_coeff = pd.DataFrame(tab, columns=nom_coeff) #Matrice de coefficients
    df_ratio = pd.DataFrame({"ratio": ratio}) #Table de ratios
    return pd.concat([df_param, df_coeff, df_ratio], axis=1)

# totals = pd.DataFrame([Zj], columns=nom_coeff)
# df = pd.concat([df_param, df_coeff, df_ratio], axis=1)
# df_final = pd.concat([df, totals], ignore_index=True)
# df_test = pd.DataFrame([0,0,0,0,0,0,0,0,0,0], columns=df_final.columns)
# print(df_test.columns)
# return df_final

# df_tab0 = built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio) 

def print_tab_simplex(z,df_tab, msg, zj, Cj_Zj):
    # # Affichage du DataFrame
    print("Tableau simplexe :", msg)
    print("               Cj", objectif)
    print(df_tab)
    print("       Z =", z, "| Zj", zj)
    print("          Cj - Zj", Cj_Zj)
    print(" ")

# print_tab_simplex(df_tab0, "Tableau initial")

def calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj):
    index_colonne_valeur_entrante = Cj_Zj.index(max_Cj_Zj)
    colonne_pivot = [ligne[index_colonne_valeur_entrante] for ligne in tab]
    return index_colonne_valeur_entrante, colonne_pivot

# index_colonne_valeur_entrante, colonne_pivot, valeur_entrante = calcule_v_entrante(tab, max_Cj_Zj, nom_coeff, Cj_Zj)

# Etape 4 : Choisir la variable à enlever de la base

def calcule_ratios(quantite, colonne_pivot):
    ratio = np.divide(quantite, colonne_pivot).tolist()
    return ratio

def calcule_v_sortante(tab, ratio):
    index_ligne_valeur_sortante = ratio.index(min(ratio))
    ligne_pivot = tab[index_ligne_valeur_sortante]
    return index_ligne_valeur_sortante, ligne_pivot

def calcule_pivot(tab, index_ligne_valeur_sortante, index_colonne_valeur_entrante ):
    return tab[index_ligne_valeur_sortante][index_colonne_valeur_entrante]

def ratio_pivot_a_jour(ratio, index_ligne_valeur_sortante, pivot):
    ratio[index_ligne_valeur_sortante] = ratio[index_ligne_valeur_sortante]/pivot


# ratio, min_ratio, index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, quantite, colonne_pivot)

# Etape 6 : Diviser la ligne du pivot par le pivot

def mise_a_jour_ligne_pivot(tab,pivot,index_ligne_valeur_sortante,index_colonne_valeur_entrante,ligne_pivot, nom_coeff, vdb, cp):
    ligne_pivot = [x / pivot for x in ligne_pivot]
    tab[index_ligne_valeur_sortante] = ligne_pivot
    quantite[index_ligne_valeur_sortante] = quantite[index_ligne_valeur_sortante]/pivot
    vdb[index_ligne_valeur_sortante] = nom_coeff[index_colonne_valeur_entrante]
    return cp, vdb, quantite, tab, nom_coeff, ligne_pivot

# cp, vdb, quantite, tab, nom_coeff, ratio = mise_a_jour_ligne_pivot(tab, index_ligne_valeur_sortante,index_colonne_valeur_entrante,ligne_pivot, nom_coeff, ratio, vdb, cp)

def cp_a_jour(cp, index_ligne_valeur_sortante, index_colonne_valeur_entrante):
    cp[index_ligne_valeur_sortante] = objectif[index_colonne_valeur_entrante]
    return cp

def z_a_jour(cp, q, z):
    for i in range(len(cp)):
        # print(cp[i], "x", q[i], "=", cp[i] * q[i] )
        z += cp[i] * q[i]
    # print("Z =", z)
    return z

def zj_a_jour(cp, ligne_pivot, index_ligne_valeur_sortante):
    return [x * cp[index_ligne_valeur_sortante] for x in ligne_pivot]

def zj_cj_a_jour(cj, zj):
    return np.subtract(cj, zj).tolist()

# Etape 7 : Calculer les valeurs des autres lignes

def calcule_autre_lignes(tab, colonne_pivot, ligne_pivot, index_ligne_valeur_sortante):
    for index_ligne in range(len(tab)):
        if index_ligne != index_ligne_valeur_sortante:
            for index_colonne in range(len(tab[index_ligne])):
                tab[index_ligne][index_colonne] = tab[index_ligne][index_colonne] - colonne_pivot[index_ligne] * ligne_pivot[index_colonne] 
            quantite[index_ligne] = quantite[index_ligne] - colonne_pivot[index_ligne] * quantite[index_ligne_valeur_sortante]  
    return tab

# tab = calcule_autre_lignes(tab, colonne_pivot, ligne_pivot, index_ligne_valeur_sortante)

# df_tab0 = built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio) 

# print_tab_simplex(df_tab0, "1ère itération")

def simplexe(contraintes, inegalites, quantite):
    # Initialisation du premier
    tab = forme_standard(contraintes, inegalites) #  Ecrire le système sous forme standard
    nom_coeff, cp, vdb, ratio, z, zj, Cj_Zj, max_Cj_Zj = initParam(tab, size_contraintes, objectif) # Initialisation des paramètres
    index_colonne_valeur_entrante, colonne_pivot = calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj) # Valeur entrante
    ratio = calcule_ratios(quantite, colonne_pivot)
    index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, ratio) # Valeur sortante
    pivot = calcule_pivot(tab, index_ligne_valeur_sortante, index_colonne_valeur_entrante) # On détermine le pivot
    print("Max Cj-Zj =", max_Cj_Zj)
    print("Valeur entrante =", nom_coeff[index_colonne_valeur_entrante])
    print("Valeur sortante =", vdb[index_ligne_valeur_sortante])
    print("Pivot =", pivot)    
    df_tab0 = built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio)  # Construction du tableau simplex
    print_tab_simplex(z,df_tab0, "Tableau initial", zj, Cj_Zj)


# Bug : La colonne pivot ne change pas ici elle reste la meme le max Zj-CJ n'est pas changé
    if max(Cj_Zj) > 0 :
        indicate = 0
        while max(Cj_Zj) > 0 and indicate < 5:
            indicate +=1
            # Mise à jour des indicateurs
            # cp = cp_a_jour(cp, index_ligne_valeur_sortante, index_colonne_valeur_entrante)    
            cp, vdb, quantite, tab, nom_coeff, ligne_pivot = mise_a_jour_ligne_pivot(tab,pivot,index_ligne_valeur_sortante,index_colonne_valeur_entrante,ligne_pivot, nom_coeff, vdb, cp)
            tab = calcule_autre_lignes(tab, colonne_pivot, ligne_pivot, index_ligne_valeur_sortante)
            # z = z_a_jour(cp, quantite, z)
            # zj = zj_a_jour(cp, ligne_pivot, index_ligne_valeur_sortante)
            cp = cp_a_jour(cp, index_ligne_valeur_sortante, index_colonne_valeur_entrante)
            # Cj_Zj = zj_cj_a_jour(objectif, zj)
            # max_Cj_Zj = max(Cj_Zj)
            # print("max_Cj_Zj",max_Cj_Zj)

            # Calcule du nouveau pivot
            # index_colonne_valeur_entrante, colonne_pivot = calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj) # Valeur entrante
            # ratio = calcule_ratios(quantite, colonne_pivot) # On calcule les ratios
            index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, ratio) # Valeur sortante
            z = z_a_jour(cp, quantite, z)
            zj = zj_a_jour(cp, ligne_pivot, index_ligne_valeur_sortante)
            Cj_Zj = zj_cj_a_jour(objectif, zj)
            max_Cj_Zj = max(Cj_Zj)
            index_colonne_valeur_entrante, colonne_pivot = calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj) # Valeur entrante
            ratio = calcule_ratios(quantite, colonne_pivot) # On calcule les ratios
            index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, ratio) # Valeur sortante


            print("Max Cj-Zj =", max_Cj_Zj)
            print("Valeur entrante =", nom_coeff[index_colonne_valeur_entrante])
            print("Valeur sortante =", vdb[index_ligne_valeur_sortante])
            print("Pivot =", pivot)  
            df_tab0 = built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio)
            if max(Cj_Zj) > 0 : 
                print_tab_simplex(z,df_tab0, "Itération " + str(indicate), zj, Cj_Zj)
            else :
                print_tab_simplex(z,df_tab0, "Tableau Final" + str(indicate), zj, Cj_Zj)



simplexe(contraintes, inegalites, quantite)
