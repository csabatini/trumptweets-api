trumptweets-api
===============
RESTful API built with Flask for `Donald Trump's Twitter <https://twitter.com/realDonaldTrump>`_. 

See it in action with the official Android app.

.. image:: play_store.png
    :target: https://play.google.com/store/apps/details?id=com.slickmobile.trumptweets


Why?
----
Yes, you can use the Twitter API - and of course that's what this app does. It authenticates with Twitter and relays data to clients.

With this API, clients can consume Trump's tweets with tag metadata in JSON format without being registered Twitter users.


Environment Setup
-----------------
Looking into Docker, for now you'll need a local MySQL instance, and a /home/{USER}/.my.cnf config file like the one in this project.

Make sure your MySQL user has create/read/write access. Then run these shell commands to get started: ::

    echo "CREATE DATABASE trumptweets CHARACTER SET utf8 COLLATE utf8_general_ci;" | mysql
    gunzip sql/trumptweets.sql.gz
    mysql trumptweets < sql/trumptweets.sql
    pip install -r requirements.txt
    python app.py

Example Usage
-------------
Let's try making an HTTP GET call on the tag endpoint: ::

    curl http://localhost:5000/api/v1/tag
    [{
        "count": 100,
        "max_created_at": 1514941510000,
        "tag": "Fake News",
        "tag_id": 21
    }, ...]

Next, let's query tweets tagged with Fake News: ::

    curl http://localhost:5000/api/v1/status?tag_id=21
    [{
        "status": {
            "created_at": 1514941510000,
            "media_url": null,
            "status_id": "874609480301936640",
            "text": "Fake News is at an all time high. Where is their apology to me for all of the incorrect stories???"
        }, 
        "tags": [
            {
                "tag": "Fake News",
                "tag_id": 21
            }
        ]
    }, ...]
    
Refreshing Data
---------------
New tweets are constantly being created that should be added to the database - ``scripts/insert_latest_tweets.py`` can handle this for us. I recommend running it as a cron job.    

