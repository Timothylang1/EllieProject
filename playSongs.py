import pygame
import os
import tkinter as tk
from random import shuffle

# WEBSITE TO CONVERT FROM YOUTUBE TO MP3: https://getx.topsandtees.space/downloader

class musicMaker():

    def __init__(self, root, pathwayToFolder):
        self.topLevel = tk.Toplevel(root)
        self.topLevel.title("Music Player")
        self.topLevel.protocol("WM_DELETE_WINDOW", self.destroy)

        # Song tracker
        self.current = 1

        # Initialization of pygame mixer
        pygame.init()
        pygame.mixer.init()    
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        # Sets up the pathway
        self.pathwayToFolder = pathwayToFolder
        self.listOfSongs = os.listdir(pathwayToFolder)
        shuffle(self.listOfSongs) # Randomizes songs order

        # Sets up the first two songs
        pygame.mixer.music.set_volume(0.2) # Sets the volume a bit quieter (really loud otherwise)
        pygame.mixer.music.load(os.path.join(self.pathwayToFolder, self.listOfSongs[0]))
        pygame.mixer.music.play()
        pygame.mixer.music.queue(os.path.join(self.pathwayToFolder, self.listOfSongs[1]))

        # Sets up nessecary buttons
        self.pauseButton = tk.Button(self.topLevel, font = "Futura 16", text="Pause",
                        relief = tk.RAISED, bd = 2, command=self.pause)
        self.pauseButton.grid(row = 0, column=0, padx = 5, pady = 5)

        self.nextButton = tk.Button(self.topLevel, font = "Futura 16", text="Next Song",
                        relief = tk.RAISED, bd = 2, command=self.skip)
        self.nextButton.grid(row = 1, column=0, padx = 5, pady = 5)

        instructions = tk.Label(self.topLevel, font = "Futura 16", text=
        """Control current song being played here. \n
        Feel free to close this window if you're not a fan of Glass Animals.""",
                        relief = tk.RAISED, bd = 2, justify="center")
        instructions.grid(row = 1, column=1, padx = 5, pady = 5)

        self.currentSongName = tk.Label(self.topLevel, font = "Futura 16", text = "Loading songs...",
                        relief = tk.RAISED, bd = 2)
        self.currentSongName.grid(row = 0, column=1, padx = 5, pady = 5)

        # Changes the label to match the current song being played
        self.updateSongName()

        # Starts the loop for checking if a song is finished, then queueing up the next one if it is
        self.check_event()


    def updateSongName(self):
        self.currentSongName["text"] = "Current song: " + self.listOfSongs[self.current - 1][0:len(self.listOfSongs[self.current - 1]) - 16].replace("_", " ")
        self.topLevel.update()


    def pause(self):
        pygame.mixer.music.pause()
        self.pauseButton["text"] = "Play"
        self.pauseButton["command"] = self.unpause


    def unpause(self):
        pygame.mixer.music.unpause()
        self.pauseButton["text"] = "Pause"
        self.pauseButton["command"] = self.pause


    def destroy(self):
        """Closes the program pygame and toplevel widget without affecting the main root."""
        pygame.quit()
        self.topLevel.destroy()


    def check_event(self):
        """Continuous loop that checks if the song has finished, then queues up the next song."""
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                self.queueSong()

        self.topLevel.after(500, self.check_event)

    def skip(self):
        self.nextButton["state"] = "disabled" # Temporarily disables button until everything is queued up and good to go
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(self.pathwayToFolder, self.listOfSongs[self.current])) # Reloads the other song as the new one
        pygame.mixer.music.play()
        self.nextButton["state"] = "normal"


    def queueSong(self):
        """If we've already gone through the entire list, randomizes the list of songs again. Updates the current song tracker, and queues up the next song."""
        self.current += 1
        # Loops back to beginning
        if self.current == len(self.listOfSongs):
            self.current = 0
            shuffle(self.listOfSongs) # Everytime the user has looped through once, randomizes song list again
        
        self.updateSongName()
            
        pygame.mixer.music.queue(os.path.join(self.pathwayToFolder, self.listOfSongs[self.current]))




# --- main ---


root = tk.Tk()

folder = os.path.join(os.path.dirname(__file__), 'songs')

musicMaker(root, folder)

root.mainloop()


# time.sleep(300)
# print("Finished") # DOESN'T WORK

# 16