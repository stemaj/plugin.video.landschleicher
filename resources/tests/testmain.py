import unittest
from lib import main
from lib import read

class Test_1(unittest.TestCase):

  def test_1(self):
    data = read.load_file('000')
    arr = main.listOfNewest(data)
    self.assertEqual(59, len(arr))

  def test_2(self):
    data = read.load_file('001')
    link = main.videoLink(data)
    self.assertEqual('https://rbbhttpstream-a.akamaihd.net/rbb/aktuell/landschleicher/prignitz/aktuell_19990131_Gerdshagen_PR_m_16_9_512x288.mp4', link)
  