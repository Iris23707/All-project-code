library(ggplot2) 
library(tseries) 
library(forecast) 
library(Metrics) 
library(MLmetrics) 
library(stats) 
library(lmtest) 
library(FitAR)

flow1.path <- 'D:/UQ semester2/Data 7202/Assignment 2/DATA7202_2020_translink_upload/flow_20130225-20130303.csv'
flow1 <- read.csv(flow1.path,skip = 1)
flow2.path <- 'D:/UQ semester2/Data 7202/Assignment 2/DATA7202_2020_translink_upload/flow_20130304-20130310.csv'
flow2 <- read.csv(flow2.path,skip = 1)
flow3.path <- 'D:/UQ semester2/Data 7202/Assignment 2/DATA7202_2020_translink_upload/flow_20130311-20130317.csv'
flow3 <- read.csv(flow3.path,skip = 1)
flow4.path <- 'D:/UQ semester2/Data 7202/Assignment 2/DATA7202_2020_translink_upload/flow_20130318-20130324.csv'
flow4 <- read.csv(flow4.path,skip = 1)

flow <- rbind(flow1,flow2,flow3,flow4)
View(flow)

# fliter region 1-5
flow <- flow[flow$region_from == 1,]
flow <- flow[flow$region_to == 5,]
nrow(flow) #576
ncol(flow)

#original data
flow<- flow[1:7]

train <- ts(flow$v0_num_traj,frequency = 19) #1-5 are noise
plot(train) #original data

#the first type model
pred_mean <- aggregate(v0_num_traj~time_id, data=flow, mean)
pred_mean
plot(pred_mean)

# find seasonality
train_decomposition <- decompose(train)
plot(train_decomposition)

#find stationary
adf.test(train) #d=0


#choose parameters by acf and pacf of original data
acf(train, lag.max = 80)
pacf(train,lag.max = 80)


# choose parameters by acf and pacf of the data after difference
##d=1
diff_seasonal <- diff(train,lag = 1) 
plot(diff_seasonal)
rmse(diff_seasonal,train) #103.2569

###acf,d=1
acf(diff_seasonal,lag.max = 80) #p=1
###pacf,d=1
pacf(diff_seasonal,lag.max = 80)#q=2

##d=2
diff_seasonal_2 <- diff(train,lag = 2) 
plot(diff_seasonal_2)
rmse(diff_seasonal_2,train) #103.3175


#auto-arima
arima_auto <- auto.arima(train,test = 'adf', ic = 'aic', trace = T) #(1,0,1)(1,0,0)
arima_auto

# p=1, d=0, q=1
arima_auto_fit <- Arima(train,order = c(1,0,1),seasonal=c(1,0,0)) 
arima_auto_fit


# p=1,d=1,q=2
arima_fit <- Arima(train,order = c(1,1,2),seasonal=c(1,0,0))
arima_fit

#Q5
checkresiduals(arima_fit)

#Q7
#predict next 19 hours
next_day_fitted <- forecast(arima_fit,h=19,level=c(95))
next_day_fitted
next_day_fitted_value <- round(next_day_fitted$mean,0)
next_day_fitted_value
autoplot(forecast(next_day_fitted))

real <- c(2,18,34,68)
predicted <-c(1,0,0,0) 
MSE(real,predicted)

#Q8



# data of work days
flow_work1<- flow1[1:65813,]
flow_work2<- flow2[1:65153,]
flow_work3<- flow3[1:65812,]
flow_work4<- flow4[1:65479,]

flow_work <- rbind(flow_work1,flow_work2,flow_work3,flow_work3)
View(flow_work)

# fliter region 1-5 of work days data
flow_work <- flow_work[flow_work$region_from == 1,]
flow_work <- flow_work[flow_work$region_to == 5,]

flow_work<- flow_work[1:7]

train_work_days <- ts(flow_work$v0_num_traj,frequency = 19) #1-5 are noise
plot(train_work_days)



#the first type model of work days data
pred_mean_work <- aggregate(v0_num_traj~time_id, data=flow_work, mean)
pred_mean_work
plot(pred_mean_work)

# find seasonality
train_work_decomposition <- decompose(train_work_days)
plot(train_work_decomposition)

