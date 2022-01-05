// Learn more about model development with Stan at:
//
//    http://mc-stan.org/users/interfaces/rstan.html
//    https://github.com/stan-dev/rstan/wiki/RStan-Getting-Started
//

data {
  int<lower=0> N;         // Number of distances 
  real<lower=0> Y[N];     // Estimated ratios
}
parameters {
  real<lower=0> alpha;             
  real<lower=0> beta;      
}
model {
  Y ~ beta(alpha, beta); // Likelihood
  //alpha ~ uniform(0,25); //Prior alpha
  //beta ~ uniform(0,2500); //Prior beta
  alpha ~ uniform(0.0191999999,90); //Prior alpha
  beta ~ uniform(0.9407999,810); //Prior beta
}
generated quantities{
  vector[N] log_lik;
  vector[N] lsimData;
  int aMax_indicator;
  int aMin_indicator;
  real meanRep;
  real stdRep;
  real mean_ind;
  real std_ind;
  vector[N] sum_mean;
  real p_val_mean;
  for (i in 1:N){
    lsimData[i] = beta_rng(alpha,beta)*10+1;
    sum_mean[i] = mean(lsimData) > mean(Y);
  }
  for (i in 1:N) {
    log_lik[i] = beta_lpdf(Y[N]|alpha,beta);
  }
  // COmpare with real data
  aMax_indicator = max(lsimData) > max(Y);
  aMin_indicator = min(lsimData) < min(Y);
  meanRep = mean(lsimData);
  stdRep = sd(lsimData);
  mean_ind = meanRep > mean(Y);
  std_ind = stdRep > sd(Y);
  p_val_mean = sum(sum_mean)/N;
}
