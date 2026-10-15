# 7. Propensity score adjustment
# Kod wyodrębniony z notatnika codes/qmd/11-propensity-score.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(readxl)
library(glmnet)

# Ważenie przez odwrotność -- metoda podstawowa ----
gosp <- read_excel("data/gospodarstwa-zajecia.xlsx")
gosp <- transform(gosp, 
                  klm = as.factor(klm),
                  woj = as.factor(woj))
head(gosp)

summary(gosp[, c("los", "dochg", "wydg")])

gosp$R <- !is.na(gosp$dochg)

m1 <- glm(R ~ klm + woj, data = gosp, family = binomial())
summary(predict(m1, type = "response"))

gosp$w_rho <- 1/predict(m1, gosp, type="response")

c(mean(gosp$dochg, na.rm=T), weighted.mean(gosp$dochg, gosp$w_rho, na.rm=T))

set.seed(2026)
m2 <- cv.glmnet(x = model.matrix(~ klm + woj, gosp)[, -1],
                y = gosp$R,
                family = "binomial")
coef(m2, s = "lambda.min")

gosp$w_rho_lasso <- 1/as.numeric(predict(m2, newx = model.matrix(~ klm + woj, gosp)[, -1], type="response", s = "lambda.min"))

c(bez = mean(gosp$dochg, na.rm=T), 
  glm = weighted.mean(gosp$dochg, gosp$w_rho, na.rm=T),
  lasso = weighted.mean(gosp$dochg, gosp$w_rho_lasso, na.rm=T))

summary(gosp[, c("w_rho", "w_rho_lasso")])

plot(gosp$w_rho, gosp$w_rho_lasso)
