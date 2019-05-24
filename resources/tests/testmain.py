import unittest
from lib import main
from lib import read

class Test_1(unittest.TestCase):

  def test_1(self):
    data = read.load_file('000')
    arr = main.listOfNewest(data)
    self.assertEqual(59, len(arr))