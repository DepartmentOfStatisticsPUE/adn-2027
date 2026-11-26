# 4b. Imputacja metodą najbliższego sąsiada
# Kod wyodrębniony z notatnika codes/qmd/4b-imputacja-nn.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(simputation)
library(VIM)

# Krok 0 -- dane i braki ----
dane <- read.csv("data/data6-wydatki.csv", stringsAsFactors = TRUE)
## wydatki jako liczby rzeczywiste (VIM::kNN() obcina średnią do liczby całkowitej)
dane$wydatki <- as.numeric(dane$wydatki)
braki <- is.na(dane$wydatki)
mean(braki)

mean(dane$wydatki_prawda)
mean(dane$wydatki, na.rm = TRUE)

par(mfrow = c(1, 2))
boxplot(dochod ~ braki, data = dane)
boxplot(wiek ~ braki, data = dane)

## obciążenie: średnia po imputacji minus średnia prawdziwa
bias <- function(y) mean(y) - mean(dane$wydatki_prawda)
bias(ifelse(braki, mean(dane$wydatki, na.rm = TRUE), dane$wydatki))

# Krok 1 -- najbliższy sąsiad krok po kroku ----
biorca <- which(braki)[1]
dawcy <- dane[!braki, ]
dane[biorca, c("dochod", "wiek", "liczba_osob", "wydatki_prawda")]

odl <- abs(dawcy$dochod - dane$dochod[biorca])
dawcy[which.min(odl), c("dochod", "wiek", "liczba_osob", "wydatki")]

imp <- impute_knn(dane, wydatki ~ dochod, k = 1)
bias(imp$wydatki)

# Krok 2 -- same zmienne jakościowe ----
klasy <- c("plec", "wyksztalcenie", "klasa_miejsc")
table(gower::gower_dist(dane[biorca, klasy], dawcy[klasy]))

set.seed(2025)
imp_hd <- impute_rhd(dane, wydatki ~ plec + wyksztalcenie + klasa_miejsc)
imp_nn <- impute_knn(dane, wydatki ~ plec + wyksztalcenie + klasa_miejsc, k = 1)
bias(imp_hd$wydatki)
bias(imp_nn$wydatki)
length(unique(imp_hd$wydatki[braki]))
length(unique(imp_nn$wydatki[braki]))

# Krok 3 -- liczba zmiennych ----
imp1 <- impute_knn(dane, wydatki ~ dochod, k = 1)
imp2 <- impute_knn(dane, wydatki ~ dochod + wiek + liczba_osob, k = 1)
imp3 <- impute_knn(dane, wydatki ~ dochod + wiek + liczba_osob + wzrost + czas_wywiadu, k = 1)
imp4 <- impute_knn(dane, wydatki ~ dochod + wiek + liczba_osob + wzrost + czas_wywiadu +
                     nr_ankietera + miesiac_urodzenia, k = 1)
c(bias(imp1$wydatki), bias(imp2$wydatki), bias(imp3$wydatki), bias(imp4$wydatki))

# Krok 4 -- liczba sąsiadów i korekta obciążenia ----
xs <- c("dochod", "wiek", "liczba_osob")
set.seed(2025)
## dawca losowany spośród k najbliższych
imp_los5 <- impute_knn(dane, wydatki ~ dochod + wiek + liczba_osob, k = 5)
imp_los31 <- impute_knn(dane, wydatki ~ dochod + wiek + liczba_osob, k = 31)
## średnia z k najbliższych
imp_sr5 <- kNN(dane, variable = "wydatki", dist_var = xs, k = 5, numFun = mean)
imp_sr31 <- kNN(dane, variable = "wydatki", dist_var = xs, k = 31, numFun = mean)
c(bias(imp_los5$wydatki), bias(imp_los31$wydatki),
  bias(imp_sr5$wydatki), bias(imp_sr31$wydatki))

## korekta obciążenia: wartość teoretyczna z modelu + średnia reszt k najbliższych dawców
model <- lm(wydatki ~ dochod + wiek + liczba_osob, data = dane)
dane$reszta <- dane$wydatki - predict(model, dane)    # dla biorców reszta to brak
imp_r <- kNN(dane, variable = "reszta", dist_var = xs, k = 31, numFun = mean)
bias(predict(model, dane) + imp_r$reszta)

# Krok 5 -- odległość i skalowanie zmiennych ----
X <- dane[, xs]
X_std <- scale(X)
nn_sur <- FNN::get.knnx(X[!braki, ], X[braki, ], k = 1)$nn.index
nn_std <- FNN::get.knnx(X_std[!braki, ], X_std[braki, ], k = 1)$nn.index
## najbliższy dawca pierwszego biorcy
dane[biorca, xs]
dawcy[nn_sur[1], xs]
dawcy[nn_std[1], xs]

