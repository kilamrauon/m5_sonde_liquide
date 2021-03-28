from m5stack import *
from m5ui import *
from uiflow import *
import face
import time

setScreenColor(0x222222)


temp = None
countdown = None
bipok = None
minsensor = None
maxsensor = None
item = None
temp1 = None
tempsaisie = None
i = None
liquide = None
temperatureliquide = None
infusion = None
menuaffiche = None
temperaturesonde1 = None

faces_boy = face.get(face.GAMEBOY)
labeltemperaturesonde = M5TextBox(210, 207, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
temp_cible = M5TextBox(26, 207, "Temperature sonde", lcd.FONT_Default, 0xFFFFFF, rotate=0)
tempsouhaitee = M5TextBox(210, 185, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
saisie = M5TextBox(26, 185, "Temperature souhaitee", lcd.FONT_Default, 0xFFFFFF, rotate=0)
labelliquide = M5TextBox(26, 21, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
labeltempliquide = M5TextBox(26, 44, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
labelinfusion = M5TextBox(26, 64, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label0 = M5TextBox(26, 93, "alarm", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(59, 64, "Secondes", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(68, 45, "C", lcd.FONT_Default, 0xFFFFFF, rotate=0)
labeltempsrestant = M5TextBox(26, 163, "Temps restant", lcd.FONT_Default, 0xFFFFFF, rotate=0)
tempsrestant = M5TextBox(210, 163, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(265, 185, "C", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label4 = M5TextBox(265, 207, "C", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label5 = M5TextBox(257, 163, "Sec", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label6 = M5TextBox(63, 40, "o", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
label8 = M5TextBox(260, 202, "o", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
label9 = M5TextBox(260, 180, "o", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)

from numbers import Number




from machine import Pin
import _onewire

def init(pin):
  Pin(pin, Pin.OPEN_DRAIN, Pin.PULL_UP)

def convert(pin):
  _onewire.reset(Pin(pin))
  _onewire.writebyte(Pin(pin), 0xcc)
  _onewire.writebyte(Pin(pin), 0x44)

def read(pin):
  _onewire.reset(Pin(pin))
  _onewire.writebyte(Pin(pin), 0xcc)
  _onewire.writebyte(Pin(pin), 0xbe)
  tlo = _onewire.readbyte(Pin(pin))
  thi = _onewire.readbyte(Pin(pin))
  _onewire.reset(Pin(pin))
  temp = tlo + thi * 256
  if temp > 32767:
    temp = temp - 65536
  temp = temp * 0.0625
  return(temp)

init(26)

minsensor = -55
maxsensor = 125
item = 1
temp1 = 25
tempsaisie = 26
bipok = 'Alarme OFF'
i = 0
liquide = ['The vert', 'The noir', 'The blanc', 'The Oolong', 'Rooibos', 'Cafe instantane', 'cafe filtre', 'Lait pour yaourt / eau pate a pizza', 'Bain', 'Eau bouillante / tisane', 'Glace', 'Sucre filet', 'Sucre petit boule']
temperatureliquide = [75, 85, 70, 90, 95, 80, 55, 45, 37, 100, 0, 110, 116]
infusion = [150, 240, 600, 300, 300, 0, 0, 0, 0, 300, 0, 0, 0]
tempsaisie = temperatureliquide[int(item - 1)]
tempsouhaitee.setText(str(tempsaisie))
while True:
  menuaffiche = liquide[int(item - 1)]
  labelliquide.setText(str(menuaffiche))
  menuaffiche = temperatureliquide[int(item - 1)]
  labeltempliquide.setText(str(menuaffiche))
  menuaffiche = infusion[int(item - 1)]
  labelinfusion.setText(str(menuaffiche))
  tempsrestant.setText(str(menuaffiche))
  if faces_boy.getStatus(3):
    tempsaisie = tempsaisie + 1
    bipok = 'Alarme ON'
    if tempsaisie >= maxsensor:
      tempsaisie = maxsensor
  if faces_boy.getStatus(2):
    tempsaisie = tempsaisie - 1
    bipok = 'Alarme ON'
    if tempsaisie <= minsensor:
      tempsaisie = minsensor
  if faces_boy.getStatus(7):
    if bipok == 'Alarme OFF':
      bipok = 'Alarme ON'
    else:
      bipok = 'Alarme OFF'
    wait_ms(150)
  if faces_boy.getStatus(1):
    item = item + 1
    if item >= len(liquide):
      item = len(liquide)
    tempsaisie = temperatureliquide[int(item - 1)]
  if faces_boy.getStatus(0):
    item = item - 1
    if item <= 1:
      item = 1
    tempsaisie = temperatureliquide[int(item - 1)]
  if faces_boy.getStatus(4):
    countdown = infusion[int(item - 1)]
    while countdown:
      countdown = (countdown if isinstance(countdown, Number) else 0) + -1
      if faces_boy.getPressed(5):
        countdown = 0
      tempsrestant.setText(str(countdown))
      wait(1)
    speaker.tone(1800, 500)
    wait(0.2)
    speaker.tone(1800, 500)
  wait_ms(150)
  tempsouhaitee.setText(str(tempsaisie))
  label0.setText(str(bipok))
  convert(26)
  temperaturesonde1 = read(26)
  labeltemperaturesonde.setText(str("%.2f"%(temperaturesonde1)))
  if (read(26)) < tempsaisie:
    labeltemperaturesonde.setColor(0x33ccff)
    label4.setColor(0x00cccc)
    label8.setColor(0x00cccc)
  if (read(26)) > tempsaisie:
    labeltemperaturesonde.setColor(0xff0000)
    label4.setColor(0xff0000)
    label8.setColor(0xff0000)
    if bipok != 'Alarme OFF':
      speaker.setVolume(50)
      speaker.tone(1800, 200)
  wait_ms(2)
