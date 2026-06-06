""" BIBLIOTHEQUE """
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator



""" FONCTIONS """
def generer_ma_1(Y, nb_pas) :
    for n in range(1, nb_pas) :
        p = random.random()
        if p >= 0.5 :
            Y[n] = Y[n-1] + 1
        else :
            Y[n] = Y[n-1] - 1
    return Y

def generer_ma_2(nb_pas, origine):
    # choix : (1,0), (-1,0), (0,1), (0,-1)
    abscisse, ordonnee = origine
    abscisses = [abscisse for _ in range(nb_pas)]
    ordonnees = [ordonnee for _ in range(nb_pas)]
    for n in range(1, nb_pas):
        p = random.random()
        if p < 0.25 :
            abscisses[n] = abscisses[n-1] +1
            ordonnees[n] = ordonnees[n-1]
        elif 0.25 <= p < 0.5 :
            abscisses[n] = abscisses[n-1] -1
            ordonnees[n] = ordonnees[n-1]
        elif 0.5 <= p < 0.75 :
            abscisses[n] = abscisses[n-1]
            ordonnees[n] = ordonnees[n-1] +1
        else :
            abscisses[n] = abscisses[n-1]
            ordonnees[n] = ordonnees[n-1] -1
    return abscisses, ordonnees

def temps_borne(origine, nb_pas, M) :
    rang = origine
    i = 1
    while(i < nb_pas) :
        p = random.random()
        if p < 0.5 : rang -= 1
        else : rang += 1
        if rang >= M or rang <= 0 :
            return i
        i += 1
    return 0

def temps_retour_1(origine, nb_pas) :
    x = origine
    i = 1
    while(i < nb_pas) :
        p = random.randint(0, 1)
        match p :
            case 0 : x += 1
            case _ : x -= 1
        if x == 0 :
            return i
        i += 1
    return 0

def temps_retour_2(origine, nb_pas) :
    (x, y) = origine
    i = 1
    while(i < nb_pas) :
        p = random.randint(0, 3)
        match p :
            case 0 : x += 1
            case 1 : x -= 1
            case 2 : y += 1
            case _ : y -= 1
        if x == 0 and y == 0 :
            return i
        i += 1
    return 0


def generer_marches_aleatoires(origine, nb_pas, nb_ma) :
    l = [[] for _ in range(nb_ma)]
    for i in range(1, nb_ma) :
        Y = [origine for _ in range(nb_pas)]
        Y = generer_ma_1(Y, nb_pas)
        l[i] = Y
    return(l)


def moyenne_temps(origine, nb_ma, nb_pas, M) :
    liste_temps = []
    for _ in range(nb_ma) :
        rang = temps_borne(origine, nb_pas, M)
        if rang != 0 :
            liste_temps.append(rang)
    moyenne = np.mean(liste_temps)
    return moyenne

def calcul_moyennes(origine, nb_ma, nb_pas, M, nb_experiences) :
    moyennes = []
    for _ in range(nb_experiences):
        moyenne = moyenne_temps(origine, nb_ma, nb_pas, M)
        moyennes.append(moyenne)
    return moyennes


def calcul_moyenne_temps_borne(borne_basse, borne_haute, compteur_borne, moyenne, origine, nb_pas, M) :
    for _ in range(borne_basse, borne_haute) :
        rang = temps_borne(origine, nb_pas, M)
        if rang != 0 :
            moyenne += rang
            compteur_borne += 1
    return compteur_borne, moyenne

def calcul_convergence_moyenne(n, origine, nb_pas, M) :
    temps = []
    compteurs = []
    borne_basse = 1
    borne_haute = 2
    moyenne_i = 0
    compteur_i = 0
    for _ in range(0, n) :
        compteur_i, moyenne_i = calcul_moyenne_temps_borne(borne_basse, borne_haute, compteur_i, moyenne_i, origine, nb_pas, M)
        if compteur_i != 0 :
            compteurs.append(compteur_i)
            temps.append(moyenne_i / compteur_i)
        borne_basse = borne_haute
        borne_haute *= 2
    return compteurs, temps



""" AFFICHAGES """
def plusieurs_ma(liste_ma) :
    plt.figure(figsize=(20, 8))
    for e in liste_ma :
        plt.plot(e)
    plt.grid(True)
    plt.savefig(f"resultats_marche/marche_aleatoire.png", transparent = True, dpi=300, bbox_inches='tight')

