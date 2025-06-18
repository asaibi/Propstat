#  Analisi Completa - Simulazione PageRank

Questo documento raccoglie tutto il codice Python utilizzato per generare i grafici e i risultati presentati nella simulazione dell'algoritmo PageRank, organizzato slide per slide.

---

##  Matrice di Transizione

```python
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])
```

---

##  Slide 3 – Frequenze dopo 10.000 passi

```python
import numpy as np
import matplotlib.pyplot as plt

transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

visite = np.zeros(6)
pagina_attuale = np.random.randint(6)

for _ in range(10000):
    visite[pagina_attuale] += 1
    pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])

frequenze = visite / 10000

print("Distribuzione finale delle visite:")
for i in range(6):
    print(f"Pagina {i+1}: {frequenze[i]:.4f} ({visite[i]:.0f} visite)")

# Optional: Visualizzazione grafica
plt.bar([f'Pagina {i+1}' for i in range(6)], frequenze, color='#4285F4')
plt.title('Frequenze dopo 10.000 passi')
plt.ylabel('Frequenza')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
```

---

##  Slide 4 – Heatmap: indipendenza dalla partenza

```python
import numpy as np
import matplotlib.pyplot as plt

transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

# Simulazione: indipendenza dalla pagina iniziale
n_passi = 10000
n_pagine = 6
risultati = []

for pagina_iniziale in range(n_pagine):
    visite = np.zeros(n_pagine, dtype=int)
    pagina_attuale = pagina_iniziale
    for _ in range(n_passi):
        visite[pagina_attuale] += 1
        pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
    frequenze = visite / n_passi
    risultati.append(frequenze)

# Organizzazione risultati in DataFrame
import pandas as pd
df = pd.DataFrame(risultati, columns=[f'Pagina {i+1}' for i in range(n_pagine)],
                  index=[f'Inizio in P{i+1}' for i in range(n_pagine)])

# Visualizzazione come heatmap
import seaborn as sns
plt.figure(figsize=(8, 5))
sns.heatmap(df, annot=True, fmt=".2f", cmap="Blues", cbar=False)
plt.title("Distribuzione finale delle visite partendo da ogni pagina", fontsize=12)
plt.tight_layout()
plt.show()
print("\nDistribuzione finale delle visite:")
print(df)
```

---

##  Slide 5 – Frequenze con terminazione (p = 0.01)

```python
import numpy as np

# Parametri
n_pagine = 6
n_utenti = 10000
p_terminazione = 0.01
max_passi_per_utente = 100

# Matrice di transizione
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

# Contatore delle visite totali
visite = np.zeros(n_pagine, dtype=int)

# Simulazione per ciascun utente
for _ in range(n_utenti):
    pagina_attuale = np.random.randint(n_pagine)  # pagina iniziale casuale
    passi = 0
    while passi < max_passi_per_utente:
        visite[pagina_attuale] += 1
        if np.random.rand() < p_terminazione:
            break  # termina con probabilità p
        pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
        passi += 1

# Calcolo frequenze normalizzate
frequenze = visite / np.sum(visite)

# Stampa risultato
print("\n📊 Frequenze con terminazione (p = 0.01):\n")
for i, freq in enumerate(frequenze):
    print(f"Pagina {i+1}: {freq:.4f}")

```

---

##  Slide 6 – Intervalli di confidenza per Pagina 2

```python
import numpy as np
from scipy.stats import norm

# Parametri
n_pagine = 6
p_terminazione = 0.01
max_passi = 100

# Matrice di transizione
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

# Funzione per stimare la frequenza di visita alla Pagina 2
def stima_frequenza_pagina_2(K):
    output = []
    for _ in range(K):
        pagina_attuale = np.random.randint(n_pagine)
        p2 = 0
        tot = 0
        passi = 0
        while passi < max_passi:
            if pagina_attuale == 1:
                p2 += 1
            tot += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
            passi += 1
        output.append(p2 / tot if tot > 0 else 0)
    return np.array(output)

# Calcolo e stampa degli intervalli di confidenza per diversi K
for K in [50, 100, 200, 2000]:
    campione = stima_frequenza_pagina_2(K)
    media = np.mean(campione)
    varianza = np.var(campione, ddof=1)
    errore = np.sqrt(varianza / K)
    z = norm.ppf(0.975)
    ic = (media - z * errore, media + z * errore)
    print(f"\n📏 K = {K}")
    print(f"  Media stimata: {media:.5f}")
    print(f"  Varianza campionaria: {varianza:.5f}")
    print(f"  Intervallo di confidenza 95%: ({ic[0]:.5f}, {ic[1]:.5f})")

```

---

##  Slide 7 – Teorema del Limite Centrale

```python
import numpy as np
from scipy.stats import norm

# Usa la stessa matrice di transizione già definita
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])

n_pagine = 6
p_terminazione = 0.01
max_passi = 100

# Funzione per stimare la frequenza di visita alla Pagina 2
def stima_frequenza_pagina_2(K):
    output = []
    for _ in range(K):
        pagina_attuale = np.random.randint(n_pagine)
        tot = p2 = passi = 0
        while passi < max_passi:
            if pagina_attuale == 1:
                p2 += 1
            tot += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(n_pagine, p=transition_matrix[pagina_attuale])
            passi += 1
        output.append(p2 / tot if tot > 0 else 0)
    return np.array(output)

# Funzione per calcolare 50 medie campionarie
def medie_campionarie(n_prove, n_campioni=50):
    medie = []
    for _ in range(n_campioni):
        frequenze = stima_frequenza_pagina_2(n_prove)
        media = np.mean(frequenze)
        medie.append(media)
    return np.array(medie)

# Stampa a console le distribuzioni
for taglia in [10, 30, 50, 100]:
    campione = medie_campionarie(taglia)
    media = np.mean(campione)
    var = np.var(campione, ddof=1)
    print(f"\n📊 Campione da {taglia} prove (50 medie calcolate):")
    print(f"  Media generale: {media:.5f}")
    print(f"  Varianza delle medie: {var:.5f}")
    print(f"  Prime 10 medie: {np.round(campione[:10], 5)}")
```

---
