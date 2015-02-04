# Estimating the sampling distribution.
approximate_sampling_dist = function(n, theta, N=100, plot=F){
  p = 2/3*theta + 2/9
  #simvec = sample(c(0,1), size=n*N, replace=T, prob=c(1-p, p))
  #simmat = matrix(simvec, nrow = N)
  #simmean = rowMeans(simmat)
  simmean = rbinom(N, size = n, prob = p)/n
  simulated_mles = 3/2*(simmean - 2/9)
  if (plot){
    hist(simulated_mles, freq=F)
  }
  return((sum(simulated_mles<0) + sum(simulated_mles>1))/N)
}