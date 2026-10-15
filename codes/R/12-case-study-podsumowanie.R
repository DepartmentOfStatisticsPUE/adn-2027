# 9. Case study -- podsumowanie zajęć
# Kod wyodrębniony z notatnika codes/qmd/12-case-study-podsumowanie.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

library(haven)
library(tidyverse)

# [w notatniku nie uruchamiane (eval = FALSE)]
# ## źródło: https://www.parp.gov.pl/images/publications/BKL/nowy-uklad/Baza_danych_z_badania_ludnoci_BKL_edycja_2021_SAV-SPSS.sav
# ## (strona blokuje pobieranie z poziomu R, dlatego wczytujemy kopię lokalną)
# bkl2021 <- read_spss("data/downloaded_data.sav", user_na = T)
