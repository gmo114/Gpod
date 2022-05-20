from player import mp3Player
from display import pirateDisplay
import RPi.GPIO as GPIO
import os
import time

# setting up  gpio pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN,pull_up_down=GPIO.PUD_UP)

if __name__ == "__main__":
    time2 = time.time
    disp = pirateDisplay()
    
    disp.update("click A to start music player")
    br = 100
    while(GPIO.input(5)):
        if(not GPIO.input(6)):
            disp.setBacklight(0)
        time.sleep(0.1)
    disp.script = []
    
    player = mp3Player("//home//gmo//Music//")
    player.stop()
    player = mp3Player("//home//gmo//Music//")
    player.loadSong()
    player.play()
    disp.musicBar(player.getPosition(),player.getlength())
    disp.script.append("------------------------------------")
    disp.update("currently playing: "+player.currentSong)
    pause = False
    tm = 0.0
    br = 100
    while True:
        
        
        if(tm > 3 and br > 0.0):
            br -= 2
        disp.setBacklight(br)
        
        answer  = [not GPIO.input(5),not GPIO.input(6),not GPIO.input(16),not GPIO.input(24)]
        
        #checks if songs is still the same if it is not it will write to the dispay what song is playing
        currentSongCheck = player.currentSong
        player.Running()
        if currentSongCheck != player.currentSong:
            disp.musicBar(player.getPosition(),player.getlength())
            disp.script.append("------------------------------------")
            disp.update("currently playing: "+player.currentSong)
            disp.setBacklight(100)
            br = 100
        
        if answer == [True,False,False,False]:# pause/play
            if(not pause):
                player.pause()
                pause = True
            else:
                player.unpause()
                pause = False
            time.sleep(0.15)
            br = 100
            tm = 0.0
        elif answer == [False,True,False,False]:# whats playing
            disp.setBacklight(100)
            br = 100
            tm = -5.0
            time.sleep(0.15)
        elif answer == [True,True,True,True]:# stop
            disp.musicBar(0,10,0,0,0)
            player.stop()
            disp.write("you have stop the mp3 player")
            time.sleep(5)
            disp.write("good bye!")
            time.sleep(1.5)
            disp.script = []
            disp.musicBar(0,10,0,0,0)
            disp.update(write = False)
            disp.setBacklight(0)
            os.system("sudo -H shutdown now")
            break
        elif answer == [False,False,True,False]: # vol plus
            player.volPlus()
            br = 100
            tm = 0.0
        elif answer == [False,False,False,True]: # vol minus
            player.volMinus()
            br = 100
            tm = 0.0
        elif answer == [False,True,False,True]: # Get Random playlist
            player.getRandom()
            player.loadSong()
            player.play()
            disp.musicBar(player.getPosition(),player.getlength())
            disp.script.append("------------------------------------")
            disp.update("currently playing: "+player.currentSong)
            br = 100
            tm = 0.0
        elif answer == [False,False,True,True]:
            player.nextSong()
            player.loadSong()
            player.play()
            disp.musicBar(player.getPosition(),player.getlength())
            disp.script.append("------------------------------------")
            disp.update("currently playing: "+player.currentSong)
            br = 100
            tm = 0.0
        elif answer == [True,True,False,False]:
            player.prevSong()
            player.loadSong()
            player.play()
            disp.musicBar(player.getPosition(),player.getlength())
            disp.script.append("------------------------------------")
            disp.update("currently playing: "+player.currentSong,)
            br = 100
            tm = 0.0
            
        elif answer == [True,False,True,False]:
            disp.script.append("------------------------------------")
            disp.update("A+B+X+Y = stop")
            disp.update("A = pause/play")
            disp.update ("B = turn on display")
            disp.update("X = vol up")
            disp.update("Y = vol down")
            disp.update("A+y scroll up")
            disp.update("B+X scroll down")
            disp.update("B+Y = rand list play first song")
            br = 100
            tm = 0.0
        elif answer == [False,True,True,False]:
            disp.scope("up")
            br = 100
            tm = 0.0
        elif answer == [True,False,False,True]:
            disp.scope("down")
            br = 100
            tm = 0.0
        disp.musicBar(player.getPosition(),player.getlength())
        disp.update(write = False) # helps update music bar without adding anything to the script
        tm += 0.15
        time.sleep(0.15)