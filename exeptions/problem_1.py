import datetime
import pytz

tday = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'))
print(tday.strftime('%b%d %H:%M %p'))
