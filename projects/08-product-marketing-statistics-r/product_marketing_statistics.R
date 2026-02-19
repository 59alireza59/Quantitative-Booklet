
```r
DATA_FILE <- file.path("..", "..", "data", "product-marketing", "store.csv")
store.df <- read.delim(DATA_FILE, header = TRUE)

str(store.df)
summary(store.df)
head(store.df, 10)
tail(store.df, 10)

hist(
  store.df$p1sales,
  main = "Product 1 Weekly Sales Frequencies at All Stores",
  xlab = "Product 1 Sales (Units)",
  ylab = "Relative frequency",
  breaks = 30,
  freq = FALSE,
  xaxt = "n"
)
axis(side = 1, at = seq(60, 300, by = 20))
lines(density(store.df$p1sales, bw = 10), type = "l", lwd = 2)

boxplot(
  store.df$p2sales ~ store.df$storeNum,
  horizontal = TRUE,
  ylab = "Store",
  xlab = "Weekly unit sales",
  las = 1,
  main = "Weekly Sales of the Second Product by Store"
)

plot(
  ecdf(store.df$p1sales),
  main = "Cumulative distribution of the first product weekly sales",
  ylab = "Cumulative Proportion",
  xlab = c("First Product weekly sales at all stores",
           "90% of weeks sold <= 90th percentile"),
  yaxt = "n"
)
axis(side = 2, at = seq(0, 1, by = 0.1), las = 1,
     labels = paste(seq(0, 100, by = 10), "%", sep = ""))
abline(h = 0.9, lty = 3)
abline(v = quantile(store.df$p1sales, probs = 0.9), lty = 3)

print(by(store.df$p1sales, store.df$storeNum, mean))
print(by(store.df$p1sales, list(store.df$storeNum, store.df$Year), mean))
