
```r
require(stats)
require(graphics)
require(wql)

par(mfrow = c(2, 2))
plot(Nile)
acf(Nile)
pacf(Nile)
ar(Nile)
cpgram(ar(Nile)$resid)
par(mfrow = c(1, 1))

fit_arima <- arima(Nile, c(2, 0, 0))
print(fit_arima)

NileNA <- Nile
NileNA[c(21:40, 61:80)] <- NA
print(arima(NileNA, c(2, 0, 0)))

plot(NileNA)
pred1 <- predict(arima(window(NileNA, 1871, 1890), c(2, 0, 0)), n.ahead = 20)
lines(pred1$pred, lty = 3, col = "red")
lines(pred1$pred + 2 * pred1$se, lty = 2, col = "blue")
lines(pred1$pred - 2 * pred1$se, lty = 2, col = "blue")

pred2 <- predict(arima(window(NileNA, 1871, 1930), c(2, 0, 0)), n.ahead = 20)
lines(pred2$pred, lty = 3, col = "red")
lines(pred2$pred + 2 * pred2$se, lty = 2, col = "blue")
lines(pred2$pred - 2 * pred2$se, lty = 2, col = "blue")

mk <- mannKen(Nile)
print(mk)

plot(Nile, ylab = "Flow", xlab = "")
abline(v = 1898, col = "blue")

pt <- pett(Nile)
print(pt)

Nile_pett <- ts.intersect(Nile, LakeHuron)
print(pett(Nile_pett))

par(mfrow = c(3, 1))
plot(Nile)

fit_level <- StructTS(Nile, type = "level")
print(fit_level)
lines(fitted(fit_level), lty = 2)
lines(tsSmooth(fit_level), lty = 2, col = 4)
plot(residuals(fit_level)); abline(h = 0, lty = 3)

fit_trend <- StructTS(Nile, type = "trend")
print(fit_trend)

pred <- predict(fit_level, n.ahead = 30)
ts.plot(Nile, pred$pred, pred$pred + 0.67 * pred$se, pred$pred - 0.67 * pred$se)
