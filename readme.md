# Repozytorium na potrzeby zajęć z przedmitu "Analiza danych niekompletnych"

## Podstawowe informacje

+ Materiały: github, moodle
+ Zaliczenie: projekt przez Kaggle
+ [Sylabus - stacjonarni](https://esylabus.ue.poznan.pl/pl/document/fbb48377-9db7-4bbc-8d72-de1eb839a0a1.pdf)
+ [Sylabus - niestacjonarni](https://esylabus.ue.poznan.pl/pl/document/5aa99be4-4418-4e73-ba48-76b8474734e6.pdf)
+ [Slajdy](https://www.overleaf.com/read/cndnkcyqrjjx#42c1d9)
+ Shiny:
  + [Wizualizacja imputacji danych 1](https://berenz.shinyapps.io/missing-data-class1/)

+ Zaliczenie:

## Materiały na zajęcia

### 1. Problematyka braków danych

  + przydatne procedury:
    + R: `rnorm`, `plogis`, `density`, ...
    + Python: `np.random...`,  `gaussian_kde`, ...
  + [kody do generowania braków danych](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/0-kody-do-slajdow.html)

### 2. Kodowanie braków danych w pakietatch statystycznych:
  + R: `NA`, `NA_integer_`, `NA_character_`, `is.na`, `Inf`, `NaN`
  + Python: `np.nan`, `pd.NA`, `pd.NaT`, `isna`, `isnull`
  + [kody na zajecia](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/1-problematyka-brakow-danych.html)
  + Zbiory danych na potrzeby zajęć:
    + `csv`
    + `sav` -- [Bilans Kapitału Ludzkiego](https://www.parp.gov.pl/component/site/site/bilans-kapitalu-ludzkiego) -- [zbiór](), [kwestionariusz](https://www.parp.gov.pl/images/publications/BKL/Kwestionariusz_z_badania_ludnoci_BKL_edycja_2021_1.docx)

### 3. Metody wizualizacji braków danych
  + narzędzia:
    + R: `VIM`, `naniar`, `panelView`
    + Python: `missingno`, `upsetty`
  + Kody generujące przykłady: [R](https://github.com/DepartmentOfStatisticsPUE/adn-2025/blob/main/codes/script-01-gen-mechanisms.R), [Python](https://github.com/DepartmentOfStatisticsPUE/adn-2025/blob/main/codes/script-01-gen-mechanisms.py)
  + Zbiory danych na zajęcia: [dane przekrojowe](data/data2-cross_sectional.csv), [dane panelowe (long)](data/data2-panel_long.csv), [dane panelowe (wide)](data/data2-panel_wide.csv)
  + Zbiór danych na ćwiczenia [data2-zajecia-przyklad1.csv](data/data2-zajecia-przyklad1.csv)
  + Notatnik na zajęcia: [Wizualizacja braków danych](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/2-wizualizacja-brakow.html)
  
### 4. Imputacja danych

+ Imputacja dedukcyjna:
    + R: `zoo::na.locf`, `tidyr::fill`, `data.table::nafill`, `validate`, `deductive`
    + Python: `fillna` z `pandas`
    + Zbiór danych na ćwiczenia [data3-zajecia-przyklad1.csv](data/data3-przyklad-imputacji.csv)
    + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/3-imputacja-dedukcyjna.html)

+ Imputacja metodą najbliższego sąsiada:
    + R: `simputation`, `VIM`
    + Python: `KNNImputer` z `sklearn.impute`
    + Zbiór danych na ćwiczenia [data4-czytelnictwo.csv](data/data4-czytelnictwo.csv)
    + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/4-imputacja-nn.html)
    
+ Imputacja metodą predykcyjnego dopasowania średnich (ang. *predictive mean matching*)
  + R: `simputation`, `FNN`
  + Python: `sklearn.linear_model`, `sklearn.neighbors`
  + Zbiór danych na ćwiczenia [data4-czytelnictwo.csv](data/data4-czytelnictwo.csv)
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/5-imputacja-pmm.html)

+ Imputacja wielokrotna
  + R: [`mice`](https://github.com/amices/mice), [`rMIDAS`](https://cran.r-project.org/web/packages/rMIDAS/index.html)
  + Python: `IterativeImputer` (from `sklearn.impute`), [`MIDASpy`](https://github.com/MIDASverse/MIDASpy)
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/6-imputacja-mi.html)

+ Imputacja regresyjna
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/7-imputacja-reg.html)

### 5. Case study

+ [opis](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/8-case-study.html)
+ [zbior](./data/gospodarstwa-zajecia.xlsx)
 
### 6. Kalibracja

+ Wstęp do kalibracji
  + R: `survey`, `sampling`, `laeken`
  + Python: [`svy`](https://svylab.com/docs/svy)
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/9-kalibracja-wstep.html)
  + Dane na zajęcia [data5-kalibracja.csv](data/data5-kalibracja.csv)

+ Kalibracja (bardziej zaawansowana)
  + R: `survey`
  + Python: [`svy`](https://svylab.com/docs/svy)
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/10-kalibracja-case-study.html)
  + Dane na zajęcia [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx)
  

### 7. Ważenie przez odwrotność prawdopodobieństwa odpowiedzi

+ PSW
  + R: `stats`, `glmnet`
  + Python: TBA
  + [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2027/refs/heads/main/codes/11-propensity-score.html)
  + Dane na zajęcia [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx)
  

### 8. Estymacja wariancji

+ R: `boot`
+ Python: TBA
+ [Notatnik](https://htmlpreview.github.io/?https://raw.githubusercontent.com/DepartmentOfStatisticsPUE/adn-2025/refs/heads/main/codes/10-estymacja-wariancji.html)
+ Dane na zajęcia [gospodarstwa-zajecia.xlsx](data/gospodarstwa-zajecia.xlsx)

### 9. Case study

+ [dane z Badania Kapitału Ludzkiego](https://www.parp.gov.pl/images/publications/BKL/nowy-uklad/Baza_danych_z_badania_ludnoci_BKL_edycja_2021_SAV-SPSS.sav)
+ zadania do wykonania: slajdy do zajęć na Overleaf.
