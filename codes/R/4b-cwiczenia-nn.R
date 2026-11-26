# 4b. Imputacja metodą najbliższego sąsiada -- ćwiczenia
# Pod każdym komentarzem "Zadanie" proszę napisać kod.
# Rozwiązania: codes/qmd/4b-imputacja-nn.qmd (Krok 0--5).

library(simputation)
library(VIM)

# Krok 0 -- dane i braki ----
dane <- read.csv("data/data6-wydatki.csv", stringsAsFactors = TRUE)
## wydatki jako liczby rzeczywiste (VIM::kNN() obcina średnią do liczby całkowitej)
dane$wydatki <- as.numeric(dane$wydatki)
braki <- is.na(dane$wydatki)

## obciążenie: średnia po imputacji minus średnia prawdziwa
obciazenie <- function(y) mean(y) - mean(dane$wydatki_prawda)

## Zadanie: odsetek braków, średnia prawdziwa (wydatki_prawda) i średnia z respondentów.

## Zadanie: wykresy pudełkowe dochodu i wieku według braków (boxplot(dochod ~ braki, data = dane)).

## Zadanie: imputacja średnią z respondentów i jej obciazenie().

# Krok 1 -- najbliższy sąsiad krok po kroku ----
biorca <- which(braki)[1]
dawcy <- dane[!braki, ]

## Zadanie: odległość dochodu pierwszego biorcy od dochodu każdego dawcy; najbliższy dawca (which.min).

## Zadanie: imputacja wszystkich braków: impute_knn(), k = 1, zmienna dochod; obciazenie().

# Krok 2 -- same zmienne jakościowe ----

## Zadanie: odległości Gowera pierwszego biorcy od dawców według plec, wyksztalcenie, klasa_miejsc
## (gower::gower_dist) w tabeli liczebności.

## Zadanie: impute_rhd() w klasach plec, wyksztalcenie, klasa_miejsc oraz impute_knn() z k = 1
## po tych samych zmiennych; obciazenie() i liczba różnych wstawionych wartości (length(unique(...))).

# Krok 3 -- liczba zmiennych ----

## Zadanie: impute_knn() z k = 1 dla zbiorów zmiennych:
##   dochod
##   + wiek, liczba_osob
##   + wzrost, czas_wywiadu
##   + nr_ankietera, miesiac_urodzenia
## i porównać obciazenie().

# Krok 4 -- liczba sąsiadów i korekta obciążenia ----

## Zadanie: zmienne dochod, wiek, liczba_osob; dla k = 5 i k = 31:
##   dawca losowy spośród k najbliższych -- impute_knn(),
##   średnia z k najbliższych -- kNN(..., numFun = mean).
## Porównać obciazenie().

## Zadanie: korekta obciążenia dla k = 31:
##   1. model lm(wydatki ~ dochod + wiek + liczba_osob),
##   2. reszty = wydatki - predict(model, dane) (dla biorców brak),
##   3. reszty biorców imputować średnią z 31 sąsiadów (kNN, numFun = mean),
##   4. predict(model, dane) + reszty; obciazenie().

# Krok 5 -- odległość i skalowanie zmiennych ----

## Zadanie: najbliższy sąsiad według odległości euklidesowej (FNN::get.knnx) po zmiennych dochod, wiek,
## liczba_osob: na danych surowych i po standaryzacji (scale). Porównać dawcę pierwszego biorcy
## i obciazenie() dla wszystkich braków.
