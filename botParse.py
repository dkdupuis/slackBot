import json
import pandas as pd
import datetime
from slackclient import SlackClient

slack_client = SlackClient('***')

messDicts = []
with open('bot.log') as f:
    for line in f:
        if len(line) > 15 and line[0:14] == 'WARNING:root:{':
            evt = json.loads(line[13:])
            if evt.get('type','') == 'message' and "text" in evt and 'bot_id' not in evt and evt.get('username','') != 'slackbot':
                chan = evt['channel']
                if chan[0] == "D":
                    user = evt.get('user', None)
                    ts = evt.get('ts', None)
                    text = evt.get('text', None)
                    if ts:
                        dt = datetime.datetime.utcfromtimestamp(float(ts))
                    if user:
                        name = slack_client.api_call('users.info',user=user).get('user',{}).get('real_name',None)
                    messDicts.append({'name':name, 'user':user, 'chan':chan, 'dt': dt, 'text':text})

m = pd.DataFrame(messDicts)

def getDate(dt):
    return dt.strftime('%Y-%m-%d')

def gethour(dt):
    return dt.strftime('%H')

def getDayOfWeek(dt):
    return dt.strftime('%a')

#numUsers = len(m.groupby('user'))
m['hour'] = m.apply(lambda x: gethour(x['dt']), axis=1)
m['dayOfWeek'] = m.apply(lambda x: getDayOfWeek(x['dt']), axis=1)
del m['dt']
m.to_csv('insightsBotUse.csv', encoding = "utf-8")




botm = []
with open('bot.log') as f:
    for line in f:
        if len(line) > 15 and line[0:14] == 'WARNING:root:{':
            evt = json.loads(line[13:])
            if evt.get('type','') == 'message' and "text" in evt and 'bot_id' in evt and evt.get('username','') != 'slackbot':
                chan = evt['channel']
                if chan[0] == "D":
                    user = evt.get('user', None)
                    ts = evt.get('ts', None)
                    text = evt.get('text', None)
                    if ts:
                        dt = datetime.datetime.utcfromtimestamp(float(ts))
                    botm.append({'user':user, 'chan':chan, 'dt': dt, 'text':text})

pd.DataFrame(botm).to_csv('BotMessages.csv', encoding = "utf-8")      
            
