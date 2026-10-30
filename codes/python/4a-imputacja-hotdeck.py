# 3a. Imputacja hot-deck
# Kod wyodrębniony z notatnika codes/qmd/4a-imputacja-hotdeck.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% # Przykład 1 z zajęć
przyklad1 = pd.DataFrame({
    'plec': ["K", "K", "K", "K", "M", "M", "M", "M"],
    'X': [21, 24, 30, 35, 22, 28, 33, 40],
    'Y': [25, np.nan, 35, np.nan, 45, np.nan, 55, 65]
})
przyklad1

def hotdeck_losowy(dane, y, klasy=None):
    wynik = dane[y].copy()
    # bez klas wszystkie jednostki tworzą jedną grupę
    grupy = [dane.index] if klasy is None else dane.groupby(klasy, observed=True).groups.values()
    for idx in grupy:
        y_grupa = dane.loc[idx, y]
        biorcy = y_grupa.index[y_grupa.isna()]
        dawcy = y_grupa.dropna().to_numpy()
        # jeżeli w klasie nie ma dawców, braki pozostają
        if len(biorcy) > 0 and len(dawcy) > 0:
            wynik.loc[biorcy] = np.random.choice(dawcy, size=len(biorcy), replace=True)
    return wynik

def hotdeck_sekwencyjny(dane, y, sortowanie, klasy=None):
    wynik = dane[y].copy()
    grupy = [dane.index] if klasy is None else dane.groupby(klasy, observed=True).groups.values()
    for idx in grupy:
        y_grupa = dane.loc[idx].sort_values(sortowanie)[y]
        if y_grupa.notna().any():
            # brak na początku uzupełniamy ostatnim respondentem, tak jak impute_shd w R
            wynik.loc[y_grupa.index] = y_grupa.ffill().fillna(y_grupa.dropna().iloc[-1])
    return wynik

np.random.seed(2025)
przyklad1.assign(Y=hotdeck_losowy(przyklad1, 'Y'))

np.random.seed(2025)
przyklad1.assign(Y=hotdeck_losowy(przyklad1, 'Y', klasy='plec'))

przyklad1.assign(Y=hotdeck_sekwencyjny(przyklad1, 'Y', 'X'))

przyklad1.assign(Y=hotdeck_sekwencyjny(przyklad1, 'Y', 'X', klasy='plec'))

# %% # Przykład 2 -- czytelnictwo
data = pd.read_csv("data/data4-czytelnictwo.csv",
                   dtype={'plec': 'category',
                         'wiek': 'float64',
                         'wyksztalcenie': 'category',
                         'czyta_ksiazki': 'float64',
                         'czyta_ksiazki_z_brakami': 'float64'})
data['wiek_kat'] = pd.cut(data['wiek'], bins=[17, 29, 39, 49, 59, 80])
data.head()

respondenci = data[data['czyta_ksiazki_z_brakami'].notna()]
pd.crosstab(respondenci['plec'], respondenci['wyksztalcenie'])

dawcy_klasy = respondenci.groupby(['plec', 'wyksztalcenie', 'wiek_kat'], observed=False).size()
(dawcy_klasy == 0).sum()

np.random.seed(2025)
y = 'czyta_ksiazki_z_brakami'
wyniki = {
    'respondenci': data[y],
    'losowy': hotdeck_losowy(data, y),
    'klasy: plec, wyksztalcenie': hotdeck_losowy(data, y, klasy=['plec', 'wyksztalcenie']),
    'klasy: plec, wyksztalcenie, wiek': hotdeck_losowy(data, y, klasy=['plec', 'wyksztalcenie', 'wiek_kat']),
    'sekwencyjny: wiek': hotdeck_sekwencyjny(data, y, 'wiek')
}

pd.DataFrame({
    'srednia': [data['czyta_ksiazki'].mean()] + [w.mean() for w in wyniki.values()],
    'braki': [0] + [w.isna().sum() for w in wyniki.values()]
}, index=['prawda'] + list(wyniki.keys()))

# %% # Symulacja
# Ustawienie ziarna losowości
np.random.seed(123)

# Parametry symulacji
N = 50000  # rozmiar populacji
n = 1000    # rozmiar próby

# Generowanie zmiennych objaśniających
x1 = np.random.uniform(0, 1, N)
x2 = np.random.uniform(0, 1, N)
e = np.random.normal(0, 1, N)

# Generowanie zmiennej y dla dwóch modeli
y1 = -1 + x1 + x2 + e
y2 = -1.167 + x1 + x2 + (x1-0.5)**2 + (x2-0.5)**2 + e

# Tworzenie wskaźnika odpowiedzi
logit_p = 0.2 + x1 + x2
p = np.exp(logit_p)/(1 + np.exp(logit_p))

# Tworzenie ramki danych
populacja = pd.DataFrame({
   'id': range(N),
   'x1': x1,
   'x2': x2,
   'y1': y1,
   'y2': y2,
   'p': p,
   # klasy imputacyjne
   'klasa': np.minimum(x1 // 0.25, 3) * 4 + np.minimum(x2 // 0.25, 3)
})

y_true = populacja[['y1', 'y2']].mean()

# Imputacja średnią w klasach
def impute_srednia(proba, y):
    return proba[y].fillna(proba.groupby('klasa')[y].transform('mean'))

# Symulacja (2000 razy)
R = 2000
results = np.zeros((R, 10))
columns = [f"{t}_{y}" for t in ['naive', 'hd', 'hd_kl', 'sr_kl', 'shd'] for y in ['y1', 'y2']]

for r in range(R):
    # Losowanie próby
    proba = populacja.sample(n=n)

    # Generowanie braków danych
    delta = np.random.binomial(1, proba['p'])
    proba.loc[delta == 0, ['y1', 'y2']] = np.nan

    results[r, 0:2] = proba[['y1', 'y2']].mean()
    results[r, 2:4] = [hotdeck_losowy(proba, y).mean() for y in ['y1', 'y2']]
    results[r, 4:6] = [hotdeck_losowy(proba, y, klasy='klasa').mean() for y in ['y1', 'y2']]
    results[r, 6:8] = [impute_srednia(proba, y).mean() for y in ['y1', 'y2']]
    results[r, 8:10] = [hotdeck_sekwencyjny(proba, y, 'x1').mean() for y in ['y1', 'y2']]

plt.figure(figsize=(10, 6))
plt.boxplot(results - np.tile(y_true, 5))
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('')
plt.ylabel('Obciążenie')
plt.title('Hot-deck: bez klas, w klasach, sekwencyjny i średnia w klasach')
plt.xticks(range(1, 11), columns, rotation=90)
plt.tight_layout()
plt.show()

bias = results.mean(axis=0) - np.tile(y_true, 5)
pd.DataFrame({'bias': np.round(bias*100, 2),
              'var': np.round(results.var(axis=0, ddof=1)*100, 4),
              'rmse': np.round(np.sqrt(bias**2 + results.var(axis=0, ddof=1))*100, 2)},
             index=columns)

np.random.seed(2025)
proba = populacja.sample(n=n)
y1_pelne = proba['y1'].copy()
proba.loc[np.random.binomial(1, proba['p']) == 0, 'y1'] = np.nan

pd.Series({'prawda': y1_pelne.std(),
           'respondenci': proba['y1'].std(),
           'hd_kl': hotdeck_losowy(proba, 'y1', klasy='klasa').std(),
           'sr_kl': impute_srednia(proba, 'y1').std()}).round(3)
