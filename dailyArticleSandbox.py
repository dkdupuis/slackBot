import pysolr
import datetime
import pandas as pd
    
class findArt:
    def __init__(self,date):
        self.query = "sentenceText:\"content marketing\" AND publishDate:["+date+"T00:00:00Z TO "+date+"T23:59:59Z]"
        
    def getSolr(self):
        return pysolr.Solr('***')
        
    def searchOpinions(self):
        self.opinions = pd.DataFrame(list(self.getSolr().search(self.query, fl="sentenceText,docLink,opinionScore,documentId", rows = 10000)))
    
    def getTopArt(self):        
        return self.opinions.groupby('docLink').sum().sort('opinionScore', ascending = False).index[0]
    
    def getOpinions(self):
        return self.opinions
        

import datetime

def getTopArts(startDate, endDate=None):
    if endDate == None:
        endDate = startDate
    dtStartDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dtEndDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    t = dtStartDate
    daysToScore = []
    while t <= dtEndDate:
        d = t.strftime('%Y-%m-%d')
        f = findArt(d)
        f.searchOpinions()
        print 'Top article for {} is {}'.format(d,f.getTopArt())
        t = t + datetime.timedelta(1)
        
import requests

def resolve_url(u):
    return requests.get(u).url

        
        

from slacker import Slacker

slack = Slacker('***')

# Send a message to #general channel
d = '2016-07-05'
l = 'http://twitter.com/socialmedia2day/statuses/750830502899249152'
slack.chat.post_message('#***', "Here's the best content marketing related content I found yesterday: "+ l)

# Get users list
response = slack.users.list()
users = response.body['members']

# Upload a file
slack.files.upload('hello.txt')

hist = [('2016-06-28','http://twitter.com/Journey_America/statuses/747697597725425664'),
 ('2016-06-29','http://twitter.com/MisterSalesman/statuses/748229990798462976'),
 ('2016-07-02','http://twitter.com/markwschaefer/statuses/749280736075653120'),
 ('2016-07-03','http://twitter.com/jeffsheehan/statuses/749618815865090048'),
 ('2016-07-04','http://twitter.com/jeffbullas/statuses/749938198692761600')]
 
import time 
for ent in hist:
    d = ent[0]
    l = ent[1]
    slack.chat.post_message('#***', "Here's the best content marketing related content I found on {}: ".format(d) + l)
    time.sleep(10)
    
    
from slackclient import SlackClient    
slack_client = SlackClient('***')

def send_message(channel_id, message):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        as_user='true'
    )

send_message('@***', 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=sewage+treatment')

def getChanInfo(channel_id):
    print sc.api_call(
        'channels.info',
        channel=channel_id
    )
    
sc.api_call('channels.list')

import slackclient
import time
from slackclient import SlackClient
sc = SlackClient('***')

if sc.rtm_connect():
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            print(evt)
            if "type" in evt:
                if evt["type"] == "message" and "text" in evt and 'bot_id' not in evt:    
                    print evt['text']
                    print evt['channel']
                    send_message(evt['channel'],evt['text'])
        time.sleep(3)
else:
    print "Connection Failed, invalid token?"
    
    