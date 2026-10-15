# 6. Kalibracja -- wstęp
# Kod wyodrębniony z notatnika codes/qmd/9-kalibracja-wstep.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(survey)
library(sampling)

# Rozwiązanie przykładu 1 ----

## Podejście krok po kroku ----
dane <- read.csv2("data/data5-kalibracja.csv")
head(dane)

wynik_poprawny <- c(52.275, 50.5821, 51.4286, 50.5462, 48.4301, 39.9657, 51.0054, 54.3911, 45.4675, 49.7357, 52.275, 51.4286, 45.0443, 51.0054, 51.0054, 48.8893, 52.275, 52.275, 50.5462, 51.4286)

d <- dane$Waga

Xs <- model.matrix(~0+Przychod + Wielkosc, dane)
head(Xs)

wartosci_globalne <- c(19000, 280, 720)

wartosci_est <- colSums(Xs*d)
wartosci_est

n_wierszy <- NROW(dane)

macierz_sum <- matrix(0, 3, 3)

for (i in 1:n_wierszy) {
  macierz_sum <- macierz_sum + d[i]*Xs[i,]%*% t(Xs[i, ])
}

w1 <- numeric(n_wierszy)
for (i in 1:n_wierszy) {
  w1[i] <- d[i] + d[i]*t(wartosci_globalne - wartosci_est) %*% solve(macierz_sum) %*% Xs[i, ]
}

all.equal(round(w1,3),  round(wynik_poprawny,3))

## Sposób 2: obliczenia macierzowe ----
w2 <- d + d * t(wartosci_globalne - wartosci_est) %*% solve(t(d*Xs) %*% Xs) %*% t(Xs)
w2 <- as.numeric(w2)

all.equal(round(w2,3),  round(wynik_poprawny,3))

## Sposób 3: Wykorzystanie dostępnych pakietów ----
wskaznik <- calib(Xs = Xs, 
                  d=dane$Waga, 
                  method = "linear", 
                  total = wartosci_globalne)
w2 <- dane$Waga*wskaznik

all.equal(round(w2,3),  round(wynik_poprawny,3))
