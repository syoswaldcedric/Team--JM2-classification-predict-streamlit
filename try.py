# Importing pre-process packages
import streamlit as st
import pandas as pd
from nltk import SnowballStemmer, PorterStemmer, LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, TreebankWordTokenizer
import string
import re
import nltk  # Importing nltk for preprocessing the datasets
from nltk.corpus import stopwords  # importing Stopwords
# sns.set()   # setting plot style


df = st.file_uploader("Upload a file")
st.write(df)


# Removing noise from the test dataset
pattern_url = r'http[s]?://(?:[A-Za-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9A-Fa-f][0-9A-Fa-f]))+'
subs_url = r'url-web'
df['message'] = df['message'].replace(
    to_replace=pattern_url, value=subs_url, regex=True)

# converting all test text to lower case
df['message'] = df['message'].str.lower()

# Tokenising the test data
tokenised_tweet = dft['message'].apply(
    lambda x: x.split())  # Tokenising the train data
df['tokens'] = tokenised_tweet

# Removing stopwords from the test data
df['stem'] = df['tokens'].apply(remove_stop_words)
tokenised_tweet = df['stem']

# stemming the words from the test data
tokenised_tweet = tokenised_tweet.apply(
    lambda sentence: [stemmer.stem(word) for word in sentence])

# Lemmatizing the test data
tokenised_tweet = tokenised_tweet.apply(
    lambda sentence: [lemmatizer.lemmatize(word) for word in sentence])

# combining the cleaned message column into single sentence for the test dataset
for j in range(len(tokenised_tweet)):
    tokenised_tweet[j] = " ".join(tokenised_tweet[j])
df['cleaned_tweet'] = tokenised_tweet
