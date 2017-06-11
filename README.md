# RBC: Resource Based Community

### A resource manager for a community farm


##### Overview

Connect sensors to nodes. Any sensor can connect to any node via a universal connector.
Nodes are solar powered and collect timestamped data as often as possible at low power, sending only when surplus power is available

Sensor types:
- Soil moisture
- Ambient light intensity (split by UV/IR/Visible)
- Ambient light color
- Temperature
- Air humidity
- Rain
- Air-pressure/weather
- Water level sensors for butts/rivers/lakes
- ph
- chemical (air/soil/water quality)
- O2/CO2 concentrations
- Mains-power voltage
- Wi-Fi strength
- Water-pressure at pumps/butts
- Water flow in rivers, irrigation systems
- Wind speed
- Appliance conditions (eg temperature of solar water heater)
- Timelapse photos (Visible and IR)

Workflow:
- Define zones on map of farm
- Within zones, define beds/pots/plants
- For each remote node, specify in webapp which connectors are which type of sensor
- Send config data to each node, node reads sensor in appropriate way
- Pin sensors to zones
- Record all measurements over time
- Alert when measurements outside reasonable bounds (too dry, too cold etc)
- Alert when conditions are optimal (eg excess hot water = have a shower, night temperatures no longer below x degrees = transplant seedlings)
- Calculate water usage of particular plant type based on temp, humidity, sunlight
- Calculate how much water is necessary (or even optimal) at different times
- Control water (or other controls, eg greenhouse vents) based on scheduled events, alerts, or optimization
- For each bed, keep log of work done, work todo, weight harvested
- Get tips about how to do each task
- Scan QR code at each location to tell phone where you are
- schedule work to minimize workload: spread out over time, and focused on location
