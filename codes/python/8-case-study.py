# Case Study 2025
# Kod wyodrębniony z notatnika codes/qmd/8-case-study.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
