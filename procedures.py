import whisper
import os
import datetime
from os import walk
from Config_Logger.logger import logging

class Transcribe_Audio_Procedure:
    def __init__(self, model_name, path):
        logging.info("Transcribe Audio Procedure __Init__")
        self.model_name = model_name
        self.model = whisper.load_model(self.model_name, download_root='models')
        self.isRunning = False
        self.path = path
        self.valid_audio_sources = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
        logging.info("/Transcribe Audio Procedure __Init__")

    def transcribe_audio(self):

        self.isRunning = True

        starttime = datetime.datetime.now().strftime("%H:%M:%S")
        logging.info(f"Start check for files in directories ({starttime})")
        for root, dirs, files in walk(self.path):
            if 'directory' in dirs:
                dirs.remove('directory')
            if '.ipynb_checkpoints' in dirs:
                dirs.remove('.ipynb_checkpoints') #Exclusive for test in jupyter notebook/lab
            if 'archive' in dirs:
                dirs.remove('archive')
            for filename in files:

                if any(filename.endswith(ext) for ext in self.valid_audio_sources):
                    logging.info(f"Found {filename}")
                    current_dir = os.getcwd()
                    logging.info(f"Found file {current_dir}/{filename}")
                    file_path = os.path.join(root, filename)
                    try:
                        logging.info("Start transcribe of file.")
                        result = self.model.transcribe(file_path, language="sv", fp16=False, verbose=True)
                        logging.info(f"{filename} transcribed.")
                        new_file_name = "/transcribed_" + filename.rsplit(".",1)[0]

                        logging.info(f"Create output file {root+new_file_name}.txt")
                        with open(root+new_file_name + ".txt", "w") as f:
                            f.write(result["text"])
                            f.close()

                        if os.path.exists(f"{root}/archive"):
                            continue
                        else:
                            os.makedirs(f"{root}/archive")
                            logging.info(f"made new archive directory in: {root}")

                        logging.info("Move original file to archive")
                        os.rename(file_path, root+"/archive/"+filename)
                    except Exception as e:
                        logging.error(f"{e}")

        logging.info(f"Finished checking for files ({starttime})")
        self.isRunning = False

    def transcribe_check(self):
        if self.isRunning is False:
            self.transcribe_audio()
        else:
            logging.info("Already Running. Trying again in 5 min.")
