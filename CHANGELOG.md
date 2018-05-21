# Change Log
All notable changes to this project will be documented in this file, following the suggestions of [Keep a CHANGELOG](http://keepachangelog.com/). This project adheres to [Semantic Versioning](http://semver.org/).

## v1.1.2 - 2018-05-21
### Changed
- msgpack to new 0.5.6

## v1.1.1 - 2018-04-27
### Fixed
- Imported BASE_URL_REDUCED to download reduced files

## v1.1.0 - 2018-04-04
### Changed
- Switch to msgpack-defaults for easier parsing #38
### Removed
- Mac testing from CI

## v1.0.11 - 2018-02-26
### Added
- Add option to get reduced files from API #36

## v1.0.10 - 2018-03-01
### Fixed
- Don't leak open file handles #32

## v1.0.8 - 2017-08-17
### Fixed
- Changing ascii to utf8 #29

## v1.0.7 - 2017-06-28
### Fixed
- Resolve issue with get_coords

## v1.0.6 - 2017-06-02
### Fixed
- Resolve #22 #22

## v1.0.5 - 2016-11-24
### Added
- Added files to manifest.in

### Changed
- Classes to new style

## v1.0.4 - 2016-09-16
### Added
- Added pass_data_on and write_mmtf to the mmtf API
- Added API functions to MMTFDecoder to get coordinates and bonds as a single list. get_coords and get_bonds

## v1.0.3 - 2016-09-16
### Changed
- Refactored MMTFDecoder to seperate file

### Added
- API functions to write out MMTF files
- Exposed TemplateEncoder, MMTFEncoder, write_mmtf and pass_data_on to API
- Unit test of roundtripping data
- Improved docs

## v1.0.2 - 2016-09-10
### Changed
- Bug fix for handling of null values

## v1.0.1 - 2016-08-19
### Changed
- Improved handling of missing values
- Handle non-gzipped data from URL

## v1.0.0 - 2016-08-15
### Changed
- updated URL to new v1.0 data stores

## v0.2.2 - 2016-08-10
### Changed
- convert_ints_to_floats for old versions of numpy

## v0.2.1 - 2016-08-03
### Added
- API function (get_url) to get the URL of the data

## v0.2.0 - 2016-07-14
### Added
- Initial release of mmtf-python

