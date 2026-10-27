# 2b. Imputacja dedukcyjna na podstawie danych tekstowych
# Kod wyodrębniony z notatnika codes/qmd/3b-imputacja-dedukcyjna-tekst.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(data.table)
library(tidyr) ## funkcja fill
library(stringr)
library(zoo)
library(ellmer) ## do modeli jezykowych

# Przykład imputacji dedukcyjnej ----
dane <- read.csv("data/data3-przyklad-imputacji.csv")
head(dane)

dane |>
  fill(liczba_pokoi)

zoo::na.locf(dane$liczba_pokoi)

data.table::nafill(dane$liczba_pokoi, "locf")

data.table::setnafill(dane, "locf", cols = c("liczba_pokoi"))
dane

substr("1465011", 1, 2)

str_extract("Przytulna kawalerka 32,1m2, 1 pokój w centrum!", "\\d{2},\\d{1}")

# [w notatniku nie uruchamiane (eval = FALSE)]
# chat <- chat_ollama(model = "qwen3:4b",
#                     params = params(temperature = 0, seed = 2025))
#
# type_apartment <- type_object(
#   floor_area = type_number(),
#   is_studio = type_boolean(),
#   number_of_rooms = type_number()
# )
#
# wynik <- chat$chat_structured(
#   "Przytulna kawalerka 32,1m2, 1 pokój w centrum!`",
#   type = type_apartment
# )

# [w notatniku nie uruchamiane (eval = FALSE)]
# $floor_area
# [1] 32.1
#
# $is_studio
# [1] TRUE
#
# $number_of_rooms
# [1] 1

# [w notatniku nie uruchamiane (eval = FALSE)]
# wynik <- chat$chat_structured(
#      "Luksusowy apartament 85m2, 4 pokoje",
#      type = type_apartment
# )

# [w notatniku nie uruchamiane (eval = FALSE)]
# > wynik
# $floor_area
# [1] 85
#
# $is_studio
# [1] FALSE
#
# $number_of_rooms
# [1] 4

# [w notatniku nie uruchamiane (eval = FALSE)]
# wynik <- chat$chat_structured(
#      "Kompaktowe mieszkanie 30m2 w świetnej lokalizacji",
#      type = type_apartment
# )

# [w notatniku nie uruchamiane (eval = FALSE)]
# > wynik
# $floor_area
# [1] 30
#
# $is_studio
# [1] TRUE
#
# $number_of_rooms
# [1] 1
