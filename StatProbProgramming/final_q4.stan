data {
  int<lower=0> N;
  array[N] int y;
  vector[N] x;
}
parameters {
  real alpha;
  real beta;
}
transformed parameters{
  vector<lower=0, upper=1>[N] theta;
  
  for (n in 1:N) {
  theta[n] = 1/ (1 + exp(-(alpha + beta * x[n])));
}
  
  //theta 
}
model {
  y ~ bernoulli(theta);
  
  alpha ~ normal(-4, 2);
  beta ~ normal(1,2);

}



