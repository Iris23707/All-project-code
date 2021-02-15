library(lattice)
library(Hmisc)
library(car)
library(tidyverse)
library(broom)
library(Metrics)
library(caret)
library(pROC)

OnlineNewsPopularity <- read.csv("D:/UQ semester2/Data 7202/Assignment 1/OnlineNewsPopularity/OnlineNewsPopularity.csv")
ONP<-OnlineNewsPopularity
attach(ONP)

#1(iv)
aov_result<-aov(ONP$shares~ONP$num_hrefs+ONP$data_channel_is_tech+
                  ONP$num_hrefs*ONP$data_channel_is_tech)
summary(aov_result)
interaction.plot(ONP$num_hrefs, ONP$data_channel_is_tech, ONP$shares, fixed = TRUE, col = 2:3, leg.bty = "o", type = 'l')


#2(i)
summary(ONP)
#find all attributes' outliers or error values.
boxplot(n_unique_tokens,col = "green", main = "n_unique_tokens")
boxplot(n_non_stop_words,col = "green", main = "n_non_stop_words")
boxplot(n_non_stop_unique_tokens,col = "green", main = "n_non_stop_unique_tokens")

#delete the unusable data and outliers
data_set <- ONP[,!names(ONP) %in% c("url","timedelta")]
data_set <- data_set[data_set$n_non_stop_unique_tokens != max(n_non_stop_unique_tokens),]

#Delete negative values.
data_set <- data_set[,!names(data_set) %in% "kw_min_min"]
data_set <- data_set[data_set$kw_avg_min >= 0 & data_set$kw_min_avg >= 0,]

#Try first construction
lm1 <- lm(shares ~ ., data = data_set)
summary(lm1)

#Try second construction
data_set <- data_set[,!names(data_set) %in% c("weekday_is_sunday","is_weekend", "LDA_04")]
lm2 <- lm(shares ~ ., data = data_set)
summary(lm2)

#Using VIF test to check the variance inflation factor.
vif_test <- vif(lm2)
vif_test
#Delete all the variables which their variance inflation factor is larger than 10 and reconstruct the model.
data_set <- data_set[,!names(data_set) %in% c("n_unique_tokens",
                                              "n_non_stop_words", 
                                              "n_non_stop_unique_tokens",
                                              "average_token_length",
                                              "kw_max_min",
                                              "kw_avg_min",
                                              "kw_avg_avg",
                                              "self_reference_avg_sharess",
                                              "rate_positive_words",
                                              "rate_negative_words")]

lm3 <- lm(shares ~ ., data = data_set)
summary(lm3)
vif(lm3)


#2(ii)
#using aov function to test the interaction
aov_result1<-aov(shares~num_hrefs+data_channel_is_tech+
                   num_hrefs*data_channel_is_tech,data = data_set)
summary(aov_result1)
interaction.plot(num_hrefs, data_channel_is_tech, shares , fixed = TRUE, col = 2:3, leg.bty = "o", type = 'l')

#adding the variable "num_hrefs*data_channel_is_tech" to do linear regression.
lm4 <- lm(shares~.+num_hrefs*data_channel_is_tech, data = data_set)
summary(lm4)


#2(iii)
#making the residuals visualized.
par(mfrow = c(2,2))
plot(lm3)

#2(iv) 
#transform data on "shares"
data_set$shares = log(data_set$shares+1)
lm5 <- lm(shares~., data = data_set)
summary(lm5)

#transform data on other variables whose p-value is over 0.05
data_set$n_tokens_title <- log(data_set$n_tokens_title+1)
data_set$n_tokens_content <- log(data_set$n_tokens_content+1)
data_set$num_videos <- log(data_set$num_videos+1)
data_set$LDA_01 <- log(data_set$LDA_01+1)
data_set$LDA_03 <- log(data_set$LDA_03+1)
data_set$global_sentiment_polarity <- log(data_set$global_sentiment_polarity+1)
data_set$global_rate_positive_words <- log(data_set$global_rate_positive_words+1)
data_set$global_rate_negative_words <- log(data_set$global_rate_negative_words+1)
data_set$avg_positive_polarity <- log(data_set$avg_positive_polarity+1)
data_set$max_positive_polarity <- log(data_set$max_positive_polarity+1)
data_set$abs_title_sentiment_polarity <- log(data_set$abs_title_sentiment_polarity+1)
ds <- data_set
lm6 <- lm(shares~., data = ds)
summary(lm6)
par(mfrow = c(2,2))
plot(lm6)

