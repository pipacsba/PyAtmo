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
        else:
            person_away = "Unknown"
    else:
        person_away = "Unknown"

    if person_away != "N/A":
        status = json.dumps({'person_away': person_away}, sort_keys=True, indent=4)
    else:
        status = json.dumps({'NAPlug_rf_strength': NAPlug_rf_strength,
                             'NAPlug_wifi_strength': NAPlug_wifi_strength,
                             'NATherm1_battery_state': NATherm1_battery_state,
                             'NATherm1_rf_strength': NATherm1_rf_strength,
                             'NACamera_wifi_strength': NACamera_wifi_strength,
                             'NACamera_sd_status': NACamera_sd_status,
                             'NACamera_alim_status': NACamera_alim_status,
                             'HomeID': home_id}, sort_keys=True, indent=4)
    return status

status = main()
print(status)
