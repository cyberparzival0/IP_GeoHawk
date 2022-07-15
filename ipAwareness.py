#!/usr/bin/python3

import requests
import ctypes as C
import time
import multiprocessing as mp
import concurrent.futures
import subprocess
import re
import os
import sys
from padAddresses import padIPv6s
from ipstat import getForeignIPs
from whitelistedZones import allowedIP
import pyfiglet
#from printy import printy 
from termcolor import colored

class IPGEO(C.Structure):
    _fields_ = [
            ("ip", C.c_char_p),
            ("latitude", C.c_float),
            ("longitude", C.c_float),
            ("seconds", C.c_int) #POF
    ]

class IpGeoManager:
    _displayBanner = False

    @classmethod
    def displayCoordinates(self, ipCoordList):
        cmdList = ["python3", "googleMaps.py"]

        for item in ipCoordList:
            # ip=lat=long
            cmdList.append(item)

        subprocess.run(cmdList)

        return 

    @classmethod
    def greeting(cls):
        _list = "toilet -f smblock --filter border:metal".split()
        displayText = "Welcome to GeoHawk!!!\nThis is a command-line friendly tool to help you track ip locations across the globe.\n"
        _list.append(displayText)
        subprocess.run(_list)
        _displayBanner = True

    @classmethod
    def ipNotAllowed(cls, ip):
        text = pyfiglet.figlet_format(f"{ip}", font = "bubble")
        print(colored(text, 'red'))

    def __init__(self, sharedLib = "./cffi/libIP.so"):
        self.sharedLib = C.CDLL(sharedLib)
        
        global _displayBanner

        if self._displayBanner == False:
            self.greeting()
            self._displayBanner = True

        self.getKey()

    def updateUrl(self):
        self.url = 'https://api.ipgeolocation.io/ipgeo' + '?apiKey=' + self.apiKey

    def getKey(self):
        with open("key.txt") as _file:
            self.apiKey = _file.read().strip()

        self.updateUrl()

    def userInputKey(self, _input):
        with open("key.txt", "w") as writer:
            writer.write(_input.strip())

        self.getKey()

    def whileLoopTerminal(self):
        _input = input("Please enter your next command!\n$ ")
        
        # Cycle
        self.argParser(_input)

    def __str__(self):
        #_list = "toilet -f ascii12 --filter metal".split()
        displayText = "Here are some basic commands to help you.\nIt is expected that your key resides in the cwd of this tool in a file called key.txt.\nHelp: -h --h --help\nTake IP addresses from a file: -f --f --file\nThe default delimiter is a comma: ,\nChange the default delimiter: -d --d.\nAn example is ./geohawk -f ip_addresses.txt -d \\t. Check your current client connection with -n or n or netstat."
        #_list.append(displayText)
        #subprocess.run(_list)
        # subprocess.run(["pyflakes", self.file], capture_output=True).returncode
        return displayText

    def validIPAddress(self, IP):
        patternIPv4 = "^((([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9])).){3}(([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9]))$"
        patternIPv6 = "^([0-9a-fA-F]{1,4}[:]){7}[0-9a-fA-F]{1,4}$"
        if re.search(patternIPv4, IP):
            return "IPv4"
        elif re.search(patternIPv6, IP):
            return "IPv6"
        return "Neither"

    def apiKeyError(self):
        print("Invalid key!!!")
        _input = input("You must enter a valid key here: ")
        self.userInputKey(_input)

        self.whileLoopTerminal()

    def wrongFileFormat(self, _filename):
        print("%s filename can't be found" % (_filename))

    def singleIpError(self, ipAddr):
        print("The website, IP Geolocation, does not like this ip address: %s" % (ipAddr))

    def unknownError(self, _input):
        print("You don't like playing by the rules, you won't be served at this time! :P\n%s" % (_input))

    def argParser(self, _input):
        _inputList = _input.split()
        length = len(_inputList)
        if length == 1 and ("-h" in _inputList or "--h" in _inputList or "--help" in _inputList or "help" in _inputList or "h" in _inputList):
            print(self.__str__())

        elif len(_inputList) ==  2 and ("-f" in _inputList or "--f" in _inputList or "--file" in _inputList):
            with open(_inputList[1]) as _file:
                try:
                    ipList = _file.read().split(",")
                    self.selectorHits(ipList)
                except:
                    print(self.wrongFileFormat(_inputList[1]))
        elif length == 1 and (_inputList[0] == "-n" or _inputList[0] == 'n' or _inputList[0] == "netstat"):
            try:
                self.selectorHits(getForeignIPs())
            except Exception as e:
                print(self.unknownError(_input))
        elif length == 1 and self.validIPAddress(padIPv6s(_inputList[0])) != "Neither":
            try:
                self.selectorHits(_inputList)
            except Exception as e:
                print(self.unknownError())
        elif length == 1 and ("q" in _inputList or "-q" in _inputList or "-quit" in _inputList or "--q" in _inputList or "--quit" in _inputList or 'quit' in _inputList or 'exit' in _inputList):
            #self.__del__()
            sys.exit()
        else:
            print(self.unknownError(_input))

        # Cycle
        self.whileLoopTerminal()
            

    def urlBuilder(self, ip):
        return self.url + '&ip=' + ip

    def getIpGeo(self, ip):
        return requests.get(self.urlBuilder(ip)).json()

    def parseRequest(self, data):
        try:
            if data['message'] == "Provided API key is not valid. Contact technical support for assistance at support@ipgeolocation.io":
                raise Exception("Invalid Key")
        except Exception as e:
            if str(e) == "Invalid Key":
                raise Exception(e)
            else:
                pass

        if allowedIP(data["country_name"]) != True:
            self.ipNotAllowed(data['ip'])

        return [bytes(data['ip'], 'utf-8'),float(data['latitude']),float(data['longitude']),int(time.time())]
    
    def setupCtypes(self, **kwargs):
        kwargs["func"].argtypes = kwargs["argtypes"]
        kwargs["func"].restype = kwargs["restype"]

    def getRequest(self, url):
        try:
            return self.parseRequest(requests.get(url).json())
        except Exception as e:
            if str(e) == "Invalid Key":
                return "Key Error"
            else:
                return "Error with %s" % (url)

    def getRequests_parallel(self, list_of_ips):
        results = []
        list_of_urls = [self.urlBuilder(padIPv6s(ip)) for ip in list_of_ips]
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        for result in executor.map(self.getRequest, list_of_urls):
            results.append(result)
        return results

    def selectorHits(self, ip_addrs):
        responses = self.getRequests_parallel(ip_addrs)
        coordList = []

        for addr in responses:
            try:
                if "Error with" in addr:
                    raise Exception("Error")
                elif "Key Error" in addr:
                    raise Exception("Key Error")
                
                #print(*addr)
                # [ip, lat, long]
                coordList.append(f'{addr[0].decode()}={addr[1]}={addr[2]}')
                
                selectorHit = self.sharedLib.selectorHit
                tok = {"argtypes": [C.c_char_p, C.c_float, C.c_float, C.c_int], "restype": C.POINTER(IPGEO), "func": selectorHit}
                self.setupCtypes(**tok)
            
                displaySelector = self.sharedLib.displaySelector
                tok2 = {"argtypes": [C.POINTER(IPGEO)], "restype": C.c_void_p, "func": displaySelector}
                self.setupCtypes(**tok2)
            
                displaySelector(selectorHit(*addr))
            
            except Exception as e:
                if str(e) == "Key Error":
                    return self.apiKeyError()
                else:
                    print("Error with %s" % (addr.split("=")[-1]))

        self.displayCoordinates(coordList)

    def __del__(self):
        _list = "toilet -f smblock --filter border:metal -w 70".split()
        displayText = "Thanks for using this tool!\nEnjoy your day!"
        _list.append(displayText)
        subprocess.run(_list)

#ipGeoManager = IpGeoManager() #("432fda484a774610b95ec29c0aa3ed94")

if __name__ == "__main__":
    IpGeoManager().whileLoopTerminal()
