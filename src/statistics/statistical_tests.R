#install.packages('EnvStats')
#install.packages("zoo")
#install.packages("twosamples")

library(zoo)
library(readxl)
library(EnvStats)
library(twosamples)
propdata <- read_excel("Propdata.xlsx")

beta <- 1
n <- length(propdata$Prop)
n
sum <- sum(log(propdata$Prop))
alphaMLE <- n/(sum-n*log(beta))
alphaMVUE <- (n-1)/sum-n*log(beta)

z = c()
for (i in 1:114){
  z[i] <- dpareto(1, 1, shape=alphaMVUE)
}

paretoPDF <- rpareto(100000, 1, shape=alphaMVUE)



x2 <- chisq.test(propdata$Prop, p=paretoPDF, rescale.p = TRUE, simulate.p.value=TRUE)
x3 <- ks.test(propdata$Prop, paretoPDF)
x33 <- ks_test(propdata$Prop, paretoPDF, n=1000)
x33
x4 <- cvm_test(propdata$Prop,paretoPDF, n=1000)
x4
x5 <- ad_test(propdata$Prop, paretoPDF, n=1000)
x5

