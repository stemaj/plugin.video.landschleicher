#coding: utf-8

import re

def increment(i):
  return i+1

class Film():
  def __init__(film, link, plot, poster):
        self.film = str1
        self.link = str2
        self.plot = str3
        self.poster = str4

def listOfNewest(bytes):
  split1 = bytes.decode('utf-8').split('Default Content')[1]
  split2 = split1.split('actionbar')[0]
  splits3 = split2.split('<article')
  splits4 = splits3[1:len(splits3)]
  filme1 = []
  for data in splits4:
      regex = "img data-src=.+'(.+)'.+href=\"(.+)\" .+manualteasertitle\">(.+)</span.+manualteaserdoctype.+<p>(.+)&nbsp"
      matches = re.finditer(regex, data, re.LOCALE)
      for matchNum, match in enumerate(matches, start=1):
        print ("Match {matchNum} wurde an {start}-{end} gefunden: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        for groupNum in range(0, len(match.groups())):
          groupNum = groupNum + 1
          print ("Group {groupNum} wurde an {start}-{end} gefunden: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

        if len(comp) > 0:
          filme1.append(comp[0])
  filme = []
  for x in range(0, len(filme1)):
    link = 'https://www.rbb-online.de' + filme1[x][1] + '/trailer'
    filme.append(Film(filme1[x][2], link, filme1[x][3], filme1[x][0]))
  return filme
