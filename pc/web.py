#!/usr/bin/python3
import urllib.parse as urlparse
import http.server
import socketserver
import os
import subprocess
import configparser
import json
import datetime
import time
from threading import Timer
from urllib.parse import parse_qs
from os import path
from datetime import datetime as dt
from os import listdir
from os.path import isfile, join, isdir
import winreg

scriptpath=os.path.dirname(os.path.realpath(__file__))+"\\"
config = configparser.ConfigParser()
config.read(scriptpath+"config.ini")
WEBPATH=config['system']['path']+"web"
os.chdir(WEBPATH)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        pathSplit = self.path.split("?")
        pathSection = pathSplit[0].split("/")
        if self.path == '/':
            self.path = './index.html'
            try:
                f = open(self.path, 'rb')
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return None

            ctype = self.guess_type(self.path)
            fs = os.fstat(f.fileno())

            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()            

            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()            
            ##return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif path.exists(WEBPATH+pathSplit[0]) is True:
            self.path = pathSplit[0]
            try:
                f = open(self.path, 'rb')
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return None

            ctype = self.guess_type(self.path)
            fs = os.fstat(f.fileno())

            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()            

            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
            ##return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        elif pathSection[1] == "api":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            wanted=pathSection[2]
            outputJson={"result":str(self.getRegistry(config['monitors'][wanted+"_type"],config['monitors'][wanted]))}
            return self.wfile.write(bytes(json.dumps(outputJson), "utf-8"))
        
        elif pathSection[1] == "stats":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            outputJson={
                "pcname":str(self.getRegistry(config['monitors']["pcname_type"],config['monitors']["pcname"])),
                "cpuname":str(self.getRegistry(config['monitors']["cpuname_type"],config['monitors']["cpuname"])),
                "cpuspeed":str(self.getRegistry(config['monitors']["cpuspeed_type"],config['monitors']["cpuspeed"])),
                "cpubus":str(self.getRegistry(config['monitors']["cpubus_type"],config['monitors']["cpubus"])),
                "cpumulti":str(self.getRegistry(config['monitors']["cpumulti_type"],config['monitors']["cpumulti"])),
                "cpuload":str(self.getRegistry(config['monitors']["cpuload_type"],config['monitors']["cpuload"])),
                "cputemp":str(self.getRegistry(config['monitors']["cputemp_type"],config['monitors']["cputemp"])),
                "cpupower":str(self.getRegistry(config['monitors']["cpupower_type"],config['monitors']["cpupower"])),
                "fancpu":str(self.getRegistry(config['monitors']["fancpu_type"],config['monitors']["fancpu"])),
                "fansys1":str(self.getRegistry(config['monitors']["fansys1_type"],config['monitors']["fansys1"])),
                "fansys2":str(self.getRegistry(config['monitors']["fansys2_type"],config['monitors']["fansys2"])),
                "fangpu":str(self.getRegistry(config['monitors']["fangpu_type"],config['monitors']["fangpu"])),
                "sysname":str(self.getRegistry(config['monitors']["sysname_type"],config['monitors']["sysname"])),
                "syspower":str(self.getRegistry(config['monitors']["syspower_type"],config['monitors']["syspower"])),
                "systemp1":str(self.getRegistry(config['monitors']["systemp1_type"],config['monitors']["systemp1"])),
                "systemp2":str(self.getRegistry(config['monitors']["systemp2_type"],config['monitors']["systemp2"])),
                "ramname":str(self.getRegistry(config['monitors']["ramname_type"],config['monitors']["ramname"])),
                "ramload":str(self.getRegistry(config['monitors']["ramload_type"],config['monitors']["ramload"])),
                "ramuse":str(self.getRegistry(config['monitors']["ramuse_type"],config['monitors']["ramuse"])),
                "ramfree":str(self.getRegistry(config['monitors']["ramfree_type"],config['monitors']["ramfree"])),
                "ramtotal":str(self.getRegistry(config['monitors']["ramtotal_type"],config['monitors']["ramtotal"])),
                "gpuname":str(self.getRegistry(config['monitors']["gpuname_type"],config['monitors']["gpuname"])),
                "gpucorespeed":str(self.getRegistry(config['monitors']["gpucorespeed_type"],config['monitors']["gpucorespeed"])),
                "gpuvideospeed":str(self.getRegistry(config['monitors']["gpuvideospeed_type"],config['monitors']["gpuvideospeed"])),
                "gpupower":str(self.getRegistry(config['monitors']["gpupower_type"],config['monitors']["gpupower"])),
                "gpuload":str(self.getRegistry(config['monitors']["gpuload_type"],config['monitors']["gpuload"])),
                "gputemp":str(self.getRegistry(config['monitors']["gputemp_type"],config['monitors']["gputemp"])),
                "vramname":str(self.getRegistry(config['monitors']["vramname_type"],config['monitors']["vramname"])),
                "vramload":str(self.getRegistry(config['monitors']["vramload_type"],config['monitors']["vramload"])),
                "vramuse":str(self.getRegistry(config['monitors']["vramuse_type"],config['monitors']["vramuse"])),
                "vramfree":str(self.getRegistry(config['monitors']["vramfree_type"],config['monitors']["vramfree"])),
                "vramtotal":str(self.getRegistry(config['monitors']["vramtotal_type"],config['monitors']["vramtotal"])),
                "vramspeed":str(self.getRegistry(config['monitors']["vramspeed_type"],config['monitors']["vramspeed"]))
                }
            return self.wfile.write(bytes(json.dumps(outputJson), "utf-8"))
        
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes('Document requested is not found.', "utf-8"))
        return
        
    def getData(self,data,url):
        parsed = urlparse.urlparse("http://localhost"+url)
        try:
            return str(parse_qs(parsed.query)[data]).replace("['","").replace("']","")
        except:
            return ""
            pass

       
    def getRegistry(self,rType,rKey):
        keyPath = r"HARDWARE\\SIV\\"+rType
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, rKey)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None
        
def start():
    pcStats = MyHttpRequestHandler
    pcStatsServer = socketserver.TCPServer(("0.0.0.0", int(config['ctrl']['port'])), pcStats)
    print("*** RUNNING WEB SERVER AT PORT "+str(config['ctrl']['port'])+" ***")
    pcStatsServer.serve_forever()

            
            
            