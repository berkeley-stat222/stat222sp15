
# coding: utf-8

# The material for this lecture is adapted from a few sources:
# *    the free book Natural Language Processing with Python, available from http://www.nltk.org/book
# *    tutuorials for the [gensim](http://radimrehurek.com/gensim/index.html) Python library
# 
# These are great resources if you want to learn more.

# NLP refers to computations done on "natural" languages, i.e. naturally arising human languages such as English (NOT programming languages).
# 
# Some applications:
# *    predicting word completion (e.g. for cellphones)
# *    computer translation (see http://translationparty.com/ for an illustration of current limitations)
# *    sentiment analysis
# *    search (which document is most relevant for a query)

## 1. Importing example data

# We'll start with some data from the NLTK book.

# In[22]:

import nltk, string
#nltk.download() # download book collection (need to do this once)
from nltk.book import *
from __future__ import division


# In[2]:

# see the name of the example texts
text1


# In[3]:

type(text1)


# Later we'll learn how to create objects of this type. For now, just note we're working with something that looks like a list of words and punctuation. (These are called *tokens*.)

# In[4]:

text1[:10]


# In[5]:

len(text1) # in tokens


## 2. Word useage: contexts

# NLTK has some very useful functions for examining how specific words are used; that is, examining their context.

#### concordance: how are words used?

# In[6]:

text1.concordance("monstrous") # note that case is ignored


# In[7]:

text2.concordance("monstrous")


#### similar: what words are used in a similar context?

# In[8]:

text2.similar("monstrous")


#### common_contexts: for two words used in similar contexts, see the contexts

# In[9]:

text2.common_contexts(["monstrous", "very"])


#### collocations: see words often used together

# In[10]:

text1.collocations()


# In[11]:

text8.collocations()


## 3. Word useage: frequencies

# Let's make an alphabetically sorted list of the unique tokens in the Book of Genesis.

# In[12]:

unique_tokens = sorted(set(text3))
unique_tokens[:20]


# In[13]:

len(unique_tokens)


# We can measure "lexical richness" by dividing the number of unique tokens by the total number of tokens. Let's compare text1 (Moby Dick) to text6 (Monty Python).

# In[14]:

print len(set(text1)) / len(text1)
print len(set(text6)) / len(text6)


# In[15]:

text3.count("begat") # count a given token


# In[16]:

# note this is better for our purposes than the string version shown earlier
print "is this".count("is")
print ["is", "this"].count("is")


# In[17]:

# percentage of text made up of specific word
100 * text3.count("the") / len(text3)


# NLTK provides built-in support for working with frequency distributions (counts of each unique token).

# In[18]:

fdist1 = FreqDist(text1)


# In[19]:

print fdist1


# In[20]:

# extract count for a given token - compare with earlier
fdist1["the"] 


# In[21]:

# see most commonly occurring words; usually most consist of stop words
fdist1.most_common(20)


## 4. Identifying "important" words

# How can we identify "important" or "interesting" words in a text? One way of qualifying this is to find commonly used long words.

# In[26]:

# show words that are > 7 characters long and occur more than 7 times
fdist1 = FreqDist(text1)
count_long = [(word, fdist1[word]) for word in set(text1) 
              if len(word) > 7 and fdist1[word] > 7]
sorted(count_long, key=lambda el: -el[1])


# Approaching this from the opposite direction, we might *remove* commonly occuring short words. These are also known as *stop words*.

# In[27]:

from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')
stopwords[:10]


# In[28]:

# Find most frequently occurring words, removing stop words first
content1 = [word for word in text1 if word.lower() not in stopwords]
fdist1 = FreqDist(content1)
fdist1.most_common(20)


# We'll come back to the question of how to remove tokens that are nothing but punctuation.

## 5. Working with raw text data

# Now we'll grab some text from the web. Project Gutenberg has an online collection of free ebooks in various formats, including plain text.

# In[29]:

import urllib

# link for Crime and Punishment
url = "http://www.gutenberg.org/files/2554/2554.txt"

response = urllib.urlopen(url)
raw = response.read().decode('utf8')


# In[30]:

type(raw)


# In[31]:

# Length - in characters, not tokens
len(raw)


# In[32]:

raw[:500]


### Manually searching for the content

# I opened the link from the Project Gutenburg website to look at the text we just downloaded. There's an introduction I don't want to include. Scrolling down, I see that the book begins with the words "PART I." There's also some copyright information at the end, following the words "End of Project Gutenberg's Crime and Punishment, by Fyodor Dostoevsky."

# In[33]:

raw.find("PART I") # first instance


# In[34]:

raw[5338:5500]


# In[35]:

raw.rfind("End of Project Gutenberg's Crime") # last instance


# In[36]:

raw[1157600:1157746]


# In[37]:

raw = raw[5338:1157746]


### Tokenization

