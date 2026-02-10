import praw
import pandas as pd
import datetime as dt
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    password=os.getenv("PASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("USERNAME")
)

target_total = 20000
target_subreddit = "politics" # Removed 'r/'
subreddit = reddit.subreddit(target_subreddit)

queries = {
    "Russia_Ukraine": "Russia Ukraine War",
    "American_Elections": "American Elections"
}

for filename_prefix, query in queries.items():
    comment_list = []
    comment_count = 0
    print(f"Starting search for: {query}")

    # limit=500 is plenty; 20k comments will come from these threads
    for submission in subreddit.search(query, sort="relevance", time_filter="all", limit=500):
        if comment_count >= target_total:
            break
        
        # limit=0 is much faster for large-scale scraping because limit=None will call API to many times
        submission.comments.replace_more(limit=0) 
        
        for comment in submission.comments.list():
            if comment_count >= target_total:
                break
                
            author_name = str(comment.author) if comment.author else '[deleted]'
            readable_date = dt.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            
            comment_list.append({
                'username': author_name,
                'comment_body': comment.body.replace('\n', ' '), # Cleaning it to store in CSV in proper format
                'date': readable_date,
                'upvotes': comment.score
            })
            comment_count += 1

    # Save current query results
    df = pd.DataFrame(comment_list)
    df.to_csv(f'{filename_prefix}_comments.csv', index=False, encoding='utf-8')
    print(f"Saved {len(df)} comments to {filename_prefix}_comments.csv\n")