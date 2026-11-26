# 4b. Imputacja metodą najbliższego sąsiada
# Kod wyodrębniony z notatnika codes/qmd/4b-imputacja-nn.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LinearRegression
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import gower

# %% # Krok 0 -- dane i braki
dane = pd.read_csv("data/data6-wydatki.csv")
braki = dane['wydatki'].isna().to_numpy()
braki.mean()

print(dane['wydatki_prawda'].mean())
print(dane['wydatki'].mean())

dane.assign(brak=braki).boxplot(column=['dochod', 'wiek'], by='brak')
plt.show()

# obciążenie: średnia po imputacji minus średnia prawdziwa
def obciazenie(y):
    return np.mean(y) - dane['wydatki_prawda'].mean()

obciazenie(dane['wydatki'].fillna(dane['wydatki'].mean()))

dawcy = dane[~braki]
y_dawcow = dawcy['wydatki'].to_numpy()

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

# %% # Krok 1 -- najbliższy sąsiad krok po kroku
biorca = np.flatnonzero(braki)[0]
dane.loc[biorca, ['dochod', 'wiek', 'liczba_osob', 'wydatki_prawda']]

odl = (dawcy['dochod'] - dane.loc[biorca, 'dochod']).abs()
dawcy.loc[odl.idxmin(), ['dochod', 'wiek', 'liczba_osob', 'wydatki']]

idx = sasiedzi(dane[['dochod']], k=1)
obciazenie(wstaw(y_dawcow[idx[:, 0]]))

# %% # Krok 2 -- same zmienne jakościowe
klasy = ['plec', 'wyksztalcenie', 'klasa_miejsc']
# na ilu zmiennych dawcy różnią się od pierwszego biorcy?
(dawcy[klasy] != dane.loc[biorca, klasy]).sum(axis=1).value_counts().sort_index()

rng = np.random.default_rng(2025)
# losowy hot-deck w klasach
imp_hd = dane.groupby(klasy)['wydatki'].transform(
    lambda s: s.fillna(pd.Series(rng.choice(s.dropna(), len(s)), index=s.index)))
# najbliższy sąsiad (k = 1); zmienne jakościowe zamieniamy na zero-jedynkowe
idx = sasiedzi(pd.get_dummies(dane[klasy]), k=1)
imp_nn = wstaw(y_dawcow[idx[:, 0]])
print(obciazenie(imp_hd), obciazenie(imp_nn))
print(len(np.unique(imp_hd[braki])), len(np.unique(imp_nn[braki])))

# %% # Krok 3 -- liczba zmiennych
zm1 = ['dochod']
zm2 = zm1 + ['wiek', 'liczba_osob']
zm3 = zm2 + ['wzrost', 'czas_wywiadu']
zm4 = zm3 + ['nr_ankietera', 'miesiac_urodzenia']
pd.Series([obciazenie(wstaw(y_dawcow[sasiedzi(dane[zm], k=1)[:, 0]])) for zm in [zm1, zm2, zm3, zm4]]).round(1)

# %% # Krok 4 -- liczba sąsiadów i korekta obciążenia
xs = ['dochod', 'wiek', 'liczba_osob']
rng = np.random.default_rng(2025)
idx5 = sasiedzi(dane[xs], k=5)
idx31 = sasiedzi(dane[xs], k=31)
# dawca losowany spośród k najbliższych
print(obciazenie(wstaw([rng.choice(y_dawcow[i]) for i in idx5])),
      obciazenie(wstaw([rng.choice(y_dawcow[i]) for i in idx31])))
# średnia z k najbliższych
print(obciazenie(wstaw(y_dawcow[idx5].mean(axis=1))),
      obciazenie(wstaw(y_dawcow[idx31].mean(axis=1))))

# korekta obciążenia: wartość teoretyczna z modelu + średnia reszt k najbliższych dawców
model = LinearRegression().fit(dawcy[xs], y_dawcow)
mu = model.predict(dane[xs])
reszty = y_dawcow - mu[~braki]
obciazenie(wstaw(mu[braki] + reszty[idx31].mean(axis=1)))

# %% # Krok 5 -- odległość i skalowanie zmiennych
X = dane[xs].to_numpy(dtype=float)
X_std = StandardScaler().fit_transform(X)
nn_sur = NearestNeighbors(n_neighbors=1).fit(X[~braki]).kneighbors(X[braki], return_distance=False)[:, 0]
nn_std = NearestNeighbors(n_neighbors=1).fit(X_std[~braki]).kneighbors(X_std[braki], return_distance=False)[:, 0]
# najbliższy dawca pierwszego biorcy
print(dane.loc[biorca, xs])
dawcy.iloc[[nn_sur[0], nn_std[0]]][xs]

print(obciazenie(wstaw(y_dawcow[nn_sur])), obciazenie(wstaw(y_dawcow[nn_std])))

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

