import sqlite3
from redditscrape import Reddit_Scrape
d = Reddit_Scrape()
d.top_post(5)
print(d.top_post(5))
comments_tree = d.get_all_comments()
print("COMMENTS TREE")
print(comments_tree)
print("COMMENTS TREE 2")
print(comments_tree[0])
print("COMMENTS TREE 3")
print(comments_tree[1])

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

# cursor.execute("""CREATE TABLE Posts (id TEXT PRIMARY KEY,
#                 title TEXT,
#                 author TEXT,
#                 score INTEGER,
#                 url TEXT,
#                 created_utc INTEGER)""")
# cursor.execute("""CREATE TABLE Comments (id TEXT PRIMARY KEY,
#                post_id TEXT,
#                author TEXT,
#                body TEXT,
#                score INTEGER,
#                created_utc INTEGER,
#                FOREIGN KEY(post_id) REFERENCES Posts(id))""")
# cursor.execute("""CREATE TABLE Replies (id TEXT PRIMARY KEY,
#                comment_id TEXT,
#                author TEXT,
#                body TEXT,
#                score INTEGER,
#                created_utc INTEGER,
#                FOREIGN KEY(comment_id) REFERENCES Comments(id))""")

for item in range(len(d.top_post(5))):
    cursor.execute(f"""INSERT INTO Posts (id, title, author, score, url, created_utc)
                    VALUES(?, ?, ?, ?, ?, ?)""",
    (d.top_post(5)[5]["ID"],
    d.top_post(5)[5]["TITLE"],
    d.top_post(5)[5]["AUTHOR"],
    d.top_post(5)[5]["SCORE"],
    d.top_post(5)[5]["URL"],
    d.top_post(5)[5]["CREATED_UTC"])) #make sure this is tuple, only takes 2 arguments
    
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