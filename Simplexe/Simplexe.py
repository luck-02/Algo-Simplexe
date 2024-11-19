import numpy as np
import pandas as pd

# # Coeff fonction objectif :
# objectif = [7,6]
# # Coeff contraintes :
# contraintes = [[2, 4],
#  [3, 2],]
# # Quantité :
# quantite = [16, 12]

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

def built_tab_simplex(cp, vdb, quantite, tab, nom_coeff, ratio):
    df_param = pd.DataFrame({"Cp": cp,"VDB": vdb,"Q": quantite}) #Tables de gauche
    df_coeff = pd.DataFrame(tab, columns=nom_coeff) #Matrice de coefficients
    df_ratio = pd.DataFrame({"ratio": ratio}) #Table de ratios
    return pd.concat([df_param, df_coeff, df_ratio], axis=1)

def print_tab_simplex(z,df_tab, msg, zj, Cj_Zj):
    # # Affichage du DataFrame
    print("Tableau simplexe :", msg)
    print("               Cj", objectif)
    print(df_tab)
    print("       Z =", z, "| Zj", zj)
    print("          Cj - Zj", Cj_Zj)
    print(" ")

def calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj):
    index_colonne_valeur_entrante = Cj_Zj.index(max_Cj_Zj)
    colonne_pivot = [ligne[index_colonne_valeur_entrante] for ligne in tab]
    return index_colonne_valeur_entrante, colonne_pivot

# Etape 4 : Choisir la variable à enlever de la base

def calcule_ratios(quantite, colonne_pivot):
    np.seterr(divide='ignore', invalid='ignore') #Pour ignorer warning quand division par zéro
    ratio = np.divide(quantite, colonne_pivot).tolist()
    return ratio

def calcule_v_sortante(tab, ratios):
    ratios_positifs = [x for x in ratios if x > 0]
    if ratios_positifs :
        min_ratio = min(ratios_positifs)

    index_ligne_valeur_sortante = ratios.index(min_ratio)
    ligne_pivot = tab[index_ligne_valeur_sortante]
    return index_ligne_valeur_sortante, ligne_pivot

def calcule_pivot(tab, index_ligne_valeur_sortante, index_colonne_valeur_entrante ):
    return tab[index_ligne_valeur_sortante][index_colonne_valeur_entrante]

def ratio_pivot_a_jour(ratio, index_ligne_valeur_sortante, pivot):
    ratio[index_ligne_valeur_sortante] = ratio[index_ligne_valeur_sortante]/pivot

# Etape 6 : Diviser la ligne du pivot par le pivot

def mise_a_jour_ligne_pivot(tab,pivot,index_ligne_valeur_sortante,index_colonne_valeur_entrante,ligne_pivot, nom_coeff, vdb, cp):
    ligne_pivot = [x / pivot for x in ligne_pivot]
    tab[index_ligne_valeur_sortante] = ligne_pivot
    quantite[index_ligne_valeur_sortante] = quantite[index_ligne_valeur_sortante]/pivot
    vdb[index_ligne_valeur_sortante] = nom_coeff[index_colonne_valeur_entrante]
    return cp, vdb, quantite, tab, nom_coeff, ligne_pivot

def cp_a_jour(cp, index_ligne_valeur_sortante, index_colonne_valeur_entrante):
    cp[index_ligne_valeur_sortante] = objectif[index_colonne_valeur_entrante]
    return cp

def z_a_jour(cp, q, z):
    z = 0
    for i in range(len(cp)):
        z += cp[i] * q[i]
    return z

def zj_a_jour(cp,tab,Zj, index_ligne_valeur_sortante):
    for i in range(len(tab[index_ligne_valeur_sortante])):
        Zj[i] = 0
        for j in range(len(cp)):
            Zj[i] += cp[j] * tab[j][i]
    return Zj

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
        while max(Cj_Zj) > 0:
            indicate +=1
            # Mise à jour des indicateurs
            cp, vdb, quantite, tab, nom_coeff, ligne_pivot = mise_a_jour_ligne_pivot(tab,pivot,index_ligne_valeur_sortante,index_colonne_valeur_entrante,ligne_pivot, nom_coeff, vdb, cp)
            tab = calcule_autre_lignes(tab, colonne_pivot, ligne_pivot, index_ligne_valeur_sortante)
            cp = cp_a_jour(cp, index_ligne_valeur_sortante, index_colonne_valeur_entrante)
            z = z_a_jour(cp, quantite, z)
           
            # Calcule du nouveau pivot
            index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, ratio) # Valeur sortante
            zj = zj_a_jour(cp,tab,zj, index_ligne_valeur_sortante)
            Cj_Zj = zj_cj_a_jour(objectif, zj)
            max_Cj_Zj = max(Cj_Zj)
            index_colonne_valeur_entrante, colonne_pivot = calcule_v_entrante(tab, max_Cj_Zj, Cj_Zj) # Valeur entrante
            ratio = calcule_ratios(quantite, colonne_pivot) # On calcule les ratios
            index_ligne_valeur_sortante, ligne_pivot = calcule_v_sortante(tab, ratio) # Valeur sortante
            pivot = calcule_pivot(tab, index_ligne_valeur_sortante, index_colonne_valeur_entrante) # On détermine le pivot

            if max_Cj_Zj > 0 :
                print("Max Cj-Zj =", max_Cj_Zj)
                print("Valeur entrante =", nom_coeff[index_colonne_valeur_entrante])
                print("Valeur sortante =", vdb[index_ligne_valeur_sortante])
                print("Pivot =", pivot)  
            df_tab0 = built_tab_simplex(cp,vdb, quantite, tab, nom_coeff, ratio)  # Construction du tableau simplex
            if max(Cj_Zj) > 0 : 
                print_tab_simplex(z,df_tab0, "Itération " + str(indicate), zj, Cj_Zj)
            else :
                print_tab_simplex(z,df_tab0, "Tableau Final", zj, Cj_Zj)

simplexe(contraintes, inegalites, quantite)
