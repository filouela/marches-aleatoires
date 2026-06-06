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

int marche_aleatoire(int origine, int nb_pas){
    int x = origine ;
    for(int i = 1 ; i < nb_pas ; i += 1){
        int p = rand() ;
        switch (p%2){
            case 0 :
                x += 1 ;
                break ;
            default :
                x -= 1 ;
                break ;
        }
        if(x == 0) return i ;
    }
    return 0 ;
}



int main() {

    // Initialisation du générateur aléatoire
    srand(time(NULL)) ;

    // Paramètres
    int origine = 0 ;
    int nb_pas = 1000000 ;
    int nb_ma = 1000 ;
    int compteur_transient = 0 ;

    for (int i = 0 ; i < nb_ma ; i+= 1){
        if(marche_aleatoire(origine, nb_pas) == 0) {
            compteur_transient += 1 ;
        }
    }
    double proportion = (double)(nb_ma-compteur_transient) / nb_ma ;

    printf("Nombre total de marches : %d.\n", nb_ma) ;
    printf("Nombre de marches transientes : %d.\n", compteur_transient) ;
    printf("Proportion de marches récurrentes : %.2f %%.\n", proportion * 100) ;

    return 0;
}
