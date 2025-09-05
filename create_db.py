import sqlite3

db = sqlite3.connect("instance/period-track.db")

cursor = db.cursor()

cursor.execute("CREATE TABLE period (id INTEGER PRIMARY KEY, date_start INTEGER NOT NULL, month_start INTEGER NOT NULL, year_start INTEGER NOT NULL, date_end INTEGER NOT NULL, month_end INTEGER NOT NULL, year_end INTEGER NOT NULL, difference INTEGER NULL)")

cursor.execute("INSERT INTO period VALUES(1, '29', '6', '2025', '6', '7', '2025', null)")
cursor.execute("INSERT INTO period VALUES(2, '10', '8', '2025', '17', '8', '2025', null)")
#id | date_start | month_start | year_start | date_end | month_end | year_end | difference
#1  | 29         | 6           | 2025       | 6        | 7         | 2025     |
#2  | 10         | 8           | 2025       | 17        | 8        | 2025     |
    #29
    #10
    #first day of p, day before next p
    #42!!!
#how much of the calculation needs to be python and how much can be sql
#should i use the func that i already made?
cursor.execute(f'SELECT date_start + date_end AS difference FROM period;')
cursor.execute(f'UPDATE period SET difference = date_start + date_end; ')
    # print(row)
db.commit()
db.close()

#average = round(sum(length)/len(length))