#find stationary
adf.test(train_work_days)

#choose parameters by acf and pacf of original data
acf(train_work_days, lag.max = 80)
pacf(train_work_days,lag.max = 80)


# choose parameters by acf and pacf of the work days data after difference
##d=1
diff_seasonal_work <- diff(train_work_days,lag = 1) 
plot(diff_seasonal_work)
rmse(diff_seasonal_work,train_work_days) #103.7794

###acf
acf(diff_seasonal_work,lag.max = 80) #p=1
###pacf
pacf(diff_seasonal_work,lag.max = 80)#q=2

##d=2
diff_seasonal_work_2 <- diff(diff_seasonal_work,lag = 2) 
plot(diff_seasonal_work_2)
rmse(diff_seasonal_work_2,train_work_days) #131.4262

#auto-arima
arima_auto_work <- auto.arima(train_work_days,test = 'adf', ic = 'aic', trace = T)
arima_auto_work

# p=1, d=0, q=1
arima_auto_fit_work <- Arima(train_work_days,order = c(1,0,1),seasonal = c(0,1,1))
arima_auto_fit_work

# p=1, d=1, q=2
arima_fit_work <- Arima(train_work_days,order = c(1,1,2),seasonal = c(0,1,1))
arima_fit_work

#Q5
checkresiduals(arima_fit_work)

#Q7
#predict next 19 hours
next_workday_fitted <- forecast(arima_fit_work,h=19,level=c(95))
next_workday_fitted
next_workday_fitted_value <- round(next_workday_fitted$mean,0)
next_workday_fitted_value
autoplot(forecast(next_workday_fitted))

# data of day time(time_id from 6 to 18)
train_day_time <- ts(flow$v0_num_traj,frequency = 12)
plot(train_day_time) #original data

#the first type model
pred_mean_daytime <- aggregate(v0_num_traj~time_id, data=flow, mean)
pred_mean_daytime
plot(pred_mean_daytime)


# find seasonality
train_decomposition_daytime <- decompose(train_day_time)
plot(train_decomposition_daytime)

#find stationary
adf.test(train_day_time) #d=0


#choose parameters by acf and pacf of original data
acf(train_day_time, lag.max = 80)
pacf(train_day_time,lag.max = 80)

# choose parameters by acf and pacf of the day time data after difference
##d=1
diff_seasonal_daytime <- diff(train_day_time,lag = 1) 
plot(diff_seasonal_daytime)
rmse(diff_seasonal_daytime,train_day_time) #103.2569

###acf
acf(diff_seasonal_daytime,lag.max = 80) #p=1
###pacf
pacf(diff_seasonal_daytime,lag.max = 80)#q=2

##d=2
diff_seasonal_daytime_2 <- diff(train_day_time,lag = 2) 
plot(diff_seasonal_daytime_2)
rmse(diff_seasonal_daytime_2,train_day_time) #131.4262

#auto-arima
arima_auto_daytime <- auto.arima(train_day_time,test = 'adf', ic = 'aic', trace = T)
arima_auto_daytime

# p=4, d=0, q=5
arima_auto_fit_daytime <- Arima(train_day_time,order = c(4,0,5),seasonal = c(2,0,1))
arima_auto_fit_daytime

# p=1, d=1, q=2
arima_fit_daytime <- Arima(train_day_time,order = c(1,1,2),seasonal = c(2,0,1))
arima_fit_daytime

#Q5
checkresiduals(arima_fit_daytime)

#Q7
#predict next 19 hours
next_daytime_fitted <- forecast(arima_fit_daytime,h=19,level=c(95))
next_daytime_fitted
next_daytime_fitted_value <- round(next_daytime_fitted$mean,0)
next_daytime_fitted_value
autoplot(forecast(next_daytime_fitted))

#Q8
flow_select<- flow_work[,c("date","time_id","v0_num_traj")]
flow_sub<- subset(flow_select,time_id>=6)

# Build the 1 hour ahead predict model:
i = 1
one_hour_predict = vector()
for (index in (nrow(flow_sub)-19):(nrow(flow_sub)-1)){
  v0 = train_work_days[1:index]
  arima_model_predict = arima(v0, order = c(1,1,2),seasonal = list(order = c(0,1,1), period=19))
  one_hour_predict[i] = forecast(arima_model_predict,h=1)$mean[1:1]
  i = i + 1
}
one_hour_predict

