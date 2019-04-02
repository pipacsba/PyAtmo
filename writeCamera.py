#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Test Netatmo  class
#
import Netatmo
import time, json
from sys import argv

def main():
    netatmo = Netatmo.Netatmo("<absolut path to>PyAtmo.conf")
    netatmo.getAccessToken()
    
    HomesData = netatmo.getHomesData(size=5)

    home_id = HomesData["body"]["homes"][0]["id"]
    persons = HomesData["body"]["homes"][0]["persons"]
    
    for aperson in persons:
        if aperson["pseudo"] == netatmo.config["person"]["pseudo"]:
            person_id = aperson["id"]
        else:
            person_id = ""
    
    if len(argv) > 1:
        if argv[1] == "disarm":
            status = netatmo.Setpersonshome(homeId=home_id, person_id=person_id)
        elif argv[1] == "arm":
            status = netatmo.Setpersonsaway(homeId=home_id, person_id="")
        else:
            status = netatmo.Setpersonshome(homeId=home_id, person_id=person_id)
    else:
        status = ""
    
    if len(status)>1:
        print(status["body"]["status"])
    else:
        print("NOK")


main()
