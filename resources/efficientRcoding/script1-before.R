# Estimating the sampling distribution.
approximate_sampling_dist = function(n, theta, N=100, plot=F){
  p = 2/3*theta + 2/9
  simulated_mles = c()
  for (i in 1:N){
    Ys = sample(c(0,1), size=n, replace=T, prob=c(1-p, p))
    theta_mle = 3/2*(mean(Ys) - 2/9)
    simulated_mles = c(simulated_mles, theta_mle)
  }
  if (plot){
    hist(simulated_mles, freq=F)
  }
  return((sum(simulated_mles<0) + sum(simulated_mles>1))/N)
}