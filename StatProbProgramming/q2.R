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

# Models used:
# y ~ N(a + bx, 1)
# a ~ N(2, 3)
# b ~ N(1.5, 1.5)

# Data:
x = c(0.27,0.12,-0.04,-1.12,-1.35,0.77,0.41,-0.35,-0.11,0.82)
y = c(2.06,4.3,3.86,1.02,0.16,3.97,3.32,1.93,3.22,2.85)

# Define grids
delta = 0.01
a_grid = seq(from = -1, to = 5, by = delta)
b_grid = seq(from = 0, to = 3, by = delta)

# Create df
df = expand.grid(a = a_grid, b = b_grid)

# Likelihood
for(i in 1:nrow(df)) {
  
  df[i, "likelihood"] = prod(dnorm(x = y,
                                    mean = df[i, "a"] + df[i, "b"] * x,
                                    sd = 1))
}

# Prior, posterior and normalization
# Due to the coefficient delta^2, sum(df$posterior) = 10000
# Hence some values on the graph are like 0.9
df <- df %>% 
  mutate(prior = dnorm(a, 2, 3) * dnorm(b, 1.5, 1.5), 
         posterior_unnormalize = prior*likelihood, 
         posterior = posterior_unnormalize/(sum(posterior_unnormalize)*delta^2))

# Find the MAP
posterior_mode <- df[which.max(df$posterior), c("a", "b")]

# Plot the full posterior and the MAP lines
p <- df %>% 
  ggplot(aes(x = a, y = b, fill = posterior)) +
  geom_tile() +
  scale_fill_gradientn(colours = rainbow(5)) +
  ggtitle("Full Posterior with MAPs") +
  geom_hline(yintercept = posterior_mode$b, color = "black") +
  geom_vline(xintercept = posterior_mode$a, color = "black")


p
