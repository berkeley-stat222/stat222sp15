## Five ways to remove rows with any NAs from a data frame
## (Example by Phil Spector)

# Loop through rows, check for NAs in that row
# If no NAs, append row
funAgg <- function(x){
  res <- NULL
  n <- nrow(x)
  for (i in 1:n){
    if (!any(is.na(x[i,]))) res <- rbind(res, x[i,])
  }
  return(res)
}

# Creates drop vector by applying 
# any to rows of logical matrix
funApply <- function(x) {
 drop <- apply(is.na(x), 1, any)
 x[!drop, ]
}

# Similar to funAgg but preallocates storage
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

# Loops over columns and setting
# drop to TRUE the first time an NA
# is encountered in that row
funOmit <- function(x) {
 drop <- FALSE
 n <- ncol(x)
 for (i in 1:n)
   drop <- drop | is.na(x[, i])
 x[!drop, ]
}

# Uses fact that mean(y) is NA if y has any NAs in it
# Constructs logical vector 
funRow <- function(x) {
 return(x[!is.na(rowMeans(x)), ])
}