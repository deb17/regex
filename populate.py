import psycopg2
import datetime
import os
import re

DATABASE_URL = os.environ['DATABASE_URL']
HASH = os.environ['HASH']

mo = re.match(r'\w+://(?P<USER>\w+):(?P<DBPASSWORD>\w+)@(?P<HOST>.*)' +
              r':5432/(?P<DBNAME>\w+)', DATABASE_URL)

DBSTRING = ('dbname={DBNAME} user={USER} password={DBPASSWORD} '
            'host={HOST}').format_map(mo.groupdict())

conn = psycopg2.connect(DBSTRING)
cur = conn.cursor()

cur.execute('''insert into roles (role, level) values
            ('admin', 100)''')
cur.execute('''insert into roles (role, level) values
            ('user', 50)''')
now = datetime.datetime.now()

cur.execute('''insert into users
            (username, email_addr, "desc", role, hash, creation_date,
            last_login)
            values
            ('admin',
             'debs.regex@gmail.com',
             'Administrator',
             'admin',
             %s, %s, %s)''', (HASH, now, now))

conn.commit()
cur.close()
conn.close()
