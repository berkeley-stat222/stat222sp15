##------------------
# Assume Theta = 0.2
theta <- 0.2
prob = theta*2/3+2/9

mean(sim_Y)
Include<-NULL ##check if interval include true parameter
for (j in 1:100){
  sim_Y = rbinom(117,1,prob) 
  Boot.sample<-NULL
  for (i in 1:10000){
    
    mean(sim_Y)
    stat1 <- mean(sample(sim_Y,size = length(sim_Y),replace = T))
    
    Boot.sample[i]=(9*stat1-2)/6
    
  }
  Boot.sample[which(Boot.sample>1)] = 1
  Boot.sample[which(Boot.sample<0)] = 0
  hist(Boot.sample)
  quan<-quantile(Boot.sample,c(0.025,0.975))
  if (theta>quan[2] | theta<quan[1]){
    Include[j] = FALSE
  }
  else Include[j] = TRUE
  
}

##





