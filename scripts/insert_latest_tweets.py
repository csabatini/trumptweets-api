import re
import MySQLdb
import twitter

from datetime import datetime
from HTMLParser import HTMLParser

# Replace these with your Twitter API credentials
CONS_KEY = ''
CONS_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

api = twitter.Api(consumer_key=CONS_KEY,
                  consumer_secret=CONS_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=True,
                  tweet_mode='extended')

parser = HTMLParser()
db = MySQLdb.connect(
    read_default_file='~/.my.cnf',
    db='trumptweets',
    use_unicode=True,
    charset="utf8")
cursor = db.cursor()

select_tags = """select * from (select tag_id, tag from tag\n
union all\n
select t.tag_id, ta.tag_alias\n
from tag t inner join tag_alias ta\n
on t.tag_id = ta.tag_id) t
order by 1 asc;
"""

ins_status_tag = \
    "INSERT IGNORE INTO status_tag (status_id, tag_id) SELECT %s, %s;"

cursor.execute(select_tags)
tags = cursor.fetchall()

statuses = api.GetUserTimeline(screen_name='realDonaldTrump',
                               count=50,
                               include_rts=False,
                               exclude_replies=True)
for s in statuses:
    created_at = datetime.strptime(
        s.created_at,
        '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
    media_url = None
    if s.media is not None and len(s.media) > 0:
        media_url = s.media[0].media_url_https
    parsed_txt = parser.unescape(s.full_text)

    cursor.execute(
        'INSERT IGNORE INTO status(status_id, text, media_url, created_at) '
        'SELECT %s, %s, %s, %s' %
        (s.id_str, parsed_txt, media_url, created_at))
    db.commit()

    for t in tags:
        if re.search(t[1], parsed_txt, re.IGNORECASE) is not None:
            cursor.execute(ins_status_tag, (s.id_str, t[0]))
            db.commit()
            break

cursor.close()
db.close()
