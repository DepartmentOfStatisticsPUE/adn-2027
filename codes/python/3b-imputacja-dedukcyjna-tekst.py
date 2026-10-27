# 2b. Imputacja dedukcyjna na podstawie danych tekstowych
# Kod wyodrębniony z notatnika codes/qmd/3b-imputacja-dedukcyjna-tekst.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import pandas as pd
import re

# %% # Przykład imputacji dedukcyjnej
dane = pd.read_csv("data/data3-przyklad-imputacji.csv")
dane.head()

dane.assign(liczba_pokoi=dane['liczba_pokoi'].ffill())

dane['liczba_pokoi'].ffill()

"1465011"[:2]  # pierwsze 2 znaki

tekst = "Przytulna kawalerka 32,1m2, 1 pokój w centrum!"
pattern = r'\d{2},\d{1}'
match = re.search(pattern, tekst)
if match:
    print(match.group())

s = pd.Series(["Przytulna kawalerka 32,1m2, 1 pokój w centrum!"])
s.str.extract(r'(\d{2},\d{1})')
