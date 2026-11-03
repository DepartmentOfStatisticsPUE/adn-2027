# Hot-deck w klasach: krzyżowanie zmiennych, komórki przewidywanej średniej (yhat),
# komórki skłonności do odpowiedzi (phat) i krzyżowanie yhat x phat.
# Symulacja do interaktywnego podsumowania wizualizacje/4a-imputacja-hotdeck.html (część 5).

suppressMessages(library(simputation))
set.seed(2026)
N <- 50000; n <- 1000; R <- 5000
X <- matrix(runif(N*6), N, 6, dimnames = list(NULL, paste0("x", 1:6)))
pop <- as.data.frame(X)
pop$y <- with(pop, -2 + x1 + x2 + 2*x3 + 2*x4 + rnorm(N))   # Y: x1..x4
pop$p <- with(pop, plogis(-1.5 + 1.5*(x3 + x4 + x5 + x6)))  # odpowiedz: x3..x6
y_true <- mean(pop$y)
kw <- function(v, k) cut(v, unique(quantile(v, 0:k/k)), include.lowest = TRUE)
est <- c("naive","hd","hd_x12","hd_x6","hd_pm","hd_rp","hd_pmrp")
res <- matrix(NA, R, length(est), dimnames = list(NULL, est)); nas <- res
for (r in 1:R) {
  s <- pop[sample(N, n), ]
  s$odp <- rbinom(n, 1, s$p) == 1
  s$y[!s$odp] <- NA
  s$kl_x12 <- interaction(kw(s$x1, 4), kw(s$x2, 4))                         # 16 komorek
  s$kl_x6  <- interaction(lapply(s[paste0("x", 1:6)], kw, 2))               # 64 komorki
  s$yhat <- predict(lm(y ~ x1 + x2 + x3 + x4 + x5 + x6, data = s), newdata = s)
  s$phat <- predict(glm(odp ~ x1 + x2 + x3 + x4 + x5 + x6, family = binomial, data = s), type = "response")
  s$kl_pm <- kw(s$yhat, 16); s$kl_rp <- kw(s$phat, 16)
  s$kl_pmrp <- interaction(kw(s$yhat, 4), kw(s$phat, 4))
  imp <- list(naive = s$y[s$odp], hd = impute_rhd(s, y ~ 1)$y,
              hd_x12 = impute_rhd(s, y ~ kl_x12)$y, hd_x6 = impute_rhd(s, y ~ kl_x6)$y,
              hd_pm = impute_rhd(s, y ~ kl_pm)$y, hd_rp = impute_rhd(s, y ~ kl_rp)$y,
              hd_pmrp = impute_rhd(s, y ~ kl_pmrp)$y)
  res[r, ] <- sapply(imp, mean, na.rm = TRUE)
  nas[r, ] <- sapply(imp, function(v) sum(is.na(v)))
}
b <- colMeans(res) - y_true; v <- apply(res, 2, var)
print(round(cbind(bias100 = b*100, var100 = v*100, rmse100 = sqrt(b^2 + v)*100, braki = colMeans(nas)), 4))
cat("resp rate", mean(pop$p), " sd y", sd(pop$y), "\n")
cat("Błąd Monte Carlo obciążenia x 100:", round(sqrt(v/R)*100, 3), "
")
