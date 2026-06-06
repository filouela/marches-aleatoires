#include <metal_stdlib>
using namespace metal ;

constant uint max_steps = 1'000'000 ;
constant uint borne = 100 ;

uint random(uint seed) {
    uint state = seed * 747796405u + 2891336453u ;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u ;
    return (word >> 22u) ^ word ;
}

struct RW{
    int abscisse ;
    int ordonnee ;
    uint proba ;
    uint64_t nb_pas ;
} ;

kernel void initialiser_ma_2(
    device RW * marches_aleatoires  [[buffer(0)]], 
    uint id                    [[thread_position_in_grid]])
{
    marches_aleatoires[id].abscisse = 0 ;
    marches_aleatoires[id].ordonnee = 0 ;
    marches_aleatoires[id].proba = id ;
    marches_aleatoires[id].nb_pas = 0 ;
}

kernel void initialiser_ma_borne(
    device RW * marches_aleatoires  [[buffer(0)]], 
    uint id                    [[thread_position_in_grid]])
{
    marches_aleatoires[id].abscisse = 50 ;
    marches_aleatoires[id].ordonnee = 0 ;
    marches_aleatoires[id].proba = id ;
    marches_aleatoires[id].nb_pas = 0 ;
}

kernel void temps_retour_1(
    device int* temps [[buffer(0)]],
    device RW* marches_aleatoires      [[buffer(1)]], 
    uint id [[thread_position_in_grid]])
{
    if (temps[id] != 0) return ;

    int x = marches_aleatoires[id].abscisse ;
    uint p = marches_aleatoires[id].proba ;
    
    for(uint i = 0 ; i < max_steps ; i += 1){
        p = random(p) ;
        uint direction = p & 1u ;
        if (direction == 0)      { x += 1 ; }
        else { x -= 1 ; }
        
        if (x == 0){
            temps[id] = marches_aleatoires[id].nb_pas + i + 1 ;
            break ;
        }
    }
    marches_aleatoires[id].abscisse = x ;
    marches_aleatoires[id].proba = p ;
    marches_aleatoires[id].nb_pas += max_steps ;
}

kernel void temps_retour_2(
    device int* temps              [[buffer(0)]], 
    device RW* marches_aleatoires      [[buffer(1)]], 
    uint id                   [[thread_position_in_grid]])
{
    if (temps[id] != 0) return ;

    int x = marches_aleatoires[id].abscisse ;
    int y = marches_aleatoires[id].ordonnee ;
    uint p = marches_aleatoires[id].proba ;
    
    for(uint i = 0 ; i < max_steps ; i += 1){
        p = random(p) ;
        uint direction = p & 3u ;
        if (direction == 0)      { x += 1 ; }
        else if (direction == 1) { x -= 1 ; }
        else if (direction == 2) { y += 1 ; }
        else                     { y -= 1 ; }
        
        if (x == 0 && y == 0){
            temps[id] = marches_aleatoires[id].nb_pas + i + 1 ;
            break ;
        }
    }
    marches_aleatoires[id].abscisse = x ;
    marches_aleatoires[id].ordonnee = y ;
    marches_aleatoires[id].proba = p ;
    marches_aleatoires[id].nb_pas += max_steps ;
}

kernel void temps_borne(
    device uint64_t* temps [[buffer(0)]],
    device RW* marches_aleatoires      [[buffer(1)]], 
    uint id [[thread_position_in_grid]])
{
    if (temps[id] != 0) return ;

    int x = marches_aleatoires[id].abscisse ;
    uint p = marches_aleatoires[id].proba ;
    
    for(uint i = 0 ; i < max_steps ; i += 1){
        p = random(p) ;
        uint direction = p & 1u ;
        if (direction == 0)      { x += 1 ; }
        else { x -= 1 ; }
        
        if (x == borne || x == 0){
            temps[id] = marches_aleatoires[id].nb_pas + i + 1 ;
            break ;
        }
    }
    marches_aleatoires[id].abscisse = x ;
    marches_aleatoires[id].proba = p ;
    marches_aleatoires[id].nb_pas += max_steps ;
}
