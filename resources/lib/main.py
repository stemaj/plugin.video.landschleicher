import re

def increment(i):
  return i+1

class Film():
  def __init__(self, film, link, plot, poster):
        self.film = film
        self.link = link
        self.plot = plot
        self.poster = poster

def listOfNewest(bytes):
  split1 = bytes.decode('utf-8').split('Default Content')[1]
  split2 = split1.split('actionbar')[0]
  splits3 = split2.split('<article')
  splits4 = splits3[1:len(splits3)]

  regex = r"rbbhandle\":\"(.+)\",\"A.+src=\\'(.+)\\'.+teasertitle\">(.+)</span.+shorttext.+<p>(.+)</p>"
  
  filme = []
  for data in splits4:
      data = data.replace("\n","\\n")
      data = data.replace("\t","\\t")
      data = data.replace("\'","\\\'")
      matches = re.findall(regex, data, re.MULTILINE)
      if len (matches) > 0:
        link = 'https://www.rbb-online.de' + matches[0][1] + '/trailer'
        link2 = 'https://www.rbb-online.de' + matches[0][0]
        film = Film(matches[0][2], link, matches[0][3], link2)
        filme.append(film)
  return filme
