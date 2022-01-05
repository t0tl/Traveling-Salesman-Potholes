library(rstan)
library(readxl)
library(ggplot2)
library(loo)
library(shinystan)

setwd("~/VSC code/Python/Traveling-Salesman-Potholes/src")
rstan_options(auto_write=TRUE)
h <- read_excel("Propdata.xlsx")
h$Propad <- (h$Prop-1)/10
vect <- as.numeric(h$Prop)

options(mc.cores = 6)

schools_dat <- list(N = 113, 
                    Y = c(h$Propad))

#Fittting the model using Stan
fit1 <- stan(file = 'HMC1.stan', chains = 6, iter= 100000, data = schools_dat)
fit2 <- stan(file = 'HMC2.stan', chains = 6, iter= 100000, data = schools_dat)

#Calculating WAIC
logLikehood1 <- extract_log_lik(fit1, 'log_lik')
waic1 <- waic(logLikehood1)
print(waic1)
logLikehood2 <- extract_log_lik(fit2, 'log_lik')
waic2 <- waic(logLikehood2)
print(waic2)
#Comparing WAIC
loo_compare(waic1, waic2)
#Calculating PSIS-LOO
loo1 <- loo(fit1)
loo2 <- loo(fit2)
print(loo2)
#Comparing PSIS-LOO
loo_compare(loo1,loo2)

#Use shinystan for visualisation of model
aFit1 <- as.shinystan(fit1)
aFit2 <- as.shinystan(fit2)
launch <- launch_shinystan(aFit1)
launch <- launch_shinystan(aFit2)
