# 1. Problematyka braków danych
# Kod wyodrębniony z notatnika codes/qmd/2-wizualizacja-brakow.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebych pakietów
import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
from upsetty import Upset
# pip install missmecha-py ipython  (missmecha wymaga IPython przy imporcie)
from missmecha.visual import plot_missing_matrix, plot_missing_heatmap

# %% # Przykład 1: dane przekrojowe
df_cross = pd.read_csv("data/data2-cross_sectional.csv")
df_cross.head()

miss_plot = msno.matrix(df_cross)
plt.show()
plt.ioff()

miss_dendro = msno.dendrogram(df_cross)
plt.show()

upset = Upset.generate_plot(df_cross.isnull())
upset.show()

# %% # Przykład 1: missmecha
# funkcje z missmecha same wywołują plt.show()
plot_missing_matrix(df_cross)               # obserwowane wartości kolorowane wg wielkości, na dole % braków
plot_missing_matrix(df_cross, sort_by="y")  # sortowanie wg y -- czy braki zależą od y?
plot_missing_heatmap(df_cross, figsize=(8, 6))  # korelacje wskaźników braków

# %% # Przykład 2: dane panelowe
df_long = pd.read_csv("data/data2-panel_long.csv")
df_long.head()

df_wide = pd.read_csv("data/data2-panel_wide.csv")
df_wide.head()

missing_pattern = df_long.pivot(index='unit_id', columns='year', values='y').isnull()
plt.figure(figsize=(12, 8))
sns.heatmap(missing_pattern, cbar=True, cmap='binary')
plt.title('Panel View of Missing Data')
plt.show()

# missmecha: dane szerokie, jednostki na osi y (ts=True)
plot_missing_matrix(df_wide.set_index('unit_id'), color=False, ts=True, fontsize=10)
