import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7789
import RPi.GPIO as GPIO


class pirateDisplay:
    script = []
    start = 0
    end = 5
    lines = 9
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
        draw.rectangle((0, 0, 240, 240), (0, 0, 0))
        draw.text((int(0), 0), message, font=font, fill=(255, 255, 255))
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

    def update(self, message):
        if len(self.script) >= 100:
            script = scirp[49:].copy()
        for a in self.fixmessage(message):
            self.script.append(a)
    
        if len(self.script) > self.lines: # resets the scope back to the end
            self.end = len(self.script)
            self.start = len(self.script)-self.lines
        output = ""
        for s in self.script[self.start:self.end]:
            output += s+"\n"
        self.write(output)

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
       