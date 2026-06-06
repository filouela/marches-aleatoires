#include <metal_stdlib>
using namespace metal ;

constant uint max_steps = 1000'000 ;
// nb max de pas faits en un calcul

uint random(uint seed) {
    // on fait un peu n'importe quoi pour donner un nombre aleatoire
    // les operations et nombres sont random
    // u pour unsigned
    // >> pour decaler a droite (ca fait des nombres tres petits)
    // ^ pour faire xor

    uint state = seed * 747796405u + 2891336453u ;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u ;
    return (word >> 22u) ^ word ;
}

struct RW{
    int abscisse ;
    int ordonnee ;
    uint proba ;
    uint nb_pas ;
} ;

kernel void temps_retour_1(
    device int* temps [[buffer(0)]],
    uint id [[thread_position_in_grid]])
{
    // faut mettre kernel devant une fonction utilisee par le processeur
    // faut mettre device devant les taleaux
    // temps : tableau des temps de retour des ma
    // id : id du thread

    temps[id] = 0 ;
    uint p = id ;
    int position = 0 ;
    for(int i = 0 ; i < 1'000'000; i += 1){
        p = random(p) ;
        position += (p & 1u) ? 1 : -1 ;
        // p & 1u : et bit a bit avec 1 (donc on regarde le dernier bit de p -> 2 choix)
        if (position == 0){
            temps[id] = i ;
            break ;
        }
    }
}

kernel void initialiser_ma_2(
    device RW * marches_aleatoires  [[buffer(0)]], 
    uint id                    [[thread_position_in_grid]])
{
    marches_aleatoires[id].abscisse = 0 ;
    marches_aleatoires[id].ordonnee = 0 ;
    marches_aleatoires[id].proba = id ;
    marches_aleatoires[id].nb_pas = 0 ;
}

kernel void temps_retour_2(
    device int* temps              [[buffer(0)]], 
    device RW* marches_aleatoires      [[buffer(1)]], 
    uint id                   [[thread_position_in_grid]])
{
    if (temps[id] != 0) return ;
    //deja calcule

    int x = marches_aleatoires[id].abscisse ;
    int y = marches_aleatoires[id].ordonnee ;
    uint p = marches_aleatoires[id].proba ;
    
    for(uint i = 0 ; i < max_steps; i += 1){
        p = random(p);
        uint direction = p & 3u ;
        // on regarde les deux derniers bits de p -> 4 choix
        if (direction == 0)      { x += 1 ; }
        else if (direction == 1) { x -= 1 ; }
        else if (direction == 2) { y += 1 ; }
        else                     { y -= 1 ; }
        
        if (x == 0 && y == 0){
            temps[id] = marches_aleatoires[id].nb_pas + i + 1;
            break;
        }
    }
    marches_aleatoires[id].abscisse = x ;
    marches_aleatoires[id].ordonnee = y ;
    marches_aleatoires[id].proba = p ;
    marches_aleatoires[id].nb_pas += max_steps ;
}
