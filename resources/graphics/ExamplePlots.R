
##################
# Supernova data #
##################

load("SN2001fe.RData")
head(SN2001fe)

# Put spectra into a matrix, one per column
length(unique(SN2001fe$phase))
m <- matrix(SN2001fe$flux, ncol = 25)

# Add an offset to each column
m <- m + rep(0.1*(unique(SN2001fe$phase)), each = nrow(m))

# Plot

quartz(width = 8, height = 10)
matplot(log(unique(SN2001fe$wavelength)), m, 
        type = "l", col = 1, lty = 1,
        xlab = "Wavelength (log scale)", ylab = "Day", 
        xaxt = "n", yaxt = "n")
range(SN2001fe$phase)
axis(2, at = 0.1*(seq(-15, 25, by = 5)), labels = seq(-15, 25, by = 5))
axis(1, at = log(c(3000, 4000, 5000, 6000, 7000, 8000, 9000)), 
     labels = c(3000, 4000, 5000, 6000, 7000, 8000, 9000))
abline(v = log(c(5950,6300)), lty = 2)
checking <- which(unique(SN2001fe$wavelength) >= 5950 & unique(SN2001fe$wavelength) <= 6300)
sapply(1:25, function(i){
  ok <- which(m[checking, i] == min(m[checking, i]))
  points(log(unique(SN2001fe$wavelength))[checking][ok], m[checking[ok], i], pch = 16)
})

dev.print(pdf, height = 8, width = 10, file = "fluxes.pdf")
dev.off()

################
# Birdflu data #
################

rm(list = ls())
load("turkeySpObjects.RData")
ls()

class(turkeyLonLatGrid)
head(turkeyLonLatGrid@data)
class(turkeyBird)
head(turkeyBird@data)

# Overlay two density estimates for two vectors
densitycompare <- function(x1, x2, from = NULL, to = NULL,
                           xlab = "", log10 = FALSE, eps = 0, ylim = NULL,
                           adjust1 = 1, adjust2 = 1, legendloc = "topright"){
  if(is.null(from)) from <- min(c(x1, x2), na.rm = TRUE)
  if(is.null(to)) to <- max(c(x1, x2), na.rm = TRUE)
  if(log10) {
    x1 <- log(x1+eps, base = 10)
    x2 <- log(x2+eps, base = 10)
    from <- log(from+eps, base = 10)
    to <- log(to+eps, base = 10)
  }
  x1 <- x1[!is.na(x1)]; x2 <- x2[!is.na(x2)]
  d1 <- density(x1, from = from, to = to, adjust = adjust1)
  d2 <- density(x2, from = from, to = to, adjust = adjust2)
  if(is.null(ylim)) ylim <- range(c(d1$y, d2$y))
  plot(d1, ylim = ylim, type = "n", main = "",
       xlab = xlab, xaxt = if(log10) "n" else "s")
  if(log10) axis(1, at = pretty(c(from, to)), labels = 10^pretty(c(from, to)))
  polygon(x = c(d1$x, d1$x[length(d1$x):1]), y = c(d1$y, rep(0, length(d1$y))),
          col = rgb(0, 0, 1, alpha = 0.1))
  polygon(x = c(d2$x, d2$x[length(d1$x):1]), y = c(d2$y, rep(0, length(d2$y))),
          col = rgb(1, 0, 0, alpha = 0.1))
  legend(legendloc, bty = "n", fill = rgb(c(0, 1), c(0, 0), c(1, 0), alpha = 0.2),
         legend = c("All locations", "Outbreak locations"))
  return(NULL)
}

quartz(width = 10, height = 5)
par(mfrow = c(1, 2), mar = c(4, 4, 4, 1), cex = 1.05)
densitycompare(turkeyLonLatGrid$poultryPopDens, turkeyBird$poultryPopDens,
               log10 = TRUE, eps = 0.001,
               from = 0, to = 30000, ylim = c(0, 1),
               xlab = expression("Poultry/km"^2), legendloc = "topleft")
