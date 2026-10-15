# 3. Imputacja NN
# Kod wyodrębniony z notatnika codes/qmd/4-imputacja-nn.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebych pakietów ----
library(simputation)
library(VIM)

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

## imputacja średnią z M najbliższych sąsiadów (odległość Gowera, tak jak w impute_knn)
## bc = TRUE: korekta obciążenia na podstawie modelu regresji z wielomianem 2 stopnia
impute_nn_mean <- function(proba, y, xs, M, bc = FALSE) {
  resp <- !is.na(proba[[y]])
  y_resp <- proba[[y]][resp]
  ## macierz M x liczba nierespondentów z numerami wierszy dawców
  nn <- gower::gower_topn(x = proba[!resp, xs], y = proba[resp, xs], n = M)$index
  if (bc) {
    model <- lm(reformulate(sprintf("polym(%s, degree = 2, raw = TRUE)",
                                    paste(xs, collapse = ", ")), response = y),
                data = proba[resp, ])
    mu <- predict(model, proba)
    y_imp <- mu[!resp] + colMeans(matrix((y_resp - mu[resp])[nn], nrow = M))
  } else {
    y_imp <- colMeans(matrix(y_resp[nn], nrow = M))
  }
  proba[[y]][!resp] <- y_imp
  proba[[y]]
}

## sumulacja (2000 razy)
R <- 2000
results <- matrix(0, R, 12)
colnames(results) <- paste0(rep(c("naive", "nn", "nn_avg", "nn_bc"), each = 3),
                            rep(c("_y1", "_y2", "_y3"), times=4))

xs_2 <- c("x1", "x2")
xs_6 <- c("x1", "x2", "x3", "x4", "x5", "x6")
M_2 <- floor(n^(2/(2+2))) ## M=31 dla d=2
M_6 <- floor(n^(2/(2+6))) ## M=5 dla d=6

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

  ## średnia z M najbliższych sąsiadów
  results[r, 7:9] <- c(mean(impute_nn_mean(proba, "y1", xs_2, M_2)),
                       mean(impute_nn_mean(proba, "y2", xs_2, M_2)),
                       mean(impute_nn_mean(proba, "y3", xs_6, M_6)))

  ## średnia z M najbliższych sąsiadów z korektą obciążenia
  results[r, 10:12] <- c(mean(impute_nn_mean(proba, "y1", xs_2, M_2, bc = TRUE)),
                         mean(impute_nn_mean(proba, "y2", xs_2, M_2, bc = TRUE)),
                         mean(impute_nn_mean(proba, "y3", xs_6, M_6, bc = TRUE)))

}

boxplot(results -  matrix(rep(y_true, times = 4), byrow=T, ncol = 12, nrow=R),
        xlab = "", ylab = "Obciążenie",
        main = "Imputacja NN: jeden sąsiad, średnia z M sąsiadów i korekta obciążenia",
        las = 2)
abline(a=0,b=0,col="red")

round((colMeans(results) - rep(y_true, times = 4))*100,2)

round(apply(results, 2, var)*100,4)

bias <- (colMeans(results) - rep(y_true, times = 4))
round(sqrt(bias^2 + apply(results, 2, var))*100,2)

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

# Przyklad 3 ----
## reading
data <- read.csv(file = "data/data4-czytelnictwo.csv", 
                 colClasses = c("factor", "numeric", "factor", "logical", "logical"))

glm(I(is.na(czyta_ksiazki_z_brakami)) ~ plec + wiek + wyksztalcenie,
    data = data, family = binomial()) |>
  summary()