# Tokenizers divide strings into lists of substrings. Usually we do this because we want to split a string into sentences or words. This topic is complex and NLTK has some built-in functions we can use, without delving too much into the algorithms behind them.

# In[38]:

raw[:500]


# One simple way to tokenize is with split.

# In[39]:

# default separator is any whitespace
raw[:500].split()


# In[40]:

from nltk import word_tokenize

tokens = word_tokenize(raw)
type(tokens)


# In[41]:

len(tokens)


# In[42]:

print tokens[:50]


# The word_tokenize function is based on the [Treebank tokenization algorithm](http://www.cis.upenn.edu/~treebank/tokenization.html). One advantage of this algorithm is that it handles contractions in an appropriate way, which is tricky to do for all cases using regular expressions.

# In[43]:

word_tokenize("I've been to the U.S. twice. I don't plan to go back.")


# In[44]:

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+') # one or more word characters
tokenizer.tokenize("I've been to the U.S. twice. I don't plan to go back.")


# One refinement we might want to make is to remove the tokens that consist *only* of punctuation.

# In[45]:

string.punctuation


# In[46]:

def all_punct(x):
    return(all([char in string.punctuation for char in x]))

def my_tokenize(text):
    init_words = word_tokenize(text)
    return([w for w in init_words if not all_punct(w)])


# In[47]:

tokens = my_tokenize(raw)
print tokens[:50]


# Exercise:
# 1.    Write a new function called any_punct that checks whether a string contains any punctuation.
# 2.    Use this function to create a set of tokens containing punctuation from the example above. Do you see any examples of tokens that suggest further improvements we could make?

### Creating an nltk.Text object

# Now we can create an nltk.Text object and use all the NLTK functions for processing.

# In[48]:

text = nltk.Text(tokens)
type(text)


# In[49]:

print text[:20]


# In[50]:

text.collocations()


# In[51]:

content = [w for w in text if w.lower() not in stopwords]
fdist = FreqDist(content)
fdist.most_common(10)


## 6. Vector representations

# Much of advanced text processing is based on creating a vector representation of each text. Think of each element of the vector being a real number representing the answer to a specific question. 
# 
# For example, we could have a dictionary of all possible words and then a long vector counting the number of times each word occurs in a text. Note that this vector would be *sparse*, i.e. containing many zeroes. Efficient implementatations of text-mining algorithms take advantage of this sparsity.
# 
# For working with efficient vector representations, we can use the [gensim](http://radimrehurek.com/gensim/index.html) Python library. I'm going to switch over now to using a simple example from one of the gensim tutorials.
# 
# Imagine that the following are titles of academic papers. The goal is to return the best matching paper for a particular search string.

# In[52]:

from gensim import corpora, models, similarities
documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]


# In[53]:

# remove common words and tokenize
stoplist = set('for a of the and to in'.split()) # an abbreviated list of stop words
texts = [[word for word in document.lower().split() 
          if word not in stoplist]
          for document in documents]
texts


# In[54]:

# find the unique words
dictionary = corpora.Dictionary(texts)
print dictionary


# In[55]:

print dictionary.token2id # numbers represent ids, not counts


# In[56]:

# for a new string, convert to "bag of words" representation using the dictionary
dictionary.doc2bow("human computer interaction survey computer".split())


# Note that the word "interaction" is not in the dictionary and is ignored.

# In[57]:

# convert all documents
corpus = [dictionary.doc2bow(text) for text in texts]
corpus


# A *term-document matrix* has rows representing words/tokens and columns representing documents. Each element counts the number of times a particular word occurs in a particular document. We can think of the corpus object above as representing the term-document matrix in a format that discards all the zero entries.
# 
# It is common to divide each entry by a function of the number of times the word occurs in the entire corpus (collection of documents). This calculation is called TF-IDF, which stands for "term frequency x inverse document frequency."
# 
# Let's see the options by looking at the help for models.TfidfModel in gensim.

# In[54]:

get_ipython().magic(u'pinfo models.TfidfModel')


# In[58]:

tfidf = models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)


# Now we're ready to implement the search. First we need to convert our query to the TF-IDF representation.

# In[59]:

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_tfidf = tfidf[vec_bow]
print(vec_tfidf)


# Now we need a way of determining which of the article titles are "closest" to our query. Think of our vectors in high-dimensional space. We'll use the cosine of the angle between each pair of vectors as our similarity metric.

# In[60]:

index = similarities.MatrixSimilarity(corpus_tfidf)
sims = index[vec_tfidf] # perform a similarity query against the corpus
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples


# In[61]:

sorted(enumerate(sims), key=lambda item: -item[1])


# Various other transformations of the basic bag-of-words representation have been proposed. For example, Latent Semantic Indexing (LSI) is based on taking the SVD of either the term-document matrix or the TF-IDF matrix. See the list of avaiable transformations in gensim [here](http://radimrehurek.com/gensim/tut2.html).
