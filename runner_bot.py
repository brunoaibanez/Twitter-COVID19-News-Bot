from telegram_bot import run_telegram
from api_twitter import run_api_twitter
from reader_spark_streaming import run_spark
import time


def run_bot():
    run_telegram()
    run_api_twitter()

    time.sleep(2)
    run_spark()


if __name__ == "__main__":
    run_bot()




