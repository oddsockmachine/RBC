Pick from different config profiles (test, local, remote etc)
Convert models to sqla etc instead of pony
use flask-admin to create frontend quickly


# Roadmap

## Hardware
- Pick from different config profiles (test, local, remote etc)
- Rasberry Pi support
  - In progress
  - Now working
- Orange Pi support
  - http://lucsmall.com/2017/01/19/beginners-guide-to-the-orange-pi-zero/
  - Now working
- NanoPi support
  - http://nanopi.io/nanopi-neo.html
  - http://www.friendlyarm.com/index.php?route=product/product&product_id=197
  - More expensive the opi, not bothering

- esp8266/esp32 support
  - deferring to SBCs due to ease of development/library support/ethernet etc, but IOT chips have lower power consumption and inbuilt ADCs
  - requires standardized interface over different libraries
- Add ADCs to SBCs
- Solar power nodules
- Low-power/sleep modes
- Buffer readings and report when power is most available

## Sensors/Actuators
- Default job to report addresses of all connected 1-wire/i2c devices


## Jobs & Scheduling
- Job to immediately reload config from manager
- Internal clock
  - Update on wake from central server
- More flexible scheduling, eg:
  - time of day
  - day of week
  - once per hour/minute/day
- Ad-hoc execution
  - Call an actuator (or even sensor) immediately
  - eg: Must have configured non-sensor component (like IP report) or actuator (like git pull) already, even if it doesn't have an associated job
- Jobs/Components as templates
  - Pick and choose standard jobs/components on a nodule
  - Or deploy a standardized type of nodule
- Job to git pull and restart process

## UI
- Create and deploy new nodules
- Set up jobs and components on a nodule
- Pick from preset components/common jobs
- GIS, mapping and visualization
- Push notifications to mobile

## Logging and Analytics
- Dashboards
- Alerts
- Machine learning - http://blog.oddsockmachine.com:5601/app/ml#/jobs?_g=()
- IFTTT/rules engine


## Development Environment
- Dockerized deployment
  - Support infrastructure such as DBs, APIs, Brokers
- Fully dockerized test environment
  - Including nodules and all supporting infrastructure
- OTA firmware upgrades
  - Reasonably simple to do with git on a SBC
