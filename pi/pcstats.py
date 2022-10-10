import json, requests, configparser
import gi, re, os, subprocess, datetime, time
import numpy as np
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from datetime import datetime as dt
print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Start application")


class PCStats():
    def __init__(self):
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Loading configuration")
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Configuration loaded")    
           
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Loading UI")
        self.root = Gtk.Builder()
        self.root.add_from_file("ui.glade")
        self.window = self.root.get_object("mainapp")
        self.window.set_default_size(480, 320)        
        self.window.set_title("PCStats")
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        self.window.show_all()
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "UI loaded")
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Loading values attributions")
        self.data_computername = self.root.get_object("computername")
        self.data_cpuname = self.root.get_object("cpuname")
        self.data_cpuloadbar = self.root.get_object("cpuloadbar")
        self.data_cpuloadtxt = self.root.get_object("cpuload")
        self.data_cpupowertxt = self.root.get_object("cpupower")
        self.data_cpuspeedtxt = self.root.get_object("cpuspeed")
        self.data_cputemptxt = self.root.get_object("cputemp")
        self.data_sysname = self.root.get_object("sysname")
        self.data_syspowertxt = self.root.get_object("syspower")
        self.data_systemp1txt = self.root.get_object("systemp1")
        self.data_systemp2txt = self.root.get_object("systemp2")
        self.data_gpuname = self.root.get_object("gpuname")
        self.data_gpuloadbar = self.root.get_object("gpuloadbar")
        self.data_gpuloadtxt = self.root.get_object("gpuload")
        self.data_gpupowertxt = self.root.get_object("gpupower")
        self.data_gpuspeedtxt = self.root.get_object("gpuspeedcore")
        self.data_gputemptxt = self.root.get_object("gputemp")
        self.data_vramloadbar = self.root.get_object("vramloadbar")
        self.data_vramloadtxt = self.root.get_object("vramload")
        self.data_vramusedtxt = self.root.get_object("vramused")
        self.data_vramtotaltxt = self.root.get_object("vramtotal")
        self.data_vramspeedtxt = self.root.get_object("vramspeed")
        self.data_ramname = self.root.get_object("ramname")
        self.data_ramloadbar = self.root.get_object("ramloadbar")
        self.data_ramloadtxt = self.root.get_object("ramload")
        self.data_ramusedtxt = self.root.get_object("ramused")
        self.data_ramtotaltxt = self.root.get_object("ramtotal")
        self.data_computername.set_text("Starting...")
        print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Values attributions loaded")
        GLib.timeout_add_seconds(1, self.updates)
        Gtk.main()

    def getData(self,path):
        try:
            jsonUrl = "http://" + self.config['system']['remoteIP'] + ":" + self.config['system']['remotePort']  + "/" + path
            try:
                result = requests.get(jsonUrl, timeout=1)
                if str(result.status_code) != "200":
                    return False
                else:
                    return json.loads(result.text)
            except Timeout:
                return False
        except:
            return False

    def cleanValue(self,s,f=False,r=False,v=True):
        sc=s.replace("%","").replace("MHz","").replace("W","").replace("GB","").replace("RPM","").replace(" ","")
        if sc == "": sc="0"
        if s == "None" or s is None or s is False or s is True:
            if f:
                return round(float(0))
            else:
                return "-"
        elif f:
            if r:
                return float(round(float(sc)))
            else:
                return float(sc)
        elif v:
            if r:
                return str(round(float(sc)))
            else:
                return str(sc)
        else:
            sf=s.replace(sc,"%DATA%")
            if r:
                return sf.replace("%DATA%",str(round(float(sc))))
            else:
                return str(s)

    def updates(self):
        try:
            datas = self.getData("stats")
        except:
            datas = False
            print(dt.now().strftime("%m-%d-%y %H:%M > ") + "Remote Host Error, offline ?")    
            
        if(datas is False):
            datas={"pcname": "Remote host is offline", "cpuname": "None", "cpuspeed": "0,0,0,0", "cpubus": "0", "cpumulti": "0", "cpuload": "0,0,0,0", "cputemp": "0,0,0,0", "cpupower": "0,0,0,0", "fancpu": "0,0,0,0", "fansys1": "0,0,0,0", "fansys2": "0,0,0,0", "fangpu": "0,0,0,0", "sysname": "None", "syspower": "0,0,0,0", "systemp1": "0,0,0,0", "systemp2": "0,0,0,0", "ramname": "None", "ramload": "0", "ramuse": "0", "ramfree": "0", "ramtotal": "0", "gpuname": "None", "gpucorespeed": "0,0,0,0", "gpuvideospeed": "None", "gpupower": "0,0,0,0", "gpuload": "0,0,0,0", "gputemp": "0,0,0,0", "vramname": "None", "vramload": "0,0,0,0", "vramuse": "0,0,0,0,0", "vramfree": "None", "vramtotal": "0,0,0,0,0", "vramspeed": "0,0,0,0"}
        
        self.data_computername.set_text(self.cleanValue(datas['pcname'],False,False,False))    
        self.data_cpuname.set_text(self.cleanValue(datas['cpuname'],False,False,False))
        self.data_cpuloadtxt.set_text(self.cleanValue(str(datas['cpuload']).split(",")[0],False,True) + " %")
        self.data_cpuloadbar.set_value(self.cleanValue(str(datas['cpuload']).split(",")[0],True))
        self.data_cpuspeedtxt.set_text(self.cleanValue(str(datas['cpuspeed']).split(",")[0],False,True) +  " MHz")
        self.data_cpupowertxt.set_text(self.cleanValue(str(datas['cpupower']).split(",")[0],False,True) + " W")
        self.data_cputemptxt.set_text(str(datas['cputemp']).split(",")[0])
        
        self.data_gpuname.set_text(self.cleanValue(datas['gpuname'],False,False,False))
        self.data_gpuloadtxt.set_text(self.cleanValue(str(datas['gpuload']).split(",")[0],False,True) + " %")
        self.data_gpuloadbar.set_value(self.cleanValue(str(datas['gpuload']).split(",")[0],True))
        self.data_gpuspeedtxt.set_text(self.cleanValue(str(datas['gpucorespeed']).split(",")[0],False,True) +  " MHz")
        self.data_gpupowertxt.set_text(self.cleanValue(str(datas['gpupower']).split(",")[0],False,True) + " %")
        self.data_gputemptxt.set_text(str(datas['gputemp']).split(",")[0])
        
        self.data_sysname.set_text(self.cleanValue(datas['sysname'],False,False,False))
        self.data_syspowertxt.set_text(self.cleanValue(str(datas['syspower']).split(",")[0],False,True) + " W")
        self.data_systemp1txt.set_text(str(datas['systemp1']).split(",")[0])
        self.data_systemp2txt.set_text(str(datas['systemp2']).split(",")[0])
        
        self.data_ramname.set_text(self.cleanValue(datas['ramname'],False,False,False))
        self.data_ramloadtxt.set_text(self.cleanValue(str(datas['ramload']).split(",")[0],False,True) + " %")
        self.data_ramloadbar.set_value(self.cleanValue(str(datas['ramload']).split(",")[0],True))
        self.data_ramusedtxt.set_text(self.cleanValue(str(datas['ramuse']).split(",")[0],False) + " GB")
        self.data_ramtotaltxt.set_text(self.cleanValue(str(datas['ramtotal']).split(",")[0],False,True) + " GB")
        
        self.data_vramloadtxt.set_text(self.cleanValue(str(datas['vramload']).split(",")[0],False,True) + " %")
        self.data_vramspeedtxt.set_text(self.cleanValue(str(datas['vramspeed']).split(",")[0],False,True) +  " MHz")
        self.data_vramloadbar.set_value(self.cleanValue(str(datas['vramload']).split(",")[0],True))
        self.data_vramusedtxt.set_text(self.cleanValue(str(datas['vramuse']).split(",")[0],False) + " GB")
        self.data_vramtotaltxt.set_text(self.cleanValue(str(datas['vramtotal']).split(",")[4],False,True) + " GB")

        return True
        

app=PCStats()  
