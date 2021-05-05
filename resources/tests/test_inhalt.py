import unittest
from resources import inhalt

class Test_Inhalt(unittest.TestCase):

    def test_neueste(self):
        arr = inhalt.listeDerNeuestenFilme()
        self.assertEqual(len(arr), 2)