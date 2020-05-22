# CHANGELOG

## [0.5.6] - 2020-05-22
### Fixed
  - Removed blocking event in init

## [0.5.5] - 2020-05-18
### Fixed
  - Add missing zero in prices

## [0.5.2] - 2020-05-04
### Added
  - Add store latitude and longitude
  
### Fixed
  - Fixed error handling when Jumbo API throws an error

## [0.5.1] - 2020-05-02
### Fixed
  - Fixed error handling when Jumbo API throws an error


## [0.5.0] - 2020-05-02
### Added
  - add open pick ups
  - add time slots for pick ups
 
### Changed
  - renamed some methods and variables related to deliveries
  - strings like "OPEN" are now being made lower case
  
### Removed
  - removed the ability to retrieved closed orders

## [0.4.4] - 2020-05-01
### Changed
  - add "ready to deliver" state to open deliveries

## [0.4.3] - 2020-04-30
### Changed
  - add "processing" state to open deliveries
  
## [0.4.2] - 2020-04-29
### Changed
  - matched pricing for deliveries with basket and time slots

## [0.4.1] - 2020-04-29
### Changed
  - changed pricing object so format becomes available in Home Assistant

## [0.4.0] - 2020-04-29
### Added
  - add pricing to basket
  - add pricing to time slot
 
## [0.3.1] - 2020-04-28
### Changed
  - fixed casting in time slot
 
## [0.3.0] - 2020-04-28
### Added
  - ability to retrieve time slots
  
## [0.2.0] - 2020-04-28
### Added
  - exposed more information for deliveries and basket

## [0.1.0] - 2020-04-28
### Added
  - ability to retrieve basket information
  - ability to retrieve deliveries