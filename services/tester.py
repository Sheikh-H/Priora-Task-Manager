from datetime import datetime, timedelta

now = datetime.now().replace(microsecond=0)

time = now.time().replace(second=0)
print(time)
