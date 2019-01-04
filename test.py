import time

print(time.strftime("%Y%m%d%H%M%S", time.gmtime()))

import datetime
x= datetime.datetime.now()
y = x + datetime.timedelta(0,3600)
print(x.strftime("%Y%m%d%H%M%S"))
print(y.strftime("%Y%m%d%H%M%S"))
