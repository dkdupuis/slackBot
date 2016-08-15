# slackBot

Code implements a chat bot on slack. Bot listens for messages from users, uses the message text to query a solr database of content, and returns back the top related content.

##slackBotListener.py
Entry point to the bot listener in `startSlackBot()`

##solrQuery.py
Contains support functions to query solr

##botParse.py
Script code used to parse the bot's logs to examine conversations

##docClusteringSandbox.py
Experimentation with clustering documents with tf-idf. Ultimately, this may be of use in an effort to ensure delivery of diverse content (eg pick only 1 document/cluster)