title(main = "(a) Estimated poultry population")
densitycompare(turkeyLonLatGrid$humanPopDens, turkeyBird$humanPopDens,
               log10 = TRUE, eps = 0.001,
               from = 0, to = 30000, ylim = c(0, 1),
               xlab = expression("People/km"^2), 
               adjust1 = 10, legendloc = "topleft")
title(main = "(b) Estimated human population")
dev.print(pdf, height = 5, width = 10, file = "densities.pdf")
dev.off()

# Example 2 - a map
## First figure out categories for population density (human and poultry)

hist(log(humanPopulation$popdens, base = 10))
hist(log(poultryPopulation$popdens, base = 10))
breaks <- c(0, 10^seq(0, 4.5, by = 0.5))
pal <- gray(seq(1, 0.1, length = length(breaks)-1))
humanPopulation$category <- as.numeric(cut(humanPopulation@data$popdens,
                                           breaks = breaks, include.lowest = TRUE))
poultryPopulation$category <- as.numeric(cut(poultryPopulation@data$popdens,
                                             breaks = breaks, include.lowest = TRUE))

## Now back to the plot

quartz(width = 10, height = 4)
par(mar = rep(0, 4), oma = c(0, 0, 0, 5), xpd = NA)
plot(turkey)
image(humanPopulation["category"], col = pal, add = TRUE) # slow
plot(turkey, add = TRUE)
plot(turkeyLakes, add = TRUE, col = "lightblue", border = "lightblue")
plot(turkeyRoad[turkeyRoad$RTT_DESCRI!="Primary Route",], col = "darkolivegreen", add = TRUE, lwd = 0.5)
plot(turkeyRoad[turkeyRoad$RTT_DESCRI=="Primary Route",], col = "darkolivegreen", add = TRUE, lwd = 2)
#plot(turkeyRail, col = "darkolivegreen", lwd = 2, lty = 2, add = TRUE)
plot(turkeyPorts, pch = 19, col = "yellow", add = TRUE)
plot(turkeyPorts, pch = 1, add = TRUE)
plot(turkeyBird, col = "red", cex = 0.8, pch = "+", add = TRUE)
par(oma = rep(0, 4))
library(fields)
image.plot(legend.only = TRUE, zlim = c(-0.5, 4.5),
           axis.args = list(at = 0:4, labels = 10^(0:4)),
           col = pal, legend.shrink = 0.6)

dev.print(pdf, file = "turkeysitemap.pdf", height = 4, width = 10)
dev.off()

##################
## Coweeta data ##
##################

rm(list = ls())
load("CoweetaLocs.RData")
load("CoweetaTimes.RData")

x11(width = 10, height = 4)
layout(matrix(c(1, 2), 1, 2, byrow = TRUE), widths = c(2, 3), heights = 2)
par(mar = rep(0, 4))

col <- c("gold", "dodgerblue2", "cyan", "red", "darkorange",
         "darkorchid1", "aquamarine4", "chartreuse2", "lightpink2")

## DEM

library(fields)
library(date)
image(as.image(Z = topo$elev, ind = topo[,1:2],
               nrow = length(unique(topo$x)),
               ncol = length(unique(topo$y))),
      xaxt = "n", yaxt = "n", bty = "n", col = gray.colors(64, start = .1))

## Measurement locations
ind <- siteinfo$study == 3033
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[2], pch = 16, cex = 1.2)
ind <- siteinfo$study == 3034
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[3], pch = 16, cex = 1.2)
ind <- siteinfo$study == 1011
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[1], pch = 16, cex = 1.2)
ind <- siteinfo$study == 1040
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[6], pch = 16, cex = 1.2)
ind <- siteinfo$study == "gaps" & substring(siteinfo$site, 1, 1) != "J"
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[8], pch = 16, cex = 1.2)
ind <- siteinfo$study == "gaps" & substring(siteinfo$site, 1, 1) == "J"
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[7], pch = 16, cex = 1.2)
ind <- siteinfo$study == 1095
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[9], pch = 16, cex = 1.2)
ind <- siteinfo$study == 1013
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[5], pch = 16, cex = 1.3)
ind <- siteinfo$study == 1023
points(siteinfo$xutm[ind], siteinfo$yutm[ind], col = col[4], pch = 16, cex = 1.2)

