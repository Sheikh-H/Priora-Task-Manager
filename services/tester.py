from datetime import datetime, timedelta

now = datetime.now().replace(microsecond=0).date()

print(now + timedelta(days=9))
