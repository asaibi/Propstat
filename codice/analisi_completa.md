🧮 Matrice di Transizione

<pre>``` python transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])</pre>

<pre>```</pre>

🎯 Slide 3 – Frequenze dopo 10.000 passi

visite = np.zeros(6)
pagina_attuale = np.random.randint(6)
for _ in range(10000):
    visite[pagina_attuale] += 1
    pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
frequenze = visite / 10000

🔁 Slide 4 – Heatmap: indipendenza dalla partenza

risultati = []
for i in range(6):
    visite = np.zeros(6)
    pagina_attuale = i
    for _ in range(10000):
        visite[pagina_attuale] += 1
        pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
    risultati.append(visite / 10000)

df = pd.DataFrame(risultati, index=[f'Start P{i+1}' for i in range(6)],
                  columns=[f'Pagina {i+1}' for i in range(6)])

🛑 Slide 5 – Frequenze con terminazione (p = 0.01)

p_terminazione = 0.01
max_passi = 100
visite = np.zeros(6)
for _ in range(10000):
    pagina_attuale = np.random.randint(6)
    passi = 0
    while passi < max_passi:
        visite[pagina_attuale] += 1
        if np.random.rand() < p_terminazione:
            break
        pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
        passi += 1
frequenze = visite / np.sum(visite)

📏 Slide 6 – Intervalli di confidenza per Pagina 2

def stima_frequenza_p2(K):
    output = []
    for _ in range(K):
        pagina_attuale = np.random.randint(6)
        tot = p2 = passi = 0
        while passi < 100:
            if pagina_attuale == 1:
                p2 += 1
            tot += 1
            if np.random.rand() < p_terminazione:
                break
            pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
            passi += 1
        output.append(p2 / tot if tot > 0 else 0)
    return np.array(output)

for K in [50, 100, 200, 2000]:
    campione = stima_frequenza_p2(K)
    media = np.mean(campione)
    var = np.var(campione, ddof=1)
    errore = np.sqrt(var / K)
    z = norm.ppf(0.975)
    ic = (media - z * errore, media + z * errore)
    print(f"K={K} → media: {media:.5f}, var: {var:.5f}, IC 95%: {ic}")

🧪 Slide 7 – Teorema del Limite Centrale

def medie_campionarie(n_prove, n_campioni=50):
    return [np.mean(stima_frequenza_p2(n_prove)) for _ in range(n_campioni)]

campioni = {
    "10 prove": medie_campionarie(10),
    "30 prove": medie_campionarie(30),
    "50 prove": medie_campionarie(50),
    "100 prove": medie_campionarie(100),
}

Ogni serie campioni[...] viene poi visualizzata in un istogramma.
