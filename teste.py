from datetime import datetime, timedelta

now = datetime.now()
fut = now + timedelta(minutes=5)

print(now.timestamp())
print(fut.timestamp())
