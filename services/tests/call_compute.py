from __future__ import absolute_import

import time

from services.compute.compute import add

# delay() is a shortcut to apply_async(). Calling a task returns an AsyncResult
# instance, which can be used to check the state of the task, wait for the task
# to finish or get its returned value (or if the task failed, the exception and
# traceback)
result = add.delay(3, 4)

counter = 0
while counter < 3:
    if result.ready():
        print(result.result)
        counter = 3
    else:
        print('Waiting for 3 seconds...')
        time.sleep(3)
        counter += 1

