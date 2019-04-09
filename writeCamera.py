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
        HomesData = netatmo.getHomesData(size=5)
        
        if HomesData != "NOK":    
            # print(HomesData)
        
            home_id = HomesData["body"]["homes"][0]["id"]
            persons = HomesData["body"]["homes"][0]["persons"]
            
            # print('HomeID:' + home_id)
            
            for aperson in persons:
                if aperson["pseudo"] == netatmo.config["person"]["pseudo"]:
                    person_id = aperson["id"]
                    person_away = aperson["out_of_sight"]
                    if person_away:
                        person_away = "True"
                    else:
                        person_away = "False"
                else:
                    person_id = ""
                    person_away = "Unknown"
            # print('Person_ID:' + person_id)
            
            if len(argv) > 1:
                if argv[1] == "disarm":
                    status = netatmo.Setpersonshome(homeId=home_id, person_ids=person_id)
                    if status != "NOK":
                        person_away = "False"
                elif argv[1] == "arm":
                    status = netatmo.Setpersonsaway(homeId=home_id, person_id= "")
                    if status != "NOK":
                        person_away = "True"
        else:
            person_away = "Unknown"
    else:
        person_away = "Unknown"

    return person_away

status = main()
print(json.dumps({'person_away': status}, sort_keys=True, indent=4))