imp_sur <- imp_std <- dane$wydatki
imp_sur[braki] <- dawcy$wydatki[nn_sur]
imp_std[braki] <- dawcy$wydatki[nn_std]
bias(imp_sur)
bias(imp_std)

# Przykład 1 -- symulacja ----
# Ustawienie ziarna losowości dla reprodukowalności
set.seed(123)

# Parametry symulacji
N <- 50000  # rozmiar populacji
n <- 1000    # rozmiar próby

# Generowanie zmiennych objaśniających
x1 <- runif(N, 0, 1)
x2 <- runif(N, 0, 1)
x3 <- runif(N, 0, 1)
x4 <- rnorm(N, 0, 1)
x5 <- rnorm(N, 0, 1)
x6 <- rnorm(N, 0, 1)
e <- rnorm(N, 0, 1)

# Generowanie zmiennej y dla trzech modeli
y1 <- -1 + x1 + x2 + e
y2 <- -1.167 + x1 + x2 + (x1-0.5)^2 + (x2-0.5)^2 + e
y3 <- -1.5 + x1 + x2 + x3 + x4 + x5 + x6 + e

# Tworzenie wskaźnika odpowiedzi (mechanizm braków danych)
logit_p <- 0.2 + x1 + x2
p <- exp(logit_p)/(1 + exp(logit_p))

# Tworzenie ramki danych
populacja <- data.frame(
 id = 1:N,
 x1 = x1,
 x2 = x2,
 x3 = x3,
 x4 = x4,
 x5 = x5,
 x6 = x6,
 y1 = y1,
 y2 = y2,
 y3 = y3,
 p = p
)
y_true <- colMeans(populacja[, c("y1", "y2", "y3")])

## imputacja średnią z k najbliższych sąsiadów (odległość Gowera, tak jak w impute_knn)
## bc = TRUE: korekta obciążenia na podstawie modelu regresji z wielomianem 2 stopnia
impute_nn_mean <- function(proba, y, xs, k, bc = FALSE) {
  resp <- !is.na(proba[[y]])
  y_resp <- proba[[y]][resp]
  ## macierz k x liczba nierespondentów z numerami wierszy dawców
  nn <- gower::gower_topn(x = proba[!resp, xs], y = proba[resp, xs], n = k)$index
  if (bc) {
    model <- lm(reformulate(sprintf("polym(%s, degree = 2, raw = TRUE)",
                                    paste(xs, collapse = ", ")), response = y),
                data = proba[resp, ])
    mu <- predict(model, proba)
    y_imp <- mu[!resp] + colMeans(matrix((y_resp - mu[resp])[nn], nrow = k))
  } else {
    y_imp <- colMeans(matrix(y_resp[nn], nrow = k))
  }
  proba[[y]][!resp] <- y_imp
  proba[[y]]
}

## symulacja (2000 razy)
R <- 2000
results <- matrix(0, R, 12)
colnames(results) <- paste0(rep(c("naive", "nn", "nn_avg", "nn_bc"), each = 3),
                            rep(c("_y1", "_y2", "_y3"), times=4))

xs_2 <- c("x1", "x2")
xs_6 <- c("x1", "x2", "x3", "x4", "x5", "x6")
k_2 <- floor(n^(2/(2+2))) ## k=31 dla p=2
k_6 <- floor(n^(2/(2+6))) ## k=5 dla p=6

for (r in 1:R) {
  proba <- populacja[sample(1:N, n), ]
  proba$delta <- rbinom(nrow(proba), 1, proba$p)
  proba$y1[proba$delta == 0] <- NA
  proba$y2[proba$delta == 0] <- NA
  proba$y3[proba$delta == 0] <- NA

  results[r, 1:3] <- colMeans(proba[, c(c("y1", "y2", "y3"))], na.rm=T)

  ## najbliższy sąsiad (k=1)
  res_y1_y2 <- impute_knn(proba, y1 + y2  ~ x1 + x2, k=1)
  res_y3 <- impute_knn(proba, y3  ~ x1 + x2 + x3  + x4 + x5 + x6, k=1)
  results[r, 4:6] <- c(mean(res_y1_y2$y1), mean(res_y1_y2$y2), mean(res_y3$y3))

  ## średnia z k najbliższych sąsiadów
  results[r, 7:9] <- c(mean(impute_nn_mean(proba, "y1", xs_2, k_2)),
                       mean(impute_nn_mean(proba, "y2", xs_2, k_2)),
                       mean(impute_nn_mean(proba, "y3", xs_6, k_6)))

  ## średnia z k najbliższych sąsiadów z korektą obciążenia
  results[r, 10:12] <- c(mean(impute_nn_mean(proba, "y1", xs_2, k_2, bc = TRUE)),
                         mean(impute_nn_mean(proba, "y2", xs_2, k_2, bc = TRUE)),
                         mean(impute_nn_mean(proba, "y3", xs_6, k_6, bc = TRUE)))

}

