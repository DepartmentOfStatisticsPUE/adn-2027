# 2a. Imputacja dedukcyjna z wykorzystaniem ograniczeń liniowych
# Kod wyodrębniony z notatnika codes/qmd/3a-imputacja-dedukcyjna-ograniczenia.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(MASS)
library(validate)
library(deductive)

# Bez wykorzystania dodatkowych pakietów ----
# Znane wartości
x1 <- 100
x4 <- 40
x3 <- 150
# Definiujemy macierze dla układu równań:
# x1 + x2 = x3
# x4 + x5 = x1
# Macierz dla niewiadomych [x2, x5]
Am <- matrix(c(1, 0, 0, 1), nrow = 2, byrow = TRUE)

 # Macierz dla znanych wartości [x1, x3, x4]
Ao <- matrix(c(1, -1, 0,
               -1, 0, 1),
             nrow = 2, byrow = TRUE)

# Wektor znanych wartości
xo <- matrix(c(100, 150, 40), nrow = 3)

# Wektor wyrazów wolnych
b <- matrix(c(0, 0), nrow = 2)

# Obliczamy prawą stronę równania
b_star <- b - Ao %*% xo
# Rozwiązujemy używając pseudoodwrotności Moore-Penrose
x_m <- ginv(Am) %*% b_star
x_m

# Definiujemy macierze
Am <- matrix(c(1, -1, -1, 0), nrow = 2, byrow = TRUE)
Ao <- matrix(c(1, 2), nrow = 2, ncol = 1)
xo <- matrix(10, nrow = 1)
b <- matrix(c(0, 0), nrow = 2)
b_star <- b - Ao %*% xo
xm <- solve(Am, b_star)
xm

# Wykorzystanie odpowiednich pakietów ----
v <- validate::validator(
      x1 + x2 == x3,
      x4 + x5 == x1)
v

dat <- data.frame(x1 = 100, x2=NA_real_, x3=150, x4 = 40, x5 = NA_real_)
dat

impute_lr(dat,v)

v1 <- validate::validator(
      x1 + x2 == x3,
      x4 + x5 == x1,
      x6 + x7 == x2,
      x8 + x9 == x3)

impute_lr(data.frame(x1=80, x5=50, x8=10, x9=20,
                     x2=NA, x3=NA, x4=NA, x6=NA, x7=NA),
          v1)

v2 <- validate::validator(
      x1 + x2 == x3,
      x4 + x5 + x6 == x2,
      x7 + x8 == x1,
      x9 + x10 == x3,
      x4 + x7 == x9)

impute_lr(data.frame(x2=90, x4=30, x5=40, x7=45, x10=10 ,
                     x1=NA, x3=NA, x6=NA, x8=NA, x9=NA),
          v2)
