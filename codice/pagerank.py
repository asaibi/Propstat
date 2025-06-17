import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import norm

# Matrice di transizione corretta
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

n_pagine = 6
max_passi_per_utente = 100
p_terminazione = 0.01

def simulazione_passi(n_passi):
    visite = np.zeros(n_pagine, dtype=int)
    pagina_attuale = np.random.randint(n_pagine)
    for _ in range(n_passi):
        visite[pagina_attuale] += 1
        pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
    return visite

def simulazione_terminazione(n_utenti):
    visite_totali = np.zeros(n_pagine, dtype=int)
    for _ in range(n_utenti):
        pagina_attuale = np.random.randint(n_pagine)
        passi = 0
        while passi < max_passi_per_utente:
            visite_totali[pagina_attuale] += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
            passi += 1
    return visite_totali

def stima_frequenza_pagina_2(k_utenti):
    frequenze_p2 = []
    for _ in range(k_utenti):
        pagina_attuale = np.random.randint(n_pagine)
        visite_p2 = 0
        visite_totali = 0
        passi = 0
        while passi < max_passi_per_utente:
            if pagina_attuale == 1:
                visite_p2 += 1
            visite_totali += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
            passi += 1
        frequenze_p2.append(visite_p2 / visite_totali if visite_totali > 0 else 0)
    return np.array(frequenze_p2)

if __name__ == "__main__":
    # Simulazione senza terminazione
    frequenze = simulazione_passi(10000) / 10000
    print("Frequenze senza terminazione:", frequenze)

    # Simulazione con terminazione
    freq_terminazione = simulazione_terminazione(10000)
    print("Frequenze con terminazione:", freq_terminazione / np.sum(freq_terminazione))

    # Intervallo di confidenza per pagina 2
    for K in [50, 100, 200, 2000]:
        campione = stima_frequenza_pagina_2(K)
        media = np.mean(campione)
        varianza = np.var(campione, ddof=1)
        errore = np.sqrt(varianza / K)
        z = norm.ppf(0.975)
        ic = (media - z * errore, media + z * errore)
        print(f"K={K} - media: {media:.5f}, varianza: {varianza:.5f}, IC95%: {ic}")
