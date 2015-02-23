import json
import re
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import twitter

CONSUMER_KEY       = ""
CONSUMER_SECRET    = ""
OAUTH_TOKEN        = ""
OAUTH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
api = twitter.Twitter(auth=auth)

# get the list of senators
senators = api.lists.members(owner_screen_name="gov", slug="us-senate", count=100)
with open("senators-list.json", "w") as f:
    json.dump(senators, f, indent=4, sort_keys=True)

# get all the senators' timelines
names = [d["screen_name"] for d in senators["users"]]
timelines = [api.statuses.user_timeline(screen_name=name) for name in names]
with open("timelines.json", "w") as f:
    json.dump(timelines, f, indent=4, sort_keys=True)

# could check who has the most followers
followers = [t[0]["user"]["followers_count"] for t in timelines]
zipped = zip(names, followers)
zipped.sort(key=itemgetter(1))

# get all the tweets and see what words are used
tweets = [" ".join([tweet["text"] for tweet in tweets]) for tweets in timelines]
words = [w for text in tweets for w in re.split('\W', text) if w]
vocab = sorted(set(words))

# construct document-term matrix
M = np.asmatrix(np.zeros([len(tweets), len(vocab)]))
for n, tweet in enumerate(tweets):
    for m, term in enumerate(vocab):
        M[n, m] = tweet.count(term)

# pca using scikit-learn
from sklearn import decomposition
pca = decomposition.PCA(n_components=2)
pca.fit(M)
pc = pca.transform(M)
plt.scatter(pc[:, 0], pc[:, 1])
plt.show()
