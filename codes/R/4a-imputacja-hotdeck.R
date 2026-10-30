# 3a. Imputacja hot-deck
# Kod wyodrębniony z notatnika codes/qmd/4a-imputacja-hotdeck.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(simputation)
library(VIM)

# Przykład 1 z zajęć ----
przyklad1 <- data.frame(plec = c("K", "K", "K", "K", "M", "M", "M", "M"),
                        X = c(21, 24, 30, 35, 22, 28, 33, 40),
                        Y = c(25, NA, 35, NA, 45, NA, 55, 65))
przyklad1

set.seed(2025)
przyklad1 |>
  impute_rhd(Y ~ 1)

set.seed(2025)
przyklad1 |>
  impute_rhd(Y ~ plec)

set.seed(2025)
przyklad1_wynik <- przyklad1
for (klasa in unique(przyklad1$plec)) {
  ## biorcy i dawcy z danej klasy
  biorcy <- which(przyklad1$plec == klasa & is.na(przyklad1$Y))
  dawcy <- which(przyklad1$plec == klasa & !is.na(przyklad1$Y))
  ## losujemy dawców ze zwracaniem i przepisujemy ich wartości
  wybrani <- dawcy[sample.int(length(dawcy), length(biorcy), replace = TRUE)]
  przyklad1_wynik$Y[biorcy] <- przyklad1$Y[wybrani]
}
przyklad1_wynik

przyklad1 |>
  impute_shd(Y ~ X)

przyklad1 |>
  impute_shd(Y ~ X | plec)

VIM::hotdeck(przyklad1, variable = "Y", ord_var = "X", domain_var = "plec")

# Przykład 2 -- czytelnictwo ----
## reading
data <- read.csv(file = "data/data4-czytelnictwo.csv",
                 colClasses = c("factor", "numeric", "factor", "logical", "logical"))
data$wiek_kat <- cut(data$wiek, breaks = c(17, 29, 39, 49, 59, 80))
head(data)

with(data[!is.na(data$czyta_ksiazki_z_brakami), ], table(plec, wyksztalcenie))

dawcy_klasy <- with(data[!is.na(data$czyta_ksiazki_z_brakami), ],
                    table(plec, wyksztalcenie, wiek_kat))
sum(dawcy_klasy == 0)

set.seed(2025)
wynik <- data |>
  impute_rhd(czyta_ksiazki_z_brakami ~ 1)

wynik_klasy <- data |>
  impute_rhd(czyta_ksiazki_z_brakami ~ plec + wyksztalcenie)

wynik_klasy3 <- data |>
  impute_rhd(czyta_ksiazki_z_brakami ~ plec + wyksztalcenie + wiek_kat)

wynik_shd <- data |>
  impute_shd(czyta_ksiazki_z_brakami ~ wiek)

data.frame(
  metoda = c("prawda", "respondenci", "losowy", "klasy: plec, wyksztalcenie",
             "klasy: plec, wyksztalcenie, wiek", "sekwencyjny: wiek"),
  srednia = c(mean(data$czyta_ksiazki),
              mean(data$czyta_ksiazki_z_brakami, na.rm = TRUE),
              mean(wynik$czyta_ksiazki_z_brakami),
              mean(wynik_klasy$czyta_ksiazki_z_brakami),
              mean(wynik_klasy3$czyta_ksiazki_z_brakami, na.rm = TRUE),
              mean(wynik_shd$czyta_ksiazki_z_brakami)),
  braki = c(0,
            sum(is.na(data$czyta_ksiazki_z_brakami)),
            sum(is.na(wynik$czyta_ksiazki_z_brakami)),
            sum(is.na(wynik_klasy$czyta_ksiazki_z_brakami)),
            sum(is.na(wynik_klasy3$czyta_ksiazki_z_brakami)),
            sum(is.na(wynik_shd$czyta_ksiazki_z_brakami)))
)

# Symulacja ----
# Ustawienie ziarna losowości dla reprodukowalności
set.seed(123)

# Parametry symulacji
N <- 50000  # rozmiar populacji
n <- 1000    # rozmiar próby

# Generowanie zmiennych objaśniających
x1 <- runif(N, 0, 1)
x2 <- runif(N, 0, 1)
e <- rnorm(N, 0, 1)

# Generowanie zmiennej y dla dwóch modeli
y1 <- -1 + x1 + x2 + e
y2 <- -1.167 + x1 + x2 + (x1-0.5)^2 + (x2-0.5)^2 + e

# Tworzenie wskaźnika odpowiedzi (mechanizm braków danych)
logit_p <- 0.2 + x1 + x2
p <- exp(logit_p)/(1 + exp(logit_p))

# Tworzenie ramki danych
populacja <- data.frame(
 id = 1:N,
 x1 = x1,
 x2 = x2,
 y1 = y1,
 y2 = y2,
 p = p,
 ## klasy imputacyjne
 klasa = interaction(cut(x1, breaks = seq(0, 1, 0.25)), cut(x2, breaks = seq(0, 1, 0.25)))
)
y_true <- colMeans(populacja[, c("y1", "y2")])

## imputacja średnią w klasach
impute_srednia <- function(proba, y) {
  srednie <- ave(proba[[y]], proba$klasa, FUN = function(v) mean(v, na.rm = TRUE))
  ifelse(is.na(proba[[y]]), srednie, proba[[y]])
}

## symulacja (2000 razy)
R <- 2000
results <- matrix(0, R, 10)
colnames(results) <- paste0(rep(c("naive", "hd", "hd_kl", "sr_kl", "shd"), each = 2),
                            rep(c("_y1", "_y2"), times = 5))

for (r in 1:R) {
  proba <- populacja[sample(1:N, n), ]
  proba$delta <- rbinom(nrow(proba), 1, proba$p)
  proba$y1[proba$delta == 0] <- NA
  proba$y2[proba$delta == 0] <- NA

  results[r, 1:2] <- colMeans(proba[, c("y1", "y2")], na.rm = TRUE)
  results[r, 3:4] <- colMeans(impute_rhd(proba, y1 + y2 ~ 1, pool = "univariate")[, c("y1", "y2")])
  results[r, 5:6] <- colMeans(impute_rhd(proba, y1 + y2 ~ klasa, pool = "univariate")[, c("y1", "y2")])
  results[r, 7:8] <- c(mean(impute_srednia(proba, "y1")), mean(impute_srednia(proba, "y2")))
  results[r, 9:10] <- colMeans(impute_shd(proba, y1 + y2 ~ x1, pool = "univariate")[, c("y1", "y2")])
}

boxplot(results - matrix(rep(y_true, times = 5), byrow = TRUE, ncol = 10, nrow = R),
        xlab = "", ylab = "Obciążenie",
        main = "Hot-deck: bez klas, w klasach, sekwencyjny i średnia w klasach",
        las = 2)
abline(a = 0, b = 0, col = "red")

bias <- colMeans(results) - rep(y_true, times = 5)
round(bias*100, 2)

round(apply(results, 2, var)*100, 4)

round(sqrt(bias^2 + apply(results, 2, var))*100, 2)

set.seed(2025)
proba <- populacja[sample(1:N, n), ]
y1_pelne <- proba$y1
proba$y1[rbinom(n, 1, proba$p) == 0] <- NA

round(c(prawda = sd(y1_pelne),
        respondenci = sd(proba$y1, na.rm = TRUE),
        hd_kl = sd(impute_rhd(proba, y1 ~ klasa)$y1),
        sr_kl = sd(impute_srednia(proba, "y1"))), 3)
