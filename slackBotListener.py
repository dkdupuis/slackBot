from solrQuery import *
import time
import datetime
from slackclient import SlackClient
import logging
import json

#logging.basicConfig(filename='example.log',level=logging.WARN)

def genContent(query, channel, sc=None):
    ts = datetime.datetime.fromtimestamp(time.time())
    end = ts.strftime('%Y-%m-%dT%H:%M:%SZ')
    start = (ts - datetime.timedelta(1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    arts = getSetHoursArts(query, 3, start, end)
    #print arts
    if arts:
        slackTopArtsFromYesterday(channel, arts, query, sc)
    else:
        send_message(channel, 'Sorry, no content from the last 24 hours contained the phrase "{}". Try a shorter or more general query to get results'.format(query), sc)

def send_message(channel_id, message, sc=None):
    if sc is not None:
        slack_client = sc
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        as_user='true'
    )

def slackTopArtsFromYesterday(user,artList, query, sc=None):
    m = ''
    for link in artList:
        m += link + '\n'
    if len(artList) == 3:
        message = 'Here is the best {} content from the last 24 hours '.format(query) + m
    else:
        message = 'Only {} was found for {} over the last 24 hours. Your results are below, and if you\'d like more results, try a shorter or more general query '.format(len(artList), query) + m
    send_message(user, message, sc)


def startSlackBot():
    slack_client = SlackClient('***')
    if slack_client.rtm_connect():
        while True:
            new_evts = slack_client.rtm_read()
            for evt in new_evts:
                #print(evt)
                logging.warn(json.dumps(evt))
                if "type" in evt:
                    if evt["type"] == "message" and "text" in evt and 'bot_id' not in evt and evt.get('username','') != 'slackbot':
                        chan = evt['channel']
                        if chan[0] == "D":
                            query = evt['text']
                            send_message(chan, 'Got it. Give me a moment to scour Insights for you', slack_client)
                            try:
                                genContent(query, chan, slack_client)
                            except:
                                send_message(chan, 'Sorry, I ran into trouble finding content for you. Please try again. If you continue to have problems, please report them to <#C1S6K00KF>', slack_client)
                                raise
        time.sleep(3)
    else:
        print "Connection Failed, invalid token?"
    
    
def postTopCMArtsFromYesterday():
    ts = datetime.datetime.fromtimestamp(time.time())
    end = ts.strftime('%Y-%m-%dT%H:%M:%SZ')
    start = (ts - datetime.timedelta(1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    arts = getSetHoursArts('content marketing', 3, start, end)
    if arts:
        m = ''
        for link in arts:
            m += link + '\n'
        if arts:
            message = 'It\'s time to satisfy your daily Content Marketing Fix! Here is the best Content Marketing content from the last 24 hours ' + m
            slack_client = SlackClient('***')
            send_message('contentmarketingdaily', message, slack_client)
 
    
########
#date+"T00:00:00Z
#ts = datetime.datetime.fromtimestamp(time.time())
#end = ts.strftime('%Y-%m-%dT%H:%M:%SZ')
#begin = (ts - datetime.timedelta(1)).strftime('%Y-%m-%dT%H:%M:%SZ')
