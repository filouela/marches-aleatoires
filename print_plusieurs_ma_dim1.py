""" BIBLIOTHEQUE """
import matplotlib.pyplot as plt
import random


""" PARAMETRES """
origine = 0
nb_pas = 100
nb_marches = 5


""" FONCTIONS """
def creer_marche(Y, nb_pas) :
    for n in range(1, nb_pas) :
        p = random.random()
        if p >= 0.5 :
            Y[n] = Y[n-1] + 1
        else :
            Y[n] = Y[n-1] - 1
    return Y

def marches_aleatoires(origine, nb_pas, nb_marches) :
    l = [[] for _ in range(nb_marches)]
    for i in range(1, nb_marches) :
        Y = [origine for _ in range(nb_pas)]
        Y = creer_marche(Y, nb_pas)
        l[i] = Y
    return(l)


""" TESTS """
def afficher_resultats(liste_ma) :
    plt.figure(figsize=(20, 8))
    for e in liste_ma :
        plt.plot(e)
    plt.grid(True)
    plt.savefig(f"resultats_marche/marche_aleatoire.png", transparent = True, dpi=300, bbox_inches='tight')

liste_ma = marches_aleatoires(origine, nb_pas, nb_marches)
afficher_resultats(liste_ma)
