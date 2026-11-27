"""Live checks against the rbb website: URLs are reachable and the scraper still finds data.

These tests need network access and break when rbb changes its markup, so they are
not part of any automatic run. Start them with: python -m unittest discover -s tests -t .
"""
import unittest
import urllib.request

from resources.lib.scraper import http, parser

ROOT_URL = parser.BASE_URL + '/brandenburgaktuell/landschleicher/'


class LiveScrapingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = http.fetch(ROOT_URL)
        cls.landkreise = parser.parse_landkreise(cls.root)

    def test_root_page_lists_landkreise(self):
        self.assertGreaterEqual(len(self.landkreise), 10)
        for landkreis in self.landkreise:
            self.assertTrue(landkreis.name)
            self.assertTrue(landkreis.url.startswith(ROOT_URL))

    def test_root_page_lists_latest_videos(self):
        neueste = parser.parse_neueste(self.root)
        self.assertGreaterEqual(len(neueste), 5)
        for dorf in neueste:
            self.assertTrue(dorf.name)
            self.assertTrue(dorf.url.startswith(parser.BASE_URL))

    def test_every_landkreis_page_lists_villages(self):
        for landkreis in self.landkreise:
            with self.subTest(landkreis=landkreis.name):
                doerfer = parser.parse_doerfer(http.fetch(landkreis.url))
                self.assertGreater(len(doerfer), 0)
                for dorf in doerfer:
                    self.assertTrue(dorf.name)
                    self.assertTrue(dorf.url.startswith(parser.BASE_URL))
                    self.assertRegex(dorf.datum, r'^\d{4}-\d{2}-\d{2}')

    def test_a_z_page_supports_search(self):
        doerfer = parser.parse_doerfer(http.fetch(ROOT_URL + 'a-z.html'))
        self.assertGreater(len(doerfer), 500)

    def test_beitrag_page_has_meta_and_playable_stream(self):
        landkreis = self.landkreise[0]
        doerfer = parser.parse_doerfer(http.fetch(landkreis.url))
        beschreibung, bild = parser.parse_meta(http.fetch_head(doerfer[0].url))
        self.assertTrue(bild.startswith('http'))
        self.assertTrue(beschreibung)

        stream = parser.parse_video_url(http.fetch(doerfer[0].url))
        self.assertTrue(stream.startswith('https://'))
        request = urllib.request.Request(stream, headers={'User-Agent': http.USER_AGENT})
        with urllib.request.urlopen(request, timeout=20) as response:
            self.assertEqual(response.status, 200)
            response.read(1024)


if __name__ == '__main__':
    unittest.main()
