## Five ways to remove rows with any NAs from a data frame
## (Example by Phil Spector)

funAgg <- function(x){
  res <- NULL
  n <- nrow(x)
  for (i in 1:n){
    if (!any(is.na(x[i,]))) res <- rbind(res, x[i,])
  }
  return(res)
}

funApply <- function(x) {
 drop <- apply(is.na(x), 1, any)
 x[!drop, ]
}

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

funOmit <- function(x) {
 drop <- FALSE
 n <- ncol(x)
 for (i in 1:n)
   drop <- drop | is.na(x[, i])
 x[!drop, ]
}

funRow <- function(x) {
 return(x[!is.na(rowMeans(x)), ])
}