#Reform the dataset and make predict value together with actual value for comparing
Compare_data_one_hour = data.frame(one_hour_predict,train_work_days[(nrow(flow_sub)-18):(nrow(flow_sub))])
Compare_data_one_hour = cbind(flow_sub$date[(nrow(flow_sub)-18):(nrow(flow_sub))],
                            flow_sub$time_id[(nrow(flow_sub)-18):(nrow(flow_sub))],
                            Compare_data_one_hour)
names(Compare_data_one_hour)[1] <- "date"
names(Compare_data_one_hour)[2] <- "time"
names(Compare_data_one_hour)[3] <- "Predict passenger flow"
names(Compare_data_one_hour)[4] <- "Actual passenger flow"
Compare_data_one_hour

#Calculate the MSE for 1 hour ahead predict
mse(one_hour_predict,train_work_days[(nrow(flow_sub)-18):(nrow(flow_sub))])

# Build the 2 hours ahead predict model:
j = 1
two_hours_predict = vector()
for (index in (nrow(flow_sub)-20):(nrow(flow_sub)-2)){
  v0_2_hours = train_work_days[1:index]
  arima_model_predict_2_hours = arima(v0_2_hours, order = c(1,1,2),seasonal = list(order = c(0,1,1), period=19))
  two_hours_predict[j] = forecast(arima_model_predict_2_hours,h=2)$mean[2:2]
  j = j + 1
}
two_hours_predict

#Reform the dataset and make predict value together with actual value for comparing
Compare_data_two_hour = data.frame(two_hours_predict,train_work_days[(nrow(flow_sub)-18):(nrow(flow_sub))])
Compare_data_two_hour = cbind(flow_sub$date[(nrow(flow_sub)-18):(nrow(flow_sub))],
                            flow_sub$time_id[(nrow(flow_sub)-18):(nrow(flow_sub))],
                            Compare_data_two_hour)
names(Compare_data_two_hour)[1] <- "date"
names(Compare_data_two_hour)[2] <- "time"
names(Compare_data_two_hour)[3] <- "Predict passenger flow"
names(Compare_data_two_hour)[4] <- "Actual passenger flow"
Compare_data_two_hour

#Calculate the MSE for 2 hours ahead predict
mse(two_hours_predict,train_work_days[(nrow(flow_sub)-18):(nrow(flow_sub))])


#Q9
#Add the known rows to the original data
row1 <- c("2013-03-25",6,2)
row2 <- c("2013-03-25",7,18)
row3 <- c("2013-03-25",8,34)
row4 <- c("2013-03-25",9,68)
new_data <- rbind(flow_sub,row1,row2,row3,row4)

#Transform the type of the data for building model
new_data$time_id = as.integer(new_data$time_id)
new_data$v0_num_traj = as.integer(new_data$v0_num_traj)

#Build new time series model
new_train <- ts(new_data$v0_num_traj, frequency = 19,start=c(1,1))
new_arima_model = arima(new_train, order = c(1,1,2),seasonal = list(order = c(0,1,1), period=19))

#Show the predict results
predicted_next_4_hours <- data.frame(forecast(new_arima_model,4)$mean[1:4])
time_column <- new_data[c("time_id")]
predicted_next_4_hours <- cbind(time_column[1:4,],predicted_next_4_hours)
names(predicted_next_4_hours)[1] <- "Time ID"
names(predicted_next_4_hours)[2] <- "Predict passenger flow"
predicted_next_4_hours

real <- c(2,18,34,68)
predicted <-c(49.15296,48.73464,51.71732,64.67783) 
RMSE(real,predicted)

#Show the predict results
predicted_next_15_hours <- data.frame(forecast(new_arima_model,15)$mean[1:15])
time_column_1 <- new_data[c("time_id")]
predicted_next_15_hours <- cbind(time_column_1[1:15,],predicted_next_15_hours)
names(predicted_next_15_hours)[1] <- "Time ID"
names(predicted_next_15_hours)[2] <- "Predict passenger flow"
predicted_next_15_hours

