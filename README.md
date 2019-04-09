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
python3 writeCamera.py <arm/disarm>

returns json "person_away":
 - "True" - if called with "arm", or without argument if out_of_sight = true
 - "False" - if called with "disarm", or without argument if out_of_sight = false
 - "Unknown" - if something went wrong
```

For your own application ID and camera the application does not need to have write_camera as available scope
