"""
Usage: python3 setup.py py2app
"""

from setuptools import setup
import os

# Create list of songs in the folder titled song
listOfSongs = []
folderName = os.path.join(os.path.dirname(__file__), 'songs')
for songName in os.listdir(folderName):
    listOfSongs.append(os.path.join(folderName, songName))


APP = ['ELLIEPROJECT.py']
DATA_FILES = [
    ('songs', listOfSongs) # Then takes each song and puts it in the resource folder under the title songs folder
    ]
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)