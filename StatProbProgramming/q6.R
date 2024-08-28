# Setup (copied from the exercise solutions)

library(tidyverse)
library(magrittr)
library(rstan)
library(grafify)
theme_set(theme_bw(20))
okabi_colors <- c("#E69F00", "#56B4E9", "#009E73")
prior_color <- "#009E73"
likelihood_color <- "#E69F00"
posterior_color <- "#56B4E9"


# Get the data
path = "C:/Users/alpye/Downloads/ecoli.txt"
x = read.csv(file = path, header = TRUE)
t = x[, 1, drop = FALSE]
t = unlist(t[, 1, drop = FALSE])
x = x[, -1, drop = FALSE] # get the data without time
P_o = 0.005


# Start and fit the model

e_coli_model = stan_model("final_q6.stan")

e_coli_fit <- sampling(e_coli_model,
                          list(row_num = nrow(x),
                               col_num = ncol(x), 
                               x = x,
                               t = t,
                               P_o = P_o))

# Extract r (plus the observed r given in the question)
df = data.frame(r = extract(e_coli_fit, "r")[[1]])
r_vect = c(0.724,0.683,0.423,0.262,0.411,0.829,0.469,0.629,0.667,0.384)
# 10 Histograms

ggplot(df, aes(x = r.1)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[1], color = "red") +
  ggtitle("r1")

ggplot(df, aes(x = r.2)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[2], color = "red") +
  ggtitle("r2")

ggplot(df, aes(x = r.3)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[3], color = "red") +
  ggtitle("r3")

ggplot(df, aes(x = r.4)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[4], color = "red") +
  ggtitle("r4")

ggplot(df, aes(x = r.5)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[5], color = "red") +
  ggtitle("r5")

ggplot(df, aes(x = r.6)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[6], color = "red") +
  ggtitle("r6")

ggplot(df, aes(x = r.7)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[7], color = "red") +
  ggtitle("r7")

ggplot(df, aes(x = r.8)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[8], color = "red") +
  ggtitle("r8")

ggplot(df, aes(x = r.9)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[9], color = "red") +
  ggtitle("r9")

ggplot(df, aes(x = r.10)) +
  geom_histogram(fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = r_vect[10], color = "red") +
  ggtitle("r10")


df_r = data.frame(r_tilde = extract(e_coli_fit, "r_tilde")[[1]])
mean(df_r$r_tilde < 0)
