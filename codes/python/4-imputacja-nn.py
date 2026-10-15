# 3. Imputacja NN
# Kod wyodrębniony z notatnika codes/qmd/4-imputacja-nn.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebych pakietów
import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import gower

# %% # Przykład 1 -- symulacja
# Ustawienie ziarna losowości
np.random.seed(123)

# Parametry symulacji
N = 50000  # rozmiar populacji
n = 1000    # rozmiar próby

# Generowanie zmiennych objaśniających
x1 = np.random.uniform(0, 1, N)
x2 = np.random.uniform(0, 1, N)
x3 = np.random.uniform(0, 1, N)
x4 = np.random.normal(0, 1, N)
x5 = np.random.normal(0, 1, N)
x6 = np.random.normal(0, 1, N)
e = np.random.normal(0, 1, N)

# Generowanie zmiennej y dla trzech modeli
y1 = -1 + x1 + x2 + e
y2 = -1.167 + x1 + x2 + (x1-0.5)**2 + (x2-0.5)**2 + e
y3 = -1.5 + x1 + x2 + x3 + x4 + x5 + x6 + e

# Tworzenie wskaźnika odpowiedzi
logit_p = 0.2 + x1 + x2
p = np.exp(logit_p)/(1 + np.exp(logit_p))
# Tworzenie ramki danych
populacja = pd.DataFrame({
   'id': range(N),
   'x1': x1,
   'x2': x2,
   'x3': x3,
   'x4': x4,
   'x5': x5,
   'x6': x6,
   'y1': y1,
   'y2': y2,
   'y3': y3,
   'p': p
})

y_true = populacja[['y1', 'y2', 'y3']].mean()

# Imputacja średnią z M najbliższych sąsiadów (dla M=1: wartość najbliższego sąsiada)
# Dla zmiennych ilościowych odległość Gowera = odległość Manhattan na zmiennych przeskalowanych rozstępem
# bc=True: korekta obciążenia na podstawie modelu regresji z wielomianem 2 stopnia
def impute_nn(proba, y_col, x_cols, M, bc=False):
   obs = proba[y_col].notna().to_numpy()
   X = MinMaxScaler().fit_transform(proba[x_cols])
   nn = NearestNeighbors(n_neighbors=M, metric='manhattan').fit(X[obs])
   idx = nn.kneighbors(X[~obs], return_distance=False)
   y = proba[y_col].to_numpy().copy()
   y_obs = y[obs]
   if bc:
       Z = PolynomialFeatures(degree=2, include_bias=False).fit_transform(proba[x_cols])
       mu = LinearRegression().fit(Z[obs], y_obs).predict(Z)
       y[~obs] = mu[~obs] + (y_obs - mu[obs])[idx].mean(axis=1)
   else:
       y[~obs] = y_obs[idx].mean(axis=1)
   return y

# Symulacja (2000 razy)
R = 2000
results = np.zeros((R, 12))
columns = [f"{t}_{y}" for t in ['naive', 'nn', 'nn_avg', 'nn_bc'] for y in ['y1', 'y2', 'y3']]

xs_2 = ['x1', 'x2']
xs_6 = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
M_2 = int(np.floor(n**(2/(2+2)))) # M=31 dla d=2
M_6 = int(np.floor(n**(2/(2+6)))) # M=5 dla d=6

for r in range(R):
   # Losowanie próby
   proba = populacja.sample(n=n)

   # Generowanie braków danych
   delta = np.random.binomial(1, proba['p'])
   proba.loc[delta == 0, ['y1', 'y2', 'y3']] = np.nan

   # Średnie dla metody naiwnej
   results[r, 0:3] = proba[['y1', 'y2', 'y3']].mean()

   # Najbliższy sąsiad (k=1)
   results[r, 3:6] = [impute_nn(proba, 'y1', xs_2, 1).mean(),
                      impute_nn(proba, 'y2', xs_2, 1).mean(),
                      impute_nn(proba, 'y3', xs_6, 1).mean()]

   # Średnia z M najbliższych sąsiadów
   results[r, 6:9] = [impute_nn(proba, 'y1', xs_2, M_2).mean(),
                      impute_nn(proba, 'y2', xs_2, M_2).mean(),
                      impute_nn(proba, 'y3', xs_6, M_6).mean()]

   # Średnia z M najbliższych sąsiadów z korektą obciążenia
   results[r, 9:12] = [impute_nn(proba, 'y1', xs_2, M_2, bc=True).mean(),
                       impute_nn(proba, 'y2', xs_2, M_2, bc=True).mean(),
                       impute_nn(proba, 'y3', xs_6, M_6, bc=True).mean()]

plt.figure(figsize=(10, 6))
bias = results - np.tile(y_true, 4)
plt.boxplot(bias)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('')
plt.ylabel('Obciążenie')
plt.title('Imputacja NN: jeden sąsiad, średnia z M sąsiadów i korekta obciążenia')
plt.xticks(range(1, 13), columns, rotation=90)
plt.tight_layout()
plt.show()

bias = results.mean(axis=0) - np.tile(y_true, 4)
pd.DataFrame({'bias': np.round(bias*100, 2),
              'var': np.round(results.var(axis=0, ddof=1)*100, 4),
              'rmse': np.round(np.sqrt(bias**2 + results.var(axis=0, ddof=1))*100, 2)},
             index=columns)

# %% # Przykład 2 -- Gower
dane = pd.DataFrame({
   'plec': pd.Categorical(["K", "M", "K"]),                          # zmienna nominalna
   'wyksztalcenie': pd.Categorical(                                  # zmienna porządkowa
       ["wyższe", "średnie", "podstawowe"],
       categories=["podstawowe", "średnie", "wyższe"],
       ordered=True
   ),
   'wiek': [25, 35, 45]                                             # zmienna ilorazowa
})

gower.gower_matrix(dane.astype({'plec': object, 'wyksztalcenie': object}))
