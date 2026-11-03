# Analiza danych niekompletnych 2026/27

Repozytorium na potrzeby zajęć z przedmiotu „Analiza danych niekompletnych” (Uniwersytet Ekonomiczny w Poznaniu, Katedra Statystyki).

## Podstawowe informacje

-   Materiały: GitHub, Moodle
-   Zaliczenie: projekt przez Kaggle
-   Sylabus: [stacjonarni](https://esylabus.ue.poznan.pl/pl/document/fbb48377-9db7-4bbc-8d72-de1eb839a0a1.pdf) | [niestacjonarni](https://esylabus.ue.poznan.pl/pl/document/5aa99be4-4418-4e73-ba48-76b8474734e6.pdf)
-   [Slajdy (Overleaf)](https://www.overleaf.com/read/cndnkcyqrjjx#42c1d9)

## Interaktywne materiały

Podsumowania w formie stron przewijanych: przykłady krok po kroku, narzędzia do samodzielnego sprawdzenia i kod w R i Pythonie. Między krokami można przechodzić strzałkami ← →.

| # | Temat | Strona | Co zawiera |
|---|-------|--------|------------|
| 3a | Imputacja dedukcyjna z ograniczeniami liniowymi | [otwórz](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/wizualizacje/3a-imputacja-dedukcyjna-ograniczenia.html) | zapis $Ax = b$, trzy przypadki rozwiązań, pseudoodwrotność, zadanie z 10 zmiennymi, narzędzie do własnych reguł, quiz |
| 3b | Imputacja dedukcyjna z tekstu i innych zmiennych | [otwórz](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/wizualizacje/3b-imputacja-dedukcyjna-tekst.html) | wyrażenia regularne, kody TERYT i PESEL, reguły z definicji, porządek pliku, modele językowe |
| 4a | Imputacja hot-deck | [otwórz](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/wizualizacje/4a-imputacja-hotdeck.html) | warianty hot-decku, niejawny model, rozkład średniej, tworzenie klas imputacyjnych, symulacje |
| -- | Wizualizacja imputacji danych (Shiny) | [otwórz](https://berenz.shinyapps.io/missing-data-class1/) | aplikacja Shiny |

## Notatniki z kodami

| # | Temat | HTML | QMD | R | Python | Dane |
|---|-------|------|-----|---|--------|------|
| 0 | Problematyka braków danych | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/0-kody-do-slajdow.html) | [qmd](codes/qmd/0-kody-do-slajdow.qmd) | [.R](codes/R/0-kody-do-slajdow.R) | [.py](codes/python/0-kody-do-slajdow.py) | -- |
| 1 | Kodowanie braków danych w pakietach statystycznych | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/1-problematyka-brakow-danych.html) | [qmd](codes/qmd/1-problematyka-brakow-danych.qmd) | [.R](codes/R/1-problematyka-brakow-danych.R) | [.py](codes/python/1-problematyka-brakow-danych.py) | [exercise2.csv](data/exercise2.csv), [BKL](https://www.parp.gov.pl/component/site/site/bilans-kapitalu-ludzkiego) ([kwestionariusz](https://www.parp.gov.pl/images/publications/BKL/Kwestionariusz_z_badania_ludnoci_BKL_edycja_2021_1.docx)) |
| 2 | Wizualizacja braków danych | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/2-wizualizacja-brakow.html) | [qmd](codes/qmd/2-wizualizacja-brakow.qmd) | [.R](codes/R/2-wizualizacja-brakow.R) | [.py](codes/python/2-wizualizacja-brakow.py) | [przekrojowe](data/data2-cross_sectional.csv), [panel long](data/data2-panel_long.csv), [panel wide](data/data2-panel_wide.csv), [ćwiczenie](data/data2-zajecia-przyklad1.csv) |
| 3a | Imputacja dedukcyjna z ograniczeniami liniowymi | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/3a-imputacja-dedukcyjna-ograniczenia.html) | [qmd](codes/qmd/3a-imputacja-dedukcyjna-ograniczenia.qmd) | [.R](codes/R/3a-imputacja-dedukcyjna-ograniczenia.R) | [.py](codes/python/3a-imputacja-dedukcyjna-ograniczenia.py) | -- |
| 3b | Imputacja dedukcyjna na podstawie danych tekstowych | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/3b-imputacja-dedukcyjna-tekst.html) | [qmd](codes/qmd/3b-imputacja-dedukcyjna-tekst.qmd) | [.R](codes/R/3b-imputacja-dedukcyjna-tekst.R) | [.py](codes/python/3b-imputacja-dedukcyjna-tekst.py) | [data3-przyklad-imputacji.csv](data/data3-przyklad-imputacji.csv) |
| 4a | Imputacja hot-deck | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/4a-imputacja-hotdeck.html) | [qmd](codes/qmd/4a-imputacja-hotdeck.qmd) | [.R](codes/R/4a-imputacja-hotdeck.R), [symulacja klas](codes/R/4a-hotdeck-klasy-symulacja.R) | [.py](codes/python/4a-imputacja-hotdeck.py) | [data4-czytelnictwo.csv](data/data4-czytelnictwo.csv) |
| 4b | Imputacja metodą najbliższego sąsiada | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/4b-imputacja-nn.html) | [qmd](codes/qmd/4b-imputacja-nn.qmd) | [.R](codes/R/4b-imputacja-nn.R) | [.py](codes/python/4b-imputacja-nn.py) | [data4-czytelnictwo.csv](data/data4-czytelnictwo.csv) |
| 5 | Imputacja regresyjna | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/5-imputacja-reg.html) | [qmd](codes/qmd/5-imputacja-reg.qmd) | [.R](codes/R/5-imputacja-reg.R) | [.py](codes/python/5-imputacja-reg.py) | -- |
| 6 | Predykcyjne dopasowanie średnich (PMM) | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/6-imputacja-pmm.html) | [qmd](codes/qmd/6-imputacja-pmm.qmd) | [.R](codes/R/6-imputacja-pmm.R) | [.py](codes/python/6-imputacja-pmm.py) | [data4-czytelnictwo.csv](data/data4-czytelnictwo.csv) |
| 7 | Imputacja wielokrotna | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/7-imputacja-mi.html) | [qmd](codes/qmd/7-imputacja-mi.qmd) | [.R](codes/R/7-imputacja-mi.R) | [.py](codes/python/7-imputacja-mi.py) | -- |
| 8 | Case study: imputacja | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/8-case-study.html) | [qmd](codes/qmd/8-case-study.qmd) | [.R](codes/R/8-case-study.R) | [.py](codes/python/8-case-study.py) | [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx) |
| 9 | Wstęp do kalibracji | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/9-kalibracja-wstep.html) | [qmd](codes/qmd/9-kalibracja-wstep.qmd) | [.R](codes/R/9-kalibracja-wstep.R) | [.py](codes/python/9-kalibracja-wstep.py) | [data5-kalibracja.csv](data/data5-kalibracja.csv) |
| 10 | Kalibracja (bardziej zaawansowana) | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/10-kalibracja-case-study.html) | [qmd](codes/qmd/10-kalibracja-case-study.qmd) | [.R](codes/R/10-kalibracja-case-study.R) | [.py](codes/python/10-kalibracja-case-study.py) | [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx) |
| 11 | Ważenie przez odwrotność prawdopodobieństwa odpowiedzi (PSW) | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/11-propensity-score.html) | [qmd](codes/qmd/11-propensity-score.qmd) | [.R](codes/R/11-propensity-score.R) | [.py](codes/python/11-propensity-score.py) | [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx) |
| -- | Estymacja wariancji (notatnik z 2025) | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2025/refs/heads/main/codes/10-estymacja-wariancji.html) | -- | -- | -- | [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx) |
| 12 | Case study: podsumowanie (BKL) | [html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/qmd/12-case-study-podsumowanie.html) | [qmd](codes/qmd/12-case-study-podsumowanie.qmd) | [.R](codes/R/12-case-study-podsumowanie.R) | -- | [BKL 2021 (.sav)](https://www.parp.gov.pl/images/publications/BKL/nowy-uklad/Baza_danych_z_badania_ludnoci_BKL_edycja_2021_SAV-SPSS.sav) |

Kody generujące przykłady mechanizmów braków (z edycji 2025): [R](https://github.com/DepartmentOfStatisticsPUE/adn-2025/blob/main/codes/script-01-gen-mechanisms.R) | [Python](https://github.com/DepartmentOfStatisticsPUE/adn-2025/blob/main/codes/script-01-gen-mechanisms.py). Zadania do case study (12) są na slajdach w Overleaf.

## Pakiety

| # | Temat | R | Python |
|---|-------|---|--------|
| 0 | Problematyka braków danych | `rnorm`, `plogis`, `density` | `numpy.random`, `gaussian_kde` |
| 1 | Kodowanie braków danych | `NA`, `NA_integer_`, `NA_character_`, `is.na`, `Inf`, `NaN` | `np.nan`, `pd.NA`, `pd.NaT`, `isna`, `isnull` |
| 2 | Wizualizacja braków danych | `VIM`, `naniar`, `panelView` | `missingno`, `upsetty`, `missmecha` |
| 3a | Imputacja dedukcyjna: ograniczenia liniowe | `MASS::ginv`, `validate`, `deductive` | `numpy.linalg.pinv`, `sympy` |
| 3b | Imputacja dedukcyjna: dane tekstowe | `zoo::na.locf`, `tidyr::fill`, `data.table::nafill`, `stringr`, `ellmer` | `pandas` (`ffill`, `str.extract`), `re` |
| 4a | Hot-deck | `simputation`, `VIM` | `numpy`, `pandas` (własna implementacja) |
| 4b | Najbliższy sąsiad | `simputation`, `VIM` | `KNNImputer` z `sklearn.impute` |
| 6 | PMM | `simputation`, `FNN` | `sklearn.linear_model`, `sklearn.neighbors` |
| 7 | Imputacja wielokrotna | [`mice`](https://github.com/amices/mice), [`rMIDAS`](https://cran.r-project.org/web/packages/rMIDAS/index.html) | `IterativeImputer` z `sklearn.impute`, [`MIDASpy`](https://github.com/MIDASverse/MIDASpy) |
| 9–10 | Kalibracja | `survey`, `sampling`, `laeken` | [`svy`](https://svylab.com/docs/svy) |
| 11 | PSW | `stats`, `glmnet` | -- |
| -- | Estymacja wariancji | `boot` | -- |
