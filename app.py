import imp
from itertools import count
import profile
import re
from flask import Flask
from ipaddress import collapse_addresses
from re import X
from typing import Collection
from xml.dom.minidom import Document
from flask_pymongo import PyMongo
from distutils.debug import DEBUG
from flask import Flask, render_template, jsonify
import pymongo
import os
import json
import bson.json_util as json_util
from pymongo import MongoClient
from bson.son import SON


app = Flask(__name__)

# CONNECTION TO DATABASE
client = pymongo.MongoClient("localhost", 27017)
db = client.BootcampCyber
Collection = db.ChampionsLeague


# ROUTES

# Top Tweets API
@app.route("/TopTweets")
def Top_api():
    cursor10 = Collection.find().sort("average", pymongo.DESCENDING).limit(3)

    TopList = []

    for i in cursor10:
        TopList.append(
            {"name": i["user_name"], "location": i["location"], "link": i["link"]})

    return json.loads(json_util.dumps(TopList))

# Total Number Of Users API


@app.route("/TotalNumOfUsers")
def Users_api():
    cursor8 = Collection.distinct(
        "user_name"
    )
    MainList = []

    for i in cursor8:
        MainList.append(i)
        result = len(MainList)

    return jsonify(result)

# Total Number Of Likes API


@app.route("/TotalNumOfLikes")
def Likes_api():
    cursor8 = Collection.aggregate(
        [{u"$group": {u"_id": "null", u"sum_val": {u"$sum": u"$like_count"}}}])

    LikeList = []

    for i in cursor8:
        LikeList.append(i)

    return jsonify(LikeList)

# Total Number Of Replies API


@app.route("/TotalNumOfReplies")
def Replies_api():
    cursor8 = Collection.aggregate(
        [{u"$group": {u"_id": "null", u"sum_val": {u"$sum": u"$reply_count"}}}])

    ReplyList = []

    for i in cursor8:
        ReplyList.append(i)

    return jsonify(ReplyList)

# Total Number Of Retweets API


@app.route("/TotalNumOfRetweets")
def Retweets_api():
    cursor8 = Collection.aggregate(
        [{u"$group": {u"_id": "null", u"sum_val": {u"$sum": u"$retweet_count"}}}])

    RetweetList = []

    for i in cursor8:
        RetweetList.append(i)

    return jsonify(RetweetList)

# Total Number Of Tweets API


@app.route("/TotalNumOfTweets")
def Tweets_api():
    return jsonify(Collection.count())

# Dashboard Route


@app.route("/Dashboard")
@app.route("/")
def dashboard_page():
    return render_template("Dashboard.html")


