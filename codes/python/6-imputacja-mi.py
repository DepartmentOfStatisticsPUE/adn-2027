# 5. Imputacja wielokrotna
# Kod wyodrębniony z notatnika codes/qmd/6-imputacja-mi.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebych pakietów
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.imputation import mice

# %% # Przykład 1 z zajęć
# Set random seed for reproducibility
np.random.seed(42)

n_rows = 20
# Create original dataframe
df_example = pd.DataFrame({
    'A': np.arange(1, n_rows + 1) * 2,
    'B': 5 + np.arange(1, n_rows + 1) * 2 + 10 * np.random.normal(size=n_rows),
    'C': 2 + np.sqrt(np.arange(1, n_rows + 1)) + np.random.normal(size=n_rows)
})

# Create copy with missing values
df_example_miss = df_example.copy()
df_example_miss.loc[[1, 4, 12], 'A'] = np.nan  # R indices 2,5,13
df_example_miss.loc[[0, 1, 7, 19], 'B'] = np.nan  # R indices 1,2,8,20
df_example_miss.loc[[8, 9, 13, 14, 15, 16, 17], 'C'] = np.nan  # R indices 9,10,14:18
df_example_miss

imp = IterativeImputer(random_state=42, max_iter=10, n_nearest_features=None)
df_example_imp_single = pd.DataFrame(
    imp.fit_transform(df_example_miss),
    columns=df_example_miss.columns
)

df_example_imp_single

np.random.seed(2025)
df_example_imp = mice.MICEData(df_example_miss, k_pmm=5)
df_example_imp.update_all(5)

df_example_imp.data

df_example.mean() ## bez braków
df_example_miss.mean() ## z brakami
df_example_imp.data.mean() ## po imputacji

np.random.seed(2025)
df_example_imp = mice.MICEData(df_example_miss, k_pmm=5)
df_example_imp.set_imputer("B", formula="A")
df_example_imp.set_imputer("C", formula="A")

m = 4
df_example_imp_all = []
for i in range(m):
    df_example_imp.update_all(5)
    df_example_imp_all.append(df_example_imp.data.copy())

df_example_imp_all[0]

srednie = pd.concat([d.mean() for d in df_example_imp_all], axis=1)
srednie
srednie.mean(axis=1)

df_example.mean() ## bez braków

np.random.seed(2025)
lm_results = mice.MICE("C ~ A", sm.OLS, df_example_imp).fit(n_burnin=5, n_imputations=m)
lm_results.summary()

smf.ols("C ~ A", df_example).fit().summary().tables[1]
smf.ols("C ~ A", df_example_miss).fit().summary().tables[1]