# Imputacja średnią z k najbliższych sąsiadów (dla k=1: wartość najbliższego sąsiada)
# Dla zmiennych ilościowych odległość Gowera = odległość Manhattan na zmiennych przeskalowanych rozstępem
# bc=True: korekta obciążenia na podstawie modelu regresji z wielomianem 2 stopnia
def impute_nn(proba, y_col, x_cols, k, bc=False):
   obs = proba[y_col].notna().to_numpy()
   X = MinMaxScaler().fit_transform(proba[x_cols])
   nn = NearestNeighbors(n_neighbors=k, metric='manhattan').fit(X[obs])
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
k_2 = int(np.floor(n**(2/(2+2)))) # k=31 dla p=2
k_6 = int(np.floor(n**(2/(2+6)))) # k=5 dla p=6

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

   # Średnia z k najbliższych sąsiadów
   results[r, 6:9] = [impute_nn(proba, 'y1', xs_2, k_2).mean(),
                      impute_nn(proba, 'y2', xs_2, k_2).mean(),
                      impute_nn(proba, 'y3', xs_6, k_6).mean()]

   # Średnia z k najbliższych sąsiadów z korektą obciążenia
   results[r, 9:12] = [impute_nn(proba, 'y1', xs_2, k_2, bc=True).mean(),
                       impute_nn(proba, 'y2', xs_2, k_2, bc=True).mean(),
                       impute_nn(proba, 'y3', xs_6, k_6, bc=True).mean()]

plt.figure(figsize=(10, 6))
bias = results - np.tile(y_true, 4)
plt.boxplot(bias)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('')
plt.ylabel('Obciążenie')
plt.title('Imputacja NN: jeden sąsiad, średnia z k sąsiadów i korekta obciążenia')
plt.xticks(range(1, 13), columns, rotation=90)
plt.tight_layout()
plt.show()

bias = results.mean(axis=0) - np.tile(y_true, 4)
pd.DataFrame({'bias': np.round(bias*100, 2),
              'var': np.round(results.var(axis=0, ddof=1)*100, 4),
              'rmse': np.round(np.sqrt(bias**2 + results.var(axis=0, ddof=1))*100, 2),
              'mc_se': np.round(np.sqrt(results.var(axis=0, ddof=1)/R)*100, 3)},
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

# %% # Przykład 3 -- czytelnictwo
data = pd.read_csv("data/data4-czytelnictwo.csv",
                   dtype={'plec': 'category',
                          'wiek': 'float64',
                          'wyksztalcenie': 'category',
                          'czyta_ksiazki': 'float64',
                          'czyta_ksiazki_z_brakami': 'float64'})

y = 'czyta_ksiazki_z_brakami'
xs = ['plec', 'wiek', 'wyksztalcenie']
resp = data[y].notna().to_numpy()
y_resp = data.loc[resp, y].to_numpy()

X = data[xs].astype({'plec': object, 'wyksztalcenie': object})
D = gower.gower_matrix(X[~resp], X[resp])

remisy = (D == D.min(axis=1, keepdims=True)).sum(axis=1)
print(pd.Series(remisy).value_counts().sort_index())
(remisy > 1).mean()

rng = np.random.default_rng(2025)
# dawcy uporządkowani od najbliższego; przy remisie decyduje kolejność w danych
kolejnosc = np.argsort(D, axis=1, kind='stable')
biorcy = np.arange(D.shape[0])

imputacje = {
    # k = 1: pierwszy dawca w kolejności danych
    'k = 1': y_resp[kolejnosc[:, 0]],
    # k = 1: dawca losowany spośród remisów
    'k = 1, remisy losowo': np.array([rng.choice(y_resp[D[i] == D[i].min()]) for i in biorcy]),
    # k = 5: dawca losowany spośród 5 najbliższych
    'k = 5, dawca losowy': y_resp[kolejnosc[biorcy, rng.integers(0, 5, len(biorcy))]],
    # k = 5: dominanta wartości 5 najbliższych (przy nieparzystym k nie ma remisu)
    'k = 5, dominanta': (y_resp[kolejnosc[:, :5]].mean(axis=1) > 0.5).astype(float),
}

Z = pd.get_dummies(data[['plec', 'wyksztalcenie']]).astype(float)
Z['wiek'] = (data['wiek'] - data['wiek'].min()) / (data['wiek'].max() - data['wiek'].min())
Z[y] = data[y]
knn_srednia = KNNImputer(n_neighbors=5).fit_transform(Z)[~resp, -1]

prawda = data.loc[~resp, 'czyta_ksiazki'].to_numpy()
pd.DataFrame({
    'srednia': [data['czyta_ksiazki'].mean(), data[y].mean()] +
               [(y_resp.sum() + v.sum()) / len(data) for v in imputacje.values()] +
               [(y_resp.sum() + knn_srednia.sum()) / len(data)],
    'trafnosc': [np.nan, np.nan] + [np.mean(v == prawda) for v in imputacje.values()] + [np.nan]
}, index=['prawda', 'respondenci'] + list(imputacje.keys()) + ['k = 5, średnia (KNNImputer)']).round(3)
