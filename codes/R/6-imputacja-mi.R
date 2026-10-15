# 5. Imputacja wielokrotna
# Kod wyodrębniony z notatnika codes/qmd/6-imputacja-mi.qmd
# Ścieżki do danych są względne względem głównego folderu repozytorium (adn-2027/).

# Wczytanie potrzebych pakietów ----
library(mice)
#library(rMIDAS)
#set_python_env(x = "/opt/homebrew/bin/python3.10")

# Przykład 1 z zajęć ----
set.seed(2025)
n_rows <- 20
df_example <- data.frame(
  A = seq(1:n_rows)*2, 
  B = 5 + seq(1:n_rows)*2 + 10*rnorm(n_rows), 
  C = 2+sqrt(seq(1:n_rows)) + rnorm(n_rows)
)
df_example_miss <- df_example
df_example_miss$A[c(2,5, 13)] <- NA
df_example_miss$B[c(1,2,8,20)] <- NA
df_example_miss$C[c(9,10,14:18)] <- NA
df_example_miss

df_example_imp <- mice(df_example_miss, m=1, seed = 2025)

df_example_imp

complete(df_example_imp)

colMeans(df_example) ## bez braków
colMeans(df_example_miss, na.rm=T) ## z brakami
colMeans(complete(df_example_imp)) ## po imputacji

pred_mat <- df_example_imp$predictorMatrix
pred_mat["C", "B"] <- 0
pred_mat["B", "C"] <- 0
pred_mat

df_example_imp <- mice(data = df_example_miss, 
                       m=4, 
                       method = "rf", 
                       predictorMatrix = pred_mat, 
                       seed = 2025)

df_example_imp

complete(df_example_imp, 1)
complete(df_example_imp, 3)

sapply(complete(df_example_imp, "all"), colMeans)

sapply(complete(df_example_imp, "all"), colMeans) |> 
  apply(MARGIN = 1, FUN = mean)

colMeans(df_example) ## bez braków

lm_results <- with(df_example_imp, lm(C ~ A))
str(lm_results,1)

pool(lm_results)

summary(pool(lm_results))

coef(summary(lm(C~A, df_example)))
coef(summary(lm(C~A, df_example_miss)))

# Przyklad użycia pakietu `MIDAS` ----
# [w notatniku nie uruchamiane (eval = FALSE)]
# adult <- read.csv("https://raw.githubusercontent.com/MIDASverse/MIDASpy/master/Examples/adult_data.csv",row.names = 1)[1:1000,]

# [w notatniku nie uruchamiane (eval = FALSE)]
# set.seed(89)
# adult <- add_missingness(adult, prop = 0.1)

# [w notatniku nie uruchamiane (eval = FALSE)]
# adult_cat <- c('workclass','marital_status','relationship','race','education','occupation','native_country')
# adult_bin <- c('sex','class_labels')
#
# # Apply rMIDAS preprocessing steps
# adult_conv <- convert(adult, 
#                       bin_cols = adult_bin, 
#                       cat_cols = adult_cat,
#                       minmax_scale = TRUE)

# [w notatniku nie uruchamiane (eval = FALSE)]
# adult_train <- train(adult_conv,
#                        training_epochs = 20,
#                        layer_structure = c(128,128),
#                        input_drop = 0.75,
#                        seed = 89)

# [w notatniku nie uruchamiane (eval = FALSE)]
# adult_complete <- complete(adult_train, m = 10)

# [w notatniku nie uruchamiane (eval = FALSE)]
# adult_model <- combine("class_labels ~ hours_per_week + sex", 
#                     adult_complete,
#                     family = stats::binomial)
#
# adult_model
