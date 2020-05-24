from flask import Flask, jsonify, request
from flask_cors import CORS

#from dotenv import load_dotenv
from langdetect import detect
#import os
import tweepy
import pdb
import json

app = Flask(__name__)
CORS(app)

#load env file
load_dotenv(os.path.join('/', '.env'))
#laoad env vairable
# CONSUMER_KEY = os.getenv("CONSUMER_KEY")
# CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = 'pKyuzP3OzJsDFCoXPy9HjSrLx'
CONSUMER_SECRET = 'xqtxf1HpPcnHzSkriHnIUR85JjfN92gl8tzBQGhsVmNuh4pj72'
ACCESS_TOKEN = '3310660274-XX9HkivKuFJAIYqBCb0rzVYKw76wXOQclC8Xx15'
ACCESS_TOKEN_SECRET = 'ncG6se0SM89rxim8k5VtnCMEGJs6jGyHUFPWyI9wzznVg'

@app.route('/', methods=['GET','POST'])
def index():
    twt_data = twitter_data('apple')
    if (request.method == 'POST'):
        response = request.get_json()
        twt_data = twitter_data(response['keyword'])
        return jsonify(twt_data), 201
    else:
        return jsonify(twt_data)
@app.route('/trending', methods=['GET'])
def trending():
    api = twitter_auth_connection()
    trends_result = api.trends_place(2475687)
    trending = []
    for trend in trends_result[0]["trends"]:
        trendingObj = {}
        trendingObj['name'] = trend['name']
        trendingObj['url'] = trend['url']
        trending.append(trendingObj)
    return jsonify(trending), 201


def twitter_data(search):
    api = twitter_auth_connection()
    tweets = []
    for tweet in api.search(q='#{search}', lang="en", rpp=5, tweet_mode="extended"):
        #pdb.set_trace()
        tweetObj ={}
        tweetObj["tweet"] = tweet.full_text
        tweetObj["location"] = tweet.user.location
        tweetObj["retweet_count"] = tweet.retweet_count
        tweetObj['id'] = tweet.id
        #https://twitter.com/user/status/{tweet.id} link to tweet
        tweets.append(tweetObj)
    return tweets
    # with open('data1.json', 'w') as outfile:
    #     json.dump(tweets, outfile)

def twitter_auth_connection():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)
