# 2a. Imputacja dedukcyjna z wykorzystaniem ograniczeń liniowych
# Kod wyodrębniony z notatnika codes/qmd/3a-imputacja-dedukcyjna-ograniczenia.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import numpy as np
from numpy.linalg import pinv
from sympy import symbols, solve, Eq

# %% # Bez wykorzystania dodatkowych pakietów
x1 = 100
x4 = 40
x3 = 150

# Definiujemy macierze dla układu równań:
# x2 = x3 - x1      →  x2 + (-1)x3 + x1 = 0
# x5 = x1 - x4      →  x5 + (-1)x1 + x4 = 0

# Macierz dla niewiadomych [x2, x5]
Am = np.array([
        [1, 0],     # przy x2
        [0, 1]      # przy x5
        ])

    # Macierz dla znanych wartości [x1, x3, x4]
Ao = np.array([
        [1, -1, 0],    # przy x1, x3, x4 w równaniu dla x2
        [-1, 0, 1]     # przy x1, x3, x4 w równaniu dla x5
        ])

    # Wektor znanych wartości [x1, x3, x4]
xo = np.array([x1, x3, x4])

    # Wektor wyrazów wolnych
b = np.zeros(2)

    # Obliczamy prawą stronę równania
b_star = b - np.dot(Ao, xo)

    # Obliczamy rozwiązanie używając pseudoodwrotności Moore-Penrose
x_m = np.dot(pinv(Am), b_star)
x_m

Am = np.array([[1, -1],[-1, 0]])
Ao = np.array([[1], [2]])
xo = np.array([10])
b = np.array([0, 0])
b_star = b - np.dot(Ao, xo)
xm = np.linalg.solve(Am, b_star)
xm

# %% # Wykorzystanie odpowiednich pakietów
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

eq1 = Eq(x1 + x2, x3)  # x1 + x2 = x3
eq2 = Eq(x4 + x5, x1)  # x4 + x5 = x1

known_values = {
        x1: 100,  # x1 = 100
        x4: 40,   # x4 = 40
        x3: 150   # x3 = 150
        }

# Tworzymy system równań
system = [eq1.subs(known_values), eq2.subs(known_values)]

# Rozwiązujemy system
solution = solve(system, [x2, x5])
solution
# Tworzymy pełne rozwiązanie dodając znane wartości
full_solution = {**known_values, **solution}
full_solution
