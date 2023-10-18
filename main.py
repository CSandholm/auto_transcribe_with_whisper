import json
import schedule

from procedures import TranscribeAudioProcedure
from Config_Logger import logger
from Config_Logger.logger import logging
from priority_handler import set_priority

def main():

    with open("config.json", "r") as f:
        config = json.load(f)

    #Call logger configuration
    logger.config_logger()
    print("Start application")
    logging.info("Assigning config variables")
    path_to_customer_folders = config.get("path_to_customer_folders")
    model_name = config.get("model_name")
    transcribe_timer = int(config.get("transcribe_timer"))
    log_reset_time = config.get("log_reset_time")
    logging.info("/Assigning config variables")
    print("Check folders")
    logging.info("Check folder")
    logging.info(f"{path_to_customer_folders}")
    print("Start transcribe procedure")
    transcribe = TranscribeAudioProcedure(model_name, path_to_customer_folders)
    transcribe.transcribe_audio()
    print("Schedule timer")
    #Check for audio files in path directory every 5 minutes.
    schedule.every(transcribe_timer).minutes.do(transcribe.transcribe_check)
    print("Schedule log rotation")
    #Start writing logs in a new logging file
    schedule.every().day.at(log_reset_time).do(logger.config_logger)
    print("Initiate schedule to run")

    while True:
        #As long as schedules are pending the application won't stop running
        schedule.run_pending()

    # logger.logging("Finished")


if __name__ == "__main__":
    set_priority()
    main()


