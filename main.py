import json
import schedule

from procedures import Transcribe_Audio_Procedure
from Config_Logger import logger

def main():

    with open("config.json", "r") as f:
        config = json.load(f)

    path_to_customer_folders = config.get("path_to_customer_folders")
    model_name = config.get("model_name")
    transcribe_timer = int(config.get("transcribe_timer"))
    log_reset_time = config.get("log_reset_time")

    #Call logger configuration
    logger.config_logger()

    transcribe = Transcribe_Audio_Procedure(model_name, path_to_customer_folders)
    transcribe.transcribe_audio()

    #Check for audio files in path directory every 5 minutes.
    schedule.every(transcribe_timer).minutes.do(transcribe.transcribe_audio)

    #Start writing logs in a new logging file
    schedule.every().day.at(log_reset_time).do(logger.config_logger)

    while True:
        #As long as schedules are pending the application won't stop running
        schedule.run_pending()

if __name__ == "__main__":
    main()
