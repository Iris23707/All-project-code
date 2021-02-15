library(lattice)
library(Hmisc)
library(car)
library(tidyverse)
library(broom)
library(Metrics)
library(qcc)
library(MASS)

# Part1
OnlineNewsPopularity <- read.csv("D:/UQ semester2/Data 7202/Assignment 1/OnlineNewsPopularity/OnlineNewsPopularity.csv")
ONP<-OnlineNewsPopularity
attach(ONP)


#Q1

summary(ONP)
#Find all attributes' outliers or error values.
boxplot(n_tokens_content,col = "green", main = "n_tokens_content")
boxplot(n_unique_tokens,col = "green", main = "n_unique_tokens")
boxplot(n_non_stop_words,col = "green", main = "n_non_stop_words")
boxplot(n_non_stop_unique_tokens,col = "green", main = "n_non_stop_unique_tokens")

#Delete the unusable data and outliers
data_set <- ONP[,!names(ONP) %in% c("url","timedelta")]
data_set <- data_set[data_set$n_non_stop_unique_tokens != max(n_non_stop_unique_tokens),]

#Delete negative values.
data_set <- data_set[,!names(data_set) %in% "kw_min_min"]
data_set <- data_set[data_set$kw_avg_min >= 0 & data_set$kw_min_avg >= 0,]

head(data_set)

#Poisson

##Try first construction
glm1 <- glm(shares ~ .,family=poisson(link = 'sqrt'),data= data_set) 
summary(glm1)

##Try second construction
data_set1 <- data_set[,!names(data_set) %in% c("weekday_is_sunday","is_weekend", "LDA_04")]
glm2 <- glm(shares ~ .,family=poisson(link = 'sqrt'),data= data_set1) 
summary(glm2)

##Using VIF test to check the variance inflation factor.
vif_test <- vif(glm2)
vif_test

##Delete all the variables which their variance inflation factor is larger than 10 and reconstruct the model.
data_set2 <- data_set1[,!names(data_set1) %in% c("n_unique_tokens",
                                              "n_non_stop_words", 
                                              "n_non_stop_unique_tokens",
                                              "average_token_length",
                                              "kw_max_min",
                                              "kw_avg_min",
                                              "kw_avg_avg",
                                              "self_reference_avg_sharess",
                                              "rate_positive_words",
                                              "rate_negative_words")]

glm3 <- glm(shares ~ .,family=poisson(link = 'sqrt'),data= data_set2) 
summary(glm3) #AIC:231557948

# over divergence examination
qcc.overdispersion.test(shares,type = 'poisson')

vif_test1 <- vif(glm3)
vif_test1

##Poisson RMSE
poisson_result <- glm3$fitted.values
rmse(shares,poisson_result) #11661.01

##Poisson R^2
poisson_r2 <- 1-glm3$deviance/glm3$null.deviance
poisson_r2 #0.101801


#Gamma

gamma1 <- glm(shares ~ .,family=Gamma(link = 'log'),data= data_set2)
summary(gamma1) #AIC: 702279

vif(gamma1)

##Gamma RMSE
gamma_result <- gamma1$fitted.values
rmse(shares,gamma_result) #94724.52

##Gamma R^2
gamma_r2 <- 1-gamma1$deviance/gamma1$null.deviance
gamma_r2 #0.1441833

#Gaussian
gaussian1 <- glm(shares ~ .,family=gaussian(link = 'identity'),data= data_set2)
summary(gaussian1) #AIC: 836616

vif(gaussian1)

##Gaussian RMSE
gaussian_result <- gaussian1$fitted.values
rmse(shares,gaussian_result) #11628.08

##Gaussian R^2
gaussian_r2 <- 1-gaussian1$deviance/gaussian1$null.deviance
gaussian_r2 #0.01900314

# negative binomial
negative_binominal <- glm.nb(shares~.,data = data_set2)
summary(negative_binominal) #AIC: 701818
plot(negative_binominal$fitted.values)
plot(negative_binominal$residuals)
rmse(shares, negative_binominal$fitted.values) #94012.61
negative_binominal_r2 <- 1 - negative_binominal$deviance / negative_binominal$null.deviance
negative_binominal_r2 #0.1441977

