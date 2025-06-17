#############################################################################################
# Marcos Paulo Pazzinatto - BlackBoard Wisdom - Level Digital Meter PRO
# Displays a "bubble" that moves on the display according to the angle of the plate.
#############################################################################################

#libraries
from machine import Pin, I2C, ADC
from time import sleep
import math
import ssd1306
import gfx #library for displaying graphics with the display
from RoboCore_MMA8452Q import MMA8452Q
  
#disables the board LEDs
led_25 = Pin(13, Pin.OUT)
led_50 = Pin(4, Pin.OUT)
led_75 = Pin(16, Pin.OUT)
led_100 = Pin(17, Pin.OUT)
led_25.off()
led_50.off()
led_75.off()
led_100.off()
led_R = Pin(19, Pin.OUT)
led_G = Pin(23, Pin.OUT)
led_B = Pin(18, Pin.OUT)
led_R.off()
led_G.off()
led_B.off()

#creates an I2C bus on pins 22 (SCL) and 21 (SDA)
i2c = I2C(scl=Pin(22), sda=Pin(21))

#creates the display control object connected to the I2C bus
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#creates the object for drawing graphics on the display object
graphics = gfx.GFX(128, 64, oled.pixel)

#creating the BlackBoard Wisdom accelerometer object
accel = MMA8452Q(i2c)

#sensor initialization
accel.init()

#slider initialization
slider = ADC(Pin(39))
slider.atten(ADC.ATTN_11DB)

#button initialization
button = Pin(27, Pin.IN, Pin.PULL_UP)
modo_pro = False

#value mapping function
def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    
  #read the potentiometer to map the radius of the circle
  radius = map(slider.read(), 4095, 0, 8, 16)
  radius = math.fabs(radius)
  radius = int(radius)
  
  #press the button to start pro mode
  if button.value() == False:
      sleep(0.025)
      if button.value() == False:
          modo_pro = not modo_pro
          while button.value() == False:
              pass
  
  #performs the accelerometer reading
  accel.read()
  
  #performs X-axis mapping
  position_axisX = map(accel.x, -1, 1, 128 - radius, 0 + radius)
  #converts the mapping to a positive integer value
  position_axisX = math.fabs(position_axisX)
  position_axisX = int(position_axisX)
  
  #performs Y-axis mapping
  position_axisY = map(accel.y, -1, 1, 0 + radius, 64 - radius)
  #converts the mapping to a positive integer value
  position_axisY = math.fabs(position_axisY)
  position_axisY = int(position_axisY)
  
  #check if the board is upside down
  if accel.z < -0.8:
    inverte_axisZ = True
  else:
    inverte_axisZ = False
    
  oled.fill(0) #clears the display information
  graphics.rect(0, 0, 128, 64, 1) #draw the square
  graphics.line(64, 0, 64, 64, 1) #draw the vertical line
  graphics.line(0, 32, 128, 32, 1) #draw the horizontal line
  if modo_pro == True:
      graphics.line(16, 8, 16, 56, 1) #draw the vertical line
      graphics.line(32, 0, 32, 64, 1) #draw the vertical line
      graphics.line(48, 8, 48, 56, 1) #draw the vertical line
      graphics.line(80, 8, 80, 56, 1) #draw the vertical line
      graphics.line(96, 0, 96, 64, 1) #draw the vertical line
      graphics.line(112, 8, 112, 56, 1) #draw the vertical line
      graphics.line(8, 16, 120, 16, 1) #draw the horizontal line
      graphics.line(8, 48, 120, 48, 1) #desenha a linha horizontal
  graphics.circle(position_axisX, position_axisY, radius, 1) #draw the hollow circle
  if inverte_axisZ == True: #if the plate is upside down
      graphics.fill_circle(position_axisX, position_axisY, radius - 4, 1) #draw the filled circle
  oled.show() #displays the last information on the display
  
  #wait 100 milliseconds
  sleep(0.01)
