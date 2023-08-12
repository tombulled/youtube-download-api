import random
import time

from ytd_api.api import get_channel_singles


def delay() -> None:
    timeout: float = random.randint(2000, 5000) / 1000

    time.sleep(timeout)


channel_id: str = "UC8Yu1_yfN5qPh601Y4btsYw"  # Arctic Monkeys

d = get_channel_singles(channel_id)