def ma_dim2(abscisses, ordonnees) :
    fig, ax = plt.subplots()
    ax.plot(abscisses, ordonnees, marker='o', color='black', markersize=2)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.set_aspect('equal')
    ax.grid(True)
    fig.savefig(f"resultats_marche/etat_recurrent.png", transparent = True, dpi=300, bbox_inches='tight', pad_inches = 0)

def convergence_temps_borne(x, y) :
    plt.plot(x, y, color='orange')
    plt.xlabel("Nombre de marches aleatoires bornees")
    plt.ylabel("Temps moyen de depassement de borne")
    plt.xscale("log", base=2)
    plt.axhline(y=2500, color='chocolate')
    plt.savefig(f"resultats_marche/convergence_temps.png", transparent = True, dpi=300, bbox_inches='tight', pad_inches = 0)

def repartition_moyennes(moyennes) :
    moyennes = np.array(moyennes)
    plt.figure(figsize=(6, 10))
    plt.hist(moyennes, bins=15, alpha=0.7, color='darkorange', edgecolor='black')
    plt.axvline(2500, color='chocolate', linestyle='-', linewidth=2)
    plt.xlabel("Moyenne de 100 temps de depassement")
    plt.ylabel("Nombre d'occurences")
    plt.grid(alpha=0.3)
    plt.savefig(f"resultats_marche/temps_atteinte.png", transparent = True, dpi=300, bbox_inches='tight')

def queue_temps_retour_1(liste_temps) :
    liste_temps = np.array(liste_temps)
    plt.figure(figsize=(20, 8))
    bins = np.logspace(np.log10(liste_temps.min()), np.log10(liste_temps.max()), 50)
    plt.hist(liste_temps, bins=bins, color="orange", edgecolor='black', alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Temps de retour")
    plt.ylabel("Nombre d'occurences")
    plt.grid(True, which='both', alpha=0.2)
    plt.savefig(f"resultats_marche/temps_retour_dim1.png", transparent = True, dpi=300, bbox_inches='tight')

def queue_temps_retour_2(liste_temps) :
    liste_temps = np.array(liste_temps)
    plt.figure(figsize=(20, 8))
    bins = np.logspace(np.log10(liste_temps.min()), np.log10(liste_temps.max()), 50)
    plt.hist(liste_temps, bins=bins, color="orange", edgecolor='black', alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Temps de retour")
    plt.ylabel("Nombre d'occurences")
    plt.grid(True, which='both', alpha=0.2)
    plt.savefig(f"resultats_marche/temps_retour_dim2.png", transparent = True, dpi=300, bbox_inches='tight')



""" TESTS """
def main_print_plusieurs_1() :
    origine = 0
    nb_pas = 100
    nb_ma = 5
    liste_ma = generer_marches_aleatoires(origine, nb_pas, nb_ma)
    plusieurs_ma(liste_ma)

def main_print_ma_2() :
    origine = (0,0)
    nb_pas = 50
    abscisses, ordonnees = generer_ma_2(nb_pas, origine)
    ma_dim2(abscisses, ordonnees)

def main_convergence_temps() :
    n = 25
    origine = 50
    nb_pas = int(1e6)
    limite = 50
    M = limite + origine
    compteurs, temps = calcul_convergence_moyenne(n, origine, nb_pas, M)
    convergence_temps_borne(compteurs, temps)

def main_repartition_moyennes() :
    origine = 50
    limite_superieure = 50
    nb_pas = int(1e5)
    nb_ma = 100
    M = origine + limite_superieure
    nb_experiences = 1000
    moyennes = calcul_moyennes(origine, nb_ma, nb_pas, M, nb_experiences)
    repartition_moyennes(moyennes)

def main_temps_retour_1() :
    origine = 0
    nb_pas = int(1e6)
    nb_ma = int(1e3)
    compteur_transient = 0
    liste_temps = []
    for _ in range(nb_ma) :
        rang = temps_retour_1(origine, nb_pas)
        if rang == 0:
            compteur_transient += 1
        else:
            liste_temps.append(rang)
    queue_temps_retour_1(liste_temps)

def main_temps_retour_2() :
    origine = (0,0)
    nb_pas = int(1e9)
    nb_ma = int(1e3)
    compteur_transient = 0
    liste_temps = []
    for _ in range(nb_ma) :
        rang = temps_retour_2(origine, nb_pas)
        if rang == 0:
            compteur_transient += 1
        else:
            liste_temps.append(rang)
    queue_temps_retour_2(liste_temps)
