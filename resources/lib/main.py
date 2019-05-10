def increment(i):
  return i+1

class Film():
  def __init__(film, link, plot, poster):
        self.film = str1
        self.link = str2
        self.plot = str3
        self.poster = str4

def listOfXxx(bytes):
  split1 = bytes.decode('utf-8').split('trackingCategory')[1]
  split2 = split1.split('</main>')[0]
  splits3 = split2.split('_1rtC2')
  splits4 = splits3[1:len(splits3)]
  filme1 = []
  for data in splits4:
      comp = re.compile("CUBOJ.+href=\"(.+)\" class=\"_2lnW0\" title=\"(.+)\" .+2hm9z.+srcset=\"(.+) 2x.+_2Ie5A.+[0-9]\">(.+)</div><div class=\"p7P3N.+<p>(.+)</p>.+3FIJo").findall(data)
      if len(comp) > 0:
        filme1.append(comp[0])
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][0] + '/trailer'
    filme.append(Film(filme1[x][1], link, '', ''))
  return filme
