import time
import random
from src import sha3


def get_public_key() -> str:
    time.sleep(0.5)
    random.seed(time.time())
    seed: str = str(random.randint(-2**64, 2*64))+str(time.time())
    public_key: str = sha3.sha3_256(seed)
    return public_key
