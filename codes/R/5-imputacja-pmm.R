# 4. Imputacja PMM
# Kod wyodrębniony z notatnika codes/qmd/5-imputacja-pmm.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebych pakietów ----
library(simputation)
library(FNN) 

# Przykład 1 z zajęć ----
przyklad1 <- data.frame(X = seq(10, 35, by=5),
                        Y = c(25, 35, NA, 55, 65, NA))
przyklad1

przyklad1 |>
  impute_pmm(formula = Y~ X,
             predictor = impute_lm)

## model liniowy
model1 <- lm(formula = Y~X, data=przyklad1)
## wartości przewidywane
przyklad1$pred <- predict(model1, przyklad1)
## wyszukiwanie najbliższego sąsiada
sasiedzi <- get.knnx(data = przyklad1[!is.na(przyklad1$Y), "pred"], 
                     query = przyklad1[is.na(przyklad1$Y), "pred"],
                     k = 1)
## przepisujemy wartości najbliższego sąsiada
przyklad1_wynik <- przyklad1
przyklad1_wynik[is.na(przyklad1$Y), "Y"] <- przyklad1_wynik[!is.na(przyklad1$Y), "Y"][sasiedzi$nn.index[,1]]
przyklad1_wynik

## wyszukiwanie najbliższego sąsiada
sasiedzi <- get.knnx(data = przyklad1[!is.na(przyklad1$Y), "pred"], 
                     query = przyklad1[is.na(przyklad1$Y), "pred"],
                     k = 2)
sasiedzi
## przepisujemy wartości najbliższego sąsiada

przyklad1_wynik <- przyklad1
przyklad1_wynik[is.na(przyklad1$Y), "Y"] <- apply(sasiedzi$nn.index, 1, FUN=function(x) mean(przyklad1_wynik[!is.na(przyklad1$Y), "Y"][x]))
przyklad1_wynik

# Krótkie ćwiczenie ----
set.seed(42)
n <- 10

df <- data.frame(
  id = 1:10,
  plec = c("K", "M", "M", "K", "M", "K", "M", "K", "M", "K"),
  rok_studiow = c(1, 2, 3, 1, 2, 3, 1, 2, 3, 1),
  pracuje = c("Tak", "Nie", "Tak", "Nie", "Tak", "Nie", "Tak", "Tak", "Nie", "Tak"),
  piwa = c(2, 5, 8, NA, 6, NA, 9, 4, 7, NA)
)

df

# Przykład 2 -- czytelnictwo ----
## reading
data <- read.csv(file = "data/data4-czytelnictwo.csv", 
                 colClasses = c("factor", "numeric", "factor", "logical", "logical"))
head(data)

summary(data)

data$czyta_ksiazki_z_brakami_nni <- data$czyta_ksiazki_z_brakami
data$czyta_ksiazki_z_brakami_pmm <- as.numeric(data$czyta_ksiazki_z_brakami) ## musimy zamienić na braki numeryczny (patrz poniżej)

data |> 
  impute_pmm(formula = czyta_ksiazki_z_brakami_pmm ~ plec + wiek + wyksztalcenie)  |>
  impute_knn(czyta_ksiazki_z_brakami_nni ~ plec + wiek + wyksztalcenie, k = 1) -> imputacja_wynik

aggregate(cbind(True=czyta_ksiazki, 
                NNI=czyta_ksiazki_z_brakami_nni,
                PMM = czyta_ksiazki_z_brakami_pmm) ~ 1, imputacja_wynik, FUN=mean)

# Symulacja ----
# Ustawienie ziarna losowości dla reprodukowalności
set.seed(123)

# Parametry symulacji
N <- 50000  # rozmiar populacji
n <- 400    # rozmiar próby

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

## sumulacja (2000 razy)
R <- 2000
results <- matrix(0, R, 9)
colnames(results) <- paste0(rep(c("naive", "nn", "pmm"), each = 3), 
                            rep(c("_y1", "_y2", "_y3"), times=3))

for (r in 1:R) {
  set.seed(r)
  proba <- populacja[sample(1:N, n), ]
  proba$delta <- rbinom(nrow(proba), 1, proba$p)
  proba$y1[proba$delta == 0] <- NA
  proba$y2[proba$delta == 0] <- NA
  proba$y3[proba$delta == 0] <- NA
  
  results[r, 1:3] <- colMeans(proba[, c(c("y1", "y2", "y3"))], na.rm=T)
  
  results_nn <- proba |>
    impute_knn(y1 + y2  ~ x1 + x2, k=5) |>
    impute_knn(y3 ~ x1 + x2 + x3 + x4 + x5 + x6, k=5)
 
  results_pmm <- proba |>
    impute_pmm(y1 + y2  ~ x1 + x2, predictor = impute_lm) |>
    impute_pmm(y3 ~ x1 + x2 + x3 + x4 + x5 + x6, predictor = impute_lm)

  proba$y1_nn <- results_nn$y1
  proba$y2_nn <- results_nn$y2
  proba$y3_nn <- results_nn$y3
  
  proba$y1_pmm <- results_pmm$y1
  proba$y2_pmm <- results_pmm$y2
  proba$y3_pmm <- results_pmm$y3
  
  results[r, 4:9] <- colMeans(proba[, c("y1_nn", "y2_nn", "y3_nn", "y1_pmm", "y2_pmm", "y3_pmm")])
   
}

boxplot(results - matrix(rep(y_true, times = 3), byrow=T, ncol = 9, nrow=R), 
        xlab = "Estymator", ylab = "Obciążenie",
        main = "Obciążenie estymatorów: naiwny, NN i PMM")
abline(a=0,b=0,col="red")

(colMeans(results) - rep(y_true, times = 3))*100
