#include <stdio.h>
#include <stdlib.h>
#include <time.h>


/* FONCTIONS */
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
    srand(time(NULL)) ;

    // Paramètres
    int abscisse = 0 ;
    int ordonnee = 0 ;
    int nb_pas = 1000000 ;
    int nb_ma = 1000 ;
    int compteur_recurrent = 0 ;

    for (int i = 0 ; i < nb_ma ; i+= 1){
        if(marche_aleatoire(abscisse, ordonnee, nb_pas) == 0) {
            compteur_recurrent += 1 ;
        }
    }
    double proportion = (double) (compteur_recurrent / nb_ma) ;

    printf("Nombre total de marches : %d.\n", nb_ma) ;
    printf("Proportion de marches récurrentes : %.2f %%.\n", proportion * 100) ;

    return 0 ;
}
