#include <stdio.h>
#include <stdlib.h>
#include <time.h>



/* FONCTIONS */
double calcul_moyenne(int* liste, int n){
    int somme = 0 ;
    for(int i = 0 ; i < n ; i += 1){
        somme += liste[i] ;
    }
    return somme/n ;
}

int marche_aleatoire(int abscisse, int ordonnee, int nb_pas){
    int x = abscisse ;
    int y = ordonnee ;
    for(int i = 1 ; i < nb_pas ; i += 1){
        int p = rand() ;
        switch (p%4){
            case 0 :
                x += 1 ;
                break ;
            case 1 :
                x -= 1 ;
                break ;
            case 2 :
                y += 1 ;
                break ;
            default :
                y -= 1 ;
                break ;
        }
        if(x == 0 && y == 0) return i ;
    }
    return 0 ;
}



int main() {

    // Initialisation du générateur aléatoire
    srand(time(NULL)) ;

    // Paramètres
    int abscisse = 0 ;
    int ordonnee = 0 ;
    int nb_pas = 1000000 ;
    int nb_ma = 1000 ;
    int compteur_transient = 0 ;

    for (int i = 0 ; i < nb_ma ; i+= 1){
        if(marche_aleatoire(abscisse, ordonnee, nb_pas) == 0) {
            compteur_transient += 1 ;
        }
    }
    double proportion = (double)(nb_ma-compteur_transient) / nb_ma ;

    printf("Nombre total de marches : %d.\n", nb_ma) ;
    printf("Nombre de marches transientes : %d.\n", compteur_transient) ;
    printf("Proportion de marches récurrentes : %.2f %%.\n", proportion * 100) ;

    return 0;
}
