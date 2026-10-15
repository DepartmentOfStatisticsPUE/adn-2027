# 7. Kalibracja -- case study
# Kod wyodrębniony z notatnika codes/qmd/10-kalibracja-case-study.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# %% # Wczytanie potrzebnych pakietów
import numpy as np
import pandas as pd
import polars as pl ## svy pracuje na ramkach danych polars
import svy

# %% # Kalibracja
gosp = pd.read_excel("data/gospodarstwa-zajecia.xlsx")
gosp['klm'] = gosp['klm'].astype('category')
gosp['woj'] = gosp['woj'].astype('category')
gosp.head()

gosp[['dochg', 'wydg']].describe()
# Missing values
gosp[['dochg', 'wydg']].isnull().sum()

gosp_resp = gosp.dropna(subset=['dochg', 'wydg']).copy()

pop_klm = gosp['klm'].value_counts().to_dict()
pop_woj = gosp['woj'].value_counts().to_dict()

pop_klm_woj = gosp.groupby(['klm', 'woj'], observed=False).size().to_dict() ## wszystkie przekroje (także puste), jak xtabs w R

gosp_resp['weight'] = 1.0

# Początkowe wagi
gosp_resp['weight'].unique()

gosp_resp_svy = svy.Sample(pl.from_pandas(gosp_resp), svy.Design(wgt="weight"))

gosp_resp_svy_klm = gosp_resp_svy.weighting.calibrate(
    controls={svy.Cat("klm"): pop_klm},
    wgt_name="w_klm")

gosp_resp_svy_woj = gosp_resp_svy.weighting.calibrate(
    controls={svy.Cat("woj"): pop_woj},
    wgt_name="w_woj")

gosp_resp_svy_klm_woj_noint = gosp_resp_svy.weighting.calibrate(
    controls={svy.Cat("klm"): pop_klm, svy.Cat("woj"): pop_woj},
    wgt_name="w_klm_woj_noint")

gosp_resp_svy_klm_woj_int = gosp_resp_svy.weighting.poststratify(
    controls={k: v for k, v in pop_klm_woj.items() if v > 0}, ## pomijamy puste przekroje
    cells=["klm", "woj"],
    wgt_name="w_klm_woj_int")

gosp_resp_svy.estimation.mean(["dochg", "wydg"])

gosp_resp_svy_klm.estimation.mean(["dochg", "wydg"])
gosp_resp_svy_woj.estimation.mean(["dochg", "wydg"])
gosp_resp_svy_klm_woj_noint.estimation.mean(["dochg", "wydg"])
gosp_resp_svy_klm_woj_int.estimation.mean(["dochg", "wydg"])
