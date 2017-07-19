from threading import Thread, Semaphore
from peyetribe import EyeTribe
import csv

import sys
import time

INTERVAL = 10

class EyeTribeThread(Thread):

    def __init__(self, workerSemaphore, processorSemaphore):
        super(EyeTribeThread, self).__init__()
        self.closeThread = False


    def run(self):

        # tracker = EyeTribe()
        # tracker.connect()
        # n = tracker.next()
        # tracker.pushmode()
        #
        print("eT;dT;aT;Fix;State;Rwx;Rwy;Avx;Avy;LRwx;LRwy;LAvx;LAvy;LPSz;LCx;LCy;RRwx;RRwy;RAvx;RAvy;RPSz;RCx;RCy")

        while True:
                if self.closeThread == True:
                    print("Thread Closed")
                    break
                time.sleep(1)
                # n = tracker.next()
                # print(n)



