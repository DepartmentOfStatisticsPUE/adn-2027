# 4b. Imputacja metodą najbliższego sąsiada -- ćwiczenia
# Pod każdym komentarzem "Zadanie" proszę napisać kod.
# Rozwiązania: codes/qmd/4b-imputacja-nn.qmd (Krok 0--5).

# %% Krok 0 -- dane i braki
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LinearRegression

dane = pd.read_csv("data/data6-wydatki.csv")
braki = dane['wydatki'].isna().to_numpy()
dawcy = dane[~braki]
y_dawcow = dawcy['wydatki'].to_numpy()

# obciążenie: średnia po imputacji minus średnia prawdziwa
def obciazenie(y):
    return np.mean(y) - dane['wydatki_prawda'].mean()

def sasiedzi(X, k=1):
    """Numery k najbliższych dawców każdego biorcy (zmienne przeskalowane do [0, 1], odległość miejska)."""
    X = MinMaxScaler().fit_transform(X)
    nn = NearestNeighbors(n_neighbors=k, metric='manhattan').fit(X[~braki])
    return nn.kneighbors(X[braki], return_distance=False)

def wstaw(wartosci):
    """Wstawia wartości w miejsce braków."""
    y = dane['wydatki'].to_numpy().copy()
    y[braki] = wartosci
    return y

# Zadanie: odsetek braków, średnia prawdziwa (wydatki_prawda) i średnia z respondentów.

# Zadanie: wykresy pudełkowe dochodu i wieku według braków
# (dane.assign(brak=braki).boxplot(column=['dochod', 'wiek'], by='brak')).

# Zadanie: imputacja średnią z respondentów (fillna) i jej obciazenie().

# %% Krok 1 -- najbliższy sąsiad krok po kroku
biorca = np.flatnonzero(braki)[0]

# Zadanie: odległość dochodu pierwszego biorcy od dochodu każdego dawcy; najbliższy dawca (idxmin).

# Zadanie: imputacja wszystkich braków: sasiedzi(dane[['dochod']], k=1), wstaw(); obciazenie().

# %% Krok 2 -- same zmienne jakościowe
klasy = ['plec', 'wyksztalcenie', 'klasa_miejsc']

# Zadanie: na ilu zmiennych z `klasy` dawcy różnią się od pierwszego biorcy? (tabela liczebności)

# Zadanie: losowy hot-deck w klasach (groupby) oraz najbliższy sąsiad (k=1) po zmiennych zero-jedynkowych
# (pd.get_dummies); obciazenie() i liczba różnych wstawionych wartości (np.unique).

# %% Krok 3 -- liczba zmiennych
# Zadanie: najbliższy sąsiad (k=1) dla zbiorów zmiennych:
#   dochod
#   + wiek, liczba_osob
#   + wzrost, czas_wywiadu
#   + nr_ankietera, miesiac_urodzenia
# i porównać obciazenie().

# %% Krok 4 -- liczba sąsiadów i korekta obciążenia
xs = ['dochod', 'wiek', 'liczba_osob']

# Zadanie: dla k = 5 i k = 31: dawca losowy spośród k najbliższych (rng.choice) oraz średnia z k najbliższych;
# porównać obciazenie().

# Zadanie: korekta obciążenia dla k = 31:
#   1. model LinearRegression na dawcach,
#   2. wartości teoretyczne mu dla wszystkich i reszty dawców (y_dawcow - mu dawców),
#   3. mu biorcy + średnia reszt jego 31 najbliższych dawców; obciazenie().

# %% Krok 5 -- odległość i skalowanie zmiennych
# Zadanie: najbliższy sąsiad według odległości euklidesowej (NearestNeighbors) po zmiennych xs:
# na danych surowych i po standaryzacji (StandardScaler). Porównać dawcę pierwszego biorcy
# i obciazenie() dla wszystkich braków.
