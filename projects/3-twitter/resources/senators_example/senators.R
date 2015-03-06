setwd("~/Dropbox/Work/current/stat222sp15-private/senators/")

senators = read.csv("senators.csv", header = TRUE)

# Work with pre-computed LSI

lsi = read.csv("lsi.csv", header = TRUE)

col = ifelse(senators$party == "R", "red", "blue")
col[senators$party == "I"] = "purple"

pairs(lsi[,1:4], col = col)

plot(lsi[,1:2], col = col, pch = 16, xlab = "Topic 1", ylab = "Topic 2")
identify(lsi[,1:2], labels = paste(senators$first_name, senators$last_name))

plot(lsi[,3:4], col = col, pch = 16, xlab = "Topic 3", ylab = "Topic 4")
identify(lsi[,3:4], labels = paste(senators$first_name, senators$last_name))