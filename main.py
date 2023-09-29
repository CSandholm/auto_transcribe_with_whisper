import schedule
from procedures import Transcribe_Audio_Procedure
from Config_Logger import logger

def main():

    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            key, value = line.strip().split(' = ')
            config[key] = value

    path_to_customer_folders = config.get("path_to_customer_folders")
    model_name = config.get("model_name")

    #Call logger configuration
    logger.config_logger()

    transcribe = Transcribe_Audio_Procedure(model_name, path_to_customer_folders)
    transcribe.transcribe_audio()

    #Check for audio files in path directory every 5 minutes.
    schedule.every(5).minutes.do(transcribe.transcribe_audio)

    #Start writing logs in a new logging file
    schedule.every().day.at("00:00").do(logger.config_logger)

    while True:
        #As long as schedules are pending the application won't stop running
        schedule.run_pending()

if __name__ == "__main__":
    main()