#Q2
##lm
lm <- lm(shares ~ ., data = data_set2)
summary(lm) #R^2=0.019

step(lm) #Start:  AIC=726493.3, End: AIC=726471.6

lm_result <- lm$fitted.values
rmse(shares,lm_result) #11628.08

par(mfrow = c(2,2))
plot(lm)

#transform data on "shares"
data_set3 <- data_set2

data_set3$shares = log(data_set3$shares+1)
lm1 <- lm(shares~., data = data_set3)
summary(lm1)

#transform data on other variables whose p-value is over 0.05
data_set3$n_tokens_title <- log(data_set3$n_tokens_title+1)
data_set3$n_tokens_content <- log(data_set3$n_tokens_content+1)
data_set3$num_videos <- log(data_set3$num_videos+1)
data_set3$LDA_01 <- log(data_set3$LDA_01+1)
data_set3$LDA_03 <- log(data_set3$LDA_03+1)
data_set3$global_rate_positive_words <- log(data_set3$global_rate_positive_words+1)
data_set3$global_rate_negative_words <- log(data_set3$global_rate_negative_words+1)
data_set3$avg_positive_polarity <- log(data_set3$avg_positive_polarity+1)
data_set3$max_positive_polarity <- log(data_set3$max_positive_polarity+1)
data_set3$abs_title_sentiment_polarity <- log(data_set3$abs_title_sentiment_polarity+1)
ds <- data_set3

#plot of lm after transformation
lm2 <- lm(shares~., data = ds)
summary(lm2)
par(mfrow = c(2,2))
plot(lm2)
AIC(lm2) #100151.9

##gamma plot
par(mfrow = c(2,2))
plot(gamma1)

#plot of glm after transformation
gamma2 <- glm(shares ~ .,family=Gamma(link = 'log'),data= ds)
AIC(gamma2) #97532.19 
par(mfrow = c(2,2))
plot(gamma2)

#95% predective interval before transformation
##multiple linear regression
lm_predict=predict(lm,data_set2,interval = 'predict',level = 0.95,se.fit = TRUE)
lwlm=lm_predict$fit-1.96*lm_predict$se.fit
uplm=lm_predict$fit+1.96*lm_predict$se.fit
lmfit=cbind(lm_predict$fit,lwlm,uplm)
lmfit=lmfit[order(lmfit[,1]),]
matplot(lmfit,type = 'l',lty=1:3,col = 2:4, main='95% predective interval for multiple linear regression model')

##gamma distribution
gamma_predict=predict(gamma1,data_set2,interval = 'predict',level = 0.95,se.fit = TRUE)
lwgm=gamma_predict$fit-1.96*gamma_predict$se.fit
upgm=gamma_predict$fit+1.96*gamma_predict$se.fit
gmfit=cbind(gamma_predict$fit,lwgm,upgm)
gmfit=gmfit[order(gmfit[,1]),]
matplot(gmfit,type = 'l',lty=1:3,col = 2:4, main='95% predective interval for gamma distribution model')


#95% predective interval after transformation
##multiple linear regression
lm_predict1=predict(lm,ds,interval = 'predict',level = 0.95,se.fit = TRUE)
lwlm1=lm_predict1$fit-1.96*lm_predict1$se.fit
uplm1=lm_predict1$fit+1.96*lm_predict1$se.fit
lmfit1=cbind(lm_predict1$fit,lwlm1,uplm1)
lmfit1=lmfit1[order(lmfit1[,1]),]
matplot(lmfit1,type = 'l',lty=1:3,col = 2:4, main='95% predective interval for multiple linear regression model')

##gamma distribution
gamma_predict1=predict(gamma1,ds,interval = 'predict',level = 0.95,se.fit = TRUE)
lwgm1=gamma_predict1$fit-1.96*gamma_predict1$se.fit
upgm1=gamma_predict1$fit+1.96*gamma_predict1$se.fit
gmfit1=cbind(gamma_predict1$fit,lwgm1,upgm1)
gmfit1=gmfit1[order(gmfit1[,1]),]
matplot(gmfit1,type = 'l',lty=1:3,col = 2:4, main='95% predective interval for gamma distribution model')
