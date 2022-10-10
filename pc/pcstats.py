#!/usr/bin/python3
import configparser
import os
import threading
import systray as SysTray
import web as Web       

path=os.path.dirname(os.path.realpath(__file__))+"\\"

config = configparser.ConfigParser()
config.read(path+'config.ini')

def openWeb(sysTrayIcon):
    print("Open Website")
    os.system('cmd /c start chrome "http://127.0.0.1:'+config['ctrl']['port']+'/"')
    return True
def openStats(sysTrayIcon):
    print("Open stats")
    os.system('cmd /c start chrome "http://127.0.0.1:'+config['ctrl']['port']+'/stats"')
    return True
def bye(sysTrayIcon):
    print('Exiting...')
    systray.destroy()
    exit

systray=False
webserver=False

def startSysTray():
    systray=SysTray.SysTrayIcon(path+"app.ico", "PCStats", menu_options, on_quit=bye, default_menu_index=1)
    
def startWebServer():
    webserver=Web.start()
    



menu_options = (
    ('Open internal website', None, openWeb),
    ('Open internal JSon PC Stats', None, openStats),
)     
    
print("starting web server")
pcStatsServerForever = threading.Thread(target=startWebServer)
pcStatsServerForever.daemon=True 
pcStatsServerForever.start()

print("starting systray")
pcStatsSysTray = threading.Thread(target=startSysTray)
pcStatsSysTray.daemon=True 
pcStatsSysTray.start()
while True:
    pass

print("end of script")
