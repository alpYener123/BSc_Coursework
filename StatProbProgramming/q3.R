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



# Generate 20 samples

y = c()
x = c()

for (i in 1:20){
  x_new = rnorm(1,0,1)
  x = append(x, x_new)
  new_y = rnorm(1, 1 + 2*x_new + 1.2*(x_new^2), 1)
  y = append(y, new_y)
}

# Start and fit the model

normal_model = stan_model("final_q3.stan")

normal_fit <- sampling(normal_model,
                        list(N = length(y),
                             y = y, 
                             x = x))

# Get samples
df = data.frame(b_1 = extract(normal_fit, "b_1")[[1]],
                b_2 = extract(normal_fit, "b_2")[[1]],
                b_3 = extract(normal_fit, "b_3")[[1]],
                sigma = extract(normal_fit, "sigma")[[1]])

# Draw histograms for each parameter to show that
# the parameters are recovered approximately
ggplot() +
geom_histogram(data = data.frame(b_1 = df$b_1), 
               aes(b_1), bins = 75) +
  geom_vline(xintercept = 1, color = "blue") +
  ggtitle("b_1 samples")

ggplot() +
  geom_histogram(data = data.frame(b_2 = df$b_2), 
                 aes(b_2), bins = 75) +
  geom_vline(xintercept = 2, color = "blue") +
  ggtitle("b_2 samples")

ggplot() +
  geom_histogram(data = data.frame(b_3 = df$b_3), 
                 aes(b_3), bins = 75) +
  geom_vline(xintercept = 1.2, color = "blue") +
  ggtitle("b_3 samples")

ggplot() +
  geom_histogram(data = data.frame(sigma = df$sigma), 
                 aes(sigma), bins = 75) +
  geom_vline(xintercept = 1, color = "blue") +
  ggtitle("sigma samples")

# Since -1 and 1 are the same when you square it
ggplot() +
  geom_histogram(data = data.frame(sigma = abs(df$sigma)), 
                 aes(sigma), bins = 75) +
  geom_vline(xintercept = 1, color = "blue") +
  ggtitle("sigma samples, in absolute value")

# In ax^2 + bx + c = 0 if b^2 - 4ac < 0,
# then the equation does not have any real roots

# In our formula, this corresponds to: (b_2)^2 - 4 * b_3 * b_1 < 0
# which corresponds to: (b_2)^2 < 4 * b_3 * b_1

no_real_roots_prob = mean((df$b_2)^2 < 4*df$b_3*df$b_1)
print(no_real_roots_prob)





