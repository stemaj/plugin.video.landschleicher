import unittest
from lib import main
from lib import read

class Test_1(unittest.TestCase):

  def test_1(self):
    read.load_file('000')
    self.assertEqual(4, main.increment(3))