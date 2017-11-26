# Roadmap

## Hardware

- Rasberry Pi and Orange Pi support
- esp8266/esp32 support
  - deferring to SBCs due to ease of development/library support etc, but IOT chips have lower power consumption and inbuilt ADCs
  - requires standardized interface over different libraries
- Solar power nodules
- Low-power/sleep modes
- Buffer readings and report when power is most available


## Jobs & Scheduling

- Internal clock
  - Update on wake from central server

- More flexible scheduling, eg:
  - time of day
  - day of week
  - once per hour/minute/day


- Ad-hoc execution
  - Call an actuator (or even sensor) immediately


- Jobs/Components as templates
  - Pick and choose standard jobs/components on a nodule
  - Or deploy a standardized type of nodule

## UI

- Create and deploy new nodules
- Set up jobs and components on a nodule
- GIS, mapping and visualization
- Push notifications to mobile

## Logging and Analytics

- Dashboards
- Alerts
- Machine learning?
- IFTTT/rules engine


## Development Environment
- Dockerized deployment
  - Support infrastructure such as DBs, APIs, Brokers
- Fully dockerized test environment
  - Including nodules and all supporting infrastructure
- OTA firmware upgrades
  - Reasonably simple to do with git on a SBC
