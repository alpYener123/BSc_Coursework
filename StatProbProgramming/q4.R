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


# Generate data

y = c()
x = c()
theta = c()
alpha = -5
beta = 1.5

for (i in 1:46){
  x_new = runif(1,0,10)
  x = append(x, x_new)
  
  theta_new = 1/ (1 + exp(-(alpha + beta * x_new)))
  theta = append(theta, theta_new)
  
  y_new = rbernoulli(1, theta_new)
  y = append(y, y_new)
}

# Start and fit the model

bernoulli_model = stan_model("final_q4.stan")

bernoulli_fit <- sampling(bernoulli_model,
                       list(N = length(y),
                            y = y, 
                            x = x))

# Get samples
df = data.frame(alpha = extract(bernoulli_fit, "alpha")[[1]],
                beta = extract(bernoulli_fit, "beta")[[1]])

# Draw histograms for each parameter to show that
# the parameters are recovered approximately
ggplot() +
  geom_histogram(data = data.frame(alpha = df$alpha), 
                 aes(alpha), bins = 75) +
  geom_vline(xintercept = -5, color = "blue") +
  ggtitle("alpha samples")

ggplot() +
  geom_histogram(data = data.frame(beta = df$beta), 
                 aes(beta), bins = 75) +
  geom_vline(xintercept = 1.5, color = "blue") +
  ggtitle("beta samples")


# Simplified: calculate average theta when x = 5
# 1/ (1 + exp(-(alpha + beta * 5)))

df$theta_when_5hrs = 1/ (1 + exp(-(df$alpha + df$beta * 5)))
mean(df$theta_when_5hrs)
