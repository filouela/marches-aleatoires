""" BIBLIOTHEQUE """
import numpy as np
import random
import matplotlib.pyplot as plt


""" PARAMETRES """
nb_pas = int(1e5)
nb_marches_aleatoires = 100
nb_experiences = 1000
origine = 50
limite_superieure = 50
M = origine + limite_superieure


""" FONCTIONS """
def marche_aleatoire(origine, nb_pas, borne) :
    rang = origine
    i = 1
    while(i < nb_pas) :
        p = random.random()
        if p < 0.5 : rang -= 1
        else : rang += 1
        if rang >= borne or rang <= 0 :
            return i
        i += 1
    return 0

def premiere_moyenne(origine, nb_marches_aleatoires, nb_pas, M) :
    liste_temps = []
    for _ in range(nb_marches_aleatoires) :
        rang = marche_aleatoire(origine, nb_pas, M)
        if rang != 0 :
            liste_temps.append(rang)
    moyenne = np.mean(liste_temps)
    return moyenne

def calcul_moyennes(origine, nb_marches_aleatoires, nb_pas, M, nb_experiences) :
    moyennes = []
    for _ in range(nb_experiences):
        moyenne = premiere_moyenne(origine, nb_marches_aleatoires, nb_pas, M)
        moyennes.append(moyenne)
    return moyennes


""" TESTS """
def afficher_resultat() :
    moyennes = calcul_moyennes(origine, nb_marches_aleatoires, nb_pas, M, nb_experiences)
    moyennes = np.array(moyennes)
    plt.figure(figsize=(7, 10))
    plt.hist(moyennes, bins=15, alpha=0.7, color='darkorange', edgecolor='black')
    plt.axvline(2500, color='chocolate', linestyle='-', linewidth=2)
    plt.xlabel("Moyenne de 100 temps de dépassement")
    plt.ylabel("Nombre d'occurences")
    plt.grid(alpha=0.3)
    plt.savefig(f"resultats_marche/temps_atteinte.png", transparent = True, dpi=300, bbox_inches='tight')

afficher_resultat()
