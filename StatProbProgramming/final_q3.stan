data {
  int<lower=0> N;
  vector[N] y;
  vector[N] x;
}
parameters {
  real b_1; 
  real b_2;
  real b_3;
  real sigma;
}
model {
  y ~ normal(b_1 + b_2*x + b_3*(x^2), sigma^2);
  
  b_1 ~ normal(0,1);
  b_2 ~ normal(0,1);
  b_3 ~ normal(0,1);
  sigma ~ normal(0,1);

}



