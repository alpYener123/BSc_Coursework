# Setup (copied from the code examples for Gaussian Processes)

knitr::opts_chunk$set(echo = TRUE)
library(rstan)
library(tidyverse)
library(magrittr)
library(grafify)
theme_set(theme_bw(20))
okabi_colors <- c("#E69F00", "#56B4E9", "#009E73")
prior_color <- "#009E73"
likelihood_color <- "#E69F00"
posterior_color <- "#56B4E9"


# Get the data
path = "C:/Users/alpye/Downloads/EURUSD.txt"
df = read.csv(file = path, header = TRUE)
y = as.array(df$Return_scaled)
x = as.array(df$Time)
alpha = 1
lambda = 30
N = nrow(df)


# Start and fit the model

usd_model = stan_model("final_q7.stan")

usd_fit <- sampling(usd_model,
                       list(N = N,
                            y = y, 
                            x = x,
                            alpha = alpha,
                            lambda = lambda),
                    chains = 1, iter = 1000)



# Got sigma square samples
sigma_sq_samples <- (exp(rstan::extract(usd_fit, "sigma_log")[["sigma_log"]]))^2 %>% 
  t %>% data.frame() %>% 
  mutate(x = df$Time)

sigma_sq_samples_l <- sigma_sq_samples %>% 
  gather(key = "sample", value = "sigma_sq", -x)


# Got the normal sigma samples
sigma_samples = (exp(rstan::extract(usd_fit, "sigma_log")[["sigma_log"]]))
sigma_mean = mean(sigma_samples)


p_f <- ggplot() +
  geom_line(
    data = sigma_sq_samples_l,
    aes(x = x, y = sigma_sq, group = sample),
    alpha = 0.01) +
  geom_point(data = df, 
             aes(x = Time, y = Return_scaled), color ="red") +
  ggtitle("Sigma square values (black lines) and \n Return_scaled values (red dots) 
          and sigma mean (blue line)") +
  geom_hline(yintercept = sigma_mean, color = "blue") +
  labs(y="y")
  

print(p_f)

# As we can see, the variance increases just after x=50
# To make blue more visible, I made the black alpha = 0.01