#3.(ii)
data_set<-data_set[,!names(data_set) %in% c("weekday_is_monday","weekday_is_tuesday","weekday_is_wednesday","weekday_is_thursday","weekday_is_friday","weekday_is_saturday","weekday_is_sunday","self_reference_min_shares","self_reference_max_shares","self_reference_avg_sharess","is_weekend","LDA_04")]
lm5<-lm(shares~.,data=data_set)
summary(lm5)
vif(lm5)
#3(iii)
library(lm.beta)
coef<-lm.beta(lm5)
sort(coef$standardized.coefficients)

#4.
#delete columns with invalid values
news <- OnlineNewsPopularity[,-c(1)]
attach(news)
#found -1 in kw_min_min, kw_avg_min, kw_min_avg
news <- news[,-c(19,21,25)]
attach(news)
summary(news)
# logit
logit.news <- news
logit.target <- news$shares
logit.target[logit.target < 1000] = 0
logit.target[logit.target >= 1000] = 1
logit.target
plot(logit.target)

# origin model
lo.model <- glm(logit.target~., data = logit.news[,-57], family = binomial(link = 'logit'))
summary(lo.model)

# Transformation
logit.news.log <- logit.news
#logit.news.log$LDA_01 <- log(logit.news.log$LDA_01/(1 - logit.news.log$LDA_01))
#logit.news.log$LDA_02 <- log(logit.news.log$LDA_02/(1 - logit.news.log$LDA_02))
#logit.news.log$LDA_03 <- log(logit.news.log$LDA_03/(1 - logit.news.log$LDA_03))
logit.news.log$abs_title_sentiment_polarity <- log(logit.news.log$abs_title_sentiment_polarity + 1)
logit.news.log$num_hrefs <- log(logit.news.log$num_hrefs + 1)

lo.model.log <- glm(logit.target~., data = logit.news.log[,-57], family = binomial(link = 'logit'))
summary(lo.model.log)
tidy.result2 <- tidy(lo.model.log, conf.int = TRUE)
View(tidy.result2)

#5.
# multiple linear regression
lm.pred <- fitted(lm6)
lm.pred
lm.pred[lm.pred <= 0.5] <- 0
lm.pred[lm.pred > 0.5] <- 1
lm.rmse <- rmse(lm.pred, ds$shares)
lm.rmse

# logistic regression
lo.pred <- fitted(lo.model.log)
lo.pred

lo.rmse <- rmse(lo.pred, logit.target)
lo.rmse
lo.pred[lo.pred <= 0.5] <- 0
lo.pred[lo.pred > 0.5] <- 1

# confusion matrix
lo.confusionMatrix <- confusionMatrix(table(lo.pred, logit.target))
lo.confusionMatrix

#roc
lo.roc <- roc(logit.target, lo.pred)
plot(lo.roc, print.auc = TRUE, auc.polygon = TRUE, grid = c(0.1, 0.2),
     grid.col = c('green', 'red'), max.auc.polygon = TRUE, auc.polygon.col = 'yellow', print.thres = TRUE)

#7(ii)

#GLM
linear_predict_result <- lm6%>%predict(ds)
high=ONP[rownames(ONP) == which(linear_predict_result %in% max(linear_predict_result)),]
high

#logistic regression
logistic_predict_result <- predict(lo.model.log,newdata=logit.news.log,
                                   type="response")
high1=ONP[rownames(ONP) == which(logistic_predict_result %in% max(logistic_predict_result)),]
high1

#7(iii)
#GLM
fake = ONP[ONP$rate_positive_words==1,]
fake$rate_negative_words=1
fake_pred=predict(lm6,fake)
fake_high=fake[which.max(fake_pred),]
fake_high

#logistic model
max(predict(lo.model.log,ONP))
predict(lo.model.log,high1)
fake_pred1=predict(lo.model.log,fake)
fake_high1=fake[which.max(fake_pred1),]
fake_high1