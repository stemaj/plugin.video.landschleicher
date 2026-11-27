# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Root list of Landkreise, scraped from the Landschleicher start page.
- Village list per Landkreis, with the broadcast date to tell repeat visits apart.
- Main menu with latest videos, Landkreise and search.
- Latest videos, read from the "Die neuesten Folgen" ticker of the start page.
- Search over all villages by name, using the A-Z index page.
- Video playback for villages; the stream URL is read from the Beitrag page (HLS or MP4).
- Settings: sort order of Landkreise and villages, debug logging and a button to clear the cache (English and German strings).
- Thumbnails and descriptions for villages, read from the Open Graph tags of each Beitrag page. They load in the background after the list is shown, are cached in the addon profile, and the list refreshes once they are available.
- MIT `LICENSE` file, an unofficial-add-on disclaimer and an English summary in `addon.xml`.

### Changed

- Restructured `resources/lib` into `models`, `player`, `scraper` and `utils`.
- Require `xbmc.python` 3.0.0.
- Reduced `kodiutils` to the helpers in use, moved string IDs to `strings.py` and removed empty `addon.xml` tags.

### Fixed

- Searching for only whitespace listed every village.
- Truncated HTTP responses are reported as errors instead of crashing the background loader.
- Errors are now written to the Kodi log; the "no video" message is localised.

### Removed

- External dependencies: `pyStemaj` submodule, `script.module.routing` and `script.module.urllib3`.
- Tests, settings, language files, license file and CI configuration.

## [1.0.1]

### Changed

- Rework.

## [1.0.0]

### Changed

- Rework.

## [0.1.6]

### Fixed

- Other changes while the rbb site is malfunctioning.

## [0.1.5]

### Fixed

- Changes while the rbb site does not include 2016.

## [0.1.4]

### Fixed

- Try to fix by removing socket.

## [0.1.3]

### Changed

- Sort years from new to old.

### Fixed

- Error handling when there is no response.

## [0.1.2]

### Changed

- Repository test.

## [0.1.1]

### Added

- Error handling and notifications.

## [0.1.0]

### Changed

- Adapt to changes on the rbb site.

## [0.0.8]

### Fixed

- Try to fix.

## [0.0.7]

### Fixed

- Missing `response.read`.

## [0.0.6]

### Added

- Error handling and notifications.

## [0.0.5]

### Fixed

- Missing import.

## [0.0.4]

### Added

- Video quality settings.

### Fixed

- Try to handle the `IncompleteRead` exception.
- Missing entry for the current year.

## [0.0.3]

### Added

- Description and date in the video info.

### Changed

- Better fanart and icon.
- Sorting moved to settings.

### Removed

- Blocked videos.

## [0.0.2]

### Added

- Icon.

## [0.0.1]

### Added

- First version.
