data {
  int<lower=1> row_num; // number of rows
  int<lower=1> col_num; // number of columns (without the time column)
  matrix[row_num, col_num] x; // observations (P_meas(t))
  vector[row_num] t; // time column
  real<lower=0> P_o; // P_0 for the cultures of bacteria
}
parameters {
  row_vector<lower=0>[col_num] K; // population boundary
  row_vector[col_num] r; // growth rate
  real<lower=0> sigma_sq;
  
  // Hyperparameters
  real mu_r;
  real<lower=0> mu_sigma;
}
transformed parameters{
  matrix<lower=0, upper=2>[row_num, col_num] Pt;
  
  for (n in 1:row_num) {
    for (m in 1:col_num) {
    Pt[n, m] = K[m]/(1+((K[m]/P_o)-1)*exp(-r[m]*t[n]));
  }
}  
}
model {
  
  // Likelihood
  for (n in 1:row_num) {
    for (m in 1:col_num) {
    x[n, m] ~ normal(Pt[n,m], sigma_sq);
  }
}  

  // Priors
  K ~ normal(1.5,0.5);
  r ~ normal(mu_r, mu_sigma);
  sigma_sq ~ normal(0.005, 0.05);
  
  
  // Hyperpriors
  mu_r ~ normal(0.5, 0.1);
  mu_sigma ~ gamma(1, 1);
}
generated quantities {
  real r_tilde = normal_rng(mu_r, mu_sigma);
}


