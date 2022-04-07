import sqlite3
conn=sqlite3.connect('schedule.db')
c=conn.cursor()
# va 時間指定の有無,ti 予定の日時,co 予定の内容,user_id 予定の対象者
# c.execute('CREATE TABLE schedules (va int, ti datetime, co text, user_id int)')
c.execute('CREATE TABLE schedules (va int, ti text, co text, user_id int)')
conn.commit()
conn.close()