# piPCStats
Display PC Stats on a Raspberry Pi

## Requirement
- Windows computer with Python 3.7+
- Computer with Satic IP on local network
- SIV ( http://rh-software.com/ )
- Raspberry Pi with Raspbian Lite
- 3.5" LCD/TFT Screen for Raspberry Pi (can support other screen, but youneed to create your own display)
- Few Python mdules on both devices

## Concept
The "pc" folder have files for starting a Web Server. This server take information from Windows registry and past it to a JSon output when requested. 

The computer informations was generated by the SIV application ( http://rh-software.com/ ) and saved into the Windows registry.

The "pi" folder have files for the Raspberry PI, Setup the RPi into a lite CLI with a minimal Desktop and put this script to display over a 3.5" LCD screen all the details.


