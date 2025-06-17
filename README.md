# 📊 Simulazione PageRank con Catene di Markov

Questo progetto simula l'algoritmo PageRank tramite catene di Markov, con analisi statistica dei risultati e grafici esplicativi.  
Sono inclusi i punti richiesti dalla traccia: distribuzione invariante, probabilità di terminazione, analisi su Pagina 2 e teorema del limite centrale.

---

## 📘 Matrice di Transizione

```python
transition_matrix = np.array([
    [0.0, 0.23, 0.0, 0.77, 0.0, 0.0],
    [0.09, 0.0, 0.06, 0.0, 0.0, 0.85],
    [0.0, 0.0, 0.0, 0.63, 0.0, 0.37],
    [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.62, 0.0, 0.0, 0.0, 0.38],
])
🎯 Slide 3 — Frequenze dopo 10.000 passi
python
Copia
Modifica
pagina_attuale = np.random.randint(6)
visite = np.zeros(6)
for _ in range(10000):
    visite[pagina_attuale] += 1
    pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
frequenze = visite / 10000
📈 Output: grafico a barre delle frequenze di visita per ogni pagina.

🔁 Slide 4 — Distribuzione indipendente dalla partenza
python
Copia
Modifica
risultati = []
for i in range(6):
    visite = np.zeros(6)
    pagina_attuale = i
    for _ in range(10000):
        visite[pagina_attuale] += 1
        pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
    risultati.append(visite / 10000)
📊 Output: heatmap che mostra la convergenza della distribuzione.

🛑 Slide 5 — Frequenze con terminazione (p = 0.01)
python
Copia
Modifica
for _ in range(10000):
    pagina_attuale = np.random.randint(6)
    passi = 0
    while passi < 100:
        visite[pagina_attuale] += 1
        if np.random.rand() < 0.01:
            break
        pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
        passi += 1
📏 Slide 6 — Intervalli di Confidenza Pagina 2
python
Copia
Modifica
def stima_frequenza_p2(K):
    output = []
    for _ in range(K):
        pagina_attuale = np.random.randint(6)
        tot = p2 = passi = 0
        while passi < 100:
            if pagina_attuale == 1:
                p2 += 1
            tot += 1
            if np.random.rand() < 0.01:
                break
            pagina_attuale = np.random.choice(6, p=transition_matrix[pagina_attuale])
            passi += 1
        output.append(p2 / tot if tot > 0 else 0)
    return np.array(output)
📌 Confronto per K = 50, 100, 200, 2000

🧪 Slide 7 — Teorema del Limite Centrale
python
Copia
Modifica
def medie_campionarie(n_prove, n_campioni=50):
    return [np.mean(stima_frequenza_p2(n_prove)) for _ in range(n_campioni)]
📊 4 istogrammi: medie su campioni da 10, 30, 50, 100

📁 Struttura del Progetto
Copia
Modifica
📦 pagerank-simulazione/
├── README.md
├── pagerank.py
├── requirements.txt
├── grafici/
│   ├── slide3_frequenze.png
│   ├── slide4_heatmap.png
│   ├── slide5_terminazione.png
│   ├── slide6_tabella_ic.png
│   └── slide7_teorema_limite_centrale.png
🔧 Requisiti
nginx
Copia
Modifica
numpy
matplotlib
seaborn
scipy
pandas
Installa tutto con:

bash
Copia
Modifica
pip install -r requirements.txt
