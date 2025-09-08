import sqlite3
from redditscrape import Reddit_Scrape
d = Reddit_Scrape()
post = d.top_post(25)
print(post)
comments_tree = d.get_all_comments()
print("COMMENTS TREE")
print(comments_tree)
print("COMMENTS TREE 2")
print(comments_tree[0])
print("COMMENTS TREE 3")
# print(comments_tree[1])

#comments
for item in range(len(comments_tree)):
    print(f"COMMENT {item}")
    print(comments_tree[item])
    print(comments_tree[item]["author"])
    for item2 in range(len(comments_tree[item]["replies"])):
        print("REPLIES")
        print(comments_tree[item]["replies"])

db = sqlite3.connect("data.db")

cursor = db.cursor()

cursor.execute("""CREATE TABLE Posts (id TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                score INTEGER,
                url TEXT,
                created_utc INTEGER)""")
cursor.execute("""CREATE TABLE Comments (id TEXT PRIMARY KEY,
               post_id TEXT,
               author TEXT,
               body TEXT,
               score INTEGER,
               created_utc INTEGER,
               FOREIGN KEY(post_id) REFERENCES Posts(id))""")
cursor.execute("""CREATE TABLE Replies (id TEXT PRIMARY KEY,
               comment_id TEXT,
               author TEXT,
               body TEXT,
               score INTEGER,
               created_utc INTEGER,
               FOREIGN KEY(comment_id) REFERENCES Comments(id))""")
def myprint(d):
    replies = {}
    print("DICK")
    print(d)
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v) #FIX THIS
        else:
            replies[k] = v
            # print("{0} : {1}".format(k, v))
    return replies

the_post = False
try:
    for item in post:
        print(item)
        cursor.execute(f"""INSERT INTO Posts (id, title, author, score, url, created_utc)
                        VALUES(?, ?, ?, ?, ?, ?)""",
        (post[item]["ID"],
        post[item]["TITLE"],
        post[item]["AUTHOR"],
        post[item]["SCORE"],
        post[item]["URL"],
        post[item]["CREATED_UTC"])) #make sure this is tuple, only takes 2 arguments
        the_post = post[item]["ID"]
except sqlite3.IntegrityError:
    pass
try:
    for item in range(len(comments_tree)):

        cursor.execute(f"""INSERT INTO Comments (id, post_id, author, body, score, created_utc)
                        VALUES(?, ?, ?, ?, ?, ?)""",
        (comments_tree[item]["id"],
        the_post,
        comments_tree[item]["author"],
        comments_tree[item]["body"],
        comments_tree[item]["score"],
        comments_tree[item]["created_utc"])) #make sure this is tuple, only takes 2 arguments\
        print("hi")
        print(comments_tree[item]["replies"])
        for item2 in comments_tree[item]["replies"]:
            print("ITEM2")
            print(item2)
            print("replies")
            print(myprint(item2))



            cursor.execute(f"""INSERT INTO Replies (id, comment_id, author, body, score, created_utc)
                            VALUES(?, ?, ?, ?, ?, ?)""",
            (myprint(item2)["id"],
            comments_tree[item]["id"],
            myprint(item2)["author"],
            myprint(item2)["body"],
            myprint(item2)["score"],
            myprint(item2)["created_utc"])) #make sure this is tuple, only takes 2 arguments

except sqlite3.IntegrityError:
    pass
    # print(f"COMMENT {item}")
    # print(comments_tree[item])
    # print(comments_tree[item]["author"])
    # for item2 in range(len(comments_tree[item]["replies"])):
    #     print("REPLIES")
    #     print(comments_tree[item]["replies"])


# cursor.execute("INSERT INTO Posts VALUES(1,
#  '29',
#  '6',
#  '2025',
#  '6',
#  '7',
#  '2025',
#  null)")
# cursor.execute("INSERT INTO Comments VALUES(1,
#  '29',
#  '6',
#  '2025',
#  '6',
#  '7',
#  '2025',
#  null)")
# cursor.execute("INSERT INTO Replies VALUES(1,
#  '29',
#  '6',
#  '2025',
#  '6',
#  '7',
#  '2025',
#  null)")
# cursor.execute("INSERT INTO period VALUES(2, '10', '8', '2025', '17', '8', '2025', null)")
# #id | date_start | month_start | year_start | date_end | month_end | year_end | difference
# #1  | 29         | 6           | 2025       | 6        | 7         | 2025     |
# #2  | 10         | 8           | 2025       | 17        | 8        | 2025     |
#     #29
#     #10
#     #first day of p, day before next p
#     #42!!!
# #how much of the calculation needs to be python and how much can be sql
# #should i use the func that i already made?
# cursor.execute(f'SELECT date_start + date_end AS difference FROM period;')
# cursor.execute(f'UPDATE period SET difference = date_start + date_end; ')
    # print(row)
db.commit()
db.close()

#average = round(sum(length)/len(length))