boxplot(results -  matrix(rep(y_true, times = 4), byrow=T, ncol = 12, nrow=R),
        xlab = "", ylab = "Obciążenie",
        main = "Imputacja NN: jeden sąsiad, średnia z k sąsiadów i korekta obciążenia",
        las = 2)
abline(a=0,b=0,col="red")

round((colMeans(results) - rep(y_true, times = 4))*100,2)

round(apply(results, 2, var)*100,4)

bias <- (colMeans(results) - rep(y_true, times = 4))
round(sqrt(bias^2 + apply(results, 2, var))*100,2)

round(sqrt(apply(results, 2, var)/R)*100,3)

# Przykład 2 -- Gower ----
dane <- data.frame(
   plec = factor(c("K", "M", "K")),                     # zmienna nominalna
   wyksztalcenie = factor(                              # zmienna porządkowa
       c("wyższe", "średnie", "podstawowe"),
       levels = c("podstawowe", "średnie", "wyższe"),   # określamy porządek poziomów
       ordered = TRUE
   ),
   wiek = c(25, 35, 45)                                 # zmienna ilorazowa
)

VIM::gowerD(data.x = dane,
            factors = "plec",
            numerical = "wiek",
            orders = "wyksztalcenie",
            levOrders = 3)

## odległość pierwszej obserwacji od wszystkich (rozstęp liczony na całym zbiorze)
gower::gower_dist(x = dane[1, ],
                  y = dane)

# Przykład 3 -- czytelnictwo ----
## reading
data <- read.csv(file = "data/data4-czytelnictwo.csv", 
                 colClasses = c("factor", "numeric", "factor", "logical", "logical"))

glm(I(is.na(czyta_ksiazki_z_brakami)) ~ plec + wiek + wyksztalcenie,
    data = data, family = binomial()) |>
  summary()

xs <- c("plec", "wiek", "wyksztalcenie")
resp <- !is.na(data$czyta_ksiazki_z_brakami)
remisy <- sapply(which(!resp), function(i) {
  d <- gower::gower_dist(data[i, xs], data[resp, xs])
  sum(d == min(d))
})
table(remisy)
mean(remisy > 1)

impute_nn_ties <- function(dane, y, xs) {
  resp <- !is.na(dane[[y]])
  dawcy <- dane[resp, ]
  dane[[y]][!resp] <- sapply(which(!resp), function(i) {
    d <- gower::gower_dist(dane[i, xs], dawcy[xs])
    kandydaci <- which(d == min(d))
    dawcy[[y]][kandydaci[sample.int(length(kandydaci), 1)]]
  })
  dane[[y]]
}

set.seed(2025)
f <- czyta_ksiazki_z_brakami ~ plec + wiek + wyksztalcenie
## k = 1: przy remisie wybierany jest pierwszy dawca w kolejności danych
wynik_nn1 <- impute_knn(data, f, k = 1)$czyta_ksiazki_z_brakami
## k = 1: dawca losowany spośród remisów
wynik_nn1_los <- impute_nn_ties(data, "czyta_ksiazki_z_brakami", xs)
## k = 5: dawca losowany spośród 5 najbliższych sąsiadów
wynik_nn5 <- impute_knn(data, f, k = 5)$czyta_ksiazki_z_brakami
## k = 5: dominanta wartości 5 najbliższych sąsiadów (pakiet VIM)
wynik_nn5_dom <- kNN(data, variable = "czyta_ksiazki_z_brakami", dist_var = xs,
                     k = 5, imp_var = FALSE)$czyta_ksiazki_z_brakami

wyniki <- list(`k = 1` = wynik_nn1,
               `k = 1, remisy losowo` = wynik_nn1_los,
               `k = 5, dawca losowy` = wynik_nn5,
               `k = 5, dominanta` = wynik_nn5_dom)

data.frame(
  metoda = c("prawda", "respondenci", names(wyniki)),
  srednia = c(mean(data$czyta_ksiazki),
              mean(data$czyta_ksiazki_z_brakami, na.rm = TRUE),
              sapply(wyniki, mean)),
  trafnosc = c(NA, NA, sapply(wyniki, function(w) mean(w[!resp] == data$czyta_ksiazki[!resp]))),
  row.names = NULL
)

srednie_nn5 <- replicate(100, mean(impute_knn(data, f, k = 5)$czyta_ksiazki_z_brakami))
summary(srednie_nn5)
