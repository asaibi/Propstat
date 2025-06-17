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

plt.bar([f'Pagina {i+1}' for i in range(6)], frequenze, color='#4285F4')
plt.title('Frequenze dopo 10.000 passi')
plt.ylabel('Frequenza')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

'''plt.savefig('frequenze_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'frequenze_plot.png'")
print("Frequenze calcolate:")
for i, freq in enumerate(frequenze):
    print(f"Pagina {i+1}: {freq:.4f}")'''
