from time import sleep
import logging
import f

class LongPrintable:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        sleep(10.0)
        return str(self.data)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

number = LongPrintable(33)
logging.info(f('{number} kittens drink milk'))
