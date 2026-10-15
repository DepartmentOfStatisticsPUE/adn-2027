# 1. Braki danych w pakietach statystycznych
# Kod wyodrębniony z notatnika codes/qmd/1-problematyka-brakow-danych.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Braki danych w pakietach statystycznych

# %% ## Kodowanie braków danych
import pandas as pd
import numpy as np
import polars as pl
import pyreadstat

x1 = pd.Series([1, 2, 3, np.nan])
x1.describe()

x1.value_counts()

x1.value_counts(dropna=False)

x1.mean(skipna=False)

x1.mean()

x1.dropna()

## np.nan nie jest równy samemu sobie -- braki sprawdzamy przez isna() (alias isnull())
np.nan == np.nan

x1.isna()

## różne postaci braków danych: None, np.nan, pd.NA, pd.NaT
pd.isna(None), pd.isna(np.nan), pd.isna(pd.NA), pd.isna(pd.NaT)

## typ zmiennej a braki danych (typy nullable: Int64, boolean, string)
pd.Series([1, 2, 3, None])

pd.Series([1, 2, 3, None], dtype="Int64")

pd.Series([True, False, None])

pd.Series([True, False, None], dtype="boolean")

## pandas 3.0: domyślny typ tekstowy to str, brak zapisywany jako nan
pd.Series(["a", "b", None])

pd.to_datetime(["2024-10-01", None])

## logika trójwartościowa pd.NA (jak NA w R)
pd.NA | True, pd.NA & False, pd.NA & True

## nieskończoność nie jest brakiem danych
x3 = pd.Series([1, 2, np.inf, np.nan])
x3.isna()

x3.mean()

np.isinf(x3)

## korelacja: pandas pomija braki (pary kompletne), R zwraca NA
df_kor = pd.DataFrame({"x": [1, 2, 3, 4, np.nan], "y": [2, np.nan, 5, 4, 6]})
df_kor["x"].corr(df_kor["y"])

df_kor.dropna().shape[0]

## polars: null (brak) to nie to samo co NaN
x_pl = pl.Series([1.0, None, np.nan])
x_pl.is_null()

x_pl.is_nan()

# %% ## Praca z brakami danych

# %% ### Dane wczytywane z plików
dane = pd.read_csv(
    "data/plik-przyklad.csv",
    skip_blank_lines=True,
    on_bad_lines="skip"
)
dane.head()

dane.tail()

## jakie typy mają kolumny? dlaczego wiek, wzrost i ocena nie są liczbami?
dane.dtypes

## ile braków pandas rozpoznał domyślnie?
dane.isna().sum()

## Zadanie: jakie kody braków są w pliku? ustaw je (hint: na_values, keep_default_na)
## i sprawdź ponownie dane.dtypes -- jaki typ ma czy_pracuje? co zmienia dtype_backend="numpy_nullable"?

# [w notatniku nie uruchamiane (eval = FALSE)]
# correlation = dane["wiek"].corr(
#     dane["ocena"],
#     method="pearson"
# )


## źródło: https://www.parp.gov.pl/images/publications/BKL/nowy-uklad/Baza_danych_z_badania_ludnoci_BKL_edycja_2021_SAV-SPSS.sav
## (strona blokuje pobieranie z poziomu Pythona, dlatego wczytujemy kopię lokalną)
file_name = "data/downloaded_data.sav"

df, meta = pyreadstat.read_sav(file_name)
# Print structure of m9_1
df['m9_1'].dtype
df['m9_1'].head(2)

df['m9_1'].value_counts()
df['m9_1'].value_counts(dropna=False)

df2, meta2 = pyreadstat.read_sav(file_name, user_missing=True, usecols = ["m9_1"])
df2['m9_1'].dtype
df2['m9_1'].head(2)

df2['m9_1'].value_counts()
df2['m9_1'].value_counts(dropna=False)

## braki zdefiniowane w SPSS (user-defined missing) zapisane są w metadanych
meta2.missing_ranges["m9_1"]

meta2.variable_value_labels["m9_1"]

df['m9_1'].isna().sum(), df2['m9_1'].isna().sum()

## Zadanie: korzystając z meta2.missing_ranges zamień w df2 wartości z zakresu braków na np.nan
## i porównaj wynik value_counts(dropna=False) z df
