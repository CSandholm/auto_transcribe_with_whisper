import whisper
import os
from os import walk

model = whisper.load_model("tiny")
valid_audio_sources = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

def transcribe_audio(path):
    for root, dirs, files in walk(path):
        if 'directory' in dirs:
            dirs.remove('directory')
        if '.ipynb_checkpoints' in dirs:
            dirs.remove('.ipynb_checkpoints')
        if 'archive' in dirs:
            dirs.remove('archive')
        for filename in files:
            if any(filename.endswith(ext) for ext in valid_audio_sources):
                file_path = os.path.join(root, filename)
                result = model.transcribe(file_path, language="sv", fp16=False, verbose=True)
                new_file_name = "/transcribed_" + filename.rsplit(".",1)[0]

                with open(root+new_file_name + ".txt", "w") as f:
                    f.write(result["text"])
                    f.close()

                os.rename(file_path, root+"/archive/"+filename)
