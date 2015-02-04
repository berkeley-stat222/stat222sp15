
# Calculate MLE from mean of data vector
mleRR <- function(ybar){
  pmin(pmax(3/2*(ybar-2/9), 0), 1)
}

# Simulate B bootstrap MLEs - nonparametric bootstrap
bootsim1 <- function(y, B){
  ysim <- replicate(B, sample(y, size = length(y), replace = TRUE))
  mleRR(colMeans(ysim))
}

# Simulate B bootstrap MLEs - parametric bootstrap 
# Mathematically equivalent to nonparametric bootstrap for this problem
bootsim2 <- function(y, B){
  ybarsim <- rbinom(B, size = length(y), prob = mean(y))/length(y)
  mleRR(ybarsim)
}

system.time(print(summary(bootsim1(y = c(0,0,1,1), B = 10000))))
system.time(print(summary(bootsim2(y = c(0,0,1,1), B = 10000)))) # much faster

# Approximate empirical coverage of 95%
# bootstrap interval for data of size n
# N = number of simulated datasets
# B = number of bootstrap samples
bootcover <- function(theta, n, N = 1000, B = 1000){
  p <- 2/3 * theta + 2/9
  simvec <- sample(c(0,1), size=n*N, replace=T, prob=c(1-p, p))
  simmat <- matrix(simvec, nrow = N)
  bootmles <- apply(simmat, 1, bootsim2, B = B)
  bootints <- apply(bootmles, 2, quantile, prob = c(0.025, 0.975))
  mean(theta > bootints[1,] & theta < bootints[2,])
}

# compare timing with original file
system.time(bootcover(theta = 0.2, n = 117, N = 100, B = 10000))
system.time(source("script2-before.R"))

# Note it would be more accurate to bump N up to at least 1000