nlocs <- c(1, 1, 1, 2, 2, 3, 1, 1, 1)
for(i in 1:9){
  text(locator(nlocs[i]), lab = paste("(", i, ")", sep = ""), col = col[i])
}

## Soil moisture observation times

par(mar = c(4, 1, 0, 1))

xlim <- c(-8461, 18700)
ylim <- c(0, 17)
m <- mean(xlim)

plot(times.ncdc, rep(15, length(times.ncdc)),
     xlim = xlim, ylim = ylim, col = col[1],
     xlab = "", ylab = "", xaxt = "n", yaxt = "n",
     pch = "|", bty = "n")
text(xlim[2], 15, lab = "(1)", col = col[1])
text(x = m, y = 16.5,  lab = "Temperature and Precipitation") 

points(times.weir18, rep(11, length(times.weir18)),
       pch = "|", col = col[2])
text(xlim[2], 11, lab = "(2)", col = col[2])
points(times.weir27, rep(10, length(times.weir27)),
       pch = "|", col = col[3])
text(xlim[2], 10, lab = "(3)", col = col[3])
text(x = m, y = 12.5, lab = "Streamflow") 

text(x = m, y = 7.5,  lab = "Soil moisture")
points(times.1023, rep(6, length(times.1023)),
       pch = "|", col = col[4])
text(xlim[2], 6, lab = "(4)", col = col[4])
points(times.soil.1013, rep(5, length(times.soil.1013)),
       pch = "|", col = col[5])
text(xlim[2], 5, lab = "(5)", col = col[5])
points(times.soil.1040, rep(4, length(times.soil.1040)),
       pch = "|", col = col[6])
text(xlim[2], 4, lab = "(6)", col = col[6])
points(c(times.soil.1114, times.gaps),
       rep(3, length(c(times.soil.1114, times.gaps))),
       pch = "|", col = col[7])
text(xlim[2], 3, lab = "(7)", col = col[7])
points(times.gaps, rep(2, length(times.gaps)),
       pch = "|", col = col[8])
text(xlim[2], 2, lab = "(8)", col = col[8])
points(times.soil.1095, rep(1, length(times.soil.1095)),
       pch = "|", col = col[9])
text(xlim[2], 1, lab = "(9)", col = col[9])

require(date)
axis(1, at = mdy.date(month = 1, day = 1, year = seq(1930, 2010, by = 10)),
     labels = seq(1930, 2010, by = 10))
dev.print(pdf, "file = LocsAndTimes.pdf", width = 10, height = 4)
dev.off()

## Plot locations of gaps data

x11()
par(mar = c(5, 5, 2, 2))
topo.small <- topo[topo$xutm >= 275400 & topo$xutm <= 276000 &
                     topo$yutm >= 3879900 & topo$yutm <= 3880750,]
image.plot(as.image(Z = topo.small$elev, ind = topo.small[,1:2],
                    nrow = length(unique(topo.small$x)),
                    ncol = length(unique(topo.small$y))),
           col = gray.colors(64, start = .1, end = 0.7),
           xlab = "Easting", ylab = "Northing")
for(i in 1:10){
  ok <- grep(LETTERS[i], utm.gaps$site)
  col <- ifelse(i < 10, "chartreuse2", "aquamarine4")
  points(utm.gaps$xutm[ok], utm.gaps$yutm[ok], col = col, pch = 16)
  text(locator(1), lab = paste("(", LETTERS[i], ")", sep = ""), col = col)
}