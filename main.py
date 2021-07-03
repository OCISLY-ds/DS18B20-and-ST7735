from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont
import time
import threading
import pytz, random, os, json
from datetime import datetime
import threading
serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
device = st7735(serial, rotate=2)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
timezoneBerlin = pytz.timezone("Europe/Berlin")
now = datetime.now(timezoneBerlin)
current_time = now.strftime("%H\t%M\t%S")
   
def Wassertemperatur():
    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01193a114ec3/w1_slave')
    filecontent = file.read()
    file.close()

    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000

    # Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature
    return rueckgabewert

def AuslassTemperatur():
    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01193a1a932f/w1_slave')
    filecontent = file.read()
    file.close()

    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000

    # Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature
    return rueckgabewert

# Box and text rendered in portrait mode
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="black", fill="black")
    #draw.text((10, 10), "Uhrzeit:", current_time(), fill="white"

# core klasse
def Core():
    # timer, der die nächste ausführung der funktion Core() alle 10 sek plant
    threading.Timer(10, Core).start()    
    draw.text((10, 25), "Temperatur Auslass:", fill="red", font=font1)
    draw.text((10, 45), (AuslassTemperatur()) + "°C", fill="red", font=font)
    draw.text((10, 70), "Temperatur Wasser:", fill="blue", font=font1)
    draw.text((10, 90), (Wassertemperatur()) + "°C", fill="blue", font=font)
    device.clear()
    Core()

# einmaliges aufrufen der funktion Core() beim start, 
# denn wie du weißt werden def's beim starten des skripts nicht automatisch ausgeführt
