# 7. Kalibracja -- case study
# Kod wyodrębniony z notatnika codes/qmd/10-kalibracja-case-study.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebnych pakietów ----
library(readxl)
library(survey)

# Kalibracja ----
gosp <- read_excel("data/gospodarstwa-zajecia.xlsx")
gosp <- transform(gosp, 
                  klm = as.factor(klm),
                  woj = as.factor(woj))
head(gosp)

summary(gosp[, c("los", "dochg", "wydg")])

## miejsce na rozwiązanie

gosp_resp <- gosp[complete.cases(gosp),]

pop_klm <- xtabs(~klm, gosp)
pop_woj <- xtabs(~woj, gosp)
pop_klm_woj <- xtabs(~klm+woj, gosp)

## miejsce na rozwiązanie

gosp_resp_svy <- svydesign(ids=~1, data=gosp_resp)

table(weights(gosp_resp_svy))

gosp_resp_svy_klm <- calibrate(design = gosp_resp_svy, 
                               formula = list(~klm),
                               population = list(pop_klm))

## miejsce na rozwiązanie

gosp_resp_svy_woj <- calibrate(design = gosp_resp_svy, 
                               formula = list(~woj),
                               population = list(pop_woj))

## miejsce na rozwiązanie

gosp_resp_svy_klm_woj_noint <- calibrate(design = gosp_resp_svy, 
                                         formula = list(~klm, ~woj),
                                         population = list(pop_klm, pop_woj))

## przy liniowej jest problem numeryczny bo są zera w pop_klm_woj
gosp_resp_svy_klm_woj_int <- calibrate(design = gosp_resp_svy, 
                                       formula = list(~klm+woj),
                                       population = list(pop_klm_woj),
                                       calfun = "raking") 

svymean(~dochg+wydg, gosp_resp_svy)

svymean(~dochg+wydg, gosp_resp_svy_klm)
svymean(~dochg+wydg, gosp_resp_svy_woj)
svymean(~dochg+wydg, gosp_resp_svy_klm_woj_noint)
svymean(~dochg+wydg, gosp_resp_svy_klm_woj_int)
