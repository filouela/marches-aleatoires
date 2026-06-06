#include <stdio.h>
#include <stdlib.h>
#include <time.h>


/* FONCTIONS */
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
    srand(time(NULL)) ;

    // PARAMETRES
    int origine = 0 ;
    int nb_pas = 1000000 ;
    int nb_ma = 1000 ;
    int compteur_recurrent = 0 ;

    for (int i = 0 ; i < nb_ma ; i+= 1){
        if(marche_aleatoire(origine, nb_pas) != 0) {
            compteur_recurrent += 1 ;
        }
    }
    double proportion = (double) (compteur_recurrent / nb_ma) ;

    printf("Nombre total de marches : %d.\n", nb_ma) ;
    printf("Proportion de marches récurrentes : %.2f %%.\n", proportion * 100) ;

    return 0;
}
