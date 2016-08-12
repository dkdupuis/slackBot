import pysolr
import datetime
import pandas as pd
import requests
#from slackclient import SlackClient    

class findArt:
    #def __init__(self, query, date):
    #    self.query = "sentenceText:\"" + query +"\" AND publishDate:["+date+"T00:00:00Z TO "+date+"T23:59:59Z]"
    
    def __init__(self, query, start, end):
        self.query = "sentenceText:\"" + query +"\" AND publishDate:["+start+" TO "+end+"]"
    
    def getSolr(self):
        return pysolr.Solr('***')
    
    def searchOpinions(self):
        self.opinions = pd.DataFrame(list(self.getSolr().search(self.query, fl="sentenceText,docLink,opinionScore,documentId,headline", rows = 1000)))
    
    def getOpinions(self):
        return self.opinions
    
    def getTopArts(self, numArts = 1):
        arts = []
        headList = []
        if numArts < 1 or len(self.opinions) == 0:
            return arts
        links = self.opinions.groupby('docLink').sum().sort('opinionScore', ascending = False)
        for r in links.iterrows():
            if r[0][:36] != '***':
                h = self.opinions[self.opinions['docLink'] == r[0]]['headline'].values[0].lower()
                if h not in headList or h == None:
                    resolvedUrl = resolve_url(r[0])
                    if resolvedUrl is not None and resolvedUrl != 404 and resolvedUrl not in arts:
                        arts.append(resolvedUrl)
                        if h:
                            headList.append(h)
                        if len(arts) >= numArts:#== should be sufficent
                            return arts
        return arts

def getTimes():
    ts = datetime.datetime.fromtimestamp(time.time())
    end = ts.strftime('%Y-%m-%dT%H:%M:%SZ')
    start = (ts - datetime.timedelta(1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    return (start, end)

def resolve_url(u):
    try:
        r = requests.get(u)
        if r.status_code == 404:
            return 404
        return r.url
    except:
        return None


def cleanTopArts(arts):
    newArtList = []
    for tup in arts:
        newDayList = []
        for link in tup[1]:
            resovledUrl = resolve_url(link)
            if resovledUrl:
                newDayList.append(resolve_url(resovledUrl))
        newArtList.append((tup[0],newDayList))
    return newArtList

#def getTopArts(query, numArtsPerDay, startDate, endDate=None):
#    if endDate == None:
#        endDate = startDate
#    dtStartDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
#    dtEndDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
#    t = dtStartDate
#    artLinks = []
#    while t <= dtEndDate:
#        d = t.strftime('%Y-%m-%d')
#        f = findArt(query, d)
#        f.searchOpinions()
#        artLinks.append((d,f.getTopArts(numArtsPerDay)))
#        t = t + datetime.timedelta(1)
#    return cleanTopArts(artLinks)

def getSetHoursArts(query, numArts, start, end):
    f = findArt(query, start, end)
    f.searchOpinions()
    arts = f.getTopArts(numArts)
#    cleanArts = []
#    for a in arts:
#        resovledUrl = resolve_url(a)
#        if resovledUrl:
#            cleanArts.append(resovledUrl)
    return arts

#def send_message(channel_id, message):
#    slack_client.api_call(
#        "chat.postMessage",
#        channel=channel_id,
#        text=message,
#        as_user='true'
#    )

#def slackTopArtsFromYesterday(user,artList):
#    m = ''
#    for link in artList[0][1]:
#        m += link + '\n'
#    send_message(user, 'Here is the best Content Marketing content from yesterday '+ m)


###sample usage
#slack_client = SlackClient('***')
#arts = getTopArts(3, '2016-07-05')
#slackTopArtsFromYesterday('@***', arts)
#{u'text': u'incoming message from channel', u'ts': u'1468331881.000002', u'user': u'***', u'team': u'***', u'type': u'message', u'channel': u'***'}
        