# Top Hashtags API
@app.route("/Tophashtags")
def TopHashtags_api():

    cursor2 = Collection.aggregate([
        {
            u"$unwind": u"$hashtags"
        },
        {
            u"$group": {
                u"_id": u"$hashtags",
                u"number": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$sort": SON([(u"number", -1)])
        },
        {
            u"$limit": 50.0
        }
    ]
    )
    Trending_hashtagsList = []
    for j in cursor2:
        Trending_hashtagsList.append({"name": j["_id"], "weight": j["number"]})

    return jsonify(Trending_hashtagsList)

# Top Hashtags WordCloud


@app.route("/TophashtagsWordcloud")
def TopHashtags_page():
    return render_template("TopHashtags.html")

# Verification API


@app.route("/Verification")
def verified_api():
    cursor1 = Collection.aggregate([
        {
            u"$group": {
                u"_id": u"$verified",
                u"count": {
                    u"$sum": 1
                }
            }
        }
    ])
    verified_usersList = []
    for i in cursor1:
        verified_usersList.append({"category": i["_id"], "value": i["count"]})
    return jsonify(verified_usersList)

# Verification Chart


@app.route("/VerificationChart")
def Verified_page():
    return render_template("Verified.html")

# Languages API


@app.route("/Languages")
def Languages_api():

    cursor3 = Collection.aggregate(
        [
            {
                "$group": {
                    "_id": "$language",
                    "number": {
                        "$sum": 1.0
                    }
                }
            },
            {
                "$sort": {
                    "number": -1.0
                }
            },
            {
                "$limit": 100.0
            }
        ]
    )
    LanguagesList = []

    for i in cursor3:
        LanguagesList.append({"country": i["_id"], "sales": i["number"]})
    return jsonify(LanguagesList)

# Languages PieChart


@app.route("/LanguagesPie")
def Languages_page():
    return render_template("Languages.html")

# Influencers API


@app.route("/Influencers")
def Influencers_api():

    cursor4 = Collection.aggregate(
        [{
            u"$group": {
                u"_id": {
                    u"user_name": u"$user_name",
                    u"Profile": u"$Profile"
                },
                u"bookCount": {
                    u"$sum": 1.0
                }
            }
        },
            {
            u"$group": {
                u"_id": u"$_id.user_name",
                u"Profiles": {
                    u"$push": {
                        u"src": u"$_id.Profile",

                    }
                },
                u"count": {
                    u"$sum": u"$bookCount"
                }
            }
        },
            {
            u"$sort": SON([(u"count", -1)])
        },
            {
            u"$limit": 9
        },
            {
            u"$project": {
                u"Profiles": {
                    u"$slice": [
                        u"$Profiles",
                        1.0
                    ]
                },
                u"count": 1.0
            }
        }
        ]
    )
    InfluencersList = []

    for k in cursor4:
        InfluencersList.append(
            {"name": k["_id"], "steps": k["count"], "pictureSettings": k["Profiles"][0]})
    return jsonify(InfluencersList)

# Influencers Chart


@app.route("/InfluencersChart")
def Influencers_page():
    return render_template("Influencers.html")


# Creation API
@app.route("/Creation")
def Creation_api():
    cursor5 = Collection.aggregate([
        {
            u"$group": {
                u"_id": u"$created",
                u"count": {
                    u"$sum": 1
                }
            },
        }, {u"$sort": SON([(u"_id", 1)])}
    ])
    CreationsList = []

    for i in cursor5:
        CreationsList.append({"value": i["count"], "year": f'"{i["_id"]}"'})
    return jsonify(CreationsList)

# Creation Graph


@app.route("/CreationGraph")
def Creation_page():
    return render_template("Creation.html")

# Months API


@app.route("/Months")
def Months_api():
    cursor7 = Collection.aggregate([
        {
            u"$group": {
                u"_id": u"$Month",
                u"count": {
                    u"$sum": 1
                }
            },
        }, {u"$sort": SON([(u"count", -1)])}
    ])
    MonthsList = []

    for i in cursor7:
        MonthsList.append({"country": i["_id"], "value": i["count"]})
    return jsonify(MonthsList)

# Months Graph


@app.route("/MonthsGraph")
def Months_page():
    return render_template("Months.html")

# Countries API


@app.route("/Countries")
def Countries_api():
    cursor9 = Collection.aggregate([
        {
            u"$group": {
                u"_id": u"$location",
                u"count": {
                    u"$sum": 1
                }
            },
        }, {u"$sort": SON([(u"count", -1)])}
    ])
    Countries_List = []

    for i in cursor9:
        country = clean_data(i["_id"])
        Countries_List.append({"name": i["_id"], "value": i["count"]})
    return jsonify(Countries_List)

# Countries Map


@app.route("/CountriesMap")
def Countries_page():
    return render_template("Countries.html")

# Cleaning Data Method


def clean_data(tweet: str):
    clean_tweet = tweet.lower()
    clean_tweet = re.sub(
        "#[0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z_]+", "", clean_tweet)
    clean_tweet = re.sub("#[A-Za-z0-9_]+", "", clean_tweet)
    clean_tweet = re.sub("@[A-Za-z0-9_]+", "", clean_tweet)
    clean_tweet = re.sub(r"http\S+", "", clean_tweet)
    clean_tweet = re.sub(r"www.\S+", "", clean_tweet)
    clean_tweet = clean_tweet.replace("\n", "")
    clean_tweet = clean_tweet.replace("/ ", "")
    clean_tweet = clean_tweet.replace(":", "")
    clean_tweet = clean_tweet.replace(".", "")
    clean_tweet = clean_tweet.replace("/", "")
    clean_tweet = clean_tweet.replace("•", "")
    clean_tweet = clean_tweet.replace(",", "")
    clean_tweet = clean_tweet.replace("'", "")
    clean_tweet = clean_tweet.replace('"', "")
    return clean_tweet


if __name__ == "main__":
    app.run(debug=True)
