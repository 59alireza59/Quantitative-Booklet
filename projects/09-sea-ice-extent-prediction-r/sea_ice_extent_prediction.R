
### Create file: `projects/09-sea-ice-extent-prediction-r/sea_ice_extent_prediction.R`
```r
library(dplyr)
library(zoo)
library(ggplot2)
library(forecast)
library(xts)
library(gridExtra)

DATA_FILE <- file.path("..", "..", "data", "sea-ice", "seaice.csv")
theData <- read.csv(DATA_FILE, header = TRUE, sep = ",")

theData$DateTime <- as.POSIXct(
  paste0(sprintf("%02d", theData$Day), sprintf("%02d", theData$Month), theData$Year),
  format = "%d%m%Y",
  tz = "UTC"
)

theDataNorth <- theData %>%
  filter(hemisphere == "north") %>%
  group_by(Year, Month)

ggplot(theDataNorth, aes(x = DateTime, y = Extent, col = hemisphere)) +
  geom_line() +
  labs(x = "Year", y = "Northern Hemisphere Ice Extent (10^6 sq km)") +
  ggtitle("Northern Hemisphere Ice Extent by Day (1978–2015)")

northAsst <- aggregate(Extent ~ Month + Year, theDataNorth, mean)
northData_ts <- ts(northAsst$Extent, frequency = 12, start = c(1978, 10), end = c(2020, 12))

northSample <- window(northData_ts, end = c(2015, 12))
northFit <- window(northData_ts, end = c(2012, 12))

northSeasonal <- decompose(northSample)
autoplot(northSeasonal) + ggtitle("Northern Hemisphere")

northModelling <- auto.arima(northFit, lambda = 0, d = 0, D = 1, max.order = 4,
                            stepwise = FALSE, approximation = FALSE)
northForecast <- forecast(northModelling, h = 360)
autoplot(northForecast, xlab = "Time", ylab = "Ice Extent of Northern Hemisphere")
