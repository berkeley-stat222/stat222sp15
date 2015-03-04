from __future__ import division, print_function

import json
from time import sleep
import twitter

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
api = twitter.Twitter(auth=auth)


def retrieve_timeline(screen_name):

    print("Beginning retrieval of " + screen_name)
    try:
        timeline = api.statuses.user_timeline(screen_name=screen_name,
                                              count=200, include_rts=1)
    except:
        print("Reached rate limit; sleeping 15 minutes")
        sleep(900)
        timeline = api.statuses.user_timeline(screen_name=screen_name,
                                              count=200, include_rts=1)

    ntweets = len(timeline)
    if ntweets < 200:
        return(timeline)
    while ntweets == 200:
        min_id = min([tweet["id"] for tweet in timeline])
        try:
            next_timeline = api.statuses.user_timeline(screen_name=screen_name,
                                                       count=200, max_id=min_id - 1,
                                                       include_rts=1)
        except:
            print("Reached rate limit; sleeping 15 minutes")
            sleep(900)
            next_timeline = api.statuses.user_timeline(screen_name=screen_name,
                                                       count=200, max_id=min_id - 1,
                                                       include_rts=1)
        ntweets = len(next_timeline)
        timeline += next_timeline
    return timeline

senators = api.lists.members(
    owner_screen_name="gov", slug="us-senate", count=100)
screen_names = [d["screen_name"] for d in senators["users"]]

timelines = [retrieve_timeline(screen_name=name) for name in screen_names]
with open("timelines.json", "w") as f:
    json.dump(timelines, f, indent=4, sort_keys=True)


# Step 2: Get additional data for each senator (party, state, etc.)
# and match up with twitter data

import requests

apikey = ''
query_params = {'apikey': apikey,
                'chamber': 'senate',
                'per_page': 10,
                'page': 1}
endpoint = 'http://congress.api.sunlightfoundation.com/legislators?'
response = requests.get(endpoint, params=query_params)
sen_dict = json.loads(response.content)
sen_list = sen_dict["results"]

for p in range(2, 11):
    query_params["page"] = p
    response = requests.get(endpoint, params=query_params)
    sen_dict = json.loads(response.content)
    sen_list += sen_dict["results"]

screen_names_sunlight = [sen["twitter_id"] for sen in sen_list]
screen_names_sunlight.count(None)

# in twitter data but not sunlight data
set(screen_names).difference(set(screen_names_sunlight))
# in sunlight data but not twitter data
set(screen_names_sunlight).difference(set(screen_names))


def levenshtein(a, b):
    """ Calculates the Levenshtein distance between a and b.
        from http://hetland.org/coding/python/levenshtein.py
    """
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]

realnames_twitter = [s["name"] for s in senators["users"]]
realnames_sunlight = [
    " ".join([sen["first_name"], sen["last_name"]]) for sen in sen_list]

# loop through in order of twitter data
# find the index of the closest match in the sunlight data


def findlowermatch(name, namelist):
    # returns only the first match, if there is one
    index = [i for i, t in enumerate(
        namelist) if not t is None and t.lower() == name.lower()]
    if len(index) == 0:
        return(None)
    return(index[0])


def findlevmatch(name, namelist):
    name_dists = [levenshtein(name, nm) for nm in namelist]
    return name_dists.index(min(name_dists))

index = [findlowermatch(name, screen_names_sunlight) for name in screen_names]
for i, name in enumerate(realnames_twitter):
    if index[i] is None:
        index[i] = findlevmatch(name, realnames_sunlight)
        print("Matching " + name + " with " + realnames_sunlight[index[i]])

# fix the one mistake
index[realnames_twitter.index("FrankenCommTeam")] = realnames_sunlight.index(
    "Alan Franken")

# verify matches
for i, name in enumerate(realnames_twitter):
    print(name, "---", realnames_sunlight[index[i]])

import pandas as pd

df = pd.DataFrame([sen_list[i] for i in index])
df.to_csv('senators.csv', encoding='utf-8', index_label=False)


# Step 3: Preliminary text analysis using nltk

