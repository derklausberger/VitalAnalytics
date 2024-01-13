import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate():
    duration = 10 # time in seconds
    sampling_rate = 600 # ekg in hertz

    p_dur = 100 # p wave duration in milliseconds: 60-100
    pq_dur = 100
    qrs_dur = 100 #
    st_dur = 100
    t_dur = 200 # 

    # time stamps for specific complexes
    t_p = np.linspace(0, 0.15, p_dur, endpoint=False)
    t_pq = np.linspace(0.15, 0.3, pq_dur, endpoint=False)
    t_qrs = np.linspace(0.3, 0.6, qrs_dur, endpoint=False)
    t_st = np.linspace(0.6, 0.75, st_dur, endpoint=False)
    t_t = np.linspace(0.75, 1, t_dur, endpoint=False)
    
    p_wave = 0.3 * np.sin(4 * np.pi * t_p) #0.1-0.3 mV

    pq_dist = 0 * t_pq

    # S(0.) < Q(-0.1--0.3mV) < R(1-3mV)
    qrs_complex = np.concatenate((
        (t_qrs[0:25] - t_qrs[0]) * -5, # because last value = 0.06*5 = 0.3 = max value
        (t_qrs[25:50] - t_qrs[25]) * 55 - (t_qrs[24] - t_qrs[0]) * 5, # 
        (t_qrs[50:75] - t_qrs[50]) * -57 + (t_qrs[49] - t_qrs[25]) * 50,
        (t_qrs[75:100] - t_qrs[75]) * 7 - (t_qrs[74] - t_qrs[50]) * 7
    ))

    st_dist = 0 * t_st
    
    t_wave = - 0.6 * np.sin(4 * np.pi * t_t)
    
    ekg_data = np.concatenate((p_wave, pq_dist, qrs_complex, st_dist, t_wave))


    """np.column_stack((t, ekg_data))"""
    t = np.concatenate((t_p, t_pq, t_qrs, t_st, t_t))
    np.savetxt('ekg.csv', np.column_stack((t, ekg_data)), delimiter=',', header='Time,EKG Amplitude', comments='')

def plot():
    ekg_df = pd.read_csv('ekg.csv')

    plt.plot(ekg_df['Time'], ekg_df['EKG Amplitude'])
    plt.xlabel('time(s)')
    plt.ylabel('amplitude')
    plt.title('data')
    plt.grid(True)
    plt.xlim(0, 10) 
    plt.ylim(-2, 5) 
    plt.show()

    ekg_df.to_csv('ekg.csv', index=False)

generate()
plot()