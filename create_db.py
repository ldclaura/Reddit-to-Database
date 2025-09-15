import sqlite3
from redditscrape import Reddit_Scrape

d = Reddit_Scrape()
post = d.top_post(3)
comments_tree = d.get_all_comments()

def extract_comments(comments, parent_id=None, collected=None):
    """
    Flatten comments tree into a list of dicts.
    parent_id = parent comment ID (None if top-level)
    """
    if collected is None:
        collected = []

    for comment in comments:
        collected.append({
            "id": comment["id"],
            "parent_id": parent_id,  # store parent ID (comment or post)
            "author": comment["author"],
            "body": comment["body"],
            "score": comment["score"],
            "created_utc": comment["created_utc"]
        })

        if "replies" in comment and comment["replies"]:
            extract_comments(comment["replies"], parent_id=comment["id"], collected=collected)

    return collected


# ---------------- DB Setup ----------------
db = sqlite3.connect("data.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    score INTEGER,
    url TEXT,
    created_utc INTEGER
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Comments (
    id TEXT PRIMARY KEY,
    post_id TEXT,
    author TEXT,
    body TEXT,
    score INTEGER,
    created_utc INTEGER,
    FOREIGN KEY(post_id) REFERENCES Posts(id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Replies (
    id TEXT PRIMARY KEY,
    comment_id TEXT,
    author TEXT,
    body TEXT,
    score INTEGER,
    created_utc INTEGER,
    FOREIGN KEY(comment_id) REFERENCES Comments(id)
)""")


# ---------------- Insert Post ----------------
the_post = False
try:
    for item in post:
        cursor.execute("""INSERT OR IGNORE INTO Posts (id, title, author, score, url, created_utc)
                          VALUES (?, ?, ?, ?, ?, ?)""",
            (post[item]["ID"],
             post[item]["TITLE"],
             post[item]["AUTHOR"],
             post[item]["SCORE"],
             post[item]["URL"],
             post[item]["CREATED_UTC"]))
        the_post = post[item]["ID"]
except sqlite3.IntegrityError:
    pass


# ---------------- Insert Comments ----------------
try:
    for item in comments_tree:
        cursor.execute("""INSERT OR IGNORE INTO Comments (id, post_id, author, body, score, created_utc)
                          VALUES (?, ?, ?, ?, ?, ?)""",
            (item["id"],
             the_post,
             item["author"],
             item["body"],
             item["score"],
             item["created_utc"]))

        # extract all replies to this comment (and nested ones)
        all_replies = extract_comments(item["replies"], parent_id=item["id"])

        for r in all_replies:
            cursor.execute("""INSERT OR IGNORE INTO Replies (id, comment_id, author, body, score, created_utc)
                              VALUES (?, ?, ?, ?, ?, ?)""",
                (r["id"],
                 r["parent_id"],   # this links reply → parent comment
                 r["author"],
                 r["body"],
                 r["score"],
                 r["created_utc"]))
except sqlite3.IntegrityError:
    pass

db.commit()
db.close()