import unittest
from resources import inhalt
from pyStemaj import helper_extractWebsite, byteStream, bytesExtractor

class Test_Inhalt(unittest.TestCase):

    def test_neueste(self):
        arr = inhalt.listeDerNeuestenFilme()
        self.assertEqual(len(arr), 2)

    def test_000(self):
        #helper_extractWebsite.run("https://www.rbb-online.de/brandenburgaktuell/landschleicher/a-z.html", "resources/tests/file.000")
        file = byteStream.fromFile("resources/tests/file.000")
        self.assertEqual(len(file), 918762)
        data = bytesExtractor.extractInnerPartAndSplit(file, b"tab_content", b"commentSaved", b"</article>")
        self.assertEqual(len(data), 1380)
        inhalt.listeDerLandkreiseByData(data)
        self.assertEqual(len(inhalt.Landschleicher.beitraege), 16)

