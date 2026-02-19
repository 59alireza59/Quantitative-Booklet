
```r
library(dplyr)
library(plotly)

DATA_FILE <- file.path("..", "..", "data", "sea-ice", "seaice.csv")
seaiceExtent <- read.csv(DATA_FILE)

northHemisphere <- seaiceExtent %>%
  filter(hemisphere == "north") %>%
  group_by(Year, Month) %>%
  summarize(avg_extent = mean(Extent), .groups = "drop") %>%
  na.omit()

northHemisphere$Year <- as.factor(northHemisphere$Year)
northHemisphere$Month <- as.factor(northHemisphere$Month)

plot_ly(northHemisphere, x = ~Year, y = ~Month, z = ~avg_extent, color = ~Month) %>%
  add_markers() %>%
  layout(
    scene = list(
      xaxis = list(title = "Year"),
      yaxis = list(title = "Month"),
      zaxis = list(title = "Extent")
    ),
    annotations = list(
      x = 1.13, y = 1.05, text = "Month",
      xref = "paper", yref = "paper", showarrow = FALSE
    ),
    title = "North Hemisphere's Average Ice Extent"
  )
