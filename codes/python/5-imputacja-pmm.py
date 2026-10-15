# 4. Imputacja PMM
# Kod wyodrębniony z notatnika codes/qmd/5-imputacja-pmm.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebych pakietów
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import NearestNeighbors
import gower

# %% # Przykład 1 z zajęć
przyklad1 = pd.DataFrame({
    'X': np.arange(10, 36, 5),
    'Y': [25, 35, np.nan, 55, 65, np.nan]
})

mask = ~przyklad1['Y'].isna()
X = przyklad1.loc[mask, 'X'].values.reshape(-1, 1)
y = przyklad1.loc[mask, 'Y'].values

## Zwykła regresja liniowa
model = LinearRegression()
model.fit(X, y)

## Wartości przewidywane
przyklad1['pred'] = model.predict(przyklad1['X'].values.reshape(-1, 1))

# Sąsiadzi
# Dane obserwowane
observed_pred = przyklad1.loc[mask, 'pred'].values.reshape(-1, 1)
# Dane brakujące
missing_pred = przyklad1.loc[~mask, 'pred'].values.reshape(-1, 1)

# Znajdź najbliższych sąsiadów
nbrs = NearestNeighbors(n_neighbors=1).fit(observed_pred)
distances, indices = nbrs.kneighbors(missing_pred)

# Imputacja wartości
przyklad1.loc[~mask, 'Y'] = przyklad1.loc[mask, 'Y'].values[indices.flatten()]

przyklad1

# %% # Krótkie ćwiczenie
np.random.seed(42)
n = 10

df = pd.DataFrame({
    'id': range(1, 11),
    'plec': ["K", "M", "M", "K", "M", "K", "M", "K", "M", "K"],
    'rok_studiow': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
    'pracuje': ["Tak", "Nie", "Tak", "Nie", "Tak", "Nie", "Tak", "Tak", "Nie", "Tak"],
    'piwa': [2, 5, 8, np.nan, 6, np.nan, 9, 4, 7, np.nan]
})

# %% # Przykład 2 -- czytelnictwo
data = pd.read_csv("data/data4-czytelnictwo.csv", 
                   dtype={'plec': 'category', 
                         'wiek': 'float64',
                         'wyksztalcenie': 'category',
                         'czyta_ksiazki': 'float64',  # zmiana z bool
                         'czyta_ksiazki_z_brakami': 'float64'})  # zmiana z bool

# Head
data.head()
# Summary
data.describe(include='all')

data['czyta_ksiazki_z_brakami_nni'] = data['czyta_ksiazki_z_brakami']
data['czyta_ksiazki_z_brakami_pmm'] = data['czyta_ksiazki_z_brakami']

def pmm_imputation(X, y):
   # Maska dla obserwowanych wartości
   mask = ~y.isna()

   # Przygotowanie danych do modelu (zmienne jakościowe jako zmienne zero-jedynkowe)
   X_encoded = pd.get_dummies(X, drop_first=True, dtype=float)

   # Dopasowanie modelu regresji liniowej (jak impute_lm w R)
   model = LinearRegression()
   model.fit(X_encoded[mask], y[mask])

   # Przewidywane wartości
   pred_all = model.predict(X_encoded).reshape(-1, 1)

   # Dla każdej brakującej wartości znajdź najbliższą obserwowaną (wg wartości przewidywanych)
   nbrs = NearestNeighbors(n_neighbors=1).fit(pred_all[mask])
   distances, indices = nbrs.kneighbors(pred_all[~mask])

   # Przypisz wartość od najbliższego sąsiada
   y_imputed = y.copy()
   y_imputed[~mask] = y[mask].values[indices.flatten()]

   return y_imputed

def nn_imputation(X, y, k=1):
   # Oblicz macierz odległości Gowera (zmienne jakościowe muszą być typu object)
   X_gower = X.astype({col: object for col in X.select_dtypes(include=['category']).columns})
   gower_mat = gower.gower_matrix(X_gower)

   # Maska dla obserwowanych wartości
   mask = (~y.isna()).to_numpy()

   # Imputacja
   y_imputed = y.copy()
   
   for idx in y[~mask].index:
       # Weź odległości do wszystkich obserwowanych wartości
       distances = gower_mat[idx, mask]
       # Znajdź k najbliższych sąsiadów
       closest = np.argpartition(distances, k)[:k]
       # Wybierz losowo jednego z k najbliższych sąsiadów
       chosen = np.random.choice(closest)
       # Przypisz wartość od wybranego sąsiada
       y_imputed[idx] = y[mask].iloc[chosen]
   
   return y_imputed
 

# Wykonanie imputacji
X = data[['plec', 'wiek', 'wyksztalcenie']]
data['czyta_ksiazki_z_brakami_pmm'] = pmm_imputation(X, data['czyta_ksiazki_z_brakami_pmm'])
data['czyta_ksiazki_z_brakami_nni'] = nn_imputation(X, data['czyta_ksiazki_z_brakami_nni'], k=1)

# Obliczenie średnich
results = pd.DataFrame({
   'True': [data['czyta_ksiazki'].mean()],
   'NNI': [data['czyta_ksiazki_z_brakami_nni'].mean()],
   'PMM': [data['czyta_ksiazki_z_brakami_pmm'].mean()]
})

# Średnie wartości
results
