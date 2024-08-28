data {
  
  // Input Data
  int<lower=1> N;
  real y[N];
  real x[N];
  
  // Gaussian Process hyperparameters
  real<lower=0> alpha;
  real<lower=0> lambda;
  
}
transformed data {
  matrix[N, N] K;

  // Matern 3/2 covariance kernel
  K = gp_matern32_cov(x, alpha, lambda);
  
  // Add a bit of noise to the diagonal for numerical stability
  for (n in 1:N) {
    K[n, n] = K[n, n] + 1e-6;
  }


}
parameters {
  // time-varying variance function
  vector[N] sigma_log;
}
model {

  // Likelihood
  y ~ normal(0, square(exp(sigma_log)));

  // GP
  sigma_log ~ multi_normal(rep_vector(-1, N), K);

}




