def average_frequency(v_array, t): 
    N_spikes = count_spikes(v_array) 
    average_frequency = N_spikes / t 
    return average_frequency
    # Или не выёживаться и сделать через Фурье 

def count_spikes(v_array): 
    pass 

def I_from_frequency(ode_system, Iapp_range): 
    v_arrays = np.array(Iapp_range, t_length) # FIXME: задать массив правильно!
    for Iapp in Iapp_range: 
        v_array = ode_system.solve() # Решить систему уравнений
        v_arrays[Iapp] = v_array 
    
    frequencies = np.array() # FIXME: доделать нормально!
    for Iapp in Iapp_range: 
        frequencies[I_app] = average_frequency(v_arrrays[I_app]) # FIXME: тут синтаксис неправильный и через жопу