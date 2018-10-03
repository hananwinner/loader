import threading
import time
import logging


class RepeatedTimer(threading.Thread):
    def __init__(self, operation, interval_sec, stop_event=None, start_immediately=False, log=None):
        threading.Thread.__init__(self)
        self._operation = operation
        self._delay_sec = interval_sec
        self._stop_event = stop_event
        self._start_immediately = start_immediately
        self._log = log or logging.getLogger('dummy')

    def run(self):
        if self._start_immediately:
            self._operation()
            self._start_immediately = False

        while True:
            if self._stop_event is None:
                time.sleep(self._delay_sec)
            else:
                if self._stop_event.wait(self._delay_sec):
                    break
            self._operation()
