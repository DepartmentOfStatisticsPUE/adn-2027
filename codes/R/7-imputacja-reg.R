# 6. Imputacja regresyjna
# Kod wyodrębniony z notatnika codes/qmd/7-imputacja-reg.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebych pakietów ----
library(simputation)
library(naniar)
library(ggplot2)
library(patchwork)
library(data.table)

# Przykład 1 z zajęć -- wizualizacja ----
set.seed(2025)
n <- 1000
x <- rnorm(n)
y <- 2 + 2*x + rnorm(n)
pr <- plogis(1-1*x)
R <- rbinom(n, 1, pr)
y_miss <- ifelse(R == 1,y,NA)
sim_data <- data.frame(x,y,R,y1=y_miss,y2=y_miss,y3=y_miss)
head(sim_data)

set.seed(2025)
sim_data <- sim_data |> 
  bind_shadow() |>
  impute_lm(y1 ~ x, add_residual = "none") |>
  impute_lm(y2 ~ x, add_residual = "observed") |>
  impute_lm(y3 ~ x, add_residual = "normal") |>
  add_label_shadow()

ggplot(sim_data,
       aes(x = x,
           y = y1,
           color = any_missing)) + 
  geom_point() +
  scale_color_brewer(palette = "Dark2") +
  theme(legend.position = "bottom") +
  labs(y="y", title = "Deterministic") -> p1

ggplot(sim_data,
       aes(x = x,
           y = y2,
           color = any_missing)) + 
  geom_point() +
  scale_color_brewer(palette = "Dark2") +
  theme(legend.position = "bottom")  +
  labs(y="y", title = "Stochastic (observed)")-> p2

ggplot(sim_data,
       aes(x = x,
           y = y3,
           color = any_missing)) + 
  geom_point() +
  scale_color_brewer(palette = "Dark2") +
  theme(legend.position = "bottom") +
  labs(y="y", title = "Stochastic (normal)") -> p3

p1 + p2 + p3 +
  plot_layout(guides = "collect") &
  theme(legend.position = "bottom") -> plot_slides

ggsave(filename = "fig-regimp.png", width = 10, height = 5, plot= plot_slides)
plot_slides
