import numpy as np
import matplotlib.pyplot as plt
import pymetal as pm

def init_gpu() :
    # device : carte graphique
    device = pm.create_system_default_device()

    # queue : permet de donner le programme
    queue = device.new_command_queue()

    # compile le fichier metal (pour la carte graphique)
    source = open("aleatoire.metal").read()
    bibliotheque = device.new_library_with_source(source)

    # prend une fonction et la transforme pour pouvoir la mettre dans la queue
    fonction_init = bibliotheque.new_function("initialiser_ma_2")
    init_pipeline = device.new_compute_pipeline_state(fonction_init)

    fonction_init2 = bibliotheque.new_function("initialiser_ma_borne")
    init_pipeline2 = device.new_compute_pipeline_state(fonction_init2)

    fonction_1D = bibliotheque.new_function("temps_retour_1")
    temps_retour_1 = device.new_compute_pipeline_state(fonction_1D)

    fonction_2D = bibliotheque.new_function("temps_retour_2")
    temps_retour_2 = device.new_compute_pipeline_state(fonction_2D)

    fonction_borne = bibliotheque.new_function("temps_borne")
    temps_borne = device.new_compute_pipeline_state(fonction_borne)

    return device, queue, init_pipeline, init_pipeline2, temps_retour_1, temps_retour_2, temps_borne


def call_kernel(pipeline_fonction, queue, nb_ma, best_group_size, *arguments) :
    # message : ce qu'on met dans la queue
    # encodeur : traduit la fonction en message
    message = queue.command_buffer()
    encodeur = message.compute_command_encoder()
    encodeur.set_compute_pipeline_state(pipeline_fonction)   

    for indice, arg in enumerate(arguments):
        encodeur.set_buffer(arg, 0, indice)

    encodeur.dispatch_threads(nb_ma, 1, 1, best_group_size, 1, 1)
    encodeur.end_encoding()
    message.commit()
    return message  # Return the buffer so we can wait on the final one later


def main_temps_1D() :
    nb_ma = 1024

    # permet de commander la carte graphique
    device, queue, init_pipeline, _, temps_retour_1, _, _  = init_gpu()

    # calcule le nb max de fils utilisable en un appel
    best_group_size = temps_retour_1.max_total_threads_per_threadgroup

    struct_ma = np.dtype([
        ('abscisse', np.int32),
        ('ordonnee', np.int32),
        ('proba', np.uint32),
        ('nb_pas', np.uint32)
    ])

    # on initialise les marches aleatoires et on attend que ce soit finit
    tableau_ma = device.new_buffer(nb_ma * struct_ma.itemsize, pm.ResourceStorageModePrivate)
    message = call_kernel(init_pipeline, queue, nb_ma, best_group_size, tableau_ma)
    message.wait_until_completed()

    # on initialise le tableau des temps
    tableau_temps = device.new_buffer(nb_ma * np.dtype(np.int32).itemsize, pm.ResourceStorageModeShared)
    np.frombuffer(tableau_temps.contents(), dtype=np.int32, count=nb_ma).fill(0)

    # on fait faire a la carte temps_retour_1
    message = call_kernel(temps_retour_1, queue, nb_ma, best_group_size, tableau_temps, tableau_ma)
    message.wait_until_completed()

    resultats = np.frombuffer(tableau_temps.contents(), dtype=np.int32, count=nb_ma)
    return resultats


def main_temps_2D() :
    nb_ma = 1024
    nb_iterations = 1000
    # nb_iterations * max_steps = nb pas total

    device, queue, init_pipeline, _, _, temps_retour_2, _  = init_gpu()
    best_group_size = temps_retour_2.max_total_threads_per_threadgroup

    struct_ma = np.dtype([
        ('abscisse', np.int32),
        ('ordonnee', np.int32),
        ('proba', np.uint32),
        ('nb_pas', np.uint32)
    ])

    tableau_ma = device.new_buffer(nb_ma * struct_ma.itemsize, pm.ResourceStorageModePrivate)
    message = call_kernel(init_pipeline, queue, nb_ma, best_group_size, tableau_ma)
    message.wait_until_completed()

    tableau_temps = device.new_buffer(nb_ma * np.dtype(np.int32).itemsize, pm.ResourceStorageModeShared)
    np.frombuffer(tableau_temps.contents(), dtype=np.int32, count=nb_ma).fill(0)

    for _ in range(nb_iterations) :
        message = call_kernel(temps_retour_2, queue, nb_ma, best_group_size, tableau_temps, tableau_ma)

    message.wait_until_completed()
    resultats = np.frombuffer(tableau_temps.contents(), dtype=np.int32, count=nb_ma)
    return resultats



def main_convergence_temps() :
    nb_iterations = 25
    nb_ma = 2**nb_iterations
    moyennes = []
    compteurs = []

    device, queue, _, init_pipeline2, _, _, temps_borne  = init_gpu()
    best_group_size = temps_borne.max_total_threads_per_threadgroup

    struct_ma = np.dtype([
        ('abscisse', np.int32),
        ('ordonnee', np.int32),
        ('proba', np.uint32),
        ('nb_pas', np.uint64)
    ])

    tableau_ma = device.new_buffer(nb_ma * struct_ma.itemsize, pm.ResourceStorageModePrivate)
    message = call_kernel(init_pipeline2, queue, nb_ma, best_group_size, tableau_ma)
    message.wait_until_completed()

    tableau_temps = device.new_buffer(nb_ma * np.dtype(np.uint64).itemsize, pm.ResourceStorageModeShared)
    np.frombuffer(tableau_temps.contents(), dtype=np.uint64, count=nb_ma).fill(0)

    message = call_kernel(temps_borne, queue, nb_ma, best_group_size, tableau_temps, tableau_ma)
    message.wait_until_completed()
    
    resultats = np.frombuffer(tableau_temps.contents(), dtype=np.uint64, count=nb_ma)

    for i in range(0, nb_iterations) :
        taille_i = 2**i
        resultats_i = resultats[0:taille_i]
        moyenne_i = np.mean(resultats_i, where=(resultats_i != 0))
        compteurs.append(taille_i)
        moyennes.append(moyenne_i)

    return compteurs, moyennes


if __name__ == "__main__" :
    compteurs, moyennes = main_convergence_temps()
    plt.plot(compteurs, moyennes, color='orange')
    plt.xlabel("Nombre de marches aleatoires bornees")
    plt.ylabel("Temps moyen de depassement de borne")
    plt.xscale("log", base=2)
    plt.axhline(y=2500, color='chocolate')
    plt.savefig(f"/Users/jeanne/tipe/programmes/resultats_marche/convergence_temps.png", transparent = True, dpi=300, bbox_inches='tight', pad_inches = 0)