tweet_list = [[tweet["text"] for tweet in tl] for tl in timelines]
text_list = [' '.join(tl) for tl in tweet_list]  # tweets back to back

import nltk
from nltk import word_tokenize, FreqDist

text_repub = ' '.join(
    [text for i, text in enumerate(text_list) if df["party"][i] == "R"])
text_dem = ' '.join(
    [text for i, text in enumerate(text_list) if df["party"][i] == "D"])

textnltk_repub = nltk.Text(word_tokenize(text_repub))
textnltk_dem = nltk.Text(word_tokenize(text_dem))

textnltk_repub.collocations()
textnltk_dem.collocations()

textnltk_repub.count("climate") / len(textnltk_repub)
textnltk_dem.count("climate") / len(textnltk_dem)

textnltk_repub.count("Obama") / len(textnltk_repub)
textnltk_dem.count("Obama") / len(textnltk_dem)

textnltk_repub.concordance("Obama")
textnltk_dem.concordance("Obama")

# Step 4: Clean up tokens

import string
stopwords = nltk.corpus.stopwords.words('english')


def tweet_clean(t):
    cleaned_words = [word for word in t.split()
                     if 'http' not in word
                     and not word.startswith('@')
                     and not word.startswith('.@')
                     and not word.startswith('#')
                     and word != 'RT']
    return(' '.join(cleaned_words))


def all_punct(x):
    return(all([char in string.punctuation for char in x]))


def my_tokenize(text):
    init_words = word_tokenize(text)
    return([w.lower() for w in init_words if not all_punct(w) and w.lower() not in stopwords])

tweet_list_cleaned = [
    [my_tokenize(tweet_clean(tweet)) for tweet in tweets] for tweets in tweet_list]
tokens_list_cleaned = [sum(tweets, []) for tweets in tweet_list_cleaned]


# Step 5: Look for words more frequently used by dems or repubs

tokens_repub = sum([sen_tokens for i, sen_tokens in enumerate(tokens_list_cleaned)
                    if df["party"][i] == "R"], [])
tokens_dem = sum([sen_tokens for i, sen_tokens in enumerate(tokens_list_cleaned)
                  if df["party"][i] == "D"], [])

words = set(tokens_repub + tokens_dem)

fd_repub = FreqDist(nltk.Text(tokens_repub))
fd_dem = FreqDist(nltk.Text(tokens_dem))

# find frequently occuring words, filter out the short ones (use state
# abbreviations)
highfreq_words = [word for word in list(words)
                  if fd_repub[word]+fd_dem[word] > 20 and len(word) > 2]

hf_repub = [(word, fd_repub[word], fd_dem[word]) for word in highfreq_words
            if fd_repub[word]/len(tokens_repub) > 5.0 * fd_dem[word]/len(tokens_dem)]
hf_dem = [(word, fd_dem[word], fd_repub[word]) for word in highfreq_words
          if fd_dem[word]/len(tokens_dem) > 5.0 * fd_repub[word]/len(tokens_repub)]

from operator import itemgetter
sorted(hf_repub, key=itemgetter(1), reverse=True)
sorted(hf_dem, key=itemgetter(1), reverse=True)

textnltk_repub.concordance("obamacare")
textnltk_dem.concordance("obamacare")


# Step 6: Use gensim to create a bag-of-words representation for each senator and
# project it into a 2-dimensional subspace for visualization using LSI

from gensim import (corpora,
                    models,
                    similarities)

# limit analysis to high-frequency words only
dictionary = corpora.Dictionary([highfreq_words])
corpus = [dictionary.doc2bow(tokens) for tokens in tokens_list_cleaned]
tfidf = models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

#tfidf_df = pd.DataFrame([[v[1] for v in vector] for vector in corpus_tfidf])
#tfidf_df.to_csv('tfidf.csv', encoding='utf-8', index_label=False)

num_topics = 10
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)

lsi.print_topics(num_topics)

lsi_df = pd.DataFrame([[v[1] for v in vector] for vector in lsi[corpus]])
lsi_df.to_csv('lsi.csv', encoding='utf-8', index_label=False)
