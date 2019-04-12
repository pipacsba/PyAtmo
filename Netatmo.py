import os
import configparser
import requests


class Netatmo:
    commands = {"Gethomedata", "Setpersonsaway", "Setpersonshome", "getHomeStatus", "Getstationsdata"}

    baseUrl = "https://api.netatmo.com/api/"

    def __init__(self, configFile):
        self.accessToken = None
        self.refreshToken = None
        self.home = None
        self.modules = None
        self.rooms = None
        self.home_id = None
        self.config = configparser.ConfigParser()
        self.configFileName = configFile
        self.loadConfigFile(self.configFileName)

    '''
    NATherm1 = thermostat
    NRV = valve
    NAPlug = relay
    NACamera = welcome camera
    NOC = pr
    '''
    def NAtypes(argument):
        switcher = {
            'NATherm1': 'thermostat',
            'NRV': 'valve',
            'NAPlug': 'relay',
            'NACamera': 'welcome camera',
            'NOC': 'pr'
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "Invalid type")

    def loadConfigFile(self, configFileName):
        #print('read config file')
        if not(os.path.isfile(configFileName)):
            exit(1)
        self.config.read(configFileName)

    def getAccessToken(self):
        payload = {}
        payload["grant_type"] = "password"
        payload["username"] = self.config["security"]["username"]
        payload["password"] = self.config["security"]["password"]
        payload["client_id"] = self.config["security"]["client_id"]
        payload["client_secret"] = self.config["security"]["client_secret"]
        payload["scope"] = self.config["security"]["scope"]

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()

            scope = str(response.json()["scope"])
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            self.accessToken = access_token
            # print('Token:' + access_token)
            self.refreshToken = refresh_token

            self.config.add_section('token')
            self.config.set('token', 'scope', scope)
            return "OK"

        except requests.exceptions.HTTPError as error:
            #print('Request Exception:')
            #print(payload)
            return "NOK"

    def post(self, command, headers=None, data=None):
        # headers = {'Authorization': 'Bearer ' + self.config["security"]["access_token"]}
        headers = {'Authorization': 'Bearer ' + self.accessToken }

        try:
            if data==None:
                response = requests.post(Netatmo.baseUrl+command, headers=headers)
            else:
                response = requests.post(Netatmo.baseUrl+command, headers=headers, params=data)
            response.raise_for_status()
            # print(response.url)
            return response
        except requests.exceptions.HTTPError as error:
            return "NOK"
            # print(response.url)
            # print(error.response.status_code, error.response.text)
            # raise

    # access_token=[YOUR_TOKEN]&home_id=[YOUR_HOME_ID]&size=5
    def getHomesData(self, homeName=None, homeId=None, size=None):
        response = self.post("gethomedata", data={'size': str(size)})
        return response.json()
    
    #access_token=[ACCESS_TOKEN]&home_id=[HOME_ID]&person_id=[PERSONS_ID_ARRAY]
    def Setpersonsaway(self, homeId=None, person_id=None):
        if len(person_id) > 1:
            response = self.post("setpersonsaway", data={'home_id' : homeId, 'person_id' : person_id})
        else:
            response = self.post("setpersonsaway", data={'home_id' : homeId })
        if response != "NOK":
            return response.json()
        else:
            return "NOK"
    
    #access_token=[ACCESS_TOKEN]&home_id=[HOME_ID]&person_ids[]=[PERSONS_ID_ARRAY]
    def Setpersonshome(self, homeId=None, person_ids=None):
        response = self.post("setpersonshome", data={'home_id' : homeId, 'person_ids[]' :  [person_ids]})
        if response != "NOK":
            return response.json()
        else:
            return "NOK"

    # https://dev.netatmo.com/resources/technical/reference/energy/homestatus
    # GET /api.netatmo.com/api/homestatus?home_id=[HOME_ID] 
    def getHomeStatus(self, homeName=None, homeId=None):
        params={}
        params["home_id"]=homeId
        response=self.post("homestatus", data=params)
        if response != "NOK":
            return response.json()
        else:
            return "NOK"

    #GET /api/getstationsdata?access_token=[YOUR_TOKEN]&device_id=[DEVICE_ID]
    def Getstationsdata(self):
        response=self.post("getstationsdata")
        if response != "NOK":
            return response.json()
        else:
            return "NOK"
