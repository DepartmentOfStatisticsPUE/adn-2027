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
