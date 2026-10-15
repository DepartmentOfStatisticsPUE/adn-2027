# 1. Braki danych w pakietach statystycznych
# Kod wyodrębniony z notatnika codes/qmd/1-problematyka-brakow-danych.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Braki danych w pakietach statystycznych ----

## Kodowanie braków danych ----
x1 <- c(1,2,3,NA)
summary(x1)

table(x1)

table(x1, useNA = "ifany")

mean(x1)

mean(x1, na.rm = T)

na.omit(x1)

x2 <- c(1,2,3, NA, NaN)

summary(x2)

mean(x2, na.rm=T)

table(x2)
table(x2, useNA = "ifany")

na.omit(x2)

## Praca z brakami danych ----

### Dane wczytywane z plików ----
dane <- read.csv("data/plik-przyklad.csv")
head(dane)

tail(dane)

# [w notatniku nie uruchamiane (eval = FALSE)]
# with(dane, cor(wzrost, ocena))

### Dane ankietowe ----
library(haven)

## źródło: https://www.parp.gov.pl/images/publications/BKL/nowy-uklad/Baza_danych_z_badania_ludnoci_BKL_edycja_2021_SAV-SPSS.sav
## (strona blokuje pobieranie z poziomu R, dlatego wczytujemy kopię lokalną)
doc <- read_spss("data/downloaded_data.sav")
str(doc$m9_1,2)

table(doc$m9_1)
table(doc$m9_1, useNA = "ifany")

doc <- read_spss("data/downloaded_data.sav", user_na = T)
str(doc$m9_1,2)

table(doc$m9_1)
table(doc$m9_1, useNA = "ifany")
