import time
from procedures import transcribe_audio

path = "C:/Users/CharlesSandholm/Documents/Charles Sandholm/Jupyter/S2TApplication/testfolder"

def main():
    while True:
        transcribe_audio(path)
        time.sleep(300)

main()
