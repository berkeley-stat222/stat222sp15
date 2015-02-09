## Five ways to remove rows with any NAs from a data frame
## (Example by Phil Spector)

## Starts with NULL, loops over rows, adding each
## row if there are no NAs in it
funAgg <- function(x){
  res <- NULL
  n <- nrow(x)
  for (i in 1:n){
    if (!any(is.na(x[i,]))) res <- rbind(res, x[i,])
  }
  return(res)
}

## Creating vector drop (same as in funOmit)
## Method for creating vector is to make
## a logical matrix (is.na(x)) and then
## using apply to the rows
funApply <- function(x) {
 drop <- apply(is.na(x), 1, any)
 x[!drop, ]
}

## Initializes res by making a copy of x
## Looping over rows, replacing elements of res
## corresponding to rows in x without NAs
funLoop <- function(x){
  res <- x
  n <- nrow(x)
  k <- 0
  for (i in 1:n) {
    if (!any(is.na(x[i,]))) {
      k <- k + 1
      res[k, ] <- x[i,]
    }
  }
  res[1:k, ]
}

## Loops over columns
## Create vector drop - logical,
## elements are TRUE if any NA in the
## corresponding row
funOmit <- function(x) {
 drop <- FALSE
 n <- ncol(x)
 for (i in 1:n)
   drop <- drop | is.na(x[, i])
 x[!drop, ]
}

## Uses rowMeans to generate logical
## vector (similar to drop)
## Uses fact that mean(y) is NA if any
## elements of y are NA
funRow <- function(x) {
 return(x[!is.na(rowMeans(x)), ])
}

## Make up large test case

xx <- matrix(runif(100000), ncol = 10)
xx[xx>.95] <- NA # we will have about 5% NAs
x <- as.data.frame(xx)
x[1:10,]

## Compare timings

system.time(y1 <- funAgg(x)) # 16.812
system.time(y2 <- funApply(x)) # 0.029 
system.time(y3 <- funLoop(x)) # 10.101
system.time(y4 <- funOmit(x)) # 0.006
system.time(y5 <- funRow(x)) # 0.008

## Using Rprof to see how a function
## spends its time

Rprof("aggfile")
y <- funAgg(x)
Rprof(NULL)
summaryRprof("aggfile")

 
