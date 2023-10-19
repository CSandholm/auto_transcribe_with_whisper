import whisper
import os
import datetime
from os import walk
from Config_Logger.logger import logging


class TranscribeAudioProcedure:
    def __init__(self, model_name, path, models_path):
        logging.info("Transcribe Audio Procedure __Init__")
        self.model_name = model_name
        self.model = whisper.load_model(self.model_name, download_root=models_path)  # '../Models' in staging
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
                dirs.remove('.ipynb_checkpoints')  # Exclusive for test in jupyter notebook/lab
            if 'archive' in dirs:
                dirs.remove('archive')
            for filename in files:

                if any(filename.endswith(ext) for ext in self.valid_audio_sources):
                    logging.info(f"Found {filename}")
                    current_dir = os.getcwd()
                    logging.info(f"Found file {current_dir}/{filename}")
                    file_path = os.path.join(root, filename)
                    new_file_name = "/transcribed_" + filename.rsplit(".", 1)[0]

                    # Check if a transcribed .txt file already exists. Continue if it does.
                    if os.path.exists(f"{root}{new_file_name}.txt"):
                        logging.info("Transcribed .txt file already exists, or is under transcribe procedure.")
                        continue
                    else:
                        try:
                            logging.info("Start transcribe of file.")

                            result = self.transcribe(file_path)

                            # result = self.model.transcribe(audio, language="sv", fp16=False, verbose=True)
                            logging.info(f"{filename} transcribed.")
                            logging.info(f"Create output file {root+new_file_name}.txt")
                            with open(root+new_file_name + ".txt", "w") as f:
                                f.write(result)
                                f.close()
                            # Create an archive folder if it does not exist
                            if os.path.exists(f"{root}/archive") is False:
                                os.makedirs(f"{root}/archive")
                                logging.info(f"Created new archive directory in: {root}")

                            logging.info(f"Move original audio file to archive: {root}+/archive")
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

    def trim_audio(self, _file_path):

        logging.info("Trim audio.")
        # load audio and pad/trim it to 30 seconds
        audio = whisper.load_audio(_file_path)
        audio = whisper.pad_or_trim(audio)

        return audio

    def transcribe(self, _file_path):

        audio = self.trim_audio(_file_path)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # might want to implement detect the spoken language at some time, like so:
        # _, probs = self.model.detect_language(mel)
        # logging.info(f"Detected language: {max(probs, key=probs.get)}")

        # decode audio
        options = whisper.DecodingOptions(fp16=False, language="sv")
        result = whisper.decode(self.model, mel, options)

        return result.text
