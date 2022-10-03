import pymongo as pymongo
import twitter as TwitterCyber

Collector = TwitterCyber.TwitterCustomHashtagCollector("championsleague")

datacollection = []

client = pymongo.MongoClient("localhost:27017")
db = client.BootcampCyber
collection = db.ChampionsLeague

for i, tweet in enumerate(Collector.get_items()):
    if i > 100000:
        break

    datacollection.append(
        {"user_name": tweet.user.username, "Year": tweet.date.year, "Month": tweet.date.month,
         "verified": tweet.user.verified, "Profile": tweet.user.profileImageUrl, "created": tweet.user.created.year,
         "id": tweet.id, "reply_count": tweet.replyCount,
         "retweet_count": tweet.retweetCount, "date": tweet.date, "like_count": tweet.likeCount, "language": tweet.lang,
         "link": tweet.url, "source": tweet.source, "location": tweet.user.location, "hashtags": tweet.hashtags,
         "content": tweet.rawContent,"average" :(tweet.replyCount+tweet.likeCount+tweet.retweetCount)/3})

y = collection.insert_many(datacollection)


