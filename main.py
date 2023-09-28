import schedule

from procedures import transcribe_audio
from Logger import logger

def main():

    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            key, value = line.strip().split(' = ')
            config[key] = value

    path = config.get("path_to_customer_folders")

    #Call logger configuration
    logger.config_logger()

    transcribe_audio(path)

    #Check for audio files in path directory every 5 minutes.
    schedule.every(5).minutes.do(transcribe_audio, path)

    #Start writing logs in a new logging file
    schedule.every().day.at("00:00").do(logger.config_logger)

    while True:
        #As long as schedules are pending the application won't stop running
        schedule.run_pending()

main()

