# 1. Problematyka braków danych
# Kod wyodrębniony z notatnika codes/qmd/0-kody-do-slajdow.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wizualizacja braków danych
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from tabulate import tabulate
from scipy.stats import gaussian_kde

# Ustawiamy ziarno losowości dla powtarzalności wyników
np.random.seed(123)

# Generowanie danych
n = 1000  # liczba obserwacji
x = np.random.normal(loc=50, scale=10, size=n)  # X z rozkładu normalnego
y = 5 * x + np.random.normal(loc=0, scale=20, size=n)  # Wzmocniona zależność Y od X

# Funkcja do generowania braków danych
def generate_missing(y, x, mechanism, prob=0.3):
    n = len(y)
    missing = np.full(n, False)
    
    if mechanism == "MCAR":
        missing = np.random.random(n) < prob
    elif mechanism == "MAR":
        prob_missing = stats.logistic.cdf(2 * stats.zscore(x))  # Prawdopodobieństwo braku zależy od X
        missing = np.random.random(n) < prob_missing
    elif mechanism == "NMAR":
        prob_missing = stats.logistic.cdf(2 * stats.zscore(y))  # Prawdopodobieństwo braku zależy od Y
        missing = np.random.random(n) < prob_missing
    
    y_missing = y.copy()
    y_missing[missing] = np.nan
    return y_missing

# Generowanie braków danych dla każdego mechanizmu
y_mcar = generate_missing(y, x, "MCAR")
y_mar = generate_missing(y, x, "MAR")
y_nmar = generate_missing(y, x, "NMAR")

# Funkcja do tworzenia wykresu porównawczego rozkładów gęstości
def plot_density_comparison(y_full, y_obs, title, ax):
    kde_full = gaussian_kde(y_full)
    kde_obs = gaussian_kde(y_obs[~np.isnan(y_obs)])
    
    x_range = np.linspace(min(y_full), max(y_full), 100)
    
    ax.plot(x_range, kde_full(x_range), color="blue", label="Pełne dane")
    ax.plot(x_range, kde_obs(x_range), color="red", label="Obserwowane dane")
    ax.set_title(title)
    ax.set_xlabel("Y")
    ax.set_ylabel("Gęstość")
    ax.legend(loc='upper right')

# Tworzenie wykresów
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
plot_density_comparison(y, y_mcar, "MCAR", ax1)
plot_density_comparison(y, y_mar, "MAR", ax2)
plot_density_comparison(y, y_nmar, "NMAR", ax3)
plt.tight_layout()
plt.savefig("fig-missing-examples-py.pdf")
plt.close()

# Tworzenie ramki danych z wynikami
results = pd.DataFrame({
    "Statystyka": ["Procent brakujących danych", "Średnia Y", "Odchylenie standardowe Y", "Korelacja między X i Y"],
    "Pełne dane": [0, np.mean(y), np.std(y), np.corrcoef(x, y)[0, 1]],
    "MCAR": [np.mean(np.isnan(y_mcar)) * 100, np.nanmean(y_mcar), np.nanstd(y_mcar), np.corrcoef(x[~np.isnan(y_mcar)], y_mcar[~np.isnan(y_mcar)])[0, 1]],
    "MAR": [np.mean(np.isnan(y_mar)) * 100, np.nanmean(y_mar), np.nanstd(y_mar), np.corrcoef(x[~np.isnan(y_mar)], y_mar[~np.isnan(y_mar)])[0, 1]],
    "NMAR": [np.mean(np.isnan(y_nmar)) * 100, np.nanmean(y_nmar), np.nanstd(y_nmar), np.corrcoef(x[~np.isnan(y_nmar)], y_nmar[~np.isnan(y_nmar)])[0, 1]]
})

# Zaokrąglamy wszystkie wartości numeryczne do 2 miejsc po przecinku
results.iloc[:, 1:] = results.iloc[:, 1:].round(2)

# Generujemy kod LaTeX
latex_code = tabulate(results, headers='keys', tablefmt='latex_booktabs', showindex=False)

# Dodajemy nagłówek i stopkę tabeli LaTeX
latex_code = f"""
\\begin{{table}}[htbp]
\\centering
\\caption{{Porównanie statystyk dla różnych mechanizmów braków danych}}
\\label{{tab:missing-data-stats}}
{latex_code}
\\end{{table}}
"""

# Wyświetlamy kod LaTeX
print(latex_code)
