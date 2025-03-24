from AudioAnalyzer import *
import random
import colorsys
import numpy as np

filename = "testing4.mp3"

pygame.init()
infoObject = pygame.display.Info()

analyzer = AudioAnalyzer()
analyzer.load(filename)

pygame.mixer.music.load(filename)
screen = pygame.display.set_mode([1280, 720])
clock = pygame.time.Clock()
running = True

print("screen shown")

dt = 0

rangeOfFrequencySpec = {"bass" : [21,250], "lowmid" : [251, 1000], "himid": [1001,2000], "treble" : [2001,10000]}
chosenColor = {0 : (255, 255, 255) ,1 : (255, 175, 255), 2: (175,125,255), 3:(255, 255, 175)}
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# 100 ~ 1180
startingPositionX = 100
startingPositionY = 600
numberOfBars = 64 # have to be multiple of 4 max: 196
spaceBetweenBarsIn = 1080 / numberOfBars
barsWidth = spaceBetweenBarsIn / 3 * 2

barsAllocatedFrequency = [] # bass, lowm, him, treble

frequencyInterval = {"bass" : 0, "lowmid": 0,"himid":0,"treble":0} # interval of bass, lowm, him, trble
# sort out the bars for low, mid, mid-high and high


for key, val in rangeOfFrequencySpec.items():
    frequencyInterval[key] = [(max(val) - min(val) + 1) // (numberOfBars / 4), (max(val) - min(val) + 1) % (numberOfBars / 4)]

    for j in range(numberOfBars//4): # allocate the frequency range for one bar
        barsAllocatedFrequency.append([int(rangeOfFrequencySpec[key][0] +(frequencyInterval[key][0]*j)),
                                  int(rangeOfFrequencySpec[key][0] + (frequencyInterval[key][0]*(j+1)))])
    barsAllocatedFrequency[-1][1] = int(barsAllocatedFrequency[-1][1] + (frequencyInterval[key][1]-1))

print(barsAllocatedFrequency)
bars = []
    
for i in range(numberOfBars):
    bars.append(AverageAudioBar(x= startingPositionX+i*spaceBetweenBarsIn,
                                y= 600,
                                color= chosenColor[int(i/numberOfBars*4)],
                                rng= barsAllocatedFrequency[i],
                                width= barsWidth
                                ))


pygame.mixer.music.play()


print("RUNNING")
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = pygame.time.get_ticks()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for b in bars: # update the height of bars
        b.update_all(dt,pygame.mixer.music.get_pos() /1000 ,analyzer) # beware that height is needed to be fixed

    for i in range(numberOfBars):
        pass

        # amp_db = analyzer.get_decibel(pygame.mixer.music.get_pos() /1000,  100 + 2**(i/numberOfBars*12)) # 0 ~ 12
        
        # pygame.draw.polygon(screen, color, [(startingPositionX+i*spaceBetweenBarsIn,600),
        #                                     (startingPositionX+barsWidth+i*spaceBetweenBarsIn, 600),
        #                                     (startingPositionX+barsWidth+i*spaceBetweenBarsIn, 600-160-(amp_db*2)),
        #                                     (startingPositionX+i*spaceBetweenBarsIn, 600-160-(amp_db*2))])

    for b in bars:
        b.update_rect()
        b.render(screen)
    

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    # flip() the display to put your work on screen
    pygame.display.flip()
    

pygame.quit()


# read pygame documentation
# read librosa documentation


print("end")