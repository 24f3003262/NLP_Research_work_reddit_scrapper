import praw
import os
import pandas as pd
import datetime as dt
import dotenv

reddit=praw.Reddit(
    client_id=dotenv.get_key(".env","CLIENT_ID"),
    client_secret=dotenv.get_key(".env","CLIENT_SECRET"),
    password=dotenv.get_key(".env","PASSWORD"),
    user_agent=dotenv.get_key(".env","USER_AGENT"),
    username=dotenv.get_key(".env","USERNAME"),
    password=dotenv.get_key(".env","PASSWORD")
)

target=20000

comment_list=[]

comment_count=0

target_subreddit="r/politics"
subreddit=reddit.subreddit(target_subreddit)

query1="Russia Ukraine War"
query2="American Elections"

for submission in subreddit.search(query1,limit=target):
    if comment_count>=target:
        break
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        author_name=str(comment.author) if comment.author else '[deleted]'
        readable_date=dt.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        comment_list.append({
            'username':author_name,
            'comment_body':comment.body,
            'date':readable_date,
            'upvotes':comment.score
        })
        comment_count+=1

#save_to_csv
df=pd.DataFrame(comment_list)
df.to_csv('Russia_ukraine_comments.csv',index=False)

comment_list=[]
comment_count=0

for submission in subreddit.search(query2,limit=target):
    if comment_count>=target:
        break
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        author_name=str(comment.author) if comment.author else '[deleted]'
        readable_date=dt.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        comment_list.append({
            'username':author_name,
            'comment_body':comment.body,
            'date':readable_date,
            'upvotes':comment.score
        })
        comment_count+=1

df=pd.DataFrame(comment_list)
df.to_csv('American_elections_comments.csv',index=False)
# load_csv(username,comment_body,date) 
