import time
# import pygame
# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
# pygame.mixer.init()
# sound = pygame.mixer.Sound('songs/OtherSideOfParadise.mp3')
# sound.set_volume(0.2)
# sound.play()
# # pygame.mixer.music.play()


# time.sleep(300)
# print("Finished") # DOESN'T WORK


# import playsound
# playsound.playsound('songs/HeatWaves.mp3') # DOESN'T WORK

import vlc
p = vlc.MediaPlayer('songs/OtherSideOfParadise.mp3')
p.play()
time.sleep(1)
print(p.get_length())
time.sleep(p.get_length())

print("Finished")


# from playsound import playsound

# playsound('songs/HeatWaves.mp3') # Works with python 2.7


# import os

# os.system('C:/Users/bblah/OneDrive/Desktop/EllieProject/songs/HeatWaves.mp3') # Works, but opens other applications to run it


# import subprocess # Maybe works on Mac?
# audio_file = 'C:/Users/bblah/OneDrive/Desktop/EllieProject/songs/HeatWaves.mp3'

# return_code = subprocess.call(["afplay", audio_file])

