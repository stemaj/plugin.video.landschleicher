# Landschleicher

A Kodi video add-on for the **Landschleicher** archive of
[rbb Brandenburg aktuell](https://www.rbb-online.de/brandenburgaktuell/landschleicher/):
since 1993 the Landschleicher visits a Brandenburg village with fewer than 2,000 inhabitants every weekend.

> **Unofficial.** This add-on is not affiliated with rbb. All videos, images and texts belong to
> Rundfunk Berlin-Brandenburg (rbb). They are only linked from its website, not stored or redistributed.

## Features

- Latest videos, taken from the "Die neuesten Folgen" ticker.
- Browse by Landkreis, then by village. Repeat visits show their broadcast date.
- Search over all villages by name.
- Thumbnails and descriptions, loaded in the background after the list is shown and cached locally.
- Playback of the HLS or MP4 stream of each Beitrag.
- English and German user interface.

There is no official API, so the add-on reads the public web pages.
It may stop working when rbb changes its website.

## Requirements

Kodi 20 (Nexus) or newer. Developed and tested with Kodi 21.3 (Omega).

## Installation

1. Download the zip from the "Build release zip" workflow run (Actions tab), or zip the
   `plugin.video.landschleicher` folder yourself.
2. In Kodi: *Add-ons → Install from zip file*, and select the zip.

For development, clone the repository into the Kodi `addons` folder and restart Kodi.

## Settings

| Group | Setting | Description |
| --- | --- | --- |
| Sorting | Landkreise | A-Z or Z-A |
| Sorting | Villages | A-Z, Z-A, newest first or oldest first |
| Development | Debug logging | Write debug messages to the Kodi log |
| Development | Clear cache | Remove cached thumbnails and descriptions |

## Tests

The tests call the real rbb website to check that URLs are reachable and scraping still works.
They need network access and are not run automatically. Run them locally with:

```sh
python3 -m unittest discover -s tests -t .
```

or start the "Live tests" workflow manually in the GitHub Actions tab.

## License

The source code is licensed under the [MIT License](LICENSE).
`icon.png` and `fanart.jpg` are based on rbb material and are not covered by it.
