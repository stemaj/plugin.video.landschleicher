# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Root list of Landkreise, scraped from the Landschleicher start page.
- Village list per Landkreis, with the broadcast date to tell repeat visits apart.

### Changed

- Restructured `resources/lib` into `models`, `player`, `scraper` and `utils`.
- Require `xbmc.python` 3.0.0.

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
