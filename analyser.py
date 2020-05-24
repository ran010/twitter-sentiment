# -*- coding: utf-8 -*-
'''
Authors: 
Debaleen Das Spandan (https://github.com/the-it-weirdo)
Shouvit Pradhan (https://github.com/shaw8wit)
'''

#call: output_in_json = get_result(output of twitter_data())
# pip install vaderSentiment first

import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#for list of tweets. It will return in json format
def get_result(data):
  outputs = []
  for tweet in data:
    output = get_output(tweet)
    outputs.append(output)
  obj = json.dumps(outputs)
  return obj

#for single tweet. It will return a dict object
def get_output(tweet):
  analyzer = SentimentIntensityAnalyzer()
  analyzer_out = analyzer.polarity_scores(tweet['tweet'])
  out_obj = {}
  out_obj['id'] = tweet['id']
  out_obj['location'] = tweet['location']
  out_obj['retweet_count'] = tweet['retweet_count']
  out_obj['tweet'] = tweet['tweet']
  out_obj['filtered_words'] = filter_data(tweet['tweet'])[3]
  out_obj['neg'] = analyzer_out['neg']
  out_obj['pos'] = analyzer_out['pos']
  out_obj['net'] = analyzer_out['compound'] + analyzer_out['neu']
  return out_obj

# for filtering a single tweet. It return a tuple containing hashtags, mentions, url and filtered words as 4 respective lists.
def filter_data(tweet_str):
  hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
  mention_re = re.compile("(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
  url_re = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

  hashtag_list = re.findall(hashtag_re, tweet_str)
  mention_list = re.findall(mention_re, tweet_str)
  url = re.findall(url_re, tweet_str)
  url_list = [x[0] for x in url]
  stopwords_list = stopwords.words('english')
  stopwords_list.extend(extend_stopwords(hashtag_list, "#")) # extending stopwords list to include # tags for the particular tweet
  stopwords_list.extend(extend_stopwords(hashtag_list, "\n#")) # extending stopwords list to include # tags in new line for the particular tweet
  stopwords_list.extend(extend_stopwords(hashtag_list, "\n\n#")) # extending stopwords list to include # tags in new line for the particular tweet
  stopwords_list.extend(extend_stopwords(mention_list, "@")) # extending stopwords list to include @ mentions for the particular tweet
  stopwords_list.extend(extend_stopwords(mention_list, "\n@")) # extending stopwords list to include @ mentions for the particular tweet starting in newline
  stopwords_list.extend(extend_stopwords(mention_list, "\n\n@")) # extending stopwords list to include @ mentions for the particular tweet starting in newline
  stopwords_list.extend(extend_stopwords(url_list, "\n\n")) # extending stopwords list to include include urls for the particular tweet starting in newline
  stopwords_list.extend(extend_stopwords(url_list, "\n")) # extending stopwords list to include include urls for the particular tweet starting in newline
  stopwords_list.extend(url_list) # extending stopwords list to include urls for the particular tweet
  stopwords_list.append('\n')
  stopwords_list.append('RT')
  stopwords_list.append('\n\n')
  stopwords_list.append('&amp;')
  #print(stopwords_list)
  filtered_words_temp = [word for word in tweet_str.split(" ") if word not in stopwords_list] # removing hashtags, mentions, links and stopwords
  #print(' '.join(filtered_words_temp))
  res = re.sub('['+string.punctuation+']', '', ' '.join(filtered_words_temp)).split() # removing punctuations
  #print(res)
  filtered_words = [word for word in res if word.lower() not in stopwords_list]
  return (hashtag_list, mention_list, url_list, filtered_words)

# helper function to filter hashtags and mentions and urls
def extend_stopwords(theList, character):
  a = []
  for i in theList:
    i = i[:0] + character + i[0:]
    a.append(i) # appending "'character'whatever". for e.g. #whatever
    i = i[0:] + '\n\n' # for words ending with newline characters
    a.append(i) # appending e.g. '#whatever\n\n'
    i = i[0:] + '\n' # for words ending with newline characters
    a.append(i) # appending e.g. '#whatever\n'
  return a