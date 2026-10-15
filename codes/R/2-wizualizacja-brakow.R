# 1. Problematyka braków danych
# Kod wyodrębniony z notatnika codes/qmd/2-wizualizacja-brakow.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebych pakietów ----
library(VIM)
library(naniar)
library(panelView)
library(ggplot2)
library(data.table)
library(tidyverse)

# Przykład 1: dane przekrojowe ----
df_cross <- read.csv("data/data2-cross_sectional.csv")
head(df_cross)

summary(df_cross)

vim_result <- aggr(x = df_cross)

summary(vim_result)

vis_miss(df_cross)

vis_miss(df_cross, cluster = T, sort_miss = T)

gg_miss_var(df_cross)

gg_miss_upset(df_cross)

ggplot(data=df_cross, aes(x = x1, y)) + geom_point()

ggplot(data=df_cross, aes(x = x1, y)) + geom_miss_point()

# Przykład 2: dane panelowe ----
df_long <- read.csv("data/data2-panel_long.csv")
head(df_long)

df_wide <- read.csv("data/data2-panel_wide.csv")
head(df_wide)

VIM::aggr(df_wide)

df_long |>
  subset(select=c(unit_id, year, y)) |>
  setDT() |> 
  dcast(unit_id ~ year, value.var = "y") |>
  VIM::aggr(plot = F)  |>
  summary()

df_long |>
  select(unit_id, year, y) |>
  pivot_wider(names_from = year, values_from = y) |>
  VIM::aggr(plot = F) |>
  summary()

panelview(data = df_long, formula = y ~ 1, index = c("unit_id", "year"), type = "missing")

panelview(data = df_long, formula = x2 ~ 1, index = c("unit_id", "year"), type = "missing")

panelview(data = df_long, formula = 1 ~ y + x1 + x2, index = c("unit_id", "year"), type = "missing")
