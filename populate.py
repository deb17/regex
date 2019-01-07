import psycopg2
import datetime

conn = psycopg2.connect("dbname=pyregex user=postgres password=hello "
                        "host=localhost")
cur = conn.cursor()

# cur.execute('''insert into roles (role, level) values
            # ('admin', 100)''')
# cur.execute('''insert into roles (role, level) values
#             ('user', 50)''')
now = datetime.datetime.now()

cur.execute('''insert into users
            (username, email_addr, "desc", role, hash, creation_date,
            last_login)
            values
            ('admin',
             'debs.regex@gmail.com',
             'Administrator',
             'admin',
             'cAiCSwQLUiYx90eReBPMFs+1ygQK6dXqWOESj83MkojHdFuUeKhuRS7CF0n'
             'VHd3BKXo+yc9U9fi5AaQexhvZ6X8=',
             %s, %s)''', (now, now))

conn.commit()
cur.close()
conn.close()
