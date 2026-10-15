# 7. Propensity score adjustment
# Kod wyodrębniony z notatnika codes/qmd/11-propensity-score.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
import statsmodels.api as sm
import matplotlib.pyplot as plt

# %% # Ważenie przez odwrotność -- metoda podstawowa
gosp = pd.read_excel("data/gospodarstwa-zajecia.xlsx")
gosp['klm'] = gosp['klm'].astype('category')
gosp['woj'] = gosp['woj'].astype('category')
gosp.head()

gosp[['dochg', 'wydg']].describe()

gosp['R'] = gosp['dochg'].notna()

X = pd.get_dummies(gosp[['klm', 'woj']], drop_first=True, dtype=float)
X = sm.add_constant(X)
m1 = sm.GLM(gosp['R'].astype(int), X, family=sm.families.Binomial()).fit()
pd.Series(m1.predict(X)).describe()

gosp['w_rho'] = 1 / m1.predict(X)

mean_unweighted = gosp['dochg'].mean()
mean_weighted = np.average(gosp.loc[gosp['dochg'].notna(), 'dochg'], 
                           weights=gosp.loc[gosp['dochg'].notna(), 'w_rho'])
[mean_unweighted, mean_weighted]

X_lasso = pd.get_dummies(gosp[['klm', 'woj']], drop_first=True, dtype=float)
m2 = LogisticRegressionCV(l1_ratios=(1,), solver='saga', cv=10, max_iter=10000, random_state=2026,
                          scoring='neg_log_loss', use_legacy_attributes=False)
m2.fit(X_lasso, gosp['R'].astype(int))
gosp['w_rho_lasso'] = 1 / m2.predict_proba(X_lasso)[:, 1]
# Intercept
m2.intercept_
# Coefficients
dict(zip(X_lasso.columns, m2.coef_[0]))

mean_bez = gosp['dochg'].mean()
mean_glm = np.average(gosp.loc[gosp['dochg'].notna(), 'dochg'], 
                      weights=gosp.loc[gosp['dochg'].notna(), 'w_rho'])
mean_lasso = np.average(gosp.loc[gosp['dochg'].notna(), 'dochg'], 
                        weights=gosp.loc[gosp['dochg'].notna(), 'w_rho_lasso'])

{'bez': mean_bez, 'glm': mean_glm, 'lasso': mean_lasso}

gosp[['w_rho', 'w_rho_lasso']].describe()

plt.scatter(gosp['w_rho'], gosp['w_rho_lasso'])
plt.xlabel('w_rho')
plt.ylabel('w_rho_lasso')
plt.show()
