# 6. Kalibracja -- wstęp
# Kod wyodrębniony z notatnika codes/qmd/9-kalibracja-wstep.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import numpy as np
import pandas as pd
import polars as pl ## svy pracuje na ramkach danych polars
import svy

# %% # Rozwiązanie przykładu 1

# %% ## Podejście krok po kroku
dane = pd.read_csv("data/data5-kalibracja.csv", sep=';')
dane.head()

wynik_poprawny = np.array([52.275, 50.5821, 51.4286, 50.5462, 48.4301, 39.9657, 
                       51.0054, 54.3911, 45.4675, 49.7357, 52.275, 51.4286, 
                       45.0443, 51.0054, 51.0054, 48.8893, 52.275, 52.275, 
                       50.5462, 51.4286])
wynik_poprawny

d = dane['Waga'].values.astype(np.float64)

Xs = pd.get_dummies(dane[['Przychod', 'Wielkosc']], drop_first=False).values.astype(np.float64)
Xs[:3,:]

wartosci_globalne = np.array([19000, 280, 720], dtype=np.float64)

wartosci_est = np.sum(Xs * d[:, np.newaxis], axis=0)
wartosci_est

n_wierszy = len(dane)

macierz_sum = np.zeros((3, 3), dtype=np.float64)
for i in range(n_wierszy):
    macierz_sum += d[i] * np.outer(Xs[i,], Xs[i,])
macierz_sum

w1 = np.zeros(n_wierszy, dtype=np.float64)
for i in range(n_wierszy):
    w1[i] = d[i] + d[i] * (wartosci_globalne - wartosci_est).T @ np.linalg.solve(macierz_sum, Xs[i,])

np.round(w1, 3)
np.round(wynik_poprawny, 3)
np.allclose(np.round(w1, 3), np.round(wynik_poprawny, 3))

# %% ## Sposób 2: obliczenia macierzowe
temp_matrix = np.linalg.solve((d[:, np.newaxis] * Xs).T @ Xs, Xs.T)
w2 = d * (1 + (wartosci_globalne - wartosci_est) @ temp_matrix)
w2 = w2.flatten()  # equivalent to as.numeric() in R
w2

np.allclose(np.round(w2, 3), np.round(wynik_poprawny, 3))

# %% ## Sposób 3: Wykorzystanie dostępnych pakietów
dane_pl = pl.from_pandas(dane).with_columns(pl.col("Waga").cast(pl.Float64))
proba = svy.Sample(dane_pl, svy.Design(wgt="Waga")) ## waga pierwotna (d)

## wartosci globalne: zmienna ciągła oraz zmienna jakościowa (svy.Cat)
totals = {"Przychod": 19000, svy.Cat("Wielkosc"): {"L": 280, "M": 720}}

proba_kalib = proba.weighting.calibrate(controls=totals, wgt_name="calib_weight")
w3 = proba_kalib.data["calib_weight"].to_numpy()
proba_kalib.data.select(["Lp", "Przychod", "Wielkosc", "Waga", "calib_weight"]).head(10)

np.allclose(np.round(w3, 3), np.round(wynik_poprawny, 3))
