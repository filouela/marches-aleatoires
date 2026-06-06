""" BIBLIOTHEQUE """
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


""" PARAMETRES """
nb_pas = 50
abscisse = 0
ordonnee = 0


""" FONCTIONS """
def marche_aleatoire(nb_pas, abscisse, ordonnee):
    # choix : (1,0), (-1,0), (0,1), (0,-1)
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


""" TESTS """
def afficher_ma(abscisses, ordonnees) :
    fig, ax = plt.subplots()
    ax.plot(abscisses, ordonnees, marker='o', color='black', markersize=2)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.set_aspect('equal')
    ax.grid(True)
    fig.savefig(f"resultats_marche/etat_recurrent.png", transparent = True, dpi=300, bbox_inches='tight', pad_inches = 0)

abscisses, ordonnees = marche_aleatoire(nb_pas, abscisse, ordonnee)
afficher_ma(abscisses, ordonnees)
