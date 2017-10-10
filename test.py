# This Python file uses the following encoding: utf-8

from logWatcher import LogWatcher
import time

# def callback(source, message):
#     print('{0}: {1}'.format(source, message))
def callback(filename, lines):
    for line in lines:
        print('{0}: {1}'.format(filename, line))

watcher = LogWatcher('upos', callback)

while 1:
    watcher.loop(blocking=False)
    time.sleep(0.1)
