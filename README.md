# PyAtmo (based on mr3188/PyAtmo project)
Python Netatmo scripts for write_camera

<b>Clone repo</b>
```
git clone https://github.com/pipacsba/PyAtmo
```

<b>Create config file and edit</b>
```
cp PyAtmo_sample.conf PyAtmo.conf
cat PyAtmo.conf

```

<b>Run test Python script</b>
```
python3 writeCamera.py <arm/disarm/sysstat/stationdata>

<arm/disarm> or without argument:
returns json "person_away":
 - "True" - if called with "arm", or without argument if out_of_sight = true
 - "False" - if called with "disarm", or without argument if out_of_sight = false
 - "Unknown" - if something went wrong
 
<sysstat>
returns json containing:
{'NAPlug_rf_strength','NAPlug_wifi_strength','NATherm1_battery_state','NATherm1_rf_strength','NACamera_wifi_strength','NACamera_sd_status','NACamera_alim_status','HomeID'}

<stationdata>
returns json containing:
{'Indoor_wifi_status','Indoor_temperature','Indoor_pressure','Indoor_humidity','Indoor_co2','Indoor_noise','Outdoor_temperature','Outdoor_humidity','Outdoor_battery_percent','Outdoor_rf_status}
```

For your own application ID and camera the application does not need to have write_camera as available scope
