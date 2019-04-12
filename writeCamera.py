#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Test Netatmo  class
#
import Netatmo
import time, json
from sys import argv

def main():
    netatmo = Netatmo.Netatmo("/home/homeassistant/.homeassistant/scripts/Netatmo_writeCamera/PyAtmo.conf")
    token_got = netatmo.getAccessToken()
    
    person_away = "Unknown"
    
    if token_got != "NOK":
        HomesData = netatmo.getHomesData(size=0)
        
        if HomesData != "NOK":    
            # print(HomesData)
        
            home_id = HomesData["body"]["homes"][0]["id"]
            persons = HomesData["body"]["homes"][0]["persons"]
            
            # print('HomeID:' + home_id)
            person_id = ""
            person_away = "Unknown"
            for aperson in persons:
                if "pseudo" in aperson:
                    if aperson["pseudo"] == netatmo.config["person"]["pseudo"]:
                        person_id = aperson["id"]
                        person_away = aperson["out_of_sight"]
                        if person_away:
                            person_away = "True"
                        else:
                            person_away = "False"

            # print('Person_ID:' + person_id)
            
            if len(argv) > 1:
                if argv[1] == "disarm":
                    status = netatmo.Setpersonshome(homeId=home_id, person_ids=person_id)
                    if status != "NOK":
                        person_away = "False"
                    else:
                        person_away = "Unknown"
                elif argv[1] == "arm":
                    status = netatmo.Setpersonsaway(homeId=home_id, person_id= "")
                    if status != "NOK":
                        person_away = "True"
                    else:
                        person_away = "Unknown"
                elif argv[1] == "sysstat":
                    person_away = "N/A"
                    NAPlug_rf_strength = ""
                    NAPlug_wifi_strength = ""
                    NATherm1_battery_state = ""
                    NATherm1_rf_strength = ""
                    NACamera_wifi_strength = ""
                    NACamera_sd_status = ""
                    NACamera_alim_status = ""
                    status = netatmo.getHomeStatus(homeId=home_id)
                    # print(status)
                    if status != "NOK":
                        modules = status["body"]["home"]["modules"]
                        for amodule in modules:
                            if amodule["type"] == "NAPlug":
                                NAPlug_rf_strength = amodule["rf_strength"]
                                NAPlug_wifi_strength = amodule["wifi_strength"]
                            elif amodule["type"] == "NATherm1":
                                NATherm1_battery_state = amodule["battery_state"]
                                NATherm1_rf_strength = amodule["rf_strength"]
                            elif amodule["type"] == "NACamera":
                                if "wifi_strength" in amodule:
                                    NACamera_wifi_strength = amodule["wifi_strength"]
                                NACamera_sd_status = amodule["sd_status"]
                                NACamera_alim_status = amodule["alim_status"]
                elif argv[1] == "stationdata":
                    person_away = "N/A"
                    Indoor_wifi_status = ""
                    Indoor_temperature = ""
                    Indoor_pressure = ""
                    Indoor_humidity = ""
                    Indoor_co2 = ""
                    Indoor_noise = ""
                    Outdoor_temperature = ""
                    Outdoor_humidity = ""
                    Outdoor_battery_percent = ""
                    Outdoor_rf_status = ""
                    status = netatmo.Getstationsdata()
                    # print(status)
                    if status != "NOK":
                        device = status["body"]["devices"][0]
                        module = status["body"]["devices"][0]["modules"][0]
                        # Indoor: temperature, pressure, co2, noise, humidity, wifi_status
                        # Outdoor: temperature, humidity, battery_percent, rf_status
                        Indoor_wifi_status = device["wifi_status"]
                        Indoor_temperature = device["dashboard_data"]["Temperature"]
                        Indoor_pressure = device["dashboard_data"]["Pressure"]
                        Indoor_humidity = device["dashboard_data"]["Humidity"]
                        Indoor_co2 = device["dashboard_data"]["CO2"]
                        Indoor_noise =  device["dashboard_data"]["Noise"]
                        Outdoor_temperature = module["dashboard_data"]["Temperature"]
                        Outdoor_humidity = module["dashboard_data"]["Humidity"]
                        Outdoor_battery_percent = module["battery_percent"]
                        Outdoor_rf_status = module["rf_status"]
        else:
            person_away = "Unknown"
    else:
        person_away = "Unknown"

    if person_away != "N/A":
        status = json.dumps({'person_away': person_away}, sort_keys=True, indent=4)
    else:
        if argv[1] == "sysstat":
            status = json.dumps({'NAPlug_rf_strength': NAPlug_rf_strength,
                                 'NAPlug_wifi_strength': NAPlug_wifi_strength,
                                 'NATherm1_battery_state': NATherm1_battery_state,
                                 'NATherm1_rf_strength': NATherm1_rf_strength,
                                 'NACamera_wifi_strength': NACamera_wifi_strength,
                                 'NACamera_sd_status': NACamera_sd_status,
                                 'NACamera_alim_status': NACamera_alim_status,
                                 'HomeID': home_id}, sort_keys=True, indent=4)
        elif argv[1] == "stationdata":
            status = json.dumps({'Indoor_wifi_status': Indoor_wifi_status,
                                 'Indoor_temperature': Indoor_temperature,
                                 'Indoor_pressure': Indoor_pressure,
                                 'Indoor_humidity': Indoor_humidity,
                                 'Indoor_co2': Indoor_co2,
                                 'Indoor_noise': Indoor_noise,
                                 'Outdoor_temperature': Outdoor_temperature,
                                 'Outdoor_humidity': Outdoor_humidity,
                                 'Outdoor_battery_percent': Outdoor_battery_percent,
                                 'Outdoor_rf_status': Outdoor_rf_status}, sort_keys=True, indent=4)
        else:
            status = json.dumps({'person_away': person_away}, sort_keys=True, indent=4)
    return status

status = main()
print(status)
