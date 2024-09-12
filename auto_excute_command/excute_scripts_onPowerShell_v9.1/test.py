from datetime import datetime
import time


TIMES = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
print(TIMES)
print(TIMES[11:])