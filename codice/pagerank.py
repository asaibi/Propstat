import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 1. Matrice di transizione (riga = da quale pagina, colonna = verso quale pagina)
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

# 2. Funzione per simulare la passeggiata con terminazione
def stima_frequenza_pagina_2(k_utenti, p_terminazione=0.01):
    n_pagine = 6
    frequenze_p2 = []
    for _ in range(k_utenti):
        pagina_attuale = np.random.randint(n_pagine)
        passi = 0
        visite_p2 = 0
        visite_totali = 0
        while passi < 100:
            if pagina_attuale == 1:
                visite_p2 += 1
            visite_totali += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
            passi += 1
        frequenze_p2.append(visite_p2 / visite_totali if visite_totali > 0 else 0)
    return np.array(frequenze_p2)

# 3. Calcolo intervalli di confidenza per diversi K
for k in [50, 100, 200, 2000]:
    campione = stima_frequenza_pagina_2(k)
    media = np.mean(campione)
    varianza = np.var(campione, ddof=1)
    errore_standard = np.sqrt(varianza / k)
    z = stats.norm.ppf(0.975)
    intervallo = (media - z * errore_standard, media + z * errore_standard)
    print(f"K = {k} --> media: {media:.5f}, varianza: {varianza:.5f}, IC 95%: {intervallo}")

# 4. Distribuzione delle medie campionarie (Teorema del Limite Centrale)
def medie_campionarie(n_prove, n_campioni=50):
    medie = []
    for _ in range(n_campioni):
        frequenze = stima_frequenza_pagina_2(n_prove)
        media = np.mean(frequenze)
        medie.append(media)
    return np.array(medie)

campioni_dict = {
    "Campione 10": medie_campionarie(10),
    "Campione 30": medie_campionarie(30),
    "Campione 50": medie_campionarie(50),
    "Campione 100": medie_campionarie(100),
}

plt.figure(figsize=(12, 8))
for i, (label, medie) in enumerate(campioni_dict.items(), 1):
    plt.subplot(2, 2, i)
    plt.hist(medie, bins=10, color='mediumseagreen', edgecolor='black', alpha=0.8)
    plt.title(label)
    plt.xlabel('Media frequenza Pagina 2')
    plt.ylabel('Frequenza')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
