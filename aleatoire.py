import numpy as np
import pymetal as pm

def init_gpu():
    # Device Initialization
    device = pm.create_system_default_device()
    queue = device.new_command_queue()
    # Build the code
    shader_source = open("aleatoire.metal").read()
    library = device.new_library_with_source(shader_source)
    # compile le fichier metal

    # Set up kernel pipelines
    init_function = library.new_function("initialiser_ma_2")
    init_pipeline = device.new_compute_pipeline_state(init_function)

    fun_2D = library.new_function("temps_retour_2")
    temps_retour_2 = device.new_compute_pipeline_state(fun_2D)

    fun_1D = library.new_function("temps_retour_1")
    temps_retour_1 = device.new_compute_pipeline_state(fun_1D)

    best_group_size = temps_retour_2.max_total_threads_per_threadgroup
    return device, queue, best_group_size, init_pipeline, temps_retour_1, temps_retour_2

def call_kernel(pipeline_state, queue, size, best_group_size, *buffers):
    cmd_buffer = queue.command_buffer()
    encoder = cmd_buffer.compute_command_encoder()
    encoder.set_compute_pipeline_state(pipeline_state)   

    for index, buf in enumerate(buffers):
        encoder.set_buffer(buf, 0, index)

    encoder.dispatch_threads(size, 1, 1, best_group_size, 1, 1)
    encoder.end_encoding()
    cmd_buffer.commit()
    return cmd_buffer  # Return the buffer so we can wait on the final one later

if __name__ == "__main__" :
    nb_ma = 65536
    total_iterations = 1
    # total_iterations * max_steps = nb pas total

    device, queue, best_group_size, init, temps_retour_1, temps_retour_2  = init_gpu()
    # The representation of a state on the GPU
    rw_struct_type = np.dtype([
        ('abscisse', np.int32),
        ('ordonnee', np.int32),
        ('proba', np.uint32),
        ('nb_pas', np.uint32)
    ])

    state_buffer = device.new_buffer(nb_ma * rw_struct_type.itemsize, pm.ResourceStorageModePrivate)
    cmd_buffer = call_kernel(init, queue, nb_ma, best_group_size, state_buffer)
    cmd_buffer.wait_until_completed()

    c_buffer = device.new_buffer(nb_ma * np.dtype(np.int32).itemsize, pm.ResourceStorageModeShared)
    np.frombuffer(c_buffer.contents(), dtype=np.int32, count=nb_ma).fill(0)

    print("Starting 1 Billion step simulation loop")
    for _ in range(total_iterations):    
        cmd_buffer = call_kernel(temps_retour_2, queue, nb_ma, best_group_size, c_buffer, state_buffer)

    cmd_buffer.wait_until_completed() 
    final_results = np.frombuffer(c_buffer.contents(), dtype=np.int32, count=nb_ma)
    print(f"Done: {final_results[0:20]}")

