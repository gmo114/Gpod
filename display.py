import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7789
import RPi.GPIO as GPIO


class pirateDisplay:
    script = []
    lines = 10
    start = 0
    end = lines
    disp = ST7789.ST7789(
            height=240,
            width=240,
            rotation=90,
            port=0,
            cs=1,
            dc=9,
            backlight=None,
            spi_speed_hz=60 * 1000 * 1000,
            offset_left=0,
            offset_top=0
        )
    GPIO.setup(13,GPIO.OUT)
    bw = GPIO.PWM(13, 500)
    bw.start(100)
    #music bar
    musicPos = 0
    red = 0
    green = 0
    blue = 0
    #
    def _init_(self,script = []):
        script = script

    def setBacklight(self, brightness):
        self.bw.ChangeDutyCycle(brightness)

    def write(self, message):
        WIDTH = self.disp.width
        HEIGHT = self.disp.height
        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        draw.text((int(0), 0), message, font=font, fill=(255, 255, 255))
        
        draw.rectangle((0, 240, self.musicPos,220), (self.red,self.green,self.blue))
        self.disp.display(img)

    # splist message into a list with each slot haveing 22 charters max
    def fixmessage(self, message):
        max = 0
        newlist = []
        temp = ""
        for a in message:
            if(max == 22): #characters per line
                newlist.append(temp)
                temp = ""
                max = 0
            max += 1
            temp += a
        newlist.append(temp)
        return newlist

    def update(self, message = "",write = True):
        if len(self.script) >= 100:
            script = scirp[49:].copy()
        # if statement required to allow us to updated the music bar without adding a new line to the script
        if write:
            for a in self.fixmessage(message):
                self.script.append(a)
    
        if len(self.script) > self.lines: # resets the scope back to the end
            self.end = len(self.script)
            self.start = len(self.script)-self.lines
        output = ""
        for s in self.script[self.start:self.end]:
            output += s+"\n"
        self.write(output,)

    def scope(self,scroll):
        if len(self.script) > self.lines:
            if self.end < len(self.script) and scroll == "down":
                self.start += 1
                self.end +=1
            elif self.start > 0 and scroll == "up":
                self.start -= 1
                self.end -= 1
        output = ""
        for s in self.script[self.start:self.end]:
            output += s+"\n"
        self.write(output)
        
    def musicBar(self,postion,length,red= 225,green=114,blue = 118):
        self.red = red
        self.green = green
        self.blue = blue
        precent = postion/length
        self.musicPos = int(240*precent)
        