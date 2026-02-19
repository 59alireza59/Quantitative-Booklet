
### Create file: `projects/06-climate-stations-profiling-r/climate_stations_profiling.R`
```r
# Data Profiling of Climate Stations Database by Country (R)

library(dplyr)
library(GmAMisc)
library(rlist)

DATA_DIR <- file.path("..", "..", "data", "climate-stations")
setwd(DATA_DIR)

COUNTRY_CODE <- "IT"
MIN_YEARS_1960_2010 <- 30

database <- read.csv("REGO_STAT_INFO.csv", header = FALSE, sep = ",", dec = ".")

col_names <- c(
  "stationCode_data","lat","lon","river","location","area",
  "outelev","country","nyears","nyears6010","firstyear","lastyear","var"
)

database <- lapply(list(database), setNames, col_names)
database <- as.data.frame(database[[1]][, 1:13])

country_data <- database %>%
  filter(country == COUNTRY_CODE) %>%
  filter(firstyear >= 1960 & lastyear <= 2010) %>%
  filter(nyears6010 >= MIN_YEARS_1960_2010)

stationCode_data <- country_data[1:3]
stationCode_data[, 1] <- paste0(stationCode_data[, 1], ".mrc")

theCounter <- dim(stationCode_data)[1]

filelist_Asst <- list()
for (i in 1:theCounter) {
  filelist_Asst[[i]] <- as.list(read.table(stationCode_data[i, 1], header = TRUE))
}
for (i in 1:length(filelist_Asst)) {
  filelist_Asst[[i]] <- list.append(filelist_Asst[[i]], stationCode_data[i, 1])
}

myMin <- vector()
myMax <- vector()
j <- 1
for (i in 1:length(filelist_Asst)) {
  myMin[j] <- min(filelist_Asst[[i]]$year)
  myMax[j] <- max(filelist_Asst[[i]]$year)
  j <- j + 1
}

yearMin <- min(myMin)
yearMax <- max(myMax)
myCol <- c(yearMin:yearMax)

my_matrix <- matrix(NA, dim(stationCode_data)[1], length(myCol))
colnames(my_matrix) <- myCol
my_list <- as.data.frame(my_matrix)

theCountry_List <- cbind.data.frame(stationCode_data, my_list)

xTime <- matrix(NA, 1, length(myCol))
xTime <- as.data.frame(xTime)

for (i in 1:dim(theCountry_List)[1]) {
  for (j in 4:dim(theCountry_List)[2]) {
    for (n in 1:length(filelist_Asst[[i]]$year)) {
      if (filelist_Asst[[i]]$year[n] == colnames(theCountry_List[j])) {
        theCountry_List[i, j] <- filelist_Asst[[i]]$Qmax[n]
        xTime[i, j - 3] <- filelist_Asst[[i]]$year[n]
      }
    }
  }
}

print(head(theCountry_List))
